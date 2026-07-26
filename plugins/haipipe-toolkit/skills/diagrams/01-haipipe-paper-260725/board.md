# /haipipe-paper: pinning down what a paper lifecycle is, so it can be run

spine: A paper is a delivery contract, not a writing folder. Pin down where truth lives, how a stage page runs, what its Content and sentences mean, how evidence and Displays enter, how outputs render, and when work may close, so a fresh agent can take one paper from seed to submission from the Board.
close: Every Q here reaches ✅ or ⏸️, `PHILOSOPHY.md` and the stage contracts say the same thing, and a fresh agent with no background can read them and run one stage correctly end to end.

## Topic
`/haipipe-paper` takes one paper from "why might this exist" to a submitted manuscript. Its unit
is the STAGE: eight of them, each answering exactly one question, each running the same four
phases, each closing at a human gate.

What makes the design hard is that a paper is the downstream consumer of two other layers. It may
not run code and may not read the literature itself; it asks, and the task and discovery layers
answer. So half of this skill's design is about a boundary it must not cross, and the other half
is about the shape of the thing it writes.

The Board is the durable control plane for that work. Sessions are replaceable workers, stage
pages carry their own queues and handoffs, sentence attachments resolve to inspectable evidence,
and generic Display renderers sit outside Paper while Paper retains the meaning of every Display.

This board is where those choices are recorded and argued. Settled questions graduate into
`PHILOSOPHY.md` and the per-stage contracts; unsettled ones stay here so nobody mistakes a
convenient improvisation for a rule.

Words this board leans on. A STAGE is one lifecycle step with one question and one artifact. DPRC
is its four phases: DRAFT, PROBE, REVISE, CHECK. A GATE is a human yes that closes a stage. The
BANK is the task and discovery layers, which answer questions the paper cannot answer itself. A
PROBE ENTRY binds one paper question by path to one bank answer. VENUE-FREE means a stage survives
retargeting to another journal; VENUE-ALIGNED means it is rewritten.

Cast: JL decides. CC is Claude Code, doing the work.

## Pipeline
```
QA · where things LIVE      separate the skill package from a live paper first
   QA1 boundary ──→ QA2 family layers ──→ QA3 one-skill anatomy
        └── QC1 + QF1 + QF3 + QF4 ─────→ QA4 paper scaffold

QB · what a stage IS        the unit, its phases, its gate, its grain
   QB1 stage → QB2 phases → QB3 gate → QB4 grain → QB5 venue-free vs aligned

QBa · CONTENT is the link   the one object both skills write, and how it is read
   QBa1 Content boundary → QBa2 composed blueprint
   QBa3 sentence unit → QBa4 semantic attachments → QBa5 hover preview

QC · what a stage WRITES    the artifact and who names it
   QC1 artifact ──┬──→ QC2 naming
                  └──→ QC3 LaTeX + Word + HTML projections

QD · how evidence GETS IN   the one door, its price, and what prose holds meanwhile
   QD1 probe loop → QD2 cost ladder → QD3 placeholders

QE · shipping the skill     the contract form and the acceptance test
   QE1 contract form → QE2 fresh-agent acceptance

QF · the board relationship one file, two skills: who owns which half
   QF1 ownership ──┬──→ QF2 dependencies
                   ├──→ QF3 state
                   └──→ QF4 creation

QG · how the Board RUNS WORK
   QG1 control plane → QG2 page queue → QG3 in-item handoff → QG4 page-first runner

QI · how Display is SHARED without losing meaning
   QI1 ownership → QI2 render contract ──┬──→ QI3 renderer taxonomy
                                         └──→ QI4 format adapters → QC3
```
QA is the coordinate system: nothing downstream is safely placed until the reusable skill, the
design Board, the live paper, and the evidence banks are separated. QB is then the main
lifecycle line. QBa is lettered as a sub-question of QB rather than given a letter of its own,
because Content is not a separate topic from what a stage is: it is what a stage produces and
what the Board renders, so the two skills meet on it before anything downstream is decided. The
remaining groups each own one downstream boundary, with explicit cross-links where the Board,
the Display family, and the output adapters meet.

## Pages
### QA · Where things live
The folder architecture comes first because it decides which kind of truth each later question
is allowed to create. It separates reusable behavior from one paper's live state, keeps the
front door compact, and makes a new paper runnable from its Board without speculative files.
QA1-skill-vs-paper-folder.md
QA2-skill-family-layers.md
QA3-one-skill-anatomy.md
QA4-paper-scaffold.md
### QB · What a stage is
The thing itself. Eight stages exist and run today, so these questions are not hypothetical: they
ask whether the rules the stages already follow are the right ones and whether they are written
down anywhere a stranger would find them.
QB1-what-is-a-stage.md
QB2-four-phases.md
QB3-what-is-a-gate.md
QB4-unit-grain.md
QB5-venue-free-aligned.md
### QBa · Content links `/haipipe-paper` to `/haipipe-board`
There is ONE file. The stage's artifact and the board's page are the same markdown, and
`## Content` is the part both skills reach for: `/haipipe-paper` writes it as the stage's real
product, `/haipipe-board` renders it, folds it, and hangs comments and evidence off its
sentences. So Content is not a section of a page, it is the joint between the two skills. These
questions ask what may go in it, how stage and venue templates compose its structure, where one
sentence ends, and how a citation, a value or a Display attaches to a sentence and stays
inspectable. Lettered QBa, not QH, because it belongs under QB rather than beside it.
QBa1-stage-content-boundary.md
QBa2-content-blueprint.md
QBa3-sentence-unit.md
QBa4-semantic-attachments.md
QBa5-hover-preview.md
### QC · What a stage writes
The artifact is the paper. LaTeX, Word, and HTML are projections of the same authored Content,
not three manuscripts that must be synchronized by hand.
QC1-artifact-and-tex.md
QC2-who-names-files.md
QC3-one-content-many-formats.md
### QD · How evidence gets in
The paper cannot run code or read the literature. Every fact it states arrives through one door,
and the design of that door is what keeps a claim traceable.
QD1-probe-loop.md
QD2-cost-ladder.md
QD3-placeholders.md
### QE · Shipping the skill
Hand it over so a fresh agent can run a stage without us.
QE1-contract-form.md
QE2-fresh-agent.md
### QF · The board relationship
`/haipipe-board` renders the same files this skill writes. That was a deliberate choice: one
file, no adapter, so a rendering can never disagree with its source. The cost is that two skills
now write to one page, and every question here is a consequence of that: who owns which half, who
declares dependencies, which record is authoritative, and who creates a page in the first place.
QF1-one-file-two-skills.md
QF2-two-dependency-declarations.md
QF3-where-state-lives.md
QF4-who-creates-a-page.md
### QG · How the Board runs work
The Board is the remote control plane and each coding session is an ephemeral worker. These
questions define the executable queue, completed handoff, and the page-first runner that lets a
fresh session continue without the previous transcript.
QG1-board-control-plane.md
QG2-items-are-the-queue.md
QG3-handoff-on-the-item.md
QG4-page-first-runner.md
### QI · The reusable Display family
Paper owns the visual argument; Display owns reusable rendering; Task owns computed evidence;
Deliver owns target-format embedding; low-level drawing engines remain utilities.
QI1-display-ownership.md
QI2-render-contract.md
QI3-renderer-taxonomy.md
QI4-format-adapters.md

## Links
HANDOFF.md         ../../paper/HANDOFF.md
PHILOSOPHY.md      ../../paper/PHILOSOPHY.md
README.md          ../../paper/README.md
stages/            ../../paper/1-lifecycle/haipipe-paper-stage/stages/
index.yml          ../../paper/1-lifecycle/haipipe-paper-stage/stages/index.yml
CONTRACT.md        ../../paper/1-lifecycle/haipipe-paper-stage/stages/CONTRACT.md
venue/             ../../paper/venue/
haipipe-probe/     ../../probe/haipipe-probe/
haipipe-board/     ../../0_utils/haipipe-board/
paper-folder/      ../../paper/3-deliver/1-build/haipipe-paper-folder/
display/           ../../display/
paper-display/     ../../paper/1-lifecycle/4-display/
0-lifecycle/       ../../../../../../examples/Project-Personality-OpioidRx/papers/Paper-Personality2Opioid-MISQ2026/0-lifecycle/
