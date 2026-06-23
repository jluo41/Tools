---
name: haipipe-insight-knowledge
description: "K-level knowledge writer API of the haipipe-insight family. Files one judged claim as a validated belief in insights/K_knowledge/ from a approved by review probe/lit/review source; cites supporting I_information entries where they exist. NO code, pure markdown synthesis. Prefer /haipipe-insight review; call directly only with a complete judged source spec."
argument-hint: "<source_ref> [--id K<NN>] [--project <path>] [--supports <I-ids>] [--slug <slug>]"
allowed-tools: Bash, Read, Write, Edit, Grep, Glob, Skill
metadata:
  version: "1.2.0"
  last_updated: "2026-06-20"
  summary: "K-level knowledge writer API of the haipipe-insight family."
  changelog:
    - "1.2.0 (2026-06-20): repositioned as review-called judged-source writer API."
    - "1.0.0 (2026-05-31): baseline metadata added."
    - "1.1.0 (2026-05-31): K sources a confirmed probe's claim (was >=1 I card); cites supporting I cards in the body."
---

Skill: haipipe-insight-knowledge
=================================

K-level of the Insight base (D → I → K → W). This writer files one GENERALIZATION
claim as a K card: does an in-sample pattern (an I card) hold beyond the sample,
and with what confidence. The generalization basis is the inferential evidence —
a significance test (p / CI), robustness across subgroups/cohorts/time, or a
vetted literature/review claim. NO probe is required. Prefer
`/haipipe-insight review ...`; direct calls are the low-level writer path.

**Invocation modes** (see `../../ref/invocation-modes.md`): interactive (a
human steers; may tighten the claim wording) OR headless (a claim + basis +
confidence → file silently), chosen by input completeness. Review apply or
`card-creator-knowledge-agent` calls this skill headless during fan-out; agent
+ no claim / no generalization basis → `status: blocked` (never hang). A low or
negative confidence is NOT a block — it is recorded. End with the structured
return block.

```
D — Data:         "what one dataset looks like"
I — Information:  "the pattern inside that dataset"  (input)
K — Knowledge:    "does it generalize, + confidence" ← THIS SKILL
W — Wisdom:       "what to do, tuned to confidence"
```

K differs from I in scope: I describes the pattern in THIS sample, K commits to
"the pattern holds beyond the sample (scope Y, confidence Z)". The p-value / CI /
confidence live at K, never at I.


Input
-----

```
From `INSIGHT_REVIEW.yaml`, a generalization claim + its basis + a confidence:
  the I card(s) whose in-sample pattern is being generalized (sources)
  a generalization basis, one of:
    a significance test on the pattern (p / CI)
    robustness across subgroups / cohorts / time windows
    probe:<probe-id-or-path>       (a judged probe verdict, when one exists — optional, not required)
    lit:<citekey>                  (vetted literature/review claim)
    discover:<note-id-or-path>     (reviewed synthesis claim)
  a confidence level (high / medium / low / contested)
```


Output
------

```
examples/<project>/insights/K_knowledge/K{NN}_<slug>.md
```

May also UPDATE an existing K entry (if new patterns reinforce or refute
an existing belief).


Hard rules
----------

- NO Python. NO statistical computation. The inferential numbers (p / CI /
  robustness) were produced upstream by the task/probe that fit the model; this
  layer reads them and commits to a generalization belief with confidence.
- A K entry must list ALL contradicting evidence (counter-findings + any I/D
  counter-evidence). Cherry-picking is a violation.
- Confidence is qualitative (high / medium / low / contested), ALWAYS present,
  and justified in the body. A low or negative confidence is recorded, not withheld.
- K granularity is one scoped belief/claim per card. If the candidate is a
  topic essay, split it; if it reinforces an active K, merge evidence instead
  of filing a duplicate (see `../../ref/card-granularity.md`).
- If a K entry would directly contradict an existing K entry, the new
  entry's "supersedes / contradicts" field MUST point to the prior K,
  and the prior K's status MUST be updated to "superseded" (not deleted).


Workflow
--------

```
Step 1: Parse args
  <source_ref> (required) / --project / --supports <I-ids> / --slug

Step 2: Resolve paths and load inputs
  - Read the cited I card(s): the in-sample pattern being generalized.
  - Read the generalization basis: the significance test (p / CI), the robustness
    evidence across subgroups, or — when one exists — a probe verdict's numbers
    (`result`) and `caveats`, or a lit/discover claim. The basis is what lets the
    pattern generalize; a probe is one possible basis, not a requirement.
  - Require a claim + a basis + a confidence. If the claim or basis is absent,
    block. A LOW or NEGATIVE confidence is NOT a block — record it.

Step 3: State the generalization belief
  - Positive: "the I-pattern X holds beyond this sample (scope Y)", with the
    inferential basis (p / CI / robustness) in `## Generalization basis` and the
    confidence set to what the basis supports.
  - Negative ("does not generalize", e.g. ns): write the K as "X does NOT
    generalize to <scope> (state the null)", set confidence to what the null
    supports, and state the null in the headline so it is never read as an effect
    (see ../ref/dikw-boundaries.md "Negative and uncertain K").
  - lit/discover source: use the review-provided claim and confidence basis;
    cite the original reference in `sources`.

Step 4: Check for existing K entries to update
  - Grep K_knowledge/*.md for topic overlap
  - If overlap: decide MERGE/UPDATE existing vs SUPERSEDE vs CO-EXIST
  - Block broad candidates that contain multiple independent claims; split
    them before filing.

Step 5: Pick output NN, then compose + atomic write
  - If `--id K<NN>` was passed, USE IT verbatim (apply pre-assigns ids for
    parallel safety). Otherwise NN = max existing + 1 (serial writes only).

Step 6: Update INDEX.md and back-links on cited P/D entries
```


Entry schema
------------

Canonical schema: **`../../ref/insight-md-schema.md`** (see "K layer" section).

Quick reminder for K entries:

```
frontmatter (≤ 16 lines):
  id, type=Insight Knowledge, layer=K, title, description,
  tags, status, created, updated,
  claim, confidence,
  sources, ref_by

body sections (in order):
  ## Claim                 (1-2 paragraphs: the generalization belief, with scope)
  ## Generalization basis  (the inferential evidence: p / CI / robustness; cite I cards)
  ## Counter-evidence      (honestly list contradictions; "none found" + why if so)
  ## Confidence rationale  (why high/medium/low — statistical-only vs robust; what would change it)
  ## Scope                 (where/when this belief holds beyond the sample)

length: ≤ 150 lines total
```

The `claim` field in frontmatter is THE belief in ONE sentence —
load-bearing for skim and INDEX.md. `confidence` is qualitative:
`high | medium | low | contested`. Supersede chain (if any K marked
superseded) tracked in body via "supersedes: [K_old]" in supporting
evidence section.


Definition of done
-------------------

- [ ] `insights/K_knowledge/K{NN}_<slug>.md` written
- [ ] judged source and evidence trail are explicit
- [ ] counter_evidence honestly populated (or "none found" with reasoning)
- [ ] If supersedes set: target K entry's status flipped to "superseded"
- [ ] `## Change log` records creation source, merge/update, or supersede reason
- [ ] NO Python written, NO computation run
- [ ] Back-links added to cited P/D entries' Cross-references


Risk profile
-------------

WRITES new file under `insights/K_knowledge/`. MAY UPDATE existing K
entries' status field (supersede chain). APPENDS back-links to cited
P/D entries. Read-only on probes/, tasks/, all other folders.


Specialist tail
---------------

```
status:    ok | blocked | failed
summary:   "K04_<slug> written (high confidence; supersedes K01)"
artifacts: [insights/K_knowledge/K04_<slug>.md, INDEX.md, back-links]
next:      /haipipe-insight-wisdom to derive strategic recommendation
```
