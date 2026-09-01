---
name: haipipe-plugin-render
description: >-
  The render/ plugin of a Board page: the page's units as the RECIPIENT sees
  them, at PAGE/delivery/render/STEM-UNIT-vN.EXT, derived, so a person can
  accept a message they have actually seen. Trigger: render plugin, message
  preview, as the recipient sees it, render version, sms preview,
  /haipipe-plugin-render.
metadata:
  version: "0.1.3"
  last_updated: "2026-08-31"
---

# /haipipe-plugin-render · the unit, as the recipient sees it

**LOAD `haipipe-plugin` FIRST.** It owns what any plugin is: storage, surface, writer, boundary.
This file owns only render's delta: why it exists before acceptance, and the three stamps.

> 📤 This lane's surface home is the 📱 segment inside the 📤 Delivery tab
> (`haipipe-plugin-delivery`). The files remain fully usable through the Folder
> surface even when a served UI adapter is unavailable.

## 🎯 Why this exists

A design division specifies a message. It does not show one. A 148-character SMS with a link breaks where its markdown bullet did not: the line wraps elsewhere, the link eats characters, the truncation point moves.

The acceptance row names a **render version**, so the render has to exist first:

```text
draft the division  ──▶  render it  ──▶  a person reads the render  ──▶  accepted:
```

This is the correction to the retired `fn/artifact.md`, which refused to render an unaccepted division and so made acceptance unreachable. Rendering is free; **distribution** is what requires an accepted row.

## 🗂 Storage · DERIVED, one file per unit per version

```text
<page>/delivery/render/
├── <stem>-<unit>-v<N>.<ext>     DERIVED · the unit as it will appear
└── manifest.json                three stamps per file
```

The extension follows the venue: `.txt` for sms, push and reminder; `.html` for ui-card and dashboard; `.docx` for report. A page whose venue is not pinned cannot render.

**Three stamps, not one**, because the same content can be re-rendered unchanged and the same render can go stale when the evidence under it moves:

```text
design    the DS page version the division came from
warrants  zero or more promoted-P versions PLUS every directly bound W handoff
render    this file's own version
```

## ⚖️ The one law · the page is the source

A render is regenerated, never edited. Someone will edit a rendered file directly, usually while reading it aloud in review, and that edit is real feedback landing in the wrong place. Copy it into the owning division, which clears that division's `accepted:` row, then re-render. Never re-render over an unreconciled edit: that silently deletes it.

## ⚙️ Writer · one contract, optional UI adapter

```text
haipipe-application/fn/render.md
    render one division or all · stamp design/warrants/render · rebuild the
    derived preview · refuse when the venue is unpinned

POST /_board/render
    optional served adapter over the same writer; its absence never blocks the
    Folder-native render verb
```

## 📡 Surface · the 📱 tab

One card per unit showing the render as the recipient sees it, its character count against the venue cap in red when over, its three stamp classes, and whether the owning division carries an `accepted:` row. A unit whose division changed after its last render shows ⚠️ STALE, which `haipipe-plugin-folder` already computes for any derived plugin.


> Since 260831 this lane lives under the page's category folder (`evidence/` or `delivery/`, haipipe-page 0.47.0 §📁); a flat lane name on an unmigrated page, or a flat SYMLINK STUB on a migrated one, is the same lane during the migration.

## 📂 Files

- `../../haipipe-plugin/ref/roster.md`
  The row this plugin expands.
