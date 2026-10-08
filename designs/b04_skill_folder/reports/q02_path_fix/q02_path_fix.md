# q02_path_fix

answer-status: open

Answer
======

The paths broken by the skills/ regroup into `0_utils · 1_base · 2_theme` fell into seven
kinds. All seven are fixed in code, tests and Markdown, and the checks below pass in the live
tree. During the work `servers/workbench-page` went to `servers/_backup/` (JL's merge) and
came back as `servers/workbench/task`; the b02 session repointed its references.

Code now finds the skills by name, not by counting folders:

- `Tools/plugins/haipipe-toolkit/servers/_host/host_paths.py` has `skill_dir(name)`. It searches
  `skills/` for a skill or family folder by its name, nearest first, so the next layer move
  breaks no server path. `PAGE_ENGINE` is `skill_dir("haipipe-page")`.
- `Tools/plugins/haipipe-toolkit/skills/1_base/page/haipipe-page/src/skill_paths.py` (new)
  does the same for the Page engine: `SKILLS` (the folder named `skills` above the file),
  `skill_dir`, and `in_skills(rel)`, which also resolves a path written before the layers
  (`paper/venue/...`).
- Skill code reaches the skills root as
  `next(p for p in Path(__file__).resolve().parents if p.name == "skills")` instead of
  `parents[N]`.

Drawing: [s01 skill folder changes](../../studio/s01-skill-folder-changes/s01-skill-folder-changes.excalidraw), the folders before and after, read from git and disk.

Drawing: [s03 path lookup](../../studio/s03-path-lookup/s03-path-lookup.excalidraw), read from disk; open points in red.


What broke, and the fix
=======================

1. Fixed paths in server code (`SKILLS / "design" / ...`, `TOOLKIT + "skills/task/..."`,
   `parents[2] / "skills/question/..."`): changed to `skill_dir("<skill>")`.
   `guide_families.py` now writes `skill("<skill>", role)` and `at("<skill>", "ref/...")`;
   all 91 of its paths are checked.
2. Depth-based paths in skill code (`parents[3]`, `ENGINE.parents[1]`, `.parent.parent`,
   inline `X.parents[2] / "servers"`) that reached the skills root, the toolkit or
   `servers/_host`: changed to the name anchor.
3. Globs over the skills root (`skills_root.glob("*/haipipe-*/SKILL.md")`, folder-kinds
   discovery): now one level deeper (`*/*/...`). `structure-source:` values written before the
   layers still resolve (`plan_shape._resolve_source`, `check.py`, `requirement.py`).
4. Written paths `skills/<family>/` and `<skills>/<family>/` in code strings and Markdown:
   210 rewritten with their layer. Examples: AGENTS.md rule 8 (`page.py export`), the
   AGENTS.md Skills section, the `page.py export` run script that `src/page_export.py`
   writes, and the 40-permissions.js prompt.
5. Bare skills-rooted tokens in backticks (`page/haipipe-page/ref/x.md`): 39 rewritten as
   `1_base/page/...`. `haipipe-writing/cli/agree.py` now accepts `1_base` and `2_theme` as
   heads, so it can check them.
6. Relative links, both `[x](../..)` and backticked `../../x.md`: 105 rewritten, each resolved
   from the file's location before the move and mapped forward. Toolkit `agents/*.md` are
   symlinks into the skills, so each was fixed in its real file.
7. The paper `venue` submodule: its `.git` file, the module's `core.worktree` and
   `Tools/.gitmodules` `path =` now point at `skills/2_theme/paper/venue`.
   `git -C .../venue status` works again.

Tests changed to the layout: `test_interactive_skill_contract.py` (its entry-point list, and
its expected `../haipipe-page/fn/runs.md`, which now resolves), `test_folder_contract.py` (its
skills root and its temporary fixture tree), and `test_aims_state.py`. `skills/README.md` has a
new section, "The three layers".


Checks
======

- ast-parse: 415 Python files under the toolkit, inlab-human and b03 studio, 0 errors.
- pytest (first on a scratch copy while the Page presenters were in `_backup`, then in the live tree):
  `servers/_host/tests` 41 passed · `workbench-task/tests` (now `workbench-work/tests`) 20 passed ·
  `workbench-cowork/tests` 8 passed · `workbench-discovery/tests` 4 passed ·
  `servers/haipipe-page/tests` 34 passed, 5 failed (standalone-server HTML and status
  assertions, no path) · `haipipe-page-workflow/tests` 17 passed, 5 failed (the haipipe-run
  SKILL.md text no longer has `Closed records` and `run-structure-`; `docs/page-writing-philosophy.md`
  exists nowhere) · `skills/1_base/page/haipipe-page/tests` 905 passed, 10 failed (baseline
  before the move: 11). The 10 are folder-kind SKILL.md content (missing sections and outline
  blocks), insight register settlement in the design fixtures, and one Insight definition
  example. None is a missing path.
- Live tree after the b02 merge: _host 41 · workbench-task (now workbench-work) 20 · cowork 8 · discovery 4 passed;
  servers/haipipe-page 34 passed, 5 failed; haipipe-page-workflow 17 passed, 6 failed;
  skills/1_base/page/haipipe-page 906 passed, 11 failed. The extra one,
  `test_real_a00_board`, compares a cell mark on a real Insight Board: content, not a path.
- guide_families.FAMILIES: 90 paths, 0 missing.
- Link checker over skills, servers, agents, the toolkit README, `Tools/README.md`,
  `Tools/AGENTS.md` and `AGENTS.md`: 798 relative links, 60 not resolving. Of these, 23 pointed at
  `servers/workbench-page/` (b02 has since repointed them to `servers/workbench/task/`) and 37
  were already broken before the move:
  ideation's `shared-references/` from the ARIS import, `STRUCTURE.md`,
  `principle/WORKBENCH-DESIGN.md`, `haipipe-discovery-search`, and example `results/` paths.
- The final grep for `skills/(page|paper|task|...)/` returns only skipped history: a dated chat
  transcript in `servers/workbench-insight/studio/` and this Block's HANDOFF.md.
- `Tools/install.sh --no-marketplace --project <SPACE>`: 186 skills and 30 agents linked,
  1 stale link removed, 0 dangling. A restart loads them.


Limits
======

- Skipped as generated or history, per AGENTS.md rule 0: `*.excalidraw`, `.seed.json`,
  `delivery/`, `board/`, `draft/`, `records/`, `chat/` and `*.jsonl` transcripts,
  `CHANGELOG.md`, `_legacy/`, `_old/`, `_backup/`. Already exported `delivery/` run scripts
  still name `skills/page/...` until each Page is exported again.
- 44 Pages in project folders declare `structure-source:` in the old form (`paper/venue/...`, or
  `Tools/plugins/haipipe-toolkit/skills/paper/...`). The skills-relative form still resolves.
  The SPACE-rooted form did not resolve before the move either. These Pages were not edited.
- The Tools git index still has the pre-move paths, because the move was a plain `mv`. The
  regroup shows as deletions plus untracked folders until it is staged.


Next
====

- The 37 links that were already broken (listed above) need their owners.
- q03 (merge plugins/subjective-label) is done; see its report. q01 writes down the layers.
