paper/sections — Per-Section Playbooks (Dimension B)"、0-sections/、3-write/4-revise/5-review 旧生命周期;跟 1-probe 无关,是搬家遗留。
> 原文: "paper/sections — Per-Section Playbooks (Dimension B)…"
> 提议: 整体替换为 probe 桶 README:hub(haipipe-paper-probe 4 步)+ 三 harvester(citation/values/display → _CITATION_/_VALUES_/_DISPLAY_,Part-0 新架构)+ PP 卡模型 + check-probe-cards.sh 一句。
> 例子: 新人进 1-probe/ 第一眼读到的是 sections playbook 说明,会以为走错目录;README 是桶的门面。
> 风险: 若这份 sections 内容在别处没有副本,直接覆盖会丢一份旧文档(建议先挪去 paper/_archive/)。
> 问你: A=旧内容挪 paper/_archive/ 再写新 probe README(推荐) / B=直接覆盖不留档?
> JL:

paper/sections — Per-Section Playbooks (Dimension B)
=======================================================

Each playbook here is **reference material for a specific section**:
which angles exist, common framings, what to avoid, what a strong
version looks like. Read by lifecycle skills (3-write / 4-revise /
5-review) when they target a particular .tex file under `0-sections/`.

Each playbook is a thin SKILL.md with slug `section-<name>` — invocable
directly for guidance, or pulled in by a stage skill as context.

Layout
------

```
sections/
├── section-intro/           hooks, motivation framings, contribution claim
├── section-methods/         formal vs operational angles, reproducibility
├── section-results/         story arc, claim mapping, figure choice
├── section-discussion/      limitation framing, implication framing, future-work
├── section-abstract/        condensation strategies (which 3 sentences to keep)
├── section-related-work/    positioning angles
└── section-appendix/        which extras live in appendix vs main paper
```

These map to file groups under `0-sections/` in a real paper folder:

```
0-sections/00_abstract.tex          ← section-abstract
0-sections/01_introduction.tex      ← section-intro
0-sections/02*.tex (Results)        ← section-results
0-sections/03*.tex (Discussion)     ← section-discussion
0-sections/04*.tex (Methods)        ← section-methods
0-sections/05_back-matter.tex       ← (covered by section-discussion / -appendix)
0-sections/A_*.tex .. E_*.tex       ← section-appendix
```

What playbooks are NOT
-----------------------

- NOT a writing skill — they don't produce prose. They provide guidance
  consumed by writing/revising skills.
- NOT venue-specific — venue conventions live in `_venue/` specialists.
- NOT tied to a stage — the same intro playbook informs both writing
  (3-write) and revising (4-revise).

Open questions (not yet decided)
---------------------------------

- Should there also be `section-title/` and `section-cover-letter/`?
  Cover letter is in `0-extra/`, not `0-sections/`, so it may belong
  elsewhere.
- Are 7 sections enough? Real papers may have `limitations/`,
  `ethics/`, `reproducibility/` as standalone sub-sections.
