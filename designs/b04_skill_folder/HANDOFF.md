You are the session for the design Block Tools/designs/b04_skill_folder (read its board.md first). JL handed this work over from the b02 workbench session. Work in place in the SPACE (Tools is a symlink to ../Tools-SPACE); never commit, push, reset, clean or stash: the tree has many uncommitted changes from JL and other sessions. Chat replies follow /response-format. Record each Question's outcome in its report Page under reports/ (ASCII doc style, SPACE-relative paths), keep answer-status open until JL settles it.

What happened
-------------
JL regrouped plugins/haipipe-toolkit/skills/ by plain `mv` into three layers. Old -> new, relative to skills/:

  page/ -> 1_base/page/        task/ -> 1_base/task/        project/ -> 1_base/project/
  question/ -> 1_base/question/   writing/ -> 1_base/writing/   display/ -> 1_base/display/
  ideation/ -> 1_base/ideation/   search/ -> 1_base/search/
  paper/ -> 2_theme/paper/     insight/ -> 2_theme/insight/   design/ -> 2_theme/design/
  discovery/ -> 2_theme/discovery/   cowork/ -> 2_theme/cowork/   (0_utils/ unchanged)
  2_theme/labeling/ exists, empty: it is for the subjective-label merge (q03).

Three background agents started the path fix and were STOPPED part way, so some files may already be fixed and others not. Do not assume either: grep and check every hit.

q02 · path fix (do this first)
------------------------------
1. Code in servers and designs: plugins/haipipe-toolkit/servers/** (workbench-shared/guide_families.py has ~25 old paths in both `TOOLKIT + "skills/<old>/..."` and `SKILLS + "<old>/..."` forms; taskboard.py, coworkboard.py, discoveryboard.py use `parents[2] / "skills/question/..."`; insight studio scripts; tests; 40-permissions.js), plugins/inlab-human/** (`skills/task/4_individual`), Tools/designs/b03_project_workbench/studio/_build/{disk_facts,build_project_scratch}.py, and in Tools/designs/b03_project_workbench/studio/s01-overall-tree-structure/build_ladder_v4.py ONLY the `f"{TK}/<old>/..."` path strings (other sessions edit that file and level_views.py). Where code looks a skill up by family, prefer a search by skill folder name over a fixed path, so the next move does not break it.
2. Code inside skills/** (.py .sh .js .toml .yaml .json): literal old paths (`SKILLS / "page/..."`, `Tools/plugins/haipipe-toolkit/skills/page/haipipe-page/cli/page.py`, ...) and depth-based paths (`Path(__file__).resolve().parents[N]`, `.parent.parent`, `ENGINE.parents[1]`) that reach the skills root, the toolkit root or servers/_host: every skill is now one folder deeper. Prefer `next(p for p in Path(__file__).resolve().parents if p.name == "skills")` over bumping N.
3. Markdown: broken relative links in skills/**, servers/**/*.md, the toolkit README and agents, Tools/README.md, Tools/AGENTS.md (resolve each missing link from the file's pre-move location, map the target forward, rewrite relative); written old paths (`skills/page/...`); the SPACE-root AGENTS.md rule 8 (`Tools/plugins/haipipe-toolkit/skills/page/haipipe-page/cli/page.py`) and its Skills section (task/1_data/... now under 1_base/task/). Add a short section to skills/README.md describing the three layers (0_utils generic, not tied to the ladder; 1_base what every theme is built on; 2_theme one folder per theme with its haipipe-<theme> skills and workbench-<theme>).
Skip generated or history files (AGENTS.md rule 0): *.excalidraw, *.png, .seed.json, static board/ sites and _assets/board.js, delivery/ outputs, CHANGELOG.md, _legacy/, _old/. No absolute /Users/... paths in tracked files.
Checks: ast-parse edited .py; pytest (from the SPACE root: `source .venv/bin/activate && source env.sh`) for servers/_host/tests, workbench-task/tests, workbench-cowork/tests, workbench-discovery/tests, skills/1_base/page/haipipe-page/tests (11 failures were the baseline before the move), haipipe-page-workflow/tests and any tests beside changed code; a script that checks every path in guide_families.FAMILIES exists; a link checker over the Markdown; a final grep for `skills/(page|paper|task|project|question|writing|display|insight|design|discovery|cowork|ideation|search)/` returning only skipped files. Then rerun `../Tools-SPACE/install.sh --no-marketplace --project "$(pwd)"` from the SPACE root so the skill links follow (tell JL a restart loads them).

q03 · merge plugins/subjective-label into haipipe-toolkit (after q02 passes)
------------------------------------------------------------------------------
subjective-label already depends on the toolkit (its servers/_host/serve.py only runs the toolkit host with `--only labeling`), and the toolkit host, space-home/home.py, workbench-shared/guide_families.py, haipipe-page/standalone_server.py and some tests name plugins/subjective-label. Plan JL agreed:
  skills/ (19 skills)            -> skills/2_theme/labeling/   (workbench-labeling inside)
  agents/ (9)                    -> plugins/haipipe-toolkit/agents/   (keep names for now; note that generic names like moderator-agent may be renamed labeling-...-agent later)
  engine/ + fixtures/            -> skills/2_theme/labeling/engine/ and .../fixtures/
  servers/workbench-labeling/    -> plugins/haipipe-toolkit/servers/workbench-labeling/
  servers/_host/serve.py         -> dropped; document `plugins/haipipe-toolkit/servers/_host/serve.py --only labeling` as the annotator-only host (own port and auth, no terminal, chat or Board writes)
  diagram/, README.md, CORPUS-PREPARATION.md -> skills/2_theme/labeling/
  .claude-plugin/plugin.json     -> removed; drop subjective-label from Tools/.claude-plugin/marketplace.json, the root README package table and the install.sh hint; bump the toolkit plugin version.
Move with `mv` (it carries uncommitted and untracked files; it has uncommitted edits in labeling.py, its README, a test). Then fix every reference (code, tests, Markdown, the host's optional-plugin discovery: the labeling workbench is no longer optional) and how engine/ is imported (sys.path inserts by relative depth).
Checks: the engine tests; haipipe-page tests/test_labeling.py; `serve.py --only labeling` answers labeling routes and 404 for terminal and chat; the full host opens a labeling Board; reinstall and confirm the labeling skills and agents are listed; a final grep for `subjective-label/` paths returns only history.

q01 · skill layers
------------------
Write down, in reports/q01_skill_layers/, what is in each layer now and the open choices JL raised: workbench-page sits in 1_base/page (it is the Page theme's workbench, so it could go to 2_theme/page while the page core stays in base); a workbench-shared skill (the frame contract) would belong in 1_base; whether servers/ mirror the layers. The design behind it is Tools/designs/b03_project_workbench/studio/s02-workbench-shared/ and s13-task-variants/.

Report to JL in chat as each Question finishes: what changed (files, one line each), the checks and their counts, what is left.
