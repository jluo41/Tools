# Writing rules: how to write so it reads like human language

JL's words: **"If it is not easy to read, writing that much is rubbish."**
A board's entire value is that a second person can read it. Unreadable means unwritten. This rule sits above structure and layout.

`board-form.md` owns the board's shape. This file owns **how the words inside each section are written.** Everything is in English (JL 260724: board markdown, generated pages, and artifacts are English).

## The section shapes decided this session (260724)

These are not style preferences. `build.py` renders each section a specific way, so writing against the shape produces a broken page. The worked example is QB4 (`skills/diagrams/BoardSkillBoard-260722/QPs-page-structure/QPs1-overall/QPs1-overall.md`).

- `## Opening` = one lead sentence, then one plain paragraph
  The first paragraph is the actual question, written as a question, and stays in Opening. Everything before the FIRST BLANK LINE is what a reader sees without clicking, and it is 4 to 5 sentences, about five lines on screen, target roughly 450 characters, hard ceiling 520, which is what `check.py` enforces, measured on the render (JL 260801). Inside that ceiling it is **one flowing, page-specific rationale** with no required order of beats. Stop when a cold reader can say why the question deserves attention and what this page owns. Scope, difficulty, failure, downstream effect, and a success consequence are diagnostic prompts, not sentence slots; use only the ones that reveal this page's real stake. build.py labels that drawer "More details" as a collapsed row inside Opening for Q and S (it read "Why this matters" until JL renamed it on 260801). Do NOT use the old bullet form. There is no separate `## Boundary`; name the neighbouring page in this paragraph when it owns excluded work.
- `## Diagram` = the ascii figure, alone, collapsed by default
  The page renders a peer-level `🖼 Diagram` row after Opening; the figure stays hidden until that row is clicked. The section holds ascii only: a page's real drawing is an Excalidraw scene in the page's own `draw/` folder, opened through the Draw split, never embedded here (JL 260815). Delete the whole section when the figure adds no information. EVERY FIGURE CARRIES A CAPTION LINE ABOVE IT (JL 260801): write `**Name**: what this diagram shows.` directly above the fence, one line only, since a section may hold several figures and an unlabelled one has to be decoded before it can be read. A ROW IS A LABEL AND ITS VALUE, NEVER A CLAUSE (JL 260801): if a row could end in a period it is prose and belongs in the paragraph under the figure, so write `🎯 Aims   A3.1 · A3.2 · P1` rather than `🎯 Aims are durable targets that stay stable when the route changes`. A figure earns its fence by being scannable.
- S `## Content` = the stage's real product, and nothing else (JL 260725)
  On a manuscript page Content IS the section: its parts, paragraphs, and prose. Keep four kinds of material out of it. Required Inputs and Venue go under `## Stage Contract`; inherited and page-owned prose rules go under `## Writing Style`. `stage.py sync` replaces only their generated `haipipe:contract` and `haipipe:style` blocks. Settled flags and corrections go to `## States`, which is what "what is true now" means. Intended outcomes go to `## Aims`; a temporary next move may appear as that Aim's optional `Plan`. build.py labels the section with the stage's name (`📚 Content · Main 7 §6 Results`), so if the name does not describe what a reader finds here, this section is carrying something that belongs elsewhere. That label comes from the page title, so when the artifact has its own number and it is offset from the board index, title the page `S Main 7 · §6 Results` and both numbers are stated instead of competing.
- `## Content` = two heading levels, and the number carries the depth (JL 260725)
  `###` is a division: a part that holds content of its own and folds on its own. `####` is one paragraph inside it, always, with no third level. Read the depth off the numbering (`§6` against `§6.1`), not off the heading level, because the page folds exactly one level and a deeper tree would collapse a whole section into one box. Write a division only when it holds something: a flat section carries one `### §1 Introduction` over its paragraphs, a subsectioned one starts at `### §6.1`, and no page opens a box onto nothing. The payoff is a shape you can check without reading: the subsection count is the number of `###` headings whose number contains a dot.
- `#### heading` then a full-line `(…)` = the paragraph and its job
  A paragraph heading carries no icon; 🔹 belongs to a group title, which is a full-line `**bold**` that really does lead a run of items. Do not use bold for a paragraph: build.py used to flatten `####` into bold and every paragraph came out claiming to be a group title. The optional `(…)` line directly under the heading is what that paragraph does, it renders in grey italic and stays on stage as a scan hook, and only the line immediately after the heading is read that way. Keep it to about 80 to 120 characters: past that it reads as prose and stops being scannable.
- S `## Stage Contract` = the stage's ONE contract, and there is no second name for it
  Everything a stage must honour goes in this section: what it requires, the venue's constraints, what it provides. JL 260801 collapsed the old `### Stage Record` into it, because two names for one obligation meant nobody could say which held what. A legacy `### Stage Record` under `## Content` still renders: build.py lifts it into the Stage Contract as its opening lines. Write nothing new under that heading.
- `## Aims` = durable targets linked to Content
  Mirror the relevant Content division: `A3.1` is an Aim for division 3, and its group is `### A3 · <that division's name>`, carrying the division's number, name and emoji (JL 260801, the letter fixed to `A` on 260802; `C<n>` still resolves). Use `P1` only when a target crosses divisions. Write `Done when` as a testable result and add `Plan` only when a temporary next move is worth preserving. A checkbox Aim (`- [ ]` with an emoji lead) is the first-class form (JL 260815); write id Aims only when a page's progress must be machine-tracked, and then keep States mirroring the ids.
- `## States` = one factual current State row per Aim
  The paired section labels are plural because both contain multiple records: Aims contains Aim records; States contains their State records. Mirror the Aims groups and ids. Use `⬜` not started, `🔨` being worked on now, `🧠` waiting on a person or on something outside this page, `✅` met with the evidence named, or `❄️` on ice; each says its meaning by shape (JL 260802), and the older `🟡` `🟠` `⏸️` still parse but are not what to write. A State says what is true now; it never says what should happen next, and it never keeps an earlier now beside the current one. Put the reason for a transition in `## Log`.
- Other items (in `## Law`, `## Lesson`, and dated Log records) = `- ICON heading` then a folded explanation
  Only the heading shows on stage, with a caret; the explanation opens on click. Start every item heading with an author-chosen emoji icon (build.py never guesses one). The first indented line is a one-sentence summary; the lines after it are the long explanation. Write the explanation as a real paragraph (what it means, what happened, what we understand so far, why it ended up this way), not a clause. Length is free here because it is folded. A `## Glossary` entry takes the same `- ICON` row, with the TERM in bold and its definition after a colon (JL 260802), because the term is what the reader arrived looking for.

## Hard rules

- **Content is numbered all the way down** (JL 260801)
  A division is `### 3 · Content`, a group is `**3.2 · Group title**`, a paragraph is `#### 3.2.1 · Its heading`; an ungrouped division runs `#### 3.1 ·` straight through, so the number's depth says whether a group exists. The index makes a long division navigable and citable: `1.2.3` is something a person can point at, and a bare heading is not.

- **`More details` is a list of labelled parts, never one block of prose** (JL 260801)
  Each part starts with a bold label saying what it answers, then its sentences, with a blank line between. The paragraph on stage is read straight through; `More details` is opened by someone hunting one specific thing, and a block of prose gives them no label to scan for.

- **A change is finished when it is ON THE RENDERED PAGE** (JL 260801)
  Do not stop mid-way to ask for approval. Write the source, propagate the rule to `ref/page-template.md` and `haipipe-page` so new pages inherit it, run `check.py`, then confirm the RENDER, not the markdown. Source-is-correct is not page-is-correct: a stopped watcher and a shut `<details>` each produce a correct file and a wrong page. A half-applied change is worse than either finishing or not starting.


- **No em-dashes** (JL 260724, ruled emphatically)
  Never use the em-dash in prose. Use a colon when expanding on what came before, a semicolon or a new sentence for two linked clauses, parentheses or commas for an aside. This is a rewrite per sentence, never a blind find-and-replace: each dash needs the mark its own sentence calls for.
- **One sentence per source line** (JL 260725)
  The renderer gives every plain prose line its own row on the page, so a hard wrap in the middle of a sentence becomes a broken line the reader sees. Write each sentence as one source line and let the browser soft-wrap it; start a new line only at a sentence boundary. This also gives each sentence a clean anchor for comments and future sentence-level apparatus.
- **Sound like a person, not a model**
  Plain declaratives. Cut the AI tells: "it is worth noting", "plays a crucial role", "in the realm of", "delve into", "a testament to", empty tricolons, and sentences that restate the previous sentence with grander words. Say the thing once, concretely, and stop.
- **Do not turn review questions into a prose template**
  A rubric may ask about value, difficulty, failure, downstream effect, and acceptance. That does not authorize five matching sentences or a fixed order. Repeating `This page ...`, `The hard part ...`, `Without ...`, and `It succeeds when ...` across a batch is form filling, even when every sentence is individually clear. Speak about the subject, use the beats the page actually needs, and stop. Apply the noun-substitution test: if changing a few nouns makes the paragraph fit another page, it says too little about this one.
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
  Sentence-local `> Comment WHO` and `> ✎` lines are the durable review trail; do not erase them. A person's remark is written `> Comment JL …` (JL 260802); the older `> JL:` still renders, and `check.py` warns on it inside Content.
- **The page says what IS; the Log keeps the story** (JL 260815)
  Write the title, Opening, and Content for someone who arrived today: the current contract, in plain words, standing on its own.
  Decision dates, people's names, ruling references, retired mechanisms, and what the old way did are history, and history's home is `## Log` (and the board's Pipeline), where a reader goes when they want the story.
  The test: if a sentence needs a date or a name to stay true, it is a Log line, not Content.
- **Clear out stale text**
  When the board changes, old descriptions elsewhere become wrong. Real case: QA4 said "side by side" long after the layout had been stacked. A zero-background reader catches these self-contradictions on the first pass.

## Zero-background review (the convergence test)

Reading it yourself in the same conversation is useless: you know too much that never made it onto the page. Open a fresh agent.

Its brief:

**The zero-background reviewer prompt**: what to paste to a fresh agent so the page is read cold.

```
You have never seen this project, attended any meeting, read any code, or met JL, CC, or their colleagues.
Read only the markdown files I give you, nothing else.
Report only four things. Do not praise, do not summarise what reads well:
  1. Which sentence is unreadable. Quote it, and say whether it is unclear reference,
     a missing premise, or three things packed into one sentence.
  2. Which word is undefined. List it, note the file it first appears in and whether
     that file's ## Glossary defines it.
  3. What premise is missing. Something you must know to follow these files that the
     files never state.
  4. Which paragraph is interchangeable or templated. Name the other page it could fit,
     the repeated sentence stem or rhetorical sequence, and the smallest specific rewrite.
Then rate each question: clear / half / unreadable.
"half" = you can restate what it asks, but not why it matters or what counts as done.
```

Fix what it reports, then it is done.

For a batch, read the changed sections consecutively in Board order after the page-by-page pass. A page that is clear alone still fails readability when the batch reveals a reusable form-letter voice.

**Convergence test:** no question is "unreadable", every "half" reason is either handled or written down as a known gap, and no changed paragraph remains interchangeable after noun substitution.
