# Reference: Schema & Metric Contract

The contract that keeps the engine (`lib/label.py`, `lib/kappa.py`) **general** —
it labels and scores any construct, not a frozen tri-polar physician case.
Agreed 2026-07-21. Scope now: **categorical + ordinal**. multilabel / scalar =
roadmap.

---

## 1. Label schema (config `labels:` block)

```yaml
labels:
  type: categorical | ordinal      # (multilabel, scalar = future)
  values: [...]                     # 2–6 values (order matters iff ordinal)
  none_value: <value|null>          # the "signal absent" catch-all, if any
  tie_break: none_loses | first     # majority-vote tie rule (default: none_loses if none_value set, else first)
```

| type | meaning | example |
|------|---------|---------|
| **categorical** | unordered, mutually exclusive classes | `{authoritative, advisory, informational, none}` |
| **ordinal** | ordered classes; being off by 2 is worse than by 1 | `{none < low < high}` · `{1,2,3,4,5}` |

Rules (from `ref-schema.md`): 2–6 values, mutually exclusive, exhaustive (add a
`none`/`other` catch-all if needed). For ordinal, `values` is listed **in order**.

---

## 2. Metric families (auto-selected by `labels.type`, overridable)

| type | metrics computed |
|------|------------------|
| **categorical** | Cohen's κ (2 raters) · Fleiss' κ (>2) · accuracy · per-label P/R/F1 · confusion |
| **ordinal** | **quadratic weighted κ (primary)** · Spearman ρ · MAE · + all categorical metrics |
| **inter-annotator (any type)** | **Krippendorff's α** (nominal or ordinal distance) — the unifying ≥2-rater agreement metric → human ceiling / reliability |

Primary κ shown in the trajectory: categorical → Cohen (or Fleiss if >2 raters);
ordinal → quadratic weighted κ.

---

## 3. Comparison contexts (same metric family, different pairing)

| context | who vs who | meaning |
|---------|-----------|---------|
| `agent_vs_gold` | agent labels vs human gold | correctness |
| `annotator_vs_annotator` | human vs human (≥2) | human ceiling (Krippendorff α) |
| `panel_internal` | LLM vs LLM | reliability (not correctness) |
| `version_vs_version` | vN vs vM on the fixed anchor | did a change help/hurt |

---

## 4. Engine acceptance (S0)

`lib/label.py` and `lib/kappa.py` must satisfy BOTH:
- **(a) faithful port** — on B03 data in categorical mode, reproduce the original
  Cohen's κ (v04 majority-vs-gold = 0.9322) exactly.
- **(b) genuinely general** — a fake binary / 5-point-ordinal / 4-way-categorical
  config runs end-to-end (proves nothing is frozen to tri-polar HIGH/LOW/NONE).

Both scripts read `labels` from config (or `--labels`/`--type` CLI override), take
`--project-dir`, and never hardcode physician / openness / HIGH-LOW-NONE.
