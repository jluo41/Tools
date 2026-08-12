# How many artifact paths does each page-type contract actually name?

requires: QBt5-for-value

#### Q-executor

Across the ten page-type contracts under `board/page-types/`, count how many times each one names a path that a page of that type owns on disk. Report one row per contract with the count and the contract's own line count, so a length explanation can be ruled in or out.

#### consumer trace

- [Q-Value-1] · `QBt5-for-value` E1 · the page's own claim that the contracts are silent about what their pages own.
- [Q-Value-1] · `QBt9-for-slide` · the deck prints every row and both totals, and its template carries no digits.
- [Q-Value-1] · `QB-delivery/QB6-page-types.md` §7 · the opening claim of that division.

#### bank binding

**route**: task
**bank**: run
**target**: ../../_bank/tasks/A01_page-type-contracts/QA/1-artifact-paths.md
**state**: read

The answer lives in the bank, not here. This file holds the binding, the digest below, and one extract: `1-artifact-paths.data/counts.csv`, parsed from the bank's `## Answer` fence by `1-artifact-paths.data/source/build.py`. The bank is never copied in.

#### A-executor

Two of the ten contracts name no artifact path at all, and the ten together name thirty. The two at zero are `meeting` and `skill`, correctly rather than owed: neither produces a paper artifact.

The `lines` column rules out length as the explanation, and the bank carries the full reading.
