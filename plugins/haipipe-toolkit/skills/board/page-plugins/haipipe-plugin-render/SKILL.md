---
name: haipipe-plugin-render
description: >-
  The render/ plugin of a Board page: the page's own units as the RECIPIENT sees them, at <page>/render/<stem>-<unit>-v<N>.<ext> (DERIVED), with a manifest carrying three version stamps. It exists so a human can accept a message they have actually seen, since an acceptance row names a render version. The venue picks the extension and the preview shape. Loads haipipe-plugin for the four-facet contract and never restates it. Trigger: render plugin, message preview, as the recipient sees it, character count, render version, sms preview, /haipipe-plugin-render.
metadata:
  version: "0.1.0"
  last_updated: "2026-08-20"
  summary: "New 260820: replaces the board-level artifacts/ folder. A render is one page's derived output, so it is a plugin like latex and word, not a group."
---

# /haipipe-plugin-render · the unit, as the recipient sees it

**LOAD `haipipe-plugin` FIRST.** It owns what any plugin is: storage, surface, writer, boundary.
This file owns only render's delta: why it exists before acceptance, and the three stamps.

## 🎯 Why this exists

A design division specifies a message. It does not show one. A 148-character SMS with a link breaks where its markdown bullet did not: the line wraps elsewhere, the link eats characters, the truncation point moves.

The acceptance row names a **render version**, so the render has to exist first:

```text
draft the division  ──▶  render it  ──▶  a person reads the render  ──▶  accepted:
```

This is the correction to the retired `fn/artifact.md`, which refused to render an unaccepted division and so made acceptance unreachable. Rendering is free; **distribution** is what requires an accepted row.

## 🗂 Storage · DERIVED, one file per unit per version

```text
<page>/render/
├── <stem>-<unit>-v<N>.<ext>     DERIVED · the unit as it will appear
└── manifest.json                three stamps per file
```

The extension follows the venue: `.txt` for sms, push and reminder; `.html` for ui-card and dashboard; `.docx` for report. A page whose venue is not pinned cannot render.

**Three stamps, not one**, because the same content can be re-rendered unchanged and the same render can go stale when the evidence under it moves:

```text
design   the DS page version the division came from
warrant  the P page version, and through it the W handoff version
render   this file's own version
```

## ⚖️ The one law · the page is the source

A render is regenerated, never edited. Someone will edit a rendered file directly, usually while reading it aloud in review, and that edit is real feedback landing in the wrong place. Copy it into the owning division, which clears that division's `accepted:` row, then re-render. Never re-render over an unreconciled edit: that silently deletes it.

## ⚙️ Writer · one route

```text
POST /_board/render     one division or all · stamps all three versions ·
                        rebuilds the preview · refuses when the venue is unpinned
```

## 📡 Surface · the 📱 tab

One card per unit showing the render as the recipient sees it, its character count against the venue cap in red when over, its three stamps, and whether the owning division carries an `accepted:` row. A unit whose division changed after its last render shows ⚠️ STALE, which `haipipe-plugin-folder` already computes for any derived plugin.

## 📂 Files

- `../../haipipe-plugin/ref/roster.md`
  The row this plugin expands.
