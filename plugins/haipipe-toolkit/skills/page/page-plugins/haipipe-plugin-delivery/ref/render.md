# Render lane · the unit as the recipient sees it

This is an internal lane contract of `haipipe-plugin-delivery`. The category
skill owns the public surface; this reference owns why a render exists before
acceptance, its writer boundary, and the three stamps.

> 📤 This lane's surface home is the 📱 segment inside the 📤 Delivery tab
> (`haipipe-plugin-delivery`). The files remain fully usable through the Folder
> surface even when a served UI adapter is unavailable.

## Profile ownership

| Profile | Authority and storage | Meaning |
|---|---|---|
| Current Design Generate/Verify | Generate `result.yaml` pins `render_manifest` under its own `results/<run>/render/` | The preview depicts the exact candidate. Independent Verify determines readiness; rendering does not alter its verdict or introduce an Adopt gate. |
| Division delivery | `delivery/render/manifest.json`, owned by this lane | Design/warrants/render stamps describe a recipient-facing division version. Its declared human acceptance is required for distribution. |
| Historical Design previews | An existing Delivery manifest, read only when that exact candidate has no Result-local manifest | Migration evidence only. An invalid current manifest never falls back to an older picture. |

These profiles have different owners and destinations. A current Design writer
must not overwrite the division Delivery manifest. Keep historical entries
unchanged. Do not treat a division acceptance as Design Verify or vice versa.

### Current Design manifest (contract version 1)

`result.yaml` pins the manifest path and hash using the Design Unit Result
contract. The manifest is a nonempty JSON list; each entry contains:

```json
[{
  "item": "ITEM01",
  "candidate": "generate-01",
  "version": 1,
  "source": "../content/screen.html",
  "sha256": "<source SHA-256>",
  "render": "screen.png",
  "render_sha256": "<picture SHA-256>"
}]
```

Paths are relative to the manifest. The source must be a pinned content artifact
of that Generate candidate; the picture stays in the same Result's `render/`.
`version` is a positive integer. A candidate/source/version appears once.
The implementation authority is Design Unit's `check_unit.py::render_records`;
its enclosing Result schema versions this contract. Unknown formats or failed
hash checks produce an audit finding and no preview.

### Division delivery manifest (contract version 1)

This lane's new records are a JSON list with an explicit profile per row:

```json
[{
  "profile": "division-delivery",
  "schema_version": 1,
  "unit": "C1",
  "design": "DS-v2",
  "warrants": ["W1-v3"],
  "render": "Page-C1-v1.html",
  "version": 1
}]
```

The owning division retains its `accepted:` decision referencing this exact
render version. Older unprofiled entries remain history; writers preserve
unknown entries and require the appropriate owner to interpret them.

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
haipipe-plugin-delivery/ref/render.md
    render one division or all · stamp design/warrants/render · rebuild the
    derived preview · refuse when the venue is unpinned

POST /_board/render
    optional served adapter over the same writer; its absence never blocks the
    Folder-native render verb
```

## 📡 Surface · the 📱 segment

One card per unit showing the render as the recipient sees it, its character count against the venue cap in red when over, its three stamp classes, and whether the owning division carries an `accepted:` row. A unit whose division changed after its last render shows ⚠️ STALE, which `haipipe-plugin-folder` already computes for any derived lane.


The division-delivery writer lands new previews in `delivery/render/`. Current
Design workers use their Result-local render directory as described above. A pre-migration
flat `render/` may be read during a sweep, but it is not a current destination
and must not be shown as the canonical Folder row.

## 📂 Files

- `../../../haipipe-plugin/ref/roster.md`
  The `delivery/render/` lane row this category owns.
