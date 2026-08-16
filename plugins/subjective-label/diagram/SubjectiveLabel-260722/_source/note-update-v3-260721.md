# Subjective-Label — Method Critique & Autonomy Roadmap (v3)

- **Date:** 2026-07-21 (v3 — general engine + full-autonomy architecture)
- **Source:** 2026-07-17 meeting + B01/B02/B03 runs + junjie's discoveries (P01/P02/S01) + design discussion
- **Purpose:** design baseline for the subjective-label skill as a GENERAL, near-autonomous labeling engine, with the honesty guards that keep its output defensible.

---

## Part 0 — Framing

The skill is a **general engine**: any (corpus × subjective construct). Physician
Big-Five is one instance. Nothing physician/openness/Big-Five may be hardcoded.

**Autonomy target:** a new construct on new data runs **near-fully-autonomously**.
Human input shrinks to a one-time **objective** + a one-time **engine license**
(+ optional extreme-case escape hatch). See Part 2 for exactly where humans remain.

---

## Part 1 — Flaws to avoid (from the meeting; all construct-general) + how autonomy handles each WITHOUT adding per-project human labeling

| # | Flaw | Autonomy-compatible fix |
|---|------|--------------------------|
| F1 | **Circular ground truth** (guideline fit to model labels, same models "validate") | (a) each round a **fresh held-out** the guideline never saw; (b) **validation model ≠ labeling model**; (c) correctness-vs-human measured ONCE externally on public data (Part 4), not by models judging models |
| F2 | **Construct-transfer gap** (validate on dataset A, claim on B) | autonomy license = engine reaches human ceiling on a **battery** of public constructs; the license only covers constructs **adjacent** to the battery — coverage is reported, not assumed |
| F3 | **No human ceiling** | ceiling comes from public **per-rater** datasets (junjie P02), amortized once at the engine level — not per project |
| F4 | **Clarity ≠ correctness** | report as **separate metrics**: reliability (panel-κ), clarity (executor-independence), correctness (only on public/licensed data) |
| F5 | **Embedding geometry ≠ label geometry** (+ "guideline reshapes embedding" error) | hard-case mining from a **label-trained classifier** (`classify.py`), not raw embedding distance; delete the reshape claim from docs |
| F6 | **Enriched-hard conflated with representative** | **two pools**: representative (base-rate, honest metrics) vs enriched (refinement) |
| F7 | **n=24 random anchor** | **fixed** representative anchor (versions comparable) + **fresh held-out** (honest generalization) |
| F8 | **Stop = stable ≠ correct** | convergence gate includes **held-out gap** + downstream/discriminance score, not just stability |

---

## Part 2 — Where humans remain (the irreducible minimum)

Full autonomy is achievable **only because a selection criterion replaces human
judgment**. Without a criterion, "which construct / which label is right" is
underdetermined and needs a human. With one, it becomes optimization → automatable.

| Human input | Frequency | Why it cannot be automated away |
|---|---|---|
| **State the objective** (what the labels are for) — e.g. "traits must predict opioid Rx and be mutually discriminant" | once per construct family; **already in the research design** | a subjective construct is a *choice for a purpose*; the purpose is the human's |
| **Engine license sign-off** (accept that the engine reached ceiling on the public battery) | once at engine level | a human decides the license bar is met |
| **Extreme-case escape hatch** | optional, rare | cheap insurance; can be turned off |

Everything else — proposing the construct, refining the guideline, labeling,
resolving disagreements, scaling — is automated.

---

## Part 3 — Construct auto-selection (objective-driven)

The construct itself is automated via three levers; the third is the real unlock:

| Lever | Role | Limit |
|---|---|---|
| **multi-LLM propose** | generate candidate definitions **and surface where they diverge** (the divergences = the parts that need pinning down) | consensus = generic textbook meaning, not the purpose-specific one |
| **labeled-dataset anchor** | adopt/borrow an existing human-defined construct | only for constructs that already exist publicly |
| **objective-driven select ⭐** | keep the candidate that maximizes an **objective**: downstream predictive validity, mutual discriminance, or dataset match | needs an objective to exist |

Flow: multi-LLM proposes N candidate constructs+guidelines → each labels a sample →
**select the candidate that best optimizes the declared objective** (e.g. discriminance
from sibling traits + downstream opioid-Rx signal) → refine it autonomously by resolving
model divergences against the same objective.

**Integrity boundary (must be reported):** an objective-selected construct is an
**operational / engineered** construct ("the labeling that best serves the objective"),
NOT necessarily the theoretical psychological trait. Do NOT claim it *is* "openness"
in the textbook sense unless it also passes a **construct-validity cross-check**
(agreement with the multi-LLM textbook definition and/or a public per-rater set).

---

## Part 4 — Ground truth & the autonomy license

For ANY construct, correctness is anchored **once, externally**, then trusted:

1. **Autonomy license (mandatory, one-time, engine-level).** Run the full autonomous
   engine on a **battery** of public **per-rater** datasets (DICES / POPQuorn /
   GoEmotions / LeWiDi — junjie P02) on THEIR native constructs. Assert engine κ ≥
   human ceiling. Passing earns the right to run autonomously on new constructs where
   no human labels exist. **The more diverse the battery, the wider the license.**
2. **Per-project, on new data (no human truth):** measure what CAN be measured without
   a ceiling —
   - **reliability**: panel-internal κ (multi-LLM agreement)
   - **stability**: guideline version plateau
   - **generalization**: fresh held-out each round (anti-circularity)
   - **objective score**: downstream predictive / discriminance validity
   Correctness-vs-human is NOT claimed per-project; it is inherited from the license,
   scoped to constructs adjacent to the battery.

**Role of multi-LLM (junjie):** the labeler + the reliability signal. It is NOT ground
truth (models share priors; agreement ≠ correctness). Ground truth lives in the public
battery, once.

---

## Part 5 — Three sets, distinct jobs (never merged)

| Set | Changes? | Job | Origin |
|---|---|---|---|
| **rolling batch** | every round | active-learning: mine hard cases, grow the gallery | junjie — keep |
| **fixed anchor** | frozen, representative, ≥100 | version-to-version comparison | new |
| **held-out** | fresh each round, never trained on | honest generalization + anti-circularity | new |

The meeting's "random 24 each round" is the wrong evaluation set (confounds version
comparison + high variance). It survives only as the *rolling batch* for refinement.

---

## Part 6 — General contract (config-driven, zero hardcoding)

```yaml
task:      {corpus_path, text_field, id_field}
construct:
  mode: auto | seed            # auto = multi-LLM propose + objective-select; seed = human one-liner
  seed_definition: null | "..."
  discriminant_from: [...]     # sibling constructs → confound strata + discriminance objective
objective:                     # the selection/stop criterion (the irreducible human input)
  kind: downstream | discriminance | dataset_match
  spec: {...}                  # e.g. downstream target = opioid_rx regression
labels: null | [values...]
labeler: {panel: [model...], validator_model: <≠ labeler>}   # F1: validator ≠ labeler
sampling:
  representative: {size, base_rate_aware: true, none_quota}
  enriched:       {per_stratum}                              # discriminant_from-driven
embedding: {backend, model}
eval:  {anchor:{size, frozen}, heldout:{size, fresh}}
metrics: [reliability_panel_kappa, executor_independence, generalization_gap, objective_score]
license: {battery: [popquorn, dices, ...], require_ceiling: true}   # Part 4
convergence: {objective_plateau, stability, heldout_gap_max}
escape_hatch: {extreme_case_review: on|off}
```

---

## Part 7 — Autonomous pipeline

```
0 profile + base-rate probe    ← probe lexicon auto-generated from construct.definition
1 construct                    ← mode=auto: multi-LLM propose N → label sample →
                                 objective-select → refine by resolving divergences
                                 (mode=seed: human one-liner instead)
2 label                        ← multi-LLM panel labels; validator model ≠ labeler
3 refine loop                  ← classifier uncertainty mines rolling batch → guideline vN
4 measure (per-project)        ← reliability + stability + held-out generalization + objective score
5 converge   when: objective plateau ∧ stability ∧ held-out gap < ε
6 scale                        ← classifier + cascade over full corpus; flag class imbalance
                 ── ENGINE LEVEL, once ──
L license                      ← run whole engine on public per-rater battery; assert κ ≥ ceiling
```

Human touches: `objective` (once, from research design), license sign-off (once),
optional extreme cases. Nothing else.

---

## Part 8 — Generalizing junjie's assets (hardcoded → mechanism)

| junjie (openness-specific) | Generalize to |
|---|---|
| `probe_base_rate.py` hardcoded lexicon | **construct→probe generator** (LLM derives lexicon from `construct.definition`) |
| `sample_candidates.py` confound strata | **`discriminant_from`-driven** confound strata |
| P02 datasets | **autonomy-license battery** + registry-match |
| P01 executor-independence | generic **clarity** metric |
| B01–B03 labeler/kappa/iterate | promote to `lib/label.py` + `lib/kappa.py` (canonical, de-physician-ized) |

---

## Part 9 — Skill changes (commit-sized, ordered)

| Step | Change | Files | Fixes |
|---|---|---|---|
| **S0** | canonical engine: `lib/label.py` (multi-engine labeler, validator≠labeler) + `lib/kappa.py` | new lib | base |
| **S1** | config contract (Part 6); strip hardcoding | `ref/ref-config.md`(new), `sl-init` template, `INIT.md` | F2 |
| **S2** | construct auto-selection: `lib/construct.py` (multi-LLM propose → objective-score → select + divergence report) | new lib, `moderator`/`INIT.md` | Part 3 |
| **S3** | metrics split: `lib/kappa.py` emits reliability / executor-independence / generalization / objective-score | `lib/kappa.py`, `ref-output-style.md` | F4 |
| **S4** | three sets + convergence gate (held-out + objective) | `INIT.md`, `sl-init`, `sl-iterate`, `moderator` | F7,F8 |
| **S5** | base-rate two pools + construct→probe; hard-case via classifier (not embedding); delete "guideline reshapes embedding" | `lib/sample.py`(new), `sampler-agent`, `ref-schema` | F5,F6 |
| **S6** | autonomy license battery + registry-match on public per-rater sets | `sl-validate`, `validator-agent`, `ref-datasets`→registry, `lib/license.py`(new) | F1,F2,F3 |

Dependency: S0 → {S2, S3}; S1 → S2; S2 → S4; S5 ∥ (S2–S4); S6 last (needs S3).

---

## Part 10 — Honesty boundaries (research integrity — do not skip)

1. **Operational ≠ theoretical construct.** An objective-selected construct must be
   reported as an engineered feature, not the psychological trait, unless it passes a
   construct-validity cross-check (textbook + public per-rater).
2. **Objective-gaming.** An auto-selected construct can exploit confounds → guard with a
   **downstream held-out** (does it still predict on unseen data?).
3. **License coverage.** Autonomy is only as trustworthy as the public battery's coverage
   of the target construct space. Report the battery + the adjacency of the target.
4. **Circularity residue.** Same models proposing + labeling + selecting can self-serve →
   held-out + objective (external anchor) + validator≠labeler are mandatory, not optional.

---

## Part 11 — Open decisions

- **Objective function**: can we wire the ProjB opioid-Rx regression (or a proxy) as the
  construct-selection objective now? If not, fall back to discriminance-only until it's available.
- **License battery**: which public sets, how many, how diverse (defines autonomy width).
- **Numbering/construct** for the physician instance (two `B02_*`; adopt narrow+curiosity as the seed OR let auto-select decide).

---

## Part 12 — Implementation status (2026-07-21)

Engine code + docs for S0–S6 **built and unit-tested** (5 lib selftests green;
`label.py` parser verified — no selftest since it needs OAuth). All in
`plugins/subjective-label/`, **uncommitted**.

| step | built | tested |
|------|-------|--------|
| S0 canonical `lib/label.py` + `lib/kappa.py` | ✅ | B03 reproduces Cohen κ 0.9322 · binary/5-pt run |
| S1 `ref/ref-config.md` + sl-init align | ✅ | non-physician (sarcasm) config expressible |
| S2 `lib/construct.py` (discriminance×info select) | ✅ | good wins · redundant/degenerate → 0 |
| S3 `kappa.py` executor_independence | ✅ | three signals separated |
| S4 `lib/converge.py` + three-set / held-out gate | ✅ | catches the B03 OVERFIT (0.93/0.67) trap |
| S5 `lib/sample.py` base-rate + two pools | ✅ | real corpus 6.6% · enriched strata |
| S6 `lib/license.py` + registry + sl-validate | ✅ | good agent PASS / random BELOW |

**NOT yet done = real runs (execution, not engine code):**
- establish the autonomy license on REAL public data (download POPQuorn/DICES → run engine → `lib/license.py`)
- construct auto-selection on the physician instance (needs `objective` wired — discriminance now, opioid-downstream when the regression/PHI is accessible)
- the LLM `construct→probe` lexicon generation that feeds `lib/sample.py`
- the ≥2nd-annotator / objective decisions in Part 11

## Related files

- `plugins/subjective-label/skills/*/SKILL.md`, `skills/subjective-label/INIT.md`
- `plugins/subjective-label/lib/{embed,classify}.py` (+ new label/kappa/sample/construct/license)
- `plugins/subjective-label/ref/ref-datasets.md` → registry/battery
- `examples/Project-Subjective-Label/discoveries/P02_external-validation-datasets/` — battery audit
- `examples/Project-Subjective-Label/tasks/B02_dim_openness/` — junjie's base-rate scaffold (to generalize)
- `examples/Project-Subjective-Label/tasks/B03_dim_openness/` — full-run engine instance (κ inflated by non-representative anchor)
