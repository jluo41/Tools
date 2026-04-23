---
name: dikw-plan
description: "DIKW analysis plan skill. Design a structured DIKW analysis plan based on exploration findings. Use when the user asks to create a plan, design analysis tasks, write a DIKW plan, or says /dikw-plan. Trigger: plan, analysis plan, design tasks, task plan, DIKW plan."
---

Skill: dikw-plan
==================

Runs during **`step=task`** of **`phase=plan`** (the single task of that
phase). Designs the initial plan, or — when re-entering `phase=plan` via a
`revise plan` gate outcome — rewrites the plan using all accumulated
insights + gate feedback.

On invocation, `$ARGUMENTS` = `{snapshot_dir} [revision_feedback]`.

Two modes, determined by the presence of prior plan versions and the
`plan_version` in DIKW_STATE.json:

| Mode | Trigger | Inputs | Output |
|------|---------|--------|--------|
| **initial** (v1) | no prior `plan-raw-v*.yaml` | snapshot `exploration/explore_notes.md` + question | `plan-raw-v1.yaml` |
| **revision** (v2+) | triggered by gate `revise plan "<feedback>"` | full context from `/dikw-context plan` (explore + ALL reports + full gate history + triggering feedback) + previous `plan-raw-v{N-1}.yaml` | `plan-raw-v{N}.yaml` |

After writing, update the convenience symlink:
`plan/plan-raw.yaml → plan-raw-v{N}.yaml`.

Note: `snapshot_dir` is a `_agent_dikw_space/snapshot-<date>/` folder.

---

Steps
-----

1. Load context:
   - snapshot_dir = first whitespace-separated token; revision_feedback =
     remainder of `$ARGUMENTS` (may be empty, may be a single
     double-quoted string — strip surrounding quotes if present).
     Orchestrator call shape: `/dikw-plan {snapshot_dir} "<feedback>"`.
   - Determine mode:
     - If `sessions/{aim}/plan/plan-raw-v*.yaml` exists → **revision** mode
     - Else → **initial** mode
   - In **revision** mode, invoke `/dikw-context plan {snapshot_dir}` first
     and read the full package (explore + all reports + gate history +
     triggering feedback). Also read the latest prior `plan-raw-v{N-1}.yaml`.
   - In **initial** mode, read only `{snapshot_dir}/exploration/explore_notes.md`
     (snapshot-level, not session-level). If missing, ask the user to run
     `/dikw` (which will run `/dikw-explore` at Stage 4.5).

2. Design the analysis plan:
   - Based on what the data actually contains (initial)
   - In revision mode, carry forward tasks that are still valid, modify
     those affected by the feedback, add new ones to close the gap.
     Preserve task `name`s where semantics are unchanged (so cached
     `insights/*/` folders stay usable).
   - 2 to `MAX_TASKS_PER_LEVEL` tasks per DIKW level (D, I, K, W); target
     2–3 by default, never exceed `MAX_TASKS_PER_LEVEL` (see
     `dikw-session/SKILL.md § Constants`; default 4)
   - Each task: `name` (short_lowercase) + `description` (specific to this
     data and complete enough to stand alone at Gate G-plan).

3. Write the plan:
   - New plan version N = (max existing v{k}) + 1, or 1 if none.
   - Output path: `{snapshot_dir}/sessions/{aim}/plan/plan-raw-v{N}.yaml`
   - Update symlink: `{snapshot_dir}/sessions/{aim}/plan/plan-raw.yaml` → `plan-raw-v{N}.yaml`
   - In revision mode, include a top-level `revision:` block recording:
     ```yaml
     revision:
       from_version: {N-1}
       triggered_by_gate: "G-D"
       feedback: "<feedback text>"
       changes:
         - kept:     [<task names unchanged>]
         - modified: [<task names with updated descriptions>]
         - added:    [<new task names>]
         - removed:  [<task names dropped from prior plan>]
     ```

Required YAML format:

```yaml
goal: <one sentence describing the analysis goal>
D:
  - name: understand_columns
    description: Understand all columns — types, meaning, characteristics
  - name: quality_assessment
    description: Assess data quality — nulls, duplicates, anomalies
I:
  - name: statistical_summary
    description: Distributions, central tendencies, variability measures
  - name: correlation_analysis
    description: Identify relationships between variables
K:
  - name: rule_extraction
    description: Extract rules, principles, causal relationships
W:
  - name: strategic_recommendations
    description: Prioritized recommendations based on findings
```

Task names are the CANONICAL key — they appear in:
  - plan-raw.yaml (no `{L}{NN}-` prefix)
  - DIKW_STATE.json (no `{L}{NN}-` prefix)
  - Folder name on disk: `insights/{level}/{L}{NN}-{name}/ where L=D/I/K/W per level` (prefixed at execution time)

---

Rules
-----

- Tasks per level: between 2 and `MAX_TASKS_PER_LEVEL` (defined by
  `/dikw-session`, default 4). Default target 2–3.
- **Persona-aware task richness.** Read `DIKW_STATE.gate_persona` if it
  exists. When `ambition >= 7` (`creative` preset), bias task descriptions
  toward richer, more synthetic outputs (named hypotheses, patient-level
  inferences, cross-stream linkage). When `ambition <= 3` (`lenient`),
  keep task specs minimal and contract-shaped. `balanced`/`strict` map to
  current default richness.
- Task names: short lowercase with underscores (e.g., col_overview)
- NO session prefix in task names — they are snapshot-scoped, reusable
- NO `{L}{NN}-` prefix in plan-raw.yaml — that is added when the insight folder is
  created at execution time, based on the order tasks run within the level
- Base the plan on what explore_notes.md actually found, not generic templates
- Each task description MUST be specific to THIS dataset and MUST be complete
  enough to stand on its own in the `G-plan` approval view (the `description`
  field is what gets rendered to the human — a terse or vague description
  makes the gate unreviewable). Prefer multi-sentence descriptions that state
  inputs, method, and expected artifact.

---

Downstream presentation contract
--------------------------------

`/dikw-session` renders `plan-raw.yaml` at `G-plan` as **one markdown table per
DIKW level** with columns `#` / `Task` / `Description`, showing the full
`description` text for every task. The human uses that to approve, revise,
remove, or add.

Write descriptions with that renderer in mind:
  - Each description should read as a self-contained specification.
  - If a description is shorter than ~15 words, expand it to state what the
    task actually does (inputs, transformation, artifact).
  - Avoid rewording the task `name` — descriptions must add substance beyond
    the name.
