---
name: haipipe-plugin-draw
description: >-
  The draw/ plugin of a Board page: one Excalidraw scene per owner, page
  scenes in <page>/draw/ and the group scene beside its pages. Owns
  split/sync/compose/verify and the ✨ autodraw writer. Trigger: draw plugin,
  attach a drawing, page scene, group scene, excalidraw, autodraw, draw it,
  /haipipe-plugin-draw.
metadata:
  version: "0.2.4"
  last_updated: "2026-08-31"
---
# /haipipe-plugin-draw · one scene per owner, saved to exactly one owner

**LOAD `haipipe-plugin` FIRST.** It owns what any plugin is: storage, surface, writer, boundary.
This file owns only draw's delta: who owns which scene, and which gesture writes which file.

> 🎨 Since 260831 evening this editor is the UPPER half of the one 🎨 Studio tab (`haipipe-plugin-studio`), staged above the live chat with its ✨ bar; ownership, the autodraw hand-drawn refusal and the chat pen are unchanged — only where the canvas hangs moved.

## 🗂 Storage · the page owns its scene, the group owns the relations

A folded page's scene lives in its own plugin; the group scene stays with the group, because relations BETWEEN pages belong to no one page.

```text
QX-group/
├── draw/
│   ├── group.excalidraw      group-owned elements + the import manifest
│   └── assets/               owner-scoped image bytes
├── QX1-page/
│   ├── QX1-page.md
│   └── draw/QX1.excalidraw   the page's own source
└── QX2-page/
    └── draw/QX2.excalidraw
```

`draw/` is lowercase everywhere.
Every group has one `group.excalidraw`, even when its own canvas is empty; every page has one source, even when its drawing is still empty.
A page whose scene file is missing gets an empty one MINTED on the first open (`live/xcal.py`), so the editor never falls back to a leftover buffer.
The composed group view is a runtime result, never a second editable copy of page content.
A flat page (no folder of its own) keeps the legacy home beside the group scene; the engine reads both through the manifest's relative `source` paths.

## ⚖️ The ownership rule · a gesture writes exactly one file

```text
surface              edit target
──────────────────────────────────────────────────────────
page drawing         that page's <stem>.excalidraw
group own layer      group.excalidraw
page instance move   group.excalidraw placement only
page source edit     <stem>.excalidraw, every group recomposes
```

**The chat holds this pen too (JL 260831: "I want the chat can change the
excalidraw as well during the discussion")**: a page chat may edit that page's
`<stem>.excalidraw` when the person asks in the session — the ask is the
grant, quoted in the one log record the write leaves. The ownership rule
binds unchanged (the chat writes only the open page's scene, never
`group.excalidraw`); ✨ autodraw's whole-scene authoring still refuses a
hand-drawn scene, while a chat edit is a scoped MODIFICATION of it — the
element(s) the ask names, nothing else redrawn.

The group editor has two explicit modes, and the UI always shows which owner will receive the save.
`Arrange Instance` changes only the imported page's placement, scale, visibility, and crop in the manifest.
`Edit Page Source` opens the page source as the write target; saving it invalidates every composition that imports it.

## ⚙️ Writer · the commands, all offline-safe

```bash
python3 <engine>/cli/draw.py split <board>             # read-only plan
python3 <engine>/cli/draw.py split <board> --apply     # new draw/ files only
python3 <engine>/cli/draw.py sync <board> --apply      # add only missing page sources
python3 <engine>/cli/draw.py compose <board> --output /tmp/board.excalidraw
python3 <engine>/cli/draw.py verify <board>            # exact legacy round trip
```

`split --apply` preflights every target and refuses the whole run if any linked source exists; each create is exclusive and a failure rolls back the run's creates.
It never changes the legacy `board.excalidraw`.
A cross-group or ownerless element stops migration instead of being guessed into a source; `customData.haipipeOwner` or both bound endpoints name the owner.
`compose` prefixes ids with the page owner, so independent sources cannot collide; `verify` proves the migration reconstructs every legacy element exactly.

## ✨ Generated drawings · the second writer and its style

The ✨ Draw it button on the Draw tab POSTs `/_board/autodraw`; `live/autodraw.py` runs `claude -p` over the page's own `.md` and writes the scene server-side.
An empty ask draws the page's `## Diagram` figure as a real scene; a typed ask draws that instead.
When the page carries an ascii figure, the SERVER places it verbatim at the top of the scene as one gray monospace text element, and the drawn version goes below it (JL 260816: the copy is deterministic, because ascii retyped by a model comes back bent).
A generated scene carries a `haipipe.autodraw` stamp and may be regenerated freely; a scene a person drew by hand carries no stamp, and the writer refuses it.
The style contract every generated scene follows (JL 260816):

```text
🫙 fill      backgroundColor "transparent" on every shape · boxes stay unfilled
🖊 emphasis  a shape that must stand out uses a colored STROKE
             #e8590c · #2f9e44 · #1971c2 · #9c36b5 (default stroke #1e1e1e)
✍️ text      fontFamily 8 on every text element · Comic Shanns Mono
🔗 form      every box is a rectangle with a BOUND label · every arrow BINDS both ends
📏 size      under 40 elements · span near 900x600 from (0,0)
```

The enforcing copy of this contract is the prompt inside `live/autodraw.py`; a style change lands in both places in one commit.

## 📡 Surface · the live editor's guarantees

The live editor (`live/xcal.py`) recognizes linked sources by schema and keeps the legacy `board.excalidraw` route for old boards.
Every linked save carries the revision the browser opened; a stale revision gets a visible conflict, never an overwrite.
Loading and toolbar navigation never arm autosave: the first non-toolbar human gesture is the snapshot point, so entering or leaving an owner cannot rewrite either source.
Pasted image bytes land under `draw/assets/<owner>/`; the scene keeps a relative pointer.
`cli/xcal.py` is a legacy seeder for old boards, not the source contract for new drawing work.

## 📂 Files

- `../../haipipe-board/cli/draw.py`
  split · sync · compose · verify · retire.
- `../../haipipe-board/live/xcal.py`
  The live editor's save path, owner modes, and the mint.
- `../../haipipe-board/live/autodraw.py`
  The ✨ writer: the generation route and the enforcing style prompt.
- `../../haipipe-plugin/ref/roster.md`
  The row this skill expands.
