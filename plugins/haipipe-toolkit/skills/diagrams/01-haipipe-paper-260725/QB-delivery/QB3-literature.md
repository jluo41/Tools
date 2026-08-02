# Delivery Literature: the path from a bank source to the sentence that rests on it

state: ✅ RULED
owner: JL
method: bind discovery-returned sources to manuscript sentences without letting the paper invent bibliography entries

## Opening

How does literature travel from the bank into a sentence and into the delivered file?

A source arrives from the discovery bank as an answer to a question QB2 Work asked. A binding is the path that ties it to the exact sentence it supports. A bibliography key is the short name the manuscript cites it by, and that key is the one thing on this path a machine may never mint.

**Where this page sits**: QB2 Work commissioned the discovery, and QB12a specifies the citation marker and the evidence card themselves.
This page owns the stretch between them: what has to be true for a returned source to become a citation a reviewer can follow.

**Why the key is the hard part**: everything else on this path can be checked automatically.
Whether a source exists, whether it resolves, whether the marker renders: all mechanical. Whether *this* source supports *this* sentence is a judgment, and inventing a key is how a fabricated citation enters a paper looking exactly like a real one.
So an agent may search and verify all day, and still may not write the entry.

**What is still unsolved**: Word has no `.bib`.
The LaTeX path has a real bibliography and the Word path does not, so the same binding has to survive as an explicit citation field or a baked reference, and that is an open gap rather than a settled rule.

## Writing Style

How this page must be written. Read it before editing, and edit to it.

**Inherited from `QB4`**: the page grammar, the section order, and the sentence rules come from `QB4-overall.md` and are not restated here.

**Never specify the marker**: `\cite{TOADD}`, the chip, and the evidence card belong to QB12a.
This page says a citation must be bound and human-keyed; it does not say what the binding looks like on screen.

**Always separate searching from writing**: the Law turns on that distinction, so a sentence that blurs "find" and "record" weakens the one rule this page exists to hold.

**This page DESIGNS; the paper board SHOWS**: `### 2` states what a paper must carry for this concern, not what one paper happens to have today.
Where the MISQ paper differs, say so as a gap with an owner, never as the definition.

## Diagram

**The literature path**: five hops, and the one a machine may not take.

```text
  🔍 QB2 Work probe
        ▼
  📚 discovery answer          ← the bank returns a verified source
        ▼
  ✍️ S-page sentence           ← a person decides it supports THIS claim
        ▼
  🔖 citation marker           ← 🧠 HUMAN-ONLY: the bibliography key
        ▼
  📖 bibliography              ← rendered per format

  ✅ an agent may SEARCH and VERIFY
  🚫 an agent may never INVENT or silently WRITE an entry
  ⚠️ Word has no .bib, so the last hop is an open gap
```

## Content

### 1 · The delivery contract

**What Literature owes**: a returned source in, a followable citation out.

```text
  📥 CONSUMES                📤 PROJECTS TO           🚪 GATE
  verified literature   ━━▶  sentence citations  ━━▶  the cited source
  returned by                format-specific          supports the EXACT
  discovery                  bibliography             sentence, and the key
                             rendering                is human-approved
```

📜 Establishes what a returned source must satisfy before a sentence may rest on it.

| Field | Contract |
|---|---|
| Lifecycle | After Work and before Value and Display in the Delivery reading order. |
| Authority | S-page prose plus the discovery answer bound through `1-probes/`. |
| Projects to | Sentence citations and format-specific bibliography rendering. |
| Skills | `haipipe-paper-probe`, evidence checks, and format adapters. |
| Consumes | Verified literature returned by discovery. |
| Gate | The cited source supports the exact sentence and the bibliography key is human-approved. |
| Open gaps | Word export has no `.bib` and must preserve an explicit citation field or baked reference. |

#### 1.1 · The gate tests the pairing, not the source
(a real, resolvable, correctly formatted source can still be the wrong one)
Verifying that a source exists is the cheap half and it is already automatic.
The gate is whether it supports the sentence it was attached to, which no checker can answer, and which is the only failure a reviewer will actually catch.

### 2 · What we want on the paper board

**The group we are designing**: two pages, two families, and no stage of its own.

```text
  🎯 WHAT WE WANT a paper to carry for this concern
  ### Delivery · Literature
        📄 S-Seed-1-literature.md   the research-lineage MAP
                                    written BEFORE Work · refreshed AFTER
        📄 S-Main-2-literature.md   the reader-facing Literature Review
                                    the authoritative manuscript section

  ⚡ this concern owns NO STAGE ── `index.yml` has no `literature` key
  🔑 so its pages are written by OTHER stages: seed writes the map,
     section-edit writes the review
  🚫 no S-Literature family ── the filename says who wrote it,
     the group says who owns the rule
```

🎯 Establishes what a paper board must show for this concern, and why a concern can be real with no stage behind it.

#### 2.1 · A concern can own a rule without owning a stage
(QB1 and QB2 each group stages; this one groups a rule that cuts across pages other stages wrote)
`index.yml` declares seed, resource, claims, venue, pitch, narrative, display, and section-edit, and none of them is literature.
The map page is written during seed and the review section during section-edit, so this concern never runs anything.
What it owns is the Law: an agent may search and verify a source and may never invent or silently write a bibliography entry, and that binds both pages plus every citing sentence in the manuscript.

#### 2.2 · The map comes twice, and that is the design rather than a repair
(`S-Seed-1` is drafted before Work and refreshed once Work accepts discovery answers)
The first pass frames the questions Work will commission, so it is oriented intuition rather than a survey.
The second pass rewrites it against what discovery actually returned, which is the only version a reader should trust.
`S-Main-2` is separate and stays the authoritative standalone section, so the map is working state and the review is the deliverable.

#### 2.3 · Where the MISQ paper stands against this
(the concern is built as designed, and the gap is one open rule rather than a missing page)
Both pages exist on the MISQ paper and sit under `Delivery · Literature`.
The open gap is not on the paper board: it is that Word has no `.bib`, so a citation binding has no agreed form in that export, which QB11b owns.

## Aims

### A1 · 📜 The delivery contract
- A1.1 · A bibliography entry never enters the paper without a person approving its key.
  **Done when:** no bibliography key on any paper reaches the manuscript without a recorded human approval, and an unapproved one renders as visibly owed.
- A1.2 · The detailed citation contract stays on QB12a rather than being restated here.
  **Done when:** this page names no marker syntax, and QB12a is the only page specifying the chip and the evidence card.

### A2 · 🎯 What we want on the paper board
- A2.1 · A paper board shows this concern as one group holding the map and the review.
  **Done when:** `Delivery · Literature` lists `S-Seed-1-literature.md` and `S-Main-2-literature.md`, and neither is filed under the group of the stage that wrote it.
- A2.2 · The map is refreshed after Work rather than left at its first pass.
  **Done when:** a paper's `S-Seed-1` names the discovery answers it was rewritten against.

### P · 🏁 Page-level
- P1 · A binding survives export to a format with no bibliography.
  **Done when:** a Word export carries an explicit citation field or baked reference that a reader can follow back to the same source as the LaTeX build.

## States

### A1 · 📜 The delivery contract
- ✅ A1.1 · Ruled and stated in the Law: an agent may search and verify, never invent or silently write.
- ✅ A1.2 · Held. The Scope paragraph hands the marker to QB12a, and no marker syntax appears on this page.

### A2 · 🎯 What we want on the paper board
- ✅ A2.1 · Built as designed on the MISQ paper: both pages sit under `Delivery · Literature`, although `S-Seed-1` carries a Seed prefix and `S-Main-2` a Main one.
- ❄️ A2.2 · Held while we work the design board. The two-pass design is written here; reading the MISQ `S-Seed-1` to see whether it was refreshed is paper work, and it thaws when we turn to the paper.

### P · 🏁 Page-level
- ❄️ P1 · Held, pending QB11b. This concern's rule is ruled without it: QB11b owns the Word adapter and has not yet decided how a citation survives with no `.bib`, so P1 thaws when that adapter rules.

## Files

- `QB12a-sentence-citation.md` · the marker, the chip, and the evidence card
- `QB11b-section-to-word.md` · the adapter where the no-bibliography gap has to be closed

## Law

- An agent may search and verify bibliography evidence; it never invents or silently writes a bibliography entry.

## Glossary

- **Literature binding**: the inspectable path from a sentence marker to the source that supports it.

## Log

260802 · `### 2 · What we want on the paper board` added. This concern turned out to own NO stage: `index.yml` has no `literature` key, so its two pages are written by seed and by section-edit, and what the concern owns is the Law rather than a stage. That is a second kind of Delivery concern, and QB1 and QB2 read as though every concern grouped stages.
260802 · Migrated to the QB4 page contract: Writing Style added, Content numbered with a face figure and caption, Aims regrouped as A1/P with `Done when`, States mirrored per Aim.
260729 · Literature placed after Work in the accepted Delivery order.
