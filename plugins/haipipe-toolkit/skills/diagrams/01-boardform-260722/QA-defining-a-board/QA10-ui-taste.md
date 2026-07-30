# Index page and visual design
state: 🟡 PARTIAL
owner: JL
method: settle which questions the front page must answer, then settle how the whole surface looks; audit before editing, prototype at most three changes, compare before graduating anything
session: d2199106-8b6a-499d-8c24-9db3658486b5

## Question
You open a board and have not clicked into any question yet: what you see is the front-page list. What should it look like so that a person knows **within three seconds which question to act on**, and what visual language makes that answer legible without turning the board into a marketing page?

It is hard because the single-question page (`QAa0` and the QAa faces) is settled, but the front page must hold everything at once: all questions, all groups, every state and completion. One notch more information and it becomes a wall nobody can enter.
It matters because a board is for the second person: if the front page does not show "which question is stuck, which one is mine to move", the board is only usable by whoever wrote it.
The visual half is the same question asked about pixels. An external taste skill can expose defaults an AI repeats without noticing, but the default taste skill targets landing pages and portfolios rather than dense control planes, and applied literally its layout variance, motion and imagery would make this board less useful. The narrow version is what this face owns: which bias-correction rules improve a research work surface, which must be rejected, and what evidence is required before a visual preference becomes board law.
Downstream it drives group ordering, state display, completion coloring and default sort, all in `build.py`'s index-rendering pass, coupled to `board.md`'s `## Pages`, and the shared palette, typography and density in `assets/board.css`.

## Boundary
- ✅ Covered here
  **The front-page list**: group headers, what each row shows, the visuals of state and completion, sort rules, the structure controls, the board chat entry, the ACTIVITY block, and how "see at a glance what to act on" is achieved.
  **The board's visual design read**: density and motion settings, typography and surface consistency, accessibility checks, and the audit-first adoption protocol that governs any of it changing.
- ↪ Covered elsewhere
  The **single-question page** after the click: `QAa0` and the QAa faces, one per section.
  Whether each question's **prose is well written**, and the mechanical checks after any change: `QA9`.
  Automatic **group-title emoji** selection: `QAa3`, which carries the group-title marker (absorbed from QD4 on 260726, moved 260729).
  Which folder the board **lives in**: `QA1` (which absorbed QC1 on 260729).
  Paper and venue **writing style**: the Paper lifecycle.

## Diagram

```
top of board.html (no question opened yet)
┌──────────────────────────────────────────────┐
│ board name · 🦴 spine · 🏁 close condition    │
│ ▓▓▓▓▓░░░░░  N/M settled                      │  progress bar
├──────────────────────────────────────────────┤
│ QA · Defining a board            [＋Q] [🗄]  │  group header (hover controls)
│ ▸ Pin down the thing itself; nothing …       │  ← group intro: one sentence,
│   (click ▸ → expands: what / why this group) │    click to expand the why
│  ✅ QA1  Board folder shape        🔧 CC      │  ← what does each row show?
│  🟡 QAa0 Page overall: shared layout  🔧 CC  7/9 │     how is completion colored?
│  🔴 QAa3 group-title icons        🗄 🔧 CC  0/4 │     hover 🗄 = archive (2-click)
│  …                                            │
│  [＋ Group]                                   │
├──────────────────────────────────────────────┤
│  … all the page cards …                      │
├──────────────────────────────────────────────┤
│ ACTIVITY   (absorbed from QD8, 260726)       │
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
### 1 · Board orientation, say what this board is doing
The top strip gives the board name, spine, and close condition before showing any individual page.
It should let a newcomer understand the board's common question and the condition for finishing it without opening a row.

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
(absorbed from QD8 on 260726; the index closes on the measure of itself)
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

The broader baseline audit remains open because chat and comment interaction states have not yet
received the same full visual comparison.

### 14 · After a page opens
This face stops at the index and at the shared surface.
`QAa0` owns the opened Q/S webpage's order, and since 260729 each section has its own QAa face: Opening (`QAa1`), Diagram (`QAa2`), Content (`QAa3`), Items to Finish (`QAa4`), Where we are (`QAa5`), and the folds (`QAa6`).
The two specifications use the same principle without mixing their responsibilities.

## Items to Finish
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

**📊 Activity (absorbed from QD8, 260726)**

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

**🎨 Visual design (the former QA10 half)**

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
**The index is now a place you can WORK and understand, not only view: its Content subsections explain what every component is eventually for; paper lifecycles use seven readable S-family groups; the structure itself is editable from the page; and the index carries its own chat. The reading design questions (sort, coloring, the three-second test) stay open, and so does the visual baseline audit.**

- 260729 JL · 🔗 QC2 merged in here, and the QC group is now fully dissolved
  JL: "You should merge QC2 to QA10? about the Index-UI-Design?"
  The two faces were one subject seen twice: QC2 owned what the front page must SHOW, and QA10 owned how the whole surface must LOOK, and neither could settle its half without the other's.
  QC2's eight index components became §1 to §8 and its two item blocks came with them; the visual read, audit signals, borrow and reject lists and pilot became §9 to §13.
  The id kept is `QA10`, because the QC group dissolved on 260729 and its remaining pages moved into QA; `QC2` is a Links row to `_archive/` so every page citing it still resolves.

- 260726 JL · 🎨 The index rows lost their coloured left stripe
  JL asked for the red and green bars down the left of the index to go.
  Removed: `.ir`'s 4px `border-left` and the four `.ir.todo/.wip/.done/.hold` colour rules. The row keeps its 1px border and its hover accent.
  Nothing was lost, which is why it was safe: every row already opens with the state emoji, so the bar restated the state in a second language, and stacked down a 27-row index the bars read as a chart rather than as a list.
  Two neighbours were deliberately left alone: the pale green completion wash on each row is different information (percent done, not state), and the page's own left stripe on `.slide.q` is a different surface.

- 260726 CC · 🧪 Applied the first reversible UI taste pilot
  Added global keyboard focus, semantic radius tokens, and reduced-motion handling.
  Kept the existing focused-page framing because the source audit showed it already satisfies the proposed unframed reading direction.

- 260726 JL · 🧮 The dashboard changed its unit, and QD8 folded in here
  JL: "for the activity dashboard, I don't care about the time. What I care is about the numbers of updates."
  The timer was exact about the wrong quantity: it watched a browser tab, and most work on these boards is done through Claude Code, so the thing it measured was not the thing that happened.
  Counting dated `## Log` lines fixed the measure and the history in one move, because a record does not have to have been present to be read later.
  QD8 merged into QC2 in the same round on JL's call, which is right on ownership grounds: the dashboard is a component of the index, and this face already owns what every index component is for.
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
  The buttons are writers only: board.md's `## Pages` plus the Q files stay the single source of truth, `_archive/` keeps everything recoverable, and the live watcher (QD6) swaps the updated index in under you after each op.

- 260724 CC · 📖 Group intros landed with a new Pages grammar
  Intro lines sit directly under each `### ` heading in `## Pages`; the per-group paragraphs that used to live in `## Pipeline` moved there (Pipeline keeps only the overall narrative), so nothing is said twice.

- What the index looks like today
  Board name + spine + close condition + progress bar + two global fold-outs (what is this board / how are the Qs ordered) + the grouped list in `## Pages` order, each group led by its intro.

- What each row has today
  State badge · id · title · open-comment badge · owner · row tinted white to green by completion (`--fill`, percentage in `title`) · hover archive.

- Known defects
  ⏸️ ON HOLD renders as full green like ✅, reads as "done"; with many questions it is one long strip with no visible priority; group order is entirely hand-maintained in the Pages.
  No external skill has been installed and no dependency has been added.

## Files
- `build.py`
  The index-rendering pass (`rows` / `frac_done` / the `.ir` CSS family), now also the Pages-intro parse (`gintro`) and the `details.gi` render.
  Changing the index half of this question starts here.
- `board.md`
  `## Pages` decides grouping, order, AND each group's intro (plain lines under the `### ` heading; line 1 = the visible sentence).
  If sorting ever becomes automatic, this section's role must be redefined too.
- `serve.py`
  `structure_op()`: the one writer for add_group / add_question / archive_question / archive_group; `POST /_board/structure`.
  The console imports it, never reimplements.
- `assets/board.js` + `assets/board.css`
  The page-side controls (＋Q, ＋Group, 🗄 with two-click confirm, inline mini form) and the intro styling; wired into `__boardRewire` so they survive live swaps.
  Also the ACTIVITY render: `sampleData` / `rowHtml` / `render`, and the `.act-*` styles.
  `board.css` additionally holds the palette, typography, density, surfaces, interaction feedback, dark mode, and responsive rules that the visual half audits.
- `serve.py` · `log_counts` / `log_boards` / `activity_stats`
  The update counter. `log_counts` reads only `## Log`, caches on file mtime, and `activity_stats` joins it to `## Pages` for group ownership.
- `src/page_board.py`
  The static ACTIVITY shell, emitted after the page cards. Runtime data stays an enhancement: with no server the section reads as a sentence and the board is still complete.
- `test_activity.py`
  Regression tests for the span recorder, which nothing displays any more (see the open item).
- `.haipipe-board/activity.sqlite3`
  Local runtime spans, gitignored. Written, and currently unread.
- `ref/board-form.md`
  Settled display rules graduate here only after the pilot and a human decision.
- `../QAa-the-page/QAa0-overall.md`
  Owns the existing shared page hierarchy and the unframed reading intent this audit must preserve, and owns automatic icon assignment; this face does not reopen the semantic role of authored icons.
- `QA9-acceptance.md`
  Owns repeatable post-change checks once a visual rule becomes mechanical.

## Discussion
> JL: QC2 Index page design 我们在这个地方需要能够添加和删除板块，也就是说，既能添加和删除 question group，也能添加和删除 question item。 另外，在 question group 之间，也需要有一个非常短的句子来介绍一下这个 group。我想的是这样的：比如你有一个 question group（像 QC、QA 这种），下面配一个简单的介绍（sentence）。当我们点击它的时候，它就会向下展开，弹出一个下拉的介绍。 这个介绍主要用来解释这个 group 是干嘛的，以及我们为什么要在这里使用它。大概就是这样的一个意思。
>> CC0724: both shipped. (1) Group intros: every group header now carries one always-visible sentence; click the ▸ and it drops open into the longer "what this group is for, why it is here" body. It lives in board.md's ## Pages as plain lines under the ### heading (first line = the sentence, the rest = the dropdown), rendered as a native details element, so it survives script-stripping and stays hand-editable. (2) Add/delete: ＋Q on each group header, ＋Group at the end of the list, and a hover 🗄 on every row and header. All of them only write the md through one endpoint (/_board/structure in serve.py, relayed by the console); "delete" is an archive that moves the file into _archive/, so nothing is ever lost. Try it on this page: hover a group header.
> JL: I think QD8 can merge to the QC2 Index page design. And for the activity dashboard, I don't care about the time. What I care is about the numbers of updates. (260726)
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

## Log
260729 · QC2 (Index page design) merged in on JL's call, completing the 260729 dissolution of the QC group. Its eight index components became §1 to §8 and its item blocks came with them; the former QA10 visual-taste content became §9 to §13; title changed from "Visual taste without drift" to "Index page and visual design". QC2 retired to `_archive/` with a `## Links` row, so the eight pages citing it still resolve
260726 · Applied the first reversible UI taste pilot: shared `:focus-visible` ring, four radius tokens, `prefers-reduced-motion` fallback; verified at desktop and 390px, light and dark, keyboard flow, and with scripts stripped
260726 · Index rows lost their coloured left stripe on JL's call; the state emoji already carried that information and the bars read as a chart down a long index
260726 2300 · QD8 absorbed (JL: "I think it can merge to the QC2 Index page design"): `§8 Activity` added, QD8's finish lines folded in, QD8-activity-timing.md deleted and delisted from board.md. The dashboard's unit changed from focus seconds to UPDATES counted from `## Log` (JL: "I don't care about the time"), which recovered 260722-260725 that the timer never saw: 509 updates · 8 boards · 129 pages, this board 300 over 5 days. Span recorder still runs and is now unread; its fate is an open item
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
