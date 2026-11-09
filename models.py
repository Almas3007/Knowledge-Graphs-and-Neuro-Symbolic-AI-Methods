"""Neural, concept and neuro-symbolic heads trained on frozen image embeddings."""
import copy

import numpy as np
import torch
import torch.nn as nn
import torch.nn.functional as F
from sklearn.metrics import cohen_kappa_score, f1_score

from reasoner import KGReasoner


class NeuralHead(nn.Module):
    """Conventional deep-learning baseline: MLP on the frozen encoder embedding."""

    def __init__(self, d=512, h=256, p=0.2):
        super().__init__()
        self.net = nn.Sequential(nn.Linear(d, h), nn.GELU(), nn.Dropout(p), nn.Linear(h, 5))

    def forward(self, x):
        return F.log_softmax(self.net(x), dim=1)


class ConceptHead(nn.Module):
    """Text-anchored lesion detectors.

    logit_c(x) = softplus(a_c) * z_c(x) + b_c + w_c . x
    z_c is the standardised zero-shot score cos(x, t_c) - cos(x, t_neutral) from the encoder's text tower,
    so each detector starts from the language model's notion of the lesion; softplus keeps that link
    monotone. residual=False gives an 18-parameter detector bank (pure text grounding)."""

    def __init__(self, T, N, mu, sd, residual=True):
        super().__init__()
        self.register_buffer("T", torch.tensor(T))
        self.register_buffer("N", torch.tensor(N))
        self.register_buffer("mu", torch.tensor(mu))
        self.register_buffer("sd", torch.tensor(sd))
        k = len(T)
        self.a = nn.Parameter(torch.full((k,), 0.5413))   # softplus(0.5413) = 1
        self.b = nn.Parameter(torch.zeros(k))
        self.W = nn.Linear(T.shape[1], k, bias=False) if residual else None
        if self.W is not None:
            nn.init.zeros_(self.W.weight)

    def zero_shot(self, x):
        return ((x @ self.T.T - (x @ self.N)[:, None]) - self.mu) / self.sd

    def forward(self, x):
        logit = F.softplus(self.a) * self.zero_shot(x) + self.b
        if self.W is not None:
            logit = logit + self.W(x)
        return logit

    def penalty(self):
        return 0.0 if self.W is None else (self.W.weight ** 2).sum()


class KGSymbolic(nn.Module):
    """Concepts -> DR-KG reasoner. Prediction is entirely rule-derived."""

    def __init__(self, concept_head, reasoner: KGReasoner, gamma=1e-3):
        super().__init__()
        self.ch, self.r, self.gamma = concept_head, reasoner, gamma

    def concepts(self, x):
        return torch.sigmoid(self.ch(x))

    def forward(self, x):
        return torch.log(self.r.grade_probs(self.concepts(x)))

    def penalty(self):
        return self.gamma * self.ch.penalty()


class CBMHead(nn.Module):
    """Knowledge-guided concept bottleneck: frozen KG-trained concepts -> learned linear map (no rules)."""

    def __init__(self, sym: KGSymbolic):
        super().__init__()
        self.sym = sym
        for p in self.sym.parameters():
            p.requires_grad_(False)
        self.lin = nn.Linear(len(sym.r.concepts), 5)

    def forward(self, x):
        with torch.no_grad():
            logit = self.sym.ch(x)
        return F.log_softmax(self.lin(logit), dim=1)


class NSJoint(nn.Module):
    """Jointly trained neuro-symbolic model: log p = log_softmax(neural logits + lam * log P_KG(q(x))).
    Trained with NLL(fused) + mu * NLL(symbolic) so the concept branch must explain the grade on its own."""

    def __init__(self, neural: NeuralHead, sym: KGSymbolic, lam=1.0, mu=1.0):
        super().__init__()
        self.nn, self.sym, self.lam, self.mu = neural, sym, lam, mu

    def parts(self, x):
        ln = self.nn.net(x)
        ls = self.sym(x)
        return F.log_softmax(ln + self.lam * ls, dim=1), F.log_softmax(ln, dim=1), ls

    def forward(self, x):
        return self.parts(x)[0]

    def aux_loss(self, x, y, w):
        return self.mu * F.nll_loss(self.sym(x), y, weight=w)

    def penalty(self):
        return self.sym.penalty()


def class_weights(y, power=0.5):
    c = np.bincount(y, minlength=5).astype(np.float64)
    w = (c.sum() / np.maximum(c, 1)) ** power
    return torch.tensor(w / w.mean(), dtype=torch.float32)


def val_score(logp, y):
    pred = logp.argmax(1)
    return 0.5 * (cohen_kappa_score(y, pred, weights="quadratic") + f1_score(y, pred, average="macro"))


def fit(model, Xtr, ytr, Xva, yva, seed, lr=1e-3, wd=1e-4, epochs=200, batch=512, patience=20):
    torch.manual_seed(seed)
    w = class_weights(ytr)
    Xt, yt = torch.tensor(Xtr), torch.tensor(ytr)
    Xv = torch.tensor(Xva)
    params = [p for p in model.parameters() if p.requires_grad]
    opt = torch.optim.AdamW(params, lr=lr, weight_decay=wd)
    best, best_state, bad = -np.inf, None, 0
    g = torch.Generator().manual_seed(seed)
    for ep in range(epochs):
        model.train()
        for idx in torch.randperm(len(yt), generator=g).split(batch):
            loss = F.nll_loss(model(Xt[idx]), yt[idx], weight=w)
            if hasattr(model, "aux_loss"):
                loss = loss + model.aux_loss(Xt[idx], yt[idx], w)
            if hasattr(model, "penalty"):
                loss = loss + model.penalty()
            opt.zero_grad()
            loss.backward()
            opt.step()
        model.eval()
        with torch.no_grad():
            s = val_score(model(Xv).numpy(), yva)
        if s > best + 1e-4:
            best, best_state, bad = s, copy.deepcopy(model.state_dict()), 0
        else:
            bad += 1
            if bad >= patience:
                break
    model.load_state_dict(best_state)
    model.eval()
    return model, {"best_val_score": float(best), "epochs": ep + 1}


def fit_temperature(logp_val, yva):
    """Post-hoc temperature scaling on validation (affects calibration only, never the argmax)."""
    lv, yv = torch.tensor(logp_val), torch.tensor(yva)
    t = torch.zeros((), requires_grad=True)
    opt = torch.optim.LBFGS([t], lr=0.1, max_iter=100)

    def closure():
        opt.zero_grad()
        loss = F.nll_loss(F.log_softmax(lv / t.exp(), 1), yv)
        loss.backward()
        return loss

    opt.step(closure)
    return float(t.detach().exp())


def apply_temperature(logp, T):
    return F.log_softmax(torch.tensor(logp) / T, 1).numpy()
