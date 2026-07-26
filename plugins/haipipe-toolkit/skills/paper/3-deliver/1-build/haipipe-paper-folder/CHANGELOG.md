haipipe-paper-folder — Changelog
================================

Skill-scoped changelog (never loaded at invocation; read on demand). Versions match SKILL.md frontmatter `version:`. Newest first. Rollup: layer-level `paper/CHANGELOG.md`.


## [0.5.0] — 2026-07-26 — Board-first and minimal; no STATUS.md, no 0-displays/

Rewritten against the layout ruled on the design board (face QA6).

- **The scaffold shrank and gained a runnable page.** Was `README` + `STATUS.md` + `.gitignore` + three EMPTY containers. Now `README` + `.gitignore` + `0-lifecycle/` carrying `board.md` and one `S-Seed-0-seed.md`, so a new paper is workable on day 0 instead of being a set of empty directories.
- **`STATUS.md` is no longer created.** The frontier is derived from disk and from each page's own `state:`; a stored frontier can only go stale, and a stale one becomes a third answer to "where is this paper" that disagrees with the other two.
- **`0-displays/` is gone from creation.** Displays are unnumbered (`displays/`) and arrive with the manuscript upgrade, one folder per unit. There is no top-level `figures/`.
- **`1-probes/` is no longer pre-created.** It arrives on the first probe, like everything else: absent until allocated.
- **One family, one folder** documented, with the note that `haipipe-board/stage.py resolve` owns the filename rule and this skill must not reimplement it.
- **The manuscript upgrade section rewritten**: the deliverable is unnumbered (`<paper>.tex`, `<paper>.bib`, `sections/`, `appendices/`, `displays/`, the venue shell) and only `2-src/` carries a number. Ends with a hard requirement to run `/haipipe-paper-conform` and report the delete-test verdict.


## [0.4.0] — 2026-07-24

Renumbered under the 0.x policy — the whole haipipe-toolkit is pre-1.0 until JL says otherwise (was 4.0.1; older entries below keep their original numbers).

## 4.0.1 — 2026-07-14

- "probe plans (PPNN_*.md) -> fn/probe-plans.md" -> "probe files (PPNN_<topic>.md) -> fn/probes.md" (the file was renamed).

## [3.1.0] — 2026-07-08
## 4.0.0 — 2026-07-14

- PROBE REDESIGN (Tools/plugins/haipipe-toolkit/diagram/260714-probe-qa/ v3, approved JL 2026-07-14 — R1-R18). 1-probe-plans/ -> 1-probes/ (PPNN_<topic>.md, one file per TOPIC, one SECTION per question: serves/target/state/commission/reading + ONE `## Why` per file holding the stake). Binding is by PATH: a section's `target:` points at the answering `<leaf>/QA/<n>-<slug>.md` in the bank. DELETED: `## Verdict`, the `verdicted` and `dispatched` states, `_ASK/`/`_ANS/` stubs, `answers:`, and Agent(haipipe-probe-orchestrator-agent) (the GATEWAY — archived + de-registered). A claim's STATUS now lives ONLY in 0-lifecycle/1b-claims/1b-claims.md. Dispatch is now DIRECT: the section's `commission:` block, VERBATIM, to Agent(haipipe-task-orchestrator-agent) / Agent(haipipe-discovery-orchestrator-agent).
- THE SCAFFOLDER NO LONGER CREATES A RETIRED FOLDER. It scaffolded `1-probe-plans/`, so every NEW paper was born in the migration-needed state — the v8 probe worker and checker look in `1-probes/` and would find nothing. Now scaffolds `1-probes/`.

Changed (venue lockfile wiring)
- Manuscript Upgrade section format now consults the paper's `0-lifecycle/2a-venue/2a-venue.md` Structural Blueprint first; direct `_venue/playbook-<venue>` read demoted to fallback when 2a-venue.md is absent.

## [3.0.1] — 2026-07-04

Fixed
- `1-probe-plans/` comment updated: it is the INDEX home (README.md created on first plan); plan files live per-stage in `0-lifecycle/<stage>/_PROBE/`.

## [3.0.0] — 2026-07-03

- rewritten to the current architecture. Prospectus terminology retired (papers start at maturity seed); 0-lifecycle spine corrected (1-claims, 2-pitch, 5-section-edit; minimap dead); early stages are markdown so creation ships ZERO LaTeX; scaffold reduced to README + STATUS.md + .gitignore + empty containers (absent-until-written); master tex / 0-sections / compile scripts demoted to the Manuscript Upgrade section (on request, typically at display or section-edit); scripts/init_paper_layout.py (854 lines, generated the pre-2026-07 layout) retired to _archive/.

## [2.0.0] — 2026-06-08

- complete rewrite matching real Paper-* folders; venue templates + section stubs (now superseded).

## [1.1.0] — 2026-06-05

- renamed from paper-bootstrap to haipipe-paper-bootstrap.

## [1.0.0] — 2026-05-31

- baseline metadata added.
