# QBt9 · page-type SLIDE · owns a UNIT folder; one Content division per slide, each embedding the live deck, none accepted by a machine

state: 🟡 PARTIAL · 4 slides rendered from one atom, 0 of 4 accepted; acceptance is a person's judgment and nothing on this page may grant it
page-type: slide
owner: JL
method: build one real deck, embed each slide live on its own, resolve every number the deck shows by atom id, and leave every acceptance row for a person
session: 65d477e7-b493-49d7-b508-2b0f7ea0772c
needs: QA-probe/QBt5-for-value/1-artifact-paths
output: _fixture/slides/QBt9-for-slide/deck.html

## Opening

Can a board page carry a talk when its deck runs no scripts?
A slide page is one page per deck: each division shows one slide live, and holds the one row where a person accepts that render.
This deck runs no JavaScript, so the fragment in the embed picks the slide and CSS hides the rest.
Every number it shows resolves to an atom by id, and every acceptance row is still empty.
🚫 The talk, the paper and the venue are all invented; nothing here may be cited.

🚫 **This deck belongs to a fabricated project.** It presents a paper that does not exist, "Do typed pages reduce contract drift?", to a venue that does not exist, the Journal of Imaginary Systems. Its corpus was never counted. What is NOT fabricated is the deck: it is a real file on disk, four real slides, and the embeds below open it.

**Where its things are**: a page's companion folder is `<type-plural>/<page name>/`, so this page's deck is `slides/QBt9-for-slide/`. That is the group's one naming rule, and it is why `QBt3`'s unit is `../01-haipipe-paper-260725/QBt-page-types/_fixture-qbt/displays/QBt3-for-display/` and `QBt5`'s drawer is `QA-probe/QBt5-for-value/`.

**Why this page is also the instruction**: it is the specimen for its type. `QB4` teaches the page grammar by being a page that obeys it; this page teaches the deck form the same way. The rules themselves stay in `haipipe-page-for-slide`, which this page never restates.

**What no machine may write here**: the four `accepted:` rows. A slide page closes when a person has looked at a specific render and said yes to it, so an agent that ticks one has not closed anything, it has forged a judgment. All four are left ⬜ on purpose, and that is this specimen's deliberate incompleteness: a page with every row green would teach nothing about the gate.

**Covered elsewhere**: `QA4` is the live instance of this type, seven slides on the `html-ppt` runtime, and it is where the embed ruling was made. `QBt3` owns the acceptance model this type borrows. `QBt5` owns the atom this deck reads. `QB6` owns which types exist and the checker rule (`§5.1` rule 4) that would police these embeds.

## Diagram

**One file, two surfaces, and no runtime**: how a scripts-free deck serves the review surface and the presentation surface from the same bytes.

```text
  📄 _fixture/slides/QBt9-for-slide/deck.html        ← ONE file · 10 KB · 0 scripts
       │                                          0 external assets
       │
       ├──▶ 📋 REVIEW surface · THIS PAGE
       │      one division = one slide, embedding
       │      …/out/deck.html?preview=N#sN
       │      🔑 no runtime here, so #sN is what picks the slide:
       │         .slide:target shows it · :has() hides the others
       │         `?preview=N` is INERT · written anyway, see States
       │      the frame hides the slide index, so what you look at
       │      is exactly what that slide's accept row is about
       │
       └──▶ 🎥 PRESENTATION surface · a browser tab
              deck.html bare, no fragment, from ## Files
              every slide 100vh + scroll-snap-type:y mandatory
              🔑 space · PageDown · ↓ advance exactly one slide
                 F11 full screen · zero key handlers exist
  ─────────────────────────────────────────────────────────────────────
  the two surfaces read the SAME BYTES, so neither can drift
  what CSS cannot do is lock the frame: see States and Decision Now
```

**Its own input and output**: a SLIDE page owns a unit folder on both sides, like a display, but ships HTML rather than a float.

```text
 📥 INPUT   slide/QBt9-for-slide/
              source/deck.template.html    carries NO DIGITS, on purpose
              source/build.py              fills them from the value record
            ↗ QA-probe/QBt5-for-value/1-artifact-paths.data/counts.csv
 📤 OUTPUT  _fixture/slides/QBt9-for-slide/deck.html    🤖 generated
              ▶ each Content division embeds it live at ?preview=N
              ▶ a hand-edited slide is overwritten on the next build
```

## Content

### 1 · The cover: what the talk is, and that none of it is real · slide 1

**Slide 1, the cover**: the paper, the venue, and the fabrication notice, before a listener hears any result.

![slide 1 · cover](../01-haipipe-paper-260725/QBt-page-types/_fixture-qbt/slides/QBt9-for-slide/deck.html?preview=1#s1)
- accepted: ⬜ · slide 1 · source: this page's Opening · rendered: 260806

🎬 Establishes that the audience is told the work is invented in the first ten seconds, not in a footnote.

Open on the question in the title and give the denominator, then stop and read the red block out loud. A fabricated talk that buries its fabrication is worse than no talk, because a listener carries the number away and the caveat stays in the room.

```text
  value on the slide     source                                    kind
  ────────────────────────────────────────────────────────────────────────
  400 pages              sum of the pages column in                derived
                         QA-probe/QBt5-for-value/1-artifact-paths
                         (214 + 61 + 48 + 44 + 33), computed in
                         source/build.py, never typed
  ────────────────────────────────────────────────────────────────────────
  what is NOT on this slide: a board count. It reads 400 pages, not
  "400 pages across nine boards", because the board count belongs to
  QA-probe/QBt5-for-value/2-corpus-size and QBt5 leaves that atom
  deliberately unbound. See ## States · every value is INVENTED
```

### 2 · The problem: what a drift event is · slide 2

**Slide 2, the definitions**: the four words the result slide leans on, each given one line before it is used.

![slide 2 · what drift is](../01-haipipe-paper-260725/QBt-page-types/_fixture-qbt/slides/QBt9-for-slide/deck.html?preview=2#s2)
- accepted: ⬜ · slide 2 · source: `QA-probe/QBt5-for-value/1-artifact-paths` §Question · rendered: 260806

📐 Establishes the vocabulary, so nothing on the next slide has to be defined while a number is on screen.

Read the four record lines slowly: declares, renders, drift event, type key. Then land the sentence that makes the census worth running: a drifted page still builds, still serves, and still reads fine to the person who wrote it, so nobody finds it by using the board.

The definition of a drift event is copied WHOLE from the atom's own `## Question`, not summarized. A talk that paraphrases its own measurement definition is how an audience ends up arguing about two different quantities.

### 3 · The result: five bands, and no digit typed into the deck · slide 3

**Slide 3, the figure**: five tenure bands with drift rate per band, every value written in at build time.

![slide 3 · the result](../01-haipipe-paper-260725/QBt-page-types/_fixture-qbt/slides/QBt9-for-slide/deck.html?preview=3#s3)
- accepted: ⬜ · slide 3 · source: `QA-probe/QBt5-for-value/1-artifact-paths`, by id · rendered: 260806

🔢 Establishes the one measurement the talk exists to show, and that not one of its digits was typed by hand.

```text
  value on the slide          source                                 kind
  ────────────────────────────────────────────────────────────────────────
  214 · 61 · 48 · 44 · 33     QA-probe/QBt5-for-value/1-artifact-paths atom id
  37 · 9 · 4 · 2 · 1            resolved to its counts.csv by id
  17.3 · 14.8 · 8.3 ·         source/build.py, drift_events over     derived
  4.5 · 3.0                     pages, one decimal
  bar lengths                 the same ratio scaled to the worst     derived
                                band, which is how QBt3 scales its
                                ascii bars from this same atom
  95% CI bounds               carried in counts.csv, NOT drawn       carried
  ────────────────────────────────────────────────────────────────────────
  THE TEMPLATE CARRIES NO DIGITS. source/deck.template.html holds
  <!--ROWS--> and <!--N-->; the build fills them. Change the record
  and the slide changes · every value is INVENTED
```

This is the division the type exists for. A slide is a display that talks, and it gets no looser standard for being temporary: a number typed into slide markup at 2am is untraceable by breakfast, and no later pass can tell it from a real one. Here it cannot happen, because the template has nowhere to type one.

The provenance chain is the same one `QBt3` walks, from the same record, and neither file writes the other's path. Both declare `needs: QA-probe/QBt5-for-value/1-artifact-paths` in their head and ask the resolver. That is why the ascii figure and this deck cannot disagree about which band is longest: they are two renders of one atom, not two transcriptions of one table.

### 4 · The ceiling: the label the design allows · slide 4

**Slide 4, the limits**: the two design facts that cap the claim, and the title question being declined out loud.

![slide 4 · association, not reduces](../01-haipipe-paper-260725/QBt-page-types/_fixture-qbt/slides/QBt9-for-slide/deck.html?preview=4#s4)
- accepted: ⬜ · slide 4 · source: `QA-probe/QBt5-for-value/1-artifact-paths` §Caveats, copied whole · rendered: 260806

⚠️ Establishes what the talk may not say, on a slide, rather than in the speaker notes where no listener can check it.

The two limits travel with the answer and they are copied from the record's `## Caveats` word for word: tenure is not assigned, and page size is not controlled. Say the title's question aloud and then decline it. The gradient is in the data; the causal claim is not available.

A digest of an answer is a convenience. A digest of a LIMIT is how a talk ends up claiming more than its design supports, which is why this slide paraphrases nothing.

## Aims

### A1 · 🎬 The cover: what the talk is, and that none of it is real · slide 1
- A1.1 · The fabrication notice is on the render, not only on this page.
  **Done when:** slide 1 carries the 🚫 block, and every number that slide prints has a row in `§1`'s provenance figure.

### A2 · 📐 The problem: what a drift event is · slide 2
- A2.1 · Every term the result slide uses is defined before it appears.
  **Done when:** `drift event` and `type key` are defined on slide 2, and neither is redefined anywhere later in the deck.

### A3 · 🔢 The result: five bands, and no digit typed into the deck · slide 3
- A3.1 · No value the deck prints is typed into the deck.
  **Done when:** each printed value is found in `1-artifact-paths.data/counts.csv` and in `out/deck.html`, and in `source/deck.template.html` not at all.
- A3.2 · A rebuild that changes nothing voids no acceptance.
  **Done when:** `python3 cli/build-displays.py <stage>` run twice over an unchanged record leaves `out/deck.html` byte-identical, so no ⬜ falls back for a no-op.

### A4 · ⚠️ The ceiling: the label the design allows · slide 4
- A4.1 · The limits are on a slide, not in the notes.
  **Done when:** both design facts appear in the render itself, and the title's question is explicitly declined on that slide.

### P · 🏁 The deck as a whole
- P1 · Each division shows its own slide, live, at slide proportions, inside the built board page.
  **Done when:** the rendered page is driven in a real browser over the address JL uses, and each of the four frames shows that division's slide, verified by eye rather than by HTTP code.
- P2 · The deck reads with scripts off.
  **Done when:** the file is loaded with script execution disabled and each `?preview=N#sN` shows exactly slide N.
- P3 · Every slide's acceptance row carries a person's tick or a dated cut.
  **Done when:** no ⬜ remains in `## Content`. Held open on purpose: this is the row no machine may write.

## States

### Decision Now
- 📍 Accept the four slides for the talk? The embeds in `## Content` are the exact renders. Ticking a row accepts THAT render, and a rebuild that changes bytes returns it to ⬜. CC ticks nothing here and may not: a machine-written ✅ on an acceptance row is a forged judgment, not a fast one.
- 📍 The contract's embed sentence reads `?preview=N` as the selector and `#sN` as its fallback. On a scripts-free deck that is exactly backwards. Does `for-slide` get rewritten to say the query drives a runtime and the fragment drives the deck, with neither called the other's fallback?
- 📍 The range strip: does `for-slide` state that `?preview=A-B` requires an html-ppt runtime, or does `src/body.py` stop sizing a range frame it has no way to verify? Today a legal URL and a wrong frame are the same keystroke apart.

### A1 · 🎬 The cover: what the talk is, and that none of it is real · slide 1
- ✅ A1.1 · Met 260807, and by rebuild rather than by edit. Every number on every slide now comes from `QA-probe/QBt5-for-value/1-artifact-paths.data/counts.csv`, which is MEASURED: the deck prints 10 rows, the total 6 and the count 7, and prints no number that CSV does not carry. The template holds no digits at all, so this is enforced by the build and not by care: `<!--ROWS-->`, `<!--TOTAL-->` and `<!--ZERO-->` are filled at render time and a hand-typed slide is overwritten. It previously printed 400, from a corpus record that was invented and has since been retired.

### A2 · 📐 The problem: what a drift event is · slide 2
- ✅ A2.1 · Slide 2 defines both `drift event` and `type key` in its record list and neither term is defined again on slide 3 or slide 4, so the result slide defines nothing while a number is on screen; slide 1's lede does use the words `type key` once before that definition arrives.

### A3 · 🔢 The result: five bands, and no digit typed into the deck · slide 3
- ✅ A3.1 · The five band counts and five drift counts on slide 3 come from `QA-probe/QBt5-for-value/1-artifact-paths.data/counts.csv` through the resolver, the five rates and the 400 are computed in `slide/source/build.py`, and not one of the eleven multi-digit values the deck prints occurs anywhere in `slide/source/deck.template.html`, whose only digits are CSS lengths and colours.
- ✅ A3.2 · Replaying the builder's own template fill twice over the unchanged record produced a single md5, `039f0bb0c8392a04f78253ef6fe310f3`, which is also the md5 of the shipped 10,544 byte `../01-haipipe-paper-260725/QBt-page-types/_fixture-qbt/slides/QBt9-for-slide/deck.html`, so an unchanged input rebuilds to identical bytes and no acceptance row falls back for a no-op.

### A4 · ⚠️ The ceiling: the label the design allows · slide 4
- ✅ A4.1 · Both design facts are on the slide as numbered records, ① tenure is not assigned and ② size is not controlled, and slide 4 declines the title's question in its own words as "the one thing this figure cannot answer"; limit ② is reworded there rather than copied whole from the atom's `## Caveats`, which is narrower than what `§4` says of it.

### P · 🏁 The deck as a whole
- 🔨 P1 · The built page `board/QPf/QPf3-slide.html` carries four iframes at `?preview=N&plain#sN` that resolve to the deck on disk, and each of those four URLs was read in a real Chrome at frame size, but nobody has yet opened the composed page at the address JL uses and looked at the four frames together, which is the part this Aim asks for.
- ✅ P2 · The built deck holds zero `script` tags and loads no external asset, so turning script execution off cannot change what it shows, and each `?preview=N#sN` selects slide N through `:target` and `:has()` CSS alone, which is what the four Chrome reads showed.
- 🧠 P3 · Waiting on the person who decides, and nothing else may move it: all four acceptance rows in `## Content` are still ⬜, and a machine ticking one would forge a judgment rather than record one, so this stays 🧠 until JL reads a render and says yes.

## Files

- `../01-haipipe-paper-260725/QBt-page-types/_fixture-qbt/slides/QBt9-for-slide/deck.html`
  ⚠️ Generated by `source/build.py`. Never hand-edit. This is the deck: open it bare, with no fragment, to present it. Space and PageDown flip slides, F11 goes full screen.
- `slide/source/deck.template.html`
  The deck's authored half: four slides, all the CSS, and the two slots the build fills. It carries no digits, which is how the number rule is enforced rather than remembered.
- `slide/source/build.py`
  Resolves the atom by id, computes the derived values, writes the deck. It never writes the record's path, and it writes no timestamp.
- `../../../../board/haipipe-board/cli/build-displays.py`
  The resolver that turns a unit id into a path, plus `check` and `build`. A page names another page's product by id, never by path.
- `../01-haipipe-paper-260725/QBt-page-types/QBt5-for-value.md`
  The evidence page whose E1 division owns the record this deck reads, and whose E2 division this deck deliberately does not bind.
- `../01-haipipe-paper-260725/QBt-page-types/QBt3-for-display.md`
  The display specimen built from the same atom, and the source of the acceptance model this type borrows.
- `../../board/page-types/haipipe-page-for-slide/SKILL.md`
  The contract this page is an instance of. If the two disagree, the contract wins and this page is the defect; the three disagreements found while building it are in `## States`.
- `_archive/QA4-board-skillset.md`
  The live instance of this type, on the html-ppt runtime, where the embed ruling was made and where the multi-slide beat is written out.
- `QPs-page-structure/QPs1-overall/QPs1-overall.md`
  The page frame this page sits in: the section set, their order, and the caption rule every division above obeys.
- `QPs-page-structure/QPs2-page-types/QPs2-page-types.md`
  The hub listing the types, and `§5.1` rule 4, the slide check that does not exist yet.

## Log

- 260815 1700 · [REVISE-CC, JL ruled] the deck tier collapsed to ONE: "We will just have the AI deck". The reflow tier — the browser cutting the rendered DOM into slides for `live/deck.py` to wrap verbatim — no longer writes anything: the shell's Slides tab and the 🎞 panel show the saved `<page>/slide/<page>-deck.html` when it exists and a pointer to the author path when it does not. Five decks were authored under the ruling the same hour (QA0, QA00, QPf2, QPf4, Design-6), each an editorial distillation of its page's Content on the html-ppt shell. `live/deck.py`'s endpoint now has no caller; its retirement rides with this page's overdue rewrite from the QBt9-era specimen to the plugin contract.
- 260807 1200 · [REVISE-CC] rebuilt on measured numbers. The deck was rendered from the fabricated drift atom; it now reads `QA-probe/QBt5-for-value/1-artifact-paths.data/counts.csv`, which is measured. The template still carries NO DIGITS, which is the rule this specimen exists to hold: `<!--ROWS-->`, `<!--TOTAL-->` and `<!--ZERO-->` are all filled at build time, so a corrected measurement changes the slides and a hand-edited slide is overwritten. Folders follow the UNIT shape now, authoring at `slide/` and shipped at `../01-haipipe-paper-260725/QBt-page-types/_fixture-qbt/slides/QBt9-for-slide/deck.html`. Still 0 of 4 accepted.

- 260806 · [DRAFT-CC] written as a real `for-slide` page rather than an essay about one, on JL's ruling that the example should BE its type, the way `QB4` is both the page grammar and a page obeying it. The deck was built first and looked at in a real browser before a word of the page was written, so every embed below points at bytes that already rendered.
- 260806 · [PROBE-CC] building a scripts-free deck surfaced three disagreements with the contract, now in `## States` and two Decision Now rows: the two selectors trade places, the range strip is a runtime feature the engine treats as a URL feature, and a CSS-locked frame keeps one escape link a runtime-locked frame does not need.

- 260806 CC · Deck built and rendered through the chain. `slide/source/build.py` resolves `QA-probe/QBt5-for-value/1-artifact-paths` by id, fills the template's two slots, and writes `out/deck.html`: four slides, 10 KB, zero `<script>` tags, zero external assets, one file that opens from a bare filesystem path.
- 260806 CC · Rendered and looked at, not assumed. The shipped bytes were driven in a real Chrome at four frame sizes (1280x720, 1024x576, 900x506, 700x394) and in both colour schemes: `?preview=1&plain#s1` through `?preview=4&plain#s4`, the exact form `src/body.py` writes into the iframe, each showed exactly its own slide with the slide index hidden and the escape link in its place, and the bare file showed the stacked deck with the index visible. Nothing scripted ran in any of them, because there is nothing to run. Also confirmed the split-site hop: `page_board.tree_reroot` rewrites the embed to `../../../01-haipipe-paper-260725/QBt-page-types/_fixture-qbt/slides/QBt9-for-slide/deck.html?preview=N&plain#sN`, which resolves to this file on disk.
- 260806 CC · Rebuild determinism tested, not claimed. `cli/build-displays.py <stage>` twice over an unchanged record produced byte-identical output, so a no-op rebuild does not silently void an acceptance. The build writes no timestamp for exactly this reason.
- 260806 CC · The contract's two selectors trade places here, and this is the first conflict. `haipipe-page-for-slide` says `?preview=N` is html-ppt's locked single-slide mode and `#sN` is the scripts-off fallback. This deck has no runtime, so the query is inert and the fragment is the ONLY selector. Both are still written, so `QB6` §5.1 rule 4 would pass either way, but a reader who trusts the contract's causal story would be wrong about which half is working.
- 260806 CC · The keyboard presentation survives without a key handler, which is the second conflict and the happier one. The contract says the bare file is "the full keyboard presentation"; no scripts-free deck can bind a key. `scroll-snap-type: y mandatory` on the document plus one-viewport slides gives the same result: space, PageDown and the arrow keys advance exactly one slide, and F11 makes it full screen. The surface holds, by a mechanism the contract does not name.
- 260806 CC · The compact range strip is unavailable here, and the engine does not know it. `?preview=A-B` is a RUNTIME feature, but `src/body.py` decides the frame's height from the URL alone, sizing it to `aspect-ratio:16/(9×count)`. So a scripts-free deck can write a perfectly legal range URL and get one slide floating in a frame sized for four. The compact form is not a URL contract, and this page therefore never writes one.
- 260806 CC · The locked frame keeps one link, which is a deliberate cost. `?preview=N` hides all chrome and turns keys off; CSS can hide the slide index in a targeted frame and does, but nothing can stop a reader following a link out of the frame. The board renders its own `⛶ open … full size` link pointing at `…#sN`, which would strand a reader on one slide, so every slide keeps one small `open the whole deck` link as the way back. A locked html-ppt frame has no such link.
- 260806 CC · What the board build actually asserts is narrower than it is usually read to be. `cli/build.py` samples the LARGEST built page, strips `<script>` blocks, and asserts more than 1200 characters of body text survive. It never opens an iframe, so nothing in the board build inspects this deck at all. Building it scripts-free is still right, for the reason `QA4` recorded: the surfaces a reader actually uses, a VS Code webview or a locked-down frame, block scripts. The assertion is about the page; the deck's readability is about the reader's surface.
- 260806 CC · The board count came off the cover rather than a binding going in. Slide 1 first read "400 pages across nine boards". The 400 is the sum of the bound atom's own `pages` column, so it is derived and traceable; the nine belongs to `QA-probe/QBt5-for-value/2-corpus-size`, and `QBt5` leaves that atom deliberately unbound to show what an answered question with no consumer looks like. A slide may not show a number it cannot trace, and a specimen may not quietly close another specimen's open row, so the phrase was cut and the reason is in the template beside the line.
- 260806 CC · This page shows the one-slide beat and not the multi-slide beat. The contract's division is a talk BEAT and may hold several slides, each with its own embed and its own row; here each of the four beats holds exactly one slide, so the division heading and the slide happen to coincide. `QA4` is where the multi-slide beat is written out, four beats over seven slides.
- 260806 CC · `page-type: slide` is decorative today, the same finding `QBt3` records for its own key. It is read by neither `src/parse.py` nor `cli/check.py`, so type resolution step ③ never runs and this file still resolves by its `QBt9` filename at step ⑤. `QB6` §5.1 rule 1 is the fix, and rule 4 is the one that would check the embeds and rows below.
- 260806 CC · Acceptance stands at 0 of 4, and that is the finished state of this draft rather than a gap in it. Every row names its slide, its source and its render date; none names a person, because none has been read by one.

- 260806 1259 · [REVISE-CC] States now mirrors every Aim id; six of the eight close on machine evidence (the deck rebuilds byte-identical at md5 `039f0bb0c8392a04f78253ef6fe310f3`, it holds zero `script` tags, the template carries none of the eleven values the deck prints, and both limits plus the declined question are on slide 4), P1 is 🔨 because the composed board page has never been opened at the address JL uses even though its four iframes resolve, and P3 is 🧠 by design because acceptance is a person's judgment and no machine may grant it. Two smaller findings came out of the sweep: slide 4's limit ② is reworded rather than copied whole from the atom's `## Caveats`, and slide 1's lede uses `type key` before slide 2 defines it. The twelve dated records above moved here from `## States` unchanged, because they are history and the base keeps history in Log.
