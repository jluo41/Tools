fn-scaffold: Scaffold an LLM-agent job
=================================================

Call an LLM agent (Claude / GPT) with prompts + tools for an analysis, summarization, or audit task.
Hierarchy prefixes are bNN / jNN / tNN / rNN; domain belongs in the descriptive suffix.

Output: `work/bNN_<block>/jNN_<job>/tNN_<task>/`.


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
work/bNN_<block>/
├── board.md
└── jNN_<job>/
    ├── src/                         shared code + config-defaults.yaml
    └── tNN_<task>/
        ├── tNN_<task>.md
        ├── draft/
        ├── workflow/                plan.yaml + report.yaml
        ├── scripts/<worker>.py
        ├── scripts/config/prompts/      system.md + user.md, shared by every Run
        └── runs/rNN_<run>/              one folder per Run
            ├── rNN_<run>.sh             the ticket
            ├── config.yaml              this Run's settings
            ├── run.yaml                 its card (role: trial | make)
            └── result/                  runtime.yaml (the receipt) + the agent's outputs

Generated: $OUTPUT_ROOT/tNN_<task>/runs/rNN_<run>/result/
           $OUTPUT_ROOT/tNN_<task>/notebooks/rNN_<run>.ipynb
```

Note: `scripts/config/prompts/` is unique to agent tasks — keeps prompt content diff-friendly and out of the `.py`.
A Block not yet moved still has the flat `runs/rNN_<run>.sh` beside `results/rNN_<run>/`, with its config in
`scripts/config/rNN_<run>.yaml`; scaffold new Runs in the Run folder only.


Step 4 — Seed config + prompts
-------------------------------

Copy `ref/config-seed.yaml` to `runs/rNN_<run>/config.yaml`.
Fill in:
- `_meta:` block.
- `model:`, `max_tokens:`, `temperature:`.
- `prompts.system:` and `prompts.user:` (Task-relative paths to the `scripts/config/prompts/` files).
- `tools:` (optional — list of allowed tool names).
- `inputs:` (placeholder values for the user prompt).

Seed minimal `scripts/config/prompts/system.md` + `scripts/config/prompts/user.md` stubs.


Step 5 — Run-script
--------------------

Copy `../../../haipipe-task/ref/run-sh-template.sh` to `runs/rNN_<run>/rNN_<run>.sh`.
Set `TASK_NAME="<worker>"` (the worker filename without .py); the Run folder and its Ticket share the exact `rNN_<run>` name.
Write the card `runs/rNN_<run>/run.yaml` (fields: haipipe-run `ref/receipts-and-inventory.md`) with `role: trial`
for a smoke Run and `role: make` for a campaign Run.


Step 6 — Cross-skill link
--------------------------

Engine: `../_parts/llm-engine/PART.md` (owns code/haiutils/llm_engine/, the LLM call runtime these tasks import).
Adjacent: `/claude-api` for Claude SDK patterns (caching, tool-use loops, retries).


Step 7 — Report
----------------

```
status:    ok
summary:   Scaffolded agent job <NN>_<name> under the selected bNN Block / jNN Job.
artifacts: [paths created including scripts/config/prompts/system.md, scripts/config/prompts/user.md, runs/rNN_<run>/run.yaml]
next:      edit scripts/config/prompts/, set inputs in runs/rNN_<run>/config.yaml, then runs/rNN_<run>/rNN_<run>.sh
```


MUST NOT
---------

- Embed prompts inline in the `.py` — they live in `scripts/config/prompts/*.md`.
- Skip transcript logging — `$OUTPUT_ROOT/<task>/runs/rNN_<run>/result/transcript.json` is mandatory
  (every API call + tool call recorded for audit).
- Hardcode an API key in the script — read from env var.
- Create `README.md`.


First-run gate
---------------

`runs/<RUN>/<RUN>.sh` blocks execution if `CODE_REVIEW.md` is missing or stale (gate inherited from `../../../haipipe-task/ref/run-sh-template.sh`).
For the first run after this scaffold, do ONE of:

  1. **Recommended** — run the haipipe-task-reviewer-agent (Gate 1) on this
     job to produce a fresh `CODE_REVIEW.md`:
     `Tools/plugins/haipipe-toolkit/skills/1_base/task/agents/haipipe-task-reviewer-agent.md`

  2. **Temporary bypass** — set env var at launch:
     `HAIPIPE_SKIP_REVIEW=1 bash runs/<RUN>/<RUN>.sh`
     (skips the gate for one run; logs a warning to stderr.)

  3. **Permanent skip for this config** — add to `runs/<RUN>/config.yaml`:
     ```yaml
     _meta:
       skip_review: true
     ```
     (Only appropriate for throwaway / disposable runs.)

Surface this to the user in the orchestrator's `next:` line so they know **before** trying to launch.
