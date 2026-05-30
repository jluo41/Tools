Narrative Schema — Canonical Spec
===================================

Authoritative shape for every file under `examples/<project>/narratives/`.
The `haipipe-narrative` skill writes files that conform to this. Mirrors the
discipline of `E_insight/ref/insight-md-schema.md`: tight frontmatter,
reference-by-ID (never copy), pure markdown, no code.

A narrative folder holds FOUR files:

```
narratives/<NN>_<slug>/
├── story.md          the angle (the NOUN)
├── claims.md         needed K cards by reference + GAP/weak ledger
├── ignite-log.md     ③ append-only "am I ignited?" judgments
└── decision-tree.md  section paths A/B/C/D
```


ID & naming
===========

```
id:     N + 2-digit, project-scoped, no gap on creation  (N01, N02, ...)
folder: narratives/<NN>_<slug>/   (NN = 2-digit, snake_case slug)
```

Cross-reference style: `narrative N01` or `[N01]` in prose.


story.md
========

The angle. The single load-bearing file.

```markdown
---
id:        N01
layer:     narrative
slug:      fairness_angle
status:    exploring | igniting | ready | shelved
created:   YYYY-MM-DD
updated:   YYYY-MM-DD
tags:      [fairness, conditioning]
papers:    []                      # paper ids that render this story (back-ref)
---

# N01: <one-line story title>

## Angle
<1-2 paragraphs: the lens. The surprising / important framing.>

## Why it matters
<who cares, and why now. The "eager to sell this" test.>

## Core claim (one sentence)
<the single sentence this story exists to defend>
```

`status` enum:

| status    | meaning                                                        |
|-----------|---------------------------------------------------------------|
| exploring | still finding the angle; KB→N induction phase                 |
| igniting  | angle found; accumulating claims; ignite judgments running    |
| ready     | ignited enough to sell → eligible for narrative-report → paper |
| shelved   | dropped (reason recorded in ignite-log)                        |

Length budget: ≤ 60 lines.


claims.md
=========

The N→KB interface. The GAP/weak rows ARE the "which probe to crack next"
list. `needs[]` references K cards BY ID — never copies their content.

```markdown
# N01 — claims ledger

## Needed (what the story must defend)
| slot | claim (free text)                | KB card | status |
|------|----------------------------------|---------|--------|
| C1   | FiLM helps in-distribution       | K03     | have   |
| C2   | benefit survives param-matching  | —       | GAP    |
| C3   | holds on test-od                 | K05     | weak   |

## Gap summary
- C2: no K card → candidate next probe: param-matched re-test
- C3: K05 exists but confidence=low → strengthen or re-scope
```

Per-slot `status`:

| status | meaning                                                  |
|--------|----------------------------------------------------------|
| have   | a K card matches AND confidence high/medium              |
| weak   | a K card matches BUT confidence low/contested            |
| GAP    | no K card matches                                        |

Rules:
- slot ids (C1, C2, …) are per-narrative (C1 in N01 ≠ C1 in N02).
- `KB card` column holds a K id or `—`. Never inline the claim text from K.
- The `claims` verb re-derives `status` by reading insights/K; humans set
  the `needed` rows.


ignite-log.md
=============

The heart: each entry is one round-trip across the KB⇄Narrative arrow.
APPEND-ONLY — never rewrite past judgments. Honest "NO" entries are what
stop motivated reasoning (wanting to be ignited just to start writing).

```markdown
# N01 — ignite log (append-only)

## YYYY-MM-DD — after probe 01 (FiLM in-dist confirmed)
- ignited? YES
- why: in-dist effect is clean (K03 high-conf); the "conditioning helps the
  hard sub-population" angle suddenly feels sellable
- next: crack probe for C2 (param-matched) to kill the scale confound

## YYYY-MM-DD — after probe 02 (param-matched null)
- ignited? NO
- why: param-matched result is null → the angle's spine (C2) is gone
- decision: re-scope to "in-dist-only" claim (chose re-scope, not shelve)
```

Each entry MUST have: a date + trigger header, `ignited?` (YES/NO), `why`,
and `next`/`decision`. New entries are appended at the bottom.


decision-tree.md
================

Section paths. Each major section can go down one of several paths; the
chosen spine is what stitches them into one coherent story.

```markdown
# N01 — section decision tree

## Intro
- [x] A. "fairness gap in CGM forecasting"   (chosen)
- [ ] B. "personalization angle"
## Method
- [x] A. FiLM conditioning
- [ ] B. mixture-of-experts
## Results spine
- [x] in-dist win + honest od-limitation   ← the thread tying the [x] paths together
```

Use `[x]` for the chosen path per section, `[ ]` for alternatives kept on
the table. The "Results spine" (or a final note) names the thread that ties
the chosen paths into one story.


Validation rules (any file)
===========================

- YAML frontmatter (story.md) parses.
- `id` matches the folder NN and starts with `N`.
- `claims.md` `KB card` entries are K ids that exist in insights/K, or `—`.
- `ignite-log.md` is append-only (new entries at the bottom; never edit old).
- No code, no notebooks, no `[[wikilinks]]` — pure standard markdown.
- Reference K/W cards by ID; never copy their body text.
- story.md `papers:` back-ref is consistent with each paper's `narrative:` meta.


INDEX.md (project-level, auto)
==============================

```markdown
# Narratives — INDEX

| id  | slug          | status   | claims (have/weak/GAP) | last ignite | papers   |
|-----|---------------|----------|------------------------|-------------|----------|
| N01 | fairness_angle| igniting | 1 / 1 / 1              | YES (05-30) | —        |
| N02 | robustness    | exploring| 0 / 0 / 2              | —           | —        |
```

Rebuilt by `status` / `new` / `claims` / `ignite`. Derived; not a source of
truth — the per-narrative files are.
