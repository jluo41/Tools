---
name: haipipe-board-page-for-labeling
description: >-
  The VARIANT contract for a LABELING run Page: one Page per corpus and label target being labeled by a human authority, plus one control page per family. It loads haipipe-board-page for the base frame and adds only what a run Page needs: the per-unit test that makes one corpus plus one target one Page, the rule that a round is a RECORD and never a division so the Page cannot grow without end, five Content divisions that mirror the run rather than argue a question, Aims that ARE the stopping gates so States answers "may we stop" without a second source of truth, the rule that an empty division is a status, and the evidence rules that a quoted item carries its id and that a machine may propose a class but only a human session makes it gold. Use when writing or fixing a labeling Page, when rounds are turning into sections, when a page shows a score with no round behind it, or when a machine's proposed label is being read as gold. Trigger: labeling page, S-Label, label run, calibration round, annotation policy, gold, sealed test, stopping gate, region, H L N, /haipipe-board-page-for-labeling.
metadata:
  version: "0.3.0"
  last_updated: "2026-08-07"
  summary: "Ships from the plugin that maintains it, not from the board family."
  # version history: ./CHANGELOG.md (skill-scoped, never loaded at invocation)
---

# /haipipe-board-page-for-labeling · a run page records a judgment it does not make

**LOAD `haipipe-board-page` FIRST.** It owns the base: the sections and their fixed order, the five rows that define each one, the title rule, the Opening split, the numbering, and the evaluation contract.
This file adds only what a labeling page needs and an ordinary stage page does not.
It never repeats a base rule, because a copied rule goes a night out of date while the contract moves.

**What a labeling run is** comes from the `subjective-label` plugin's own board, `diagram/02-subjective-label-260722`, whose QA0 through QF5 fix the method.
This file never restates that method. It says only what the BOARD PAGE must carry.

## 🧩 The two kinds

```
kind          filename                          subject                closes when
──────────────────────────────────────────────────────────────────────────────────────
control       S-Label-Dash.md                   which runs exist and   never; it is an
                                                where each one stands  inventory
per-unit run  S-Label-<n>-<corpus>-<target>.md  ONE corpus and ONE     its human gate
                                                label target           passes
```

**The test for a unit is QC3b's, and it is about people, not files**: can a person say yes to one thing here while saying no to the thing beside it?
A human authority can accept `authority` on a corpus and still refuse `social-proof` on the same corpus, so each target is its own unit with its own gate.
Size does not decide it, and neither does how long the page grows.

**⛔ A ROUND IS NOT A UNIT.** Round 4 cannot be approved while round 3 is refused, because a round opens only after the previous checkpoint closed. Rounds are strictly ordered, so they fail the test, and the rule below follows from that.

**One target per page also keeps the class single-valued.** One item may carry two targets at once. Giving each target its own page keeps each page's HIGH, LOW, and NONE clean, and lets multi-label live across pages instead of forcing one page to hold classes that are not mutually exclusive.

## 🔁 The rule this Page Type exists for

**A round is a RECORD, never a division.**

Rounds keep arriving, and the base fixes the section order, so a `###` per round would make the Page grow without end and change shape every round.
One `### 2 · Rounds` division holds them all, newest first, as record blocks:

```markdown
**Round 3** · closed 260806 · policy G_3 · 60 items
  🎯 challenge  policy and the human disagreed on 11 of 60
  📊 audit      agreement 0.86 on the consensus stratum
  📜 diff       rule 3 and rule 4 added; no rule dropped
  🗺 coverage   region 5 still thin at 3 items
```

Round 12 costs exactly what round 2 cost: four lines at the top, and no heading moves.
Record lines, never a markdown table.
The heavy artifacts stay in the run folder on disk; this ledger is the readable index into them.

## 📚 Content: five divisions that mirror the run

A labeling page's Content mirrors a run in progress. It does not argue a question.

```
### 1 · What <target> means now      the boundary as the human draws it TODAY, with real items
### 2 · Rounds                       the ledger
### 3 · Gates: may we stop?          the current reading of each stopping gate
### 4 · Freeze, sealed test, scores  empty until the policy freezes
### 5 · The labeled corpus           empty until the executor runs
```

**§1 must SAY what LOW means on this page**, because it differs by target and a reader cannot guess.
On a graded trait, LOW is a weaker HIGH.
On a discrete move such as a persuasion tactic, nothing is "a bit of" it, so LOW is the NEAR MISS: the item does adjacent work by another route.
Where LOW is the near miss, the boundary region carries the work and §1 should say so.

**An empty division is a STATUS, not a gap.**
`§4` and `§5` stay on the page while empty, with their rows showing what has not happened.
A missing heading cannot say "the freeze has not happened", so deleting them loses the only honest thing they had to report.

## 🎯 Aims ARE the gates

The base says Aims are durable targets and States carries one row per Aim.
On a labeling page those targets are already defined by the method's stopping gates, so **do not invent a second set**.

```
A1  the policy is executable, and every rule is traceable to its round
A2  every closed round is reproducible from its own folder
A3  the stopping gates: quality · stability · coverage · risk        ← one Aim item each
A4  the seal holds, and every candidate executor is scored on it
A5  the corpus is complete with provenance, and the audit says what is reliable
```

The payoff is that `## States` answers "may we stop" with no second source of truth, and a reader scanning it sees which gate blocks.
A control button on a division may read that state to decide whether it is enabled; it must never write a state of its own.

## 🌉 The two boards, and why every run page straddles them

**A run page and the method it obeys are always on DIFFERENT boards.**

```
design board                          run board
how the loop works                    what one run found
settles questions, then closes        records a judgment, never settles the method
   QA0 … QF5                             S-Label-Dash · S-Label-1 · S-Label-2 …
```

Keeping them apart is what stops "how we decided to do this" and "what this run produced" from being edited as one document.
It is also what makes the design board closable while runs keep opening.

The cost is that **every reference from a run page to a method page is cross-board**, and cross-board behaves differently in the two places it appears:

- `requires:` and `style-from:` look a bare page id up in THIS board's pages. A method page is not one, so it needs a real path relative to this board's root. An id there reports `Stage Contract source not found` and then builds anyway.
- `### 🔗 Related Board Pages` may hold **only pages on this board**. A method page there reports `dead-related-page`, and its rendered link reports `dead-href`. Declare method pages in `board.md`'s `## Links` and cite them by name in a separate block.

Both failures let the page build, so nothing stops an author who gets it wrong. This is the single most likely defect in a new run page, which is why the specimen carries the warning three times.

## 🗂 The control page still needs a Stage Contract

A control page has no upstream, and the checker requires `## Stage Contract` on every S page regardless, reporting `missing-stage-section` without it.
Write the section and say **None, by design**, with the reason.
Leaving it out and leaving it empty look identical to the checker and different to a reader, and the reader is the one who has to know that a control page is not a run page missing its inputs.

Its Aims are about the ROSTER's completeness, never about any run's progress.
An Aim tracking a run's gate belongs on that run's page, or the same fact lives in two places and one of them goes stale.

## 🧾 Evidence rules

- **A quoted item carries its id.** A paraphrased example cannot be re-judged in a later session, so it is not evidence. Quote verbatim and name the item.
- **A number names the round that produced it.** A score with no round behind it does not belong on the page.
- **A machine may PROPOSE a class; only a human session makes it gold.** Mark a proposal as a proposal in the line that carries it.
- **On a boundary item, propose the region and leave the class blank.** Proposing the class there pre-answers the thing the human is there to decide, which is the one thing this whole method reserves to them.
- **The seal is a field, not a promise.** Prefer a boundary that already exists in the data, such as a split the corpus shipped with, so "was the test read" is checkable in a manifest rather than trusted.

## 🚦 State

This is an S page, so `✅` means this page's own human gate passed, and the index counts it under the `Label` family.
A run that is deliberately parked is `⏸️`, and a run whose gates are still open is `🟡` however many rounds have closed.
`state:` never reads `✅` because the rounds went well; it reads `✅` because a person signed the freeze.

## 📄 Files

| File | What it is |
|---|---|
| `template.md` | The specimen for a RUN page. Copy it, fill it, delete each RULE comment as you satisfy it. |
| `template-dash.md` | The specimen for the CONTROL page. One per board, not one per run. |
| `CHANGELOG.md` | Version history, never loaded at invocation. |

Two kinds, two specimens. Copying the run specimen for a control page produces a page with `requires:` it does not have and Aims about a run it does not own.

`examples/Project-Subjective-Label/diagram/01-label-runs-260807/SL-labeling-runs/S-Label-1-acibench-authority.md` is the reference implementation, and `S-Label-Dash.md` beside it is the control page.
Read them before writing a new one.
A worked example lives on a board and never in this folder, because a page that renders nowhere cannot show that its Decision Now row can be answered.

The `Label` family is admitted to the six lists that close the family set; `haipipe-board`'s own board records where they are and why a name missing from one of them fails differently in each.
