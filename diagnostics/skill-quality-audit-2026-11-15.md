# Skill quality audit, 2026-11-15

Scope: the 136 SKILL.md files under `plugins/**/skills/` that install.sh installs (folders starting with `_` and node_modules/ skipped), with their ref/, scripts, tests and agents. Read-only round: nothing in a skill was edited.

Method: a mechanical sweep (frontmatter, sizes, markdown and path links, skill names, retired names, person and deployment names, trigger overlap), `--help` on the 65 scripts the skills tell you to run, every `skills/**/tests` suite with `uv run --python 3.13 --with pytest --with pyyaml --with markdown --with 'pandas<3' --with pyarrow`, `diagnostics/skill_report.py`, and a fresh-context dry run of 10 skills by two new agents.

Score: 5 clean; 4 one medium issue or size close; 3 a high issue or cold score 3; 2 cold score 2 or several high issues.

## 1. All skills

| Skill | Family | Lines | FM | Links | Size | Cold | Score | Top issue |
|---|---|---|---|---|---|---|---|---|
| ask-questions | 0_utils | 118 | ✅ | ✅ | ✅ |  | 5 |  |
| call-peer | 0_utils | 310 | ❗ | ✅ | ❗ |  | 4 | 1 helper files >=700 lines |
| diagram-ascii | 0_utils | 467 | ✅ | ✅ | ✅ |  | 5 |  |
| draw-logic-tree | 0_utils | 164 | ✅ | ✅ | ❗ |  | 4 | 1 helper files >=700 lines |
| notebook-cell-python | 0_utils | 302 | ✅ | ✅ | ✅ |  | 5 |  |
| remote-error | 0_utils | 420 | ✅ | ✅ | ✅ |  | 5 |  |
| remote-keyboard-typist | 0_utils | 555 | ✅ | ✅ | ✅ |  | 5 |  |
| response-format | 0_utils | 519 | ✅ | ✅ | ✅ |  | 5 |  |
| table-papers | 0_utils | 104 | ✅ | ✅ | ✅ |  | 5 |  |
| table-workbench | 0_utils | 111 | ✅ | ✅ | ✅ |  | 5 |  |
| haipipe-display | 1_base/display | 192 | ✅ | ✅ | ❗ | 2 | 2 | 1 helper files >=700 lines |
| haipipe-display-method | 1_base/display | 127 | ✅ | ✅ | ✅ |  | 5 |  |
| html-ppt | 1_base/display | 262 | ✅ | ✅ | ❗ |  | 4 | 1 helper files >=700 lines |
| haipipe-draft | 1_base/draft | 1339 | ✅ | ✅ | ❗ | 2 | 2 |  |
| haipipe-draft-logic | 1_base/draft | 63 | ✅ | ✅ | ❗ |  | 4 | 1 helper files >=700 lines |
| haipipe-draft-review | 1_base/draft | 171 | ✅ | ✅ | ❗ |  | 4 | 1 helper files >=700 lines |
| haipipe-draft-workflow | 1_base/draft | 656 | ✅ | ✅ | 🔶 |  | 4 | SKILL.md 656 lines (600-699) |
| haipipe-draft-writing | 1_base/draft | 322 | ✅ | ✅ | ❗ |  | 4 | 1 helper files >=700 lines |
| haipipe-evidence | 1_base/evidence | 169 | ✅ | ✅ | ✅ |  | 5 |  |
| excalidraw | 1_base/excalidraw | 44 | ✅ | ✅ | ✅ |  | 5 |  |
| excalidraw-draft (hidden) | 1_base/excalidraw | 56 | ✅ | ✅ | ❗ |  | 4 | 1 helper files >=700 lines |
| excalidraw-ideation (hidden) | 1_base/excalidraw | 172 | ✅ | ✅ | ✅ |  | 5 |  |
| excalidraw-job (hidden) | 1_base/excalidraw | 361 | ✅ | ✅ | ❗ |  | 4 | 2 helper files >=700 lines |
| excalidraw-read (hidden) | 1_base/excalidraw | 202 | ✅ | ✅ | ❗ |  | 4 | 1 helper files >=700 lines |
| excalidraw-report (hidden) | 1_base/excalidraw | 256 | ✅ | ✅ | ✅ |  | 5 |  |
| excalidraw-slide (hidden) | 1_base/excalidraw | 135 | ❗ | ✅ | ✅ |  | 4 | description 1191 chars >1024 |
| excalidraw-story (hidden) | 1_base/excalidraw | 114 | ❗ | ✅ | ❗ |  | 4 | 1 helper files >=700 lines |
| excalidraw-studio (hidden) | 1_base/excalidraw | 270 | ❗ | ✅ | ✅ |  | 4 | description 1296 chars >1024 |
| excalidraw-task (hidden) | 1_base/excalidraw | 227 | ✅ | ✅ | ❗ |  | 4 | 1 helper files >=700 lines |
| excalidraw-workflow (hidden) | 1_base/excalidraw | 191 | ❗ | ✅ | ❗ |  | 4 | 1 helper files >=700 lines |
| haipipe-ideation | 1_base/ideation | 403 | ✅ | ✅ | ❗ |  | 4 | 2 helper files >=700 lines |
| haipipe-block | 1_base/project | 132 | ✅ | ✅ | ✅ | 4 | 4 |  |
| haipipe-delivery | 1_base/project | 226 | ✅ | ✅ | ✅ |  | 5 |  |
| haipipe-job | 1_base/project | 106 | ✅ | ✅ | ✅ |  | 5 |  |
| haipipe-mindmap | 1_base/project | 153 | ✅ | ✅ | ✅ |  | 5 |  |
| haipipe-project | 1_base/project | 197 | ✅ | ✅ | ❗ |  | 4 | 1 helper files >=700 lines |
| haipipe-related | 1_base/project | 150 | ✅ | ✅ | ✅ |  | 5 |  |
| haipipe-report | 1_base/project | 244 | ✅ | ✅ | ✅ |  | 5 |  |
| haipipe-run | 1_base/project | 385 | ✅ | ✅ | ✅ |  | 5 |  |
| haipipe-studio | 1_base/project | 573 | ❗ | ✅ | ❗ |  | 3 | 2 helper files >=700 lines |
| word-track-change | 1_base/project | 60 | ✅ | ✅ | ✅ |  | 5 |  |
| haipipe-search | 1_base/search | 176 | ✅ | ✅ | ✅ |  | 5 |  |
| haipipe-task | 1_base/task | 187 | ✅ | ✅ | ✅ | 2 | 2 |  |
| haipipe-task-for-evidence (hidden) | 1_base/task/10_evidence | 309 | ✅ | ✅ | ✅ |  | 5 |  |
| haipipe-data | 1_base/task/1_data | 311 | ✅ | ✅ | ❗ |  | 4 | 1 helper files >=700 lines |
| haipipe-task-for-data (hidden) | 1_base/task/1_data | 399 | ❗ | ✅ | ✅ |  | 4 | names deployment: deployment names |
| haipipe-task-for-description (hidden) | 1_base/task/1_data | 344 | ✅ | ✅ | ✅ |  | 4 | names deployment: deployment names |
| haipipe-task-for-raw (hidden) | 1_base/task/1_data | 403 | ✅ | ✅ | ✅ |  | 4 | names deployment: deployment names |
| haipipe-nn | 1_base/task/2_nn | 174 | ✅ | ✅ | ✅ |  | 5 |  |
| haipipe-task-for-algo (hidden) | 1_base/task/2_nn | 140 | ❗ | ✅ | ✅ |  | 4 | description has no Use/Trigger clause |
| haipipe-end | 1_base/task/3_end | 342 | ✅ | ✅ | ✅ |  | 5 |  |
| haipipe-task-for-endpoint (hidden) | 1_base/task/3_end | 261 | ❗ | ✅ | ✅ |  | 4 | description has no Use/Trigger clause |
| haipipe-individual | 1_base/task/4_individual | 240 | ✅ | ✅ | ✅ |  | 5 |  |
| haipipe-individual-inference | 1_base/task/4_individual | 151 | ✅ | ✅ | ✅ |  | 5 |  |
| haipipe-individual-inference-judge | 1_base/task/4_individual | 198 | ✅ | ✅ | ✅ |  | 5 |  |
| haipipe-individual-inference-report | 1_base/task/4_individual | 193 | ✅ | ✅ | ✅ |  | 5 |  |
| haipipe-task-for-individual (hidden) | 1_base/task/4_individual | 117 | ❗ | ✅ | ✅ |  | 4 | description has no Use/Trigger clause |
| haipipe-task-for-fit (hidden) | 1_base/task/5_fit | 151 | ✅ | ✅ | ✅ |  | 5 |  |
| haipipe-task-for-eval (hidden) | 1_base/task/6_eval | 118 | ❗ | ✅ | ✅ |  | 4 | description has no Use/Trigger clause |
| haipipe-task-for-display (hidden) | 1_base/task/7_display | 145 | ❗ | ✅ | ✅ |  | 4 | description has no Use/Trigger clause |
| haipipe-task-for-stata (hidden) | 1_base/task/8_stata | 407 | ❗ | ✅ | ✅ |  | 4 | description has no Use/Trigger clause |
| haipipe-task-for-agent (hidden) | 1_base/task/9_agent | 122 | ✅ | ✅ | ✅ |  | 5 |  |
| haipipe-interaction | 1_base/workbench | 371 | ✅ | ✅ | ❗ | 3 | 3 | 1 helper files >=700 lines |
| haipipe-ui | 1_base/workbench | 572 | ❗ | ✅ | ✅ |  | 4 | description 1195 chars >1024 |
| workbench | 1_base/workbench | 339 | ✅ | ✅ | ✅ |  | 5 |  |
| workbench-task-draft | 1_base/workbench | 596 | ✅ | ✅ | ✅ |  | 4 | 35 'JL' provenance tags |
| haipipe-cowork | 2_theme/cowork | 173 | ✅ | ✅ | ✅ |  | 5 |  |
| workbench-cowork | 2_theme/cowork | 99 | ✅ | ✅ | ✅ |  | 5 |  |
| haipipe-design | 2_theme/design | 184 | ❗ | ✅ | ✅ | 2 | 2 | description 1234 chars >1024 |
| haipipe-design-brief (hidden) | 2_theme/design | 145 | ✅ | ✅ | ✅ |  | 5 |  |
| haipipe-design-delivery (hidden) | 2_theme/design | 138 | ✅ | ✅ | ✅ |  | 5 |  |
| haipipe-design-goal (hidden) | 2_theme/design | 164 | ✅ | ✅ | ✅ |  | 5 |  |
| haipipe-design-method | 2_theme/design | 161 | ✅ | ✅ | ✅ |  | 5 |  |
| haipipe-design-unit | 2_theme/design | 135 | ✅ | ✅ | ❗ |  | 4 | 1 helper files >=700 lines |
| haipipe-design-workflow | 2_theme/design | 184 | ✅ | ✅ | ✅ |  | 5 |  |
| workbench-design | 2_theme/design | 213 | ✅ | ✅ | ❗ |  | 4 | 1 helper files >=700 lines |
| haipipe-discovery | 2_theme/discovery | 525 | ✅ | ✅ | ❗ | 2 | 2 | 5 helper files >=700 lines |
| haipipe-discovery-inquiry | 2_theme/discovery | 230 | ✅ | ✅ | ✅ |  | 5 |  |
| haipipe-discovery-review | 2_theme/discovery | 85 | ✅ | ✅ | ✅ |  | 5 |  |
| haipipe-discovery-synthesize | 2_theme/discovery | 172 | ✅ | ✅ | ✅ |  | 5 |  |
| workbench-discovery | 2_theme/discovery | 78 | ✅ | ✅ | ✅ |  | 5 |  |
| haipipe-insight | 2_theme/insight | 160 | ✅ | ✅ | ❗ | 3 | 3 | 1 helper files >=700 lines |
| haipipe-insight-bind (hidden) | 2_theme/insight | 90 | ✅ | ✅ | ✅ |  | 5 |  |
| haipipe-insight-check | 2_theme/insight | 97 | ✅ | ✅ | ✅ |  | 5 |  |
| haipipe-insight-evidence-plan | 2_theme/insight | 100 | ✅ | ✅ | ✅ |  | 5 |  |
| haipipe-insight-workflow (hidden) | 2_theme/insight | 106 | ✅ | ✅ | ✅ |  | 5 |  |
| haipipe-page-insight | 2_theme/insight | 242 | ✅ | ✅ | ❗ |  | 4 | 1 helper files >=700 lines |
| workbench-insight | 2_theme/insight | 194 | ✅ | ✅ | ✅ |  | 5 |  |
| haipipe-insight-data | 2_theme/insight/folder-kinds | 97 | ✅ | ✅ | ✅ |  | 5 |  |
| haipipe-insight-information | 2_theme/insight/folder-kinds | 107 | ✅ | ✅ | ✅ |  | 5 |  |
| haipipe-insight-knowledge | 2_theme/insight/folder-kinds | 147 | ✅ | ✅ | ✅ |  | 5 |  |
| haipipe-insight-meta | 2_theme/insight/folder-kinds | 116 | ✅ | ✅ | ✅ |  | 5 |  |
| haipipe-insight-question | 2_theme/insight/folder-kinds | 154 | ✅ | ✅ | ✅ |  | 5 |  |
| haipipe-insight-wisdom | 2_theme/insight/folder-kinds | 147 | ✅ | ✅ | ✅ |  | 5 |  |
| haipipe-labeling | 2_theme/labeling | 249 | ✅ | ✅ | ✅ |  | 5 | labeling/engine loose at family root |
| haipipe-labeling-building (hidden) | 2_theme/labeling | 166 | ✅ | ✅ | ✅ |  | 5 |  |
| haipipe-labeling-scanning (hidden) | 2_theme/labeling | 125 | ✅ | ✅ | ✅ |  | 5 |  |
| haipipe-labeling-workflow (hidden) | 2_theme/labeling | 171 | ✅ | ✅ | ✅ |  | 5 |  |
| workbench-labeling | 2_theme/labeling | 163 | ✅ | ✅ | ✅ |  | 5 |  |
| workbench-task-labeling | 2_theme/labeling | 509 | ✅ | ✅ | ✅ |  | 5 |  |
| haipipe-labeling-contract (hidden) | 2_theme/labeling/1_data | 145 | ✅ | ✅ | ✅ |  | 5 |  |
| haipipe-labeling-embedding (hidden) | 2_theme/labeling/1_data | 79 | ✅ | ✅ | ✅ |  | 5 |  |
| haipipe-labeling-preparation (hidden) | 2_theme/labeling/1_data | 162 | ✅ | ✅ | ✅ |  | 5 |  |
| haipipe-labeling-definition (hidden) | 2_theme/labeling/2_labeling | 143 | ✅ | ✅ | ✅ |  | 5 |  |
| haipipe-labeling-expression | 2_theme/labeling/2_labeling | 80 | ✅ | ✅ | ✅ |  | 5 |  |
| haipipe-labeling-guideline (hidden) | 2_theme/labeling/2_labeling | 64 | ✅ | ✅ | ✅ |  | 5 |  |
| haipipe-labeling-interaction | 2_theme/labeling/2_labeling | 139 | ✅ | ✅ | ✅ |  | 5 |  |
| haipipe-labeling-rounds (hidden) | 2_theme/labeling/2_labeling | 229 | ✅ | ✅ | ✅ |  | 5 |  |
| haipipe-labeling-audit (hidden) | 2_theme/labeling/3_quality | 59 | ✅ | ✅ | ✅ |  | 5 |  |
| haipipe-labeling-evaluation (hidden) | 2_theme/labeling/3_quality | 55 | ✅ | ✅ | ✅ |  | 5 |  |
| haipipe-labeling-test (hidden) | 2_theme/labeling/3_quality | 66 | ✅ | ✅ | ✅ |  | 5 |  |
| haipipe-labeling-final-labels (hidden) | 2_theme/labeling/4_delivery | 45 | ✅ | ✅ | ✅ |  | 5 |  |
| haipipe-labeling-handoff (hidden) | 2_theme/labeling/4_delivery | 52 | ✅ | ✅ | ✅ |  | 5 |  |
| haipipe-labeling-scan (hidden) | 2_theme/labeling/4_delivery | 66 | ✅ | ✅ | ✅ |  | 5 |  |
| haipipe-paper | 2_theme/paper | 520 | ✅ | ✅ | ❗ | 3 | 3 | 2 helper files >=700 lines |
| haipipe-paper-assemble | 2_theme/paper | 866 | ✅ | ✅ | ❗ |  | 3 |  |
| haipipe-paper-comments | 2_theme/paper | 425 | ✅ | ✅ | ✅ |  | 5 |  |
| haipipe-paper-draft | 2_theme/paper | 694 | ✅ | ✅ | 🔶 |  | 4 | SKILL.md 694 lines (600-699) |
| haipipe-paper-evidence | 2_theme/paper | 512 | ✅ | ✅ | ❗ |  | 4 | 2 helper files >=700 lines |
| haipipe-paper-ideation | 2_theme/paper | 648 | ✅ | ✅ | 🔶 |  | 4 | SKILL.md 648 lines (600-699) |
| haipipe-paper-plan | 2_theme/paper | 248 | ✅ | ✅ | ✅ |  | 5 |  |
| haipipe-paper-related | 2_theme/paper | 206 | ✅ | ✅ | ✅ |  | 5 |  |
| haipipe-paper-story | 2_theme/paper | 783 | ✅ | ✅ | ❗ |  | 3 | SKILL.md 783 lines (>=700) |
| haipipe-paper-venue | 2_theme/paper | 266 | ✅ | ✅ | ✅ |  | 5 | paper/venue data tree loose at family root |
| haipipe-paper-workflow | 2_theme/paper | 277 | ✅ | ✅ | ✅ |  | 5 |  |
| workbench-paper | 2_theme/paper | 262 | ✅ | ✅ | ✅ |  | 5 |  |
| haipipe-work | 2_theme/work | 144 | ✅ | ✅ | ✅ |  | 5 |  |
| workbench-work | 2_theme/work | 214 | ✅ | ✅ | ✅ |  | 5 |  |
| inlab-human | inlab-human/inlab-human | 73 | ✅ | ✅ | ✅ |  | 5 |  |
| describe-exercise | utils/describe-exercise | 314 | ✅ | ✅ | ✅ |  | 4 | names deployment: WellDoc named |
| describe-food | utils/describe-food | 457 | ✅ | ✅ | ❗ | 2 | 2 | names deployment: WellDoc named 23x |
| describe-insulin | utils/describe-insulin | 254 | ✅ | ✅ | ✅ |  | 4 | names deployment: WellDoc named |
| describe-medication | utils/describe-medication | 240 | ✅ | ✅ | ✅ |  | 4 | names deployment: WellDoc named |
| haipipe-norm | utils/haipipe-norm | 378 | ✅ | ✅ | ✅ |  | 4 | names deployment: deployment names |
| meal-cam-logger | utils/meal-cam-logger | 280 | ✅ | ✅ | ✅ |  | 5 |  |
| whoop-connect | utils/whoop-connect | 186 | ✅ | ✅ | ✅ |  | 5 |  |

## 2. Findings by severity

✅ = fixed in round 1 (2026-11-15, after JL's ok; uncommitted). Splitting 700+ files and repairing failing tests are round 2.

### High

- ✅ **haipipe-draft** `1_base/draft/haipipe-draft/SKILL.md:106` (Keep it general): A real person's full name is the `--author` value in the fast-path export command (also :119). Fixed: `--author "<Your Name>"` at all 3 places; same in page.py help, wordtc.py, page-delivery.md (2), track_changes.py, test_page_export.py; word_round.py reads AUTHOR_NAMES from settings.env.
- ✅ **workbench** `1_base/workbench/workbench/SKILL.md:28` (Keep it general): Bakes a personal domain (`<space>.jjluo.com`), six named SPACEs with ports (:34-35), an institution's email domain (:41) and DrFirst's ports (:47). Fixed: `<space>.<DOMAIN>`, example.test; SPACE list, ports, institution and DrFirst ports removed; values stay in each SPACE's .server_config/.
- ✅ **workbench** `1_base/workbench/workbench/cli/wb_share.py:18` (Keep it general): Docstring lists the personal share domains by name. Fixed: Docstring and two --help texts made general; code still reads access.yaml.
- ✅ **haipipe-design** `2_theme/design/haipipe-design/SKILL.md:73` (Commands that do not run): `design_ladder.py release ... --from "M01 m2"` does not exist; the script's levels are block, book, method, job, task, run, goals, audit, update (design_ladder.py:444). Fixed: Real commands (`block`, `book`, `method --version`), checked on a scratch copy; says plainly there is no `release` level.
- ✅ **all** `(system python3 = 3.9.6)` (Commands that do not run): SKILL.md files say `python3 <script>`, but 7 named scripts need 3.10+ and fail on the Mac's python3 with `TypeError: unsupported operand |` (draw_logic_tree.py, cli/check.py, design_ladder.py, release.py, summary.py, servers/_host/serve.py); `page.py` refuses below 3.11. Fixed: skills/README.md § Running a skill's scripts (uv form, 3.10+ / 3.11+); a pointer line in draw-logic-tree, haipipe-draft, haipipe-design, haipipe-design-delivery.
- ✅ **haipipe-insight-meta** `2_theme/insight/folder-kinds/haipipe-insight-meta/SKILL.md:56` (Broken links and stale names): Links `../../haipipe-insight/ref/partition.md`, renamed to `segment.md` (also :113, and haipipe-insight-workflow ref/segment-policy.md:4). Fixed: All 7 partition.md links now point at segment.md (meta, segment-policy.md, migration.md).
- ✅ **haipipe-draft** `1_base/draft/haipipe-draft/SKILL.md:914` (Broken links and stale names): `ref/Run-cards.md` is named as the six-field Run statement; no such file. Fixed: `ref/run-cards.md` (haipipe-draft-workflow's).
- ✅ **haipipe-design** `2_theme/design/haipipe-design/SKILL.md:13` (Clarity from a fresh context): Cold score 2: `block` scaffold never shown in SKILL.md (only the script docstring); "launch a Job" never mapped to a Run; version 0.4.0 at :43 vs 0.4.2 in frontmatter. Fixed: Version line now 0.4.2; real block/book/method commands shown (round 1).
- ✅ **haipipe-task** `1_base/task/haipipe-task/SKILL.md:72` (Clarity from a fresh context): Cold score 2: never says how to create a Task; the scaffold writes `task-kind:` and no scripts/, runs/ (new_job.py:94) while the face contract wants `task-type:`. Fixed: New Task route in SKILL.md; new_job.py task writes `task-type:`, scripts/config/, runs/ (haipipe-job tests 12 passed).
- ✅ **haipipe-display** `1_base/display/haipipe-display/SKILL.md:137` (Clarity from a fresh context): Cold score 2: two preview recipes (SKILL.md:137 vs _parts/table/PART.md:199) and two reviewers (fresh agent :64 vs a Codex MCP model in PART.md:73, :223). Fixed: Door is the one source: build_preview.py for every kind (fixed its --help and missing threeparttable/siunitx), a fresh blind agent reviews (Codex optional), bare-input default location, float.tex owner; parts point to it.
- ✅ **describe-food** `plugins/haipipe-utils/skills/describe-food/SKILL.md:123` (Clarity from a fresh context): Cold score 2: two confidence vocabularies (MEASURED/ESTIMATED/MISS, "PARTIAL retired") vs GOOD/PARTIAL/MISS at :349-354; five vs six nutrients (:139 vs :229). Fixed: One vocabulary from the code (NutritionConf MEASURED/ESTIMATED/MISS; GOOD/OK/ALIAS only inside T2), six nutrients, items.py, bank location, which output when; retired --bench lines fixed.
- ✅ **haipipe-draft** `1_base/draft/haipipe-draft/tests` (Tests): 20 failed of 972. Tests read `haipipe-task/ref/check_task_tree.py` (moved to scripts/); 5 Evidence tests expect `bound` and get `blocked`; design snapshot tests drift. Fixed: All repaired: engine reads `report: shape:` as well as `outline:` (src/plan_shape.py, src/folder_contract.py); old four-Space page's Runs-panel checks retired with a note. 979 passed, 0 failed.
- ✅ **haipipe-draft** `1_base/draft/haipipe-draft/SKILL.md` (File size): 1,338 lines (limit 700). Its src/ holds body.py 1,724, page_question.py 1,446, dialect_paper.py 1,250, plan_shape.py 1,199. Fixed: 1,340 → 578 lines, a route table first; 8 new ref/ files (draft-steps, page-runs, file-to-page, page-folder-layout, page-face, run-workflow, open-page, closing-checks); 1,310 tests passed before and after.
- ✅ **haipipe-paper-assemble** `2_theme/paper/haipipe-paper-assemble/SKILL.md` (File size): 865 lines; scripts latex_room_to_docx.py 1,875 and build_delivery.py 1,783. Fixed: 865 → 587 lines; 7 topics moved to ref/ (no new test failures).
- ✅ **haipipe-paper-story** `2_theme/paper/haipipe-paper-story/SKILL.md` (File size): 782 lines. Fixed: 782 → 555 lines; ref/research-questions.md, ref/roadmaps.md.
- ✅ **haipipe-discovery, paper venue scripts** `2_theme/discovery/haipipe-discovery/scripts/paper_result_build.py:52` (Keep it general): Four scripts sent a personal email address in the User-Agent to outside APIs (also playbook-utd-is build-inventory.py, filter-ai-healthcare.py, merge-isr-frame.py). Fixed: Address now comes from CONTACT_EMAIL; none set sends none.
- ✅ **draft family** `1_base/draft/haipipe-draft-writing/SKILL.md:153` (Clarity from a fresh context): 25 conflicts: the plan sign said both "write nothing without ✅" and "do not block on a blank approved:"; paragraph 4 to 6 vs 4 to 7; two vs three sentence scores; flat runs/ + results/ vs one folder per Run; structure.md at 758 lines. Fixed: One rule in every file (signed plan first, 4 to 7, three scores, runs/<name>/passes/); structure.md split into bullet.md and survey.md; paragraphs.py default 7.
- ✅ **task family** `1_base/task/agents/haipipe-task-reviewer-agent.md:50` (Clarity from a fresh context): 25 conflicts: agents and haipipe-data/haipipe-end taught the flat Run layout; a missing CODE_REVIEW.md blocked in six scaffolds and was advisory in the template; status words; who writes the review files; fn-3-design-chef.md at 820 lines. Fixed: Docs follow run-sh-template.sh and task-folder.md; the long file split in two. Left: about 100 lines of named examples, attempts/ vs passes/.
- ✅ **paper, evidence, display** `2_theme/paper/haipipe-paper/ref/paper-ladder.md:137` (Clarity from a fresh context): 25 conflicts: comments batch in reports/ vs a review Job; compile order in the Story vs the version face; Section evidence Runs; Work view retired or current; display home; blind reviewer packet. Fixed: 29 docs aligned to the code; older forms kept as "an older Board". Four left for a decision (bibliography home, Draft version bump, display Task names, display plan home).
- ✅ **insight, design, labeling, discovery, cowork, work** `2_theme/insight/haipipe-insight/SKILL.md:131` (Clarity from a fresh context): 25 conflicts: run types the scripts refuse (segment for partition/cut), a Job folder pattern the scaffold refuses, retired cowork-board and discovery-board pages named as current, a retired board/ build step, initials in a signature. Fixed: 67 docs aligned to the scripts and the shared frame; level skills carry an older-layout banner.
- ✅ **project, workbench, excalidraw, utils** `1_base/workbench/haipipe-ui/SKILL.md:142` (Clarity from a fresh context): 25 conflicts: reports/qNN and a studio/ folder taught as current after both were retired; topic limit 10 soft vs 9/5/3 hard; haipipe-ui required state words and tallies that AGENTS.md bans; project.md vs README.md as the required face. Fixed: About 60 docs aligned to new_topic.py, ladder.py and ui_parts.py. Four left for a decision (delivery/ per level, Work section, Spaces vocabulary, reply-format See line).

### Medium

- ✅ **haipipe-draft** `1_base/draft/haipipe-draft/ref/standalone.md:34` (Keep it general): Names Physician-SPACE and its Tailscale origin as the hosting rule. Fixed: "the SPACE's configured origin (`DOMAIN`)".
- ✅ **haipipe-interaction** `1_base/workbench/haipipe-interaction/SKILL.md:364` (Keep it general): "the Tailscale origin, never localhost" names one deployment's network. Fixed: "its configured origin, `DOMAIN` in settings.env".
- ✅ **describe-food** `plugins/haipipe-utils/skills/describe-food/SKILL.md:22` (Keep it general): One data partner is named 23 times as the benchmark and ground truth (:102-105, :367-381); same in describe-exercise:80, describe-medication, describe-insulin. Fixed: Partner company names replaced in prose across 9 skill docs; dataset ids, dialect keys and real paths kept (code matches them).
- ✅ **haipipe-draft** `1_base/draft/haipipe-draft/SKILL.md:105` (Commands that do not run): Commands use `.venv/bin/python` and `Tools/plugins/...`; Tools-SPACE has no `.venv` and `plugins/` sits at the root. Same pattern in haipipe-interaction and haipipe-discovery (`Tools/references/aris`). Fixed: A line above the fast path says: from Tools-SPACE drop `Tools/`; with no `.venv`, use the uv form.
- ✅ **haipipe-insight** `2_theme/insight/haipipe-insight/SKILL.md:65` (Commands that do not run): `--check` reads like a script flag but insight_ladder.py has none (:861-888); ref/update.md mixes `uv run` (:17) and bare `python` (:34, :57). Fixed: Says `--check` is an instruction to stop after update.md step 2, not a flag.
- ✅ **haipipe-block** `1_base/project/haipipe-block/ref/board-contract.md:93` (Commands that do not run): `new_job.py <block> --slug` misses the required `job` subcommand and `--title`. Fixed: Real call: `new_job.py job <block> --slug … --title`.
- ✅ **haipipe-paper-assemble** `2_theme/paper/haipipe-paper-assemble/SKILL.md:158` (Broken links and stale names): `ref/word.md` is not in the skill's ref/ (holds only build.py.wrapper, paper-build.toml.example). Fixed: Points at haipipe-delivery ref/page-delivery.md and `page.py export --lane word`.
- ✅ **workbench** `1_base/workbench/workbench/SKILL.md:163` (Broken links and stale names): Names `haipipe-project-meeting` as the owner of meetings; no such skill (meetings are haipipe-related). Fixed: haipipe-related.
- ✅ **table-papers** `0_utils/table-papers/SKILL.md:57` (Broken links and stale names): `ref/papers/README.md` (license list) does not exist. Fixed: Says the folder and README are made with the first PDF.
- ✅ **haipipe-paper, haipipe-task** `2_theme/paper/haipipe-paper/SKILL.md:13` (Broken links and stale names): Cites "AGENTS.md rule 6 / rule 9" (also :15; haipipe-task SKILL.md:31, :96). AGENTS.md has no numbered rules and no hash rule. Fixed: 29 files: "AGENTS.md rule N" now "the SPACE's AGENTS.md § Working rules" (the numbers came from a SPACE's AGENTS.md and differ per SPACE).
- ✅ **haipipe-draft** `1_base/draft/haipipe-draft/SKILL.md:395` (Clarity from a fresh context): Cold score 2: the "file to page" route starts at line 395 of 1,338; :458 says rerun setup but standalone.md:85 says rerun refuses without `--force`. Fixed: The route table now opens the skill; "file to page" is one row.
- ✅ **haipipe-discovery** `2_theme/discovery/haipipe-discovery/SKILL.md:20` (Clarity from a fresh context): Cold score 2: ~15 required reads across 4 skills before "add a paper"; `add` has no script; scope roots (:342) omit `discovery/`. Fixed: New § Minimum to add one paper: tNN is the question (not qNN), one contract ref, paper_result_build.py's real flags, close with paper_runs.py.
- ✅ **hash rule** `2_theme/paper/haipipe-paper/SKILL.md:15` (Clarity from a fresh context): haipipe-paper bans every content hash; haipipe-insight (update.md:46, :73) and haipipe-design (ref/design-ladder.md rules 3-4) pin sha256. Fixed: Decided 2026-11-15: insight's tables_sha256 and design's method-sha/manifest sha256 are the two exceptions; written in haipipe-paper, haipipe-draft, haipipe-draft-writing, insight ref/update.md, design ref/design-ladder.md.
- ✅ **haipipe-draft-workflow** `1_base/draft/haipipe-draft-workflow/tests` (Tests): 7 failed of 23: tests grep haipipe-run SKILL.md for text it no longer has (`run-structure-`, `Closed records`, `interactive-writing-run.md`). Fixed: Contract tests read haipipe-run ref/identity-and-history.md and ref/run-catalog.md; one dead link removed. 19 passed.
- ✅ **haipipe-paper-assemble** `2_theme/paper/haipipe-paper-assemble/tests` (Tests): 34 failed without python-docx; 5 still fail with it (JAMA eTable labels, equations). Fixed: No code bug: needs latex2mathml and pillow. With them 131 passed.
- ✅ **haipipe-paper-draft, haipipe-draft-workflow, haipipe-paper-ideation** `2_theme/paper/haipipe-paper-draft/SKILL.md` (File size): 693, 655 and 647 lines: one edit from the limit. Fixed: Split: paper-draft 695 → 462, draft-workflow 655 → 459, paper-ideation 647 → 482 (7 new refs); 256 tests passed.
- ✅ **all** `(82 files)` (File size): 82 readable files at 700+ lines and 27 at 600-699 inside skill folders (code, tests, refs); largest: excalidraw-job job_drawing.py 1,757, job_ladder.py 1,713, excalidraw-task task_drawing.py 1,616, haipipe-interaction collect.py 1,479. Fixed: Decided, no change now: AGENTS.md splits a code file when its part is next changed ("the part you change moves out"); a bulk split of 82 files while other sessions edit them would break more than it fixes.
- ✅ **haipipe-design, haipipe-ui, haipipe-studio** `2_theme/design/haipipe-design/SKILL.md:3` (Frontmatter and triggers): Descriptions over 1,024 characters (1,234; 1,195; 1,072). Hidden excalidraw-slide, -story, -studio, -workflow are 1,191 to 1,528. Fixed: All 7 long descriptions now 698-888 characters; skill_report finds 0 problems.
- ✅ **display, draft, paper, design, labeling** `1_base/display/ref` (Family shape): Non-skill folders at family root, not under a door's _parts/: display/ref, draft/pages-example, paper/venue, paper/tests, design/venue, labeling/engine. Fixed: Moved: paper/tests → haipipe-paper/tests, draft/pages-example → haipipe-draft/ref/pages-example, labeling fixtures beside engine tests. Kept, with the reason in each family README: display/ref and design/venue (cited by SPACE pages), paper/venue (a submodule cited by 405 SPACE files), labeling/engine (imported by servers/ code).
- ✅ **haipipe-paper-venue** `2_theme/paper/venue/playbook-nature-portfolio/nature-medicine/examples/INDEX.md:7` (Keep it general): A personal email address in a curated paper list. Fixed: Placeholder.
- ✅ **labeling engine** `2_theme/labeling/engine` (Tests): 19 failed: 13 need scikit-learn, 5 patched old module names after a split, 1 needed a fixture deleted in 4a2a01451. Fixed: sklearn tests skip when absent; patches point at live.labeling_board / _runs_view / _hold; fixture restored to labeling/fixtures/job-mini/. 357 passed.

### Low

- ✅ **many** `(651 lines across skills)` (Keep it general): 651 `JL <date>` provenance tags in SKILL.md text; haipipe-ui alone has 53. Allowed in docs, but they cost tokens and name one person. Fixed: Decided, no change: AGENTS.md § Page words puts provenance in code comments, commits and docs, so dated tags in skill docs are allowed; they leave a file when it is next rewritten.
- ✅ **haipipe-individual-inference-judge** `1_base/task/4_individual/haipipe-individual-inference-judge/scripts/judge_report_cli.py` (Commands that do not run): Needs `claude_agent_sdk`, not named in the skill; same for haipipe-individual-inference-report. Fixed: Tests now skip when pydantic (the real import need) is absent; the SDK is stubbed in tests.
- ✅ **haipipe-discovery** `2_theme/discovery/haipipe-discovery/SKILL.md:114` (Broken links and stale names): Puts `_parts/` under workbench-discovery; the folder is in haipipe-discovery. Fixed: Tree shows _parts/ under haipipe-discovery; scope roots include discovery/.
- ✅ **haipipe-interaction** `1_base/workbench/haipipe-interaction/SKILL.md:53` (Clarity from a fresh context): "Choose a version" listed as "not yet" while :51 and :174 say choices are built. Fixed: "Choose a version" moved to the built row.
- ✅ **haipipe-block** `1_base/project/haipipe-block/SKILL.md:74` (Clarity from a fresh context): Cold score 4: two items numbered 5 (:74, :76); singular vs plural world folders in board-contract.md:10 vs :107. Fixed: Renumbered (6. Check).
- ✅ **paper fragments** `2_theme/paper/tests/test_import_fragments.py` (Tests): 2 failed: expect `S1` sentence ids; another session is renaming S to s tonight. Fixed: Expectations use lowercase s ids (rename done in that code path). Passes.
- ✅ **haipipe-individual-inference-*** `1_base/task/4_individual` (Tests): 2 collection errors: `claude_agent_sdk` not installed. Fixed: Tests skip when pydantic is absent; 7 + 6 pass with it.
- ✅ **haipipe-paper-venue** `2_theme/paper/venue/bank/1-QBv-desks` (File size): 16 venue desk files of 700 to 1,384 lines (data). Out of scope if treated as data; say so in the folder README. Fixed: venue/README.md says the desk files are reference data, which § Keep files short exempts.
- ✅ **haipipe-task-for-*, call-peer** `1_base/task/1_data/haipipe-task-for-data/SKILL.md:3` (Frontmatter and triggers): Seven task-type skills (data, algo, endpoint, individual, eval, display, stata) and call-peer have no Use or Trigger clause; reached only through haipipe-task. Fixed: No change needed: "Called by /haipipe-task when task-type=X" is the when clause. call-peer got its Use/Trigger clause.
- ✅ **triggers** `(descriptions)` (Frontmatter and triggers): Trigger words shared by 2+ skills: "propose a question" (ask-questions, haipipe-insight-question, haipipe-report), "run spec" (haipipe-draft, haipipe-draft-workflow, haipipe-run), "workflow" (haipipe-paper-workflow, haipipe-run), "draft folder", "page context", "design handoff", "claim". Fixed: Each shared phrase now on one owner (e.g. "propose an insight question", "page Run Spec", "paper workflow", "insight claim").
- ✅ **aliases** `~/.claude/skills` (Frontmatter and triggers): Four skills install under a second link name (wb, haipipe-collect, haipipe-paper-display, haipipe-discovery-search); fresh agents saw `haipipe-collect (haipipe-interaction)` and paused. Fixed: Decided, no change: the alias links are how /wb and the other short names work; removing them would break those commands.
- ✅ **task family** `1_base/task/1_data/SKILLSET_REVIEW.md` (Family shape): Review notes left at family level (task/DESIGN.md 666 lines, 1_data/SKILLSET_REVIEW.md, 3_end/LESSON.md) and task/agents/CODE_REVIEW.md naming a retired haipipe-task-builder-agent. Fixed: The 6 review notes moved to 1_base/task/_notes/ (installers skip it); task/README.md points there.

## 3. Ten fixes to do first

1. ✅ **Remove the person's name**: haipipe-draft SKILL.md:106, :119: `--author "<Author>"`.
2. ✅ **Generalize the share door**: workbench SKILL.md:28-47 and wb_share.py:18: `<space>.<DOMAIN>`, no SPACE list.
3. ✅ **Fix the fake command**: haipipe-design SKILL.md:73: replace `release --from` with the real path.
4. ✅ **One runner line**: Every script command: `uv run --python 3.13 --with pyyaml python ...`.
5. ✅ **Fix 5 dead links**: partition.md→segment.md (3 places), Run-cards.md, word.md, papers/README.md, haipipe-project-meeting.
6. ✅ **Fix test paths**: haipipe-draft tests: ref/check_task_tree.py → scripts/; rerun the 20.
7. ✅ **Split haipipe-draft**: 1,338-line SKILL.md into door + ref/ per route.
8. ✅ **One vocabulary**: describe-food: one confidence scale, one nutrient count.
9. ✅ **One display loop**: haipipe-display: one preview recipe and one reviewer in the door.
10. 🔶 **Settle the hash rule**: AGENTS.md: decide; align haipipe-paper, insight, design; drop "rule 6/9".

## 4. Tests run

```text
1_base/draft (all suites) :: 1,027 passed, 3 skipped (after round 4)
2_theme/paper (all suites) :: 237 passed (after round 4; with python-docx, latex2mathml, pillow)
2_theme/labeling/engine :: 357 passed (after round 4; with scikit-learn)
1_base/task (all tests folders) :: 23 passed (after round 4; with pydantic)
1_base/display (all suites) :: 8 passed (after round 4)
2_theme/discovery (all suites) :: 103 passed (after round 4)
2_theme/design (all suites) :: 111 passed, 4 skipped (after round 2)
2_theme/insight (all suites) :: 113 passed (after round 3)
1_base/project (all suites) :: 155 passed (after round 2)
1_base/workbench/lab/tests (new /lab) :: 5 passed
1_base/workbench/workbench/tests :: 7 passed
After round 5 (rule-conflict fixes, docs) :: draft 990 passed; paper 249; insight 113; labeling engine 357; design 111; discovery 103; project 156; task 10; display 8; lab 6; workbench 7
```

Paths in findings are relative to `plugins/haipipe-toolkit/skills/` unless they start with `plugins/`.
