# QPf3-slide · outline v1
outline-version: v1
supersedes: —
date: 260817
approved: ⬜            🚧 a person ticks this. No machine may.

Generated 260817 from this page's own divisions, face-figure captions and
sentences, so no bullet claims anything the page does not already say.
UNAPPROVED, so it is a working document: rewrite it, delete what is wrong.

## C1 · One path per page, and no list to keep in step

### C1.P1 · if the file is there, the page has a deck
- B1 · A folded page (`<name>/<name>.md`) owns the `slide/` folder.
- B2 · The deck's file name is the page name plus `-deck.html`.
- B3 · Both doors below work this path out from the page they are on, so no list is kept and no list can go stale.
- B4 · When the file is not there, both views say so and offer the button.
- B5 · Nothing builds a deck behind your back.

## C2 · Two ways in, and neither can show you an old deck

### C2.P1 · the shell tab and the page panel, with one loader behind both
- B1 · Both doors send a HEAD request for that path, which is a small web question that asks only whether a file is there.
- B2 · They show the saved deck, or a pointer to the ✨ button when there is none.
- B3 · Every load skips the browser cache, so a freshly written deck appears on the next click.
- B4 · An old copy in the window can never outlive the file it came from.

## C3 · One click rewrites the deck, and always replaces it

### C3.P1 · the steps it runs, and the file it replaces
- B1 · Leave it empty and the deck presents the page's argument, or type an ask and the talk leans the way you asked.
- B2 · The server writes the `<head>` and its asset links itself, from real paths on disk.
- B3 · So the model starts writing at `<body>`, and a new deck can never miss its own stylesheets.
- B4 · The server also checks the result before it saves anything.
- B5 · It wants a whole document, at least three slides, and the asset links in place.
- B6 · If any of that is missing the new deck is refused, and the old file stays.
- B7 · A rebuild always overwrites, so a lasting fix belongs on the PAGE, and the page is what every rebuild reads.

## C4 · What you get: six to nine slides you can stand up and present

### C4.P1 · html-ppt supplies the shell, and the board supplies the words
- B1 · A deck is six to nine slides: a cover, a closing slide, and middle slides in between.
- B2 · The middles are built from the page's own emoji, numbers, and quoted rulings.
- B3 · The deck points at the html-ppt skill's files by relative path.
- B4 · So a better theme reaches every deck at once, with nothing to rebuild.
- B5 · Nothing from the skill is copied into the board, and the board adds no CSS of its own.

## C5 · Why Claude writes the deck, and what was dropped

### C5.P1 · three ways a page could have had a deck, and the one still standing
- B1 · This way won on evidence, not on argument.
- B2 · Six decks were written in the hour of the ruling, and the first live `/_board/autodeck` run produced a real talk for `QF2-newcomer`.
- B3 · The reflow copy lost because it copied instead of choosing, so one part of the page came back as its own paragraphs in a box.
- B4 · It was dropped whole, endpoint and route with it, and nothing in the board turns a page into slides that way now.
- B5 · The slide page-type lost because it asked for a second page to keep beside the page it was about.
- B6 · That second page held one part of the page per slide, each with a frame inside it.
- B7 · It was dropped, and its example is kept whole at `_archive/QBt9-for-slide.md`, where the reason it lost stays readable.

