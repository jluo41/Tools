# When a ruling becomes shipped text
state: 🔴 OPEN
owner: JL
method: name the moment, name the destination file, and make the copy checkable rather than remembered

## Question
A ruling reaches `✅` on this board. What happens next, who does it, and how would anyone know it did not happen? The board is a working record and the skill is what ships, so a ruling that stays here binds nothing: no runtime reads a design board. Until the Law is copied into the owning skill, the decision exists and has no effect.

The mechanism is stated once, in `haipipe-board`'s own manual: a Q reaching `✅ SETTLED` has its `## Law` copied into the skill it governs, operating rules into `SKILL.md` and display or syntax specs into `ref/`. That is the whole contract, and nothing verifies any part of it. No check knows which skill a face governs, whether the copy was made, or whether the copy still matches the face it came from.

This is not hypothetical drift. On 2026-07-26 alone the two halves disagreed three times, in both directions, and none of the three was caught by anything: a check found them all by accident, hours later, while doing something else.

## Boundary
- ✅ Covered here
  The moment a ruling graduates, which file receives it, and how a reader verifies the copy happened and still matches.
- ↪ Covered elsewhere
  Whether the ruling is any good is the face that made it. What a Law reaching `haipipe-board` specifically must respect is `QA4`. How the board tool ships ITSELF is `QB-shipping-the-skill@boardform`, a different subject: that group is about `haipipe-board`'s manual, this face is about the 35 skills in `skills/paper/`. Whether a shipped skill actually WORKS is `QE2`, which owns the fresh-agent test.

## Diagram
```
   THE GRADUATION PATH, and where it is unverified

   ② this board                          ① skills/paper/
   ┌──────────────────────┐             ┌──────────────────────┐
   │ QA6 · state: ✅       │             │ haipipe-paper-folder │
   │                      │  copy the   │   SKILL.md           │
   │ ## Law               │ ──Law────▶  │   the rule, restated │
   │   the delete test    │  BY HAND    │   for an executor    │
   └──────────────────────┘             └──────────────────────┘
            │                                      │
            │  nothing records WHICH skill         │  nothing records
            │  a face governs                      │  WHERE it came from
            ▼                                      ▼
        ✗ no check that the copy happened
        ✗ no check that it still matches
        ✗ no check that a 🟡 face did NOT graduate early

   ── the three failures of 2026-07-26, all the same shape ────────
      ⓵  chips SHIPPED in ③; four faces here still called them unbuilt
                                          board BEHIND the skill
      ⓶  the round ruling landed HERE; haipipe-paper-round still
         described the layer it removed   skill BEHIND the board
      ⓷  ① specified a `venue:` frontmatter key in 12 places that
         ③'s parser cannot read           board WRONG about the skill

      same day · both directions · none detected by anything
```

```
   ── what a check COULD know, and what it could not ──────────────

   knowable, cheaply
     a face is ✅ and its ## Law is empty          → nothing graduated
     a face names a skill in ## Files and that
       file has no matching text                  → copy never made
     a face's Law changed after the skill's
       last_updated                               → copy went stale

   NOT knowable without a declaration
     WHICH skill a face governs. Today it is guessed from ## Files,
     which lists files a face TOUCHES, not the file it OWNS.
     That missing declaration is why none of the three failures
     above could have been caught mechanically.
```

## Content
### The rule exists and is stated in exactly one place
`haipipe-board`'s manual carries it: a `✅` Q has its `## Law` copied into the owning skill, operating rules into `SKILL.md`, display and syntax specs into `ref/`. Unsettled faces do not graduate, so the manual is always the sum of settled rules and nothing more.

That is a good rule. The problem is that it is a habit, performed by whoever happens to be working, with no record that it was performed.

### `## Files` is not an ownership declaration
Every face already lists files under `## Files`, and it is tempting to read that as "the skills this face governs". It is not. `QA6`'s `## Files` lists the four `1-build/` skills, the console and the router: files the ruling TOUCHES. The face does not own the console.

Without a field that says which skill a face owns, no check can ask whether the Law arrived. That is the first thing this face has to rule.

### Both directions fail, and they fail differently
```
 board BEHIND skill    someone shipped without ruling. The code is
                       right and the record is wrong. Cheap to fix,
                       and it rots the board's credibility.

 skill BEHIND board    someone ruled without shipping. The record is
                       right and the code is wrong. This is the
                       expensive one: an executor reads the skill.

 board WRONG           the ruling specified something the other side
                       cannot do. Neither copy is right, and only
                       running the thing finds it.
```
The third kind is the one nothing on either side can catch, because both documents are internally consistent. It took running the skill against a real paper to surface it.

## Items to Finish
- [ ] 📌 Rule how a face declares the skill it OWNS
      A `governs:` line in the frontmatter is the obvious shape, but the face grammar is a CLOSED whitelist owned by `haipipe-board` and ruled on `④` (`QA4`'s Law). So this needs either a key that already parses or a request to that board. Do not invent one.
- [ ] 🔁 Rule what graduation produces as EVIDENCE
      A Log line, a version bump, a line in the skill naming the face: any of these makes the copy checkable. None is required today.
- [ ] 🧪 A check for the cheap half
      `✅` with an empty `## Law`; a named skill with no matching text; a Law edited after the skill's `last_updated`. All three are mechanical.
- [ ] 🧠 Rule what happens when a ruling CANNOT be shipped
      Failure ⓷ is this case: the board ruled something the tool's grammar forbids. Today it was found by accident and fixed by rewriting the ruling. Nothing says whether that is the general answer.

## Where we are
The rule is stated in `haipipe-board`'s manual and practiced by hand. Nothing declares which skill a face owns, nothing records that a copy was made, and nothing compares the two halves afterwards.

The cost is measured rather than feared: three disagreements on 2026-07-26, in three different directions, none detected by any check. Two were found by a reader noticing a contradiction; the third was found only by running the skill against a real paper.

## Files
- `../BoardSkillBoard-260722/QB-shipping-the-skill/QB1-skillmd.md`
  How the board tool ships its own manual. The neighbouring subject, and worth reading before ruling here.
- `QA4-the-board-tool.md`
  Carries the three failures in its Diagram, and the Law that came out of the third.

## Log
260726 · Created. Three cross-package failures in one day, all previously logged on `QA4` because there was nowhere else to put them. `QA4` is about the `①`/`③` contract; this face is about how any ruling reaches any skill, which is a different question and had no home.
