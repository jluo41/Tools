<!-- TEMPLATE · ONE DECK = ONE SLIDE PAGE.
     Copy this file to your Board as `<group>/<page name>.md`, fill every <angle-bracket> slot,
     and DELETE each RULE comment as you satisfy it. A RULE comment never ships in a filled page.

     LOAD FIRST, in this order:
       1. `haipipe-board-page`                      the base frame: section order, Opening shape,
                                                    caption rule, Aims/States grammar, Files menu
       2. `haipipe-board/ref/page-template.md`      the authoritative base source form
       3. `haipipe-board-page-for-slide/SKILL.md`   this type's contract, which this file serializes
     This template adds ONLY what a deck page adds. Everything it does not mention, the base owns,
     and the base wins on any conflict.

     WHAT THIS PAGE IS. One page per DECK. The deck is ONE html file. Each Content division is one
     talk BEAT; inside the beat, each SLIDE gets its own live embed of that one file and its own
     acceptance row. The same file opened bare is the presentation, so the review surface and the
     presentation surface read the same bytes and can never drift.

     WHAT THIS PAGE IS NOT. It does not hold anything true of more than one deck:
       which Page Types exist                -> the board's page-type hub page
       the acceptance model it borrows       -> `haipipe-board-page-for-display`
       the number rule it borrows            -> `haipipe-board-page-for-value`
       the deck BUILDER (themes, layouts)    -> `display/skills/html-ppt`
       the outline extractor (paper family)  -> `display/skills/paper-slides`
       how a sentence in prose cites a slide -> the base's sentence apparatus
     There is no deck control page, and no second map of slide to source: reading each acceptance
     row's `source:` field IS that map.

     NO markdown pipe tables anywhere (JL 2026-07-10): every would-be table is record lines.
     English only. No em-dashes. One sentence per source line. -->

# <Short title in sentence case, saying what the talk is FOR>
state: 🔴 OPEN
page-type: slide
owner: <JL | CC>
method: build one deck file, embed every slide live in its own beat division, resolve every number the deck shows, and leave every acceptance row for a person
needs: <atom or record ids this deck reads, comma separated, or delete the line>
provides: <group>/slides/<page name>/<deck path>

<!-- RULE: `page-type: slide` is REQUIRED and it goes on its own line between `state:` and `owner:`.
     A deck can sit on any filename, so the KEY is what says this page closes slide by slide
     (base type resolution step ③, which beats the filename at step ⑤). Today no engine code reads
     the key: `grep -rn page-type` over `haipipe-board/src` and `cli` returns nothing, so it is
     contract-only and nothing will report you for omitting it. Write it anyway; the resolver rule
     is what other readers trust. -->

<!-- RULE: `state:` takes one of the base's four values, 🔴 OPEN · 🟡 PARTIAL · ✅ SETTLED · ⏸️ ON HOLD,
     with a short readable detail after the emoji. For THIS type ✅ means one thing only: every slide's
     acceptance row is ticked by a person, or the slide is explicitly cut from the talk. A deck that is
     built, rendered, and verified is still 🟡 while any row is ⬜. Put the count in the detail, for
     example `🟡 PARTIAL · 7 slides in 4 beats, 0 of 7 accepted`. -->

<!-- RULE: `needs:` and `provides:` are OPTIONAL and belong to boards that run an id resolver
     (`unit.py` on the boardform board's QBt group). Use them when your board has one, because a page
     that names another page's product by id survives a folder move and a hand-written path does not.
     Delete both lines on a board with no resolver. -->

## Opening

<!-- RULE: the base owns this section's shape and its 520-character ceiling on the visible paragraph,
     measured on the render. Do not restate the base here. The slide-specific obligation is that the
     visible paragraph says three things: this page is one page per deck, each division shows its
     slides LIVE from that one file, and each slide carries the one row a person ticks. -->
<Can a board page carry <this talk> without the slides going stale beside it?>
<One sentence: what the deck is about, in the words a listener would use.>
<One sentence: one page per deck, one division per beat, each slide embedded live with its own accept row.>
<One sentence: the same file opened bare is the presentation, so the two surfaces cannot drift.>

**Where its things are**: a page's companion folder is `<type-plural>/<page name>/`, so this page's deck is `<group>/slides/<page name>/`.
<!-- RULE: THIS PART IS REQUIRED AND IT IS THE NAMING RULE. The folder is named after the page
     EXACTLY, it sits inside the page's own group folder, and its type-plural is `slides`. A display
     page's is `displays/<page name>/`, an inward-evidence page's drawer is `QA-probe/<page name>/`;
     one rule, three folders, no per-page invention. Inside the folder:
       hand-authored deck   slides/<page name>/deck.html
       generated deck       slides/<page name>/out/deck.html  beside  slides/<page name>/source/
     A deck dropped beside the folder as a flat `slides/<page>-deck.html` breaks the rule: nothing
     else about the deck then has a home, so the build script, the template, and the export land
     wherever the author happened to be standing. -->

**What each division owes**: <the beat's speaking notes in order, one live embed per slide, and one acceptance row under each embed>.

**What no machine may write here**: the `accepted:` rows.
<!-- RULE: REQUIRED. A slide page closes when a person has looked at a specific render and said yes
     to it. An agent that ticks a row has not closed anything, it has forged a judgment. Say this on
     the page, because the page is where the next agent reads it. -->

**Covered elsewhere**: <the sibling deck page or the type contract, and what each handles>.

## Diagram

<!-- RULE: the base requires a caption line directly above every fence. The slide-specific figure is
     ALWAYS the two-surface diagram: one file, the review surface here, the presentation surface in a
     tab. Draw it with `/diagram-ascii`, put an emoji on every box, keep it under about 80 columns,
     and write rows as label plus value, never as clauses that could end in a period. -->

**One file, two surfaces**: how the same deck bytes serve the review surface on this page and the presentation surface in a tab.

```text
  📄 <group>/slides/<page name>/<deck path>          ← ONE file
       │
       ├──▶ 📋 REVIEW surface · THIS PAGE
       │      division = one talk BEAT, embedding
       │      <deck path>?preview=N#sN once PER SLIDE
       │      one frame = one slide · no chrome · no keys
       │      read it, then tick THAT slide's acceptance row
       │
       └──▶ 🎥 PRESENTATION surface · a browser tab
              the same file bare, linked from ## Files
              <the real keys this deck answers to>
  ──────────────────────────────────────────────────────────
  the two surfaces read the SAME BYTES, so neither can drift
```

## Content

<!-- RULE: ONE DIVISION PER BEAT, ONE EMBED AND ONE ACCEPT ROW PER SLIDE INSIDE IT.
     A beat is a unit of talk, so it may hold one slide or several. The common case is one slide per
     beat, and then the division heading and the slide coincide; that is not a different shape.
     Acceptance is always at SLIDE grain, which is the point of the 0.4.0 ruling: one slide is
     accepted while its neighbour is redone, and that is the iteration a review loop needs.
     Deck order IS page order: beats run down the page, slides run down their beat, and the slide
     numbers never skip or repeat across the whole page. -->

<!-- RULE: the division heading carries the beat number, the beat title, and the slide range it
     covers: `### 3 · How it works · slides 5-6`, or `### 1 · The cover · slide 1` for one slide.
     NO EMOJI on the heading. The emoji lives on the matching Aims and States group, and `check.py`
     fires `group-name-drift` when it is on the heading instead. -->

<!-- RULE: THE MECHANICAL GATE, and it is the one thing a checker really enforces here.
     `check.py check_division_figures` requires that every Content division's FIRST non-blank line
     is a caption matching `**Name**: …`, and that the division contains a fenced figure or a
     standalone media-embed line. THE EMBED IS THE FIGURE for this type: a line that is exactly
     `![alt](path)` counts, which is why a slide division needs no ascii fence (JL 260805, QA4).
     Get the caption wrong and you get `division-no-caption`; drop the embed with no fence and you
     get `division-no-figure`. Both are WARN, both are visible in `check.py --summary`. -->

<!-- RULE: THE EMBED, and both selectors are always written: `![slide N · <what it shows>](<board-root-relative deck path>?preview=N#sN)`.
     The path is BOARD-ROOT-relative, starting at the group folder, because the split-site build
     reroots it per output page (`src/page_board.tree_reroot`). A page-relative path breaks there.
     WHICH SELECTOR ACTUALLY PICKS THE SLIDE depends on the deck, and the two live pages differ:

       selector     what makes it work                          with scripts OFF
       ─────────────────────────────────────────────────────────────────────────────
       ?preview=N   html-ppt's `assets/runtime.js`, which the    inert · picks nothing
                    deck must LOAD; it stamps `data-preview`
                    and hides every slide but N
       #sN          the deck's own `id="sN"` per slide plus a    works · this is then
                    `:target` CSS pair in the deck                the ONLY selector

     So the fragment is the selector that always works, and the query works only on a deck that
     loads the runtime. The board engine picks no slide at all: `src/body.py` renders any
     `![alt](x.html)` as an iframe, appends `plain` (the serve shell's opt-out, without which a
     tailnet request comes back as the three-pane shell with the query dropped, and every division
     shows the cover), and reads the URL only to size a RANGE frame. Write both selectors on every
     embed, whichever kind of deck you built.

     SCOPING, when the deck DOES load the runtime: the `:target` pair must be scoped
     `html:not([data-preview])`, or with scripts on it fights the runtime and hides every non-target
     slide of a strip. A scripts-free deck needs no scoping, and harmless scoping is still fine. -->

<!-- RULE: THE DECK MUST SHOW ITS SLIDE WITH SCRIPTS OFF. Give every `<section class="slide">` an
     `id="sN"` and carry the `:target` pair in the deck's own style block. State the real reason,
     because the usual one is wrong: `cli/build.py` samples only the LARGEST built page, strips
     `<script>` blocks, and asserts more than 1200 characters of body text survive. It never opens an
     iframe, so nothing in the board build inspects your deck. The binding reason is the READER'S
     SURFACE: a VS Code webview and a locked-down frame both block scripts, and a deck that needs a
     runtime shows a blank frame there. -->

<!-- RULE: THE RANGE STRIP `?preview=A-B` IS A RUNTIME FEATURE, and it is optional. It renders slides
     A..B as one vertical strip and the board sizes the frame to `aspect-ratio:16/(9×count)`. Use it
     only for a beat that is ALREADY SETTLED, and only on a deck that loads the runtime. Its three
     costs, all stated on the contract: acceptance goes back to set grain, the scripts-off fallback
     shows only the range's first slide, and `src/body.py` sizes the frame from the URL alone, so a
     scripts-free deck writing a legal range gets one slide floating in a frame built for four. -->

### <N> · <Beat title, no emoji> · slides <A>-<B>

**<What this beat must land>**: <one sentence, and this line is also the division's required caption>.

<The outline and the talk notes, in speaking order, one sentence per line.>
<Say what is spoken, not what the slide contains: the slide is right there.>

![slide <A> · <what this slide shows>](<group>/slides/<page name>/<deck path>?preview=<A>#s<A>)
- accepted: ⬜ · slide <A> · source: <the section page, outline line, or record this slide draws on> · rendered: <YYMMDD>

![slide <B> · <what this slide shows>](<group>/slides/<page name>/<deck path>?preview=<B>#s<B>)
- accepted: ⬜ · slide <B> · source: <…> · rendered: <YYMMDD>

<!-- RULE: THE ACCEPTANCE ROW IS THE SLIDE BINDING, one per SLIDE, and it sits DIRECTLY UNDER ITS OWN
     EMBED with nothing between them. Adjacency is the whole binding: a row one paragraph away leaves
     a reader guessing which render was accepted. Four fields, in this order and no other:
       accepted:   ⬜ waiting for a person · ✅ <WHO> <YYMMDD> once they have seen THAT render ·
                   ✂️ cut <YYMMDD> when the slide leaves the talk
       slide:      the slide number, matching the embed's `?preview=N#sN`
       source:     what feeds this slide, by page id, section, or record id, never a re-description
       rendered:   the date the embedded bytes were built
     The beat's speaking notes may sit before the embeds or after them, and the two live pages differ:
     `QA4` writes notes then embeds, `QBt9` writes each embed then its commentary. Both read fine.
     What is NOT free is the embed-to-row gap, so keep those two lines together whichever order you pick.
     A ⬜ that a machine flips to ✅ is a forged judgment, not a fast one. A rebuild or a reword that
     changes the deck's bytes returns THAT slide's row to ⬜, because what was accepted was the old
     render; a byte-identical rebuild changes nothing, which is why a generated deck should write no
     timestamp. A beat embedded as a compact `?preview=A-B` strip carries ONE row for the set and
     resets as a set, which is the compact form's stated cost. -->

<!-- RULE: EVERY NUMBER THE SLIDE SHOWS CARRIES A BINDING, exactly as `for-value` requires: a value
     binding by path or id, or the producing run named. A slide is a display that talks, and it gets
     no looser standard for being temporary; a number typed into slide markup at 2am is untraceable
     by breakfast. Add the record figure below to any division whose slide prints a number, and
     delete it from every division whose slides print none. The strongest form is a deck TEMPLATE
     that carries no digits at all and a build that fills them, so the rule is enforced instead of
     remembered. -->

```text
  value on the slide     source                                    kind
  ────────────────────────────────────────────────────────────────────────
  <the printed value>    <atom id, record path, or named run>      <bound |
                                                                    derived |
                                                                    carried>
  ────────────────────────────────────────────────────────────────────────
  <what is deliberately NOT on this slide, and which unbound source is why>
```

## Aims

<!-- RULE: the base owns the grammar. One Aims group per Content division, written
     `### A<n> · <emoji> <beat title> · slides <A>-<B>`, taking the division's NUMBER and NAME and
     carrying the emoji the division heading may not. `### P` is for a target that genuinely crosses
     beats. Every Aim needs a testable `Done when`. -->

### A<n> · <emoji> <Beat title> · slides <A>-<B>
- A<n>.1 · <the outcome this beat's slides must make true>
  **Done when:** <a test a reader can run on the render, not on the source>

### P · 🏁 The deck as a whole
<!-- RULE: THESE THREE PAGE-LEVEL AIMS ARE THIS TYPE'S OWN, and a slide page carries all three.
     P1 is verified by EYE in a real browser over the address the reader actually uses, never by an
     HTTP status: an embed can return 200 and still show the cover in every division, which is
     exactly what happened on QA4 before `plain` was appended. P3 is the one Aim a page may never
     close by itself. -->
- P1 · Each division shows its own slides, live, at slide proportions, inside the built board page.
  **Done when:** the rendered page is driven in a real browser over the address <the reader> uses, and every frame shows its own slide, verified by eye.
- P2 · The deck reads with scripts off.
  **Done when:** the deck is loaded with script execution disabled and each `?preview=N#sN` shows exactly slide N.
- P3 · Every slide's acceptance row carries a person's tick or a dated cut.
  **Done when:** no ⬜ remains in `## Content`. Held open on purpose: this is the row no machine may write.

## States

<!-- RULE: the base owns this section. `### Decision Now` comes FIRST when the page has one, then one
     State row per Aim id, mirroring the Aims groups exactly: ⬜ not started · 🔨 in progress ·
     🧠 waiting on a person · ✅ met with the evidence named · ❄️ on ice. States is a snapshot;
     why a row changed goes in `## Log`. -->

### Decision Now
- [ ] 🗣 Accept the <N> slides for the talk?
      📍 `Part` `## Content`, one row per slide, under the embed that is the exact render.
      🔔 `Why now` <what waits on the deck: a rehearsal, a submission, a colleague read>.
      ⭐ `A ·` tick every row, which accepts all <N> renders as they stand.
      `B ·` tick the rows that are ready and name the slides to redo, which returns only those to the producer.
      🛑 `Blocks` P3, and the page's ✅ state with it.
      🤖 `If nobody answers` nothing is accepted; the rows stay ⬜, because a machine may not tick one.

### A<n> · <emoji> <Beat title> · slides <A>-<B>
- ⬜ A<n>.1 · <what is true now, in one factual clause>

### P · 🏁 The deck as a whole
- ⬜ P1 · <not started, or the browser, address, and frame sizes it was verified at>
- ⬜ P2 · <not started, or the scripts-disabled run and what each fragment showed>
- 🧠 P3 · Waiting on a person; <n> of <N> rows accepted.

## Files

<!-- RULE: name the ARTIFACTS, never the folder, and take the base's action-named groups that apply:
     ⚙️ Engines · 📋 Contracts · 🧪 Checks · 📥 Input files · 📤 Output files. `check.py` resolves
     every backticked path and reports the dead ones. -->

<!-- RULE: THE DECK ENTRY IS REQUIRED AND IT IS THE PRESENTATION SURFACE. Files is the only place a
     reader can reach the deck bare, because every embed above is locked to one slide, so the entry
     must say how to present it: which keys flip a slide and which key goes full screen. Name the
     mechanism honestly. A deck on the html-ppt runtime answers arrow keys because `runtime.js` binds
     them; a scripts-free deck answers space, PageDown, and the arrows because `scroll-snap-type: y
     mandatory` plus one-viewport slides give the same result with no key handler at all. -->

- `<group>/slides/<page name>/<deck path>`
  <The deck. Open it bare, with no fragment, to present it. Keys: <the real keys>.>
  <⚠️ Generated by `<the build script>`. Never hand-edit.  ← delete this line for a hand-authored deck>
- `<group>/slides/<page name>/source/<template and build script>`
  <The authored half and the build that fills it. Delete this row for a hand-authored deck.>
- `<the type contract>/SKILL.md`
  The contract this page is an instance of. If the two disagree, the contract wins and this page is the defect, so record the disagreement in `## States` rather than quietly diverging.

## Log
<!-- RULE: the ruling history belongs HERE, not in Content. Which slides were rebuilt, which were
     cut, who accepted what and when. Content says what the deck IS; the Log says how it got here.
     Never delete a `> USER:` line: resolve it and move it here verbatim. -->
- <YYMMDD> · <what changed>
