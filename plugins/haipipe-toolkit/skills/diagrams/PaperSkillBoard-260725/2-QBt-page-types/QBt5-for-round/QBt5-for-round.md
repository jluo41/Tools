# QBt5 · Close one bounded feedback cycle as a Round

state: ✅ SETTLED · current Round contract validated
page-type: round
owner: JL
method: atomize one feedback batch and route every item to its owning Page

## Opening
How can a paper answer one editor, reviewer, coauthor, or internal feedback batch without losing an item?
Round preserves the intake, gives every atomic concern a ledger row, records human dispositions, and routes accepted work to owning Pages.
It closes only with checked Page versions, response artifacts, and human approval.

**Where this page sits**: Round begins from one named build and returns checked work to assembly.

## Writing Style
Preserve received wording by quote or faithful pointer.
Distinguish completed changes from promises and deferred work.

## Diagram
**Round routing**: feedback is tracked here while substantive edits stay with their owners.

```text
feedback + base build ─▶ ledger ─┬─▶ Narrative
                                 ├─▶ Section/plugins
                                 └─▶ response + revised build
```

## Content
### 1 · Round contract
**Coverage rule**: every received concern appears exactly once and ends with proof, rationale, or a deferred handoff.

```text
intake · ledger · decisions · routing · checked changes
response package · close receipt
```

The Round never becomes a second home for revised prose or substantive paper evidence.

## Aims
### A1 · 🔄 Round contract
- A1.1 · One feedback batch closes without missing or duplicating a concern.
  **Done when:** all ledger items have terminal dispositions and checked destinations.

## States
### A1 · 🔄 Round contract
- ✅ A1.1 · The current contract distinguishes Paper Rounds from Page workflow rounds.

## Files
- `../../paper/page-types/haipipe-page-for-round/SKILL.md` · source contract

## Log
260820 · Promoted review and rebuttal into one persistent feedback Page Type.
