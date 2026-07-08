haipipe-paper-folder — Changelog
================================

Skill-scoped changelog (never loaded at invocation; read on demand). Versions match SKILL.md frontmatter `version:`. Newest first. Rollup: layer-level `paper/CHANGELOG.md`.


## [3.1.0] — 2026-07-08

Changed (venue lockfile wiring)
- Manuscript Upgrade section format now consults the paper's `0-lifecycle/2-venue/2-venue.md` Structural Blueprint first; direct `_venue/playbook-<venue>` read demoted to fallback when 2-venue.md is absent.

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
