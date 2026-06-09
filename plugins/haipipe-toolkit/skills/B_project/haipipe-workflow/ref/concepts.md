IPO — the shape of every workflow
=================================

Every workflow in haipipe-toolkit has exactly one shape:

```
I  →  P₁[S₁,S₂,...] → P₂[S₁,S₂,...] → ... → Pₙ[...]  →  O
```

Four letters, four concerns:

| Letter | Name    | What it holds |
|--------|---------|---------------|
| **I**  | Input   | What goes in — specs, configs, flags, files |
| **P**  | Phase   | A coarse-grained chunk of work |
| **S**  | Step    | An atomic action inside a phase (may be optional) |
| **O**  | Output  | What comes out — results, artifacts, verdicts |


Why these names
---------------

**Phase, not Process.**
Process = the entire middle of IPO (everything between Input and Output).
Phase = one chunk within the process. The Workflow tool already uses
`phase()` — we match it.

**Step, not Stage.**
Stage = the 6-stage data pipeline (0-RawDataStore through 6-EndpointStore).
Reusing "stage" inside workflows would be ambiguous. Step = the smallest
unit of work, an `agent()` call.


Lifecycle: Plan → Build → Execute → Report
=============================================

Every workflow goes through four acts:

```
┌──────────┐    ┌──────────┐    ┌──────────┐    ┌──────────┐
│   PLAN   │──▶ │  BUILD   │──▶ │ EXECUTE  │──▶ │  REPORT  │
│          │    │          │    │          │    │          │
│ design   │    │ generate │    │ run the  │    │ what     │
│ the IPO  │    │ .js from │    │ script   │    │ actually │
│ (iterate │    │ plan     │    │          │    │ happened │
│  rounds) │    │          │    │          │    │          │
└──────────┘    └──────────┘    └──────────┘    └──────────┘
    ↑  ↓                                             │
    └──┘ rounds                                      ▼
                                              structured record
```

| Act | Question | Input | Output |
|-----|----------|-------|--------|
| **Plan** | What will we do? | Purpose + constraints | `plan.yaml` (frozen IPO) |
| **Build** | How to execute it? | Frozen plan | `.workflow.js` (executable script) |
| **Execute** | Do it. | `.workflow.js` + args | Raw results per step |
| **Report** | What happened? | Plan + execution results | `report.yaml` (structured record) |

```
plan.yaml ──▶ .workflow.js ──▶ results ──▶ report.yaml
 (human)       (machine)       (raw)       (structured)
```

### Plan (iterate until frozen)

The Plan act designs the IPO. It may take several rounds:

```
round 1: draft phases and steps
round 2: refine — "wait, need an extra step for config validation"
round 3: ready ✓ — freeze the plan
```

The frozen plan is the contract. Build translates it. Execute runs it.
Report echoes it.

### Build (plan → script)

Generate a `.workflow.js` from the frozen plan. The `.js` is the
machine-executable form — it maps plan phases to `phase()` calls,
plan steps to `agent()` calls, plan schemas to JSON Schema constants.

You read and edit the `plan.yaml`. The `.workflow.js` is generated.
You should rarely edit the `.js` directly.

### Execute (run the script)

Run the `.workflow.js` via the Workflow engine:
`Workflow({ scriptPath: "..." }, args)`.

Each Step calls a subagent (or a sub-workflow skill). The execute act
follows the frozen plan — if something unexpected arises, it records
the deviation, it doesn't re-plan.

For manual mode (CMS server, GPU jobs), the `plan.yaml` serves as the
checklist. The human follows the phases/steps and records results.

### Report (the plan's echo)

The Report mirrors the Plan structure — same Phases, same Steps —
but filled with what actually happened:

```
PLAN says:                          REPORT says:
  P1.S1: write <TASK>.py             P1.S1: ✅ done, created build_lbp.py (45 lines)
  P1.S2: fill config (optional)      P1.S2: ✅ done, filled 3 fields
  P2.S1: syntax check                P2.S1: ✅ pass
  P2.S2: dry-run (optional)          P2.S2: ⏭️ skipped (no test data)
```

The Report contains:
- Per-step status (done / skipped / failed)
- Per-step actual files read and created
- Per-step output values
- Issues or deviations
- Overall summary


Template vs Specific
=====================

The skill (haipipe-workflow) defines the **template** — the abstract
shape. When you instantiate a real workflow, everything becomes
**specific**.

```
TEMPLATE (in the skill):              SPECIFIC (a real instance):
──────────────────────                ─────────────────────────
  Phase: "Author"                      Phase: "Author"
  Step: "write script"                 Step: "write build_lbp.py"
  files_in: [template file]            files_in: [ref/source_fn_template.py]
  files_out: [<TASK>.py]               files_out: [tasks/A01_lbp/build_lbp.py]
  prompt: "Create {{type}} script"     prompt: "Create data pipeline for LBP cohort"
```

The skill owns the template. Each specific workflow fills in the
blanks with concrete file paths, concrete field values, concrete
prompts. The Plan act is where template → specific happens.


File tracking
==============

Every Step declares which files it reads and which files it produces.
Files are the tangible artifacts that flow through the pipeline.

### In the Plan (what we expect)

```yaml
steps:
  - label: "write build_lbp.py"
    files_in:
      - ref/source_fn_template.py          # template to read
      - configs/run_lbp.yaml               # config to reference
    files_out:
      - tasks/A01_lbp/build_lbp.py         # script to create
```

### In the Report (what actually happened)

```yaml
steps:
  - label: "write build_lbp.py"
    status: done
    files_in:
      - ref/source_fn_template.py          # ✅ read (42 lines)
    files_out:
      - tasks/A01_lbp/build_lbp.py         # ✅ created (45 lines)
    note: "used alt template — original missing RecordFn section"
```

### Why track files?

1. **Auditability** — you can see exactly what each step read and produced
2. **Dependency** — P2.S1 reads a file that P1.S2 created → implicit ordering
3. **Completeness** — Report can check: were all planned files_out actually created?
4. **Debugging** — if a step fails, you know which input file was wrong


The hierarchy (full picture)
=============================

```
Workflow
├── I (Input)
│   ├── schema: what fields? what types?
│   ├── files_in: input files the workflow starts with
│   └── example: a concrete args value
│
├── P (Phases) — ordered sequence
│   ├── P1: "Author"
│   │   ├── S1: "write script"                    (required)
│   │   │   ├── files_in:  [template.py, config.yaml]
│   │   │   └── files_out: [build_lbp.py]
│   │   ├── S2: "fill config"                     (optional)
│   │   │   ├── files_in:  [config_template.yaml]
│   │   │   └── files_out: [configs/run_lbp.yaml]
│   │   └── fan: serial
│   │
│   ├── P2: "Validate"
│   │   ├── S1: "syntax check"                    (required)
│   │   │   ├── files_in:  [build_lbp.py]         ← reads P1.S1 output
│   │   │   └── files_out: []                      ← produces no files
│   │   └── S2: "dry-run"                         (optional)
│   │       ├── files_in:  [build_lbp.py, test_data/]
│   │       └── files_out: [results/dry_run.log]
│   │
│   └── P3: "Review"
│       └── S1: "QA gate"
│           ├── files_in:  [build_lbp.py, configs/run_lbp.yaml]
│           └── files_out: [CODE_REVIEW.md]
│
└── O (Output)
    ├── schema: what the workflow returns
    ├── files_out: all files the workflow produced (collected from steps)
    └── example: a concrete return value
```


Step types
===========

A Step can be one of three things:

| Type | What it does | Caller sees |
|------|-------------|-------------|
| **agent** | Atomic action (read, write, compute) | Step result |
| **skill** | Calls another haipipe skill (sub-workflow) | Only I/O — internal P/S hidden |
| **workflow** | Calls a .workflow.js script | Only I/O — internal P/S hidden |

When a Step calls a sub-workflow (type = skill or workflow):

```
caller's Plan says:                 callee internally:
  S1: scaffold arm-A                  has its OWN Plan → Execute → Report
    calls: haipipe-task               has its OWN Phases and Steps
    sub_I: { type: data, name: ... }  has its OWN file tracking
    sub_O: { status, folder, files }
    files_in: [arm spec]              caller doesn't see callee's files_in
    files_out: [task folder]          caller sees callee's final files_out via sub_O

caller's Report says:
  S1: ✅ done
    sub_report_summary: "task created 3 files, syntax clean"
    files_out: [tasks/A01_.../]       ← surfaced from sub_O
```


Boundary rule
==============

Three things cross the wall between caller and callee:

```
CALLER                              CALLEE
──────                              ──────
declares sub_I  ──── I ────▶  receives I
                                has own Plan → Execute → Report
                                has own P[S], own files_in/files_out
expects  sub_O  ◀─── O ────  returns O
sees summary    ◀── report ──  returns report summary (one line)

NOT visible: callee's internal Phases, Steps, or file details
```

The rule: **own your Phases, hide your Phases from your caller.**


Naming cheat sheet
===================

| Scope | Convention | Example |
|-------|-----------|---------|
| Workflow name | kebab-case | `haipipe-task-batch` |
| Phase title | PascalCase, short | `Author`, `Gate1`, `Run` |
| Step label | `phase:item` | `author:training`, `gate1:eval` |
| Schema constant | CAPS_SNAKE | `AUTHORED`, `VERDICT`, `RUN` |
| Plan file | `plan.yaml` | `ref/plan.yaml` |
| Script file | `<name>.workflow.js` | `ref/batch-pipeline.workflow.js` |
| Report file | `report.yaml` or `report.md` | `results/report.yaml` |
| files_in | relative to project root | `ref/source_fn_template.py` |
| files_out | relative to project root | `tasks/A01_.../build_lbp.py` |
