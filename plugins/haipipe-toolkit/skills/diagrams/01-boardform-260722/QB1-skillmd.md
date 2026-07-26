# What SKILL.md must say
state: 🟡 PARTIAL
owner: CC
method: SKILL.md stays as short as possible; details live in the ref/ files

## Question
Someone else, or a future me without this conversation's memory, types `/haipipe-board`.
What should they follow?
What exactly does SKILL.md say, and what does it leave to `ref/`?

It is hard because SKILL.md enters the context on every invocation, so shorter is better, yet too short and nothing is explained, and the cut line needs a rule, not a feel.
Leave it unwritten and the whole workflow lives only in this conversation: a different agent walking in sees a `build.py` and a few boards, cannot guess the moves, and what was built here would be gone next time.
It reaches downstream because SKILL.md is the skill's entry point and the only export channel for "rules the board has settled" (the graduation mechanism).

## Boundary
- ✅ Covered here
  **What goes into SKILL.md**: which actions, how long, what belongs in the body vs. in `ref/`, and how it stays in sync with the board (graduation).
- ↪ Covered elsewhere
  How to **verify it suffices** once written: that is `QB2` (fresh-agent cold read).

## Diagram

```
user types  /haipipe-board
          │
          ▼
      SKILL.md  ~280 lines (260725): operations only, details never inlined
          ├─ the shape: what a board looks like (Q + S pages, group intros, embeds)
          ├─ nine actions: view · open · add · build · sync · link · close   (offline)
          │                serve · comment                                    (live)
          ├─ the sections of one Q/S page (the source side of QA4's contract)
          ├─ three writing rules (no invented terms / purge stale lines / fresh-agent cold read)
          ├─ the four prohibitions
          └─ board ↔ SKILL.md: the graduation mechanism
                │
                ▼  go to ref/ only when detail is needed
        ref/q-template.md     copy to add a Q or S page (mirrors QA4 since 0.15.1)
        ref/board-form.md     full spec: numbering · section↔page · syntax table · embeds §5 · order §8
        ref/writing-rules.md  how to write plainly + cold-read prompt + convergence criterion
        ref/board-example.md  a minimal two-question example
```

http://127.0.0.1:5599/_excalidraw/?board=Tools/plugins/haipipe-toolkit/skills/diagrams/01-boardform-260722/fig/board.excalidraw&frame=QB1

## Items to Finish
- [x] SKILL.md written
      Shape · actions (view/open/add/build/sync/link/close + serve/comment) · the sections of one Q/S page · writing rules · prohibitions · ref/ index.
- [x] Answers "how to open a new board"
      The open section, five steps, including the single place that must stop and ask the user (the Q list needs a nod).
- [x] Answers "how to add a Q to a board"
      Copy `ref/q-template.md` → rename → into the Pages → regenerate.
- [x] Answers "when does a board close"
      Every question at ✅ or ⏸️; `close:` is the closing condition and must be verifiable.
- [x] Settles how SKILL.md stays in sync with the board
      The **graduation mechanism** (see ## Law): when a Q reaches ✅, its `## Law` is copied into SKILL.md; unsettled ones never enter.
      Written into SKILL.md as the "board ↔ SKILL.md" section.
      This rule is itself one of the things SKILL.md must state.
- [ ] The live layer (serve/chat/terminal) written as rules
      SKILL.md currently holds only pointers (provisional, aimed at the QD group), because QD1/QD2/QD3 are still 🟡.
      When they reach ✅, graduate them in one by one.
- [x] A fresh agent can open a decent board from it alone
      QB2 ran (260723, GPU-cluster topic): a fresh agent, given only SKILL.md + ref/, opened a valid 5-question board on the first try, verdict YES.
      The single real gap it exposed (how to invoke build.py) is fixed into SKILL.md.
      Re-run 260725 against the shared Q/S skill (4 Q + 1 S), verdict YES again; see the next item for what it cost.
- [x] 📝 The manual describes S pages on the writing side, not only the reading side
      Until 260725 SKILL.md explained how an S page RENDERS but never how to create one: `open` asked "有哪几个 Q", step 4 named files `Q<letter><n>` only, `close` used the words "human-gated / explicitly parked" as if they were states, and nothing said how an S is listed in `## Pages`.
      QB2's re-run had to guess all of it (and guessed right, which is worse: the documents took credit for the agent's judgment).
      Fixed in the same pass: `open` steps 1 and 4 now ask for Q **and** S pages and give both filename shapes plus S's required `## Content`; `close` and the Page section state that both kinds share the same four `state:` values, with ✅ meaning "checkboxes closed" on Q and "human gate passed" on S; `ref/board-form.md` §2 gained the S state mapping and the Pages rule (bare filename, free-text group heading), §3's example gained an S line; `ref/q-template.md`'s consumer record no longer assumes a paper's `1-probes/` tree.
      The build section also names the interpreter split (build/watch on any `python3`, `serve.py` on the venv for the SDK).


## Where we are
**Written, validated by QB2, and kept current through the 0.15.x series; the live layer stays pointer-only until the QD group settles.**

- `SKILL.md`, ~280 lines as of 260725
  Operations only: the shape (Q + S pages, group intros, embeds), nine actions (view / open / add / build / sync / link / close offline, serve / comment live), the sections of one Q/S page, three writing rules, four prohibitions, the graduation mechanism, a ref/ index.
  Spec and prose details never inlined; it enters the context on every invocation, shorter is better.
- `ref/`, four files
  `q-template.md`: the shared Q/S source template; mirrors QA4's rendered contract (0.15.1).
  `board-form.md`, the full spec: folder, numbering, section↔page mapping, syntax table, embeds (§5), on-stage order (§8), Comments format, the invariant.
  `writing-rules.md`: hard writing rules + the zero-background review prompt, convergence criterion, and past scores.
  `board-example.md`: a minimal two-question example; predates the Q/S merge (no S page, no Content section) and its prose is still Chinese, so the template, not it, is the authority on shape.
- `CHANGELOG.md`, one entry per body of work, version matching SKILL.md's `version:` line
  Grown from 0.2.0 alongside the board: the Q/S page merge (0.13.0), the Opening and Diagram rulings (0.13.x-0.14.0), the index chatbot (0.15.0), and the QA2 template alignment (0.15.1) are all recorded there.
  Its early self-correction stands: the invariant is "strip every script and every page plus all body text remains", asserted on every build.

- 260725 CC · 📝 The S-page instructions caught up with the S-page renderer
  QB2's re-run exposed that every S instruction in the manual was about reading a stage, not writing one, so a newcomer had to invent the Pages listing, the state value, the filename, and the probe pointer.
  All four are now written down (`open` steps 1/4, `close`, the Page section, `ref/board-form.md` §2/§3, `ref/q-template.md`).
  The lesson is general: **the reading contract graduated on its own and left the authoring contract behind**, which is invisible to anyone who already knows both.

Still open: the live layer (serve/chat/terminal) graduates in only when the QD questions settle.


## Files
- `SKILL.md`
  The deliverable itself.
- `ref/board-form.md` · `ref/writing-rules.md` · `ref/q-template.md` · `ref/board-example.md`
  Where the details go; SKILL.md stays minimal because these four catch everything.
- `CHANGELOG.md`
  Version and change record, aligned with SKILL.md's `version:`.

## Law
- Graduation: SKILL.md = the crystallization of the board's settled questions
  This board (`diagram/01-boardform-260722/`) is the full design record; SKILL.md keeps only the conclusions of `✅ SETTLED` questions.
  When a Q reaches ✅, copy its `## Law` rules into SKILL.md's matching spot. **Unsettled questions (🟡/🔴) never enter the manual**, otherwise ad-hoc choices get written as iron law (QD1's permission rule was hard-coded and overturned exactly that way).
  So SKILL.md always equals the sum of settled rules; before editing it, check whether that question is ✅.
- SKILL.md stays minimal
  Operations only; spec, syntax, and prose details all go to `ref/`.
  It enters the context on every invocation.
- The live layer gets pointers, not rules, for now
  serve.py's comment write-back graduated with QA6 ✅; chat/terminal (the QD group) are still 🟡, so SKILL.md carries only pointers.

## Glossary
`SKILL.md`: the entry file of a Claude Code skill.
When the user types `/haipipe-board`, this is what gets read in. graduation: once a Q settles (✅), moving its settled rules from the board into SKILL.md, where they become instructions people follow.

## Discussion

## Log
260725 1215 · S pages written into the manual's authoring side after QB2's re-run found four gaps (open steps 1/4 · close + Page state values · board-form §2/§3 Pages and state mapping · q-template probe pointer · the python3-vs-venv split); 0.16.0
260725 1140 · Stale numbers purged in the QB alignment pass (JL's go): "128 lines / five actions / CHANGELOG up to 0.2.0" replaced with the 0.15.x reality (~280 lines, nine actions, Q/S page wording); ref/ descriptions updated, board-example.md's pre-merge shape noted
260724 1242 · Translated to English (JL 260724: everything on the board in English); purged the stale "written but not yet verified" lead: QB2 passed on 260723
260723 · Rewritten to the new structure: Question expanded into "one paragraph + bullets", added `## Boundary` and `## Files`; the retired `## Why here` merged into Question
260723 1720 · QB2 acceptance passed → ticked "a fresh agent can open a board"; SKILL.md gains: invoke build.py with its path + slug/default-state/owner conventions
260723 1700 · Graduation mechanism settled (Q ✅ → Law copied into SKILL.md), written into ## Law and SKILL.md's "board ↔ SKILL.md" section;
              graduated the three already-✅ questions along the way: fixed the stale "Sync" wording in the comment section (QA6: Save writes the disk),
              introduced the serve.py action, live layer as provisional pointers only; version 0.2.0 → 0.3.0
260723 1210 · Added the sync and link actions; board↔artifact coupling had never been written down
260723 1210 · board.md gains ## Links; paths in body text become clickable links
260723 1150 · SKILL.md finished (128 lines) + the four ref/ files; CHANGELOG at 0.2.0
260723 1150 · ref/board-example.md replaced (old format); ref/q-template.md gains ## Comments
260723 0919 · Renumbered Q4 → QB1; title compressed; finish line into a checklist
260722 2255 · Opened
260722 2249 · Skill folder moved from skills/board/ to skills/0_utils/haipipe-board/
