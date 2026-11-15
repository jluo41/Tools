# Update an older design Block

`/haipipe-design update <Block>` is an agent procedure around one script. It renames; it does not design, verify,
release or sign anything. `--check` stops after step 2.

```text
before                                       after
inputs/i1/                                   inputs/inputs-v1/
runs/run-add-inputs-i1/                      runs/run-add-inputs-v1/
j01_<goal name>_goal-only/                   j01_<goal name>_M01-goal-only-m2_inputs-v1/
(no Book)                                    design/DesignMethodBook-<Channel>/jNN_M0x-<slug>/  (versions unsigned)
```

The new Job name is read from the Job's own face: `method: M01 m2` and `inputs: i1`. Nothing is guessed from the
folder name. Every command below runs from this skill's folder with a Python that has PyYAML
(`uv run --quiet --python 3.13 --with pyyaml python scripts/design_ladder.py …`).

## 1. Look before changing

1. Resolve the exact Block (a folder with `board.md`, `board-kind: design-board`). Read its repository's guidance.
2. Run `git status --short -- <Block>` in its repository. Note three cases:
   - clean and tracked: the update can be undone with git;
   - uncommitted paths: someone may be working there. Say so and ask before applying;
   - untracked (the whole Block shows `??`) or not in a git repository at all (`fatal: not a git repository`): git
     cannot undo it. Copy the Block to a scratch folder first. The dry run says so too.
3. Check nobody else is mid-change: a pull or a commit in the last few minutes (`git reflog -3`) is a reason to
   look again right before applying.

## 2. Audit and dry run

```bash
python scripts/design_ladder.py audit  <Block>
python scripts/design_ladder.py update <Block>
```

`audit` prints one line per check; ✅ means nothing to do.

| check | what it counts | fixed by |
|---|---|---|
| names | Jobs and inputs versions still on the older names | `update --apply` |
| by hand | Jobs whose folder is not `jNN_<goal name>_<method name>` | rename it by hand, then rerun |
| words | text files and links that still say an old name | `update --apply` |
| book | method versions the Jobs pin that the Book does not hold | `update --apply` |
| signs | Book versions with no sign | a person, on the method type's face (`versions:`) |
| hashes | a manifest's recorded hash that no longer matches its file | stop and read it; never apply over it |

The dry run prints every old name and its new name. Read that list. Stop when a new name is wrong: the fix is in the
Job's face pins (`method:`, `inputs:`), not in the script. A `by hand` or `hashes` line also stops the update.

## 3. Apply

When the Block is untracked, or the person asked for a rehearsal, apply on a copy first and compare (step 4) before
the original.

```bash
python scripts/design_ladder.py update <Block> --apply
```

What it does, in order: rewords text files and links, renames folders and files, makes or extends the Book, then
checks every recorded hash and every link again and prints the result. What it leaves alone: files whose hash a
manifest records (an inputs version's files, a Job's fence), files outside the Block and its Book, and every
`versions:` sign.

## 4. Verify

1. `audit` again: every line ✅ except `signs`.
2. The printed line says `recorded hashes: all match` and `links: all resolve`.
3. Open the Board and its Book through `/wb` on the running host: the same Jobs, designs and states as before; the
   Book lists each method type with the Jobs that run it. When no host is running, say the page check is pending.
4. In a git repository, `git status` shows renames, not deletions plus new files with different content.

## 5. Hand back

The Book's face is written from the Board's `channel:` (`goal:` and the title say "the sms designer"). Leave it as
it is unless the person gives better words. A Book made before 261109 may still show `<…>` placeholders: fill them
the same way.

Report in the Block map: the Board, one line per Job with its old and new name. Then the one thing left for a
person: sign each version in the Book (`versions:` on `jNN_M0x-<slug>/jNN_M0x-<slug>.md`, `mK: ✅ <YYMMDD>`). A
new Job on an unsigned version is refused by `design_ladder.py job`. Commit only when asked.
