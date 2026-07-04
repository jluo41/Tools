haipipe-paper — Changelog
=========================

Skill-scoped changelog (never loaded at invocation; read on demand). Versions match SKILL.md frontmatter `version:`. Newest first. Rollup: layer-level `paper/CHANGELOG.md`.


## [2.2.0] — 2026-07-03

- JL in-file comment round applied (> JL: / > CC: threads kept in SKILL.md): (1) retired write/edit/polish/draft alias words entirely (省得误导); (2) closing block now TWO-LINE focus strip (stage + phase) with the simplified tail (status·stage merged, paper_root dropped, next only); (3) wiki/01-focus-strip-markers ABSORBED into the Closing Block section as the single source of truth (file deleted; enter skill + 10-stage-strip.sh + wiki README repointed; wiki numbering gap kept); (4) umbrella no longer calls /haipipe-probe directly -- probe run hands 1-probe-plans/ to haipipe-paper-probe (the PROBE phase worker inside a stage's phase), composing diagram + dispatch note + description updated; (5) gate-aware line now names the two approval modes (copilot human / autopilot reviewer subagent), full design pending JL confirm (wiki/08 + check skill).

## [2.1.0] — 2026-07-03

- Dedup rewrite (JL: "会有比较重复的地方吗", same treatment as discovery 2.6.0): say each thing ONCE. Command table + keyword map + positional aliases + Routing Step 2 (the same dispatch stated 4 times) merged into one Verbs block + one 6-rule Routing pass; feedback/digest full spec (written twice + fn/) reduced to one pointer section; create recipe (written twice + owner fn) reduced to one dispatch note; probe/venue-coupling/folder-tree/skill-tree restatements replaced by pointers to their owners (fn/probe-plans.md, wiki/03, paper-folder-anatomy.md, wiki/06). ~545 -> ~200 lines.
- Stale fixes swept in: 2-claims -> 1-claims backfill refs; 3-narrative.tex -> .md; phantom top-level 2-section-edit/ dir removed from the skill tree (real homes: 1-lifecycle/5-section-edit + 2-phase/); write/edit rerouted to section-edit (old targets haipipe-paper-edit-write/-weaving no longer exist); stage list gained section-edit; "phase skills" wording corrected to stage skills (DPRC phases are internal); retired upstream workflow names dropped from the composing diagram.
- Three open questions embedded as > CC: markers for JL review (write/edit verb fate, retired upstream workflow names, dropped display-figure reference).

## [2.0.2] — 2026-07-03

- create verb added to the front door (JL: should be /haipipe-paper create, not a sub-skill invocation): routes to haipipe-paper-lifecycle folder; repo-backed inside Project-* repos per project/haipipe-project/fn/repo-project.md papers-inside recipe; --org resolved per invocation (paper owner may differ from project owner). Retired prospectus verb/aliases removed (seed replaced it); haipipe-paper-bootstrap specialist entry replaced by haipipe-paper-folder; paper-folder contract tree fixed to current spine (1-claims, 2-pitch, 5-section-edit, .md early stages).

## [2.0.1] — 2026-07-03

- phase spine renamed DGPC -> DPRC (GATHER -> PROBE, POLISH -> REVISE; phase workers probe/ and revise/).

## [2.0.0] — 2026-06-22

- cross-cutting protocol wiring. All stage skills now reference ../wiki/08-stage-gate.md (confirm-before-advance), ../wiki/09-stage-illuminate.md (Socratic taste elicitation), ../wiki/13-tex-quality.md (self-contained compilable tex), ../wiki/12-evidence-routing.md (\needprobe macro + probe handoff). Stage strip end-of-reply convention enforced. Enter dashboard restructured (pitch summary first). 22 feedback items addressed.

## [1.5.0] — 2026-06-22

- probe buffer (1-probe-plans/). Claim-related evidence needs accumulate as probe plans during lifecycle work, then batch-dispatch to /haipipe-probe. Probe is the universal evidence gateway for claims; it calls task/discover during Gather. Direct task/discover verbs kept for non-claim utility work. See fn/probe-plans.md.

## [1.4.0] — 2026-06-22

- added probe/discover/task verbs as evidence-worker dispatchers. Paper orchestrator can now route directly to /haipipe-probe, /haipipe-discovery, /haipipe-task with project context resolved from the paper path. Paper stays story layer; evidence workers do the work.

## [1.3.0] — 2026-06-21

- renamed paper working-memory layer from feedback to rounds; added lifecycle, rounds, and skill-structure references.

## [1.2.0] — 2026-06-21

- made paper lifecycle the delivery-side owner of story/claims and routed GAP/NEED items through the shared delivery-need interface.

## [1.1.0] — 2026-06-21

- added enter/status paper-session loader routing.

## [1.0.0] — 2026-05-31

- baseline metadata added.
