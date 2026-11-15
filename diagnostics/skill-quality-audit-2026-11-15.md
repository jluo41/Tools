# Skill quality audit, 2026-11-15

Scope: the 136 SKILL.md files under `plugins/**/skills/` that install.sh installs (folders starting with `_` and node_modules/ skipped), with their ref/, scripts, tests and agents. Read-only round: nothing in a skill was edited.

Method: a mechanical sweep (frontmatter, sizes, markdown and path links, skill names, retired names, person and deployment names, trigger overlap), `--help` on the 65 scripts the skills tell you to run, every `skills/**/tests` suite with `uv run --python 3.13 --with pytest --with pyyaml --with markdown --with 'pandas<3' --with pyarrow`, `diagnostics/skill_report.py`, and a fresh-context dry run of 10 skills by two new agents.

Score: 5 clean; 4 one medium issue or size close; 3 a high issue or cold score 3; 2 cold score 2 or several high issues.

## 1. All skills

| Skill | Family | Lines | FM | Links | Size | Cold | Score | Top issue |
|---|---|---|---|---|---|---|---|---|
| ask-questions | 0_utils | 118 | ✅ | ✅ | ✅ |  | 5 |  |
| call-peer | 0_utils | 310 | ❗ | ✅ | ❗ |  | 4 | Seven task-type skills (data, algo, endpoint, individual, eval, display, stata) and call-peer have no Use or Trigger clause; reached only through haipipe-task. |
| diagram-ascii | 0_utils | 467 | ✅ | ✅ | ✅ |  | 5 |  |
| draw-logic-tree | 0_utils | 164 | ✅ | ✅ | ❗ |  | 4 | 1 helper files >=700 lines |
| notebook-cell-python | 0_utils | 302 | ✅ | ✅ | ✅ |  | 5 |  |
| remote-error | 0_utils | 420 | ✅ | ✅ | ✅ |  | 5 |  |
| remote-keyboard-typist | 0_utils | 555 | ✅ | ✅ | ✅ |  | 5 |  |
| response-format | 0_utils | 519 | ✅ | ✅ | ✅ |  | 5 |  |
| table-papers | 0_utils | 104 | ✅ | ❗ | ✅ |  | 4 | `ref/papers/README.md` (license list) does not exist. |
| table-workbench | 0_utils | 111 | ✅ | ✅ | ✅ |  | 5 |  |
| haipipe-display | 1_base/display | 192 | ✅ | ✅ | ❗ | 2 | 2 | Cold score 2: two preview recipes (SKILL.md:137 vs _parts/table/PART.md:199) and two reviewers (fresh agent :64 vs a Codex MCP model in PART.md:73, :223). |
| haipipe-display-method | 1_base/display | 127 | ✅ | ✅ | ✅ |  | 5 |  |
| html-ppt | 1_base/display | 262 | ✅ | ✅ | ❗ |  | 4 | 1 helper files >=700 lines |
| haipipe-draft | 1_base/draft | 1339 | ✅ | ❗ | ❗ | 2 | 2 | A real person's full name is the `--author` value in the fast-path export command (also :119). |
| haipipe-draft-logic | 1_base/draft | 63 | ✅ | ✅ | ❗ |  | 4 | 1 helper files >=700 lines |
| haipipe-draft-review | 1_base/draft | 171 | ✅ | ✅ | ❗ |  | 4 | 1 helper files >=700 lines |
| haipipe-draft-workflow | 1_base/draft | 656 | ✅ | ✅ | 🔶 |  | 4 | 7 failed of 23: tests grep haipipe-run SKILL.md for text it no longer has (`run-structure-`, `Closed records`, `interactive-writing-run.md`). |
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
| haipipe-block | 1_base/project | 132 | ✅ | ✅ | ✅ | 4 | 4 | `new_job.py <block> --slug` misses the required `job` subcommand and `--title`. |
| haipipe-delivery | 1_base/project | 226 | ✅ | ✅ | ✅ |  | 5 |  |
| haipipe-job | 1_base/project | 106 | ✅ | ✅ | ✅ |  | 5 |  |
| haipipe-mindmap | 1_base/project | 153 | ✅ | ✅ | ✅ |  | 5 |  |
| haipipe-project | 1_base/project | 197 | ✅ | ✅ | ❗ |  | 4 | 1 helper files >=700 lines |
| haipipe-related | 1_base/project | 150 | ✅ | ✅ | ✅ |  | 5 |  |
| haipipe-report | 1_base/project | 244 | ✅ | ✅ | ✅ |  | 5 |  |
| haipipe-run | 1_base/project | 385 | ✅ | ✅ | ✅ |  | 5 |  |
| haipipe-studio | 1_base/project | 573 | ❗ | ✅ | ❗ |  | 3 | Descriptions over 1,024 characters (1,234; 1,195; 1,072). Hidden excalidraw-slide, -story, -studio, -workflow are 1,191 to 1,528. |
| word-track-change | 1_base/project | 60 | ✅ | ✅ | ✅ |  | 5 |  |
| haipipe-search | 1_base/search | 176 | ✅ | ✅ | ✅ |  | 5 |  |
| haipipe-task | 1_base/task | 187 | ✅ | ✅ | ✅ | 2 | 2 | Cold score 2: never says how to create a Task; the scaffold writes `task-kind:` and no scripts/, runs/ (new_job.py:94) while the face contract wants `task-type:`. |
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
| haipipe-individual-inference-judge | 1_base/task/4_individual | 198 | ✅ | ✅ | ✅ |  | 5 | Needs `claude_agent_sdk`, not named in the skill; same for haipipe-individual-inference-report. |
| haipipe-individual-inference-report | 1_base/task/4_individual | 193 | ✅ | ✅ | ✅ |  | 5 |  |
| haipipe-task-for-individual (hidden) | 1_base/task/4_individual | 117 | ❗ | ✅ | ✅ |  | 4 | description has no Use/Trigger clause |
| haipipe-task-for-fit (hidden) | 1_base/task/5_fit | 151 | ✅ | ✅ | ✅ |  | 5 |  |
| haipipe-task-for-eval (hidden) | 1_base/task/6_eval | 118 | ❗ | ✅ | ✅ |  | 4 | description has no Use/Trigger clause |
| haipipe-task-for-display (hidden) | 1_base/task/7_display | 145 | ❗ | ✅ | ✅ |  | 4 | description has no Use/Trigger clause |
| haipipe-task-for-stata (hidden) | 1_base/task/8_stata | 407 | ❗ | ✅ | ✅ |  | 4 | description has no Use/Trigger clause |
| haipipe-task-for-agent (hidden) | 1_base/task/9_agent | 122 | ✅ | ✅ | ✅ |  | 5 |  |
| haipipe-interaction | 1_base/workbench | 371 | ✅ | ✅ | ❗ | 3 | 3 | "the Tailscale origin, never localhost" names one deployment's network. |
| haipipe-ui | 1_base/workbench | 572 | ❗ | ✅ | ✅ |  | 4 | Descriptions over 1,024 characters (1,234; 1,195; 1,072). Hidden excalidraw-slide, -story, -studio, -workflow are 1,191 to 1,528. |
| workbench | 1_base/workbench | 339 | ✅ | ❗ | ✅ |  | 3 | Bakes a personal domain (`<space>.jjluo.com`), six named SPACEs with ports (:34-35), an institution's email domain (:41) and DrFirst's ports (:47). |
| workbench-task-draft | 1_base/workbench | 596 | ✅ | ✅ | ✅ |  | 4 | 35 'JL' provenance tags |
| haipipe-cowork | 2_theme/cowork | 173 | ✅ | ✅ | ✅ |  | 5 |  |
| workbench-cowork | 2_theme/cowork | 99 | ✅ | ✅ | ✅ |  | 5 |  |
| haipipe-design | 2_theme/design | 184 | ❗ | ✅ | ✅ | 2 | 2 | `design_ladder.py release ... --from "M01 m2"` does not exist; the script's levels are block, book, method, job, task, run, goals, audit, update (design_ladder.py:444). |
| haipipe-design-brief (hidden) | 2_theme/design | 145 | ✅ | ✅ | ✅ |  | 5 |  |
| haipipe-design-delivery (hidden) | 2_theme/design | 138 | ✅ | ✅ | ✅ |  | 5 |  |
| haipipe-design-goal (hidden) | 2_theme/design | 164 | ✅ | ✅ | ✅ |  | 5 |  |
| haipipe-design-method | 2_theme/design | 161 | ✅ | ✅ | ✅ |  | 5 |  |
| haipipe-design-unit | 2_theme/design | 135 | ✅ | ✅ | ❗ |  | 4 | 1 helper files >=700 lines |
| haipipe-design-workflow | 2_theme/design | 184 | ✅ | ✅ | ✅ |  | 5 |  |
| workbench-design | 2_theme/design | 213 | ✅ | ✅ | ❗ |  | 4 | 1 helper files >=700 lines |
| haipipe-discovery | 2_theme/discovery | 525 | ✅ | ✅ | ❗ | 2 | 2 | Cold score 2: ~15 required reads across 4 skills before "add a paper"; `add` has no script; scope roots (:342) omit `discovery/`. |
| haipipe-discovery-inquiry | 2_theme/discovery | 230 | ✅ | ✅ | ✅ |  | 5 |  |
| haipipe-discovery-review | 2_theme/discovery | 85 | ✅ | ✅ | ✅ |  | 5 |  |
| haipipe-discovery-synthesize | 2_theme/discovery | 172 | ✅ | ✅ | ✅ |  | 5 |  |
| workbench-discovery | 2_theme/discovery | 78 | ✅ | ✅ | ✅ |  | 5 |  |
| haipipe-insight | 2_theme/insight | 160 | ✅ | ✅ | ❗ | 3 | 3 | `--check` reads like a script flag but insight_ladder.py has none (:861-888); ref/update.md mixes `uv run` (:17) and bare `python` (:34, :57). |
| haipipe-insight-bind (hidden) | 2_theme/insight | 90 | ✅ | ✅ | ✅ |  | 5 |  |
| haipipe-insight-check | 2_theme/insight | 97 | ✅ | ✅ | ✅ |  | 5 |  |
| haipipe-insight-evidence-plan | 2_theme/insight | 100 | ✅ | ✅ | ✅ |  | 5 |  |
| haipipe-insight-workflow (hidden) | 2_theme/insight | 106 | ✅ | ❗ | ✅ |  | 4 | broken: ref/segment-policy.md:4 ../../haipipe-insight/ref/partition.md |
| haipipe-page-insight | 2_theme/insight | 242 | ✅ | ✅ | ❗ |  | 4 | 1 helper files >=700 lines |
| workbench-insight | 2_theme/insight | 194 | ✅ | ✅ | ✅ |  | 5 |  |
| haipipe-insight-data | 2_theme/insight/folder-kinds | 97 | ✅ | ✅ | ✅ |  | 5 |  |
| haipipe-insight-information | 2_theme/insight/folder-kinds | 107 | ✅ | ✅ | ✅ |  | 5 |  |
| haipipe-insight-knowledge | 2_theme/insight/folder-kinds | 147 | ✅ | ✅ | ✅ |  | 5 |  |
| haipipe-insight-meta | 2_theme/insight/folder-kinds | 116 | ✅ | ❗ | ✅ |  | 3 | Links `../../haipipe-insight/ref/partition.md`, renamed to `segment.md` (also :113, and haipipe-insight-workflow ref/segment-policy.md:4). |
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
| haipipe-paper | 2_theme/paper | 520 | ✅ | ✅ | ❗ | 3 | 3 | Cites "AGENTS.md rule 6 / rule 9" (also :15; haipipe-task SKILL.md:31, :96). AGENTS.md has no numbered rules and no hash rule. |
| haipipe-paper-assemble | 2_theme/paper | 866 | ✅ | ❗ | ❗ |  | 2 | 865 lines; scripts latex_room_to_docx.py 1,875 and build_delivery.py 1,783. |
| haipipe-paper-comments | 2_theme/paper | 425 | ✅ | ✅ | ✅ |  | 5 |  |
| haipipe-paper-draft | 2_theme/paper | 694 | ✅ | ✅ | 🔶 |  | 4 | 693, 655 and 647 lines: one edit from the limit. |
| haipipe-paper-evidence | 2_theme/paper | 512 | ✅ | ✅ | ❗ |  | 4 | 2 helper files >=700 lines |
| haipipe-paper-ideation | 2_theme/paper | 648 | ✅ | ✅ | 🔶 |  | 4 | 693, 655 and 647 lines: one edit from the limit. |
| haipipe-paper-plan | 2_theme/paper | 248 | ✅ | ✅ | ✅ |  | 5 |  |
| haipipe-paper-related | 2_theme/paper | 206 | ✅ | ✅ | ✅ |  | 5 |  |
| haipipe-paper-story | 2_theme/paper | 783 | ✅ | ✅ | ❗ |  | 3 | 782 lines. |
| haipipe-paper-venue | 2_theme/paper | 266 | ✅ | ✅ | ✅ |  | 5 | 16 venue desk files of 700 to 1,384 lines (data). Out of scope if treated as data; say so in the folder README. |
| haipipe-paper-workflow | 2_theme/paper | 277 | ✅ | ✅ | ✅ |  | 5 |  |
| workbench-paper | 2_theme/paper | 262 | ✅ | ✅ | ✅ |  | 5 |  |
| haipipe-work | 2_theme/work | 144 | ✅ | ✅ | ✅ |  | 5 |  |
| workbench-work | 2_theme/work | 214 | ✅ | ✅ | ✅ |  | 5 |  |
| inlab-human | inlab-human/inlab-human | 73 | ✅ | ✅ | ✅ |  | 5 |  |
| describe-exercise | utils/describe-exercise | 314 | ✅ | ✅ | ✅ |  | 4 | names deployment: WellDoc named |
| describe-food | utils/describe-food | 457 | ✅ | ✅ | ❗ | 2 | 2 | Cold score 2: two confidence vocabularies (MEASURED/ESTIMATED/MISS, "PARTIAL retired") vs GOOD/PARTIAL/MISS at :349-354; five vs six nutrients (:139 vs :229). |
| describe-insulin | utils/describe-insulin | 254 | ✅ | ✅ | ✅ |  | 4 | names deployment: WellDoc named |
| describe-medication | utils/describe-medication | 240 | ✅ | ✅ | ✅ |  | 4 | names deployment: WellDoc named |
| haipipe-norm | utils/haipipe-norm | 378 | ✅ | ✅ | ✅ |  | 4 | names deployment: deployment names |
| meal-cam-logger | utils/meal-cam-logger | 280 | ✅ | ✅ | ✅ |  | 5 |  |
| whoop-connect | utils/whoop-connect | 186 | ✅ | ✅ | ✅ |  | 5 |  |

## 2. Findings by severity

### High

- **haipipe-draft** `1_base/draft/haipipe-draft/SKILL.md:106` (Keep it general): A real person's full name is the `--author` value in the fast-path export command (also :119). Fix: Use `--author "<Author>"`.
- **workbench** `1_base/workbench/workbench/SKILL.md:28` (Keep it general): Bakes a personal domain (`<space>.jjluo.com`), six named SPACEs with ports (:34-35), an institution's email domain (:41) and DrFirst's ports (:47). Fix: Move the door table to each SPACE's settings; write `<space>.<DOMAIN>`.
- **workbench** `1_base/workbench/workbench/cli/wb_share.py:18` (Keep it general): Docstring lists the personal share domains by name. Fix: Same placeholder as the skill.
- **haipipe-design** `2_theme/design/haipipe-design/SKILL.md:73` (Commands that do not run): `design_ladder.py release ... --from "M01 m2"` does not exist; the script's levels are block, book, method, job, task, run, goals, audit, update (design_ladder.py:444). Fix: Replace with the real release path (haipipe-design-delivery `release.py`).
- **all** `(system python3 = 3.9.6)` (Commands that do not run): SKILL.md files say `python3 <script>`, but 7 named scripts need 3.10+ and fail on the Mac's python3 with `TypeError: unsupported operand |` (draw_logic_tree.py, cli/check.py, design_ladder.py, release.py, summary.py, servers/_host/serve.py); `page.py` refuses below 3.11. Fix: Write one runner line per skill: `uv run --python 3.13 --with pyyaml python <script>`.
- **haipipe-insight-meta** `2_theme/insight/folder-kinds/haipipe-insight-meta/SKILL.md:56` (Broken links and stale names): Links `../../haipipe-insight/ref/partition.md`, renamed to `segment.md` (also :113, and haipipe-insight-workflow ref/segment-policy.md:4). Fix: Point at ref/segment.md.
- **haipipe-draft** `1_base/draft/haipipe-draft/SKILL.md:914` (Broken links and stale names): `ref/Run-cards.md` is named as the six-field Run statement; no such file. Fix: Restore the file or point at haipipe-run.
- **haipipe-design** `2_theme/design/haipipe-design/SKILL.md:13` (Clarity from a fresh context): Cold score 2: `block` scaffold never shown in SKILL.md (only the script docstring); "launch a Job" never mapped to a Run; version 0.4.0 at :43 vs 0.4.2 in frontmatter. Fix: Add a 5-line "new Block" route.
- **haipipe-task** `1_base/task/haipipe-task/SKILL.md:72` (Clarity from a fresh context): Cold score 2: never says how to create a Task; the scaffold writes `task-kind:` and no scripts/, runs/ (new_job.py:94) while the face contract wants `task-type:`. Fix: Add "new Task" route; align new_job.py output with the contract.
- **haipipe-display** `1_base/display/haipipe-display/SKILL.md:137` (Clarity from a fresh context): Cold score 2: two preview recipes (SKILL.md:137 vs _parts/table/PART.md:199) and two reviewers (fresh agent :64 vs a Codex MCP model in PART.md:73, :223). Fix: One recipe, one reviewer, stated in the door.
- **describe-food** `plugins/haipipe-utils/skills/describe-food/SKILL.md:123` (Clarity from a fresh context): Cold score 2: two confidence vocabularies (MEASURED/ESTIMATED/MISS, "PARTIAL retired") vs GOOD/PARTIAL/MISS at :349-354; five vs six nutrients (:139 vs :229). Fix: Keep one vocabulary; delete the other block.
- **haipipe-draft** `1_base/draft/haipipe-draft/tests` (Tests): 20 failed of 972. Tests read `haipipe-task/ref/check_task_tree.py` (moved to scripts/); 5 Evidence tests expect `bound` and get `blocked`; design snapshot tests drift. Fix: Fix test paths first; then rerun.
- **haipipe-draft** `1_base/draft/haipipe-draft/SKILL.md` (File size): 1,338 lines (limit 700). Its src/ holds body.py 1,724, page_question.py 1,446, dialect_paper.py 1,250, plan_shape.py 1,199. Fix: Split by route: Face, Run Spec, steps, file-to-page.
- **haipipe-paper-assemble** `2_theme/paper/haipipe-paper-assemble/SKILL.md` (File size): 865 lines; scripts latex_room_to_docx.py 1,875 and build_delivery.py 1,783. Fix: Move each delivery lane to ref/<lane>.md.
- **haipipe-paper-story** `2_theme/paper/haipipe-paper-story/SKILL.md` (File size): 782 lines. Fix: Move Roadmap and Narrative to ref/.

### Medium

- **haipipe-draft** `1_base/draft/haipipe-draft/ref/standalone.md:34` (Keep it general): Names Physician-SPACE and its Tailscale origin as the hosting rule. Fix: Say "the configured origin (`DOMAIN`)".
- **haipipe-interaction** `1_base/workbench/haipipe-interaction/SKILL.md:364` (Keep it general): "the Tailscale origin, never localhost" names one deployment's network. Fix: "the SPACE's configured origin".
- **describe-food** `plugins/haipipe-utils/skills/describe-food/SKILL.md:22` (Keep it general): One data partner is named 23 times as the benchmark and ground truth (:102-105, :367-381); same in describe-exercise:80, describe-medication, describe-insulin. Fix: Name the data as "a partner app log (dataset T0)"; keep partner names in that SPACE.
- **haipipe-draft** `1_base/draft/haipipe-draft/SKILL.md:105` (Commands that do not run): Commands use `.venv/bin/python` and `Tools/plugins/...`; Tools-SPACE has no `.venv` and `plugins/` sits at the root. Same pattern in haipipe-interaction and haipipe-discovery (`Tools/references/aris`). Fix: Say once: run from a SPACE (`Tools/` prefix) or from Tools-SPACE (no prefix).
- **haipipe-insight** `2_theme/insight/haipipe-insight/SKILL.md:65` (Commands that do not run): `--check` reads like a script flag but insight_ladder.py has none (:861-888); ref/update.md mixes `uv run` (:17) and bare `python` (:34, :57). Fix: Name it "stop after step 2"; one runner line.
- **haipipe-block** `1_base/project/haipipe-block/ref/board-contract.md:93` (Commands that do not run): `new_job.py <block> --slug` misses the required `job` subcommand and `--title`. Fix: Copy the real call from new_job.py --help.
- **haipipe-paper-assemble** `2_theme/paper/haipipe-paper-assemble/SKILL.md:158` (Broken links and stale names): `ref/word.md` is not in the skill's ref/ (holds only build.py.wrapper, paper-build.toml.example). Fix: Link the delivery skill's word ref.
- **workbench** `1_base/workbench/workbench/SKILL.md:163` (Broken links and stale names): Names `haipipe-project-meeting` as the owner of meetings; no such skill (meetings are haipipe-related). Fix: Say haipipe-related.
- **table-papers** `0_utils/table-papers/SKILL.md:57` (Broken links and stale names): `ref/papers/README.md` (license list) does not exist. Fix: Add it or drop the line.
- **haipipe-paper, haipipe-task** `2_theme/paper/haipipe-paper/SKILL.md:13` (Broken links and stale names): Cites "AGENTS.md rule 6 / rule 9" (also :15; haipipe-task SKILL.md:31, :96). AGENTS.md has no numbered rules and no hash rule. Fix: Quote the rule or name its AGENTS.md section.
- **haipipe-draft** `1_base/draft/haipipe-draft/SKILL.md:395` (Clarity from a fresh context): Cold score 2: the "file to page" route starts at line 395 of 1,338; :458 says rerun setup but standalone.md:85 says rerun refuses without `--force`. Fix: Split (see Size); put routes first.
- **haipipe-discovery** `2_theme/discovery/haipipe-discovery/SKILL.md:20` (Clarity from a fresh context): Cold score 2: ~15 required reads across 4 skills before "add a paper"; `add` has no script; scope roots (:342) omit `discovery/`. Fix: A minimum-read list per task; add discovery/.
- **hash rule** `2_theme/paper/haipipe-paper/SKILL.md:15` (Clarity from a fresh context): haipipe-paper bans every content hash; haipipe-insight (update.md:46, :73) and haipipe-design (ref/design-ladder.md rules 3-4) pin sha256. Fix: Decide once in AGENTS.md; align the three.
- **haipipe-draft-workflow** `1_base/draft/haipipe-draft-workflow/tests` (Tests): 7 failed of 23: tests grep haipipe-run SKILL.md for text it no longer has (`run-structure-`, `Closed records`, `interactive-writing-run.md`). Fix: Point the contract tests at the ref files that now hold it.
- **haipipe-paper-assemble** `2_theme/paper/haipipe-paper-assemble/tests` (Tests): 34 failed without python-docx; 5 still fail with it (JAMA eTable labels, equations). Fix: Name python-docx in the test runner line; fix the 5.
- **haipipe-paper-draft, haipipe-draft-workflow, haipipe-paper-ideation** `2_theme/paper/haipipe-paper-draft/SKILL.md` (File size): 693, 655 and 647 lines: one edit from the limit. Fix: Split before the next change.
- **all** `(82 files)` (File size): 82 readable files at 700+ lines and 27 at 600-699 inside skill folders (code, tests, refs); largest: excalidraw-job job_drawing.py 1,757, job_ladder.py 1,713, excalidraw-task task_drawing.py 1,616, haipipe-interaction collect.py 1,479. Fix: Split the part you touch, per AGENTS.md.
- **haipipe-design, haipipe-ui, haipipe-studio** `2_theme/design/haipipe-design/SKILL.md:3` (Frontmatter and triggers): Descriptions over 1,024 characters (1,234; 1,195; 1,072). Hidden excalidraw-slide, -story, -studio, -workflow are 1,191 to 1,528. Fix: Cut to what and when; move the rest into the body.
- **display, draft, paper, design, labeling** `1_base/display/ref` (Family shape): Non-skill folders at family root, not under a door's _parts/: display/ref, draft/pages-example, paper/venue, paper/tests, design/venue, labeling/engine. Fix: Move each under its door's _parts/ or ref/.

### Low

- **many** `(651 lines across skills)` (Keep it general): 651 `JL <date>` provenance tags in SKILL.md text; haipipe-ui alone has 53. Allowed in docs, but they cost tokens and name one person. Fix: Move dated provenance to CHANGELOG.md when a file is next touched.
- **haipipe-individual-inference-judge** `1_base/task/4_individual/haipipe-individual-inference-judge/scripts/judge_report_cli.py` (Commands that do not run): Needs `claude_agent_sdk`, not named in the skill; same for haipipe-individual-inference-report. Fix: List the dependency next to the command.
- **haipipe-discovery** `2_theme/discovery/haipipe-discovery/SKILL.md:114` (Broken links and stale names): Puts `_parts/` under workbench-discovery; the folder is in haipipe-discovery. Fix: Fix the path.
- **haipipe-interaction** `1_base/workbench/haipipe-interaction/SKILL.md:53` (Clarity from a fresh context): "Choose a version" listed as "not yet" while :51 and :174 say choices are built. Fix: Drop the stale row.
- **haipipe-block** `1_base/project/haipipe-block/SKILL.md:74` (Clarity from a fresh context): Cold score 4: two items numbered 5 (:74, :76); singular vs plural world folders in board-contract.md:10 vs :107. Fix: Renumber; one folder spelling.
- **paper fragments** `2_theme/paper/tests/test_import_fragments.py` (Tests): 2 failed: expect `S1` sentence ids; another session is renaming S to s tonight. Fix: Recheck after the rename lands.
- **haipipe-individual-inference-*** `1_base/task/4_individual` (Tests): 2 collection errors: `claude_agent_sdk` not installed. Fix: Mark as optional or skip when absent.
- **haipipe-paper-venue** `2_theme/paper/venue/bank/1-QBv-desks` (File size): 16 venue desk files of 700 to 1,384 lines (data). Out of scope if treated as data; say so in the folder README. Fix: Mark the bank as data.
- **haipipe-task-for-*, call-peer** `1_base/task/1_data/haipipe-task-for-data/SKILL.md:3` (Frontmatter and triggers): Seven task-type skills (data, algo, endpoint, individual, eval, display, stata) and call-peer have no Use or Trigger clause; reached only through haipipe-task. Fix: Add "Use when task-type: X".
- **triggers** `(descriptions)` (Frontmatter and triggers): Trigger words shared by 2+ skills: "propose a question" (ask-questions, haipipe-insight-question, haipipe-report), "run spec" (haipipe-draft, haipipe-draft-workflow, haipipe-run), "workflow" (haipipe-paper-workflow, haipipe-run), "draft folder", "page context", "design handoff", "claim". Fix: Keep each phrase on one owner.
- **aliases** `~/.claude/skills` (Frontmatter and triggers): Four skills install under a second link name (wb, haipipe-collect, haipipe-paper-display, haipipe-discovery-search); fresh agents saw `haipipe-collect (haipipe-interaction)` and paused. Fix: Keep the alias in the description only.
- **task family** `1_base/task/1_data/SKILLSET_REVIEW.md` (Family shape): Review notes left at family level (task/DESIGN.md 666 lines, 1_data/SKILLSET_REVIEW.md, 3_end/LESSON.md) and task/agents/CODE_REVIEW.md naming a retired haipipe-task-builder-agent. Fix: Move to diagnostics/ or delete.

## 3. Ten fixes to do first

1. **Remove the person's name**: haipipe-draft SKILL.md:106, :119: `--author "<Author>"`.
2. **Generalize the share door**: workbench SKILL.md:28-47 and wb_share.py:18: `<space>.<DOMAIN>`, no SPACE list.
3. **Fix the fake command**: haipipe-design SKILL.md:73: replace `release --from` with the real path.
4. **One runner line**: Every script command: `uv run --python 3.13 --with pyyaml python ...`.
5. **Fix 5 dead links**: partition.md→segment.md (3 places), Run-cards.md, word.md, papers/README.md, haipipe-project-meeting.
6. **Fix test paths**: haipipe-draft tests: ref/check_task_tree.py → scripts/; rerun the 20.
7. **Split haipipe-draft**: 1,338-line SKILL.md into door + ref/ per route.
8. **One vocabulary**: describe-food: one confidence scale, one nutrient count.
9. **One display loop**: haipipe-display: one preview recipe and one reviewer in the door.
10. **Settle the hash rule**: AGENTS.md: decide; align haipipe-paper, insight, design; drop "rule 6/9".

## 4. Tests run

```text
1_base/display/haipipe-display/_parts/slide/tests :: 4 passed
1_base/display/haipipe-display/tests :: 4 passed
1_base/draft/haipipe-draft-review/tests :: 12 passed
1_base/draft/haipipe-draft-workflow/tests :: 7 failed, 16 passed, 72 subtests passed
1_base/draft/haipipe-draft-writing/tests :: 12 passed
1_base/draft/haipipe-draft/tests :: 20 failed, 949 passed, 3 skipped, 101 subtests passed
1_base/evidence/haipipe-evidence/tests :: 3 passed
1_base/excalidraw/excalidraw-ideation/tests :: 3 passed
1_base/excalidraw/excalidraw-job/tests :: 33 passed
1_base/excalidraw/excalidraw-slide/tests :: 10 passed
1_base/excalidraw/excalidraw-story/tests :: 8 passed
1_base/excalidraw/excalidraw-studio/tests :: 10 passed
1_base/excalidraw/excalidraw-task/tests :: 4 passed
1_base/excalidraw/excalidraw-workflow/tests :: 9 passed
1_base/ideation/haipipe-ideation/tests :: 35 passed, 14 subtests passed
1_base/project/haipipe-block/tests :: 8 passed
1_base/project/haipipe-job/tests :: 11 passed
1_base/project/haipipe-mindmap/tests :: 33 passed
1_base/project/haipipe-project/tests :: 19 passed
1_base/project/haipipe-report/tests :: 17 passed
1_base/project/haipipe-run/tests :: 26 passed
1_base/project/haipipe-studio/tests :: 41 passed
1_base/task/4_individual/haipipe-individual-inference-judge/tests :: 1 error
1_base/task/4_individual/haipipe-individual-inference-report/tests :: 1 error
1_base/task/haipipe-task/tests :: 10 passed, 39 subtests passed
1_base/workbench/haipipe-interaction/tests :: 26 passed
1_base/workbench/workbench/tests :: 7 passed
2_theme/design/haipipe-design-delivery/tests :: 13 passed
2_theme/design/haipipe-design-goal/tests :: 8 passed
2_theme/design/haipipe-design-method/tests :: 12 passed
2_theme/design/haipipe-design-unit/tests :: 62 passed, 4 skipped, 16 subtests passed
2_theme/design/haipipe-design-workflow/tests :: 4 passed
2_theme/design/haipipe-design/tests :: 12 passed
2_theme/discovery/haipipe-discovery/tests :: 103 passed, 10 subtests passed
2_theme/insight/folder-kinds/haipipe-insight-question/tests :: 1 passed
2_theme/insight/haipipe-insight-check/tests :: 49 passed
2_theme/insight/haipipe-insight-workflow/tests :: 5 passed
2_theme/insight/haipipe-insight/tests :: 20 passed
2_theme/paper/haipipe-paper-assemble/tests :: 34 failed, 94 passed, 1 skipped
2_theme/paper/haipipe-paper-evidence/tests :: 29 passed
2_theme/paper/haipipe-paper-related/tests :: 7 passed
2_theme/paper/haipipe-paper/tests :: 19 passed
2_theme/paper/tests :: 2 failed, 47 passed
plugins/haipipe-utils/skills/haipipe-norm/eventnorm/tests :: no tests ran
2_theme/paper/haipipe-paper-assemble/tests (rerun with python-docx) :: 5 failed, 126 passed
```

Paths in findings are relative to `plugins/haipipe-toolkit/skills/` unless they start with `plugins/`.
