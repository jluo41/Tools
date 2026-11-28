# first speed round

## Ask

the baseline: bench b17, b11 and b16 on a fresh 5623 after the git-once and style-once fixes

## Summary

One row over a limit: b17's first Files panel after a restart takes 1.01 s, because every trace's front matter (105 files) is parsed once on the first visit (trace_view.traces, 0.43 s); after that it is 0.59 s. Pages answer in 0.3 to 0.8 s on a first visit and are kept after that; b17's page is 1.1 MB with 65 KB still repeated. In the browser, clicking a left tab under b17's Block UI › Elements froze the page for about 30 s (also without the style-once fix): open, next to fix.

## Results

```text
| Block | Files panel (first) | Block page (first) | page size | style+script blocks | repeated |
| --- | --- | --- | --- | --- | --- |
| b17_theme_work | 0.59 s (1.01) ❗ | 0.04 s (0.83) | 1098 KB | 73 | 65 KB |
| b11_theme_insight | 0.14 s (0.14) | 0.04 s (0.29) | 405 KB | 50 | 5 KB |
| b16_theme_paper | 0.19 s (0.30) | 0.03 s (0.77) | 612 KB | 51 | 5 KB |

limits: panel 1.0 s, page 1.5 s, page 1200 KB, repeated 100 KB

slowest functions while b17_theme_work's Files panel renders (cumulative):
- 1.189 s  workbench/page/block_index_page/focus_render.py:379 section_body
- 1.176 s  workbench/page/job_task_views/work_frame.py:457 shared_bodies
- 0.866 s  workbench/side_pane/files_tree/work_files.py:326 render
- 0.843 s  workbench/side_pane/files_tree/trace_view.py:207 render
- 0.427 s  workbench/side_pane/files_tree/trace_view.py:58 traces
```

## Changed

<nothing>
