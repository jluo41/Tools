# Subjective labeling: turn one person's vague concept into labels, policy, and measured executors
spine: Settle a human-grounded subjective-labeling system in which one identified person is the semantic authority, repeated Calibration Rounds jointly improve human-confirmed labels and an executable annotation policy, and a sealed final test selects how the remaining corpus is completed.
close: Every active Q reaches ✅ SETTLED or ⏸️ ON HOLD, the settled laws are reflected in the subjective-label skill family, and the resulting workflow passes a fresh-context end-to-end test.
session: bb1efa90-a20e-4915-8ce6-a5b2820d891d
excalidraw: /_excalidraw
dialect: paper

## Topic
A large corpus of reviews has no outcome label, and the target trait begins as a vague subjective idea rather than a fixed ontology.
One human supplies the target judgment.
A strong calibration agent helps that person inspect selected reviews, make the concept explicit, assign final labels, explain boundaries, and turn the emerging policy into a guideline that both people and weaker language models can follow.
Every human-reviewed item receives three separate records: a final class in HIGH, LOW, or NONE; one of seven diagnostic regions; and an uncertainty record.
Repeated Calibration Rounds expand the human-confirmed gold set, close a new annotation-policy version, measure correction and coverage, and decide whether another round is worth the human effort.
After the policy freezes, a sealed unseen set receives human gold and scores candidate executors under one protocol.
The selected executor then labels the remaining corpus, routes risky items to the human, and leaves item-level provenance.

Cast: JL is the project lead and semantic authority, who makes the subjective calls and shows as 🧠 on the page.
CC is the implementation and migration owner, who turns settled Board laws into reusable skill contracts and shows as 🔧.
RA is a research assistant who may run the workflow but cannot replace JL's semantic authority.

Words this Board leans on.
A Calibration Round starts from a closed policy, selects or receives a human batch, runs one or more Human-AI Sessions, and ends at a Checkpoint.
A Human-AI Session is one continuous dialogue in which items, regions, reasons, and policy text are refined together.
An annotation policy contains the core guideline, boundary rules, ordered decision procedure, uncertainty and escalation policy, and a compact generalized casebook.
A candidate pool is the broad set considered before the smaller human batch is composed.
Pre-labels are sealed weak-model predictions produced under the previous closed policy.
A consensus audit is a stratified random human review of items on which the weak executors agree.
A sealed test is kept outside development and receives human gold only after the final policy freezes.

## Pipeline
**Lifecycle**: the chronological path through the six responsibility groups.

```text
QA  semantic contract
 │
 ▼
QB  initialize project and run Round 1
 │
 ▼
QC  select, pre-label, and adjudicate later-round batches
 │
 ▼
QD  optimize policy, measure progress, and decide whether to stop
 │
 ▼
QE  freeze, test, score executors, and complete the corpus
 │
 └──────────────▶ QF  keep artifacts, skills, agents, and checks aligned
```

**Round state**: the artifact sequence that must close before another round begins.

```text
closed G_(t-1)
      ↓
candidate pool C_t
      ↓
sealed pre-labels P_t
      ↓
human batch B_t
      ↓
Human-AI Session or Sessions
      ↓
human gold Y*_t + policy draft G_t
      ↓
Checkpoint t
      ↓
cumulative gold D_t + closed G_t
```

QA0 is the governing conception for this edition.
The other pages make one part of that conception independently inspectable and closeable.
This Lifecycle is the GROUP axis, which is not the same thing as the RUN axis, and the difference was written down wrongly on 260818 before being corrected the same day.
The GROUP axis is the one drawn above: which responsibility group a reader visits next, and it needs no group of its own because it IS this section.
The RUN axis is what ONE `label-round` call does, and `skills/page-workflows/label-round/SKILL.md` carries it as six phases A to F with no page on this Board arguing them; `QLw00` lifts it here as eleven phases in two rhythms.
Old questions were reopened where their earlier purpose conflicted with QA0; their former filenames remain aliases under Links.

## Board Map

```text
                    ONE ROUND OF THE LIFECYCLE                       CROSSCUTTING

 QA semantic          the meaning is fixed first: authority,
 contract             H/L/N, regions, guideline shape
  │  QA0 QA1 QA2 QA3
  ▼
 QB calibration       QB1 opens the project and runs Round 1;   ┌──────────────────┐
 round                QB2 the blind Session; QB3 checkpoints    │ QF execution     │
  │  QB1 QB2 QB3                                                │ contract         │
  ▼                                                             │  QF1 commands    │
 QC selection and     every later round: QC1 pool →             │  QF2 schema      │
 adjudication         QC2 sealed prelabels → QC3 batch →        │  QF3 agents      │
  │  QC1 QC2 QC3 QC4  QC4 blind adjudication                    │  QF4 libraries   │
  ▼                                                             │  QF5 acceptance  │
 QD optimization      QD1 guideline moves; QD2 QD3 measure;     │                  │
 and convergence      QD4 rules whether to stop                 │ every group's    │
  │  QD1 QD2 QD3 QD4                                            │ settled law      │
  │     └── not stopped ──▶ back to QC1 for the next round      │ lands here as    │
  ▼                                                             │ skills + checks  │
 QE final evaluation  QD4 stop → QE1 opens the sealed test;     └──────────────────┘
 and completion       QE2 scorecards → QE3 completion →          QG page-type
  │  QE1 QE2 QE3 QE4  QE4 audit and provenance                    QG1 shows one run
  └────────────────────────────────────────────────────▶ QF       on one board page
```

## Board Structure

The folder listing reads in the order this board declares, and each page keeps its own material with it.
The leading number is the group's place in `## Pages`, added on 260816; `## Pages` stays the only authority on that order, and you change it by moving a `### ` block first and renaming the folder second.
Each page already owned a folder carrying its own name, with the name on it twice, once as the folder and once as the only `.md` inside; everything else beside that `.md` is one of the page's plugins.

```text
SubjectiveLabelBoard-260722/
├── board.md                              Board-level source and page registry
├── 1-QA-semantic-contract/               what the project means: authority, output, geometry, policy
│   └── QA0-the-revised-conception/       one page, one folder
│       └── QA0-the-revised-conception.md the page: the only .md discovery reads here
├── 2-QB-calibration-round/               the human-AI round
├── 3-QC-selection-and-adjudication/      choosing and settling cases
├── 4-QD-optimization-and-convergence/    when the policy stops moving
├── 5-QE-final-evaluation-and-completion/ the sealed test and the scorecards
├── 6-QF-execution-contract/              what actually ran
├── 7-QLw-labeling-workflow/              the RUN axis: QLw00 + one page per phase
├── 8-QG-page-type/                       the labeling Page Type this family owns
├── _source/                              raw working material, off-board under `_`
└── board/                                generated site, never hand-edited
```

## Pages
### QA · Semantic contract
This group owns what the project means: its authority, output contract, label geometry, and executable policy.
QA0-the-revised-conception.md
QA1-system-contract.md
QA2-label-region-uncertainty.md
QA3-guideline-contract.md

### QB · Calibration Round
This group owns project initialization, the human-facing interaction unit, and the Checkpoint that closes a round.
QB1-initialize-round-one.md
QB2-human-ai-session.md
QB3-checkpoint-and-versions.md

### QC · Selection and adjudication
This group owns how later-round evidence enters human review without allowing retrieval or model consensus to become gold.
QC1-candidate-pool.md
QC2-prelabel-and-seal.md
QC3-compose-human-batch.md
QC4-blind-adjudication.md

### QD · Optimization and convergence
This group owns policy improvement, comparable measurements, coverage and concept stability, and the stopping decision.
QD1-optimize-guideline.md
QD2-round-metrics.md
QD3-coverage-and-stability.md
QD4-stopping-criteria.md

### QE · Final evaluation and completion
This group owns the sealed human test, executor scorecards, full-corpus execution, and the final reliability package.
QE1-sealed-final-test.md
QE2-model-scorecard.md
QE3-complete-corpus.md
QE4-final-audit-and-provenance.md

### QF · Execution contract
This group owns how settled Board laws become references, callable skills, agent authority, implementation boundaries, and acceptance tests.
It also holds this Board's workflow pair, the two pages the BoardSkillBoard keeps in its own `QPw` group: how the labeling workflow MOVES, and the hands that move it when no person is in the room.
No `QPw-labeling-workflow` group was added on 260818, because `QB` through `QE` already ARE the time axis a `QPw1` would draw; a sixth workflow group would restate the spine that `## Pipeline` declares.

```text
🔁 the loop        QF1  the five canonical commands ARE the phases:
                        label-init · label-round · label-evaluate ·
                        label-complete, plus read-only label-status
                        carries all five in skill/, with the router
📋 the artifacts   QF2  what each phase may write
🤲 the hands       QF3  the agents, each named by the act it may never do:
                        the weak executor never writes gold, the optimizer
                        never accepts its own patch, the evaluator never
                        modifies G* · carries six of them in skill/
🧰 the libraries   QF4  what exists, what conflicts, what must be built
🚪 the gate        QF5  the fresh-context test the whole family must pass
⬜ debt            QF3 governs NINE agent files and names only six:
                        classifier-agent, embedder-agent and prober-agent
                        appear as role words in States A2.1 and in no
                        ## Files row, so skill/ cannot seed them
⬜ debt            the 15 lifecycle pages QB1 to QE4 name no runner at all:
                        each describes its step in prose and never writes
                        the command or agent that performs it, so every
                        one of them seeds an empty skill/
⬜ debt            the run-receipt contract and the human-tick surface moved
                        to `QLw` on 260818, where they are divisions 4 and 5 of
                        QLw00; the QF6/QF7/QF8 proposal of the same morning is
                        superseded, because the workflow they belonged to now
                        has a group and QF holds contracts rather than sequence
```

The three proposed pages are the ONLY parts of `QPw`'s ten-page shape that `QB` through `QE` do not already carry.
`QPw1`-`QPw6` are the six phases, and this Board argues all six across its 15 lifecycle pages; `QPw7` is `QF3` under another name; `QPw00` is `## Pipeline`.
What is left is the gate before the work, the record of the work attempted, and the one surface a person signs, which is why the borrow is three pages and not a group.
The full phase-by-phase mapping, including the four disciplines the existing pages are missing rather than the pages, was drawn on 260818 and belongs in `QF6` when it is written.
QF1-skill-command-contract.md
QF2-artifact-schema-config.md
QF3-agent-topology.md
QF4-library-mapping.md
QF5-acceptance-tests.md

### QLw · Labeling workflow
This group owns the RUN axis: what actually happens, in order, when a person labels a corpus, and what that person does in each step.
`## Pipeline` above draws the GROUP axis, which is which responsibility group a reader visits next; that is a different question and this group does not restate it.
It exists because the sequence lived nowhere: `QA` through `QE` argue each step's method one page at a time, and the only list of steps was inside `skills/page-workflows/label-round/SKILL.md`, whose phases A to F cover one round and say nothing about opening or closing the job.
Numbered 260818 (JL): `QLw00` holds the group on `QPw00`'s precedent, the eleven phases take `QLw1` to `QLw11` in run order, and the machinery takes `QLw12` to `QLw14`.
Phases count from ONE, so `QLw0` no longer sits beside `QLw00`; every phase page's number IS its phase number, and phase 8 is `QLw8` with no arithmetic in between.
A phase page owns TIMING and AUTHORITY only: when the phase starts, when it is finished, which hands may act, and what each may never do. The METHOD stays on the `QA` to `QE` page named in each row, because a copy of a method goes out of date the night it is written.

```text
📋 the sequence    QLw00 the ELEVEN phases in order, their two rhythms, the
                         person's job and cost in each, and the two contracts
                         that exist nowhere · the door a new person enters through

📆 THE LIFECYCLE · phases 1, 8, 9, 10, 11, each exactly once
🎬 start           QLw1  react to ~15 random items, and let the first guideline
                         come OUT of the reactions · method: QB1 · QA2
🧊 freeze          QLw8  the person signs, the policy stops moving · LAST and
                         accept-biased (JL 260818) · this tick closes the run
                         page · method: QE1
🏁 score           QLw9  every candidate on the sealed test, one protocol,
                         read-only · the person does NOTHING · method: QE2
🏭 label all       QLw10 the chosen executor finishes the corpus and sends the
                         hard ones back · method: QE3
🔍 spot check      QLw11 a fresh sample judged BLIND, then compared · method: QE4

🔁 THE ROUND · phases 2 to 7, run N times and nobody knows N
🔎 pick            QLw2  choose what the person spends hours on, and say WHY ·
                         exits on a person's `approved:` · method: QC1 · QC3
🔒 lock            QLw3  the small models guess first, sealed · the ONLY phase
                         defined by what may not be READ · method: QC2
🧠 label           QLw4  the person judges · class, region, uncertainty, reason ·
                         blind first pass, then the reveal · method: QB2 · QC4
                         🎯 ~85% of the person's hours in the whole job
📜 rules           QLw5  the reasons become rules a stranger could follow, each
                         citing the item ids that forced it · method: QD1 · QA3
📊 numbers         QLw6  what moved, and was QLw2's claim right · method: QD2 · QD3
🚦 next?           QLw7  close the round, and price the next one · five routes ·
                         method: QB3 · QD4

🔧 THE MACHINERY · what RUNS the phases, on the QPw7-8-9 precedent
🤖 the agents      QLw12 the nine hands, each named by the one act it may NEVER
                         do, against the phases each acts in · records that QF3
                         names six of the nine in its ## Files
🧾 the receipts    QLw13 how the loop is RUN: the four words (job · phase · step ·
                         round), one receipt per ATTEMPTED phase, chained by
                         sha256, an auditor that REHASHES, and the six stops of
                         which five are not success
                         🆕 labeling's one real difference from QPw8: phase 4 and
                            phase 10 are worked by a PERSON over hours or days,
                            so their receipts are per ITEM and not per phase
✋ the gate        QLw14 the five ticks a machine may never write, on ONE surface,
                         accept-biased: it opens only when 8 computed findings are
                         zero (JL 260818) · silence, good numbers and an agent's
                         confirmation are each refused as substitutes
```
The number alone cannot say whether a page is a phase or a service, so the three headings in this block carry that split.
JL hit exactly this on the sibling Board ("I don't understand why we have so many 7, 8, 9", 260818), and the repair there was to NAME the page for its job, which is why `QPw7` is `page-agents` and not `the-hands`.
QLw00-the-workflow.md
QLw1-start.md
QLw2-pick.md
QLw3-lock.md
QLw4-label.md
QLw5-rules.md
QLw6-numbers.md
QLw7-next.md
QLw8-freeze.md
QLw9-score.md
QLw10-label-all.md
QLw11-spot-check.md
QLw12-the-agents.md
QLw13-the-receipts.md
QLw14-the-gate.md

### QG · Page type
This group owns how one run of this workflow shows up as a board page, which is the only concern here that a reader meets before the method rather than inside it.
`QG1` is the worked specimen of the `labeling` page type: a real corpus and a real target walked through the five doors `QF1` defines, so a writer copies a page instead of copying a description. The contract it demonstrates is `haipipe-page-for-labeling`, in this plugin's own `skills/page-types/`, and that contract's `template.md` is the copy-and-fill version.
It lived on the boardform board as `QBt11` until 260808. It moved here because the steps it walks are this plugin's, not board form's, and a specimen belongs beside the thing it is a specimen of.
QG1-for-labeling.md

## Links
haipipe-page-for-labeling ../../skills/page-types/haipipe-page-for-labeling/SKILL.md
template.md ../../skills/page-types/haipipe-page-for-labeling/template.md
template-dash.md ../../skills/page-types/haipipe-page-for-labeling/template-dash.md
QB4 ../../../haipipe-toolkit/skills/diagrams/BoardSkillBoard-260722/3-QPs-page-structure/QPs1-overall/QPs1-overall.md
QB6 ../../../haipipe-toolkit/skills/diagrams/BoardSkillBoard-260722/3-QPs-page-structure/QPs2-page-types/QPs2-page-types.md
skills/subjective-label/SKILL.md ../../skills/subjective-label/SKILL.md
skills/page-workflows/label-init/SKILL.md ../../skills/page-workflows/label-init/SKILL.md
skills/page-workflows/label-round/SKILL.md ../../skills/page-workflows/label-round/SKILL.md
skills/page-workflows/label-evaluate/SKILL.md ../../skills/page-workflows/label-evaluate/SKILL.md
skills/page-workflows/label-complete/SKILL.md ../../skills/page-workflows/label-complete/SKILL.md
skills/page-workflows/label-status/SKILL.md ../../skills/page-workflows/label-status/SKILL.md
ref/ref-contract.md ../../ref/ref-contract.md
ref/ref-schema.md ../../ref/ref-schema.md
ref/ref-stages.md ../../ref/ref-stages.md
ref/ref-architecture.md ../../ref/ref-architecture.md
ref/ref-config.md ../../ref/ref-config.md
ref/ref-embeddings.md ../../ref/ref-embeddings.md
ref/ref-cascade.md ../../ref/ref-cascade.md
lib/embed.py ../../lib/embed.py
lib/sample.py ../../lib/sample.py
lib/label.py ../../lib/label.py
lib/classify.py ../../lib/classify.py
lib/converge.py ../../lib/converge.py
note-update-v3 _source/note-update-v3-260721.md
workflow-audit _source/260721-workflow-audit.txt
QA1-coldstart 2-QB-calibration-round/QB1-initialize-round-one/QB1-initialize-round-one.md
QA2-split-label 3-QC-selection-and-adjudication/QC3-compose-human-batch/QC3-compose-human-batch.md
QA3-weak-exam 5-QE-final-evaluation-and-completion/QE2-model-scorecard/QE2-model-scorecard.md
QB1-grow-140 3-QC-selection-and-adjudication/QC1-candidate-pool/QC1-candidate-pool.md
QB2-layered-eval 4-QD-optimization-and-convergence/QD2-round-metrics/QD2-round-metrics.md
QB3-external-license 5-QE-final-evaluation-and-completion/QE2-model-scorecard/QE2-model-scorecard.md
QC1-when-stop 4-QD-optimization-and-convergence/QD4-stopping-criteria/QD4-stopping-criteria.md
QC2-scale-out 5-QE-final-evaluation-and-completion/QE3-complete-corpus/QE3-complete-corpus.md
QC3-objective 1-QA-semantic-contract/QA1-system-contract/QA1-system-contract.md
QD1-embedding 2-QB-calibration-round/QB1-initialize-round-one/QB1-initialize-round-one.md
QD2-cascade 5-QE-final-evaluation-and-completion/QE3-complete-corpus/QE3-complete-corpus.md
QD3-train-classifier 3-QC-selection-and-adjudication/QC1-candidate-pool/QC1-candidate-pool.md
QD4-auto-lexicon 1-QA-semantic-contract/QA3-guideline-contract/QA3-guideline-contract.md
