haipipe-individual — Changelog
==============================

Skill-scoped changelog (never loaded at invocation; read on demand).
Versions match SKILL.md frontmatter `version:`.
Newest first.


## [0.1.2] - 2026-09-28 - No content hashes (JL 260928)

- AGENTS.md rule 9: `manifest.yaml` drops `input_fingerprint` and `fingerprint_method`. `fn/build_sample_individuals.py` reuses a cache only when `build_spec` matches, no input (builder, Source/Rec sets, raw paths; file and folder times) is newer than `inputs_read_at`, and the output inventory matches. A manifest from the older builder rebuilds once.

## [0.1.1] — 2026-07-24

Renumbered under the 0.x policy — the whole haipipe-toolkit is pre-1.0 until JL says otherwise (was 1.1.0; older entries below keep their original numbers).

## [1.1.0] — 2026-07-04

- folder-name contract made self-consistent: child = Subject-{id}, dataset tag on the parent UserGroup folder, matching the Naming Convention + shipped builder (3 stale Subject-{DatasetTag}-{id} lines fixed, C2); Sub-skills routing section added for the inference chain (C7); build steps 3-4 now write the FLAT layout per the flattening rules (E3); builder script no longer marked 'planned'; typos.

## [1.0.0] — 2026-05-31

- baseline metadata added.
