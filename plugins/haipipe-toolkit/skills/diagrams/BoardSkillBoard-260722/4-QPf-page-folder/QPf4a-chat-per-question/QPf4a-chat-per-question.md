# Chat · a session per question
state: 🗂 FOLDED · into QPf4-chat §3 the session model (JL 260815) · the full record stays here
owner: JL
method: settle the levels, the read and write permissions, and where conversations are kept; the two builds split to QD2 / QD3
session: e4ac2dc0-af0d-46cc-972c-c19582f2ba62

## Opening
How should a board, a group, or a page get its own Claude Code conversation without two windows fighting over the same work?
A conversation that owns one scope keeps its context close to the work.
The problem is saying what it may change, and which of its sessions is the live one.
If two live windows share one session, the history can fork and two file edits can collide.
This page is done when every conversation has a clear scope, a history you can resume, and one safe live window.

**Covered elsewhere**: The two builds. The web chat panel is `QD2`, and the real terminal is `QD3`.
Both also open on the whole board, through the index page's chatbot (recorded on `QD2`).


## Diagram

```
  one scope · one CURRENT session · one live window          ← the Law, 260731 wording

  🌐 board level · scope = the whole board (this very conversation, the "session for top")
  ┌──────────────────────────────────────────────────────────────────────┐
  │ open/close questions · edit build.py, serve.py · cross-question calls │
  └───────────────┬──────────────────────────────────────────────────────┘
  🗂 group level · scope = one group FOLDER, may edit any .md inside it
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
     💬 panel (QD2)    permissions like the CLI: read freely, writes to its own
                       question pass, anything else / Bash → prompts you
     ⌨ terminal (QD3)  no limits at all, a real Claude Code

  why this board fits: one file per question, so the context boundary and the
  session boundary are already the same line.
```
📌 Every scope, from the whole board down to one page, gets one current session and one live window.


## Aims
### ⚖️ The framework questions
- [x] Say what board level and question level each own
      Board level is this "session for top" conversation. It opens and closes questions, edits build.py and serve.py, and makes the calls that cross questions.
      Question level is a Q's own session. It works on that question only.
      Written into ## Law.
- [x] Settle what a question-level session may read and write
      **JL ruled: same as the Claude Code CLI, ask when asking is due.** No more of my hard-coded "may only edit this one file".
      It reads anything. Writes to this question's own file go through. Writes anywhere else, or a Bash call, raise a permission prompt: allow once, always, or deny.
      The terminal (QD3) has no limits.
      Details in ## States.
- [x] Settle where the conversation itself is kept
      The conversation IS the session, and it **stays**.
      It lands in `~/.claude/projects/<encoded cwd>/<sid>.jsonl`, and both the panel and the terminal can resume it.
      The board's md keeps outcomes only (`## States` / `## Log`), never the talk itself.
- 📖 260816 · [REVISE-CC, JL ruled] the page was rewritten in plain words, for a reader with ADHD whose English is a second language (JL: "我他妈真的读不下去"). The 🧭 Outline tab had been showing this page's own sentences back, and they were unreadable, so the tab was right and the prose was not. Every division title now names its consequence instead of a mechanism, each one gained a `📌` line saying in one sentence what the part settles, and every aim, `Done when:` and State row was replaced with a short plain-word version. House words went with them, `division` to part, `store` to list, `render` to read or draw, `seed` to suggest, `mint` to build. Measured with `haipipe-writing`'s `cli/score.py`: 31 sentences flagged before, 3 after, every one that remains inside this Log, which is history and was not touched. No fact, id, `§` mark or section changed; only the words.

### 🔒 The two-agents-one-file rule
- [ ] Write down what happens when two agents edit the same file
      The LAW already blocks "panel plus terminal on the same scope" (HOLD).
      Not yet blocked: this board-level conversation and some question's panel touching the same file at the same time. That rule is unwritten. **The only reason this question is still 🟡.**
      The group level (0.77.0) made the overlap ordinary rather than rare.
      A `7-QC-engine/` session and a `QC3` page session may both edit `QC3-*.md`, and HOLD does not see the clash, because the two scopes hash to different keys.
      So the missing rule is now about NESTED scopes, not just the board one. `QE4` holds the per-file lock design it would lean on.

### 🛠 The two routes to build
- [x] Pick the routes to build
      Both: QD2 (web panel) for daily use, QD3 (real terminal) as the way out when the panel cannot do it.
      Both are built.

## States
All three framework questions are answered. The last one, two agents on one file, is still open.

- The levels
      Exactly one board-level conversation: this one, JL's "session for top".
      It owns the global moves: opening and closing questions, editing the generator and the server, and the calls that cross questions.
      One question-level session per Q, scoped to that Q.
- What a session may read and write (JL ruled mid-way)
      QD2 first hard-coded "question level may only edit its own Q file".
      JL said "give normal permissions, like the CLI".
      So now read-only tools pass on their own, and writes to this question's own file pass.
      Writes anywhere else, or a Bash call, pop an "allow once / always allow / deny" prompt, the CLI dialog in spirit.
      The terminal route was never limited.
- Where conversations are kept
      This was never a keep-or-not choice.
      The conversation IS the session, already landing as jsonl under `~/.claude/projects/`, resumable from the panel or the terminal at any time.
      The board's md records outcomes only.
      That also settles the "board grows without end" worry at the question level.
      The talk on one question never enters this top conversation, and each stays in its own jsonl.
- The single open item
      There is no rule yet for the board-level conversation and a question's panel editing the same file at the same time.
      It is fine in practice, since clashes are rare, but it has to be written down to count.

- 260731 JL+CC · ⚖️ The Law was rewritten, because all three of its terms had moved
  JL read the old three-beat quoted on `QD3m`'s Diagram, "one question · one session · one jsonl", and ruled: "this law should be updated. It is actually very old."
  He was right on all three terms.
  **question** stopped being the unit the day group and board sessions shipped, **one session** was amended by JL's own picker ruling, and **one jsonl** followed from that amendment, since a scope now has a history of them.
  What survived the check is the window rule, so the new three-beat keeps it: **one scope · one CURRENT session · one live window**.
  Rewritten in place: the summary line and who said it, a new "three levels" bullet, and a new names bullet.
  The stale "One Q ⇄ one session" bullet was retired into "Both front ends point at the same current id".
  The ONE-id claim is gone; the no-unrecorded-session claim survives through the sidecar.
  The other bullets were widened from question to scope, parking was written into the window rule, and the Diagram grew the two upper levels.
  Nothing was built this round.
  This is the written law catching up with what shipped between 0.62.0 and 0.77.0.

- 260731 JL · 🪜 The levels became three, and the split site made them reachable
  JL: "我觉得我们的 chat 也分几类：board chat / group chat / page".
  The answer is that all three already existed, and only the split site could not reach them.
  Board and page were live.
  The group level was already built on the server (`group_folder`, `group_prime_context`, the session keyed to the group's own folder), and it simply had no door.
  In the one-file board the panel learned which page it was on from `location.hash`.
  That means nothing once QC9 gives every page its own file, so every page opened the BOARD session.
  The document now answers instead: exactly one `section.q` means that page, an `h1` in the `QA · Design` grammar means that group, and neither means the board.
  Checked across all five views: index → BOARD, QA.html → QA group, QA0/QD2 page files → their own page, and the old monolith unchanged.
  A second bug sat behind it, and it would have blocked every write the moment binding was fixed.
  `target()` read the board folder as the URL's parent, so a POST from `board/QD/QD2-….html` was refused with "no board.md here".
  It now walks up to the board folder, bounded by `--root`.

- 260731 JL · 🏷 Sessions gained names: <page-id>-<what-it-is-for>
  JL: "for each session, we can give them the name? like Qxxx-what-is-this-for? ... and this should be shown as well."
  Built the same round, as 0.74.0. It was cut as 0.72.0 and renumbered when two sessions collided on the ledger.
  The sidecar registry's entries became {id, name}.
  A name can be given at birth, since the picker's ＋ New session asks "what is this session for?", or later, with ✎ on any row, which POSTs to /_board/session-name.
  The page-id prefix is worked out on the server, so the stored purpose is bare and the display reads QD3m-fix-black-screen.
  The name shows wherever the session appears: the picker rows, in bold monospace, and the strip summary. A session with no name keeps the first-message-title fallback.
  The name lives in .haipipe-board/sessions.json, not in the page header, which honours this page's "the board's md records outcomes only".

- 260731 JL · 🗂 The levels gained a third one: the page GROUP
  JL: "for each Question group, we can also add the chat icon for them, and then we can add the sdk or cli to discuss about this Question group."
  Built as 0.77.0, cut as 0.73.0 and renumbered on the same ledger collision.
  Every group heading on the index carries 💬.
  It opens the same panel attached to the GROUP, whose identity is the group FOLDER (7-QC-engine/).
  So sessions, names, HOLD, parking and the picker all reuse the page machinery unchanged.
  The scope sits between the two levels that already existed.
  A group session may edit any .md inside its folder.
  The board session has the whole board, and a page session has its one file.
  Its prime lists the group's pages with their states.
  Group sessions have no header line to live in, so the current one is the registry's newest entry.
  That keeps this page's "the board's md records outcomes only" intact.
  Names take the group letter as their prefix (QC-group-chat-smoke).
  Checked live: a scoped SDK turn on QC, the picker listing it by name, and the ⌨ terminal resuming the panel's own session.

### Decision Now
These are the calls only JL can make; CC ticks nothing here.

- [x] ⚖️ Amend the Law's "One Q ⇄ one session" for the history picker (JL 260731, on `QD3m`)
      DECIDED 260731 by JL: "somehow we want to update this law, that one Q, multiple session. the chat session with the predefined prompt related to this Q".
      That is option A with the prime kept: one CURRENT session per question, older ones resumable through the picker, and EVERY session opens primed with this Q's context.
      HOLD and one-window-at-a-time stay untouched. The Law section below carries the amendment.
      BUILT the same day as haipipe-board 0.62.0: the 🗂 Session strip in the panel, `/_board/sessions`, and the `session:` parameter on chat and terminal.
- [ ] 🗄 Rule whether the board folder keeps a copy of the session jsonls (JL 260731: "maybe still in the home, but we can make the copy of them in the board folder?")
      The LIVE file cannot move.
      Resume is bound to the cwd's project dir under `~/.claude/projects/`, and the 260723 move test showed that a moved jsonl refuses `--resume` (Lesson below).
      So any copy in the board folder is a backup or a readable export, never the live session.
      A · the LIVE file stays only in home, as it does today, and no backup copy is made in the board folder.
      B · a jsonl mirror is written to the board folder on release and stays gitignored. Cheap insurance, and it is restored by copying it back into the project dir.
      C · once the P2 mirror's jsonl reader exists, a readable markdown transcript is exported when a session retires, giving an archive a person can read.
      D · B and C are staged together: B now for backup insurance, and C once the mirror is ready.
      → CC's proposal: D, staged. B now, one copy at release time, cheap insurance. C once the P2 mirror's jsonl reader exists anyway.
      Both stay gitignored, because a transcript can carry secrets and this repo is shared.

## Files
- `cli/serve.py` + `live/base.py`
  `HOLD` / `RUNS` / `TERMS`: these tables are what enforce "one window per session".
  Since the QC8 split into `live/` modules the tables are defined in `live/base.py`, and `serve.py` imports them.
- Each question's `.md` header
  The `session:` line is where that question's session id lives.

## Law
**one scope · one CURRENT session · one live window**, replacing the 260723 three-beat "one question · one session · one jsonl", whose every term has since moved.
A SCOPE owns sessions, and there are three levels of it: the board, a group folder, a page.
Each level holds one CURRENT session plus a history you can resume from the 🗂 picker.
Every session opens primed with its scope's context, carries a name, runs one window at a time (HOLD), and opens at the SPACE root.
N scopes may run N terminals at once.
(JL 260723; amended by JL 260731 twice, "one Q, multiple session. the chat session with the predefined prompt related to this Q" and "for each Question group, we can also add the chat icon for them"; retired by JL 260731, "this law should be updated. It is actually very old")

- Three levels, one rule (JL 260731, built 0.77.0)
      Board level runs the whole board, group level runs one group FOLDER (`7-QC-engine/`), page level runs one page file.
      A scope's IDENTITY is that path.
      So the group level cost almost nothing: `term_key`, HOLD, parking, the sidecar registry, names, and the picker all took it unchanged.
      Write scope narrows as you go down: the board's session has every file, a group's session any `.md` inside its folder, a page's session its own file.
      A group has no header line to hold an id, so its current session is the registry's newest entry. The board's md still records outcomes only.
- One scope, several sessions, one current (JL 260731)
      A page's `session:` header keeps exactly one id, the CURRENT one, which the panel and the terminal open by default.
      Every id ever built for the scope is recorded in the serve.py sidecar (`.haipipe-board/sessions.json` at the SPACE root).
      The picker lists them and can resume any that landed on disk.
      Resuming an older session makes it the current one, and the header follows.
      One window at a time still holds per scope (HOLD), because two front ends on the same jsonl still fork histories.
- Sessions carry names: `<page-id>-<what-it-is-for>` (JL 260731, built 0.74.0)
      A name is given at birth, when the picker's ＋ New session asks, or later, with ✎ on any row.
      The prefix is worked out on the server, so the stored purpose is bare and the display reads `QD3m-fix-black-screen`.
      Names live in the registry, never in the page header, for the same reason the ids do.
- Both front ends point at the same current id
      The panel (`QD2`) and the terminal (`QD3`) are two windows on one session, not two routes.
      The terminal builds a uuid on first open (`claude --session-id`) and writes it back to the header, and the panel resumes that same id.
      What the 260731 amendment removed is only the claim that a question ever has ONE id.
      What it kept is that no session appears UNRECORDED, because a new id now goes through the sidecar.

- Sessions open at the SPACE root, not the board folder
      The `claude` inside the panel (QD2) and the terminal (QD3) has the whole repo (the SPACE) as cwd, not the board folder.
      Why: a question's session constantly touches the code it discusses, and the board folder alone is too narrow.
      Sessions therefore archive under the repo root's project dir (`~/.claude/projects/-Users-…-Physician-SPACE/`).
      Write permissions stay narrow, since the restricted tier edits only this question's files, but **the reading horizon is the whole repo**.
- A session is primed the moment it opens (JL 260723)
      Panel or terminal, the opening injects a `prime_context` block: which board, which scope, what it asks, how many comments are open, where the file is.
      A group's flavour (`group_prime_context`) lists the group's pages and their states instead.
      The panel does it through system_prompt, the terminal through `--append-system-prompt`.
      It costs no turn and runs nothing on its own. The session knows its place the moment it opens.
- One session, one window at a time
      The panel and the terminal read and write the same `.jsonl` on disk.
      The same scope must not have both open, or they overwrite each other or fork a second history.
      The server enforces this with HOLD.
      PARKING (0.73.0) is the one relaxation. It releases the window and the HOLD while keeping the process alive for a 600s grace, so a reattach gets the same pid with its screen replayed.
- Terminal identity = hash of the scope's path (unique across every board)
      Not a port, and not a name like "QD3": the page's file path, or the group's folder path.
      Two boards' QD3s have different paths → different keys → naturally separate.
- Different scopes, each on its own
      QA6's terminal and QD3's terminal are two different sessions; open them at the same time at will.
      N scopes = N terminals = N sessions, and none of them touch the others.
      To watch several, open more board tabs.

## Lesson
#### A session started by the SDK is a real Claude Code session.
`claude_agent_sdk` drives the `claude` CLI underneath.
Its records land in the same place as any session: `~/.claude/projects/<encoded cwd>/<session-id>.jsonl`, where cwd is now the SPACE root.
**So**: the panel (QD2) and the terminal (QD3) are not two routes; they are **two front ends of one session**.
That is what spares QD3 from rebuilding session management. It is just another window onto the same conversation.

#### Sessions bind to the cwd; changing the cwd swaps the whole session set.
The project dir name is encoded from the cwd: one cwd, one dir.
After the cwd moved from the board folder to the SPACE root, old sessions stayed in the old project dir.
`--resume <old sid>` from root cannot find them, and even copying the jsonl into the new dir does not fool resume. That was tested, and rejected.
So the cwd change restarted every question's session under root.

#### Ask "which machine does it run on" before picking a design.
The browser is on JL's laptop; `claude` is on the server.
Whatever the route, the machine actually running Claude is the server side. The page is only a window.

## Glossary
board / group / page level: the three levels of a conversation's scope (Law, 260731).
Board level runs the whole board: opening questions, editing the generator, and the calls that cross questions.
Group level runs one group FOLDER; page level runs one page file.
headless session: a Claude session started by a program, with no terminal window.

## Discussion
> JL: how do I attach a chatbot so that opening it is really opening Claude Code, and it takes this page as input and context? With the choice of opening it or not.
> JL: for example, after I comment, I open haichat and it reads my content, updates the markdown and html, and so on.
> JL: our current claude session is the "session for top", right? Then how do we open a terminal for each question?
> JL: could we make a new Q for chat, one for terminal version, and then other one for the claude_agent_sdk version.
>> CC0723: split. This question keeps only the three unanswered framework items (levels and boundaries); the SDK chat version goes to QD2, the TUI chat version to QD3.

## Log
- 260806 2141 · [REVISE-CC] swept to the 260806 architecture; Files record repointed HOLD/RUNS/TERMS to `live/base.py` (QC8 split), dead "## Where we are" pointer in Aims fixed to ## States, Glossary caught up from two levels to the three altitudes
260731 1905 · The one-live-window rule held only for chat on the tree: navigating with ⌨ on left the old scope's PTY live AND unparked while a new one opened (two windows, one of them invisible), and a group release parked the wrong scope. Fixed in `follow()` (0.86.0, recorded on `QD3`); the law itself needed no change; the code had simply stopped enforcing it on the split site
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
