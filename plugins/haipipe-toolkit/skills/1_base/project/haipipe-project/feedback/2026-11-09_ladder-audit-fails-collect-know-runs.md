---
status: open
created: 2026-11-09
updated: 2026-11-09
occurrences: 1
---

# ladder.py audit fails every `collect.py know` Run that haipipe-collect writes correctly

## What happened

`ladder.py audit examples-1-data/Proj01-CGM-RawData` (WellDoc-SPACE) marks
`work/b51_externalstore/runs/r01_collect_meal_to_know` **failed**:

```text
✗ marked done with no result/
· to_know.yaml is not in the ladder for a Run
```

That Run was written by `haipipe-collect/scripts/collect.py know`, which by design keeps
`to_know.yaml`, `question_collection.md` and `<run>.html` beside the card (`KNOW = "to_know.yaml"`,
`_write_know`) and sets `status: done` with `source: know` and `writes: [to_know.yaml]`. A know Run
waits on nothing, so it never gets a `result/`.

## The fix it needs

`ref/ladder.md` (read by `scripts/ladder.py`) should accept a collect Run whose card says
`type: collect` and `source: know`: `to_know.yaml`, `question_collection.md`, `<run>.html` as its
files, and no `result/` required. Either skill could be the one to change; today they disagree,
so a correct Run shows in `project.py audit` as "person" work that no person can fix.
