---
name: haipipe-insight-knowledge
description: "K-level knowledge specialist of the haipipe-insight family. Reads I_information entries and synthesizes validated belief statements into insights/K_knowledge/. A K entry is a 'we now claim X is true' statement with explicit support / counter-evidence / confidence. NO code, pure markdown synthesis. Use when running K-phase via /haipipe-application ask, or directly /haipipe-insight-knowledge. Trigger: K-level, knowledge, validated belief, causal claim, what do we know."
argument-hint: "[--project <path>] [--scope <pattern-ids>] [--slug <slug>]"
allowed-tools: Bash, Read, Write, Edit, Grep, Glob, Skill
---

Skill: haipipe-insight-knowledge
=================================

K-level of the Insight base (D → I → K → W). Reads multiple
`I_information/I*.md` entries (and optionally underlying D/D*.md) and
synthesizes validated belief statements.

**Invocation modes** (see `../../ref/invocation-modes.md`): interactive (a
human steers; the belief-triage ASK runs) OR headless (`--scope` ≥ 1 I id +
`--auto` → file silently), chosen by input completeness.
`card-creator-knowledge-agent` calls this skill headless during fan-out; agent
+ no I id → `status: blocked` (never hang). End with the structured return block.

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
examples/<project>/insights/I_information/I*.md       (REQUIRED, ≥ 1 entry)
examples/<project>/insights/D_data/D*.md   (optional, for context)
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
- A K entry must list ALL contradicting evidence found in I/D entries.
  Cherry-picking is a violation.
- Confidence is qualitative (high / medium / low / contested) and must
  be justified in the entry body.
- If a K entry would directly contradict an existing K entry, the new
  entry's "supersedes / contradicts" field MUST point to the prior K,
  and the prior K's status MUST be updated to "superseded" (not deleted).


Workflow
--------

```
Step 1: Parse args
  --project / --scope / --slug

Step 2: Resolve paths and load inputs
  - Read scoped I*.md entries
  - Optionally read underlying D*.md for context

Step 3: Triage candidate beliefs (interactive default)
  - Group patterns by topic
  - Propose ≥ 1 candidate belief statement per topic
  - User picks; --auto picks top-ranked

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
