# fixes for round one

## Ask

fix p01's two problems (first Files panel over 1 s; Block UI left tab freezing the page), then bench again

## Summary

Freeze fixed and seen in Chrome: a Block UI section's script that keeps the pages and walks on the same tab was sent five times, so one click fired five listeners that clicked every same-length tab list again, multiplying; and the Elements sections' many two-tab lists all flipped, each loading a live page. Now it installs once and leaves Elements alone: the click takes 39 ms, only its own preview loads. Panel: trace headers parse with libyaml (0.13 s to 0.012 s for 110 files), git skips submodules, and its answer is kept 10 s so a slow build does not ask git again per trace. The numbers below were taken with the machine's load average at 35 to 54 (other sessions), so they are not comparable to p01; dirty() left the slowest five. Rerun on a quiet machine.

## Results

```text
| Block | Files panel (first) | Block page (first) | page size | style+script blocks | repeated |
| --- | --- | --- | --- | --- | --- |
| b17_theme_work | 3.73 s (2.10) ❗ | 3.93 s (4.38) ❗ | 1105 KB | 73 | 65 KB |
| b11_theme_insight | 2.38 s (0.40) ❗ | 0.09 s (1.23) | 409 KB | 50 | 6 KB |
| b16_theme_paper | 0.94 s (1.40) ❗ | 0.11 s (2.40) ❗ | 613 KB | 51 | 6 KB |

limits: panel 1.0 s, page 1.5 s, page 1200 KB, repeated 100 KB

slowest functions while b17_theme_work's Files panel renders (cumulative):
- 11.917 s  workbench/page/block_index_page/focus_render.py:379 section_body
- 11.288 s  workbench/page/job_task_views/work_frame.py:457 shared_bodies
- 6.618 s  workbench/side_pane/files_tree/work_files.py:342 render
- 6.192 s  workbench/side_pane/files_tree/trace_view.py:208 render
- 3.219 s  workbench/page/job_task_views/work_frame.py:435 scope_skills
```

## Changed

- plugins/haipipe-toolkit/servers/workbench/page/parts_and_map/focus_ui.py
- plugins/haipipe-toolkit/servers/workbench/side_pane/files_tree/trace_view.py
- t03_pane_speed/scripts/bench_pane.py (waits past the 10 s cache)
