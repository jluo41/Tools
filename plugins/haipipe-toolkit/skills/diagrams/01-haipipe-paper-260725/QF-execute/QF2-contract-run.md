# The contract form: a tiny index everyone pays for, and a full contract only the picked stage loads

state: 🟡 PARTIAL
owner: CC
method: keep the split; keep the index small enough to read on every invocation

## Opening

How should a stage be described, so a router can pick it cheaply and an executor can run it correctly?

Those two readers want opposite things. A router needs almost nothing, and it reads on every single invocation including the ones that turn out to be about something else. An executor needs everything, but only for the one stage that won. So the description is split across two files that are read at very different rates.

**Where this page sits**: QC2 owns what a stage IS, and QC3b owns who names its files.
This page owns the FORM of the description: what lives in `../../paper/route/haipipe-paper-stage/stages/index.yml`, what lives in `stage.md`, what a contract must declare, and how `artifact:` resolves to a real path.

**Why the split is a real constraint and not a preference**: anything added to the index is paid for by every user of the skill, forever, including users whose request had nothing to do with stages.
That is the entire reason board navigation fields live in `stage.md`, and it is why the index has stayed readable while the contracts grew.

**What the repair found**: 22 of 31 declared paths did not exist on the paper they pointed at.
Every mechanical check had been passing, because a path that resolves to nothing still parses.

## Writing Style

How this page must be written. Read it before editing, and edit to it.

**Inherited from `QB4`**: the page grammar, the section order, and the sentence rules come from `../01-boardform-260722/QB-delivery/QB4-overall.md` and are not restated here.

**Measure, then state; never assert a core**: the 24-and-43 split came from counting all eight contracts on 260726.
A claim about what contracts have in common is worth nothing unless it says how it was counted.

**A proposal is labelled a proposal**: `../../paper/route/haipipe-paper-stage/stages/CONTRACT.md` argues for keeping craft prose in the contract, and that argument is not a ruling.
This page must never let the two read alike, because a proposal that gets cited as settled is how an off-the-cuff rule becomes law.

**A dangling path is a defect; a declared block is not**: say `blocked_on: <Q page>` when a path cannot resolve yet.
Writing round it, or leaving it silent, is what produced the 22.

## Diagram

**Two files, two read rates**: what each carries, and who pays for it.

```text
 ┌ stages/index.yml ─────────────────────────────────┐
 │ key · order · dir · triggers · migrated           │  📖 READ EVERY TIME
 │ JUST enough to resolve WHICH stage is meant       │     even when the
 └──────────────────┬────────────────────────────────┘     request turns out
                    │ one row wins                          to be about
                    ▼                                       something else
 ┌ stages/<order>-<key>/stage.md ────────────────────┐
 │ phases · gates · probe_depth · artifact ·         │  📥 LOADED ONLY for
 │ venue contract · craft prose                      │     the stage picked
 └───────────────────────────────────────────────────┘

 💰 anything added to the INDEX is paid for by every user, forever
 🚫 that is why board navigation lives in stage.md, and the header says so
```

## Content

### 1 · The two-file split

**What lives where**: the line, and the reason it sits there.

```text
  📇 index.yml     one row per stage: key · order · dir · triggers · migrated
                   just enough to resolve WHICH stage is meant
                   ⏱ read on EVERY invocation

  📜 stage.md      phases · gates · probe_depth · artifact ·
                   venue contract · craft prose
                   ⏱ loaded ONLY for the stage picked
```

📇 Establishes the split, and the cost argument that decides what may cross it.

#### 1.1 · The index is small because everyone pays for it
(a field added there is a tax on requests that were never about stages)
It is read on every single invocation, including ones that turn out to concern something else entirely.
Board navigation fields therefore live in `stage.md`, and the index header states the rule so the next person does not have to rediscover it.

### 2 · The required core, measured

**24 and 43**: what all eight contracts share, against what only some carry.

```text
  🔢 measured 260726 across ALL EIGHT contracts
  ─────────────────────────────────────────────
  24 fields  in all eight          ━━▶  the REAL common core
  43 fields  in one to six         ━━▶  genuinely optional

  🔑 the core was real and had simply never been written down,
     which is why no reader could tell required from optional
  📄 now in CONTRACT.md, grouped by the QUESTION each field answers:
     identity · board · execution · product · evidence · graph · closing
```

📐 Establishes the required core as a measurement rather than an assertion, so a stranger can write a new contract without comparing eight old ones.

#### 2.1 · How the artifact resolves, in one place
(the rule had been living in three places at once by the end of the repair)
A stage names the directory and the identity; Board tooling composes `S-<board_family>-<board_unit>-<board_slug>.md`.
That composition now lives only in `haipipe-board/`'s `stage.py`, as `resolve_filename()` plus a `resolve` verb, and every other layer calls it instead of repeating the pattern.

### 3 · What the contracts were declaring before the repair

**22 of 31**: paths that parsed perfectly and pointed at nothing.

```text
  🔍 22 of 31 declared paths DID NOT EXIST on the paper they pointed at
  ────────────────────────────────────────────────────────────────────
   8×  artifact:    every stage named the PRE-restructure filename
   8×  log:         _LOG_<stage>.md ── zero have EVER existed
   6×  read paths   read_order · units_from · venue_contract · read_first

  ⚠️ a DRAFT run would have created 0-seed/0-seed.md BESIDE the
     S-Seed-0-seed.md that had replaced it
  🔑 the restructure happened on the PAPER and was never told to the SKILL
```

🔧 Establishes the failure this page exists to prevent: a description that is internally valid and externally wrong.

#### 3.1 · Old papers keep working through a declared fallback
(the repair could not be allowed to break papers that predate the layout)
Paper-SubjectiveLabel-Panel and Paper-PhyPatSim still carry `<stage>/<stage>.md`.
Each repointed contract declares `artifact_fallback:`, and a run must state which of the two it used, so the compatibility is visible in the record rather than silent.

### 4 · What is still owed to JL

**Two rulings**: neither is settled, and both change where code lives.

```text
  🧠 ①  where contract CHECKING lives
        A · the paper skill checks its own contracts     ← what exists now
        B · haipipe-board's stage.py grows a verb        one checker for all,
                                                          at the cost of teaching
                                                          board tooling what a
                                                          paper stage is
        C · no checker; CONTRACT.md alone

  🧠 ②  does craft prose belong in a contract, or split from the fields
        CONTRACT.md argues for KEEPING it: the executor that reads the
        machine fields is the one that must do the work, and a split
        would let the two drift
        ⚠️ that is a PROPOSAL, not a ruling
```

🧠 Establishes the two open decisions, so neither the provisional checker nor the proposal is read as settled.

#### 4.1 · The display artifact is blocked, not dangling
(the distinction is the whole point of `blocked_on:`)
`4-display` is the one stage whose `artifact:` still does not resolve, and it declares `blocked_on: QC3b`.
A check therefore reports it as KNOWN rather than passing it silently, and it cannot resolve until QC3b rules whether display's grain is per-unit.

## Aims

### A1 · 📇 The two-file split
- A1.1 · The two-file split is implemented across every stage.
  **Done when:** eight stages have one index row and one contract each, and nothing in the index duplicates a contract field.
- A1.2 · The index stays small enough to read on every invocation.
  **Done when:** the index header states the rule and the reason, and no board navigation field appears in it.

### A2 · 📐 The required core, measured
- A2.1 · The required fields of a contract are stated rather than inferred.
  **Done when:** `../../paper/route/haipipe-paper-stage/stages/CONTRACT.md` names the required core, the stage-specific set, the conditional set, and the retired fields, each traced to the measurement.
- A2.2 · The S filename rule has exactly one home.
  **Done when:** only `stage.py`'s `resolve_filename()` composes an S filename, and every other layer calls it.

### A3 · 🔧 What the contracts were declaring before the repair
- A3.1 · Every contract points at files that exist on a live paper.
  **Done when:** every declared path on the eight contracts resolves against the MISQ paper, or declares `blocked_on:` with a reason.
- A3.2 · Papers that predate the restructure keep working.
  **Done when:** each repointed contract declares `artifact_fallback:`, and a run reports which of the two paths it used.
- A3.3 · `4-display` has a resolvable artifact.
  **Done when:** QC3b rules whether display is per-unit, and `4-display` drops its `blocked_on:` for a real path.

### A4 · 🧠 What is still owed to JL
- A4.1 · Where contract checking lives is ruled.
  **Done when:** JL picks A, B, or C, and the checker either stays in the paper skill, moves into `stage.py`, or is deleted.
- A4.2 · Whether craft prose belongs in a contract is ruled.
  **Done when:** `../../paper/route/haipipe-paper-stage/stages/CONTRACT.md`'s argument is either adopted as a rule or replaced by a split, with the decision dated.

## States

### A1 · 📇 The two-file split
- ✅ A1.1 · Done. Eight stages, one row each, one contract each.
- ✅ A1.2 · Held. The index carries its own header stating the rule and the reason it exists.

### A2 · 📐 The required core, measured
- ✅ A2.1 · Done 260726. `../../paper/route/haipipe-paper-stage/stages/CONTRACT.md` records 24 required and 43 stage-specific fields, plus the conditional set and the two retired ones, grouped by the question each answers.
- ✅ A2.2 · Done. `resolve_filename()` and the `resolve` verb live in `stage.py`, replacing a rule that had been in three places.

### A3 · 🔧 What the contracts were declaring before the repair
- ✅ A3.1 · Done. Six stages resolved onto their S face, `log:` retired, read paths repointed, `board_slug:` added, and `venue_role:` added for the venue stage, which is neither venue-free nor venue-aligned because it picks the venue.
- ✅ A3.2 · Done. Every repointed contract declares `artifact_fallback:`, and a run says which it used.
- 🧠 A3.3 · Waiting on QC3b. `4-display` declares `blocked_on: QC3b`, so it is reported as known rather than green, and it cannot resolve until display's grain is ruled.

### A4 · 🧠 What is still owed to JL
- 🧠 A4.1 · Waiting on JL since 260726. The checker exists in the paper skill provisionally and may move or be deleted.
- 🧠 A4.2 · Waiting on JL. `../../paper/route/haipipe-paper-stage/stages/CONTRACT.md` states the case for keeping craft prose in the contract, and that remains a proposal.

## Files

- `../../paper/route/haipipe-paper-stage/stages/CONTRACT.md` · the required core, the resolution rule, the conditional fields, the retired ones
- `../../paper/route/haipipe-paper-stage/stages/index.yml` · unchanged, still one row per stage
- `stages/` · all eight contracts repointed; `5-section-edit` is the largest and the only per-unit one, and its artifact is a pattern rather than a path
- `haipipe-board/` · `stage.py` exposes `resolve_filename()` and a `resolve` verb, so the S filename rule has one home

## Law

- A contract declares the directory and the identity; it never spells an S filename.
  The name is composed by `haipipe-board/`'s `stage.py resolve` from family, unit and slug, and any layer that needs it calls that rather than repeating the pattern.
- A declared path that cannot be resolved is declared `blocked_on: <Q page>` with the reason.
  A dangling path with no `blocked_on` is a defect, not a known limitation, and nothing may report it as green.
- A stage repointed onto a new layout declares `artifact_fallback:` for as long as any live paper predates that layout, and a run says which of the two it used.

## Glossary

- **Common core**: the 24 fields present in all eight contracts, established by counting rather than by assertion.
- **`blocked_on:`**: the declaration that turns an unresolvable path from a defect into a known limitation with an owner.

## Log

260802 · Migrated to the QB4 page contract: Writing Style added, Content numbered into four divisions with face figures and captions, Aims regrouped as A1 to A4 with `Done when`, States mirrored per Aim.
260726 · Measured the eight contracts: 24 fields common to all, 43 stage-specific. Wrote `../../paper/route/haipipe-paper-stage/stages/CONTRACT.md`. Repointed 22 dangling paths; retired `log:`; added `board_slug`, `artifact_fallback`, `venue_role`, `blocked_on`. Extracted the filename rule into `stage.py`'s `resolve_filename()`. Left `4-display` blocked on QC3b, and both rulings open.
