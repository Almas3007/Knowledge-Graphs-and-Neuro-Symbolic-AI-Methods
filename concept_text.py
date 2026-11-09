"""Embed the DR-KG lesion concepts with each encoder's text tower.

For concept c with prompts P_c, t_c = normalize(mean_p enc_text(template(p))). Images are scored by
s_c(x) = cos(x, t_c) - cos(x, t_neutral): zero-shot lesion evidence that never sees a grade label.
  python3 src/concept_text.py --encoder flair
"""
import argparse
import json

import numpy as np
import torch.nn.functional as F

from config import FEATURES, KG_DIR
from encoders import ENCODER_CLASSES

TEMPLATES = {"flair": "A fundus photograph of {}",
             "biomedclip": "A color retinal fundus photograph showing {}."}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--encoder", choices=sorted(ENCODER_CLASSES), required=True)
    a = ap.parse_args()
    kg = json.loads((KG_DIR / "dr_kg.json").read_text())
    enc = ENCODER_CLASSES[a.encoder]("cpu")
    tpl = TEMPLATES[a.encoder]

    def embed(prompts):
        return F.normalize(F.normalize(enc.encode_text([tpl.format(p) for p in prompts]), dim=-1).mean(0), dim=0)

    T = np.stack([embed(c["prompts"]).numpy() for c in kg["concepts"]])
    N = embed(kg["neutral_prompts"]).numpy()
    # Zero-shot grade prompts (baseline): one embedding per ICDR grade name
    grade_terms = ["no diabetic retinopathy", "mild diabetic retinopathy", "moderate diabetic retinopathy",
                   "severe diabetic retinopathy", "proliferative diabetic retinopathy"]
    G = np.stack([embed([t]).numpy() for t in grade_terms])
    FEATURES.mkdir(parents=True, exist_ok=True)
    np.savez(FEATURES / f"concept_text_{a.encoder}.npz", T=T, neutral=N, grades=G,
             concepts=np.array([c["id"] for c in kg["concepts"]]), template=tpl)
    print(a.encoder, T.shape, "pairwise cos range", float((T @ T.T)[np.triu_indices(len(T), 1)].min()),
          float((T @ T.T)[np.triu_indices(len(T), 1)].max()))


if __name__ == "__main__":
    main()
