fn-scaffold: Scaffold an LLM-agent task-folder
=================================================

Call an LLM agent (Claude / GPT) with prompts + tools for an analysis,
summarization, or audit task. Group letter default: **F** (agent).

Output: `tasks/F{NN}_<group>/{NN}_<task_name>/`.


Step 1 — Identify project + task-group
---------------------------------------

- Auto-detect project from cwd.
- ASK task-group if not given. Group letter must be **F**;
  scaffold a new `F{NN}_<group_name>/` if needed.


Step 2 — Collect metadata
--------------------------

- 2-digit NN: next free in this group.
- snake_case task_name: descriptive
  (e.g., `summarize_eval_logs`, `audit_patient_notes`).
- Model: `claude-opus-4-7 | claude-sonnet-4-6 | claude-haiku-4-5`.
- Tools (optional): list of tool names available to the agent.
- Inputs: what data context the agent reads.
- `_meta:` block.


Step 3 — Create skeleton
-------------------------

```
F{NN}_<group>/
└── {NN}_<task_name>/
    ├── {NN}_<task_name>.py
    ├── prompts/
    │   ├── system.md                       system prompt
    │   └── user.md                         user prompt template (with {placeholders})
    ├── configs/
    │   └── agent_<name>.yaml               from ref/config-seed.yaml
    ├── runs/
    │   └── agent_<name>.sh
    ├── results/
    │   └── <run>/                           transcript.json, summary.md
    └── notebooks/
```

Note: `prompts/` is unique to agent tasks — keeps prompt content
diff-friendly and out of the `.py`.


Step 4 — Seed config + prompts
-------------------------------

Copy `ref/config-seed.yaml` to `configs/agent_<name>.yaml`. Fill in:
- `_meta:` block.
- `model:`, `max_tokens:`, `temperature:`.
- `prompts.system:` and `prompts.user:` (paths to prompts/ files).
- `tools:` (optional — list of allowed tool names).
- `inputs:` (placeholder values for the user prompt).

Seed minimal `prompts/system.md` + `prompts/user.md` stubs.


Step 5 — Run-script
--------------------

Copy `../haipipe-task/ref/run-sh-template.sh` to `runs/agent_<name>.sh`.
Set `TASK_NAME="{NN}_{task_name}"`.


Step 6 — Cross-skill link
--------------------------

No corresponding pipeline skill yet. Adjacent: `/claude-api` for Claude
SDK patterns (caching, tool-use loops, retries).


Step 7 — Report
----------------

```
status:    ok
summary:   Scaffolded agent task <NN>_<name> under F{NN}_<group>.
artifacts: [paths created including prompts/system.md, prompts/user.md]
next:      edit prompts/, set inputs in config, then run.sh
```


MUST NOT
---------

- Embed prompts inline in the `.py` — they live in `prompts/*.md`.
- Skip transcript logging — `results/<run>/transcript.json` is mandatory
  (every API call + tool call recorded for audit).
- Hardcode an API key in the script — read from env var.
- Create `README.md`.


First-run gate
---------------

`runs/<RUN>.sh` blocks execution if `CODE_REVIEW.md` is missing or
stale (gate inherited from `../haipipe-task/ref/run-sh-template.sh`).
For the first run after this scaffold, do ONE of:

  1. **Recommended** — run the Run Script Reviewer agent on this
     task-folder to produce a fresh `CODE_REVIEW.md`:
     `Tools/plugins/haipipe-toolkit/skills/C_task/agents/reviewers/run-script-reviewer-agent.md`

  2. **Temporary bypass** — set env var at launch:
     `HAIPIPE_SKIP_REVIEW=1 bash runs/<RUN>.sh`
     (skips the gate for one run; logs a warning to stderr.)

  3. **Permanent skip for this config** — add to `configs/<RUN>.yaml`:
     ```yaml
     _meta:
       skip_review: true
     ```
     (Only appropriate for throwaway / disposable runs.)

Surface this to the user in the orchestrator's `next:` line so they
know **before** trying to launch.
