# Delivery Literature: the path from a bank source to the sentence that rests on it

state: 🟡 PARTIAL · the citation Law is ruled; the dash-plus-topics shape is ruled and not built
owner: JL
method: bind discovery-returned sources to manuscript sentences without letting the paper invent bibliography entries

## Opening

How does literature travel from the bank into a sentence and into the delivered file?

A source arrives from the discovery bank as an answer to a question QB2 Work asked. A binding is the path that ties it to the exact sentence it supports. A bibliography key is the short name the manuscript cites it by, and that key is the one thing on this path a machine may never mint.

**Where this page sits**: QB2 Work commissioned the discovery, and QBe1 §4 specifies the citation marker and the evidence card themselves.
This page owns the stretch between them: what has to be true for a returned source to become a citation a reviewer can follow.

**Why the key is the hard part**: everything else on this path can be checked automatically.
Whether a source exists, whether it resolves, whether the marker renders: all mechanical. Whether *this* source supports *this* sentence is a judgment, and inventing a key is how a fabricated citation enters a paper looking exactly like a real one.
So an agent may search and verify all day, and still may not write the entry.

**What is still unsolved**: Word has no `.bib`.
The LaTeX path has a real bibliography and the Word path does not, so the same binding has to survive as an explicit citation field or a baked reference, and that is an open gap rather than a settled rule.

## Writing Style

How this page must be written. Read it before editing, and edit to it.

**Inherited from `QB4`**: the page grammar, the section order, and the sentence rules come from `../01-boardform-260722/QB-delivery/QB4-overall.md` and are not restated here.

**Never specify the marker**: `\cite{TOADD}`, the chip, and the evidence card belong to QBe1 §4.
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

**The group we are designing**: a dash plus one page per topic, the same shape as Display.

```text
  🎯 WHAT WE EXPECT a paper to carry for this concern
  ### Delivery · Literature                         ◀ ruled by QB3
      📁 (a literature/ folder, once the family exists)
      🗂 S-Literature-Dash          the control page: which topics exist
      📄 S-Literature-1-<topic>     one page per TOPIC
      📄 S-Literature-2-<topic>
      📄 S-Literature-3-<topic>

  🔗 the same shape as Display, deliberately
     Display     🗂 Dash + one page per UNIT
     Literature  🗂 Dash + one page per TOPIC
  🚫 the manuscript's Literature Review is NOT here: it is a Main
     section and lives under Delivery · Main (JL 260802)
  ⚠️ `Literature` is NOT a family yet, so none of these names resolve
```

🎯 Establishes what a paper board must show for this concern, and the one thing that stops it working today.

#### 2.1 · The unit is a TOPIC, not a stage and not a section
(JL 260802: literature should look like Display, cut by topic)
A topic is one lineage a paper has to hold: what has been done on it, where the gap is, and what this paper adds there.
QC3b's test says a unit splits when one can be approved while another is rejected, and topics do exactly that: the lineage on one topic settles while another is still being searched.
So the concern grows a page per topic and never a page per stage, because no stage owns it.

#### 2.2 · The Dash is the map, and it replaces the seed page's job
(`S-Seed-1-literature` carried the whole map in one page; a dash carries the index and the topics carry the content)
The map answers which topics this paper stands on and where each one stands.
Splitting it means a settled topic stops being re-read every time an unsettled one changes, which is the whole reason Display grew a dash.
`S-Seed-1` is still written at seed and refreshed after Work; under this shape it becomes the dash rather than the only page.

#### 2.3 · The manuscript's Literature Review is not this concern's page
(JL 260802: drop it from here; it is a Main section like any other)
`S-Main-2-literature` is prose a reader of the paper reads, so it is a numbered Main section and sits under `Delivery · Main`.
This concern owns the lineage behind it, topic by topic, and stops at the point where that lineage becomes manuscript prose.
That keeps one page under one concern and removes the join that used to put a Main-family page in this group.

#### 2.4 · Where the MISQ paper stands against this
(two pages today, both borrowed, and the family now exists to carry the new ones)
`Delivery · Literature` holds `S-Seed-1-literature.md` and `S-Main-2-literature.md`, and it still holds the second one.
This paragraph said until 260803 that `S-Main-2` had gone back to `Delivery · Main`, which QB6 denied and the live `board.md` never did; that sentence was wrong and is withdrawn.
`Literature` was admitted to all six lists on 260803, so `S-Literature-Dash.md` composes and parses today, and what is left is authoring the control page and the topic pages.
`QB0 §13.2` names the six and argues why a list spelled out six times is a list nothing enforces.

#### 2.5 · `S-Main-2-literature` keeps its Main filename and stays in this group
(ruled 260803, and reversible: it is one line in `board.md`)
The page is a numbered manuscript section, so its family is `Main` and its file stays in `4-main/`, and it is the lineage this concern owns, so its group is `Delivery · Literature`.
Now that `Literature` is a real family someone could rename the file into it, and `QB0 §12.5` is the reason not to: a group is one line a person moves inside `board.md`, while a family renames the file, moves it between folders, and breaks every id that cites it.
So the cheap cut gives way and the expensive one does not, which leaves the board's one live family-against-group trap in place on purpose.
`QB0 §12.4` names it where a reader meets it, and this page names it here, which is what closes that half of the disagreement.

## Aims

### A1 · 📜 The delivery contract
- A1.1 · A bibliography entry never enters the paper without a person approving its key.
  **Done when:** no bibliography key on any paper reaches the manuscript without a recorded human approval, and an unapproved one renders as visibly owed.
- A1.2 · The detailed citation contract stays on QBe1 §4 rather than being restated here.
  **Done when:** this page names no marker syntax, and QBe1 §4 is the only page specifying the chip and the evidence card.

### A2 · 🎯 What we want on the paper board
- A2.1 · A paper board shows this concern as one group holding the map and the review.
  **Done when:** `Delivery · Literature` lists `S-Seed-1-literature.md` and `S-Main-2-literature.md`, and neither is filed under the group of the stage that wrote it.
- A2.2 · The map is refreshed after Work rather than left at its first pass.
  **Done when:** a paper's literature dash names the discovery answers it was rewritten against.
- A2.3 · `Literature` is a first-class family, so a topic page can exist.
  **Done when:** `cli/stage.py`, `../../paper/haipipe-paper-stage/check-contracts.py` and `src/parse.py` all admit `Literature`, and `stage.py resolve` composes `S-Literature-1-<topic>.md`.
- A2.4 · The concern carries one page per topic under a dash.
  **Done when:** a paper's `Delivery · Literature` lists a dash plus one page per topic, and no single page carries the whole map.

### P · 🏁 Page-level
- P1 · A binding survives export to a format with no bibliography.
  **Done when:** a Word export carries an explicit citation field or baked reference that a reader can follow back to the same source as the LaTeX build.

## States

### A1 · 📜 The delivery contract
- ✅ A1.1 · Ruled and stated in the Law: an agent may search and verify, never invent or silently write.
- ✅ A1.2 · Held. The Scope paragraph hands the marker to QBe1 §4, and no marker syntax appears on this page.

### A2 · 🎯 What we want on the paper board
- 🔨 A2.1 · Partly. Both pages sit under `Delivery · Literature`, but the group is two pages rather than a dash plus topics, which is what JL ruled on 260802.
- ❄️ A2.2 · Held while we work the design board. The two-pass design is written here; reading the MISQ dash to see whether it was refreshed is paper work.
- ⬜ A2.3 · Not started, and it blocks A2.4. The family list is closed in three files and none of them names Literature, so no topic page can be resolved, composed, or parsed today.
- ⬜ A2.4 · Not started, and blocked on A2.3.

### P · 🏁 Page-level
- ❄️ P1 · Held, pending QBe3 §4. This concern's rule is ruled without it: QBe3 §4 owns the Word adapter and has not yet decided how a citation survives with no `.bib`, so P1 thaws when that adapter rules.

## Files

- `_archive/QBe1a-sentence-citation.md` · the marker, the chip, and the evidence card
- `_archive/QBe3b-section-to-word.md` · the adapter where the no-bibliography gap has to be closed

## Law

- 📚 An agent may search and verify bibliography evidence; it never invents or silently writes a bibliography entry.
- 🗂 **Literature is cut by TOPIC, and takes the Display shape: a dash plus one page per topic** (JL 260802: literature should look like display, split by topic). The topic pages are the working record and `S-Main-2-literature` is what ships, exactly as Display's unit pages are working record and `float.tex` ships.

## Glossary

- **Literature binding**: the inspectable path from a sentence marker to the source that supports it.

## Log

260803 · The `S-Main-2-literature` disagreement is closed, in favour of the live board. This page had said the page "has gone back to `Delivery · Main`"; QB6 said it stays under `Delivery · Literature`; the MISQ `board.md` has listed it under Literature the whole time. Two against one, so the sentence here was the wrong one and is withdrawn. `§2.5` is new and states the ruling with its reason, which is `QB0 §12.5`: a group is one line inside `board.md` and a family is a rename plus a folder move plus every citation, so the group is the cut that gives way. This is reversible by moving one line, and nothing was renamed.
260803 · `Literature` was admitted to all six family lists, so this concern is no longer blocked. `§2.4` rewritten: the count on this page went three, then five, then six inside two days, which is `QB0 A13.1`'s whole argument.
260803 · The family-list count on this page was wrong: `§2.4` said the list is closed in three places and named three. It is FIVE. The two it omitted are `src/page_board.py:497` and `live/chat.py:201`, which are exactly the two that fail with no message, so a person following this page would have admitted `Literature` to three of five and got a page that parses, sorts nowhere, and cannot be linked. Corrected in `§2.4`; the 260802 Log entry below is left as written, because it records what was believed then. `QB0 §13` now argues the write side against the read side, and `QB0`'s Law names all five paths.
260802 · State dropped from ✅ to 🟡. The concern's Law is still ruled, but JL ruled a new shape the same day and nothing carries it, so three Aims are open and `settled-with-open-aims` caught the mismatch.
260802 · JL: literature should look like Display and be cut by TOPIC, with a dash plus `S-Literature-1`, `-2`, `-3`. `§2` redrawn to that shape, and QC3b's per-unit test backs it: one topic settles while another is still being searched. A2.3 opened on the blocker, which is the same one Round carries: `Literature` is not a family, and the list is closed in `cli/stage.py:27`, `check-contracts.py:40` and `src/parse.py:247`.
260802 · `### 2 · What we want on the paper board` added. This concern turned out to own NO stage: `../../paper/haipipe-paper-stage/stages/index.yml` has no `literature` key, so its two pages are written by seed and by section-edit, and what the concern owns is the Law rather than a stage. That is a second kind of Delivery concern, and QB1 and QB2 read as though every concern grouped stages.
260802 · Migrated to the QB4 page contract: Writing Style added, Content numbered with a face figure and caption, Aims regrouped as A1/P with `Done when`, States mirrored per Aim.
260729 · Literature placed after Work in the accepted Delivery order.
