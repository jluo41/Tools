fn-review: Project Gap Analysis
===================================================

Read-only audit of an existing project against the standard structure (../../haipipe-project/ref/project-structure.md). Output is a gap report with severity tags; fixes are applied by /haipipe-project organize.

Severity: [BLOCK] [ERROR] [WARN] [NOTE]

Steps: 0 identify project → 1 naming + top-level → 2 project diagram →
3 per-group + per-task → 4 task diagram → 5 code sync → 6 paper diagram
(if applicable) → 7 output report.

The doc surface is diagram/, never README.md. Any README.md found is flagged [WARN] with `--fix migrate-to-diagram` suggestion.


Step 0 — Identify project
==========================
Auto-detect or ask. Confirm PROJECT_PATH and PROJECT_ID.


Step 1 — Naming + top-level structure
======================================
- PROJECT_ID matches Proj{Series}-{Category}-{Num}-{Name}
  ([BLOCK] on pattern mismatch; [WARN] for minor issues)
- Mandatory: tasks/, diagram/  ([BLOCK] if missing)
- Optional: paper/  ([NOTE] if missing)
- Forbidden at top level (each [WARN], suggest organize):
  README.md, docs/, cc-archive/, _old/, configs/, results/


Step 2 — Project diagram/
==========================
Required .txt: 01-story, 02-boundary, 03-exploration  ([ERROR] if missing/empty)
Required canvas: project.excalidraw  ([ERROR] if missing)
Freshness: canvas mtime >= max .txt mtime  ([WARN] if stale)
Scope discipline: project diagram is HIGH-LEVEL only. Flag operational
  content that belongs in {task}/diagram/ (status tables, run metrics,
  daily progress logs) — [WARN] with migration target.


Step 3 — Per-group and per-task review
=======================================

Group ({G}{NN}_{group}/):
- README.md forbidden  ([WARN], suggest migrate-to-diagram)
- Group letter G matches its tasks' series  ([ERROR])
- No flat task folders directly in tasks/  ([WARN])
- sbatch/ should exist with env.sh + cross-task batchers  ([NOTE])
- If cohesive: group/diagram/ has 01-overview, 02-tasks, 03-progress,
  04-design, group.excalidraw  ([WARN] if missing)

Per task ({NN}_{task_name}/):
- >=1 *.py at task root  ([WARN] if missing)
- README.md forbidden  ([WARN])
- configs/ exists with own YAMLs (no symlinks)  ([WARN])
- YAMLs parseable  ([ERROR])
- runs/<run>.sh ↔ results/<run>/ name pairing  ([ERROR] if orphaned)
- runs/*.sh has logging header (Template A) OR papermill flow (Template B);
  same template across the task — don't mix  ([WARN])
- Heavy files in results/ (.pt/.ckpt/.safetensors/.npy/.pkl/.bin/.h5)
  → [ERROR] move to _WorkSpace/
- Track A stub has paired example task  ([WARN] if missing)

Aggregate DECLARED_STAGES from configs/ YAML filenames across tasks.


Step 4 — Per-task diagram/ (only if task has its own; group diagram may cover)
==============================================================================
Required .txt: 01-overview, 02-design, 03-runs, 04-progress  ([ERROR])
Required canvas: task.excalidraw  ([ERROR])
Freshness: canvas mtime >= max .txt mtime  ([WARN] if stale)
Content discipline:
- 01-overview has all four blocks (What/Why/Inputs/Outputs); no "TODO"  ([WARN])
- Stage 5 tasks (ModelArgs in configs/): 02-design has ASCII forward-pass
  diagram + architecture-sweep table  ([WARN])
- 03-runs reflects actual runs/ folder; flag missing/orphaned rows  ([WARN])
- 04-progress has >= 1 real entry beyond the seed  ([NOTE])


Step 5 — Code sync check
==========================
Read code/INDEX.md first.

Stage map: 1 fn_source / SourceFnClass; 2 fn_record / RecordFnClass;
3 fn_case / CaseFnClass; 4 fn_aidata / TfmFnClass; 5 hainn/instance /
ModelInstanceClass; 6 fn_endpoint / EndpointFnClass.

Per FnClass key in configs/ YAMLs (stages 1-4):
- Not "TODO_*"  ([BLOCK])
- Class exists in code/haifn/{layer}/  ([BLOCK])
- Registered in code/INDEX.md  ([WARN])

Stage 5 (5_model_*.yaml):
- ModelInstanceClass in code/hainn/instance/  ([BLOCK])
- model_tuner_name in code/hainn/tuner/  ([BLOCK])
- Required keys: ModelArgs, TrainingArgs, InferenceArgs, EvaluationArgs,
  aidata_name, aidata_version, modelinstance_name  ([ERROR])

Stage 6 (6_endpoint_*.yaml):
- EndpointFnClass in code/haifn/fn_endpoint/  ([BLOCK])
- Required keys: EndpointArgs, modelinstance_name, modelinstance_version  ([ERROR])

Builder sync (stages 1-4, 6):
- code-dev/ build_*.py exists for each declared stage  ([WARN])
- Generated file exists in code/haifn/  ([ERROR] if builder ran but no output)

Imports: scan task .py files for haifn/hainn imports; each imported class
must exist in code/  ([ERROR] if broken).


Step 6 — Paper diagram/ (if paper/ exists)
============================================
Required .txt: 01-overview, 02-figure-plan  ([WARN]). 03-rebuttal [NOTE]
during rebuttal only.
Required canvas: paper.excalidraw  ([WARN]).
Freshness: canvas mtime >= max .txt mtime.
Forbidden in paper/: eval scripts ([ERROR] → tasks/), raw data / model
outputs ([ERROR] → _WorkSpace/), pipeline configs ([ERROR] → tasks/).


Step 7 — Output gap report
============================
Print grouped: Naming, Top-Level, Project Diagram, Per-Group, Per-Task,
Task Diagrams, Code Sync, Paper Diagram.

End with:
- Summary counts (BLOCK/ERROR/WARN/NOTE)
- Proposed actions: prioritized fix list with right `--fix` flag
- "All checks PASSED" if zero issues


MUST NOT
=========
- Modify any file (this skill is read-only).
- Call /diagram-ascii or /diagram-ascii-canvas (authoring belongs to -new / -organize).
- Run pipeline commands.


Next steps
===========
- Structure issues: /haipipe-project organize (with suggested --fix)
- Stale canvases: re-run /diagram-ascii-canvas <path>
- Summary view: /haipipe-project overview
- Summary doc: /haipipe-project summarize
