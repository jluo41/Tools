# /haipipe-task: pinning down what a task-group is, so it can be entered

spine: A task-group is a bank of runnable work, not a folder of scripts. Pin down where truth lives, how a task-folder runs its four phases, what binds one run together, what may leave the bank and what may not, and above all what a human SEES on entering a group, so a fresh agent can take one group from empty to answered from the Board.
close: Every Q here is RULED (✅) or PARKED (⏸️), with the decision recorded on its own page, and `SKILL.md` plus `ref/hierarchy.md` say what those rulings say. Implementation does not gate this board: a ruled question whose code is unwritten closes here and stays open in its page's Items to Finish. The board is not closed while `/haipipe-task <task-group>` still returns text instead of opening a board.

## Topic
`/haipipe-task` is one of the two EXECUTORS. It runs code, produces evidence, and does not know
who wants it. Its unit is the TASK-FOLDER: one runnable thing, running the same four phases,
Plan then Build then Execute then Report, with two machine gates and one human who actually
starts the run.

What makes the design hard is the opposite of what makes `/haipipe-paper` hard. A paper is a
CONSUMER: it may not run code, so half its design is a boundary it must not cross. This layer is
the other side of that wall. It may run anything, and its discipline is that it must never learn
who asked. A task that shapes its answer around a claim has produced evidence worth nothing to
the next question.

The thing this board was opened to settle is narrower and concrete. Entering a task-group today
prints text. Entering a paper now opens a board. The same human, the same day, gets a live
control plane for the manuscript and a paragraph for the work that produced it, and the
group-level doc surface that was supposed to close that gap is specified as MANDATORY and exists
on 5 of 67 groups. This board argues that a task-group should open the same way a paper does, and
works out what its board is made of.

Words this board leans on. A TASK-GROUP is `tasks/{G}{NN}_{name}/`, a set of task-folders sharing
one context. A TASK-FOLDER is one runnable unit, detected by STRUCTURE and never by name. PBER is
its four phases: Plan, Build, Execute, Report. A RUN is one execution, named by a RUNNAME token
shared across four sister files. The BANK is this layer plus `/haipipe-discovery`, seen from a
consumer that cannot reach inside it. A QA FILE is the readable digest this layer writes, and the
only thing a consumer ever reads.

`state:` on this board is about the DECISION and nothing else, exactly as on the paper board (JL
2026-07-26). ✅ the question is ruled, 🟡 the direction is ruled but a named sub-ruling is open,
🔴 nothing is decided, ⏸️ deliberately not deciding. Whether the code exists is a different fact
and lives in each page's `## Items to Finish`.

Cast: JL decides. CC is Claude Code, doing the work.

## Pipeline
```
QA · where things LIVE          the ONE door, and what is behind it
   QA1 the map: seven folders, one door in, one door out
        │
        ├─ what we own
        │    QA2 ① the skill set     44 skills · 9 domains · 7,134 lines
        │    QA3 ② its design board  this board, and what LEAVES it
        │
        ├─ the two channels           shared skills we do NOT own
        │    QA4 ③ the HUMAN channel  /haipipe-board  ← THE ASK LIVES HERE
        │         /haipipe-task CALLS it. A human never types it for a group.
        │    QA5 ⑤ the WALL, from inside
        │         we are the bank. The `qa` verb is the only door in.
        │
        └─ what they produce
             QA6 ⑦ the task-group folder   what exists on disk
             QA7 ⑧ its board               ONE S PAGE PER TASK-FOLDER
                       QA6 and QA7 are the pair the ask turns on

QB · a TASK-FOLDER: what it is, and running one
   ✍️ AUTHOR TIME
        QB1 what a task-folder IS     structure, never the name
                                      the {NN}_ habit misses 31% of the bank

   ⚙️ RUN TIME               the four phases, in the order they run
        QB2 PLAN     what must be fixed before any code exists
        QB3 BUILD    Gate 1 · what a reviewer catches that a test cannot
        QB4 EXECUTE  why the agent does not press the button
        QB5 REPORT   Gate 2 · what makes a number trustworthy
        QB6 the creator/reviewer pair, and why it is not one agent

QC · the RUN            the atomic unit, and what binds it
   QC1 RUNNAME ── four sister files in four folders, one token
        │
        ├─ QC2 light vs heavy      results/ or _WorkSpace/, and who decides
        └─ QC3 the notebook        two of them, and which one IS the record

QD · what LEAVES the bank
   QD1 the QA digest    the only readable answer, written for nobody in particular
   QD2 and nothing else results/ is not a consumer surface
   the QA FILE CONTRACT itself is `01-probe-qa-260726`'s, not ours: QC1@probe
   owns the state line, QC2@probe the checker. We own only the executor half.

QE · shipping the skill
   QE1 fresh-agent acceptance
```
Five letters, and the first two carry the weight. QA is the coordinate system and the home of the
question this board was opened for. QB is the lifecycle that already runs today, so nothing there
is hypothetical: the questions are whether the rules those 107 task-folders already follow are
the right ones and whether a stranger would find them written down.

QC is deliberately small and deliberately separate. A run is not a phase; it is the object the
four phases are about, and the four sister files bound by one token are the single most
load-bearing convention in the layer, because every tool depends on the pairing.

QD is smaller still, and that is the point. This layer produces a great deal and almost none of
it is allowed to leave.

## Pages
### QA · Where things live
Seven folders, one door in, and the shape underneath them: this layer is the BANK, and the wall
that the paper board sees from outside is seen here from inside. `③` is the human channel and the
only way eyes and a click reach the work. `⑤` is not a channel we reach out through; it is how a
consumer reaches in, and the `qa` verb is the whole of it.

The group's fourth beat is what this board was opened for. `QA6` is the task-group folder as it
exists on disk today, and `QA7` is what a board over it would be made of: one S page per
task-folder, so the group index IS the status table that `diagram/02-tasks.txt` was supposed to
be and is not.
QA1-the-map.md
QA2-the-skill-set.md
QA3-the-skill-board.md
QA4-the-board-tool.md
QA5-the-wall-from-inside.md
QA6-task-group-folder.md
QA7-task-group-board.md

### QB · A task-folder: what it is, and running one
The lifecycle itself. 107 task-folders exist and run today, so nothing here is hypothetical.
Read it as the router reads a folder: first what makes a directory a task-folder at all, which is
a structural test and a real trap, then the four phases in execution order, each with the one
question it actually turns on rather than a description of what it does.

The two gates are the interesting part and they are not symmetric. Gate 1 reads code that has
never run; Gate 2 reads numbers that already exist. `QB3` and `QB5` ask what each can catch that
the other cannot, and `QB6` asks why the pair is two agents rather than one careful one.
QB1-what-is-a-task-folder.md
QB2-plan.md
QB3-build.md
QB4-execute.md
QB5-report.md
QB6-creator-reviewer.md

### QC · The run, and what binds it
One execution, and the convention that holds it together. `RUNNAME` is one token appearing in
four files in four folders, and every tool in the layer depends on that pairing, which makes it
the layer's most load-bearing and least documented rule. The other two are the decisions a run
forces: where an artifact goes, and which of the two notebooks is the record of what happened.
QC1-runname.md
QC2-light-vs-heavy.md
QC3-two-notebooks.md

### QD · What leaves the bank
Small on purpose. This layer produces a great deal and almost none of it may leave: one readable
digest per direction explored, written in general language for nobody in particular, and nothing
else. The QA file's own contract, its state line and its checker, belong to `01-probe-qa-260726`
and are linked rather than restated; these two pages own only the executor's half, which is what
we write and what we refuse to let anyone read.
QD1-the-qa-digest.md
QD2-nothing-else-leaves.md

### QE · Shipping the skill
Hand it over so a fresh agent can enter a group and run a folder without us. Last, because it is
the test of everything above it.
QE1-fresh-agent.md

## Links
SKILL.md            ../../task/haipipe-task/SKILL.md
DESIGN.md           ../../task/DESIGN.md
README.md           ../../task/README.md
hierarchy.md        ../../task/haipipe-task/ref/hierarchy.md
task-structure.md   ../../task/haipipe-task/ref/task-structure.md
authoring-conventions.md ../../task/haipipe-task/ref/authoring-conventions.md
run-sh-template.sh  ../../task/haipipe-task/ref/run-sh-template.sh
type-inference.md   ../../task/haipipe-task/ref/type-inference.md
fn/qa.md            ../../task/haipipe-task/fn/qa.md
fn/task-group.md    ../../task/haipipe-task/fn/task-group.md
fn/run.md           ../../task/haipipe-task/fn/run.md
fn/audit.md         ../../task/haipipe-task/fn/audit.md
fn/scan-status.md   ../../task/haipipe-task/fn/scan-status.md
agents/             ../../task/agents/
task-lifecycle.workflow.js ../../task/haipipe-task/ref/task-lifecycle.workflow.js
haipipe-board/      ../../board/haipipe-board/
haipipe-probe/      ../../probe/haipipe-probe/
paper-board/        ../01-haipipe-paper-260725/
probe-board/        ../01-probe-qa-260726/
boardform-board/    ../01-boardform-260722/
QA4@paper           ../01-haipipe-paper-260725/QA-engine-map-and-boundaries/QA4-the-board-tool.md
QA6@paper           ../01-haipipe-paper-260725/QF-delivery-map/QA6-paper-scaffold.md
QA7@paper           ../01-haipipe-paper-260725/QA-engine-map-and-boundaries/QA7-the-paper-board.md
QA8@paper           ../01-haipipe-paper-260725/QA-engine-map-and-boundaries/QA8-owning-the-shared-page.md
QA1@paper           ../01-haipipe-paper-260725/QA-engine-map-and-boundaries/QA1-eight-folders.md
QA3@paper           ../01-haipipe-paper-260725/QA-engine-map-and-boundaries/QA3-the-skill-board.md
QE2@paper           ../01-haipipe-paper-260725/QE-engine-acceptance/QE2-fresh-agent.md
QA8@probe           ../01-probe-qa-260726/QA-the-folders-one-page-each/QA8-the-bank.md
QC1@probe           ../01-probe-qa-260726/QC-the-contract/QC1-qa-state-line.md
QC2@probe           ../01-probe-qa-260726/QC-the-contract/QC2-checker-fails.md
paper-enter/        ../../paper/0-enter/haipipe-paper-enter/
