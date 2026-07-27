# Inline comments, and what happens after one exists

state: 🟡 PARTIAL
owner: JL
method: select → wrap that live Range → write back to md in one shot; then rule what the comment's remaining states are

## Question
How do you select a sentence on the page, attach a comment right there Google-Docs style, and what happens to that comment from then until it disappears?

The browser is on the user's laptop and the files are on the server, so a browser cannot write that disk: the write has to happen on the machine the files are on.
Comments that live only in a browser vanish on the next machine and never enter git, which is not "discussion on the board" but a private sticky note.
Building it is only half the problem, because a feature that writes comments answers none of "they pile up forever", "broken quotes that nobody repairs", or "can a board close with open comments".
With open comments sitting in `## Comments` and nothing saying what they mean, the close condition is hollow: a question can be marked ✅ carrying three of them.
So this page owns the whole span, from the selection that creates a comment to the rule that lets a board close in spite of one, and it defines the storage syntax inside `.md` that `QB1`'s SKILL.md needs in order to describe commenting at all.

## Boundary
- ✅ Covered here
  **Building it**: how the button appears on selection, the storage syntax in `.md`, how the disk write happens, how the quote is highlighted, how a failed anchor is flagged.
  **Its life after that**: which states a comment passes through, who pushes each one, who repairs a broken anchor, and what open comments mean for closing a question and closing a board.
- ↪ Covered elsewhere
  Attaching typed `>` lanes to a sentence rather than a comment to a selection: that is `QA8`.
  Whether the in-page chat and terminal actually see any of it: that is `QA8a`.
  Where the comment block sits on the page: that is `QA4`.

## Diagram

```
BUILDING ONE
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

The states it passes through afterwards, and who pushes each one:

```
  ① draft      in the browser, not yet on disk (localStorage)
       │  Save (written into md automatically)
       ▼
  ② open       in the md's ## Comments, `- [ ]`; header and index carry 💬 N
       │  mark solved (click on the page, or edit the md)   ┌── reopen ──┐
       ▼                                                    │            │
  ③ solved     `- [x]`, entry dims, highlight turns grey ───┘            │
       │                                                                 │
       │  ? keep forever, or move somewhere                              │
       ▼                                                                 │
  ④ archived   ← whether this state even exists is undecided             │
                                                                         │
  ⚠ lost       the original was edited, the quote no longer matches —────┘
               ② and ③ can both fall in; today it is only flagged, repair unbuilt
```

How a comment travels from "HTML in the browser" to "md on disk" to being read by an agent (the write→store→read round-trip):

```
  ① browser board.html         ② serve.py (the machine the files are on)   ③ agent
  ┌ select a line ┐  POST      ┌ writes into QX.md's ## Comments ┐   ┌ reads ## Comments ┐
  │ write comment │ /_board/…  │ one line: - [ ] WHO “quote” ·time│   │ this session: I   │
  │ hit Save      │ ─────────► │                                  │   │  read when told   │
  │               │ ◄───────── │ then build.py → board.html       │   │ drawer/terminal AI:│
  └────┬──────────┘ {ok,wrote} └──────────┬───────────────────────┘   │  told the COUNT,   │
       │                                  │ reload to see highlight    │  then must read    │
       │  ✗ server down →                 │                            └────────┬──────────┘
       │    falls back to localStorage    └── the md is the single truth; both readers read it ──┘
       │    → never hit disk, agents cannot see it
       └──────────────────────────────────────────────────────────────────────┘

  In one line: a comment "exists" only after ①→② (written into md); agents (③) read only
  the md, never the browser. If an agent cannot see it, it is stuck at ① — not on disk.
  What ③ receives at start is a COUNT, not the text; QA8a owns that gap.
```

/_excalidraw/?board=Tools/plugins/haipipe-toolkit/skills/diagrams/01-boardform-260722/fig/board.excalidraw&frame=QA6

## Items to Finish
- [x] 🖱 Select a sentence → write a comment → instant highlight + 💬 at the sentence end
- [x] ✍️ Anyone can sign with their own initials, not just the original defaults
- [x] ⚠️ When the sentence cannot be located, say so explicitly (⚠ not anchored in the panel), never silently vanish
- [x] 📄 Without JS, comments still display (you just cannot add one)
- [x] 💾 Save writes the disk directly, no extra button
      The browser sends one POST; `serve.py` edits the md **on the machine the files are on** and regenerates the html.
      (The first plan had the browser write the file itself; JL pointed out it cannot work; see Lesson.)
- [x] 🔁 Status can be changed on the page
      mark solved / reopen beside every comment, flipping `[ ]` ↔ `[x]` in the md directly.
- [x] 📌 Comments have their own place and status
      A dedicated `## Comments`, never mixed into `## Discussion`; `- [ ]` / `- [x]` is open / solved.
- [x] 🔍 A broken anchor must be discoverable
      When the quote no longer matches the body, the page flags it, no silent failure.
- [x] ✅ One real round-trip of the disk write, verified
      `curl` against `/_board/comment` and `/_board/resolve` both pass: md edited, html regenerated, out-of-bounds file names rejected.
      And every comment you left on the page these two days went down this exact path.
- [x] 🔀 Every state written down
      draft → open → solved (↔ reopen) → archived, plus ⚠ lost.
      Exactly the second figure above, per state: what it looks like in md, on the page, and who pushes it. ①②③ implemented; ④ archived and lost-repair still empty.
- [ ] 🗄 Solved comments get a destination
      Stay in `## Comments` forever, move into `## Log` after enough pile up, or get deleted.
      Today they pile up forever.
- [ ] 🔗 Broken anchors become repairable (one-click re-anchor = the confirmed goal, JL 260723 1518)
      At minimum, jump to that md line; the real bar: when a quote no longer matches, the page offers "the closest sentence in the body" and one click moves the anchor there.
      Not a nice-to-have; this IS the acceptance bar for this step.
- [ ] 🚦 Closing rules spelled out, two nested levels (JL 260723 1519)
      There are two "closes", nested: · closing one question: a single QX.md's `state:` marked ✅/done.
      Today only Items-to-Finish ticks are checked, comments are not. · closing the board: every question in the folder closed.
      Today there is no independent board state; you check question by question.
      Open comments should block BOTH levels: a question carrying `- [ ]` must not be marked ✅, a board holding any `- [ ]` must not count as closed.
      Today neither level checks comments.

## Where we are
**Building it is done and in real use: the comments on this very board came in through this machinery.**
The lifecycle is the unfinished half. Only ①②③ exist, and they emerged while building rather than being designed first; ④ archived and the ⚠ lost repair are both still empty, and neither closing level looks at comments at all.

- Select to comment
  Select a sentence in the body; "💬 Comment" pops up under the cursor.
  Click it: quote + input + signature, then Save.
- Instant reaction on save
  The sentence gets a yellow highlight and a 💬 at its end (hover to read, click to jump to the panel).
  The counter in the corner ticks +1 and a confirmation toast appears.
- Anyone can sign with their own initials
  The signature dropdown ends with "+ new person…": type two or three letters, hit enter, remembered from then on.
  The renderer accepts any uppercase initials and assigns each name a stable color.
- Comments land on disk immediately; what queues up is processing, not syncing
  Save sends one POST; `serve.py` edits the md on the server and re-runs build.py.
  So "an unsynced comment" does not exist; the md is always the freshest copy. localStorage keeps exactly two jobs: half-written drafts, and the fallback when `serve.py` is down; only then do the panel's Sync to md / Copy buttons carry the patch back by hand.
  What actually accumulates is the other side: you leave several comments, I take one pass: edit, reply `>> CC0723:` to each, mark them solved together.
- What it looks like in md, readable to the naked eye
  Written into the `## Comments` section (below `## Discussion`), one block per comment: `- [ ] JL “the selected sentence” · 260723 1100` plus a two-space-indented body.
  `[ ]` is open, `[x]` is solved, the same open / solved shown on the page.
- Solved and open are visually distinct
  Open: yellow highlight + orange edge + open.
  Solved: grey-green highlight + dimmed entry + solved.
  While a question still has open comments its header carries a `💬 N`.
- Who reads a comment, and when (JL asked 260723; corrected 260726)
  After the disk write there are two readers, both reading the same place, the md's `## Comments`: ① this CC session, where you say "read QA6" and I Read the file, scooping the new comments right then, a snapshot on demand with no automatic sensing; ② the AI attached to this question in the drawer or terminal.
  The second one used to be described here as having open comments "injected into its system prompt", and that is not what the code does: `prime_context` gives it the board, the page id and title, the file path, the first 280 characters of `## Question`, and a COUNT of unresolved boxes, then tells it to read the file.
  So neither reader is pushed the text; both must open the md, and the difference is only that the drawer AI is told at start that unresolved items exist.
  "The agent cannot see it" still happens only while a comment is browser-side in localStorage, not yet on disk, but "it was told" is weaker than this page claimed. `QA8a` owns that gap.
- They pile up forever
  Solved comments have no exit; `## Comments` only grows.
  This board is two days old and this page already holds 11.
- Why anchors kept "getting lost", three layers (JL asked 260723)
  ① Scan range too narrow: highlighting used to skip `## Diagram`, so selecting words inside the figure got wrongly flagged. → Fixed; figures are scanned too.
  ② Quotes crossing inline tags: a sentence containing `code`/**bold** cannot match tagged HTML as plain text. → Fixed: when exact match fails, fall back to "strip tags + normalize whitespace" containment; if present, it does not count as lost.
  ③ The real bulk: many `## Comments` entries quote **things said in chat** (not sentences from the body), so there is nothing on the page to anchor to.
  These are not "lost"; they were **never anchored**.
- "anchor lost" was the wrong thing to shout, renamed
  No history is kept → "you really edited that sentence" and "this sentence was never in the body" cannot be told apart.
  So no more red "⚠ anchor lost"; now a neutral grey "· unanchored" (hover text: the quote is not in the body, maybe chat, maybe a real edit).
  Result: red alarms 45 → 0, replaced by 26 neutral "unanchored".
- Nobody guards open comments (both closing levels leak)
  Closing a question checks only its Items-to-Finish ticks; closing a board checks only per-question states; neither level mentions comments.
  A Q can carry 3 open comments and still be marked ✅; a board can hold `- [ ]` and still pass as closed.

## Files
- `serve.py`
  `add_comment` / `resolve`: the disk write and the only state-transition entry point, both executed on the machine the files are on.
- `build.py`
  `parse_comments` / `render_comments` / `mark_span`: parsing, rendering, cross-tag highlighting. Open counts, default expansion, and the lost/unanchored verdict all live in the rendering pass.
- `ref/board-form.md`
  §6 the Comments section: full syntax.

## Lesson
**Ask "which machine does this code run on" before choosing an API.**
The first version had the browser write `.md` itself via the File System Access API, fine in isolation, but this setup is Remote-SSH: **the browser is on JL's laptop, the board files are on the server.** The folder picker can only see the laptop's disk and can never reach these files; the whole path was dead from the start.
JL punctured it with one line: "that grant I gave is on my local machine, but this thing is on the server."
Letting **the process already on the server, already serving this page** do the write was also less code.

**Locating text by searching inside a single text node, a guaranteed landmine.**
The first version ran `indexOf` with the selected text after saving, but the DOM splits a paragraph into several text nodes at inline tags (`code`, **bold**), so any selection crossing a tag matched nothing in every node: silent non-highlight.
No error, nothing on screen, hardest to debug.
The fix has two branches: while saving, the Range is still alive: wrap it directly, accurate across any tags; only after a reload (Range gone) fall back to search, now cross-node concatenation + whitespace-insensitive regex.

**A quote used as an anchor will break by nature.**
That is the built-in cost of a plain-text scheme, not a bug.
Edit the original sentence and the quote no longer matches; the comment drifts.
The only correct move is making "broken" visible instead of pretending it did not happen.

**A page can describe a mechanism more generously than the mechanism behaves.**
This page said the drawer AI had open comments "injected into its system prompt". It does not; it is handed a count and told to read the file.
Nobody noticed for three days because the sentence was plausible and nobody re-read `prime_context` against it.

## Glossary
Selection API: the browser's knowledge of "which words the user currently has selected", readable only from JavaScript.
File System Access API: the browser's ability to read/write local files directly. Available on `localhost` in Chrome/Edge; after one "allow" it can write `.md` back.
CriticMarkup: an annotation syntax living in plain text: `{==this==}` marks the original, `{>>comment<<}` the note. Its virtue: readable md.
anchor: how a comment finds the sentence it hangs on, by quoting it. Edit the sentence, break the anchor.
draft: a comment still in the browser, not yet written into `.md`, and invisible from any other machine.

## Discussion
> JL: I added a comment, but the commented text got no highlight and no feedback at all.
>> CC0723: root cause: a selection crossing inline tags can never be found by single-node indexOf. Changed to wrapping the live Range at save time, plus the 💬 marker and a toast. Verified end to end.
> JL: can commenters add a new user? Others want their own initials.
>> CC0723: done. The dropdown's last entry "+ new person…": type initials, hit enter, remembered on this machine; the renderer accepts any uppercase initials.
> JL: after I write a comment, what is its lifecycle? Open a dedicated question. QA6 is mostly done, can it be closed?
>> CC0726: that dedicated question was QA7, and JL merged it back here on 260726. Building a comment and ruling what becomes of it are one subject; splitting them left QA6 able to sit ✅ while the thing it built had no ending.

## Comments
- [x] JL “stepped on a real pit worth writing down:” · 260723 1217
      a new section could be added here, just call it lesson. It can be folded, don't put it in Now.
- [x] JL “queued up, in no hurry to sync” · 260723 1217
      what if comments could sync? which approach is better?
      >> CC0723: it already IS synced: since 1140 Save writes the disk directly; the md is always the freshest copy. That Now line described the old behavior; fixed.
      What "queues up" now is not comments but processing: you leave several, I take one pass: edit + reply to each + mark solved together.
- [x] JL “A quote used as an anchor will break by nature.” · 260723 1130
      a new section could be added here, just call it lesson. It can be folded, don't put it in Now.
      This pit is not actually solved yet.
      >> CC0723: added `## Lesson` (folded, above Glossary) and moved both lessons there; Now no longer holds them.
      "How to repair a broken anchor" is indeed unsolved; today it only gets flagged; repairing means editing the md by hand. Listed as an unticked line in Done when.
- [x] JL “How do you select a sentence on the page and attach a comment right there, Google-Docs style?” · 260723 0900
      exactly this, being able to add first, syncing together later.
      >> CC0723: adding works now, save = instant highlight; syncing goes through Sync to md.
- [x] JL “the panel's three buttons: Sync to md (pick the folder once, writes straight into each Q's `## Discussion`)” · 260723 1100
      comments must not mix into Discussion; open a separate `## Comments` below it; and every comment needs a status, solved or not.
      >> CC0723: done. A `## Comments` section + `- [ ]` / `- [x]` as status, shown as open / solved on the page; open ones put a 💬 N on the question header.
- [x] JL “closing the board” · 260723 1519   (from QA7)
      do you mean board or question?
      >> CC0723: both, and they nest. Rewrote the Done-when line and the Now line in two-level form:
      · closing a question = a single QX.md's `state:` → ✅; · closing a board = every question closed.
      Open comments should block both levels; today neither level looks at comments, so a question carrying 3 `- [ ]` can be marked ✅
      and a board holding `- [ ]` can pass as closed. That is the answer to "which one closes": both levels must guard.
- [x] JL “‘the closest sentence in the body’ with one-click re-anchoring.” · 260723 1518   (from QA7)
      yes, this is exactly what I want.
      >> CC0723: noted, promoted from "nice-to-have" to the formal acceptance bar. The Done-when line "broken anchors become repairable" now reads:
      when a quote no longer matches, the page offers the closest sentence in the body and one click moves the anchor; that is the bar for done.
      (Implementation not started; the requirement is pinned first.)
- [x] JL “stay in ## Comments forever, move into ## Log after enough pile up, or get deleted. Today they pile up forever” · 260723 1518   (from QA7)
      solved comments could be collapsed.
      >> CC0723: done. Solved comments (`[x]`) fold their body into a one-line `▸ reply`; the surface keeps only the header
      (who · quote · time · solved); click reply to expand. Open ones stay expanded.
      This is v1 of "a destination for solved comments": not deleted, not moved, just tucked in. The move-to-## Log idea is parked.
- [x] JL “when a quote no longer matches the page flags ⚠ anchor lost, but repairing means editing the md yourself.” · 260723 1517   (from QA7)
      why anchor is so easier to be lost?
      >> CC0723: your sentences never actually got lost; detection had two bugs, both fixed:
      ① scan range too narrow: highlighting covered Question/Now/Done/Why but skipped `## Diagram`.
      Your “Save (written into md automatically)” lives inside the figure → wrongly flagged. Figures are scanned now; it highlights.
      ② more fundamental: quotes were matched as plain text against **tagged HTML** by exact substring.
      A selected sentence often contains inline markup (`code`→`<code>`, **bold**→`<b>`); once the quote crosses such a tag,
      `e in html` fails: the words are visibly on the page yet reported lost. Your 1517 comment quoted the backticked `⚠ anchor lost` itself, a direct hit.
      Fix: when exact match fails, fall back to "strip tags + normalize whitespace" containment; present = not lost (just not highlighted).
      Result: QA7 went from "⚠ 1 anchor lost" to 0.
      ⚠️ Genuine loss still exists: when you **really edit the original sentence**, the quote truly mismatches; that is the case worth repairing (see the 1518 one-click re-anchor).
- [x] JL “Save (written into md automatically)” · 260723 1511   (from QA7)
      the question now is: how do I let the agent read my comments?
      >> CC0723: exactly like this: I am reading this one right now; it is already in this question's ## Comments.
      The chain: Save → serve.py writes into the md's ## Comments → the agent reads that section. Two prerequisites, both required:
      ① the server is running at save time (the disk-write step; otherwise the comment is stuck in browser localStorage);
      ② the agent actually reads the file, nothing is sensed automatically: you say "read it", or the drawer AI is primed at start.
      So "cannot read it" only happens when ① is unmet (not yet on disk). This chain is precisely the "who reads" step the lifecycle diagram had missed.
      >> CC0726: prerequisite ② is right and the wording around it was too generous: "primed at start" means told a count and told to read, not given the text. `QA8a` opened to rule what the chat is actually handed.
- [x] JL “① draft, in the browser, not yet on disk (localStorage)” · 260723 1200   (from QA7)
      that grant I gave is on my local machine, but this thing is on the server, that can't work, right?
      >> CC0723: you are right, the whole path is dead. Switched to server-side writes: the browser sends one POST,
      serve.py edits the md on this machine and regenerates the html. Verified.

## Log
260726 · QA7 merged in (JL: "could we merge QA6 and QA7 to be one QA6"). Building a comment and ruling its remaining life are one subject, and the split let this page sit ✅ while the thing it built had no ending. State drops ✅ → 🟡 because QA7's three open items came with it; owner CC → JL because all three are rulings. Every QA7 comment is kept and marked `(from QA7)`, both Discussion threads survive, and the item list gained the emoji icons the current form asks for without a word of its text changing. The claim that open comments are "injected into the system prompt" was corrected against `prime_context`, which passes a count; `QA8a` opened for that gap
260724 1242 · Translated to English (JL 260724: everything on the board in English)
260723 · Rewritten to the new structure: Question expanded into "one paragraph + bullets", added `## Boundary` and `## Files`; the retired `## Why here` merged into Question
260723 1735 · (QA7) Closed two open comments: ① JL 1519 "board or question" → Done-when and Now rewritten in two-level form; ② JL 1518 "one-click re-anchor is exactly what I want" → promoted from nice-to-have to the formal acceptance bar
260723 1530 · (QA7) JL asked "why don't comments stick to the text anymore" + "solved ones should collapse" → two build.py changes: ① highlighting now uses mark_span, spanning <code>/<b>; ② solved comments fold into ▸ reply, header-only on the surface
260723 1525 · (QA7) JL asked "does the Q explain the html→disk→agent chain" → added the write→store→read round-trip figure: browser Save → serve.py writes the md's ## Comments → agents read only the md
260723 1520 · (QA7) Answered "why do anchors keep getting lost": three layers; scan-range and cross-tag bugs fixed; "anchor lost" renamed to neutral "unanchored", red alarms 45→0
260723 1515 · (QA7) JL asked "how do agents read my comments" → two readers named (this session / the drawer AI), prerequisites ① server running at save ② the agent actually reads
260723 1710 · (QA7) Ticked during the board-wide review: the state machine is written down → 🟡 PARTIAL; the archived exit + anchor repair still empty
260723 1230 · Closing pass: state → ✅ DONE; Now now opens with "in real use";
              the disk-write line in Done when gains "every comment took this real round-trip"; Comments all settled
260723 1226 · Now's "queued up, in no hurry to sync" rewritten as "save lands on disk; what queues is processing, not syncing";
              the old text predated the 1140 server-side write; the 1217 sync question closed along the way
260723 1205 · Switched to server-side writes (two POST endpoints in `serve.py`), verified;
              the browser-writes-files scheme demoted to fallback, used only without serve.py
260723 1200 · JL pointed out File System Access cannot work over Remote-SSH: browser local, files on the server
260723 1150 · (QA7) JL raised "a comment's lifecycle", question opened; "how to repair a broken anchor" moved over from QA6
260723 1140 · Comments write the disk on save: folder handle kept in IndexedDB, authorize once, no more Sync clicks
260723 1140 · mark solved / reopen beside every comment, flipping [ ] / [x] in the md
260723 1130 · JL ruled: a folded `## Lesson`, lessons never in Now; "repairing a broken anchor" listed as unfinished
260723 1110 · Anchor check added on the md side: mismatches get flagged (caught 1 on this board on the spot)
260723 1105 · Implemented: `- [ ] WHO “quote” · time` + indented body; [x] = solved,
              solved highlights turn grey, entries dim; question header shows the open count
260723 1100 · JL ruled: comments go into their own `## Comments` (below Discussion), each with a solved status
260723 1010 · Now switched to item form per JL (short heading + explanation below)
260723 1005 · JL sent the first real comment back via Copy, proving the browser → me path works
260723 0942 · All interface copy switched to English
260723 0940 · End-to-end verified: a script simulates selecting text crossing a <code> tag → save →
              mark.pend = 1, badge = 1, dock = 1 pending
260723 0938 · Fix: new comments wrap the still-alive Range at save time (accurate across tags);
              only post-reload falls back to search: cross-node concatenation + whitespace-insensitive regex
260723 0936 · Still no highlight. Root cause found: the old version ran indexOf with the selected text,
              searching a single text node, any selection crossing an inline tag (`code`, **bold**) must fail
260723 0930 · JL wants anyone to sign with their own initials → customizable, remembered;
              renderer widened from its original fixed names to any uppercase initials, with stable per-name colors
260723 0925 · JL: "no highlight, no feedback" → added save-time highlight, 💬 marker, toast, pending counter
260723 0915 · v1 built: select → popup → localStorage → Sync to md writes into ## Discussion
260723 0900 · JL asked for Google-Docs-style inline comments, question opened
