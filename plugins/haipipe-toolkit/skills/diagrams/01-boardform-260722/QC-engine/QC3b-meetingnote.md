# A meeting note on the board

state: 🟡 PARTIAL · the page kind ships; routing does not
owner: JL
method: separate the artifact from its consequences: give the note a home, and route what it decided into the Qs that own it

## Opening
How should a meeting enter the Board so its record stays citable and its decisions reach the pages they change?

A meeting leaves both a long source artifact and a small set of consequences.
Keeping only the note makes an archive, while routing only the decisions removes their evidence and context.
The split affects how readers revisit the meeting and how later pages explain why they changed.
It succeeds when the note has one readable page and each consequence points to its owning page.

## Boundary
- ✅ Covered here
  How a meeting note enters a board: whether it becomes a page, what page kind it is, what its managed half holds, and how its decisions reach the Q pages they belong to.
- ↪ Covered elsewhere
  How a folder is mirrored into a page at all: `QC3a`, which already does exactly this for a skill folder.
  How one input becomes one anchored write: `Skill-5-haipipe-board-routing`.
  The Related Folders fold that can open the file today without any of this: `QB2`.
  What a page's sections must contain once it exists: `QB4`.

## Diagram

```text
   ── one meeting, two destinations ──────────────────────────────────

   🎙 echo-meeting (Obsidian plugin, jluo41)
      records · transcribes · summarizes
              │
              ▼
   meeting/260723-meeting.md        8,573 words · 1,045 transcript lines
      frontmatter: type: meeting · source: echo-meeting
      ## Recording   ![[…webm]]
      ## Transcript  [!quote]- folded
      ## …           24 headings of summary
              │
              ├──────────────► ① THE ARTIFACT
              │                 a page you can open, link, and chat with
              │                 Meeting-1-260723.md, a page KIND like Skill-N
              │
              └──────────────► ② THE CONSEQUENCES
                                "we decided X" → the Q that owns X
                                QB2 · Where we are          + one record
                                QD3 · Decision Now          + one row
                                QA1 · Log                   + one line

   ① without ② is an archive nobody reads.
   ② without ① loses the source: a decision with no meeting to point back at.
```

## Content
### §1 Why a date-named file is invisible today

```text
page_files(d)          matches a NAME, at any depth
  Q*.md  S*.md  Agent*.md          ✅ QB4c-content.md · Skill-0-….md
  anything else                    ❌ meeting/260723-meeting.md
  under _*/ .*/ fig/               ❌ excluded wherever it sits
```

The board has no per-folder rule and no registry: a file is a page when its name says so.
That is why `meeting/` is silent rather than broken, and why the cheapest possible version of this whole question is a rename.

#### The rename is not the answer, and it is worth saying why
Naming the file `S260723-meeting.md` would put it on the board tonight, and it would put 1,045 transcript lines into the sidebar, the Section Matrix, and the page count.
A board page owes an Opening, a Diagram, Items to Finish, Where we are, and Files; a transcript owes none of them and will never have them.
The page kinds that already exist (`Skill-N`, `Agent-N`) exist precisely because some artifacts deserve a page whose shape is not a Q's shape.

### §2 The artifact half: a Meeting page kind

```text
   Meeting-1-260723.md
   ┌──────────────────────────────────────────────┐
   │ MANAGED  (generated, never hand-edited)      │  ← from the echo-meeting note
   │   date · duration · participants             │
   │   ▶ recording link                           │
   │   the summary headings, verbatim             │
   │   🗂 Transcript (folded, or left in place)    │
   ├──────────────────────────────────────────────┤
   │ AUTHORED (yours, survives every regenerate)  │
   │   What this meeting decided → which Q        │
   │   What it left open                          │
   └──────────────────────────────────────────────┘
```

`QC3a` already settled this exact managed/authored split for a skill folder, and `skillpage.py` already implements it.
A meeting page is the same generator pointed at a different source, which makes it a small change rather than a new subsystem.

### §3 The consequences half: routing, not archiving

```text
   a meeting note is INPUT to the board, the way a chat message is
   ────────────────────────────────────────────────────────────────
   read the summary, not the transcript
        │
        ├─ "we decided the tree replaces board.html"   → QC4 · Where we are
        ├─ "JL still owes the identity call"           → QB5e · Decision Now
        └─ "renamed the groups"                        → QA1 · Log
                                                         + each line cites
                                                           Meeting-1-260723
```

This is the half that matters, and it is the half that has no machinery today.
`Skill-5-haipipe-board-routing` is the verb that turns one input into one anchored write, and a meeting note is a batch of exactly that shape.

### §4 What the producing end actually emits

```text
   echo-meeting · 1,657-line Obsidian plugin + 5 python modules
   ─────────────────────────────────────────────────────────────
   🎤 mic ─────────────┐
   🔊 far end ─────────┤  EchoCapture (CoreAudio process tap, spawned as a
      (the other        │  child process over a local websocket) or BlackHole
       participants)    ▼
                    main.ts
                      ├─ LIVE   AudioWorklet PCM @16kHz ─▶ Azure Speech ─▶ `[m:ss] 🎙️ S1 …`
                      └─ BATCH  py/echo_transcribe.py   ─▶ OpenAI or self-hosted Whisper
                                       │
                                       ▼  transcript on stdin
                            py/echo_summarize.py ─▶ llm_engine
                                       │             claude_sdk (OAuth ~/.claude, $0)
                                       │             claude_api · codex_oauth
                                       ▼
                            ## Summary, in a FIXED structure
```

#### The note is written section by section, not appended
`noteMarkdown()` lays down the skeleton the moment recording stops, with `_Pending._` in each slot, and every later step calls `replaceSection(content, heading, body)`, which finds `## Heading` and swaps everything up to the next heading.
Re-transcribing or re-summarizing therefore rewrites one section and leaves the rest alone, which is the same discipline `QC4a` settled for this board's own write path: land at a section boundary, never at a byte offset.
A separate `--title --model haiku` call renames the file and rewrites both the `# ` heading and the frontmatter `title:`, which is why the note on disk is named after what the meeting was about rather than after its timestamp.

#### The summary is already board-shaped, and that is the whole opportunity
The summarizer's system prompt fixes six sections: `### TL;DR`, `### Diagram`, `### Key Points`, `### Decisions`, `### Action Items`, `### Open Questions`.
It requires the Diagram to be one emoji-dense ASCII figure in a `text` fence, which is the same figure this board's `## Diagram` section asks every page for.
Action Items arrive as `- [ ]` rows that already name their owner, which is the shape an `Items to Finish` row wants.
So routing a meeting is not natural-language interpretation, it is a mapping between four named sections and four board constructs; the only genuinely hard part left is deciding which Q owns each line.

```text
   ### Decisions       ─▶  the owning Q's `Where we are`, one record each
   ### Action Items    ─▶  `Items to Finish`, already `- [ ]` with an owner
   ### Open Questions  ─▶  candidate new Q pages
   ### Diagram         ─▶  the meeting page's own `## Diagram`
```

`260723-meeting.md` is the sharpest possible test of that mapping, because it is the meeting where this board was designed: its Action Items name the single-question page layout, the English-only rule, the per-question Excalidraw canvas, and the Related Files section, all of which this board has since shipped and recorded under different ids.

### §5 How the code works, in one read

```text
   meetingpage.py new <board> <note.md>
   ─────────────────────────────────────────────────────────────────
   read_note()        frontmatter · then `## ` sections · then the
                      `## Summary`'s `### ` ones, keyed `s:tl;dr` …
        │             fences respected, so a figure never splits a heading
        ▼
   head_block()       TL;DR + a metadata line          ┐
   diagram_block()    the summary's ASCII, or a stub   ├ THREE MANAGED SPANS
   body_block()       Key points · Decisions ·         ┘ each stamped with the
                      chapters · Transcript              note's sha256[:16]
        │
        ▼
   STUB.format()      the six base sections, with Items seeded from
                      `### Action Items` and Decision Now from
                      `### Open Questions` — SEEDED, never managed
        │
        ▼
   Meeting-<n>-<slug>.md   +  one line appended to board.md's `## Pages`

   meetingpage.py sync <board> Meeting-1
   ─────────────────────────────────────────────────────────────────
   MARKER regex ──▶ the hash AND the note path, out of the page itself
        │           (skillpage.py learned this the hard way: a span must
        │            not depend on rendered content to find its source)
        ▼
   hash unchanged ──▶ "= (note unchanged)", nothing written
   hash changed   ──▶ re.sub each span, byte for byte, everything else untouched
```

#### The four engine touch points, and why each was needed
`src/common.py` holds `PAGENAME` and `page_files()`, which decide what a page IS by NAME, so the prefix had to be added in both or the file stayed invisible.
`src/parse.py` gained a `meeting` branch beside `skill_m` and `agent_m`, giving the page its id, its kind, and a sort key that puts it after the Agent rows.
`src/page_question.py` composes the Opening's LEAD outside `body()`, which is the one place `<!-- haipipe:… -->` markers were not being dropped, so the first generated page printed its own marker as its opening sentence.
`check.py` had two assumptions to widen: its `## Pages` scanner matched only `[QS]` and `Agent-`, and its English-only rule had no reason to apply to a quotation of a meeting held in another language.

#### What is deliberately NOT in this code
It does not route, summarize, transcribe, or judge.
Routing is `Skill-5-haipipe-board-routing`'s verb, summarizing already happened in the vault, and a generator that started interpreting the meeting would be a second summarizer to keep in step with the first.

## Items to Finish
### The decision this face owes
- [ ] 🧠 Rule how a meeting note enters the board
      The options and their costs are in `Where we are`; nothing below can start before this.

### The artifact half
- [x] 🗂 Define the Meeting page kind
      Three managed spans (`head`, `diagram`, `body`) and everything else authored, which is `QC3a`'s split with the seed line drawn where ticking happens.
      The transcript is embedded as the last Content division, inside the managed span.
- [x] ⚙️ Generate it
      `meetingpage.py new|sync` ships; `Meeting-1-260723-boardform-demo.md` was generated from the real note and renders all six base sections.
- [ ] 🔢 Decide whether a Meeting page counts
      Skill and Agent pages sit outside the settled-question count; a Meeting page almost certainly should too, but the Index and Section Matrix both need telling.

### Where it sits, and how you watch for new ones
- [x] 📍 A meeting page lives in its own group, `QG · Meeting`
      Ruled in two steps (JL): first out of the engine group, then into a group of its own, because this series ACCUMULATES.
      A roster of shipped units has a natural size and can sit inside a topic group the way `Skill-N` sits inside `QC`; a history of meetings does not, and would slowly drown whichever group hosted it.
      This face stays in `QC · Engine` (JL 260801: "we have QC3b, it is the meeting to explain how the meeting are working"): the machinery is engine work, the meetings themselves are not.
      `meetingpage.py` now defaults `--group QG`.
- [ ] 🎙 Give the Index a Meetings fold
      A fourth fold beside Board Map, Section Matrix, and Related Folders: every note this board knows about, its state, and the button that imports or resyncs it.
- [ ] 📡 Say where notes come from
      Today only the board's own `meeting/` folder is read; a vault folder would have to be declared, the way `## Related Folders` declares its folders.

### The consequences half
- [ ] 🧭 Route one real meeting end to end
      Take `260723-meeting.md`, extract its decisions, and land each one on the Q that owns it with a citation back to the meeting page.
- [ ] 📐 Write the routing rules down
      What a routable line looks like in a summary, and what happens to a decision whose Q does not exist yet.

## Where we are
Opened 260731 when JL asked how meeting notes could go on the board, and the artifact half shipped the same evening.

- 260731 JL · 🗂 `Meeting-<n>` is a page kind, and it fits the base page exactly
  JL ruled the shape: a special page like `Skill`, still the base structure.
  It needed three changes in the engine and one new script: `PAGENAME` and `page_files()` learned the prefix, `parse.py` gained a `meeting` kind that sorts after Agent, and `meetingpage.py` reads an echo-meeting note into the page.
  The mapping is a lookup rather than an interpretation, because the summarizer's prompt fixes its six headings: TL;DR becomes the Opening, its ASCII figure becomes the Diagram, Key Points and Decisions and the Conversation chapters become Content divisions, and the transcript is the last division.
  `Meeting-1-260723-boardform-demo.md` was generated from the real note and renders all six sections, 18 Content divisions, and 15 sentence drawers, because an Obsidian `[!quote]-` callout becomes exactly this board's sentence apparatus: click a chapter's summary line and the words that produced it open underneath.
  Two defects surfaced and both are fixed: the lead sentence was composed outside `body()`'s marker filter, so the first generated page printed its own managed marker as its opening line, and `check.py` did not know the new filename, so a correctly listed page was reported as unlisted.

- 260801 JL · 🗂 Meetings became the seventh group
  JL: "we might have a new QG named Meeting, and we can make the meeting session, about different meetings we have."
  `QG · Meeting` now holds `Meeting-1`, and the board renders it as a real group: an Index block, a rail section, and its own `board/QG/` folder in the tree.
  The argument for a group rather than a few rows inside another one is accumulation: `Skill-N` and `Agent-N` are a roster with a natural size, and a history of meetings has none.
  A first attempt also moved this face to `QD8`, which JL reversed on the spot: the machinery of importing a note is engine work, so the question stays in `QC` and only the meetings themselves live in `QG`.

- 260731 CC · 🈶 A meeting page is exempt from English-only, on purpose
  The imported note is 8,573 Chinese words and the rule (JL 260724) is about the prose this team writes, not about a meeting that happened in the language it happened in.
  Managed spans were already skipped by the checker; the two SEEDED lists are outside them by design, because you tick action items and a resync must never eat your ticks.
  So `check.py` now exempts `Meeting-<n>` pages from the CJK and em-dash rules, and the page reports zero warnings rather than 26.

### Decision Now
- [x] 🧠 Rule how a meeting note enters the board
      **B, and C next** (JL 260731: "the MEETING-page should be a special page like SKILL, but still fit the Basic page structure"). The page kind is built; routing is the open half below.
      A · Related Folders only, which works TODAY: declare `meeting/` in `## Related Folders` and the note opens from the Index in one click, embedded at build, no new machinery, no page, no routing.
      B · A Meeting page kind, generated like `Skill-N`: the meeting gets a real page with a sidebar row, a chat, sentence rails, and a link anyone can cite, and the transcript stays folded inside it.
      C · Routing only: read each meeting, land its decisions on the Q pages that own them, and leave no meeting page behind, so the board holds consequences and the vault holds the record.
      D · B and C together: the page is the citable source, the routed lines are the effect.
      → CC recommends D, and A tonight as the stopgap, because A costs one paragraph in `board.md` and can be thrown away the moment B lands; on its own, though, A is an archive nobody opens, and C on its own leaves every routed line pointing at a meeting the board cannot show.
- [ ] 🎙 Rule the Meetings fold on the Index
      The state each row needs is FREE: `meetingpage.py` stores the note's hash in the page's own marker, so not-imported, in-sync, and note-changed-since-import are all decidable at build.
      A · a fourth Index fold listing every note with its state, plus an import or resync button that calls the live layer; with scripts off the list still renders and only the buttons go quiet.
      B · no fold; a meeting is just another page row in `QD`, and importing stays a command you type.
      C · the fold, but read-only: it reports state and never writes, so importing stays deliberate.
      → CC recommends A, because the thing you asked to monitor is exactly the state that is already computable, and a board that can tell you "this note changed since you imported it" is the only version of this that stays honest a month from now.
- [ ] 📼 Rule where the RAW transcript is shown
      Measured on the real note, the two are not the same material: the chapters carry 250 lines of CURATED quotes, and `## Transcript` carries 1,024 lines of raw ASR (`[0:08] 🎙️ S1 Hello.`).
      Today the raw half is the last Content division, which puts reference material inside the reading path.
      A · move it below the reading path, into the fold region `QB4g` owns, where Law, Glossary, Discussion and Log already sit; the renderer needs to accept one more fold name.
      B · leave it as the last Content division, which costs nothing and is already folded shut.
      C · keep only the curated quotes on the page and link to the vault note for the raw lines, which makes the page unreadable offline.
      D · slice the raw lines INTO their chapters: every chapter carries `[00:23-07:00]` and every raw line carries `[m:ss]`, so the split is deterministic and each chapter's drawer could hold its own raw run.
      → CC recommends A now and D later: A is a small change that puts reference material where reference material goes, and D is the version worth having, because a raw line is only ever wanted next to the moment it belongs to.

## Files
### Engines
- `../../board/haipipe-board/src/common.py`
  `page_files()`, the name-prefix discovery rule that makes `meeting/` invisible; a Meeting kind is a change here and in the page renderer.
- `../../board/haipipe-board/skillpage.py`
  The existing folder-to-page generator with the managed/authored split a meeting page would copy.

### Input files
- `../meeting/260723-meeting.md`
  The real note this face is written against: 8,573 words, `type: meeting`, `source: echo-meeting`.
- `../board.md`
  Where a `## Related Folders` entry would go for option A, and where a Meeting page would be listed for option B.

### The producing end, outside this repo
- `jluo41/echo-meeting` · `main.ts`
  The whole plugin, 1,657 lines: recording, the live Azure path, the batch path, and `noteMarkdown` / `replaceSection`, which decide the note's anatomy this face has to read.
- `jluo41/echo-meeting` · `py/echo_summarize.py`
  The system prompt that FIXES the six summary sections, so `### Decisions` and `### Action Items` are a contract rather than a habit. Changing it changes what a board can route.
- `jluo41/echo-meeting` · `py/llm_engine/`
  Router plus three transports (`claude_sdk` OAuth through `~/.claude`, `claude_api`, `codex_oauth`); secrets come from a sourced `env.sh` and never from `data.json`.
- `jluo41/echo-capture`
  macOS helper: far-end audio through a CoreAudio process tap, spawned by the plugin and read over a local websocket.

## Log
260801 0140 · Full renumber QC5b -> QC3b (JL forced 260801)
260801 0130 · Reindexed QC10 -> QC5b under the new QC5 generator parent (JL 260801)
260801 · `QG · Meeting` opened as the board's seventh group and `Meeting-1` moved into it; the group renders on the Index, in the rail, and as its own `board/QG/` folder in the tree. This face stays in QC. `meetingpage.py --group` defaults to QG
260731 2205 · `Meeting-<n>` page kind SHIPPED: `meetingpage.py new|sync`, three managed spans, Items and Decision Now seeded once; `common.py` + `parse.py` learned the prefix, `check.py` learned the filename and exempts a meeting from English-only, and `page_question.py` stopped printing a managed marker as the lead sentence. Meeting-1 generated from the 260723 note: 6 sections, 18 divisions, 15 sentence drawers, 0 warnings
260731 2130 · Read the producing end's source (`main.ts` 1,657 lines + 5 python modules): §4 records the pipeline, the section-boundary write discipline it shares with QC7, and the finding that the summarizer's prompt FIXES six sections, so Decisions / Action Items / Open Questions / Diagram map onto board constructs without interpretation
260731 · Opened when JL asked how meeting notes get onto the board; `meeting/260723-meeting.md` has been on disk since 260723 and invisible to `page_files()` the whole time. `jluo41/echo-meeting` + `jluo41/echo-capture` identified as the producing end
