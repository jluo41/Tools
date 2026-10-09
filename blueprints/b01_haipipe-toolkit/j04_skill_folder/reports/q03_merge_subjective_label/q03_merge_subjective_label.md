# q03_merge_subjective_label

answer-status: open

Answer
======

`plugins/subjective-label` is now the labeling theme of haipipe-toolkit, moved with plain `mv`
on 2026-10-07 to the layout JL agreed:

```text
plugins/subjective-label/                ->  plugins/haipipe-toolkit/
├── skills/<19 skills>                   ->  skills/2_theme/labeling/<skill>/
├── engine/                              ->  skills/2_theme/labeling/engine/
├── diagram/ README.md CORPUS-PREPARATION.md -> skills/2_theme/labeling/
├── agents/<9>.md                        ->  agents/   (names kept)
├── servers/workbench-labeling/          ->  servers/workbench-labeling/
├── servers/README.md                    ->  servers/workbench-labeling/README.md
├── servers/_host/serve.py               ->  dropped: servers/_host/serve.py --only labeling
└── .claude-plugin/plugin.json           ->  removed
```

The labeling workbench is no longer optional. The host imports `live.labeling` directly; the
404 stand-in for "labeling workbench not installed" is gone. The annotator-only host is the
toolkit host with `--only labeling`: its own port and auth, no terminal, no chat, no Board
writes. When `--only labeling` is given without `--space-name`, the SPACE name defaults to
`Labeling`, as the dropped wrapper did.
Drawing: [s01 skill folder changes](../../studio/s01-skill-folder-changes/s01-skill-folder-changes.excalidraw), the folders before and after, read from git and disk.



What changed
============

Code:
- `servers/workbench-labeling/labeling.py`: the engine is found with
  `host_paths.skill_dir("labeling") / "engine"`, replacing the walk up to a sibling
  `subjective-label/`. The space-mapping ref is read at `labeling/label-building/ref/`.
- `servers/haipipe-page/standalone_server.py`: the Page plugin presenter is
  `skill_dir("labeling") / "engine" / "page_plugin.py"`.
- `servers/_host/serve.py`: unconditional `LabelingMixin`, new `--only` help text, and the
  `Labeling` SPACE name default. `servers/_host/live/__init__.py` docstring updated.
- `servers/workbench/guide_families.py`: the LABELING entries use `at("workbench-labeling")`,
  `at("label-building", ...)` and `at("label-scanning", ...)`. The sentence "available only
  when the subjective-label plugin is installed" is dropped.
- Engine tests `test_run_contract.py` and `test_preparation_workbench.py`: their roots are found
  by the `skills` folder name; the `skills/` level inside the old plugin is gone.
- Toolkit tests: `test_labeling.py` (the drawer JS and the skill root),
  `_host/tests/test_workbench_short.py` (now checks the toolkit `serve.py --only labeling`),
  and `_host/tests/test_workbench_conformance.py` (the labeling presenter must exist).

Packaging:
- `Tools/.claude-plugin/marketplace.json`: the `subjective-label` entry is removed and
  haipipe is 0.4.0, its description now naming subjective labeling.
- `plugins/haipipe-toolkit/.claude-plugin/plugin.json`: version 0.3.0 -> 0.4.0.
- `Tools/README.md`: the package row is removed, the haipipe row links the labeling README,
  and the table now covers "three package directories".
- `Tools/install.sh`: the install hint names `inlab-human`.

Markdown and written paths: 56 `plugins/subjective-label/...` paths and 6 relative links were
rewritten, each mapped through the table above. A few were edited by hand: the toolkit
`servers/README.md` (tree, table rows, rule 4), the moved `workbench-labeling/README.md` (header,
dependency notes, the Runs panel at `servers/workbench/task/runs_panel.py`), the labeling
README's contents tree, the `standalone.md` and haipipe-page `SKILL.md` lines that said
"optional", the b03 studio s03/s04/s05 notes, and the b02 `build_s01_workbench_shared.py`
`LABELING` path. Schema ids (`subjective-label/v2`, ...) and skill names are identifiers and
stay as they are.


Checks
======

- Engine tests: 147 passed, 2 failed. One needs `fixtures/job-mini/test/sealed/status.json`
  (see Limits). The other is `test_prepared_page_is_discovered_before_contract_and_has_live_runs`,
  which fails on the Workbench's Page-URL check ("requires the matching generated Page URL"),
  not on a path.
- `skills/1_base/page/haipipe-page/tests/test_labeling.py` plus `servers/_host/tests`:
  96 passed, 1 skipped. `_host/tests` alone: 41 passed.
- `serve.py --only labeling` on a temporary Board with one Page-local `labeling/` job:
  `/_board/labeling-board`, `/_board/labeling` and `/workbench/labeling` return 200;
  `/_board/terms`, `/_board/chat`, `/_shell` and `/_board/write` return 404.
- Full host, same Board: `/_board/labeling-board` and `/_board/labeling` return 200.
  `/workbench/labeling` returns 400 there, by design, because it is a dedicated-host route.
- guide_families.FAMILIES: 90 paths, 0 missing.
- Reinstall (`Tools/install.sh --no-marketplace --project <SPACE>`): 186 skills, 30 agents,
  0 dangling. All 19 labeling skills now link into `skills/2_theme/labeling/`, and the 9
  agents (moderator-agent, sampler-agent, ...) into `plugins/haipipe-toolkit/agents/`.
  A restart loads them.
- Final grep for `plugins/subjective-label` and `subjective-label/(skills|servers|engine|agents)`:
  only history is left (this Block's HANDOFF.md and its q03 question text, the q02 report, and a
  dated "checked 261006 in ..." comment in b03 `level_views.py`).
- Whole live tree: _host 41 · workbench-task (now workbench-work) 20 · cowork 8 · discovery 4 passed;
  servers/haipipe-page 34 passed, 5 failed; haipipe-page-workflow 17 passed, 6 failed;
  skills/1_base/page/haipipe-page 906 passed, 11 failed. None of these failures is a path or
  import error (see q02).


Later the same day (JL 261007)
==============================

- The door was renamed to the shape every theme uses: `skills/2_theme/labeling/subjective-label`
  is now `skills/2_theme/labeling/haipipe-labeling` (v0.10.0; its description names the old name).
  `workbench-labeling` moved up from `label-building-workflow/` to `skills/2_theme/labeling/workbench-labeling`.
  38 toolkit files were rewritten (`/subjective-label` -> `/haipipe-labeling`, paths, relative links);
  the receipt `domain` id, the schema ids, the 13 `subjective-label-<view>` skills, CHANGELOGs and the
  dated feedback record keep their names. Checks: engine 147 passed, 2 failed (the same two);
  test_labeling 55 passed; `_host` 47 passed; reinstall removed the stale `subjective-label` link.
- Both installers now skip any folder whose name starts with `_` (one rule, no layer path).


Limits
======

- `fixtures/job-mini/` (2 tracked files, a sealed-test status and manifest) had been deleted from
  the working tree before the move: `git status` already showed them as `D`. They were not
  restored. If they should exist, they belong at `skills/2_theme/labeling/fixtures/job-mini/`
  (`git -C Tools show HEAD:plugins/subjective-label/fixtures/...`).
- The Tools git index still has `plugins/subjective-label/`, because the move was a plain `mv`.
  It shows as deletions plus untracked folders until it is staged.
- Agent names are kept. Generic names (moderator-agent, sampler-agent, validator-agent, ...)
  may be renamed `labeling-...-agent` later.
- A machine that installed `subjective-label@jluo41-tools` from the marketplace keeps a stale
  plugin until it is uninstalled. The labeling skills now come with `haipipe`.
- The b02 drawing builder still labels the folder "(subjective-label)"; that drawing's content
  is b02's to update.


Next
====

- JL: decide whether to restore `fixtures/job-mini`, and whether to rename the generic
  labeling agents.
- q01: write down the layers.
