# Paper Lifecycle

Paper is a delivery lifecycle. It owns the manuscript-specific story, claim
wording, displays, minimap, and section text. Project-level evidence lives in
probes, discoveries, tasks, and insights.

## Folder Contract

```text
<paper-root>/
├── STATUS.md
├── 0-lifecycle/
│   ├── 0-seed/
│   ├── 1-pitch/
│   ├── 2-claims/
│   ├── 3-narrative/
│   ├── 4-display/
│   └── 5-minimap/
├── 1-rounds/
├── 0-displays/
├── 0-sections/
└── 1-compile.sh
```

## Lifecycle Stages

| Stage | Job | Main question | Typical handoff |
|---|---|---|---|
| `0-seed` | Keep the paper possibility alive | Why might this paper exist? | back to project evidence or drop |
| `1-pitch` | Make the one-minute argument | What is the paper selling? | `2-claims` |
| `2-claims` | Maintain the claim ledger | Which claims are supported, weak, or GAP? | probe/discover/task/insight |
| `3-narrative` | Shape this paper's story | How do claims become a manuscript arc? | `4-display` or `2-claims` |
| `4-display` | Design displays | What figure/table carries each claim? | display task or `5-minimap` |
| `5-minimap` | Map paragraphs | What job does each paragraph do, and what evidence anchors it? | sections/edit/build |

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
