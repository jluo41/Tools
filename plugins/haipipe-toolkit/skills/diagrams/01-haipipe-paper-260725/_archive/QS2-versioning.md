# When a version bump and a CHANGELOG entry are owed
state: 🟡 PARTIAL
owner: JL
method: one tag per body of work, written at the end, and an entry that says what changed and why rather than what was edited

## Question
A skill changed. Does it get a version bump, does it get a CHANGELOG entry, and when are they written? The failure this prevents is not sloppiness, it is noise: a skill bumped once per edit produces a version history nobody reads, and a history nobody reads cannot answer the only question a history is for, which is "why is this file like this?"

The rule already exists and came from JL rather than from a convention: **one tag per body of work, written at the END, never per pass.** It overrode a skill-diagnose procedure that bumped per phase. It is a real, load-bearing rule and it currently lives in one agent's memory and no document, which means the next agent will not follow it.

What is genuinely unruled is the other half: what an entry must CONTAIN. On 2026-07-26 twenty skills were bumped and twenty entries written, and their quality varies precisely with whether the writer had a measurement in hand.

## Boundary
- ✅ Covered here
  When a bump is owed, when an entry is owed, what an entry must contain, and what "one body of work" means.
- ↪ Covered elsewhere
  Whether the change should have been made is the face that ruled it. Whether the change reached the skill at all is `QS1`. Where a per-skill version is DISPLAYED is `QS3`.

## Diagram
```
   ONE TAG PER BODY OF WORK  (JL, overriding haipipe-skill-diagnose)

   ✗ per pass                        ✓ per body of work
   ┌──────────────────┐              ┌──────────────────┐
   │ pass 1  → 0.2.1  │              │ pass 1  ┐        │
   │ pass 2  → 0.2.2  │              │ pass 2  ├ ONE    │
   │ pass 3  → 0.2.3  │              │ pass 3  ┘        │
   │ pass 4  → 0.2.4  │              │   ↓              │
   └──────────────────┘              │ 0.3.0 + 1 entry  │
    four entries nobody reads        └──────────────────┘
                                      written at the END

   ── 2026-07-26, as a worked example ─────────────────────────────
      35 skills in the family
      20 bumped · 20 CHANGELOG entries · 0 bumps without an entry
      the whole day was ONE body of work: "align the family with
      QA6's layout ruling". Every skill got one tag, not one per file.
```

```
   ── what separates an entry that works from one that does not ───

   ✗ "Updated paths to the new layout."
        true, useless. It restates the diff.

   ✓ "conform 0.2.0 — the delete test is now an EXECUTABLE check.
      Block J resolves every \input, \includegraphics and
      \bibliography target the masters reach and asserts none sits
      behind a number. Verified: exit 1 on the MISQ paper, 56
      findings, 18 of them delete-test failures. Before this,
      nothing could tell you a paper folder was correct, and the
      old version FAILED a folder that was."

   the difference is not length. It is that the second one carries
   a MEASUREMENT and a CONSEQUENCE, so a reader six months later
   can tell whether the change did what it claimed.
```

## Content
### What counts as one body of work
The unit is the ASK, not the file and not the session. "Align the family with the layout ruling" is one body of work even though it touched twenty skills across four phases over several hours. Two unrelated asks in one session are two bodies of work and two tags.

The test that settles it: would a reader want these described together? If yes, one entry. If the entry would need the word "also", it is probably two.

### Written at the END, and why that is not just tidiness
Writing the entry last is what makes it accurate. An entry drafted at the start describes an intention; the same entry written at the end describes what actually happened, including the parts that turned out differently. On 2026-07-26 the `conform` entry could only be written last, because its most useful line, the 56 findings, did not exist until the script ran.

### What an entry owes
```
 the ASK        what was wanted, in the asker's terms
 the CHANGE     what is now different, specifically enough to act on
 the EVIDENCE   a number, a path, a verdict. "Verified: ..." beats
                "should now work"
 the WHY        what was wrong before. An entry that only describes
                the after-state cannot be judged
```
The fourth is the one most often skipped and the one a reader most needs.

### The one thing that is enforced today
Every skill's `SKILL.md` carries `version:` and `last_updated:`, and every CHANGELOG is scoped to its own skill and never loaded at invocation. On 2026-07-26 all 20 bumped skills had a matching entry, with zero bumps undocumented. That is the practice holding, not a check holding it: nothing verifies the pairing.

## Items to Finish
- [x] 📌 One tag per body of work, written at the end
      JL's rule, overriding `haipipe-skill-diagnose`'s per-phase bump. Recorded here so it stops living only in a session's memory.
- [ ] 📝 Rule what an entry must contain
      The four-part shape above (ask, change, evidence, why) is a proposal drawn from what the good entries of 260726 happen to have, not a ruling.
- [ ] 🧪 Check that a bump has an entry
      Mechanical: read `version:` from `SKILL.md`, grep `[<version>]` in the sibling `CHANGELOG.md`. It passed for all 20 today by practice; nothing would have said so if it had not.
- [ ] 🔢 Rule what earns minor versus patch
      Today's pass used minor for a rewrite and patch for a correction, by feel. The family is pre-1.0, so nothing is riding on it yet, and that is exactly when it is cheap to decide.

## Where we are
The one-tag-per-body-of-work rule is settled and now written down. The practice is holding: 20 of 20 bumps on 2026-07-26 carried a matching CHANGELOG entry.

What is unsettled is the entry's contents and the minor-versus-patch line, and nothing checks the bump-to-entry pairing that currently holds by habit alone.

## Files
- `CHANGELOG.md` beside every `SKILL.md`
  Skill-scoped, newest first, never loaded at invocation. 20 of the family's 35 carry a 2026-07-26 entry.
- `../01-boardform-260722/QB-shipping-the-skill/QB1-skillmd.md`
  The neighbouring subject: how the board tool's own manual is kept.

## Law
ONE TAG PER BODY OF WORK, and the tag is written at the END. A version bump is per ask, never per pass and never per file. An entry drafted before the work describes an intention; the same entry written after describes what happened, which is the only version worth keeping (JL 260726, overriding `haipipe-skill-diagnose`'s per-phase procedure).

A bump without a CHANGELOG entry is incomplete work.

## Log
260726 · Created. The one-tag rule was given by JL earlier and lived only in an agent's memory, which is not a place a rule can bind anyone. Grounded in the day's own numbers: 35 skills, 20 bumped, 20 entries, one body of work.
