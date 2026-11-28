§6 Discovery Roadmap and §7 Task Roadmap of a Story, with the short Run table and §9 Venues that follow §7 (hai-paper-story).

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
hai-task or hai-discovery, which then writes the address into the
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

A telling drawn by hai-draw story keeps a short table instead, one row per Run it waits on: `| T | work |
where | state | starts |`, where `state` is done, ticket next or not started, and `starts` says who presses Run, or
`<person> starts` when the Run costs new model calls (drawn red). The rows stay here; `s03-paper-dataflow/`
(hai-paper-plan) draws how the data flows through them to each question, without copying them.

After §7 the telling's face keeps **§9 · Venues**, its venue list from the target down to the fallbacks: one row per
venue (`| V | venue | kind | editor's test | why it fits | leads with | still needs | desk record |`; the `editor's test`
cell is the short decision of that venue's editor's test, shown as the first row of its venue card, JL 261111; the
detail, a fresh-context desk screen with its decision, biggest risk, verdicts and changes, is a Board Question report
`reports/qNN_editor_test_<venue slug without hyphens>/`, which the card opens; the report keeps a
`**To raise the odds**` numbered list, each item's first sentence one plain change, which the card shows as "To pass
the desk"). A venue changes which questions
lead, not the questions; each venue's rules stay in its hai-paper-venue desk record (JL 261019: "我们要不要把这个 venue 直接塞到这个 story 里面去？ ... 也要想想它适合什么样的 journal，然后搞出来一个 journal list or conference list"). §8, the Section
Narrative, lives on the selected Story topic. Each writing version's `## Narrative`
records that send's layout (one row per Section, claims to displays, compile order), linked to its Story
through `tells:`; it is not a second authoring location for the title, story or claims.
