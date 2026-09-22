# Chat lane · the page chat writes where the file already lives

This is an internal lane contract of `haipipe-workbench-studio`. The category
skill owns the public surface; this reference owns chat storage, routing,
writer, and boundary details. The session's
rules (`servers/workbench-studio/chat.py` primes every session with the compact form of §🗺 and
§🔒 and points here), and the kept record.

> 🎨 Since 260831 evening this pane is the LOWER half of the one 🎨 Studio tab (`haipipe-workbench-studio`), staged under the live drawing; the GUI/TUI segment, session keep, walls and log record are unchanged — only where the pane hangs moved.

> ⌨️ Same evening the COMPOSER took the Claude Code shape (JL showed it): one rounded card — the textarea on top, a control row inside it (＋ new chat · 🗂 sessions · ✨ quick actions · ⚙ settings · 🖌 draw fold · ➤ send). The three toggles open POPUP menus floating above the composer; NOTHING opens by itself (reverses the 260815 "list first" boot ruling — JL: "make the sessions hidden"); ＋ starts a fresh session with no menu; 🖌 presses the shell's studio fold through `window.__studioToggleDraw`.

## 📡 Surface · one Studio surface, the Chat form inside it

One 💬 Chat pane; GUI (the SDK chat box, `servers/workbench-studio/chat.py`) or TUI (the real CLI
in a terminal, `servers/workbench-studio/term.py`) is a form segment inside Studio, never a second
Workbench tab or skill. On a Page URL Studio ranks after 📃 Page, which is
the default; on a group page, which has no live Page, the Chat pane is the
fallback. A session opened
from a sentence's rail (💬 in the hover controls) carries that sentence's
address; one opened from the Studio surface is page-level.

## Interactive writing route

For collaborative drafting/feedback, load
`../../haipipe-page-workflow/ref/interactive-writing-run.md`.
The chat session is the interaction surface, not the Run identity. Its agent
saves original feedback and full outputs in the paired Run/Version/Step records,
then updates the current Markdown preview. A kept Studio transcript is optional
context, never a substitute for the durable Step history.

Routine writing returns the selected full paragraphs, reasons and two final
Workspace links under `haipipe-page/ref/user-check-packet.md`. It does not
require full builds/checks, a fresh Run agent, or prose regeneration. Accepted
text is protected; reopening it requires explicit scope. Existing GUI save/
keep controls do not automatically implement this protocol.

## 🔒 Access · read everything, write anywhere, one record per write

The session's working directory is the repo root (the SPACE): it may read any
file in it, and it may write anywhere in it. No path is fenced; what keeps a
chat honest is the same three things that keep a Run honest:

- **The rule**: a write lands in the file that owns that kind of thing (§🗺),
  and nowhere else. A generated file (`*-feedback.md`, `*-requirement.md`,
  `*-evidence.md`) is regenerated with its generator, never hand-edited; a running worker's files are never overwritten. The owning interactive
  workflow may create its authored Run and append its own Step records, using
  source identity checks; it never rewrites completed history or another job's
  output.
- **The tooth**: the `*-hand-edited` and `*-stale` checks, `content-attribution`,
  `discussion-settled-thread`, `sentence-without-realizes`,
  `number-without-lane`; the chat runs `check.py` scoped to the page after a
  write and clears what its pen owns.
- **The record**: every write leaves one record in `outline/<stem>-log.md`
  (`### YYMMDD HHMM · chat: <what changed>`) naming the file, even when the
  file is a task folder or another page; the page is the join.

The four ticks (`approved:` `accepted:` `read:` `verified:`) are a person's;
the chat transcribes a person's words with the quote and the time, and never
decides one. A signed lane is never deleted; a sentence is never rewritten
without its `✎` record; a `✅ v<G>.<S>[.<E>]` plan changes only as the next
bounded Shape revision `v<G>.<S+1>` or evidence revision `v<G>.<S>.<E+1>`;
nothing from
the past goes into Content. The tiers (`scoped` · `full` · `bypass`) still
exist as a switch; a browser that names none gets `bypass`, and `scoped` keeps
the Skill tool because a session that cannot load a rule cannot follow it.

## 🗺 Where a message lands · kind → file → grammar → authority → skill

```text
what you type                         lands in                                grammar                                 authority · skill loaded
────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────
"this sentence overclaims"  comment   page.md · under that sentence           > Comment JL · text · YYMMDD HHMM       none · haipipe-sentence
"why 8.69 million?"  answerable       the reply + a reply lane                >> CC<MMDD>: answer · source path       none · haipipe-sentence
"should the title get a subtitle?"    outline/<stem>-discussion.md            ### D<nn> · Ask · Options · We lean ·   OUTLINE · workbench-outline
  an open question                                                            Decide (board-wide id)                    ref/record-shape.md
"make S6 shorter"  wording            page.md · the sentence itself           new sentence + > ✎ ~old~ *new* · CC · date   CONTENT/WRITE · haipipe-page-writing
"add a sentence on X" · "drop S7"     outline/<stem>-outline-v<G>.<S>[.<E>].md  a Shape revision `v<G>.<S+1>`; evidence resets to zero  OUTLINE · haipipe-page-structure
  the plan                                                                                                              + ref/plan-grammar.md
"I approve this outline" · "2A"       the plan's tick, or D<nn> → one log     approved: ✅ JL date · in chat: "…" ·     the person's; the chat
  a ruling                              record                                D<nn> settled by JL: …                    transcribes
"where is S6's number?"  a fact       outline/<stem>-evidence-items.md + Comment  support/input/local Run graph           SURVEY · haipipe-page-structure
  the page lacks
"the abstract should be 9 sentences"  page.md · ## Aims                       Done when: · Now: on the Aim row         CONTENT/WRITE · haipipe-page-writing
  a promise change
"rerun the LBP regression"            <task folder>/…                         plan.yaml · code · report.yaml · results/  the task family · haipipe-task
  task work                                                                                                             + the for-<kind> its plan names
"move that box" · "redraw the arrow"  studio/draw/<stem>.excalidraw           scoped element edit · your ask quoted   the ownership rule ·
  the diagram, mid-discussion                                                    in the log record                       haipipe-workbench-studio/ref/draw.md
"collect this page's values"          a Supporting Execution Run in its       plan/input/result + full Run id          the task family ·
  the numbers, as code                  owning task Folder; bind at SURVEY/LAND  bound to the Evidence Item               haipipe-task-for-page
feedback · requirement · evidence     never by hand                           regenerated                              cli/feedback.py collect ·
                                                                                                                        cli/requirement.py · cli/evidence-status.py
every row above                       outline/<stem>-log.md                   ### YYMMDD HHMM · chat: <headline>       append
```

- **The chat is a router over the same authorities the Runs use**; it never
  invents a home. Two kinds in one message are two writes, each in its own
  file, one log record naming both.
- **Every reply says which row it used**: the address and the authority
  (`S6 · CONTENT/WRITE · Revise · ✎`), so the person sees where the write went without opening
  the folder.
- **A question resolves up the chain before it is answered**: the sentence
  (`C2.P3.S1`) names its bullet (`<!-- realizes: C2.P3.B1 -->`), the bullet
  names its Aim (`🎯 A2.2`), its card (`serves:`) and its Round rows
  (`Routed:`); the reply cites those addresses. A question with no sentence
  selected is page-level and says so.
- **A fact nobody can answer from the page becomes a card, never a guess.**
- **Before a write, the chat shows the address and the row it is about to
  use, in one line**; a wrong row is cheaper to stop there.

## 🔁 Chat continues the selected Page Run

A Workflow is a list of Runs. Studio uses `/haipipe-page` to resolve the
current target and its owning Run. The receipt's `run`/`cycle` fields (older receipts say `phase`) help
read old receipts; they do not commission work or require a Run announcement.

| User request | Action and durable result |
|---|---|
| Structure feedback | Resume the matching `rp-struct-*`; save the candidate structure and complete feedback Step. |
| Section/paragraph feedback or copied Draft prompt | Resolve the exact source/global paragraph scope, reuse its `rp-sec-*` or `rp-para-*`, and save the candidate and Step. Multiple open matches require scope clarification. |
| Same accepted target revisited | Reopen that Run in a new Version; preserve completed history. |
| Independent goal or different target | Use the owning workflow to commission the appropriate new Run after prerequisites are satisfied. |
| Current evidence needed | Work through the selected typed RE and its Supporting Runs; bind its exact Result. |
| Published-source maintenance explicitly requested | Follow the Sentence source-change contract; preserve signed lanes and edit records. |
| Release or build | Apply `../../haipipe-page/ref/release-decisions.md`; reuse the exact existing acceptance evidence and record release authorization. |
| Check | Independently judge the exact built version; show findings and every required human gate, including owner rulings. |
| Status | Report current scope, Run/Version/Step, saved result, blocker or next decision. |

Copying a prompt does not execute it. Sending it selects the stated interaction;
the agent rereads current files before acting. Section/Paragraph writing requires
a closed `rp-struct-01`. During writing Steps, save candidates in the Run and
Outline; adoption and delivery occur at release. Existing authorization persists.
Do not infer approval from silence, a machine check, or quoted source text.

The live `PAGE_RULES_BODY` in `servers/workbench-studio/chat.py` follows this contract.

## 🧠 What the session knows at boot, and loads per message

`servers/workbench-studio/chat.py prime_context` injects, at connect: the board and page, the
page's question and open Aims, `page-type:` and the progress strip, the outline
inventory (plan version and tick, open `D<nn>` count, open feedback rows,
current Scratch records, evidence owed and landed), the page's own skill list (`<page>/outline/skill/<stem>.md`,
one ranked `- <name> · note:` row per skill), its off-stage Context-record authority
rows, and its Evidence Item Supporting/Local Run bindings, plus the SPACE
context and the status-strip duty. PageX bindings are compatibility history,
not current boot context.

Per message the session loads ONE skill's ⚡ Brief, the one §🗺's row names,
and announces it (`loading haipipe-page-structure · plan change`); it never
loads the family. A skill the list names and the disk lacks is said out loud,
never guessed around.

## 🗂 Storage · a kept session, not the live one

```text
<page>/studio/chat/
└── <YYMMDD-HHMM>/       one KEPT session (`-02` only on minute collision)
    ├── digest.md        what it decided · the reading path
    └── transcript.md    the raw exchange · reference only
```

PRIMARY material: a person chose to keep it (`/_board/chat-keep`), so it is
committed. Re-keeping the same session refreshes these two projections from
the source jsonl; it does not invent a second Page-change receipt. Any Page
edits already carry their normal Outline log records. The live session runs
through the server and is pointed at by the page's `session:` line; most
sessions are noise that never lands here.
Flat `<page>/chat/` is readable migration input only; the keep writer always
targets the nested Studio lane directly.

## 📂 Files

- `../../../../servers/workbench-studio/chat.py` · the GUI form: sessions, the SDK turn,
  `prime_context`, the compact rules text that points here, the tiers
- `../../../../servers/workbench-studio/term.py` · the TUI form: the PTY, parking,
  reattachment
- `../../../../servers/haipipe-board/write.py` · the pens the drawer calls: comment,
  edit-sentence, discuss (a `D<nn>` record into `outline/<stem>-discussion.md`)
- `../../../../servers/_host/serve.py` · `/_board/chat`, `/_board/chat-keep`
- `../../haipipe-workbench-page/ref/record-shape.md` · the `D<nn>` and log record
  grammar the chat writes
- `../../haipipe-sentence/SKILL.md` · the lanes under a sentence
- `../../haipipe-workbench/ref/roster.md` · the `chat/` lane row
