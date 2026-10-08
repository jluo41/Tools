## 2026-09-22 · vendored

- Copied from https://github.com/larashero3-dotcom/writing-dna-skill at commit `ee3d97ee` (upstream version unversioned, MIT). Role `style`: distills an author corpus into a frozen Writing DNA that `ref/writing-dna-adapter.md` consumes. The upstream repo's nested `skills/lieflat-less-ai-tone` was deliberately NOT copied: it is a separate anti-tone skill and would install as a fourth skill.
- Only the files the skill needs were copied; images and the upstream repository
  scaffolding stayed in `references/`. The SKILL.md body is unchanged; the frontmatter
  carries the haipipe provenance stamp.
- Upstream text still names `skills/lieflat-less-ai-tone/` (README.en.md, SKILL.md, workflow.en.md): that nested skill was not copied; it stays at `references/writing-dna-skill/skills/`, and the anti-tone step it offers is covered here by `2_evaluate/humanizer` and `haipipe-writing/cli/anti_slop.py`.
