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
        │    QA6 ⑦ the paper           what exists on disk   ← QB2d QA8
        │    QA7 ⑧ its board           what is worked, and why NOTHING leaves
        │              QA3 and QA7 are written as opposites on purpose
        │
        └─ how the HUMAN channel attaches
             QA8 the ①/③ seam · who owns which REGION of a shared page
             QA9 the ①/③ seam · how work is DRIVEN from a page

   ④ and ⑥ get no face: they are the design records of skills we do not own.

QB · a STAGE: hand it a page, and a predefined flow runs over it
   🎛 THE STAGE        what the skill reads to know what to do
        QB1  the contract    24 fields · 7 blocks · 3 readers · this map

   📄 THE PAGE         the thing you hand it
        QB2  one markdown file · four regions · four owners
              QB2a  what SHAPES it     a skeleton to fill, or a spec to parse
              QB2b  what it is CALLED  identity ▸ filename, and how many
              QB2c  a SECOND run       a page you have already edited
              QB2d  what comes OUT     md ▸ tex, one way, never back

   🔁 THE FLOW         the predefined thing that modifies it
        QB3  the phase list · always ends `check` · may one be skipped
              QB3a  DRAFT    what it adds, and what it refuses to write
              QB3b  PROBE    what it may do alone
              QB3c  REVISE   changing a sentence already read
              QB3d  CHECK    who says done, and on what evidence
    restructured 260726 on JL's model: a skill, a page, a flow. Four faces
    that read as interchangeable became QB2a-d, because each describes the
    same object from a different angle. The old "how a stage varies" face
    dissolved: `runs:` joined QB2b, where the identity fields that decide
    how many pages exist already live, and `venue_aligned:` went to QA6,
    which owns the stage set.

QC · the SENTENCE           what the reader READS          →  sections/
   QC0 the sentence unit ──┬──→ QC1 citation           the .bib, human-only
                           ├──→ QC2 value              bound to the producing run
                           ├──→ QC3 Display · table    display id, source_data.csv
                           └──→ QC4 Display · figure   display id, candidates
   ROWS ▲ what hangs on a sentence  ·  COLUMNS ▼ where it is delivered
                           ┌──→ QC5 as LaTeX           sections/ appendices/ \input
                           └──→ QC6 as Word            no .bib, no \input, no comment
   all four resolve `QA8@boardform`'s one blocked item: inline chips, `dialect: paper`

QD · the DISPLAY            what the reader LOOKS AT       →  displays/
   QD1 ownership → QD2 render contract ──┬──→ QD3 renderer taxonomy
                                         ├──→ QD4 format adapters → QD7
                                         └──→ QD5 who may commission one
   QD6 provenance ①run →②data →③code →④asset →⑤float →⑥sentence   joins QD to QC
   QD7 one Content, several projections: LaTeX · Word · HTML   (was QB3d)
   QC3/QC4 CITE a display; QD1-QD5 MAKE one. Different jobs, different owners.

QE · shipping the skill     the contract form and the acceptance test
   QE1 contract form → QE2 fresh-agent acceptance
```
Five letters, and three of them are folders. QB is `0-lifecycle/`, the machinery that produces
things. QC is `sections/` and QD is `displays/`, both UNNUMBERED per QA6, which are the only two
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

### QB · A stage: a page in, a predefined flow over it
The lifecycle itself, read the way you actually use it: you hand the skill a stage page and it
modifies that page in a fixed order. So the group is three things. `QB1` is what the skill READS to
know what to do, the contract, whose twenty-four fields have exactly three readers and only two of
them are programs. `QB2` is the PAGE you hand it, one markdown file with four owners that never
collide, and its four sub-faces ask what shapes it, what it is called, what a second run does to it,
and what is generated out of it. `QB3` is the FLOW, the declared phase list, and its four sub-faces
are DRAFT, PROBE, REVISE and CHECK.

WHICH stages this skill has and what each one asks is `QA6`, not here. Restructured on 260726: the
flat eleven read as interchangeable in the middle, so the two clusters became lettered, and the
"how a stage varies" face dissolved into `QB2b` and `QA6`.
QB1-what-a-stage-declares.md
QB2-the-page.md
QB2a-its-template.md
QB2b-its-name.md
QB2c-the-second-run.md
QB2d-what-comes-out.md
QB3-the-flow.md
QB3a-draft.md
QB3b-probe.md
QB3c-revise.md
QB3d-check.md

### QC · The sentence: what hangs on it, and where it is delivered
The first of the two things a reader actually meets, and the home of `sections/`. The Board
ships the mechanism at `QA8@boardform`: one sentence per source line, a `>` lane bound by
adjacency, a badge, a drawer, a write-back endpoint. What it cannot decide is what a citation, a
value or a Display MEANS, and it says so: its one unbuilt item, inline chips, is blocked on a
paper-side ruling. These pages are that ruling, split by TYPE, because the four look symmetric and
are not. A citation ends in a `.bib` entry only a human may write. A value binds to a run, not a
file. A table is checkable on sight; a figure is not, and it has candidates.
The group is a MATRIX (JL 260726). QC1-QC4 are ROWS, what hangs on a sentence. QC5 and QC6 are
COLUMNS, where it is delivered. Every cell differs, which is why one shared "projections" face was
always going to be too thin to say anything.
```
                 │ QC5 ──▶ LaTeX          │ QC6 ──▶ Word
 ────────────────┼────────────────────────┼─────────────────────────
 QC1 citation    │ \citep{key} + .bib     │ ⚠️ no .bib. a field, or
                 │ + .bst does the rest   │    baked text to maintain
 QC2 value       │ the number, inline     │ the number, inline  ✅ same
 QC3 table       │ \input{displays/<u>/   │ ⚠️ must EMBED the rendered
                 │ float.tex} + \ref      │    table. No \input exists.
 QC4 figure      │ \includegraphics in    │ ⚠️ must EMBED the image, and
                 │ the unit's float       │    invent its own numbering
 ────────────────┼────────────────────────┼─────────────────────────
 ### §6.1        │ \subsection            │ a Heading style
 > lanes         │ DROPPED                │ DROPPED             ✅ same
 %% {CC-*}:      │ survives as a comment  │ 🔴 NOWHERE TO PUT IT
```
QC0-sentence-unit.md
QC1-sentence-citation.md
QC2-sentence-value.md
QC3-sentence-display-table.md
QC4-sentence-display-figure.md
QC5-sentence-to-latex.md
QC6-sentence-to-word.md
### QD · The Display, and who may render it
The second thing a reader meets, and the home of `displays/`. Separate from QC because citing a
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
### Q-Skill · Keeping the skills true to this board
A ruling that stays on a board binds nothing, because no runtime reads a design board. This group
owns the seam between the two: when a ruling becomes shipped text, when a version and a CHANGELOG
entry are owed, and where a reader looks to see which of the 35 skills are current. It exists
because on 2026-07-26 the two halves disagreed three times in one day, in three different
directions, and nothing detected any of them. Whether a shipped skill then WORKS is `QE2`, not here.
QS1-graduation.md
QS2-versioning.md
QS3-status.md

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
haipipe-board/     ../../board/haipipe-board/
dialect_paper.py   ../../board/haipipe-board/src/dialect_paper.py
haipipe-paper-probe          ../../paper/2-phase/1-probe/haipipe-paper-probe/
haipipe-paper-revise-place   ../../paper/2-phase/2-revise/haipipe-paper-revise-place/
haipipe-paper-revise-results ../../paper/2-phase/2-revise/haipipe-paper-revise-results/
haipipe-paper-revise-content ../../paper/2-phase/2-revise/haipipe-paper-revise-content/
5-section-edit/    ../../paper/1-lifecycle/haipipe-paper-stage/stages/5-section-edit/
4-display/         ../../paper/1-lifecycle/haipipe-paper-stage/stages/4-display/
boardform-board/   ../01-boardform-260722/
probe-board/       ../01-probe-qa-260726/
QB1@probe          ../01-probe-qa-260726/QB-the-verbs-one-page-each/QB1-the-order.md
QB3@probe          ../01-probe-qa-260726/QB-the-verbs-one-page-each/QB3-match.md
QC1@probe          ../01-probe-qa-260726/QC-the-contract/QC1-qa-state-line.md
QB6@probe          ../01-probe-qa-260726/QB-the-verbs-one-page-each/QB6-interpret.md
QA8@boardform      ../01-boardform-260722/QA-defining-a-board/QA8-sentence.md
QA8a@boardform     ../01-boardform-260722/QA-defining-a-board/QA8a-sentence-chat.md
paper-folder/      ../../paper/3-deliver/1-build/haipipe-paper-folder/
display/           ../../display/
paper-display/     ../../paper/1-lifecycle/4-display/
0-lifecycle/       ../../../../../../examples/Project-Personality-OpioidRx/papers/Paper-Personality2Opioid-MISQ2026/0-lifecycle/
