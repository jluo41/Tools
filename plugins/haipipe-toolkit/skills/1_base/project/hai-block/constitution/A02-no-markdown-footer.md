# A02 · No "Open this page's Markdown" line

> "why we have this? I don't think this is necesary." (JL 261124)

## 1. Need
The page ends with its content; no extra link to its own source file.

## 2. Now
`page_shell` puts `<footer>{source}</footer>` under the card. Three writers filled it with a "Source Markdown"
pop link: `focus_render.crumbs_goal_source`, `labeling_focus_frame.task_shell`, `focus_shell.py` (Studio topic Delivery).

## 3. Gap
No rule said the face is reached through Files, so each new page writer copied the link.

## 4. Methods
1. Hide the footer by CSS: rejected, the link stays in the markup and in tests.
2. Chosen: each writer passes `source = ""`; the empty footer stays as a layout anchor.

## 5. Update
- `focus_render.py`, `labeling_focus_frame.py`: `source = ""`
- `focus_shell.py`: `source = ""` (Chat-Block-Folder-Icon)
- `workbench-labeling/tests/test_decision_view.py`: expects no link

Run line exit 0; live 5623 b16 pages show no link.

## 6. Never again
The Run line greps every server writer for `"Source Markdown"`; a new copy fails it.
