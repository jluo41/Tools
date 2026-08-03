# Paper Lifecycle

Paper is a delivery lifecycle. It owns the manuscript-specific story, claim
wording, displays, section scaffolds, and section text. Project-level evidence
lives in tasks and discoveries.

## Folder Contract

```text
<paper-root>/
├── 0-lifecycle/
│   ├── 0-seed/          venue: FREE
│   ├── 1-work/          resource + claims; venue: FREE
│   ├── 2-venue/         venue + pitch + narrative
│   ├── 3-display/       venue: HEAVY
│   ├── 4-main/          venue: SPECIFIC (per-section norms)
│   ├── 5-appendix/
│   ├── 6-submission/
│   └── 7-round/
├── 1-probes/       PPNN_<topic>/ probe files (flat cross-stage pool; campaign board in its README)
├── displays/
├── sections/
└── 2-src/compile.sh
```

Venue awareness gradient: FREE → FREE → LIGHT → MEDIUM → HEAVY → SPECIFIC.
Paper-level argument docs are S pages with `## Content` and `## Log`.
Only display compiles to .tex + PDF.

## Lifecycle Stages

| Stage | Job | Main question | Venue | Typical handoff |
|---|---|---|---|---|
| `0-seed` | Keep the paper possibility alive | Why might this paper exist? | FREE | resource or drop |
| `1-resource` | Audit what the paper can actually use | What must exist, and can it carry the claims? | FREE | claims, reseed, or park |
| `1-claims` | Maintain the claim ledger | What must be true? What evidence do we have? | FREE | venue → pitch |
| `venue` | Pin the target venue | Which venue fits? | (chooser) | pitch |
| `2-pitch` | Make the one-minute argument for THIS audience | What is the paper selling? | LIGHT | narrative |
| `3-narrative` | Structure the paper for THIS venue | How do claims become sections? | MEDIUM | display |
| `4-display` | Design displays per THIS venue's limits | What figure/table carries each claim? | HEAVY | section-edit |
| `5-section-edit` | Per-section DRAFT-PROBE-REVISE-CHECK | How to write each section? | SPECIFIC | review |

## Phase Dimension

Stages x phases is a two-axis model. Each stage skill in `1-lifecycle/` defines
WHAT the stage delivers; the `2-phase/` workers define HOW: DRAFT -> PROBE ->
REVISE -> CHECK (`haipipe-paper-{draft,probe,revise,check}`). Venue omits
REVISE by contract. The PROBE phase authors and matches entries, then sends
only authorized bank work through the isolated
`haipipe-probe-q-executor-agent` collector.
Phases are internal workers driven by the stage skill; CHECK is the only
human-involved gate. Users invoke stage skills only (`/haipipe-paper seed`, `/haipipe-paper
claims`, ...), never phases directly.

## Maturity Ladder

Use maturity to describe how real the paper is. Maturity is orthogonal to the
current stage; a paper can be mature yet loop back to claims.

| Maturity | Meaning | Expected artifacts |
|---|---|---|
| `seed` | Paper-shaped possibility | seed/pitch, no full section contract |
| `scaffold` | Manuscript folder exists | lifecycle files, sections, compile script |
| `claim-ledger` | Claims are explicit | `1-work/S-Work-1-claims.md` has C-slots and open needs |
| `display-map` | Displays are planned | `3-display/` maps claim -> display |
| `section-edit` | Section outlines with DPRC in progress | `4-main/S-Main-*.md` pages exist |
| `draft` | Section text exists | main paper compiles with rough prose |
| `submission-candidate` | Checks mostly pass | citations, claims, displays, compile stable |
| `submitted` | External venue state exists | submission metadata, frozen PDF |
| `revision` | External comments active | `0-lifecycle/7-round/S-Round-*.md` has discussion, queue, and log |
| `accepted/published` | Final external state | camera-ready/final links |

## Loopback Rule

The lifecycle is not linear. When work fails, return to the earliest stage that
explains the failure:

| Symptom | Loop back to |
|---|---|
| claim unsupported / too strong | `1-work/S-Work-1-claims.md` |
| story arc weak or abstract disagrees | `2-venue/S-Venue-1-pitch.md` / `S-Venue-2-narrative.md` |
| display cannot support claim | `3-display/` |
| paragraph has no job/evidence anchor | `4-main/` |
| reviewer/coauthor comment unresolved | the round's S-Round page, then the target lifecycle stage |

## Handoff To Evidence Workers

Handoff to probe/discover/task only when the problem is evidence, not
wording.

```text
paper GAP -> question ENTRY (1-probes/) -> the PROBE phase's MATCH ->
DISPATCH what MATCH cannot close -> the answering QA file -> the entry's
`### a-executor` -> each Q-consumer's a-consumer in its stage doc -> the paper
backfills (a claim's status flips in S-Work-1-claims.md)
```

Common routes:

```text
claim needs its status settled       -> add/route the owning Q-consumer, then run that stage's
                                        PROBE phase (it authors the entry, MATCHes, and sends only
                                        authorized work through the collector)
claim needs outside context/citation -> Q-consumer -> stage PROBE -> collector -> discovery QA
display needs materialized result    -> DR row -> display stage (which owns any task dispatch)
settled claim status                 -> 0-lifecycle/1-work/S-Work-1-claims.md (the ONLY
                                        home of a claim's status; the probe entry
                                        carries only its `### a-executor`)
```
