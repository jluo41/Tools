
## 0.2.0 — 2026-08-21

- **Resolved source re-pointed at the QBv bank** (JL 260821): the declared
  universe `paper/venue/**/template.md` marked `section-page-template: 1` held
  ZERO files — every Section silently resolved to the generic fallback. The
  structure now comes from the QBv Venue Page's unit division matching
  `section_kind`, reached through the governing Narrative's division-1 binding
  (venue 0.3.0 made those divisions carry moves-as-slots, pack refusals,
  format values, and the language per desk unit).
- Raw pack `style.md` files stay informative and may never become
  `structure-source`; a missing unit division is raised as a gap on the QBv
  page, never filled locally.
- **Two runtime groups** (JL 260821: "we will have 1-SC-Section and
  2-SA-Appendix"): main reading order in `1-SC-main/` as `SC<NN>-<kind>`,
  appendices in `2-SA-appendix/` as `SA<NN>-<slug>`, one contract for both;
  Round moves to `3-RD-round/`.
- Frontmatter gains version, summary, and `group-token: SC | SA`.

## Unreleased — 2026-08-16

The outline this type supplies is RESOLVED, and it is now reachable in one step.

- Declares `outline: mode: resolved` and names the path:
  `paper/venue/playbook-<pack>/<venue>/<venue>-<kind>/template.md`, with a one-
  line `ls` that resolves it from the page's own two keys. Verified against five
  (venue × kind) pairs; 95 templates are on disk.
- Says what arrives: a fillable skeleton, not a description. The MISQ
  introduction hands over `### P1. Phenomenon hook`, `### P2. (optional) Deepen
  the stakes`, `### P3. What is known`, each with its paragraph budget and its
  named anti-pattern. DRAFT chooses the variant and the ¶ counts; it does not
  invent an arc.
- A `(venue × kind)` that resolves to nothing is a HOLE the venue pack owes, and
  copying a sibling section's shape is the failure this type exists to prevent.
- This type read as thinner than the others because its outline lived elsewhere.
  It is the RICHEST of the ten; only the path was missing.

haipipe-page-for-section · Changelog
====================================

Skill-scoped changelog (never loaded at invocation; read on demand). Versions match
SKILL.md frontmatter `version:`. Newest first.

**v0-series rule:** inherited from `haipipe-board`; this skill stays on `0.x.x` and
never reaches `1.0.0` without JL's explicit say-so.

## 0.1.1 - 2026-08-05

Review fixes:

- The venue-chain figure is no longer redrawn here; the section cites
  `-for-stage`'s "ONE stage reads the venue page" and adds only the unit
  grain, so the LOAD line's "restates none of that" is now true.
- Corrected: other stage pages carry a venue contract block too (S-Open-Pitch
  does); what no other stage page carries is one PER READER-ORDERED UNIT.
- The REQUIRED `page-type: section` frontmatter key is stated: the filename is
  letter for letter a stage filename (base type resolution ③).
- Plain English: "The kind is the one name that ties three things together:
  the venue division, the blueprint block, and the template."

## 0.1.0 - 2026-08-05

**Created on JL's 260805 admission** ("I want is also for-venue, for-meeting,
for-stage... and also for-section (connecting with for-venue)"), thought through
against the paper skill board and the MISQ paper board together.

- Reverses the for-main rejection with a reason, not a mood: for-main failed the
  host-agnostic name test (one family's region); for-section passes it (both the
  paper and application families run section-edit), and the `### Venue contract`
  block on the real `S-Main-3-theory` is a typed record no plain stage page has.
- Loads for-stage the way the topic types load the topic core: second-level
  variant, no restated chain rules.
