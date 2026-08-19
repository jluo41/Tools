---
name: haipipe-plugin-task
description: >-
  The task/ plugin of a Board page: the fourth citation twin (bibex → literature, skill → the skill tree, pagex → other pages, this one → tasks/), a page's ranked list of task FOLDERS it is written about, materialized as relative symlinks to whole directories under <page>/task/<project>/<inner>/, with live status read off plan.yaml / report.yaml / QA/*.md — never a hand-typed word. Owns the page-side delta only: the store grammar, the directory-not-file mint rule (task's own inversion of pagex's file-not-folder rule), the tasks/-ancestor vet, and the status reader. Loads haipipe-plugin for the four-facet contract and never restates it. Trigger: task plugin, task folder link, link a task folder, task status, which task folder, task tab, /haipipe-plugin-task.
metadata:
  version: "0.1.0"
  last_updated: "2026-08-18"
  summary: "Born QPf13, alongside meeting/'s haipipe-plugin-meeting: JL wanted two new plugins, task (which task folder backs this page) and meeting (what talk backs it), added the same round."
---
# /haipipe-plugin-task · a page's own task folders, linked whole, status read live

**LOAD `haipipe-plugin` FIRST.** It owns what any plugin is: storage, surface, writer, boundary.
This file owns only task's delta: linking whole DIRECTORIES instead of files, the `tasks/`-ancestor vet, and reading status off disk.

## 🗂 Storage · a ranked list, symlinks to whole task folders

```text
<page>/task/
├── <stem>.md                 PRIMARY · one row per linked task folder, ranked
└── <project>/<inner>/        DERIVED · a relative symlink to the real folder,
                               keeping the path from the nearest `tasks/`
                               ancestor down, so two folders never collide
                               on a bare basename the way a flat layout would
```

The store's row grammar is pagex's own, one line per row:

```text
- <repo-relative path to a task folder> · note: why it is wanted
- <repo-relative path> · removed          the ✕ tombstone, never re-seeded
```

`<project>` and `<inner>` come from `_task_link_name`: walk up from the resolved
target for a folder literally named `tasks`, take its PARENT's name as the
project, and everything below `tasks/` as the inner path. A target with no
`tasks/` ancestor falls back to `<parent>/<name>`, the same shape pagex's own
minter uses when a source page sits somewhere unusual.

## 🚧 The one inversion of pagex's rule: task links FOLDERS, never files

pagex refuses a directory, because linking a page's whole home folder would
hand board discovery a ghost page. A task folder is never itself a page —
nothing under `tasks/` matches the `Q`/`S`/`Agent`/`Meeting`/`Design` name
pattern `page_files()` looks for — so the one shape that means anything here
is the opposite: **task refuses a FILE** ("a file, not a folder; task/ links
whole task folders, one row per folder") and requires the resolved path to
carry a `tasks` path segment, so a wrong path fails loud at mint time rather
than silently linking something that was never a task folder.

## 🩺 Status · read from the files, never a claim

Mirrors `plugview.py`'s `_display_state`: a badge is computed from what is
actually on disk, checked in this order —

```text
✅ reported   workflow/report.yaml (or a bare report.yaml) exists
              best-effort: the `# O: status=X` preview-comment convention,
              shown as a detail, never load-bearing
📝 planned    plan.yaml exists, report.yaml does not
❔ unknown    neither file found under workflow/ or the folder root
```

Plus, on every card: `plan.yaml` ✅/⬜, `report.yaml` ✅/⬜, a `QA/*.md` count,
and the newest file's age. None of these are typed by a person; a rebuild
re-reads them every time, the same rule the 📂 folder tab and the display/probe
plugins already follow.

## ✍️ Writer · three doors, no auto-seed

```text
/_board/task          POST   mint every row's symlink + status, re-render
/_board/task-order     POST   the drag: rank = the order
/_board/task-entry     POST   {link, note?, remove?, restore?} — the pen
```

**No scan-seed, unlike pagex.** pagex's refresh reads which PAGE IDS this
page's own prose names and seeds those rows automatically, because a page id
is a matchable token. A task-folder path is not: nothing in ordinary prose
looks like `examples/Project-X/tasks/A01_group/B02_unit` in a form a scanner
could reliably lift. So every row is typed through the ＋ pen on purpose, and
`task_refresh` only mints and re-renders what the store already holds.

## 📂 Files

- `../../haipipe-board/live/task.py`
  The whole plugin: store reader/writer, the directory minter and its vet,
  the status reader, the two POST doors, and the card view.
- `../../haipipe-board/assets/js/10-drawer/86-plugin-task.js`
  The registry entry whose `tab` spec the shell builds the 🗂 tab from.
- `../../haipipe-plugin/ref/roster.md`
  The one list of plugin names; the `task/` row there is what this page rules.
