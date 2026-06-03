---
name: haipipe-insight-knowledge
description: "K-level knowledge specialist of the haipipe-insight family. Files a CONFIRMED probe's claim as a validated belief in insights/K_knowledge/ (the confirmed probe is the controlled comparison K requires); cites supporting I_information entries where they exist. A K entry is a 'we now believe X is true' statement with explicit support / counter-evidence / confidence. NO code, pure markdown synthesis. Use when running K-phase via /haipipe-application ask, or directly /haipipe-insight-knowledge <probe_ref>. Trigger: K-level, knowledge, validated belief, file probe claim, what do we know."
argument-hint: "<probe_ref> [--project <path>] [--supports <I-ids>] [--slug <slug>]"
allowed-tools: Bash, Read, Write, Edit, Grep, Glob, Skill
metadata:
  version: "1.1.0"
  last_updated: "2026-05-31"
  summary: "K-level knowledge specialist of the haipipe-insight family."
  changelog:
    - "1.0.0 (2026-05-31): baseline metadata added."
    - "1.1.0 (2026-05-31): K sources a confirmed probe's claim (was >=1 I card); cites supporting I cards in the body."
---

Skill: haipipe-insight-knowledge
=================================

K-level of the Insight base (D → I → K → W). A CONFIRMED probe's `claim` IS the
validated belief (the probe is the controlled comparison K requires); this
skill files that claim as a K card, citing supporting I cards where they exist.

**Invocation modes** (see `../../ref/invocation-modes.md`): interactive (a
human steers; may tighten the claim wording) OR headless (a confirmed
`probe_ref` → file its claim silently), chosen by input completeness.
`card-creator-knowledge-agent` calls this skill headless during fan-out; agent
+ non-confirmed / no-claim probe → `status: blocked` (never hang). End with the
structured return block.

```
D — Data:         "what we observed"
I — Information:      "what patterns emerged"      (input)
K — Knowledge:    "what we now believe is true"  ← THIS SKILL
W — Wisdom:       "what we should do next"
```

K differs from I in commitment: I describes "the data tends to show X",
K commits to "we believe X is true (in scope Y, with confidence Z)".


Input
-----

```
examples/<project>/probes/<...>/probe.yaml            (REQUIRED; result.status in {confirmed, refuted}, has `claim`)
examples/<project>/insights/I_information/I*.md       (optional; supporting evidence to cite)
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

- NO Python. NO statistical computation. Statistics were done at the
  D_probe result-aggregate step; this layer reads numbers and
  commits to a belief.
- A K entry must list ALL contradicting evidence (the probe's `caveats` +
  any I/D counter-evidence). Cherry-picking is a violation.
- Confidence is qualitative (high / medium / low / contested) and must
  be justified in the entry body.
- If a K entry would directly contradict an existing K entry, the new
  entry's "supersedes / contradicts" field MUST point to the prior K,
  and the prior K's status MUST be updated to "superseded" (not deleted).


Workflow
--------

```
Step 1: Parse args
  <probe_ref> (required) / --project / --supports <I-ids> / --slug

Step 2: Resolve paths and load inputs
  - Read the probe.yaml: `claim` is the belief; `caveats` → counter-evidence;
    `result` → the numbers. ACCEPT status `confirmed` or `refuted`. REFUSE
    `pending` / `inconclusive` / `exploratory` (report which status it has).
  - Optionally read --supports I*.md entries to cite as supporting evidence

Step 3: Take the belief from the probe
  - status==confirmed: the probe's `claim` IS the K belief — use it verbatim
    (headless) or let the user tighten the wording (interactive).
  - status==refuted: the belief is the NEGATION of the hypothesis. Write the
    K claim as "X does NOT <hold>", set `contradicts:` to the prior K /
    hypothesis it overturns and `refutation_basis:` to the refuting numbers
    (see ../ref/dikw-boundaries.md "Refuted and inconclusive probes as K cards").

Step 4: Check for existing K entries to update
  - Grep K_knowledge/*.md for topic overlap
  - If overlap: decide UPDATE existing vs SUPERSEDE vs CO-EXIST

Step 5: Compose entry per schema below; atomic write

Step 6: Update INDEX.md and back-links on cited P/D entries
```


Entry schema
------------

Canonical schema: **`../../ref/insight-md-schema.md`** (see "K layer" section).

Quick reminder for K entries:

```
frontmatter (≤ 13 lines):
  id, layer=K, tags, status, created, updated,
  claim, confidence,
  sources, ref_by

body sections (in order):
  ## Claim                 (1-2 paragraphs: belief stated fully, with scope)
  ## Supporting evidence   (bulleted P/O citations with key numbers)
  ## Counter-evidence      (honestly list contradictions; "none found" + why if so)
  ## Confidence rationale  (why high/medium/low — what would change it)
  ## Scope                 (where/when this belief holds)

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
- [ ] supporting_patterns ≥ 1
- [ ] counter_evidence honestly populated (or "none found" with reasoning)
- [ ] If supersedes set: target K entry's status flipped to "superseded"
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
