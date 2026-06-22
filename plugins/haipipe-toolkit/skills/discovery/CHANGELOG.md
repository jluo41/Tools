discovery — Changelog
=====================

Layer-scoped changelog for the discovery (external-evidence) layer. Newest
first. Rollup lives in the plugin-level `CHANGELOG.md`. Per-skill version
history also lives in each `SKILL.md` frontmatter `changelog:`.


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
- **`ref/lifecycle-map.md`** — the canonical verb-based lifecycle table
  (Status / Open / Search / Read / Review / Verdict / Post), isomorphic to the
  probe lifecycle map: per verb, the question, action, reads, writes, external
  calls, human output, machine state, and stop gate. SKILL.md and DESIGN.md now
  point here instead of restating the per-verb columns (the lifecycle had been
  written in two places; it now has one home).
- This `CHANGELOG.md`, for parity with the task / probe / insight / project
  layers (discovery previously tracked history only in SKILL.md frontmatter and
  the DESIGN.md Decision Log).
