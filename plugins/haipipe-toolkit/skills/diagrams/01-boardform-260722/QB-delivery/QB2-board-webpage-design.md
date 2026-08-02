# Board-Webpage design
state: 🟡 PARTIAL
owner: JL
method: distinguish the Board-Webpage-Index from an opened Board-Webpage-Page, then settle what the Index must answer and how the shared surface makes it legible
session: d2199106-8b6a-499d-8c24-9db3658486b5

## Opening
How should the Board index help a reader choose the right page within three seconds?

This page defines the Index information hierarchy and the visual language shared across the Board webpage.
The hard part is showing groups, state, ownership, progress, and relationships without turning the Index into a wall of detail.
If those signals are poorly balanced, only the author can tell what is stuck or whose move comes next.
The design succeeds when a cold reader can point to the next actionable page within three seconds.


## Boundary
- ✅ Covered here
  **The Board-Webpage-Index**: Board-level Topic, Pipeline, Board-Structure, group headers, what each row shows, the visuals of state and completion, sort rules, the structure controls, the Board chat entry, the ACTIVITY block, and how "see at a glance what to act on" is achieved.
  **The board's visual design read**: density and motion settings, typography and surface consistency, accessibility checks, and the audit-first adoption protocol that governs any of it changing.
- ↪ Covered elsewhere
  The **Board-Webpage-Page** after the click: `QAa0` and the QAa faces, one per section.
  Whether each question's **prose is well written**, and the mechanical checks after any change: `QA9`.
  Automatic **group-title emoji** selection: `QAa3`, which carries the group-title marker (absorbed from QD4 on 260726, moved 260729).
  Which folder the board **lives in**: `QB1` (which absorbed QC1 on 260729).
  Paper and venue **writing style**: the Paper lifecycle.

## Diagram

```
Board-Webpage-Index (top of board.html; no page opened yet)
┌──────────────────────────────────────────────┐
│ board name · 🦴 spine · 🏁 close condition    │
│ ▓▓▓▓▓░░░░░  N/M settled                      │  progress bar
├──────────────────────────────────────────────┤
│ 🗺 Board Map                                  │
│ ┌──── QB1 ────┐   owns    ┌──── QAa0 ────┐   │  one canvas,
│ │ folder form │ ────────► │ page contract│   │  one box per page;
│ └─────────────┘           └──────┬───────┘   │  arrows are authored
│                                  owns          │  relationships only
│                           ┌──────▼───────┐   │
│                           │ QAb0 sentence│   │
│                           └──────────────┘   │
│ [read-only · pan/zoom]  [✏️ Edit map]         │
├──────────────────────────────────────────────┤
│ QA · Defining a board            [＋Q] [🗄]  │  group header (hover controls)
│ ▸ Pin down the thing itself; nothing …       │  ← group intro: one sentence,
│   (click ▸ → expands: what / why this group) │    click to expand the why
│  ✅ QB1  Board folder shape        🔧 CC      │  ← what does each row show?
│  🟡 QAa0 Page overall: shared layout  🔧 CC  7/9 │     how is completion colored?
│  🔴 QAa3 group-title icons        🗄 🔧 CC  0/4 │     hover 🗄 = archive (2-click)
│  …                                            │
│  [＋ Group]                                   │
├──────────────────────────────────────────────┤
│  … all the page cards …                      │
├──────────────────────────────────────────────┤
│ ACTIVITY   (absorbed from QE2, 260726)       │
│  WHEN  14 days   ▁▁▁▂▇▄▅▅  outer = all boards│
│                            inner = this one  │
│  WHERE Board → Group → Page, one count each  │
│  the unit is ONE UPDATE = one dated ## Log   │
│  line, so it reads every tool, not a tab     │
└──────────────────────────────────────────────┘
         ↑ within three seconds: "which question do I act on?"

  every button is only a writer into board.md:
  ＋Q       creates QXN-slug.md from the house stub + lists it under its group
  ＋Group   appends "### QX · title" (+ intro line) to ## Pages, letter auto
  🗄        moves the file to _archive/ (question) or removes an EMPTY group;
            nothing is ever deleted, and the md stays the single source of truth
```

```text
how a visual change is allowed to happen

external taste rules
        |
        v
scope filter: research control plane, not marketing page
        |
        v
read-only audit of index, page, chat, mobile, dark, and no-JS
        |
        v
at most three isolated prototypes
        |
        v
human comparison
   | adopt                 | reject
   v                       v
board specification      this face records
and QA9 checks           why it does not fit
```

/_excalidraw/?board=Tools/plugins/haipipe-toolkit/skills/diagrams/01-boardform-260722/board.excalidraw&frame=QA10

## Content
### 1 · Board-Webpage-Index and Board-Webpage-Page
The Board-Webpage is one generated `board.html` with two reader views.
The Board-Webpage-Index is `#top`: it gives the Board name, Spine, Close condition, progress, its Board Map, the Section Matrix, grouped page rows, and Activity before showing any individual page.
Topic, Pipeline, and Board-Structure left the rendered Index on 260731 (JL: "I want to just remove this"); their `board.md` sections remain source-only documentation, because the spine, the Board Map, and the matrix already orient a reader.
A Board-Webpage-Page is a focused `#<page-id>` view inside the same document.
This face owns the Index and shared visual language; the QAa faces own the opened Page's sections.

### 2 · Overall progress, show how far the board has moved
The global progress area reports settled Q decisions and passed S gates as separate workflow signals.
It answers "how far along is this board?" without implying that a paused page is complete or allowing lifecycle stages to inflate question settlement.

### 3 · Group, explain why these pages belong together
Each group header names one coherent part of the board and carries a short, always-visible introduction.
Opening the introduction reveals what the group is for and why it exists.
Group controls add a Q or archive an empty group, but the explanation remains the primary reading signal.

### 4 · Page row, identify the next action
Each row exposes only the evidence needed to choose whether to open it: workflow state, id, title, open-comment signal, owner, and finish ratio.
Its most important eventual job is to make "which page needs action, and whose action is it?" answerable within three seconds.

### 5 · Ordering, make priority legible
Group order and row order tell the reader what to scan first.
Today they follow the hand-written Pages; the open design decision is whether state, unfinished work, owner, or open comments should influence that order.
Any automatic sort must remain explainable and must not silently rewrite the source.

For a paper lifecycle board, ordering has one stronger rule: named S families are the groups.
The index follows `Seed → Work → Venue → Display → Main → Appendix → Submission`, but this is stable ownership order, not a claim that execution is linear.
Pipeline owns actual edges and may revisit the independent Display layer after Narrative.
Each S row is one concrete checkable page, and a blocking Q sits immediately after the S page it governs.
Seed includes S Seed and S Literature; Main and Appendix expose every reader-facing unit instead of hiding them inside one broad section-edit stage.
A paper-level decision may sit before Seed only when it genuinely governs the full lifecycle.

### 6 · Structure controls, edit without hiding the source
`＋Q`, `＋Group`, and archive controls are page-side writers into `board.md` and the page files.
They make the index operational while preserving markdown as the single source of truth; archive moves material rather than deleting it.

### 7 · Board chat, discuss the board as a whole
Board chat is the place to ask how the work should proceed or which page to examine next before opening one.
It supports deliberation, but it cannot replace the index's visual three-second answer because a reader should not need a conversation to discover the next action.

### 8 · Activity, count what changed, and where
(absorbed from QE2 on 260726; the index closes on the measure of itself)
The ACTIVITY block sits below the page cards, so the board's content leads and the measurement of that content closes.
It answers two questions in that order: WHEN did the work happen, as a fourteen-day strip, and WHERE did it go, as Board → Group → Page.

#### The unit is one update, not one minute
(JL 260726: "I don't care about the time. What I care is about the numbers of updates.")
One update is one dated line in one page's `## Log`.
The first version of this measured focus time from the browser: visible non-idle spans, five-minute idle stops, per-day allocation at local midnight.
It was exact and it was measuring the wrong thing, because the timer could only ever see a browser and most work on these boards arrives through Claude Code or an editor.
A Log line is written by whoever did the work in whatever tool, and it already carries its own date, so counting them is a record rather than an observation.
That difference is why the switch recovered days of history the timer could not have: a timer cannot observe a session that already ended, while the Logs were there the whole time.
Nothing else is read, and in particular not `## Where we are`, which also carries dated lines but is status prose rather than a change record; counting both would count one change twice.

#### What the ranking is for
(a count per page is only useful if it can be compared with its neighbours)
Board rows share one scale and the current board's Group and Page rows share a second, so a short page stays legible when another board dominates.
Indentation carries ownership and bar length carries the count, which is the same grammar the index itself uses.
The strip's outer bar is every board and the inner bar is this one, so a day answers "was the work here or elsewhere" without a second chart.

### 9 · The board's design read, and its dials
Read this as an expert research control plane for long-form reading, fast state scanning, and durable collaboration.
The visual language should feel calm, exact, and academic rather than cinematic or promotional.
The interface must remain useful with JavaScript removed, and visual variation must never obscure state, ownership, dependencies, or completion.

The proposed starting dials are:

```text
DESIGN_VARIANCE   3 to 4   stable hierarchy with limited asymmetry
MOTION_INTENSITY  1 to 2   feedback and state transitions only
VISUAL_DENSITY    7 to 8   compact control plane with readable prose
```

These are a proposal for JL to settle, not current board law.

### 10 · What the current surface already gets right
- One blue accent carries links and interaction while red, amber, green, and gray keep semantic state roles.
- Light and dark palettes use the same hierarchy rather than changing visual language halfway through the page.
- The 820px reading surface, serif prose, sans UI chrome, and monospace identifiers give content and control different voices.
- Motion is currently limited to short hover and disclosure feedback rather than decorative animation.
- Generated HTML stays readable when all scripts are removed.

### 11 · Initial audit signals
- `board.css` had a narrow `:focus-visible` rule for two chat-header buttons, but no shared
  treatment for links, disclosures, form fields, or the rest of the controls.
  Keyboard location was therefore not yet a consistent design primitive.
- It has no `prefers-reduced-motion` rule.
  Existing transitions are short, but the rule should exist before richer live controls arrive.
- Rounded bordered surfaces appear at many nested levels: spine, context, index row, slide, boundary, files, comparison column, chat, and comments.
  The focused page and its major inner sections already remove these frames, preserving QAa0's
  unframed reading intent; the index and all-page views still need visual comparison before
  any further surface reduction is justified.
- Radius values range across several unrelated numbers and full pills.
  A small semantic radius system may make the interface more coherent without flattening useful distinctions.
- Metadata commonly falls between 10.5px and 12.5px.
  Density is intentional, but keyboard labels, state text, and secondary controls still need a legibility check.
- Color contrast is designed by eye and has not been recorded as a mechanical acceptance check.

This is a source-level first pass, not a completed visual or accessibility audit.

### 12 · Rules worth borrowing, and rules that do not fit
Worth borrowing:
- Infer the page kind, audience, and constraints before changing visual style.
- Audit before editing and preserve existing interaction behavior.
- Use a small, explicit type, color, spacing, and radius vocabulary.
- Treat cards, borders, shadows, and motion as semantic devices rather than decoration.
- Check contrast, focus visibility, reduced motion, responsive behavior, and all interaction states before shipping.
- Compare a real before and after instead of accepting a persuasive design description.

Does not fit this board:
- No AIDA page structure, hero section, pricing CTA, image-first composition, or marketing-page storytelling.
- No mandatory GSAP, scroll pinning, cinematic motion, or randomized layout selection.
- No default `8 / 6 / 4` dial settings.
- No blanket emoji ban.
  Board icons carry authored information and are already governed by the page grammar.
- No new font, framework, icon, motion, or design-system dependency merely to satisfy an aesthetic preference.
- No change that makes hidden JavaScript necessary for reading the complete board.

The default external skill explicitly says it is not for dashboards, data tables, or multi-step product UI, so its rules can inform this audit but cannot govern it unchanged.
The redesign variant is the closer model because it begins with scan, diagnose, and targeted fixes.

[taste-skill repository](https://github.com/Leonxlnx/taste-skill)
[default v2 skill](https://github.com/Leonxlnx/taste-skill/blob/main/skills/taste-skill/SKILL.md)
[redesign skill](https://github.com/Leonxlnx/taste-skill/blob/main/skills/redesign-skill/SKILL.md)

### 13 · The pilot, and what it verified
Run the first pilot on this board itself.
Capture the index, one dense Q page, the chat drawer, mobile width, and dark mode before changing CSS.
Prototype no more than three changes in one pass: visible keyboard focus, a semantic radius vocabulary, and a reduced-motion fallback.
Do not change content structure or interaction behavior during the visual comparison.
Keep a change only if a fresh reader scans state faster, reads the page comfortably, and can still identify every boundary the old styling communicated.

Verified 260726:
- Desktop computed width remained `1440 / 1440`; the focused page kept `border: none`,
  `border-radius: 0`, and a transparent background.
- At `390px`, document and body scroll width both remained `390px`.
  Only preformatted diagrams were wider, and they retain their intentional local horizontal scroll.
- One Tab from the page start landed on the Topic disclosure with a solid `3px` focus ring,
  `3px` offset, and the dedicated light-mode focus color `rgb(7, 95, 189)`.
- Emulated reduced motion matched successfully and reduced both transition and animation duration
  to `0.01ms`.
- Light, dark, focused-page, index, and mobile screenshots rendered without visible regression.
- All seven active boards rebuilt successfully, and every build reported that its body survives
  with JavaScript stripped.

The broader baseline audit remains open because chat and comment interaction states have not yet received the same full visual comparison.

### 14 · After a page opens
This face stops at the index and at the shared surface.
`QAa0` owns the opened Q/S webpage's order, and since 260729 each section has its own QAa face: Opening (`QAa1`), Diagram (`QAa2`), Content (`QAa3`), Items to Finish (`QAa4`), Where we are (`QAa5`), and the folds (`QAa6`).
The two specifications use the same principle without mixing their responsibilities.

### 15 · Board Map, see relationships before scanning rows
The Board-Webpage-Index shows the Board's declared Board Map canvas directly below progress and above the text folds and page rows.
Each box represents one actual Q or S page; the canvas is the visual map of those pages, not a second page registry.
An arrow means a relationship someone deliberately drew and labelled: for example, *defines*, *governs*, *requires*, or *ships*. Nearby boxes and index order mean nothing by themselves.

The Index uses its local `board.excalidraw` scene by default when served through the live Board server. A Board on a static host may instead declare a shared `board-map:` URL; this Board uses its shared Excalidraw canvas so the map is available through the Tailscale reader URL. The Index still has its text list underneath: it remains the accessible, searchable, action-oriented entry point; the canvas answers a different first question, “how do these pages relate?”

This first surface deliberately does not infer arrows from `## Pages` or `## Pipeline`, and it does not make a frame click open a page. Both would require a settled relationship grammar and interaction contract rather than a visual guess.

### 16 · Related Folders, open a related folder from the Index
A third Index fold, peer to the Board Map and the Section Matrix, lists the folders this board TOUCHES rather than the pages it contains, so a reader can see the engine that ships the board and what a board folder itself looks like without leaving the Index.
It surfaces `QA0`'s three-folder argument as a working panel: the skill family that renders the board (`skills/board/haipipe-board/`, with `SKILL.md src/ assets/ ref/`), this board's own folder (`01-boardform-260722/`, with `board.md`, its group folders, `board.excalidraw`, `fig/`, and the generated `board.html`), and the sibling boards the same engine renders.
Two depths are possible and unruled: a static folder tree that only shows structure, or a browser whose folders open to reveal a file's content such as `SKILL.md`. The Decision Now row settles which.
The panel is authored, not inferred: which folders count as related and what each contains comes from `QA0` and `board.md`'s `## Links`, never from guessing.

## Items to Finish
### The Index's components, from group intros to the Board Map
- [x] 📖 Each group introduces itself on the index
      A short sentence always visible under the group header; clicking it expands the "what this group is for and why it is here" body.
      Grammar (260724): in `## Pages`, plain lines between a `### ` heading and its first `.md` line are the intro; line 1 is the sentence, the rest is the expandable body.
      Rendered as a native `<details>`, so the strip-scripts invariant holds; every group on this board carries one now.
- [x] 🧱 Groups and questions can be added and archived from the page
      JL 260724: "add and delete question groups, and add and delete question items."
      Shipped as one writer, `POST /_board/structure` (ops `add_group` / `add_question` / `archive_question` / `archive_group`) living in serve.py and imported by the console (QE3 Law). ＋Q seeds a stub Q file and lists it under its group; ＋Group appends a `### QX · title` heading with its intro; archive MOVES a question to `_archive/` and only removes a group once it lists nothing.
      Verified 260724: full add to archive round trip leaves board.md byte-identical, refusal paths clean over HTTP on 5599 and through the console on 8093.
- [x] 📚 Every index component explains its purpose
      Content now describes the eventual reader outcome for board orientation, overall progress, groups, page rows, ordering, structure controls, and board chat.
      The opened-page section meanings stay with the QAa faces so this face remains an index specification.
- [x] 🗺 The Index opens with the Board Map canvas
      The top view embeds the Board's declared canvas below progress and above the textual index. Each box is one Q/S page. A live Board server uses the local `board.excalidraw` scene; this static Tailscale Board uses its declared shared Excalidraw canvas.
      This is intentionally not an automatically inferred dependency graph: arrows are authored, labelled relationships, while proximity and `## Pages` order carry no relationship meaning.
- [x] 🗂 A RELATED FOLDERS fold, peer to the Board Map and Section Matrix — shipped 0.87.0
      Opens the folders this board touches, not the pages it contains: the shipping engine `skills/board/haipipe-board/` and this board's own folder shape, sourced from `QA0` and the new `## Related Folders` grammar in `board.md`.
      Shipped as a build-time embed (`related_folders()` in `src/page_board.py`), so clicking a folder then a file reads it inline with scripts stripped and on a static host; renders in both `board.html` and the `board/` tree; two folders, four files embedded on this board.
### The Index's reading design: order, rows, coloring, the three-second answer
- [ ] 🔗 Settle the Board Map's arrow vocabulary and page-opening interaction
      Decide the small stable set of relationship labels (for example `defines`, `governs`, `requires`, `ships`) and whether a frame should open its Q/S webpage. Until that is settled, the map remains a readable relationship surface and the text index remains the action navigator.
- [ ] Settle the questions the front page must answer
      At least three: what is this board doing · how far along is it · **which question do I act on now**.
      The third is the hardest and the one that matters.
- [ ] Settle what each row shows
      Today: state · id · title · open-comment badge · owner · completion coloring.
      Enough?
      Too much?
- [x] Settle lifecycle grouping; keep ordinary-board sorting open
      Paper lifecycle boards use seven full-name families: Seed, Work, Venue, Display, Main, Appendix, and Submission.
      Display owns the evidence-presentation layer consumed by Main and Appendix.
      Each S is one page; its blocking Q follows it.
      Ordinary boards still use hand-written Pages groups, and automatic priority sorting remains undecided.
- [ ] Settle how completion coloring reads
      Today white to green by tick ratio. ⏸️ ON HOLD also renders full, easily misread as "done".
- [ ] A zero-background person points at the right question within three seconds
      Same acceptance as `QAa0`: a fresh agent sees only the front page, is asked "which question to act on", and must answer correctly.

### 📊 Activity (absorbed from QE2, 260726)
- [x] 📅 The strip answers WHEN, the tree answers WHERE
      Fourteen days across the top, then Board → Group → Page beneath, which are two different questions and therefore two blocks rather than one clever chart.
- [x] 🧮 The unit is an update, counted from `## Log`
      One dated Log line is one update; nothing else is read, so a change is never counted twice.
      Measured 260726 across the whole repo: 509 updates on 8 boards over 129 pages, with this board at 300 across 5 days.
- [x] 🕰 The days before the dashboard existed are not empty
      This was the failure the timer could not fix: it began on 260726 1915 and 245 dated Log lines from 260722 to 260725 were invisible to it.
      Counting Logs recovers all of them, which is the argument for the unit, not a side benefit of it.
- [x] 🧭 Activity closes the index rather than opening it
      It renders after the page cards, so the board's content leads.
- [ ] 🧠 JL rules what happens to the timing recorder
      `serve.py` still records browser spans into `.haipipe-board/activity.sqlite3` and nothing reads them any more.
      Three ways out: delete the recorder and its schema, keep it silently for a later "who is looking at this board right now", or keep it and show it as a secondary readout.
      Recommend deleting: a measurement nobody reads is a maintenance cost that looks like a feature, and the six regression tests now protect a number the page does not print.

### 🎨 Visual design (the former QA10 half)
- [ ] 🎛 Set the board design read and dials
      JL accepts or revises the proposed `3 to 4 / 1 to 2 / 7 to 8` starting point.
- [ ] 📋 Freeze the borrow and reject lists
      Decide which external taste rules may enter the board audit and which remain permanently out of scope.
- [ ] 🔍 Complete the baseline audit
      Inspect index, focused page, chat, comments, mobile, dark mode, keyboard flow, and the script-stripped page with screenshots and concrete findings.
- [x] 🧪 Prototype at most three changes
      Added one shared high-contrast `:focus-visible` ring, four radius tokens
      (`inline`, `control`, `surface`, `pill`), and a `prefers-reduced-motion` fallback.
      No markup, information architecture, or dependency changed.
- [ ] 👁 Compare with fresh readers
      Ask one fresh reader to locate the next open item and explain one dense page before and after, then record what improved and what regressed.
- [ ] 📐 Graduate or reject each rule
      Adopted display rules move to `ref/board-form.md`; mechanical acceptance checks move to `QA9`; rejected rules remain recorded here with their reason.

## Where we are
**The Board-Webpage-Index is now a place you can WORK and understand, not only view: its Content subsections explain what every component is eventually for; the Board Map canvas now appears before the page rows to make page relationships visible; paper lifecycles use seven readable S-family groups; the structure itself is editable from the page; and the Index carries its own chat. Board-Structure now appears after Pipeline rather than consuming a Q webpage. The reading design questions (arrow vocabulary, sort, coloring, the three-second test) stay open, and so does the visual baseline audit.**

- 260731 CC · 🗂 RELATED FOLDERS shipped (0.87.0, depth B)
  A third Index fold, peer to the Board Map and Section Matrix, opens the folders this board touches (the shipping engine, and the board folder itself); clicking a folder then a file reads it inline.
  Built as a build-time EMBED rather than JL's literal "serve.py serves content live", because a live fetch breaks the script-stripped/static-host Law (QE3): `related_folders()` reads each listed file at build, refuses paths outside the repo root, inlines only `.md`/`.txt` under 120 KB, and shows every failure as a visible box. Renders in both `board.html` and the `board/` tree; the rail gained a 🗂 Related Folders row. Verified: order Board Map → Related Folders → Section Matrix, four files embedded, zero failures, body survives JS stripping. QC8's live endpoint is deferred for oversized folders.

- 260731 JL · 🗂 RELATED FOLDERS depth ruled: B, the clickable browser
  JL: "do the B level." The fold opens to a real file's content on click (for example `SKILL.md`), not just a static tree.

- 260731 JL · 🗂 A RELATED FOLDERS fold requested for the Index
  JL, with a screenshot of the Board Map and Section Matrix folds: add a third fold, "related folders", that opens the folders this board touches so a reader can "看到 skill board 的那个东西，也可以看到这个 board folder 该长什么样子" (see the shipping skill, and what a board folder itself looks like).
  Recorded as Content §16, an Items row, and a Decision Now depth ruling: a fold peer to the Board Map and Section Matrix, sourced from `QA0`'s three folders and `## Links`. The depth (static tree vs clickable browser) is unruled; the render lives in `src/page_board.py`, so wiring it needs an engine change beyond a board-folder-only edit.

- 260731 JL · 🧹 Topic, Pipeline, and Board-Structure left the Index
  JL, quoting the three disclosure headings: "I want to just remove this."
  The renderer no longer emits the three `ctx` disclosures; `board.md` keeps `## Topic`, `## Pipeline`, and `## Board Structure` as source-only documentation, and nothing else read them.
  The Index now reads spine → Board Map → Section Matrix → ALL PAGES → Activity, and the rail's Index outline lists exactly those components.
- 260731 JL · 📇 The Index row unfolds in the rail
  JL: "for the left panel headings, what should be the index's section content? Please add them as well."
  The `🗂 Index` row now carries the same chevron and outline as a page row: 🗺 Board Map, 🩺 Section Matrix (with its page × column count), 📄 All Pages (with the page count), 📈 Activity, each present only when the board has it, each scrolling the Index to that component.
  It unfolds by default when the board opens, since the Index is the open "page" at load.
- 260731 JL · 🩺 The Index gained the SECTION MATRIX
  JL: "We want to have a dashboard to show the status of the board. Each row is a page, each column is a subsection. the cell might be some status."
  Shipped in haipipe-board 0.75.0 as a shut-by-default disclosure between the Board Map and ALL PAGES: one row per page, one column per section, every cell computed at build from the same parses the pages render from, so the matrix is derived and can never disagree with a page.
  The cell vocabulary: 🧭 present, 🖼 figure and canvas counts, 📚 `n÷·m🖼` divisions and how many open with their face diagram (the QB4c retrofit watched from one column), 🎯 `done/total`, 📍 `DN·k` owed Decision Now ticks or `e` dated entries, 📎 files and groups, 🗄 Log lines.
  A cell is a link: click it and the page opens scrolled to that section; amber marks incomplete, accent marks waiting-on-JL, muted marks absent.
- 260731 JL · 📑 The webpage gained a hideable pages sidebar
  JL: "I also think to added the sidebar so I can choose the pages more easier ... like the side bar, and then index, QA, QA1, QA2, etc ... and that sidebar can be hidden as well."
  Shipped in haipipe-board 0.61.0: a fixed left rail listing Index, then every group with its pages (state emoji, id, title), rendered server-side from the same listing as the index rows so it needs no script to exist.
  It lives outside `.wrap`, so the `:target` show/hide rules never touch it and it stays up in both the Index view and an open page; a group link re-targets `#group-…`, which also brings the Index back on stage.
  The ☰ toggle hides or shows it, the choice persists per board in localStorage, and with no saved choice it defaults open on wide screens and hidden on narrow ones; a jump on a narrow screen closes the overlay without persisting.
- 260730 JL · 🅰 The Board Map became ASCII, and a disclosure
  JL: "what is the section for board map?
  I think I might need the ASCII version.
  Please try it. and make it collapsable." `## Board Map` is now a board.md section holding one ``` figure, and it WINS over both canvases.
  The reason is reach: a figure draws on a static host with no Excalidraw endpoint and no share URL, it survives with scripts off, and since 0.53.0 every page id and group token inside a figure is a real link, so an ASCII map is the only map a reader can travel on.
  It renders as `<details class="board-map board-map-ascii" open>`, because a map you cannot shut pushes the index off the first screen.
  The whole map head is the handle; the caret rides the BOARD MAP kicker.
  This Board's `board-map:` URL was deleted when the figure replaced it, so there is one declared source again, with the shared canvas kept as a link inside the section.
  A board with no `## Board Map` keeps the old iframe behaviour unchanged.

- 260730 CC · 🗺 Board Map landed at the top of the Index
  The Index now embeds the Board's declared relationship canvas immediately after overall progress. This Board points at its shared Excalidraw canvas so the static Tailscale reader can load it; live Board servers default to the local `board.excalidraw` scene. Connections remain authored rather than inferred, because page order is navigation and is not a dependency claim.

- 260729 JL · 🔗 QC2 merged in here, and the QC group is now fully dissolved
  JL: "You should merge QC2 to QA10? about the Index-UI-Design?"
  The two faces were one subject seen twice: QC2 owned what the front page must SHOW, and QA10 owned how the whole surface must LOOK, and neither could settle its half without the other's.
  QC2's eight index components became §1 to §8 and its two item blocks came with them; the visual read, audit signals, borrow and reject lists and pilot became §9 to §13.
  The id kept at that time was `QA10`, because the QC group dissolved on 260729 and its remaining pages moved into QA.
  JL renamed it `QA2b` on 260730 when Board-Webpage became the explicit second branch of Board-Structure; `QA10` and `QC2` remain Links aliases so earlier citations resolve.

- 260726 JL · 🎨 The index rows lost their coloured left stripe
  JL asked for the red and green bars down the left of the index to go.
  Removed: `.ir`'s 4px `border-left` and the four `.ir.todo/.wip/.done/.hold` colour rules. The row keeps its 1px border and its hover accent.
  Nothing was lost, which is why it was safe: every row already opens with the state emoji, so the bar restated the state in a second language, and stacked down a 27-row index the bars read as a chart rather than as a list.
  Two neighbours were deliberately left alone: the pale green completion wash on each row is different information (percent done, not state), and the page's own left stripe on `.slide.q` is a different surface.

- 260726 CC · 🧪 Applied the first reversible UI taste pilot
  Added global keyboard focus, semantic radius tokens, and reduced-motion handling.
  Kept the existing focused-page framing because the source audit showed it already satisfies the proposed unframed reading direction.

- 260726 JL · 🧮 The dashboard changed its unit, and QE2 folded in here
  JL: "for the activity dashboard, I don't care about the time. What I care is about the numbers of updates."
  The timer was exact about the wrong quantity: it watched a browser tab, and most work on these boards is done through Claude Code, so the thing it measured was not the thing that happened.
  Counting dated `## Log` lines fixed the measure and the history in one move, because a record does not have to have been present to be read later.
  QE2 merged into QC2 in the same round on JL's call, which is right on ownership grounds: the dashboard is a component of the index, and this face already owns what every index component is for.
  The parked half is honest rather than hidden: the span recorder still runs and nothing reads it, and its fate is the open item above.

- 260725 JL · 🖼 Display became an independent family
  Display now owns the claim-to-display map, accepted assets, captions, statistical labels, and Main/Appendix placement.
  Pipeline still places it after Narrative; Pages order remains navigation.

- 260725 JL · 🌱 Full-name paper lifecycle families
  The paper lifecycle now reads Seed, Work, Venue, Display, Main, Appendix, Submission.
  Seed contains S Seed and S Literature; every Main section and Appendix unit is its own page; reconcile, compile, review, and submit are explicit terminal pages.
  Temporary SM/SA abbreviations retired.

- 260725 JL · 🔄 Submission is a repeatable round
  Submission keeps four stable pages.
  External review reopens affected Work, Display, Main, or Appendix pages, then the paper runs the same reconcile, compile, review, submit sequence again.

- 260725 JL · 🧭 Stage-first exposed the family model
  The MISQ paper first exposed the weakness of broad QA/QB/QC buckets and moved to one group per stage.
  That intermediate form made the stable families visible; the current rule above supersedes it with seven full-name groups and one concrete page per S row.

- 260725 JL · 📚 Index anatomy made explicit
  JL asked for Content to explain what each webpage section is for.
  This face now defines its own index components and points to QAa0 for the opened Q/S page, keeping the ownership boundary visible.

- 260725 CC · 🤖 A chatbot on the index (JL's ask)
  The bottom-right button now shows on the index too, labeled "🤖 Board chat".
  It opens the same `QD2` drawer (and the ⌨ inside it is the same `QD3` terminal), just attached to `board.md` instead of one question, so "how should we work / which question next" can be discussed right on the index.
  The three-second VISUAL answer this question owes is still owed: a chat answer takes longer than three seconds.

- 260724 CC · 🧱 Structure became editable from the front page
  Per JL's ask: ＋Q on every group header, ＋Group at the list's end, hover-🗄 archive on rows and headers, all two-click confirmed, no native dialogs.
  The buttons are writers only: board.md's `## Pages` plus the Q files stay the single source of truth, `_archive/` keeps everything recoverable, and the live watcher (QD4) swaps the updated index in under you after each op.

- 260724 CC · 📖 Group intros landed with a new Pages grammar
  Intro lines sit directly under each `### ` heading in `## Pages`; the per-group paragraphs that used to live in `## Pipeline` moved there (Pipeline keeps only the overall narrative), so nothing is said twice.

- What the index looks like today
  Board name + spine + close condition + progress bar + two global fold-outs (what is this board / how are the Qs ordered) + the grouped list in `## Pages` order, each group led by its intro.

- What each row has today
  State badge · id · title · open-comment badge · owner · row tinted white to green by completion (`--fill`, percentage in `title`) · hover archive.

- Known defects
  ⏸️ ON HOLD renders as full green like ✅, reads as "done"; with many questions it is one long strip with no visible priority; group order is entirely hand-maintained in the Pages.
  No external skill has been installed and no dependency has been added.

- 260731 JL · 🎨 The Board Map header now matches the Section Matrix header
  JL: "could you make this cleaner? this is so ugly", then "make these two styles consistent", with a screenshot of the two sitting one above the other and looking nothing alike.
  The map's header was a two-column flex with a large title on the left and its blurb stranded right-aligned on the right, wrapping onto two lines; the matrix's was one compact line.
  The map now uses the matrix's shape exactly: one line, one triangle, same padding, weight and size, with the blurb dropped from the header because the body already opens with the same sentence.
  Two triangles were being drawn, and finding the second one took the browser rather than the source.
  The first was the `<summary>` disclosure marker, which `list-style:none` does NOT remove because a summary is `display:list-item` and Chrome draws it through `::marker`; only leaving list-item behind kills it.
  The second was a real `::before`, and the rule meant to suppress it had the SAME specificity as the generic `details[open]>summary::before` further down the file, so the generic one won on order alone.
  Both are now beaten explicitly, and the triangle that remains is one inline arrow on the header itself.

- 260731 JL · 🔁 The tree index was a THIRD reimplementation, and JL caught it by comparing
  JL: "the ASCII here has not become real ASCII", and "compare your configuration with the original .md one, there are big differences, look carefully."
  He was right on both counts and the cause was one thing: the tree's index and rail had been hand-written instead of reusing the builders `render()` already had.
  What that silently dropped: every `.gi` group-intro block, every `.gib` body, and all six `.gidia` figures, which are the per-group lane diagrams, so the ASCII was not rendering as ASCII because it was not being rendered at all.
  The rail lost its per-page section outline the same way, 54 `.sb-out` blocks and 298 `.sb-s` rows.
  Fixed structurally rather than patched: the index loop became `index_rows()` and the rail loop became `sidebar_rows()`, each taking an href function, and both packagings now call the same one.
  A class-by-class diff of the two indexes is the check: the only remaining differences are the progress bar and the ALL PAGES hint, both deliberate, and one rail row, because the tree's Index is its own document rather than a fragment.
  Third time this family's "one grammar, never two implementations" law has caught its author in one day, which is itself the argument for the law.

- 260731 JL · 🗂 A group is the one altitude with no template, and now it has half of one
  JL: "index has a template, page has a template, should the page GROUP have a template too? Opening a group shows only a list; can it also say what this group is for?"
  He is right, and this board states the gap against itself: the QB group intro declares the ladder Board to Group to Page to Section to Sentence, then lists faces for Board, Page and Sentence only.
  What a group owns today is thin and scattered: an intro in `board.md` under its `### ` heading, an anchor, a lane block, and since 0.77.0 a chat session. None of that is a template and none of it has state.
  Shipped now, from data that already existed: the group page renders its intro as a PURPOSE line, the remaining intro lines as a "why this group exists" drawer, and the group's own settled count. The intro was in `board.md` all along and the group page simply never read it.
  Not shipped, because it needs a source file and a parser slot rather than a render change: a group with its own `## Items to Finish`, its own `### Decision Now`, and a `state:` that can close.

### Decision Now

- [ ] 🗂 Rule whether a group gets a SOURCE FILE, and therefore a real template
      The group page now shows purpose, why, progress and members, all derived from `board.md`. That is the ceiling of what derivation can give: a group still cannot hold a decision, an open item, or a state of its own.
      A · a group gets its own markdown file with the page sections that make sense at group altitude (Opening, Items to Finish, Where we are with Decision Now), rendered as the group page, with the member list appended by the generator.
      B · the group stays derived, and anything a group needs to decide is written on whichever member page is closest.
      C · extend the `board.md` intro grammar instead, so a group can carry more without a new file.
      → CC recommends A, because a group is already the unit you click, a session attaches to, and a lane block describes, and the only thing it cannot do is close. Note what it costs: `src/parse.py`'s Q pattern requires a number, so `QA-index.md` is discovered and then fails to parse; the existing named-Q form `Q-<Name>-<slug>` already parses and is the cheapest slot.
      Also worth ruling in the same breath: if a group can close, does the board's settled count start counting groups, or stay pages only.
- [ ] 🗂 Rule whether a page group gets a PAGE of its own
      JL 260731: "for the Q group, we might have a QXX-index.md as well, but this is for the whole group, not the single page, and we can click the Group and open that page if we want."
      The gap is real and this board demonstrates it: the QB group intro declares the ladder Board to Group to Page to Section to Sentence, and then lists faces for Board, Page, and Sentence only, because the GROUP rung has no face.
      A group today owns four things and none of them is a page: an intro (plain lines under its `### ` heading), an anchor `#group-<token>`, a lane block, and since 0.77.0 a chat session.
      What it lacks is exactly the three affordances that retired the `doc:` line in 260726: no `state:`, no item counts, and no place for a comment to land.
      A · a real page per group, so a group closes, carries its own Items and Decision Now, and takes comments like any page.
      B · keep the intro and grow it, adding the missing affordances to the group heading itself without minting a page.
      C · leave it as is, and let group-level decisions live on whichever member page is closest.
      → CC recommends A, because a group is already the unit a reader clicks, a session attaches to, and a lane block describes, and everything on that list except closing is already built.
      One technical note that decides the naming, not the ruling: `src/parse.py`'s Q pattern requires a number, so `QA-index.md` is DISCOVERED by `page_files()` and then fails to parse into a group and id, landing in the ⚠️ group. A group page therefore needs a parser slot, not just a filename convention. The tidiest fit is the existing named-Q form `Q-<Name>-<slug>`, which already parses today.
- [ ] 🌐 Rule whether board.html stays one file
      JL 260731: "for the board.html, all the things are in the same .html, will that be ok? Could we make it like each page, we have each html? will that be much quicker and smoother?"
      Measured on this board: 2.02 MB total, of which shared JS and CSS are 0.20 MB (10%) and page content is 1.78 MB across 53 pages, so one page averages 34 KB and a reader downloads roughly nine times what the page they opened actually needs. The MISQ lifecycle board is 3.12 MB. A full rebuild is 0.38s, so the build is not the cost; the browser parsing 2 to 3 MB on every load and on every live swap is.
      A · one HTML file per page plus an index, which is what the question proposes.
      B · keep one file as the shareable artifact, and give the LIVE server a per-page fragment path so an update ships one page instead of the whole board.
      C · leave it, and accept the parse cost.
      → CC recommends B, and against A on its own merits rather than only on the law: page SWITCHING today is a pure CSS `:target` change with no network at all, so splitting into files would make the instant thing slower (a round trip plus a full document load plus re-running the scripts) to speed up the once-per-session thing, and it would destroy the chat drawer and terminal on every navigation, which is the entire point of `QD4`'s swap.
      B is also the only option that keeps `QE3`'s Law intact, that the static half stays one self-contained file a colleague can be handed and a projector can open offline.
      This is the page I proposed as `QC9` (the unit of change) and it is still unruled on `QA2`; JL asking it independently is the argument for opening it.
- [ ] 🩺 Confirm the SECTION MATRIX columns and cell vocabulary
      PROPOSED: seven columns (🧭 🖼 📚 🎯 📍 📎 🗄) with the cell codes recorded in the 260731 matrix entry above; a column can be changed or dropped without touching any page, since every cell is derived.
- [ ] 📌 Rule the matrix's default posture
      Recommended: shut by default, since the Index already opens with the bar and the Board Map and the matrix is a diagnostic view; the alternative is open by default so status is the first thing a reader sees.
- [ ] 🧠 Rule what happens to the timing recorder
      Three ways out: delete the recorder and its schema, keep it silently for a later "who is looking at this board right now", or keep it and show it as a secondary readout; the recommendation on the Items row is deleting.
      A tick here also closes the same row in Items to Finish.
- [ ] 🎛 Set the board design read and dials
      PROPOSED in Content §9: `3 to 4 / 1 to 2 / 7 to 8` for variance, motion, and density, to accept or revise.
      A tick here also closes the same row in Items to Finish.
- [ ] 🖼 Rule how far an ascii figure is allowed to stop looking like a terminal
      JL 260731, of `QB4f`'s head figure: "very hard to read ... could you make it more modern?"
      Half of it was a defect and is fixed board-wide: emoji are not monospace, so figures arrived bent; `body.pad_emoji` plus `pre .eu` now pin each emoji to `2ch`. The rest is taste, and taste on this surface is this face's call under the audit-first protocol in §9.
      A · leave `pre.asc` as it is. One flat grey code surface, 12.5px, no hierarchy. Cheapest, and it keeps a figure looking exactly like the text an author typed.
      B · give `pre.asc` typographic hierarchy only. The first line reads as a title, `═══` and `───` runs render as real hairlines, and the block gets a card surface instead of the code grey; still one `<pre>`, still copy-safe, one CSS rule and one build-time pass.
      C · render figures as real HTML. Cards or a grid, genuinely modern, and it costs the thing every figure rule on this board is built on: a drawing that survives being pasted into chat or mail (`QB4b` §0), plus a new authoring syntax on 53 pages.
      → CC recommends B, because it is the only option that answers "more modern" without spending the copy-survives property, and it is reversible in one rule.
- [x] 🗂 Rule the RELATED FOLDERS fold's depth — JL ruled B (260731)
      JL 260731 asked for a third Index fold, beside the Board Map and Section Matrix, that opens the folders this board touches: the shipping skill engine and "what a board folder should look like", sourced from `QA0`'s three folders.
      A · static folder tree only. Each related folder shows its structure as a rendered tree; authorable in `board.md` today, smallest engine change.
      B · a clickable browser. Each folder opens to reveal a file's content (for example `SKILL.md`); needs `src/page_board.py` to render the fold and `serve.py` to serve the content live.
      C · record the design only for now, ship neither depth until ruled.
      → JL ruled **B** (260731): the clickable browser. SHIPPED 0.87.0 as a build-time EMBED, not a live fetch: `related_folders()` in `src/page_board.py` reads each named file at build and inlines it, so the fold opens script-stripped and on a static host (QE3's Law). `QB2` owns the fold + render, `QA0` owns which folders are related and which files each opens. A live `serve.py` endpoint (`QC8`) is deferred, needed only for folders too big to inline (>120 KB).

## Files
### Engines
- `src/page_board.py`
  Builds the Board Map panel from a declared `board-map:` share URL when one exists; otherwise it uses the local scene through the Board server's Excalidraw proxy. The explicit URL supports static Tailscale hosting without changing the Board's page registry.
- `assets/css/10-focus.css`
  Holds the responsive Board Map surface. The iframe stays on `#top` only; a focused Q/S page hides it with the rest of the index.
- `cli/build.py`
  The index-rendering pass (`rows` / `frac_done` / the `.ir` CSS family), now also the Pages-intro parse (`gintro`) and the `details.gi` render.
  Changing the index half of this question starts here.
- `cli/serve.py`
  `structure_op()`: the one writer for add_group / add_question / archive_question / archive_group; `POST /_board/structure`.
  The console imports it, never reimplements.
- `assets/js/00-header.js` + `assets/css/10-focus.css`
  The page-side controls (＋Q, ＋Group, 🗄 with two-click confirm, inline mini form) and the intro styling; wired into `__boardRewire` so they survive live swaps.
  Also the ACTIVITY render: `sampleData` / `rowHtml` / `render`, and the `.act-*` styles.
  `board.css` additionally holds the palette, typography, density, surfaces, interaction feedback, dark mode, and responsive rules that the visual half audits.
- `cli/serve.py` · `log_counts` / `log_boards` / `activity_stats`
  The update counter. `log_counts` reads only `## Log`, caches on file mtime, and `activity_stats` joins it to `## Pages` for group ownership.
- `src/page_board.py`
  The static ACTIVITY shell, emitted after the page cards. Runtime data stays an enhancement: with no server the section reads as a sentence and the board is still complete.
### Input files
- `board.excalidraw`
  The one canonical scene: its generated frames are pages, while authors draw and label the relationships between them. It is not a separate page registry.
- `board.md`
  `## Pages` decides grouping, order, AND each group's intro (plain lines under the `### ` heading; line 1 = the visible sentence).
  If sorting ever becomes automatic, this section's role must be redefined too.
### The span recorder, written and unread
- `tests/test_activity.py`
  Regression tests for the span recorder, which nothing displays any more (see the open item).
- `.haipipe-board/activity.sqlite3`
  Local runtime spans, gitignored. Written, and currently unread.
### Graduation target and neighbouring faces
- `ref/board-form.md`
  Settled display rules graduate here only after the pilot and a human decision.
- `../QB-delivery/QB4-overall.md`
  Owns the existing shared page hierarchy and the unframed reading intent this audit must preserve, and owns automatic icon assignment; this face does not reopen the semantic role of authored icons.
- `QA9-acceptance.md`
  Owns repeatable post-change checks once a visual rule becomes mechanical.

## Discussion
> JL: QC2 Index page design 我们在这个地方需要能够添加和删除板块，也就是说，既能添加和删除 question group，也能添加和删除 question item。 另外，在 question group 之间，也需要有一个非常短的句子来介绍一下这个 group。我想的是这样的：比如你有一个 question group（像 QC、QA 这种），下面配一个简单的介绍（sentence）。当我们点击它的时候，它就会向下展开，弹出一个下拉的介绍。 这个介绍主要用来解释这个 group 是干嘛的，以及我们为什么要在这里使用它。大概就是这样的一个意思。
>> CC0724: both shipped. (1) Group intros: every group header now carries one always-visible sentence; click the ▸ and it drops open into the longer "what this group is for, why it is here" body. It lives in board.md's ## Pages as plain lines under the ### heading (first line = the sentence, the rest = the dropdown), rendered as a native details element, so it survives script-stripping and stays hand-editable. (2) Add/delete: ＋Q on each group header, ＋Group at the end of the list, and a hover 🗄 on every row and header. All of them only write the md through one endpoint (/_board/structure in serve.py, relayed by the console); "delete" is an archive that moves the file into _archive/, so nothing is ever lost. Try it on this page: hover a group header.
> JL: I think QE2 can merge to the QC2 Index page design. And for the activity dashboard, I don't care about the time. What I care is about the numbers of updates. (260726)
>> CC0726: both done, and the second one is the bigger of the two. The timer was measuring a browser, and most work here arrives through Claude Code, so it was precise about a quantity that was not the work. One update = one dated `## Log` line reads every tool and reads backwards, which is why the four days the timer missed came back. What is left over is the recorder itself, still writing spans nobody reads; the open item above asks you to kill it or keep it.
> JL: could we have the chatbot in the index page, so we can discuss how to work in the index page. (260725)
>> CC0725: built. The bottom-right 🤖 button now shows on the index as "🤖 Board chat"; it opens the same QD2 drawer (and QD3 terminal via ⌨), attached to board.md, primed with the index's own view: spine, close condition, every page's state and open comments. It has a canned 🧭 "Which question should I act on?" button, and its 🔧 button works comments board-wide. Implementation details are recorded on QD2; this page only owns the entry point.
> JL: Content should explain, section by section, what each part of the Q webpage is eventually for: Opening, Diagram, and so on. (260725)
>> CC0725: agreed on the principle and kept the ownership clean. The index face explains the index's own components; QA4 (now QAa0 and the QAa faces) explains the parts of an opened Q/S page and is linked from the final Content subsection.
> JL: how do we make this match the paper stages? (260725)
>> CC0725: this first became stage-first, then the paper exposed a clearer stable abstraction:
>> seven full-name S families. Seed, Work, Venue, Display, Main, Appendix, and Submission are now the groups;
>> each concrete S page is a row, and its blocking Q sits directly after it.
> JL: Display should be its own group because it is important. (260725)
>> CC0725: implemented as S Display 0. It is a separate progress family and remains between Narrative and the Main/Appendix consumers in Pipeline.
> JL: Could we try taste-skill, or add a Board Q about UI design?
>> CC0726: Add the Q first and make the trial bounded. The external default is a marketing-page skill, so the board should borrow its audit discipline rather than its visual defaults.
> JL: You should merge QC2 to QA10? about the Index-UI-Design? (260729)
>> CC0729: merged, and it closes the QC dissolution that started the same day. What the front page must SHOW and how the surface must LOOK were being decided on two faces that each needed the other's answer; the three-second test is a visual claim and the visual dials only matter because a dense index has to be scannable.
> JL: 🦴 Topic — what this board is about 🔄 Pipeline — how these Qs are ordered 🧭 Board-Structure — Board-Folder and Board-Webpage I want to remove them,just keep the Map is ok.

## Law
- 🗂 **Index stays as it is**: the Index does not roll up open `Decision Now` rows; a reader goes to a page's States to find them (JL 260802).
  Chosen over a roll-up block on the Index and over a per-page 🗣 badge in the rail.
  The rows already live where they are owned, and a second surface listing them is a second thing that can disagree with the first. The cost is real and accepted: finding what is waiting means opening pages.

## Log
260802 1150 · JL ruled option C on the Index roll-up, the same day it was raised: the Index stays as it is and a reader goes to States to find an open row. Recorded in Law and removed from Decision Now, per QB4 §5.2.7, which says an answered decision leaves States entirely rather than moving down the page
260802 1130 · An Index roll-up of every open `Decision Now` row was proposed and recorded here rather than left in a chat session (JL 260802: "don't put the decision in the claude code session"). It came out of JL asking whether a human could check Decision Now and nothing else: it is the only thing that requires them, but finding the rows today means opening 53 pages to learn that 51 have nothing waiting
260731 1945 · RELATED FOLDERS shipped as haipipe-board 0.87.0: build-time-embed fold (related_folders() in src/page_board.py + `## Related Folders` grammar in parse.py + board.md + board.css), rendering in board.html and the board/ tree; 2 folders / 4 files embedded, order Board Map → Related Folders → Section Matrix verified, body survives JS strip; QC8 live endpoint deferred. Also fixed the Board Map header typo "placement is not one." → "placement is not."
260731 1930 · RELATED FOLDERS depth ruled B (clickable browser) on JL's "do the B level"; split across QB2 (fold + page_board.py render), QA0 (folder list + contents), QC8 (serve.py content endpoint)
260731 1905 · RELATED FOLDERS Index fold requested (JL): a third fold beside the Board Map and Section Matrix, opening the folders this board touches (the shipping engine + what a board folder looks like), sourced from QA0 + ## Links; recorded as Content §16, an Items row, and a Decision Now depth ruling (static tree vs clickable browser). Renderer is src/page_board.py, so wiring needs an engine change
260731 · index_rows() and sidebar_rows() extracted so the tree and the single file share one implementation; restored the 6 group-intro ascii figures and the rail's 54 section outlines the hand-written version had dropped (haipipe-board 0.84.0)
260731 · Board Map header restyled to match the Section Matrix (one line, one triangle); two stray disclosure triangles removed, one a list-item marker and one a specificity tie (haipipe-board 0.82.0)
260731 · Two JL questions opened as Decision Now rows: a page of its own for each group (the QB ladder's Group rung has no face), and whether board.html stays one file (2.02 MB, 10% shared, 34 KB per page, 0.38s build)
260731 · Items, Where we are, and Files regrouped to the QB4d/QB4e/QB4f subsection conventions (matrix retrofit)
260731 · Topic, Pipeline, and Board-Structure removed from the rendered Index on JL's ruling; board.md keeps the sections as source-only documentation (0.78.0)
260731 · The Index row unfolds in the rail on JL's ask: Board Map, Section Matrix, All Pages, Activity, present-only, each scrolling the Index to its component (0.78.0)
260731 · Shipped the SECTION MATRIX on JL's dashboard ask: one row per page, one column per section, cells computed at build and linking into their section; columns and default posture wait in Decision Now (0.75.0)
260731 · Shipped the hideable pages sidebar (Index → group → page) on JL's ask; server-rendered rail, ☰ toggle, per-board persistence, active-row highlight
260730 · Board Map became an ASCII `## Board Map` figure rendered as a shuttable disclosure, winning over both canvas sources
260730 · Rewrote `board.md ## Board Structure` around the reader's three views: Board-Folder is the source, Board-Webpage-Index is the orientation view with the Board Map, and Board-Webpage-Page is the focused Q/S view; the map is inside the Index, not a third peer object
260730 · Added the Board Map to the Board-Webpage-Index: the top view now embeds the declared shared Excalidraw canvas below progress for static Tailscale readers; arrows stay authored rather than inferred from page order
260730 · Renamed from QA10 to QA2b, "Board-Webpage Design", on JL's terminology. Defined Board-Webpage-Index versus Board-Webpage-Page; the former QA0 map moved into board.md's Board-Structure block after Pipeline and no longer renders as a Q webpage
260729 · QC2 (Index page design) merged in on JL's call, completing the 260729 dissolution of the QC group. Its eight index components became §1 to §8 and its item blocks came with them; the former QA10 visual-taste content became §9 to §13; title changed from "Visual taste without drift" to "Index page and visual design". QC2 retired to `_archive/` with a `## Links` row, so the eight pages citing it still resolve
260726 · Applied the first reversible UI taste pilot: shared `:focus-visible` ring, four radius tokens, `prefers-reduced-motion` fallback; verified at desktop and 390px, light and dark, keyboard flow, and with scripts stripped
260726 · Index rows lost their coloured left stripe on JL's call; the state emoji already carried that information and the bars read as a chart down a long index
260726 2300 · QE2 absorbed (JL: "I think it can merge to the QC2 Index page design"): `§8 Activity` added, QE2's finish lines folded in, QD8-activity-timing.md deleted and delisted from board.md. The dashboard's unit changed from focus seconds to UPDATES counted from `## Log` (JL: "I don't care about the time"), which recovered 260722-260725 that the timer never saw: 509 updates · 8 boards · 129 pages, this board 300 over 5 days. Span recorder still runs and is now unread; its fate is an open item
260726 · Opened a scoped visual-taste decision: borrow the external project's audit-first and anti-default discipline, reject its marketing-page structure, high-motion defaults, and dependency assumptions
260725 · Display separated from Work into its own family; lifecycle index now has seven S groups
260725 · Family order clarified as navigation, Pipeline as execution; Submission pages now repeat across revision rounds
260725 · Full-name S families replaced temporary S/SM/SA grouping: Seed (including Literature), Work, Venue, Main, Appendix, Submission
260725 · Lifecycle board grouping settled: stage-order groups, canonical S first, owned Q decisions after; MISQ board reorganized to match
260725 · Content now defines the index components and explicitly hands the opened Q/S page to QA4; QA4 received the parallel section-purpose map
260725 1040 · 🤖 Board chat entry landed on the index (JL's ask; it is the QD2 drawer / QD3 terminal opened on board.md, details on QD2): fab shows on the index, label switches, follow() returns to the board session
260724 1553 · JL's two asks shipped: Pages-intro grammar + details.gi render (build.py), structure_op writer + /_board/structure (serve.py, imported by boards_api), page controls ＋Q/＋Group/🗄 (board.js/css); board.md's five groups got intros, Pipeline slimmed to the narrative; round trip byte-identical, refusals verified on 5599 + 8093; 🔴 → 🟡
260724 1242 · Translated to English (JL 260724: everything on the board in English)
260723 · Opened: the QC group refocused from "needs JL's decision" to "index and structure"; the front page becomes its own question (`QA4` owns only the single-question page; the index page had no owner)
