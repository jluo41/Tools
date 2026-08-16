# The evidence card: click a sentence, see its apparatus
state: 🟡 PARTIAL
owner: JL
method: fold typed `>` lanes and threads under the sentence they follow; resolve inline-marker chips through the paper dialect

## Opening
How can a sentence keep its evidence close without letting that evidence overwhelm the prose?

This page defines an evidence card that folds citations, values, displays, and review threads under the sentence they support.
The hard part is that those records have different forms but must share one visible attachment rule.
Rendering them as loose paragraphs makes the sentence unreadable and leaves its evidence easy to misplace.
The design succeeds when the sentence stays clean and one click reveals every adjacent record tied to the same source line.

**Covered elsewhere**: `QC0@paper` through `QC4@paper` rule the paper marker meanings, `QAa0` owns page order, `QB5b` owns comment pinning, `QB5` is the family's front door, `QB5c` owns editing the sentence itself, and `QB5d` owns what an agent is handed.


## Diagram

/_excalidraw/?board=Tools/plugins/haipipe-toolkit/skills/diagrams/BoardSkillBoard-260722/board.excalidraw&frame=QAb1

## Content
### Lane grammar
A `>` line directly under a sentence (blank lines tolerated between them) attaches to that sentence.
Typed lanes name the attachment: `> Citation:` 📚 · `> Value:` 🔢 · `> Display:` 🖼 · `> Check:` ⚠️ · `> Q-consumer:` 🔎 · `> Link:` 🔗 · `> Source:` 📄 · `> Note:` 📝.
A person's comment is `> Comment JL …`, with the colon after the name optional (JL 260802): beside the typed lanes, a bare pair of initials said nothing about what the row was.
The legacy `> JL: …` still renders so nothing already written breaks, and `check.py` warns on it inside Content.
`## Discussion` is untouched and keeps `> JL:` with `>> CC{MMDD}:` replies, because that is a thread rather than a note on one sentence.
An edit is `> ✎ ~old~ *new* · WHO · YYMMDD HHMM`, and the badge names which kind is underneath: `⚑` a typed lane, `💬` a person waiting, `✎` an edit, with a person waiting outranking a record.
For sentence-revision `> Note:` lanes, write deletions as `~~removed~~` and additions as `**inserted**`; the Board renders them as a deletion line and bold text rather than showing the delimiters.
`> JL:` / `> CC:` review threads join the same drawer with their normal comment styling.
A `>` run with no sentence above it (a thread that opens a section) renders exactly as before, and the supporting folds (Discussion, Law, Lesson, Glossary, Log, Why here) never fold apparatus.

### Click to add: the sentence as a write target
Reading is half the loop; JL also wants to click a sentence and attach anything to it (260725).
When `serve.py` runs, two entry points exist: DOUBLE-click any bare sentence to open the lane + text form beneath it (single click stays free for reading and selection, JL 260725), or use the "➕ add to this sentence" row that ends every open drawer.
Save posts `POST /_board/sentence {path, file, sentence, lane, text}`; `serve.py` finds that exact sentence line in the markdown, inserts the `> Lane: text` line after the sentence's existing apparatus, and rebuilds.
Copy is section-level (JL 260725: not per-sentence): every section heading carries a ⧉ button that copies the whole section as clean plain text, folded drawers and item explanations included, with no badges, forms, or highlight formatting (script-only enhancements; without scripts the page still reads, and writing already requires the server).
The anchor rule is the comment layer's: the sentence text must match exactly; a miss fails visibly, never silently.
This does not replace selection comments (`QA6`): select any span for a pinned `## Comments` entry; the ➕ row is for apparatus that should live in the prose, next to its sentence.

### Why adjacency, not new syntax
The paper unit docs already write review threads and CHECK blocks under the sentence they discuss, so existing files gain the behavior with zero edits once their board rebuilds.
The typed lanes are JL's extension of that same convention, proposed in the MISQ-Paper-Board session on 260725: `> Citation`, `> Value`, `> Display` lanes map one-to-one onto the paper placeholders `\cite{TOADD}`, `{VAL:? …}`, and DR display ids, which is the alignment path to `/haipipe-paper`.

## Aims
### The renderer and write mechanism
- [x] ⚑ Adjacency fold shipped
      A plain sentence followed by `>` lines renders as a native `<details>`: the sentence plus a ⚑N badge on stage, the apparatus in a drawer beneath.
      Implemented in `src/body.py` (`render_apparatus` + the `last_p` attachment walk); the zero-script invariant holds because the fold is native HTML.
- [x] 🖱 Hover tint shipped
      The sentence under the cursor tints slightly (accent at 8%), so you can see which sentence a click or a selection will target.
      Pure CSS, both themes, shipped 260725 on JL's ask.
- [x] ➕ Click-to-add writes into the markdown
      Shipped 260725: `POST /_board/sentence` in `serve.py` finds the exact sentence line (markdown-stripped match), appends `> Lane: text` at the end of its apparatus run, and rebuilds; a miss returns a visible error and writes nothing.
      On the page, double-clicking ANY sentence opens the lane + text form, and every open drawer also ends with an "➕ add to this sentence" row.
      Amended 260727: this used to read "a bare sentence", and the drawer's row was the only path for a sentence that already had apparatus. That row is reachable only once the drawer is OPEN, so on an evidenced sentence the gesture people had learned did nothing, silently. Both shapes now answer double-click. WHERE the form goes still differs: `mk` inserts `afterend`, so a drawer must insert at the end of its BODY, because inserting after the summary's own `p` puts the form inside `<summary>`, where every click toggles the drawer.
      Smoke-tested over HTTP: the Note line in QA4's second demo drawer was added through the endpoint.
- [x] 🎨 Inline-marker chips
      Shipped 260726 and live on two boards. `\citep{}` / `\cite{TOADD}` / `{VAL:? …}` / `[Q-X-n]` / `displayNN` / `\ref{tab:|fig:}` render as status chips resolved at build time against the paper's `.bib`, `1-probes/` and `displays/`, and each opens a native `popover` panel carrying the reference as the paper's own `.bst` sets it, the rows of a table, or both pictures of a figure.
      The four rulings that blocked it are made: `QC1@paper` citation, `QC2@paper` value, `QC3@paper` table, `QC4@paper` figure, over `QC0@paper` which owns the sentence unit. Measured on the MISQ board: 258 chips.
      The mechanism half lives here, and it stayed script-free: `popovertarget` alone opens the panel, inside a sentence's `<summary>` or out of it, verified in Chrome 150.
      ⚠️ The lesson belongs here because it is a mechanism defect rather than a paper-content defect.
      A panel's class list is `chipcard <kind> <state>`, so a bare `.fig{}` rule written for markdown images also matched every figure panel.
      Its `display:block` beat the browser rule that hides a closed popover, and five invisible full-width panels swallowed every click.
      `QA9`'s `check.py` now fails on a bare class selector that collides with a panel token.

### The lab demonstration and JL's gate
- [x] 🎬 Self-demonstrating example on the page-grammar face
      A "Sentence apparatus" subsection written in the grammar it documents lives with the Content grammar (on `QAa3` since 260729; it was QA4 §3 when built), so the lab board demonstrates the interaction on itself.
- [ ] 🧠 JL accepts the interaction on the lab board
      Eyeball the demo on `QAa3`: the badge shape, the drawer depth, which lanes exist, and whether attachment across blank lines feels right.
      This visual gate is still required before the interaction is settled, although a separate JL request already authorized the MISQ rollout.

### The MISQ rollout
- [x] 📄 Rolled to the MISQ paper board
      Done 260725 by the MISQ-Paper-Board session, on JL's ask there ("how do you make it to be like each sentence to have the same line").
      Every `> CHECK:` prose block on that board was rewritten into typed lanes: 3 `> Citation:` (the owed HUMAN-ONLY keys, each carrying reference, doi, `.bib` hit count, the owed `[Q-Seed-n]` bracket, and its probe source), 2 `> Display:` (DR08 stale, DR10 not built), and 15 `> Check:`.
      The board renders 20 lanes and 52 sentence drawers, and 46 `> JL:` lines came through byte-identical.
      Two lessons the rollout produced, both worth keeping in the grammar.
      First, adjacency is a real binding: a lane that used to sit after a paragraph while its prose said "the sentence above" silently attached to the wrong sentence, and had to be moved under its own.
      Second, a page-level concern (an em-dash sweep, a missing `checks.sh`) has no sentence to attach to and false-attaches to whatever precedes it; those belong in Items to Finish, or under a `###` heading where a `>` run renders as a plain thread.
- [x] 🧹 Content law applied to the first real page
      JL ruled that an S page's Content holds the stage's real product only (260725).
      All ten affected pages were swept: nine venue contracts moved into `## Stage Contract` and five settled-flags blocks into `## Where we are`, every line verbatim under a guard that aborts the page if a single moved line would be lost.
      Content is now the section itself, and each heading names it (`📚 Content · Main 7 Results`, `📚 Content · Main 9 Conclusion`).
      `stage.py sync --all` then ran and left every authored venue contract untouched, which proves an authored subsection under `## Stage Contract` survives sync.

## States
Sentence adjacency, typed lanes, click-to-add, copy controls, and inline-marker chips are implemented and live on the lab and MISQ Boards.
The only open gate is JL's visual and interaction acceptance on the lab Board before the interaction is treated as settled.

- 260731 JL · ⚑ The badge stops taking part in line breaking at all
  JL: "why is it on another line, it should be at the end of the sentence."
  The first repair had glued the badge to the last word inside a `nowrap` group, which stopped the badge from landing alone but dragged the word down with it, so the reader still saw a short line holding `row. ⚑3` and nothing else.
  The badge now sits in a zero-width inline block (`.sbz`), so the browser breaks the sentence exactly as it would with no badge present, and the pill paints off the final character; the demonstration sentence went from three lines to two.
  A badge that costs no width can paint past the text column, so the sentence's `summary` reserves a 52px flag gutter and the pill hangs inside it.
  Measured rather than eyeballed: 111 window widths from 360px to 1800px across three pages, with zero cases of the badge leaving its sentence's last line and zero cases of it crossing the card edge.

### Decision Now
- [ ] 🧠 JL accepts the interaction on the lab board
      Eyeball the demo on `QAa3`: the badge shape, the drawer depth, which lanes exist, and whether attachment across blank lines feels right; a tick here also closes the same row in Items to Finish.

## Files
### Engines
- `src/body.py`
  RENDER. The attachment walk (`last_p`, `appar`) and `render_apparatus`: which `>` lines fold under which sentence, and the ⚑ badge count.
- `cli/serve.py`
  WRITE. `add_sentence` and the `/_board/sentence` route: the anchor match, and the rule that a new lane is appended at the end of the sentence's existing run.
- `haipipe-board/assets/js/40-sentence/00-apparatus.js`
  The ➕ control that calls it: the lane dropdown, the input, and the `.saddrow` row inside an open drawer.
- `assets/css/10-focus.css`
  The `.sent` summary row, ⚑ badge, drawer, lane styles, and the hover tint.

### The demo home and the visibility boundary
- `../QB-delivery/QB4c-content.md`
  The self-demonstrating "Sentence apparatus" subsection (moved there with the Content grammar, 260729).
- `QAb3-agent-visibility.md`
  Whether anything attached this way reaches the chat opened on the same page.

## Glossary
probe binding: the path connection from a paper question to the evidence file that answers it.
paper dialect: the optional Board renderer that resolves paper-specific citations, values, displays, and probe markers.
MISQ: the target journal for the live paper Board used as the first rollout.
DR display id: the paper's short identifier for a display requirement or output.
HUMAN-ONLY: work that requires a person's account, judgment, or approval and cannot be completed silently by the agent.
`.bst`: the BibTeX style file that controls how a reference is formatted.
popover: a native browser panel that opens over the page when its marker is activated.
browser rule: the built-in browser styling that keeps a closed popover hidden.

## Log
260802 0110 · The comment lane gained its canonical form, `> Comment JL …` (JL, on QB4 §3.3.3), with the bare-initial `> JL: …` kept as a rendering alias and warned by `check.py` inside Content. Nothing needed migrating: all 156 bare-initial rows on the boards live in `## Discussion`, which is a different grammar. The badge also now names the kind rather than only the count
260731 2010 · ⚑ badge made zero-width (`.sbz`) with a 52px flag gutter on the sentence summary, so it never takes part in line breaking and never lands on a line of its own; verified over 111 window widths, 360px to 1800px
260731 · Items, Where we are, and Files regrouped to the QB4d/QB4e/QB4f subsection conventions (matrix retrofit)
260729 · Renamed QA8 -> QAb1 when the QAb sentence group was carved (JL); the overview half became `QAb0` and the demo's home is `QAa3`. Older lines below cite QA4/QA8; they are history
260725 · copy moved from per-sentence hover to section headings (JL): ⧉ on every section header copies the whole section as plain text, folded parts included
260725 · form trigger moved to double-click (single click freed, JL); hover ⧉ copy button ships the clean sentence text
260725 · click-to-add shipped: /_board/sentence endpoint + page form + drawer ➕ row; hover tint; smoke test wrote the Note line in QA4's demo drawer over HTTP
260725 · opened after the same question landed in both sessions; v1 adjacency fold + typed lanes shipped on the lab board, MISQ rollout and chips deferred
260727 · JL, on a sentence that had just gained a `> Value:` lane: "when I double click the sentence, I can enter the comments, but now it is gone, why?" The apparatus form, not the pinned comment. Cause was this face's own two-path design meeting the paper's evidence card: gaining a lane moves a sentence from a bare `<p>` into `<details><summary>`, and `board.js` excluded `summary` from the double-click guard because drawers have their own ➕ row. 116 of the MISQ board's sentences are already drawers and the count grows with every evidenced sentence, so the exclusion was retired rather than documented. First attempt inserted the form after the summary's `<p>`, which lands it INSIDE the summary where clicks toggle the drawer; corrected to the drawer body, matching what the ➕ row path already did.
