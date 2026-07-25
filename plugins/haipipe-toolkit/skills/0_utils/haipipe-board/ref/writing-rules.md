# Writing rules — how to write so it reads like human language

JL's words: **"If it is not easy to read, writing that much is rubbish."**
A board's entire value is that a second person can read it. Unreadable means unwritten. This rule sits above structure and layout.

`board-form.md` owns the board's shape. This file owns **how the words inside each section are written.** Everything is in English (JL 260724: board markdown, generated pages, and artifacts are English).

## The section shapes decided this session (260724)

These are not style preferences. `build.py` renders each section a specific way, so writing against the shape produces a broken page. The worked example is QA4 (`diagram/01-boardform-260722/QA4-pagelayout.md`).

- `## Question` = one lead sentence, then one plain paragraph
  The first paragraph is the actual question, written as a question, and stays in Opening. Write the remainder as **one flowing paragraph** covering why the question is hard, what breaks while it stays open, and what it affects downstream. build.py labels it "Why this matters": inside Opening for S, or as Content's first initially open subsection for Q. Do NOT use the old three-bullet form.
- `## Boundary` = `✅ Covered here` / `↪ Covered elsewhere`
  Two `- ` lines. The second must name the question that does cover the excluded part (for example "projection is QA3"), because a bare exclusion reads as a refusal. Use `↪`, not `❌`. Boundary folds into the same hidden block as the Question and renders as flat rows, so keep each explanation to one line.
- `## Diagram` = one optional visual section, collapsed by default
  Use one ASCII figure or supported Excalidraw share link. The page renders a peer-level `🖼 Diagram` row after Opening; the visual remains hidden until that row is clicked. Delete the whole section when the figure adds no information.
- S `### Stage Record` = one orientation record inside Opening
  Write it as a direct subsection of `## Content` with that exact heading. build.py lifts it beside "Why this matters" in Opening and keeps it collapsed; the remaining stage subsections stay under Content.
- Items (in `## Items to Finish`, `## Where we are`, `## Law`, `## Lesson`) = `- ICON heading` then a folded explanation
  Only the heading shows on stage, with a caret; the explanation opens on click. Start every item heading with an author-chosen emoji icon (build.py never guesses one). The first indented line is a one-sentence summary; the lines after it are the long explanation. Write the explanation as a real paragraph (what it means, what happened, what we understand so far, why it ended up this way), not a clause. Length is free here because it is folded.
- `## Where we are` = one summary paragraph, then dated items
  Open with a concise paragraph stating what has been achieved and what is still unproven. Then list items, each prefixed `YYMMDD WHO ·` (for example `260722 JL ·`), ordered by date. build.py strips that prefix into a muted right-aligned stamp, so the date and person never sit inside the title text.

## Hard rules

- **No em-dashes** (JL 260724: "fuck em-dash")
  Never use the em-dash in prose. Use a colon when expanding on what came before, a semicolon or a new sentence for two linked clauses, parentheses or commas for an aside. This is a rewrite per sentence, never a blind find-and-replace: each dash needs the mark its own sentence calls for.
- **Sound like a person, not a model**
  Plain declaratives. Cut the AI tells: "it is worth noting", "plays a crucial role", "in the realm of", "delve into", "a testament to", empty tricolons, and sentences that restate the previous sentence with grander words. Say the thing once, concretely, and stop.
- **No coined words**
  Every phrase is either a source-document term or is defined in `## Glossary`. Real damage done before: inventing "outward anchoring", "first act", "three-set gate", words that appear zero times in any source. The reader trusts them as jargon, goes to look them up, and finds nothing. When unsure, use the source word even if it is plain.
- **No author notes to self**
  Do not write explanations of the markup or the tooling into the page (for example a note about why an ascii figure is left-anchored). The reader needs the content, not the reasoning behind how it was typeset.
- **A short heading is a phrase, not a sentence**
  The complete question belongs in `## Question`. Keep the `# title` and every item heading short.
- **Give numbers**
  "Basically done" and "works well" say nothing. Write "2 of 7 questions are clear", "agreement fell from 0.93 to 0.67".
- **Each question is self-contained**
  A reader should not have to open another question to follow this one. To reference another question, name its id and say what it covers.
- **`## Topic` answers "what is this project"**
  The harshest first cold-read note: "it explains the format of a recipe but never says what the dish is." Identify JL, CC, and the colleagues involved, then state what real problem is being solved.
- **Never delete someone's comment**
  Lines starting `> JL:` are only added to. When resolved, tick `[x]` in `## Comments`, do not erase.
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
