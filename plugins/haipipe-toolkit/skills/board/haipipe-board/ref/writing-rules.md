# Writing rules: how to write so it reads like human language

JL's words: **"If it is not easy to read, writing that much is rubbish."**
A board's entire value is that a second person can read it. Unreadable means unwritten. This rule sits above structure and layout.

`board-form.md` owns the board's shape. This file owns **how the words inside each section are written.** Everything is in English (JL 260724: board markdown, generated pages, and artifacts are English).

## The section shapes decided this session (260724)

These are not style preferences. `build.py` renders each section a specific way, so writing against the shape produces a broken page. The worked example is QA4 (`diagram/01-boardform-260722/QA4-pagelayout.md`).

- `## Opening` = one lead sentence, then one plain paragraph
  The first paragraph is the actual question, written as a question, and stays in Opening. Write the remainder as **one flowing paragraph** covering why the question is hard, what breaks while it stays open, and what it affects downstream. build.py labels it "Why this matters": a collapsed row inside Opening for S (every Opening row starts shut, JL 260725), or Content's first initially open subsection for Q. Do NOT use the old three-bullet form.
- `## Boundary` = `✅ Covered here` / `↪ Covered elsewhere`
  Two `- ` lines. The second must name the question that does cover the excluded part (for example "projection is QA3"), because a bare exclusion reads as a refusal. Use `↪`, not `❌`. Boundary folds into the same hidden block as the Opening and renders as flat rows, so keep each explanation to one line.
- `## Diagram` = one optional visual section, collapsed by default
  Use an ASCII figure, an Excalidraw share URL on its own line, or both. The page renders a peer-level `🖼 Diagram` row after Opening; the visual remains hidden until that row is clicked. Insert the Excalidraw URL whenever the figure is worth drawing on together: it becomes a live excalidraw plus a plain link, so a colleague can move boxes in the drawing instead of describing the edit in prose. Delete the whole section when the figure adds no information. Opening the row shows `▧ ASCII` and leaves `✏️ Excalidraw` shut one click further (JL 260726); write ONE `## Diagram` and let the renderer split it, because a hand-written `### ASCII` heading in here is not a recognized construct.
- S `## Content` = the stage's real product, and nothing else (JL 260725)
  On a manuscript page Content IS the section: its parts, paragraphs, and prose. Keep three kinds of material out of it. The inherited venue or writing contract goes under `## Stage Contract` (authored subsections there are safe: `stage.py sync` replaces only the generated block between the `haipipe:contract` markers). Settled flags and corrections go to `## Where we are`, which is what "what is true now" means. Anything still owed goes to `## Items to Finish`. build.py labels the section with the stage's name (`📚 Content · Main 7 §6 Results`), so if the name does not describe what a reader finds there, the page is carrying something that belongs elsewhere. That label comes from the page title, so when the artifact has its own number and it is offset from the board index, title the page `S Main 7 · §6 Results` and both numbers are stated instead of competing.
- `## Content` = two heading levels, and the number carries the depth (JL 260725)
  `###` is a division: a part that holds content of its own and folds on its own. `####` is one paragraph inside it, always, with no third level. Read the depth off the numbering (`§6` against `§6.1`), not off the heading level, because the page folds exactly one level and a deeper tree would collapse a whole section into one box. Write a division only when it holds something: a flat section carries one `### §1 Introduction` over its paragraphs, a subsectioned one starts at `### §6.1`, and no page opens a box onto nothing. The payoff is a shape you can check without reading: the subsection count is the number of `###` headings whose number contains a dot.
- `#### heading` then a full-line `(…)` = the paragraph and its job
  A paragraph heading carries no icon; 🔹 belongs to a group title, which is a full-line `**bold**` that really does lead a run of items. Do not use bold for a paragraph: build.py used to flatten `####` into bold and every paragraph came out claiming to be a group title. The optional `(…)` line directly under the heading is what that paragraph does, it renders in grey italic and stays on stage as a scan hook, and only the line immediately after the heading is read that way. Keep it to about 80 to 120 characters: past that it reads as prose and stops being scannable.
- S `### Stage Record` = one orientation record inside Opening
  Write it as a direct subsection of `## Content` with that exact heading. build.py lifts it beside "Why this matters" in Opening and keeps it collapsed; the remaining stage subsections stay under Content.
- Items (in `## Items to Finish`, `## Where we are`, `## Law`, `## Lesson`) = `- ICON heading` then a folded explanation
  Only the heading shows on stage, with a caret; the explanation opens on click. Start every item heading with an author-chosen emoji icon (build.py never guesses one). The first indented line is a one-sentence summary; the lines after it are the long explanation. Write the explanation as a real paragraph (what it means, what happened, what we understand so far, why it ended up this way), not a clause. Length is free here because it is folded.
- `## Where we are` = one summary paragraph, then dated items
  Open with a concise paragraph stating what has been achieved and what is still unproven. Then list items, each prefixed `YYMMDD WHO ·` (for example `260722 JL ·`), ordered by date. build.py strips that prefix into a muted right-aligned stamp, so the date and person never sit inside the title text.

## Hard rules

- **No em-dashes** (JL 260724: "fuck em-dash")
  Never use the em-dash in prose. Use a colon when expanding on what came before, a semicolon or a new sentence for two linked clauses, parentheses or commas for an aside. This is a rewrite per sentence, never a blind find-and-replace: each dash needs the mark its own sentence calls for.
- **One sentence per source line** (JL 260725)
  The renderer gives every plain prose line its own row on the page, so a hard wrap in the middle of a sentence becomes a broken line the reader sees. Write each sentence as one source line and let the browser soft-wrap it; start a new line only at a sentence boundary. This also gives each sentence a clean anchor for comments and future sentence-level apparatus.
- **Sound like a person, not a model**
  Plain declaratives. Cut the AI tells: "it is worth noting", "plays a crucial role", "in the realm of", "delve into", "a testament to", empty tricolons, and sentences that restate the previous sentence with grander words. Say the thing once, concretely, and stop.
- **No coined words**
  Every phrase is either a source-document term or is defined in `## Glossary`. Real damage done before: inventing "outward anchoring", "first act", "three-set gate", words that appear zero times in any source. The reader trusts them as jargon, goes to look them up, and finds nothing. When unsure, use the source word even if it is plain.
- **An ASCII figure must survive being copied**
  Never draw two trees side by side. The column boundary is whitespace, it disappears the moment anyone pastes the figure into chat or an email, and the right column's rows then read as branches of the left one, so the figure states a structure that does not exist. Real case: a two-column comparison of the Introduction and Results heading trees came back pasted as one tree in which the Results subsections held the Introduction's paragraphs. Stack the trees, one complete tree at a time. Columns are safe only for short parallel lists where a wrong reading is obvious at a glance.
- **No author notes to self**
  Do not write explanations of the markup or the tooling into the page (for example a note about why an ascii figure is left-anchored). The reader needs the content, not the reasoning behind how it was typeset.
- **A short heading is a phrase, not a sentence**
  The complete question belongs in `## Opening`. Keep the `# title` and every item heading short.
- **Give numbers**
  "Basically done" and "works well" say nothing. Write "2 of 7 questions are clear", "agreement fell from 0.93 to 0.67".
- **Each question is self-contained**
  A reader should not have to open another question to follow this one. To reference another question, name its id and say what it covers.
- **`## Topic` answers "what is this project"**
  The harshest first cold-read note: "it explains the format of a recipe but never says what the dish is." Identify JL, CC, and the colleagues involved, then state what real problem is being solved.
- **Keep sentence review where it belongs**
  Sentence-local `> WHO:` and `> ✎` lines are the durable review trail; do not erase them.
- **Clear out stale text**
  When the board changes, old descriptions elsewhere become wrong. Real case: QA4 said "side by side" long after the layout had been stacked. A zero-background reader catches these self-contradictions on the first pass.

## Zero-background review (the convergence test)

Reading it yourself in the same conversation is useless: you know too much that never made it onto the page. Open a fresh agent.

Its brief:

```
You have never seen this project, attended any meeting, read any code, or met JL, CC, or their colleagues.
Read only the markdown files I give you, nothing else.
Report only three things. Do not praise, do not summarise what reads well:
  1. Which sentence is unreadable. Quote it, and say whether it is unclear reference,
     a missing premise, or three things packed into one sentence.
  2. Which word is undefined. List it, note the file it first appears in and whether
     that file's ## Glossary defines it.
  3. What premise is missing. Something you must know to follow these files that the
     files never state.
Then rate each question: clear / half / unreadable.
"half" = you can restate what it asks, but not why it matters or what counts as done.
```

Fix what it reports, then it is done.

**Convergence test:** no question is "unreadable", and every "half" reason is either handled or written down as a known gap.
