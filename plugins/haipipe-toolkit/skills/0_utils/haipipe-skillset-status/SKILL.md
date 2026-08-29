---
name: haipipe-skillset-status
description: >-
  Print one skill family's status as five tables, one per skill CLASS, each
  class scored on its own columns: DOOR (routes resolve), MACHINE (gates
  fired), CONTRACT (the eight-property page-type ruler), LIBRARY (assets and
  their clock), CRAFT (scope). Every row pairs a static score read off the
  contract text with a dynamic field record counted off the boards and git; a
  row with no field record is PROVISIONAL whatever its static score. Use when
  asking what state a family is in, which contract to rewrite next, or after
  any contract rewrite. Trigger: skillset status, family status, page type
  quality, contract quality, score the contracts, which contract is weakest,
  contract audit, 契约质量, 技能状态, /haipipe-skillset-status.
metadata:
  version: "0.3.0"
  last_updated: "2026-08-28"
  # version history: ./CHANGELOG.md (skill-scoped, never loaded at invocation)
---

# /haipipe-skillset-status · five classes, five tables, one row per skill

A skill family is not one kind of thing, so one ruler cannot score it. A DOOR
that routes owns no content law; a CONTRACT that owns a content law routes
nothing. Scoring both on the same columns produces a number that means
nothing for either. This skill cuts a family into five CLASSES and gives each
its own columns.

Every class shares one law across the two axes: the STATIC score is read off
the skill's own text, the DYNAMIC record is counted off the boards and git,
and **a row with an empty field record is written `(provisional)` whatever
its static score says**. A perfect contract nobody has run is a hypothesis,
not a grade. The paper family's round contract was the founding
counterexample: complete on paper, zero instances ever.

Born 260828 (JL: "每一类表有不同的 column"), generalizing the page-type-only
ruler of 0.1.0. Sibling of `field-test`: fieldtest checks a family
against a pre-registered run; this check scores a family against fixed
properties plus its accumulated record. This one picks WHICH skill to rewrite;
fieldtest proves the rewrite runs.

## 🗂 The five classes

```text
DOOR      routes intent to the member that owns it · owns no content law
MACHINE   the phase/gate machine · owns transitions, never content
CONTRACT  one artifact's persistent shape and closing rule · a page type
LIBRARY   assets consumed by the journey · outside it, on their own clock
CRAFT     a transform with no lifecycle · a tool, not a phase
```

Classify by what the skill OWNS, not by where it sits. A skill that owns a
closing rule is a CONTRACT even if it lives outside `page-types/`. A skill
nobody's gate ever reads is a CRAFT even if it is long.

## 🚪 DOOR · does every road lead somewhere

```text
| skill | ver | size | routes | resolve | stale | scaffold | desc shape |
```

```text
ver         frontmatter version:/last_updated: · MISSING is a finding, not a
            blank — the door is the file every other rewrite obliges, and an
            undated door cannot be asked whether it drifted
routes      count of skill names the door routes to
resolve     how many resolve to a real folder on disk · one DEAD fails the row
stale       names of things that no longer exist · a WRITTEN grandfather
            clause is not stale; an unmarked survivor is
scaffold    the folder figure in the door vs the folder on disk
desc shape  does the description answer "when should I be picked", or "what
            am I"
```

Mechanical: `grep -oh 'haipipe-[a-z0-9-]*' <door>/SKILL.md | sort -u` and test
each against `find -type d -name`.

## ⚙️ MACHINE · how much of the machine has ever run

```text
| skill | ver | size | phases | gates | receipt owner | fired live | gazette |
```

```text
phases         count
gates          count
receipt owner  of N gates, how many NAME the page whose Log row is the
               receipt · a gate whose receipt has no owner cannot be audited
fired live     of N gates, how many have a receipt on a real board · this is
               the column that separates a machine from a claim
gazette        renumbered gates mapped from their old ids, in-file
```

`fired live` is counted from the boards, never from the workflow file. A
machine whose gates are half unfired is not broken, but its untested half must
be visible.

## 📄 CONTRACT · the eight properties

Score ✓ (1) · ◐ (0.5) · ✗ (0) · — (not applicable, out of the denominator).
Every ✗ or ◐ NAMES the missing thing; every ✓ points at the line that earns
it. Scoring from memory is itself a defect: read the full file, every time.

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
④ 先报量再放行        size/budget stated before a person commits · the
   size-before-release machine estimates, the person releases · test: can an
                       unbudgeted row legally advance?
⑤ 逐字段合法性        each field/cell/column carries its own law: what is
   per-field-law       legal, what is a defect · a bare field list with no
                       legality rules is ◐ at best
⑥ 收据义务            which gate's receipt Log row lives on this page,
   receipt-duty        stated IN THIS contract in one sentence · a duty that
                       lives only in the machine file does not count
⑦ 关页检查可 grep     each closing check is testable by reading named files ·
   grep-able-checks    "every claim is well supported" is ✗; "every landed
                       path exists on disk" is ✓
⑧ 非职责显式          what this page never does, and where the neighboring
   explicit-non-jobs   pen's boundary runs · test: could two contracts both
                       claim the same write?
```

⑥ scores — (not ✗) when the page type correctly holds no gate and SAYS SO.
"Correctly none, said aloud" earns the —; silence earns the ✗.

Field record for a CONTRACT: `instances` (live pages declaring this type),
`fieldtest` (rounds that exercised it — a gap FOUND AND PATCHED is a credit,
reality touched the contract and it answered), `first-pass` (CHECK verdicts
closed vs routed back), `post-close` (repairs after CLOSE — escaped defects).

Tier: **EXERCISED** instances ≥ 1 and a fieldtest or CHECK pass · **USED**
instances ≥ 1, neither · **UNTESTED** zero instances ⇒ `(provisional)`.

**The population law.** `instances` counts pages on REAL boards — the work
products under `examples/` — and never the skill-documentation boards under
`skills/diagrams/`, whose pages carry a `page-type:` line because they
DESCRIBE a type, not because they instantiate it. Counting those makes an
unused contract look exercised, and the tier is the thing that breaks: the
paper family's round contract shows 1 page under the wide count and 0 under
this one, and 0 is the true answer — no `RD<NN>` folder has ever existed.
Whichever population a table uses, **the column must say which**; two tables
answering the same-sounding question with different numbers is the drift this
skill exists to catch.

## 📚 LIBRARY · assets, and whose clock they keep

```text
| asset | count | size | neutral | clock | consumed at | oldest verify |
```

```text
neutral        written for no single consumer · a bank page naming one paper
               is a defect, it has become that paper's note
clock          whose calendar refreshes it · the desk's own, never a
               consumer's deadline
consumed at    the gate or phase that reads it · an asset no gate reads is
               dead weight and should be named as such
oldest verify  the staleness floor · one date, the worst one
```

## 🔧 CRAFT · a tool, and what it may touch

```text
| skill | ver | size | last | lives in | scope | reversible |
```

```text
scope        what the transform may touch, stated as a path or artifact
             class · an unbounded scope is the whole finding
reversible   can its output be diffed against its input and undone
lives in     its real folder · a craft used by one family but stored in
             another is worth showing, not hiding
```

## 📦 Size · what a skill weighs, and whether it earns it

Every table's `size` cell is two numbers, `<SKILL.md chars>/<desc chars>`,
formatted like `18.8k/286`, both gathered by command:

```text
SKILL.md chars   what one invocation LOADS · wc -c SKILL.md
desc chars       what EVERY session pays in the skill listing, invoked or
                 not · len(frontmatter description)
```

Size is read against the skill's own CLASS in the family, never absolutely:
flag ⚠ when a member exceeds 2× its class median on either number, and always
name the family's heaviest member in the reading. A big skill is not a defect
by itself; a big skill whose extra weight is retirement narration, a second
telling, or copied law is — the calibration is haipipe-page 0.39.0, which cut
25% by character with zero rules lost, most of it two sections telling the
same story. A rule the reader never reaches is not shipped.

## 🧮 Reading the tables

Rank rows by what their repair BUYS, not by score. Then name the **top two
knife points** — the property × skill cells whose repair buys the most, each
with the concrete missing sentence and the next real event that will hit it. A
report that ranks without saying what to write next has done half the job.

## 🔁 Procedure

```text
1  enumerate the family's members · the folder is the registry, and a member
   stored elsewhere (a craft, a bank) is still a member
2  classify each into one of the five classes by what it OWNS
3  read each SKILL.md IN FULL, this session · no scoring from memory
4  gather the mechanical facts by command, not by recollection:
     versions      grep version:/last_updated: across the family
     routes        grep skill names in the door, test each with find
     inventory     haipipe-board/cli/pagetypes.py · the DERIVED page-type
                   table (page-types/ folders x check.py PAGE_TYPE_VALUES x
                   every page-type: line) · `--check` exits 1 on drift and
                   names each row · its counts use the WIDE population, so
                   read them through the population law before scoring
     instances     grep 'page-type:' under the real boards only
     gates fired   grep gate ids in the boards' Log rows
     assets        count the bank, read its oldest verify date
     sizes         wc -c each SKILL.md · desc length from frontmatter
5  emit five tables + the top-two knife points · unknown counters are `?`,
   never a guess
6  after any rewrite, re-run that row · the score travels in the commit message
```

The check never edits a skill, never averages away a ✗, and never scores a
family it cannot read end to end.

## 📌 Where the result lives

The INSTRUMENT lives here. The RESULT lives in the family's own `README.md`,
under a `Family status` section, **stamped with the date it was run and the
command that regenerates it**. That stamp is the whole discipline: a dated
table is a receipt, an undated one is a second authority that rots. This is
the Roadmap's Intake law — register, never restate — applied to the skills
themselves.

## 🧾 Worked example · the paper family, 260828

Five tables, abbreviated to the shape. The full run is in
`paper/README.md § Family status`.

```text
DOOR
| haipipe-paper | ⚠ NONE | 18.8k/286 | 12 | 12 OK | 0 | matches | use-when ✓ |

MACHINE
| haipipe-paper-workflow | 0.6.0 | 12.3k/303 | 6 | 8 | 8/8 | 4/8 | ✓ |

CONTRACT
| roadmap   | 0.3.1 | ⚠ 15.5k/669 | ✓✓✓✓✓✓✓✓ | 8/8 · EXERCISED     | 2 boards |
| narrative | 0.5.2 | 7.5k/374 | ✓✓✓◐✗✓◐✓ | 6/8 · USED          | G5 never ran |
| round     | 0.3.1 | 8.7k/325 | ✓✓✓✗✓✓◐✓ | 6.5/8 (provisional) | 0 instances ever |

LIBRARY
| venue/bank | 17 | — | ✓ | the desk's own | G5 · §1 | ? |

CRAFT
| haipipe-paper-revise-humanizer | 0.2.6 | 8.8k/336 | 08-05 | writing/ | section tex | ✓ |

knife 1  DOOR ver is MISSING · the only family member you cannot date-check,
         and the file every other rewrite obliges · needed: version: and
         last_updated: in its frontmatter · next hit: the very next rewrite
knife 2  MACHINE fired 4/8 · G5/G6/G7 have never left the page · needed:
         nothing written, only run · next hit: the MS narrative opens G5, the
         first decision letter opens G7 — that opening IS the field test
```

Two classes carried the news the old one-table ruler could not: the DOOR's
missing version, and the MACHINE's unfired half. The size column carries a
third: roadmap's ⚠ 15.5k/669 is 1.8× its class median on the body and 2.1× on
the description — the family's heaviest contract, priced for its next trim. Neither is a page type, and
neither would have appeared on the eight-property table at all.
