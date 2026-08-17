# QPf11-pagex · outline v1
outline-version: v1
supersedes: —
date: 260817
approved: ⬜            🚧 a person ticks this. No machine may.

Generated 260817 from this page's own divisions, face-figure captions and
sentences, so no bullet claims anything the page does not already say.
UNAPPROVED, so it is a working document: rewrite it, delete what is wrong.

## C1 · What you keep, and what gets rebuilt

### C1.P1 · one file is yours, everything else is rebuilt from it
- B1 · The list lives at `<page>/pagex/<stem>.md`.
- B2 · It holds one line per borrowed file: where the file is, why you wanted it, and where it sits in your order.
- B3 · A line ending ` · removed` is one you dropped, and a rebuild never brings it back.
- B4 · The shortcuts are rebuilt, not written by you.
- B5 · A rebuild deletes only shortcuts it made itself, then makes them again from the list.
- B6 · Each source page gets its own folder, keeping the file's path inside that page, so you open `pagex/QPs1-overall/QPs1-overall.md` and read the real thing.
- B7 · If the original is renamed or filed away, the shortcut breaks where you can SEE it and the card says `⚠ dangling`.
- B8 · ⚠️ 1 more sentences in this division are not planned here yet

## C2 · Which files a line may point at

### C2.P1 · what a line may reach, and what a refusal has to show you
- B1 · A line may reach into another board, or another project, not just this board.
- B2 · Only the rebuild makes shortcuts, and it checks every target first.
- B3 · A target outside the repo is refused, and the reason shows on the card instead of failing quietly.
- B4 · Shortcuts are written as relative paths, so the repo still works after it is copied or moved.

## C3 · Why a borrowed page never becomes a second page

### C3.P1 · the rule that skips plugin folders, and the shape this never makes anyway
- B1 · The board finds its pages by walking the folders.
- B2 · `_in_plugin` in `src/common.py` tells it to stop as soon as it reaches `pagex`, and to skip everything under it.
- B3 · So a borrowed `Q*.md` never appears as a second, ghost page, and neither does the list file itself.
- B4 · The hardest case would be a shortcut to a whole page FOLDER.
- B5 · That shape is never made: this plugin borrows files only, and both the rebuild and the ＋ button refuse a folder.

## C4 · The list fills itself; you put it in order

### C4.P1 · the same rule the skill list already follows
- B1 · A page cannot lean on another page in secret.
- B2 · It says so in its own words, in the "Covered elsewhere" line and in every sentence that names another page.
- B3 · The borrow is therefore already written down, and asking someone to type it again is asking them to say the same thing twice.
- B4 · So there is no picker here: no page to choose from a dropdown, no file list to open, and no reason to type before anything is borrowed.
- B5 · What the machine must NOT decide is your order.
- B6 · A suggested line lands at the bottom, and everything above it is where you put it, the same rule `QPf10` follows for skills.
- B7 · The count in a line is the count on the day that line was added, and later rebuilds leave it alone.
- B8 · ⚠️ 2 more sentences in this division are not planned here yet

## C5 · What of a page you use, and what you do not

### C5.P1 · its whole folder, with the parts you use ticked
- B1 · A plain list says nothing about what it did NOT take.
- B2 · That silence is what trips a reader up: taking one file on purpose and never opening a page at all look exactly the same.
- B3 · So a plain list cannot answer the question a reader arrives with, which is which parts of that page this one is actually using.
- B4 · Each card therefore shows that page's whole folder with `using N of M` on top, and the parts you left carry ＋ use, which takes a folder in one click with nothing to type.

## C6 · Opening a borrow, and getting back

### C6.P1 · the borrowed page opens inside a frame with ← ☰ → on top
- B1 · A bare link leaves the reader standing inside a full board page with nothing to click to get back, which makes a borrow a one-way door.
- B2 · So the arrows walk your list in your own order, ☰ goes back to the cards, and the page inside the frame is exactly what the board built, never rewritten.

## C7 · The four borrows this page actually has

### C7.P1 · the lines the machine suggested, the order a person gave them, and the shortcuts built from both
- B1 · The list holds four lines and the folder holds four shortcuts, one folder per source page.
- B2 · One rebuild wrote all of them, with nothing typed by hand.
- B3 · The order is no longer the machine's: QPs1 was suggested first on 16 mentions and now sits second, because a person moved it there, and a rebuild never touches that.
- B4 · Every shortcut is relative, so a borrow still works after the repo is copied or moved.
- B5 · How far a shortcut climbs depends on where its source page sits: three `../` when that page shares this page's own group folder, which is the case for QPf10, QPf1 and QPf3, and four when it sits in another, which is the case for QPs1.
- B6 · Opening one proves the point: `pagex/QPs1-overall/QPs1-overall.md` shows QPs1's text as it is today, where a copy would show the day it was copied.
- B7 · Each shortcut keeps the file's path inside its source page, so two files taken from one page can never collide on the same name.
- B8 · ⚠️ 1 more sentences in this division are not planned here yet

## C8 · What the card and the folder row must admit

### C8.P1 · what a card must say about the page it borrowed from, and what the folder row must not hide
- B1 · The cards stand in your order, so the top card is the borrow you said matters most.
- B2 · Each card also shows how settled its source page is, so leaning on an argument that is still changing is a choice you can see rather than an accident.
- B3 · If the target is gone the card says `⚠ dangling` and gives the reason, and a refused line keeps its own reason too.
- B4 · Being able to see that is the whole reason a borrow is a shortcut and not a copy.
- B5 · The 📂 folder tab is owned by the folder view, but two of its rules come from here.
- B6 · This folder is never marked out of date, because a shortcut cannot fall behind the file it points at.
- B7 · And every shortcut row carries a 🔗 with its full target on hover, so a borrowed file is never counted as bytes this page owns.

