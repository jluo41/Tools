# display stage checklist

Done-gate for the **display** stage (`haipipe-paper-display`). The stage is complete only when every box below is checked AND the user confirms the gate (`ref/stage-gate.md`). This checklist is the canonical home of the gallery requirements; the paper's `0-lifecycle/4-display/4-display.tex` should NOT restate them, it should point here.

## Per display unit (`0-displays/displayNN-<slug>/`)
- [ ] `README.md` present (reader takeaway, claim supported, evidence source, placement, caption job, fragility, status).
- [ ] `float.tex` present and `\input`-able from the paper root (paths are `0-displays/...`-relative).
- [ ] `preview.tex` + compiled `preview.pdf` current.
- [ ] Data displays are RENDERED by a task/probe from real evidence, never hand-authored in `float.tex`. Concept figures may use diagram (vector) or illustration (raster).
- [ ] Per-unit interrogation verdict recorded (keep / move / demote / cut + one sharp comment).

## Gallery (`0-lifecycle/4-display/4-display.tex`) — the stage doc
- [ ] Ordered to the NARRATIVE flow: Introduction/Theory -> Methods -> Results -> Discussion.
- [ ] TWO heading levels so the reader is never lost: a `\section*{<paper section>}` banner, then a named `\subsection*{Figure N. <name>}` / `Table N. <name>` per display.
- [ ] Figures/tables numbered by order of appearance.
- [ ] Shaped to the VENUE display set (read STATUS `venue`; consult `../../_venue/playbook-<venue>` `-> Display`). For UTD-IS (MISQ/ISR/MS-IS): research-model figure as the hero, a research-design figure, a hypothesis-test table, descriptives.
- [ ] The `[primary]` claim's display is the HERO (first figure).
- [ ] A PARKING section at the end keeps superseded / alternative displays for history; never `\input` into the manuscript.
- [ ] Per-display `%% {JL}: ...` preference comments kept VERBATIM inline beside each display's `\input`, across iterations. They live ONLY here, not in the unit `float.tex` (units stay portable, comment-free).
- [ ] `4-display.pdf` recompiled and current (a stale PDF is a defect; recompile after every edit, from the paper root so `0-displays/` paths resolve).
- [ ] An ASCII contact sheet `0-lifecycle/4-display/4-display-preview.txt` (via /diagram-ascii) previews EVERY display in narrative order — one block each: Fig/Tab N + name + section + claim + a compact sketch (real numbers when available) + status + a `👉 {JL}:` slot — including to-build units. It is the comment-collection surface; collected notes persist to `4-display.tex`. Regenerate as the set evolves.

## Vector renders (display-diagram)
- [ ] Research-model / framework figures use ELBOW (`"ortho": true`) connectors, not curves (the MISQ/ISR house style).
- [ ] Per-construct `"icon"` glyphs used where they aid comprehension (clinician / star / pill / clipboard / fork ...).

## Route on a gap
| gap | route |
|---|---|
| display needs a materialized data artifact | `/haipipe-task-for-display <need>` (direct, not claim-gated) |
| display rests on an unverified claim | `/haipipe-paper probe "<need>"` |
| wrong figure sequence / hero does not sell the story | `/haipipe-paper-lifecycle pitch` or `plan` |

## Exit (stage gate)
- [ ] Gallery README (`0-displays/README.md`) present and consistent with units on disk.
- [ ] Every unit + the gallery items above checked.
- [ ] Exit criteria presented to the user per `ref/stage-gate.md`; user confirmed; `STATUS.md` Gate Ledger updated.
