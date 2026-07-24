# What SKILL.md must say
state: 🟡 PARTIAL
owner: CC
method: SKILL.md stays as short as possible; details live in the ref/ files

## Question
Someone else — or a future me without this conversation's memory — types `/haipipe-board`. What should they follow? What exactly does SKILL.md say, and what does it leave to `ref/`?

- Why it is hard
  It enters the context on every invocation, so shorter is better; but too short and nothing is explained. The cut line needs a rule, not a feel.
- What breaks if we leave it
  Today this whole workflow lives only in this conversation. A different agent walking in sees a `build.py` and a few boards and cannot guess the moves — what was built here would be gone next time.
- What it affects downstream
  It is the skill's entry point, and the only export channel for "rules the board has settled" (the graduation mechanism).

## Boundary
- ✅ This question owns
  **What goes into SKILL.md**: which actions, how long, what belongs in the body vs. in `ref/`, and how it stays in sync with the board (graduation).
- ❌ This question does not own
  How to **verify it suffices** once written — that is `QB2` (fresh-agent cold read).

## Diagram
```
user types  /haipipe-board
          │
          ▼
      SKILL.md  128 lines — operations only, details never inlined
          ├─ the shape: what a board looks like
          ├─ five actions: open · add · build · comment · close
          ├─ the sections of one Q file
          ├─ three writing rules (no invented terms / purge stale lines / fresh-agent cold read)
          └─ the four prohibitions
                │
                ▼  go to ref/ only when detail is needed
        ref/q-template.md     copy to add a question
        ref/board-form.md     full spec: numbering · section↔page · syntax table · Comments format
        ref/writing-rules.md  how to write plainly + cold-read prompt + convergence criterion
        ref/board-example.md  a minimal two-question example
```

## Items to Finish
- [x] SKILL.md written
      Shape · actions (open/add/build/sync/link/close + serve/comment) · Q-file sections · writing rules · prohibitions · ref/ index.
- [x] Answers "how to open a new board"
      The open section, five steps, including the single place that must stop and ask the user (the Q list needs a nod).
- [x] Answers "how to add a Q to a board"
      Copy `ref/q-template.md` → rename → into the Roster → regenerate.
- [x] Answers "when does a board close"
      Every question at ✅ or ⏸️; `close:` is the closing condition and must be verifiable.
- [x] Settles how SKILL.md stays in sync with the board
      The **graduation mechanism** (see ## Law): when a Q reaches ✅, its `## Law` is copied into SKILL.md; unsettled ones never enter.
      Written into SKILL.md as the "board ↔ SKILL.md" section. This rule is itself one of the things SKILL.md must state.
- [ ] The live layer (serve/chat/terminal) written as rules
      SKILL.md currently holds only pointers (provisional, aimed at the QD group), because QD1/QD2/QD3 are still 🟡.
      When they reach ✅, graduate them in one by one.
- [x] A fresh agent can open a decent board from it alone
      QB2 ran (260723, GPU-cluster topic): a fresh agent, given only SKILL.md + ref/, opened a valid 5-question board on the first try, verdict YES.
      The single real gap it exposed (how to invoke build.py) is fixed into SKILL.md.


## Where we are
**Written, and validated by QB2; the live layer stays pointer-only until the QD group settles.**

- `SKILL.md`, 128 lines
  Operations only: the shape, seven actions (open / add / build / comment / sync / link / close),
  the sections of one Q file, three writing rules, four prohibitions, a ref/ index.
  Spec and prose details never inlined — it enters the context on every invocation, shorter is better.
- `ref/`, four files
  `q-template.md` — copy to add a question (now includes `## Comments`).
  `board-form.md` — the full spec: folder, numbering, section↔page mapping, syntax table, Comments format, the invariant.
  `writing-rules.md` — hard writing rules + the zero-background review prompt, convergence criterion, and past scores.
  `board-example.md` — replaced; the old one still used the pre-0.1 single-file `[BOARD]`/`[Qn]` format and would mislead.
- `CHANGELOG.md` up to 0.2.0
  Including one self-correction: 0.1.0 claimed "zero `<script>` in the output", which stopped being true the moment the comment layer landed —
  and was never the property worth keeping anyway. Restated as "strip every script and every question plus all body text remains", asserted on every build.

Still open: the live layer (serve/chat/terminal) graduates in only when the QD questions settle.


## Files
- `SKILL.md`
  The deliverable itself.
- `ref/board-form.md` · `ref/writing-rules.md` · `ref/q-template.md` · `ref/board-example.md`
  Where the details go — SKILL.md stays minimal because these four catch everything.
- `CHANGELOG.md`
  Version and change record, aligned with SKILL.md's `version:`.

## Law
- Graduation: SKILL.md = the crystallization of the board's settled questions
  This board (`diagram/01-boardform-260722/`) is the full design record; SKILL.md keeps only the conclusions of `✅ SETTLED` questions.
  When a Q reaches ✅, copy its `## Law` rules into SKILL.md's matching spot. **Unsettled questions (🟡/🔴) never enter the manual** —
  otherwise ad-hoc choices get written as iron law (QD1's permission rule was hard-coded and overturned exactly that way).
  So SKILL.md always equals the sum of settled rules; before editing it, check whether that question is ✅.
- SKILL.md stays minimal
  Operations only; spec, syntax, and prose details all go to `ref/`. It enters the context on every invocation.
- The live layer gets pointers, not rules, for now
  serve.py's comment write-back graduated with QA6 ✅; chat/terminal (the QD group) are still 🟡, so SKILL.md carries only pointers.

## Glossary
`SKILL.md`: the entry file of a Claude Code skill. When the user types `/haipipe-board`, this is what gets read in.
graduation: once a Q settles (✅), moving its settled rules from the board into SKILL.md, where they become instructions people follow.

## Discussion

## Log
260724 1242 · Translated to English (JL 260724: everything on the board in English); purged the stale "written but not yet verified" lead — QB2 passed on 260723
260723 · Rewritten to the new structure: Question expanded into "one paragraph + bullets", added `## Boundary` and `## Files`; the retired `## Why here` merged into Question
260723 1720 · QB2 acceptance passed → ticked "a fresh agent can open a board"; SKILL.md gains: invoke build.py with its path + slug/default-state/owner conventions
260723 1700 · Graduation mechanism settled (Q ✅ → Law copied into SKILL.md), written into ## Law and SKILL.md's "board ↔ SKILL.md" section;
              graduated the three already-✅ questions along the way: fixed the stale "Sync" wording in the comment section (QA6: Save writes the disk),
              introduced the serve.py action, live layer as provisional pointers only; version 0.2.0 → 0.3.0
260723 1210 · Added the sync and link actions — board↔artifact coupling had never been written down
260723 1210 · board.md gains ## Links; paths in body text become clickable links
260723 1150 · SKILL.md finished (128 lines) + the four ref/ files; CHANGELOG at 0.2.0
260723 1150 · ref/board-example.md replaced (old format); ref/q-template.md gains ## Comments
260723 0919 · Renumbered Q4 → QB1; title compressed; finish line into a checklist
260722 2255 · Opened
260722 2249 · Skill folder moved from skills/board/ to skills/0_utils/haipipe-board/
