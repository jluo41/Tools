# Update an older insight Board

`/haipipe-insight update <Board>` is an agent procedure around one script. It renames and rewords; it asks no
question, answers none, and signs nothing. `--check` stops after step 2.

```text
before                                          after
work/Prototype-bNN-<Topic>/                     insight/InsightQuestionBook-<Topic>/
jNN_pN_<slug>/  (a release)                     jNN_question-vN_<slug>/  (a question version)
jNN_prototype-pN-<slug>_data-<D>vM/             jNN_question-vN-<slug>_data-vM/
release: pN · data: vM · AP<N> · F<M>           release: question-vN · data: data-vM
"cut", "partition" in a sentence                "segment"
run-set-cuts-<version>/                         run-set-segments-<version>/
```

Every command below runs from this skill's folder with a Python that has PyYAML
(`uv run --quiet --python 3.13 --with pyyaml python scripts/insight_ladder.py …`). `<folder>` is a Board, its
Question Book, or a Project (every Board under its `insight/`).

## 1. Look before changing

1. Resolve the exact Board (a folder with `board.md`, `board-kind: insight-board` or a `prototype:` line). Read its
   repository's guidance.
2. Run `git status --short -- <Project>` in its repository. Three cases:
   - clean and tracked: git can undo the update; apply in place;
   - uncommitted paths: someone may be working there. Say so and ask before applying;
   - untracked: git cannot undo it. Copy the Board and its Question Book to a scratch folder and apply there first.
3. A register board (`*-InsightBoard`) or an Insight Block (`j01_data` … `j04_wisdom`) is carried, not updated:
   `audit` prints a `layout` row that names its script (`ref/carry_over.py`, `ref/prototype_from_block.py`).

## 2. Audit and dry run

```bash
python scripts/insight_ladder.py audit  <folder>
python scripts/insight_ladder.py update <folder>
```

`audit` prints one row per check; ✅ means nothing to do.

| check | what it counts | fixed by |
|---|---|---|
| layout | a folder in a layout older than the Question Book and the Board | its carry script, then this again |
| names | files and folders still on `pN`, `vM`, `code-vN`, or a Question Book outside `insight/` | `update --apply` |
| words | files that still say "cut" or "partition" where a person reads | `update --apply` |
| goals | faces with no `goal:` line | `update --apply` |
| hash | Jobs whose `hash:` is not their release's | `update --apply` |
| receipts | hard Runs made from an older `question.md` or script | `update --apply --rerun` |

Goals, hash and receipts are counted once the names are current. For the changed lines themselves, run
`ref/rename_code_data.py <Board>` and `ref/rename_segment.py <Board>` (both a dry run without `--apply`) and read
them: stop when a sentence used "cut" as a verb and now reads wrong, and add that phrase to `KEEP` in
`ref/rename_segment.py` before applying.

## 3. Apply

```bash
python scripts/insight_ladder.py update <folder> --apply
```

In order: the names (text, then folders, then the Question Book moves beside its Board), the words, the missing
goal lines, each Job's `hash:`. It prints the receipts that are now older than their question or script, each with
its ticket. What it leaves alone is listed in SKILL.md § Update.

## 4. Rerun the receipts

A reworded `question.md` or script has a new hash, so its receipts no longer match. The tickets read the data
version's extract, so this step runs where the data is (the SPACE that holds `env.sh` and the extract):

```bash
python scripts/insight_ladder.py update <folder> --apply --rerun
```

It runs each stale Run's own `run.sh` and compares the receipt's `tables_sha256` before and after (one of the two decided exceptions to the no-hash rule in the SPACE's AGENTS.md § Working rules; the other is haipipe-design's Job fence). The last line
counts the Runs whose tables are the same, changed, or failed. A rename changes words, never numbers: every Run
should be "the same". Read each 🔶 changed and ❗ failed line before going on; a changed table means the data, a
library or a script differs from the first run, and that is a finding for the person, not a thing to smooth over.

## 5. Verify

1. `audit` again: every row ✅.
2. Open the Board and its Question Book through `/wb` on the running host: the same Jobs, questions, answers and
   states as before, under the new names. When no host is running, say the page check is pending.
3. In a git repository, `git status` shows renames, not deletions plus new files.
4. Links from other Blocks (a design Block that names the Board's Job by path): pass each to
   `ref/rename_code_data.py <Board> --also <path>` so whole names are carried there too.

## 6. Hand back

Report the Board map: the Board, one line per Job with its old and new name, then the receipts line (same, changed,
failed). Commit only when asked.
