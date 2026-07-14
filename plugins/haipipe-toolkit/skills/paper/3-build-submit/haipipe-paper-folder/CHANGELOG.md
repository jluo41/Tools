haipipe-paper-folder — Changelog
================================

Skill-scoped changelog (never loaded at invocation; read on demand). Versions match SKILL.md frontmatter `version:`. Newest first. Rollup: layer-level `paper/CHANGELOG.md`.


## 4.0.1 — 2026-07-14

- "probe plans (PPNN_*.md) -> fn/probe-plans.md" -> "probe files (PPNN_<topic>.md) -> fn/probes.md" (the file was renamed).

## [3.1.0] — 2026-07-08
## 4.0.0 — 2026-07-14

- PROBE REDESIGN (Tools/plugins/haipipe-toolkit/diagram/260714-probe-qa/ v3, approved JL 2026-07-14 — R1-R18). 1-probe-plans/ -> 1-probes/ (PPNN_<topic>.md, one file per TOPIC, one SECTION per question: serves/target/state/commission/reading + ONE `## Why` per file holding the stake). Binding is by PATH: a section's `target:` points at the answering `<leaf>/QA/<n>-<slug>.md` in the bank. DELETED: `## Verdict`, the `verdicted` and `dispatched` states, `_ASK/`/`_ANS/` stubs, `answers:`, and Agent(haipipe-probe-orchestrator-agent) (the GATEWAY — archived + de-registered). A claim's STATUS now lives ONLY in 0-lifecycle/1-claims/1-claims.md. Dispatch is now DIRECT: the section's `commission:` block, VERBATIM, to Agent(haipipe-task-orchestrator-agent) / Agent(haipipe-discovery-orchestrator-agent).
- THE SCAFFOLDER NO LONGER CREATES A RETIRED FOLDER. It scaffolded `1-probe-plans/`, so every NEW paper was born in the migration-needed state — the v8 probe worker and checker look in `1-probes/` and would find nothing. Now scaffolds `1-probes/`.

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
