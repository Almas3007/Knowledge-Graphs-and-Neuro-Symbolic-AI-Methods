"""Extract frozen image embeddings for the DeepDRiD regular-fundus cohort (external test set).

Uses the labelled training + validation folders (1,600 images, 400 patients). Each image takes the
DR level of the eye it shows (left_eye_DR_Level / right_eye_DR_Level).

  python3 src/extract_deepdrid.py --encoder flair
  python3 src/extract_deepdrid.py --encoder biomedclip
"""
import argparse
import numpy as np
import pandas as pd
import torch
from PIL import Image, ImageOps

from config import DEEPDRID, FEATURES
from encoders import ENCODER_CLASSES


def deepdrid_table():
    rows = []
    for part in ["regular-fundus-training", "regular-fundus-validation"]:
        d = pd.read_csv(DEEPDRID / part / f"{part}.csv")
        for _, r in d.iterrows():
            eye = "left" if "_l" in r.image_id else "right"
            g = r[f"{eye}_eye_DR_Level"]
            if pd.isna(g):  # 11 training images whose grade sits in the other eye's column: ambiguous, excluded
                continue
            rel = str(r.image_path).replace("\\", "/").strip("/").split("/")[-2:]
            rows.append({"key": r.image_id, "patient": int(r.patient_id), "eye": eye, "grade": int(g),
                         "quality": int(r["Overall quality"]), "part": part,
                         "path": str(DEEPDRID / part / "Images" / rel[0] / rel[1])})
    return pd.DataFrame(rows)


class Images(torch.utils.data.Dataset):
    def __init__(self, paths, pre):
        self.paths, self.pre = paths, pre

    def __len__(self):
        return len(self.paths)

    def __getitem__(self, i):
        with Image.open(self.paths[i]) as im:
            return self.pre(ImageOps.exif_transpose(im).convert("RGB"))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--encoder", choices=sorted(ENCODER_CLASSES), required=True)
    ap.add_argument("--device", default="mps" if torch.backends.mps.is_available() else "cpu")
    ap.add_argument("--batch", type=int, default=16)
    a = ap.parse_args()
    tab = deepdrid_table()
    FEATURES.mkdir(parents=True, exist_ok=True)
    tab.to_csv(FEATURES / "deepdrid_manifest.csv", index=False)
    enc = ENCODER_CLASSES[a.encoder](a.device)
    dl = torch.utils.data.DataLoader(Images(tab.path.tolist(), enc.preprocess), batch_size=a.batch, num_workers=2)
    X = []
    for i, b in enumerate(dl):
        X.append(enc.encode_image(b).numpy())
        if i % 10 == 0:
            print(f"{a.encoder} {min((i + 1) * a.batch, len(tab))}/{len(tab)}", flush=True)
    X = np.concatenate(X).astype("float32")
    assert len(X) == len(tab) and np.isfinite(X).all()
    np.savez_compressed(FEATURES / f"deepdrid_{a.encoder}.npz", X=X, keys=tab.key.values.astype(str))
    print("saved", X.shape)


if __name__ == "__main__":
    main()
