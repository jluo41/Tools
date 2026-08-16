---
name: label-init
description: "Initialize a human-grounded subjective-labeling project from a large text corpus, vague trait idea, and one human semantic authority. Reserve a sealed final test, embed the development corpus, draw a random 50–60-item Round 1 batch, conduct resumable human-first labeling, draft the guideline, and close checkpoint G_1/D_1. Use for /label-init or a new subjective labeling project."
---

# Initialize a subjective-label project

Create the project and conduct Round 1 without assigning semantic authority to models,
embeddings, clusters, or prior taxonomies.

## Read first

Read:

- `../../../ref/ref-contract.md`
- `../../../ref/ref-config.md`
- `../../../ref/ref-schema.md`
- `../../../ref/ref-stages.md`
- `../../../ref/ref-assets.md`
- `../../../ref/ref-architecture.md`
- `../../../ref/ref-embeddings.md`
- `../../../ref/ref-output-style.md`

## Inputs

Resolve or elicit only what is needed:

- corpus path, stable id field, text field, and target population;
- vague subjective trait seed and scope;
- identified human semantic authority;
- project directory;
- project-specific batch size, sealed-test design, and embedding configuration.

Use H/L/N as terminal labels and H, L, N, HL, LN, HN, HLN as diagnostic regions
unless the human explicitly changes the schema. Keep uncertainty separate from `NONE`.

## Protocol

1. **Inspect before writing.** Detect an existing project, partial initialization,
   corpus-id collisions, legacy artifacts, and required implementation capabilities.
   Resume a valid partial phase; do not overwrite closed artifacts.
2. **Create the project contract.** Write `config.yaml`, corpus manifest, append-only
   item records, `.state.json`, and the v2 directory scaffold from `ref-assets.md`.
3. **Reserve the final test.** Before embedding, retrieval, or semantic development,
   have the Test Custodian sample and protect test ids. Record design and access policy,
   but do not create test labels or expose ids to development agents.
4. **Prepare the development corpus.** Exclude sealed ids. Compute and cache embeddings
   with complete model and text-checksum provenance. Embeddings are retrieval-only.
5. **Freeze Round 1.** Draw approximately 50–60 items randomly from the eligible
   development pool using the declared seed and inclusion probabilities. Freeze `B_1`.
   Do not prelabel, region-score, cluster-select, or import prototypes.
6. **Run a resumable Human-AI Session.** For each item, record the human's initial
   H/L/N judgment, diagnostic region, uncertainty, evidence, and rationale. The Strong
   Calibration Agent asks contrasts and consistency questions, identifies implicit
   boundaries, and maintains a draft guideline. It never decides for the human.
7. **Generalize the draft.** Convert item-specific reactions into definitions,
   boundary tests, ordered procedure, uncertainty/escalation rules, and a compact
   generalized casebook. Preserve verbatim examples only with provenance and purpose.
8. **Close checkpoint 1.** Require complete Session events, human confirmation,
   consistency checks, policy diff, and checksums. Promote only human-confirmed records
   to `D_1`; publish only a closed `G_1` to `policy/current`.
9. **Render status.** Refresh `REPORT.md`, cumulative-gold view, policy cheatsheet, and
   Round 1 report from canonical records.

## Interaction gates

Pause for the human whenever an item, label meaning, boundary, or policy change requires
semantic judgment. A paused Session is normal. Record phase and next item so the command
can resume without replaying completed decisions.

## Completion result

Return:

- corpus and sealed-test counts;
- Round 1 sample design and completed human decisions;
- closed `D_1` and `G_1` identifiers and checksums;
- unresolved risks or implementation holds;
- next valid action: `/label-round` or resume `/label-init`.

If sealing, provenance, interactive event recording, or checkpoint promotion is not
implemented, emit `HOLD`. Do not manufacture labels, regions, guideline versions, or a
successful checkpoint.
