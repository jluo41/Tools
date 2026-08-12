# haipipe-page-for-labeling · CHANGELOG

## 0.1.0 · 2026-08-07

First edition. Splits out of a single worked sample that was trying to be three things at once: a contract, a specimen, and one real run.

**What the Page Type establishes**

- Two kinds: one `S-Label-Dash` control page per family, and one `S-Label-<n>-<corpus>-<target>` page per run. The per-unit test is QC3b's, so a target is a unit because a person can accept one and refuse the one beside it.
- **A round is a RECORD, never a division.** Rounds are strictly ordered, so they fail the per-unit test, and one `### 2 · Rounds` division holds them all as record blocks, newest first. This is the rule the Page Type exists for: without it a page grows a heading per round and changes shape forever.
- Five Content divisions that mirror the run rather than argue a question, with `§1` obliged to say what LOW means because it differs between a graded trait and a discrete move.
- **Aims ARE the stopping gates**, so `## States` answers "may we stop" with no second source of truth, and a control on a division may read that state but never write one.
- An empty division is a status: `§4` and `§5` stay while empty, because a missing heading cannot report that a freeze has not happened.
- Evidence rules: a quoted item carries its id, a number names its round, a machine may propose a class but only a human session makes it gold, and on a boundary item the region is proposed while the class is left blank.
- The seal is a field, not a promise: prefer a boundary the corpus already shipped with, so "was the test read" is checkable in a manifest.

**Engine change shipped with it**

`Label` admitted to the six lists that close the S family set, verified by rebuilding three live boards and confirming their page counts did not move (77, 31, 70, all unchanged). Before the change an `S-Label-*` file was not a page at all: it vanished from the build with no warning line, which is the quietest of the six failure modes.

**Ships with**

`SKILL.md` (the contract) and `template.md` (the specimen). The worked example lives on a board, not in this folder.

## 0.2.0 · 2026-08-07

Revised after the first edition met a second board and a second run. Every change below is a defect the first edition caused, not an idea about it.

**The specimen gained a second file**

`template-dash.md`, for the control page. The first edition declared two kinds and shipped one specimen, so a control page had to be written by copying the run specimen, which gives it a `requires:` it does not have and Aims about a run it does not own. It also carries the rule that a control page still needs `## Stage Contract` and must say **None, by design**, because the checker reports `missing-stage-section` on every S page regardless.

**Cross-board references, warned three times**

Moving the worked example onto its own board broke five references at once. A run page and its method are always on different boards, and cross-board behaves differently in the two places it appears: `requires:` needs a real relative path because an id is looked up in this board's pages only, and `### 🔗 Related Board Pages` may hold only pages on this board, so method pages move to `board.md`'s `## Links`. Both failures let the page build, so nothing stops an author who gets it wrong.

**`### Required Inputs` belongs to the generator, not the author**

Found by writing a second run page from the specimen and running `stage.py sync` on it: the managed block generates `### Required Inputs` and `### Venue`, so an author who also writes `### Required Inputs` gets two of them, stacked, with no complaint from the checker because both headings are legal. Authored contract material now goes after the end marker under a heading of the author's own naming. Both live run pages were repaired.

**Verification**

`S-Label-2-acibench-social-proof` was written from this specimen and landed at 0 error, 0 warn on the first build, before the `sync` defect above surfaced. Adding it also broke the Dash's A1.1, which requires the row count to equal the run count, and that is the Aim working rather than a defect.

## 0.3.0 · 2026-08-07

**Moved out of the board plugin, into the plugin that maintains it.**

Was `haipipe-toolkit/skills/board/page-types/`, is now `subjective-label/skills/`. This is not a new rule: `haipipe-board`'s own 260803 ruling already says a Page Type variant ships WHERE THE BOARD FAMILY MAINTAINS IT, and closes with "who maintains it is the line that held twice; who consumes it never did". Every rule in this contract comes from the subjective-label method, and the board family maintains none of it, so the original placement was wrong by the rule that was already written. JL 260807: a `for-<type>` variant may live in any skill set.

The board family keeps the three variants it does maintain. The `label` value stays in `check.py`'s `PAGE_TYPE_VALUES`, because that list is the board engine's, not this contract's.
