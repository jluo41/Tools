# The paper board: a control plane nothing leaves

state: 🟡 PARTIAL · the frontier and the gate meaning are ruled and measured; the Round family is not built and the rule reaches no worker
owner: JL
method: one S page per independently gated unit, state read off the pages, and no second pointer anywhere

## Opening

What is on a paper's own board, and how is it not a design board?
`Paper-X/0-lifecycle/` uses the same tool, the same page grammar and the same four `state:` values as this one, so the two look alike.
They are opposites: a design board empties as its rulings leave, and this one never does, because a gated page's Content IS the paper.
Confuse them and you wait for a passed section to empty into the manuscript.
A control plane, a frontier that is derived rather than stored, and nothing that ever leaves.

**Where this page sits**: `QA3` is the deliberate opposite of this page, and the two were written as a pair.
`QA6` covers what else is in the paper folder, `QC3b` the grain that decides how many S pages a stage gets, and `QA8` who creates one.

**Why a stale render became a defect**: since 260726 this board is the paper's FACE rather than a file you may optionally open.
`/haipipe-paper enter` builds it and hands over its URL, so the human is looking at it before any work starts (`QA4`).
That is why every stage run now ends by rebuilding: a board nobody chose to open could be stale, and a board that IS the entry point cannot be.

## Writing Style

How this page must be written. Read it before editing, and edit to it.

**Inherited from `QB4@boardform`**: the page grammar, the section order, and the sentence rules come from `../01-boardform-260722/QB-delivery/QB4-overall.md` and are not restated here.

**Say which board a sentence is about, every time**: this page and `QA3` describe two objects that share a tool, a grammar and a glyph set.
An unqualified "the board" here is the defect the page exists to prevent.

**A glyph's meaning is stated with its owner**: `✅` means a ruling on a design board and a passed human gate here.
Never write the glyph without saying which one, because the two readings are what make a reader wait for the wrong thing.

**Never introduce a second place that holds the frontier**: not a pointer file, not a status field, not a cached value in prose.
The frontier is read, and every attempt to store it has ended by disagreeing with the pages.

## Diagram

**The execution pipeline**: eight families, and the edges that are real.

```text
 S-Seed 0,1          why this paper can exist, and where it sits
      ▼
 S-Work 0,1          the resources and the defensible claims
      ▼
 S-Venue 0..3        outlet · pitch · narrative · the decision register
      ▼
 S-Display 1..N      one page per figure or table, each gating alone
      ▼
   ┌──┴──────────────────────┐
   ▼                         ▼
 S-Main 1..9           S-Appendix 0,A..F
   └──────────┬──────────────┘
              ▼
 S-Submission 0..3    reconcile · compile · review · submit
                      four VERBS, stable and reused every round
      ▼
 S-Round 1..N         ONE page per round, carrying that round's discussion,
                      decisions, applied work and gate

 📖 this is EXECUTION order, not the Delivery reading order. Board adjacency
    never creates an edge
 🔁 an external review REOPENS the affected Work, Display, Main or Appendix
    page; the round page records what came back and what was done
```

**The two boards, side by side**: one glyph, two meanings.

```text
                    📋 ② DESIGN BOARD           📄 ⑧ PAPER BOARD
 ─────────────      ──────────────────────      ─────────────────────────
 what a page holds  the argument                the thing the unit produces
 ✅ means           a ruling was made           a human passed the gate
 on ✅              the Law LEAVES for ①        the Content STAYS
 delete it          every skill still runs      ⑦ loses frontier, queue,
                                                state, and nothing true can
                                                be said about the files
```

## Content

### 1 · A control plane, not a record

**One page per gated unit**: what an S page holds, and in which family.

```text
 📄 ONE S PAGE            = one independently gated unit
    📚 Content            the thing that unit exists to produce
    🎯 Aims               that unit's queue
    🚦 state:             where the unit actually is

 🗂 EIGHT FAMILIES   Seed · Work · Venue · Display · Main · Appendix
                     · Submission · Round
 📇 family order makes the index scannable; the pipeline holds the real edges
 🚫 nothing here empties on ✅, because the Content IS the paper
```

📄 Establishes what one S page is, what `✅` means on it, and why a passed gate keeps everything.

#### 1.1 · `state:` here means the gate, not the answer
(the single most important difference from `QA3`, where the same glyph means a ruling)
A human passes a CHECK gate; an unattended worker may prepare one and may never write the approval.
That is why the two boards cannot share a reader's expectation even though they share the glyph.

#### 1.2 · Nothing graduates, and that is the inverse of a design board
(a design board empties as its rulings leave, and this one accumulates)
When an S page passes its gate it keeps everything: the Content is the paper, the gate record is the provenance, and the queue is the history of how it got there.
Delete `②` and the skill still runs. Delete this board and `⑦` becomes a folder of files nobody can say anything true about.

#### 1.3 · One page per gated unit is ruled in general and unruled for Display
(the claim the page rests on, with one family that does not follow it)
Display has eleven S pages on the MISQ paper while its stage contract still says `runs: once`.
The ruling that would reconcile them is `QC3b`'s open migration to per-unit, so the grain holds everywhere except the one family that most needs it.

### 2 · The frontier is read, never stored

**Derivation**: where the current stage comes from, and what happens when it is written down instead.

```text
 ✅ READ IT            the earliest page in explicit pipeline order whose
                       gate has not passed, taken from the pages' own
                       state: lines

 ❌ STORE IT           tried twice, failed twice
    STATUS.md          current_layer began disagreeing with the gate record
    latest.md          a stored pointer to the current round, inside the
                       1-rounds/ folder this board absorbed

 📏 MEASURED 260726: run against the MISQ paper's 40 S pages, every stage
    predicate resolves and the frontier lands where it should
```

🧭 Establishes that the frontier is a derivation rather than a value, and records the two failed attempts to store it.

#### 2.1 · A stored pointer does not go wrong loudly
(it agrees for a while, then disagrees, and nothing announces the moment)
`STATUS.md`'s `current_layer` and `1-rounds/latest.md` are the same defect twice.
Both were written to save a derivation that takes one pass over the pages, and both would report a stage the gates no longer support.

#### 2.2 · The derivation was a claim until it was run
(260726 turned it into a measurement, and the run found one broken predicate)
Every stage predicate resolves against the MISQ paper's 40 S faces, and the frontier lands on `S-Seed-0-seed.md` 🟡, awaiting human CHECK, which is correct.
The one predicate that failed was a defect introduced the same morning: a `venue:` frontmatter key the board's grammar cannot parse, when the pin was already on the venue page's `state:` line.

### 3 · Rounds are pages, and what that replaced

**One page per round**: the four mechanisms the old folder duplicated.

```text
 📁 1-rounds/vYYMMDD/          ━▶ what already owned it
 ──────────────────────           ─────────────────────────────────────
 todo.md                       ━▶ QA9: ## Aims IS the queue
 decisions.md                  ━▶ S-Venue-3 is the decision register
 discussion.md                 ━▶ ## Discussion and anchored comments
 applied.md                    ━▶ that is what a passed gate records
 latest.md                     ━▶ 🚨 A STORED FRONTIER POINTER

 ✅ one S-Round page per round, in 0-lifecycle/7-round/
 📎 reviewer letters, decision letters and the submitted PDF sit BESIDE it
 🚫 four pages per round was considered and rejected: it would dissolve
    S-Submission for a distinction nobody has needed
```

🔁 Establishes why a round became a page, and that the reason was duplication rather than tidiness.

#### 3.1 · The dangerous file was `latest.md`, not the other four
(it is the disease this page's own Law names)
A stored pointer to the current round would have begun disagreeing with the pages exactly the way `STATUS.md` did.
The other four were merely redundant; this one was the frontier written down in a second place.

#### 3.2 · The received artifacts follow the page
(one round, one place)
Reviewer letters, decision letters and the submitted PDF sit beside `S-Round-<n>-<vYYMMDD>.md`, and `1-rounds/` is retired as a top-level container.
This differs from Display, whose S pages and rebuild workspace stay under `0-lifecycle/3-display/` while only the journal-facing `float.tex` and selected assets project out.

### 4 · Every edge runs through a page

**The boundary**: what may cross, and in which direction.

```text
 ① ━▶ ⑧  IN. The stage runner reads one contract from ①, works one S page
          here, and dispatches a bounded worker that returns to this page.
          create-page.py calls the board's stage.py: Board owns the filename
          and page grammar, Paper owns the Content jobs
 ⑧ ━▶ ⑦  OUT, by generation only. An S page's Content IS the section, and
          sections/*.tex is produced FROM it. md to tex, never back
 ⑧ ━▶ 🧱 OUT, through the page. A Q-consumer block becomes an entry in ⑦'s
          1-probes/, and the landed answer returns to the sentence that owes it
 ⑧ ━▶ ②  🚫 NOTHING. This board never writes to a design board
```

🔗 Establishes that no work reaches the paper without a page recording that it happened, which is what makes the frontier readable and the history real.

## Aims

### A1 · 📄 A control plane, not a record
- A1.1 · One S page exists per independently gated unit.
  **Done when:** every family's stage contract matches the number of pages it produces, including Display.
- A1.2 · `✅` on this board means a human passed a gate, and only a human writes it.
  **Done when:** no unattended worker can write a `✅` on an S page.
- A1.3 · The record-versus-control-plane difference reaches the worker who needs it.
  **Done when:** a stage worker reading `stage.md` learns which kind of board it is writing into, without reading a design board it is forbidden to read.

### A2 · 🧭 The frontier is read, never stored
- A2.1 · The frontier derives from the pages and exists nowhere else.
  **Done when:** no file outside the pages records the current stage or the current round, and the derivation runs against a real paper.

### A3 · 🔁 Rounds are pages, and what that replaced
- A3.1 · One S page per round, with its received artifacts beside it.
  **Done when:** `0-lifecycle/7-round/` exists, the `S-Round` family is in the board's family list, and `1-rounds/` is scaffolded by nothing.
- A3.2 · No shipped skill still describes the layer this ruling removed.
  **Done when:** `haipipe-paper-round` no longer owns a five-file `1-rounds/` contract with a `latest.md`.

### P · 🏁 Page-level
- P1 · A fresh reader can work a paper board without being taught it.
  **Done when:** a cold agent given `0-lifecycle/` alone names the frontier and the next action correctly.

## States

### A1 · 📄 A control plane, not a record
- 🔨 A1.1 · Ruled in general and unruled for one family. Display carries eleven S pages on the MISQ paper while its contract still says `runs: once`; `QC3b`'s per-unit migration is the open ruling.
- ✅ A1.2 · Ruled and in force. The CHECK gate is the one thing an unattended worker may prepare and may not write.
- 🧠 A1.3 · Waiting, and the gap is structural. Both statements of the rule, this page and `QA3`, sit on a design board runtime is forbidden to read.

### A2 · 🧭 The frontier is read, never stored
- ✅ A2.1 · Measured 260726 against the MISQ paper's 40 S faces: every predicate resolves and the frontier lands correctly. `STATUS.md` is retired and `latest.md` never shipped.

### A3 · 🔁 Rounds are pages, and what that replaced
- ⬜ A3.1 · Not built. The ruling landed on 260726 and `0-lifecycle/7-round/` plus the `S-Round` family entry are still owed.
- ⬜ A3.2 · Not started. `haipipe-paper-round` still owns the superseded contract, so a worker following it today would recreate exactly what the ruling removed.

### P · 🏁 Page-level
- ⬜ P1 · Never run.

## Files

### 📋 Contracts · what CARRIES a rule to other pages
- `../../board/haipipe-board/SKILL.md`
  The S-family grammar a paper board follows, owned by `③` and consulted here.
- `../../paper/haipipe-paper-stage/`
  The stage runner and its eight contracts, which is where `A1.3` must land for a worker to see it.

### 🧪 Checks · what CATCHES a page breaking a rule
- `../../board/haipipe-board/cli/check.py`
  Reports page structure on any board. It cannot tell a control plane from a record, which is why `A1.3` is 🧠 rather than mechanical.

### 📤 Output files · what a BUILD writes
- `../board/QA/QA7-the-paper-board.html`
  ⚠️ Generated by `cli/build.py`. Never hand-edit.

## Law

- A paper board is a control plane, not a record. Each S page is one independently gated unit; its Content is the thing that unit produces, and that Content is the paper.
- `✅` means a human passed the gate. Only a human may write it.
- The frontier is READ, as the earliest page in the explicit dependency graph whose gate has not passed, and is never stored in a second place. The Delivery index is a reading order and never an implicit execution graph.
- Nothing graduates out of a paper board. Where a design board empties as its rulings leave, a gated S page keeps everything it has.
- A round is a gated unit and therefore a page: one `S-Round` page per round, carrying that round's discussion, decisions, applied work and gate. `S-Submission`'s four verbs stay stable and are reused every round. No file outside this board records which round is current.
- Every edge runs through a page. There is no path by which work reaches the paper without a page recording that it happened.

## Lesson

- A stored derivation agrees for a while, which is why it survives review. `STATUS.md`'s `current_layer` and `1-rounds/latest.md` were the same defect twice, written to save a pass over the pages, and each would have reported a stage the gates no longer supported without announcing the moment it started lying.
- A rule stated only on a design board reaches nobody who runs. Both statements of the record-versus-control-plane difference sit where runtime is forbidden to read, so the worker most likely to confuse the two boards is the one who cannot see the rule.

## Glossary

- **Gated unit**: one part of a paper's lifecycle that a human accepts or rejects on its own, which is exactly what earns it a page.
- **The frontier**: the earliest page in pipeline order whose gate has not passed, always derived and never stored.

## Log

260802 · Migrated to the `QB4` page contract: Writing Style added, Content numbered into four divisions each with a face figure and caption, Aims regrouped as A1-A3 plus P with `Done when`, States mirrored one row per Aim, Files grouped by action. Two dead `## Files` paths repaired.

260726 · The frontier stopped being a claim and became a measurement: run against the MISQ paper's 40 S pages, every predicate resolves and the frontier derives correctly. The one failure was a `venue:` frontmatter key ruled into existence the same morning that the board's grammar cannot parse; the pin was already on the venue page's `state:` line. Also on this day the board became the paper's face rather than an optional file, so a stale render is now a defect (`QA4`).

260726 · Rounds moved inside the lifecycle (JL). `1-rounds/` is retired as a top-level container: the round page and its received artifacts both live in `0-lifecycle/7-round/`. One page per round, not four. `haipipe-paper-folder` now scaffolds three containers rather than four; `haipipe-paper-round` still owns a superseded five-file contract and needs a rewrite.
