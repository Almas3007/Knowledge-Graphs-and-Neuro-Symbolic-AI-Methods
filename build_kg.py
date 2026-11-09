"""Build the diabetic-retinopathy medical knowledge graph (DR-KG).

The graph encodes the International Clinical Diabetic Retinopathy (ICDR) severity scale
(Wilkinson et al., Ophthalmology 2003) and the ETDRS 4-2-1 rule for severe NPDR. It is the single
source of truth for the symbolic reasoner: src/reasoner.py compiles its grading rules from the
`requires_any` edges written here, so changing the graph changes the reasoning.

Outputs (kg/): dr_kg.json, dr_kg.graphml, triples.csv, figures/kg.png
  python3 src/build_kg.py
"""
import csv
import json

import networkx as nx

from config import KG_DIR, FIGURES

ICDR = "ICDR scale (Wilkinson et al., Ophthalmology 2003)"
ETDRS = "ETDRS 4-2-1 rule (ETDRS Report 12, Ophthalmology 1991)"

# ---------------------------------------------------------------- lesion concepts
# `prompts` feed the vision-language text encoders; FLAIR was pretrained with these lesion terms.
CONCEPTS = [
    dict(id="MA", name="Microaneurysms", level=1,
         description="Small saccular outpouchings of retinal capillaries; the earliest visible sign of DR.",
         location="retinal capillaries", mechanism="pericyte loss and capillary wall weakening",
         prompts=["microaneurysms", "few microaneurysms", "small red dots of microaneurysms"]),
    dict(id="HE", name="Intraretinal hemorrhages", level=2,
         description="Dot and blot hemorrhages within the retina.",
         location="inner retina", mechanism="capillary rupture",
         prompts=["retinal haemorrhages", "dot and blot haemorrhages", "intraretinal hemorrhages"]),
    dict(id="EX", name="Hard exudates", level=2,
         description="Yellow lipid and protein deposits from leaking vessels.",
         location="outer plexiform layer, often near the macula", mechanism="breakdown of the blood-retinal barrier",
         prompts=["hard exudates", "yellow lipid exudates", "exudates near the macula"]),
    dict(id="CWS", name="Cotton-wool spots (soft exudates)", level=2,
         description="Fluffy white nerve-fibre-layer infarcts.",
         location="retinal nerve fibre layer", mechanism="focal capillary occlusion and axoplasmic stasis",
         prompts=["cotton wool spots", "soft exudates", "white fluffy cotton wool spots"]),
    dict(id="SHE", name="Extensive hemorrhages in four quadrants", level=3,
         description="More than 20 intraretinal hemorrhages in each of the four quadrants (4-2-1 rule, '4').",
         location="all four retinal quadrants", mechanism="widespread capillary non-perfusion",
         prompts=["many haemorrhages in all four quadrants", "extensive retinal haemorrhages", "severe intraretinal haemorrhages"]),
    dict(id="VB", name="Venous beading", level=3,
         description="Localised dilation and constriction of retinal veins (4-2-1 rule, '2': two or more quadrants).",
         location="retinal veins", mechanism="retinal ischaemia",
         prompts=["venous beading", "beaded retinal veins", "venous abnormalities"]),
    dict(id="IRMA", name="Intraretinal microvascular abnormalities", level=3,
         description="Shunt vessels within the retina (4-2-1 rule, '1': one or more quadrants).",
         location="intraretinal capillary bed", mechanism="ischaemia-driven vascular remodelling",
         prompts=["intraretinal microvascular abnormalities", "IRMA", "abnormal intraretinal vessels"]),
    dict(id="NV", name="Neovascularisation", level=4,
         description="New vessels on the disc (NVD) or elsewhere (NVE).",
         location="optic disc or retinal surface", mechanism="VEGF-driven angiogenesis",
         prompts=["neovascularization", "new vessels on the optic disc", "neovascularisation elsewhere"]),
    dict(id="PRH", name="Preretinal or vitreous hemorrhage", level=4,
         description="Bleeding in front of the retina or into the vitreous from fragile new vessels.",
         location="preretinal space or vitreous", mechanism="rupture of new vessels",
         prompts=["preretinal haemorrhage", "vitreous haemorrhage", "boat-shaped preretinal hemorrhage"]),
]
NEUTRAL_PROMPTS = ["normal fundus", "healthy retina", "no diabetic retinopathy"]

# ---------------------------------------------------------------- severity grades
GRADES = [
    dict(id="G0", grade=0, name="No DR", rule="No abnormalities", followup="12 months"),
    dict(id="G1", grade=1, name="Mild NPDR", rule="Microaneurysms only", followup="12 months"),
    dict(id="G2", grade=2, name="Moderate NPDR", rule="More than just microaneurysms but less than severe NPDR",
         followup="6-12 months"),
    dict(id="G3", grade=3, name="Severe NPDR",
         rule="Any of: >20 intraretinal haemorrhages in each of 4 quadrants; venous beading in >=2 quadrants; "
              "IRMA in >=1 quadrant; and no signs of PDR", followup="3-4 months; consider referral"),
    dict(id="G4", grade=4, name="PDR", rule="Neovascularisation and/or vitreous or preretinal haemorrhage",
         followup="Urgent referral; panretinal photocoagulation or anti-VEGF"),
]


def build():
    g = nx.MultiDiGraph(name="DR-KG", version="1.0")
    for c in CONCEPTS:
        g.add_node(c["id"], type="Lesion", name=c["name"], description=c["description"],
                   prompts="|".join(c["prompts"]))
        loc, mech = "LOC:" + c["location"], "MECH:" + c["mechanism"]
        g.add_node(loc, type="AnatomicalSite", name=c["location"])
        g.add_node(mech, type="Mechanism", name=c["mechanism"])
        g.add_edge(c["id"], loc, relation="located_in", source=ICDR)
        g.add_edge(c["id"], mech, relation="caused_by", source=ICDR)
        g.add_edge(c["id"], f"G{c['level']}", relation="indicates_at_least",
                   source=ETDRS if c["level"] == 3 else ICDR)
    for d in GRADES:
        g.add_node(d["id"], type="SeverityGrade", name=d["name"], grade=d["grade"], rule=d["rule"])
        rid = "RULE:" + d["id"]
        g.add_node(rid, type="ClinicalRule", name=d["rule"])
        g.add_edge(d["id"], rid, relation="defined_by", source=ETDRS if d["grade"] == 3 else ICDR)
        fid = "FU:" + d["id"]
        g.add_node(fid, type="Management", name=d["followup"])
        g.add_edge(d["id"], fid, relation="recommended_followup", source="AAO Preferred Practice Pattern")
        members = [c["id"] for c in CONCEPTS if c["level"] == d["grade"]]
        for m in members:  # the edge the reasoner compiles: grade holds if ANY member lesion is present
            g.add_edge(rid, m, relation="requires_any", source=ETDRS if d["grade"] == 3 else ICDR)
        if d["grade"] > 0:
            g.add_edge(f"G{d['grade'] - 1}", d["id"], relation="progresses_to", source=ICDR)
    # Exclusion knowledge: a grade's rule requires that no higher-grade lesion is present.
    for d in GRADES[:-1]:
        for c in CONCEPTS:
            if c["level"] > d["grade"]:
                g.add_edge("RULE:" + d["id"], c["id"], relation="excludes", source=ICDR)
    g.add_node("NEUTRAL", type="Reference", name="Normal fundus", prompts="|".join(NEUTRAL_PROMPTS))
    return g


def draw(g, path):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    core = g.subgraph([n for n, a in g.nodes(data=True) if a["type"] in {"Lesion", "SeverityGrade"}])
    pos = {}
    for d in GRADES:
        pos[d["id"]] = (d["grade"] * 2.2, 0.0)
    xs = [0.9 + i * (8.8 - 0.9) / (len(CONCEPTS) - 1) for i in range(len(CONCEPTS))]
    for x, c in zip(xs, sorted(CONCEPTS, key=lambda c: c["level"])):
        pos[c["id"]] = (x, 1.6)
    fig, ax = plt.subplots(figsize=(12, 4.2))
    col = {"Lesion": "#E8A33D", "SeverityGrade": "#3A6EA5"}
    edges_ind = [(u, v) for u, v, a in core.edges(data=True) if a["relation"] == "indicates_at_least"]
    edges_pro = [(u, v) for u, v, a in core.edges(data=True) if a["relation"] == "progresses_to"]
    nx.draw_networkx_edges(core, pos, edgelist=edges_ind, ax=ax, edge_color="#999", arrows=True, arrowsize=14,
                           arrowstyle="-|>", node_size=1500)
    nx.draw_networkx_edges(core, pos, edgelist=edges_pro, ax=ax, edge_color="#3A6EA5", width=2, arrows=True,
                           arrowsize=16, arrowstyle="-|>", node_size=1500)
    nx.draw_networkx_nodes(core, pos, ax=ax, node_size=1500,
                           node_color=[col[core.nodes[n]["type"]] for n in core.nodes])
    labels = {n: (core.nodes[n]["name"].replace(" ", "\n") if core.nodes[n]["type"] == "SeverityGrade" else n)
              for n in core.nodes}
    nx.draw_networkx_labels(core, pos, labels=labels, ax=ax, font_size=7, font_color="white", font_weight="bold")
    pass  # caption carries the title
    ax.axis("off")
    fig.tight_layout()
    fig.savefig(path, dpi=200)
    plt.close(fig)


def main():
    KG_DIR.mkdir(parents=True, exist_ok=True)
    FIGURES.mkdir(parents=True, exist_ok=True)
    g = build()
    data = {"name": "DR-KG", "version": "1.0", "sources": [ICDR, ETDRS],
            "concepts": CONCEPTS, "neutral_prompts": NEUTRAL_PROMPTS, "grades": GRADES,
            "nodes": [{"id": n, **a} for n, a in g.nodes(data=True)],
            "edges": [{"head": u, "relation": a["relation"], "tail": v, "source": a["source"]}
                      for u, v, a in g.edges(data=True)]}
    (KG_DIR / "dr_kg.json").write_text(json.dumps(data, indent=2))
    nx.write_graphml(g, KG_DIR / "dr_kg.graphml")
    with open(KG_DIR / "triples.csv", "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["head", "relation", "tail", "source"])
        for e in data["edges"]:
            w.writerow([e["head"], e["relation"], e["tail"], e["source"]])
    draw(g, FIGURES / "kg.png")
    types = {}
    for _, a in g.nodes(data=True):
        types[a["type"]] = types.get(a["type"], 0) + 1
    print(f"DR-KG: {g.number_of_nodes()} nodes {types}, {g.number_of_edges()} edges")


if __name__ == "__main__":
    main()
