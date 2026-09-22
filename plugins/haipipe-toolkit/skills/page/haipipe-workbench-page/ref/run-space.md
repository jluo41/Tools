# Run Space · Outline's internal read-only Run presenter

**LOAD `haipipe-workbench`, `../SKILL.md` (`haipipe-workbench-page`), and `haipipe-run`
FIRST.** This reference is one lane contract of `haipipe-workbench-page`: the
read-only Run Space presenter. It owns no folder and has no top-level Workbench
registration. It is mounted inside `📃 Page` as Run Space. `/_board/runs`
remains a compatibility/internal route, not a separate Page tab.
Result-first cards for Page Writing, Page Evidence, and Supporting Runs are
projected from a Run Workflow Runtime and its Run Specs, including human
Scratch Runs; external or upstream Results remain inspectable references and
are never copied. Presentation only; the owning workflow controls Execute and
closure.

```text
Run Space
├── Workflow map (read-only definition view)
├── Page Writing
│   ├── Structure
│   ├── Scratch
│   ├── Section
│   ├── Paragraph (Review & Modify)
│   └── Revise (before · after · decisions)
├── Page Evidence
│   ├── Value
│   ├── Display
│   └── Citation
└── Supporting Runs
    ├── Task
    └── Discovery
```

The presentation names above are deliberately semantic. Internally, the
identity families remain RP (Page Writing), RE (Page Evidence), and owner-
native supporting Run ids. The UI does not expose those family codes as extra
lanes or hierarchy.

### Workflow map

Run Space also exposes a compact, read-only **Workflow map** tab. It is a
definition view of the canonical Workflow × Space Specification: rows are
planned Run Specs, columns are `Draft`, `Evidence`, `Run` (`runtime`), and
`Delivery`, and each cell shows `mode · schema · Page-relative path`. The map
explains the file-backed projection; it is not a fourth top-level Space,
Run inventory, or execution control. Concrete Run instances remain in the
three semantic tabs below it, and the map never writes, allocates, renames, or
copies a Run.

## 🧭 Run Workflow projection

Run Space is a read-only projection of one Workflow Runtime and its concrete
Run Instances. A card represents one Run Instance; the Workflow's Run Specs,
entry/exit gates, legal routes, and completion rule remain the authority behind
the projection. It may show the Runtime frontier and route history, but it does
not create a Run for a Step, gate decision, route decision, model call, or
Run compatibility label.

When a card opens, the reader may inspect the RunType, bounded target, current
Step, local gate evaluation, selected route, Result, and receipt. Human,
automatic/system, agent, and hybrid gate/route decisions are displayed as
recorded facts. Run Space never executes, edits, approves, closes, or invents
transitions; the owning Workflow/Run Spec skill does that.

## 🏷 Runs, not Execution

Keep **Execute** as a workflow action. Name this workbench **Runs** because it
presents a collection of durable, addressable attempts. One Run is one logical
identity with an authored ticket and a generated Result:

```text
Run address  = ticket identity = Result identity
```

The Folder kind and Run Workflow decide whether and when to Execute. Runs presents
either the Page-owned feedback history or the delegated Result that came back.
A non-Board integration may
omit the category entirely, and the internal Run presenter may exist without reusable local
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
  $OUTPUT_ROOT/<task>/results/<run>/
  optional input:  <job>/<task>/scripts/config/<run>.*
  optional record: $OUTPUT_ROOT/<task>/notebooks/<run>.ipynb

HISTORICAL TASK STORE · read through its recorded resolver
  <job-or-output-root>/results/<task>/<run>/

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
outline/<stem>-evidence-items.md      Evidence Item → Supporting Runs + Local Run contract
                   authored pointers; may name zero-to-many external runs

runs/             actual page-local Runs only
results/          paired generated page-local Results only
```

The `📃 Page → Evidence Space` explains what Evidence has landed. Run Space
then presents the semantic areas above: Page Writing, Page Evidence, and
Supporting Runs. The underlying Page Writing records are RP, Page-owned
Evidence records are RE, and Supporting Runs retain their owner-native ids.
A `new-*` route or a parent `bN.jN.tN` without an `rN` is not a Run row. Do not
copy an external Ticket or Result into the Page, and do not create empty
`runs/` or `results/` merely to make planned work look allocated.

An empty inventory is valid: render a truthful empty state in each relevant
subspace. Do not mint placeholders.

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

Current Page Runs use four explicit RP kinds: `rp-struct-NN` for the fused
SHAPE + SURVEY Structure Run (structure list, Outline Bullets, Point roles, and
evidence route decisions), `rp-scratch-NN_<target>` for human rough-thinking
capture, `rp-sec-NN` for Section-level writing, and
`rp-para-NN_Pxx[-Pyy]` for fixed paragraph or paragraph-group writing. A
Scratch target is a Section (`C1`) or whole paragraph group (`C1.P1`) in the
current Outline grammar. There is no separate subsection node, and B/symbol
rows are not Scratch targets. The initial Structure Run is `rp-struct-01`; examples of later
valid identities are `rp-scratch-01_C1.P1`, `rp-struct-02`, `rp-sec-01`, and
`rp-para-01_P03-P05`. SHAPE and SURVEY are Steps/cycles of `rp-struct-01`,
never separate planning cards.

Several people may participate in one Structure card. The presenter keeps one
Run and one paired Result, while the opened detail may show `participants` and
the current Step's `contributors`. A new participant or review pass does not
mint another RP identity; `rp-struct-02` requires a genuinely independent
post-closure structural goal.

The presenter shows the exact RP kind and preserves the distinction that a
Scratch Run is a small human capture interaction: Save keeps it open and a
human-confirmed Summary closes it. It does not edit Draft prose or require a
review cycle. A complete Section draft → review/rating → diagnose → revise
cycle is one Step inside the Section Run, not a new Run. A later independently commissioned
Section session receives another `rp-sec-NN` identity; a same-target
paragraph revisit normally reopens its existing Run in a new Version. The
Page-local RP sequences are independent from Task `rNN`, so both
`rp-para-01_P03` and `r01` may exist in one Folder. The presenter never assigns `rp` to delegated
paragraph-writing, Discovery, or another Task Run. There is no compatibility
label or resolver fallback: an identity whose kind or paragraph target does
not match its scope is shown as Held with an invalid-identity finding.

If this dialect is exposed by a presenter, keep the current Version, scope and
`waiting for feedback` available inside the opened Run, but do not lead with
them. Opening a Page Run is a result-first projection, not a raw-record viewer:
show the substantive saved Result first; put the current review input,
interpretation, and Next action behind one collapsed Review context; keep
earlier Results collapsed as semantic history; and keep repository paths and
record internals in a separate collapsed Technical details region. Do not put
frontmatter, hashes, Goal/Scope/Version metadata, or complete journal dumps in
the default reading path.
Historical prose and code blocks must wrap without widening the phone viewport.
For `rp-struct-01`, open the Result with the Page's Structure text (the same
plain text Draft Space shows at its top, read from the selected Outline): one
line per division and paragraph, so the saved result is read beside the
structure it settles. It is plain text and needs no phone-specific projection.
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

## 🖥 Surface · result first, detail on demand

```text
Run Space
├── Page Writing
│   ├── Structure
│   ├── Scratch
│   ├── Section
│   ├── Paragraph (Review & Modify)
│   └── Revise (before · after · decisions)
├── Page Evidence
│   ├── Value
│   ├── Display
│   └── Citation
└── Supporting Runs
    ├── Task
    └── Discovery
```

### Run overview

Use semantic card groups, not tables or competing family ledgers. A closed
card contains only three reader-facing facts: the Run's short name, what it is
doing, and one small status indicator. Do not show Goal, Scope, Version/Step,
paths, metadata, or a Result preview until the card is opened. One card is one
logical Run, and its Result is the returned content of that same card—not a
separate Results section.

Page Writing is split into Structure, Scratch, Section, Paragraph, and Revise.
Structure is the single SHAPE+SURVEY structure card; Scratch is the
human's rough-thinking capture card; Section is the section-writing card;
Paragraph is the paragraph-writing card; Revise is the change ledger card. Review
feedback on a candidate is input to the Section or Paragraph Run, expressed as
`Paragraph (Review & Modify)`. Revise is its own Run (`rp-revise-NN_<target>`,
`haipipe-page-revise`) with two doors: the person edits the paragraph's Draft
in one box in Draft Space → Revise, and every Save appends one Step whose
ledger holds one red/green card per changed Bullet with Decision `accept`; or an
agent compares two frozen texts of one target and writes the same ledger with
pending Decisions. Accepted Drafts stay in the Outline for the writing Run to
adopt as a Version. A Run may contain many review Steps/Versions, but the
card remains one Run.

Page Evidence is split into exactly Value, Display, and Citation. `TABLE` is a
legacy identity that presents as Display; `display_kind` such as table, figure,
diagram, illustration, or algorithm is content inside Display, not another
visible Run family. An evidence Result or Label is never presented as a
separate Run.

Supporting Runs use two columns: Task and Discovery. Group members by their
own parent Task, so one Task card may contain multiple owner-native R-level
Runs. The closed group card shows only the Task label, count, short activity,
and status. Opening it reveals each member and that member's actual Result on
demand. Supporting Tickets and Results remain external references: inspect
them through the projection, but never copy them into the Page.

Keep status vocabulary to `Ready · Running · Waiting · Done · Failed · Held`;
`Waiting` is normal for Page feedback and is not a failure. Derive status from
the owning ticket and receipt/Result. Put active or recovery-needed cards
first, then newer cards. Large or raw outputs remain behind the opened card.
Truthful empty states belong inside the relevant subspace; do not mint
placeholder Runs.

### Opened card

Opening any local or supporting card follows one order: substantive **Result**
first, then optional Review context or member context, then earlier Results,
then collapsed technical details. This makes the output—not its metadata—the
first thing a reader sees. Paths, hashes, frontmatter, Goal/Scope/Version
fields, commands, logs, actors, and output trees stay out of the default path.
Do not link directly to raw files or trigger downloads from Run Space.

For a Page Run, the Result is the current saved prose or structure list.
The current review input, interpretation, and Next action belong in one
collapsed `Review context`; earlier Steps/Versions belong in one collapsed
`Earlier results` history. The workflow remains the sole writer and closure
authority. On narrow screens, the same cards stack without compressing fields
into a table.

The query `run=<exact-run-id>` is the stable reader-facing deep link for one
card. The server renders that card expanded and keeps the query in sync with
open/close. A Page Step response may link this projection as **Current Run**;
it never links the presenter source, raw Version Markdown, or Result directory.

Delegated Paragraph Writing remains a Task Run. Show `C<n>.P<m>` only as the
short activity/target; opening the card reads its safe Markdown prompt,
`paragraph.md`, and `trace.md` as Result context. A missing receipt or missing
required output is Held. Writing Results are prose, not Evidence Items.

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
Their existence must not add a fourth area, subspace, or extra summary block.

## 🧩 The four workbench things

```text
STORAGE   none of its own; resolve authored/generated Run projections
SURFACE   Outline → Run Space: Page Writing · Page Evidence · Supporting Runs
WRITER    person/chat authors tickets; the ticket writes its paired Result
  BOUNDARY  read-only presenter; no Run Workflow, lifecycle, evidence, or closure authority
```

## Native inventory integrity

Follow `haipipe-run/ref/receipts-and-inventory.md` for the counting grain.
A Ticket without a receipt is Held with a missing-receipt finding, not Ready.
Ready requires an allocated planned receipt. Inspect the union of native
Tickets and Result/receipt stores; keep orphan and conflicting records visible.
Pair current Task output through its declared store and `<task>/results/<run>`
resolver, retaining the historical `results/<task>/<run>` fallback.
Paper judgment uses its native Ticket and human-closure journal; Design
Commission is a valid current Run alongside Generate and Verify. Retired
Adopt records remain historical evidence. None of these views allocates work.

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

`servers/workbench-page/runs.py` serves the read-only standalone and Board-hosted view.
The surface resolves Page writing history plus Folder-local, Supporting
Discovery, and canonical Job-backed Task Results, groups the reader-facing
areas into semantic cards, and shows the actual Result first when a card opens;
Discovery and Labeling workflow owners remain responsible for their own custom
allocation surfaces. The 📂 Folder tab remains the raw filesystem inventory.

## 📂 Files

- `../../../run/haipipe-run/SKILL.md` · the neutral Level-4 identity, pairing,
  receipt, and audit contract this surface presents
- `../../haipipe-workbench/ref/roster.md` · lane and presenter roster
- `../../../task/haipipe-task/ref/hierarchy.md` · Task Run address/dialect
- `../../../discovery/haipipe-discovery/ref/paper-run-contract.md` ·
  Discovery Folder-local dialect
- `../../../../../../subjective-label/skills/label-building/ref/ref-run.md` · Labeling operations,
  authority-owned resolver, gates, and protected surface boundary
