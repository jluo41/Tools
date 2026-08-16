# Board-level agent
state: 🗄️ ARCHIVED · 260801, JL: "你把那个 Q board 的 agent 给删掉，我们不再需要了" — the premise expired rather than the work being done. This page was opened when chat and terminal were pinned to ONE question, so board-wide work had nowhere to live; `QD1` has since settled that a chat attaches at three levels and board chat and group chat both ship, which answers the need this page existed to raise. The open session/HOLD-widening and how-much-power decisions retire with it. File stays readable in _archive, never deleted.
owner: CC
method: widen the live layer's scope from "one question" to "the whole board"; settle the session rules before building

## Question
Chat and terminal are both pinned to **one question** today (`QD1`/`QD2`/`QD3`). But much of the work is **board-wide**: adding a question, editing `## Roster`, regrouping, batch-rewriting every question's `## Question` into the new structure. How does that kind of work get done on the board?

- Why it is hard
  The moment the scope widens to the whole board, `QD1`'s LAW (**one session per question · one window per session**) stops sufficing: a board-level agent touches many questions' files at once and collides with any open single-question session.
- What breaks if we leave it
  "Tidy up the question list"-type work can only be typed back in the CLI; the board cannot host it, and it stays a read-only display page, not a workbench.
- What it affects downstream
  serve.py's session / HOLD machinery, where the entry point sits on the page, and how much power it gets (may it delete questions? edit a question someone is editing?).


## Boundary
- ✅ Covered here
  The agent whose **scope is the whole board**: adding Qs, editing the Roster, regrouping, cross-question batch rewrites; its entry point, session rules, permission boundary.
- ↪ Covered elsewhere
  Chat / terminal pinned to a single question: that is `QD2` (SDK drawer) and `QD3` (real terminal). Nor what the front page **looks like**, which is `QB2`; this question only owns "who gets to change it".

## Diagram
```
today (QD1/2/3)                      what this question adds
┌──────────────┐                   ┌──────────────────────────────┐
│ QD2 ─ session│ one per question  │ whole board ─ one board session│
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
      A button on the front page? Or CLI-only? (Overlaps with `QB2`'s front-page design; do not build separately.)
- [ ] Claude Code, Codex, or both
      `QD2` is the SDK chat version and runs claude_agent_sdk, `QD3` is the TUI chat version and runs the real CLI. Which stack does the board-level route take, and what gets reused?
- [ ] Built and verified on one real job
      Acceptance: have it batch-rewrite one group's `## Question` sections into the new structure with a human only reviewing.

## Where we are
**Only "one session per question" exists; board level does not exist at all.**

- What works today
  Open the SDK drawer (`QD2`) or the real terminal (`QD3`) on a single question, scoped to that question's files; the session id lives in that question's `session:` header line.
- What cannot be done today
  Cross-question work: adding a question, editing the Roster, regrouping, batch rewrites. All of it goes back to hand-typed CLI.
- Parts that already exist and can be reused
  serve.py's OAuth + SDK + HOLD machinery, `/_board/term`'s ttyd reverse proxy, `/_board/chat`'s streaming and permission callback: the board-level route does not start from zero.

### Decision Now
These are the calls only JL can make; CC ticks nothing here.

- [ ] ⚖️ Rule how a board-level session meshes with `QD1`'s LAW
      With a board-level session open, can a single question's chat or terminal still open, and who yields?
      A tick here also closes the same row in Items to Finish.
- [ ] 🔑 Rule the board session's scope and permissions
      May it create questions, delete questions, or edit a question currently open in someone's session?
      A tick here also closes the same row in Items to Finish.
- [ ] 🚪 Rule the entry point
      A · a button on the front page opens the board-level agent; the entry point is built on the page itself, overlapping with QB2's front-page design, requiring coordination with that question.
      B · the board-level agent is CLI-only; users must open the terminal manually to run board-wide work, no page button is added.
      A tick here also closes the same row in Items to Finish.
- [ ] 🧰 Rule which stack the board-level route takes
      A · Claude Code (claude_agent_sdk) is the stack; the board-level route reuses QD2's drawer infrastructure, OAuth, and HOLD machinery for the board scope.
      B · Codex is the stack; the board-level route uses a different agent infrastructure than the existing question-level routes.
      C · both stacks are used; claude_agent_sdk for the SDK chat version (QD2-style) and the real CLI for the TUI chat version (QD3-style) are both available for board-level work.
      A tick here also closes the same row in Items to Finish.

## Files
- `serve.py`
  Sessions / HOLD / chat / terminal all live here. The board-level route either reuses or extends this machinery.
- `build.py`
  If the entry button goes on the front page, it renders here (overlaps `QB2`).
- `board.md`
  What a board-level agent mostly edits is its `## Roster`.

## Log
260801 · Restored to QD; the QD5 merge reverted — the board-level agent is a chat/session concern (same stock as QD1/2/3), and QD5 (the drawing-attach page) moved to QB, so gluing the two was wrong
260731 · Items, Where we are, and Files regrouped to the QB4d/QB4e/QB4f subsection conventions (matrix retrofit)
260731 · Restored from _archive into QDa · Working (JL: board-agent work is working-layer work); ids repointed to the QDa naming
260725 1036 · Archived from the index page (moved to _archive/)
260724 1242 · Translated to English (JL 260724: everything on the board in English)
260723 · Opened: "board-level agent" moved from `QB2` into the QD group, because its machinery is the same stock as `QD1`/`QD2`/`QD3` (serve.py + sessions + windows), only the scope widens to the whole board; it collides head-on with `QD1`'s LAW, so they must sit side by side
