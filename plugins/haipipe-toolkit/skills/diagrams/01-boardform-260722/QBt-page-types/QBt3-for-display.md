# QBt3 · D1 Type-key coverage: a display unit, and the acceptance it waits for

state: 🟡 PARTIAL · rung ④ ACCEPTED · accepted 260806; one of two consumers has not cited it, so it is not yet PLACED
page-type: display
owner: JL
method: build this unit to its claim job, name its evidence source, state an honest statistical label, and land it in a known place
needs: QA-probe/QBt5-for-value/1-drift-counts
provides: displays/QBt3-for-display/out/assets/figure.txt

## Opening

Does the coverage figure show contract drift falling as a page's type key gets older, with an honest statistical label?

A display is not decoration: this unit must carry one claim job, name its evidence source, state an honest statistical label, and land in a known place in the manuscript.

🚫 **This unit belongs to a fabricated project.** Its numbers are invented, its corpus does not exist, and nothing here may be cited. What is NOT fabricated is the shape: this page is a real `for-display` page, and its bindings resolve to files that really sit on disk, one folder away.

**Where its things are**: a page's companion folder is `<type-plural>/<page name>/`, so this page's unit is `displays/QBt3-for-display/`. That is the group's one naming rule, and `QBt5`'s drawer is `QA-probe/QBt5-for-value/` by the same rule.

**Why this page is also the instruction**: it is the specimen for its type. `QB4` teaches the page grammar by being a page that obeys it; this page teaches the display form the same way. The rules themselves stay in `haipipe-board-page-for-display`, which this page never restates.

**Covered elsewhere**: `QB6` owns which types exist and what admits a new one. The `displays/<unit>/` folder shape is the paper board's, on its QBe series. How a sentence POINTS at a display is `QB8` §3.

## Diagram

**The render**: the artifact a person looks at before deciding whether to accept it.

```text
  📉 Contract drift by type-key tenure          🚫 FABRICATED
  ──────────────────────────────────────────────────────────────
  BAND                       PAGES   DRIFT   RATE
  ──────────────────────────────────────────────────────────────
  inferred from filename       214      37   ██████████████████ 17.3%
  key declared 0-3 months       61       9   ███████████████ 14.8%
  key declared 4-6 months       48       4   █████████ 8.3%
  key declared 7-12 months      44       2   █████ 4.5%
  key declared 13+ months       33       1   ███ 3.0%
  ──────────────────────────────────────────────────────────────
  drift rate = drift_events / pages · 95% CI in that atom's counts.csv
  label: ASSOCIATION. Tenure is not assigned, and no control for
  page size is applied, so this figure may not say "reduces".
```

⚠️ This is `assets/figure.txt`, the SELECTED render, reproduced here so the page can be read without opening the unit folder. A real unit embeds its render by path; this one is ASCII because a fabricated PDF would be a binary nobody can read or diff.

## Content

### 1 · The claim job: what this unit must show, and for which claim

**One unit, one job**: what the figure has to establish, and which sentence is waiting for it.

```text
  claim served   drift falls as a page's declared type key gets older
  shown by       five tenure bands, drift rate per band, one bar each
  NOT shown      causation. The label says "association", and §3 says
                 which two design facts cap it there
  consumers      S-Main-4-results §2 · S-Open-Pitch §1
```

🎯 Establishes the one job this unit does, so a reviewer can tell whether the render did it.

A unit that shows more than its claim job is not generous, it is unfocused: every extra series is one more thing a reader must rule out before reaching the one that matters.

### 2 · Provenance: one row per number the unit shows

**Every number traced**: each value on the render, and the path it comes from.

```text
  value                    source                                kind
  ──────────────────────────────────────────────────────────────────
  214 · 61 · 48 · 44 · 33  QA-probe/QBt5-for-value/1-drift-counts  atom id
  37 · 9 · 4 · 2 · 1         its counts.csv, resolved by id
  95% CI bounds            same atom, same CSV                   atom id
  17.3 · 14.8 · 8.3 ·      derived in source/build.py,           derived
  4.5 · 3.0                  drift_events divided by pages
  ──────────────────────────────────────────────────────────────────
  and that atom's own source is the answer table typed into
  QA-probe/QBt5-for-value/1-drift-counts.md, parsed, never retyped
  ──────────────────────────────────────────────────────────────────
  THIS PAGE WRITES NO PATH. Its head says
    needs: QA-probe/QBt5-for-value/1-drift-counts
  and the resolver finds it · every value is INVENTED
```

🔢 Establishes that nothing on the render appeared without a source, which is the whole job of this division on a real page.

The chain is QA record to display unit, and the hop is by ID. A real display page writes six hand-made paths in this division and every one dies when a folder moves; this page writes none. `python3 unit.py check` is what proves the chain, and it is the check a real paper cannot run today.

Proven by moving the answering atom's whole drawer and rebuilding: no script changed, no page changed, and the render came out identical.

### 3 · Spec: how the unit is produced, and what label is honest

**The recipe and its ceiling**: what makes the figure, and what the design lets it say.

```text
  unit       displays/QBt3-for-display/    ← named after this page, exactly
  declares   this page's own head: needs, provides
  input      needs: QA-probe/QBt5-for-value/1-drift-counts   ← id, not path
  build      source/build.py · resolves that id, writes out/assets/figure.txt
  rebuild    python3 unit.py build         ← dependency order, whole chain
  verify     python3 unit.py check         ← every need resolves
  ──────────────────────────────────────────────────────────────────
  label      "association", not "reduces":
             ① tenure is not assigned, pages declared keys when their
               authors got to them
             ② no control for page size, and longer pages drift more
```

📐 Establishes the recipe and the honest ceiling on what the figure may claim.

The label line is what a reviewer reads first. A figure that says "reduces" over a design supporting "association" is the defect this division exists to catch, and it is caught here rather than in the caption because the caption is downstream of the spec.

### 4 · Placement: which sentence uses this unit

**One record per consumer**: where it lands, which sentence cites it, and whether the citation resolved.

```text
  consumer               sentence                             landed?
  ──────────────────────────────────────────────────────────────────
  S-Main-4-results §2    "Drift falls across all five bands    ✅ cited
                          (Figure 1)."
  S-Open-Pitch §1        "the tenure gradient"                 ⬜ named,
                                                                  not cited
  ──────────────────────────────────────────────────────────────────
  ⬜ is why this page is at rung ④ and not ⑤. An accepted unit that a
     consumer only alludes to is not placed, and this row is what keeps
     that from going quiet.
```

🔗 Establishes whether the unit reached the manuscript, which acceptance alone does not tell you.

### 5 · Fragility: what would send this unit back down the ladder

**What breaks it**: the changes that return an accepted unit to RENDERED or further.

```text
  unit.py build re-runs             ──▶ back to ③ · acceptance was of
                                        THIS render, not of the name
  the QA-probe's table changes      ──▶ back to ③ · the value unit
                                        reparses and the numbers move
  a tenure band boundary moves      ──▶ back to ① · the claim job moved
  the venue changes figure limits   ──▶ §4 rows reset, placement re-opens
  ──────────────────────────────────────────────────────────────────
  what does NOT break it: moving any unit's folder. Needs are ids.
```

⚠️ Establishes what makes the state line fall, so a person knows when their yes expired.

Acceptance is of a specific render. That is why no machine may write rung ④, and why this division exists on a page that already reached it.

## Aims

### A1 · 🎯 The claim job: what this unit must show, and for which claim
- A1.1 · The unit shows its claim job and nothing else.
  **Done when:** every series on the render is named in `§1`, and `§1` names no series the render lacks.

### A2 · 🔢 Provenance: one row per number the unit shows
- A2.1 · Every number on the render traces to a path that resolves.
  **Done when:** each path in `§2` exists on disk and the row count covers every value the render prints.
- A2.2 · The input moves behind a value binding once the scenario has a Value page.
  **Done when:** `§2`'s input rows cite the scenario Value page's value binding instead of the CSV directly.

### A3 · 📐 Spec: how the unit is produced, and what label is honest
- A3.1 · The statistical label does not outrun the design.
  **Done when:** the label line names every design fact that caps it, and a reader can check each one against `§3`.

### A4 · 🔗 Placement: which sentence uses this unit
- A4.1 · Every consumer either cites the unit or shows an open unplaced row.
  **Done when:** no `⬜` row in `§4` remains, at which point the state line moves to rung ⑤.

### A5 · ⚠️ Fragility: what would send this unit back down the ladder
- A5.1 · The events that void acceptance are written down before acceptance is asked for.
  **Done when:** `§5` lists every rebuild path that can change a printed number.

## States

- 260806 CC · The type key on this page is currently decorative. `page-type` is read by neither `src/parse.py` nor `cli/check.py`, so resolution step ③ does not run and this file still resolves by its `QBt3` filename at step ⑤. Rule 1 of `QB6` §5.1 is the fix.
- 260806 CC · Building this specimen found a conflict the prose never surfaced: `haipipe-board-page-for-display` rules that the state line reports a LADDER RUNG, and `cli/check.py` raises `bad-state` on any state line whose first token is not one of the four health words. A pure rung is an ERROR on every board today. This page carries the health word first and the rung as the next token, which passes and loses nothing; whether that is the answer, or whether the checker should learn the ladder, is unruled.

### Decision Now
- 📍 When the thirteen live display pages get their type key, does the `## Stage Contract` span stay or go? **A ·** remove it: the type that owns the page owns its sections, and a span no contract declares is furniture nobody maintains. **B ·** keep it: it records `requires` / `style-from` / `provides`, which a display unit genuinely has, and `stage.py sync` already maintains it. This specimen is written as A; if you rule B, the span is added here first and then to the thirteen.
- 📍 The state line conflict above: does `for-display` drop the ladder from `state:`, or does `cli/check.py` learn to accept a rung? Until this is ruled, every display page written to its own contract is an ERROR.

### A1 · 🎯 The claim job: what this unit must show, and for which claim
- 🔨 A1.1 · The render's five bands and its one bar each are named in `§1`, but the `PAGES` and `DRIFT` columns it also prints are not, so `§1` does not yet name every series on the render.

### A2 · 🔢 Provenance: one row per number the unit shows
- ✅ A2.1 · `python3 unit.py check` in the group folder reports this unit's one need resolved and its product present, and every path `§2` names is on disk: the atom's `1-drift-counts.md`, its `counts.csv` carrying all five bands, and the `source/build.py` the rates are derived in.
- ⬜ A2.2 · Not begun: `§2` still cites the atom's `counts.csv` directly, and E1's consumer row on `QBt5-for-value.md` carries no value binding, even though the scenario's Value page now exists.

### A3 · 📐 Spec: how the unit is produced, and what label is honest
- ✅ A3.1 · The render's label line names two design facts, that tenure is not assigned and that page size is not controlled, and `§3` lists exactly those two as ① and ②, so a reader can check each one.

### A4 · 🔗 Placement: which sentence uses this unit
- ❄️ A4.1 · Held on purpose at one open `⬜` row: `S-Open-Pitch §1` alludes to the unit without citing it, which is what keeps the specimen showing an accepted-but-unplaced unit at rung ④ rather than ⑤.

### A5 · ⚠️ Fragility: what would send this unit back down the ladder
- ✅ A5.1 · `§5` was written in the same 260806 draft that recorded rung ④, and it lists every path that can move a printed number: a `unit.py build` re-run, a change to the atom's answer table, a band boundary move, and a venue figure limit change.

## Files

- `QA-probe/QBt5-for-value/`
  The drawer holding the QA record this unit needs, and a second record demonstrating the extract shape.
- `unit.py`
  The resolver that turns a unit id into a path, plus `check` and `build`. This is the proposal the scenario exists to try: a unit names another unit by id, never by path.
- `displays/QBt3-for-display/`
  This unit, named after this page exactly: `source/build.py`, `out/assets/figure.txt`. One folder, phases as subfolders, no published twin.
- `QBt5-for-value.md`
  The evidence page whose E1 division owns the QA record this unit needs.
- `../../board/page-types/haipipe-board-page-for-display/SKILL.md`
  The contract this page is an instance of. If the two disagree, the contract wins and this page is the defect.
- `QB-delivery/QB4-overall.md`
  The page frame this page sits in: the section set, their order, and the caption rule every division above obeys.
- `QB-delivery/QB6-page-types.md`
  The hub listing all ten types, and the ten missing checker rules whose rule 3 would check this page's `§2`.

## Log

- 260806 · [DRAFT-CC] written as a real `for-display` page rather than an essay about one, on JL's ruling that the example should BE its type, the way `QB4` is both the page grammar and a page obeying it. Unit and render built under `displays/QBt3-for-display/`, named after this page exactly, so every binding resolves while every number stays invented.
- 260806 · [PROBE-CC] building the specimen surfaced two conflicts now recorded in `## States` and both Decision Now rows: the `## Stage Contract` span the type does not declare, and the state line the checker will not accept as a ladder rung.
- 260806 CC · Unit built and rendered through the whole chain. `unit.py build` runs the chain in dependency order: the QA record parses its answer table into `counts.csv`, then this unit resolves that atom by id and writes `out/assets/figure.txt`. `unit.py check` reports both units, both needs resolved, both products present.
- 260806 CC · The id-not-path rule was tested rather than asserted. The value unit was moved out of `S04-value/` into an unrelated folder and the chain was rebuilt with no edit to any script or page; the render came out identical. Then it was moved back. This is the one property the structure exists for, so it is proven here rather than claimed.
- 260806 CC · Structure A adopted for the scenario on JL's ruling: one unit, one folder, phases as subfolders, no published twin. The MISQ paper is untouched and follows later if this holds up.
- 260806 CC · Accepted at rung ④ as the specimen's demonstration of what acceptance looks like recorded. Not advanced to ⑤ on purpose: `S-Open-Pitch` alludes to the unit without citing it, so `§4` carries one open `⬜` row and the page shows what an unplaced-but-accepted unit looks like. A specimen with every row green teaches nothing about the rows that go wrong.
- 260806 CC · Written as option A of the ruling in `States › Decision Now`: no `## Stage Contract` span, because `haipipe-board-page-for-display` declares none. The thirteen live display pages on the MISQ board all carry one, because they resolve as stage pages.
- 260806 1259 · [REVISE-CC] States now mirrors every Aim id; three Aims are genuinely met (A2.1 by `unit.py check` resolving the need and the product, A3.1 by the label naming the same two design facts `§3` lists, A5.1 by `§5` covering every path that can move a printed number), A4.1 is held at its one open `⬜` row on purpose, A2.2 has not begun because `§2` still cites `counts.csv` and E1's consumer row carries no value binding, and A1.1 is short because the render prints `PAGES` and `DRIFT` columns that `§1` never names. The five dated records above moved here from States, where they were history sitting in a snapshot (QB4 §5.3.1); the two that describe the page as it stands now stayed.
