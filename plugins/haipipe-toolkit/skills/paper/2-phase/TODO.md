# 2-section-edit TODO

Logged 2026-07-02 after the skill restructure session.

## Hub SKILL.md stale after directory restructure

The hub (`haipipe-paper-section-edit/SKILL.md`) references the OLD directory layout. Needs updating to match the current numbered-phase structure:

- `gather/` → `1-gather/` (and gather skill folders dropped `haipipe-paper-` prefix)
- `polish/` → `2-polish/`
- `check/` → `3-check/` (and `proof-checker` → `checker`)
- `sections/` → `section-type/`
- `tools/` → removed (diagram skill location TBD)
- New `0-draft/` with `section-edit-draft` + write-* skills moved from polish

Specific items:
- [ ] Update the phase workers directory tree in the hub SKILL.md
- [ ] Update the relation diagram at the bottom
- [ ] Add `section-edit-draft` to the worker list (new skill in 0-draft/)
- [ ] Rename `proof-checker` → `checker` in all references
- [ ] Remove `section-edit-write` from polish (moved to 0-draft as `section-edit-draft`)
- [ ] Remove `section-edit-diagram` references (moved or removed)
- [ ] Update USAGE.md and WIRING.md to match new paths
- [ ] Update README.md directory tree (already partially done but may be stale again)
- [ ] Verify all `name:` fields match folder names for the renamed skills
- [ ] Run a cross-reference audit (same as the 5-agent audit done earlier) to catch stale refs in the new structure
