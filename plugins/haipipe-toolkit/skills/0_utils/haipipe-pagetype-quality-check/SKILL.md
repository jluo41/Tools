---
name: haipipe-pagetype-quality-check
description: >-
  Score a Page Type contract on two axes: a STATIC eight-property ruler read
  off the contract text (grain law with a why, borrowed vocabulary, address
  grammar, size-before-release, per-field legality, receipt duty, grep-able
  closing checks, explicit non-jobs) and a DYNAMIC field record counted off
  the boards and git (live instances, fieldtest gaps, CHECK first-pass rate,
  post-close repairs). Emits one row per contract with a total score; a
  contract with zero instances may only score PROVISIONAL. Applies to any
  page-type family — paper, insight, design. Use when deciding which
  contract to rewrite next, whether a family is good enough to trust, or
  after any contract rewrite. Trigger: page type quality, contract quality,
  quality check, score the contracts, which contract is weakest, contract
  audit, 契约质量, /haipipe-pagetype-quality-check.
metadata:
  version: "0.1.0"
  last_updated: "2026-08-28"
  # version history: ./CHANGELOG.md (skill-scoped, never loaded at invocation)
---

# /haipipe-pagetype-quality-check · two axes, one row per contract

A Page Type contract is a claim about how instances of that page will be
written. Its quality is measurable on two axes, and both are needed: the
STATIC ruler catches a contract written badly, the DYNAMIC record catches a
contract written beautifully that no one can actually run. The round
contract of the paper family was the founding counterexample: complete on
paper, zero instances ever — its static score meant nothing until reality
touched it.

Born 260828 from the paper family's contract audit, where the roadmap 0.2.0
rewrite set the bar the ruler generalizes. The ruler is a sibling of
`haipipe-fieldtest`: fieldtest checks a SKILL FAMILY against a pre-registered
run; this check scores one CONTRACT against fixed properties plus its
accumulated field record.

## 📏 The static ruler · eight properties, read off the contract text

Score each property ✓ (1) · ◐ (0.5) · ✗ (0) · — (not applicable, excluded
from the denominator). Every ✗ or ◐ must NAME the missing thing; every ✓
must be able to point at the line that earns it. A property scored from
memory of the contract is a defect: read the full file in the scoring
session, every time.

```text
① 切分法则带 WHY      the grain law teaches how to CUT instances, not just
   grain-law-why       which sections exist · test: does it say what a wrong
                       cut looks like and why that cut fails?
② 词汇是借的          names come from the layer that executes, or from the
   borrowed-words      stored artifact's own field names · coined vocabulary
                       nobody else uses is a fail (the 一眼AI rule)
③ 地址语法            one string means the same thing across plan, disk,
   address-grammar     log, and receipt · test: can a reader resolve an id
                       without a legend?
④ 先报量再放行        size/budget must be stated before a person commits ·
   size-before-release the machine estimates, the person releases · test:
                       can an unbudgeted row legally advance?
⑤ 逐字段合法性        each field/cell/column carries its own law: what is
   per-field-law       legal, what is a defect · a bare field list with no
                       legality rules is ◐ at best
⑥ 收据义务            which gate's receipt Log row lives on this page,
   receipt-duty        stated IN THIS contract in one sentence · a duty that
                       lives only in the workflow file does not count
⑦ 关页检查可 grep     each closing check is testable by reading named files ·
   grep-able-checks    "every claim is well supported" is ✗; "every landed
                       path exists on disk" is ✓
⑧ 非职责显式          what this page never does, and where the neighboring
   explicit-non-jobs   pen's boundary runs · test: could two contracts both
                       claim the same write?
```

⑥ is scored — (not ✗) when the page type correctly holds no gate: a library
page, or a page whose contract states outright that its receipts live
elsewhere. "Correctly none, said aloud" earns the —; silence earns the ✗.

## 📊 The dynamic record · four counters, read off the boards and git

```text
instances      live pages declaring this page-type, across all boards
fieldtest      rounds that exercised this contract + gaps attributed to it
               (a gap FOUND AND PATCHED is a credit, not a debit — it means
                reality touched this contract and the contract answered)
first-pass     of this type's CHECK verdicts, how many closed vs routed back
post-close     repairs to instances after CLOSE (escaped defects)
```

The counters come from `git log`, the boards' Log rows, and CHECK receipts —
never from recollection. When a counter cannot be computed, write `?`, not a
guess.

## 🧮 The total score

```text
static   earned / applicable, shown as n/8-style fraction (◐ = 0.5)
tier     EXERCISED   instances ≥ 1 AND at least one fieldtest or CHECK pass
         USED        instances ≥ 1, no fieldtest and no CHECK yet
         UNTESTED    zero instances
total    "<static> · <tier>" — e.g. "8/8 · EXERCISED" or "6.5/8 · USED"
```

**The provisional law**: an UNTESTED contract's total is always written
`(provisional)` after the score, whatever the static number says. A perfect
static score with zero instances is a hypothesis, not a grade — the dynamic
axis has no data, and the report must not let a reader mistake polish for
proof.

## 📋 The report

One table, one row per contract, most recently rewritten first; then the
knife points:

```text
| contract | ver | ①why | ②词 | ③址 | ④量 | ⑤格 | ⑥据 | ⑦查 | ⑧界 | total | field record |
```

After the table, name the TOP TWO knife points — the property×contract cells
whose repair buys the most, each with the concrete missing sentence it needs
and the next real event that will hit it. A report that only ranks without
naming what to write next has done half the job.

## 🔁 Procedure

```text
1  enumerate the family's contracts (its page-types/ folder is the registry)
2  read each SKILL.md IN FULL, this session · no scoring from memory
3  score the eight properties, line-anchored · ✗/◐ name the missing thing
4  count the four dynamic counters from boards and git · ? over guesses
5  emit the table + the top-two knife points
6  after any contract rewrite, re-run for that row · the score travels in
   the rewrite's commit message
```

The check never edits a contract, never averages away a ✗, and never scores
a family it cannot read end to end. It pairs with `haipipe-fieldtest`: this
check picks WHICH contract to rewrite; fieldtest proves the rewrite runs.

## 🧾 Worked example · the paper family, 260828

The audit that birthed this skill, post roadmap-collection merge:

```text
| contract  | ver   | ①| ②| ③| ④| ⑤| ⑥| ⑦| ⑧| total              | field record          |
|-----------|-------|--|--|--|--|--|--|--|--|--------------------|-----------------------|
| roadmap   | 0.3.0 | ✓| ✓| ✓| ✓| ✓| ✓| ✓| ✓| 8/8 · EXERCISED    | 2 boards · 1 FT · 3 gaps patched |
| seed      | 0.5.3 | ✓| ✓| ✓| —| ✓| ✓| ✓| ✓| 7/7 · EXERCISED    | 2 boards · settle+G4 ran |
| ideation  | 0.5.4 | ✓| ✓| ✓| —| ✓| ✓| ✓| ✓| 7/7 · EXERCISED    | 2 boards · CHECK routed HOLD |
| venue     | 0.4.0 | ✓| ✓| ✓| —| ✓| —| ✓| ✓| 6/6 · EXERCISED    | 17 bank pages, consumed |
| section   | 0.4.0 | ✓| ✓| ✓| ◐| ◐| —| ✓| ✓| 6/7 · EXERCISED    | 16 pages, most-used |
| narrative | 0.5.2 | ✓| ✓| ✓| ◐| ✗| ✓| ◐| ✓| 6/8 · USED         | 2 pages · G5 never ran |
| round     | 0.3.1 | ✓| ✓| ✓| ✗| ✓| ✓| ◐| ✓| 6.5/8 (provisional)| 0 instances ever |

knife 1  narrative ⑤ · the 17-field section-map row has no per-field law ·
         needed: one legality sentence per field, roadmap-column style ·
         next hit: the C5 inheritance decision when the MS round opens
knife 2  round ④ + UNTESTED · concerns are never counted before triage ·
         needed: a ledger-size statement before dispositions · next hit:
         the MS/WISE decision letters — its first opening IS a field test
```
