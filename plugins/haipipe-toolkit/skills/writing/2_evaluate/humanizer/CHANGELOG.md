## 2026-09-22 · vendored

- Copied from https://github.com/blader/humanizer at commit `9862685f` (upstream version 3.0.0, MIT). Role `evaluator` for general-register prose (Pages, notes, docs); 25 patterns in five groups, with a 'when not to act' guard. Ancestor of academic-humanizer.
- Only the files the skill needs were copied; images and the upstream repository
  scaffolding stayed in `references/`. The SKILL.md body is unchanged; the frontmatter
  carries the haipipe provenance stamp.
- Upstream README still gives its own install path `skills/humanizer/`; inside haipipe the skill lives at `skills/writing/2_evaluate/humanizer/` and is selected through `haipipe-writing/ref/writing-methods.yaml`.
