# Chat · one Chat, its record in the folder, its form chosen inside
state: ✅ SETTLED · one Chat, form inside, chat/ holds a real turn · open: none here (faces carry theirs)
owner: JL
session: 82681719-498a-4c69-bf7f-5b221a925062
method: contract ruled 260815; the four face pages folded the same evening (JL: "just have one Chat in the plugin"), their substance carried here as divisions while each face keeps its own full record

## Opening
Where does a page's conversation live, and how many chat things does a page have?
One: a page has ONE Chat, and opening it offers the TUI form or the GUI form, a choice made inside the surface.
A kept conversation is one of the page's own files, so it lands in the page's folder at `<page>/chat/`.
The live session stays with the engine; the plugin folder holds what was kept.
A reader opens one Chat, picks a form, and finds that session on disk afterwards.

**Why one Chat and not two**: GUI and TUI stopped being separate subjects the moment the form became a choice made after opening.
The four face pages that carried them are folded into Content §3 to §6.

**Where a kept session sits**: `chat/<YYMMDD-HHMM>/` sits beside `draw/` and `meeting/` in the page's folder and follows the meeting plugin's shape; a folder of a page's own files is what the board calls plugin material.

**Covered elsewhere**: the engine work stays on the folded faces, the session model on `QPf4a`, the SDK chat box on `QPf4b`, the PTY pane on `QPf4c`, and the phone form on `QPf4d`.

**What this page decides**: the record contract, one Chat per page, the form chosen inside it, and what a keep writes.
How either engine is built is not decided here.

## Diagram
**One surface, two forms, one record**: the mode is chosen after opening, and both forms feed the same record.
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
### 1 · The record contract, as far as it is ruled
**One page, one conversation store**: sessions accumulate under dated folders, like meetings.
```text
  <page>/chat/<YYMMDD-HHMM>/ · one folder per kept session
  🗣 meeting/ = spoken testimony · 💬 chat/ = typed testimony · same grammar
```
A kept session follows the meeting plugin's shape: the digest is the reading path once one is written, the raw transcript is reference, and decisions are routed onto pages as sentences, which is already the rule.
The discovery boundary already protects it: a transcript full of `.md` files can never surface as ghost pages, because discovery never enters a plugin.
The fold surfaced a prior signal for this contract: the session page had carried JL's 260731 line "maybe still in the home, but we can make the copy of them in the board folder", which is this plugin, four months early.

### 2 · One surface, and the form chosen inside it
**The ruling**: GUI and TUI are two forms of one Chat, not two chats.
```text
  before 260815 evening        after
  QPf4b GUI page  ┐            💬 one Chat · open it · pick
  QPf4c TUI page  ┘ two subjects   🖥 GUI or ⌨️ TUI inside
```
The split is a difference of FORM and never of permission: both forms carry the full tier by default, and neither form is narrowed for being the smaller surface.
What each form is remains real and is held in the two divisions below; what died is the idea that each form needs its own page.

### 3 · The session model
**One session per question**: the Law the surface obeys in either form (folded from `QPf4a`).
```text
  ⚖️ one question, one session · one session, one window · N questions, N terminals
```
Sessions open at the SPACE root, and the session id is recorded on the page's `session:` line while it runs.
Its open question, the two-agents-one-file rule across nested scopes, stays on `QPf4a`'s Aims.

### 4 · The GUI form
**The rebuilt chat box**: `claude_agent_sdk` turns in the drawer (folded from `QPf4b`).
```text
  🖥 live/chat.py · sessions · the SDK turn · three permission tiers
```
The drawer sits outside `div.wrap`, so it survives the page swap.
Nine Aims are still open on `QPf4b`: A4.2 to A4.5 under what matching the extension costs, and A8.2, A8.4, A8.5, A8.6 and A8.7 under what a drawn interface has to be given.
Two calls sit in that page's `### Decision Now` and wait on JL: how a held session is reaped, and whether `QD1` re-rules one window per scope.

### 5 · The TUI form
**The real CLI**: a PTY in the pane, raw and smooth views (folded from `QPf4c`, which had absorbed the smooth-view page on 260801).
```text
  ⌨️ live/term.py · /_term/ PTY · parking · reattachment
```
Its open questions stay on `QPf4c`'s Aims: the re-key to (page, session), the web-chat rendering beside the raw pane, the fallback seam, the smoothness drop-test, and the written security boundary.

### 6 · The form per device
**Where typing happens**: what the pane shows when 80 columns will not fit (folded from `QPf4d`).
```text
  📱 phone · 💻 desktop · what the page owes a reader who switches away and back
```
Most of `QPf4d`'s Aims are still open, and A2.1 is the one this caption is about: typing on a phone still rides xterm's hidden textarea.
The phone's form is still a `### Decision Now` row there, blocking A3.1's width ruling, while A5.1's gesture audit and the four A6 rows on how the pane looks stay open too.

## Aims
- [x] 📦 The landing shape is ruled
      What a kept session writes into `chat/` is decided and written into Content §1.
- [x] 🔔 The keep trigger is ruled
      Whether a session lands automatically or only on an explicit keep is decided.
- [x] ✍️ The writer is named
      The tool that writes `chat/` is named and its home is recorded.
- [x] 🧪 One real session is kept
      A first conversation lands in some page's `chat/` and reads back cold.

## States
- ✅ 📦 The landing shape is ruled: a kept session writes `<page>/chat/<YYMMDD-HHMM>/`, and Content §1 carries it.
- ✅ 🔔 The keep trigger is ruled: the engine keeps on drawer close and on session switch, bounded to the sessions the page has registered.
- ✅ ✍️ The writer is named: `keep_sessions` in `live/chat.py`, behind `POST /_board/chat-keep`.
- ✅ 🧪 One real session is kept: `chat/260815-0457-82681719/transcript.md` holds the conversation that designed this plugin and reads back cold.

## Files
- `../../board/haipipe-board/live/chat.py`
  The GUI form's engine; §4 owns its design.
- `../../board/haipipe-board/live/term.py`
  The TUI form's engine; §5 owns its design.
- `QPf-page-folder/QPf4a-chat-per-question/QPf4a-chat-per-question.md` · `QPf-page-folder/QPf4b-chat-sdk/QPf4b-chat-sdk.md` · `QPf-page-folder/QPf4c-chat-terminal/QPf4c-chat-terminal.md` · `QPf-page-folder/QPf4d-chat-terminal-design/QPf4d-chat-terminal-design.md`
  The four folded faces, each holding its own full record and its own open Aims.

## Law
- What lands: the transcript, derived from the session's jsonl by the same walk the drawer replays; the digest half is not built and this page carries no aim for it (JL 260815, option C's transcript half).
- When: at the moments a conversation stops being on screen, drawer close and session switch, and bounded to sessions the page has registered, never every stray conversation (JL 260815: "I want the chat history to be recorded").
- Who writes: the engine, `keep_sessions` in `live/chat.py` behind `POST /_board/chat-keep`; the jsonl stays the source and transcript.md is derived, so a re-keep overwrites (JL 260815).
- One Chat per page; the TUI or GUI form is selected after opening, inside the surface (JL 260815).
- The form split is never a permission split; both forms carry the full tier by default (JL, first ruled on the session page).
- A kept conversation is plugin material at `<page>/chat/`, in the meeting shape (JL 260815).

## Log
- 260816 · [REVISE-CC] round 3, and every claim it touched was checked against disk first: `page-type: design` left the head on JL's ruling, because this page carries no candidate divisions and no SELECTION record, so it could never close under the for-design contract and its ✅ SETTLED is honest only as a plain Q page; §2 stopped saying the two forms carry "the same tier the CLI carries", which is a false equivalence, since `QPf4b`'s P2 records the browser default as `bypass` from JL's 260802 full·auto ruling while `QPf4a` ruled the CLI tier as ask-when-due; §4 now names `QPf4b`'s nine open Aims (A4.2 to A4.5, A8.2, A8.4 to A8.7) and puts the reaping and one-window calls in that page's `### Decision Now` at lines 485 and 491, where both rows actually live; §6 added A2.1, the phone typing row this division's caption is about, and stopped reading as a full list; the two engine line counts went, since `live/chat.py` is 1469 lines and `live/term.py` is 889, not 1332 and 857, and the capability lists stayed; States dropped the row that mirrored no Aim and only repeated Files; and the Opening's stage block now states the plain fact, that a kept conversation is one of the page's own files, leaving the board term "material" to the drawer.
- 260816 · [REVISE-CC] the page caught up with the close: §3 to §6 now point at each folded face's own Aims instead of claiming carried aims, States became one current-fact row per aim and dropped the false `_archive/` claim (the four faces stand as live 🗂 FOLDED pages), the Opening's rationale came back on stage with labelled drawer parts, the `state:` line became a row again, the two engine paths in Files were written in their resolving form `../../board/haipipe-board/live/*.py`, and Law stopped promising a digest aim that no Aims row carries.
- 260815 1900 · [JL via CC] `haipipe-plugin-chat` drafted under `page-plugins/`, round 2 of the thin-door migration: delta-only over `haipipe-plugin` (the landing rule stays this page's open Decision; the skill records the boundary instead of freezing it).
- 260815 1330 · [CHECK-CC] closed on JL's ruling after the loop was proven for real: a live SDK turn through the drawer (the venv fix below), its reply KEEP-TEST-OK landing in this page's own chat/ transcript. The earlier 8/8 suite had tested every gesture EXCEPT a turn, and serve.py had been started on the system python with no SDK; both are fixed (.venv created, serve restarted on it) and the miss is recorded here so the lesson outlives the fix.
- 260815 1900 · [REVISE-CC] the recorder shipped: list-first drawer opening, `chat-keep` endpoint, keep hooks on close and session switch, and this page's own `chat/` holds the first kept transcript, the session that designed it. The three Decision rows closed into Law with JL's words. The four folded faces returned as 🗂 FOLDED pages when that state shipped.
- 260815 1700 · [REVISE-CC] the door caught up with the ruling: shell tab strip GUI+TUI became one 💬 Chat tab with the form segment inside (live/shell.py), the plugin registry and Plugin menu each collapsed to one Chat entry (50-structure.js, shell), checks untouched because the #mtui/#mgui radio remains the mode's one writer.
- 260815 1600 · [REVISE-CC] the four faces folded on JL's ruling "just have one Chat in the plugin, not more ChatGUI or Chat TUI": their substance became Content §3 to §6, their 13 open aims carried with source tags, their full records archived, their scenes parked in this page's draw/.
- 260815 1500 · [DRAFT-CC] page born with the ruled half of the contract; QO1 to QO4 became faces QPf4a to QPf4d the same day.
