# Chat · one Chat, its record in the folder, its form chosen inside
state: ✅ SETTLED · one Chat, form inside, chat/ holds a real turn · open: none here (faces carry theirs)
owner: JL
session: 82681719-498a-4c69-bf7f-5b221a925062
method: ruled 260815 (JL: "just have one Chat in the plugin"); the four face pages folded the same evening, their substance moved here as parts §3 to §6, each face keeping its own record

## Opening
Where does a page's conversation live, and how many chats does a page have?
One.
A page has ONE Chat, and you pick its form after you open it: the TUI form or the GUI form.
A kept conversation is one of the page's own files, so it lands in the page's folder at `<page>/chat/`.
The live session stays with the engine, and the `chat/` folder holds what was kept.
A reader opens one Chat, picks a form, and finds that session on disk afterwards.

**Why one Chat and not two**: GUI and TUI stopped being two subjects once the form became a choice you make after opening.
The four face pages that carried them are folded into Content §3 to §6.

**Where a kept session sits**: `chat/<YYMMDD-HHMM>/` sits beside `draw/` and `meeting/` in the page's folder, and it follows the same shape as a meeting.
A folder of a page's own files is what the board calls plugin material.

**Covered elsewhere**: the engine work stays on the folded faces, the session model on `QPf4a`, the SDK chat box on `QPf4b`, the PTY pane on `QPf4c`, and the phone form on `QPf4d`.

**What this page decides**: the rules for the record, one Chat per page, the form chosen inside it, and what a keep writes to disk.
How either engine is built is not decided here.

## Diagram
**One Chat, two forms, one record**: you pick the form after opening, and both forms write the same record.
```text
                 💬 CHAT · one surface per page
                          │ open
                 ┌────────┴────────┐  choose a FORM
                 ▼                 ▼
          🖥 GUI form        ⌨️ TUI form
          the SDK chat box   the real CLI
                 └────────┬────────┘
                          ▼ keep (explicit)
              📂 <page>/chat/<YYMMDD-HHMM>/
              transcript.md · digest.md not built
```

## Content
### 1 · What a kept conversation leaves on disk
**One page, one list of conversations**: kept sessions pile up in dated folders, like meetings.
```text
  <page>/chat/<YYMMDD-HHMM>/ · one folder per kept session
  🗣 meeting/ = spoken testimony · 💬 chat/ = typed testimony · same grammar
```
📌 This part settles that a kept chat becomes a dated folder of the page's own files, read the same way a meeting is.

A kept session follows the same shape as a meeting.
The short write-up, `digest.md`, is what you read once someone writes one, and the raw transcript is there to check against.
Decisions are moved onto pages as sentences, which is already the rule.
The plugin boundary already protects this folder.
A folder full of `.md` transcripts can never show up as ghost pages, because discovery never looks inside a plugin folder.

### 2 · One Chat, and you pick its form after you open it
**The ruling**: GUI and TUI are two forms of one Chat, not two chats.
```text
  before 260815 evening        after
  QPf4b GUI page  ┐            💬 one Chat · open it · pick
  QPf4c TUI page  ┘ two subjects   🖥 GUI or ⌨️ TUI inside
```
📌 This part settles that the browser box and the terminal are two forms of one Chat, not two separate things.

The split is about FORM, never about permission.
Neither form is given fewer tools than the other, and what the tiers are called is `QPf4b`'s record.
What each form is stays real, and the two parts below hold it.
What died is the idea that each form needs its own page.

### 3 · One scope has one live session at a time
**One scope, one current session**: the Law the surface obeys in either form (folded from `QPf4a`).
```text
  ⚖️ one scope · one current session · one live window · N scopes, N terminals
```
📌 This part fixes one live session per scope, and says the copy question is still open.

Sessions open at the SPACE root, and the session id is written on the page's `session:` line while it runs.
The two-agents-one-file rule across nested scopes stays open on `QPf4a`'s Aims.
A second call is open there as a `### Decision Now` row, with four options and no tick.
It asks whether the board folder keeps a copy of the session jsonl files.
Until JL rules on it, what §1 describes is only the transcript built from the session file.
Whether the live session file is ever copied beside it stays undecided.

### 4 · The chat box in the browser, and what is still open on it
**The rebuilt chat box**: `claude_agent_sdk` turns in the drawer (folded from `QPf4b`).
```text
  🖥 live/chat.py · sessions · the SDK turn · three permission tiers
```
📌 This part holds the browser chat box, and names the nine Aims and two calls still open on it.

The drawer sits outside `div.wrap`, so it survives the page swap.
Nine Aims are still open on `QPf4b`.
A4.2 to A4.5 sit under what it costs to match the extension.
A8.2, A8.4, A8.5, A8.6 and A8.7 sit under what a drawn interface has to be given.
Two calls sit in that page's `### Decision Now` and wait on JL.
One is how a held session is cleaned up, the other is whether `QPf4a`'s Law rules again on one window per scope.

### 5 · The real command line, running inside the pane
**The real CLI**: a PTY in the pane, raw and smooth views (folded from `QPf4c`, which had absorbed the smooth-view page on 260801).
```text
  ⌨️ live/term.py · /_term/ PTY · parking · reattachment
```
📌 This part holds the terminal form, and points at the questions still open on it.

Its open questions stay on `QPf4c`'s Aims.
Among them are the re-key to (page, session), the web chat drawn beside the raw pane, the fallback seam, the smoothness drop test, and the written security boundary.

### 6 · What a reader on a phone gets, which is still mostly open
**Where typing happens**: what the pane shows when 80 columns will not fit (folded from `QPf4d`).
```text
  📱 phone · 💻 desktop · what the page owes a reader who switches away and back
```
📌 This part is about typing on a small screen, and almost all of it is still undecided.

Most of `QPf4d`'s Aims are still open.
A2.1 is the one this figure is about: typing on a phone still goes through xterm's hidden textarea.
The phone's form is still a `### Decision Now` row there, and it blocks A3.1's ruling on width.
A5.1's gesture check and the four A6 rows on how the pane looks stay open too.

## Aims
- [x] 📦 It is decided what a kept session writes to disk
      What a kept session writes into `chat/` is decided and written into Content §1.
- [x] 🔔 It is decided when a session gets kept
      Whether a session lands on its own or only when someone asks to keep it is decided.
- [x] ✍️ The one tool that writes `chat/` is named
      The tool that writes `chat/` is named and its home is recorded.
- [x] 🧪 One real session is kept
      A first conversation lands in some page's `chat/` and reads back cold.

## States
- ✅ 📦 What a kept session writes is decided: it writes `<page>/chat/<YYMMDD-HHMM>/`, and Content §1 carries it.
- ✅ 🔔 When a session gets kept is decided: the engine keeps it when the drawer closes and when you switch session, and only for sessions the page has registered.
- ✅ ✍️ The writer is named: `keep_sessions` in `live/chat.py`, behind `POST /_board/chat-keep`.
- ✅ 🧪 One real session is kept: `chat/260815-0457-82681719/transcript.md` holds the conversation that designed this plugin and reads back cold.

## Files
- `../../board/haipipe-board/live/chat.py`
  The GUI form's engine; §4 owns its design.
- `../../board/haipipe-board/live/term.py`
  The TUI form's engine; §5 owns its design.
- `4-QPf-page-folder/QPf4a-chat-per-question/QPf4a-chat-per-question.md`
  The session model folded into §3: its Law, the two-agents-one-file rule, and the open call on keeping a copy of the jsonls.
- `4-QPf-page-folder/QPf4b-chat-sdk/QPf4b-chat-sdk.md`
  The GUI form folded into §4: the drawer's design record, its nine open Aims, and its two calls waiting on JL.
- `4-QPf-page-folder/QPf4c-chat-terminal/QPf4c-chat-terminal.md`
  The TUI form folded into §5: the PTY engine, parking and reattachment, and the open Aims down to the written security boundary.
- `4-QPf-page-folder/QPf4d-chat-terminal-design/QPf4d-chat-terminal-design.md`
  The form per device folded into §6: the four constraints a device puts on the terminal, and what a phone gets instead.

## Law
- What lands: the transcript, derived from the session's jsonl by the same walk the drawer replays; the digest half is not built and this page carries no aim for it (JL 260815, option C's transcript half).
- When: at the moments a conversation stops being on screen, drawer close and session switch, and bounded to sessions the page has registered, never every stray conversation (JL 260815: "I want the chat history to be recorded").
- Who writes: the engine, `keep_sessions` in `live/chat.py` behind `POST /_board/chat-keep`; the jsonl stays the source and transcript.md is derived, so a re-keep overwrites (JL 260815).
- One Chat per page; the TUI or GUI form is selected after opening, inside the surface (JL 260815).
- The form split is never a permission split; both forms carry the full tier by default (JL, first ruled on the session page).
- A kept conversation is plugin material at `<page>/chat/`, in the meeting shape (JL 260815).

## Log
- 📖 260816 · [REVISE-CC, JL ruled] the page was rewritten in plain words, for a reader with ADHD whose English is a second language (JL: "我真的读不下去"). The 🧭 Outline tab had been showing this page's own sentences back, and they were unreadable, so the tab was right and the prose was not. Every division title now names its consequence instead of a mechanism, each one gained a `📌` line saying in one sentence what the part settles, and every aim, `Done when:` and State row was replaced with a short plain-word version. House words went with them, `division` to part, `store` to list, `render` to read or draw, `seed` to suggest, `mint` to build. Measured with `haipipe-writing`'s `cli/score.py`: 5 sentences flagged before, 0 after, every one that remains inside this Log, which is history and was not touched. No fact, id, `§` mark or section changed; only the words.
- 260816 · [REVISE-CC] seven factual corrections, each checked against the face on disk: §3's caption and figure carried the 260723 three-beat "one question, one session · one session, one window · N questions, N terminals", which `QPf4a`'s own Law retired for "one scope · one CURRENT session · one live window" plus "N scopes may run N terminals at once" (`QPf4a-chat-per-question.md:148` and `:150`), and the stale beat contradicted this page's §4 and `QPf4b`'s A8.5; §3 now also names the open `### Decision Now` row at `QPf4a-chat-per-question.md:133`, JL's unticked "Rule whether the board folder keeps a copy of the session jsonls" with options A to D, which §3 had reported as one open item and this page's head line had downgraded to none; §1 lost the sentence quoting that same row's words as "a prior signal" and "four months early", since it is a live call, not history, and JL's line is 260731 against the 260815 ruling, fifteen days rather than four months; §2 stopped claiming "both forms carry the full tier by default", a phrase this page never defines, and says instead that neither form is given fewer tools than the other, leaving the tier names to `QPf4b`, whose P2 records the browser default as `bypass` while `QPf4a` records the terminal as fully unrestricted, two defaults that differ in kind; §4's `QD1` became `QPf4a`'s Law, since `QD1` is the retired alias for that face (`board.md:327`) and appears nowhere else on a page that names its faces QPf4a to QPf4d; §5 gained "among them", because its five named open questions omit A4.2, the terminal sized to its pane at every width, whose State `QPf4c` never mirrors; and Files split the four faces off one shared row into one row each, with the record each keeps. Not fixed here and left for its own turn: the Law fold still carries the same "both forms carry the full tier by default" wording §2 just dropped.
- 260816 · [REVISE-CC] round 3, and every claim it touched was checked against disk first: `page-type: design` left the head on JL's ruling, because this page carries no candidate divisions and no SELECTION record, so it could never close under the for-design contract and its ✅ SETTLED is honest only as a plain Q page; §2 stopped saying the two forms carry "the same tier the CLI carries", which is a false equivalence, since `QPf4b`'s P2 records the browser default as `bypass` from JL's 260802 full·auto ruling while `QPf4a` ruled the CLI tier as ask-when-due; §4 now names `QPf4b`'s nine open Aims (A4.2 to A4.5, A8.2, A8.4 to A8.7) and puts the reaping and one-window calls in that page's `### Decision Now` at lines 485 and 491, where both rows actually live; §6 added A2.1, the phone typing row this division's caption is about, and stopped reading as a full list; the two engine line counts went, since `live/chat.py` is 1469 lines and `live/term.py` is 889, not 1332 and 857, and the capability lists stayed; States dropped the row that mirrored no Aim and only repeated Files; and the Opening's stage block now states the plain fact, that a kept conversation is one of the page's own files, leaving the board term "material" to the drawer.
- 260816 · [REVISE-CC] the page caught up with the close: §3 to §6 now point at each folded face's own Aims instead of claiming carried aims, States became one current-fact row per aim and dropped the false `_archive/` claim (the four faces stand as live 🗂 FOLDED pages), the Opening's rationale came back on stage with labelled drawer parts, the `state:` line became a row again, the two engine paths in Files were written in their resolving form `../../board/haipipe-board/live/*.py`, and Law stopped promising a digest aim that no Aims row carries.
- 260815 1900 · [JL via CC] `haipipe-plugin-chat` drafted under `page-plugins/`, round 2 of the thin-door migration: delta-only over `haipipe-plugin` (the landing rule stays this page's open Decision; the skill records the boundary instead of freezing it).
- 260815 1330 · [CHECK-CC] closed on JL's ruling after the loop was proven for real: a live SDK turn through the drawer (the venv fix below), its reply KEEP-TEST-OK landing in this page's own chat/ transcript. The earlier 8/8 suite had tested every gesture EXCEPT a turn, and serve.py had been started on the system python with no SDK; both are fixed (.venv created, serve restarted on it) and the miss is recorded here so the lesson outlives the fix.
- 260815 1900 · [REVISE-CC] the recorder shipped: list-first drawer opening, `chat-keep` endpoint, keep hooks on close and session switch, and this page's own `chat/` holds the first kept transcript, the session that designed it. The three Decision rows closed into Law with JL's words. The four folded faces returned as 🗂 FOLDED pages when that state shipped.
- 260815 1700 · [REVISE-CC] the door caught up with the ruling: shell tab strip GUI+TUI became one 💬 Chat tab with the form segment inside (live/shell.py), the plugin registry and Plugin menu each collapsed to one Chat entry (50-structure.js, shell), checks untouched because the #mtui/#mgui radio remains the mode's one writer.
- 260815 1600 · [REVISE-CC] the four faces folded on JL's ruling "just have one Chat in the plugin, not more ChatGUI or Chat TUI": their substance became Content §3 to §6, their 13 open aims carried with source tags, their full records archived, their scenes parked in this page's draw/.
- 260815 1500 · [DRAFT-CC] page born with the ruled half of the contract; QO1 to QO4 became faces QPf4a to QPf4d the same day.
