# The Studio screen · one room, two tools, one tab

The screen manual of haipipe-studio (`../SKILL.md`), folded in from the retired skill `workbench-studio` on 2026-10-16 (s21-D05). `/workbench-studio` still triggers haipipe-studio.

**LOAD `workbench` FIRST** (`../../../workbench/workbench/SKILL.md`). A CATEGORY workbench (workbench §🔌):
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
  person's ask (`draw.md` § chat pen) — with both halves live, the person
  watches the scene change while talking, no tab switch between the ask and
  the result.
- **The split is the layout's own**: the pane is a flex column, so two
  visible frames share it; no divider machinery.
- **Lineage**: the 260815 refusal of "full chat under the canvas" bound the
  DRAW tab (a button generates the drawing, not a chat). The studio room is
  both tools', by JL's 260831 ask; the refusal stays true of the draw LANE.
- **One skill, two lane laws**: chat's session keep, walls, log record, draw's
  ownership rule, and the autodraw hand-drawn refusal remain distinct in
  `chat.md` and `draw.md` while Studio is the only callable skill.
- **Migration**: stored tab sets speaking the old ids are rewritten on load
  (chat, draw → studio; slides → delivery). New Page-owned bytes land only at
  `studio/chat/` and `studio/draw/`; flat `chat/` and `draw/` remain readable
  aliases for old Pages, never writer destinations. A Group's relation scene
  remains Group-owned at its own `draw/group.excalidraw`.

## 🗺 Status · 🟢 built 260831 evening

The Studio is served by `servers/workbench/` inside every workbench. The static
Board page's three-pane shell that also carried a `studio` tab (`servers/haipipe-block/shell.py`)
retired with the Board's static site (JL 261004); the old ids stay internal so every chat
and draw mechanism runs untouched.

## 📂 Files

- `chat.md` · `draw.md` · `workbench-table.md` · the two internal lane contracts this
  category stages; load only the one needed for the requested operation
- `../../../workbench/workbench/ref/roster.md` · the studio/ category row
- `../../../../../servers/workbench/` · the Studio every workbench mounts
