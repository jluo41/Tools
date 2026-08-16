# Adding a stage: the test, the four files, the two flags
state: 🟡 PARTIAL
owner: JL
method: admit a stage by a test that can say no, then declare it in four files and two flags

## Question
How do you add a lifecycle stage, and what stops you from adding one that should not exist? Today the whole procedure is a single sentence, `SKILL.md:193`, "Adding a stage = one folder + one row in `index.yml`", and the test that would refuse a bad stage is written nowhere at all. That combination is how a lifecycle becomes a folder of chores: every addition is individually reasonable, nothing ever argues against one, and after six of them nobody can say what the stages have in common.

The test is one question, one artifact, one gate. It already does real work: it is why "compile the manuscript" is not a stage of section-edit, and it is what separates resource, which asks whether evidence EXISTS and can carry a claim, from claims, which RUNS the thing that moves a claim's status. Without it those two collapse into "the data stage" and the paper loses the difference between having evidence and having a verdict.

The rest is declaration. Four files, two of which are one line each, and two flags that decide how the stage varies: `runs:` for its grain and `venue_aligned:` for whether it survives a change of journal. Both are set here, at add time, and both have a one-sentence test. What we want is a definition strong enough to refuse a ninth stage, because one that admits everything is doing no work.

## Boundary
- ✅ Covered here
  What makes something a stage, the files you touch to add one, the required contract core, and the two variation flags.
- ↪ Covered elsewhere
  What `template.md` holds is `QB2`; how the stage reaches its page is `QB3`; what the phases do is `QB4` and below; whether a stranger can do all this unaided is `QE2`.

## Diagram
```
   ➕ ADDING A STAGE.   the test comes first; the files are the easy part.

   ── ① THE TEST, and it must be able to say NO ─────────────────────
      ONE question  ·  ONE artifact  ·  ONE gate
        two questions   ──▶  that is TWO stages
        no gate         ──▶  that is a PHASE              (→ QB4)
        no artifact     ──▶  that is a FOLDER
      ⛔ compile · submit · answer reviewers sit OUTSIDE the eight,
         and the reason has never been written down.

   ── ② THE FOUR FILES ──────────────────────────────────────────────
      1  stages/index.yml                            + ONE ROW
           key · order · dir · triggers · migrated
           READ ON EVERY INVOCATION, including ones that turn out to
           be about something else. Nothing belongs here that a router
           does not need in order to CHOOSE.

      2  stages/<order>-<key>/                       + ONE FOLDER
      3    stage.md      the contract · 24 required fields
      4    template.md   the shape DRAFT fills                (→ QB2)

      ✅ no new skill · no version bump · no router edit

   ── ③ THE TWO FLAGS, set here and nowhere else ────────────────────
      runs:            once  |  per-unit
        TEST  could a human approve one unit and reject another?
              yes ──▶ per-unit.   display: 11 assets, obviously yes.
                                  seed: there is one thing, no.

      venue_aligned:   free  |  aligned  |  venue_role
        TEST  could a different journal change this stage's ANSWER?
              yes ──▶ aligned.    a claim's status does not change
              because a different editor reads it. A narrative's
              ORDER does.
              venue_role is the pin itself: 2a-venue is neither.

   ── ④ WHAT A CONTRACT MAY NOT DO ──────────────────────────────────
      ✗ spell an S filename        board tooling owns it       (→ QB3)
      ✗ leave a path dangling      declare `blocked_on: <Q page>`
      ✓ `artifact_fallback:`       while any live paper predates the
                                   layout, and a run says which it used

   ── the required core, measured across all eight ──────────────────
      IDENTITY   key order title one_line
      BOARD      board_family board_unit                       → QB3
      EXECUTION  phases gates probe_depth runs needs_paper      → QB4
      PRODUCT    artifact template sections formatting          → QB2
      EVIDENCE   probes q_id_pattern q_anchor                   → QB6
      GRAPH      upstream downstream handoff
      CLOSING    done_criteria closed_when exit_when            → QB8
```

## Content
### The test that admits a stage, and can refuse one
One question, one artifact, one gate. The rule is stated and followed, and nothing enforces it: a stage that grows a second question grows it silently, and the only symptom is a gate nobody can pass. That is what happened to display before it was split, and it was caught by a human noticing a thirteen-record checklist that would not close.

Its worth is entirely in whether it can refuse a NINTH stage, and it has never been asked to. Compiling, submitting and answering reviewers all sit outside the eight, and the reason has never been argued in writing, so the next addition will be appended rather than argued.

### Why two files, read at different rates
`index.yml` is read on EVERY invocation, including ones that turn out to be about something else. `stage.md` is loaded only for the stage actually picked. That difference in read rate is the whole constraint on what may live where: the index holds only what a router needs in order to CHOOSE, and everything else goes in the contract. It is the reason the index has stayed readable while the contracts have grown to 24 required and 43 stage-specific fields.

There is no stage object anywhere in the code. A stage IS its `stage.md` frontmatter. That changes what a ruling on this board means: settling the grain is a change to `runs:`, settling the spending ceiling is a change to `probe_depth:`, and a face here that cannot name the field it would change has not finished its work.

### The two flags, and why they are set here
Both are variation, and variation declared later is variation that has already been improvised. `runs:` follows the human gate rather than the folder: per-unit exactly when one unit can be approved while another is rejected. `venue_aligned:` follows the line between what is true and how it is told: seed, resource and claims survive a retarget untouched; pitch, narrative, display and section-edit are rewritten.

Display is where both flags still hurt. It qualifies as per-unit under the test and still carries `runs: once`, so its `artifact:` cannot resolve and is declared `blocked_on:` rather than passing silently. And it sits on the aligned side, which means a rejected paper retargeted elsewhere keeps every claim and may keep almost none of its figures. That is expensive and it is still the right side of the line: a figure is an argument made FOR a venue, not a fact about the world.

## Items to Finish
- [x] 📝 The eight questions are written down
      `PHILOSOPHY.md` carries them as a table, and each `stage.md` repeats its own as `one_line`.
- [x] 🗂 The two-file split is implemented
      Eight stages, one row each, one contract each, and the index's own header states the rule and the reason.
- [x] 📐 State the required fields of a contract
      `CONTRACT.md`, from a measurement of all eight: 24 required, 43 stage-specific, plus the conditional set and the two retired fields.
- [x] 🔧 Repoint every contract onto the live S faces
      Six stages resolved, `log:` retired, read paths repointed, `board_slug:` added, `venue_role:` added for the venue stage, which is neither free nor aligned because it is the stage that picks the venue.
- [x] 🛟 Do not break the papers that predate the restructure
      Each repointed contract declares `artifact_fallback:`, and a run must say which of the two it used.
- [x] 🧠 Rule the grain, with the test
      Per-unit exactly when units gate independently. Display and section-edit are per-unit; seed, resource, claims, venue, pitch and narrative are single-output by the same test.
- [x] ✂️ The venue split is stated
      `PHILOSOPHY.md` and the per-stage `venue_aligned:` field.
- [ ] 🧠 Rule whether the one-question test is enforceable
      A stage whose gate cannot be answered in one human sentence has probably grown a second question. That is a checkable symptom; decide whether CHECK is where it is caught.
- [ ] 📐 State what disqualifies something from being a stage
      Compiling, submitting and responding to reviewers all sit outside the eight. Say why, so the next addition is argued rather than appended.
- [ ] 📐 Give display a resolvable artifact
      It qualifies as per-unit and still declares `runs: once`, so its `artifact:` dangles behind `blocked_on: QB1`. Needs `unit:`, `units_from:` and a pattern rather than a path.
- [ ] 🧠 Rule where contract checking lives
      A: the paper skill checks its own contracts, which is what exists now. B: `haipipe-board/`'s `stage.py` grows a verb, one checker for everything, at the cost of teaching board tooling what a paper stage is. C: no checker, and `CONTRACT.md` alone. JL raised this on 260726 and it is not settled.
- [ ] 🧠 Rule whether craft prose belongs in the contract
      `CONTRACT.md` states the case for keeping it: the executor that reads the machine fields is the one that must do the work, and a split would let the two drift. That is a proposal, not a ruling.
- [ ] 📐 State what retargeting actually does to each aligned stage
      Rewrite from scratch, or re-derive against the new blueprint while keeping the argument? These are different operations and the contracts do not distinguish them.
- [ ] 🧠 Rule whether a retarget reopens the claims stage
      It should not, by this design. Say so explicitly, because the temptation at a new venue is to re-cut the claims to fit.
- [ ] ✍️ Write the add procedure down where an adder will find it
      Four files, the test, and the two flags. Today it is one sentence at `SKILL.md:193` and a field list in `CONTRACT.md`.

## Where we are
The form is stated rather than inferred, and every declared path on the eight contracts resolves against the MISQ paper except display's artifact, which is declared blocked rather than left dangling. The grain and the venue split are ruled and honoured.

Three things are open and all need JL: whether the one-question test is enforced or merely stated, where contract checking lives, and whether craft prose belongs in a contract. Two are ruled and not yet true: display's per-unit migration, and the add procedure itself, which exists as one sentence.

## Files
- `stages/CONTRACT.md`
  The required core, the resolution rule, the conditional fields, the retired ones.
- `stages/index.yml`
  One row per stage; its header explains what belongs in it.
- `haipipe-paper-stage/SKILL.md`
  Line 193 is the entire current add procedure.
- `PHILOSOPHY.md`
  The stage table, the design prompt, and the venue-free/aligned split.

## Law
A stage answers exactly ONE question, produces ONE artifact, and closes at ONE human gate. A thing with two questions is two stages; a thing with no gate is a phase; a thing with no artifact is a folder.

A stage is added by four files and nothing else: one row in `stages/index.yml`, one folder at `stages/<order>-<key>/`, its `stage.md`, and its `template.md`. No new skill, no version bump, no router edit. `index.yml` holds only what a router needs in order to choose, because it is read on every invocation.

Every stage declares both variation flags at add time. `runs:` follows the human gate, not the folder: `per-unit` exactly when one unit can be approved while another is rejected. `venue_aligned:` follows the line between what is true and how it is told, and the venue stage itself declares `venue_role` because it is neither.

A contract declares a directory and an identity and never spells an S filename. A declared path that cannot be resolved carries `blocked_on: <Q page>` with the reason; a dangling path with no `blocked_on` is a defect, and nothing may report it as green. A stage repointed onto a new layout declares `artifact_fallback:` for as long as any live paper predates that layout, and a run says which of the two it used.

## Discussion
> CC 260726: the merge put display's two open items next to each other for the first time, and they turn out to be one item. `QE1` had "give display a resolvable artifact, blocked on the grain ruling" and `QB12` had "apply the grain to display". Same migration, tracked in two groups, each looking like someone else's problem.

## Log
260726 · Created in the QB restructure, absorbing four faces: `QB1` (what is a stage), `QE1` (the contract form), `QB12` (unit grain, ✅), `QB13` (venue-free and aligned). The group was reframed from an ontology of a stage to the four things you actually do with one: add it, template it, page it, run it. `QE1`'s filename Law moved to `QB3` rather than here, because it is a Board seam rather than a contract rule.
