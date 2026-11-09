"""Train and evaluate every model on the internal and external cohorts.

Models (all on the same frozen embedding):
  ZS-Grade   zero-shot grade prompts (no training except a temperature)
  NN         conventional deep-learning head (MLP)                          -- neural only
  CBM-KG     KG-weakly-supervised concepts -> learned linear map           -- knowledge-guided learning
  KG-Sym-T   18-parameter text-grounded concepts -> DR-KG reasoner          -- symbolic only
  KG-Sym     text-anchored + residual concepts -> DR-KG reasoner            -- symbolic only
  NS-Fuse    product of experts: NN (calibrated) x KG-Sym^lambda, lambda tuned on validation
  NS-Fuse-T  same with the text-grounded KG-Sym-T expert (added post hoc, see README)
  NS-Joint   neural + symbolic branches trained jointly through the fused likelihood

  python3 src/run_experiments.py --encoders flair biomedclip --seeds 0 1 2 3 4
"""
import argparse
import json
import time

import numpy as np
import pandas as pd
import torch
import torch.nn.functional as F
from sklearn.metrics import roc_auc_score

from config import FEATURES, GRADES, RESULTS, SEED
from data import duplicate_mask, load_external, load_internal
from metrics import bootstrap_ci, metrics, paired_bootstrap
from models import (CBMHead, ConceptHead, KGSymbolic, NeuralHead, NSJoint, apply_temperature, fit,
                    fit_temperature, val_score)
from reasoner import KGReasoner

torch.set_num_threads(4)
R = KGReasoner()
MODELS = ["ZS-Grade", "NN", "CBM-KG", "KG-Sym-T", "KG-Sym", "NS-Fuse", "NS-Fuse-T", "NS-Joint"]
CONCEPT_MODELS = ["CBM-KG", "KG-Sym-T", "KG-Sym", "NS-Fuse", "NS-Fuse-T", "NS-Joint"]
# Fusion variant -> symbolic expert. NS-Fuse-T was added after the first DeepDRiD evaluation (post hoc).
FUSION = {"NS-Fuse": "KG-Sym", "NS-Fuse-T": "KG-Sym-T"}
EPS = 1e-4  # "lesion absent" value used when deleting a concept


def t(x):
    return torch.tensor(x)


def concept_fn(name, m, aux):
    """Returns (q(x), f(q, x) -> grade probs) so explanations can be perturbed in concept space."""
    if name in ("KG-Sym", "KG-Sym-T"):
        return (lambda X: m.concepts(t(X)).numpy(),
                lambda q, X: R.grade_probs(t(q)).numpy())
    if name == "CBM-KG":
        return (lambda X: m.sym.concepts(t(X)).numpy(),
                lambda q, X: F.softmax(m.lin(torch.logit(t(q).clamp(EPS, 1 - EPS))), 1).detach().numpy())
    if name in FUSION:
        nn_m, sym, T, lam = aux
        return (lambda X: sym.concepts(t(X)).numpy(),
                lambda q, X: F.softmax(nn_m(t(X)) / T + lam * torch.log(R.grade_probs(t(q))), 1).numpy())
    if name == "NS-Joint":
        return (lambda X: m.sym.concepts(t(X)).numpy(),
                lambda q, X: F.softmax(m.nn.net(t(X)) + m.lam * torch.log(R.grade_probs(t(q))), 1).numpy())
    raise ValueError(name)


def cited(name, m, q, k):
    """Concepts the model's explanation cites for grade k."""
    if k == 0:
        return []
    if name == "CBM-KG":
        contrib = m.lin.weight[k].detach().numpy() * np.log(np.clip(q, EPS, 1 - EPS) / np.clip(1 - q, EPS, 1))
        n = len(R.explain(q, k))
        return list(np.argsort(-contrib)[:n])
    return R.explain(q, k)


def faithfulness(name, m, aux, X, rng):
    qf, f = concept_fn(name, m, aux)
    with torch.no_grad():
        q = qf(X)
        p = f(q, X)
    k = p.argmax(1)
    rows = []
    qd, qr = q.copy(), q.copy()
    keep = np.zeros(len(X), bool)
    for i in range(len(X)):
        E = cited(name, m, q[i], k[i])
        if not E:
            continue
        keep[i] = True
        others = [c for c in range(q.shape[1]) if c not in E]
        Rnd = rng.choice(others, size=len(E), replace=False)
        qd[i, E] = EPS
        qr[i, Rnd] = EPS
    with torch.no_grad():
        pd_, pr_ = f(qd, X), f(qr, X)
    idx = np.where(keep)[0]
    pk = p[idx, k[idx]]
    rows = {"n_explained": int(len(idx)),
            "comprehensiveness": float((pk - pd_[idx, k[idx]]).mean()),
            "comprehensiveness_random": float((pk - pr_[idx, k[idx]]).mean()),
            "flip_rate": float((pd_[idx].argmax(1) != k[idx]).mean()),
            "flip_rate_random": float((pr_[idx].argmax(1) != k[idx]).mean())}
    return rows


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--encoders", nargs="+", default=["flair", "biomedclip"])
    ap.add_argument("--seeds", nargs="+", type=int, default=[0, 1, 2, 3, 4])
    ap.add_argument("--external", nargs="+", default=["deepdrid"], choices=["deepdrid", "fdr26"],
                    help="fdr26 labels are sealed by the MVLM04 Stage-15 protocol; add it only deliberately")
    a = ap.parse_args()
    RESULTS.mkdir(parents=True, exist_ok=True)
    (RESULTS / "preds").mkdir(exist_ok=True)
    (RESULTS / "models").mkdir(exist_ok=True)
    rows, faith, cons, cohort_info, zs_auc, per_source, cis, paired = [], [], [], [], [], [], [], []
    for enc in a.encoders:
        t0 = time.time()
        X, y, meta = load_internal(enc)
        sp = meta.split.values
        tr, va, te = sp == "train", sp == "val", sp == "test"
        cohorts = {"internal_test": (X[te], y[te], meta[te].reset_index(drop=True))}
        for name in a.external:
            Xe, ye, me = load_external(enc, name)
            dup, mx = duplicate_mask(Xe, X[tr])
            cohort_info.append({"encoder": enc, "cohort": name, "n_total": len(ye), "n_possible_duplicates": int(dup.sum()),
                                "max_cos_to_train_median": float(np.median(mx)), "n_used": int((~dup).sum())})
            cohorts[name] = (Xe[~dup], ye[~dup], me[~dup].reset_index(drop=True))
        cohort_info.append({"encoder": enc, "cohort": "internal", "n_train": int(tr.sum()), "n_val": int(va.sum()),
                            "n_test": int(te.sum())})
        ct = np.load(FEATURES / f"concept_text_{enc}.npz")
        T, N, G = ct["T"], ct["neutral"], ct["grades"]
        z_tr = X[tr] @ T.T - (X[tr] @ N)[:, None]
        mu, sd = z_tr.mean(0).astype(np.float32), z_tr.std(0).astype(np.float32)

        # Zero-shot concept validity: never trained on labels. AUC of z_c for "grade >= level(c)".
        for cname, (Xc, yc, _) in cohorts.items():
            z = Xc @ T.T - (Xc @ N)[:, None]
            for ci, c in enumerate(R.concepts):
                L = R.level_of[ci]
                zs_auc.append({"encoder": enc, "cohort": cname, "concept": c, "level": L,
                               "auc_grade_ge_level": roc_auc_score(yc >= L, z[:, ci])})

        for seed in a.seeds:
            s = SEED + seed
            fitted, info = {}, {}
            fitted["NN"], info["NN"] = fit(NeuralHead(), X[tr], y[tr], X[va], y[va], s)
            fitted["KG-Sym"], info["KG-Sym"] = fit(KGSymbolic(ConceptHead(T, N, mu, sd, True), R), X[tr], y[tr],
                                                   X[va], y[va], s)
            fitted["KG-Sym-T"], info["KG-Sym-T"] = fit(KGSymbolic(ConceptHead(T, N, mu, sd, False), R), X[tr],
                                                       y[tr], X[va], y[va], s, lr=1e-2, wd=0.0)
            fitted["CBM-KG"], info["CBM-KG"] = fit(CBMHead(fitted["KG-Sym"]), X[tr], y[tr], X[va], y[va], s, lr=1e-2)
            fitted["NS-Joint"], info["NS-Joint"] = fit(NSJoint(NeuralHead(), KGSymbolic(ConceptHead(T, N, mu, sd, True), R)),
                                                       X[tr], y[tr], X[va], y[va], s)

            def logp(name, Xc):
                with torch.no_grad():
                    if name == "ZS-Grade":
                        return F.log_softmax(t(Xc @ G.T) * 100.0, 1).numpy()
                    return fitted[name](t(Xc)).numpy()

            temps = {m: fit_temperature(logp(m, X[va]), y[va]) for m in ["ZS-Grade"] + list(fitted)}
            # Product-of-experts fusion; lambda chosen on internal validation only
            l_nn_va = apply_temperature(logp("NN", X[va]), temps["NN"])
            grid = np.round(np.arange(0, 3.01, 0.25), 2)
            lams = {}
            for fm, expert in FUSION.items():
                l_sy_va = logp(expert, X[va])
                sc = [val_score(l_nn_va + lam * l_sy_va, y[va]) for lam in grid]
                lams[fm] = float(grid[int(np.argmax(sc))])
                info[fm] = {"expert": expert, "lambda": lams[fm], "best_val_score": float(max(sc))}

            def fuse(fm, Xc):
                return F.log_softmax(t(apply_temperature(logp("NN", Xc), temps["NN"]) +
                                       lams[fm] * logp(FUSION[fm], Xc)), 1).numpy()

            for fm in FUSION:
                temps[fm] = fit_temperature(fuse(fm, X[va]), y[va])

            def aux_of(m):
                return (fitted["NN"], fitted[FUSION[m]], temps["NN"], lams[m]) if m in FUSION else None
            rng = np.random.default_rng(s)
            for cname, (Xc, yc, mc) in cohorts.items():
                P = {}
                for m in MODELS:
                    lp = fuse(m, Xc) if m in FUSION else logp(m, Xc)
                    P[m] = np.exp(apply_temperature(lp, temps[m]))
                    rows.append({"encoder": enc, "seed": seed, "cohort": cname, "model": m, "n": len(yc),
                                 **metrics(P[m], yc)})
                # Rule consistency of every model against the same text-grounded concept evidence (KG-Sym-T)
                with torch.no_grad():
                    q_ref = fitted["KG-Sym-T"].concepts(t(Xc)).numpy()
                    ps_ref = R.grade_probs(t(q_ref)).numpy()
                for m in MODELS:
                    sup = ps_ref[np.arange(len(yc)), P[m].argmax(1)]
                    cons.append({"encoder": enc, "seed": seed, "cohort": cname, "model": m,
                                 "mean_kg_support": float(sup.mean()), "kg_violation_rate": float((sup < 0.05).mean())})
                for m in CONCEPT_MODELS:
                    aux = aux_of(m)
                    mod = fitted.get(m)
                    faith.append({"encoder": enc, "seed": seed, "cohort": cname, "model": m,
                                  **faithfulness(m, mod, aux, Xc, rng)})
                if seed == a.seeds[0]:
                    with torch.no_grad():
                        qs = {m: concept_fn(m, fitted.get(m), aux_of(m))[0](Xc) for m in ["KG-Sym", "KG-Sym-T", "NS-Joint"]}
                    np.savez_compressed(RESULTS / "preds" / f"{enc}_{cname}.npz", y=yc,
                                        **{f"p_{m}": P[m] for m in MODELS}, **{f"q_{m}": q for m, q in qs.items()},
                                        keys=mc.key.astype(str).values)
                    for m in ["NS-Fuse", "NS-Fuse-T", "NS-Joint", "KG-Sym-T", "KG-Sym", "NN", "ZS-Grade"]:
                        cis.append({"encoder": enc, "cohort": cname, "model": m,
                                    **{f"{k}_ci": v for k, v in bootstrap_ci(P[m], yc).items()}})
                    for m in ["NS-Fuse", "NS-Fuse-T", "NS-Joint", "KG-Sym-T"]:
                        for key in ["qwk", "macro_f1"]:
                            d, ci, pv = paired_bootstrap(P[m], P["NN"], yc, key)
                            paired.append({"encoder": enc, "cohort": cname, "model": m, "vs": "NN", "metric": key,
                                           "mean_diff": d, "ci_low": ci[0], "ci_high": ci[1], "p_one_sided": pv})
                    if cname == "internal_test":
                        for src in sorted(mc.source.unique()):
                            ii = (mc.source == src).values
                            for m in MODELS:
                                per_source.append({"encoder": enc, "source": src, "model": m, "n": int(ii.sum()),
                                                   **metrics(P[m][ii], yc[ii])})
            if seed == a.seeds[0]:
                for m, mod in fitted.items():
                    torch.save(mod.state_dict(), RESULTS / "models" / f"{enc}_{m}.pt")
                (RESULTS / "models" / f"{enc}_training_info.json").write_text(
                    json.dumps({"temperatures": temps, "info": info}, indent=2))
            print(f"[{enc}] seed {seed} done ({time.time() - t0:.0f}s) lambdas={lams}", flush=True)

    df = pd.DataFrame(rows)
    df.to_csv(RESULTS / "metrics_all_seeds.csv", index=False)
    keys = ["acc", "bal_acc", "macro_f1", "qwk", "ece", "nll", "brier", "referable_auc"] + [f"recall_{k}" for k in range(5)]
    agg = df.groupby(["encoder", "cohort", "model"])[keys].agg(["mean", "std"])
    agg.columns = [f"{k}_{s}" for k, s in agg.columns]
    agg.reset_index().to_csv(RESULTS / "summary_mean_sd.csv", index=False)
    pd.DataFrame(faith).groupby(["encoder", "cohort", "model"]).mean(numeric_only=True).drop(columns="seed") \
        .reset_index().to_csv(RESULTS / "faithfulness.csv", index=False)
    pd.DataFrame(cons).groupby(["encoder", "cohort", "model"]).mean(numeric_only=True).drop(columns="seed") \
        .reset_index().to_csv(RESULTS / "kg_consistency.csv", index=False)
    pd.DataFrame(cohort_info).to_csv(RESULTS / "cohorts.csv", index=False)
    pd.DataFrame(zs_auc).to_csv(RESULTS / "concept_zero_shot_auc.csv", index=False)
    pd.DataFrame(per_source).to_csv(RESULTS / "internal_per_source.csv", index=False)
    pd.DataFrame(cis).to_csv(RESULTS / "bootstrap_ci_seed0.csv", index=False)
    pd.DataFrame(paired).to_csv(RESULTS / "paired_vs_nn_seed0.csv", index=False)
    print("done")


if __name__ == "__main__":
    main()
