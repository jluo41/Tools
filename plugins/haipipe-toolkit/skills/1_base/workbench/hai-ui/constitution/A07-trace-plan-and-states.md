# A07 · A trace writes its plan first, and the Files pane shows its files with their state

> "for a trace, to be recorded, what is the requirements, like we might have the plan, be clear about what to change, right? and think about what files to changed, what aims to achived, right?" (JL 261125, chat)
> "so we can have the files to be flag like before, during, and after, what is your thoughts?" (JL 261125, Files pane)
> "I want to show what files are related to this Trace, you know, could you show me the expected outcome" (JL 261125)
> "the prompt is limited, I think this prompt should be many, right? I asked many things." (JL 261125, a trace's Prompts)

## 1. Need
For each piece of work JL sees, in one file and on the tree: what it aimed at, which files it meant to change,
every prompt that drove it, which files it did change, how it was checked, and how it ended.

## 2. Now
A trace is `<Block>/trace/<YYMMDD>/<HHMM>_<slug>.md`, named for its first prompt: front matter `title`, `date`,
`aim`, `closed`, `plan` (do, path, what), `changed`; then `## Prompts`, `## Check`, `## Summary`.
`side_pane/files_tree/trace_view.py` reads a Block's traces, marks each file ◌ ◐ ●✓ ◆ (git decides committed), and gives the Files
pane a switch: Files, then one button per trace still in play (title, MM-DD).

## 3. Gap
Before, a chat kept three lines per turn (`hai-chat` cNN) with no plan, no grouping by aim, and nothing on
the tree. The first trace listed only the last prompt: prompts and `changed:` are still written by hand, because
the Stop hook does not yet write traces.

## 4. Methods
1. Keep cNN's per-turn lines: rejected, a turn is not a piece of work.
2. One file per aim, plan first, drawn on the real tree: chosen.
3. A Run per change (`run.yaml`, receipt): rejected, too heavy for a chat.

## 5. Update
- `side_pane/files_tree/trace_view.py`, `side_pane/files_tree/file_icons.py` (`STATE_MARKS`), `side_pane/files_tree/work_files.py` (switch)
- `tests/test_trace_view.py`: states, ghost rows, parts, closed and committed
- `hai-ui/scripts/folder_icons_check.py`: aim, plan lines, Check and Summary on close, the switch live
Cases: ✅ 1051_trace_view · ✅ 1748_page_subfolders (a move's new place) · ✅ 1110_folder_icons_rules · ✅ a Block with no trace · ⬜ prompts by the hook · ⬜ `changed:` by the hook.

## 6. Never again
The check fails a trace with no aim or plan, a plan line without do, path and what, a closed trace with an
empty Check or Summary, and a closed trace whose `do: move` path is not on disk.

1748_page_subfolders (261125) wrote its 78 moves with the old path in `path:`; once moved, those paths were gone,
so the Files pane drew each as a + file still to create under `page/`. A move now names the new place in `path:`
and `from <old>` in `what:` (1810_trace_move_path). Open until a Stop hook writes every prompt and `changed:` by itself (hai-chat, which had one, was retired 261126 for the trace).
