---
name: haipipe-plugin-runs
description: >-
  The Runs presenter of a Folder: one ⚙️ surface over authored Run
  tickets and their paired generated Results. Its neutral overview schema groups
  Runs as Execution, Discovery, Page, or Labeling when the owning Folder surface
  exposes those families; Page divides into Evidence
  Item, Division Writing, and Display, while Labeling groups its independently
  closable operations by P0-P5 episode. A second, collapsible Scripts region shows freestyle
  implementation files when present. Use for Discovery Paper Runs, Task Page
  runs, Labeling Runs, model/data jobs, run status tables, result details, or any Folder that
  exposes addressable Runs. Presentation only; the owning workflow controls
  Execute and closure. Trigger: Runs plugin, Runs tab, run overview, run status,
  run results, show the runs, /haipipe-plugin-runs.
metadata:
  version: "0.9.7"
  last_updated: "2026-09-04"
  # version history: ./CHANGELOG.md (skill-scoped, never loaded at invocation)
---

# /haipipe-plugin-runs · one surface for addressable Runs

**LOAD `haipipe-plugin` and `haipipe-run` FIRST.** This is a PRESENTER plugin
(`haipipe-plugin` §🔌): it owns no folder and has no roster row. It presents
the Run projections already owned by the Folder or its containing Task Job.
It is an optional presenter beneath a Folder's Task Face, never a replacement
for that Face or its workflow authority.

## 🏷 Runs, not Execution

Keep **Execute** as a workflow action. Name this plugin **Runs** because it
presents a collection of durable, addressable attempts. One Run is one logical
identity with an authored ticket and a generated Result:

```text
Run address  = ticket identity = Result identity
```

The Folder kind and workflow decide whether and when to Execute. Runs only
presents what was launched and what came back. A non-Board integration may
omit the category entirely, and a Runs plugin may exist without reusable local
code. On a source-backed Board Page, however, the Runs tab stays visible and
may truthfully report that no local Run is allocated.

## 📍 Resolve the physical dialect

Pair by logical address, not by assuming Results always sit inside the Page
Folder. Detect the dialect from the surrounding contract:

```text
FOLDER-LOCAL · Discovery and standalone Folder
  <folder>/runs/<run>.sh
  <folder>/results/<run>/

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

### Board Page separation

For a paper/Board Page, keep the two questions visibly separate:

```text
outline/evidence/supporting-runs/    Evidence Item → Supporting Runs + Local Run binding map
                   derived pointers only; may name zero-to-many external runs

runs/             actual page-local Runs only
results/          paired generated page-local Results only
```

The `🧭 Outline → Evidence Workspace` explains why an Evidence exists and
groups its related Run cards by Evidence. Its internal `Runs` lens includes
every mapped Supporting and Paper-local route, including planned routes, and
reports mappings separately from unique Run identities. The top-level `⚙️ Runs`
plugin lists only a
physical Run found in the page's own
`runs/` tree and its paired local Result. A `new-*` route, a parent `bN.jN.tN`
without an `rN`, an external Supporting Run, or a result copied for display is
not a local Runs row. Do not create empty `runs/` or `results/` merely to make
planned work look allocated.

An empty local inventory is still a valid presenter state: render one compact
“No local Run allocated” message. Do not hide the tab and do not infer that an
external Supporting Run is local.

Accordingly, a Run token in the Outline first deep-links to the owning
Evidence Item card in the Outline workspace. From there, allocated Run,
Result, and Runtime paths are displayed as selectable repository-relative text;
they are not raw browser links because scripts and receipts may download rather
than open. That evidence-side detail separates Purpose/Plan, Availability, and
Next action; it does not misuse `new`, `rerun`, `run only`, and `ready` as one
lifecycle status. Do not send an unallocated or external
route to this local Runs overview merely because its text resembles a Run id.

`scripts/`, config, and notebooks are optional projections. A Run may instead
call a skill, CLI, API, or declared worker. Scripts are freestyle supporting
files: they need no manifest, internal grammar, or one-to-one Run binding. The
ticket's actual command is the authority for which files a Run invokes.

## 🖥 Surface · overview first, detail on demand

```text
⚙️ Runs
├── RUN OVERVIEW
│   ├── Execution                 computation · data · models
│   ├── Discovery                 search · papers · external evidence
│   ├── Page
│       ├── Evidence Item          one focal ready VALUE/CITE/DISPLAY Result
│       ├── Division Writing
│       └── Display
│   └── Labeling
│       ├── P0 Contract operations
│       ├── P1 Round operations grouped by round_<t>
│       ├── P2 Handoff operation
│       ├── P3 Test operations
│       ├── P4 Scan operations
│       └── P5 Audit operations
└── SCRIPTS                          collapsible · freestyle · read-only
```

### Run overview

Show one compact table, with `All · Execution · Discovery · Page · Labeling` as
filters rather than competing ledgers. One row is one logical Run; its
Result is the returned half of that same row, never a separate Results section.

```text
Run   Kind                       Target       Status       Result
r01   Execution                  Model fit    ✅ Done      4 files
r02   Discovery                  Smith 2025   🔄 Running   —
r03   Page · Evidence Item        E01-VALUE…   ✅ Done      ready value
r04   Page · Division Writing     C02          ⏸ Held      candidate
r05   Page · Display              C02.F01      ✅ Done      preview
r06   Labeling · Human Calibration round_03    ⏸ Held      human gate
r07   Labeling · Scan Shard       shard_01     ✅ Done      1 pointer
```

Keep the overview vocabulary to `Ready · Running · Done · Failed · Held`.
Derive it from the ticket and the owning Run contract's receipt/Result; do not
mint another hand-maintained status file. Put active or recovery-needed rows
first, then newer rows. Large and raw outputs remain counts or safe labels.

Reader-facing labels are always `Run` and `Result`. Legacy implementation
fields may still be named ticket/receipt internally, but the presenter must not
surface those words as alternative object names. Show literal repository-
relative Run and Result paths and allow them to wrap on narrow screens.

Clicking a row opens that Run's detail: summary, authored Run, paired Result,
log or error, and selectable text for any script/config/notebook paths the Run
actually uses. Do not link directly to raw Run or Result files; the Runs
surface must not trigger downloads. Do not put commands, logs, actor metadata, or full output trees
in the overview.

For Page · Evidence Item rows, the overview shows the actual local Run,
paired Result, status, and any explicitly bound Evidence Item ids. The
detail shows the safe target and exact local paths. Supporting Run ids, frozen
input envelopes and unallocated plans remain in Evidence Items. Historical
PageX rows are migration input, never extra Runs or Results. Never
expand Supporting Runs into extra local rows or present the Result as a
separate Run.

For Labeling rows, show safe identities, checksums, gate summaries, and counts
only. Never render sealed ids, protected text, raw judgments, or a second
approve/freeze/reveal/final/run control. A row may deep-link to the same Run in
the Labeling workbench; only the subjective-label workflow may operate it.
Use the operation name as the row Kind and the P0-P5 episode only as a grouping
label. Never add a second row for the Round, Test, Scan, or Audit episode.

Surface an orphan or logical address mismatch as an error. A missing Result is
normal for `Ready` or `Running`; it is a finding only when the Run claims
`Done`. A generated Result is not Page evidence merely because it exists; an
evidence lane must bind or aggregate it.

### Scripts region

Show `Scripts ▸ <N> files` below the overview and keep it collapsed by default.
When opened, present the files as a read-only tree. Do not classify them by Run,
require a manifest, or mark an unreferenced file as an error. A Run detail may
link the exact paths its ticket calls; the Scripts region itself interprets
nothing.

## 🧩 The four plugin things

```text
STORAGE   none of its own; resolve authored/generated Run projections
SURFACE   ⚙️ Runs: one family-filtered overview table plus a collapsible
          freestyle Scripts tree; click one Run for its Run + Result detail
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
- **No scripts requirement.** Only a Run ticket may invoke scripts when they
  exist; their absence does not invalidate a Run, and unused supporting files
  do not invalidate Scripts.

## 🗺 Status · 🟢 live 260904

`live/runs.py` and `85-plugin-runs.js` serve the read-only Board Page view.
The surface resolves both Folder-local and canonical Job-backed Task pairs;
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
