# The Block Structure topic

The type's requirement for every part is `elements.md` beside this file. A Block Structure topic shows how one
kind of Block is laid out: its folders, its Jobs and Tasks, its Studio, and the types of Job and Task it has.

```text
top     Structure · Job types · Task types · Draw · Skills
left    Structure: Folder · Job-Task · Studio        Job types, Task types: one tab per type the topic lists
right   the topic's own trees and type cards, built from two files it writes by hand
```

## What the topic writes by hand

1. **`structure.md`**: the Folder, Job-Task and Studio trees of this Block type, as indented lines.
2. **`types.md`**: its Job group, Job, Task group and Task types; a level it does not have says `none: <why>`.

## What the scripts build

Run from the SPACE root; `type_follow.py follow <topic>` (the shared script) runs all three builders and then holds the topic
to the type.

```text
scripts/block_structure_page.py <topic> [--check]    delivery/structure.html from structure.md
scripts/block_types_pages.py <topic>                 one page per type in types.md, and the views file's buttons
scripts/block_structure_draw.py <topic> [--check]    the topic's one drawing and its preview, from structure.md
scripts/block_types_check.py <Block>                 every example Job and Task names a type the topic lists
```

1. **The tree is the type's tree.** The Structure page is drawn by the same code as the type's Pattern, so the two
   read alike; `  | words` after a name on a tree line is its hover.
2. **A level with no type gets no button.** A Block type without Tasks has no Task types button; the type marks
   that part with `when:`.
3. **Names in 〈 〉** are slots a real Block fills in.
4. **The drawing reads the same file.** `block_structure_draw.py` draws the folders, the Job-Task levels and the
   Studio bands from `structure.md`, so the drawing and the Structure page cannot name things differently; a
   person's marks on the drawing are kept on a redraw.
