# Slide · every page may have a deck, and the deck is authored
state: ✅ SETTLED · one authored deck per page, owned by the slide plugin · open: none
owner: JL
page-type: design
method: describe the plugin as it runs today; history lives in Log and `_archive/`
session: 65d477e7-b493-49d7-b508-2b0f7ea0772c

## Opening
Where does a page's talk live, and how does it stay fresh?
Every page MAY have one deck at `slide/<page>-deck.html`, optional, like a `draw/` scene or a kept `chat/` session.
The deck is authored, not projected: Claude reads the page's markdown and writes a real talk onto the html-ppt shell.
A ✨ Regenerate button on both doors re-authors it in one click.
So the talk you give is never more than one click behind the page, and no deck is maintained by hand.

**What a deck is here**: one self-navigating html file of six to nine slides, opened bare to present, or framed in the 🎞 tab to read.

**Why authored and not projected**: a projection pastes a page's prose into boxes, and prose a reader skims is not a talk a presenter can speak, so the model is allowed to cut, reorder, and quote instead.

**Where a correction belongs**: the deck is derived and overwritten whole, so a hand edit to it dies at the next ✨ click; a lasting fix goes on the page, which is what every regeneration reads.

**Covered elsewhere**: `QPf1` rules that every subfolder of a page is a plugin; `QPf2` and `QPf4` are the sibling plugins this one is shaped like; the html-ppt skill (`display/html-ppt`) owns everything a deck looks like.

## Diagram
**One file, two doors, one button**: where the deck lives and how it opens and refreshes.
```text
  📋 the PAGE                        🎞 the DECK, beside it (OPTIONAL)
  ┌─────────────────────────┐       ┌──────────────────────────────┐
  │ ## Content …            │  tab  │ <page>/slide/                │
  │ the source Claude       │ ─────▶│   <page>-deck.html           │
  │ distills into a talk    │  🎞    │ html-ppt shell · themes ·    │
  └───────────┬─────────────┘       │ runtime · speaker notes      │
              │                     └──────────▲───────────────────┘
              │   ✨ Regenerate                │ writes
              └──▶ POST /_board/autodeck ── claude -p ──┘
```

## Content
### 1 · The home: derived, never registered
**One path per page**: existence of the file is the whole state.
```text
  📄 <page>/slide/<page>-deck.html
  🔑 derived from the page's own path, the way Draw derives its owner
  🕳 no manifest row, no registry: HEAD the path and you know
```
A folded page (`<name>/<name>.md`) owns the `slide/` folder, and the deck's filename is the page stem plus `-deck.html`.
Both doors below derive this path from the page they are on, so nothing keeps a list that could drift.
When the file is absent the surfaces say so and offer the button, and nothing generates a deck behind your back.

### 2 · The two doors
**Where a deck opens**: the shell tab and the page panel, one loader behind both.
```text
  🚪 the shell's 🎞 Slides tab      beside Chat and Draw, with the
                                    ✨ bar riding above the frame
  🚪 the page's 🎞 panel            a resizable right split, with
                                    ✨ regenerate in its header
  🔑 ?plain                         or the deck comes back wearing
                                    the operating shell
```
Both doors HEAD the derived path and show the saved deck, or a pointer to the ✨ button when none exists.
Every load is cache-busted, so a freshly written deck appears on the next click and a stale iframe can never survive its file.

### 3 · ✨ Regenerate: one click, one authored deck
**The loop**: what the button does and what it overwrites.
```text
  ✨ click ──▶ POST /_board/autodeck {file, prompt?}
           ──▶ live/autodeck.py runs `claude -p` on the page's .md
           ──▶ 💾 slide/<page>-deck.html replaced ──▶ frame reloads
  ⏱ a few minutes · the status word says so while it thinks
```
The ask box is optional: empty means present the page's argument, and a typed ask steers the talk's emphasis.
The `<head>` with its asset hops is computed server-side from real paths, so the model's freedom starts at `<body>` and a generated deck can never 404 its own stylesheets.
The server validates before writing: a complete document, at least three slides, the asset links present, or the deck is refused and the old file stands.
Regeneration always overwrites, so a lasting correction belongs on the PAGE, which is what every regeneration reads.

### 4 · What a deck is
**The form**: html-ppt's shell, this board's voice.
```text
  🎨 academic-report theme · T cycles the short gallery
  ⌨️ ← → move · F fullscreen · O overview · S presenter mode
  🗣 every slide carries speaker notes, surfaced by S
  🛡 scripts blocked? a data-js stamp is absent and CSS flattens
     the deck to one fragment-picked slide, so it still reads
```
A deck is six to nine slides: a cover, a closer, and distilled middles built from the page's own emoji, numbers, and quoted rulings.
The deck links at the html-ppt skill's assets by relative path, so a theme improvement reaches every deck with no rebuild.
Nothing from the skill is copied into the board, and the board contributes no CSS of its own.

### 5 · SELECTION: why the authored deck, and what lost
**The record**: the three ways a page could have had a deck, and the one left standing.
```text
  SELECTION · 260815 · JL ruled: "We will just have the AI deck"
  🏆 winner       the authored deck · claude -p writes it from the page's .md
                  it won on six real talks written the hour of the ruling
  🪦 loser        the reflow projection · live/deck.py
                  dropped · it copied a division instead of distilling it
  🪦 loser        the slide page-type · one page per deck
                  dropped · a second page to keep beside the page it was about
  📤 downstream   ../../board/page-plugins/haipipe-plugin-slide/
```
The authored deck won on evidence rather than argument: six decks were written the hour of the ruling, and the first live `/_board/autodeck` run produced a real talk for `QF2-newcomer`.
The reflow projection lost because it copied rather than distilled, so a division came back as its own paragraphs in a box; it was dropped whole, endpoint and route with it, and nothing in the board projects a page into slides now.
The slide page-type lost because it asked for a second page to maintain beside the page it was about, with one division per slide and an embedded frame each; it was dropped, and its specimen is archived whole at `_archive/QBt9-for-slide.md`, where the reason it lost stays readable.

## Aims
- [x] ✂️ `live/deck.py` retires
      Deleted 260815 with its `/_board/deck` route and the DeckMixin; the ✨ path is the only writer.
- [x] 🗑 `haipipe-page-for-slide` leaves `page-types/`
      The variant folder is deleted and `haipipe-page` 0.26.0 dropped the `page-type: slide` key, so no page can declare a type the board no longer has.
      A deleted variant leaves its old global symlink behind, and `install.sh --global` sweeps that dangling link on its next run.
- [x] 🧾 `QPs2`'s roster drops for-slide
      The hub was swept to the two-kind world the same day; its pre-sweep record is archived whole.
- [x] 👀 A deck needs no acceptance gate
      The presenter is responsible for having read what they present, and regeneration is one click, so a gate would add friction with no consumer.
      The ruling is reversible: the day a deck misleads someone, a gate goes back on.

## States
- ✅ ✂️ `live/deck.py` retires
      Met: `haipipe-board/live/` holds `autodeck.py` and no `deck.py`, and the `/_board/deck` route went with it.
- ✅ 🗑 `haipipe-page-for-slide` leaves `page-types/`
      Met: `board/page-types/` holds four variants, for-design, for-meeting, for-skill, and for-stage, and no for-slide folder is among them.
      No `haipipe-page-for-slide` resolves in the installed skill roster either, where its siblings load from `~/.claude/skills/`, and the stale-link sweep in `install.sh --global` removes any symlink still pointing at the deleted folder.
- ✅ 🧾 `QPs2`'s roster drops for-slide
      Met: the pre-sweep hub stands whole at `_archive/QPs2-page-types-260815-pre-sweep.md`, and the live `QPs2` carries the two-kind roster.
- ✅ 👀 A deck needs no acceptance gate
      Met by ruling on 260815 and unchallenged since; neither door carries a gate, and the ✨ button writes without asking anyone to accept the result.

## Files
- `../../board/haipipe-board/live/autodeck.py`
  The ✨ button's server half: prompt, validation, and the computed `<head>`.
- `../../board/haipipe-board/assets/js/10-drawer/70-plugin-slides.js`
  The page panel: derives the deck path, shows it or the pointer, carries ✨ regenerate.
- `../../board/haipipe-board/live/shell.py`
  The Slides tab and its ✨ bar; one loader, cache-busted.
- `../../display/html-ppt/assets/academic-report-extras.css`
  The house style, including the monospace carve-out that keeps ascii figures aligned inside a Times deck.
- `../../display/html-ppt/`
  The skill that owns what a deck looks like; every deck links at its assets.

## Log
- ✅ 260816 · [REVISE-CC, JL ruled] the fourth aim closed on evidence, and its heading narrowed back
      JL ruled the earlier reopening wrong on both counts: "everywhere it is installed" widened the aim instead of clarifying it, and the evidence for the aim was on disk the whole time.
      The heading went back to the repo fact, `haipipe-page-for-slide` leaves `page-types/`, and the aim is ticked again with a ✅ State row: `board/page-types/` holds for-design, for-meeting, for-skill and for-stage and nothing else, no `haipipe-page-for-slide` resolves in the installed skill roster, and the stale-link sweep in `install.sh --global` removes any symlink still pointing at the deleted folder.
      With all four aims met the `state:` line is ✅ SETTLED again.
      Three smaller repairs rode along: the installer is repo-root `install.sh`, so the folder prefix two lines used to hang in front of it is gone; the `SELECTION` record now writes its `downstream` path board-relative like every `Files` row and says why the winner won and why each loser lost; and the acceptance aim dropped its attribution parenthetical so the Aims and States headings read the same, the delegation staying here in the Log where attribution belongs.
      One thing this pass could not do: the writer had no shell, so the symlink timestamps JL cited were not re-read, and the ✅ rests on the page-types tree and the loaded skill roster instead.
- 🩹 260816 · [REVISE-CC] the page made honest again, and the selection written down
      A review found the page saying SETTLED while its own second aim said a re-run was still owed, so the status was corrected instead of the sentence.
      That aim was reopened with a 🧠 State row and its heading widened to every place the skill is installed, on the ground that an `install.sh --global` re-run was still owed.
      The `state:` line became a row under 110 characters with an `open:` part, and States became one row per aim carrying its own evidence.
      The tier choice moved out of this Log into a `SELECTION` division, which is what a `page-type: design` page closes on and what the 260815 2010 rewrite had swept away.
      Smaller repairs in the same pass: the blank line that had pushed the whole rationale into the drawer is gone, the drawer's parts carry bold labels, the Files row for the html-ppt skill lost one `../`, and these records were split into headings with folded explanations.
- 🗳 260815 2100 · [CHECK-CC, JL delegated] the four aims worked through in one pass
      JL delegated the check ("you should check it yourself, we will just keep the things with slides like the plugin") and CC closed three aims by subtraction and one by ruling.
      `live/deck.py` was deleted with its `/_board/deck` route and the DeckMixin; `haipipe-page-for-slide` was removed and `haipipe-page` bumped to 0.26.0, with `Design-3` re-plugged and its title refreshed; `QPs2` was swept to the two-kind hub.
      The acceptance question was ruled no-gate by CC under that delegation, on the ground that a presenter is responsible for having read what they present.
      Same pass: ascii figures inside decks render aligned again, through a monospace carve-out in `academic-report-extras.css` where strict Times had crushed them, plus figure-alignment rules in autodeck's prompt.
- ✂️ 260815 2010 · [REVISE-CC, JL asked] rewritten to the working contract only
      JL asked to "focus on how current slide plugin work", so the page stopped narrating a type that no longer exists.
      The dead type's story and the tier history left for `_archive/QBt9-for-slide.md` and this Log, where the board keeps history.
      The selection record left with them, which is the gap the 260816 pass repaired.
- ✨ 260815 1930 · [REVISE-CC, JL asked] the ✨ Regenerate button shipped on both doors
      `POST /_board/autodeck` runs `claude -p` server-side and writes the deck, so a talk is re-authored without leaving the browser.
      Deck loads became cache-busted, and the display plugin's move from `display/skills/html-ppt` to `display/html-ppt` was repaired across every deck.
      The runtime-versus-fallback freeze, where only slide 1 was ever visible, was fixed with the `data-js` stamp.
- 🚪 260815 1900 · [JL via CC] `haipipe-plugin-slide` drafted under `page-plugins/`
      Round 2 of the thin-door migration: the new skill is delta-only over `haipipe-plugin` and restates none of the four-facet contract.
- 🗑 260815 1730 · [REVISE-CC, JL ruled] the slide page-type retired
      JL ruled it plainly: "the slide will just be the plugin version".
      Every page may now have one optional deck in `slide/`, the QBt9 specimen was archived whole, and the third kind was reduced to material sitting after for-skill and for-meeting.
- 🏆 260815 1700 · [REVISE-CC, JL ruled] the deck tier collapsed to the authored deck
      JL's words were "We will just have the AI deck", which retired the browser reflow from both the client and the shell.
      Six decks were authored the same hour, which is the evidence that the authored tier could carry the board on its own.
      This is the ruling the `SELECTION` division now records.
