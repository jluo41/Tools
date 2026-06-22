discovery — Changelog
=====================

Layer-scoped changelog for the discovery (external-evidence) layer. Newest
first. Rollup lives in the plugin-level `CHANGELOG.md`. Per-skill version
history also lives in each `SKILL.md` frontmatter `changelog:`.


## [2.0.0] — 2026-06-22

### Changed (TWO-AXIS redesign, mirrors task)
- **Lifecycle is now the uniform `Plan -> Build(opt) -> Execute -> Report`.** Retires the
  old `open -> search -> read -> review -> post` verb-lifecycle. Build is optional (only
  for a systematic query string / extraction schema). One execution per folder (no `runs/`
  multiplicity, unlike task).
- **`search/read/review/idea` are no longer stage verbs — they are the capability buckets
  (Execute-stage workers).** The folder TYPE is one of 3 Chinese-char types:
  - `搜` source = search + read merged -> `sources.md` + `notes.md` (a reusable, accumulating source base).
  - `析` analyze = judge + synthesize merged -> `verdict.md` (判, role prior_art/counter/novelty -> probe)
    or `landscape.md` (综, role landscape/benchmark -> paper); `role:` picks the branch.
  - `创` idea -> `ideas.md` (-> probe-open / paper-seed).
- **`verdict:` block renamed to `report:`** (report-to-human; generalized across types).
- **New terminal files** `landscape.md` + `ideas.md` alongside `verdict.md`.
- Workers (4 buckets) and types (3) are different axes; per-type specialist skills are NOT created.
- Old folders (`role:` + `verdict:`, no `type:`) remain readable; treat missing `type:` as `析`.
- Updated: `SKILL.md` (2.0.0), `DESIGN.md` (2.0.0), `ref/lifecycle-map.md`,
  `ref/discovery-yaml-schema.md`, and the minimal-dry-run fixture.


## [Unreleased] — 2026-06-21

### Changed
- **Skill renamed `haipipe-discover` -> `haipipe-discovery` (1.8.0).** Matches the
  haipipe-<noun> sibling convention (probe/paper/task/insight/project/application);
  the verb-named skill was the lone exception. Inner folder `haipipe-discovery/`,
  the `.claude` symlink, the command `/haipipe-discovery`, and all in-repo refs
  updated.
- **Discovery is a FOLDER, not a single file (reverted v1.5).** A discovery is
  one research topic = its own folder (`discovery.yaml` + `sources.md` /
  `notes.md` / `verdict.md` + `status.yaml` / `site.md`), mirroring a
  task-folder; sources/notes/verdict are its `results/`. The dry-run fixture and
  blueprint already used folders; v1.5's single-file default never landed.
  `ref/lifecycle-map.md` recast as `open -> search -> read -> review/idea -> post`,
  each stage filling one IO file (no separate `verdict` verb; review writes
  `verdict.md`). SKILL.md / DESIGN.md / discovery-yaml-schema.md flipped to
  match. Version 1.7.0.
- **Folder renamed `discover/` to `discovery/`.** The layer concept now reads as
  a noun, matching the `discoveries/` artifact dir and the task/probe/insight
  sibling layers. (The skill itself was renamed too, see above.) Cross-reference
  path fixups in `STRUCTURE.md`, the blueprint, and the plugin CHANGELOG are a
  follow-up.
- **Narrative layer retired across discovery docs.** A discovery now has exactly
  two parents: a delivery lifecycle (`paper` / `application`) for L* landscape /
  novelty work, and a `probe` for claim-level evidence. The story-side dispatch
  that used to come from `Narrative-open` now comes from `Delivery-open`. Updated
  DESIGN.md (layer table, project tree, combine-with-probe section, boundary
  rules), SKILL.md, and `ref/discovery-yaml-schema.md`.

### Added
- **`feedback/` inbox + `feedback` utility verb (1.9.0, mirrors probe).**
  `/haipipe-discovery feedback "<text>"` captures a complaint/confusion/wish about
  the skill into `feedback/<date>_<slug>.md` (capture-only); `feedback list`
  reviews open items. Fixing is a separate revision pass, so users can improve the
  skill as they use it.
- **`ref/lifecycle-map.md`** — the canonical verb-based lifecycle table
  (Status / Open / Search / Read / Review / Verdict / Post), isomorphic to the
  probe lifecycle map: per verb, the question, action, reads, writes, external
  calls, human output, machine state, and stop gate. SKILL.md and DESIGN.md now
  point here instead of restating the per-verb columns (the lifecycle had been
  written in two places; it now has one home).
- This `CHANGELOG.md`, for parity with the task / probe / insight / project
  layers (discovery previously tracked history only in SKILL.md frontmatter and
  the DESIGN.md Decision Log).
