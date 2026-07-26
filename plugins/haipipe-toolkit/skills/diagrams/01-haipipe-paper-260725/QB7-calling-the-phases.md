# How does a stage call its phases, and may it skip one?
state: 🟡 PARTIAL
owner: JL
method: phases are a declared list, not a fixed type; a skip is legal only when it is announced

## Question
A stage does not do its own work. It declares a list of phases and dispatches each one to a separate worker skill, in order, and that list is the whole of what "running a stage" means. So two things decide the behaviour of every stage in the system: what is in the list, and whether anything may be left out of a run.

Both are more open than they look. `phases:` reads like a type and is a list, and one stage already proves it: `2a-venue` declares `[draft, probe, check]` with no revise at all. Nothing says whether that is a legal shape or an undeclared exception, so the next contract will copy whichever neighbour it happens to look at. And there are two entirely different ways to skip a phase, one at declaration time and one at run time, which nothing distinguishes and which have different costs.

The run-time one has already caused real damage. A live seed run silently skipped PROBE and REVISE and drifted into CHECK, and the person running it discovered the missing phase by accident afterwards. The rule written in response is the right one, that a skip must be an explicit logged verdict rather than a silence, and it lives in a reference file rather than in anything a worker reads.

## Boundary
- ✅ Covered here
  How the phase list is declared and dispatched, and what a legal skip is.
- ↪ Covered elsewhere
  Each phase's own rules are `QB8` to `QB11`; what a re-run does to the page is `QB5`; what admits a stage in the first place is `QB1`.

## Diagram
```
   🔁 phases:  IS A LIST, NOT A TYPE.

      ┌ stage.md ─────────────────────────────────────────────┐
      │ phases: [draft, probe, revise, check]                 │
      │ gates:  [check]                                       │
      └──────────────────────┬────────────────────────────────┘
                             │  the router walks the list IN ORDER
        ┌────────────────────┼────────────────────┬───────────┐
        ▼                    ▼                    ▼           ▼
   Skill(haipipe-      Skill(…-probe)      Skill(…-revise)  Skill(…-check)
     paper-draft)
      → QB8               → QB9                → QB10        → QB11

      ⚠️ a phase executed INLINE, rather than through its Skill(),
         did not run. There is no "I did that part myself".

   ── what the eight actually declare ───────────────────────────────
      0-seed          [draft, probe, revise, check]
      1a-resource     [draft, probe, revise, check]
      1b-claims       [draft, probe, revise, check]
      2a-venue        [draft, probe,         check]   ◄── no REVISE
      2b-pitch        [draft, probe, revise, check]
      3-narrative     [draft, probe, revise, check]
      4-display       [draft, probe, revise, check]
      5-section-edit  [draft, probe, revise, check]

      ✅ INVARIANT: the list always ENDS with `check`.
      ❓ 2a-venue omits revise. Legal shape, or undeclared exception?
         Nothing says. It produces a recommendation, not prose, so
         there may be nothing to revise. That is a guess, not a rule.

   ── TWO ways to skip, and they are NOT the same thing ─────────────
      ① DECLARED     the contract omits the phase from `phases:`
                     visible before the run · reviewable · permanent
                     this is what 2a-venue does

      ② RUN-TIME     the phase is in the list and is not executed
                     legal ONLY as an explicit logged verdict:
                       one reply line with the reason
                       `[PROBE] skipped -- <reason>` in `_LOG`
                       `--` on the phase line of the closing block
                     "the draft looks fine" is a verdict to RECORD,
                     never a licence to say nothing.

      📍 default: a NEW artifact runs all four. Skip is for
         RE-ENTRIES and minor edits, which hands the question
         straight to QB5.

   ── the failure that produced the announce rule ───────────────────
      a live seed run silently skipped PROBE and REVISE and drifted
      into CHECK. The user found the missing phase by accident.
      ⚠️ the rule now says: announce every boundary, one reply line
         + a [PHASE] entry in `_LOG` + the phase line moves 🔥.
         It lives in ref/08-stage-gate.md, not in any worker contract.

   ── per-unit changes what "the list" means ────────────────────────
      runs: per-unit  ──▶  the WHOLE list runs once PER UNIT   (→ QB2)
      so section-edit runs draft·probe·revise·check per section,
      and a skip is per unit too. Nothing says that out loud.
```

## Content
### The list is the stage
There is no code path in which a stage does work. It resolves a contract, creates or finds its page, and walks `phases:`, dispatching each name to its own skill. Everything else on this board about stages is a statement about one of those four workers or about the fields the router read on the way in.

That is why "a phase executed inline did not run" is a real rule and not pedantry. A phase has a worker because the worker has its own contract, its own limits, and in PROBE's case its own clean context. Doing the work in the stage's context is not a shortcut past the dispatch; it is a shortcut past the limit.

### Two skips, one word
A declared skip is a design decision, visible in the contract before anything runs, reviewable by whoever reads it. A run-time skip is a judgment made mid-flight about this particular artifact. They deserve different treatment and currently share a word, which is why the venue contract's missing `revise` reads as though someone forgot rather than decided.

The run-time rule is already good: announce the boundary, log the verdict, mark the phase line. Its weakness is location. It sits in `ref/08-stage-gate.md`, and the workers that would have to obey it do not cite it.

### What per-unit does to all of this
For a per-unit stage the phase list runs once per unit, so both kinds of skip become per-unit too: a section that needs no probe, a display asset already revised. Nothing states that, and section-edit is the stage where it will come up first.

## Items to Finish
- [x] 📐 The phase list is declared per stage and ends with `check`
      Eight contracts, one invariant, honoured by all of them.
- [x] 🚦 A run-time skip must be announced and logged
      One reply line, a `[PROBE] skipped -- <reason>` in `_LOG`, and `--` on the phase line.
- [ ] 🧠 Rule whether a stage may DECLARE a shorter list
      `2a-venue` already does. Either that is a legal shape with a stated test, or it is an exception that should be corrected.
- [ ] 📐 Separate the two skips in the vocabulary
      A declared omission and a run-time verdict are different acts. One word covers both today.
- [ ] 🔧 Move the announce rule where the workers read it
      It lives in `ref/08-stage-gate.md` and is cited by no worker contract, which is how the silent seed run happened in the first place.
- [ ] 📐 State what a skip means for a per-unit stage
      The whole list runs per unit, so a skip is per unit. Never said out loud, and section-edit will hit it first.

## Where we are
The dispatch works and is uniform across all eight stages. The invariant holds: every list ends with `check`, and every stage declares its gates the same way it declares its phases.

Two things are open and both are about the shape of the list rather than the walking of it: whether a stage may declare a short list, and where the anti-silence rule should live so that the workers bound by it can see it.

## Files
- `haipipe-paper-stage/SKILL.md`
  Step 4: drive the declared phases, each through its own `Skill()` dispatch.
- `stages/2a-venue/stage.md`
  The one contract that declares three phases instead of four.
- `1-lifecycle/ref/08-stage-gate.md`
  The announce-every-boundary rule and the no-silent-skips rule, and the seed run that caused them.

## Law
A stage does not do work; it walks its declared `phases:` in order and dispatches each to its own worker skill. A phase executed inline did not run.

`phases:` is a list, not a type, and it always ends with `check`. `gates:` is declared the same way, and defaults to `[check]`.

No silent skips. A phase may be skipped at run time only by an explicit logged verdict: one reply line with the reason, a `[PHASE] skipped -- <reason>` entry in `_LOG`, and `--` on the phase line. "The draft looks fine" is a verdict to record, never a licence to say nothing.

## Log
260726 · Created in the QB restructure, replacing `_archive/QB2-four-phases.md`, which explained what the four phases are. The live question is how they are CALLED and whether one may be left out, which is the thing that has actually gone wrong. Tabulating all eight contracts is what surfaced `2a-venue`'s three-phase list.
