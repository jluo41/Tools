# Haipipe skill-size audit

Date: 2026-09-21. Scope: active skills under
`plugins/haipipe-toolkit/skills/`. The installer excludes `_todo`, `_archive`,
`_old`, and `_paper-writing-backup`; this audit excludes those paths too.

## Measurement method

- **Lines** are physical Markdown lines.
- **Words** are whitespace-separated tokens, matching `wc -w` closely.
- **Entry point** means an active `SKILL.md`.
- **Full Markdown** includes references, functions, venue records, feedback,
  pages, and changelogs, whether or not a normal invocation loads them.
- The thresholds below are review heuristics derived from the skill-creator
  rule that entrypoints should stay concise and move conditional detail into
  supporting references. They are not repository build limits.

| Status | Entry-point heuristic | Meaning |
|---|---:|---|
| GREEN | ≤300 lines and ≤3,000 words | Concise enough for ordinary loading |
| AMBER | 301–500 lines or 3,001–5,000 words | Review for routing/detail separation |
| RED | >500 lines or >5,000 words | Strong split candidate; likely context-heavy |

## Inventory status

| Scope | Files | Lines | Words | Status |
|---|---:|---:|---:|---|
| Active `SKILL.md` entrypoints | 137 | 32,448 | 219,457 | **AMBER** as an inventory; acceptable only with lazy loading |
| Excluded `SKILL.md` files | 4 | — | — | Excluded by installer |
| Active Markdown, all supporting content | 1,014 | 169,094 | 1,465,872 | **RED** as a full tree; not a single prompt |
| Active Markdown excluding changelogs, feedback, pages, and venue records | 498 | 83,620 | 533,454 | **RED** as a documentation corpus |

The entrypoint distribution is concentrated rather than uniformly large:

| Entrypoint status | Count | Share |
|---|---:|---:|
| GREEN | 104 | 75.9% |
| AMBER | 25 | 18.2% |
| RED | 8 | 5.8% |

## Family status

| Family | Entrypoints | Lines | Words | Status |
|---|---:|---:|---:|---|
| Page | 15 | 6,000 | 50,345 | **RED aggregate**; routing and workflow entrypoints need trimming |
| Paper | 9 | 3,843 | 29,320 | **AMBER aggregate**; several core entrypoints are individually large |
| Task | 49 | 8,388 | 42,101 | **AMBER aggregate**; broad catalog, mostly smaller workers |
| Discovery | 16 | 3,346 | 20,546 | **AMBER aggregate** |
| Display | 10 | 2,339 | 16,419 | **GREEN/AMBER aggregate** |
| Writing | 1 | 442 | 3,547 | **AMBER** |
| Remaining families | 37 | 8,090 | 47,179 | **AMBER aggregate** |

## Largest active entrypoints

| File | Lines | Words | Status |
|---|---:|---:|---|
| `page/haipipe-page/SKILL.md` | 970 | 8,030 | **RED** |
| `page/page-workflows/haipipe-page-outline/SKILL.md` | 775 | 7,136 | **RED** |
| `page/haipipe-workbench-page/SKILL.md` | 697 | 6,173 | **RED** |
| `page/page-workflows/haipipe-page-workflow/SKILL.md` | 623 | 4,698 | **RED** |
| `design/haipipe-workbench-design/SKILL.md` | 598 | 5,820 | **RED** |
| `paper/haipipe-paper-assemble/SKILL.md` | 555 | 4,089 | **RED** |
| `paper/haipipe-paper/SKILL.md` | 530 | 4,242 | **RED** |
| `paper/workflow-phases/haipipe-paper-ideation/SKILL.md` | 525 | 4,291 | **RED** |
| `page/page-workflows/haipipe-page-check/SKILL.md` | 388 | 3,078 | **AMBER** |
| `paper/haipipe-paper-workflow/SKILL.md` | 245 | 2,002 | **GREEN** |

## Paper/Page route-load risk

If every file in the common Paper/Page route is loaded at once—Paper router,
Page router, Page workflow/check, Paper workflow/Section/assembly, and Writing—
the entrypoint total is **4,152 lines and 32,498 words**. That is **RED** as a
single context. The route is workable when each skill loads only the exact
supporting reference needed for the current operation.

The current design therefore has a **progressive-disclosure success but an
entrypoint-size failure**: the repository is organized into many skills, yet
the Page root and several workflow contracts still carry too much conditional
detail in `SKILL.md`.

## Recommended action

1. Split `haipipe-page/SKILL.md` first. Keep routing, authority, boundaries,
   and the short lifecycle in the entrypoint; move delivery/UI details,
   file-shape tables, historical compatibility and long examples into refs.
2. Split `haipipe-page-outline`, `haipipe-page-workflow`, and
   `haipipe-workbench-page` next. These are the largest repeated Page context
   sources.
3. Split `haipipe-paper` and `haipipe-paper-assemble` after Page. Keep Paper
   routing and G0–G5 ownership in `SKILL.md`; move build mechanics, venue
   profiles and detailed receipt schemas into references.
4. Keep the 21-point submission overlay as a reference, where it is already
   located. Do not copy its 21 rows into every Page or Writing entrypoint.
5. Do not install the full external NatureSkills collection into the core
   context. Treat selected NatureSkills as optional workers behind existing
   Paper/Page owners.

No source skills were changed by this audit.
