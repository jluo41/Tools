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
  one scope · one CURRENT session · one live window          ← the Law, 260731 wording

  🌐 board level — scope = the whole board (this very conversation, the "session for top")
  ┌──────────────────────────────────────────────────────────────────────┐
  │ open/close questions · edit build.py, serve.py · cross-question calls │
  └───────────────┬──────────────────────────────────────────────────────┘
  🗂 group level — scope = one group FOLDER, may edit any .md inside it
  ┌──────────────────────────────────────────────────────────────────────┐
  │ 💬 on every group heading · primed with the group's pages and states  │
  └───────────────┬──────────────────────────────────────────────────────┘
                  │  one CURRENT session per scope (a page's id in its session: line)
      ┌───────────┼───────────┐
      ▼           ▼           ▼
  ┌────────┐  ┌────────┐  ┌────────┐
  │ QA6    │  │ QD3    │  │ QC1    │  ← 📄 page level, scope = this one file
  └────────┘  └────────┘  └────────┘
   the history behind each: every id ever minted lives in .haipipe-board/sessions.json,
   named <page-id>-<purpose>, and the 🗂 picker resumes any of them (the header follows)

   two front ends, one session:
     💬 drawer (QD2)   permissions like the CLI: read freely, writes to its own
                       question pass, anything else / Bash → prompts you
     ⌨ terminal (QD3)  fully unrestricted — a real Claude Code

  why this board is a natural fit: one file per question — the context boundary
  and the session boundary already coincide.
```

/_excalidraw/?board=Tools/plugins/haipipe-toolkit/skills/diagrams/01-boardform-260722/board.excalidraw&frame=QD1

## Items to Finish
### ⚖️ The framework questions
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

### 🔒 The two-agents-one-file rule
- [ ] Write down what happens when two agents edit the same file
      The LAW already blocks "drawer + terminal on the same scope" (HOLD).
      Not yet blocked: this board-level conversation and some question's drawer touching the same file at the same time, that rule is unwritten. **The only reason this question is still 🟡.**
      The group altitude (0.77.0) made the overlap ordinary rather than rare: a `QC-engine/` session and a `QC3` page session may both edit `QC3-*.md`, and HOLD does not see the collision because the two scopes hash to different keys.
      So the missing rule is now about NESTED scopes, not just the board one; `QE4` holds the per-file lock design it would lean on.

### 🛠 The implementation routes
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

- 260731 JL+CC · ⚖️ The Law was rewritten, because all three of its terms had moved
  JL, reading the old three-beat quoted on `QD3m`'s Diagram ("one question · one session · one jsonl"), ruled: "this law should be updated. It is actually very old."
  It was: **question** stopped being the unit the day group and board sessions shipped, **one session** was amended by JL's own picker ruling, and **one jsonl** followed from that amendment, since a scope now has a history of them.
  What survived the audit is the window rule, so the new three-beat keeps it: **one scope · one CURRENT session · one live window**.
  Rewritten in place: the summary line and its attribution, a new "three altitudes" bullet, a new names bullet, and the stale "One Q ⇄ one session" bullet retired into "Both front ends point at the same current id" (the ONE-id claim is gone, the no-unrecorded-session claim survives through the sidecar).
  The remaining bullets were generalized from question to scope, parking was written into the window rule, and the Diagram grew the two upper altitudes.
  Nothing built this round: this is the written law catching up with what shipped between 0.62.0 and 0.77.0.

- 260731 JL · 🪜 The levels became three, and the split site made them reachable
  JL: "我觉得我们的 chat 也分几类：board chat / group chat / page"; the answer is that all three already existed, and only the split site could not reach them.
  Board and page were live; the group level was already built server-side (`group_folder`, `group_prime_context`, the session keyed to the group's own folder) and simply had no door.
  In the one-file board the drawer learned which page it was on from `location.hash`, which is meaningless once QC9 gives every page its own file, so every page opened the BOARD session.
  The document now answers instead: exactly one `section.q` means that page, an `h1` in the `QA · Design` grammar means that group, neither means the board.
  Verified across all five surfaces: index → BOARD, QA.html → QA group, QA0/QD2 page files → their own page, and the old monolith unchanged.
  A second bug sat behind it and would have blocked every write the moment binding was fixed: `target()` derived the board folder as the URL's parent, so a POST from `board/QD/QD2-….html` was refused with "no board.md here"; it now walks up to the board folder, bounded by `--root`.

- 260731 JL · 🏷 Sessions gained names: <page-id>-<what-it-is-for>
  JL: "for each session, we can give them the name? like Qxxx-what-is-this-for? ... and this should be shown as well."
  Built the same round (0.74.0, cut as 0.72.0 and renumbered when two sessions collided on the ledger): the sidecar registry's entries became {id, name}; a name can be given at birth (the picker's ＋ New session asks "what is this session for?") or later (✎ on any row, POST /_board/session-name); the page-id prefix is derived server-side, so the stored purpose is bare and the display reads QD3m-fix-black-screen.
  Shown wherever the session appears: the picker rows (bold, monospace), the strip summary; unnamed history keeps the first-message-title fallback.
  The name lives in .haipipe-board/sessions.json, not the page header, honoring this page's "the board's md records outcomes only".

- 260731 JL · 🗂 The levels gained a third altitude: the page GROUP
  JL: "for each Question group, we can also add the chat icon for them, and then we can add the sdk or cli to discuss about this Question group."
  Built as 0.77.0 (cut as 0.73.0, renumbered on the same ledger collision): every group heading on the index carries 💬; it opens the same drawer attached to the GROUP, whose identity is the group FOLDER (QC-engine/), so sessions, names, HOLD, parking, and the picker all reuse the page machinery unchanged.
  The scope sits between the two existing levels: a group session may edit any .md inside its folder (the board session has the whole board, a page session has its one file), and its prime lists the group's pages with their states.
  Group sessions have no header line to live in, so current = the registry's newest entry, which keeps this page's "the board's md records outcomes only" intact; names prefix with the group letter (QC-group-chat-smoke).
  Verified live: a scoped SDK turn on QC, the picker listing it named, and the ⌨ terminal resuming the drawer's own session.

### Decision Now
These are the calls only JL can make; CC ticks nothing here.

- [x] ⚖️ Amend the Law's "One Q ⇄ one session" for the history picker (JL 260731, on `QD3m`)
      DECIDED 260731 by JL: "somehow we want to update this law, that one Q, multiple session. the chat session with the predefined prompt related to this Q".
      That is option A with the prime kept: one CURRENT session per question, older ones resumable through the picker, and EVERY session opens primed with this Q's context.
      HOLD and one-window-at-a-time stay untouched; the Law section below carries the amendment.
      BUILT the same day as haipipe-board 0.62.0: the 🗂 Session strip in the drawer, `/_board/sessions`, and the `session:` parameter on chat and terminal.
- [ ] 🗄 Rule whether the board folder keeps a copy of the session jsonls (JL 260731: "maybe still in the home, but we can make the copy of them in the board folder?")
      The LIVE file cannot move: resume is bound to the cwd's project dir under `~/.claude/projects/`, and the 260723 migration test showed a relocated jsonl refuses `--resume` (Lesson below); any board-folder copy is therefore a backup or a readable export, never the live session.
      A · the LIVE file stays only in home, matching current behavior; no backup copy is made in the board folder.
      B · a jsonl mirror is written to the board folder on release and stays gitignored, providing cheap insurance that can be restored by copying back into the project dir.
      C · once the P2 mirror's jsonl parser exists, a readable markdown transcript is exported when a session retires, providing a human-readable archive.
      D · both B and C are staged together, B now for backup insurance and C once the mirror infrastructure is ready.
      → CC's proposal: D, staged: B now (cheap insurance, one copy at release time) and C once the P2 mirror's jsonl parser exists anyway; both stay gitignored, because transcripts can carry secrets and this repo is distributed.

## Files
- `serve.py`
  `HOLD` / `RUNS` / `TERMS`: "one window per session" is enforced by these tables.
- Each question's `.md` header
  The `session:` line is where that question's session id lives.

## Law
**one scope · one CURRENT session · one live window**, replacing the 260723 three-beat "one question · one session · one jsonl", whose every term has since moved.
A SCOPE owns sessions, and there are three altitudes of it: the board, a group folder, a page; each holds one CURRENT session plus a resumable history in the 🗂 picker.
Every session opens primed with its scope's context, carries a name, runs one window at a time (HOLD), and opens at the SPACE root; N scopes may run N terminals at once.
(JL 260723; amended by JL 260731 twice, "one Q, multiple session. the chat session with the predefined prompt related to this Q" and "for each Question group, we can also add the chat icon for them"; retired by JL 260731, "this law should be updated. It is actually very old")

- Three altitudes, one rule (JL 260731, built 0.77.0)
      Board level runs the whole board, group level one group FOLDER (`QC-engine/`), page level one page file.
      A scope's IDENTITY is that path, which is why the group altitude cost almost nothing: `term_key`, HOLD, parking, the sidecar registry, names, and the picker all took it unchanged.
      Write scope narrows with altitude: the board's session has every file, a group's session any `.md` inside its folder, a page's session its own file.
      A group has no header line to hold an id, so its current session is the registry's newest entry; the board's md still records outcomes only.
- One scope, multiple sessions, one current (JL 260731)
      A page's `session:` header keeps exactly one id, the CURRENT one, which drawer and terminal open by default.
      Every id ever minted for the scope is recorded in the serve.py sidecar (`.haipipe-board/sessions.json` at the SPACE root); the picker lists them and can resume any that landed on disk.
      Resuming an older session makes it the current one, and the header follows.
      One window at a time still holds per scope (HOLD), because two front ends on the same jsonl still fork histories.
- Sessions carry names: `<page-id>-<what-it-is-for>` (JL 260731, built 0.74.0)
      A name is given at birth (the picker's ＋ New session asks) or later (✎ on any row); the prefix is derived server-side, so the stored purpose is bare and the display reads `QD3m-fix-black-screen`.
      Names live in the registry, never in the page header, for the same reason the ids do.
- Both front ends point at the same current id
      Drawer (`QD2`) and terminal (`QD3`) are two windows on one session, not two routes: the terminal mints a uuid on first open (`claude --session-id`) and writes it back to the header, and the drawer resumes that same id.
      What the 260731 amendment removed is only the claim that a question ever has ONE id; what it kept is that no session appears UNRECORDED, because minting now goes through the sidecar.

- Sessions open at the SPACE root, not the board folder
      The `claude` inside drawer (QD2) and terminal (QD3) has the whole repo (the SPACE) as cwd, not the board folder.
      Why: a question's session constantly touches the code it discusses; the board folder alone is too narrow.
      Sessions therefore archive under the repo root's project dir (`~/.claude/projects/-Users-…-Physician-SPACE/`).
      Write permissions stay narrow (the restricted tier edits only this question's files), but **the reading horizon is the whole repo**.
- A session is primed the moment it opens (JL 260723)
      Drawer or terminal, the opening injects a `prime_context` block: which board, which scope, what it asks, how many comments are open, where the file is.
      A group's flavor (`group_prime_context`) lists the group's pages and their states instead.
      Drawer via system_prompt, terminal via `--append-system-prompt`.
      Costs no turn, runs nothing on its own; the session knows its place the moment it opens.
- One session, one window at a time
      Drawer and terminal read and write the same on-disk `.jsonl`.
      The same scope must not have both open, or they overwrite each other or fork a second history.
      The server enforces this with HOLD; PARKING (0.73.0) is the one relaxation, releasing the window and the HOLD while keeping the process alive for a 600s grace, so a reattach gets the same pid with its screen replayed.
- Terminal identity = hash of the scope's path (globally unique across boards)
      Not a port, not a name like "QD3": the page's file path, or the group's folder path.
      Two boards' QD3s have different paths → different keys → naturally separate.
- Different scopes, each on its own
      QA6's terminal and QD3's terminal are two different sessions; open them simultaneously at will.
      N scopes = N terminals = N sessions, mutually independent.
      To watch several, open more board tabs.

## Lesson
#### A session started by the SDK is a real Claude Code session.
`claude_agent_sdk` drives the `claude` CLI underneath; records land in the same place as any session: `~/.claude/projects/<encoded cwd>/<session-id>.jsonl` (cwd is now the SPACE root). **Corollary**: the drawer (QD2) and the terminal (QD3) are not two routes; they are **two front ends of one session**.
This is what spares QD3 from reinventing session management; it is just another window onto the same conversation.

#### Sessions bind to the cwd; changing the cwd swaps the whole session set.
The project dir name is encoded from the cwd: one cwd, one dir.
After the cwd moved from the board folder to the SPACE root, old sessions stayed in the old project dir; `--resume <old sid>` from root cannot find them; even copying the jsonl into the new dir does not fool resume (tested, rejected).
So the cwd change restarted every question's session under root.

#### Ask "which machine does it run on" before picking a design.
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

## Log
260731 1905 · The one-live-window rule held only for chat on the tree: navigating with ⌨ on left the old scope's PTY live AND unparked while a new one opened (two windows, one of them invisible), and a group release parked the wrong scope. Fixed in `follow()` (0.86.0, recorded on `QD3`); the law itself needed no change — the code had simply stopped enforcing it on the split site
260731 · Items, Where we are, and Files regrouped to the QB4d/QB4e/QB4f subsection conventions (matrix retrofit)
260731 · JL: "this law should be updated. It is actually very old"; the Law rewritten to **one scope · one CURRENT session · one live window**; three-altitudes and names bullets added, "One Q ⇄ one session" retired, remaining bullets generalized question → scope, parking written into the window rule, Diagram and Boundary follow; two renumbered version refs (0.72.0→0.74.0, 0.73.0→0.77.0) corrected on the way
260724 1242 · Translated to English (JL 260724: everything on the board in English)
260723 · Rewritten to the new structure: Question expanded into "one paragraph + bullets", added `## Boundary` and `## Files`; the retired `## Why here` merged into Question
260723 1745 · Law gains: question-level sessions are primed on open (prime_context, one flavor each for drawer/terminal), see QD2/QD3
260723 1730 · JL ruled: claude opens at the SPACE root (not the board folder), written into ## Law, QD2/QD3 updated together.
              The session's reading horizon became the whole repo; changing cwd reset sessions (old ones stayed put), added to Lesson
260723 1655 · Updated to actual progress: three framework questions answered (permissions CLI-style per JL / conversations stay in jsonl / levels in Law);
              only "two agents, one file" open; Diagram and Now rewritten; the voided ↗ removed from Law
260723 1445 · JL ruled: split into three. This question keeps the framework; implementations go to QD2 (SDK) and QD3 (terminal)
260723 1215 · JL raised "hang a chat on every Q", the QD group and this question opened
