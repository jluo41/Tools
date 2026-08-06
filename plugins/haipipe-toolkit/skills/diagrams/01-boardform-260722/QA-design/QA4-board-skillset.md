# The board skill set, explained as a deck: the first real slide page
state: 🟡 IN PROGRESS · 7 slides in 4 beats, one embed and one accept row per slide (re-ruled A 260805); every row waits for JL
page-type: slide
owner: JL
method: build one real deck about a subject we actually need to explain, embed each slide LIVE in its own division via the deck's ?preview=N mode, and let this page prove or break the for-slide contract

## Opening
Can a board page carry a talk, beat by beat, without the slides going stale beside it?
This is the first real page of the `for-slide` type: one page per deck, one Content division per talk beat.
A beat holds one or several slides, each embedded LIVE from one deck file with its own accept row, so every slide iterates on its own.
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
        │      division = one talk BEAT, embedding
        │      deck.html?preview=N#sN once PER SLIDE
        │      one frame = that one slide · no chrome · no keys
        │      read it, then tick THAT slide's acceptance row
        │
        └──▶ 🎥 PRESENTATION surface · a browser tab
               deck.html bare, from ## Files
               ← → flip · F fullscreen · S notes · T theme

   division anatomy, per the for-slide contract (re-ruled A, 260805)
   ──────────────────────────────────────────────
   ### N · <beat title> · slides A-B
   **What this beat must land**: <one sentence>
   <the outline · talk notes, in speaking order>
   ![slide A](…deck.html?preview=A#sA)   ← one embed PER SLIDE, so each
   - accepted: ⬜ · slide A · source: …     slide iterates on its own
   ![slide B](…deck.html?preview=B#sB)
   - accepted: ⬜ · slide B · source: …
   (?preview=A-B stays a legal COMPACT form for a settled beat)
```

## Content
### 1 · Why boards exist · slides 1-2
**What this beat must land**: the one-liner, then the three failures a listener recognizes from their own team.
Open plainly: every decision this team makes lives on a page you can open, not in a chat you cannot search.
Then the pain: unfindable ("we settled this last month", but where?), re-argued (the same question, the same hours, every few weeks), unreadable (a new collaborator cannot reconstruct why anything is as it is).

![slide 1 · cover](QA-design/slides/QA4-board-skillset-deck.html?preview=1#s1)
- accepted: ⬜ · slide 1 · source: `board.md` opening prose · rendered: 260805

![slide 2 · the problem](QA-design/slides/QA4-board-skillset-deck.html?preview=2#s2)
- accepted: ⬜ · slide 2 · source: `QA2` §1 (why pages exist) · rendered: 260805

### 2 · The system · slides 3-4
**What this beat must land**: what a reader opens, and the three skill names that run it.
The shape first: a board is a folder, one page per question, every page the same skeleton, and the human acts in one place (a Decision Now row; the tick is the ruling).
Then the names: `haipipe-board` the engine, `haipipe-board-page` the page contract, the verbs for movement; if they remember one name, it is `haipipe-board-page`.

![slide 3 · the shape](QA-design/slides/QA4-board-skillset-deck.html?preview=3#s3)
- accepted: ⬜ · slide 3 · source: `QB4` (the page grammar) · rendered: 260805

![slide 4 · the skill set](QA-design/slides/QA4-board-skillset-deck.html?preview=4#s4)
- accepted: ⬜ · slide 4 · source: `Skill-0` `Skill-3` mirrors on QCskill · rendered: 260805

### 3 · How it works · slides 5-6
**What this beat must land**: Page = Type × Phase, then the bounded loop that runs it.
Type is found from the file; phase is decided by authority: DRAFT borrows, PROBE earns, REVISE pays only with what landed, CHECK audits and alone may close.
Then the loop: CREATE, WORK ON, RUN; bounded, receipts kept, and hitting the limit is a stop, never a pass.

![slide 5 · type × phase](QA-design/slides/QA4-board-skillset-deck.html?preview=5#s5)
- accepted: ⬜ · slide 5 · source: `QB5` `QB6` · rendered: 260805

![slide 6 · the loop](QA-design/slides/QA4-board-skillset-deck.html?preview=6#s6)
- accepted: ⬜ · slide 6 · source: `QB5` §6 §9 · rendered: 260805

### 4 · The proof · slide 7
**What this beat must land**: the loop closed on itself, live in front of the listener.
This deck is one html file; the page you are reading embeds it slide by slide with `?preview=N#sN`, four beats and seven frames.
The slide page type produced the deck that explains the system that defines the slide page type.
End by opening the bare deck from Files and flipping through it full screen.

![slide 7 · the proof](QA-design/slides/QA4-board-skillset-deck.html?preview=7#s7)
- accepted: ⬜ · slide 7 · source: this page itself · rendered: 260805

## Aims
### P · 🏁 Page-level validation
- P1 · Each of the 4 divisions shows its beat's slides, live, one frame per slide at slide proportions, inside the built board page (7 slides total).
  **Done when:** the rendered page is driven in a real browser OVER THE ADDRESS JL USES and each frame shows its beat's actual slides, verified by eye, not by HTTP code.
- P2 · The embed survives the split-site build's path rerooting.
  **Done when:** the iframe src in `board/QA/QA4-board-skillset.html` resolves 200 from the served site.
- P3 · The bare deck link opens the full presentation with keyboard navigation and notes.
  **Done when:** opening the deck from ## Files and pressing → advances slides in a real browser.
- P4 · Every slide carries its own binding row inside its beat, and a rebuilt slide returns only ITS row to ⬜.
  **Done when:** all 7 rows exist naming their slide, source, and render date, and the rule is stated on the page.
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
   2  rewrite P4? its Done when tests that    A · rebind   P4's row
      the 7 rows EXIST, not that a person       it to        reading
      ticked one, so States read P4 as met      the tick     met
      while zero slides were accepted
```

- 📍 **Accept the deck** · ⬜ OPEN · the 7 embeds above are the exact renders; ticking a slide's row accepts that render 🤖 A
- 📍 **Rewrite P4, or keep it?** · ⬜ OPEN · 📍 Part: `## Aims` P4 · 🔔 Why now: this section reported P4 as met while 0 of the 7 acceptance rows carried a tick, and P4's own Done when is what allowed that: it asks only that the 7 rows EXIST naming slide, source and render date, which is true the moment CC writes them. ⭐ A · rebind P4's Done when to the TICK, so it can close only once a person has accepted a render and the number a reader sees is the number of accepted slides · B · keep the wording as a row-shape target and leave acceptance to row 1 alone, which means no Aim on this page ever tracks whether the deck was accepted · 🛑 Blocks: P4's State row, which stays 🧠 until this is ruled, because CC may not edit an Aim's text
- 📍 **Several slides per division** · ✅ `Ruled B` JL 260805 ("Do this one."), against CC's ⭐ A (multi-embed). Range mode built the same hour: `?preview=A-B` renders slides A..B as a vertical strip (html-ppt `runtime.js`), the board sizes the frame to the strip (`src/body.py`), acceptance moved to BEAT grain, and the scripts-off fallback shows the range's FIRST slide, recorded in the contract at 0.3.0.
- 📍 **Re-ruled A the same day** · ✅ JL 260805, after seeing B rendered: "So it is not like I can do the iteration. What about the old method of A? will that be easier." Beat-grain acceptance blocked slide-by-slide iteration, which is the review loop's whole point. The page now carries A inside B's beats: divisions stay talk beats, but each slide gets its OWN embed and its OWN accept row, so one slide can be accepted while its neighbor is redone. The range strip stays built and legal as a compact form for a settled beat; the contract records both at 0.4.0.

### Where we are
Zero of the seven slides are accepted: every acceptance row in Content reads ⬜, so the deck is rendered and reviewable and nothing about it has been ruled.
The page waits on two things and both are JL's: the seven acceptance ticks, and whether P4 should test the tick instead of the row.

### P · 🏁 Page-level validation
- 🔨 P1 · The built page does carry one frame per slide: `board/QA/QA4-board-skillset.html` holds seven iframe srcs, `?preview=1&plain#s1` through `?preview=7&plain#s7`, read off the built file on 260806. That is not what P1 asks for. It asks for eyes on the 4-beat page over the address JL uses, and the last recorded by-eye Chrome pass (Log, 260805) looked at the SEVEN-DIVISION shape that the re-ruling replaced later that same day. The embed URLs did not change, the grouping did, so this closes when someone drives the current page and looks.
- ✅ P2 · Served 200 over the address JL uses, re-checked 260806: all seven iframe srcs return 200 from `http://100.121.165.84:5599/Tools/plugins/haipipe-toolkit/skills/diagrams/01-boardform-260722/QA-design/slides/QA4-board-skillset-deck.html?preview=N&plain`, as do the deck's `runtime.js` and `base.css`, and a request carrying `Sec-Fetch-Dest: iframe` returns 200 too, which is the header whose absence hid the 260805 same-slide bug.
- ✅ P3 · Keyboard flip verified in a real Chrome on 260805, and nothing that surface depends on has moved since: the deck file's mtime is 260805 1140 and `runtime.js` is 260805 1141, the deck loads `runtime.js` at its line 107, and that file binds `ArrowRight` at lines 886 and 981.
- 🧠 P4 · Waiting on JL, and it may not read ✅ while the ticks are absent. All 7 acceptance rows exist naming slide, source and render date, so P4's Done when is literally satisfied, and that is the defect: 0 of the 7 rows are ticked, yet this section reported P4 as met, which a reader takes to mean the deck was accepted. CC may not rewrite an Aim, so the wording stands and this row stays 🧠; the choice is Decision Now row 2.
- ✅ P5 · The contract's embed rule matches what this page does, and its changelog names this page as the reason: `haipipe-board-page-for-slide/CHANGELOG.md` 0.4.0 records the re-ruling this page forced and names QA4 in its bullets, and 0.5.0 cites QA4 again. Two facts this row owes: the contract shipped 0.5.0 on 260806, which `## Files` lagged at 0.4.0 until it was repointed the same day, and 0.5.0 records that this deck's flat path `QA-design/slides/QA4-board-skillset-deck.html` predates its new companion-folder rule and does not follow it. Neither touches the embed rule P5 names.

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
  The for-slide contract this page tests, now 0.5.0 in its own frontmatter; corrected here three times (live html embed at 0.2.0, beat strip at 0.3.0, per-slide accept rows at 0.4.0). 0.5.0 shipped without this page: it adds `template.md`, fixes the acceptance row's four fields, and records that this deck's flat path `QA-design/slides/QA4-board-skillset-deck.html` predates the companion-folder rule and does not follow it.

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
- 260806 · [REVISE-CC] the `## Files` contract entry said "now 0.4.0" and the file's own frontmatter says `version: "0.5.0"`, so the entry was repointed and told the reader what 0.5.0 added: `template.md`, the four-field acceptance row, and the note that this deck's flat path does not follow the new companion-folder rule. P5's State row had already spotted the drift on 260806 and named it as a debt without paying it; that clause now records the repoint instead of the lag. Nothing about the embed rule P5 tests moved, so P5 stays ✅ and no acceptance row was touched.
- 260806 1257 · [REVISE-CC] States now mirrors every Aim id; the false green is CONFIRMED. `### Where we are` reported P1 through P5 as met while 0 of the 7 acceptance rows in Content carried a tick, so the page read finished and JL had accepted nothing. The checker never saw it because that line wrote the glyph AFTER the id and not as a `- <glyph> P<n> ·` row, so `aim_progress` matched no row, defaulted all five to ⬜, and reported `aim-without-state` while a human read five greens. The line it replaced, verbatim: `P1 ✅ re-verified over the tailnet address 260805 · P2 ✅ served 200 · P3 ✅ keyboard flip verified · P4 ✅ 7 per-slide rows inside 4 beats · P5 ✅ contract at 0.4.0` and `The page waits on one thing: JL's acceptance ticks in Decision Now.` The five real rows now read P1 🔨 (the only by-eye Chrome pass over `100.121.165.84` is 260805 on the seven-division shape the re-ruling replaced), P2 ✅ (all seven iframe srcs plus `runtime.js` and `base.css` return 200 over that address today, including one request carrying `Sec-Fetch-Dest: iframe`), P3 ✅ (deck 260805 1140 and `runtime.js` 260805 1141 unchanged, `ArrowRight` bound at runtime.js:886 and :981), P4 🧠 (its Done when tests that the rows EXIST rather than that a person ticked one, which is the wording that produced the false green; the Aim's text is untouched and Decision Now row 2 now asks JL to rebind it to the tick), P5 ✅ (CHANGELOG 0.4.0 and 0.5.0 both name this page; the contract has since shipped 0.5.0 while `## Files` still says 0.4.0). Nothing was ticked: the seven acceptance rows are JL's alone.
- 260806 2218 · [REVISE-CC] type-conformance pass against haipipe-board-page-for-slide; cleared the leftover beat-strip claims the re-ruling left behind (Diagram review lane, §4's `?preview=A-B`, P1's "as a strip") and repointed the Files contract entry from 0.2.0 to 0.4.0
- 260806 2121 · [REVISE-CC] swept to the 260806 architecture; verified clean, no corrections (deck file, QB4/QB5/QB6/Skill-0/Skill-3 sources, engine paths, for-slide contract 0.4.0 all check out on disk)
- 260805 · RE-RULED A after seeing B rendered (JL: "So it is not like I can do the iteration"): beat-grain acceptance blocked slide-by-slide review, so the page keeps the 4 beat divisions but gives every slide its own embed and its own accept row again. The range strip stays built in the engine and legal as a compact form for a settled beat. Contract at 0.4.0.
- 260805 · RULED B and rebuilt as beats: JL picked range mode over CC's multi-embed recommendation ("Do this one."). html-ppt's runtime gained `?preview=A-B` strip rendering, the board renderer sizes a range frame to `16/(9×count)`, and this page regrouped from 7 one-slide divisions into 4 beats (1-2 why · 3-4 the system · 5-6 how it works · 7 the proof). Acceptance moved to beat grain; the scripts-off fallback shows a range's first slide.
- 260805 · The same-slide-everywhere bug JL caught ("in division 2, and 3, they are always of the same slide number") fixed at the engine: the renderer now appends `plain` to every html-embed URL. Over the tailnet address the server's Accept-header fallback wrapped each embed iframe in the three-pane shell and dropped `?preview=N`, so every division showed the cover; verification had passed only because 127.0.0.1 carries `Sec-Fetch-Dest` and the tailnet does not. Reproduced with a header-faithful request, fixed, and re-verified in a real Chrome over `100.121.165.84` itself: seven divisions, seven different slides.
- 260805 · Scripts-off fallback added after JL pasted a view with no slides in it: every embed now carries `?preview=N#sN`, and the deck gained `id="sN"` per slide plus a CSS `:target` block, so the right slide shows even where a surface blocks JS. Verified in a real Chrome with script execution disabled; the JS-on path re-verified unchanged.
- 260805 · Page created as the first real `for-slide` page, on JL's ruling "embed the html in the content division". Seven divisions, each embedding `deck.html?preview=N` live; the renderer gained the `![](x.html)` iframe rule and the split-site reroot fix the same day. The contract's "never embed the live deck" rule is corrected by this page: the build never strips scripts from an iframe's file, it only asserts the page reads without them.
