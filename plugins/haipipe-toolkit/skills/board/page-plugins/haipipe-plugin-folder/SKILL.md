---
name: haipipe-plugin-folder
description: >-
  The 📂 Folder tab of a Board page: the live inventory surface, one row per
  plugin subfolder with file count, weight, age, and a ⚠️ STALE flag when a
  derived plugin predates the page's .md. Stores nothing, renders live.
  Trigger: folder plugin, folder tab, what does this page hold, stale plugin,
  folder inventory, /haipipe-plugin-folder.
metadata:
  version: "0.3.0"
  last_updated: "2026-09-02"
---
# /haipipe-plugin-folder · the folder is the truth

**LOAD `haipipe-plugin` FIRST.** It owns what any plugin is: storage, surface, writer, boundary.
This file owns only folder's delta, and the delta is an inversion: every other plugin is a subfolder the tab surfaces, and this one is the tab that surfaces the subfolders.

## 🗂 Storage · none, and none is the contract

There is no `folder/` subfolder, and one appearing on disk would be a mistake, not a feature.
The plugin's material is the page folder ITSELF: every sibling's subfolder is what this surface reads, so it holds no roster row — the roster lists subfolder names, and this is the view OVER them.
A status has no artifact: written to disk it starts aging the moment it lands, and a stale page about staleness would be the board's best joke at its own expense — so nothing is ever stored, and the render is live every time.

## ⚖️ The one law · staleness is claimed narrowly

Only a DERIVED lane — `delivery/latex` `delivery/word` `outline/evidence/bibex`
`delivery/slide` `outline/evidence/display` — can be ⚠️ STALE, and it is stale
exactly when its newest file predates the page's `.md`.
Source material (`studio/draw` `studio/chat` `meeting` `skill`) is often older
than the prose and that is HEALTHY: it gets an age, never a warning.
Widening the flag to source folders would train readers to ignore it, which is the one way a staleness signal dies.

## 📡 Surface · explicit lanes, live on every open

The 📂 tab follows 🧭 Outline, 🎨 Studio, ⚙️ Runs, and 📤 Delivery. This keeps
the paper workflow first and the supporting inventory afterward; an explicit
registry `order` makes the sequence independent of asset filenames. Folder
still tells a reader "no deck" from "deck built, tab unopened".
It applies only to a FOLDED page (`<stem>/<stem>.md`); a flat page has no folder to show.
`GET /_board/folderstat?path=…&file=…` renders one row per material lane — icon
· exact path · file count and weight · newest age · state (⚠️ STALE / ✅ fresh
/ source material) — plus a ⬜ not-present line for categories the folder lacks.
`outline/` counts only the process files it directly owns; each existing
`outline/evidence/<lane>/` is a separate row. Delivery likewise shows
`delivery/latex/`, `delivery/word/`, `delivery/slide/`, and `delivery/render/`.
No aggregate parent row recursively double-counts the files shown beneath it.
A row is a door, not just a gauge (JL 260816): clicking it unfolds the folder in place, ▸ turning ▾, and every file is a link that opens the served file itself in a new browser tab, so the status view is also the folder's browser.
The unfold shows STRUCTURE, not a path list: files a level owns come first, then one 📁 branch per subfolder with its own file count, indented by depth (JL 260816: a flat alphabetical list buried a folder's shape, and `display/` spelled every unit's inner path on every line).
A file that is a symlink wears a bare 🔗 with its full target on hover, because the row reports the RESOLVED file and a borrowed page md would otherwise read as duplicated bytes.
Fresh is a two-layer contract (JL 260816): the server sends no-store, and the shell's landing reloads the frame even when the URL is unchanged — one URL per page means "same src" is the common case, and skipping it is how a live view goes stale in the frame while staying fresh on the wire.
A ⚠️ STALE row of a MECHANICAL writer (latex, word, bibex, display) carries ♻ rebuild: one click fires that plugin's own POST and re-renders (JL 260816: "could we update them along the time?"). display joined the same day (JL: "I want to add the rebuild button"): its POST recompiles each unit's DERIVED preview.tex ▶ preview.pdf and touches no intake, recipe, or accepted: tick. slide alone stays a pointer — a compile may be a button reflex, an AUTHORED artifact (claude -p, minutes, money) never is.
The header carries the same pill the Word and LaTeX views wear: 🔄 rebuild stale (n) walks every curable row in sequence — never in parallel, the writers share the folder and xelatex is not a thing to race — and the pill renders only while something mechanical is actually stale (JL 260816).

## ⚙️ Writer · a twin that writes nothing

`POST /_board/folderstat` exists only so the shell's `tab: {url, write}` contract holds; it returns the live URL and lands not one byte.
No route may ever cache or persist this view — the no-store header is part of the contract, not a tuning choice.

## 📂 Files

- `../../haipipe-board/live/folderstat.py`
  The live walk, the staleness rule, the GET and its no-write POST twin.
- `../../haipipe-board/assets/js/10-drawer/06-plugin-folder.js`
  The registration: ordered after Delivery, folded pages only.
- `../../haipipe-plugin/ref/roster.md`
  The list this surface renders the truth of — the one skill here with no row of its own.
