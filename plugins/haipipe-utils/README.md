haipipe-utils
================================================================================

Normalizer utilities for the haipipe pipeline.

Every skill here does one job, on a different noun:

    free text in a cohort's own dialect
        -> typed components
        -> a reference bank
        -> numbers that carry their own provenance

    describe-food       FoodName      -> USDA FDC       -> Calories Carbs
                                                                 Protein Fat Fiber
    describe-exercise   ActivityType  -> MET compendium -> kcal MET minutes


WHY THEY ARE SIBLINGS AND NOT ONE SKILL
--------------------------------------------------------------------------------

The nouns differ in every particular that matters: a food bank is keyed on a
description and an exercise bank on an activity code, a meal has components and
a session has intervals, and the quantity a food log omits is grams while the
one an exercise log omits is minutes. What they share is the SHAPE of the
problem, not the solution to it.

So `haipipe-norm` holds the contract and no code, and each member ships its own
implementation. A shared base package written while only one member exists would
fit neither.


THE DOOR
--------------------------------------------------------------------------------

A caller never imports a member's internals. It imports the member's client and
calls one function:

    from foodnorm import normalize
    out = normalize(["fried rice; egg", "Cucumber 100g"])

That is deliberately the shape of a third-party API call: the caller knows a
signature, and nothing about the dialect layer, the bank, or where either lives.
`client.py` chooses the transport (`local` in process, or `http` against a
running service) from `FOODNORM_TRANSPORT`.


LAYOUT
--------------------------------------------------------------------------------

    .claude-plugin/     plugin.json + marketplace.json
    skills/
        haipipe-norm/               the contract every member obeys, no code
        describe-food/        SKILL.md · client.py · food_norm/ · tests
        describe-exercise/    same six files, when it is built
