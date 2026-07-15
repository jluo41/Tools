# discovery.yaml — Discovery Folder Schema (v3.0)

## The whole model

One research topic = one folder. One file matters: `discovery.yaml` — Plan writes it, Report appends the outcome to it. Execute writes the evidence files next to it. That is the entire contract.

```
examples/<PROJECT>/discoveries/<GROUP_slug>/<NN_slug>/
├── discovery.yaml    Plan spec + Report outcome (source of truth)
├── build/            optional instrument (only if Build ran)
├── sources.md        work product: what was found   (Search: terminal)
├── notes.md          work product: what was read    (Search: terminal)
├── verdict.md | landscape.md | ideas.md   TERMINAL (by type + role)
└── QA/               OPTIONAL readable digests — QA/<n>-<slug>.md
                      written at Report, by THIS layer. Contract: fn/qa.md.
```

`QA/` is optional; not every discovery-folder has one. `<n>` = creation order, and the numbering IS the index (`ls QA/` is the index). Slug only — no PP id, no claim id, no paper reference in a bank filename, ever. Write-once: a later question ADDS `QA/<n+1>-<slug>.md`.

NOT part of the contract: `status.yaml`, `site.md`, per-folder logs, `_ASK/`, `_ANS/`. Lifecycle progress is discovery.yaml `status:`; the human summary is `report.summary`; events go to the project-level `_haipipe/project.log.jsonl`.

## Types × roles → terminal

```
type    role                 question                          terminal
------  -------------------  --------------------------------  ------------
Search  source_gather        what sources exist?               sources.md
Search  source_read          what do the key sources say?      notes.md
Review  prior_art_check      does the claim already exist?     verdict.md
Review  counterevidence      what argues against the claim?    verdict.md
Review  landscape_review     map approaches / baselines        landscape.md
Review  benchmark_landscape  standard eval setups              landscape.md
Idea    idea_generation      generate + rank candidate claims  ideas.md
Idea    novelty_check        is this idea new enough?          verdict.md
```

`type` is the folder kind (Axis 2); `role` picks the terminal within it. `novelty_check` sits under `Idea` — it is the evaluation half of the ideation loop (generate → check novelty), even though its terminal is a verdict.

## Fields

| Field | Required | Notes |
|---|---|---|
| kind | yes | always `discovery` |
| id | yes | `<GROUP-id>.<NN>`, mirrors the path: `discoveries/L01_x/03_y/` -> `L01.03` |
| type | yes | `Search` / `Review` / `Idea` |
| role | yes | see table above |
| group | yes | `{id, slug, title}` of the discovery-group |
| slug, title | yes | folder slug + human title |
| status | yes | lifecycle progress, see below |
| question | yes | the external-world question (Plan) |
| sources | opt | search scope; `from_source_folder` reuses a Search folder |
| build | opt | `{needed, artifact}` — only for a systematic instrument |
| expected_outputs | yes | files Execute will write (work products + terminal) |
| report | at Report | outcome block, APPENDED at Report — absent before |
| created_at, updated_at | yes | quoted ISO8601 strings |

**No parent field — a discovery is self-contained.** It knows nothing outside its own folder: whoever needs the terminal records the link in THEIR OWN files; the discovery just answers its question and never tracks who commissioned or consumed it. Same principle for tasks.

## Skeleton

```yaml
kind: discovery
id: P01.02
type: Review              # Search | Review | Idea
role: prior_art_check     # picks the terminal (see table)
group:
  id: P01
  slug: rare-phenotype-lift
  title: Rare phenotype lift (claim evidence)
slug: prior-art-adaptive-sampling
title: Does adaptive sampling for rare phenotypes already exist?
status: planned
created_at: "2026-07-03T10:00:00-04:00"
updated_at: "2026-07-03T10:00:00-04:00"

question: |
  Has adaptive sampling for rare-phenotype detection been published?
sources:
  requested: [research-lit, semantic-scholar]
  from_source_folder: ""    # optional: reuse a Search folder instead of searching inline
  local_first: true
  verification_required: true
build:
  needed: false
  artifact: ""
expected_outputs:
  - sources.md              # work product (inline search)
  - notes.md                # work product (inline read)
  - verdict.md              # terminal for this role

# --- appended at Report ---
report:
  outcome: supports         # per-type vocabulary below
  summary: >
    One line a human can act on.
  confidence: medium
  supports_claim: true      # judge roles only
  contradicts_claim: false  # judge roles only
```

## Lifecycle status (Axis 1)

```
planned -> building (opt) -> executing -> reported -> ok | inconclusive | blocked
```

`ok` = terminal complete and usable. Reuse by any number of consumers is recorded on THEIR side, never here; there is no `consumed` status.

## Report block (appended at Report — absent before)

The block does not exist until Report writes it: a discovery.yaml WITH a `report:` block has been reported; one WITHOUT has not. `report.outcome` is the per-type result (never confuse with the top-level lifecycle `status:`):

```
Search             gathered      (N sources curated / read)
Review-judge       supports | contradicts | inconclusive
Review-synthesize  mapped
Idea-generate      generated     (N candidates ranked)
Idea-novelty       novel | partial | preempted | inconclusive
```

Common fields: `outcome`, `summary`, `confidence` (high/medium/low). Judge roles (prior_art/counterevidence/novelty) add `supports_claim` / `contradicts_claim`.

## 💀 DELETED: the `answers:` field and the `_ASK/` bridge (v3.0, 2026-07-14)

`answers: [PPNN]` is **gone**, and so is everything it connected to: `_ASK/` stub folders, `_ANS/`, and every PP id under `discoveries/`. **The bank is probe-unaware** (R2). A discovery no longer carries any trace of who asked.

Do not resurrect them, and do not write them into a new discovery.yaml. What replaced them:

```
  the CONSUMER keeps the question + the stake in ITS OWN probe file
     papers/<P>/1-probes/PPNN_<topic>.md — a `q-executor:` block per question
  it hands us that block, VERBATIM, and nothing else
  we answer it through the `qa` verb (fn/qa.md) and return ONE PATH:
     discoveries/<discovery-group>/<discovery-folder>/QA/<n>-<slug>.md
  the consumer's section points at that path. Nothing points back.
```

There is no disk signal to grep for, because there is no id: the answer IS a file, and the caller's `target:` is the pointer to it. Constitution: `probe/haipipe-probe/SKILL.md`.


## Terminal templates

### verdict.md (Review-judge; Idea-novelty)

```md
# Verdict
status: supports | contradicts | inconclusive    (novelty: novel | partial | preempted)
confidence: high | medium | low

## Answer
One paragraph answering the question.

## Evidence
- Full citation / URL / id — one-line finding — VERIFIED | NEEDS-VERIFICATION

## Caveats
- What this discovery did not check.
```

### landscape.md (Review-synthesize) — a map, not a yes/no

```md
# Landscape: <topic>
confidence: high | medium | low

## Approaches (taxonomy)
- <cluster> — what it does — exemplar refs

## Gaps / open questions
- <gap> — why it is open

## References (full, verified)
1. <self-contained full citation>     (Review Output Contract rules 1-5)
```

### ideas.md (Idea-generate) — ranked candidates, not a verdict

```md
# Ideas: <prompt>

## Candidates (ranked)
1. <claim> — rationale — novelty: NOVEL | PARTIAL | SEEN (vs <ref>) — testability: <how it could be tested>

## Grounding
- which Search / Review folder this builds on
```

### sources.md + notes.md (Search terminals; work products elsewhere)

Format lives in ONE place: `ref/source-format.md` — one source = one `###` subsection with the full title in the heading; venue/locator first line, Scholar link, role, verification flag, a 2-4 sentence `summary:` of the paper itself, and a one-line `finding:` for our question; NEVER a table. Heavy artifacts (PDFs, snapshots) go in an optional `sources/` subfolder.

### `QA/<n>-<slug>.md` (optional readable digest — NOT a terminal)

A QA file is not a terminal and never replaces one: it is the READABLE digest of one direction this discovery-folder has explored, anchored back into the artifacts. Exactly three sections, no markdown tables, general language only (LAW 2 — no `C\d`, no `H\d`, no "the paper"). List it in `expected_outputs` when a commission names it.

```md
# Q — <the question, self-contained, general language>

## Answer
Plain words, actionable by a reader who has never opened this folder.
Anchors: [→ sources.md#S02]  [→ verdict.md#Evidence]  [→ landscape.md#Gaps]

## Caveats
- What this does NOT establish.

## Not-done
- What was asked but not resolved, and why.
```

Full contract — the gate, the depth ladder, the three legal reasons a QA file may exist: `fn/qa.md`.



## Log events (project-level, `_haipipe/project.log.jsonl`)

```
discovery.opened     {"ts", "event", "discovery_group", "discovery_folder", "type", "role"}
discovery.completed  {"ts", "event", "discovery_group", "discovery_folder", "status", "outcome"}
discovery.consumed   {"ts", "event", "discovery_group", "discovery_folder", "consumed_by"}
```

One JSON object per line. `discovery.consumed` is appended by the CONSUMER when it links the terminal — consistent with one-way references; the discovery itself never writes it. Old lines (append-only history) may carry `discovery_file`/`verdict`/`parent` fields — readers tolerate them; never rewrite the log.
