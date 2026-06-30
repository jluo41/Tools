---
status: fixed
created: 2026-06-29
updated: 2026-06-29
occurrences: 1
context: skill architecture redesign, venue-awareness gradient
fixed_in: "v2.1.0 (reordered lifecycle: seed→claims→pitch→narrative→display→section-edit)"
regressed: ""
---

Lifecycle reordered from seed→pitch→claims→narrative→display to seed→claims→pitch→narrative→display→section-edit.

Reason: venue-awareness should increase monotonically across the lifecycle.
- seed: venue-FREE (why this paper exists)
- claims: venue-FREE (what must be true, evidence inventory)
- pitch: venue-LIGHT (story for THIS audience)
- narrative: venue-MEDIUM (paper structure for THIS venue)
- display: venue-HEAVY (figures per THIS venue's limits)
- section-edit: venue-SPECIFIC (per-section norms)

Also: claims-before-pitch is evidence-first (know what you have before deciding how to sell it). The old pitch-before-claims order risked overclaiming.

Fix: applied to ref/paper-lifecycle.md, ref/lifecycle-map.md, ref/stage-strip.sh, README.md, STATUS.md, section-edit SKILL.md.
