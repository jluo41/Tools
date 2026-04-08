DIKW Analysis Agent Plugin
===========================

Skills for the DIKW (Data → Information → Knowledge → Wisdom) analysis pipeline.

Run a complete analysis session with `/dikw-session`, or invoke individual levels.


Skills
------

**Orchestration:**

| Skill | What it does |
|---|---|
| /dikw-session | Full pipeline: explore → plan → D → I → K → W → report with gates |
| /dikw-review | Gate review between levels: proceed, add tasks, go back, revise plan |

**Individual levels:**

| Skill | Level | What it does | Code? |
|---|---|---|---|
| /dikw-explore | - | Profile raw data, assess quality | no |
| /dikw-plan | - | Design analysis plan from explore notes | no |
| /dikw-data | D | Analyze raw data (WHAT is in the data?) | yes |
| /dikw-information | I | Extract patterns (WHAT PATTERNS exist?) | yes |
| /dikw-knowledge | K | Synthesize insights (WHY do patterns exist?) | no |
| /dikw-wisdom | W | Strategic recommendations (WHAT SHOULD WE DO?) | no |
| /dikw-report | - | Final report synthesizing all findings | no |


Usage
-----

Full session (recommended):
```
/dikw-session /path/to/project "What patterns exist in this dataset?"
```

Individual skill:
```
/dikw-explore /path/to/project
/dikw-data col_overview /path/to/project
/dikw-review /path/to/project
```

With cloud executor (FastAPI bot on Mattermost):
```
claude -p "/dikw-data col_overview /workspace/projects/drfirst"
```


DIKW Boundaries
---------------

```
Level   Question                  Method        Reads              Produces
─────   ────────                  ──────        ─────              ────────
D       WHAT is in the data?      CODE          raw data only      facts + code
I       WHAT PATTERNS exist?      CODE          raw data + D       patterns + code
K       WHY do patterns exist?    REASONING     D + I reports      explanations
W       WHAT SHOULD WE DO?        REASONING     D + I + K reports  recommendations
```


Iteration (non-linear flow)
-----------------------------

DIKW is NOT always linear. The `/dikw-review` gate after each level can:

```
PROCEED     → move to next level
ADD_TASKS   → add more tasks to current level, re-run
GO_BACK     → return to a prior level to fix gaps
REVISE_PLAN → redesign the plan based on new findings
DONE        → skip remaining levels, go to report
```

`/dikw-session` handles all of this automatically.


Principle
---------

**Skill-first development:** Always make skills work locally in Claude Code
first (`/dikw-data col_overview`), then deploy to cloud agents.
The skill prompt is the source of truth.
