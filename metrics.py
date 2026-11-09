"""Classification, calibration and agreement metrics with bootstrap confidence intervals."""
import numpy as np
from sklearn.metrics import (accuracy_score, balanced_accuracy_score, cohen_kappa_score, f1_score,
                             recall_score, roc_auc_score)


def ece(p, y, bins=15):
    conf, pred = p.max(1), p.argmax(1)
    edges = np.linspace(0, 1, bins + 1)
    e = 0.0
    for lo, hi in zip(edges[:-1], edges[1:]):
        m = (conf > lo) & (conf <= hi)
        if m.any():
            e += m.mean() * abs((pred[m] == y[m]).mean() - conf[m].mean())
    return float(e)


def metrics(p, y):
    pred = p.argmax(1)
    oh = np.eye(5)[y]
    out = {"acc": accuracy_score(y, pred), "bal_acc": balanced_accuracy_score(y, pred),
           "macro_f1": f1_score(y, pred, average="macro", labels=range(5), zero_division=0),
           "qwk": cohen_kappa_score(y, pred, weights="quadratic", labels=range(5)),
           "ece": ece(p, y), "nll": float(-np.log(np.clip(p[np.arange(len(y)), y], 1e-12, 1)).mean()),
           "brier": float(((p - oh) ** 2).sum(1).mean())}
    rec = recall_score(y, pred, average=None, labels=range(5), zero_division=0)
    out.update({f"recall_{k}": float(r) for k, r in enumerate(rec)})
    # Referable DR (grade >= 2) screening view
    pr = p[:, 2:].sum(1)
    out["referable_auc"] = roc_auc_score(y >= 2, pr) if 0 < (y >= 2).mean() < 1 else np.nan
    return {k: float(v) for k, v in out.items()}


def bootstrap_ci(p, y, keys=("qwk", "macro_f1", "bal_acc"), n=1000, seed=0):
    rng = np.random.default_rng(seed)
    vals = {k: [] for k in keys}
    for _ in range(n):
        i = rng.integers(0, len(y), len(y))
        m = metrics(p[i], y[i])
        for k in keys:
            vals[k].append(m[k])
    return {k: (float(np.percentile(v, 2.5)), float(np.percentile(v, 97.5))) for k, v in vals.items()}


def paired_bootstrap(pa, pb, y, key="qwk", n=1000, seed=0):
    """Distribution of metric(a) - metric(b) on shared resamples; returns mean diff, 95% CI, P(diff<=0)."""
    rng = np.random.default_rng(seed)
    d = []
    for _ in range(n):
        i = rng.integers(0, len(y), len(y))
        d.append(metrics(pa[i], y[i])[key] - metrics(pb[i], y[i])[key])
    d = np.array(d)
    return float(d.mean()), (float(np.percentile(d, 2.5)), float(np.percentile(d, 97.5))), float((d <= 0).mean())
