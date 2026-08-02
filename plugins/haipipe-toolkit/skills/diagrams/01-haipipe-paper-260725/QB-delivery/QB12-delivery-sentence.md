# Delivery-Sentence: the four things that may hang off one sentence

state: 🟡 PARTIAL · the four attachment types are collected; lifting their shared rules to this head is open
owner: JL
method: hold every rule whose unit is one sentence and the evidence hanging off it, so the four attachment types are specified once and not four times

## Opening

What may hang off one sentence, and who is allowed to complete it?

A sentence is the smallest thing a reader can check. An attachment is evidence tied to it by a marker, such as `\cite{TOADD}` for a source or `{VAL:? 0.42}` for a number. Four types exist today and more may come. They share one grammar and differ only in who may finish them.

**Where this page sits**: QB11 holds the rules whose unit is a whole section, and QB13 holds the float as an object.
This page is the rung below both: one sentence, and what a reader can verify about it without reading anything around it.
Its four faces are QB12a a citation, QB12b a value, QB12c a pointer to a table, and QB12d a pointer to a figure.

**Why one head page and not four**: the four faces were written under three different concerns, so their shared rules were each written once, on whichever face happened to need it first.
Two are already visibly series-wide: a marker resolves at BUILD time and never at page load, written on QB12a, and staleness is COMPUTED and never declared, written on QB12c.
Neither is about citations or tables in particular.

**What differs between the four**: only who may complete the marker, and what a wrong one costs.
A citation is the one type an agent may never complete alone, because the key comes from a bibtex entry only a human may write.
A value has the shortest path to a retraction, so it binds to the RUN rather than to a file.
A table pointer is checkable on sight, while a figure pointer built from the wrong column is invisible, which is why the panel rules live on QB12d.

## Writing Style

How this page must be written. Read it before editing, and edit to it.

**Inherited from `QB4`**: the page grammar, the section order, and the sentence rules come from `QB4-overall.md` and are not restated here.
Read `QB4 § Writing Style` first; everything below is what this page adds.

**The unit is one sentence, and the test is shuffling**: before writing a rule here, ask whether it still holds with the surrounding paragraphs reordered.
If it needs to know what came before, it is a section rule and belongs on QB11.
This is the only admission test this page has, so apply it to every line.

**Name the four types, never count them**: write "a citation, a value, a table pointer, a figure pointer" rather than "the four attachment types".
A count becomes wrong the day a fifth arrives, and QB4 §1 already forbids opening with a roster that will grow.

**A shared rule names the face it came from**: when a rule is lifted here from one face, say which face wrote it.
The provenance is what lets a later reader check whether it really generalizes, and lifting without it is how a three-of-four rule becomes a false four-of-four rule.

## Diagram

**The four attachments**: what each carries in the prose, in its lane, and on screen.

```text
   📝 PROSE                  🗂 LANE                👁 READER
   ───────────               ──────────             ────────────────
📚 QB12a  \cite{TOADD}  ━━▶  source record    ━━▶  ❓ owed  · human-only key
🔢 QB12b  {VAL:? 0.42}  ━━▶  run binding      ━━▶  📦 ready · bound to the RUN
📊 QB12c  \ref{tab:x}   ━━▶  unit id          ━━▶  🥀 stale · computed, never declared
🖼 QB12d  \ref{fig:y}   ━━▶  unit id          ━━▶  ⚠️ panel · worst state wins

🔑 one grammar: marker in prose · record in a lane · state computed at BUILD
⚡ they differ ONLY in who may complete the marker, and what a wrong one costs
🚫 never: a state a human has to remember to set
```

## Content

### 1 · The shared grammar

**One shape, four fillings**: the three parts every attachment has, whichever type it is.

```text
     ┌──────────────┐   ┌──────────────┐   ┌──────────────┐
     │ 📝 MARKER    │──▶│ 🗂 RECORD    │──▶│ 👁 CHIP      │
     │ in the prose │   │ in its lane  │   │ on the page  │
     └──────────────┘   └──────────────┘   └──────────────┘
      author writes      probe or unit      build computes

  🔑 the join key `[Q-…]` sits BESIDE the marker, never fused into it
```

🔑 Establishes the one grammar all four types obey, and the two rules already proven series-wide.

#### 1.1 · A marker resolves at build time, never at page load
(lifted from QB12a, and it holds for all four because none of the four records live in the browser)
The chip a reader sees is computed while the page is generated, so what they read is what the repository held at that moment.
Resolving at page load would make the same page say different things to two readers, and neither could quote it.

#### 1.2 · Staleness is computed, never declared
(lifted from QB12c, and it holds wherever the evidence can change without the sentence changing)
A state a human has to remember to set is a state that will be wrong.
The rule survives the harder case too: a re-render only stales a state, while renaming the units stales the WORDS a page used to name them.

#### 1.3 · What is not yet proven shared
(the honest gap, kept visible rather than assumed away)
QB12b's bracket rule and QB12d's worst-state-wins panel are each written on one face and look general.
Neither has been tested against the other three, so neither is lifted here yet.
A rule that turns out to hold for only three of the four stays on its face.

### 2 · What separates the four

**Who may finish it**: the one axis on which the four genuinely differ.

```text
  🧠 HUMAN ONLY            🤖 AGENT MAY COMPLETE
  ─────────────            ─────────────────────
  📚 citation              🔢 value      ━▶ binds to the RUN, not a file
   the key comes from      📊 table ref  ━▶ checkable on sight
   a bibtex entry only     🖼 figure ref  ━▶ ⚠️ a wrong column is INVISIBLE
   a person may write

  💥 cost of a wrong one   value ━━▶ retraction    figure ━━▶ silent
                           citation ━━▶ visible    table  ━━▶ visible
```

⚖️ Establishes why one grammar still needs four faces, and what each face must therefore specify alone.

#### 2.1 · Completion authority is the real split
(it decides what an agent may do unattended, which is the only thing the distinction is for)
A citation may be searched and verified by an agent but never invented or silently written.
The other three may be completed from evidence the repository already holds, so the difference is not difficulty but authority.

#### 2.2 · Visibility of a wrong one decides how much checking a face owes
(a defect a reader can see needs less apparatus than one they cannot)
A wrong table is checkable on sight, because the numbers are printed.
A plausible-looking plot built from the wrong column is not, so QB12d carries the panel that names every asset and every candidate separately.

## Aims

### A1 · 🔑 The shared grammar
- A1.1 · The rules that hold for all four types are stated once, here, with the face each came from.
  **Done when:** QB12a's build-time rule and QB12c's computed-staleness rule appear on this page with their provenance, and neither face repeats the general statement.
- A1.2 · Every candidate shared rule has been tested against all four faces before being lifted.
  **Done when:** QB12b's bracket rule and QB12d's worst-state-wins rule each carry a written verdict here: general, or face-specific and why.

### A2 · ⚖️ What separates the four
- A2.1 · The completion-authority split is stated once and not re-argued on each face.
  **Done when:** each of the four faces names its completion authority in one line and points here for the reasoning.

### P · 🏁 Page-level
- P1 · A reader can find the rule governing one sentence without opening all four faces.
  **Done when:** a reader given a sentence with an unfamiliar marker reaches the right rule from this page in one hop.

## States

### A1 · 🔑 The shared grammar
- 🔨 A1.1 · Both rules are written into §1.1 and §1.2 with their originating face named. The faces still state them in their own words, so the de-duplication half is not done.
- ⬜ A1.2 · §1.3 records that QB12b's and QB12d's rules are untested against the other faces. No verdict is written for either.

### A2 · ⚖️ What separates the four
- ⬜ A2.1 · §2.1 states the split here. None of the four faces has been edited to point at it.

### P · 🏁 Page-level
- ⬜ P1 · Untested. The page exists and the four faces are collected under it; no reader has been asked to make the hop.

## Files

- `QB12a-sentence-citation.md` · the citation face, and the source of §1.1
- `QB12b-sentence-value.md` · the value face, holding the untested bracket rule
- `QB12c-sentence-display-table.md` · the table face, and the source of §1.2
- `QB12d-sentence-display-figure.md` · the figure face, holding the untested panel rule
- `QC5-sentence-evidence-contract.md` · the Paper board's sentence and evidence dialect above the Board grammar

## Law

- The unit of this series is one sentence, and the test of a sentence rule is that it survives the paragraphs being shuffled.
  A rule that needs to know what came before belongs in QB11.
  A rule is lifted to this head only after it has been checked against all four faces, and it names the face it came from.

## Glossary

- **Attachment**: evidence bound to one sentence through a marker, of which four types exist today and more may come.
- **Completion authority**: who is allowed to turn an owed marker into a resolved one, which is the only axis on which the four types differ.

## Log

260802 · Rewritten to the QB4 page contract: Writing Style added, Content numbered into two divisions with face figures and captions, Aims regrouped as A1/A2/P with `Done when`, States mirrored one row per Aim.
260802 · Opened as the head of the sentence series; QB3a, QB4a, QB5a, and QB5b became faces QB12a through QB12d.
