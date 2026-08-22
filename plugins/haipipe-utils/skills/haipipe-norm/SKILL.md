---
name: haipipe-norm
description: "The contract every describe-* normalizer obeys: free text in a cohort's own dialect, resolved against a reference bank, into numbers that carry their own provenance. Owns the five rules and the door signature; ships no code. Load before building or changing a normalizer. Trigger: normalizer contract, new normalizer, describe-food, describe-exercise, normalize door, provenance columns, basis column, haipipe-utils."
metadata:
  version: "0.1.0"
  last_updated: "2026-08-21"
  members: "describe-food · describe-exercise"
---

Skill: haipipe-norm
================================================================================

The head of the `haipipe-utils` normalizer family. It owns the CONTRACT and no
code; each member ships its own implementation.

    free text in a cohort's own dialect
        -> typed components
        -> a reference bank
        -> numbers that carry their own provenance

    🍎 describe-food       FoodName      -> USDA FDC
                                               -> Calories Carbs Protein Fat Fiber
    🏃 describe-exercise   ActivityType  -> MET compendium
                                               -> kcal MET minutes


WHY A CONTRACT AND NOT A BASE PACKAGE
--------------------------------------------------------------------------------

The nouns differ in every particular that matters. A food bank is keyed on a
description and an exercise bank on an activity code. A meal has components; a
session has intervals. The quantity a food log omits is grams, and the one an
exercise log omits is minutes.

What they share is the SHAPE of the problem, not its solution. A base class
written while only one member exists would fit neither, so this file holds the
rules and each member holds its own code.


THE DOOR
--------------------------------------------------------------------------------

Every member exposes exactly one entry point, with this signature:

    normalize(items: list[str]) -> list[dict]

Batch, order-preserving, one result per input, duplicates resolved once. It is
deliberately shaped like a third-party API call: a caller knows the signature and
nothing about the dialect layer, the bank, or the stage sequence, so all of those
can move or be rewritten without a caller changing.

A member picks its transport from `<MEMBER>_TRANSPORT`: `local` in process by
default, `http` against a running service. `local` is the default because a
pipeline cook must not fail because a daemon was down.

A workspace declares where the members live. That is what `env.sh` is for: a
space is the unit of work, and each space puts the normalizer skill dirs it wants
on `PYTHONPATH`, so the package imports as a bare top-level name.


THE FIVE RULES
--------------------------------------------------------------------------------

Each was earned by a real defect in `describe-food`; a new member gets them
for free.

1. ONE DOOR
   `normalize()` and nothing else is public. Anything a caller must know about
   the internals is a leak -- including a stage number in a keyword argument.

2. TYPE, DO NOT DELETE
   A placeholder is CLASSIFIED, never dropped: 'Just Carbs' is a declaration,
   'dinner' a meal slot, 'Unknown' unnamed. So it never reaches the bank, and it
   never sits in the denominator as a failed match. Deleting placeholders made a
   cohort read as 100% miss while its items were matching.

3. TRUSTED ONLY
   Only GOOD / OK / ALIAS may be written into value columns. WEAK and MISS stay
   NULL. A confidently wrong value is worse than a missing one, because nothing
   downstream can tell it apart from a measurement.

4. BASIS IS A COLUMN, NOT A FOOTNOTE
   Never invent the quantity the log did not state. When it is absent, say so in
   a `<X>Basis` column and report on the reference scale instead:
       food      per_meal | per_100g | None
       exercise  per_session | per_minute | None
   Basis is a SCALE, so it is a property of the whole record: mixing one scaled
   component with one unscaled yields a number that is neither.

5. PROVENANCE NEVER FOLDS
   `<X>Source`, `<X>Conf`, `<X>Basis`, and each answers ONE question. When a
   member derives its own input -- food's stage 0 reads a photo into a name --
   that derivation gets its OWN pair (`NameSource`, `NameConf`) and tags the
   source column, so a model's guess can never be mistaken for a report.
   Collapsing two independent failures into one column is the bug this rule
   exists for: 'the bank did not know it' and 'the log stated no portion' once
   shared a single code path.


ADDING A MEMBER
--------------------------------------------------------------------------------

A member is named `describe-<noun>`: the verb first, because the folder names what
the skill DOES to that noun, and a reader scanning the skill list groups the family
on sight instead of on a suffix they have to read to the end of.

    skills/describe-<noun>/
        SKILL.md            its dialect, its bank, its measured coverage
        <noun>norm/
            client.py       normalize() + the transport switch
            dialect.py      text -> typed components
            retrieve.py     component -> bank candidates + a confidence ladder
            aggregate.py    components -> one record, with its basis
        pipeline.py         CLI
        test_<noun>norm.py  regression suite

Then add one line to the workspace `env.sh` putting that skill dir on
`PYTHONPATH`, and register nothing else: the plugin manifest already covers the
folder.
