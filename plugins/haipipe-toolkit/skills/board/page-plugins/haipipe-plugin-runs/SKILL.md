---
name: haipipe-plugin-runs
description: >-
  The optional Runs presenter of a Folder: one ⚙️ surface over authored Run
  tickets and their paired generated Results. Its default overview table groups
  complete Runs as Execution, Discovery, or Page; Page divides into Division
  Writing and Display. A second, collapsible Scripts region shows freestyle
  implementation files when present. Use for Discovery Paper Runs, Task Page
  runs, model/data jobs, run status tables, result details, or any Folder that
  exposes addressable Runs. Presentation only; the owning workflow controls
  Execute and closure. Trigger: Runs plugin, Runs tab, run overview, run status,
  run results, show the runs, /haipipe-plugin-runs.
metadata:
  version: "0.5.0"
  last_updated: "2026-09-01"
  # version history: ./CHANGELOG.md (skill-scoped, never loaded at invocation)
---

# /haipipe-plugin-runs · one surface for addressable Runs

**LOAD `haipipe-plugin` FIRST.** This is a PRESENTER plugin
(`haipipe-plugin` §🔌): it owns no folder and has no roster row. It presents
the Run projections already owned by the Folder or its containing Task Job.

## 🏷 Runs, not Execution

Keep **Execute** as a workflow action. Name this plugin **Runs** because it
presents a collection of durable, addressable attempts. One Run is one logical
identity with an authored ticket and a generated Result:

```text
Run address  = ticket identity = Result identity
```

The Folder kind and workflow decide whether and when to Execute. Runs only
presents what was launched and what came back. A Folder may therefore have a
Task Face without a Runs plugin, and a Runs plugin without reusable local code.

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
```

The two paths are two storage dialects of the same Run contract. Never copy or
symlink job-owned Results into the Task Page merely to make the first shape.
Never treat a Result folder as a fifth hierarchy level.

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
│   └── Page
│       ├── Division Writing
│       └── Display
└── SCRIPTS                          collapsible · freestyle · read-only
```

### Run overview

Show one compact table, with `All · Execution · Discovery · Page` as
filters rather than four competing ledgers. One row is one complete Run; its
Result is the returned half of that same row, never a separate Results section.

```text
Run   Kind                       Target       Status       Result
r01   Execution                  Model fit    ✅ Done      4 files
r02   Discovery                  Smith 2025   🔄 Running   —
r03   Page · Division Writing     C02          ⏸ Held      candidate
r04   Page · Display              C02.F01      ✅ Done      preview
```

Keep the overview vocabulary to `Ready · Running · Done · Failed · Held`.
Derive it from the ticket and the owning Run contract's receipt/Result; do not
mint another hand-maintained status file. Put active or recovery-needed rows
first, then newer rows. Large and raw outputs remain counts or safe labels.

Clicking a row opens that Run's detail: summary, authored ticket, paired Result,
receipt/log or error, and links to any script/config/notebook paths the ticket
actually uses. Do not put commands, logs, actor metadata, or full output trees
in the overview.

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
          freestyle Scripts tree; click one Run for its Ticket + Result detail
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

## 🗺 Status · 🟡 contract 260901 · tab pending

The contract covers both Discovery Paper Runs and canonical Task Page Runs. A
live `runs.py` drawer and registry row remain pending; until then the 📂 Folder
tab is the filesystem surface.

## 📂 Files

- `../../haipipe-plugin/ref/roster.md` · lane and presenter roster
- `../../../task/haipipe-task/ref/hierarchy.md` · Task Run address/dialect
- `../../../discovery/haipipe-discovery/ref/paper-run-contract.md` ·
  Discovery Folder-local dialect
