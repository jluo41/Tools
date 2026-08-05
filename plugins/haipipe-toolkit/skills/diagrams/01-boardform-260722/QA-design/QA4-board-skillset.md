# The board skill set, explained as a deck: the first real slide page
state: 🟡 IN PROGRESS · all 7 slides built and embedded live; every acceptance row waits for JL
owner: JL
method: build one real deck about a subject we actually need to explain, embed each slide LIVE in its own division via the deck's ?preview=N mode, and let this page prove or break the for-slide contract

## Opening
Can a board page carry a talk, slide by slide, without the slides going stale beside it?
This is the first real page of the `for-slide` type: one page per deck, one Content division per slide.
Each division below embeds the LIVE slide, not a screenshot: one deck file loaded with `?preview=N`, which shows exactly slide N with no chrome and no keys.
The same file, opened bare from Files, is the full keyboard presentation: one file, two surfaces, zero drift.

**The ruling under test**: JL ruled the embed must be the html itself, in the content division; this page is that ruling made real.

**What the deck is about**: the board skill set itself, for someone who has never seen it.
Seven slides: why boards exist, the shape of a page, the three skill layers, Type × Phase, the working loop, and the proof.

**What each division owes**: the slide's outline in speaking order, the live embed, and a slide binding row.
The binding row carries acceptance (a person accepts a specific render), the source the slide draws on, and the render date.
A rebuilt slide returns its row to ⬜, because what was accepted was the old render.

**What this page proves or breaks**: the `for-slide` contract said the board must never embed the live deck, on the belief that the build strips scripts.
That belief was wrong: the build only ASSERTS pages stay readable with scripts off, and an iframe's file is never rewritten by the build at all.
The contract gets corrected from what happens on this page.

## Diagram

**One file, two surfaces**: the deck html serves the review surface here and the presentation surface in a tab, so neither can drift from the other.

```text
   📄 QA-design/slides/QA4-board-skillset-deck.html      ← ONE file
        │
        ├──▶ 📋 REVIEW surface · THIS PAGE
        │      division N embeds  deck.html?preview=N
        │      exactly slide N · no chrome · no keys
        │      read it, then tick its acceptance row
        │
        └──▶ 🎥 PRESENTATION surface · a browser tab
               deck.html bare, from ## Files
               ← → flip · F fullscreen · S notes · T theme

   division anatomy, per the for-slide contract
   ──────────────────────────────────────────────
   ### N · <slide title>
   **What this slide must land**: <one sentence>
   <the outline · talk notes, in speaking order>
   ![slide N](…deck.html?preview=N)     ← the LIVE embed
   - accepted: ⬜ · source: … · rendered: 260805
```

## Content
### 1 · Cover: a filesystem of decisions
**What this slide must land**: the one-liner a listener repeats afterwards.
Say it plainly: every decision this team makes lives on a page you can open, not in a chat you cannot search.
One board per topic, one page per question, one human verb per ruling.

![slide 1 · cover](QA-design/slides/QA4-board-skillset-deck.html?preview=1)
- accepted: ⬜ · source: `board.md` opening prose · rendered: 260805

### 2 · The problem: decisions die in chat
**What this slide must land**: the three failures a listener recognizes from their own team.
Unfindable: someone says "we settled this last month" and nobody can point at where.
Re-argued: the same question returns every few weeks and costs the same hours again.
Unreadable: a new collaborator cannot reconstruct why anything is the way it is.

![slide 2 · the problem](QA-design/slides/QA4-board-skillset-deck.html?preview=2)
- accepted: ⬜ · source: `QA2` §1 (why pages exist) · rendered: 260805

### 3 · The shape: one page, four sections, one place to rule
**What this slide must land**: what a reader sees when they open any page, and where the human acts.
A board is a folder whose `board.md` lists groups of Q pages, built to a static site.
Every page keeps the same skeleton: Opening, Diagram, Content, State.
Open choices sit as Decision Now rows; a human ticks a row, and the tick is the ruling.

![slide 3 · the shape](QA-design/slides/QA4-board-skillset-deck.html?preview=3)
- accepted: ⬜ · source: `QB4` (the page grammar) · rendered: 260805

### 4 · The skill set: three layers run it
**What this slide must land**: the three names, and which one to remember.
`haipipe-board` is the engine: build, serve, check.
`haipipe-board-page` is the page contract: what any page owes its reader.
The verbs (routing, regrouping, meeting capture) move things between pages.
If a listener remembers one name, it should be `haipipe-board-page`.

![slide 4 · the skill set](QA-design/slides/QA4-board-skillset-deck.html?preview=4)
- accepted: ⬜ · source: `Skill-0` `Skill-3` mirrors on QCskill · rendered: 260805

### 5 · The one design idea: Page = Type × Phase
**What this slide must land**: type is found, phase is decided, and the skill loads both.
A page's TYPE is its stable identity, found from the file itself: stage, section, venue, skill, meeting, literature, value, display, slide.
Its PHASE is what it needs now, decided by authority: DRAFT borrows, PROBE earns, REVISE pays only with what landed, CHECK audits and alone may close.
Nobody memorizes the matrix; the skill resolves both and loads the right contracts.

![slide 5 · type × phase](QA-design/slides/QA4-board-skillset-deck.html?preview=5)
- accepted: ⬜ · source: `QB5` `QB6` · rendered: 260805

### 6 · How work happens: agents draft, humans rule
**What this slide must land**: the bounded loop, and why hitting the limit is never a pass.
CREATE gives a question a page; WORK ON improves it under the right contracts; RUN loops phases with receipts.
The loop is bounded: only CHECK may close, and stopping at the limit is a stop, not a pass.
The human's whole interface stays two moves: read the page, tick a row.

![slide 6 · the loop](QA-design/slides/QA4-board-skillset-deck.html?preview=6)
- accepted: ⬜ · source: `QB5` §6 §9 · rendered: 260805

### 7 · The proof: this very deck
**What this slide must land**: the loop closed on itself, live in front of the listener.
This deck is one html file; the page you are reading embeds it slide by slide with `?preview=N`.
The slide page type produced the deck that explains the system that defines the slide page type.
End by opening the bare deck from Files and flipping through it full screen.

![slide 7 · the proof](QA-design/slides/QA4-board-skillset-deck.html?preview=7)
- accepted: ⬜ · source: this page itself · rendered: 260805

## Aims
### P · 🏁 Page-level validation
- P1 · Each of the 7 divisions shows its own slide, live, at slide proportions, inside the built board page.
  **Done when:** the rendered page is driven in a real browser and each frame shows its slide's actual content, verified by eye, not by HTTP code.
- P2 · The embed survives the split-site build's path rerooting.
  **Done when:** the iframe src in `board/QA/QA4-board-skillset.html` resolves 200 from the served site.
- P3 · The bare deck link opens the full presentation with keyboard navigation and notes.
  **Done when:** opening the deck from ## Files and pressing → advances slides in a real browser.
- P4 · Every division carries a slide binding row, and a rebuilt slide returns its row to ⬜.
  **Done when:** all 7 rows exist with source and render date, and the rule is stated on the page.
- P5 · This page's shape passes the `for-slide` contract it exists to test, and what the contract got wrong is corrected in the contract, not papered over here.
  **Done when:** the contract's embed rule matches what this page actually does, and its changelog names this page as the reason.

## States
### Decision Now
These are the calls only JL can make; CC ticks nothing here.

```text
   the ask                                   CC picks     blocks
   ──────────────────────────────────────────────────────────────
   1  accept the 7 slides for the talk?      A · accept   P4 closing
      (tick per slide by flipping its          all 7
      row to ✅, or name the ones to redo)
```

- 📍 **Accept the deck** · ⬜ OPEN · the 7 embeds above are the exact renders; ticking a row accepts that render 🤖 A

### Where we are
P1 ✅ verified in a real browser on 260805 · P2 ✅ served 200 · P3 ✅ keyboard flip verified · P4 ✅ rows in place · P5 ✅ contract corrected at 0.2.0
The page waits on one thing: JL's acceptance ticks in Decision Now.

## Files
### ⚙️ Engines · what RUNS this subject
- `../../display/skills/html-ppt/assets/runtime.js`
  The deck runtime: keyboard navigation, presenter mode, and the `?preview=N` single-slide mode every division embed rides on.
- `../../board/haipipe-board/cli/build.py`
  Builds this page into the split site; its completeness check asserts the page reads with scripts off, which the fallback link under each frame satisfies.
- `../../board/haipipe-board/src/body.py`
  The renderer rule this page forced: `![alt](x.html)` becomes a live iframe embed, added 260805.

### 📋 Contracts · what CARRIES a rule to other pages
- `../../board/page-types/haipipe-board-page-for-slide/SKILL.md`
  The for-slide contract this page tests; corrected at 0.2.0 from what happened here.

### 🧪 Checks · what CATCHES a page breaking a rule
- `../../board/haipipe-board/cli/check.py`
  The mechanical checker; this page must add zero findings.

### 📥 Input files · what the work READS
- `QA-design/slides/QA4-board-skillset-deck.html`
  The deck itself: one hand-authored html file, seven slides, html-ppt conventions, academic-report theme. Open it bare to present.
- `QB-delivery/QB6-page-types.md`
  Where for-slide was admitted, and where its embed ruling is logged.

### 📤 Output files · what a BUILD writes
- `board/QA/QA4-board-skillset.html`
  ⚠️ Generated by `cli/build.py`. Never hand-edit.

## Log
- 260805 · Page created as the first real `for-slide` page, on JL's ruling "embed the html in the content division". Seven divisions, each embedding `deck.html?preview=N` live; the renderer gained the `![](x.html)` iframe rule and the split-site reroot fix the same day. The contract's "never embed the live deck" rule is corrected by this page: the build never strips scripts from an iframe's file, it only asserts the page reads without them.
