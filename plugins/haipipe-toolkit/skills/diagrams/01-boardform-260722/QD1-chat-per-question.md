# A chat session per question
state: 🟡 PARTIAL
owner: JL
method: settle the levels, the read/write permissions, and where conversations go; implementation split to QD2 / QD3
session: e4ac2dc0-af0d-46cc-972c-c19582f2ba62

## Question
Give every Q on the board its own conversation, but first the thing itself must be spelled out: what does the board level own vs. the question level?
How far can a question-level session read and write?
Where does the conversation itself live?

The hard part is that one conversation per question forces an answer to whether the same session can be open in two windows at once: get it wrong and, mildly, they overwrite each other, or badly, Claude Code forks a second history on its own.
This is the one question on this board that **changes how we work**, because until it is settled the loop stays "you comment on the page → I read it elsewhere → I edit the md", always one relay in between.
It is also the shared foundation of `QD2` (drawer) and `QD3` (terminal): change that LAW and both follow.

## Boundary
- ✅ Covered here
  **The rules**: board level vs. question level, one session per question, one window per session, where the session id is stored.
- ↪ Covered elsewhere
  The implementations: the web drawer is `QD2`, the real terminal is `QD3`; both also open on the whole board through the index page's chatbot (recorded on `QD2`).

## Diagram
```
  board level (this very conversation — the "session for top")
  ┌────────────────────────────────────────────────────┐
  │ open/close questions · edit build.py, serve.py · cross-question decisions │
  └───────────────┬────────────────────────────────────┘
                  │  one session per question (id in that question's session: line)
      ┌───────────┼───────────┐
      ▼           ▼           ▼
  ┌────────┐  ┌────────┐  ┌────────┐
  │ QA6    │  │ QD3    │  │ QB1    │  ← question level, one session each
  └────────┘  └────────┘  └────────┘
   two front ends, one session:
     💬 drawer (QD2)   permissions like the CLI: read freely, writes to its own
                       question pass, anything else / Bash → prompts you
     ⌨ terminal (QD3)  fully unrestricted — a real Claude Code

  why this board is a natural fit: one file per question — the context boundary
  and the session boundary already coincide.
```

## Items to Finish
- [x] Spell out what board level and question level each own
      Board level = this "session for top" conversation: open/close questions, edit build.py and serve.py, cross-question decisions.
      Question level = a Q's own session: works only on that question.
      Written into ## Law.
- [x] Settle question-level read/write permissions
      **JL ruled: same as the Claude Code CLI, ask when asking is due.** No longer my hard-coded "may only edit this one file".
      Read anything; writes to this question's own file pass; writes elsewhere / running Bash → a permission prompt (allow once / always / deny).
      The terminal (QD3) is fully unrestricted.
      Details in ## Where we are.
- [x] Settle where the conversation itself goes
      The conversation IS the session, and it **stays**: it lands in `~/.claude/projects/<encoded cwd>/<sid>.jsonl`, resumable from both drawer and terminal.
      The board's md keeps only outcomes (`## Where we are` / `## Log`), never transcripts.
- [ ] Write down what happens when two agents edit the same file
      The LAW already blocks "drawer + terminal on the same question" (HOLD).
      Not yet blocked: this board-level conversation and some question's drawer touching the same file at the same time, that rule is unwritten. **The only reason this question is still 🟡.**
- [x] Pick the implementation routes
      Both: QD2 (web drawer) for daily use, QD3 (real terminal) as the escape hatch.
      Both are built.

## Where we are
All three framework questions are answered; the last one (two agents, one file) remains.

- The levels
      Exactly one board-level conversation: this one, JL's "session for top".
      It owns the global moves: opening/closing questions, editing the generator and the server, cross-question decisions.
      One question-level session per Q, scoped to that Q.
- Read/write permissions (JL ruled mid-way)
      QD2 originally hard-coded "question level may only edit its own Q file".
      JL said "give normal permissions, like the CLI", so now: read-only tools pass automatically; writes to this question's own file pass; writes elsewhere or Bash → the page pops an "allow once / always allow / deny" prompt, the CLI dialog in spirit.
      The terminal route was never restricted.
- Where conversations go
      Never a keep-or-not choice: the conversation IS the session, already landing as jsonl under `~/.claude/projects/`, resumable from drawer or terminal at any time.
      The board's md records outcomes only.
      The "board grows unbounded" worry is thereby solved at the question level: per-question back-and-forth never enters this top conversation; each stays in its own jsonl.
- The single open item
      No rule yet for the board-level conversation and a question's drawer editing the same file simultaneously.
      Fine in practice (collisions are rare), but it must be written down to count.

## Files
- `serve.py`
  `HOLD` / `RUNS` / `TERMS`: "one window per session" is enforced by these tables.
- Each question's `.md` header
  The `session:` line is where that question's session id lives.

## Law
One session per question; sessions open at the SPACE root; N questions may run N terminals at once.
(JL 260723)

- Sessions open at the SPACE root, not the board folder
      The `claude` inside drawer (QD2) and terminal (QD3) has the whole repo (the SPACE) as cwd, not the board folder.
      Why: a question's session constantly touches the code it discusses; the board folder alone is too narrow.
      Sessions therefore archive under the repo root's project dir (`~/.claude/projects/-Users-…-Physician-SPACE/`).
      Write permissions stay narrow (the restricted tier edits only this question's files), but **the reading horizon is the whole repo**.
- A question-level session is primed the moment it opens (JL 260723)
      Drawer or terminal, the opening injects a `prime_context` block: which board, which question, what it asks, how many comments are open, where the file is.
      Drawer via system_prompt, terminal via `--append-system-prompt`.
      Costs no turn, runs nothing on its own; the session knows its place the moment it opens.
- One Q ⇄ one session
      The session id lives in the question file's `session:` header line, one per question.
      Whether that session was first opened in the web drawer or in the terminal, both point at the same id: the terminal generates a uuid on first open (`claude --session-id`) and writes it back to the header; no second unrecorded session appears.
- One session, one window at a time
      Drawer and terminal read and write the same on-disk `.jsonl`.
      The same question must not have both open, or they overwrite each other or fork a second history.
      The server enforces this with HOLD.
- Terminal identity = hash of the Q file path (globally unique across boards)
      Not a port, not a name like "QD3".
      Two boards' QD3s have different paths → different keys → naturally separate.
      Underneath: one unix socket per question, no port pool.
- Different questions, each on its own
      QA6's terminal and QD3's terminal are two different sessions; open them simultaneously at will.
      N questions = N terminals = N sessions, mutually independent.
      To watch several, open more board tabs.

## Lesson
**A session started by the SDK is a real Claude Code session.**
`claude_agent_sdk` drives the `claude` CLI underneath; records land in the same place as any session: `~/.claude/projects/<encoded cwd>/<session-id>.jsonl` (cwd is now the SPACE root). **Corollary**: the drawer (QD2) and the terminal (QD3) are not two routes; they are **two front ends of one session**.
This is what spares QD3 from reinventing session management; it is just another window onto the same conversation.

**Sessions bind to the cwd; changing the cwd swaps the whole session set.**
The project dir name is encoded from the cwd: one cwd, one dir.
After the cwd moved from the board folder to the SPACE root, old sessions stayed in the old project dir; `--resume <old sid>` from root cannot find them; even copying the jsonl into the new dir does not fool resume (tested, rejected).
So the cwd change restarted every question's session under root.

**Ask "which machine does it run on" before picking a design.**
The browser is on JL's laptop; `claude` is on the server.
Whatever the route, the machine actually running Claude is the server side; the page is only a window.

## Glossary
board level / question level: a conversation's scope.
Board level runs the whole board (opening questions, editing the generator, cross-question decisions); question level runs one Q. headless session: a Claude session started by a program, with no terminal UI.

## Discussion
> JL: how do I attach a chatbot so that opening it is really opening Claude Code, and it takes this page as input and context? With the choice of opening it or not.
> JL: for example, after I comment, I open haichat and it reads my content, updates the markdown and html, and so on.
> JL: our current claude session is the "session for top", right? Then how do we open a terminal for each question?
> JL: could we make a new Q for chat, one for terminal version, and then other one for the claude_agent_sdk version.
>> CC0723: split. This question keeps only the three unanswered framework items (levels and boundaries); the SDK version goes to QD2, the terminal version to QD3.

## Comments
- [x] JL “open claude in the SPACE dir, not in the board; same to QD1 and QD2” · 260723 1430
      >> CC0723: made board-level LAW: the claude inside drawer and terminal opens at the SPACE root (reading horizon = the whole repo,
      write permissions stay narrow). QD2/QD3 updated together. Side effect: changing cwd reset the sessions; every question restarted under root, see Lesson.
- [x] JL “QD1 A chat session per question How do you want to update this as well?” · 260723 1655
      >> CC0723: the three framework questions had in fact been answered along the way: permissions ruled by JL as "like the CLI", conversations stay in the jsonl,
      the levels written into Law. All ticked; only "two agents, one file" remains, the sole reason this stays 🟡.

## Log
260724 1242 · Translated to English (JL 260724: everything on the board in English)
260723 · Rewritten to the new structure: Question expanded into "one paragraph + bullets", added `## Boundary` and `## Files`; the retired `## Why here` merged into Question
260723 1745 · Law gains: question-level sessions are primed on open (prime_context, one flavor each for drawer/terminal), see QD2/QD3
260723 1730 · JL ruled: claude opens at the SPACE root (not the board folder), written into ## Law, QD2/QD3 updated together.
              The session's reading horizon became the whole repo; changing cwd reset sessions (old ones stayed put), added to Lesson
260723 1655 · Updated to actual progress: three framework questions answered (permissions CLI-style per JL / conversations stay in jsonl / levels in Law);
              only "two agents, one file" open; Diagram and Now rewritten; the voided ↗ removed from Law
260723 1445 · JL ruled: split into three. This question keeps the framework; implementations go to QD2 (SDK) and QD3 (terminal)
260723 1215 · JL raised "hang a chat on every Q", the QD group and this question opened
