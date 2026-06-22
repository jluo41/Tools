---
status: fixed
created: 2026-06-22
context: lifecycle tex generation. Convention source: 3-write-edit/haipipe-paper-edit-content + 3-write-edit/_shared/sentence-format.md (+ paragraph-indexing.md). Generators to fix: haipipe-paper-folder / scripts/init_paper_layout.py (lifecycle_stage_tex + per-stage *_tex) and the stage skills haipipe-paper-structure-{seed,pitch,claims,narrative,minimap}.
fixed_in: "2026-06-22 revision pass (init_paper_layout.py prose generators + haipipe-paper-structure-pitch template)"
---

Reporter (JL): lifecycle 的 paper 里,生成这个 tex 的时候,要符合
3-write-edit/haipipe-paper-edit-content 定义的格式: ---- Pn.Sn ---- 的 sentence,
然后 % 当作 sentence 分割符。

Detail: the `0-lifecycle/<stage>/<stage>.tex` files (seed/pitch/claims/narrative/
minimap) are currently generated with plain `\section*{}` blocks and free-running
prose. They do NOT carry the canonical edit-cycle layout from
`_shared/sentence-format.md`: a paragraph banner with a stable `[id]`, one
sentence per line, each sentence tagged `%% ---- Pn.Sm ----` (Pn restarts per
file, Sm per paragraph), with a lone `%` line allowed between sentences. Because
lifecycle tex is not in this layout, the edit/annotate/improve tooling in
3-write-edit cannot attach comments cleanly to lifecycle stage files.

Fix (2026-06-22): the PROSE lifecycle generators (seed/pitch/narrative in
init_paper_layout.py) now emit the canonical layout: a paragraph banner per
section + one sentence per line + `%% ---- Pn.Sm ----` tags, with an inline
pointer to 3-write-edit/_shared/sentence-format.md. The pitch skill template
demonstrates the same. Table stages (claims/figures-tables/minimap) deliberately
stay plain `\section*{}` + tabular with NO paragraph banner, per JL: the
sentence-format is for prose, not table rows.
