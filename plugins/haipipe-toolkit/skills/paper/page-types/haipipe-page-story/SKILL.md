---
name: haipipe-page-story
description: >-
  Paper journey phase P1 (Story) and the Page Type contract for one lettered
  Story page: a forward-looking blueprint from which a reader can understand
  the whole paper, what it still needs to learn and produce, and how the final
  argument will unfold. Integrates the Seed, Discovery Roadmap, Task Roadmap,
  and Section Narrative on one page. Use when starting, reviewing, repairing,
  or retargeting a paper's overall story. Not an execution runbook or receipt
  register. Trigger: story page, seed, paper blueprint, research questions,
  discovery roadmap, task roadmap, section narrative, paper story.
metadata:
  version: "0.9.1"
  last_updated: "2026-09-07"
  group-token: "Story-<letter>"
  outline:
    mode: fixed
    source: "this SKILL.md"
    shape: "Identity → Pitch → Research Questions → Stakes → Evidence Basis and Boundaries → Discovery Roadmap → Task Roadmap → Section Narrative"
---

# /haipipe-page-story · the prospective blueprint for one paper

Load `haipipe-page` first and `haipipe-page-workflow` when building the Page.
Declare `page-type: story` (`page-type: seed` is a historical compatibility
alias). In a runtime paper board the page is:
`A1-Story/Story-<letter>/Story-<letter>.md`.

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
SEED · C1–C5
what the paper is, asks, values, already has, and refuses
        │
        ▼
DISCOVERY ROADMAP · C6
what the paper must learn from literature and external sources
        │
        ▼
TASK ROADMAP · C7
what evidence the study itself must produce
        │
        ▼
SECTION NARRATIVE · C8
how questions, claims, and evidence become a reader-ordered paper
```

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

Use these eight divisions in order. Subsections describe what the Story must
say about the paper; they are not instructions for operating a workflow.

### 1 · Identity

Cover:

- **Working title** — a concrete name for the paper being planned.
- **One-sentence identity** — phenomenon, relationship, or intervention and
  the paper's intended contribution in one sentence.
- **Study object and unit** — who or what is observed, at what level, in what
  setting and period.
- **Scope** — the population, construct, outcome, design family, and boundaries
  that make this paper one coherent object.

After C1, a reader should be able to say what paper this is without describing
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

Use one row per RQ:

```text
RQ | question | why the paper needs it | answer form | Discovery | Task | intended claim/Section | answer state
```

The RQ text describes the paper's inquiry. State and cross-references keep the
inquiry traceable, but they are secondary to the question and answer logic.

### 4 · Stakes

Explain why this particular paper deserves to exist:

- **Practical stakes** — the real decision, population, institution, or harm
  affected by the unanswered question.
- **Intellectual gap** — what current theory, evidence, or method cannot yet
  explain.
- **Contribution promise** — what becomes newly knowable if the paper succeeds.
- **Why this study** — why this setting, data, design, or combination can close
  the gap.
- **Why it is worth finishing** — what changes for research or practice even if
  some expected results fail.

### 5 · Evidence Basis and Boundaries

State the paper's starting position before new Discovery and Task work:

- **Source Pages and provenance** — the bounded pages, datasets, prior outputs,
  and ideation origin the Story is allowed to read.
- **Existing evidence basis** — what is already supported and the evidence on
  which that support rests.
- **Evidence gaps** — what remains provisional or absent and therefore creates
  an obligation in C6 or C7.
- **Novelty basis** — closest prior work and the proposed delta at claim level,
  with unresolved verification made visible.
- **Assumptions and open tensions** — unresolved choices that could change the
  interpretation or final arc.
- **Hard boundaries and non-claims** — causal, construct, population,
  generalization, ethical, or venue claims the paper will not make.

Use an E-row for each consequential proposition the paper may eventually
defend:

```text
E | RQ | proposition | established / provisional / absent | basis or missing evidence | interpretation boundary
```

The E-board is a map of the paper's support, not a run log. Every provisional
or absent central E-row must point forward to a Discovery or Task need. Every
established row must point backward to a real source. A null or contradictory
result may limit, redirect, or defeat a proposition; the Story must show that
branch rather than assume success.

### 6 · Discovery Roadmap

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
D | what the paper must learn | question | source scope | expected synthesis | possible story consequence | feeds RQ/E/Section
```

The roadmap states **what must become known and why it matters to the paper**.
Owner, folder, run, and status may be linked in a compact suffix; they do not
replace the substantive cells above. Discovery completion means the Story can
make a bounded intellectual decision, not merely that a search was run.

### 7 · Task Roadmap

Describe the evidence-producing study work required to answer the RQs. Cover:

- **Evidence obligations** — the empirical, computational, qualitative,
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

Use one row per coherent paper-level evidence block:

```text
T | evidence obligation / analytical question | study material and design | required contrast | result form | interpretation branches | depends on | feeds RQ/E/Section
```

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
  state, boundary, and intended landing place.
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

The row should be rich enough that a fresh Section writer can understand its
job without inventing the paper's logic. It should not contain final prose.
The Section Narrative ends with a whole-paper reading: why the sequence is
necessary, how the primary answer accumulates, where the strongest boundary
enters, and what the reader should carry away from the conclusion.

## 🧵 Evidence is the through-line

Evidence is not a separate ninth division and not synonymous with execution:

```text
C5  states the evidence the paper starts with and the limits it already knows
C6  identifies outside knowledge needed to interpret and position the paper
C7  identifies study evidence needed to answer the paper's questions
C8  assigns both kinds of evidence to claims, displays, and reader turns
```

Every central claim should therefore be readable as one continuous line:

```text
RQ → starting E-row → Discovery need and/or Task need → interpreted claim → Section landing
```

If that line breaks, the Story has exposed a real paper gap. It should show the
gap rather than fill it with operational detail or aspirational prose.

## ✅ Story CHECK · does the paper read clearly from start to finish?

CHECK the built Story as a prospective paper, not as a completed work ledger:

- Can a new reader state the paper's identity, primary RQ, answer form, and
  stakes after C1–C4?
- Does C5 distinguish established, provisional, and absent evidence and state
  the paper's non-claims?
- Does every consequential external knowledge gap appear in C6 with a clear
  synthesis and story consequence?
- Does every consequential evidence gap appear in C7 with an analysis design,
  result form, interpretation branches, and paper destination?
- Can every central claim be traced from RQ and E-row through Discovery/Task
  evidence into exactly the Sections that use it?
- Does C8 explain the paper's claim order, reader journey, section jobs,
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

This is a `v0.9.1` design draft. Keep every generated Story outline at `v0.x`
with `approved: ⬜` unless the user explicitly approves it. No CHECK result,
agent recommendation, apparent completeness, or previous discussion may
create or promote a `v1.0` outline without the user's direct invitation.

This variant owns no execution scripts. Discovery, Task, Run, Section, and
Compile owners keep their detailed artifacts; the Story keeps the prospective
paper logic that connects them.
