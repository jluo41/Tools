# One source for the vocabulary

state: 🟡 PARTIAL
owner: JL
method: name the source file, list what must be copied from it, and accept that nothing enforces the copy

## Question
Five skills use the same field names and state values; which file is allowed to define them?
`SKILL.md`, which says so in its own first lines, and the others COPY the canonical strings from it.
What turns on it is the real failure mode of a shared vocabulary, which is not disagreement but silent divergence.

The list of what must be propagated is explicit, and that is the useful part: a `state:` value, a field name (`state:` / `started:` / `by:`), the TTL constant `QA_WORKING_TTL_HOURS`, the timestamp format `YYYY-MM-DDTHH:MM`, and the `set -C` idiom.
Change any of those here, then propagate.
Nothing checks that the propagation happened, so the rule is a convention held by whoever remembers it, and today gave the board two fresh examples of what that is worth: a documented behaviour that was never implemented, and a cross-board id list that a rename silently emptied.

## Boundary
- ✅ Covered here
  Which file owns the vocabulary, what must be copied from it, and how a divergence would be noticed.
- ↪ Covered elsewhere
  The values themselves are `QC1` and `QC3`; the checker that consumes them is `QC2`.

## Items to Finish
- [x] 📖 The source file is named, and says so in its own first lines
- [x] 📋 The list of propagated strings is explicit rather than implied
- [ ] 🔍 A divergence is detected rather than discovered
      Five consumers copy these strings and nothing compares them.
      A grep that asserts each canonical string appears identically in every copier would close it, and would have caught a rename on the day it happened.
- [ ] 🧠 JL rules what happens on a conflict
      "This file wins" settles precedence and not procedure: nothing says whether a diverging skill is fixed, blocked, or merely noted.

## Where we are
The rule is stated clearly and in the right place, at the top of the file it governs.
It is held by memory alone: no check compares the copies, so the first sign of divergence would be a checker passing on a file it no longer understands.

## Files
- `SKILL.md`
  The vocabulary rule and the list of strings that must be propagated.
- `CHANGELOG.md`
  Where a vocabulary change should be visible to the skills that copy from it.
