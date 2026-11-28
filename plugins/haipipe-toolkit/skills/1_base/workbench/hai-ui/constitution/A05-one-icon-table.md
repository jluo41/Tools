# A05 · A file's icon comes from one table; a type with its own mark shows that mark

> "could you also give the good icon for each type of files here? what is your thoughts?" (JL 261124, Files pane)
> "this should be python icon, not this one" (JL 261124, on 🐍 beside a .py file)
> "I think we can use the same system as we used in the folder panel, right? it can also be sharing" (JL 261126, on ✅ 🙋 beside a Task row)

## 1. Need
In any file tree, JL sees what a file is before reading its name; a Python file shows Python's own mark.

## 2. Now
Before: `frame_folders.py` kept its own `FILE_ICONS`, `work_files.file_node` drew no type at all, and the first
shared table gave `.py` the 🐍 emoji. Now `servers/workbench/side_pane/files_tree/file_icons.py` holds `FILE_ICONS`, `FILE_MARKS`
(`.py` → an inline SVG in Python's blue and yellow) and `file_icon(path)`; every tree calls it.

## 3. Gap
Each tree chose its icons in its own module, so a fix in one never reached the other, and an emoji was taken as
good enough for a type that has a real mark.

## 4. Methods
1. Fix the .py icon in each tree: rejected, the next tree would choose again.
2. One table every tree imports, with real marks drawn inline beside the emoji table: chosen.
3. An icon font: rejected, one more asset to serve, and still emoji for the rest.

## 5. Update
- `side_pane/files_tree/file_icons.py`: one table, `FILE_MARKS` for real marks
- `side_pane/files_tree/work_files.py`, `side_pane/files_tree/frame_folders.py`, `side_pane/files_tree/trace_view.py`: call `file_icon`
Cases: ✅ Files pane · ✅ Studio › Folder · ✅ trace trees · ✅ every other server module (scanned).
Run: `folder_icons_check.py` → `✅ folder icons: 2 trace files, 0 problems`.

## 5b. State marks (261126)
A state's mark is one table too: `page/parts_and_map/state_marks.py` holds `STATE_MARKS` (the Files pane's plan, edit,
done, off, kept, and a row's you, new, void, one 12px circle family) and `state_key(state)`. `file_icons.py` re-exports
it; `ui_parts.state_mark` draws from it with its `fx-<key>` class, and focus.css gives each its effect (done pops once,
running breathes and sweeps, waits for you pings, new fades with a plus, void is struck). A Task or Run git does not
track yet is new (`focus_plan_results.git_new`). Before: `state_mark` printed the emoji (✅ 🙋 ⬜) and kept the words
"waiting for you" beside a waiting row.

## 6. Never again
`folder_icons_check.py` fails on any server module but `file_icons.py` that maps a suffix to an icon, on a .py
that is not Python's mark, and on any server module but `state_marks.py` that draws a state mark. `/hai-stack sweep` reruns it.
