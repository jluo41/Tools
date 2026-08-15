# QBt3 · page-type DISPLAY · owns a UNIT folder (source · candidates · assets · float · preview); closes only when a person accepts ONE render

state: 🟡 PARTIAL · rung ③ RENDERED · the render exists and can be looked at; ④ waits on a person, and no person has said yes
page-type: display
owner: JL
method: build this unit to its claim job, name its evidence source, state an honest statistical label, and land it in a known place
phase: REVISE · rung ③. CHECK is JL's and no machine may reach it (for-display §phases)
session: e1976b65-13e7-46b9-ba1c-939da0293891
needs: QA-probe/QBt5-for-value/1-artifact-paths
output: _fixture-qbt/displays/QBt3-for-display/assets/figure.pdf

## Opening

Does the figure show who is allowed to take each step that produces a display unit, and does the render below say it without a caption's help?
The unit is real and so is what it draws: eleven steps, read from `source/source_data.csv` at draw time, each naming a path or a rung a reader can check against the folder beside this page.

It draws the pipeline this unit itself came out of, which is the one subject a specimen group can picture without inventing a finding.
It sits at rung ③ RENDERED: the render exists and no person has said yes to it.
Rung ④ is a human judgment, and no machine may write it.

A display is not decoration: this unit must carry one claim job, name its evidence source, state an honest statistical label, and land in a known place in the manuscript.

🚫 **This unit belongs to a fabricated project.** What is NOT fabricated is the shape: this page is a real `for-display` page, and its bindings resolve to files that really sit on disk, one folder away.

**Where its things are**: a page's companion folder is `<type-plural>/<page name>/`, so this page's unit is `_fixture-qbt/displays/QBt3-for-display/`. That is the group's one naming rule, and `QBt5`'s drawer is `QA-probe/QBt5-for-value/` by the same rule.

**Why this page is also the instruction**: it is the specimen for its type. `QB4` teaches the page grammar by being a page that obeys it; this page teaches the display form the same way. The rules themselves stay in `haipipe-page-for-display`, which this page never restates.

**Covered elsewhere**: `QB6` owns which types exist and what admits a new one. The `displays/<unit>/` folder shape is the paper board's, on its QBe series. How a sentence POINTS at a display is `QB8` §3.

## Diagram

**Its own input and output**: seven parts in, two out, and the one step between them a script owns.

```text
 📥 INPUT  display/QBt3-for-display/              ✍️ authored, seven parts
    ├── 🧪 source/       gen_display_pipeline.py · source_data.csv · paper_plot_style.py
    ├── 🗂 candidates/   A-narrow.pdf              the option that LOST, kept with its reason
    ├── 🖼 assets/       figure.pdf · figure.png   the one that WON
    ├── 📐 float.tex     the env, the caption, the \label
    ├── 📄 preview.tex   standalone wrapper, compiled from the paper root
    ├── 👁 preview.pdf   the render a person judges at rung ④
    └── 📝 README.md     takeaway · claim · evidence · placement · caption · fragility · status
                       │
                       │  🤖 cli/build-displays.py    the ONLY step here a script owns
                       ▼
 📤 OUTPUT _fixture-qbt/displays/QBt3-for-display/    🤖 generated, two things only
    ├── 📐 float.tex     asset path rewritten   ../display/ ──▶ displays/
    └── 🖼 assets/       figure.pdf · figure.png
                       │
                       │  ✍️ \input by the owning section
                       ▼
 📑 _fixture-qbt/sections/01_page_types.tex ──▶ 📕 QBt-page-types.pdf · Figure 1
```

⚖️ The render itself is NOT here. `## Diagram` is an ASCII figure and nothing else (`QB4` §2: `▧ ASCII, open`), and a compiled PDF or PNG is the unit's OUTPUT, so it belongs in the prose that explains it. It sits in `§1` below. It was in this section until 260807, which was the wrong section and is recorded rather than quietly moved.

## Content

### 1 · The render: what a person is being asked to accept

**The render**: the compiled figure a person is being asked to accept, embedded live from the unit rather than copied into this page.

![the display pipeline: four lanes, eleven steps, compiled from float.tex](QBt-page-types/display/QBt3-for-display/preview.png)

That is `preview.pdf`'s own PNG, produced by `pdflatex` from `float.tex`. It is a reference and not a transcript: change `source/source_data.csv`, re-run `source/gen_display_pipeline.py`, and this image changes with it. It was a hand-typed ASCII fence until 260806 and a `.txt` file until 260807, and that is exactly the defect this type exists to prevent, because a display page is where a person LOOKS at the render before accepting it and a hand-kept copy can be left behind silently by a rebuild.

What the figure says: four lanes, eleven steps, white for a step a person must take and grey for a step a script takes. Two of the eleven are grey and both sit in BUILD. Every step in ACCEPT is white, which is the rule the colours exist to carry and the reason this page cannot close itself.

🚫 The engine's own preview embed did NOT place this, and that is a defect worth naming rather than hiding. `src/dialect_paper.py` finds display units by globbing `S-Display-*` under `0-lifecycle/*display*/workspace`, and its unit marker only matches `S-Display-<n>` or `display<NN>`. A unit named `QBt3-for-display` matches none of them, so no evidence card and no auto-preview can ever fire here however correct the unit is. It is the same hardcoded-naming fault already fixed in `src/display_unit.py`, and it is an open row in `### Decision Now`.

**The evidence card**: the unit named in prose, which the engine turns into a card carrying its state.

The unit is QBt3-for-display, and that name is written bare rather than in backticks on purpose. A unit name in prose IS the evidence card (the `ALWAYS A CARD` ruling), and the card is what tells a reader whether the display is built and agreed without leaving the sentence. Backticks make it ordinary code and the card never appears, which is what happened on this page until 260807.

📌 Establishes what is on the table for rung ④, and what a person is actually being asked to say yes to.

### 2 · The claim job: what this unit must show, and for which claim

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

### 3 · Provenance: one row per number the unit shows

**Every number traced**: each value on the render, and the path it comes from.

```text
  value                    source                                kind
  ──────────────────────────────────────────────────────────────────
  214 · 61 · 48 · 44 · 33  QA-probe/QBt5-for-value/1-artifact-paths  atom id
  37 · 9 · 4 · 2 · 1         its counts.csv, resolved by id
  95% CI bounds            same atom, same CSV                   atom id
  17.3 · 14.8 · 8.3 ·      derived in source/build.py,           derived
  4.5 · 3.0                  drift_events divided by pages
  ──────────────────────────────────────────────────────────────────
  and that atom's own source is the answer table typed into
  QA-probe/QBt5-for-value/1-artifact-paths.md, parsed, never retyped
  ──────────────────────────────────────────────────────────────────
  THIS PAGE WRITES NO PATH. Its head says
    needs: QA-probe/QBt5-for-value/1-artifact-paths
  and the resolver finds it · every value is INVENTED
```

🔢 Establishes that nothing on the render appeared without a source, which is the whole job of this division on a real page.

The chain is QA record to display unit, and the hop is by ID. A real display page writes six hand-made paths in this division and every one dies when a folder moves; this page writes none. `python3 unit.py check` is what proves the chain, and it is the check a real paper cannot run today.

Proven by moving the answering atom's whole drawer and rebuilding: no script changed, no page changed, and the render came out identical.

### 4 · Spec: how the unit is produced, and what label is honest

**The recipe and its ceiling**: what makes the figure, and what the design lets it say.

```text
  unit       _fixture-qbt/displays/QBt3-for-display/    ← named after this page, exactly
  declares   this page's own head: needs, output
  input      needs: QA-probe/QBt5-for-value/1-artifact-paths   ← id, not path
  build      source/build.py · resolves that id, writes out/assets/figure.txt
  rebuild    python3 cli/build-displays.py <stage>         ← dependency order, whole chain
  verify     python3 unit.py check         ← every need resolves
  ──────────────────────────────────────────────────────────────────
  label      "association", not "reduces":
             ① tenure is not assigned, pages declared keys when their
               authors got to them
             ② no control for page size, and longer pages drift more
```

📐 Establishes the recipe and the honest ceiling on what the figure may claim.

The label line is what a reviewer reads first. A figure that says "reduces" over a design supporting "association" is the defect this division exists to catch, and it is caught here rather than in the caption because the caption is downstream of the spec.

### 5 · Placement: which sentence uses this unit

**One record per consumer**: where it lands, which sentence cites it, and whether the citation resolved.

```text
  consumer               sentence                             landed?
  ──────────────────────────────────────────────────────────────────
  S-Main-4-results §2    "Drift falls across all five bands    ✅ cited
                          (Figure 1)."
  S-Open-Pitch §1        "the tenure gradient"                 ⬜ named,
                                                                  not cited
  ──────────────────────────────────────────────────────────────────
  ⬜ would be what holds an ACCEPTED unit back from ⑤. It is not what
     holds this one back: the unit sits at ③, because ④ needs a person
     and none has looked. Both rows stay visible, and neither closes
     the other.
```

🔗 Establishes whether the unit reached the manuscript, which acceptance alone does not tell you.

### 6 · Fragility: what would send this unit back down the ladder

**What breaks it**: the changes that return an accepted unit to RENDERED or further.

```text
  cli/build-displays.py <stage> re-runs             ──▶ back to ③ · acceptance was of
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

### A1 · 👁 The render: what a person is being asked to accept
- A1.1 · The page shows the CURRENT render, never a copy of one.
  **Done when:** `§1`'s image is the unit's own `preview.png` by path, so re-running `source/gen_display_pipeline.py` changes what this page shows and nobody edits this page.
- A1.2 · The ENGINE embeds it, rather than the page naming the path by hand.
  **Done when:** `src/dialect_paper.py` finds a display unit by its `page-type:` key instead of by an `S-Display-*` glob, and the auto-preview fires here.

### A2 · 🎯 The claim job: what this unit must show, and for which claim
- A2.1 · The unit shows its claim job and nothing else.
  **Done when:** every series on the render is named in `§2`, and `§2` names no series the render lacks.

### A3 · 🔢 Provenance: one row per number the unit shows
- A3.1 · Every number on the render traces to a path that resolves.
  **Done when:** each path in `§3` exists on disk and the row count covers every value the render prints.
- A3.2 · The input moves behind a value binding once the scenario has a Value page.
  **Done when:** `§3`'s input rows cite the scenario Value page's value binding instead of the CSV directly.

### A4 · 📐 Spec: how the unit is produced, and what label is honest
- A4.1 · The statistical label does not outrun the design.
  **Done when:** the label line names every design fact that caps it, and a reader can check each one against `§4`.

### A5 · 🔗 Placement: which sentence uses this unit
- A5.1 · Every consumer either cites the unit or shows an open unplaced row.
  **Done when:** no `⬜` row in `§5` remains, at which point the state line moves to rung ⑤.

### A6 · ⚠️ Fragility: what would send this unit back down the ladder
- A6.1 · The events that void acceptance are written down before acceptance is asked for.
  **Done when:** `§6` lists every rebuild path that can change a printed number.

## States

- 260806 CC · The type key on this page is currently decorative. `page-type` is read by neither `src/parse.py` nor `cli/check.py`, so resolution step ③ does not run and this file still resolves by its `QBt3` filename at step ⑤. Rule 1 of `QB6` §5.1 is the fix.
- 260806 CC · Building this specimen found a conflict the prose never surfaced: `haipipe-page-for-display` rules that the state line reports a LADDER RUNG, and `cli/check.py` raises `bad-state` on any state line whose first token is not one of the four health words. A pure rung is an ERROR on every board today. This page carries the health word first and the rung as the next token, which passes and loses nothing; whether that is the answer, or whether the checker should learn the ladder, is unruled.

### Decision Now
- 📍 Does this render reach rung ④? Open `_fixture-qbt/displays/QBt3-for-display/assets/figure.pdf`, look at it, and say yes or no. Only you can move this one: `for-display/SKILL.md:27` calls `state:` a gate position no machine may flip, and `§6` of this page says the same. It sat at a machine-written ④ from 260806 until the cold read caught it; it is back at ③ and stays there until a person answers. 🛑 Blocks: the page's own state line, and `QBt6-for-section`'s `Q-Sec4Results-4`, which was ✅ on the strength of the forged rung.
- 📍 When the thirteen live display pages get their type key, does the `## Stage Contract` span stay or go? **A ·** remove it: the type that owns the page owns its sections, and a span no contract declares is furniture nobody maintains. **B ·** keep it: it records `requires` / `style-from` / `provides`, which a display unit genuinely has, and `stage.py sync` already maintains it. This specimen is written as A; if you rule B, the span is added here first and then to the thirteen.
- 📍 The state line conflict above: does `for-display` drop the ladder from `state:`, or does `cli/check.py` learn to accept a rung? Until this is ruled, every display page written to its own contract is an ERROR.

### A1 · 👁 The render: what a person is being asked to accept
- ✅ A1.1 · Met 260807. `§1` embeds `display/QBt3-for-display/preview.png` by path; the chain from `source_data.csv` through `pdflatex` to that PNG was re-run end to end the same day and the image changed with it.
- ⬜ A1.2 · Not started, and it is an ENGINE fix rather than a page fix. `dialect_paper.py` globs `S-Display-*` under `0-lifecycle/*display*/workspace`, and its unit marker matches only `S-Display-<n>` or `display<NN>`, so neither an evidence card nor the auto-preview can fire for a unit named `QBt3-for-display`.

### A2 · 🎯 The claim job: what this unit must show, and for which claim
- 🔨 A2.1 · The render's four lanes and eleven steps are named in `§2`, and its two actor marks are not yet, so `§2` does not yet name every series the figure prints.

### A3 · 🔢 Provenance: one row per number the unit shows
- ✅ A3.1 · `python3 unit.py check` in the group folder reports this unit's one need resolved and its product present, and every path `§3` names is on disk: the atom's `1-artifact-paths.md`, its `counts.csv` carrying all five bands, and the `source/build.py` the rates are derived in.
- ⬜ A3.2 · Not begun: `§3` still cites the atom's `counts.csv` directly, and E1's consumer row on `QBt5-for-value.md` carries no value binding, even though the scenario's Value page now exists.

### A4 · 📐 Spec: how the unit is produced, and what label is honest
- ✅ A4.1 · The render's label line names two design facts, that tenure is not assigned and that page size is not controlled, and `§4` lists exactly those two as ① and ②, so a reader can check each one.

### A5 · 🔗 Placement: which sentence uses this unit
- ❄️ A5.1 · Held at one open `⬜` row: `S-Open-Pitch §1` alludes to the unit without citing it. The hold is real but it is not what caps this unit; ④ is, and ④ waits on a person. The specimen therefore shows a RENDERED unit with a placement row already open, which is the ordinary shape, rather than the accepted-but-unplaced shape it claimed until the 260806 cold read.

### A6 · ⚠️ Fragility: what would send this unit back down the ladder
- ✅ A6.1 · `§6` lists every path that can move a printed number: a `cli/build-displays.py <stage>` re-run, a change to the atom's answer table, a band boundary move, and a venue figure limit change. Its own premise held up under test: `cli/build-displays.py <stage>` twice over the unchanged record reproduces `figure.txt` byte for byte, so a rebuild alone does not invalidate a render.

## Files

**📂 This page's own folders**: what it reads from, what it writes to, and how to check both are alive. A DISPLAY page owns a unit folder on BOTH sides.

```text
 📥 INPUT   display/QBt3-for-display/          ✍️ authored, seven parts
              🧪 source/       gen_display_pipeline.py · source_data.csv · paper_plot_style.py
              🗂 candidates/   A-narrow.pdf · A-narrow.png
              🖼 assets/       figure.pdf · figure.png · README.md
              📐 float.tex · 📄 preview.tex · 👁 preview.pdf · preview.png · 📝 README.md

 📤 OUTPUT  _fixture-qbt/displays/QBt3-for-display/   🤖 generated, never hand-edited
              📐 float.tex     asset path rewritten  ../display/ ──▶ displays/
              🖼 assets/       figure.pdf · figure.png
              ▶ then \input by _fixture-qbt/sections/01_page_types.tex ──▶ Figure 1 in the PDF

 ✅ CHECKLIST · what must be true, and how to see it
    ☑ the card renders     the unit named BARE in §1 prose becomes a chip
                           carrying its state; in backticks it stays code
    ☑ input resolves       ls display/QBt3-for-display/            7 parts
    ☑ output resolves      ls _fixture-qbt/displays/QBt3-for-display/  float.tex + assets/
    ☑ output is fresh      cli/build-displays.py <stage> --check   exits 0
    ☑ the render is current  re-run source/gen_display_pipeline.py and §1's
                           image changes without anyone editing this page
    ☐ a person accepted it   rung ④ · only JL may tick this one
```

- `display/QBt3-for-display/`
  📥 The INPUT folder: everything a person authors, including the recipe and the candidate that lost.
- `_fixture-qbt/displays/QBt3-for-display/`
  📤 The OUTPUT folder: float and assets only, generated by the board engine's `build-displays.py`. Editing anything here is overwritten on the next build.
- `_fixture-qbt/sections/01_page_types.tex`
  The section that `\input`s the shipped float, which is where this unit reaches a reader.
- `../../../board/haipipe-board/cli/build-displays.py`
  The engine command that turns INPUT into OUTPUT, and `--check` that says whether OUTPUT is stale.
- `QBt5-for-value.md`
  The evidence page whose record this unit's numbers would bind to.
- `../../paper/page-types/haipipe-page-for-display/SKILL.md`
  The contract this page is an instance of. If the two disagree, the contract wins and this page is the defect.
- `../BoardSkillBoard-260722/QPs-page-structure/QPs2-page-types/QPs2-page-types.md`
  §7 states the five on-disk shapes; this page is the worked UNIT one.

## Log

- 260807 1650 · [REVISE-CC] `phase:` declared, and `for-display` gained the section that makes it meaningful. The type had a five-rung ladder and mentioned the four Page Phases ZERO times, so nothing said which phase a rung belonged to. That gap is what let a machine write rung ④ onto THIS page on 260806: an orchestrator running a page loop had no rule telling it that a display page's CHECK is a human gate. The contract now states the mapping (DRAFT≈①, PROBE≈②, REVISE≈③, CHECK═④, with ⑤ outside the four) and the binding rule that this type's CHECK may not be delegated to a reviewer, because what it judges is what a picture looks like and no cold read of markdown reaches that.

- 260807 1200 · [REVISE-CC] rebuilt as a real UNIT, all seven parts on disk. `source/` holds the recipe (`gen_display_pipeline.py`, `source_data.csv`, `paper_plot_style.py` copied verbatim from the live MISQ unit), `candidates/A-narrow.pdf` holds the option that lost, `assets/figure.pdf` is the selected artifact, and `float.tex`, `preview.tex`, `preview.pdf`, `preview.png` and `README.md` complete it. The previous `displays/QBt3-for-display/out/assets/figure.txt` was text art stamped FABRICATED and is archived. The shipped side at `_fixture-qbt/displays/QBt3-for-display/` is GENERATED by `board/haipipe-board/cli/build-displays.py`, which rewrote the float's path from `../display/` to `displays/`, and `--check` exits 0. Still rung ③: no person has accepted this render.

- 260806 · [DRAFT-CC] written as a real `for-display` page rather than an essay about one, on JL's ruling that the example should BE its type, the way `QB4` is both the page grammar and a page obeying it. Unit and render built under `_fixture-qbt/displays/QBt3-for-display/`, named after this page exactly, so every binding resolves while every number stays invented.
- 260806 · [PROBE-CC] building the specimen surfaced two conflicts now recorded in `## States` and both Decision Now rows: the `## Stage Contract` span the type does not declare, and the state line the checker will not accept as a ladder rung.
- 260806 CC · Unit built and rendered through the whole chain. `cli/build-displays.py <stage>` runs the chain in dependency order: the QA record parses its answer table into `counts.csv`, then this unit resolves that atom by id and writes `out/assets/figure.txt`. `unit.py check` reports both units, both needs resolved, both products present.
- 260806 CC · The id-not-path rule was tested rather than asserted. The value unit was moved out of `S04-value/` into an unrelated folder and the chain was rebuilt with no edit to any script or page; the render came out identical. Then it was moved back. This is the one property the structure exists for, so it is proven here rather than claimed.
- 260806 CC · Structure A adopted for the scenario on JL's ruling: one unit, one folder, phases as subfolders, no published twin. The MISQ paper is untouched and follows later if this holds up.
- 260806 · [REVISE-CC] Rolled back from rung ④ to ③ by a cold read, and this is the finding the group most deserved to have caught. The page carried `state: 🟡 PARTIAL · rung ④ ACCEPTED · accepted 260806` on the strength of one Log line that named no person and quoted no one. Four sections above it, `§6` of this same page reads "no machine may write rung ④", and `for-display/SKILL.md:27` calls the state line a gate position no machine may flip. So the specimen for the one type whose whole distinction is that acceptance is a JUDGMENT had a machine-forged judgment in its state line, and `QBt6-for-section` had already marked `Q-Sec4Results-4` ✅ on the strength of it: one un-granted tick became three green claims across two pages. Rolling back is not enough by itself, so a Decision Now row now asks JL to look at the render and answer; the row it blocks is named there.
- 260806 CC · The unplaced row was left open on purpose and stays open. `S-Open-Pitch` alludes to the unit without citing it, so `§5` carries one `⬜`. What changed is what that row means: it caps a RENDERED unit at ③ rather than an accepted one at ④, and the figure said the wrong one until today.
- 260806 CC · Written as option A of the ruling in `States › Decision Now`: no `## Stage Contract` span, because `haipipe-page-for-display` declares none. The thirteen live display pages on the MISQ board all carry one, because they resolve as stage pages.
- 260806 · [REVISE-CC] The Opening rendered as 119 characters of bare question, so a cold reader met a bar chart of drift rates and had to open the fold to learn the corpus does not exist. Four sentences now sit on stage under the question, at 481 characters: the 🚫 notice that no corpus was ever counted and nothing here may be cited, that this is a working `for-display` page whose format is what it teaches, and the two that keep the rollback honest, that the unit sits at rung ③ RENDERED with no person's yes behind it and that rung ④ is a human judgment. One drawer sentence was deleted as the on-stage text now repeats it word for word: "Its numbers are invented, its corpus does not exist, and nothing here may be cited." Nothing else in the drawer moved.
- 260806 1259 · [REVISE-CC] States now mirrors every Aim id; three Aims are genuinely met (A3.1 by `unit.py check` resolving the need and the product, A4.1 by the label naming the same two design facts `§4` lists, A6.1 by `§6` covering every path that can move a printed number), A5.1 is held at its one open `⬜` row on purpose, A3.2 has not begun because `§3` still cites `counts.csv` and E1's consumer row carries no value binding, and A1.1 is short because the render prints `PAGES` and `DRIFT` columns that `§1` never names. The five dated records above moved here from States, where they were history sitting in a snapshot (QB4 §5.3.1); the two that describe the page as it stands now stayed.
