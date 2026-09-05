# Chat lane · the page chat writes where the file already lives

This is an internal lane contract of `haipipe-plugin-studio`. The category
skill owns the public surface; this reference owns chat storage, routing,
writer, and boundary details. The session's
rules (`live/chat.py` primes every session with the compact form of §🗺 and
§🔒 and points here), and the kept record.

> 🎨 Since 260831 evening this pane is the LOWER half of the one 🎨 Studio tab (`haipipe-plugin-studio`), staged under the live drawing; the GUI/TUI segment, session keep, walls and log record are unchanged — only where the pane hangs moved.

> ⌨️ Same evening the COMPOSER took the Claude Code shape (JL showed it): one rounded card — the textarea on top, a control row inside it (＋ new chat · 🗂 sessions · ✨ quick actions · ⚙ settings · 🖌 draw fold · ➤ send). The three toggles open POPUP menus floating above the composer; NOTHING opens by itself (reverses the 260815 "list first" boot ruling — JL: "make the sessions hidden"); ＋ starts a fresh session with no menu; 🖌 presses the shell's studio fold through `window.__studioToggleDraw`.

## 📡 Surface · one Studio surface, the Chat form inside it

One 💬 Chat pane; GUI (the SDK chat box, `live/chat.py`) or TUI (the real CLI
in a terminal, `live/term.py`) is a form segment inside Studio, never a second
Plugin tab or skill. On a Page URL Studio ranks after 🧭 Outline, which is
the default; on a group page, which has no live Page, the Chat pane is the
fallback. A session opened
from a sentence's rail (💬 in the hover controls) carries that sentence's
address; one opened from the Studio surface is page-level.

## 🔒 Access · read everything, write anywhere, one record per write

The session's working directory is the repo root (the SPACE): it may read any
file in it, and it may write anywhere in it. No path is fenced; what keeps a
chat honest is the same three things that keep a phase honest:

- **The rule**: a write lands in the file that owns that kind of thing (§🗺),
  and nowhere else. A generated file (`*-feedback.md`, `*-requirement.md`,
  `*-evidence.md`) is regenerated with its generator, never hand-edited; a run
  folder (`_runs/`, `runs/`) and a QA file in `state: working` are never
  written, because a job may be running there.
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
without its `✎` record; a `✅ vN.0` plan is changed only as the next working
`vN.<k+1>` revision; nothing from
the past goes into Content. The tiers (`scoped` · `full` · `bypass`) still
exist as a switch; a browser that names none gets `bypass`, and `scoped` keeps
the Skill tool because a session that cannot load a rule cannot follow it.

## 🗺 Where a message lands · kind → file → grammar → authority → skill

```text
what you type                         lands in                                grammar                                 authority · skill loaded
────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────
"this sentence overclaims"  comment   page.md · under that sentence           > Comment JL · text · YYMMDD HHMM       none · haipipe-sentence
"why 8.69 million?"  answerable       the reply + a reply lane                >> CC<MMDD>: answer · source path       none · haipipe-sentence
"should the title get a subtitle?"    outline/<stem>-discussion.md            ### D<nn> · Ask · Options · We lean ·   OUTLINE · plugin-outline
  an open question                                                            Decide (board-wide id)                    ref/record-shape.md
"make S6 shorter"  wording            page.md · the sentence itself           new sentence + > ✎ ~old~ *new* · CC · date   CONTENT/WRITE · haipipe-page-content
"add a sentence on X" · "drop S7"     outline/<stem>-outline-v<N>.<k>.md      a plan bullet; next vN.<k+1> if vN.0 is ✅ OUTLINE · haipipe-page-outline
  the plan                                                                                                              + ref/plan-grammar.md
"I approve this outline" · "2A"       the plan's tick, or D<nn> → one log     approved: ✅ JL date · in chat: "…" ·     the person's; the chat
  a ruling                              record                                D<nn> settled by JL: …                    transcribes
"where is S6's number?"  a fact       outline/<stem>-evidence-items.md + Comment  support/input/local Run graph           SURVEY · haipipe-page-outline
  the page lacks
"the abstract should be 9 sentences"  page.md · ## Aims                       Done when: · Now: on the Aim row         CONTENT/WRITE · haipipe-page-content
  a promise change
"rerun the LBP regression"            <task folder>/…                         plan.yaml · code · report.yaml · QA/     the task family · haipipe-task
  task work                                                                                                             + the for-<kind> its plan names
"move that box" · "redraw the arrow"  studio/draw/<stem>.excalidraw           scoped element edit · your ask quoted   the ownership rule ·
  the diagram, mid-discussion                                                    in the log record                       haipipe-plugin-studio/ref/draw.md
"collect this page's values"          a Supporting Execution Run in its       plan/input/result + full Run id          the task family ·
  the numbers, as code                  owning task Folder; bind at SURVEY/LAND  bound to the Evidence Item               haipipe-task-for-page
feedback · requirement · evidence     never by hand                           regenerated                              cli/feedback.py collect ·
                                                                                                                        cli/requirement.py · cli/evidence-status.py
every row above                       outline/<stem>-log.md                   ### YYMMDD HHMM · chat: <headline>       append
```

- **The chat is a router over the same authorities the phases use**; it never
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

## 🔁 The chat runs the page workflow

The page chat is the session a person works a page in, so it is also the
interactive RUN controller: it knows the five Page phases, reads which one the Page
is in from disk, performs a phase when asked, and reports the strip. A phase
word you type is the verb:

```text
you type                 phase     the chat loads                       ends when                                   trace it leaves
──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────
"prepare context"        PREPARE   haipipe-page-context + ref/record-shape.md     required authorities resolve and freeze  outline/<stem>-context.md · receipt
"outline it" · "plan"    SHAPE     haipipe-page-outline + ref/plan-grammar.md   five checks pass; YOUR approved: tick   plan v<N>.<k> · D<nn> · log record · receipt
"survey"                 SURVEY    haipipe-page-outline                 every item has support + input + local Run  outline/<stem>-evidence-items.md · log · receipt
"land" · "make the runs" LAND      haipipe-page-evidence                every ☑ make item has a ready local Result  Runs · item → Result · receipt
"embed" · "fold"         EMBED     haipipe-page-evidence                every ready item is in next working plan    outline/<stem>-outline-v<N>.<k+1>.md · receipt
"draft it"               WRITE     haipipe-page-content                 commissioned divisions pass trace/style   Page Content · Division Results · receipt
"revise" · "trim"        WRITE     haipipe-page-content                 revised divisions pass trace/style        Page Content · Division Results · receipt
"build" · "compile"      WRITE     haipipe-page-content                 delivery projections match Page source    delivery/ · build receipt
"check it"               CHECK     haipipe-page-check (read-only here)  a fresh judge routes CLOSE or back            a receipt from haipipe-page-check-agent
"where are we"           none      the strip                            one line: ⏱️ 🧩 OUTLINE · 🧭✅ 🧩⏳ 🃏⏳ ✏️⬜ 🔍⬜ · ✋2
```

- **The strip comes from disk, never from what the page says about itself**:
  `cli/pagephase.py <page-dir>` (`src/page_phase.py compact()`), injected at
  boot and re-read after every pass. `--owed` is the ledger of the ticks that
  are yours.
- **A pass performed in the chat is a pass**: it leaves the same trace the
  phase agent leaves (the artifact, one log record with the receipt folded
  under it, the strip in the reply); the agent-per-phase RUN
  (`haipipe-page-workflow`) is the unattended path for the same work.
- **The chat announces the cycle on every reply** (`WRITE · SM00`),
  because work that does not name its phase cannot be routed or audited.
- **Two things the chat may not do**: write your four ticks (it transcribes
  your words), and judge its own version. `✅ Quality Check` in the chat is
  read-only; a formal CHECK dispatches `haipipe-page-check-agent` in a fresh
  context and the chat relays its route.
- **The order is authority-driven**: PREPARE freezes context; SHAPE ⇄ SURVEY ⇄
  LAND ⇄ EMBED continues until the plan and its evidence agree and the
  required approval is durable; CONTENT/WRITE then performs Draft, Revise,
  Build, and Pre-check as internal movements; CHECK judges and may send the
  Page back to any named phase. The chat says which cycle is next and why, and
  never skips SURVEY when a new Supporting or Local Run route is needed.

## 🧠 What the session knows at boot, and loads per message

`live/chat.py prime_context` injects, at connect: the board and page, the
page's question and open Aims, `page-type:` and the phase strip, the outline
inventory (plan version and tick, open `D<nn>` count, open feedback rows,
evidence owed and landed), the page's own skill list (`<page>/outline/skill/<stem>.md`,
one ranked `- <name> · note:` row per skill), its Context Workspace authority
rows, and its Evidence Item Supporting/Local Run bindings, plus the SPACE
context and the status-strip duty. PageX bindings are compatibility history,
not current boot context.

Per message the session loads ONE skill's ⚡ Brief, the one §🗺's row names,
and announces it (`loading haipipe-page-outline · plan change`); it never
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

- `../../../haipipe-board/live/chat.py` · the GUI form: sessions, the SDK turn,
  `prime_context`, the compact rules text that points here, the tiers
- `../../../haipipe-board/live/term.py` · the TUI form: the PTY, parking,
  reattachment
- `../../../haipipe-board/live/write.py` · the pens the drawer calls: comment,
  edit-sentence, discuss (a `D<nn>` record into `outline/<stem>-discussion.md`)
- `../../../haipipe-board/cli/serve.py` · `/_board/chat`, `/_board/chat-keep`
- `../../haipipe-plugin-outline/ref/record-shape.md` · the `D<nn>` and log record
  grammar the chat writes
- `../../../haipipe-sentence/SKILL.md` · the lanes under a sentence
- `../../../haipipe-plugin/ref/roster.md` · the `chat/` lane row
