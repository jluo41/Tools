# Where per-skill status lives
state: 🔴 OPEN
owner: JL
method: one home for "is this skill current", derived where possible, and never on a face about something else

## Question
Thirty-five skills ship in this family. Which of them are current with the board's rulings, which are behind, and where does a reader look to find out? Today the answer is a table on `QA6`, a face about what exists in a paper FOLDER. It is there because there was nowhere else, and a status table on a face about folders is exactly the kind of thing that goes stale without anyone noticing, because nobody visits a folder face to check on skills.

The table earns its keep, which is why it survived: it carries a per-skill verdict, a version, and a debt count, and building it is what surfaced that `haipipe-paper-stage`'s real debt was in eight run-time contracts rather than in its `SKILL.md`. Measuring per file understated the work by a factor that changed the whole priority order.

So the question is not whether to track this. It is where it lives, and how much of it can be derived rather than typed.

## Boundary
- ✅ Covered here
  Where per-skill currency is recorded, what "current" means, and which parts can be computed instead of maintained.
- ↪ Covered elsewhere
  How a ruling reaches a skill at all is `QS1`; when a bump is owed is `QS2`; how a skill is proven to work is `QE2`. What the paper folder contains, which is what `QA6` is actually about, stays there.

## Diagram
```
   THE TABLE, AND WHERE IT IS SQUATTING

   QA6 · ⑦ The paper folder: what exists on disk
   ├─ the delete test                    ← the face's real subject
   ├─ one family, one folder             ← its real subject
   └─ WHO WRITES WHAT + UPDATED?         ← a SKILL STATUS TABLE
        Paper-X/        enter        ✅ 0.6.1
        0-lifecycle/    folder       ✅ 0.5.1
        1-probes/       probe        ✅ 0.7.0
        ...
        whole tree      conform      ✅ 0.2.2
                                     ▲
                        this is not about the folder.
                        It is about the skills, on a face
                        nobody opens to ask about skills.

   ── what the table is FOR, and it is not decoration ──────────────
      building it is what caught the real priority order:

        per SKILL.md          enter 9 · compile 6 · lifecycle 6
        per skill DIRECTORY   stage 22 old-path + 12 STATUS.md   ◀ worst

      haipipe-paper-stage's debt was in eight stages/*/stage.md
      contracts, whose paths RESOLVE AT RUN TIME. A stale path there
      does not read wrong; it WRITES to the wrong place.
```

```
   ── derived versus typed ────────────────────────────────────────

   DERIVABLE, today, with a grep
     version           SKILL.md frontmatter
     last_updated      SKILL.md frontmatter
     has an entry      grep [version] in the sibling CHANGELOG
     names a dead path  grep the retired vocabulary

   NOT DERIVABLE without a declaration
     "is this skill current with the board"
       requires knowing which face governs it → Q-Skill-graduation

   So three of the four columns are free, and the fourth is blocked
   on the same missing declaration that blocks graduation.
```

## Content
### Why it cannot stay on QA6
A face answers one question. `QA6` answers "what is in a paper's folder", and a reader arrives there asking about directories. The skill table is correct and useful and invisible to anyone who needs it, and it will be the last thing updated when a skill changes, because updating it is not part of changing a skill.

The rule this violates is one the board already applies elsewhere: a thing lives on the face whose question it answers.

### Most of it should not be typed at all
Three of the four columns are already on disk in machine-readable form: `version:` and `last_updated:` in the frontmatter, the CHANGELOG pairing by grep, and dead-vocabulary counts by grep. A page that RESTATES those will go stale exactly as fast as it is convenient.

What a page can usefully hold is the part no grep can produce: the judgement of whether a skill is current with a ruling, and the ordering by binding rather than by count, which is what made 2026-07-26's sweep tractable.

### The measurement that changes the order
```
 counted per SKILL.md       counted per skill DIRECTORY
 enter          9           stage    22 old-path · 12 STATUS.md
 compile        6           enter     8 · 16
 lifecycle      6           lifecycle 6 ·  7
```
`haipipe-paper-stage` does not appear in the left column at all, because its debt is not in its `SKILL.md`. It is in `stages/*/stage.md`, in `artifact:`, `probes:` and `output:` fields that resolve when a stage runs. That distinction, a path that is READ versus a path that is EXECUTED, is what this page exists to keep visible.

## Items to Finish
- [ ] 🏠 Rule the home
      A page here, a generated report beside the skills, or a column the console prints. A page that duplicates greppable state is the option most likely to rot.
- [ ] ⚙️ Generate the three derivable columns
      `version`, `last_updated`, and bump-to-entry pairing are all one grep each. Typing them is the failure mode.
- [ ] ✂️ Move the table off `QA6`
      Blocked on the home above; `QA6` keeps the delete test and the folder rules, which are its actual subject.
- [ ] 📏 Rule what "current" means
      Blocked on `QS1`: without a declaration of which face governs a skill, currency cannot be computed, only asserted.

## Where we are
The table exists, is accurate as of 2026-07-26, and is on the wrong face. Twenty of the family's thirty-five skills carry a 2026-07-26 entry; the other fifteen were not in scope for that ruling rather than being behind on it, and nothing on disk records that distinction.

Three of the four columns are derivable today and are currently typed by hand.

## Files
- `QA6-paper-scaffold.md`
  Carries the `WHO WRITES WHAT` / `UPDATED?` table today, in its Diagram.
- `QS1-graduation.md`
  Blocks the fourth column: currency needs an ownership declaration.

## Log
260726 · Created. The status table was written onto `QA6` the same day, when JL asked which skills a rule touched and whether they were done. It answered the question well and belongs on a face about skills, not on a face about folders.
