Report template — applications/ask/<NN>/report.md
====================================================

Every ask-session report MUST follow the DIKW-spine template below.
The spine makes the report's epistemological depth visible to the
reader (D = measured / I = patterns / K = validated claims /
W = recommendations) and lets future sessions cite specific blocks
instead of paragraph-mining freeform prose.

Composed by `haipipe-application-plan compose report`. Enforced by
`haipipe-application-ask` Phase 4 step C and the G-report HARSH gate.


Top of file (always present)
=============================

```
Application: ask · <one-line subject + topic>
==============================================

Session:     <session-folder relative path>
Subject:     <subject store path, if --individual>
Asked at:    <date>  (persona, attendance, --auto if used)
Data cut:    <SESSION_STATE.data_cut>
Question:    "<verbatim question from question.md>"
```


Answer (TL;DR) — first 20 lines
================================

3-7 sentences. Plain prose. Lead with the *answer*, not the
methodology. If the report is descriptive only (no K/W cards), the
TL;DR ends with a one-sentence honesty signal:

  "This report is descriptive (D + I only) — no causal claims."


Per-layer blocks (in order: D, I, K, W)
========================================

For each filed insight card the session produced, emit ONE block
under the matching layer header. Order within a layer: by card id
ascending (D01, D02, ...).

Block structure — 5 elements, in this order:

```
<layer>NN · <card headline>
─────────────────────────────

Illustration                             ← from card source_artifact
  ![<caption>](<relative-path-to-figure>)
  (or: "n/a — no figure produced")

Table                                    ← verbatim from card body
  | metric | value | target | verdict |
  | ...    | ...   | ...    | ...     |

Narrative                                ← 2-4 sentences interpreting the table
  <prose>

Source
  card:      insights/<L>_<folder>/<L>NN_<slug>.md
  artifact:  tasks/<...>/results/<RUN>/   OR   experiments/<NN>_<slug>/
  yields:    <task or experiment id, e.g. T1, E12>
```

Figure paths in `![](...)` MUST be file-relative (relative to
report.md's own location), so standard markdown viewers (Obsidian,
GitHub, VS Code preview) render the image inline. From a session
folder at `applications/ask/<NN>/`, a task figure is reached as
`../../../tasks/<...>/results/<RUN>/<fig>.png` (three `../` to
reach PROJECT_ROOT, then down). The HTML render step (Phase 4 step
E, future) will re-resolve these to absolute or base64-embed.


Empty layers (descriptive sessions, etc.)
==========================================

If a layer produced zero cards this session, the block is NOT
omitted — emit the canonical "no cards" placeholder so the
report's honest scope is visible:

```
K · Knowledge
─────────────
(no experiments triggered in this session; no validated claims
filed. Promotion to K requires D_experiment evidence — open a new
ask session with experiment_batch populated to elevate the I-level
patterns above.)
```

Same convention for empty W:

```
W · Wisdom
──────────
(no recommendations filed. W cards require either a K-level claim
to act on OR a strategic synthesis spanning multiple K cards.)
```

Silently dropping K/W hides the report's epistemological scope and
is a G-report violation.


Trailing sections
==================

```
Did we answer the original question?
─────────────────────────────────────
Verdict: Yes / Partial / No

  Answered:  <one sentence — what the report resolves>
  Deferred:  <one sentence — what wasn't covered and why>
  Open:      <one sentence — what remains for a follow-up session>

Provenance
───────────
  plan_version:    <N>
  gates fired:     G-design (approve), G-observe (approve), ...
  data_cut:        <tag>
  contract_path:   data/contract.yaml
  full state:      SESSION_STATE.json
```


Invariants (G-report HARSH gate)
=================================

1. Header block exists and includes Data cut + Question verbatim.
2. TL;DR exists and is <= 20 lines.
3. Every card listed in plan.insight_yield has a corresponding block
   under the matching layer header.
4. Every block has all 5 elements (illustration may be the literal
   string "n/a — no figure produced"; other 4 cannot be empty).
5. Source paths in every block resolve on disk.
6. Empty layers carry the canonical placeholder, not omission.
7. "Did we answer..." trailing section is non-empty; verdict is one
   of {Yes, Partial, No}.

Failure of any invariant → G-report outcome forced to
`revise "report template invariant <N> violated"`.


Cross-references
=================

```
haipipe-application-ask/SKILL.md          Phase 4 step C invokes this template
haipipe-application-plan/SKILL.md         "compose report" mode produces it
haipipe-application/ref/session-state-schema.md
                                          data_cut, contract_path source fields
haipipe-application/ref/data-contract-schema.md
                                          available.md powers the Provenance block
```
