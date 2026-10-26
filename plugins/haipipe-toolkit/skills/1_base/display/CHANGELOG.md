display — Changelog
===================

Family-level changes. Skill implementation history stays in each skill's own CHANGELOG.

## 2026-10-26 · the five renderers become parts of the door (JL 261026)

- Same day, second pass: the three converters figure-to-svg, html-to-svg and icon-to-svg (never used) also became
  parts, `haipipe-display/_parts/<name>/PART.md`, listed in the door under its route table
  (`diagnostics/merge_parts.py --spec base-more`). html-ppt stays a skill (used).

- haipipe-display-table, -figure, -diagram, -illustration and -tex move to
  `haipipe-display/_parts/<kind>/PART.md` (`git mv`); the installers skip `_` folders, so only the door is listed
  (476 fewer listing tokens). The door's route table and `haipipe-display-unit-agent` read the part for the kind.
  Done by `diagnostics/merge_parts.py --spec display` (Tools root); each touched skill got one CHANGELOG entry and
  one version bump (door 0.5.0).

## 2026-10-16 · the Excalidraw skills move out (JL 261016)

- excalidraw-studio, -report, -section, -read, -revise, -workflow, -job, -task, -slide and -ideation move to
  `1_base/excalidraw/` ("we also need a 1_base/excalidraw to put the excalidraw-xxx skills into here"). Every path
  in the seven SPACEs is swept (425 files, then 16 scripts that built the path in pieces); no link is left at the old
  place (JL: "do not use the symlink within the Tools"). The drawings that recorded the old path were rebuilt.

## 2026-10-10 · excalidraw-read joins the family

JL 261010: read a paper's PDF, extract its logic, screenshot the key parts with the quote
highlighted, comment on each, and link each to our paper. `excalidraw-read` 0.1.0 does it with
one script (`text`, `shoot`, `draw`) and `haipipe-studio`'s merge-safe canvas writer. It is a
working drawing, like `excalidraw-report` and `excalidraw-draft`, not a display unit.

## 2026-09-28 · No content hashes (JL 260928)

AGENTS.md rule 9: a display intake records where its snapshot came from and
when it was frozen (`snapshot.materialized_at`), never a `sha256`; a local
canonical artifact newer than the snapshot means the snapshot is stale.
`haipipe-display` 0.3.6 (shared `ref/`), `haipipe-display table` 0.2.2,
`haipipe-display figure` 0.2.3 and `haipipe-display-unit-agent` 0.1.1 follow.
`figure-to-svg` finds a byte-identical prior source with `cmp -s`, not MD5.

## 2026-09-20 · Figure review evidence and tolerances

`figure-to-svg` now requires matched source/replica render context, dimensions,
intended display size, and visible evidence for each issue. Its local severity
anchors distinguish meaning changes, material readability loss, and local
differences; missing context returns `not-verifiable`.

## 2026-08-16 · The ✒️ tex kind gets its skill

JL: "should we have a new skill for the tikz? or make haipipe-display diagram include tikz?"
Ruled: its own skill, `haipipe-display tex`, named after the MECHANISM — so one
skill covers a TikZ figure, an `algorithm2e` block, and a display equation,
which share a writer (a person), a recipe (a hand-authored `.tex`), and a
binding (`float.tex` `\input`s it).

Kept out of `haipipe-display diagram` deliberately: that skill compiles a JSON FigureSpec
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
- `haipipe-display table` and `haipipe-display figure` return as full skills.
- RETIRED to `_todo/`, per the toolkit's park-don't-delete convention:
  `haipipe-display-poster`, `haipipe-display-slides`, their paper-side selection
  doors `paper-poster` and `paper-slides`, and `ref/content-plan-spec.md`, which
  served that chain alone. A board page's talk is the slide workbench's deck, and
  `html-ppt` stays because that deck links its assets.
- The ✒️ TeX-native method was NAMED in the routing tables as hand-authored and
  skill-less; the entry above closed that gap the same day.
- The family also gained its README and CHANGELOG, and a stray empty `skills/`
  directory from 260815 was removed.
