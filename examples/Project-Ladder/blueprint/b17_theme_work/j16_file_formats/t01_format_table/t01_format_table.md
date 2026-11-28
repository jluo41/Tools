# Format table
state: 🔴 OPEN
goal: one table, the Block's delivery/page-spec/file-formats.md, says for every kind of file a Block holds where it sits, what it holds, which script writes it, which page code reads it, and where its rule is written
close: never while these kinds exist; a new kind or a changed field updates its row in the same change
owner: JL
folder-kind: task
task-type:
task: .

## Files

`examples/Project-Ladder/blueprint/b17_theme_work/delivery/page-spec/file-formats.md`: the format table, part of the page spec b17 hands to the code and the skills.

## Checks

1. Every kind in the table names a writer and a page code that exist on disk
2. Every rule file it names exists
3. A kind found on disk (by t02) and missing from the table is added
