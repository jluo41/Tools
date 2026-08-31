# Slide · every page may have a deck, and the deck is authored
state: ✅ SETTLED · one authored deck per page, owned by the slide plugin · open: none
owner: JL
method: describe the plugin as it runs today; history lives in Log and `_archive/`
session: 65d477e7-b493-49d7-b508-2b0f7ea0772c

## Opening
Where does a page's talk live, and how does it stay up to date?
Every page may have one deck of slides at `slide/<page>-deck.html`.
It is optional, the same way a `draw/` scene or a kept `chat/` session is.
Claude writes the deck by reading the page and choosing what to say.
A ✨ Regenerate button sits on both doors and rewrites the deck in one click.
So the talk is never more than one click behind the page, and nobody keeps a deck by hand.

**What a deck is here**: one html file of six to nine slides that moves itself.
You open it bare to present, or inside the 🎞 tab to read.

**Why Claude writes it, instead of the page pouring itself in**: pouring a page into boxes gives you prose.
Prose a reader skims is not a talk a person can speak, so the model may cut, reorder, and quote.

**Where a fix belongs**: the deck is rebuilt for you and overwritten whole, so a hand edit to it dies at the next ✨ click.
A lasting fix goes on the page, because the page is what every rebuild reads.

**Covered elsewhere**: `QPf1` rules that every subfolder of a page is a plugin.
`QPf2` and `QPf4` are the sibling plugins this one is shaped like, and the html-ppt skill (`display/html-ppt`) owns everything a deck looks like.

## Diagram
**One file, two doors, one button**: where the deck sits, how you open it, and how you rebuild it.
```text
  📋 the PAGE                        🎞 the DECK, beside it (OPTIONAL)
  ┌─────────────────────────┐       ┌──────────────────────────────┐
  │ ## Content …            │  tab  │ <page>/slide/                │
  │ what Claude reads to    │ ─────▶│   <page>-deck.html           │
  │ write the talk          │  🎞    │ html-ppt shell · themes ·    │
  └───────────┬─────────────┘       │ runtime · speaker notes      │
              │                     └──────────▲───────────────────┘
              │   ✨ Regenerate                │ writes
              └──▶ POST /_board/autodeck ── claude -p ──┘
```

## Content
### 1 · One path per page, and no list to keep in step
**One path per page**: if the file is there, the page has a deck.
```text
  📄 <page>/slide/<page>-deck.html
  🔑 worked out from the page's own path, the way Draw finds its owner
  🕳 no list, no registry: ask for the path and you know
```
📌 This part settles where a deck lives, and how both doors find it with no list to keep.
A folded page (`<name>/<name>.md`) owns the `slide/` folder.
The deck's file name is the page name plus `-deck.html`.
Both doors below work this path out from the page they are on, so no list is kept and no list can go stale.
When the file is not there, both views say so and offer the button.
Nothing builds a deck behind your back.

### 2 · Two ways in, and neither can show you an old deck
**Where a deck opens**: the shell tab and the page panel, with one loader behind both.
```text
  🚪 the shell's 🎞 Slides tab      beside Chat and Draw, with the
                                    ✨ bar sitting above the deck
  🚪 the page's 🎞 panel            a right side panel you can resize,
                                    with ✨ regenerate in its header
  🔑 ?plain                         ask for the deck this way, or it
                                    comes back wearing the whole shell
```
📌 This part settles that both doors read the same saved file, and that neither can show you an old one.
Both doors send a HEAD request for that path, which is a small web question that asks only whether a file is there.
They show the saved deck, or a pointer to the ✨ button when there is none.
Every load skips the browser cache, so a freshly written deck appears on the next click.
An old copy in the window can never outlive the file it came from.

### 3 · One click rewrites the deck, and always replaces it
**What the button does**: the steps it runs, and the file it replaces.
```text
  ✨ click ──▶ POST /_board/autodeck {file, prompt?}
           ──▶ live/autodeck.py runs `claude -p` on the page's .md
           ──▶ 💾 slide/<page>-deck.html replaced ──▶ the view reloads
  ⏱ a few minutes · the status word says so while it thinks
```
📌 This part settles that a rebuild always replaces the whole deck, so a lasting fix belongs on the page.
The ask box is optional.
Leave it empty and the deck presents the page's argument, or type an ask and the talk leans the way you asked.
The server writes the `<head>` and its asset links itself, from real paths on disk.
So the model starts writing at `<body>`, and a new deck can never miss its own stylesheets.
The server also checks the result before it saves anything.
It wants a whole document, at least three slides, and the asset links in place.
If any of that is missing the new deck is refused, and the old file stays.
A rebuild always overwrites, so a lasting fix belongs on the PAGE, and the page is what every rebuild reads.

### 4 · What you get: six to nine slides you can stand up and present
**The look**: html-ppt supplies the shell, and the board supplies the words.
```text
  🎨 academic-report theme · T cycles the short gallery
  ⌨️ ← → move · F fullscreen · O overview · S presenter mode
  🗣 every slide carries speaker notes, and S shows them
  🛡 scripts blocked? the data-js stamp is missing, so CSS shows
     one slide picked by the url, and the deck still reads
```
📌 This part settles what a deck looks like, and where that look comes from.
A deck is six to nine slides: a cover, a closing slide, and middle slides in between.
The middles are built from the page's own emoji, numbers, and quoted rulings.
The deck points at the html-ppt skill's files by relative path.
So a better theme reaches every deck at once, with nothing to rebuild.
Nothing from the skill is copied into the board, and the board adds no CSS of its own.

### 5 · Why Claude writes the deck, and what was dropped
**The record**: three ways a page could have had a deck, and the one still standing.
```text
  SELECTION · 260815 · JL ruled: "We will just have the AI deck"
  🏆 winner       the deck Claude writes · claude -p writes it from the page's .md
  🪦 loser        the reflow copy · live/deck.py · dropped
  🪦 loser        the slide page-type · one page per deck · dropped
  📤 downstream   ../../board/page-plugins/haipipe-plugin-slide/
```
📌 This part settles which of the three ways won, and why each of the other two was dropped.
This way won on evidence, not on argument.
Six decks were written in the hour of the ruling, and the first live `/_board/autodeck` run produced a real talk for `QF2-newcomer`.
The reflow copy lost because it copied instead of choosing, so one part of the page came back as its own paragraphs in a box.
It was dropped whole, endpoint and route with it, and nothing in the board turns a page into slides that way now.
The slide page-type lost because it asked for a second page to keep beside the page it was about.
That second page held one part of the page per slide, each with a frame inside it.
It was dropped, and its example is kept whole at `_archive/QBt9-for-slide.md`, where the reason it lost stays readable.

## Aims
- [x] ✂️ Only the ✨ button writes a deck, so `live/deck.py` goes
      It was deleted on 260815 with its `/_board/deck` route and the DeckMixin, so the ✨ path is the only writer left.
- [x] 🗑 `haipipe-page-for-slide` leaves `page-types/`
      The folder is deleted, and `haipipe-page` 0.26.0 dropped the `page-type: slide` key.
      So no page can claim a type the board no longer has.
      A deleted folder leaves its old global symlink behind, and `install.sh --global` clears that dead link on its next run.
- [x] 🧾 `QPs2`'s list of page types drops for-slide
      The hub was cut back to the two-kind world the same day, and its earlier version is kept whole.
- [x] 👀 Nobody has to sign off on a deck before it is used
      The person presenting is responsible for having read what they present.
      A rebuild is one click, so a sign-off step would slow people down and help nobody.
      The ruling can be undone: the day a deck misleads someone, the sign-off comes back.

## Discussion

### From the retired States section (merged 260831)
- ✅ ✂️ Only the ✨ button writes a deck, so `live/deck.py` goes
      Met: `haipipe-board/live/` holds `autodeck.py` and no `deck.py`, and the `/_board/deck` route went with it.
- ✅ 🗑 `haipipe-page-for-slide` leaves `page-types/`
      Met: `board/page-types/` holds four kinds, for-design, for-meeting, for-skill, and for-stage, and no for-slide folder is among them.
      No `haipipe-page-for-slide` is among the loaded skills either.
      The stale-link sweep in `install.sh --global` removes any symlink still pointing at the deleted folder.
- ✅ 🧾 `QPs2`'s list of page types drops for-slide
      Met: the earlier hub stands whole at `_archive/QPs2-page-types-260815-pre-sweep.md`, and the live `QPs2` carries the two-kind list.
- ✅ 👀 Nobody has to sign off on a deck before it is used
      Met by CC's ruling under JL's 260815 delegation; neither door carries a gate.
      The ✨ button writes without asking anyone to accept the result.

## Files
- `../../board/haipipe-board/live/autodeck.py`
  The ✨ button's server half: the prompt, the checks, and the `<head>` it works out.
- `../../board/haipipe-board/assets/js/10-drawer/70-plugin-slides.js`
  The page panel: it works out the deck path, shows the deck or the pointer, and carries ✨ regenerate.
- `../../board/haipipe-board/live/shell.py`
  The Slides tab and its ✨ bar, with one loader that always skips the cache.
- `../../display/html-ppt/assets/academic-report-extras.css`
  The house style, including the monospace rule that keeps ascii figures lined up inside a Times deck.
- `../../display/html-ppt/`
  The skill that owns what a deck looks like, and every deck points at its files.

## Log
- 📖 260816 · [REVISE-CC, JL ruled] the page was rewritten in plain words, for a reader with ADHD whose English is a second language (JL: "我真的读不下去"). The 🧭 Outline tab had been showing this page's own sentences back, and they were unreadable, so the tab was right and the prose was not. Every division title now names its consequence instead of a mechanism, each one gained a `📌` line saying in one sentence what the part settles, and every aim, `Done when:` and State row was replaced with a short plain-word version. House words went with them, `division` to part, `store` to list, `render` to read or draw, `seed` to suggest, `mint` to build. Measured with `haipipe-writing`'s `cli/score.py`: 15 sentences flagged before, 12 after, every one that remains inside this Log, which is history and was not touched. No fact, id, `§` mark or section changed; only the words.
- ↩️ 260816 · [REVISE-CC] the `page-type: design` line deleted, reversing the ruling that kept it
      JL reversed an earlier ruling of his own: the head no longer declares a page type, so this page resolves as a plain Q decision page and its ✅ closes on its Aims.
      An independent reviewer showed the page cannot satisfy the for-design contract, which wants one Content part per candidate carrying the artifact and its reasons, Aims that are the brief's own criteria, and an Opening stating audience, goal, and constraints.
      This page has a Q-page Opening, Aims that are retirement chores, and four parts all describing the winner: it is a plugin description that happens to record a selection, so part 5 stays as ordinary Content, which a Q page may carry.
      Three factual repairs rode along.
      The acceptance State row names CC as the ruler under JL's 260815 delegation, because a ruling's author is its evidence while "nobody has argued with it since" is only the absence of objection.
      The for-slide State row now claims only what was seen, that no `haipipe-page-for-slide` is among the loaded skills, instead of naming the folder those skills load from, which implies a directory read this Log admits did not happen.
      The `SELECTION` figure dropped the three "why" clauses added last pass and keeps winner, loser, disposition, and downstream, because each clause could end in a period and the paragraph below already says all three.
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

- 260831 0113 · `## States` merged into `## Aims` (tick + `Now:` per Aim; asks and threads kept verbatim), skill 0.148.0