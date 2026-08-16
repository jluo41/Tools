# How may a stage vary: how many pages, and does it survive a new journal?
state: 🟡 PARTIAL
owner: JL
method: two flags, each decided by one sentence you can test, both declared at add time

## Question
The eight stages are not the same shape as each other, and they vary along exactly two axes: how many things one run produces, and whether a change of target journal destroys the work. Both are declared as a single field in the contract, `runs:` and `venue_aligned:`, and both are the kind of decision that gets improvised if it is not tested. Improvised grain is how display accumulated a gate nobody could answer; improvised venue alignment is how a rejected paper becomes an open-ended rewrite instead of a bounded one.

Each flag has a one-sentence test, and both tests are about a human rather than about the work. For grain: could a person approve one unit and reject another? For venue: could a different editor change this stage's ANSWER? Where the answer is yes, the stage is per-unit or venue-aligned, and where it is no, it is not. Neither test is about how big the stage feels or how many files it happens to touch.

What is settled is the tests. What is not is one migration and one definition. Display passes the grain test and still declares `runs: once`, so its `artifact:` cannot resolve and sits behind a `blocked_on:` marker. And "rewritten on retarget" has never been given a meaning: rewrite from scratch, or re-derive against the new blueprint while keeping the argument, are different operations and the contracts do not distinguish them.

## Boundary
- ✅ Covered here
  The two variation flags, the test behind each, and what each costs.
- ↪ Covered elsewhere
  What admits a stage at all is `QB1`; how many PAGES a per-unit stage creates on the board is `QB4`; who accepts a unit is `QB11`.

## Diagram
```
   🚩 TWO FLAGS, SET AT ADD TIME, EACH WITH A ONE-SENTENCE TEST

   ── runs:   once | per-unit ───────────────────────────────────────
      TEST   could a human APPROVE one unit and REJECT another?

      BEFORE  one artifact for 4-display
      ┌──────────────────────────────────────────────────┐
      │ gate: "is the display stage done?"               │
      │   display01 … display02 … display03 …  ×11       │
      │   different statuses · different source data ·   │
      │   different blockers                             │
      │   13-record checklist   ──▶   NEVER CLOSED  ⚠️    │
      └──────────────────────────────────────────────────┘
      AFTER   one page per asset
      ┌────────────┐┌────────────┐┌────────────┐
      │ display01  ││ display02  ││ display04  │  …
      │ gate: ✅    ││ gate: ⏳    ││ gate: ✅    │
      └────────────┘└────────────┘└────────────┘
       each question answerable in ONE sentence

      per-unit     4-display  ⚠️ still declares `once`
                   5-section-edit  ✅ already true
      once         0-seed · 1a-resource · 1b-claims ·
                   2a-venue · 2b-pitch · 3-narrative

      ⚠️ the rule is NOT "everything is per-unit". It is "per-unit
         where the WORK is per-unit", and the gate is the test.

   ── venue_aligned:   free | aligned | venue_role ──────────────────
      TEST   could a different journal change this stage's ANSWER?

      venue-FREE                       survives a retarget untouched
      ┌──────────────────────────────────────────────┐
      │ 0-seed        why might this exist            │
      │ 1a-resource   does it exist, does it carry    │  THE SCIENCE
      │ 1b-claims     supported / weak / GAP          │
      └──────────────────────────────────────────────┘
                          │
                     2a-venue   ◄── THE PIN, `venue_role`,
                          │          neither free nor aligned
      ┌──────────────────────────────────────────────┐
      │ 2b-pitch      what it sells, to whom          │
      │ 3-narrative   reveal order, section list      │  THE TELLING
      │ 4-display     display budget, conventions     │
      │ 5-section-edit house style, citation density  │
      └──────────────────────────────────────────────┘
      venue-ALIGNED                      rewritten on retarget

      ⚖️ the line falls between what is TRUE and how it is TOLD.
         A claim's status does not change because a different editor
         reads it. A narrative's ORDER does.

   ── the case that hurts, and still lands aligned ──────────────────
      MISQ ──rejected──▶ another outlet
        evidence   KEPT         every claim, number and probe entry
        figures    MOSTLY LOST  limits and conventions differ
      expensive, and still right: a figure is an argument made FOR a
      venue, not a fact about the world.

   ── WHO READS THESE FIELDS, AND HOW THEY FAIL ────────────────────
      fields   runs · venue_aligned · unit · units · units_from
      reader   ③ THE EXECUTOR · an agent, reading prose        → QB1
      fails    🔇 SILENT. display declares `runs: once` over eleven
               independently gated units and nothing has ever raised.
      to bind  ✅ THIS ONE IS CHECKABLE, cheaply: a stage that declares
               `units:` must declare `runs: per-unit`. `4-display`
               declares the first and not the second, which is the whole
               defect, expressible as one assertion.
```

## Content
### Why the gate decides the grain
A gate is one human saying yes to one specific thing. So the grain of the artifact and the grain of the gate have to match, or the gate becomes unanswerable, and an unanswerable gate does not fail loudly: it just never closes, and the stage sits open while everything around it moves.

That is why the test is about approval rather than about size. Seed produces one thing and gains nothing from per-unit machinery. Display produces eleven things with independent blockers, and asking one question about all eleven was the actual defect.

### What "rewritten on retarget" has never meant
The aligned stages are rewritten when the venue changes. That sentence has been enough so far because no paper has actually been retargeted end to end, so it is design rather than practice. Two readings are live and they are different amounts of work: rewrite from scratch against the new blueprint, or keep the argument and re-derive its shape. The contracts do not distinguish them, and the first retarget will pick one by accident.

The related temptation should be named now rather than at that moment: a new venue invites re-cutting the claims to fit. By this design it must not, because claims are venue-free, and the value of the split is exactly that it holds when it is inconvenient.

## Items to Finish
- [x] 🧠 Rule the grain, with the test
      Per-unit exactly when units gate independently; one artifact otherwise.
- [x] 📐 Confirm which stages stay single
      Seed, resource, claims, venue, pitch and narrative are single-artifact by the same test, so it reads as a decision rather than as an omission.
- [x] ✂️ The venue split is stated
      `PHILOSOPHY.md` and the per-stage `venue_aligned:` field, with `venue_role` for the pin itself.
- [ ] 📐 Migrate display to per-unit, and it is half done
      `5-section-edit` has the full set: `runs: per-unit`, `unit: section`, `units_from:` pointing at the narrative page, and a `board_family` resolved per section. `4-display` has `units: displays/displayNN-<slug>/` and still declares `runs: once`, so it names its units and does not iterate them, and its `artifact:` dangles behind `blocked_on: QB2`. What is missing is `unit:`, `units_from:`, and a pattern rather than a path.
- [ ] 🔍 Assert that `units:` implies `runs: per-unit`
      One line. `4-display` declares the first and not the second, and that contradiction IS the open migration below, expressible as a check rather than as a plan.
- [ ] 📐 Define what retargeting does to each aligned stage
      Rewrite from scratch, or re-derive while keeping the argument. Different operations; the contracts do not distinguish them.
- [ ] 🧠 Rule whether a retarget reopens the claims stage
      It should not, by this design. Say so explicitly, because the temptation at a new venue is to re-cut the claims to fit.

## Where we are
Both flags are implemented and honoured across all eight contracts. Section-edit is the one stage that already answers per-unit; the grain ruling is made and display's migration is the visible remainder of it.

The venue split has never been exercised: no paper on this system has been retargeted, so what the aligned stages actually do on retarget is a design intention rather than an observed behaviour.

## Files
- `stages/4-display/stage.md`
  The stage the grain argument is really about; carries `runs: once` and a blocked artifact.
- `stages/5-section-edit/stage.md`
  The only stage that already answers per-unit; its artifact is a pattern, not a path.
- `stages/*/stage.md`
  The `venue_aligned:` field, and `venue_role:` on `2a-venue`.
- `PHILOSOPHY.md`
  The venue-free and venue-aligned split.

## Law
The unit follows the human gate, not the folder called a stage. A stage is `per-unit` exactly when one unit can be approved while another is rejected. By this rule Display and Section Edit are per-unit; Seed, Resource, Claims, Venue, Pitch and Narrative are single-output.

Every stage declares exactly one of venue-free or venue-aligned, decided by whether a different journal could change its answer. The venue stage itself declares `venue_role`, because it is the stage that picks the venue and is therefore neither.

Evidence is venue-free. A retarget may rewrite how a paper is told and may not reopen what it found.

## Log
260726 · Merged from `_archive/QB12-unit-grain.md` (✅, with its Law intact) and `_archive/QB13-venue-free-aligned.md`. Both were about the same thing, how one stage differs from another, and both are declared as one contract field set at add time.
260726 · Aligned against `QA6`, which had moved well past this group. The display migration is half done rather than not started: `units:` is already declared while `runs:` still says `once`, and `5-section-edit` carries the full per-unit set. The item now says which half is missing.

260726 · The display migration gained a check rather than a plan: `units:` implies `runs: per-unit` is one assertion, and `4-display` declaring the first without the second IS the open item.
