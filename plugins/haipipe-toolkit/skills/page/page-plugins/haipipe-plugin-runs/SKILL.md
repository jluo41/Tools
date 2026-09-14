---
name: haipipe-plugin-runs
description: >-
  The internal Run Space presenter of Plugin Outline: Run P for human/Page
  interaction, Run E for Page-owned Evidence production, and Supporting Runs
  for inspectable external or upstream references that are never copied.
  Use for Discovery Paper Runs, Task Page
  runs, Labeling Runs, model/data jobs, run status tables, result details, or any Folder that
  exposes addressable Runs. Presentation only; the owning workflow controls
  Execute and closure. Trigger: Runs plugin, Runs tab, run overview, run status,
  run results, show the runs, /haipipe-plugin-runs.
metadata:
  version: "0.26.0"
  last_updated: "2026-09-13"
  # version history: ./CHANGELOG.md (skill-scoped, never loaded at invocation)
---

# /haipipe-plugin-runs · Outline's internal Run Space

**LOAD `haipipe-plugin`, `haipipe-plugin-outline`, and `haipipe-run` FIRST.**
This presenter owns no folder and has no top-level Plugin registration. It is
mounted inside `🧭 Outline` as Run Space. `/_board/runs` remains a
compatibility/internal route, not a separate Page tab.

```text
Run P             human ↔ Page interaction; `rpNN`
Run E             Page-owned Evidence attempt; VALUE/TABLE/DISPLAY/CITE Result
Supporting Runs   external/upstream Runs named by a Result; inspect, never copy
```

## 🏷 Runs, not Execution

Keep **Execute** as a workflow action. Name this plugin **Runs** because it
presents a collection of durable, addressable attempts. One Run is one logical
identity with an authored ticket and a generated Result:

```text
Run address  = ticket identity = Result identity
```

The Folder kind and workflow decide whether and when to Execute. Runs presents
either the Page-owned feedback history or the delegated Result that came back.
A non-Board integration may
omit the category entirely, and a Runs plugin may exist without reusable local
code. On a source-backed Page, however, Run Space stays available inside
Outline and reports all three empty lanes truthfully when nothing is allocated.

## 📍 Resolve the physical dialect

Pair by logical address, not by assuming Results always sit inside the Page
Folder. Detect the dialect from the surrounding contract:

```text
FOLDER-LOCAL · Discovery and standalone Folder
  <folder>/runs/<run>.sh
  <folder>/results/<run>/

DELEGATED PARAGRAPH WRITING TASK · same Folder, Markdown commission
  <folder>/runs/rNN_page-writing_cNN-pNN.md     includes input references + prompt
  <resolved-result>/paragraph.md + trace.md + runtime.yaml

JOB-BACKED TASK · canonical haipipe Task Page
  <job>/<task>/runs/<run>.sh
  <job>/results/<task>/<run>/
  optional input:  <job>/<task>/scripts/config/<run>.*
  optional record: <job>/notebooks/<task>/<run>.ipynb

LABELING JOB · subjective-label
  runs/<RUNNAME>.yaml
  results/<RUNNAME>/runtime.yaml
  results/<RUNNAME>/result.yaml
  result.yaml points to canonical P0-P5 artifacts without copying protected data
```

These are storage dialects of the same Run contract. Never copy or
symlink job-owned Results into the Task Page merely to make the first shape.
Never treat a Result folder as a fifth hierarchy level.

### Board and standalone Page separation

For a paper/Board Page, keep the two questions visibly separate:

```text
outline/evidence/supporting-runs/    Evidence Item → Supporting Runs + Local Run binding map
                   derived pointers only; may name zero-to-many external runs

runs/             actual page-local Runs only
results/          paired generated page-local Results only
```

The `🧭 Outline → Evidence Space` explains what Evidence has landed.
The sibling Run Space separates ownership rather than native family:
**Run P** comes from interactive-writing records; **Run E** comes from
Page-owned Evidence tickets/results; **Supporting Runs** resolve allocated
external/upstream identities from Result manifests or the compatibility index. A
`new-*` route or a parent `bN.jN.tN` without an `rN` is not a Run row. The
Page Run lane uses its own `rpNN` sequence; the Task Run lane retains every
owner-native identity, including ordinary `rNN` and Labeling `rlNN`. Do not
copy an external Ticket or Result into the Page, and do not create empty
`runs/` or `results/` merely to make planned work look allocated.

An empty inventory is valid: render separate `No Run P`, `No Run E`, and
`No Supporting Run` states. Do not mint placeholders.

Any Run token opens its exact Run Space row. Its single URL carries
`lens=run`, the owning Evidence Item `focus=run-<item-id>`, and the exact `run`
address. An Evidence chip uses `lens=evidence` to focus its Result row. Old
`lens=workspace&seg=items|runs` URLs are compatibility aliases.
Page Run records and Results are displayed as selectable repository-relative
text. For Task Runs, only the Result path crosses into the Page surface;
Ticket, command, log, actor, and Runtime paths remain with the native owner.
They are not raw browser links because artifacts may download rather than open.
That evidence-side detail separates Purpose/Plan, Availability, and
Next action; it does not misuse `new`, `rerun`, `run only`, and `ready` as one
lifecycle status. Normal chip navigation opens no popover. If an unresolved
address has no matching Runs card, any fallback inspector must explicitly
report that fact and remain closable within the mobile viewport.
Do not send an unallocated route to Runs merely because its text resembles a
Run id.

`scripts/`, config, and notebooks remain available through Folder/detail
inspection; they are not a fourth visible Run Space lane. A Run may instead
call a skill, CLI, API, or declared worker. Scripts are freestyle supporting
files: they need no manifest, internal grammar, or one-to-one Run binding. The
ticket's actual command is the authority for which files a Run invokes.

## Page Run · interactive writing history

The Page workflow's `interactive-writing` profile keeps one local Run row for
the entire goal, not rows for each Version, Step or review window. Its authored
Run points to paired `working.md`, root `runtime.yaml` and one append-only
`vNNN.md` journal per Version. Every Step in that Version is a section in the
same Markdown file.
The workflow, not this presenter, owns the human acceptance and close state.

Current Page Runs begin with the reserved `rp00_mermaid-structure`; paragraph
Runs start at `rp01` and use concise `rpNN_pNN[-pNN]` identities such as
`rp01_p01` and `rp02_p02-p03`. The exact
paragraph serial or range is always visible, while descriptive wording stays
in Goal. `rp` means Run of Page. This Page-local sequence is independent from
Task `rNN`, so both `rp01` and `r01` may exist in one Folder. The presenter
never assigns `rp` to delegated paragraph-writing, Discovery, or another Task Run.
There is no compatibility label or resolver fallback: any other
`interactive-writing` identity is shown as Held with an invalid-identity
finding, and it never substitutes for the required `rp00` structure Run.

If this dialect is exposed by a presenter, show the current Version, scope and
`waiting for feedback` explicitly (not an error). Opening a Page Run is a
reader-first projection, not a raw-record viewer: lead with Goal, Scope, Status,
Version/Step, the current Step's original request, its substantive saved result,
and the declared Next action. Render that Markdown as readable blocks. Keep
earlier Steps collapsed as semantic history, and keep repository paths and
record internals in a separate collapsed Technical details region. Do not put
frontmatter, hashes, or complete journal dumps in the default reading path.
Historical prose and code blocks must wrap without widening the phone viewport.
For `rp00_mermaid-structure`, reuse the Page's deterministic Mermaid renderer
so the saved result includes the actual labelled argument flow as well as its
paragraph index. On a phone, project the same Mermaid source as a larger
node-and-relationship reading sequence; do not shrink connector labels until
they are technically present but practically unreadable.
Never infer acceptance from file presence or a successful model call. History
is read-only and must not become another editable prose authority.

The read-only presenter shows the current Version/Step, treats
`waiting-for-feedback` as an ordinary waiting state, and safely previews the
owned Version journal. It may show `Waiting` only when the current Step section
contains both Human feedback and Saved result; unresolved records show `Held`.
It does not edit, approve, close, or
automatically capture feedback; the workflow remains the sole writer.

When a saved Step contains `#### Track changes`, render one card per feedback
item from its clean `Before` and `After` fields. Compute the smallest practical
word/punctuation-level spans: deletion is red and struck through, insertion is
green and underlined, and surviving context stays plain. Use whole-sentence
red/green only when the whole sentence was removed/added. Show the item's
classification, Why, and any available Inferred preference, Analysis status, or
Preference status; a missing preference is normal for a record-first Step.
Escape all stored text and never write visual markup back into the Version or
Page source.
Render a card only when both fields exist and differ. Equal/missing fields and
status, navigation, acceptance-only, or presenter-only feedback produce no
visual diff. The card heading is the classification source; do not require a
second classification table. Show only the current Step by default and keep
all earlier Steps collapsed.

## 🖥 Surface · overview first, detail on demand

```text
Run Space
├── Run P              human/Page feedback history
├── Run E              Page-owned Evidence Result
└── Supporting Runs    linked external/upstream Results
```

### Run overview

Show three compact tables rather than competing family ledgers. One row is one
logical Run; its Result is the returned half of that same row, never a separate
Results section. Native families appear only as origin/type metadata inside
Run E or Supporting Runs, never as additional lanes.

```text
Page Run                 Goal                     Version/Step  Status       Result
rp00 · Mermaid Structure Agree plan and map       v001/s003     ⏳ Waiting    history
rp01 · P01                Revise the opening       v001/s003     ⏳ Waiting    history

Task Run          Kind / Where         What happened                 Status       Result
r01_page-setup    Page setup · Local   10 sections; gate passed     ✅ Done      output
rl01_corpus-contract corpus-contract · Local  P0 contract landed    ✅ Done      output
b03.j01.t01.r02   Discovery · Linked    Working on — Smith 2025      🔄 Running   —
b02.j04.t01.r01   Execution · Task Job  Fitted the requested model   ✅ Done      output
```

`Local`, `Task Job`, and `Linked` are physical-origin labels inside the Task
Run lane, not new Run families or top-level lanes. A standalone Page's local
`rNN` keeps that exact identity; do not prefix it with Paper's `P` namespace.
Prefer a receipt-declared safe `outcome`/`summary` for **What happened**. For a
Folder-local Page setup Result, the presenter may derive a compact digest from
its bounded `report.md` and prefix the receipt's setup mode as a reader-facing
action such as `Created semantic records` or `Resumed and rebuilt Page`.
Otherwise show an honest state plus Target, such as
`Working on — <target>` or `Needs attention — <target>`; never invent a result.
Keep the fixed order Run P, Run E, Supporting Runs, including truthful empty
states; do not reorder or add lanes based on what happens to be nonempty.

Keep Task status vocabulary to `Ready · Running · Done · Failed · Held`.
Page Runs additionally use `Waiting` for `waiting-for-feedback`; it is not a
failure.
Derive it from the ticket and the owning Run contract's receipt/Result; do not
mint another hand-maintained status file. Put active or recovery-needed rows
first, then newer rows. Large and raw outputs remain counts or safe labels.

Reader-facing labels are always `Run` and `Result`. Legacy implementation
fields may still be named ticket/receipt internally, but the presenter must not
surface those words as alternative object names. Show literal repository-
relative Run and Result paths and allow them to wrap on narrow screens.

Clicking a Page Run opens its goal, scope, current state, latest original
feedback, substantive saved output, and next action. Earlier Steps remain
available behind one collapsed history control; paths and integrity metadata
remain behind collapsed Technical details. On narrow screens the overview
becomes stacked cards instead of compressing five table columns, and each row
keeps a visible expand indicator. Clicking a Task Run opens its Kind/origin,
purpose, concise outcome or current state, Result/output pointer, and consuming
Evidence Items when bindings exist. Do not print an empty Evidence field for
ordinary local work. Do not project Task
commands, logs, actors, Ticket paths, Runtime paths, or output trees into the
Page surface. Do not link directly to raw files; the Runs surface must not
trigger downloads.

The query `run=<exact-run-id>` is the stable reader-facing deep link for one
row. The server renders that row expanded so the current Step and collapsed
earlier history are immediately visible, and row interaction keeps the query in
sync. A Page Step response links this projection as **Current Run**; it never
links the presenter Python file, raw Version Markdown, or Result directory.

Delegated Paragraph Writing is a Task Run. Show `C<n>.P<m>` as Target;
expanding the row reads the
Markdown Run's instructions/prompt, `paragraph.md`, and `trace.md` inside the
Runs surface, without a raw-file link, download or popover. Render the text
safely and wrap it on mobile. A writing Ticket missing its runtime receipt
displays Held with a missing-receipt finding. A complete receipt missing either paragraph or
trace displays Held; file presence does not itself establish semantic quality
or promotion into Content. Writing Results are prose, not Evidence Items.

Page Evidence Item work and allocated Supporting Runs appear as Task Runs. The
overview preserves native kind; detail shows the safe target, Result/output,
and explicitly bound Evidence Item ids. Frozen input envelopes and unallocated
plans remain in Evidence Items. Historical PageX rows are migration input,
never extra Runs or Results. Never present a Result as a separate Run.

For Labeling rows, show safe identities, checksums, gate summaries, and counts
only. Never render sealed ids, protected text, raw judgments, or a second
approve/freeze/reveal/final/run control. A row may deep-link to the same Run in
the Labeling workbench; only the subjective-label workflow may operate it.
Use the operation name as the row Kind and the P0-P5 episode only as a grouping
label. Use `Local` as Where when the Labeling job is physically nested in this
Page Folder; `Labeling` is the native family, not a physical-origin value.
Never add a second row for the Round, Test, Scan, or Audit episode.

Surface an orphan or logical address mismatch as an error. A missing Result is
normal for `Ready` or `Running`; it is a finding only when the Run claims
`Done`. A generated Result is not Page evidence merely because it exists; an
evidence lane must bind or aggregate it.

### Scripts stay off-stage

Do not render a Scripts tree in Run Space. Scripts, config, notebooks,
commands, and logs remain available through Folder or the owning workflow.
Their existence must not add a fourth lane or extra summary block.

## 🧩 The four plugin things

```text
STORAGE   none of its own; resolve authored/generated Run projections
SURFACE   Outline → Run Space: Run P + Run E + Supporting Runs
WRITER    person/chat authors tickets; the ticket writes its paired Result
BOUNDARY  read-only presenter; no lifecycle, evidence, or closure authority
```

## 🔒 Boundaries

- **No browser run button.** Launch the exact ticket through the owning Task or
  Discovery workflow; long jobs keep that family's runner/tmux law.
- **No Result editing and no PHI.** Results are machine-written and inspected
  through receipts or safe summaries.
- **No lifecycle authority.** The owning workflow controls Execute, retry,
  terminal state, and Folder closure.
- **No scripts surface or requirement.** Only a Run ticket may invoke scripts
  when they exist; their absence does not invalidate a Run.

## 🗺 Status · 🟢 live 260912

Page-owned `live/runs.py` serves the read-only standalone and Board-hosted view.
The surface resolves Page writing history plus Folder-local, Supporting
Discovery, and canonical Job-backed Task Results, labels their origin, and
shows a concise outcome/state directly in the overview;
Discovery and Labeling workflow owners remain responsible for their own custom
allocation surfaces. The 📂 Folder tab remains the raw filesystem inventory.

## 📂 Files

- `../../../run/haipipe-run/SKILL.md` · the neutral Level-4 identity, pairing,
  receipt, and audit contract this surface presents
- `../../haipipe-plugin/ref/roster.md` · lane and presenter roster
- `../../../task/haipipe-task/ref/hierarchy.md` · Task Run address/dialect
- `../../../discovery/haipipe-discovery/ref/paper-run-contract.md` ·
  Discovery Folder-local dialect
- `../../../../../subjective-label/ref/ref-run.md` · Labeling operations,
  authority-owned resolver, gates, and protected surface boundary
