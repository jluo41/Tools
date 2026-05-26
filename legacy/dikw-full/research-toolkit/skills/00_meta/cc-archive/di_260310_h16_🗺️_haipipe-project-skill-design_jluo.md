Session 1: haipipe-project Skill Design (2026-03-10 16:00)
===========================================================

Location: Tools/plugins/research/skills/haipipe-project/
Status: 🗺️ Design decided, ready to implement

Overview
--------

Designed the `haipipe-project` skill for standardizing new project creation
in `examples/`. Covered: current state analysis, standard folder structure,
results/ boundary, and skill file plan.

**Two development tracks (always distinguish):**
- Track A: code/code-dev (new pipeline functions, new data topics)
- Track B: examples/ (project-level experiments, uses the library)

This skill covers Track B.


Issue 1: Current examples/ are structurally inconsistent
---------------------------------------------------------

**Severity**: [HIGH]
**Location**: `examples/`
**Problem**: Each project invented its own layout. No shared conventions.

| Project | Structure | Missing |
|---------|-----------|---------|
| ProjB-Bench-0-Record | config/ only | scripts, CLAUDE.md |
| ProjD-EHR-Mimic | config/ + cc-archive/ | workspace, scripts |
| ProjB-Bench-1-FairGlucose | workspace/{config,script,notebook} | CLAUDE.md |
| ProjC-Model-1-ScalingLaw | scripts/ + sbatch/ + 2-haipipe-nn/ | CLAUDE.md |

**Decision**: Define a standard four-part layout and encode it in the skill.


Issue 2: Standard project folder structure
------------------------------------------

**Severity**: [DESIGN DECISION]
**Location**: `examples/{project-id}/`

Agreed standard:

```
examples/Proj{Series}-{Category}-{Num}-{Name}/
├── cc-archive/        <- CC session exports (cc_*.md, di_*.md)
├── config/            <- YAML pipeline configs
│   ├── 1_source_*.yaml
│   ├── 2_record_*.yaml
│   └── ...
├── scripts/           <- Python + shell scripts
│   ├── 001_260310_train_baseline.py
│   └── 002_260310_eval_results.sh
└── results/           <- light summaries only (in git)
    ├── 001_260310_train_baseline/
    │   ├── report.md
    │   └── metrics.json
    └── 002_260310_eval_results/
```

**Naming convention**: `Proj{Series}-{Category}-{Num}-{Name}`
- Series: A-Z (research area)
- Category: EHR, Bench, Model, etc.
- Num: sequential integer
- Name: CamelCase descriptor

**Correction (260310)**: "CC file" = `cc-archive/` directory (not CLAUDE.md).
Stores CC session summaries (`cc_*.md`) and discussion logs (`di_*.md`).


Issue 3: results/ boundary design
----------------------------------

**Severity**: [DESIGN DECISION]
**Location**: `examples/{project-id}/results/`

**Decision** (user-proposed, agreed):

```
_WorkSpace/5-ModelInstanceStore/    <- heavy: weights, full metrics (not git)
examples/ProjX/results/             <- light: report.md, metrics.json (git)
```

**Script-result naming** is the key linking scripts to results:
- `scripts/001_260310_train_baseline.py` ↔ `results/001_260310_train_baseline/`
- Format: `{seq}_{YYMMDD}_{description}` — seq for order, date for when written


Issue 4: CC file vs config file relationship
---------------------------------------------

**Severity**: [DESIGN DECISION]

- **CC file** = `cc-archive/` directory → stores CC session summaries + discussion logs
- **Config file** = YAML files in `config/` → pipeline configuration
- They "互相配合": cc-archive records why configs were designed the way they are

cc-archive/ per project contains:
- `cc_*.md` — CC session exports (from /cc-session-summary skill)
- `di_*.md` — Discussion/design logs (from /coding-by-logging skill)


Issue 5: Skill file plan
------------------------

**Severity**: [DESIGN DECISION]
**Location**: `Tools/plugins/research/skills/haipipe-project/`

Agreed file structure:

```
SKILL.md                  <- entry point, commands + dispatch table
fn/
  fn-new.md               <- scaffold new project (interactive)
  fn-review.md            <- check existing project vs standard
ref/
  project-structure.md    <- ground truth for standard structure
```

Commands:
```
/haipipe-project new               -> interactive project scaffold
/haipipe-project review [path]     -> gap analysis vs standard
```

`fn-new.md` flow:
1. Collect: project ID, description, stages, data sources
2. Create: cc-archive/ + config/ + scripts/ + results/
3. Generate: config YAML skeletons based on selected stages

`fn-review.md` checks:
- cc-archive/ present
- config/ has YAML files
- scripts/ and results/ {seq}_{YYMMDD}_{desc} alignment
- results/ has no heavy files (weights, full checkpoints)

`ref/project-structure.md` encodes:
1. Naming convention: `Proj{Series}-{Category}-{Num}-{Name}`
2. Standard four-part layout: cc-archive/ + config/ + scripts/ + results/
3. Script-result naming: `{seq}_{YYMMDD}_{description}`
4. results/ boundary (light/heavy split)
5. Track A vs Track B distinction


Issue 6: scripts/ scope and naming
------------------------------------

**Severity**: [DESIGN DECISION]

**Scope**: All executable scripts go in `scripts/` — not Python-only.
- `.py` — main logic
- `.sh` / `.bash` — env setup, batch submission (e.g., SLURM sbatch)
- If shell scripts are heavy, can use `scripts/sbatch/` subdirectory
- Rule: script triggers execution; output goes to `results/` or `_WorkSpace/`

**Naming**: `{seq}_{YYMMDD}_{description}.{ext}` (Option B, confirmed)
- `001_260310_train_baseline.py`
- `002_260310_eval_results.sh`
- `seq` = logical execution order (3 digits, zero-padded)
- `YYMMDD` = date written
- Results folder mirrors the script name exactly


Unsolved Items
--------------

| # | Issue | Status | Notes |
|---|-------|--------|-------|
| 1 | _WorkSpace path declaration location | RESOLVED | See Session 2 |
| 2 | Actual skill file creation | TODO | Ready to proceed |


Session 2: Final Structure + Skill Scope Expansion (2026-03-10 16:30)
======================================================================

Location: Tools/plugins/research/skills/haipipe-project/
Status: 🗺️ Scope expanded — skill covers both example/ and code/

Overview
--------

Two additions from discussion:
1. Finalized the complete example/ folder structure
2. Expanded skill scope: haipipe-project covers Track A (code dev) AND Track B (example)

Also resolved: _WorkSpace path declaration location.


Issue 7: _WorkSpace path declaration — RESOLVED
-------------------------------------------------

**Severity**: [RESOLVED]

`_WorkSpace` paths are declared in `env.sh` as environment variables.
`setup_workspace()` in `code/haipipe/base.py` reads them at runtime:

```python
local_source_store      = os.environ['LOCAL_SOURCE_STORE']
local_record_store      = os.environ['LOCAL_RECORD_STORE']
local_case_store        = os.environ['LOCAL_CASE_STORE']
local_aidata_store      = os.environ['LOCAL_AIDATA_STORE']
local_modelinstance_store = os.environ['LOCAL_MODELINSTANCE_STORE']
...
```

**Conclusion**: No project-level path declaration needed. Paths come from
`env.sh` → `setup_workspace()`. Scripts call `setup_workspace()` at the top
and get the SPACE dict back with all resolved paths.


Issue 8: Final example/ folder structure
-----------------------------------------

**Severity**: [DESIGN DECISION]

```
examples/Proj{Series}-{Category}-{Num}-{Name}/
├── cc-archive/                      <- CC session history
│   ├── cc_YYMMDD_h{HH}_*.md        <- session exports (/cc-session-summary)
│   └── di_YYMMDD_h{HH}_*.md        <- discussion logs (/coding-by-logging)
│
├── config/                          <- YAML pipeline configs
│   ├── 1_source_{dataset}.yaml      <- Stage 1 (if used)
│   ├── 2_record_{dataset}.yaml      <- Stage 2 (if used)
│   ├── 3_case_{dataset}.yaml        <- Stage 3 (if used)
│   ├── 4_aidata_{dataset}.yaml      <- Stage 4 (if used)
│   └── 5_model_{name}.yaml          <- Stage 5 (if used)
│
├── scripts/                         <- All executable scripts (py + sh)
│   ├── 001_{YYMMDD}_{desc}.py
│   ├── 002_{YYMMDD}_{desc}.sh       <- shell/sbatch also allowed
│   └── sbatch/                      <- optional subfolder for SLURM scripts
│
└── results/                         <- Light summaries only (in git)
    ├── 001_{YYMMDD}_{desc}/         <- mirrors script name exactly
    │   ├── report.md
    │   └── metrics.json
    └── 002_{YYMMDD}_{desc}/
```

**Rules:**
- `cc-archive/` — all Claude Code session context lives here
- `config/` — only YAML, named by stage number + dataset/model name
- `scripts/` — all executables; naming: `{seq}_{YYMMDD}_{desc}.{ext}`
- `results/` — light only; name mirrors script; heavy → `_WorkSpace/`
- `_WorkSpace/` paths come from `env.sh` via `setup_workspace()`, not declared here


Issue 9: haipipe-project skill scope — expanded to both tracks
---------------------------------------------------------------

**Severity**: [DESIGN DECISION]

The skill covers TWO tracks simultaneously. A real project touches both.

**Track A — code/ development** (library side)
```
code-dev/1-PIPELINE/
├── 1-Source-WorkSpace/    <- new SourceFn for dataset
├── 2-Record-WorkSpace/    <- new RecordFn
├── 3-Case-WorkSpace/      <- new CaseFn / TriggerFn
├── 4-AIData-WorkSpace/    <- new InputTfmFn / SplitFn
└── 5-Instance-WorkSpace/  <- new Algorithm / Tuner / Instance

code/hainn/
├── algo/                  <- new Algorithm class
├── tuner/                 <- new Tuner config
└── instance/              <- new Instance runner
```
Changes here are built/generated into `code/haifn/`.

**Track B — examples/ development** (experiment side)
```
examples/Proj.../
├── cc-archive/
├── config/
├── scripts/
└── results/
```

**Skill commands (final):**

```
/haipipe-project new              -> scaffold both tracks together (no need to specify)
/haipipe-project review [path]    -> check both sides, propose actions
```

- `new`     → collect metadata, then generate example/ + code/ side automatically
- `review`  → inspect existing example/ folder AND code-dev/hainn/ stubs,
              output gap report + proposed actions

**Key principle**: user doesn't need to think about which track.
The skill handles both sides in one flow.

**fn files needed (final):**
```
fn/fn-new.md        <- scaffold both tracks (example/ + code/)
fn/fn-review.md     <- check both sides, propose actions
```

**ref files needed:**
```
ref/project-structure.md    <- example/ folder standard (Track B)
ref/code-structure.md       <- code-dev/ + hainn/ conventions (Track A)
```

Unsolved Items
--------------

| # | Issue | Status | Notes |
|---|-------|--------|-------|
| 1 | Actual skill file creation | TODO | Design complete, ready to implement |


Session 3: Command Design Simplification (2026-03-10 16:45)
============================================================

Location: Tools/plugins/research/skills/haipipe-project/
Status: ✅ Design finalized

Overview
--------

User clarified the command interface: no need to distinguish Track A vs Track B
when invoking the skill. The two-track split is an internal detail, not user-facing.


Issue 10: Remove track distinction from commands
-------------------------------------------------

**Severity**: [DESIGN CORRECTION]

**Original proposal (wrong):**
```
/haipipe-project new example   -> Track B only
/haipipe-project new code      -> Track A only
/haipipe-project new both      -> both tracks
```

> JL: 在处理一个 new project 的时候，自动生成 example 和 code 就行了；
> JL: 或者检查现有的 example folder 和 code folder，然后 propose 你要做什么。
> JL: 在使用的时候不需要刻意区分。

>> CC: DONE. Simplified to two commands. `new` always handles both tracks
>> CC: automatically. `review` inspects both sides and proposes actions.
>> CC: User never needs to specify which track.

**Final commands:**
```
/haipipe-project new           -> collect metadata, scaffold example/ + code/ together
/haipipe-project review        -> check both sides, output gap report + proposed actions
```

**Key principle**: Track A / Track B is an internal detail inside `fn-new.md`.
The user says `new` and the skill figures out what to create based on setup
questions (which stages? which datasets? new algorithm or existing one?).


Changes Made
------------

- Updated Issue 9 command table to reflect final simplified design
- `fn` files confirmed: `fn-new.md` (both tracks) + `fn-review.md` (both sides)
- Design complete — ready to create actual skill files
