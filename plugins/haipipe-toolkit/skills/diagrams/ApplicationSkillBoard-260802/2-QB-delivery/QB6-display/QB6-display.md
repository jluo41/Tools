# Delivery Display: venue-gated units between evidence and artifact

state: 🔴 OPEN
owner: JL
method: state the gate and the unit contract from the stage doc, then put QB5@paper's seam in front of JL for adoption

## Opening
What does Display deliver for an intervention, which venues fire it, and where is the seam with the shared Display layer?
The stage maps each claim to a display unit (a panel, chart, or section) and gives each unit one job for the reader.
An sms venue skips the stage because its template fixes the elements; a dashboard or report venue requires it.
This page states what the stage owns and asks JL to adopt the seam that leaves rendering to the display layer.

**Display unit**: one content element carrying one claim, such as a chart on an engagement dashboard; every unit carries a Type, a Claim, a Job, and a Data source.

**Venue gate**: the pinned venue decides whether this stage fires at all, read from `STATUS.md`'s `stages_skipped` row; sms, push, reminder, and checklist skip it, dashboard, ui-card, and report require it, and email pulls it in on user request.

**Covered elsewhere**: QB5@paper ruled this seam for the paper family, where the units are figures and tables; this page adopts its line for interventions and adds the gate in front of it.

**Why it matters**: without the gate an sms intervention pays for a stage whose venue template already fixed the elements, and without the seam this concern rewrites the shared display layer's rendering rules one unit at a time.

## Writing Style

How this page must be written, so the next editor edits to the same rules.

**Inherited**: the page grammar, section order, and sentence rules come from the board's page contract and are not restated here.

**Ownership as a pair**: write what the intervention family owns and what the shared display layer owns in the same sentence, because half the pair alone reads as a land grab.

**The gate comes first**: every ownership sentence assumes the stage fired, so where a skipped venue changes the answer, say so in the sentence itself.

## Diagram

**The gate, then the seam**: whether the stage fires, and who owns what when it does.

```text
          🚦 VENUE GATE · read from STATUS.md stages_skipped
   ⏭ skipped      sms · push · reminder · checklist
   🔀 optional     email · on user request
   ✅ required     dashboard · ui-card · report
                       │ fires
                       ▼
   🧩 FAMILY OWNS                    ⚙️ DISPLAY LAYER OWNS
   which units exist                 rendering
   claim linkage · Job
   unit -> section placement
        └─────────── 🤝 the seam · QB5@paper ───────────┘
```

## Content

### 1 · 🚦 The venue gate

**Which venues fire the stage**: the gate as the stage doc states it.

```text
  ⏭ skipped     sms · push · reminder · checklist
  🔀 optional    email · on user request
  ✅ required    dashboard · ui-card · report
  📖 read from   STATUS.md · stages_skipped
  🔁 on change   a venue change re-runs the display set
```
📌 This part settles when the stage exists at all, and the pinned venue decides that, never the stage itself.

The gate is read from the intervention's `STATUS.md` `stages_skipped` row, so an absent `4-display.md` on an sms intervention is correct rather than missing.
A skipped venue is not a lost stage: the venue template already fixes the elements, so a display map would only restate it.
The venue-ALIGNED stages 3 to 5 (narrative, display, section-edit) exist only when the pinned venue requires them, and display reads narrative's arc only if that stage fired.
The available element types come from the venue stage doc's Artifact Principles in `0-lifecycle/2-venue/2-venue.md`, which is why a venue change re-runs the whole display set.

### 2 · 🧩 The unit and its job

**One display unit**: the fields every unit must carry.

```text
  🏷 Type          panel · widget · chart · section
  🧾 Claim         the 1c-claims entry it carries
  🎯 Job           what the reader must see or do · one sentence
  📥 Data source   the task-side output it shows
  📊 Status        planned · commissioned (PP<nn>) · landed
```
📌 This part settles what the stage delivers: a map from every primary claim to at least one unit, each with a required job.

The stage answers what content element carries each claim and what job each unit does for the reader.
A unit is a panel, widget, chart, or section, where the paper family would have a figure or table.
The Job field is the retired minimap stage's concern folded in per unit: one sentence on what this unit must make the reader see or do.
The deliverable is `0-lifecycle/4-display/4-display.md`, with the phase journal in `_LOG_4-display.md` and, on sectioned venues, a unit-to-section mapping inside it.
Display is the one stage that commissions its own units: a unit missing from narrative or a section becomes a request row fulfilled here, and a unit whose data source does not exist yet is raised as a section in the flat probe pool `1-probes/PPNN_<topic>/`.
The stage plans and links; its LAW 1 forbids it to compute, render, or hand-author an asset, so the rendered output lands task-side and the unit's Data source field points at it.

**2.1 · What done means at CHECK**
- `4-display.md` exists, when the venue requires it.
- Every primary claim has at least one display unit.
- Every unit carries all four fields: Type, Claim, Job, Data source.
- Every unmaterialized data source has a probe-pool section, commissioned by this stage.
- Every unit's type is in the venue's element set.

### 3 · 🤝 The seam with the shared Display layer

**The seam, adopted from the paper board**: two owners, and who may change their mind.

```text
  🧩 FAMILY OWNS                     ⚙️ DISPLAY LAYER OWNS
  which units exist                  rendering
  caption side · claim linkage
  placement · unit -> section
       └────────── 🤝 QB5@paper's line, offered here ──────────┘
```
📌 This part carries the one ruling this page needs from JL: whether QB5@paper's seam is adopted verbatim.

QB5@paper ruled the seam for the paper family: the family owns why a display exists, what it argues, where it lands, and whether it is accepted, and the Display layer makes it.
Read for an intervention, the family side is the unit set (which units exist), each unit's Claim and Job (this family's caption and claims linkage), and the unit-to-section mapping (placement), while the shared display layer owns rendering.
Acceptance stays family-side here too: the stage's CHECK phase reads the done list against the unit set and writes a Gate Ledger row in `STATUS.md`.
The stage doc already holds this line from its own side, because LAW 1 says display plans and links units and never computes, renders, or hand-authors one.
What QB5@paper never faced is the gate: on a skipped venue the venue template owns the elements outright, so the seam here carries one option the paper board did not need, and that choice sits in Decision Now.

## Aims

### A1 · 🚦 The venue gate
- A1.1 · This page states the gate exactly as the stage doc does.
  **Done when:** the skipped, optional, and required venue sets in Part 1 match the stage doc, and the re-run rule on venue change is stated beside them.

### A2 · 🧩 The unit and its job
- A2.1 · The stage's deliverable is readable from this page alone.
  **Done when:** Part 2 carries the four unit fields, the three unit statuses, and the five done conditions, without sending the reader to the stage doc.

### A3 · 🤝 The seam with the shared Display layer
- A3.1 · The seam ruling is adopted for the intervention family.
  **Done when:** JL answers the Decision Now row, and the chosen form of the seam lands in this page's Law with the date and the rejected option.

## States

### Decision Now
- [ ] 🗣 Adopt QB5@paper's seam verbatim, or amend it for skipped venues?
      📍 `Part 3` the seam with the shared Display layer
      🔔 `Why now` the stage doc's LAW 1 already behaves as if the seam holds, but no ruling on this board says the intervention family adopted it.
      ⭐ `A ·` adopt verbatim: the family owns which units exist, their caption and claims linkage, and placement, and the shared display layer owns rendering, with the gate deciding only whether the stage fires; CC recommends A because LAW 1 already enforces exactly this line and an amendment would give one layer two seams.
      `B ·` amend for skipped venues: on sms, push, reminder, and checklist the venue template owns the elements outright, so the seam is written venue-owned there and family-owned everywhere else.
      🛑 `Blocks` A3.1, which stays open until the ruling lands in Law.
      🤖 `If nobody answers` A holds provisionally, because it is the only seam anyone has written down.

### A1 · 🚦 The venue gate
- ✅ A1.1 · Met at creation; Part 1 carries the gate and the re-run rule from the stage doc read on 260802.

### A2 · 🧩 The unit and its job
- ✅ A2.1 · Met at creation; Part 2 carries the four fields, the three statuses, and the five done conditions from the stage doc read on 260802.

### A3 · 🤝 The seam with the shared Display layer
- 🧠 A3.1 · Waiting on JL; the Decision Now row above holds the choice, and LAW 1 behaves as option A in the meantime.

## Files

### Engines
- `../../../../application/1-lifecycle/4-display/haipipe-application-display/SKILL.md`
  The stage this page maps; the gate roster, the four unit fields, LAW 1, and the done list live here, so a change to any of them starts in this file.

### Input files
- `../PaperSkillBoard-260725/2-QB-delivery/QB5-display/QB5-display.md`
  The paper board's seam ruling this page adopts as QB5@paper; open it when the two families' seams look like they disagree.

## Glossary

- 🚦 **Venue gate**: the `STATUS.md` `stages_skipped` read that decides whether a venue-gated stage fires; an sms venue skips display and a dashboard venue requires it.
- 🧩 **Display unit**: one content element carrying one claim, a panel, widget, chart, or section, with a Type, a Claim, a Job, and a Data source.
- 🤝 **Seam**: the ownership line between an artifact family and the shared display layer, deciding who may change their mind about what.
- 🕳 **Probe pool**: the intervention's flat `1-probes/PPNN_<topic>/` folder where a stage raises questions it cannot answer itself; display raises unit materialization there.
- 📄 **QB5@paper**: the Delivery Display page on the paper board of 260725, this page's precedent for the seam.

## Log

260802 · Page created: the venue gate and the unit contract stated from the stage doc, and QB5@paper's seam raised to JL for adoption in Decision Now.
