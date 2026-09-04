## 0.23.1 · 2026-09-04

- Use the canonical Page dependency order.
- Make copilot-versus-auto gate behavior explicit: auto records human acts as
  owed and may follow declared policy, but deferral never becomes approval.
- Separate phase `route` from `next_cycle` in OUTLINE receipts.

## 0.23.0 · 2026-09-04

- Require the frozen `haipipe-page-context` PREPARE record before SHAPE or
  SURVEY and present it through the shared Outline plugin's Context Workspace.
- Remove PageX Bindings from the active SURVEY graph. Cross-Folder evidence
  now arrives through Supporting Run Results; governed page-local static
  sources may be named in Local Input.
- Route an approved, fully folded plan to `haipipe-page-content` instead of the
  retired DRAFT/REVISE phase split.
- Keep the typed Evidence Item names, separate Supporting and Local Runs, and
  Paper-local `pjNNtNNrNN` reservation introduced by the preceding design.

## 0.22.3 · 2026-09-03

- Require the main Page and Outline plan card to use the same four-cycle status
  strip and keep Shape-versus-Content conformance out of the planning UI.

## 0.22.2 · 2026-09-03

- Require Evidence Workspace to distinguish explanatory Evidences from Run
  cards grouped under the Evidence contracts they support.

## 0.22.1 · 2026-09-03

- Require Run details to separate Purpose/Plan, path-derived Availability,
  and Next action.
- Keep unallocated Page-local Run plans in the Evidence Item's Expected,
  Acceptance, and Local Input fields until LAND creates `runs/` and `results/`.

## 0.22.0 · 2026-09-03

- Give every proposed Paper-local Evidence Item Run its own `pjNNtNNrNN`
  identity during SURVEY, displayed as `P jNN.tNN.rNN`; keep `new` explicit
  until LAND creates the Ticket.
- Keep Evidence wall labels (`E<n><V/C/D>.<Label>`) separate from Run identity.

## 0.21.0 · 2026-09-03

- Read the ranked Skills Page Record from its canonical Outline-owned path,
  `outline/skill/<stem>.md`.

## 0.20.0 · 2026-09-03

- Define the addressed Bullet as the primary plan-evidence-draft unit shared by
  Bullet Workspace and Evidence Workspace.
- Include Skills with Files and Log under Page Records while keeping its one
  ranked store at the sibling `skill/<stem>.md` path.

## 0.19.0 · 2026-09-03

- Define the Outline UI as Bullet Workspace + Evidence Workspace, with Plan
  Context and Page Records as subordinate groups rather than peer plugins.
- Keep the compact Outline Table on the main Page and all detailed records in
  the single `outline/` authority.

## 0.18.4 — 2026-09-03

- Require Local Run plans to use the same complete `new-*` hierarchy as
  Supporting routes; retire the free-text dash placeholder.

## 0.18.3 — 2026-09-03

- Replace the remaining “registered graph” shorthand with the inventory-only
  SURVEY contract and report existing versus planned routes separately.

## 0.18.2 — 2026-09-03

- Define the complete `new-run` / `new-task` / `new-job` / `new-block`
  hierarchy and separate a never-attempted registered Ticket from a rerun.

## 0.18.1 — 2026-09-03

- Define dotted `bNN.jNN.tNN.rNN` labels as presentation aliases of canonical
  compact Run identities, with no `rNN` invented for planned parents.

## 0.18.0 — 2026-09-03

- Make the Outline plugin the one review surface for Shape, Evidence Items,
  supporting-run lineage, and routed feedback.
- Write generated lineage to `outline/evidence/supporting-runs/`; the main Page
  remains a compact read-only projection of this authority.

## 0.17.3 — 2026-09-03

- Require one joined Evidence Items panel after SURVEY: canonical compact item
  identity, grouped Run items, and collapsed Run/Result paths.

## 0.17.2 — 2026-09-02

- Make SHAPE author a stable 1–12 character `Label` for every new or updated
  Evidence Item so Outline chips remain concise without replacing immutable ids.

## 0.16.0 — 2026-09-02

- Extend each SURVEY Evidence Item graph with zero-to-many exact PageX source
  bindings. PageX authorities are named in the item's one frozen Local Input;
  they are sources, never Supporting Runs, local Runs, or Result types.
- Keep SHAPE and SURVEY planning-only: they specify item identity, expected
  ready evidence, acceptance, source graph, and actions without allocating or
  executing a Level-4 Run.

## 0.15.0 — 2026-09-01

- **Human review packet**: when a person asks to review, check, read, or
  approve an outline, the phase now presents four linked parts before seeking
  a decision: current Shape and arc; material typed Evidence Items and their
  surveyed sources; routed feedback/requirements/open threads that shaped the
  plan; and the exact human decision still needed.  The packet reports records
  on disk, does not write prose, and never infers `approved:` or `Decide:`.

## 0.14.0 — 2026-09-01

- SHAPE now names typed `E<NN>-VALUE|CITE|DISPLAY-<slug>` items and specifies
  Target, Need, Expected, and Acceptance. SURVEY remains planning-only and
  adds 0..N Execution/Discovery Supporting Runs plus exactly one local Page
  Evidence Item Run. The ledger is `<stem>-evidence-items.md`; `found`,
  `person`, and `none` retire as actions.

## 0.13.0 — 2026-09-01

- Owns the OUTLINE part's two human-gated cycles: SHAPE (brief → propose →
  react → revise, `approved:`) and SURVEY (the item table: one row per mark,
  Need · Route · Run = found | rerun | new-run | new-task | new-job |
  new-block | person | none with its tasks/ address, a person's Decide).
  The tick at SHAPE carries the fork (fresh marks → SURVEY, every row folded
  → the DRAFT part). The circled phase numbers retire.

## 0.12.0 — 2026-08-31

Rewritten as ONE pass: 535 → 199 lines, present tense. ⓪ Boot (load this
brief, the type's `outline:` block, `ref/plan-grammar.md`, the page, `outline/`;
nothing else) · ① Prepare, one command: `haipipe-board/cli/outline-pass.py
<page>.md` regenerates the three derived files, runs the plan checks for this
page (hard), the page-scoped checker and the build, and prints the receipt-lite
· ② Plan (the type gives the words, the pass gives the arc; a Section page
plans sentence slots) · ③ Threads and the log record · ④ Five checks, with
④ SHAPE now judging heads (4 to 11 words), Notes (≤ 30 words) and a Note that
quotes the page · 🧑 the tick, with the chat-transcription rule · 🔀 · 🧾.
- Fixed: the authority test said the Aims live "in the plan file" while
  `haipipe-page` 0.42.0 put them on the page; the exit and the routing said
  "four checks" while the brief said five.
- Stated: a pass in a person's own session is a pass (same trace as the
  agent's); the ten-box checklist is now the six mechanical boxes inside
  `outline-pass.py` plus the four the pass writes.
- **Field-tested the same day** (cold desk, SM01 OUTLINE pass: plan v3 at 0 ❌,
  10 min, 229k tokens, 15 frictions, 1 of 7 pre-registered gaps hit). Patched
  from it: the type's `outline:` block is frontmatter the Skill tool strips
  (read the first 20 lines); read the page once with the Read tool; run
  `outline-pass.py` twice (before to read, after to measure) and write the log
  record after the second run, `--no-build` named; the by-hand list now matches
  the script; one `## C<n>` per Content division (a flat Section is `C1`); the
  swap test and the heaviest-finding rule at paragraph level on a one-division
  page; the Narrative row's order binds over a Round's proposed order; ①
  COVERAGE counts a bare mark as owed before ② PROBE instead of failing.

## 0.11.3 — 2026-08-31

- **Head style rule in the checklist** (JL 260831): heads of 4 to 11 plain
  words, one-line Notes, no drafted sentence in the plan; points at
  `haipipe-plugin-outline` §✂️ for the approved SM00 v3 shape.

## 0.11.2 — 2026-08-31

- **⓪ REQUIRE** (JL: "add the fn for the haipipe-page-outline as well … so it
  can check what is the requirement of writing this page"): every pass opens
  by running `cli/requirement.py <page>.md` and READING the V (venue division),
  N (Narrative row, Writing Style) and B (board rules) records before a bullet
  is written; ④ SHAPE is judged against V and N. Receipt line `requirement:`.
- **§✅ Checklist** (JL: "it should have a checklist to check the items
  needed"): ten boxes, REQUIRE → COLLECT → TYPE → PLAN → CHECKS → EVIDENCE →
  THREADS → LOG → TAB → RECEIPT; receipt line `checklist: n/10`.
- The THREADS and LOG boxes carry haipipe-plugin-outline 0.18.0's record
  shape: open threads only, Ask/Options/We lean/Decide; settled threads are
  log records.
- `version:` in the frontmatter had stayed at 0.11.0 through 0.11.1; fixed.

## 0.11.1 — 2026-08-31

Patched from the NA01 field test (20 frictions on a 0.11.0 law one run old):
- **Five checks, not four**, everywhere the brief and the routing said four;
  the receipt gains an `arc:` line. ⓪ was added on 260822 and three sentences
  never followed.
- **`Routed:` keeps the mark on the last line**, stated where the fold is
  taught, with the measured loss (8 of 16 lines vanished from the render).
- **A declined row has a shape**: `declined: <RD> <id> · <reason>` in the
  plan's header, because no division but `## C<n>`/`## Aims` is legal.
- **A routed concern may mint an Aim** in an unapproved plan; 0.16.1's
  thread rule covers an ASK from the retired States fold, not a Round's row.
- `cli/feedback.py reopen` named; the collector's role stated as PULL.

## 0.11.0 — 2026-08-31

- **⓪ COLLECT**: the fold gains a second source. Every OUTLINE pass opens by
  projecting the Round rows routed to this page into `outline/<stem>-feedback.md` (one file, a section per Round; the per-Round folder lasted one hour)
  (JL 260831: a function of this phase, not a new plugin). ① COVERAGE gains
  one direction: an open register row is served by a bullet or declined with a
  reason. The bullet gains `Routed:` beside `Answered:`/`Drawn:`; the receipt
  gains `feedback: n routed · n served · n declined`. G7 runs
  `feedback-coverage` board-wide so a Round cannot close on a page nobody
  opened.

## 0.10.0 — 2026-08-22 — this phase takes the ARC, and self-consistency becomes FIVE checks

Ruled by JL while deciding where a story arc belongs when there are ten Page
Types: "我们也会有其他的 pages 所以这个 four types 就是我们提供什么样的 outline
template，然后 haipipe-page-outline 目的就是想要讲什么样的 story arcs."

- **New §🎭 · the TYPE gives the WORDS, this phase gives the ARGUMENT.** The type's
  `metadata.outline` block already said which words a page may use, in what order
  and how many of each — §📐 has read it since 260819. What no contract owned was
  which ARGUMENT those words are arranged to make.
- **Three rules move here from `haipipe-page-for-task` 0.7.0**, where they had been
  living since they were written: role-complete-is-not-arc-coherent, the three
  forbidden orderings (run · config · the order the AUTHOR found things out), and
  the per-boundary swap test. They are not task-shaped. Any page ordered by its
  author's history passes every mechanical check and fails its reader, and nine
  other types had no statement of the rule at all.
- **One rule is new, and it came from running the section before writing it.** ⛔ THE
  BIGGEST FINDING GETS A DIVISION, NOT A BULLET INSIDE SOMEONE ELSE'S. On
  `QC1-postrain-replication` the largest measured effect on the board — training
  cutting non-termination roughly tenfold, across two benchmarks and two
  measurement surfaces — was bullet `B7` inside a division named for the run that
  happened to produce it. That plan was coverage-complete, address-clean and
  value-checked, and no existing check could say it was mis-weighted.
- **Self-consistency goes from FOUR checks to FIVE, and ARC runs FIRST**, because a
  plan with the wrong arc is not worth address-checking. Its three tests: an `arc:`
  line stating the argument in one sentence (a table of contents fails it), every
  adjacent pair passing the swap test, and the heaviest finding owning a division.
- **⓪ and ④ are stated as different questions.** SHAPE asks whether the words are
  the type's; ARC asks whether their order is an argument. A plan can pass SHAPE
  with every word legal and fail ARC as a run log wearing correct prefixes.
- **What ⓪ deliberately does not do**: choose the words (a word outside the type's
  set is a SHAPE failure), or judge whether the plan aims at the right thing (that
  is the person's, at `approved:`). It is also the one check a machine can only
  half-run, and it is written as a check anyway, because a judgement with a written
  form is arguable and one with none is not.

## 0.9.0 — 2026-08-19

- **0.9.0 shipped in SKILL.md with no entry here.** Reconstructed from the
  frontmatter: Aims joined the authority test and now live in the plan file, and
  the version rule was stated as protecting a PROMISE and never a FORMAT — so an
  old-grammar plan is rewritten on its next pass rather than frozen, and
  `checks/outline.py` fails `bullet-missing-note`. Recorded 260822 in a
  version-vs-changelog sweep.

## 0.8.0 — 2026-08-20

- **The fold marks self-referential values `· recount`** (JL: "看看哪里可以去
  优化"): a value counting the run's own artifacts (receipts, findings, a
  pinned hash) drifts as phases append, so its `Answered:` line carries the
  mark and DRAFT re-reads only those cards (haipipe-page-draft §📖).
- **A head or Note states the PRESENT, never the past** (JL: "content 永远
  只包含最新的东西"): a renumber or reversal rewrites the bullet clean; the
  old state lives in `## Log` and receipts, never beside the new one.

## 0.7.0 — 2026-08-19

- **The version rule protects a PROMISE, never a FORMAT** (JL: "remove all
  the legacy-grammar, I don't want to maintain the old things"): an
  old-grammar plan is rewritten into the current grammar on its next OUTLINE
  pass — in place while unapproved, as `v<N+1>` when ticked. Found on
  `QC1-visitlbp`: a fold pass appended onto 260817 long-sentence bullets and
  every check stayed green, so `checks/outline.py` now FAILS
  `bullet-missing-note` on any bullet lacking its `Note:`/`Answered:`/`Drawn:`
  line, every plan, no legacy carve-out.
- **The Aims enter the authority test**: agreed at OUTLINE, living in the
  plan file with `Done when:` tests (haipipe-plugin-outline 0.14.0 owns the
  grammar); plus a pointer to the plugin's §✂️ bullet grammar, stated once
  there.

## 0.6.0 — 2026-08-19

- **有问有答: an answered ask is appended in place** — when a 📮 bullet's card
  lands its `## Values`, the same bullet gains the answer with each value id
  quoted inline; no new bullet, mark stays. Landing values obliges the next ①
  fold to write the append (`haipipe-page-evidence` 0.11.0 carries the
  producing side of the same rule).
- **The same night's extensions**: 🖼 bullets gain `Drawn: <claim>` once their
  unit is built, transcribed from the unit's README; and the tick's meaning is
  BREAK-not-bless — the person hunts for what is wrong, and the tick records
  that the hunt failed.
- **Coherence sweep (260819)**: §🔀 routes the four-pass plan through the
  🧑 LOOK before ② PROBE and ③ EVIDENCE run; §🕳's example heads are
  Capitalized per the plugin's §✂️ bullet style; §📦 counts five marks, not
  six (✅ retired).

## 0.5.0 — 2026-08-19

- **COVERAGE (§🚦 test ①) now runs BOTH directions of the plan⇄disk join**
  (JL, on seeing Display4 under "on disk, cited by no bullet": "you should try
  to make every display to be used", and when its README back-pointer was
  offered as the fix: "you should cite it"): every display unit on disk must
  be CITED BY A BULLET'S MARK — a `serves:` line inside the unit's README is
  not citing, because the plan's reader never sees it. A README may carry a
  `retired:` line to take the unit out of the plan deliberately.

## 0.4.0 — 2026-08-19

- **📮 probe and 🧮 value are now SEPARATE marks** (JL: "You mean you put the
  probe and values together? I want to separate them"). 📮 = this point needs
  a QUESTION answered — bare before ② raises the card, `📮 PP<NN>` after; the
  answer may be a finding or a folder of numbers. 🧮 = this point QUOTES one
  value, `PP<NN>.v<n>`, out of an answered card's `## Values` block, and
  `checks/values.py` re-computes it. 📮 deliberately shares phase ②'s glyph
  (same concept) and is end-anchored in the scanners so prose about the phase
  never reads as a mark.

## 0.3.1 — 2026-08-19

- **The value mark is 🧮** (JL: "🧮 maybe this one?" — he never liked 🔢).
  🔢 stays accepted as the legacy alias, so pre-260819 plans remain legal.
  The abacus was the proof mark retired earlier on 260819 and is revived with
  its new meaning: a recomputable number, which is what `checks/values.py`
  does to every one of them.

## 0.3.0 — 2026-08-19

- **OUTLINE is now the head of a PREPARE loop.** JL 260819: "outline 之后就直接
  probe 准备证据，基于证据我们再改 outline，直到 outline 自己是自洽的." OUTLINE →
  PROBE → EVIDENCE repeats, and only the plan's own gate lets DRAFT start.
- **Self-consistent is FOUR checkable things**: coverage, address, value, shape.
  All four run before the person is asked, so the human tick answers direction
  rather than arithmetic.
- **A tick belongs to the version it ticked.** Evidence that changes an approved
  plan makes a `v<N+1>`. On 260819 the tick stayed on `v2` through five more
  edits, and all three stale `serves:` addresses came from that.

## 0.2.0 — 2026-08-19

- **The Page Type's `outline:` block is now READ.** All eleven surviving types
  already declared a mode (`fixed` | `grammar` | `resolved`) under `metadata:`,
  and nothing in this phase looked at it, so a plan's shape was whatever its
  author felt like.
- OUTLINE now has TWO exits, and the machine one runs first: the plan's shape must
  match the declared mode, THEN a person ticks `approved:`. A plan that
  contradicts its own type wastes the one gate that is supposed to be cheap.
- `checks/outline.py` owes a `plan-shape-off-type` rule.
- No `page-type:` key stays the flexible default: base section order only, which
  is 247 of 274 pages.

## 0.1.2 — 2026-08-18

- Pointer added to `../haipipe-page-workflow/ref/phase-cards.md` §①, which
  states this phase and every sibling in the SAME six fields
  (`❓ ASKS · 📥 READS · 📤 WRITES · 🚪 EXITS · ✋ TICK · 🔀 ROUTES`). This
  contract still owns the reasoning; the card is the readable-across-phases
  summary, and the contract wins when they disagree.
- Board backlink retargeted: `QPw7`/`QPw8`/`QPw9` became `QPw00a`/`QPw00r`/
  `QPw00g` when JL ruled that pages which are not phases may not carry
  phase numbers.


## 0.1.1 — 2026-08-18

Added the Board page backlink: the page that argues this contract, created 260818 when JL ruled one page per workflow step.
haipipe-page-outline · Changelog
================================

Skill-scoped changelog (never loaded at invocation; read on demand). Versions
match SKILL.md frontmatter `version:`. Newest first.

## 0.1.0 — 2026-08-17

First contract. OUTLINE becomes phase ① of the page workflow (JL 260817:
"Outline 现在要成为这个 workflow 的一部分"), overturning
`haipipe-plugin-outline` 0.1.0, which had ruled in these words that *"the answer
to 'should there be an outline phase before DRAFT' is no."*

- The authority moves OUT of `haipipe-page-draft`, whose §🗂 had owned the
  outline. DRAFT keeps purpose, Aims and the page's own promise.
- The deliverable is `<page>/outline/<stem>-outline-v<N>.md`; its shape,
  addressing and marks stay in `haipipe-plugin-outline` and are not restated.
- The exit is a HUMAN GATE: a person ticks `approved:` on the 🧭 tab. No machine
  may write that tick.
- Before the tick the file is a working document: rewrite it, delete a wrong
  bullet, no version and no record. `v2` means the work MOVED ON, not that `v1`
  was wrong, which is why `v1` is kept rather than corrected.
- A named hole is the phase working: OUTLINE marks what a bullet owes and
  STOPS. Raising the card is PROBE's and landing it is EVIDENCE's.

**Why a phase and not a step**: one phase owning both "agree the shape" and
"write the page" let a single done-report cover both, and the plan was pasted
into the page's own `## Content`, where it went stale immediately
(`QC1-visitlbp`, CMSRegBoard, 260817). Changing a section list before the prose
costs one line; after the prose it costs the prose.
