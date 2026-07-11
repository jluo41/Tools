# display stage checklist

Done-gate for the **display** stage (`haipipe-paper-display`). The stage is complete only when every box below is checked AND the user confirms the gate (`../../wiki/08-stage-gate.md`). This checklist is the canonical home of the gallery requirements; the paper's stage files should NOT restate them, they should point here.

## Stage doc (`0-lifecycle/4-display/`) — the md → tex → pdf trio
- [ ] `4-display.md` present and is the ONLY hand-edited stage file (canonical template `ref/display-template.md`): Venue Set + gallery config, Display Map (row order = narrative order = gallery order), Probes (`###` sub-items, seed/claims shape), one paper-section group per section (`venue expects:` line; each display a `###` subsection; grouping matches the map's `section` column), Parking section.
- [ ] Legacy files migrated and gone: no `4-display-probes.md`, no `4-display-preview.txt` / contact-sheet file, no `%% {USER}:` comments left in the tex (all merged VERBATIM into the md; `[MIGRATE]` logged).
- [ ] `_LOG_4-display.md` exists (created at first invocation; missing = defect).
- [ ] `_DISPLAY_REQUEST.md` inbox consumed: no row left `requested` (each `accepted`/`declined` with reason; delivered units flipped `done (unit: ...)`).
- [ ] `Probes` entries all terminal: every `###` entry `done` with its `Outcome:` filled, or user-skipped (logged at the gate); no `✋` entry run while its gating thread was unruled, none silently dropped. PROBE's S0 cross-stage sweep ran (or was explicitly skipped with a logged reason): unfiled section/narrative display needs are DR rows, not invisible.
- [ ] `4-display.tex` is REGENERATED from the md by sync — never hand-edited: `\section*{<paper section>}` banner at each section change, a named `\subsection*{Figure N. <name>}` / `Table N. <name>` per display, small-font interrogation verdicts, `\input` per unit, Parking section last (parked units never `\input` into the manuscript).
- [ ] Gallery sizing knobs (width cap, float pinning, spacing) live in the md's gallery config and are emitted into the generated tex preamble — never pushed into a unit's `float.tex` or source spec.
- [ ] `4-display.pdf` recompiled and current (a stale PDF is a defect; recompile after every edit, from the paper root so `0-displays/` paths resolve).
- [ ] Shaped to the VENUE display set (read STATUS `venue`; consult the paper's `0-lifecycle/2-venue/2-venue.md` Structural Blueprint display units + Writing Principles display limits; fall back to `../../_venue/playbook-<venue>` `-> Display` only if 2-venue.md is absent). For UTD-IS (MISQ/ISR/MS-IS): research-model figure as the hero, a research-design figure, a hypothesis-test table, descriptives.
- [ ] The `[primary]` claim's display is the HERO (first figure).
- [ ] Figures/tables numbered by order of appearance.

## Per display block (in `4-display.md`)
- [ ] Block present: takeaway, claim, evidence source, section, caption job, fragility, status.
- [ ] ASCII sketch present (real numbers when available) — the md's sketches ARE the contact sheet; no separate preview file.
- [ ] Method candidates recorded: 2–3 lettered candidate lines for non-trivial displays (different forms/routes, incl. diagram/illustration where apt); every line PROBE-filled (output + one-line self-assessment) or explicitly struck.
- [ ] No markdown pipe tables anywhere in `4-display.md` (JL 2026-07-10): map, probe plan, candidates, and Parking are record lines; tabular text appears only inside fenced sketches.
- [ ] No block stuck at `candidates`: winner promoted to `assets/` with a recorded why per loser (losers in `versions/`), or the block is parked. A `> USER:` preference decides — never overruled.
- [ ] `> USER:` threads kept VERBATIM in the block; every one has a `> CC:` reply or a user resolution (resolved threads moved to `_LOG`). No comments in unit files or the generated tex.
- [ ] Per-display interrogation verdict recorded (keep-main / keep-supplement / fix / demote / cut + one sharp reason), from the independent render-review subagent (builder ≠ judge).

## Per display unit (`0-displays/displayNN-<slug>/`)
- [ ] `README.md` present and status-mirrored from the md map.
- [ ] `float.tex` present and `\input`-able from the paper root (paths are `0-displays/...`-relative); no pasted numbers (data displays RENDERED from task-produced evidence; concept figures via diagram (vector) or illustration (raster)).
- [ ] `preview.tex` + compiled `preview.pdf` current.
- [ ] `candidates/` resolved (empty or archived to `versions/` after the pick); winning asset in `assets/`; rebuild spec in `source/` pointing at the producing task output.

## Vector renders (display-diagram)
- [ ] Research-model / framework figures use ELBOW (`"ortho": true`) connectors, not curves (the MISQ/ISR house style).
- [ ] Per-construct `"icon"` glyphs used where they aid comprehension (clinician / star / pill / clipboard / fork ...).

## Route on a gap
| gap | route |
|---|---|
| display needs task-produced numbers | PROBE evidence lane: `/haipipe-task-for-display <need>` (direct, not claim-gated) |
| display rests on an unverified claim | PROBE evidence lane: `/haipipe-paper probe "<need>"` |
| missing / weak render, candidate never tried | PROBE render lane: figure / table / diagram / illustration skill |
| wrong figure sequence / hero does not sell the story | `/haipipe-paper-lifecycle pitch` or DRAFT |

## Exit (stage gate)
- [ ] Display Map consistent with units on disk — no orphans either way (asset without row, row without asset/float).
- [ ] Every display referenced in narrative (`3-narrative.md`).
- [ ] Every block + unit + stage-doc item above checked.
- [ ] Exit criteria presented to the user per `../../wiki/08-stage-gate.md`; user confirmed; `STATUS.md` Gate Ledger updated.
