
## 0.1.2 · 2026-08-31

Remove the retired Task-plugin name from the live comparison vocabulary;
meetings now compare only with PageX and Skill attachments.

## 0.1.1 · 2026-08-31

LEAVING banner: meetings move to project/SPACE level, parsed into
affected pages' outline/; lane stops minting on pages.

Historical Page meeting lineage
===============================

Skill-scoped changelog (never loaded at invocation). Versions match SKILL.md frontmatter `version:`. Newest first.

## 0.1.0 - 2026-08-18

- Born from JL's ask on the QPf14 design round ("meeting: what communication
  is related to this page"), alongside task/'s haipipe-plugin-task. The
  roster row had stood 📋 declared since 260815 with no skill and no writer;
  this round asked whether it should point at the separate `Meeting-<n>`
  page type instead, JL ruled STANDALONE (§⚖️), and the shape shipped
  exactly as the row already named it: `live/meeting.py`, the drawer entry,
  and the roster row went 🟢 in the same round.
## 1.0.0 · 2026-09-04

- Move meeting ownership from a Page plugin to an on-demand project/SPACE
  `meetings/` lane.
- Route each decision into the affected Page Outline or Task Folder while the
  meeting record remains at its true shared owner.
- Retire the Page-local writer; existing Page meeting folders are read-only
  migration input.
