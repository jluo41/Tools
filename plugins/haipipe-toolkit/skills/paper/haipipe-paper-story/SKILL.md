---
name: haipipe-paper-story
description: >-
  Draft, review, revise, or draw one paper's prospective Story: its Seed, its
  research questions (each with hypotheses, claims, contributions and the work
  that tests them), Discovery Roadmap, Task Roadmap, related papers, and Section
  Narrative. Use to explain the whole paper from questions and evidence needs
  to its intended argument, to plan a new telling, or to redraw the Story's
  drawings in studio/. Execution release and receipt handling use the Paper
  workflow. Trigger: story, research question, hypothesis, claim, High-level
  logic, Low-level work, Related Papers, RoadMap Draw, workflow drawing,
  /haipipe-paper-story.
metadata:
  version: "0.18.0"
  last_updated: "2026-10-02"
  group-token: "Story<Letter>-<desk>-<idea-slug>"
  outline:
    mode: fixed
    title-match: exact
    source: "this SKILL.md"
    shape: "Identity → Pitch → Research Questions → Stakes → Evidence Basis and Boundaries → Discovery Roadmap → Task Roadmap → Section Narrative"
---

# /haipipe-paper-story · the prospective blueprint for one paper

For a discussion or content-structure sketch, apply this contract directly.
For a Page edit or build, load `haipipe-page`, `haipipe-page-workflow`, the
current Run Workflow/Spec owner, `haipipe-paper-workflow`, then this semantic
contract and relevant references. Their lifecycle records describe
how the Story is authored; this skill defines what the Story says.
For workflow, Section, or compiler integration, also read
[ref/integration.md](ref/integration.md).
Declare `page-type: story`. In a runtime paper board the page is:
`A1-Story/Story<Letter>-<desk>-<idea-slug>/Story<Letter>-<desk>-<idea-slug>.md`, for example `A1-Story/StoryA-misq-phytrait-discretion/StoryA-misq-phytrait-discretion.md`.

## 🔤 The Story id (JL 260908)

A Story id is three words joined by hyphens, and every part is read by a
stranger who never opened the folder:

```text
Story<Letter>-<desk>-<idea-slug>
  Letter      A, B, C … orders the Stories beside Story00-ideation (the pool);
              JL ruled letters, not numbers ("Story A, not Story 01", 260907)
  desk        the venue this Story is told to, lowercase: misq · jama · isr
  idea-slug   what the idea IS, two or three plain words: phytrait-discretion

StoryA-misq-phytrait-discretion     ✅ the MISQ telling of physician trait × discretion
StoryA-jama-phytrait-highdose       ✅ the JAMA telling, its own idea slug
Story-A                             ⛔ a bare letter says nothing (JL: "why this is just A? really silly")
Story01-agreeable-opioid            ⛔ numbers were rejected 260907
```

The folder, the page `.md`, every `draft/` stem and every `story-row:` path
carry the full id. The board parser accepts the bare `Story-A` form only to read
grandfathered boards; a new Story never mints one.

## 🧭 What the Story page IS

The Story is the shortest complete account of the paper the team intends to
make. A person reading it from top to bottom should understand:

1. what the paper is about and what it will not claim;
2. which questions organize the study and why answering them matters;
3. what is already known, supported, uncertain, or absent;
4. what external discovery must still clarify;
5. what study work must still produce;
6. what claims the resulting paper can make; and
7. how those claims will unfold, section by section, for the reader.

The Story is therefore a **prospective guide to the paper**, not a work
manual. It may exist before all evidence lands, but it must distinguish an
anticipated answer from an established finding. Its job is to make the future
paper legible while the work is still being planned.

```text
SEED · §1–§5
what the paper is, asks, values, already has, and refuses
        │
        ▼
DISCOVERY ROADMAP · §6
what the paper must learn from literature and external sources
        │
        ▼
TASK ROADMAP · §7
what evidence the study itself must produce
        │
        ▼
SECTION NARRATIVE · §8
how questions, claims, and evidence become a reader-ordered paper
```

The diagram is a reading order. Discovery and Task work may inform each other
and proceed in parallel; new evidence can revise any affected part of the
Story. The Story remains useful on day one, with unknowns explicitly named.

This page does not execute Discovery or Task work, mirror task folders, store
raw results, or write final manuscript prose. Operational identifiers, states,
paths, and receipts may appear as compact traceability fields only when they
help the reader understand whether a planned part of the paper is grounded.
They must not become the Story's organizing logic.

## 🌱 One Story, four integrated views

There is one Story for one paper idea. The former Seed, Roadmap, and Narrative
contracts are integrated here as four views of the same paper rather than as
separate planning pages:

```text
Seed                  defines the paper and its starting evidence boundary
Discovery Roadmap     plans knowledge the paper must obtain from outside itself
Task Roadmap          plans evidence the paper must generate through the study
Section Narrative     plans the claims and reader journey of the finished paper
```

The first five divisions are the Seed. They should remain comparatively stable
under a venue change. The Section Narrative may change substantially for a new
target; Discovery and Task plans change only when the new telling exposes a
real knowledge or evidence gap. A retarget must not silently turn the Story
into a different paper.

## 📐 Fixed Content outline

Use these eight divisions in order. The coverage bullets below describe the
content to include, not a fixed list of subsection names. Name instance
subsections for this paper's actual subjects, inquiries, analytical blocks,
and manuscript units. For example, a Discovery subsection can be “Prior work
on review-derived traits and prescribing”; its prose explains that inquiry's
question, scope, synthesis, and significance for this paper.

**Names (JL 260930).** A Story part is written `§N` or by its name (§7, the Task
Roadmap; a Task Roadmap row), as the file's own `### 7 · Task Roadmap` headings
are, never `C7`. `C1`, `C2` … are claim ids only (`- **1a** · C1 · from 1a`), and
`C1.P1.B1` stays the Page's Bullet address. The Paper Workbench shows none of these
codes: it shows Question N, Hypothesis 1a, Claim 1a, and each work row's name.

Each division opens with a short connected account of its role in the paper.
Tables compress the account and keep references inspectable; a table of
generic fields alone is insufficient. §6–§8 should make the planned study and
argument concrete enough to understand without opening an execution folder.
Keep row details in compact tables or subsection records rather than forcing
every field into an unreadably wide table.

### 1 · Identity

Cover:

- **Working title** — a concrete name for the paper being planned.
- **One-sentence identity** — phenomenon, relationship, or intervention and
  the paper's intended contribution in one sentence.
- **Study object and unit** — who or what is observed, at what level, in what
  setting and period.
- **Scope** — the population, construct, outcome, design family, and boundaries
  that make this paper one coherent object.

After §1, a reader should be able to say what paper this is without describing
its workflow or target venue.

### 2 · Pitch

Give the whole paper in one minute:

1. the tension or puzzle;
2. what the study examines or does;
3. the current or anticipated answer; and
4. who should care and why.

The Pitch is honest about time. An established answer cites an established
Evidence row. An anticipated answer is visibly marked `⟦pending E<n>⟧` or
written as a conditional expectation. A hoped-for result is never narrated as
if it already exists.

### 3 · Research Questions

Cover:

- **Primary Research Question** — the one question whose answer defines the
  paper's center.
- **Supporting Research Questions** — mechanism, consequence, heterogeneity,
  validity, or boundary questions needed to complete the primary answer.
- **Answer form** — what kind of evidence would answer each question, without
  presuming that the answer will be favorable.
- **Question logic** — which questions depend on others and how their answers
  jointly resolve the paper's puzzle.

Write one block per question (JL 260929: "the question is the main block"): a
`#### 3.N · Question N · RQn` heading, the question's own fields, then four
groups, each a bold label and one line per item. Every link is written once,
pointing up the chain, so the block reads as a narrative: the question, the
guesses at its answer, what the paper would claim, why a reader would care,
and the work that tests each guess.

```markdown
#### 3.1 · Question 1 · RQ1
- **Name**: <a short phrase, five words or fewer>
- **Question**: <one plain sentence: what we do to answer it>
- **Why the paper needs it**: <its job in the paper>
- **Answer form**: <what evidence would answer it>
- **Answer state**: <where the answer stands>
- **Section**: Results, Discussion

**Hypotheses**
- **1a** · <Short name>: <one plain sentence> · tested by E1
- **1b** · <Short name>: <one plain sentence> · tested by E2

**Potential claims**
- **1a** · C1 · from 1a · <Short name>: <the statement the paper would make>
  - **Role**: <primary · mechanism · scope …>
  - **Now**: <where it stands and what gates it>
  - **If it fails**: <what the paper becomes>

**Potential contributions**
- rests on 1a, 1b · <Short name>: <what the reader gains>

**Potential work**
- **T1** · for 1a, 1b
- **T9** · for 1a · b04.j03.t01, b04.j03.t02
- **D1** · for 1a, 1b
```

A question's **Name** is a short phrase of five words or fewer, often itself a question ("Model or data?", "Different Prediction Horizon"), the words the Paper Workbench prints beside "Question N"; the **Question** below it is one plain sentence saying what the paper does to answer it, with no field terms ("We make the model bigger, or give it more training data, and see which one lowers the forecast error."). The precise, technical wording belongs in the hypotheses and claims, not here (JL 260930: "the question here we have are just too long"). Items are coded by question: 1a, 1b under Question 1, 2a under Question 2 (JL 260929).

A question that sets the study's tasks instead of testing a guess (the pretraining task and
the downstream tasks every other question is scored on) comes first, as `#### 3.0 · Question 0
· RQ0`, and opens with a **Tasks** group, one line per task: `- Pretraining · Next reading:
<what the model reads, what it predicts, how it learns>` and `- Downstream · <Short name>:
<what it predicts and how it is scored>`. Its other groups say `- none: <why>` (JL 260930:
"we missed one important question about what is the task we used here … what is the
pretraining task, and also the downstream task"). The Paper Workbench draws the Tasks
first and leaves out the groups that are empty.
A hypothesis and the claim it yields share a code; a claim keeps its paper-wide id
(C1, C2, …, used by the Pitch, §8 and the Section Pages) right after its code. Every
item is a short name, a colon, and one plain sentence (JL 260929: "short-phrase-name:
explanation"), so the bold names alone read as the argument. A hypothesis guesses an
answer and names the §5 evidence rows (E1, E2, …) that test it. A claim says which
hypothesis it comes from; a hypothesis may yield no claim (a corollary the paper will
never claim says so as `- none: <why>`). A contribution names the claims it rests on.
A work item names a §7 Task or §6 Discovery row and the hypotheses it tests;
addresses after it narrow a row several questions use to the folders this question
needs. The foundation every question stands on (the training set, the model runs,
their scores) is not listed: its §7 row says `every question`, and it belongs to
every block. The Paper Workbench reads these blocks for its High-level logic +
Low-level work tab; the older one-row-per-RQ table is still read (`RQ | question |
why the paper needs it | answer form | Discovery | Task | intended claim/Section |
answer state`), with one hypothesis per §5 evidence row.

The RQ text describes the paper's inquiry. State and cross-references keep the
inquiry traceable, but they are secondary to the question and answer logic.
An RQ asks; a hypothesis anticipates an answer; an evidence proposition states
what is or could be supported. Operational checks need not become separate
RQs. One RQ can need several propositions and several inquiries or analyses.
“Answered” describes a supported answer, including a null or adverse answer;
it does not mean the hoped-for proposition was confirmed.

### 4 · Stakes

Explain why this particular paper deserves to exist:

- **Practical stakes** — the real decision, population, institution, or harm
  affected by the unanswered question.
- **Intellectual gap** — what current theory, evidence, or method cannot yet
  explain.
- **Contribution promise** — what becomes newly knowable if the paper succeeds.
- **Why this study** — why this setting, data, design, or combination can close
  the gap.
- **Why it is worth finishing** — what remains informative if expected results
  fail, and under which outcomes the paper must be narrowed, redesigned, or
  abandoned. A null result does not automatically establish a publishable
  contribution.

### 5 · Evidence Basis and Boundaries

State the paper's current evidence position, beginning with the starting
material and updating it as findings become available:

- **Source Pages and provenance** — the bounded pages, datasets, prior outputs,
  and ideation origin the Story is allowed to read.
- **Existing evidence basis** — what is already supported and the evidence on
  which that support rests.
- **Evidence gaps** — what remains provisional or absent and therefore creates
  a need in §6 or §7.
- **Novelty basis** — closest prior work and the proposed delta at claim level,
  with unresolved verification made visible.
- **Assumptions and open tensions** — unresolved choices that could change the
  interpretation or final arc.
- **Hard boundaries and non-claims** — causal, construct, population,
  generalization, ethical, or venue claims the paper will not make.

Use an E-row for each consequential proposition the paper may eventually
defend:

```text
E | RQ | proposition | support state | basis or missing evidence | interpretation boundary
```

The E-board contains propositions, not errands such as “add three references.”
Unfinished work belongs in §6/§7 or the relevant Section's open needs. Link
one or more RQs and claims as appropriate; do not force one E-row per RQ.
Separate evidence support (established / provisional / absent / contradicted /
inconclusive) from execution progress. A completed, accepted analysis can
contradict a proposition. Keep that result and its implication visible.

The Novelty basis also holds the **P-board** (JL 260930): the papers this study
stands beside, one row each, each held as a Discovery Paper Run (a §6 row names the
Discovery Task that holds them):

```text
P | paper | role | question | why it matters | keep | bears on | Discovery Run
```

`role` is `closest`, `question`, `background` or `caution`; `question` is an RQ id
or `all`; `Discovery Run` is the Paper Run's address (`b01.j02.t01.r01`). Search the
venue the paper is written for first (JL 260930: "我们选 paper 一定要选一个 venue 的"),
then add papers from other venues (JL 260930: "this is not limited to NMI"). The why
line says in plain words what the paper shows for this study, from what was read (its
abstract, or the PDF when the row says so). The Paper Workbench draws the P-board as
Story › Related Papers: the target venue's papers first, then other venues, one card
per row with the Run's `paper.pdf` inside.

`keep` and `bears on` are optional (JL 261002: "make the related works be something we
should keep"). `keep` says why THIS study keeps the paper: what it takes from it, or
what it must answer. It is about this study, not a summary of the paper, and the card
shows it as "Why we keep it" in place of the why line. `bears on` marks this study's
questions, separated by `;`, each with one verdict: `supports`, `limits`,
`contradicts`, `method` (a method borrowed) or `frames`, as in `RQ1 limits; RQ2
supports`. The paper's own logic and work is not written here: it is the Paper Run's
`logic-work.yaml` (haipipe-discovery 0.21.0), so every Story that cites the Run shows
the same reading.

“Established” requires inspected evidence with adequate scope. User-reported
availability is a labeled planning input until verified; a path or receipt
alone establishes neither validity nor the substantive conclusion. Do not
invent missing sources, units, coefficients, methods, or novelty verdicts.
Name design choices as proposed when the supplied material does not decide
them. §5 summarizes the finding and limitation with a source reference; it
does not reproduce raw tables. These Story proposition ids are distinct from
typed Page Evidence Item ids such as `E01-VALUE-...`.

The E-board is a map of the paper's support, not a run log. Every provisional
or absent central E-row must point forward to a Discovery or Task need. Every
established row must point backward to a real source. A null or contradictory
result may limit, redirect, or defeat a proposition; the Story must show that
branch rather than assume success.

### 6 · Discovery Roadmap

**The Roadmap is question first (JL 260928).** §6 opens with a few general
questions; each D row (here) and each T row (§7) serves one of them and names
the BJTR folder (Block › Job › Task › Run) that answers it. Read top down:
general question → its T and D questions → their folders.

```text
Q | general question | serves        a few rows (about five), each a short plain question;
                                     `serves` names the RQs, or `the whole paper`
```

Every D and T row leads with a **short plain question** a reader understands
without the paper ("Has anyone shown this link before?"), carries a `folder`
cell with its BJTR address (`b01.j05`, `b03.j02.t06`, a range such as
`b03.j02.t01–t03`, or `none yet`), and ends with a `Q` cell. Row ids are `D<n>`
and `T<n>`; never `B<n>` (a leftover Block Board id that reads as a Block).
A new T or D starts as a question; its folder is created from it by
haipipe-task or haipipe-discovery, which then writes the address into the
row. A folder the paper uses that no row names is a missing question: add one.

Describe the knowledge the paper must obtain from literature, external sources,
or source interpretation before its claims and framing are defensible. Cover:

- **Discovery gaps** — what the team does not yet understand about novelty,
  theory, construct validity, mechanism, context, counterevidence, method, or
  interpretation.
- **Discovery questions** — the specific questions each inquiry must answer.
- **Source universe and boundary** — which literatures, corpora, policy records,
  precedents, or external materials must be covered, and what falls outside the
  inquiry.
- **Expected synthesis** — the form of knowledge the paper needs back: a
  landscape, closest-prior comparison, theory bridge, construct boundary,
  counterargument, method precedent, citation set, or venue reading.
- **Story consequence** — how each possible discovery could confirm, narrow,
  reposition, or preempt an RQ, claim, boundary, or contribution.
- **Order and coverage** — what must be understood first and which RQ, E-row,
  and Section each discovery will inform.

Use one row per discovery need:

```text
D | name | question | folder | what it must settle | source scope | expected synthesis | possible story consequence | feeds RQ/E/Section | Q
```

Distinguish essential inquiries from useful extensions and state dependencies
that affect the paper's feasibility. Reuse inspected existing syntheses when
they already answer the question; the roadmap covers the paper's knowledge
needs, not only new searches. Venue-related discovery can be included when it
informs §8; it must not rewrite the Seed's factual identity.

The roadmap states **what must become known and why it matters to the paper**.
Owner, folder, run, and status may be linked in a compact suffix; they do not
replace the substantive cells above. Discovery completion means the Story can
make a bounded intellectual decision, not merely that a search was run.

### 7 · Task Roadmap

Describe the evidence-producing study work required to answer the RQs. Cover:

- **Evidence needs** — the empirical, computational, qualitative,
  measurement, validation, or robustness evidence each claim requires.
- **Analytical questions** — what each task must determine for the paper.
- **Study material and design** — the relevant data, cohort, variables,
  comparison, model, experiment, or evaluation at Story-level resolution.
- **Required contrasts and checks** — the comparisons that separate the
  paper's interpretation from plausible alternatives.
- **Expected result form** — the table, estimate, pattern, model comparison,
  case synthesis, or validation result needed to answer the question; this is
  an output shape, not a preferred outcome.
- **Interpretation and failure branches** — what positive, null,
  contradictory, or infeasible outcomes would allow the paper to claim, force
  it to narrow, or require it to drop.
- **Dependency and destination** — what must precede the task and which RQ,
  E-row, claim, display, and Section its result will serve.

Use one row per coherent paper-level evidence block, named as the question it
answers and tagged with its stage, and order the work as it runs (JL 260929:
"the work should follow the logics"; name it "in the question format"):

```text
T | name | question | stage | study material and design | required contrast | result form | interpretation branches | depends on | feeds
```

Stages, in run order: `data` (build or profile the data), `training` (train the
models), `evaluation` (score them, or add a new readout), `results` (collect the
scores and fit), `analysis` (one contrast or refit per row), `figures` (draw the
displays). Include the upstream work (data, training, evaluation) even when it
already ran: a paper whose Task Roadmap starts at analysis hides what its
numbers stand on. A row every research question needs says `every question` in
its feeds cell; the others are named by the §3 question blocks. Like a §3 question,
a T or D row has a `name`, a short phrase of five words or fewer ("Still true
without the cap?"), and a `question`, one plain sentence saying what we do ("We refit
the law without the upper limit we set on it, and check whether bigger models still
stop helping."), not "Refit α with the bound relaxed"; the Paper Workbench prints the
name beside the stage and the sentence below (JL 260930). Write its folders in full in the feeds or
design cell (`Task: b04.j01.t01, b04.j01.t02.`); work built in another project
names that project's path.

Distinguish the evidence needed for a sufficient paper from optional analyses.
Describe meaningful dependencies and feasibility limits (available data,
required access or prohibitive cost) where they change the study's scope.
Bind existing accepted results before proposing new computation. Study
completion is judged by interpretable evidence and reported uncertainty, not
by obtaining the desired sign or statistical significance.

The Task Roadmap says **what the study must produce for the paper to be
answerable**. Detailed jobs, configurations, commands, budgets, retries, and
run receipts belong in the Task layer. A compact task id or result link is
traceability, not Story content.

### 8 · Section Narrative

Show how the finished paper will turn the Seed, discoveries, and produced
evidence into one reader-ordered argument. Cover:

- **Target reader and venue promise** — when a target is selected, who the
  paper addresses, the question that reader brings, and the contribution the
  telling promises without changing the Seed's identity.
- **Claim system** — each exact proposition, its role, E-row parent, evidence
  state, boundary, and intended landing place. When §3 Research Questions
  holds the hypotheses (one block per question), this §8 Section Narrative
  names their roles and points to §3 instead of restating each statement.
- **Argument arc** — the dependency order among puzzle, gap, mechanism,
  evidence, boundary, contribution, and implication.
- **Reader journey** — what the reader believes, asks, sees, and may conclude
  at each turn.
- **Per-section narrative** — one detailed row for every manuscript and
  appendix Section in reader order.
- **Evidence and display allocation** — where each discovery, study result,
  citation, table, figure, and appendix object does narrative work.
- **Transitions, cut rules, and open risks** — what each Section receives from
  the previous one, what the next may assume, and how the paper changes when a
  planned evidence item does not land.
- **Compile order** — the final main-text and appendix order as a projection of
  the Section rows.

Each Section row must cover:

```text
Section | reader question | reader entry state | ordered moves | must establish | must refuse | Discovery/Task evidence | display | reader exit state | transition / cut rule
```

Keep the paper-wide claim system, argument arc, and reader journey explicit
before the detailed Section map; they cannot be inferred merely from section
titles. A claim has a stable id, precise proposition, E-row support, rhetorical
role, and limit. Planned claims remain conditional where support is missing.
One claim may appear in several Sections for different reader purposes.

The selected target/category and its binding Venue contract belong here.
An unselected target stays open; no target selection is inferred from a sample
outline. Later rebindings record the user's decision. Scope, data and prior
evidence survive retargeting unless a substantive change is explicitly made.

A planned Section can have a stable Story row before its Page exists; distinguish
its proposed identity from a real file path. An execution release is a separate
workflow decision, never implied by including the Section in the blueprint.
Preserve exact existing Section ids when repairing an established paper.

The row should be rich enough that a fresh Section writer can understand its
job without inventing the paper's logic. It should not contain final prose.
The Section Narrative ends with a whole-paper reading: why the sequence is
necessary, how the primary answer accumulates, where the strongest boundary
enters, and what the reader should carry away from the conclusion.

## 🧵 Evidence is the through-line

Evidence is not a separate ninth division and not synonymous with execution:

```text
§5  states the evidence the paper starts with and the limits it already knows
§6  identifies outside knowledge needed to interpret and position the paper
§7  identifies study evidence needed to answer the paper's questions
§8  assigns both kinds of evidence to claims, displays, and reader turns
```

Every central claim should therefore be readable as one continuous line:

```text
RQ → starting E-row → Discovery need and/or Task need → interpreted claim → Section landing
```

If that line breaks, the Story has exposed a real paper gap. It should show the
gap rather than fill it with operational detail or aspirational prose.

## 🖼 Drawings of the Story · the RoadMap Draw tab

A paper may keep drawings of its Story in `<paper>/studio/`, shown in Story ›
RoadMap Draw. Each drawing is written by its own script beside it,
`studio/make_<name>.py` → `studio/<name>.excalidraw`. The script reads the Story
when it runs (the §3 question blocks, Question 0's Tasks, the §5.2 E-board, the §6
and §7 tables) and reads numbers from the files that hold them, so the drawing
follows the Story instead of copying it. **draw** mode reruns every
`studio/make_*.py` and looks at the result in RoadMap Draw (the `Redraw` card in
`haipipe-paper-workflow/ref/run-cards.md`). The `.excalidraw` is generated: change
the script or the Story and rerun it, never the drawing; a box moved by hand in
the editor goes back on the next run.

The first one is the workflow drawing of Paper-ScalingGlucose-NatSeries2026
(WellDoc-SPACE, `examples-2-nn/Proj11-CGM-FM/papers/Paper-ScalingGlucose-NatSeries2026/studio/make_paper_workflow.py`,
JL 260930): data → pretraining task → downstream tasks → one law, then one row
per question: analysis → hypothesis and claim → where the answer lands. For a new
paper, copy it and change only its SPEC (the card text, the task folders, the
state of each piece of work); its Story reader works on any Story with §3
question blocks.

## 🎯 Aims · what the Story must make clear

Use the shared Page Aim form: `Target`, `Done when`, and factual `Now`.
A1–A8 map to §1–§8 with matching names. Their tests judge the Story's explanatory
content, not whether the future study has finished.

| Aim | Read-through test |
|---|---|
| A1 Identity | The paper's object, unit, scope, and identity are clear. |
| A2 Pitch | The whole paper is understandable in one minute, with honest uncertainty. |
| A3 Research Questions | Questions and answer forms form one coherent inquiry. |
| A4 Stakes | The practical problem, intellectual gap, and conditional contribution are clear. |
| A5 Evidence Basis and Boundaries | Sources, support, gaps, and non-claims are distinguishable. |
| A6 Discovery Roadmap | Needed knowledge, source coverage, synthesis, and story consequences are concrete. |
| A7 Task Roadmap | Study design, contrasts, outputs, dependencies, and outcome branches are concrete. |
| A8 Section Narrative | Claims, reader journey, Section moves, evidence allocation, and ending fit together. |

An Aim may be satisfied by clearly describing an unresolved research need;
that does not answer the RQ or establish its E-row. CHECK remains the shared
Page controller check, not a ninth Content division or automatic approval.

## ✅ Story CHECK · does the paper read clearly from start to finish?

CHECK the built Story as a prospective paper, not as a record of finished work:

- Can a new reader state the paper's identity, primary RQ, answer form, and
  stakes after §1–§4?
- Does §5 distinguish established, provisional, absent, contradicted, and
  inconclusive evidence as applicable and state
  the paper's non-claims?
- Does every consequential external knowledge gap appear in §6 with a clear
  synthesis and story consequence?
- Does every consequential evidence gap appear in §7 with an analysis design,
  result form, interpretation branches, and paper destination?
- Can every central claim be traced from RQ and E-row through Discovery/Task
  evidence into exactly the Sections that use it?
- Does §8 explain the paper's claim order, reader journey, section jobs,
  evidence/display allocation, transitions, cut rules, and ending?
- Are anticipated results visibly distinguished from established findings?
- Could the Story remain intellectually coherent under a null or adverse
  result, or does it state exactly which claim and Section would change?
- Has runbook material stayed in the owner layer rather than displacing the
  paper logic on this page?

The Page still uses the generic `CONTEXT → OUTLINE ⇄ EVIDENCE → CONTENT →
CHECK` lifecycle. Those records document how this Page was built; they are not
additional Story Content divisions.

## 🛑 Draft and human version gate

This Story skill remains the `v0.9.1` design draft. Both the skill contract and
new Story outlines remain `v0.x` until the user explicitly authorizes the
respective promotion. Preserve existing genuine approvals; never copy them
onto a changed structure. New or structurally revised outlines carry
`approved: ⬜`. Approval to edit, a passing CHECK, successful tests, another
agent's recommendation, or a router's version is not permission to label this
skill or an outline `v1` or “current approved law.” Record approval only for
the exact artifact/version the user approved.

On an existing Story, inspect the current content, outline, Aims, and source
bindings before revising. Preserve research facts, ids, provenance, and prior
decisions. Carry old Seed, Roadmap and Narrative content into the relevant
divisions without reinterpreting findings from their status symbols. Do not
recreate deleted planning pages or compatibility registries. Do not rename or archive whole
paper trees merely because this contract changed.

This variant owns no execution scripts. Discovery, Task, Run, Section, and
Compile owners keep their detailed artifacts; the Story keeps the prospective
paper logic that connects them.
