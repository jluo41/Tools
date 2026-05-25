---
name: haipipe-insight-information
description: "I-level patterns specialist of the haipipe-insight family. Reads multiple D_observations entries and synthesizes cross-observation patterns into markdown entries at insights/I_patterns/. NO code execution — pure markdown synthesis. Looks for statistical regularities, repeated effects, paired contrasts across experiments. Use when running I-phase via /haipipe-insight-session, or directly /haipipe-insight-information. Trigger: I-level, patterns, cross-experiment patterns, regularities, what trends emerge."
argument-hint: [--project <path>] [--scope <observation-ids>] [--slug <slug>]
allowed-tools: Bash, Read, Write, Edit, Grep, Glob, Skill
---

Skill: haipipe-insight-information
================================

I-level of the Insight base (D → I → K → W). Reads multiple
`D_observations/O*.md` entries and synthesizes the **cross-observation
patterns** that emerge: statistical regularities, repeated effects,
paired contrasts.

```
D — Observations: "what we observed"          (input)
I — Patterns:     "what patterns emerged"     ← THIS SKILL
K — Knowledge:    "what we now believe"
W — Wisdom:       "what we should do next"
```


Input
-----

```
examples/<project>/insights/D_observations/O*.md   (REQUIRED, ≥ 2 entries)
examples/<project>/experiments/<NN>_<slug>/        (read-only, for back-refs)
```


Output
------

```
examples/<project>/insights/I_patterns/P{NN}_<slug>.md
```


Hard rules
----------

- NO Python execution. Patterns are extracted by **reading** multiple
  D entries and noticing regularities — not by running statistics.
- The statistical work (paired-t, sign-test, effect sizes) was already
  done in D_experiment at result-aggregate time. This skill READS those
  numbers and synthesizes the pattern.
- If a pattern needs NEW computation (e.g. a meta-analysis across
  experiments not yet computed), scaffold an eval task in C_task. Never
  inline here.
- A pattern must cite ≥ 2 source D entries (otherwise it's just an
  observation, not a pattern).


Workflow
--------

```
Step 1: Parse args
  - --project <path>          optional, else cwd-inferred
  - --scope <O01,O02,...>     optional; restrict to specific D entries
  - --slug <slug>             optional, descriptive name for the pattern

Step 2: Resolve paths
  - project root              from arg or cwd
  - d_dir                     examples/<project>/insights/D_observations/
  - i_dir                     examples/<project>/insights/I_patterns/

Step 3: Scan D entries
  - Read all (or scoped) D_observations/O*.md files
  - Build a mental table: per-experiment metric / split / Δ / direction
  - Surface candidate patterns: same metric across experiments, same
    direction across seeds, etc.

Step 4: Triage patterns (interactive default; --auto skips ASK)
  - Present candidate patterns ranked by evidence-strength
  - User picks which to materialize (or --slug forces one)

Step 5: Pick output NN
  - List existing I_patterns/P*.md
  - NN = max existing + 1

Step 6: Compose entry (markdown only)
  - Per the entry schema below

Step 7: Write
  - insights/I_patterns/P{NN}_<slug>.md (atomic)
  - Update insights/INDEX.md
  - Back-link: append "linked patterns: P{NN}" to each cited D entry's
    Cross-references section
```


Entry schema
------------

Canonical schema: **`../../ref/insight-md-schema.md`** (see "I layer" section).

Quick reminder for I entries:

```
frontmatter (≤ 13 lines):
  id, layer=I, tags, status, created, updated,
  pattern, n_obs, direction,
  sources, ref_by

body sections (in order):
  ## Pattern statement   (1-3 sentences: the invariant)
  ## Evidence            (table: Source O / Metric / Δ / Direction)
  ## Counter-evidence    (null/reversed findings; "none found" + reason if so)

length: ≤ 120 lines total
```

The `pattern` enum is one of: `statistical_regularity | repeated_effect
| paired_contrast | null_finding`. `direction` is the overall direction
across cited O entries.


Definition of done
-------------------

- [ ] `insights/I_patterns/P{NN}_<slug>.md` written, non-empty
- [ ] Evidence table cites ≥ 2 D entries with concrete numbers
- [ ] Non-confirming evidence section honestly populated (or "none found"
      stated explicitly with rationale)
- [ ] NO Python file written, NO script executed
- [ ] Back-link added to each cited D entry's Cross-references section
- [ ] `insights/INDEX.md` updated


Disambiguation
---------------

- fewer than 2 D entries to draw from → REFUSE; suggest running
  /haipipe-insight-data on more experiments first
- proposed pattern actually visible in only 1 D entry → REFUSE; report
  as observation not pattern
- new statistical computation needed → STOP; recommend C_task eval
  scaffolding


Risk profile
-------------

WRITES one new file under `insights/I_patterns/`. APPENDS to
`insights/INDEX.md`. APPENDS one back-link line to each cited D entry.
Read-only on experiments/ and tasks/.


Specialist tail
---------------

```
status:    ok | blocked | failed
summary:   "P02_<slug> written from [O01, O03, O07]"
artifacts: [insights/I_patterns/P{NN}_<slug>.md, insights/INDEX.md,
            <back-linked D entries>]
next:      /haipipe-insight-knowledge to elevate pattern → validated knowledge
```
