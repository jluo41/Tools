display — Changelog
===================

Family-level changes. Skill implementation history stays in each skill's own CHANGELOG.

## 2026-08-16 · The ✒️ tex kind gets its skill

JL: "should we have a new skill for the tikz? or make -diagram include tikz?"
Ruled: its own skill, `haipipe-display-tex`, named after the MECHANISM — so one
skill covers a TikZ figure, an `algorithm2e` block, and a display equation,
which share a writer (a person), a recipe (a hand-authored `.tex`), and a
binding (`float.tex` `\input`s it).

Kept out of `-diagram` deliberately: that skill compiles a JSON FigureSpec
through 1095 lines of SVG machinery, while this kind has no script at all, and
FigureSpec has no vocabulary for named tikz styles, TeX macros, or math. The
craft written down came from QPf5's two hand-authored units: the two-compile law
(`assets/figure.pdf` must exist for consumers who cannot carry the preamble),
`preview.tex`'s package list as the dependency declaration, and the rule that a
clipped preview is a failed build.

Five renderers now: table · figure · diagram · illustration · tex.

## 2026-08-16 · Four renderers and a door

JL, in two steps on the same day. First: "我们是不是只保留一个 … 没必要搞那么多" —
`haipipe-display` was born as the family's door and the two thin data skills were
folded into it. Then, on seeing the shape: "figure 和 table 是不是也可以保留呢?"
and "poster 和 slides 我们都不要了" — which is the better cut, so the fold was
reversed and the real reduction happened by retirement instead.

- `haipipe-display` stays, now a PURE ROUTER: one name to say when you do not
  know which renderer you want, skippable when you do.
- `haipipe-display-table` and `haipipe-display-figure` return as full skills.
- RETIRED to `_todo/`, per the toolkit's park-don't-delete convention:
  `haipipe-display-poster`, `haipipe-display-slides`, their paper-side selection
  doors `paper-poster` and `paper-slides`, and `ref/content-plan-spec.md`, which
  served that chain alone. A board page's talk is the slide plugin's deck, and
  `html-ppt` stays because that deck links its assets.
- The ✒️ TeX-native method was NAMED in the routing tables as hand-authored and
  skill-less; the entry above closed that gap the same day.
- The family also gained its README and CHANGELOG, and a stray empty `skills/`
  directory from 260815 was removed.
