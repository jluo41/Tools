# Delivery Main: one authored source, and every manuscript file as a projection of it

state: 🟡 PARTIAL
owner: JL
method: treat each Main S page as the authoritative manuscript unit and its LaTeX/Word forms as projections

## Opening

How do Main pages become the journal's manuscript without becoming a second place to write?

A Main page is one authored unit of the argument, held as an S page on the board. A projection is a file generated from it, such as `sections/03_method.tex`. The danger is that a projection gets edited directly, and then two files both claim to be the source.

**Where this page sits**: QB5 Display hands over accepted visual units, and QB9 Build owns generating, checking, and promoting the candidate files.
This page owns only the question of which file a person may type into.

**Why a second authoring tree is the specific failure**: it never announces itself.
Someone fixes a typo in `sections/` because that is the file open in front of them, the fix is real, and from that moment the S page and the projection disagree with nothing reporting it.
Every later regeneration silently discards the better text.

**What makes the rule enforceable rather than aspirational**: the projection is regenerated from the S page and compared byte for byte.
A hand edit shows up as a difference the moment anything runs, so the rule is checked by the machinery rather than by everyone remembering it.

## Writing Style

How this page must be written. Read it before editing, and edit to it.

**Inherited from `QB4`**: the page grammar, the section order, and the sentence rules come from `../01-boardform-260722/QB-delivery/QB4-overall.md` and are not restated here.

**This page DESIGNS; the paper board SHOWS**: the design division states what a paper must carry for this concern, not what one paper happens to have today.
Where the MISQ paper differs, say so as a gap with an owner, never as the definition.

**Never explain the gates**: G0 through G5 belong to QB9 Build, and naming them here reads as though this page owned them.
Say "projection checks pass" and let Build define what that means.

**Always write the direction**: S page projects to `sections/`, never the reverse.
A sentence that puts `sections/` first, even harmlessly, is how the second-authoring-tree reading gets back in.

## Diagram

**One direction only**: what a person types into, and what is generated.

```text
   ✍️ AUTHORED                          🤖 GENERATED
   ────────────                         ─────────────
   S-Main-* ## Content  ━━━━━━━━━━━━▶  candidate
   the ONE place a                      │  projection checks
   person types                         ▼
                                       sections/*.tex
                                       Word handoff
                                        │
                                        ▼
                                       root master

   🚫 nobody edits sections/ ── a hand edit is silently
      discarded by the next regeneration
   ✅ the check: regenerate and compare byte for byte
```

## Content

### 1 · The delivery contract

**What Main owes**: the authored unit it holds, and the gate that lets it project.

```text
  📥 CONSUMES                📤 PROJECTS TO         🚪 GATE
  Opening · Work        ━━▶  sections/*.tex   ━━▶  the owning S page is
  Literature · Value         Word handoffs         explicitly GATED, and
  Display contracts          the root master       projection checks pass
```

📜 Establishes which file is authoritative, what it projects into, and what must be true before it may.

| Field | Contract |
|---|---|
| Lifecycle | Main manuscript work after the evidence/display lanes. |
| Authority | `0-lifecycle/4-main/S-Main-*.md`. |
| Projects to | `sections/*.tex`, Word handoffs, and the root master. |
| Skills | Section-edit stages plus `haipipe-paper-project`. |
| Consumes | Opening, Work, Literature, Value, and Display contracts. |
| Gate | The owning S page is explicitly GATED and projection checks pass. |
| Open gaps | Only MISQ Main-1 currently passes G1; the rest remain open or partial. |

#### 1.1 · Detailed Main-unit pages are earned, not scheduled
(a page per manuscript section would duplicate the S pages that already exist)
The board adds a Main-unit page only when a rule has to hold across papers.
Anything true of one paper's §3 belongs on that paper's own S page, where the prose it governs actually lives.

### 2 · What we want on the paper board

**The group we are designing**: a control page, then one page per numbered manuscript section.

```text
  🎯 WHAT WE WANT a paper to carry for this concern
  ### Delivery · Main
        🗂 S-Main-Dash.md         controls the SET
        📄 S-Main-0-abstract       ┐
        📄 S-Main-1-introduction   │ one page per numbered section,
        📄 S-Main-3-theory         │ NUMBERED because order is the argument
        📄 S-Main-4 … 8            ┘
        ⚠️ S-Main-2-literature is filed under Delivery · Literature

  ⚡ written by section-edit, the ONE stage that declares `runs: per-unit`
  🔗 units_from: S-Venue-2-narrative.md ── the arc supplies the section list
  🔢 NUMBERED, unlike Appendix, because a Main section's position IS
     part of what it claims
```

🎯 Establishes what a paper board must show for this concern, and where its section list comes from.

#### 2.1 · The section list is inherited twice, and this concern is the end of the chain
(the venue names the sections, narrative cuts them for this paper, section-edit makes one page each)
`section-edit` reads `units_from: S-Venue-2-narrative.md`, so Work's arc decides the units.
The arc did not invent them either: a venue playbook holds one folder per section, the venue stage transcribes them into the Structural Blueprint, and narrative adapts that list into the sections this paper writes (JL 260802).
So a Main unit exists because a venue has that section and this paper kept it, and changing either end changes the page list here.

#### 2.2 · One page is filed under another concern, and that is correct
(`S-Main-2-literature.md` keeps its Main id and sits under `Delivery · Literature`)
Its family prefix says Main wrote it and its group says Literature owns the rule it follows.
This is the clearest single example of the board's rule that a filename names the family and a group names the concern.

## Aims

### A1 · 📜 The delivery contract
- A1.1 · Exactly one file is authored per Main unit, and every manuscript file is derived from it.
  **Done when:** regenerating any projected Main file reproduces it byte for byte from its S page, with no hand edit surviving.
- A1.2 · The board grows a Main-unit page only when a cross-paper rule needs one.
  **Done when:** every Main-unit page on this board names the cross-paper rule that justified it.

### P · 🏁 Page-level
- P1 · The projection path is proven on real manuscript units, not only on one.
  **Done when:** more than one MISQ Main unit passes the projection checks that Main-1 passes today.

## States

### A1 · 📜 The delivery contract
- ✅ A1.1 · Ruled and exercised. The first candidate-only projection reproduced Main-1 byte-exact against its S page Content.
- ✅ A1.2 · Held so far. No Main-unit page exists on this board, which is the correct state while no cross-paper rule has appeared.

### P · 🏁 Page-level
- 🔨 P1 · Active and mostly unproven. Of the MISQ Main units, only Main-1 passes; the rest are open or partial, so the path is demonstrated once rather than established.

## Files

📋 **Contracts** · what carries this page's rule to somewhere else

- `board.md` · the `## Pages` order and the Board Map row for this concern
- `QB2-work.md` · owns the narrative page that supplies this concern's section list

📥 **Input files** · what the work reads

- `../../paper/S06-main/section-edit/stage.md` · the per-unit stage that authors a Main page, and where `units_from:` is declared

## Law

- Main S pages are authored.
  `sections/` is a submission projection and is never edited as the independent source.

## Glossary

- **Main unit**: one authoritative S page and the manuscript files it projects.
- **Projection**: a generated manuscript file whose contents are reproducible from its S page.

## Log

260802 · `§2.1` rewritten to name the whole chain rather than only its last hop: venue playbook, then Structural Blueprint, then narrative's adaptation, then `units_from` here.
260802 · Migrated to the QB4 page contract: Writing Style added, Content numbered with a face figure and caption, Aims regrouped as A1/P with `Done when`, States mirrored per Aim.
260730 · Main-1 candidate passed G0-G3 in the first runtime trial.
