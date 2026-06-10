C_task — open issues
=====================

Tracked here so future sessions can pick them up without re-discovering.


haipipe-task-for-agent: LOW QUALITY, needs rethink
----------------------------------------------------

- [ ] `ref/config-seed.yaml` is a generic placeholder — model IDs stale (`claude-opus-4-7` → 4.8), `inputs:` example points to a non-existent path, `api:` block uses `env:` prefix syntax that no runner actually parses.
- [ ] `fn/scaffold.md` is copy-paste boilerplate — prompts/ dir is the only differentiator from the generic scaffold, and even that is thin.
- [ ] `ref/workflow-plan-sample.yaml` phases (Setup → Execute → Parse) are too generic — every task could be described this way.
- [ ] Zero task instances in any project. Never been used end-to-end.
- [ ] Possible overlap with `G_application` family (`haipipe-application-ask`, `-message`) which already orchestrates LLM-driven sessions with plans, gates, and DIKW cards. Is `for-agent` a simpler version of the same thing, or a genuinely different scope?
- [ ] Decision needed: update to be useful, or remove and let `haipipe-application` own agent-driven tasks.


Specialist architecture: scaffold vs lifecycle tension
-------------------------------------------------------

- [ ] Path 1 (scaffold new folder) calls `Skill("haipipe-task-for-<type>")` which runs `fn/scaffold.md`. Path 2 (lifecycle on existing folder) runs `task-lifecycle.workflow.js` where the creator agent reads the specialist's `ref/workflow-plan-sample.yaml` + `SKILL.md` as reference only — never calls the specialist as a Skill. Two paths, two roles, one set of files.
- [ ] Long-term: consider collapsing scaffold into the creator agent (Path 1 becomes a Build stage invocation), eliminating `fn/scaffold.md` as a separate procedure.
- [ ] `fn/scaffold.md` across 12 specialists is ~90% identical (same 7-step pattern). Extract a shared scaffold-base with per-type overrides.


Specialist coverage gaps
-------------------------

- [ ] Most real B-series tasks are **statistical analysis** scripts (heterogeneity, robustness, arm decomposition, funnel, descriptives, data foundation) — not model evaluations. `for-eval` is the closest match but its description says "score a trained model." Broaden `for-eval` to "any analytical script that produces results/" or add `for-analysis`.
- [ ] `C_insight_report` group has many `report_*.py` scripts with no specialist.
- [ ] `for-individual` has zero task instances (but has a real cross-reference to `/haipipe-individual`).
- [ ] `for-algo` has one task instance (`X01_algo_LBG`).


Model IDs drift
----------------

- [ ] `for-agent` refs `claude-opus-4-7` — latest is `claude-opus-4-8`. Any specialist that hardcodes model IDs will drift. Consider a shared `ref/model-ids.yaml` or just document "use the latest" without pinning.
