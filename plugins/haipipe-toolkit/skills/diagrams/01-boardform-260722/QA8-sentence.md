# Sentence apparatus: click a sentence, see its evidence
state: 🟡 PARTIAL
owner: JL
method: fold typed `>` lanes and threads under the sentence they follow; inline-marker chips come next

## Question
When a sentence carries evidence (a citation, a number, a display, a probe binding, a review thread), how does the page show the sentence clean and reveal that apparatus only on click?

One sentence per source line (0.19.0) made the sentence the board's atomic row, and the paper dialect already writes evidence next to it: `> CHECK:` blocks and `> JL:` / `> CC:` threads sit directly under the sentence they discuss, while placeholders (`\cite{TOADD}`, `{VAL:? …}`, `[Q-Section-n]`) sit inside it.
Until now the board rendered all of that as loose sibling paragraphs, so a reviewed sentence drowned in its own apparatus.
JL asked for the sentence to be clickable with the hidden things beneath it (260725, asked in both working sessions); this face is the single ruling both sessions implement against, piloted on this board as the experiment lab before anything touches the MISQ paper board.

## Boundary
- ✅ Covered here
  The apparatus lane grammar (`> Kind:` lines under a sentence), which `>` runs attach and which do not, the ⚑ badge, and the drawer rendering.
- ↪ Covered elsewhere
  Inline-marker chips (`\citep` resolution, probe-state coloring) are the paper dialect layer, not yet ruled; `QA4` owns the page order the drawer lives in; comment pinning stays `QA6`.

## Content
### Lane grammar
A `>` line directly under a sentence (blank lines tolerated between them) attaches to that sentence.
Typed lanes name the attachment: `> Citation:` 📚 · `> Value:` 🔢 · `> Display:` 🖼 · `> Check:` ⚠️ · `> Q-consumer:` 🔎 · `> Link:` 🔗 · `> Source:` 📄 · `> Note:` 📝.
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

## Items to Finish
- [x] ⚑ Adjacency fold shipped
      A plain sentence followed by `>` lines renders as a native `<details>`: the sentence plus a ⚑N badge on stage, the apparatus in a drawer beneath.
      Implemented in `src/body.py` (`render_apparatus` + the `last_p` attachment walk); the zero-script invariant holds because the fold is native HTML.
- [x] 🎬 Self-demonstrating example on QA4
      QA4's Content carries a "Sentence apparatus" subsection written in the grammar it documents, so the lab page demonstrates the interaction on itself.
- [x] 🖱 Hover tint shipped
      The sentence under the cursor tints slightly (accent at 8%), so you can see which sentence a click or a selection will target.
      Pure CSS, both themes, shipped 260725 on JL's ask.
- [x] ➕ Click-to-add writes into the markdown
      Shipped 260725: `POST /_board/sentence` in `serve.py` finds the exact sentence line (markdown-stripped match), appends `> Lane: text` at the end of its apparatus run, and rebuilds; a miss returns a visible error and writes nothing.
      On the page, clicking a bare sentence opens the lane + text form beneath it, and every open drawer ends with an "➕ add to this sentence" row.
      Smoke-tested over HTTP: the Note line in QA4's second demo drawer was added through the endpoint.
- [ ] 🧠 JL accepts the interaction on the lab board
      Eyeball QA4: the badge shape, the drawer depth, which lanes exist, and whether attachment across blank lines feels right.
      This checkbox is the stop point before anything rolls beyond this board.
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
- [ ] 🎨 Inline-marker chips
      `\citep{}` / `\cite{TOADD}` / `{VAL:? …}` / `[Q-X-n]` render as status chips inside the sentence, resolved against the paper's .bib, `1-probes/`, and `0-displays/`.
      Needs the `dialect: paper` opt-in ruling before code.

## Where we are
v1 shipped 260725 on this board only: `src/body.py` gained `render_apparatus` and the attachment walk, `assets/board.css` gained `.sent` / `.sbadge` / `.sapp` / `.lane`, and QA4 carries the live demo.
The hover tint and the click-to-add ➕ flow shipped the same day: `/_board/sentence` in `serve.py`, the form and drawer row in `assets/board.js`, smoke-tested live on QA4.
The MISQ paper board took the rollout the same day (the 📄 item): 20 typed lanes, 52 sentence drawers, every `> JL:` line intact.
Interaction refinements, 260725 evening: double-click opens the form (single click freed for reading), and every section heading carries a ⧉ button that copies the whole section as plain text (the per-sentence hover copy was tried and removed on JL's call).

## Files
- `src/body.py`
  The attachment walk (`last_p`, `appar`) and `render_apparatus`.
- `assets/board.css`
  The `.sent` summary row, ⚑ badge, drawer, and lane styles.
- `QA4-pagelayout.md`
  The self-demonstrating "Sentence apparatus" subsection.

## Log
260725 · copy moved from per-sentence hover to section headings (JL): ⧉ on every section header copies the whole section as plain text, folded parts included
260725 · form trigger moved to double-click (single click freed, JL); hover ⧉ copy button ships the clean sentence text
260725 · click-to-add shipped: /_board/sentence endpoint + page form + drawer ➕ row; hover tint; smoke test wrote the Note line in QA4's demo drawer over HTTP
260725 · opened after the same question landed in both sessions; v1 adjacency fold + typed lanes shipped on the lab board, MISQ rollout and chips deferred
