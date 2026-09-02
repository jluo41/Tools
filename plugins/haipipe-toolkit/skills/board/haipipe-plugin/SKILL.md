---
name: haipipe-plugin
description: >-
  The PLUGIN contract of a Board page: every Board-material subfolder is
  rostered, while one category plugin may own several internal storage lanes.
  A plugin is defined by STORAGE, SURFACE, WRITER, and BOUNDARY.
  ref/roster.md is the single list of material names. Trigger: page
  plugin, plugin folder, plugin roster, plugin tab, add a plugin,
  /haipipe-plugin.
metadata:
  version: "0.4.1"
  last_updated: "2026-09-02"
---

# /haipipe-plugin · a page's material, as one contract

`haipipe-page` owns what the page's `.md` SAYS; this skill owns what sits BESIDE it.
A page lives in its own home folder (QPf1 on the design board), and every
Board-material subfolder is ROSTERED. A roster row may be an internal lane
owned by a category Plugin; folder count and Plugin count are not required to
match. A Plugin is defined ONCE by four things, and `ref/roster.md` is the
single list of material names.

## 🧩 The four things a plugin is

```
📦 STORAGE   what files live in <page>/<name>/, named by the page's stem
🖼 SURFACE   its tab in the split's right pane, framing the material live
✍️ WRITER    the ONE tool allowed to land files there
🚧 BOUNDARY  board discovery never enters a plugin folder
```

A category Plugin meets all four directly. An internal lane inherits the
category's surface while retaining its named storage, writer, and gate. A
folder absent from the roster is not Board material and the checker may warn.
Adding a new top-level Plugin is one roster update plus one drawer
registration—the shell is never edited for it.

## 📦 Storage

Material lands in `<page-dir>/<plugin>/`, and artifacts carry the page's stem: `QPf2-draw-attach/draw/QPf2.excalidraw`.
PRIMARY plugins hold originals a person makes (draw, chat, meeting): they are committed and only their writer edits them.
DERIVED plugins hold projections of the page's own text (slide, latex, word,
citation workbench): they regenerate on demand, a hand edit is overwritten on
the next build, and the folder is safe to gitignore.
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
The drawer plugin registers `{id, label, hint, menu, order, applies, open, tab}` in `assets/js/10-drawer/05-plugins.js`'s registry; `order` fixes the reader-facing sequence independently of asset load order, while `tab.url(page)` names the saved artifact and `tab.write(page, cb, err)` builds one, so how an artifact is made never reaches the shell.
Server-side builders live as one `live/` module per concern and one `/_board/<plugin>` route (`live/autodeck.py` and `/_board/autodeck` are the slide's pair).

## 🚧 Boundary

Discovery (`src/common.py`) never surfaces a plugin folder's files as pages, so a `chat/` transcript full of `.md` can never become ghost pages.
The `session:` line and the page's own text stay `haipipe-page`'s; this contract begins at the folder.

## 🗂 The roster, and each plugin's own skill

`ref/roster.md` is the single list: name · kind · storage · surface · writer · status.
Every optional surface, including the Page phases stepper, appears in the one
Plugin picker. A surface may use its own panel layout after opening, but that
never creates a second top-level menu.
A Plugin's OPERATING knowledge lives in its own skill under
`page-plugins/haipipe-plugin-<name>/`. Internal lanes may instead live as
references under their owning category skill; Citation/Bib, Value, Display,
and PageX therefore live under `haipipe-plugin-evidence/ref/` and do not mint
four duplicate skills.
One of them inverts the shape: `haipipe-plugin-folder` is the 📂 meta-surface over the roster itself — no subfolder, no storage, no roster row (JL 260816).
This contract stays the base every one of them loads on top of; the board pages (`QPf2`-`QPf8`) stay the design records; the engine keeps only routes and machinery.

## 🗂 Category folders and the Runs door (260901)

A unit folder has TWO PARTS (JL 260831 v5). The UPPER, page part: three
CATEGORY folders that group lanes without changing any lane's grammar,
writer or gate — `evidence/` (citations in `bibex/` · probe · display ·
pagex · materials —
what the page CITES, each behind its human gate), `delivery/` (latex · word ·
slide · render — what leaves the page) and `studio/` (chat · draw — the
HUMAN's room: the person talks and sketches, and the chat may redraw on
their ask) — plus outline/ and workflow/. The LOWER, Task-side material is
presented as **Runs**: each authored ticket pairs with one generated Result by
logical Run address. A standalone/Discovery Folder stores both projections at
its root; a canonical Task Page stores the ticket inside the Task and its
generated Result at the containing Job's `results/<task>/<run>/`. A custom
Labeling dialect keeps Ticket and Result receipt in its authority-owning
round/evaluation/production/audit folder while preserving the same logical Run
address and receipt contract. `scripts/`
(any language, with optional `config/` inside) is supporting material only when
reusable local code exists; many Runs call a skill, CLI, API, or worker with no
scripts lane. The ticket is the ONE execution door under the simple-code law.
Results are regenerable, never evidence merely by existing, and become Page
evidence only when an evidence lane binds or aggregates them. Rows and physical
dialects: `ref/roster.md` and `haipipe-plugin-runs`.

## 🔌 The two plugin kinds, and the tab bar they make (260831)

A LANE contract owns one rostered folder's LAW—storage grammar, the one
writer, and the gate. It may be a separate Plugin such as
`haipipe-plugin-probe`, or an internal reference owned by its category.
A CATEGORY plugin owns one SURFACE over a whole category. It may delegate a
lane to another contract or own it directly: `haipipe-plugin-evidence` owns
Citation/Bib, Value, Display, and PageX, while presenting separately governed
Probe beside them. A storage lane therefore does not require a duplicate
Plugin or Skill. ONE TAB PER CATEGORY (JL 260831: "one plugin for
evidence, one plugin for the delivery, only one plugin for the studio"),
outline included:

```text
🧭 Outline   haipipe-plugin-outline    outline/ + workflow/ — the page's own
                                       process; FIRST and the default tab
🧾 Evidence  haipipe-plugin-evidence   citations · probe · value · display ·
                                       pagex, one segment each; Evidence owns
                                       all except Probe's crossing contract
📤 Delivery  haipipe-plugin-delivery   latex · word · slide · render — the
                                       🎞 segment carries the deck's ✨ pen
🎨 Studio    haipipe-plugin-studio     chat + draw AS ONE PAGE: the drawing
                                       above, the chat below, both live — the
                                       scene the chat redraws changes in front
                                       of the person talking. Both tools keep
                                       every rule and pen they had
⚙️ Runs      haipipe-plugin-runs       one overview table: Execution ·
                                       Discovery · Page · Labeling, each row pairing its
                                       ticket + Result; Scripts below, optional
📂 Folder    haipipe-plugin-folder     the roster itself, the meta-surface
```

The reader-facing Plugin picker follows one fixed sequence:
🧭 Outline · 🧾 Evidence · 🎨 Studio · 📤 Delivery · 📂 Folder · 🛠 Skill ·
🏷 Labeling. Optional entries still keep their assigned place when applicable;
an unassigned third-party entry follows these in stable registration order.
No lane sells its own strip row; the shell's
old 💬, 🖌 and 🎞 rows folded 260831 (stored tab sets migrate on load). The
260815 refusal of "full chat under the canvas" bound the DRAW tab; the
studio room is both tools', by JL's 260831 ask.
