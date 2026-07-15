task — open issues
=====================

Tracked here so future sessions can pick them up without re-discovering.


haipipe-task-for-agent: LOW QUALITY, needs rethink
----------------------------------------------------

- [ ] `ref/config-seed.yaml` is a generic placeholder — `inputs:` example points to a non-existent path, `api:` block uses `env:` prefix syntax that no runner actually parses. (Model IDs were stale `claude-opus-4-7`; FIXED → `4-8` / `sonnet-5` on 2026-07-15.)
- [ ] `fn/scaffold.md` is copy-paste boilerplate — prompts/ dir is the only differentiator from the generic scaffold, and even that is thin.
- [ ] `ref/workflow-plan-sample.yaml` phases (Setup → Execute → Parse) are too generic — every task could be described this way.
- [ ] Zero task instances in any project. Never been used end-to-end.
- [ ] Possible overlap with the `application` family, which already orchestrates LLM-driven sessions with plans and gates. Is `for-agent` a simpler version of the same thing, or a genuinely different scope?
      ⚠️ PREMISE PARTLY DEAD (2026-07-14) — this item originally compared against `haipipe-application-ask` and "DIKW cards". Neither exists: `haipipe-application-ask` is ARCHIVED (`application/_archive/haipipe-application-ask/`, de-registered) and the insight layer's D/I/K/W cards were RETIRED 2026-07-12. Compare against the CURRENT application family before deciding.
- [ ] Decision needed: update to be useful, or remove and let `haipipe-application` own agent-driven tasks.


Specialist architecture: scaffold vs lifecycle tension
-------------------------------------------------------

- [ ] Path 1 (scaffold new folder) calls `Skill("haipipe-task-for-<type>")` which runs `fn/scaffold.md`. Path 2 (lifecycle on existing folder) runs `task-lifecycle.workflow.js` where the creator agent reads the specialist's `ref/workflow-plan-sample.yaml` + `SKILL.md` as reference only — never calls the specialist as a Skill. Two paths, two roles, one set of files.
- [ ] Long-term: consider collapsing scaffold into the creator agent (Path 1 becomes a Build stage invocation), eliminating `fn/scaffold.md` as a separate procedure.
- [ ] `fn/scaffold.md` exists in 10 specialists sharing the same 7-step SKELETON, but the bodies have DIVERGED (measured 2026-07-15: ~95 diff-lines / ~120 vs the for-data baseline — the old "~90% identical" figure no longer holds). Decide: extract a shared scaffold-base with per-type overrides, OR accept the divergence as intentional per-type specialization and close this item.


Specialist coverage gaps
-------------------------

- [ ] Most real B-series tasks are **statistical analysis** scripts (heterogeneity, robustness, arm decomposition, funnel, descriptives, data foundation) — not model evaluations. `for-eval` is the closest match but its description says "score a trained model." Broaden `for-eval` to "any analytical script that produces results/" or add `for-analysis`.
- [ ] `C_insight_report` group has many `report_*.py` scripts with no specialist.
- [ ] `for-individual` has zero task instances (but has a real cross-reference to `/haipipe-individual`).
- [ ] `for-algo` has one task instance (`X01_algo_LBG`).


Model IDs drift
----------------

- [ ] Model-id drift (general). The concrete `for-agent` + `llm-engine` `claude-opus-4-7` / `claude-sonnet-4-6` residuals were FIXED → `4-8` / `sonnet-5` on 2026-07-15. STILL OPEN — the recurrence risk: any specialist that hardcodes model IDs will drift again. Consider a shared `ref/model-ids.yaml`, or document 'use the latest' without pinning, so this stops coming back.


Lifecycle design: validate before expanding (2026-06-11 review)
----------------------------------------------------------------

The 4-phase lifecycle architecture is sound at the structural level (hub-and-spoke, creator-reviewer separation, IPO schema chain, strict file ownership). But the system has more machinery than battle-tested usage. These items should be revisited after running the lifecycle on 3-5 real tasks.

- [x] **Execute = the human's real run on the cluster/server — BY DESIGN, not a fiction (JL, 2026-07-15).** `autoExecute` defaults to false because the heavy tasks (NN training, big-data, endpoint deploy, edit-local→run-server) execute OUTSIDE this local Claude session — on the real cluster/server, run by the human, eventually and for real. The local lifecycle deliberately wraps Plan/Build/Report AROUND that manual run and records it; it does NOT try to auto-run what it cannot reach. The `autoExecute=true` branch (spawn a runner agent → Gate-2 audit) stays available for genuinely local tasks (data-prep, local stata, display render). ⚠️ DO NOT "fix" this by flipping the default or deleting the stage — the earlier "3+1 fiction" framing was WRONG. Only doc honesty is owed: SKILL.md may mark it `Plan → Build → [Execute] → Report` where `[Execute]` = the (usually remote, manual) run.
- [ ] **No lifecycle state persistence.** Running `/haipipe-task plan <path>`, closing the session, then running `/haipipe-task build <path>` starts fresh — no record that Plan completed with verdict=pass. Add a `workflow/state.yaml` tracking per-stage completion + verdicts for cross-session continuity.
- [ ] **Agent prompts lack worked examples.** The workflow.js tells creators "read the schema, generate the YAML" and reviewers "check 5 things" — but neither prompt includes a concrete example of a good vs. bad artifact. LLM agents do much better with examples than with checklists alone.
- [ ] **Retry feedback is unstructured.** On revise, feedback is `reviewerResult.feedback || issues.join('; ')` — a concatenated string. No mechanism ensures the creator actually addresses each point vs. regenerating. Structured feedback (`{issues: [{id, severity, file, line, description}]}`) would make retries more reliable.
- [ ] **Reviewer model is weaker than creator.** Reviewer uses `model: sonnet`, creator inherits (likely Opus). Can Sonnet reliably catch intent-vs-implementation bugs that Opus wrote? The two-stage Claude+Codex review partially compensates, but monitor this.
- [ ] **SKILL.md is 330 lines.** The keyword table, dispatch table, and 7-step protocol are lookup tables that could be externalized to `ref/` files and read on demand, reducing the context load during routing.
- [ ] **Report can run without Execute.** If a human runs manually then calls `/haipipe-task report`, the report creator must find and interpret results it didn't witness. No mechanism verifies the results are from the current plan cycle.
- [ ] **Schema compliance is reviewer-trust only.** The reviewer is told "check schema compliance" in natural language. There is no programmatic JSON Schema validation step — it's all trust-the-reviewer.
