---
name: haipipe-plugin-studio
description: >-
  The ONE presentation plugin for a page's studio: a single 🎨 Studio tab
  staging the drawing above the chat, both live at once, so the scene the
  chat redraws changes in front of the person talking. It owns both internal
  lane contracts without exposing duplicate Chat or Draw skills. Trigger: studio
  plugin, studio tab, chat, page chat, keep this session, draw, Excalidraw,
  autodraw, chat and draw together, the human's room,
  /haipipe-plugin-studio.
metadata:
  version: "0.2.1"
  last_updated: "2026-09-04"
  # version history: ./CHANGELOG.md (skill-scoped, never loaded at invocation)
---

# /haipipe-plugin-studio · one room, two tools, one tab

**LOAD `haipipe-plugin` FIRST.** A CATEGORY plugin (haipipe-plugin §🔌):
one public surface over the `studio/` category, with Chat and Draw as internal
lane references rather than standalone skills. JL 260831: "I think we still keep the basic
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
  person's ask (`ref/draw.md` § chat pen) — with both halves live, the person
  watches the scene change while talking, no tab switch between the ask and
  the result.
- **The split is the layout's own**: the pane is a flex column, so two
  visible frames share it; no divider machinery.
- **Lineage**: the 260815 refusal of "full chat under the canvas" bound the
  DRAW tab (a button generates the drawing, not a chat). The studio room is
  both tools', by JL's 260831 ask; the refusal stays true of the draw LANE.
- **One skill, two lane laws**: chat's session keep, walls, log record, draw's
  ownership rule, and the autodraw hand-drawn refusal remain distinct in
  `ref/chat.md` and `ref/draw.md` while Studio is the only callable skill.
- **Migration**: stored tab sets speaking the old ids are rewritten on load
  (chat, draw → studio; slides → delivery). New Page-owned bytes land only at
  `studio/chat/` and `studio/draw/`; flat `chat/` and `draw/` remain readable
  aliases for old Pages, never writer destinations. A Group's relation scene
  remains Group-owned at its own `draw/group.excalidraw`.

## 🗺 Status · 🟢 built 260831 evening

`live/shell.py`: tab id `studio`, the paired stage, the folded 💬/🖌/🎞
strip rows, the stored-set migration. The old ids stay internal so every
chat and draw mechanism runs untouched.

## 📂 Files

- `ref/chat.md` · `ref/draw.md` · the two internal lane contracts this
  category stages; load only the one needed for the requested operation
- `../../haipipe-plugin/ref/roster.md` · the studio/ category row
- `../../haipipe-board/live/shell.py` · the tab, the split, the migration
