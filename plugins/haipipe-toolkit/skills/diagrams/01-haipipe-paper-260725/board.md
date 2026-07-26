# /haipipe-paper: pinning down what a paper lifecycle is, so it can be run

spine: A paper is a delivery contract, not a writing folder. Pin down where truth lives, how a stage page runs, what its Content and sentences mean, how evidence and Displays enter, how outputs render, and when work may close, so a fresh agent can take one paper from seed to submission from the Board.
dialect: paper        # so the QC faces can SHOW their rules, not only state them
paper-root: _fixture  # a tiny synthetic paper; see _fixture/README.md
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
reached. Reading the 33 pages' own `## Where we are` lines against that split moved 17 of them
from 🟡 to ✅ without a single ruling being made: they had already been decided and were being
reported as open.

Cast: JL decides. CC is Claude Code, doing the work.

## Pipeline
```
QA · where things LIVE      ① writes the paper and owns NEITHER channel out of it
   QA1 the map: eight folders in four pairs, two channels out
        │
        ├─ what we own
        │    QA2 ① the skill set       what ships
        │    QA3 ② its design board    what is argued, and what LEAVES
        │
        ├─ the two channels               both are shared skills we do NOT own
        │    QA4 ③ the HUMAN channel     /haipipe-board
        │    QA5 ⑤ the EVIDENCE channel  /haipipe-probe
        │
        ├─ what they produce
        │    QA6 ⑦ the paper           what exists on disk   ← QB6 QA8
        │    QA7 ⑧ its board           what is worked, and why NOTHING leaves
        │              QA3 and QA7 are written as opposites on purpose
        │
        └─ how the HUMAN channel attaches
             QA8 the ①/③ seam · who owns which REGION of a shared page
             QA9 the ①/③ seam · how work is DRIVEN from a page

   ④ and ⑥ get no face: they are the design records of skills we do not own.

QB · a STAGE: adding one, and running one
   ✍️ AUTHOR TIME      you write these once, by hand
        QB1 what it DECLARES    24 fields · 7 blocks · 3 readers
        QB2 how it may VARY    how many pages · does it survive a new journal
        QB3 its TEMPLATE       a skeleton to fill, or a spec to parse

   ⚙️ RUN TIME         the router does these on every invocation
        QB4 ──▶ the BOARD      who names the page
        QB5                    …and on the SECOND run, what happens to it
        QB6                    …and what is only GENERATED from it
        QB7 ──▶ the PHASES     how they are called, and may one be skipped
                 QB8  DRAFT    what must it refuse to write
                 QB9  PROBE    what may it do alone
                 QB10 REVISE   when may it change a sentence already read
                 QB11 CHECK    who says done, and on what evidence
    rebuilt 260726. The group used to ask what a stage IS; it now asks what
    you DO with one, in the order the router does it. Six faces that
    described rather than asked were deleted; three questions are new (the
    template, the second run, the skip); the probe loop and the cost ladder
    shrank to the paper's half, because ⑥ owns the mechanism.

QC · the SENTENCE           what the reader READS          →  0-sections/
   QC0 the sentence unit ──┬──→ QC1 citation           the .bib, human-only
                           ├──→ QC2 value              bound to the producing run
                           ├──→ QC3 Display · table    display id, source_data.csv
                           └──→ QC4 Display · figure   display id, candidates
   all five read ONE paragraph, out of ONE file, and each names only its own chips
   all four resolve `QA8@boardform`'s one blocked item: inline chips, `dialect: paper`

QD · the DISPLAY            what the reader LOOKS AT       →  0-displays/
   QD1 ownership → QD2 render contract ──┬──→ QD3 renderer taxonomy
                                         ├──→ QD4 format adapters → QD7
                                         └──→ QD5 who may commission one
   QD6 provenance ①run →②data →⑦code →⑧asset →③float →④sentence   joins QD to QC
   QD7 one Content, several projections: LaTeX · Word · HTML   (was QB11)
   QC3/QC4 CITE a display; QD1-QD5 MAKE one. Different jobs, different owners.

QE · shipping the skill     the contract form and the acceptance test
   QE1 contract form → QE2 fresh-agent acceptance
```
Five letters, and three of them are folders. QB is `0-lifecycle/`, the machinery that produces
things. QC is `0-sections/` and QD is `0-displays/`, which are the only two kinds of thing a
reader of the finished paper actually meets: sentences, and the displays they point at. QA is the
coordinate system that has to be settled before any of it is placed, and QE is whether a stranger
can run the result.

That cut replaced nine invented-in-order letters (260726). The letter now names the parent, so a
`QB` number says on sight that the question is a sub-question of the stage, which the old `QD2`
said nothing about. QB carries eleven faces, which is honest: the machinery IS most of this skill.

Within a letter the order is the order the work happens in, not the order the questions were
asked. QB runs author time then run time, and inside run time it follows the router: resolve the
contract, make the page, walk the phases. So a number is a position in a procedure, and a face
that cannot be placed in that procedure is a face that belongs to a different letter.
## Pages
### QA · Where things live
Eight folders in four pairs, and the shape underneath them: `①` writes the paper and owns NEITHER
channel out of it. `③` is the human channel, the only way eyes and a click reach the work. `⑤` is
the evidence channel, the only door a number or a citation enters by. Both are shared skills whose
models this family depends on and does not own, and the paper skill says exactly that about both.
Read the group in four beats: the map, what we own, the two channels, what they produce, and how
the human channel attaches. `④` and `⑥` get no face on purpose: they are the design records of
skills we do not own, named on `QA1` and explained by `QA3`'s Law.
QA1-eight-folders.md
QA2-the-skill-set.md
QA3-the-skill-board.md
QA4-the-board-tool.md
QA5-the-probe-layer.md
QA6-paper-scaffold.md
QA7-the-paper-board.md
QA8-owning-the-shared-page.md
QA9-driving-work-from-a-page.md

### QB · A stage: adding one, and running one
The lifecycle itself. Eight stages exist and run today, so nothing here is hypothetical: the
questions are whether the rules those stages already follow are the right ones, and whether they
are written anywhere a stranger would find them. Read it as the router reads a stage. First author
time, the three things a person writes by hand: the twenty-four fields a stage declares and who
reads each one, how it declares its two variations, and what its template is. Then run time, in execution order: the page gets named, and
we ask what a second run does to it and what is only generated from it; then the phase list is
walked, and each of DRAFT, PROBE, REVISE and CHECK gets the one question it actually turns on.

Rebuilt on 260726, and the rebuild deleted more than it moved. Six faces asked "what is X" and
answered it, which is a glossary entry rather than a question, and they are in `_archive/`. Three
questions are new and each was found by reading the code rather than the docs: `template.md` is
parsed while its own header says it is copied, a second run has six different rules in five
shapes, and one stage already declares a three-phase list. `QB9` shrank to the paper's half of the
probe contract, because `QA1`'s Law says ⑥ owns the loop and the ladder.
QB1-what-a-stage-declares.md
QB2-how-a-stage-varies.md
QB3-stage-template.md
QB4-who-names-the-page.md
QB5-the-second-run.md
QB6-write-vs-generate.md
QB7-calling-the-phases.md
QB8-draft.md
QB9-probe.md
QB10-revise.md
QB11-check.md

### QC · The sentence, and what hangs on it
The first of the two things a reader actually meets, and the home of `0-sections/`. The Board
ships the mechanism at `QA8@boardform`: one sentence per source line, a `>` lane bound by
adjacency, a badge, a drawer, a write-back endpoint. What it cannot decide is what a citation, a
value or a Display MEANS, and it says so: its one unbuilt item, inline chips, is blocked on a
paper-side ruling. These pages are that ruling, split by TYPE, because the four look symmetric and
are not. A citation ends in a `.bib` entry only a human may write. A value binds to a run, not a
file. A table is checkable on sight; a figure is not, and it has candidates.
All five read the SAME paragraph, embedded from one file, so the asymmetry is visible in one object
rather than argued across four examples that used to drift apart.
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
QD7-one-content-many-formats.md
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
probe-board/       ../01-probe-qa-260726/
QB2@probe          ../01-probe-qa-260726/QB2-cost-ladder.md
QB1@probe          ../01-probe-qa-260726/QB1-five-step-loop.md
QA8@boardform      ../01-boardform-260722/QA8-sentence.md
QA8a@boardform     ../01-boardform-260722/QA8a-sentence-chat.md
paper-folder/      ../../paper/3-deliver/1-build/haipipe-paper-folder/
display/           ../../display/
paper-display/     ../../paper/1-lifecycle/4-display/
0-lifecycle/       ../../../../../../examples/Project-Personality-OpioidRx/papers/Paper-Personality2Opioid-MISQ2026/0-lifecycle/
