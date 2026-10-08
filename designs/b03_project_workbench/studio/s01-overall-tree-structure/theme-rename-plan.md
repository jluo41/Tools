Theme rename plan: `tasks/` → `work/`, every Theme singular
=============================================================

decided: s01-D28 (the work Theme), s01-D29 (every Theme folder singular), JL 261007
status: phase 1 done in the working tree (261007, not yet committed); no folder moved yet


The map
-------

```text
tasks/        →  work/
discoveries/  →  discovery/
cowork/          cowork/        (unchanged)
papers/       →  paper/
insights/     →  insight/
designs/      →  design/
labelings/    →  labeling/
```

The level keeps its name: a `tNN_<task>/` folder is a Task in every Theme.


What it touches (counted 261007)
--------------------------------

```text
Tools skills and servers   ~330 files name a Theme folder (docs, refs, code, tests)
                           ~240 code or test lines build a Theme path as a string
  where the Theme list lives today:
    servers/space-home/home.py                    THEMES, THEME_KIND
    skills/1_base/project/haipipe-project/scripts/ladder.py   LADDER_WORLDS
    skills/1_base/page/haipipe-page/src/common.py, dialect_paper.py
    skills/2_theme/discovery/haipipe-discovery/scripts (3 files), servers/workbench-* (8)
Projects on disk           DrFirst-SPACE 24 Theme folders in 12 project repos (submodules)
                           WellDoc-SPACE 19, Physician-SPACE 5 (each has its own Tools)
Run tickets (.sh)          752 in DrFirst-SPACE name a Theme path: source, edited with the move
Receipts and notebooks     1249 (runtime.yaml, executed .ipynb): generated, never hand-edited
SPACE docs                 AGENTS.md (rule 3's builder path), README.md
code/ submodule            4 files outside code/haifn/; code/haifn/ is rebuilt, never edited
```

Unaffected: `_WorkSpace/` and `ProjectResult/` (no Theme level in their paths).

Not a Theme folder, and so left alone by every replace:
- `ref/papers/` (a workbench's open-licensed PDFs)
- the Design workbench's `papers` and `designs` views
- "tasks" meaning Task folders (`run-plan-tasks/`, "its Tasks")
- CHANGELOG entries (history) and `_legacy/`


Rules the move keeps
--------------------

1. A generated file is never changed by hand (AGENTS rule 0). Receipts and executed notebooks
   keep the old path as a record of the run; they are refreshed only when their ticket reruns.
   Readers resolve an old recorded path through the alias in phase 1.
2. Tools is shared by three SPACEs. Tools reads both names until every SPACE has moved, so
   a pull never breaks a SPACE whose projects still use the old folders.
3. One project repo per commit, all its Themes at once (`git mv`), its tickets and configs in
   the same commit. Before a push, the env.sh secrets rule (AGENTS rule 6) applies.
4. No relative path may turn absolute (AGENTS rule 7).


Phases
------

**0 · Settle.** Other sessions are reshaping Tools now (`skills/2_theme/`,
`servers/workbench-work/`, ~1900 uncommitted changes). Wait until that is committed, so the
rename lands on a clean tree.

**1 · One Theme table, both names (Tools).** Add one module, owned by haipipe-project, that
lists each Theme: kind, folder, and its old folder as an alias. Every place above reads it
instead of its own list. Path lookups try the new folder, then the alias. Tests move to the
new names, plus one test that an old-layout project still opens. Ship Tools.
Check: the haipipe-page and server tests pass; `audit_projects.py` and the workbench open
one old-layout and one new-layout project.

Done 261007: the table is `skills/1_base/page/haipipe-page/src/themes.py` (kind · folder · old
folder; `theme_dir`, `theme_dirs`, `kind_of`). Read through it: space-home `home.py`, haipipe-page
`common.py`, `dialect_paper.py`, `item_table.py`, and the workbench servers (discovery, design,
work, insight, paper, `workbench/related_papers.py`). Standalone scripts carry the same pairs
inline: haipipe-project `ladder.py`, haipipe-task `check_task_tree.py` (S16 checks `work/` or
`tasks/` paths by the name they use), haipipe-data `space_check.py`, haipipe-discovery
`regroup_bjtr.py` and `migrate_bjtr.py`. The work Theme's kind stays `task` (folder-kind,
board-kind `task-block`, the kind filter) until the kind is renamed on its own. Tests:
`tests/test_themes.py` (both layouts); the page and host suites keep their 11 known failures.
Not yet: Tools is not committed (the reshaping around it is still open), and two projects
already have a singular `paper/`, now read as the new name.

**2 · Words (Tools).** Replace the Theme folder names in SKILL.md and ref files, minus the
exclusions above; bump each touched skill's version and CHANGELOG. haipipe-project's audit
reports an old Theme folder as "rename pending", not an error.
Check: `git grep` finds the old names only in CHANGELOGs, `_legacy/` and the alias table.

**3 · Move DrFirst-SPACE, one project at a time.** In each project repo: `git mv` its Theme
folders, update its run tickets and configs, rebuild anything generated from a moved
builder (`code/haifn/` from its builder, per AGENTS rule 3), and run one ticket per Block as
a smoke test. Then the SPACE's own AGENTS.md path, README and workspace files.
Order: smallest first (labeling, design), Raw2AIData last (its builders feed `code/haifn/`).
Check per project: the audit is clean, the workbench opens every Block, and one rerun ticket
writes its receipt under the new path.

**4 · WellDoc-SPACE and Physician-SPACE.** The same per-project move after they pull Tools.

**5 · Drop the alias.** Once no SPACE has an old Theme folder: remove the alias, and the
audit then flags an old name as an error.


Open
----

1. Do Page evidence bindings and paper Boards store a Result by path? If so, the binding
   reader resolves the alias (phase 1), or the bindings are re-bound by their Runs (phase 3).
2. A Page folder's own `labeling/` lane shares the Theme's new name at another depth (s01-D29).
   b15 proposes to keep both names and tell them apart by depth: the Theme's parent is the
   Project, the lane's parent is a `tNN_` folder with its own `.md`. Renaming the lane would
   touch the engine, its receipts and all 26 Run types. Waiting for JL (b15 Q01, open point 6).
3. One phase-1 reader is left to b15: workbench-labeling's `_labeling_job` still checks only
   `labelings`; b15 moves it onto `themes.py` when it next builds.
