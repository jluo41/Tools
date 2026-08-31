# The life of a board: how one is born, and how it ends

state: 🟡 PARTIAL · the close is ruled (§6, 260816), not yet shipped · open: the proposal method
owner: JL
method: derive a proposal procedure from real boards and test whether a fresh agent produces clear pages and coherent groups; rule the close the same way, from what the `close` verb already does and what it leaves undecided

## Opening
How should a topic become a board, and what must be true for that board to end?

A board is born when a topic is cut into pages and groups, and it ends when every page is answered or parked.
Both ends are this page's subject, because they are the same judgement made twice: what deserves a page of its own, and when there is nothing left to own.
The middle, one round of work, belongs to `QA3`.

**Where this page sits**: This is the second rung of the `QA` chapter, between why a board exists (`QA00`) and the round (`QA3`); what graduates when a page settles is `QA6`.

**What changed on 260816**: The close joined this page (JL ruled the `QA` restructure).
Birth had a page and death had none, while the `close` verb shipped with one rule and nothing arguing it, so the two ends of one life now sit together as `§1`-`§4` and `§5`-`§6`.

**Why birth still matters**: The file grammar says how to store an accepted page, and it cannot decide which decisions or stages deserve pages of their own.
Without a decomposition test, an agent can create overlap, vague titles, and arbitrary groups that render cleanly but cannot steer the work.
The proposal succeeds when the user can see complete, non-overlapping ownership before approving any new file.

**Covered elsewhere**: File membership and numbering are `QB1`; the page's own section shape is `QPs1`; Board-Webpage-Index rendering and structure controls are `QB2`; prose inside an accepted page is checked by `QF1`; the gate at the end of one round is `QA3`.


## Diagram

**One board's life**: the two ends this page owns, and the loop between them that belongs to other pages.

```text
  🌱 BIRTH                         §1-§4, still unruled
     topic · files · throughline · finish condition
                     │
                     ▼
           candidate decisions or stages
                     │  remove overlap, expose gaps
                     ▼
           cluster by one enduring responsibility
                     │
                     ▼
        👤 the user reviews ONE proposal table
                     │  only then are files written
                     ▼
        📝 ## Pages  +  one page file each
                     │
  ═══════════════════╪═══════════════════════════════════
     🔁 the loop     │  argue → settle → graduate
        one round's gate is QA3 · what ships is QA6
  ═══════════════════╪═══════════════════════════════════
                     ▼
  🏁 CLOSE                          §5-§6
     ✅/⏸️ every page   +   `close:` satisfied      ← the verb checks this
                     │
                     ▼
     📦 the folder STAYS · `closed:` goes in the head
     🎓 `close` REPORTS every Law with no landing site named
     🔓 a doubted decision reopens it, like any page   ← §6, ruled 260816
```

## Content
### 1 · Terms and inputs
**Inputs and vocabulary**: the terms the proposal method defines and what open and add each receive.
```text
🧵 throughline        one sentence all pages collectively advance
🏁 finish condition   the evidence that the board's topic is resolved
❓ Q page             owns one answerable decision
🪜 S page             owns one ordered lifecycle stage and its outputs
🗂 group              one enduring responsibility, not similar words

📥 open   topic · files in scope · throughline · finish · constraints
📥 add    the same five  +  existing board index  +  the new concern
📝 both   assumptions block + requirements inventory before the table
```

A **throughline** is one sentence stating what all pages collectively advance. A **finish condition** is the evidence that the board's topic is resolved. A **Q page** owns one answerable decision; an **S page** owns one ordered lifecycle stage and the outputs needed to finish that stage. A **group** contains pages that share one enduring responsibility, not merely similar words.

**Files in scope** are existing source or evidence files that constrain the topic, not the page files that the action may create. **Known constraints** are requirements and exclusions stated by the user or the project. From these inputs, the agent writes a requirements inventory: the decisions or stage outputs that the proposed pages must cover.

For `open`, the procedure receives the topic, files in scope, throughline, finish condition, and known constraints. For `add`, it also receives the existing board index and the new concern to place. A short assumptions block and the requirements inventory appear before the proposal table. Missing inputs are drafted there for review instead of being silently invented.

### 2 · Deliverable
**The proposal table**: the seven columns a user judges before any file is written.
```text
              📋 one proposal table, shown BEFORE any file exists
type ❓🪜 · title 🏷 · lead · boundary ✂️ · finish 🏁 · group 🗂 · reason
                                |
        🌐 open   the whole candidate board
        ➕ add    the change + every page needed to judge overlap
                                |
                                v
   👤 user accepts or revises  →  only then ## Pages and files
✍️ settled form will land in ref/proposal-rules.md (open · add · propose)
```

Before writing files, the action shows one proposal table with these columns:

| Field | What the user must be able to judge |
|---|---|
| Page type | Q decision or S lifecycle stage |
| Proposed title | Short, concrete label unique on this board |
| Actual question or stage | The self-contained lead the page will own |
| Boundary | What belongs here and what belongs elsewhere |
| Finish condition | What permits this page to close |
| Proposed group | The index section that will contain the page |
| Group reason | One sentence true of every page in that group |

An `open` proposal shows the whole candidate board. An `add` proposal shows the requested change plus every existing page or group needed to judge overlap and placement. For a group-only addition, the table lists every proposed member.

The settled procedure will be recorded as `ref/proposal-rules.md` and invoked by the `open` and `add` sections of `SKILL.md`, and by the `propose` verb of `haipipe-board-routing`, which absorbed board-structure proposals on 260802; those two descriptions are corrected together. This page records the design discussion and evidence until those rules are settled.

### 3 · What exists today, and what none of it decides
**Today's fragments, and the tests they are missing**: every rule that exists, and the judgement none of them make.
```text
⚙️ SKILL.md open        asks page-list approval, gives no method
⚙️ routing propose      six-line structure proposal, no decomposition test
📄 page-template.md     title = short phrase · lead = actual question
📄 writing-rules.md     self-contained question · short heading
📄 board-form.md        ids · slugs · the ## Pages grammar
🖥 QB2                  how groups and rows render on the Index
🔧 live/structure.py    materializes a supplied title, never judges it
                =  🧩 fragments everywhere, no proposal method anywhere
```

The `open` action asks for a list of pages and requires user approval, but it gives the agent no method for producing that list. Since 260802, `haipipe-board-routing`'s board altitude owns `propose` and `materialize` for an agent: it shows a six-line structure proposal (spine, close, groups, pages, connections, skills) and stops for approval, but it too has no test for judging the decomposition. `page-template.md` says a page title is a short phrase and its lead is an actual question. `writing-rules.md` requires a self-contained question and a short heading. `board-form.md` defines ids, slugs, and the `## Pages` grammar. `QB2` defines how accepted groups and rows appear on the Board-Webpage-Index. `serve.py` can add a group or question from a title (through `live/structure.py` since the 260731 live split), but it does not judge the title or group.

**The missing tests**: what a page proposal and a group proposal must each pass.
```text
❓ page tests    🔒 one independently closable decision or stage
                 ✂️ no two pages overlap
                 🕳 no inventory item left without a page
                 🏷 title distinguishes without repeating the lead
🗂 group test    🧲 one enduring responsibility true of every member
                 🚫 never a mere cluster of similar words
↩️ on failure    revise the decomposition · leave pages ungrouped
🗑 never         invent a miscellaneous group to look complete
```

A page proposal needs a test for whether each page owns one independently closable decision or stage, whether two pages overlap, whether an item in the requirements inventory has no page, and whether the title distinguishes the page without repeating the full question. A group proposal needs an enduring responsibility: a shared function, output, stakeholder, or lifecycle segment that applies to every member and distinguishes those pages from pages outside the group. It must not merely cluster similar words.

If page scope, coverage, or separation fails, revise the decomposition. If the pages pass those tests but share no coherent responsibility, leave them ungrouped. Do not invent a miscellaneous group to make the index look complete.

### 4 · Acceptance dimensions to operationalize
**Seven acceptance dimensions**: the pass criteria a finished proposal is scored against.
```text
🎯 Scope        one decision or stage · one observable finish
🗺 Coverage     every approved inventory item lands on one page
✂️ Separation   no two pages claim the same decision or output
🏷 Name         distinguishes in the index without the full lead
🗂 Group        one responsibility sentence true of every member
🕊 Fallback     no shared responsibility  →  stays ungrouped
👤 Review       no files until the user accepts the table
```

- **Scope:** every page owns one decision or stage and one observable finish condition.
- **Coverage:** every item in the approved requirements inventory appears on one page.
- **Separation:** no two pages claim the same decision, output, or finish condition.
- **Name:** the title distinguishes the page in the index without restating its full lead.
- **Group:** one responsibility sentence applies to every member and distinguishes them from pages outside the group.
- **Fallback:** pages with no coherent shared responsibility remain ungrouped.
- **Review:** no files are created until the user accepts or revises the proposal table.

### 5 · The close, as the verb performs it today
**What ships**: two conditions, both readable off the board without judgement.
```text
🚦 every page's state:   starts with ✅ or ⏸️
      ✅ on a Q          every Aim met or explicitly held
      ✅ on an S         its own human gate passed
      ⏸️ either kind     a deliberate park, not a shortcut
📜 close:                the one sentence in board.md is satisfied
      ✍️ written to be ACCEPTED, never as "close enough"
                    =  🏁 the board may close
```

`haipipe-board`'s `close` verb states both conditions and nothing else: a board closes only once every page's `state:` starts with ✅ or ⏸️, and the sentence in `close:` is satisfied.
The state half is mechanical, because `check.py` already reads every `state:` line and refuses a ✅ page with an open Aim, so nobody has to be believed.
The `close:` half is a human judgement by design, which is why the sentence must be written so that it can be accepted: "SKILL.md is written, and a fresh agent with no background can read only that and open a decent board" can be tried, while "the board is in good shape" cannot.

This board's own `close:` is the worked example, and it is deliberately a test somebody runs rather than a feeling somebody reports.

### 6 · The second half of the close, ruled 260816
**Three answers**: what happens after the last ✅, ruled by CC under JL's delegation ("make the decision yourself", 260816).
```text
📦 the folder      it STAYS where it is · read-only by convention
                   `close:` gains a `closed: YYMMDD · who accepted it`
🎓 the audit       `close` REPORTS every ✅ page whose Law has no
                   landing site named, and a person clears the list
🔓 the reopen      a closed board reopens like any page (QPw00) ·
                   the head keeps `closed:` and gains `reopened:`
                   a drifted implementation is a defect, not a reopen
                =  🏁 the verb now has a second half, and none of it refuses
```
📌 Establishes the whole tail of a board's life; each of the three is stated so it can graduate into `SKILL.md`'s `close` section as written.

#### 6.1 · The folder stays, because the argument is the only place the reasons live

`QA00` §5 reads as a licence to delete, and it is not one: its test is a DEPENDENCY test, that nothing shipped may read a Q page, and it says nothing about what to do with the folder afterwards.
`QS2`'s law decides the rest: a record is archived and never deleted, and a whole board is the largest record this system makes.
So a closed board stays exactly where it is, keeps its generated site, and is rebuilt like any other board when the engine changes.
What closing changes is the reading, not the location: the board becomes read-only by convention, and `board.md` records the close with one line under `close:`, `closed: YYMMDD · <who accepted the condition>`, so a reader knows at the head whether the argument is still live.
Moving closed boards under an archive root was refused because it breaks every citation to them from the shipped units at once, and a shipped file citing its own design record is the one link this family most wants to keep.

#### 6.2 · The close reports the graduation, and never refuses it

`close` lists every page that reached ✅ or 🗂 and carries a `## Law`, and for each one names the file its Law landed in; a page with no landing site named is a row on the report, and a person either names the file or writes why the Law stays on the board.
It is a REPORT and not a refusal, for a measurable reason: a Law graduates as prose rewritten to fit its destination, never as a copied string, so no script can decide whether the rule really arrived, and a gate that cannot judge would either block every close or be waved through until nobody reads it.
The cheap half that makes the report possible is a note on the Law itself: when a rule graduates, its row gains `→ landed in <file> §<n>`, so the audit is a lookup instead of a re-read of two documents.
That note is what `QA6` §6.1's mechanism was always missing, and it is worth writing whether or not any board closes soon.

#### 6.3 · A closed board reopens, and the head says so

Reopening is already normal here, and CC's first draft of this division banned it, which contradicted three things at once.
`QPw00` and both shipped agents carry `reopens_promise: true` as a first-class route, DRAFT may reopen a page that already has polished prose, and a reopened promise starts a new round.
`QA00` itself reads `reopened 260816 as the introduction chapter`, and `QF` is described on `board.md` as the lane with a reopen path.
Nobody had ruled that a board is different from a page, and there was no reason to invent it.

So the ruling is that a closed board reopens the same way a page does, and the only new thing is the record.
When a settled page on a closed board goes back to 🟡 or 🔴, the board is open again: `board.md` keeps its `closed:` line and gains `reopened: YYMMDD · why`, both visible, because a board that closed once and reopened is a different thing from a board that never closed.

What is NOT a reopen is the case that will arrive most often.
A rule that shipped and that the code has since drifted from is a defect in the shipped unit, and it is fixed in that unit by whoever owns it today; the DECISION was never in question, so nothing reopens.
The page reopens only when the decision itself is doubted.

What a reopen never does is edit the old argument in place.
It adds a round, exactly as `QPw00` describes, for the same reason a sentence is archived rather than deleted: the record has to keep saying what was decided then, or the history stops being evidence.

## Aims
### Decision Now
These are the calls only JL can make; CC ticks nothing here.
The three close rows below are the exception and say so on their face: JL handed those three to CC on 260816 ("make the decision yourself"), and the last of them he then corrected.

- [ ] 📋 Approve the proposal table in Content §2 as the deliverable
      Both `open` and `add` would show this seven-column table before writing any file.
      → CC's proposal: yes as drawn; its columns already carry every acceptance dimension listed in §4.
- [ ] 🗂 Ratify the group default for a Skill-Board
      The ladder as the core (Board → Page-Structure · Page-Folder · Page-Workflow → Sentence), with Engine · Operating · Execute as the standing tail.
      → CC's proposal: yes; the three-layer version was field-tested twice, and the 260815 restructure is the same idea with the middle layer split by what it argues.
- [ ] ✍️ Decide when `ref/proposal-rules.md` gets drafted
      A · draft it now from §3 and §4, which gives a fresh agent something to be handed and exposes what §3 still leaves undefined.
      B · keep designing on this page until the tests above are settled, which delays the fixture test that needs the file.
      → CC's proposal: A; the fixture test needs a rules file a fresh agent can be handed, and drafting it will expose exactly what §3 still leaves undefined.
- [x] 📦 Rule what a closed board folder becomes
      ✅ `A` · CC ruled it under JL's delegation, 260816: "make the decision yourself".
      The folder stays where it is with its site, and `board.md` gains `closed: YYMMDD · who accepted it`; `§6.1` carries the reasoning.
      `B`, an archive root, was refused because it breaks every citation from a shipped unit to its own design record at once; `C`, deletion, misreads `QA00` §5, whose test is that nothing shipped may READ a board.
- [x] 🎓 Rule whether `close` requires the graduation audit
      ✅ `A as a report` · CC ruled it under the same delegation, 260816.
      `close` lists every ✅ page whose `## Law` names no landing site, and a person clears the list; it never refuses, because a Law graduates as rewritten prose and no script can judge whether the rule arrived.
      The mechanism that makes it cheap is new and small: a graduated Law row gains `→ landed in <file> §<n>`, so the audit is a lookup. `§6.2` carries it.
- [x] 🔓 Rule what reopens a closed board
      ✅ CC ruled, corrected by JL the same round.
      CC's first answer was that a closed board is never reopened; JL asked "who said so???" and nobody had: `QPw00` and both shipped agents carry `reopens_promise: true`, and `QA00`'s own state line reads `reopened 260816`.
      The ruling that stands is `§6.3`: a doubted decision reopens a closed board exactly as it reopens any page, `board.md` keeps `closed:` and gains `reopened: YYMMDD · why`, and a shipped rule the code drifted from is a defect in that unit rather than a reopen.


### The proposal method's tests
- [ ] 🧭 Settle how candidate pages are derived
      Define how the approved requirements inventory becomes candidate decision pages or ordered lifecycle-stage pages.
- [ ] ✂️ Settle the page-scope test
      Make the scope, coverage, and separation tests operational enough that two reviewers reach the same result.
- [ ] 🏷️ Settle the page-name test
      Define measurable title checks for length, concreteness, uniqueness, and stability as the work evolves.
- [ ] 🗂️ Settle the group proposal test
      Define when a new group is earned, whether a one-page group is ever valid, how its title and responsibility sentence are written, and which weak groupings are rejected.

### The deliverable and its trial
- [ ] 📋 Settle the proposal shown for approval
      Decide whether the table above is sufficient for both `open` and `add`, then place the final format in the Board reference file.
- [ ] 🧪 Test the method on real boards
      Freeze two fixture packets and answer keys: one decision board with independent questions and one lifecycle board with ordered stages and outputs. A fresh agent receives only `ref/proposal-rules.md` plus each packet and produces a proposal table. An independent reviewer scores both tables on the acceptance dimensions. After an accepted table is materialized, a second cold reader sees only `board.md` and must match the answer key for every page title's ownership and every group's reason without opening page bodies. Finish conditions are judged from the proposal table, not inferred from `board.md`.

### The close
- [x] 📦 Rule what happens to a board folder once it closes
      Ruled 260816 (§6.1): it stays where it is, keeps its site, and `board.md` records `closed: YYMMDD · who accepted it`.
- [x] 🎓 Rule whether closing requires a graduation audit
      Ruled 260816 (§6.2): `close` REPORTS every ✅ page whose Law names no landing site, and never refuses; the Law row carries `→ landed in <file>` from now on.
- [x] 🔓 Rule what reopens a closed board
      Ruled 260816 (§6.3): a doubted decision does, the same way it reopens any page (`QPw00`), and `board.md` keeps `closed:` while gaining `reopened: YYMMDD · why`.
      CC's first draft banned reopening and was struck the same round: `QPw00`, both agents, and `QA00`'s own state line already reopen things (JL: "who said so???").
- [ ] 🎓 The `→ landed in` note exists on a real Law row
      Done when: one settled page on this board carries the landing site on its `## Law` row, so the audit in §6.2 can be a lookup rather than a re-read.
- [ ] 🧪 Make the close runnable in one command
      Done when: `close --check` reports the pages still open, the pages whose Law names no landing site, and the `close:` sentence left for a person, so human judgement is the only thing the command does not do.
- [ ] 🎓 The three rulings graduate into the door
      Done when: `SKILL.md`'s `close` section and `ref/board-form.md` carry §6.1-§6.3 as written, including the `closed:` head key.

## Files
### Engines
- `../../board/haipipe-board/SKILL.md`
  The `open` action requires page-list approval but does not explain how the list is proposed; its `close` section carries the two conditions `§5` records.
- `../../board/haipipe-board/live/structure.py`
  `_slugify`, `Q_STUB`, and `structure_op` materialize a supplied title without judging it; they moved here in the 260731 live split, and `cli/serve.py` imports them.
- `../../board/haipipe-board/cli/check.py`
  Reads every `state:` line, which is the mechanical half of the close; a future structural check could also detect duplicate or weak page and group proposals once the human rule is settled.

### Input files
- `../../board/haipipe-board/ref/page-template.md`
  Defines the title as a short phrase and the lead as the full question.
- `../../board/haipipe-board/ref/writing-rules.md`
  Requires short headings and self-contained questions, but has no naming or decomposition test.
- `../../board/haipipe-board/ref/board-form.md`
  Defines ids, slugs, groups, and `## Pages` after the proposal has already been accepted.
- `2-QB-board/QB2-board-webpage-design/QB2-board-webpage-design.md`
  Owns how groups and page rows render and how they are edited, not how they are conceived.

## Law
- 260816 · CC under JL's delegation · 📦 **A closed board stays where it is**
  It keeps its folder, its generated site, and every path anyone cites it by; `board.md` records the close as `closed: YYMMDD · who accepted it`, and the board becomes read-only by convention.
  `QA00` §5's "the board is the deletable one" is a DEPENDENCY test, that nothing shipped may read a Q page, and it never licensed deleting the record.
- 260816 · CC under JL's delegation · 🎓 **The close reports the graduation and never refuses it**
  `close` lists every ✅ or 🗂 page carrying a `## Law` and names the file each Law landed in; a page with no landing site is a row on the report that a person clears or annotates.
  A Law graduates as prose rewritten to fit its destination, never as a copied string, so no script can decide whether the rule arrived, and a gate that cannot judge is either always blocking or always waved through.
  From now on a graduated Law row carries `→ landed in <file> §<n>`, which is what turns the audit into a lookup.
- 260816 · CC, corrected by JL · 🔓 **A closed board reopens like any page**
  A doubted decision reopens its page and with it the board; `board.md` keeps `closed:` and gains `reopened: YYMMDD · why`, because a board that closed once and reopened is not a board that never closed.
  A shipped rule the code has drifted from is a defect in that unit and reopens nothing, and no reopen ever edits the old argument in place: it adds a round, as `QPw00` already describes.
  CC first ruled the opposite, that a closed board is never reopened; JL asked "who said so???" and the answer was nobody, since `QPw00`, both shipped agents and `QA00`'s own state line all reopen things.

## Discussion
> JL: The current question names, page names, and especially proposed page groups are not consistently good. We need a dedicated question for how the Board should propose reasonable pages and groups.


### From the retired States section (merged 260831)
Only fragments exist for birth: titles must be short phrases, questions must be self-contained, ids and slugs have a grammar, and groups have an index representation. No rule currently tells an agent how to propose the pages or groups themselves.
For the close, the two shipped conditions are stated in `SKILL.md` and enforced only as far as `check.py` reads a `state:` line; the second half is ruled here as of 260816 and has not yet graduated into the door.
- 260816 · 🏁 The close's second half was ruled, on JL's delegation
  JL answered "make the decision yourself", so CC ruled all three holes in `§6`: the folder stays, the graduation audit is a report rather than a refusal, and a closed board reopens like any page.
  The reopen ruling was wrong on its first pass and JL caught it in one line, "who said so???": CC had banned reopening while `QPw00`, both shipped agents and `QA00`'s own state line all reopen things, so the ban was struck and the ruling now only adds the `reopened:` record.
  The graduation one was the load-bearing hole, because `QA6` §6.1 makes copying a settled Law the whole point of the loop and nothing checked that it happened; the fix is small and is a note on the Law row, `→ landed in <file>`, which turns the audit into a lookup.
  Nothing is enforced yet: three Aims stay open for the note, the command, and the graduation into `SKILL.md`.
- 260816 · 🏁 The close joined this page
  The `close` verb has shipped since the family's early releases and no page had ever argued it: `§5` records what it does today, and `§6` now rules everything after it.
- 260731 JL · 🗂 The groups settled at six
  The QD split and flatten produced Working · Sharing · Execute behind the unchanged three-layer core, so this board demonstrated the full shape twice over.
  Those three merged again on 260815 (`QO · Operating` plus `QF · Execute`), so a proposal method should treat Operating and Execute as the standing tail groups of a Skill-Board rather than three.
- 260730 JL · 🧭 This board's own groups were restructured to the three-layer model
  Seven groups became five: Design (what the system is) → Delivery (Board → Group → Page → Section → Sentence) → Engine (how it is made and shipped), plus Execute and Working.
  The same Delivery → Engine → Execute split had just been field-tested on the paper family's Skill-Board.
  Every page kept its id, because a page's letter is the group it was OPENED under, and the lane cells travelled with their pages (`lanes.py collect_kept`).
  The 260815 restructure replaced the Delivery layer with the ladder (Board → Page-Structure · Page-Folder · Page-Workflow → Sentence), which is the shape a proposal method should now propose in.
- 260726 JL · 🧩 The missing design layer was named
  JL observed that current question names, page names, and especially proposed page groups are not consistently good, and asked for a dedicated place to design a better proposal method.
- 260726 Cold read · 🧱 Inputs and acceptance tests were missing
  A fresh reader rated the first draft half-clear because its action names, board types, page types, inputs, deliverable, and pass criteria were undefined. This revision defines those premises without deciding the still-open proposal algorithm.
- 260726 Cold read 2 · 🧪 The design brief is clear; the test needed separation
  A second fresh reader rated the page clear as an open design brief. It found that generation and index-reading tests were conflated and that `board.md` could not expose finish conditions. The tests now have separate agents, artifacts, answer keys, and judging sources.

## Log
- 260816 · [REVISE-CC, JL delegated then corrected] `§7` went from three open holes to three rulings, on JL's "make the decision yourself".
  The folder stays, the graduation audit is a report with a `→ landed in` note behind it, and the reopen was ruled twice: CC banned it, JL replied "who said so???", and the ban was struck the same round because `QPw00`, both shipped agents and `QA00`'s own state line already reopen things.
  Three Aims stay open for the parts that are not shipped: the note on a real Law row, `close --check`, and the graduation of `§7.1`-`§7.3` into `SKILL.md` and `ref/board-form.md`.
- 260816 · [REVISE-CC, JL ruled] the close joined birth on one page and the file became `QA2-board-life`: `§6` records what the `close` verb performs today and `§7` names the three questions nothing owns, with four Aims and two Decision Now rows opened on them.
  The same pass swept the retired ids the 260815 restructure left behind (`QB4` → `QPs1`, `QC9`/`QD9`'s absorbed asks dropped as overtaken, `QE4` → `QO7`), and the group-default row was rewritten from the three-layer model to the ladder the board now runs.
- 260815 1500 · [REVISE-CC] opening figures added to §1-§5 (division-no-figure debt).
- 260806 2124 · [REVISE-CC] swept to the 260806 architecture; the live read/write proposal row marked overtaken (both ids retired into the round-trip and where-it-runs pages via the Links table), the Index citation corrected, `structure_op` repointed to `live/structure.py`, routing's 260802 propose verb added to the inventory
260731 · Items, Where we are, and Files regrouped to the section conventions of the day (matrix retrofit)
260731 · The unit-of-change proposal renumbered after a concurrent session took the id for the live-layer split: a live id beats a proposed one
260731 · The write-path page approved by JL and opened the same round; the unit of change and the optimistic echo still awaiting a ruling
260731 · Three pages proposed on the live read/write architecture (write path, unit of change, optimistic echo), awaiting JL; the stack half was already settled
260731 · Groups settled at six after the QD split (Working · Sharing · Execute); stale pointers moved to live ids
260730 · The board's seven groups were restructured into the Design → Delivery → Engine three-layer model with Execute and Working; every page kept its id
260726 · Opened from JL's request to design a better question, page-name, and page-group proposal method
260726 · Revised after cold read to define inputs, terms, deliverable, fallback, fixtures, and acceptance tests
260726 · Revised after second cold read to clarify `add`, group fallback, and two-stage validation

- 260831 0113 · `## States` merged into `## Aims` (tick + `Now:` per Aim; asks and threads kept verbatim), skill 0.148.0