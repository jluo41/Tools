# /haipipe-paper: pinning down what a paper lifecycle is, so it can be run

spine: A paper is a delivery contract, not a writing folder. Pin down where truth lives, how a stage page runs, what its Content and sentences mean, how evidence and Displays enter, how outputs render, and when work may close, so a fresh agent can take one paper from seed to submission from the Board.
close: Every Q here is RULED (✅) or PARKED (⏸️), with the decision recorded on its own page, and `PHILOSOPHY.md` and the stage contracts say what those rulings say. Implementation does not gate this board: a ruled question whose code is unwritten closes here and stays open in its page's Items to Finish.

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

`state:` on this board is about the DECISION and nothing else (JL 2026-07-26). The four values
are the board's usual ones and they read: ✅ the question is ruled, 🟡 the direction is ruled but
a named sub-ruling is still open, 🔴 nothing is decided yet, ⏸️ deliberately not deciding. Whether
the code exists is a different fact and it lives in each page's `## Items to Finish`, which is
the page's queue. The two were previously merged, so a page sat 🟡 because an implementation was
missing rather than because anything was undecided, and the close condition could never be
reached. Reading the 34 pages' own `## Where we are` lines against that split moved 17 of them
from 🟡 to ✅ without a single ruling being made: they had already been decided and were being
reported as open.

Cast: JL decides. CC is Claude Code, doing the work.

## Pipeline
```
QA · where things LIVE      separate the skill package from a live paper first
   QA1 the map: six folders in three pairs, four legal crossings
        ├──→ QA2 ① the skill set     what ships
        ├──→ QA3 ② the skill board   what is argued, and what LEAVES
        ├──→ QA4 ③ the paper         what exists on disk   ← QBa1 QBc1 QBc3 QBc4
        ├──→ QA5 ④ the paper board   what is worked, and why NOTHING leaves
        │         QA3 and QA5 are written as opposites on purpose
        └──→ QA6 ⑤ /haipipe-board     the TOOL both boards are made of
              ├──→ QA7 who owns which REGION of the shared page
              └──→ QA8 how work is DRIVEN from a page
                   merged 260726 from QBc×5 + QBd×4, every Law kept

QB · the MACHINERY          a stage, and the Board that runs it
   QB1 stage → QB2 phases → QB3 gate → QB4 grain → QB5 venue-free vs aligned
    QBa · what a stage WRITES    QBa1 artifact ─┬─→ QBa2 naming
                                                └─→ QBa3 LaTeX + Word + HTML
    QBb · how evidence GETS IN   QBb1 probe loop → QBb2 cost ladder → QBb3 placeholders
    QBc · who owns the page      QBc1 ownership ─┬─→ QBc2 dependencies
                                                 ├─→ QBc3 state
                                                 ├─→ QBc4 creation
                                                 └─→ QBc5 dialect code
    QBd · how work is DRIVEN     QBd1 control plane → QBd2 queue → QBd3 handoff → QBd4 runner
                                 mechanism ruled on the boardform board: QD1-QD3, QE4

QC · the SENTENCE           what the reader READS          →  0-sections/
   QC0 the sentence unit ──┬──→ QC1 citation           the .bib, human-only
                           ├──→ QC2 value              bound to the producing run
                           ├──→ QC3 Display · table    display id, source_data.csv
                           └──→ QC4 Display · figure   display id, candidates
   all four resolve QA8's one blocked item: inline chips, `dialect: paper`

QD · the DISPLAY            what the reader LOOKS AT       →  0-displays/
   QD1 ownership → QD2 render contract ──┬──→ QD3 renderer taxonomy
                                         ├──→ QD4 format adapters → QBa3
                                         └──→ QD5 who may commission one
   QD6 provenance ①run →②data →③code →④asset →⑤float →⑥sentence   joins QD to QC
   QC3/QC4 CITE a display; QD1-QD5 MAKE one. Different jobs, different owners.

QE · shipping the skill     the contract form and the acceptance test
   QE1 contract form → QE2 fresh-agent acceptance
```
Five letters, and three of them are folders. QB is `0-lifecycle/`, the machinery that produces
things. QC is `0-sections/` and QD is `0-displays/`, which are the only two kinds of thing a
reader of the finished paper actually meets: sentences, and the displays they point at. QA is the
coordinate system that has to be settled before any of it is placed, and QE is whether a stranger
can run the result.

That cut replaced nine invented-in-order letters (260726). The letter now names the parent, so
`QBb2` says on sight that the cost ladder is a sub-question of what a stage is, which the old
`QD2` said nothing about. QB carries nineteen faces across four sub-letters, which is honest: the
machinery IS most of this skill. Read the sub-group counts rather than a rolled-up QB number, or a
large group will hide its own frontier.
## Pages
### QA · Where things live
Six folders in three pairs: every thing has a board. Three of the six ARE boards, and two of those look identical and are opposites. This group is the coordinate system: until it is settled, a rule can land in a working
folder, working state can land in the manual, and a design argument can become something the
runtime depends on. One face for the map, then one for each folder in the order a person meets it.
QA1-six-folders.md
QA2-the-skill-set.md
QA3-the-skill-board.md
QA4-paper-scaffold.md
QA5-the-paper-board.md
QA6-the-board-tool.md
QA7-owning-the-shared-page.md
QA8-driving-work-from-a-page.md

### QB · The machinery: a stage, and the Board that runs it
Everything that PRODUCES what a reader meets. Eight stages exist and run today, so these are not
hypothetical: they ask whether the rules the stages already follow are the right ones. The Board
sits here too rather than beside it, because a stage and the tool that renders, queues and runs it
are one machine. Four sub-questions follow: what a stage writes, how evidence reaches it, who owns
the shared page, and how work is driven from it.
QB1-what-is-a-stage.md
QB2-four-phases.md
QB3-what-is-a-gate.md
QB4-unit-grain.md
QB5-venue-free-aligned.md
### QBa · What a stage writes
The artifact is the paper. LaTeX, Word, and HTML are projections of the same authored Content,
not three manuscripts that must be synchronized by hand.
QBa1-artifact-and-tex.md
QBa2-who-names-files.md
QBa3-one-content-many-formats.md
### QBb · How evidence gets in
The paper cannot run code or read the literature. Every fact it states arrives through one door,
and the design of that door is what keeps a claim traceable.
QBb1-probe-loop.md
QBb2-cost-ladder.md
QBb3-placeholders.md
### QC · The sentence, and what hangs on it
The first of the two things a reader actually meets, and the home of `0-sections/`. The Board
ships the mechanism at `QA8` on its own board: one sentence per source line, a `>` lane bound by
adjacency, a badge, a drawer, a write-back endpoint. What it cannot decide is what a citation, a
value or a Display MEANS, and it says so: its one unbuilt item, inline chips, is blocked on a
paper-side ruling. These pages are that ruling, split by TYPE, because the four look symmetric and
are not. A citation ends in a `.bib` entry only a human may write. A value binds to a run, not a
file. A table is checkable on sight; a figure is not, and it has candidates.
QC0-sentence-unit.md
QC1-sentence-citation.md
QC2-sentence-value.md
QC3-sentence-display-table.md
QC4-sentence-display-figure.md
### QD · The Display, and who may render it
The second thing a reader meets, and the home of `0-displays/`. Separate from QC because citing a
display and MAKING one are different jobs: `QC3` and `QC4` ask what a sentence points at and what
state that pointer is in, while these ask who owns the rendering. Paper owns the visual argument;
Display owns reusable rendering; Task owns computed evidence; Deliver owns target-format
embedding; low-level drawing engines remain utilities.
QD1-display-ownership.md
QD2-render-contract.md
QD3-renderer-taxonomy.md
QD4-format-adapters.md
QD5-who-may-render.md
QD6-provenance-chain.md
### QE · Shipping the skill
Hand it over so a fresh agent can run a stage without us. Last, because it is the test of
everything above it.
QE1-contract-form.md
QE2-fresh-agent.md

## Links
PHILOSOPHY.md      ../../paper/PHILOSOPHY.md
README.md          ../../paper/README.md
stages/            ../../paper/1-lifecycle/haipipe-paper-stage/stages/
index.yml          ../../paper/1-lifecycle/haipipe-paper-stage/stages/index.yml
CONTRACT.md        ../../paper/1-lifecycle/haipipe-paper-stage/stages/CONTRACT.md
venue/             ../../paper/venue/
haipipe-probe/     ../../probe/haipipe-probe/
haipipe-board/     ../../0_utils/haipipe-board/
dialect_paper.py   ../../0_utils/haipipe-board/src/dialect_paper.py
haipipe-paper-probe          ../../paper/2-phase/1-probe/haipipe-paper-probe/
haipipe-paper-revise-place   ../../paper/2-phase/2-revise/haipipe-paper-revise-place/
haipipe-paper-revise-results ../../paper/2-phase/2-revise/haipipe-paper-revise-results/
haipipe-paper-revise-content ../../paper/2-phase/2-revise/haipipe-paper-revise-content/
5-section-edit/    ../../paper/1-lifecycle/haipipe-paper-stage/stages/5-section-edit/
4-display/         ../../paper/1-lifecycle/haipipe-paper-stage/stages/4-display/
boardform-board/   ../01-boardform-260722/
QA8                ../01-boardform-260722/QA8-sentence.md
QA8a               ../01-boardform-260722/QA8a-sentence-chat.md
paper-folder/      ../../paper/3-deliver/1-build/haipipe-paper-folder/
display/           ../../display/
paper-display/     ../../paper/1-lifecycle/4-display/
0-lifecycle/       ../../../../../../examples/Project-Personality-OpioidRx/papers/Paper-Personality2Opioid-MISQ2026/0-lifecycle/
