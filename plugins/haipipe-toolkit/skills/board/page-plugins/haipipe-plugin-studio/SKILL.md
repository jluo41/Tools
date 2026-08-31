---
name: haipipe-plugin-studio
description: >-
  The ONE presentation plugin for a page's studio: a single 🎨 Studio tab
  staging the drawing above the chat, both live at once, so the scene the
  chat redraws changes in front of the person talking. Presentation only —
  chat/ and draw/ keep every rule, writer and pen they had. Trigger: studio
  plugin, studio tab, chat and draw together, the human's room,
  /haipipe-plugin-studio.
metadata:
  version: "0.1.0"
  last_updated: "2026-08-31"
  # version history: ./CHANGELOG.md (skill-scoped, never loaded at invocation)
---

# /haipipe-plugin-studio · one room, two tools, one tab

**LOAD `haipipe-plugin` FIRST.** A PRESENTER plugin (haipipe-plugin §🔌): no
roster row, no folder — the law lives in the `studio/` category row and the
chat/ + draw/ lane rows. JL 260831: "I think we still keep the basic
functions of the chat and draw, but I want to put both of them into the
studio, as one page."

```text
🎨 Studio
├── 🖌 the drawing     the live Excalidraw editor with its ✨ Draw-it bar,
│                      exactly the old Draw tab, staged in the upper half;
│                      a page with no scene keeps the chat full height
└── 💬 the chat        the chat pane with its GUI/TUI segment, exactly the
                       old Chat tab, staged in the lower half
```

- **Why one page**: the chat may redraw the scene's named elements on the
  person's ask (plugin-draw §chat pen) — with both halves live, the person
  watches the scene change while talking, no tab switch between the ask and
  the result.
- **The split is the layout's own**: the pane is a flex column, so two
  visible frames share it; no divider machinery.
- **Lineage**: the 260815 refusal of "full chat under the canvas" bound the
  DRAW tab (a button generates the drawing, not a chat). The studio room is
  both tools', by JL's 260831 ask; the refusal stays true of the draw LANE.
- **Nothing merged but the surface**: chat's session keep, walls, log
  record, draw's ownership rule, the autodraw hand-drawn refusal — all
  unchanged, each in its own lane skill.
- **Migration**: stored tab sets speaking the old ids are rewritten on load
  (chat, draw → studio; slides → delivery).

## 🗺 Status · 🟢 built 260831 evening

`live/shell.py`: tab id `studio`, the paired stage, the folded 💬/🖌/🎞
strip rows, the stored-set migration. The old ids stay internal so every
chat and draw mechanism runs untouched.

## 📂 Files

- `../haipipe-plugin-chat/SKILL.md` · `../haipipe-plugin-draw/SKILL.md` ·
  the two tool contracts this surface stages
- `../../haipipe-plugin/ref/roster.md` · the studio/ category row
- `../../haipipe-board/live/shell.py` · the tab, the split, the migration
