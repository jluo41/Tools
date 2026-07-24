# Inline comments on selected text
state: ✅ SETTLED
owner: CC
method: select → wrap that live Range → stash in localStorage → write back to md in one shot
## Question
How do you select a sentence on the page and attach a comment right there, Google-Docs style? And the comment must live in both `.md` and `board.html` — not only in someone's browser.

- Why it is hard
  The browser is on the user's laptop and the files are on the server (Remote-SSH). A browser cannot write that disk — the write has to happen on the machine the files are on.
- What breaks if we leave it
  Comments that live only in a browser vanish on the next machine and never enter git — that is not "discussion on the board", it is a private sticky note.
- What it affects downstream
  It defines the **storage syntax inside `.md`**. Without that syntax, `QB1`'s SKILL.md cannot describe "how to comment on a board".

## Boundary
- ✅ Covered here
  **Building it**: how the button appears on selection, the storage syntax in `.md`, how the disk write happens, how the quote is highlighted in the body, how a failed anchor is flagged.
- ↪ Covered elsewhere
  What happens to a comment **after it exists** — how long it lives, who pushes it, whether unresolved ones block closing — that is `QA7`.

## Diagram
```
       select a sentence on board.html
                │   selection needs JS — there is no other way to know which words were selected
                ▼
          a small box pops up, write the comment
                │
                ▼
        produce an md patch (the human-readable kind):
          …before {==the selected sentence==}{>>JL: unclear here<<} after…
                │
      ┌─────────┴──────────────────────────┐
      A write straight back to .md          B copy to clipboard
        File System Access API                paste it back yourself
        works on localhost + Chrome/Edge      works anywhere, two extra steps
      └─────────┬──────────────────────────┘
                ▼
        re-run build.py → the sentence highlights, the comment hangs beside it

  reading comments: no JS needed      adding one: JS required   ← progressive enhancement
```

## Items to Finish
- [x] Select a sentence → write a comment → instant highlight + 💬 at the sentence end
- [x] Anyone can sign with their own initials, not just JL / RA / CC
- [x] When the sentence cannot be located, say so explicitly (⚠ not anchored in the panel) — never silently vanish
- [x] Without JS, comments still display (you just cannot add one)
- [x] Save writes the disk directly, no extra button
      The browser sends one POST; `serve.py` edits the md **on the machine the files are on** and regenerates the html.
      (The first plan had the browser write the file itself; JL pointed out it cannot work — see Lesson.)
- [x] Status can be changed on the page
      mark solved / reopen beside every comment, flipping `[ ]` ↔ `[x]` in the md directly.
- [x] Comments have their own place and status
      A dedicated `## Comments`, never mixed into `## Discussion`; `- [ ]` / `- [x]` is open / solved.
- [x] A broken anchor must be discoverable
      When the quote no longer matches the body, the page flags it — no silent failure.
- [x] One real round-trip of the disk write, verified
      `curl` against `/_board/comment` and `/_board/resolve` both pass: md edited, html regenerated,
      out-of-bounds file names rejected. And every comment you left on the page these two days went down this exact path.
      ("How to REPAIR a broken anchor" is no longer this question — it moved to QA7.)

## Where we are
**Done, and in real use: the comments on this very board came in through this machinery.**

- Select to comment
  Select a sentence in the body; "💬 Comment" pops up under the cursor.
  Click it: quote + input + signature, then Save.
- Instant reaction on save
  The sentence gets a yellow highlight and a 💬 at its end (hover to read, click to jump to the panel).
  The counter in the corner ticks +1 and a confirmation toast appears.
- Anyone can sign with their own initials
  The signature dropdown ends with "+ new person…" — type two or three letters, hit enter, remembered from then on.
  The renderer accepts any uppercase initials and assigns each name a stable color.
- Comments land on disk immediately; what queues up is processing, not syncing
  Save sends one POST; `serve.py` edits the md on the server and re-runs build.py.
  So "an unsynced comment" does not exist — the md is always the freshest copy.
  localStorage keeps exactly two jobs: half-written drafts, and the fallback when `serve.py` is down —
  only then do the panel's Sync to md / Copy buttons carry the patch back by hand.
  What actually accumulates is the other side: you leave several comments, I take one pass — edit, reply `>> CC0723:` to each, mark them solved together.
- What it looks like in md — readable to the naked eye
  Written into the `## Comments` section (below `## Discussion`), one block per comment:
  `- [ ] JL “the selected sentence” · 260723 1100` plus a two-space-indented body.
  `[ ]` is open, `[x]` is solved — the same open / solved shown on the page.
- Solved and open are visually distinct
  Open: yellow highlight + orange edge + open. Solved: grey-green highlight + dimmed entry + solved.
  While a question still has open comments its header carries a `💬 N`.
- A broken anchor never fails silently
  When the quote cannot be found in the body, the comment is flagged, and the fold header says how many are affected.


## Files
- `serve.py`
  `add_comment` / `resolve` — the disk write lives in these two (executed on the machine the files are on).
- `build.py`
  `parse_comments` / `render_comments` / `mark_span` — parsing, rendering, cross-tag highlighting.
- `ref/board-form.md`
  §6 the Comments section: full syntax.

## Lesson
**Ask "which machine does this code run on" before choosing an API.**
The first version had the browser write `.md` itself via the File System Access API — fine in isolation,
but this setup is Remote-SSH: **the browser is on JL's laptop, the board files are on the server.**
The folder picker can only see the laptop's disk and can never reach these files — the whole path was dead from the start.
JL punctured it with one line: "that grant I gave is on my local machine, but this thing is on the server."
Letting **the process already on the server, already serving this page** do the write was also less code.

**Locating text by searching inside a single text node — a guaranteed landmine.**
The first version ran `indexOf` with the selected text after saving, but the DOM splits a paragraph into several text nodes at inline tags (`code`, **bold**),
so any selection crossing a tag matched nothing in every node — silent non-highlight. No error, nothing on screen, hardest to debug.
The fix has two branches: while saving, the Range is still alive — wrap it directly, accurate across any tags;
only after a reload (Range gone) fall back to search, now cross-node concatenation + whitespace-insensitive regex.

**A quote used as an anchor will break by nature.**
That is the built-in cost of a plain-text scheme, not a bug. Edit the original sentence and the quote no longer matches; the comment drifts.
The only correct move is making "broken" visible instead of pretending it did not happen.

## Glossary
Selection API: the browser's knowledge of "which words the user currently has selected" — readable only from JavaScript.
File System Access API: the browser's ability to read/write local files directly. Available on `localhost` in Chrome/Edge; after one "allow" it can write `.md` back.
CriticMarkup: an annotation syntax living in plain text — `{==this==}` marks the original, `{>>comment<<}` the note. Its virtue: readable md.
anchor: how a comment finds the sentence it hangs on.

## Discussion
> JL: I added a comment, but the commented text got no highlight and no feedback at all.
>> CC0723: root cause — a selection crossing inline tags can never be found by single-node indexOf. Changed to wrapping the live Range at save time, plus the 💬 marker and a toast. Verified end to end.
> JL: can commenters add a new user? Others want their own initials.
>> CC0723: done. The dropdown's last entry "+ new person…" — type initials, hit enter, remembered on this machine; the renderer accepts any uppercase initials.

## Comments
- [x] JL “stepped on a real pit worth writing down:” · 260723 1217
      a new section could be added here, just call it lesson. It can be folded, don't put it in Now.
- [x] JL “queued up, in no hurry to sync” · 260723 1217
      what if comments could sync? which approach is better?
      >> CC0723: it already IS synced — since 1140 Save writes the disk directly; the md is always the freshest copy. That Now line described the old behavior; fixed.
      What "queues up" now is not comments but processing: you leave several, I take one pass — edit + reply to each + mark solved together.
- [x] JL “A quote used as an anchor will break by nature.” · 260723 1130
      a new section could be added here, just call it lesson. It can be folded, don't put it in Now.
      This pit is not actually solved yet.
      >> CC0723: added `## Lesson` (folded, above Glossary) and moved both lessons there; Now no longer holds them.
      "How to repair a broken anchor" is indeed unsolved — today it only gets flagged; repairing means editing the md by hand. Listed as an unticked line in Done when.
- [x] JL “How do you select a sentence on the page and attach a comment right there, Google-Docs style?” · 260723 0900
      exactly this — being able to add first, syncing together later.
      >> CC0723: adding works now, save = instant highlight; syncing goes through Sync to md.
- [x] JL “the panel's three buttons: Sync to md (pick the folder once, writes straight into each Q's `## Discussion`)” · 260723 1100
      comments must not mix into Discussion — open a separate `## Comments` below it; and every comment needs a status, solved or not.
      >> CC0723: done. A `## Comments` section + `- [ ]` / `- [x]` as status, shown as open / solved on the page; open ones put a 💬 N on the question header.

## Log
260724 1242 · Translated to English (JL 260724: everything on the board in English)
260723 · Rewritten to the new structure: Question expanded into "one paragraph + bullets", added `## Boundary` and `## Files`; the retired `## Why here` merged into Question
260723 1230 · Closing pass: state → ✅ DONE; Now now opens with "in real use";
              the disk-write line in Done when gains "every comment took this real round-trip"; Comments all settled
260723 1226 · Now's "queued up, in no hurry to sync" rewritten as "save lands on disk; what queues is processing, not syncing" —
              the old text predated the 1140 server-side write; the 1217 sync question closed along the way
260723 1205 · Switched to server-side writes (two POST endpoints in `serve.py`), verified;
              the browser-writes-files scheme demoted to fallback, used only without serve.py
260723 1200 · JL pointed out File System Access cannot work over Remote-SSH — browser local, files on the server
260723 1150 · "How to repair a broken anchor" handed to QA7 (comment lifecycle); this question keeps only "one human-verified disk write"
260723 1140 · Comments write the disk on save: folder handle kept in IndexedDB, authorize once, no more Sync clicks
260723 1140 · mark solved / reopen beside every comment, flipping [ ] / [x] in the md
260723 1130 · JL ruled: a folded `## Lesson` — lessons never in Now; "repairing a broken anchor" listed as unfinished
260723 1110 · Anchor check added on the md side: mismatches get flagged (caught 1 on this board on the spot)
260723 1105 · Implemented: `- [ ] WHO “quote” · time` + indented body; [x] = solved,
              solved highlights turn grey, entries dim; question header shows the open count
260723 1100 · JL ruled: comments go into their own `## Comments` (below Discussion), each with a solved status
260723 1010 · Now switched to item form per JL (short heading + explanation below)
260723 1005 · JL sent the first real comment back via Copy — proving the browser → me path works
260723 0942 · All interface copy switched to English
260723 0940 · End-to-end verified: a script simulates selecting text crossing a <code> tag → save →
              mark.pend = 1, badge = 1, dock = 1 pending
260723 0938 · Fix: new comments wrap the still-alive Range at save time (accurate across tags);
              only post-reload falls back to search — cross-node concatenation + whitespace-insensitive regex
260723 0936 · Still no highlight. Root cause found: the old version ran indexOf with the selected text,
              searching a single text node — any selection crossing an inline tag (`code`, **bold**) must fail
260723 0930 · JL wants anyone to sign with their own initials → customizable, remembered;
              renderer widened from JL/RA/CC to any uppercase initials, stable per-name colors
260723 0925 · JL: "no highlight, no feedback" → added save-time highlight, 💬 marker, toast, pending counter
260723 0915 · v1 built: select → popup → localStorage → Sync to md writes into ## Discussion
260723 0900 · JL asked for Google-Docs-style inline comments — question opened
