"""Figures, per-image explanations and Markdown tables from results/ (run after run_experiments.py).

  python3 src/report.py
"""
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from PIL import Image
from sklearn.metrics import confusion_matrix

from config import FIGURES, GRADES, MVLM04, RESULTS
from reasoner import KGReasoner

R = KGReasoner()
COHORT_NAME = {"internal_test": "Internal test (Public-DR-v1)", "deepdrid": "External: DeepDRiD"}
ORDER = ["ZS-Grade", "NN", "CBM-KG", "KG-Sym-T", "KG-Sym", "NS-Fuse", "NS-Fuse-T", "NS-Joint"]
SHORT = ["0", "1", "2", "3", "4"]


def image_path(cohort, key):
    if cohort == "deepdrid":
        m = pd.read_csv(RESULTS.parent / "features" / "deepdrid_manifest.csv").set_index("key")
        return m.loc[key, "path"]
    return MVLM04 / "public_dr_v1_256" / "images" / key.split("_")[0] / f"{key}.jpg"


def md(df, index=True):
    """Minimal DataFrame -> Markdown table (avoids the optional tabulate dependency)."""
    d = df.reset_index() if index else df
    cols = [" / ".join(map(str, c)) if isinstance(c, tuple) else str(c) for c in d.columns]
    lines = ["| " + " | ".join(cols) + " |", "|" + "---|" * len(cols)]
    for r in d.itertuples(index=False):
        lines.append("| " + " | ".join(f"{v:.4g}" if isinstance(v, float) else str(v) for v in r) + " |")
    return "\n".join(lines)


def fmt(m, s):
    return f"{m:.3f} ± {s:.3f}"


def tables():
    s = pd.read_csv(RESULTS / "summary_mean_sd.csv")
    out = ["# KGNS-DR results\n", "Mean ± SD over 5 seeds. Selection used the internal validation split only.\n"]
    for enc in s.encoder.unique():
        for c in ["internal_test", "deepdrid"]:
            d = s[(s.encoder == enc) & (s.cohort == c)].set_index("model").reindex(ORDER).dropna(how="all")
            out.append(f"\n## {enc} - {COHORT_NAME[c]}\n")
            out.append("| Model | Accuracy | Balanced acc. | Macro-F1 | QWK | ECE | Referable AUC | Recall severe |")
            out.append("|---|---|---|---|---|---|---|---|")
            for m, r in d.iterrows():
                out.append(f"| {m} | " + " | ".join(fmt(r[f'{k}_mean'], r[f'{k}_std']) for k in
                           ["acc", "bal_acc", "macro_f1", "qwk", "ece", "referable_auc", "recall_3"]) + " |")
    f = pd.read_csv(RESULTS / "faithfulness.csv")
    out.append("\n## Explanation faithfulness (concept deletion, mean over seeds)\n")
    out.append("Comprehensiveness = drop in predicted-grade probability when the cited lesions are set absent; "
               "random = same number of uncited lesions removed. Flip = predicted grade changes.\n")
    out.append("| Encoder | Cohort | Model | n explained | Compr. (cited) | Compr. (random) | Flip (cited) | Flip (random) |")
    out.append("|---|---|---|---|---|---|---|---|")
    for _, r in f.iterrows():
        out.append(f"| {r.encoder} | {r.cohort} | {r.model} | {r.n_explained:.0f} | {r.comprehensiveness:.3f} | "
                   f"{r.comprehensiveness_random:.3f} | {r.flip_rate:.3f} | {r.flip_rate_random:.3f} |")
    k = pd.read_csv(RESULTS / "kg_consistency.csv")
    out.append("\n## Clinical-rule consistency (reference evidence: KG-Sym-T lesion concepts)\n")
    out.append("| Encoder | Cohort | Model | Mean KG support of prediction | Violation rate (support < 0.05) |")
    out.append("|---|---|---|---|---|")
    for _, r in k.iterrows():
        out.append(f"| {r.encoder} | {r.cohort} | {r.model} | {r.mean_kg_support:.3f} | {r.kg_violation_rate:.3f} |")
    z = pd.read_csv(RESULTS / "concept_zero_shot_auc.csv")
    piv = z.pivot_table(index=["concept", "level"], columns=["encoder", "cohort"], values="auc_grade_ge_level")
    out.append("\n## Zero-shot lesion-concept validity (no training): AUC for grade >= concept level\n")
    out.append(md(piv.round(3)))
    p = pd.read_csv(RESULTS / "paired_vs_nn_seed0.csv")
    out.append("\n## Paired bootstrap vs NN (seed 0, 1,000 resamples)\n")
    out.append(md(p.round(4), False))
    ci = pd.read_csv(RESULTS / "bootstrap_ci_seed0.csv")
    out.append("\n## 95% bootstrap CIs (seed 0)\n")
    out.append(md(ci, False))
    co = pd.read_csv(RESULTS / "cohorts.csv")
    out.append("\n## Cohorts\n")
    out.append(md(co, False))
    ps = pd.read_csv(RESULTS / "internal_per_source.csv")
    out.append("\n## Internal test by source (seed 0)\n")
    out.append(md(ps[["encoder", "source", "model", "n", "acc", "macro_f1", "qwk"]].round(3), False))
    (RESULTS / "tables.md").write_text("\n".join(out) + "\n")


def figures(enc="flair"):
    FIGURES.mkdir(parents=True, exist_ok=True)
    show = ["NN", "KG-Sym-T", "NS-Fuse-T", "NS-Joint"]
    for c in ["internal_test", "deepdrid"]:
        z = np.load(RESULTS / "preds" / f"{enc}_{c}.npz", allow_pickle=True)
        y = z["y"]
        fig, axs = plt.subplots(1, len(show), figsize=(4 * len(show), 3.8))
        for ax, m in zip(axs, show):
            cm = confusion_matrix(y, z[f"p_{m}"].argmax(1), labels=range(5), normalize="true")
            ax.imshow(cm, cmap="Blues", vmin=0, vmax=1)
            for i in range(5):
                for j in range(5):
                    ax.text(j, i, f"{cm[i, j]:.2f}", ha="center", va="center", fontsize=7,
                            color="white" if cm[i, j] > 0.5 else "black")
            ax.set_xticks(range(5), SHORT)
            ax.set_yticks(range(5), SHORT)
            ax.set_xlabel("Predicted grade")
            ax.set_title(m)
        axs[0].set_ylabel("True grade")
        fig.suptitle(f"Row-normalised confusion matrices - {COHORT_NAME[c]} ({enc}, seed 0)")
        fig.tight_layout()
        fig.savefig(FIGURES / f"confusion_{enc}_{c}.png", dpi=200)
        plt.close(fig)

        # Reliability diagram
        fig, ax = plt.subplots(figsize=(4.5, 4.2))
        bins = np.linspace(0, 1, 11)
        for m in show:
            p = z[f"p_{m}"]
            conf, cor = p.max(1), p.argmax(1) == y
            xs, ys = [], []
            for lo, hi in zip(bins[:-1], bins[1:]):
                mm = (conf > lo) & (conf <= hi)
                if mm.sum() >= 10:
                    xs.append(conf[mm].mean())
                    ys.append(cor[mm].mean())
            ax.plot(xs, ys, marker="o", label=m)
        ax.plot([0, 1], [0, 1], "k--", lw=1)
        ax.set_xlabel("Confidence")
        ax.set_ylabel("Accuracy")
        ax.set_title(f"Reliability - {COHORT_NAME[c]}", fontsize=9)
        ax.legend(fontsize=7)
        fig.tight_layout()
        fig.savefig(FIGURES / f"reliability_{enc}_{c}.png", dpi=200)
        plt.close(fig)

        # Mean lesion probability per true grade (does evidence follow the ICDR hierarchy?)
        fig, axs = plt.subplots(1, 2, figsize=(10, 3.6))
        for ax, m in zip(axs, ["KG-Sym-T", "KG-Sym"]):
            q = z[f"q_{m}"]
            M = np.stack([q[y == g].mean(0) for g in range(5)])
            ax.imshow(M, cmap="Oranges", vmin=0, vmax=1, aspect="auto")
            for i in range(5):
                for j in range(len(R.concepts)):
                    ax.text(j, i, f"{M[i, j]:.2f}", ha="center", va="center", fontsize=7)
            ax.set_xticks(range(len(R.concepts)), R.concepts, rotation=45)
            ax.set_yticks(range(5), GRADES)
            ax.set_title(f"{m}: mean lesion probability by true grade", fontsize=9)
        fig.suptitle(COHORT_NAME[c])
        fig.tight_layout()
        fig.savefig(FIGURES / f"concepts_by_grade_{enc}_{c}.png", dpi=200)
        plt.close(fig)

    # Faithfulness bars
    f = pd.read_csv(RESULTS / "faithfulness.csv")
    f = f[f.encoder == enc]
    fig, axs = plt.subplots(1, 2, figsize=(10, 3.6), sharey=True)
    for ax, c in zip(axs, ["internal_test", "deepdrid"]):
        d = f[f.cohort == c].set_index("model").reindex([m for m in ORDER if m in set(f.model)])
        x = np.arange(len(d))
        ax.bar(x - 0.2, d.comprehensiveness, 0.4, label="cited lesions removed")
        ax.bar(x + 0.2, d.comprehensiveness_random, 0.4, label="random lesions removed")
        ax.set_xticks(x, d.index, rotation=30)
        ax.axhline(0, color="k", lw=0.8)
        ax.set_title(COHORT_NAME[c], fontsize=9)
    axs[0].set_ylabel("Drop in predicted-grade probability")
    axs[0].legend(fontsize=7)
    fig.suptitle(f"Explanation faithfulness ({enc})")
    fig.tight_layout()
    fig.savefig(FIGURES / f"faithfulness_{enc}.png", dpi=200)
    plt.close(fig)


def explanations(enc="flair", model="NS-Joint", concept_model="NS-Joint"):
    for c in ["internal_test", "deepdrid"]:
        z = np.load(RESULTS / "preds" / f"{enc}_{c}.npz", allow_pickle=True)
        y, keys, p, pn, q = z["y"], z["keys"], z[f"p_{model}"], z["p_NN"], z[f"q_{concept_model}"]
        k = p.argmax(1)
        rows = []
        for i in range(len(y)):
            rows.append({"key": keys[i], "true_grade": int(y[i]), "pred_grade": int(k[i]), "p_pred": float(p[i, k[i]]),
                         **{f"q_{cn}": round(float(q[i, j]), 3) for j, cn in enumerate(R.concepts)},
                         "explanation": R.explanation_text(q[i], int(k[i]), p[i, k[i]], pn[i])})
        pd.DataFrame(rows).to_csv(RESULTS / f"explanations_{enc}_{c}.csv", index=False)

        # Panel: one correctly graded example per grade
        rng = np.random.default_rng(0)
        fig, axs = plt.subplots(2, 5, figsize=(17, 6.6), gridspec_kw={"height_ratios": [3, 2]})
        for g in range(5):
            idx = np.where((y == g) & (k == g))[0]
            ax, bx = axs[0, g], axs[1, g]
            if len(idx) == 0:
                ax.axis("off")
                bx.axis("off")
                continue
            i = int(rng.choice(idx))
            try:
                ax.imshow(Image.open(image_path(c, str(keys[i]))).convert("RGB").resize((256, 256)))
            except Exception:
                pass
            ax.set_title(f"True {GRADES[g]} | pred {GRADES[k[i]]} ({p[i, k[i]]:.2f})", fontsize=8)
            ax.axis("off")
            cols = ["#bbb"] * len(R.concepts)
            for cj in R.explain(q[i], int(k[i])):
                cols[cj] = "#D9822B"
            bx.barh(range(len(R.concepts)), q[i], color=cols)
            bx.set_yticks(range(len(R.concepts)), R.concepts, fontsize=7)
            bx.set_xlim(0, 1)
            bx.invert_yaxis()
            bx.set_xlabel("lesion probability (orange = cited by fired rule)", fontsize=7)
        fig.suptitle(f"KG-guided explanations - {COHORT_NAME[c]} ({model}, {enc})")
        fig.tight_layout()
        fig.savefig(FIGURES / f"explanation_examples_{enc}_{c}.png", dpi=170)
        plt.close(fig)


if __name__ == "__main__":
    tables()
    figures("flair")
    explanations("flair")
    print("report written to", RESULTS)
