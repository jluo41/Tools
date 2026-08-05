haipipe-board-page-for-slide · Changelog
=========================================

Skill-scoped changelog (never loaded at invocation; read on demand). Versions match
SKILL.md frontmatter `version:`. Newest first.

**v0-series rule:** inherited from `haipipe-board`; this skill stays on `0.x.x` and
never reaches `1.0.0` without JL's explicit say-so.

## 0.4.0 - 2026-08-05

**Re-ruled A, the same day, after seeing B rendered** (JL: "So it is not like
I can do the iteration. What about the old method of A? will that be easier.").

- Beat-grain acceptance blocked slide-by-slide review: one tick covered the
  set, so a reviewer could not accept slide 5 while sending slide 6 back.
- The default is now A inside B's divisions: division = talk beat, one embed
  and one accept row PER SLIDE. A rebuilt slide resets only its own row.
- `?preview=A-B` (0.3.0's strip) stays built and legal as a COMPACT form for
  a beat that is already settled, with its costs stated: set-grain reset and
  a first-slide-only scripts-off fallback.
- The deck's :target fallback CSS is scoped to `html:not([data-preview])`:
  unscoped it fought the runtime and hid every non-target slide of a strip,
  which is what "I don't think it is very good" looked like.

## 0.3.0 - 2026-08-05

**Ruled B on QA4** (JL: "Do this one.", against CC's recommended multi-embed):
division = talk BEAT, one range embed per beat.

- `?preview=A-B` renders slides A..B as a vertical strip: new range mode in
  html-ppt's `assets/runtime.js` (backward compatible; single previews and the
  presenter untouched). The board renderer (`haipipe-board` `src/body.py`)
  reads the range and sizes the frame to `aspect-ratio:16/(9×count)`.
- The slide binding moves to beat grain: the row names its range, one tick
  accepts the set, and a rebuild of any slide in the range resets the row.
  The acceptance blur was stated on the option and accepted with it.
- The scripts-off fallback shows a range's FIRST slide (`#sA`); CSS cannot
  express an interval endpoint from one fragment, and the limit is stated.
- QA4 regrouped from 7 one-slide divisions into 4 beats as the proving shape
  (three ranges, one single).

## 0.2.1 - 2026-08-05

Review fixes, no rule change:

- The REQUIRED `page-type: slide` frontmatter key is stated: a deck can sit on
  any filename, QA4 wears a Q filename, and the key beats the filename (base
  type resolution ③).
- Plain English: the 0.1.0 correction is "recorded so the mistake stays on the
  page", not "recorded so it stays wrong".

## 0.2.0 - 2026-08-05

**Corrected by its first real page, the same day.** JL rejected the PNG design
("what I am thinking is that you will embed the html in the content division")
and asked for the proof: QA4 on the boardform board, seven divisions, each
embedding the one deck file with `?preview=N`, verified live in a real browser.

- The render half is now the LIVE embed `![slide N](deck.html?preview=N)`:
  html-ppt's own locked single-slide mode, one file for both surfaces, zero
  drift. The PNG export is demoted to non-iframe surfaces (paper figures,
  offline export).
- The 0.1.0 premise "build.py strips JS" was false and is retired with the
  reason recorded in the contract: the build only asserts pages stay readable
  with scripts off, and it never rewrites an iframe's file at all.
- The embed carries both selectors, `?preview=N#sN`: the query drives the
  runtime, the fragment drives a scripts-off CSS `:target` fallback the deck
  carries in one style block, so the slide still shows where a webview blocks
  JS. Verified in a real Chrome with script execution disabled.
- Engine work the correction rode on (in `haipipe-board`): `![alt](x.html)`
  renders as a live iframe with a no-JS open link (`src/body.py`), the
  split-site reroot distinguishes authored html from generated page links by
  existence in the source tree (`src/page_board.py`), and the checker accepts
  a media embed as a division's figure (`cli/check.py`).

## 0.1.0 - 2026-08-05

**Created on JL's branch ruling** (the Page-for-Slide branch: "please go ahead and
focusing on the slide"). Division = slide; the slide binding is the typed record.

- The one constraint stated on day one: build.py strips JS, so a division embeds
  the PNG export and NEVER the live html-ppt deck; the deck stays a linked
  artifact with its runtime intact. Grounded in html-ppt's own headless Chrome
  PNG export script.
- Shares for-display's acceptance model (a person accepts a render; a rebuild
  resets the row) and for-value's number rule (no untraceable number, even on a
  temporary slide).
