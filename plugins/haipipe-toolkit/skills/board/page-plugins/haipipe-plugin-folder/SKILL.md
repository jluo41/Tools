---
name: haipipe-plugin-folder
description: >-
  The 📂 Folder tab of a Board page: the rail's FIRST surface, showing what the
  page's folder actually HOLDS — one row per plugin subfolder with file count,
  weight, newest age, and the ⚠️ STALE flag when a DERIVED plugin (latex, word,
  bibex, slide, display) predates the page's .md. The meta-plugin: it owns NO
  subfolder, stores NOTHING (GET /_board/folderstat renders live on every
  open), and writes nothing — its material is the folder itself. Loads
  haipipe-plugin for the four-facet contract and never restates it. Trigger:
  folder plugin, folder tab, page-folder status, what does this page hold,
  stale plugin, folder status, first tab, /haipipe-plugin-folder.
metadata:
  version: "0.2.0"
  last_updated: "2026-08-16"
  summary: "The unfold shows a folder's STRUCTURE, not a flat path list (JL 260816): owned files first, one branch per subfolder, symlinks marked."
---
# /haipipe-plugin-folder · the folder is the truth, the first tab shows it

**LOAD `haipipe-plugin` FIRST.** It owns what any plugin is: storage, surface, writer, boundary.
This file owns only folder's delta, and the delta is an inversion: every other plugin is a subfolder the tab surfaces, and this one is the tab that surfaces the subfolders.

## 🗂 Storage · none, and none is the contract

There is no `folder/` subfolder, and one appearing on disk would be a mistake, not a feature.
The plugin's material is the page folder ITSELF: every sibling's subfolder is what this surface reads, so it holds no roster row — the roster lists subfolder names, and this is the view OVER them.
A status has no artifact: written to disk it starts aging the moment it lands, and a stale page about staleness would be the board's best joke at its own expense — so nothing is ever stored, and the render is live every time.

## ⚖️ The one law · staleness is claimed narrowly

Only a DERIVED plugin — `latex` `word` `bibex` `slide` `display` — can be ⚠️ STALE, and it is stale exactly when its newest file predates the page's `.md`.
Source material (`draw` `chat` `meeting` `skill` `probe`) is often older than the prose and that is HEALTHY: it gets an age, never a warning.
Widening the flag to source folders would train readers to ignore it, which is the one way a staleness signal dies.

## 📡 Surface · first in the rail, live on every open

The 📂 tab is registered FIRST on purpose (the asset sorts at `06-`, right after the registry): the rail shows the surfaces someone built, and the first tab shows what the folder actually holds, so a reader can tell "no deck" from "deck built, tab unopened".
It applies only to a FOLDED page (`<stem>/<stem>.md`); a flat page has no folder to show.
`GET /_board/folderstat?path=…&file=…` renders one row per subfolder — icon · name · file count and weight · newest age · state (⚠️ STALE / ✅ fresh / source material) — plus a ⬜ not-present line for roster names the folder lacks.
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
  The registration: first in the rail, folded pages only.
- `../../haipipe-plugin/ref/roster.md`
  The list this surface renders the truth of — the one skill here with no row of its own.
