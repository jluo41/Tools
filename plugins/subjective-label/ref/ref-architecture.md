Reference: Multi-Agent Panel Architecture
==========================================

The full protocol for how skills, agents, and personas collaborate.


Topology
--------

```
Researcher (PI)
    │
    │  talks only to
    ▼
┌──────────────┐
│  Moderator   │  state machine + only researcher-facing agent
└──────┬───────┘
       │ orchestrates via Task tool
       │
       ├──> Sampler              (stage-aware: init_map, iterate_batch, validate_heldout, scale_preflight, diagnostic)
       │       │ uses
       │       ├──> Embedder     (sentence-transformers / OpenAI / FAISS)
       │       └──> Classifier   (logreg / SetFit; trained on gallery)
       │
       ├──> Boundary Prober      (LLM-judgment layer on Sampler's candidate pool)
       │
       ├──> Labeler Panel        (spawns 3-5 personas)
       │       ├── close-reader
       │       ├── fast-patterns
       │       ├── skeptic
       │       ├── plain-reader
       │       └── domain-expert (conditional)
       │
       ├──> Disagreement Analyzer   (categorizes A/B/C/D)
       ├──> Gallery Keeper          (sole writer of gallery/guideline)
       │
       ├──> Classifier              (trained after every /sl-iterate; serves Tier 1 of cascade)
       │
       ├──> Embedder                (serves Tier 0 of cascade; used by Sampler, Gallery Keeper, Validator)
       │
       └──> Validator               (public dataset benchmarking)
```

See `ref/ref-stages.md` for the three-loop decomposition (big / medium / small).
See `ref/ref-cascade.md` for the three-tier cascade used in /sl-scale.


State machine
-------------

```
initialized ──/sl-iterate──> iterating ──/sl-validate──> validating
                                 ▲                            │
                                 └────── STALLED / refine ────┤
                                                              ▼
                                                          CONVERGED
                                                              │
                                                         /sl-scale
                                                              ▼
                                                           scaled
```

Stored in `{project_dir}/.state.json`:
```json
{
  "status": "iterating",
  "iteration": 3,
  "last_validation": {"dataset": "goemotions", "kappa": 0.42, "iter": 3},
  "last_guideline_update": 3,
  "gallery_size": 18,
  "created_at": "2026-04-24T...",
  "updated_at": "..."
}
```


Skill × Agent call graph
------------------------

| Skill          | Agents invoked (in order)                                                                  |
|----------------|--------------------------------------------------------------------------------------------|
| `/sl-init`     | moderator → sampler(init_map) → embedder → prober → moderator → gallery-keeper             |
| `/sl-iterate`  | moderator → sampler(iterate_batch) → embedder + classifier → prober → labeler-panel → disagreement-analyzer → moderator → gallery-keeper → classifier(train) → embedder(rebuild index) |
| `/sl-validate` | moderator → sampler(validate_heldout) → validator → labeler-panel → moderator              |
| `/sl-scale`    | moderator → sampler(scale_preflight) → labeler-panel(scale, cascade) → embedder + classifier (tier 0/1) → labeler-panel (tier 2) |
| `/sl-status`   | (no agents — pure file read)                                                                |


Disagreement categorization (Analyzer output)
---------------------------------------------

| Category | Meaning                                      | Who resolves     | Surfaces to researcher? |
|----------|----------------------------------------------|------------------|--------------------------|
| A        | Boundary case (genuinely subjective edge)    | Researcher       | Yes — "what's the label?" |
| B        | Rule ambiguity (guideline underspecified)    | Researcher       | Yes — "refine the rule"   |
| C        | Novel pattern (schema gap)                   | Researcher       | Yes — "new label?"        |
| D        | Noise (one persona careless)                 | Panel majority   | No — auto-resolved        |


Persona selection policy
------------------------

Labeler Panel selects 3-5 personas per iteration:

- Mandatory: `close-reader`, `plain-reader`, `skeptic`
- Conditional: `fast-patterns` (include for large batches / cascade)
- Conditional: `domain-expert` (include if config.yaml specifies a domain)

Panels can vary per iteration, but consistency helps. Panel composition is
logged in `{project_dir}/panel_config.json` per iteration.


Researcher interaction budget
-----------------------------

Per iteration, the researcher sees AT MOST:
- 3-5 Category A items to adjudicate
- 1-3 Category B rule-refinement asks
- 0-2 Category C schema-gap asks

Total: ~5-10 decisions per iteration. A convergent project typically runs
3-6 iterations, meaning ~20-60 researcher decisions total — vs. labeling
the whole batch themselves.


Convergence signals
-------------------

Three signals, in order of authority:

1. **Public-dataset κ** (Validator): agent κ ≥ human κ ceiling on GoEmotions / MFTC / POPQuorn / DICES. This is the primary signal.
2. **Panel-internal κ** (Labeler Panel): pairwise κ across personas > 0.7 AND plateau across 2 iterations.
3. **Category D ratio** (Analyzer): D / (A+B+C+D) > 0.7 suggests most disagreement is noise, i.e. guideline is mature.

Moderator reports all three. Researcher decides when to /sl-scale.


File conventions
----------------

All agents write to `{project_dir}/` subfolders. No agent writes to plugin
source files. The gallery and guideline are the canonical artifacts.
Everything else (panel_labels, disagreement_items, batch.jsonl, etc.) is
regenerated per iteration and kept for audit.


Traceability
------------

Every gallery entry has `provenance` and `added_iteration`. Every guideline
rule links to the gallery item(s) that motivated it. Every decision
surfaced to the researcher is logged with the researcher's reasoning. This
gives a complete audit trail: for any final label, you can trace back to
which persona voted what, what the Analyzer categorized it as, what the
researcher decided, and which guideline rule applied.
