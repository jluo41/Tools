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

## Aims

### A1 · 📜 The delivery contract
- A1.1 · A bibliography entry never enters the paper without a person approving its key.
  **Done when:** no bibliography key on any paper reaches the manuscript without a recorded human approval, and an unapproved one renders as visibly owed.
- A1.2 · The detailed citation contract stays on QB12a rather than being restated here.
  **Done when:** this page names no marker syntax, and QB12a is the only page specifying the chip and the evidence card.

### P · 🏁 Page-level
- P1 · A binding survives export to a format with no bibliography.
  **Done when:** a Word export carries an explicit citation field or baked reference that a reader can follow back to the same source as the LaTeX build.

## States

### A1 · 📜 The delivery contract
- ✅ A1.1 · Ruled and stated in the Law: an agent may search and verify, never invent or silently write.
- ✅ A1.2 · Held. The Scope paragraph hands the marker to QB12a, and no marker syntax appears on this page.

### P · 🏁 Page-level
- ❄️ P1 · Held, pending QB11b. This concern's rule is ruled without it: QB11b owns the Word adapter and has not yet decided how a citation survives with no `.bib`, so P1 thaws when that adapter rules.

## Files

- `QB12a-sentence-citation.md` · the marker, the chip, and the evidence card
- `QB11b-section-to-word.md` · the adapter where the no-bibliography gap has to be closed

## Law

An agent may search and verify bibliography evidence; it never invents or silently writes a bibliography entry.

## Glossary

- **Literature binding**: the inspectable path from a sentence marker to the source that supports it.

## Log

260802 · Migrated to the QB4 page contract: Writing Style added, Content numbered with a face figure and caption, Aims regrouped as A1/P with `Done when`, States mirrored per Aim.
260729 · Literature placed after Work in the accepted Delivery order.
