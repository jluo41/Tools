# Paper Lifecycle

Paper is a delivery lifecycle. It owns the manuscript-specific story, claim
wording, displays, minimap, and section text. Project-level evidence lives in
probes, discoveries, tasks, and insights.

## Folder Contract

```text
<paper-root>/
├── STATUS.md
├── 0-lifecycle/
│   ├── 0-seed/          venue: FREE
│   ├── 1-claims/        venue: FREE
│   ├── 2-pitch/         venue: LIGHT
│   ├── 3-narrative/     venue: MEDIUM
│   ├── 4-display/       venue: HEAVY
│   └── 5-editing/       venue: SPECIFIC (per-section norms)
├── 1-probe-plans/       cross-paper index (probes live per-stage in _PROBE/)
├── 1-rounds/
├── 0-displays/
├── 0-sections/
└── 1-compile.sh
```

Venue awareness gradient: FREE → FREE → LIGHT → MEDIUM → HEAVY → SPECIFIC.
Paper-level argument docs (seed, claims, pitch, narrative) are markdown + _LOG.
Only display compiles to .tex + PDF.

## Lifecycle Stages

| Stage | Job | Main question | Venue | Typical handoff |
|---|---|---|---|---|
| `0-seed` | Keep the paper possibility alive | Why might this paper exist? | FREE | claims or drop |
| `1-claims` | Maintain the claim ledger | What must be true? What evidence do we have? | FREE | venue → pitch |
| `venue` | Pin the target venue | Which venue fits? | (chooser) | pitch |
| `2-pitch` | Make the one-minute argument for THIS audience | What is the paper selling? | LIGHT | narrative |
| `3-narrative` | Structure the paper for THIS venue | How do claims become sections? | MEDIUM | display |
| `4-display` | Design displays per THIS venue's limits | What figure/table carries each claim? | HEAVY | section-edit |
| `5-editing` | Per-section DRAFT-GATHER-POLISH-CHECK | How to write each section? | SPECIFIC | review |

## Maturity Ladder

Use maturity to describe how real the paper is. Maturity is orthogonal to the
current stage; a paper can be mature yet loop back to claims.

| Maturity | Meaning | Expected artifacts |
|---|---|---|
| `prospectus` | Paper-shaped possibility | seed/pitch, no full section contract |
| `scaffold` | Manuscript folder exists | lifecycle files, sections, compile script |
| `claim-ledger` | Claims are explicit | `2-claims` has C-slots and open needs |
| `display-map` | Displays are planned | `4-display` maps claim -> display |
| `section-map` | Paragraph jobs are mapped | `5-minimap` maps paragraphs/displays |
| `draft` | Section text exists | main paper compiles with rough prose |
| `submission-candidate` | Checks mostly pass | citations, claims, displays, compile stable |
| `submitted` | External venue state exists | submission metadata, frozen PDF |
| `revision` | External comments active | `1-rounds/<round>/` has review/todo/applied |
| `accepted/published` | Final external state | camera-ready/final links |

## Loopback Rule

The lifecycle is not linear. When work fails, return to the earliest stage that
explains the failure:

| Symptom | Loop back to |
|---|---|
| claim unsupported / too strong | `2-claims` |
| story arc weak or abstract disagrees | `1-pitch` / `3-narrative` |
| display cannot support claim | `4-display` |
| paragraph has no job/evidence anchor | `5-minimap` |
| reviewer/coauthor comment unresolved | `1-rounds` then target lifecycle stage |

## Handoff To Evidence Workers

Handoff to probe/discover/task/insight only when the problem is evidence, not
wording.

```text
paper GAP -> delivery need -> evidence worker -> verdict/artifact -> paper backfill
```

Common routes:

```text
claim needs verdict/robustness       -> /haipipe-probe plan from-need <need>
claim needs outside context/citation -> /haipipe-discovery <question>
display needs materialized result    -> /haipipe-task-for-display <need>
finished evidence needs reusable K/W -> /haipipe-insight <artifact>
```
