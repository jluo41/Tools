# File formats: one row per kind of file a Block holds

Each row: where the file sits, what it must hold, the one script that writes it, the page code that reads it, and where
its rule is written. t02_render_check renders every real file of each kind through that page code (`servers/workbench/checks/render_check.py`, which names the same kinds); a kind with no
writer or no page code is a gap to close, not a row to drop.

| Kind | Where | Holds (fields · sections) | Writer | Page code (servers/workbench/) | Rule |
| --- | --- | --- | --- | --- | --- |
| Block face | `bNN_<block>/board.md` | `# bNN · title`; `board-kind`, `spine`, `close`, `bands`, `theme`/`workbench`, `ui-<level>:` lines; `## Topic`, `## Questions`, `## Related resources` | `hai-block/scripts/new_board.py` | `page/block_index_page/focus_base.py` `read_face`, `focus_page.py` | `hai-block/ref/board-contract.md` |
| Job face | `jNN_<job>/jNN_<job>.md` | `# jNN · title`; `goal`, `close`, `bands`, `emoji`, `answers`; `## Topic`, `## Tasks` (numbered, one per Task folder), `## Deliverables` | `hai-job/scripts/new_job.py job` | `frame_base.py` `children`, `page/job_task_views/focus_plan_results.py` `tasks_section` | `hai-job/ref/job-contract.md` |
| Task face | `jNN/tNN_<task>/tNN_<task>.md` | `# title`; `state`, `goal`, `close`, `owner`, `folder-kind`, `task-type`; `## Files`, `## Checks` | `hai-job/scripts/new_job.py task` | `focus_base.py` `read_face`, `focus_plan_results.py` `task_name`, `side_pane/files_tree/focus_scope.py` `owns` (reads `## Files`) | `hai-task/SKILL.md` |
| Run card | `runs/run-<type>-<target>/run.yaml` + `run-<type>-<target>.md` | `run`, `kind`, `type`, `target`, `ticket`, `skill`, `agent`, `signs`, `status`, `passes`, `writes`, `feeds`; ticket: `target`, `ask`, `close` | `hai-run/scripts/soft_run.py new` | `page/job_task_views/focus_runs.py` `run_rows` | `hai-run/ref/identity-and-history.md` |
| Run round (pass) | `runs/<run>/passes/pNN-MMDD/pass.md` | `# title`; optional front matter `session`, `provider`, `date`, `goal`, `paths`, `cards`; `## Ask`, `## Summary`, `## Changed` | `hai-run/scripts/soft_run.py pass` | `focus_plan_results.py` `round_rows`, `side_pane/rail_sections/frame_sessions.py` | `hai-run/ref/identity-and-history.md` |
| Trace | `bNN/trace/YYMMDD/HHMM_<slug>.md` | front matter `title`, `date`, `aim`, `topic`, `work`, `closed`, `plan` (do · path · what), `changed`; `## Prompts`, `## Check`, `## Summary` | `0_utils/hai-trace/scripts/trace.py` | `side_pane/files_tree/trace_view.py`, `file_info.py` | `hai-trace/SKILL.md`, hai-ui A07 |
| Studio topic face | `sNN-<topic>/sNN-<topic>.md` | `# sNN · title`; `view:`; `**Tags:**`, `**Stage:**`, `**Why:**`, `**Topic:**`, `**Feeds:**`, `**Answer:**`, `**Evidence:**`, `**Limits:**`, `**Delivery type:**` | `hai-studio/scripts/new_topic.py` | `side_pane/rail_sections/focus_studio.py`, `studio/tabs/studio_tabs.py` | `hai-studio/ref/topic-face.md` |
| Page spec views table | `bNN/delivery/page-spec/<level>-views.md` (and `-elements.md`, `view-guide.json`, `example-types.json`) | one table per level: view · sections · what each shows; elements: `# type`, `## view`, `### part` with `show:`, `view:`, `folder:`, `code:` | the Block's Job (j03 for b17); `-elements.md` by `page/element_marks/ui_elements_harvest.py` | `page/parts_and_map/focus_ui.py`, `ui_docs.py`, `focus_ui_elements.py` (all through `page_spec.spec_dir`) | `page/parts_and_map/page_spec.py` docstring |

## Gaps seen while writing it (261126)

- The Run card and pass of `j12/t03_pane_speed` were written by hand, not by `soft_run.py`: nothing checks they match its format.
- The Task face's rule lives only in `hai-task/SKILL.md` prose; it has no field table like the Block's and the Job's contracts.
- The page spec's `<level>-views.md` has no written format beyond the code that parses it.
