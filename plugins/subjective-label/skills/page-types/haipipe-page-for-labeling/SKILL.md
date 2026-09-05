---
name: haipipe-page-for-labeling
description: >-
  The VARIANT contract for a SUBJECTIVE-LABEL job Page: one Page per corpus and
  target, spanning the Building and Scanning sides plus one control page per
  family. It loads haipipe-page for the base frame and adds only what a Job Page
  needs: a round is a RECORD and never a division; five Content divisions show
  meaning, rounds, Building stop gates, signed handoff/scorecards, and audited
  corpus completion; an empty division is status; quoted items carry ids; and
  only a human event creates gold. Use when writing or fixing a labeling Page,
  when rounds become sections, when freeze is mistaken for completion, when a
  score has no bound handoff, or when a machine proposal is read as gold.
metadata:
  version: "0.6.0"
  last_updated: "2026-09-04"
  # version history: ./CHANGELOG.md (skill-scoped, never loaded at invocation)
---

# /haipipe-page-for-labeling · a Job Page records a judgment it does not make

**LOAD `haipipe-page` FIRST.** It owns the base: the sections and their fixed order, the five rows that define each one, the title rule, the Opening split, the numbering, and the evaluation contract.
This file adds only what a labeling page needs and an ordinary stage page does not.
It never repeats a base rule, because a copied rule goes a night out of date while the contract moves.

**What a labeling job is** comes from the plugin's current family contracts:
`subjective-label`, `label-building`, `label-scanning`, and
`subjective-label-workflow`. The historical design Board records how those laws
were reached; it is not a second runtime authority. This file says only what the
BOARD PAGE must carry.

## 🧩 The two kinds

```
kind          filename                          subject                closes when
──────────────────────────────────────────────────────────────────────────────────────
control       S-Label-Dash.md                   which jobs exist and   never; it is an
                                                where each one stands  inventory
per-target job S-Label-<n>-<corpus>-<target>.md ONE corpus and ONE     its human gate
                                                label target           and final audit close
```

**The test for a Page unit is QC3b's, and it is about people, not files**: can a person say yes to one thing here while saying no to the thing beside it?
A human authority can accept `authority` on a corpus and still refuse `social-proof` on the same corpus, so each target is its own Page/Job unit with its own gate.
Size does not decide it, and neither does how long the page grows.

**⛔ A ROUND IS NOT A PAGE UNIT.** Round 4 cannot be approved while round 3 is refused, because a round opens only after the previous checkpoint closed. Rounds are strictly ordered, so they fail the Page-unit test. A released round is an episode that groups its independently allocated Labeling Runs; it is not itself an extra umbrella Run.

**One target per page also keeps the class single-valued.** One item may carry two targets at once. Giving each target its own page keeps each page's HIGH, LOW, and NONE clean, and lets multi-label live across pages instead of forcing one page to hold classes that are not mutually exclusive.

## 🔁 The rule this Page Type exists for

**A round is a RECORD, never a division.**

Rounds keep arriving, and the base fixes the section order, so a `###` per round would make the Page grow without end and change shape every round.
One `### 2 · Rounds` division holds them all, newest first, as record blocks.
A released round is a grouping episode on disk (`ref/ref-assets.md` §3), and the
record is its readable index: it names the released operation Tickets, quotes
the card's wager, and scores the prospect against what happened. The canonical
Run envelopes remain under `runs/` and `results/`; the round folder is not a
second Run identity.

```markdown
**round_03** · closed 260806 · G_02 → G_03 · 60 items (40 challenge / 20 audit)
  🃏 card       gap HL, LN · expected disagreement on HL
  🎯 actual     disagreed on 11 of 60 · forecast said 9 (view/result.md)
  📜 diff       rule 3 and rule 4 added; no rule dropped · 2 prior rows flipped
  🗺 register   HL covered · LN still open at 3 items
  🚦 route      another round
```

Round 12 costs exactly what round 2 cost: five lines at the top, and no heading moves.
Record lines, never a markdown table.
The heavy artifacts stay in the run folder on disk; this ledger is the readable index into them.

## 📚 Content: five divisions that mirror the job

A labeling Page's Content mirrors one job lifecycle. It does not argue a question.

```
### 1 · What <target> means now      the boundary as the human draws it TODAY, with real items
### 2 · Rounds                       the ledger
### 3 · Building gates               may the Label Handoff be signed?
### 4 · Handoff, sealed test, scores empty until P2 Freeze signs the handoff
### 5 · Scanned corpus and audit     empty until Scanning runs
```

**§1 QUOTES the built label; it never redrafts it.** The current policy version
carries two rendered files, `cheatsheet.md` (the class rules and seven region
tests on one screen) and `gallery.md` (real confirmed items per region with the
human's reason); §1 shows the cheatsheet block and draws its seed cases from the
gallery, each with its item id. A §1 whose rules disagree with the closed
`G_<t>` is a stale view, and the policy version wins.

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
A3  the Building gates: quality · stability · coverage · risk        ← one Aim item each
A4  the signed handoff and seal hold, and every candidate executor is scored on them
A5  the scanned corpus is complete with provenance, and the audit says what is reliable
```

**A gate row READS its value from the newest `checkpoint.json`** (quality,
stability streak, coverage from `register.md`, risk), naming the checkpoint
that produced it. A gate row with a number no checkpoint holds is not evidence.

The payoff is that `## States` answers "may we stop" with no second source of truth, and a reader scanning it sees which gate blocks.
A control button on a division may read that state to decide whether it is enabled; it must never write a state of its own.

## 🌉 The two boards, and why every Job Page straddles them

**A Job Page and the method it obeys are always on DIFFERENT boards.**

```
design board                          job board
how the loop works                    what one job found
settles questions, then closes        records a judgment, never settles the method
   QA0 … QF5                             S-Label-Dash · S-Label-1 · S-Label-2 …
```

Keeping them apart is what stops "how we decided to do this" and "what this job produced" from being edited as one document.
It is also what makes the design board closable while jobs keep opening.

The cost is that **every reference from a Job Page to a method page is cross-board**, and cross-board behaves differently in the two places it appears:

- `requires:` and `style-from:` look a bare page id up in THIS board's pages. A method page is not one, so it needs a real path relative to this board's root. An id there reports `Stage Contract source not found` and then builds anyway.
- `### 🔗 Related Board Pages` may hold **only pages on this board**. A method page there reports `dead-related-page`, and its rendered link reports `dead-href`. Declare method pages in `board.md`'s `## Links` and cite them by name in a separate block.

Both failures let the page build, so nothing stops an author who gets it wrong. This is the single most likely defect in a new Job Page, which is why the specimen carries the warning three times.

## 🗂 The control page still needs a Stage Contract

A control page has no upstream, and the checker requires `## Stage Contract` on every S page regardless, reporting `missing-stage-section` without it.
Write the section and say **None, by design**, with the reason.
Leaving it out and leaving it empty look identical to the checker and different to a reader, and the reader is the one who has to know that a control page is not a Job Page missing its inputs.

Its Aims are about the ROSTER's completeness, never about any job's progress.
An Aim tracking a job's gate belongs on that Job Page, or the same fact lives in two places and one of them goes stale.

## 🧾 Evidence rules

- **A quoted item carries its id.** A paraphrased example cannot be re-judged in a later session, so it is not evidence. Quote verbatim and name the item.
- **A number names the round that produced it.** A score with no round behind it does not belong on the page.
- **A machine may PROPOSE a class; only a human session makes it gold.** Mark a proposal as a proposal in the line that carries it.
- **On a boundary item, propose the region and leave the class blank.** Proposing the class there pre-answers the thing the human is there to decide, which is the one thing this whole method reserves to them.
- **The seal is a field, not a promise.** Prefer a boundary that already exists in the data, such as a split the corpus shipped with, so "was the test read" is checkable in a manifest rather than trusted.

## 🚦 State

This is an S page, so `✅` means the whole job reached audited `D*`, and the
index counts it under the `Label` family. A signed freeze changes the handoff
row in §4 and opens Scanning; it does not complete the Page. A job deliberately
parked is `⏸️`, and a job with open Building or Scanning gates is `🟡` however
many rounds closed or however good its scorecard looks. `state:` never reads
`✅` from round metrics, a freeze signature alone, or model qualification.

`state:` is DERIVED, never typed from memory: 🟡 while any checkpoint or
scanning receipt is open, the handoff row in §4 shows `handoff/label-v1.yaml`'s
id and checksum once it exists (and stays empty as status before), §5 shows
`D*`'s manifest once the audit receipt closes, and ✅ requires that receipt.

## 📄 Files

| File | What it is |
|---|---|
| `template.md` | The specimen for a JOB Page. Copy it, fill it, delete each RULE comment as you satisfy it. |
| `template-dash.md` | The specimen for the CONTROL page. One per board, not one per job. |
| `CHANGELOG.md` | Version history, never loaded at invocation. |

Two kinds, two specimens. Copying the Job specimen for a control page produces a page with `requires:` it does not have and Aims about a job it does not own.

`examples-nlp/Project-Subjective-Label/diagram/01-label-runs-260807/SL-labeling-runs/S-Label-1-acibench-authority.md` is the reference implementation, and `S-Label-Dash.md` beside it is the control page.
Read them before writing a new one.
A worked example lives on a board and never in this folder, because a page that renders nowhere cannot show that its Decision Now row can be answered.

The `Label` family is admitted to the six lists that close the family set; `haipipe-board`'s own board records where they are and why a name missing from one of them fails differently in each.
