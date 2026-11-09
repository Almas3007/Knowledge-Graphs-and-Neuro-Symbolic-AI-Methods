"""Differentiable symbolic reasoner compiled from DR-KG.

Each severity grade k>0 has a rule "grade k holds if ANY lesion linked by RULE:Gk --requires_any--> is present".
ICDR grading assigns the HIGHEST grade whose rule holds (and every grade's rule `excludes` higher lesions).
With independent concept probabilities q_c this has an exact closed form (probabilistic logic):

  h_k  = 1 - prod_{c in R_k} (1 - q_c)                    P(rule k fires)
  P(4) = h_4
  P(k) = h_k * prod_{j>k} (1 - h_j)        k = 1..3
  P(0) = prod_{j>=1} (1 - h_j)

-log P(y | q) is the semantic loss of the grade's logical definition, so training a concept detector against
it teaches lesions only through the clinical rules (weak supervision from grades, no lesion masks).
"""
import json

import torch

from config import KG_DIR


class KGReasoner:
    def __init__(self, kg_path=KG_DIR / "dr_kg.json"):
        kg = json.loads(kg_path.read_text())
        self.kg = kg
        self.concepts = [c["id"] for c in kg["concepts"]]
        self.concept_names = {c["id"]: c["name"] for c in kg["concepts"]}
        self.grade_names = [g["name"] for g in kg["grades"]]
        self.grade_rules = [g["rule"] for g in kg["grades"]]
        idx = {c: i for i, c in enumerate(self.concepts)}
        self.members = {}
        for e in kg["edges"]:
            if e["relation"] == "requires_any":
                k = int(e["head"].split(":G")[1])
                self.members.setdefault(k, []).append(idx[e["tail"]])
        self.sources = {int(e["head"][1:]): e["source"] for e in kg["edges"] if e["relation"] == "defined_by"}
        assert sorted(self.members) == [1, 2, 3, 4], self.members
        self.level_of = {c: k for k, ms in self.members.items() for c in ms}

    def rule_probs(self, q):
        """h[:, k-1] = P(rule for grade k fires), k = 1..4."""
        return torch.stack([1 - torch.prod(1 - q[:, self.members[k]], dim=1) for k in (1, 2, 3, 4)], dim=1)

    def grade_probs(self, q, eps=1e-6):
        h = self.rule_probs(q)
        none_above = torch.ones_like(h[:, 0])
        out = [None] * 5
        for k in (4, 3, 2, 1):
            out[k] = h[:, k - 1] * none_above
            none_above = none_above * (1 - h[:, k - 1])
        out[0] = none_above
        p = torch.stack(out, dim=1).clamp_min(eps)
        return p / p.sum(1, keepdim=True)

    # ------------------------------------------------------------ explanations
    def explain(self, q_row, k, thr=0.5):
        """Concepts cited for predicted grade k: members of rule k with q >= thr (else the strongest member)."""
        if k == 0:
            return []
        ms = self.members[k]
        cited = [c for c in ms if q_row[c] >= thr]
        return cited or [max(ms, key=lambda c: q_row[c])]

    def explanation_text(self, q_row, k, p_final=None, p_neural=None, thr=0.5):
        g = self.grade_names
        lines = [f"Prediction: {g[k]}" + (f" (p={p_final:.2f})." if p_final is not None else ".")]
        ps = self.grade_probs(torch.tensor(q_row, dtype=torch.float32)[None])[0]
        ks = int(ps.argmax())
        lines.append(f"KG rules alone: {g[ks]} (p={float(ps[ks]):.2f})" +
                     (" - consistent." if ks == k else " - differs from the final prediction."))
        if k == 0:
            top = max(range(len(self.concepts)), key=lambda c: q_row[c])
            lines.append(f"No grading rule cited; strongest lesion evidence is "
                         f"{self.concept_names[self.concepts[top]]} (q={q_row[top]:.2f}).")
        else:
            cited = self.explain(q_row, k)
            ev = ", ".join(f"{self.concept_names[self.concepts[c]]} (q={q_row[c]:.2f})" for c in cited)
            lines.append(f"Grading rule [{self.sources[k]}]: {self.grade_rules[k]}.")
            weak = all(q_row[c] < thr for c in cited)
            lines.append(f"Supporting evidence: {ev}" + (" - weak (below 0.5)." if weak else "."))
        higher = [c for j in range(k + 1, 5) for c in self.members[j]]
        if higher:
            conflict = [c for c in higher if q_row[c] >= thr]
            if conflict:
                cf = ", ".join(f"{self.concepts[c]} (q={q_row[c]:.2f})" for c in conflict)
                lines.append(f"Conflict: higher-grade lesion evidence present ({cf}); review advised.")
            else:
                mx = max(higher, key=lambda c: q_row[c])
                lines.append(f"Higher grades excluded: all higher-grade lesions below 0.5 "
                             f"(max {self.concepts[mx]} q={q_row[mx]:.2f}).")
        if p_neural is not None:
            kn = int(max(range(5), key=lambda j: p_neural[j]))
            lines.append(f"Neural branch: {g[kn]} (p={p_neural[kn]:.2f})" +
                         (" - agrees." if kn == k else " - overruled by clinical rules."))
        return " ".join(lines)
