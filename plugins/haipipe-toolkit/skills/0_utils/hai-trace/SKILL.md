---
name: hai-trace
description: "/hai-trace: one piece of work kept as a trace file in its Block, plan first. Write the plan (which files, what change), let the person see it in the Files pane and confirm, change the files, record what changed, close with Check and Summary. Use before changing files for a request, to add a prompt, record changes or close. Trigger: trace, plan first, what will you change, close the trace, /hai-trace."
---

# /hai-trace · plan first, then change, then close

Read [CONSTITUTION.md](CONSTITUTION.md) first; it wins over this file.

A trace is one piece of work with one aim. It can take many prompts. It lives in the Block the work is for:

```text
<Block>/trace/<YYMMDD>/<HHMM>_<slug>.md      named for the time of its first prompt
```

## The loop

```text
new (plan) ─▶ the person sees it in Files ─▶ confirm ─▶ change files ─▶ changed ─▶ close (Check, Summary)
```

1. **Plan first.** Before any file changes, write the trace with its aim and plan: one line per file (`do`: add, edit, move or delete; `path` from the SPACE root; `what` the change is). Show the list and wait for the person's confirm.
2. **Show it.** The Files pane marks every planned file (◌), a file still to create (+), and opens the tree down to them. The Trace button (highlighter) lights the trace's files, and its name opens the trace's content.
3. **Change.** Only the confirmed files. A file the plan left out shows as ◆ (off the plan); say so.
4. **Record.** Add every prompt that worked toward the aim, in the person's words, and list what changed.
5. **Close.** Write Check (what was run or looked at, with the numbers) and Summary (one paragraph), then close.

## The reply

The person reads the reply, not the trace, so each step's reply says the files.

**Before any change** (after `new`), the reply ends with:

```markdown
- `path/from/the/SPACE/root` (where): the change, 8 words or fewer
- `<Block>/trace/<YYMMDD>/<HHMM>_<slug>.md`: this plan, already written
```

every planned file one line, then one line asking for the go. No file changes until the person says go (yes, go, do it).
A new ask that adds a file adds it to the plan and the list, and waits again.

**After the change** (after `close`), the reply says what changed and how it was checked: the files that changed, one line
each, 👀 on the one to look at, the checks with their numbers (tests, the page in Chrome), and the trace closed.


```markdown
---
title: metro zoom
date: 2026-11-25 17:49
topic: s31-files-pane            # the Studio topic it serves, if any
aim: "One sentence: what is true when it is done."
closed: false
plan:
  - do: edit
    path: plugins/.../side_pane/files_tree/trace_view.py
    what: three zoom levels
changed:
  - plugins/.../side_pane/files_tree/trace_view.py
---

# metro zoom

## Prompts

- **17:49** the person's words, as typed

## Check

- what was run or looked at, with its result

## Summary

One paragraph.
```

Quote the `aim:` value: a colon inside it breaks the front matter.

## The script

`scripts/trace.py` does each step, so no trace is written by hand. Run it from the SPACE root.

```bash
python3 <skill>/scripts/trace.py new <Block> --slug metro_zoom --title "metro zoom" \
    --aim "The metro zooms by day, by trace and close up." \
    --plan "edit|plugins/.../trace_view.py|three zoom levels" --prompt "how could I zoom in and out?" [--topic s31-files-pane]
python3 <skill>/scripts/trace.py prompt <trace.md> "the person's words" [--at 17:52]
python3 <skill>/scripts/trace.py changed <trace.md> [--also path ...]   # from git: plan files that changed, plus --also
python3 <skill>/scripts/trace.py close <trace.md> --check "tests: 240 passed" --summary "One paragraph."
python3 <skill>/scripts/trace.py check [<glob>]                          # every trace parses; closed ones are complete
```

`new` writes the front matter with a YAML writer, so a colon or quote in the aim cannot break it. `check` fails on any trace with no aim or plan, a plan line without `do`, `path` and `what`, or a closed trace with an empty Check or Summary.

## Where it shows

The Files pane (`servers/workbench/side_pane/files_tree/trace_view.py`) reads every trace of the Block: marks on the tree, the metro map beside it, the Trace button, and the trace's content under its name. How the pane draws them is hai-ui's rule (its trace-plan-and-states article). This skill owns the trace file and the loop.
