"""Paths and constants shared by every KGNS-DR script."""
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]          # KGNS_DR/
MVLM04 = ROOT.parent / "MVLM04"                       # existing data + cached features
FEAT_CACHE = MVLM04 / "features"                     # B1_biomedclip / B2_flair npz files
STAGE5_MANIFEST = MVLM04 / "stage5" / "frozen_manifest.csv"   # leakage-audited, group-disjoint split
FDR26_META = MVLM04 / "FDR26" / "metadata_classification_DR.csv"
DEEPDRID = MVLM04 / "DeepDRiD-master" / "regular_fundus_images"

FEATURES = ROOT / "features"     # new features computed here (DeepDRiD, concept text embeddings)
KG_DIR = ROOT / "kg"
RESULTS = ROOT / "results"
FIGURES = RESULTS / "figures"

GRADES = ["No DR", "Mild NPDR", "Moderate NPDR", "Severe NPDR", "PDR"]
ENCODERS = {"flair": "B2_flair", "biomedclip": "B1_biomedclip"}
EMB_DIM = 512
SEED = 2026
