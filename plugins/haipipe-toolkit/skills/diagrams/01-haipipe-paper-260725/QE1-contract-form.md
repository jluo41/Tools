# The contract form: one index, one file per stage
state: 🟡 PARTIAL
owner: CC
method: keep the split; keep the index small enough to read on every invocation

## Question
How should a stage be described, so that a router can pick it cheaply and an executor can run it correctly? A tiny index is read on every single invocation and the full contract only for the stage actually picked, and that split is a real constraint on what may live where.

The design splits the description in two: a tiny index read on every invocation, and a full contract loaded only for the stage actually picked. That split is a real constraint on what may live where, and it is the reason the index has stayed readable while the contracts have grown.


The approach is a two-file split, a tiny index read on every invocation and a full contract loaded only for the stage picked, with the required fields stated rather than inferred. What we want is for a stranger to be able to write a correct new stage contract without comparing eight existing ones to guess the pattern.
## Boundary
- ✅ Covered here
  What lives in `index.yml`, what lives in `stage.md`, what a contract must declare, and how `artifact:` resolves.
- ↪ Covered elsewhere
  Who owns the filename is `QB4`; which dependency declaration is authoritative is `QA8`; whether display's grain is per-unit is `QB2`.

## Diagram
```
 TWO FILES, BECAUSE THEY ARE READ AT DIFFERENT RATES

 ┌ stages/index.yml ─────────────────────────────────┐
 │ key · order · dir · triggers · migrated           │  READ EVERY TIME
 │ JUST enough to resolve WHICH stage is meant       │  even when the
 └──────────────────┬────────────────────────────────┘  request turns out
                    │ one row wins                      to be about
                    ▼                                   something else
 ┌ stages/<order>-<key>/stage.md ────────────────────┐
 │ phases · gates · probe_depth · artifact ·         │  LOADED ONLY for
 │ venue contract · craft prose                      │  the stage picked
 └───────────────────────────────────────────────────┘

 ANYTHING ADDED TO THE INDEX IS PAID FOR BY EVERY USER, FOREVER.
 That is why board navigation lives in stage.md, and the header says so.

 THE REQUIRED CORE, MEASURED 260726 rather than asserted
   24 fields   in ALL EIGHT contracts        ──► the real common core
   43 fields   in one to six of them         ──► genuinely optional
   the core was REAL and had simply never been written down, which is
   why no reader could tell required from optional. Now in CONTRACT.md,
   grouped by the question each field answers.

 WHAT THE CONTRACTS WERE ACTUALLY DECLARING, before the repair
   22 of 31 declared paths DID NOT EXIST on the paper they pointed at
     8x  artifact:    every stage named the PRE-restructure filename
     8x  log:         _LOG_<stage>.md — zero have ever existed
     6x  read paths   read_order · units_from · venue_contract · read_first
   a DRAFT run would have created 0-seed/0-seed.md beside the
   S-Seed-0-seed.md that replaced it.  ⚠️
   the restructure happened on the PAPER and was never told to the SKILL.

 STILL OWED TO JL  🧠
   ① where contract CHECKING lives    A paper skill · B haipipe-board · C none
   ② does craft prose belong in a contract, or split from the fields
```

## Content
### The split
```
 index.yml    one row per stage: key, order, dir, triggers, migrated
              JUST enough to resolve which stage is meant. Read every time.
 stage.md     phases, gates, probe_depth, artifact, venue contract, craft prose.
              Loaded ONLY for the stage picked.
```

### Why the index must stay small
It is read on every single invocation, including ones that turn out to be about something else entirely. Anything added to it is paid for by every user of the skill forever. That is why board navigation fields live in `stage.md` and not in the index, and the header says so.

### What the required core actually is
(measured on 2026-07-26, not asserted)

Twenty-four fields appear in all eight contracts, and forty-three more appear in one to six of them. That ratio is the answer to why a reader could not tell required from optional: the common core was real, it was just never written down. It is now in `CONTRACT.md`, grouped by the question each field answers: identity, board, execution, product, evidence, graph, closing.

### How the artifact resolves
The stage names the directory and the identity; Board tooling composes the filename as `S-<board_family>-<board_unit>-<board_slug>.md`. That rule was living in three places at once by the end of the repair: `haipipe-board/`'s `stage.py`, a prose paragraph, and a checker. It now lives in `stage.py` alone, as `resolve_filename()` plus a `resolve` verb, and everything else calls it.

### What the contracts were declaring before the repair
```
 22 of 31 declared paths did not exist on the paper they pointed at
    8x artifact:    every stage pointed at the pre-restructure filename
    8x log:         _LOG_<stage>.md, of which zero have ever existed
    6x read paths   read_order, units_from, venue_contract, read_first
```
A stage run on the MISQ paper would have created a second `0-seed/0-seed.md` beside the `S-Seed-0-seed.md` that replaced it. The restructure happened on the paper and was never told to the skill.

### Craft prose in the contract
Below the frontmatter each contract carries prose about doing the work well. `CONTRACT.md` now argues for keeping it: the executor that reads the machine fields is the one that must do the work, and a split would let the two drift. That argument is written down as a PROPOSAL. It is not ruled, and the item below stays open until JL rules it.

## Items to Finish
- [x] 🗂 The two-file split is implemented
      Eight stages, one row each, one contract each.
- [x] 🪶 The index is kept small
      Its own header states the rule and the reason.
- [x] 📐 State the required fields of a contract
      `CONTRACT.md`, from a measurement of all eight: 24 required, 43 stage-specific, plus the conditional set and the two retired fields.
- [x] 🔧 Repoint every contract onto the live S faces
      Six stages resolved to their S face, `log:` retired, read paths repointed, `board_slug:` added, `venue_role:` added for the venue stage, which is neither venue-free nor venue-aligned because it is the stage that picks the venue.
- [x] 🛟 Do not break the papers that predate the restructure
      Paper-SubjectiveLabel-Panel and Paper-PhyPatSim still carry `<stage>/<stage>.md`. Each repointed contract declares `artifact_fallback:`, and a run must say which of the two it used.
- [ ] 🧠 Rule where contract checking lives
      A: the paper skill checks its own contracts, which is what exists now. B: `haipipe-board/`'s `stage.py` grows a verb, one checker for everything, at the cost of teaching board tooling what a paper stage is. C: no checker, and `CONTRACT.md` alone. JL raised this on 2026-07-26 and it is not settled.
- [ ] 🧠 Rule whether craft prose belongs in the contract
      `CONTRACT.md` states the case for keeping it. That is a proposal, not a ruling.
- [ ] 📐 Give display a resolvable artifact
      `4-display` is the one stage whose `artifact:` still dangles. It declares `blocked_on: QB2`, so a check reports it as KNOWN rather than passing it silently. It cannot resolve until QB2 rules whether display is per-unit.

## Where we are
The form is now stated rather than inferred, and the contracts point at files that exist. Every declared path on the eight contracts resolves against the MISQ paper except `4-display`'s artifact, which is declared blocked on QB2 rather than left dangling.

Two things are open and both need JL. Where the checking lives is unruled, so the checker exists in the paper skill provisionally and may move or be deleted. Whether craft prose belongs in a contract is argued in `CONTRACT.md` but not decided.

## Files
- `CONTRACT.md`
  The required core, the resolution rule, the conditional fields, the retired ones.
- `index.yml`
  Unchanged: still one row per stage.
- `stages/`
  All eight contracts repointed. `5-section-edit` is the largest and the only per-unit one; its artifact is a pattern, not a path.
- `haipipe-board/`
  `stage.py` now exposes `resolve_filename()` and a `resolve` verb, so the S filename rule has one home.

## Law
A contract declares the directory and the identity; it never spells an S filename. The name is composed by `haipipe-board/`'s `stage.py resolve` from family, unit and slug, and any layer that needs it calls that rather than repeating the pattern.

A declared path that cannot be resolved is declared `blocked_on: <Q page>` with the reason. A dangling path with no `blocked_on` is a defect, not a known limitation, and nothing may report it as green.

A stage repointed onto a new layout declares `artifact_fallback:` for as long as any live paper predates that layout, and a run says which of the two it used.

## Log
260726 · Measured the eight contracts: 24 fields common to all, 43 stage-specific. Wrote `CONTRACT.md`. Repointed 22 dangling paths; retired `log:`; added `board_slug`, `artifact_fallback`, `venue_role`, `blocked_on`. Extracted the filename rule into `stage.py`'s `resolve_filename()`. Left `4-display` blocked on QB2, and both rulings open.
