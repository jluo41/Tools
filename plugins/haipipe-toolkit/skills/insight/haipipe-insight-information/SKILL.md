---
name: haipipe-insight-information
description: "I-level patterns specialist of the haipipe-insight family. Reads multiple D_data entries and synthesizes one reusable cross-observation pattern into insights/I_information/. NO code execution — pure markdown synthesis. Looks for statistical regularities, repeated effects, and paired contrasts across D cards. Use via /haipipe-insight review/apply, /haipipe-application ask, or directly /haipipe-insight-information. Trigger: I-level, patterns, cross-D patterns, regularities, what trends emerge."
argument-hint: "[--project <path>] [--scope <observation-ids>] [--slug <slug>]"
allowed-tools: Bash, Read, Write, Edit, Grep, Glob, Skill
metadata:
  version: "1.1.0"
  last_updated: "2026-06-20"
  summary: "I-level patterns specialist of the haipipe-insight family."
  changelog:
    - "1.1.0 (2026-06-20): clarified cross-D granularity; one reusable pattern per card."
    - "1.0.0 (2026-05-31): baseline metadata added."
---

Skill: haipipe-insight-information
================================

I-level of the Insight base (D → I → K → W). Reads multiple
`D_data/D*.md` entries and synthesizes the **cross-observation
patterns** that emerge: statistical regularities, repeated effects,
paired contrasts.
Each I card should contain ONE reusable pattern. If a candidate is a whole
topic summary, split it; if it duplicates an active I card, merge evidence
instead of filing a new card (see `../../ref/card-granularity.md`).

**Invocation modes** (see `../../ref/invocation-modes.md`): interactive (a
human steers; the triage ASK runs) OR headless (`--scope` ≥ 2 D ids + `--auto`
→ file silently), chosen by input completeness. `card-creator-information-agent`
calls this skill headless during fan-out; agent + < 2 D ids → `status: blocked`
(never hang). End with the structured return block.

```
D — Data:         "what we observed"          (input)
I — Information:      "what patterns emerged"     ← THIS SKILL
K — Knowledge:    "what we now believe"
W — Wisdom:       "what we should do next"
```


Input
-----

```
examples/<project>/insights/D_data/D*.md   (REQUIRED, ≥ 2 entries)
examples/<project>/probes/<GROUP>_<group_slug>/<NN>_<slug>/        (read-only, for back-refs)
```


Output
------

```
examples/<project>/insights/I_information/I{NN}_<slug>.md
```


Hard rules
----------

- NO Python execution. Patterns are extracted by **reading** multiple
  D entries and noticing regularities — not by running statistics.
- The statistical work (paired-t, sign-test, effect sizes) was already
  done in probe at result-aggregate time. This skill READS those
  numbers and synthesizes the pattern.
- If a pattern needs NEW computation (e.g. a meta-analysis across
  probes not yet computed), scaffold an eval task in task. Never
  inline here.
- A pattern must cite ≥ 2 source D entries (otherwise it's just an
  observation, not a pattern).
- A card must contain one reusable pattern. Broad summaries should split;
  reinforcing evidence for an existing pattern should merge.


Workflow
--------

```
Step 1: Parse args
  - --project <path>          optional, else cwd-inferred
  - --scope <D01,D02,...>     optional; restrict to specific D entries
  - --slug <slug>             optional, descriptive name for the pattern

Step 2: Resolve paths
  - project root              from arg or cwd
  - d_dir                     examples/<project>/insights/D_data/
  - i_dir                     examples/<project>/insights/I_information/

Step 3: Scan D entries
  - Read all (or scoped) D_data/D*.md files
  - Build a mental table: per-probe metric / split / Δ / direction
  - Surface candidate patterns: same metric across probes, same
    direction across seeds, etc.

Step 4: Triage patterns (interactive default; --auto skips ASK)
  - Present candidate patterns ranked by evidence-strength
  - User picks which to materialize (or --slug forces one)

Step 5: Pick output NN
  - List existing I_information/I*.md
  - NN = max existing + 1

Step 6: Compose entry (markdown only)
  - Per the entry schema below

Step 7: Write
  - insights/I_information/I{NN}_<slug>.md (atomic)
  - Update insights/INDEX.md
  - Back-link: append "linked patterns: I{NN}" to each cited D entry's
    Cross-references section
```


Entry schema
------------

Canonical schema: **`../../ref/insight-md-schema.md`** (see "I layer" section).

Quick reminder for I entries:

```
frontmatter (≤ 16 lines):
  id, type=Insight Information, layer=I, title, description,
  tags, status, created, updated,
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
across cited D entries.


Definition of done
-------------------

- [ ] `insights/I_information/I{NN}_<slug>.md` written, non-empty
- [ ] Evidence table cites ≥ 2 D entries with concrete numbers
- [ ] Non-confirming evidence section honestly populated (or "none found"
      stated explicitly with rationale)
- [ ] `## Change log` records creation source or meaningful update
- [ ] NO Python file written, NO script executed
- [ ] Back-link added to each cited D entry's Cross-references section
- [ ] `insights/INDEX.md` updated


Disambiguation
---------------

- fewer than 2 D entries to draw from → REFUSE; suggest running
  /haipipe-insight-data on more probes first
- proposed pattern actually visible in only 1 D entry → REFUSE; report
  as observation not pattern
- new statistical computation needed → STOP; recommend task eval
  scaffolding


Risk profile
-------------

WRITES one new file under `insights/I_information/`. APPENDS to
`insights/INDEX.md`. APPENDS one back-link line to each cited D entry.
Read-only on probes/ and tasks/.


Specialist tail
---------------

```
status:    ok | blocked | failed
summary:   "I02_<slug> written from [D01, D03, D07]"
artifacts: [insights/I_information/I{NN}_<slug>.md, insights/INDEX.md,
            <back-linked D entries>]
next:      /haipipe-insight-knowledge to elevate pattern → validated knowledge
```
