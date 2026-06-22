---
status: open
created: 2026-06-22
context: haipipe-paper-structure-display + 4-figures-tables lifecycle stage
fixed_in: ""
---

The 4-figures-tables lifecycle stage is a PASSIVE inventory — it lists displays with a text status ("ready"/"weak") but doesn't route to any production skill. It's a dead contract.

The display skill system (haipipe-paper-structure-display) has a sophisticated pipeline designed in its SKILL.md:
- 6-status tracking: planned -> data-ready -> rendered -> input-ready -> inserted -> reviewed
- 5 modes: plan / scaffold / build / audit / insert
- per-unit folders: 0-displays/displayNN-slug/ with README.md, float.tex, preview.tex, assets/, source/

But nothing connects 4-figures-tables.tex to these skills. The lifecycle stage should be the DEMAND BOARD that actively routes to production:

1. planned (need data) -> /haipipe-task-for-display (scaffold C-series task)
2. data-ready (need plot) -> /haipipe-paper-structure-figure (generate publication fig)
3. data-ready (need diagram) -> /haipipe-paper-structure-figure-spec (FigureSpec -> SVG -> PDF)
4. rendered (need wrapper) -> /haipipe-paper-structure-display scaffold (create unit folder)
5. input-ready (need preview) -> /haipipe-paper-structure-display build (compile preview.pdf)
6. input-ready (need insertion) -> /haipipe-paper-structure-display insert (add \input to section)
7. inserted (need audit) -> /haipipe-paper-structure-display audit (claim/caption/evidence check)
8. claim unclear -> /haipipe-probe judge (verify evidence)

Currently broken for Paper-SuitableMessageForRx-JAMANO:
- No 0-displays/ structure (figures flat in 0-display/Figure/)
- No per-unit folders, no float.tex wrappers, no preview.pdf
- No source/ reproducibility (B00 task link is informal, not tracked)
- Captions baked into section files instead of display units
- Figure-planner never ran (panel roles in informal FIGURE_PLAN.md)
- No per-item status tracking in the lifecycle stage

The fix involves two things:
(a) Make 4-figures-tables.tex use the 6-status vocabulary and route to skills
(b) Make haipipe-paper-structure-display callable FROM the lifecycle stage, not just standalone

Related skills that should be called from the display demand board:
- /haipipe-paper-structure-display (plan/scaffold/build/audit/insert)
- /haipipe-paper-structure-figure (data plots from task results)
- /haipipe-paper-structure-figure-planner (panel roles, claim anchors)
- /haipipe-paper-structure-figure-spec (deterministic vector diagrams)
- /haipipe-task-for-display (scaffold C-series display tasks)
- /haipipe-probe (claim verification for display evidence)

Fix:
