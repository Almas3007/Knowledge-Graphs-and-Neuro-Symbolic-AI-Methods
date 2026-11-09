"""Cohort loading on top of cached frozen embeddings.

Internal cohort: MVLM04 Stage-5 frozen manifest (Public-DR-v1: DDR, APTOS, Messidor-2, IDRiD) with its
leakage-aware, group-disjoint train/val/test split (exact SHA-256 and perceptual-hash duplicates grouped,
conflicting-label groups quarantined). The 43 DeepDRiD images that Stage 5 contained are dropped so
DeepDRiD stays a fully external cohort.
External cohorts: FDR26 (3,000 images) and DeepDRiD regular fundus (1,589 images, 399 patients).
"""
import numpy as np
import pandas as pd

from config import EMB_DIM, ENCODERS, FDR26_META, FEAT_CACHE, FEATURES, STAGE5_MANIFEST

DUP_COS = 0.98   # external image this close to a training image is treated as a possible duplicate


def _norm(X):
    X = X[:, :EMB_DIM].astype(np.float32)
    return X / np.linalg.norm(X, axis=1, keepdims=True)


def load_internal(encoder):
    z = np.load(FEAT_CACHE / ENCODERS[encoder] / "stage5.npz")
    man = pd.read_csv(STAGE5_MANIFEST)
    assert len(man) == len(z["X"]) and (man.path.astype(str).values == z["keys"]).all()
    keep = (man.source != "DeepDRiD-master").values
    man = man[keep].reset_index(drop=True)
    X = _norm(z["X"][keep])
    meta = pd.DataFrame({"key": man.stem, "source": man.source_dataset, "split": man.split,
                         "group": man.leakage_group})
    return X, man.grade.astype(int).values, meta


def load_external(encoder, name):
    if name == "fdr26":
        z = np.load(FEAT_CACHE / ENCODERS[encoder] / "fdr26.npz")
        # NOTE: MVLM04 keeps FDR26 labels sealed for its gated Stage-15 evaluation. This branch only runs
        # when run_experiments.py is given --external fdr26 explicitly.
        lab = pd.read_csv(FDR26_META).set_index("image_id")["classe"]
        keys = z["keys"].astype(str)
        have = np.isin(keys, lab.index)      # one image file has no metadata row; it is dropped
        keys = keys[have]
        y = lab.loc[keys].astype(int).values
        meta = pd.DataFrame({"key": keys, "source": "fdr26", "split": "external"})
        return _norm(z["X"][have]), y, meta
    elif name == "deepdrid":
        z = np.load(FEATURES / f"deepdrid_{encoder}.npz")
        man = pd.read_csv(FEATURES / "deepdrid_manifest.csv")
        assert (man.key.astype(str).values == z["keys"]).all()
        y = man.grade.astype(int).values
        meta = pd.DataFrame({"key": man.key, "source": "deepdrid", "split": "external",
                             "patient": man.patient, "path": man.path})
    else:
        raise ValueError(name)
    return _norm(z["X"]), y, meta


def duplicate_mask(X_ext, X_train, thr=DUP_COS, block=2048):
    """True where an external image has cosine >= thr to some training image (possible cross-cohort duplicate)."""
    mx = np.zeros(len(X_ext), dtype=np.float32)
    for s in range(0, len(X_ext), block):
        mx[s:s + block] = (X_ext[s:s + block] @ X_train.T).max(1)
    return mx >= thr, mx
