# State is read off disk, never stored

state: ✅ SETTLED
owner: JL
method: define each state by what a reader would find, and require opening the file

## Question
How does anyone know what state a probe entry is in?
State is DERIVED, never stored: it is computed by resolving the entry's target and opening what is there.
What turns on it is that a stored state is a claim about an agent, and an agent that crashed leaves a claim that looks exactly like success.

Six states are defined by what a reader finds rather than by what a worker asserts: `planned`, `commissioned`, `answered`, `read`, `answered-local` and `failed`.
The rule that makes this work is small and easy to skip, which is why it is stated twice: the reader OPENS the file, because an `ls` is not enough.
A target can exist and be `working`, or exist and be superseded, and both look identical to a listing.
That is exactly why two of the checker's FAIL conditions are `read-target-working` and `read-target-superseded`: the entry says it harvested an answer that was not there to harvest.

## Boundary
- ✅ Covered here
  The six entry states, how each is derived, and the rule that the file must be opened.
- ↪ Covered elsewhere
  The QA file's own state line is `QC1`; the checker conditions are `QC2`.

## Diagram
```
   planned          the entry exists; the target folder is missing (or `NEW …`)
   commissioned     the folder exists with no answered QA yet, OR target is `working`
   answered         the target QA file exists AND is `state: answered`
   read             `### a-executor` is non-empty
                    LEGAL ONLY against an answered, non-superseded target
   answered-local   target points into the consumer's own registries; no dispatch
   failed           dead target · folder deleted · the executor REFUSED

   ⚠️ the reader OPENS the file. An `ls` is not enough:
      a target can exist and be `working`, or exist and be superseded.
```

## Items to Finish
- [x] 🔎 Six states, each defined by what is found on disk
- [x] 📂 The open-the-file rule is stated, and two FAIL conditions enforce it
- [x] 🚫 No stored state anywhere; `/haipipe-probe status` derives on every run
- [x] 🧪 `status` has been derived against a real consumer
      260726, MISQ paper, 17 entries across 5 topic folders: **10 read, 5 planned (NEW), 2 with no target**.
      Every target that names a path resolves, and every resolved QA file carries a state line, so nothing is dangling.

## Where we are
Ruled, implemented in the `status` verb, and backed by two of the checker's conditions.
This is the strongest page on the board, in the sense that it is the one where the rule, the derivation and the check all agree.

- 260726 CC · 📊 Derived over 17 real entries
  10 `read`, 5 `planned` against a `NEW` target, 2 with no target line at all.
  A first pass reported ten dead targets and ten QA files missing their `state:` line, and both were wrong: targets are PROJECT-relative rather than repo-relative, and the state line is written as a bullet, `- state:   answered`, which a `^state:` grep does not match.
  Worth keeping as the lesson, because deriving state is precisely this face's subject and a careless derivation invented two failures that did not exist.

## Files
- `SKILL.md`
  The six states and the `status` verb.
