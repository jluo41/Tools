# Q — How many skills live under plugins/haipipe-toolkit/skills/board, where one skill = one folder containing a SKILL.md, and what are their names grouped by subdirectory?
- state:   answered
- started: 2026-08-16T01:25
- by:      haipipe-task-orchestrator-agent

## Answer

**24 skills** — 24 folders under `plugins/haipipe-toolkit/skills/board/` each
containing a `SKILL.md` file, measured by
`find <board-dir> -name SKILL.md -type f` (raw list frozen at
`results/run_scan/skill-md-paths.txt`).

Grouped by subdirectory:

**board/ root — 5**
- haipipe-board
- haipipe-board-routing
- haipipe-page
- haipipe-plugin
- haipipe-sentence

**page-plugins/ — 10**
- haipipe-plugin-bibex
- haipipe-plugin-chat
- haipipe-plugin-display
- haipipe-plugin-draw
- haipipe-plugin-folder
- haipipe-plugin-latex
- haipipe-plugin-probe
- haipipe-plugin-skill
- haipipe-plugin-slide
- haipipe-plugin-word

**page-types/ — 4**
- haipipe-page-for-design
- haipipe-page-for-meeting
- haipipe-page-for-skill
- haipipe-page-for-stage

**page-workflows/ — 5**
- haipipe-page-check
- haipipe-page-draft
- haipipe-page-probe
- haipipe-page-revise
- haipipe-page-workflow

Group tally: 5 + 10 + 4 + 5 = 24.

## Caveats

- A "skill" here is strictly a directory whose immediate contents include a
  `SKILL.md`; directories without one (e.g. `agents/`, `haipipe-board/assets/`)
  are not counted.
- Snapshot of the working tree on 2026-08-16; the tree has uncommitted
  renames (e.g. `haipipe-page-plugin` → `haipipe-plugin`), so counts against
  older commits will differ.
- Skill NAME is taken as the folder name containing the SKILL.md; frontmatter
  `name:` fields were not cross-checked.

## Not-done

- No papermill/config scaffold was built: the question is a read-only
  filesystem scan, answered by one `find` whose raw output is preserved in
  `results/run_scan/`.
- No recursive check for nested SKILL.md below a skill folder's own subtree
  (none of the 24 paths shows nesting, so none was needed).
