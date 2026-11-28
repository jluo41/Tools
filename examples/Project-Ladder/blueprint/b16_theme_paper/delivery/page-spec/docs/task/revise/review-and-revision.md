# Review and revision

Draft Lab: the Section's text, one row per sentence, with its marks after the words and its cards beside it.
Code: `servers/workbench/workbench-task-draft/`. Rules: hai-paper `ref/must-check.md`, M-D section.
Each topic below is one part of the page, with its own requests: JL's words, the session it came through, what changed.

## 🔢 Topic: Sentence number

Two numbers, both always shown: its place in the paragraph (1, 2, 3) on top, and under it its id (s28, the address
cards and comments use).
Code: `.s-ord`, `order()` in draft_step_evidence_rows.py.

| When | Asked | Through | What changed |
| --- | --- | --- | --- |
| 11-15 | "where is the 1, 2, 3, 4? I am so confused" | ScalingGlucose Board | one number per sentence, 1, 2, 3 inside each paragraph |
| 11-15 | "I think we should also have the 1, 2, 3, 4, right?"; the C labels were cut off | AITC Board | the same; the C0/C1 labels left the column, the full id is on hover |
| 11-15 | "I get this 1, 2, 3, 4, where is the sNN, sNN, oh my god, I cannot bear anymore." | ScalingGlucose Board | both shown: 1, 2, 3 on top, sNN under it (the Board's own fix, kept; test updated) |

## 📎 Topic: Evidence marks

📊n values, ❝n citations, 🖼n displays after the sentence; a mark is lit while its evidence waits on a person; a chip
only for a broken item (its icon and ❗), ⚠ for a number with no item.
Code: `.sx-evm`, `.sx-evm.unv` in draft_step_evidence_rows.py; `chips()` in draft_step_support.py.

| When | Asked | Through | What changed |
| --- | --- | --- | --- |
| 11-15 | the "⚠ no item" chip on numbers a paper reports | ScalingGlucose t01 | a sentence a CITE item covers gets no ⚠ |
| 11-15 | "why two check marks" | ScalingGlucose t01 | the all-resolved ✓ became 🔗 |
| 11-15 | "we have the emoji for the numbers and for the cite, why we still need this" | ScalingGlucose t01 | 🔗 removed |
| 11-15 | "if it is not check, you should highlight that" | ScalingGlucose t01 | ❝ lit while a citation is unverified; the inline ? removed |
| 11-15 | all 14 ❝ orange read as alarm | ScalingGlucose Board | an unverified ❝ is soft: amber, dotted underline, no fill |
| 11-15 | t02 s2 "(Fig. 1)" showed only its value mark, no display mark | ScalingGlucose t02 | every VALUE, DISPLAY and TABLE item of the evidence-items file gives its sentence 📊 or 🖼 |
| 11-16 | the ⚠ chip and health's new support row should agree; Extended Data legends print numbers their display backs | ScalingGlucose t04 (for the Board) | a DISPLAY or TABLE item now clears ⚠, as VALUE and CITE do, the same rule as `page.py health` row support |

## ★ Topic: Scores

Every score in one form, ★ then the number; under 8 in colour.
Code: `.sx-ai`, `.sx-pscore`, the Logic card head, the Review Report.

| When | Asked | Through | What changed |
| --- | --- | --- | --- |
| 11-15 | "why I didn't see the AI eval score"; "why no per sentence eval and per paragraph eval?" | ScalingGlucose t01 | every sentence shows its score; each paragraph heading its Flow score |
| 11-15 | "for this we should have the star, right?"; "make the star to be anywere ... be consistent" | ScalingGlucose t01 | ★ before every score, in every place |

## 🧩 Topic: Logic card

A paragraph's flow: the problem first, then the paragraph drawn as the Structure view draws it (its box on the left, a
curve to one row per sentence with its role and point from § 1; on the sentence after the weakest join a small amber
note "weak link from s39: from reuse to model size"), then the Fix. Code: `map_html` in draft_step_flow_card.py, `_flow_with_map` in draft_step_revise.py.

| When | Asked | Through | What changed |
| --- | --- | --- | --- |
| 11-15 | "the logic here is less readable" | ScalingGlucose t01 | redrawn: problem first, one step per row, ✂ weakest join |
| 11-15 | "I don't understand this, why not just have the thins like the mindmap graph like we have in the structure"; "could you show it? what I want is like this." | ScalingGlucose t01 | the step rows and the quoted ✂ line replaced by the Structure view's map of the paragraph, inside the card and behind 🧩 on the heading |
| 11-15 | "what does this mean?" (the bare ✂ on the map) | ScalingGlucose t01 | the ✂ became words on that row: "weak link from s39: <why>" |

## ❝ Topic: Citation card

One card per cited sentence, a ❝ line per item. Code: `draft_step_cite_items.py`; `cite_tasks.py bind`.

| When | Asked | Through | What changed |
| --- | --- | --- | --- |
| 11-15 | no ❝ and no card unless someone hand-wrote a Local Run | ScalingGlucose t01 | a card for every CITE item; `bind` writes the Run; health flags an unbound item |

## ✏️ Topic: Edit card

A proposed change to one sentence: the change first (old to new words), then its reason as numbered points, one per row;
a source's quote or a paper list in a Detail that starts closed. Code: `_revise_card`, `_why` in draft_step_revise_cards.py.

| When | Asked | Through | What changed |
| --- | --- | --- | --- |
| 11-15 | "report the Board and Workbench, this is not readable" (a 150-word Why above the change) | ScalingGlucose t01 | the change comes first; a `Detail:` line shows closed |
| 11-15 | "No, I think the previous version and content is good, Just think about how to make it more readable." | ScalingGlucose t01 | no cap on the Why; `(1) … (2) …` points drawn one per row (rule M-D21 rewritten) |
| 11-15 | "for the sentences with problem, please show the editing card with reasoning and suggestion options in the UI" | ScalingGlucose t01 | rule M-D22: every problem sentence gets a card (reviewer gives a Fix or `A … \| B …`, writer cards it); the gate fails a problem with neither; a second Use this hides where a card stands |
| 11-15 | "why the old edit didn't faded away? I think you should add a discard button here" | ScalingGlucose t01 | a Discard button beside Confirm (the card is rejected, fades and folds, the sentence keeps its words); the "drop it" option is gone; a change made elsewhere swaps the changed rows in place at once, so an old card leaves |
| 11-15 | "I didn't find what does the B mean here? ... if B is unchanged, you say unchanged" (t02 s58, B only splits the sentence) | ScalingGlucose t02 | every option shows its change struck red and green, picked or not; an option equal to the Original reads "unchanged" |
| 11-15 | "this is very confusing" (t02 s40: option A "Keep." drawn as a rewrite; the card's "Chosen: Option B" showed A picked) | ScalingGlucose t02 | a Keep option (Keep, Keep., Keep as is, Keep it) is the Original and reads "unchanged"; `Chosen: Option B` is read as B |

## ✅ Topic: Accept

What ✓ Accept writes into the Draft. Code: `_write_sentence_locked`, `split_sentences` in draft_step_revise_notes.py.

| When | Asked | Through | What changed |
| --- | --- | --- | --- |
| 11-15 | what Confirm does with a card whose Expected is two sentences (t01 s8, s12, s17 …) | ScalingGlucose t01 | it wrote both into one row; now each sentence gets its own row (s12, then s12a) until the next renumber |
| 11-15 | adopt broke on a "B1a" row (wrote s1 twice, dropped s5); JL's look "1 / s1, 2 / s1a, 3 / s2" | ScalingGlucose t02 | a split now numbers the paragraph's Bullets on (B1, B2, B3 …), keeps later ids, shifts the evidence targets, and adds the Structure row; adopt keeps a lettered Bullet too |

## 🧩 Topic: Paragraph heading

A paragraph's heading row: its title, its ★ score, 🧩 its logic map. Code: `pscore()` in draft_step_evidence_rows.py,
`map_html` in draft_step_flow_card.py.

| When | Asked | Through | What changed |
| --- | --- | --- | --- |
| 11-15 | a mark on each paragraph heading that opens the paragraph's logic as a small map: one node per sentence, its role, A-B-A or a weak join marked | ScalingGlucose t02 | 🧩 on every heading; a click opens the steps as nodes in order, ✂ on the weakest join, each node's role when the Flow line gives `shape: topic s6, support s7 to s11, hand-off s12`; the Logic card shows the Flow line's fix |

## 📁 Topic: Paragraph fold

When a paragraph starts closed. Code: `checkedfold()` and `pfold()` in draft_step_evidence_rows.py.

| When | Asked | Through | What changed |
| --- | --- | --- | --- |
| 11-15 | a paragraph whose every sentence is checked starts collapsed to its heading and score; any unchecked or changed sentence keeps it open | ScalingGlucose t02 | already done by draft_autofold.py (a duplicate I added was removed); checked live on t01 and t02 |
| 11-15 | "so the first paragraph are all checked, right? why it is not collapsed?" | ScalingGlucose t01 | the tab remembered its first fold decision from before P1 was all checked; now judged from today's checks on every load, only hand-opened paragraphs remembered, and a lapsed check opens it again |

## ☑️ Topic: Check (✓)

The person's own mark on a sentence. Code: the `.sx-ok` click in draft_step_evidence_rows.py; `/_board/draft-comment`.

| When | Asked | Through | What changed |
| --- | --- | --- | --- |
| 11-15 | "the check doesn't work"; "I can't click this." | ScalingGlucose t01 | cause: the 📊/🖼 change reused the name holding the Section, so every ✓ and card sent "C1.P7.B5" and got 400; fixed, with a test; a refused ✓ now says why beside it |
| 11-16 | a ✓ on the ScalingGlucose Abstract s5 did nothing | ScalingGlucose Board | the checked file mixed old "S1" and new "s2" ids and their sort crashed; the sort now lowercases and keeps numbers and letters apart (fixed by the Board session) |

## 🔍 Topic: Review card

A sentence's review: its ★ and three scores, its topics and points (marked over the limit: two topics or more than
three points), the problem, a suggestion. Code: `_logic_card` in draft_step_revise.py. Rubric: hai-draft-review
`ref/sentence-logic.md`, Topic check and Point count.

| When | Asked | Through | What changed |
| --- | --- | --- | --- |
| 11-15 | "one sentence one topic, usually one or two points, at most three points. check s12" | ScalingGlucose t01 | rubric: a point defined, four or more caps read at 7, the count written on the line; card: a "1 topic · 2 points" chip, amber when over |
| 11-15 | "this is the weird expression, for the sentence level evaluation, and one rule is to identify the weird non-human expression, like this." (s12 "need not mean") | ScalingGlucose t01 | rubric: a Natural phrasing check, each unnatural phrase named with its plain wording, caps ai at 7, five worked examples; the sentence reader reads aloud; must-check M-D23 |
| 11-15 | "the editing card is very bad, report to Workbench to avoid it again" ("Fix: see the card" offered with ✓ Use this, the whole sentence struck) | ScalingGlucose t03 | a Fix is offered as a new sentence only when it is one (ends in . ? !, no pointer, at least 40% of the length, shares a word); otherwise it shows as a plain Fix note; ✓ Use this refuses the same on the server |

## 🖱️ Topic: Row highlight

What lights a sentence row. Code: `.rv-lit` in draft_steps_assets.py.

| When | Asked | Through | What changed |
| --- | --- | --- | --- |
| 11-15 | "can you find the reason why here????" (a yellow row) | ScalingGlucose Board | it was the hover highlight; removed. Pointing at a card still lights its sentence briefly |

## 🤔 Topic: Selection popup

Words selected in a sentence pop two buttons: 💬 opens a comment on them; 🤔 saves them as an issue at once, no reason
typed. An issue is a comment entry whose note is `🤔 issue`; its sentence's gutter mark shows 🤔, and its card's delete
removes a slip. Code: `.nt-sel`, `issue()` in draft_steps_assets.py; `/_board/draft-comment`.

| When | Asked | Through | What changed |
| --- | --- | --- | --- |
| 11-15 | "when I select this, could you pop out two buttom, one is comments, just emoji, and the other one is issue ... I don't want to provide the reason, to speed up"; the emoji "like a question mark?" | ScalingGlucose t01 | 💬 and 🤔 on selection (❓ first, then JL: "🤔 <--- use this one."); 🤔 writes `Quote: <words>`, `State: open`, `- Note · <time>: 🤔 issue` to the comments file |

