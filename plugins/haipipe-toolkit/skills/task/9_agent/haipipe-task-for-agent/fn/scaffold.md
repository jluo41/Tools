fn-scaffold: Scaffold an LLM-agent job
=================================================

Call an LLM agent (Claude / GPT) with prompts + tools for an analysis, summarization, or audit task.
Hierarchy prefixes are bNN / jNN / tNN / rNN; domain belongs in the descriptive suffix.

Output: `tasks/bNN_<block>/jNN_<job>/tNN_<task>/`.


Step 1 — Identify project + block
---------------------------------------

- Auto-detect project from cwd.
- AUTO_MODE: infer from cwd or return `status: blocked`. Interactive: resolve the Block and Job; create missing canonical containers through the shared Task owner.


Step 2 — Collect metadata
--------------------------

- Allocate the next unused Task index inside the selected Job and Run index inside that Task; preserve existing indices.
- snake_case task_name: descriptive
  (e.g., `summarize_eval_logs`, `audit_patient_notes`).
- Model: `claude-opus-4-8 | claude-sonnet-5 | claude-haiku-4-5-20251001`.
- Tools (optional): list of tool names available to the agent.
- Inputs: what data context the agent reads.
- `_meta:` block.


Step 3 — Create skeleton
-------------------------

```text
tasks/bNN_<block>/
├── board.md
└── jNN_<job>/
    ├── src/                         shared code + config-defaults.yaml
    └── tNN_<task>/
        ├── tNN_<task>.md
        ├── outline/
        ├── workflow/                plan.yaml + report.yaml
        ├── scripts/<worker>.py
        ├── scripts/config/rNN_<run>.yaml
        └── runs/rNN_<run>.sh

Generated: $OUTPUT_ROOT/tNN_<task>/results/rNN_<run>/
           $OUTPUT_ROOT/tNN_<task>/notebooks/rNN_<run>.ipynb
Task-local prompts/system.md + prompts/user.md hold agent prompts.
```

Note: `prompts/` is unique to agent tasks — keeps prompt content diff-friendly and out of the `.py`.


Step 4 — Seed config + prompts
-------------------------------

Copy `ref/config-seed.yaml` to `scripts/config/rNN_<run>.yaml`.
Fill in:
- `_meta:` block.
- `model:`, `max_tokens:`, `temperature:`.
- `prompts.system:` and `prompts.user:` (paths to prompts/ files).
- `tools:` (optional — list of allowed tool names).
- `inputs:` (placeholder values for the user prompt).

Seed minimal `prompts/system.md` + `prompts/user.md` stubs.


Step 5 — Run-script
--------------------

Copy `../../../haipipe-task/ref/run-sh-template.sh` to `runs/rNN_<run>.sh`.
Set `TASK_NAME="<worker>"` (the worker filename without .py); config and Ticket share the exact `rNN_<run>` stem.


Step 6 — Cross-skill link
--------------------------

Engine: `/haipipe-task-llm-engine` (owns code/haiutils/llm_engine/, the LLM call runtime these tasks import).
Adjacent: `/claude-api` for Claude SDK patterns (caching, tool-use loops, retries).


Step 7 — Report
----------------

```
status:    ok
summary:   Scaffolded agent job <NN>_<name> under the selected bNN Block / jNN Job.
artifacts: [paths created including prompts/system.md, prompts/user.md]
next:      edit prompts/, set inputs in config, then run.sh
```


MUST NOT
---------

- Embed prompts inline in the `.py` — they live in `prompts/*.md`.
- Skip transcript logging — `$OUTPUT_ROOT/<task>/results/rNN_<run>/transcript.json` is mandatory
  (every API call + tool call recorded for audit).
- Hardcode an API key in the script — read from env var.
- Create `README.md`.


First-run gate
---------------

`runs/<RUN>.sh` blocks execution if `CODE_REVIEW.md` is missing or stale (gate inherited from `../../../haipipe-task/ref/run-sh-template.sh`).
For the first run after this scaffold, do ONE of:

  1. **Recommended** — run the haipipe-task-reviewer-agent (Gate 1) on this
     job to produce a fresh `CODE_REVIEW.md`:
     `Tools/plugins/haipipe-toolkit/skills/task/agents/haipipe-task-reviewer-agent.md`

  2. **Temporary bypass** — set env var at launch:
     `HAIPIPE_SKIP_REVIEW=1 bash runs/<RUN>.sh`
     (skips the gate for one run; logs a warning to stderr.)

  3. **Permanent skip for this config** — add to `scripts/config/<RUN>.yaml`:
     ```yaml
     _meta:
       skip_review: true
     ```
     (Only appropriate for throwaway / disposable runs.)

Surface this to the user in the orchestrator's `next:` line so they know **before** trying to launch.
