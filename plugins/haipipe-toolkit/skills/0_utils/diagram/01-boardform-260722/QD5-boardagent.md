# Board-level agent
state: 🔴 OPEN
owner: CC
method: widen the live layer's scope from "one question" to "the whole board"; settle the session rules before building

## Question
Chat and terminal are both pinned to **one question** today (`QD1`/`QD2`/`QD3`). But much of the work is **board-wide**: adding a question, editing `## Roster`, regrouping, batch-rewriting every question's `## Question` into the new structure. How does that kind of work get done on the board?

- Why it is hard
  The moment the scope widens to the whole board, `QD1`'s LAW (**one session per question · one window per session**) stops sufficing: a board-level agent touches many questions' files at once and collides with any open single-question session.
- What breaks if we leave it
  "Tidy up the question list"-type work can only be typed back in the CLI; the board cannot host it — the board stays a read-only display page, not a workbench.
- What it affects downstream
  serve.py's session / HOLD machinery, where the entry point sits on the page, and how much power it gets (may it delete questions? edit a question someone is editing?).

## Boundary
- ✅ Covered here
  The agent whose **scope is the whole board**: adding Qs, editing the Roster, regrouping, cross-question batch rewrites; its entry point, session rules, permission boundary.
- ↪ Covered elsewhere
  Chat / terminal pinned to a single question — that is `QD2` (SDK drawer) and `QD3` (real terminal). Nor what the front page **looks like** — that is `QC2`; this question only owns "who gets to change it".

## Diagram
```
today (QD1/2/3)                      what this question adds
┌──────────────┐                   ┌──────────────────────────────┐
│ QA4 ─ session│ one per question   │ whole board ─ one board session│
│ QD3 ─ session│ each independent   │   may touch: board.md · any Q.md│
└──────────────┘                   │   must solve: collisions with   │
   one window per session (LAW)     │   open single-question sessions │
                                    └──────────────────────────────┘
                                        ↑ how does HOLD widen? with a board
                                          session open, can a question open?
```

## Items to Finish
- [ ] Settle how it meshes with `QD1`'s LAW
      With a board-level session open, can a single question's chat/terminal still open? Who yields? The item that matters most.
- [ ] Settle scope and permissions
      May edit `board.md` and every `Q*.md`; may it **create** questions, **delete** questions, edit a question currently open in someone's session?
- [ ] Settle the entry point
      A button on the front page? Or CLI-only? (Overlaps with `QC2`'s front-page design — do not build separately.)
- [ ] Claude Code, Codex, or both
      `QD2` runs claude_agent_sdk, `QD3` the real CLI. Which stack does the board-level route take, and what gets reused?
- [ ] Built and verified on one real job
      Acceptance: have it batch-rewrite one group's `## Question` sections into the new structure with a human only reviewing.

## Where we are
**Only "one session per question" exists; board level does not exist at all.**

- What works today
  Open the SDK drawer (`QD2`) or the real terminal (`QD3`) on a single question, scoped to that question's files; the session id lives in that question's `session:` header line.
- What cannot be done today
  Cross-question work: adding a question, editing the Roster, regrouping, batch rewrites. All of it goes back to hand-typed CLI.
- Parts that already exist and can be reused
  serve.py's OAuth + SDK + HOLD machinery, `/_board/term`'s ttyd reverse proxy, `/_board/chat`'s streaming and permission callback — the board-level route does not start from zero.

## Files
- `serve.py`
  Sessions / HOLD / chat / terminal all live here. The board-level route either reuses or extends this machinery.
- `build.py`
  If the entry button goes on the front page, it renders here (overlaps `QC2`).
- `board.md`
  What a board-level agent mostly edits is its `## Roster`.

## Log
260724 1242 · Translated to English (JL 260724: everything on the board in English)
260723 · Opened: "board-level agent" moved from `QC2` into the QD group — its machinery is the same stock as `QD1`/`QD2`/`QD3` (serve.py + sessions + windows), only the scope widens to the whole board; it collides head-on with `QD1`'s LAW, so they must sit side by side
