---
title: Design Block Structure type inventories
date: '2026-11-27'
aim: Pin the verified Board and Book types, grouping sources and absent layers; record shared rendering gaps without inventing types.
closed: true
plan:
- do: add
  path: examples/Project-Ladder/blueprint/b12_theme_design/trace/261127/block_structure_types_alignment.md
  what: Record the confirmed four-file plan, checks and remaining obligations.
- do: add
  path: examples/Project-Ladder/blueprint/b12_theme_design/s01-design/types.md
  what: Add Board type inventory with owning sources and serialization gaps.
- do: add
  path: examples/Project-Ladder/blueprint/b12_theme_design/s02-workbench-ui/types.md
  what: Add Book type inventory, explicitly without execution Tasks.
- do: edit
  path: plugins/haipipe-toolkit/skills/3_theme/design/workbench-design/ref/topics.md
  what: Record the inventory topic and shared checker limitations.
changed:
- examples/Project-Ladder/blueprint/b12_theme_design/trace/261127/block_structure_types_alignment.md
- examples/Project-Ladder/blueprint/b12_theme_design/s01-design/types.md
- examples/Project-Ladder/blueprint/b12_theme_design/s02-workbench-ui/types.md
- plugins/haipipe-toolkit/skills/3_theme/design/workbench-design/ref/topics.md
---

# Design Block Structure type inventories

## Prompts

User confirmation: “好，现在我确认了，然后现在就进行这个更改吧。”

The preceding four-file proposal is approved. Page generators, manifests, shared checkers, example records and servers are outside this batch.

## Findings

- Board execution and Book method Jobs have distinct semantic contracts but no serialized job-type field in the example faces.
- Board Task faces declare design-reason, design-item and design-whole; Method Book has no execution Task layer.
- Grouping rules do not establish a separate group-type enum.
- Shared block_types_check.py requires nonempty lists at all four levels and can report success when no types.md exists. Record unsupported absent layers instead of inventing entries.
- Structure's actual-Block Studio organization and inventory-driven views require a subsequent page batch. The approved embedded examples and folded mindmap remain.

## Check

- Required both inventory paths explicitly: two files exist, each with the four named sections and one top-level example binding. Nonexistent inventory coverage is not a passing result.
- Shared read_types() parsing matches the actual Block paths. All declared entries have for/holds. Every owning/source Markdown link resolves inside the repository.
- Actual records: Board 3 Jobs / 13 Tasks, declared Task set exactly design-reason/design-item/design-whole; Book 2 Jobs / no Task directories, each method Job has version files. Neither example declares a separate job-type enum.
- Shared block_types_check.py exits 1 with five known diagnostics: Board Job group type and Task group type undefined; Book Job group type undefined, Task group type and Task type absent. No missing example, unknown declared type or missing for/holds diagnostics remain. This is not a passing shared compliance check.
- Shared block_types_pages.build() was called in memory only: it parses four Board pages and one Book page. No generated page or manifest was written. Its output does not yet expose all ownership/absence metadata.
- During validation an inner example key was found to override the Block binding; it was changed to members in both files and the parser was rerun successfully. Keep only one example key in each inventory.
- Existing current_contract_check.py --structure passes. Scoped git diff --check passes; all four files remain under 700 lines.
- README fresh-context invocation: workbench-design reviewer independently read the final inventories, actual faces and reader. PASS for documentation scope, correctly preserving Book without Tasks and identifying type views as not live.
- No browser acceptance is claimed: this batch changes documentation only. Existing folded maps, manifests, canvases, examples, shared code and service were not changed.

## Summary

The confirmed four-file inventory batch is complete. s01 and s02 now state their distinct semantic Job contracts, real grouping criteria, serialized Task values or absent Task layer, owners, names and sources. T20 remains open for shared absent/undefined-list handling, inventory-driven type views and actual-Block Studio organization; T08 retains the serialized Job-type decision. No execution harness or type-view deployment is claimed.

## Coordination scope

The Paper owning session relayed a requirement for one Block Structure instance per actual Block type; Folder / Job-Task / Studio content; four type-list categories with for/holds, source fields and owners; shared inventory-driven pages; preserved folded mindmaps and manual canvases; actual owning Skills and example Blocks; common registry/readers without shared restarts; and a concrete approved file plan. This batch is the four-file inventory prerequisite, not the subsequent UI implementation.

## Repeatable inventory check

Run from the repository root with the SPACE Python environment. This check proves the explicit inventory scope while preserving the shared checker's expected failures.

```python
from pathlib import Path
import sys
sys.path.insert(0, 'plugins/haipipe-toolkit/skills/1_base/project/hai-studio/scripts')
import block_types_check as check
base = Path('examples/Project-Ladder/blueprint/b12_theme_design')
expected = {
    's01-design': ({'design-reason', 'design-item', 'design-whole'}, 2),
    's02-workbench-ui': (set(), 3),
}
for topic, (task_types, diagnostic_count) in expected.items():
    file = (base / topic / 'types.md').resolve()
    assert file.is_file()
    assert sum(line.startswith('example:') for line in file.read_text().splitlines()) == 1
    example, types = check.read_types(file)
    assert set(check.LEVELS) <= set(types)
    block = Path(example)
    assert (block / 'board.md').is_file()
    jobs = list(block.glob('j[0-9][0-9]_*'))
    tasks = list(block.glob('j[0-9][0-9]_*/t[0-9][0-9]_*'))
    assert jobs
    assert {check.field(t / f'{t.name}.md', 'task-type') for t in tasks} == task_types
    assert set(types['Task type']) == task_types
    assert all(not check.field(j / f'{j.name}.md', 'job-type') for j in jobs)
    if not task_types:
        assert not tasks
        assert all(list(j.glob('m[0-9]*.md')) for j in jobs)
    diagnostics = check.problems(file)
    assert len(diagnostics) == diagnostic_count
    assert all('no `##' in d and 'list' in d for d in diagnostics)
print('Inventory scope verified; shared absent/undefined-list support remains open.')
```
