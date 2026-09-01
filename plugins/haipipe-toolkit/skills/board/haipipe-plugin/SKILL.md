---
name: haipipe-plugin
description: >-
  The PLUGIN contract of a Board page: every subfolder of a page's folder is a
  plugin, defined by four things — STORAGE, SURFACE (its tab), WRITER,
  BOUNDARY. ref/roster.md is the single list of plugin names. Trigger: page
  plugin, plugin folder, plugin roster, plugin tab, add a plugin,
  /haipipe-plugin.
metadata:
  version: "0.3.1"
  last_updated: "2026-08-31"
---

# /haipipe-plugin · a page's material, as one contract

`haipipe-page` owns what the page's `.md` SAYS; this skill owns what sits BESIDE it.
A page lives in its own home folder (QPf1 on the design board), and every subfolder of that folder is a PLUGIN.
A plugin is defined ONCE, by four things, and the roster in `ref/roster.md` is the single list of names.

## 🧩 The four things a plugin is

```
📦 STORAGE   what files live in <page>/<name>/, named by the page's stem
🖼 SURFACE   its tab in the split's right pane, framing the material live
✍️ WRITER    the ONE tool allowed to land files there
🚧 BOUNDARY  board discovery never enters a plugin folder
```

A folder that meets all four is a plugin; a folder that meets none is not board material and the checker may warn on it.
Adding plugin N+1 is one roster row plus one drawer registration — the shell is never edited for it.

## 📦 Storage

Material lands in `<page-dir>/<plugin>/`, and artifacts carry the page's stem: `QPf2-draw-attach/draw/QPf2.excalidraw`.
PRIMARY plugins hold originals a person makes (draw, chat, meeting): they are committed and only their writer edits them.
DERIVED plugins hold projections of the page's own text (slide, latex, word, bibex): they regenerate on demand, a hand edit is overwritten on the next build, and the folder is safe to gitignore.
A flat page (no home folder yet) uses the board-level `<board>/<plugin>/` fallback; folded pages are the norm and every writer lands beside its page.

## 🖼 Surface

The surface is a tab in the split shell's right pane, beside 💬 Chat.
A tab appears by EXPLICIT OPEN: the strip's ➕ menu lists this page's plugins, a ● marks the ones whose folder already has material, and clicking a row opens the tab (JL 260815).
The active tab carries its own ✕: closing removes that tab only; the pane's `✕ close` puts the whole pane away.
The open-tab set persists per page, so a reader returns to the pane the way they left it.
Frames are hidden on switch, never destroyed — a live session or editor survives being put away.
Closing is always safe by construction: a derived view has nothing to lose, an editor saves on edit, and a chat turn survives its reader through the ring.

## ✍️ Writer

Each plugin names one writer in the roster, and everything else asks it.
The drawer plugin registers `{id, label, hint, menu, applies, open, tab}` in `assets/js/10-drawer/05-plugins.js`'s registry; `tab.url(page)` names the saved artifact and `tab.write(page, cb, err)` builds one, so how an artifact is made never reaches the shell.
Server-side builders live as one `live/` module per concern and one `/_board/<plugin>` route (`live/autodeck.py` and `/_board/autodeck` are the slide's pair).

## 🚧 Boundary

Discovery (`src/common.py`) never surfaces a plugin folder's files as pages, so a `chat/` transcript full of `.md` can never become ghost pages.
The `session:` line and the page's own text stay `haipipe-page`'s; this contract begins at the folder.

## 🗂 The roster, and each plugin's own skill

`ref/roster.md` is the single list: name · kind · storage · surface · writer · status.
Plugin-vs-workflow is the registry's own test: a plugin is a surface you open beside the page; a workflow is a stepper over the page and lives in the other menu.
A plugin's OPERATING knowledge lives in its own skill under `page-plugins/haipipe-plugin-<name>/` (JL 260815: one skill per plugin, keep haipipe-board small), the same third leg `page-types/` and `page-workflows/` give the page family.
One of them inverts the shape: `haipipe-plugin-folder` is the 📂 meta-surface over the roster itself — no subfolder, no storage, no roster row (JL 260816).
This contract stays the base every one of them loads on top of; the board pages (`QPf2`-`QPf8`) stay the design records; the engine keeps only routes and machinery.

## 🗂 Category folders and the execution door (260831)

A unit folder has TWO PARTS (JL 260831 v5). The UPPER, page part: three
CATEGORY folders that group lanes without changing any lane's grammar,
writer or gate — `evidence/` (bibex · probe · display · pagex · materials —
what the page CITES, each behind its human gate), `delivery/` (latex · word ·
slide · render — what leaves the page) and `studio/` (chat · draw — the
HUMAN's room: the person talks and sketches, and the chat may redraw on
their ask) — plus outline/ and workflow/. The LOWER, code part: the unit root IS the code home, as a
task folder already is — `scripts/` (any language, `config/` inside; a
script may equally live inside an evidence lane) with `runs/` and
`results/` REQUIRED wherever code exists. `runs/` is the ONE door: only a
ticket there calls a script, under the simple-code law (reads only this
folder or a pagex-linked unit's declared outputs; writes only its own lane;
no raw data, no PHI). `results/` is regenerable, never sits inside
evidence/, and becomes EVIDENCE only when a probe card binds it. A flat
lane name is the same lane during migration (a stub on a migrated page).
Rows and retirements: `ref/roster.md`.

## 🔌 The two plugin kinds, and the tab bar they make (260831)

A LANE plugin owns one rostered folder's LAW — storage grammar, the one
writer, the gate (`haipipe-plugin-bibex`, `-probe`, `-display`, …). A
PRESENTER plugin owns one SURFACE over a whole category and stores nothing —
no roster row, no folder of its own, every pen it shows is a lane's own
route pressed explicitly. ONE TAB PER CATEGORY (JL 260831: "one plugin for
evidence, one plugin for the delivery, only one plugin for the studio"),
outline included:

```text
🧭 Outline   haipipe-plugin-outline    outline/ + workflow/ — the page's own
                                       process; FIRST and the default tab
🧾 Evidence  haipipe-plugin-evidence   bibex · probe · value · display · pagex,
                                       one segment each
📤 Delivery  haipipe-plugin-delivery   latex · word · slide · render — the
                                       🎞 segment carries the deck's ✨ pen
🎨 Studio    haipipe-plugin-studio     chat + draw AS ONE PAGE: the drawing
                                       above, the chat below, both live — the
                                       scene the chat redraws changes in front
                                       of the person talking. Both tools keep
                                       every rule and pen they had
⚙️ Code      haipipe-plugin-code       scripts/ · runs/ · results/ — contract
                                       only until the first real page runs/
📂 Folder    haipipe-plugin-folder     the roster itself, the meta-surface
```

So the strip a reader sees is five categories and a mirror:
🧭 · 🧾 · 📤 · 🎨 · (⚙️) · 📂. No lane sells its own strip row; the shell's
old 💬, 🖌 and 🎞 rows folded 260831 (stored tab sets migrate on load). The
260815 refusal of "full chat under the canvas" bound the DRAW tab; the
studio room is both tools', by JL's 260831 ask.
