# ⑧ The paper board: what is worked, and why nothing leaves
state: 🟡 PARTIAL
owner: JL
method: one S page per independently gated unit, state read off the pages, and no second pointer anywhere

## Opening
What is on a paper's own board, and how is it not a design board? It uses the same tool, the same face grammar and the same four state values, which makes the two look identical. They are opposites: a design board empties as its rulings graduate out, and a paper board never empties, because its Content IS the paper.

`0-lifecycle/` uses the same tool, the same face grammar and the same four `state:` values as the board you are reading, which makes the two look like one kind of thing. They are opposites, and confusing them produces a specific error: applying the graduation rule and expecting a gated S page to empty into the manuscript. It does not. The page IS the manuscript.


Since 260726 this board is also the paper's FACE, not a file you may optionally open: `/haipipe-paper enter` builds it and hands over its URL, so the human is looking at `⑧` before any work starts (`QA4`). That raises the cost of a stale render from an inconvenience to a defect, and it is why every stage run now ends by rebuilding.

The approach is one page per independently gated unit, with state read off the pages rather than stored anywhere else. What we want is a board whose frontier can always be derived and can therefore never disagree with itself, which is exactly what a hand-written pointer to the current stage failed to give us.
Scope: This page covers What a paper board holds, how its state is derived, and why nothing graduates out of it. Neighbouring pages cover The design board is the opposite object and is `QA3`; what else is in the paper folder is `QA6`; the grain that decides how many S pages a stage gets is `QC3b`; who creates one is `QA8`.

## Diagram
```
   ⑧ PAPER BOARD    Paper-X/0-lifecycle/          explicit execution pipeline

   S-Seed 0,1        why this paper can exist, and where it sits
        ↓
   S-Work 0,1        the resources and the defensible claims
        ↓
   S-Venue 0..3      outlet · pitch · narrative · the decision register
        ↓
   S-Display 1..N    one page per figure or table, each gating alone
        ↓
     ┌──┴───────────────────────┐
     ▼                          ▼
   S-Main 1..9             S-Appendix 0,A..F
     └──────────┬───────────────┘
                ▼
   S-Submission 0..3   reconcile · compile · review · submit
                       the four VERBS, stable and reused every round
        ↓
   S-Round 1..N        ONE page per round (JL 260726), each carrying that
                       round's discussion, decisions, applied work and gate.
                       An external review REOPENS the affected Work, Display,
                       Main or Appendix pages, and the round page records
                       what came back and what was done about it.

   ── this is EXECUTION, not the Delivery index order ─────────────
      Delivery reads Opening → Work; this graph keeps the lifecycle's
      explicit dependencies. Board adjacency never creates an edge.

   ── the frontier is READ, never stored ──────────────────────────
      the earliest page above whose gate has not passed, taken from
      the pages' own state: lines. A hand-written "current stage"
      pointer was tried and began disagreeing with the gate record,
      so no second pointer or STATUS.md exists.

   ── nothing graduates ───────────────────────────────────────────
      ② a ruling closes and its Law LEAVES for the skill
      ⑧ a gate passes and the Content STAYS, because it is the paper
```

## Content
### A control plane, not a record
Each S face is one concrete, checkable unit of one paper's lifecycle. Its `## Content` is the thing that unit exists to produce: the seed, the claim ledger, the visual argument, the reader-facing section. Its `## Items to Finish` is that unit's queue. Its `state:` is where the unit actually is.

Eight named families organize ownership: Seed, Work, Venue, Display, Main, Appendix, Submission, Round. Family order makes the index scannable; the pipeline records the real execution edges.

### The eighth family: Round
(JL 260726)

A submission round used to live in `⑦` as `1-rounds/vYYMMDD/{README,discussion,decisions,todo,applied}.md`. It moves here, as one S page per round, `0-lifecycle/7-round/S-Round-<n>-<vYYMMDD>.md`.

The reason is not tidiness. That folder duplicated four mechanisms this board already owns, and one of them was actively dangerous.
```
 todo.md          QA9 already rules that ## Items to Finish IS the queue
 decisions.md     S-Venue-3 is already the decision register
 discussion.md    the board has ## Discussion and anchored comments
 applied.md       that is what a passed gate records
 latest.md        A STORED POINTER TO THE CURRENT ROUND
```
`latest.md` is the disease this page's own Law names: the frontier is read, never stored. It would have begun disagreeing with the pages exactly the way `STATUS.md`'s `current_layer` did.

One page per round, not four. `S-Submission 0..3` stay as the four stable verbs, reconcile, compile, review and submit; the round page is where that round's actual history lives and where its gate is. The alternative, four pages per round, was considered and rejected: it would have dissolved `S-Submission` and cost four pages per round for a distinction, "round 2's compile gates separately from round 1's", that nobody has needed.

The received artifacts follow the page (JL 260726). Reviewer letters, decision letters and the submitted PDF sit beside `S-Round-<n>-<vYYMMDD>.md` in `0-lifecycle/7-round/`, and `1-rounds/` is retired as a top-level container entirely. One round, one place. This differs from Display: its S pages and rebuild workspace live under `0-lifecycle/3-display/`, while only the journal-facing `float.tex` and selected `assets/` project to unnumbered `displays/<unit>/`.

### `state:` here means the gate
On a paper board `✅` means a human passed the gate, not that a question was answered. This is the single most important difference from `QA3`, where the same glyph means a ruling was made. Only a human may pass a CHECK gate; an unattended worker may prepare it and may not write the approval.

### The frontier is derived
The frontier is the earliest page in explicit pipeline order whose gate has not passed, read from the pages' own `state:` lines. No face or sidecar holds it, because a hand-written pointer to the current stage is exactly what started disagreeing with the gate record. `STATUS.md` is retired.

### Nothing graduates
A design board empties as its rulings leave. A paper board never empties. When an S page passes its gate it keeps everything: the Content is the paper, the gate record is the provenance, and the queue is the history of how it got there.

Delete `②` and the skill still runs. Delete `⑧` and the paper loses its frontier, its queue and its state, and the manuscript in `⑦` becomes a folder of files nobody can say anything true about.

### What crosses this folder's edge
```
 ① ──▶ ⑧  the skill set     IN. The stage runner reads one contract from ①,
                            works one S page here, and dispatches a bounded
                            worker that returns to this same page. Creating a
                            page is create-page.py in ① calling haipipe-board's
                            stage.py: Board owns the filename and face grammar,
                            Paper owns the Content jobs.

 ⑧ ──▶ ⑦  the paper         OUT, by generation only. An S page's ## Content IS
                            the section; sections/*.tex is produced FROM it.
                            One direction, always: md to tex, never back.

 ⑧ ──▶ the wall             OUT, through the page. A Q-consumer block on an S
                            page becomes an entry in ⑦'s 1-probes/, and the
                            landed answer comes back to the sentence that owes
                            it. The page is where a question is raised and
                            where its answer is woven in.

 ⑧ ──▶ ②                    NOTHING. This board never writes to a design board,
                            and a design board's rulings reach it only after
                            they have graduated into ① and a worker follows them.
```
Every edge here runs through a page. That is the whole design: there is no path by which work reaches the paper without a page recording that it happened, which is what makes the frontier readable and the history real.

## Items to Finish
- [x] 🏛 One S page per independently gated unit
      Display and Section have many pages because their units gate separately; single-artifact stages have one.
- [x] 🧭 The frontier is derived, not stored
      Read off the explicit pipeline from the pages' own `state:` lines; no `STATUS.md` or other current-stage pointer exists.
- [x] 🚦 `✅` on a paper board means a human gate passed
      Not that a question was answered. Only a human may write it.
- [x] 🔁 Rounds live on the board, one page per round
      `1-rounds/`'s record half duplicated the queue, the register, the discussion layer and a passed gate, and its `latest.md` was a stored frontier pointer. One S page per round, not four (JL 260726).
- [ ] 🛠 Build the Round family
      `0-lifecycle/7-round/`, the `S-Round` family in the Board's family list, and `haipipe-paper-round`'s rewrite: it still OWNS a five-file `1-rounds/` contract with a `latest.md`, so a worker following it today would recreate exactly what this ruling removed.
- [ ] 📐 Say what stays in `⑦`
      Reviewer letters, decision letters and the submitted PDF sit beside the round page in `0-lifecycle/7-round/`. `1-rounds/` is retired. `haipipe-paper-folder` no longer scaffolds it.
- [ ] 📐 State the difference where a worker reads it
      This page and `QA3` state it. A stage worker reads `stage.md`, which says nothing about which kind of board it is writing into.
- [ ] 🧪 Cold-read one paper board
      Give a fresh agent `0-lifecycle/` alone and check it can name the frontier and the next action without being told.

## Where we are
Ruled, live, and as of 260726 also EXERCISED. The MISQ paper carries 40 S faces across the eight families, and the derive-from-disk frontier was run end to end against them for the first time: every stage predicate resolves, and the frontier lands on `S-Seed-0-seed.md` 🟡 (REVISE complete, awaiting human CHECK), which is correct. The board itself builds all 40 pages; the only two `.md` files it excludes are `_`-prefixed non-S files, so nothing on that board is invisible.

That run also found the one predicate that did NOT resolve, and it was a defect introduced the same day rather than an old one: the venue pin had been specified as a `venue:` frontmatter key the board's grammar cannot parse. Corrected to read the venue page's `state:` line, where the pin already was. See `QA4`.

This board is now also the paper's FACE rather than a file that may be opened: `/haipipe-paper enter` builds it and hands over its URL, which is why a stale render became a defect and every stage run ends by rebuilding.

The rule is not written anywhere a stage worker looks. Both statements of it, this page and `QA3`, sit on a design board that runtime is forbidden to read, which is the gap the open item names.


One S page per independently gated unit is the claim this page rests on, and one of the eight families does not follow it. Display has eleven S pages on the MISQ paper while its stage contract still says `runs: once`, and the ruling that would reconcile them is `QC3b`'s open "Migrate display to per-unit". So the grain is ruled in general and unruled for Display specifically.

The md-to-tex edge stated above has the same problem one level down: `QC3d`'s "Rule what sync reads" is open, so the direction is ruled and the mechanism is not.

Reopened to 🟡 on 260726 (JL).
## Files
- `0-lifecycle/board.md`
  A live paper board's index, carrying the derived-frontier ruling in its Topic.
- `0-lifecycle/2-venue/S-Venue-3-decisions.md`
  The register that holds rulings outliving the stage that raised them.
- `haipipe-board/SKILL.md`
  The S-family grammar this board follows.

## Law
A paper board is a control plane, not a record. Each S face is one independently gated unit; its Content is the thing that unit produces, and that Content is the paper.

`✅` means a human passed the gate. Only a human may write it.

The frontier is READ, as the earliest page in the explicit dependency graph whose gate has not passed, and is never stored in a second place. The Delivery index is a reading order, not an implicit execution graph.

Nothing graduates out of a paper board. Where a design board empties as its rulings leave, a gated S page keeps everything it has.

A round is a gated unit and therefore a page: one `S-Round` page per round, carrying that round's discussion, decisions, applied work and gate. `S-Submission`'s four verbs stay stable and are reused. No file outside this board records which round is current.

## Log
260726 · The frontier stopped being a claim and became a measurement: run against the MISQ paper's 40 S pages, every predicate resolves and the frontier derives correctly. The one failure was a `venue:` frontmatter key ruled into existence the same morning that the board's grammar cannot parse; the pin was already on the venue page's `state:` line. Also on this day the board became the paper's face rather than an optional file, so a stale render is now a defect (`QA4`).

260726 · Rounds moved inside the lifecycle (JL). `1-rounds/` is retired as a top-level container: the round page and its received artifacts both live in `0-lifecycle/7-round/`. One page per round, not four. `haipipe-paper-folder` now scaffolds three containers, not four; `haipipe-paper-round` still owns a superseded five-file contract and needs a rewrite.
