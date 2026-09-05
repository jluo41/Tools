# Discovery Lifecycle Map (v7 — D1 Task workflow × Page workflow × BJTR Runs)

A Discovery `tNN_` Folder is one durable research article/question with BOTH a
Page Face and a Task Face. It is a Task Page, not a flat citation note. This file
is the canonical authority for the lifecycle/type cross; Level-4 mechanics live
only in `paper-run-contract.md`.

## Three independent dimensions

```text
HIERARCHY       Block -> Job -> Task Page -> Paper/Source Run
DOMAIN WORKFLOW D1: SCOPE -> PREPARE? -> ACQUIRE <-> SYNTHESIZE -> CLOSE
PAGE WORKFLOW   00 CONTEXT -> 01 OUTLINE -> 02 EVIDENCE -> 03 CONTENT -> 04 CHECK
DISCOVERY TYPE  one article form from page-types.md
```

`discoveries/` is the bank/root and has no address segment. Hierarchy says
WHERE the unit lives. Workflow says WHEN work happens.
Discovery Type says WHAT article the root Page promises. Never use phase names
or types as folder levels, or worker calls as Paper Runs.

## Hierarchy

```text
discoveries/                                  bank, not Block
└── b01_<noun>_<qualifier>/                   Block: broad evidence Board/program
    ├── j01_<noun>_<qualifier>/               Job: inquiry/campaign group
    └── j02_<noun>_<qualifier>/               sibling group on the same Board
        └── t01_<noun>_<qualifier>/           Task: one typed article Page
            ├── t01_<noun>_<qualifier>.md     Page Face
            ├── runs/r01_<author><year>_<paper>.sh
            └── results/r01_<author><year>_<paper>/
```

One Task Page holds MANY numbered Paper Runs. Each Run owns exactly one
canonical paper/source subject and has an exact same-stem Result. Result is not
a fifth hierarchy level. Full contract: `paper-run-contract.md`.

All four address-bearing levels use
`<level-letter><NN>_<noun>_<qualifier>`. The path yields compact
`b01j01t01r01` and readable `b01.j01.t01.r01`. Bare `01_` is invalid.

## BJTR meanings in Discovery

| Level | Discovery meaning | Owns |
|---|---|---|
| Block `bNN_` | broad evidence Board/program; prefer few and group related Jobs | Jobs |
| Job `jNN_` | self-contained inquiry or discovery campaign group | related Task Pages |
| Task `tNN_` | one question plus one `discovery_type` article | Page/Task Faces and local Runs |
| Run `rNN_` | one analysis of one admitted canonical Subject | Ticket, Result, runtime receipt |

## The two Faces

```text
Page Face                              Task Face
---------                              ---------
tNN_<task>.md                         discovery.yaml
outline/                               scripts/ (optional instrument)
outline/evidence/bibex/tNN_<task>.bib  runs/
(derived union of complete Result Bibs)    results/
typed Page synthesis                   runtime receipts
```

The Faces work on the same Task question. The Page synthesizes many Results; the Task
Face plans and executes them. `discovery.yaml` is the Task manifest, not the
whole folder or the only file that matters.

## The two workflow authorities

| D1 cycle | Domain/Task meaning | Authoritative writes | Discovery Runs |
|---|---|---|---|
| `SCOPE` | freeze BJTR identity, type, question, boundary, and admission rule | `discovery.yaml` intent | none |
| `PREPARE` | author optional reusable instrument | optional used `scripts/` | none |
| `ACQUIRE` | resolve Triggers, admit Subjects, and execute one analysis per Subject | `runs/`, paired `results/`, Task receipts | `paper-analysis` / `source-analysis` x `N_admitted` |
| `SYNTHESIZE` | hand accepted Results to the shared Page workflow | Task progress and optional typed record only | none; the D1 root records Page CONTENT no-Run rationale |
| `CLOSE` | reconcile the already-CHECKed Page with the Task Face | `discovery.yaml report/status` and handoff | none |

Low-level calls to arXiv, Crossref, a CLI, an API, or another skill are recorded
inside a Paper Run receipt. They are not Level-4 Runs themselves.

## Workflow summary

The complete contract table is owned by
`../../workflow-phases/haipipe-discovery-inquiry/ref/workflow-table.md`. It also
contains the Runs Overview, Human Actions, exact skill chains, and Skill
Coverage. The separate `haipipe-discovery-workflow` skill is retired; D1 owns
the domain table while `haipipe-page-workflow` independently owns Page writes.

Expected total Level-4 Runs is `R = N_admitted canonical Subjects`. Search
queries, candidate rows, redirects, worker/API calls, synthesis passes, typed
records, and SYNTHESIZE/CLOSE do not add Discovery Runs. Actual inventory comes only from
allocated Tickets with runtime receipts.

## Discovery Types and specialist routes

The exact article-form table lives in `page-types.md`; the manifest schema lives
in `discovery-yaml-schema.md`.

- **Search route** serves source-map and source-reading Pages.
- **Review route** serves topic summaries, prior-art/counterevidence verdicts,
  and literature/benchmark landscapes.
- **Idea route** serves ideation and novelty-verdict Pages.

Every route writes the root Page. Optional `summary.md`, `verdict.md`,
`landscape.md`, or `ideas.md` files are typed Task-side records, not rival Pages
or Level-4 Results. Missing evidence always creates another Paper/Source Run;
it is never pasted into one monolithic notes file.

The chain remains:

```text
Source Results -> Review/Summary Page -> Ideation/Novelty Page
```

Folders may reference another Topic's Page or typed record from their own side. A
Discovery Folder remains probe-unaware and never tracks its consumers.

## Trigger resolution

```text
URL / DOI / PDF / citation / request
    -> classify Trigger
    -> resolve zero, one, or many canonical Subjects
    -> allocate one Run per Subject
```

The Trigger is provenance. The Subject owns RUNNAME and the authoritative Bib.
A Trigger that resolves to zero Subjects opens no Run and is returned/logged as
unresolved intake. An allocated Subject whose analysis cannot finish may own a
truthful `status: unresolved` Result, which never enters the Page Evidence Bib.
Before allocation, match the canonical Subject and frozen intent against
existing runtimes. An unchanged duplicate Trigger reuses the existing Run and
Result and opens no new `rNN`; log or return the existing link without rewriting
its frozen inputs. A materially changed analysis allocates a new Run with
`supersedes:`.

## Agents

- **creator** drafts the topic plan, creates paired Run tickets/receipts,
  executes them, then synthesizes the Page.
- **reviewer** audits search coverage, Run/Result bijection, Subject identity,
  one-entry Bibs, claim anchors, and topic-level scope.

Citation verification is the highest-value Discovery gate. The Paper Run
contract owns each Result's `bib.verification` receipt; Outline owns any typed
CITE-item gate it explicitly declares. The checker and Bib builder are
deterministic, but `verified` is an artifact-local person judgment. Every
complete Result entering the aggregate must be verified before D1 CLOSE can claim epistemic `status: ok` or
`status: inconclusive`; without it, the receipt is `blocked`. `inconclusive`
is reserved for completed, verified admissible evidence that cannot establish
the substantive answer.

`outline/evidence/supporting-runs/` is pointer-only lineage for a Page Evidence
Item that the approved Outline explicitly declares. The derived aggregate Bib
does not create such an item by itself. Discovery's own Paper/Source Runs remain
the local `runs/` ↔ `results/` inventory; a consumer does not create a second
Evidence Run just to repackage one of those Results.

## Command routing

```text
/haipipe-discovery                              -> dashboard
/haipipe-discovery open-block <name>            -> scaffold bNN Block
/haipipe-discovery open-job <block> <name>      -> scaffold jNN Job
/haipipe-discovery open <job> <type> <question> -> scaffold tNN Task Page
/haipipe-discovery scope <task>                 -> D1 SCOPE; Page 00 consumes it
/haipipe-discovery prepare <task>               -> D1 PREPARE
/haipipe-discovery add <task> <trigger>         -> D1 ACQUIRE intake
/haipipe-discovery run <task> [RUNNAME]         -> D1 ACQUIRE execution
/haipipe-discovery acquire <task>               -> D1 ACQUIRE
/haipipe-discovery synthesize <task>            -> D1 SYNTHESIZE -> Page workflow
/haipipe-discovery close <task>                 -> Page 04 CHECK -> D1 CLOSE
/haipipe-discovery plan|build|execute|report    -> compatibility aliases
/haipipe-discovery <task>                       -> run full Task lifecycle
/haipipe-discovery <specialist> [args]          -> one-off worker, no durable folder
```

`add` resolves intake and `run` executes Discovery Level-4 tickets inside D1
ACQUIRE. Page CONTENT changes authoritative Page content; Page CHECK returns
its receipt to D1 CLOSE, which reconciles and publishes the Task outcome.
