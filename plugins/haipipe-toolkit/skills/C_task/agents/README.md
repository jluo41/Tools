C_task — Agent Roster
=====================

Two families, separated by folder. The split is the whole point:

```
creators/   🔨 BUILDER family — per task TYPE — the axis that GROWS
reviewers/  🔍 REVIEWER family — type-AGNOSTIC — FIXED at 2, gate every type
```

Folder = family. Knowledge lives in `../haipipe-task/ref/authoring-conventions.md`
(shared) + each `haipipe-task-for-<type>/ref/` (type-specific) — NOT in the
agents. Agents are thin.

The C_task lifecycle
--------------------

```
                  knowledge: ref/authoring-conventions.md (shared, both read it)
                          │
human ─┐                  ▼
       ├─▶ haipipe-task-for-<type> skill ──(params complete→silent / missing→ASK)
agent ─┘        (scaffolds the 4 sister files; returns task-folder path)
                          │
   ▼ BUILD               │ creators/ call the skill headless, then author
   code-creator-for-<type>-agent   writes <TASK>.py body + config params
                          │
   ▼ 🚦 GATE 1 (pre-run) │ reviewers/ — type-agnostic
   run-script-reviewer-agent       intent ↔ impl audit  → CODE_REVIEW.md
                          │
   ▼ EXECUTE             bash runs/<RUN>.sh → runtime.yaml + metrics.json
   ▼ 🚦 GATE 2 (post-run)
   run-result-auditor-agent        per-run trustworthiness → RUN_AUDIT.md
                          │
                          ▼  (run is now linkable as a D_probe arm)
```

creators/ (grows — one per type)
--------------------------------

| Agent | Calls skill | Sole deliverable | Status |
|-------|-------------|------------------|--------|
| `code-creator-for-training-agent`   | `haipipe-task-for-training`   | training `<TASK>.py` + config   | built |
| `code-creator-for-data-agent`       | `haipipe-task-for-data`       | data `<TASK>.py` + config       | built |
| `code-creator-for-eval-agent`       | `haipipe-task-for-eval`       | eval `<TASK>.py` + config       | built |
| `code-creator-for-display-agent`    | `haipipe-task-for-display`    | figure/table `<TASK>.py`        | built |
| `code-creator-for-individual-agent` | `haipipe-task-for-individual` | per-patient query `<TASK>.py`   | built |
| `code-creator-for-algo-agent`       | `haipipe-task-for-algo`       | algo-demo `<TASK>.py`           | built |
| `code-creator-for-agent-agent`      | `haipipe-task-for-agent`      | LLM agent-call `<TASK>.py`      | built |
| `code-creator-for-stata-agent`      | `haipipe-task-for-stata`†     | dispatcher `<TASK>.do` + `scripts/` workers | built |

† The Stata creator is the one that fronts a 4-stage family: it calls the
**parent** `haipipe-task-for-stata`, which disambiguates the stage
(cms/case/data/reg) and routes to the right `haipipe-task-for-stata-<stage>`
child. Engine = Stata + PowerShell + logs (NOT papermill); deliverable is a
multi-file `.do` job, not a single `.py`.

Each is THIN: call the type skill (headless) → author the body → return.
Type-expertise stays in the skill + ref. Adding a type = copy `_TEMPLATE.md`,
point it at `haipipe-task-for-<newtype>`, add a top-level symlink.
Until a type has a creator, its skill is the (interactive) author fallback.

reviewers/ (fixed at 2 — never split by type)
---------------------------------------------

| Agent | Gate | Sole deliverable | Does NOT do (→ who) |
|-------|------|------------------|---------------------|
| `run-script-reviewer-agent` | GATE 1 pre-run  | `CODE_REVIEW.md` | post-run audit (→auditor); fraud (→D_probe integrity) |
| `run-result-auditor-agent`  | GATE 2 post-run | `RUN_AUDIT.md`   | cross-run compare (→D_probe structural); claim (→D_probe claim) |

These gate ALL creators, current and future. Adding a task type adds **zero**
reviewer cost — that is why the families are split.

builder ≠ judge
---------------

A creator authors and stops; a different agent (the reviewer, with a Codex
second opinion) judges it. The writer rationalizes its own bugs; an
independent context does not. Never let a creator review its own output.

Registration & invocation
--------------------------

Real files live here (`creators/`, `reviewers/`). The plugin's top-level
`agents/` holds **flat symlinks** to each — that flat folder is the only
place the harness scans, so the symlinks are what make every agent callable
as a `subagent_type` (needed for fan-out: `agent_type:"code-creator-for-training-agent"`).
Nested subfolders here are for humans; the top-level symlinks are for the harness.

Automation (fan-out, one session, many task-groups)
---------------------------------------------------

```
orchestrator (thin entry skill): parse N specs, each typed
  for spec in specs:                                            # concurrent
      Agent(agent_type=f"code-creator-for-{spec.type}-agent", prompt=spec)
        → run-script-reviewer-agent (GATE 1)
        → bash run.sh
        → run-result-auditor-agent (GATE 2)
  collect N results → human review
```

creators chosen by type; the 2 reviewers shared across all. For deterministic
batch, drive this with the Workflow `pipeline()`.
