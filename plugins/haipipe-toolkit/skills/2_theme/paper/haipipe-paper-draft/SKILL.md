---
name: haipipe-paper-draft
description: "The paper's draft Task: one Section, the Abstract or a letter of one version (task-type: draft), the paper's rules on top of haipipe-draft; executes one row of the version's ## Narrative and keeps its Requirement (venue rules, rubric, SUB-* rows). Evidence and displays follow haipipe-paper-evidence; the whole manuscript is haipipe-paper-assemble. Use to add, outline, draft, revise, check or retarget one Section. Also opens as /haipipe-paper-section."
metadata:
  version: "0.26.0"
  last_updated: "2026-11-13"
  aliases: [haipipe-paper-section]
  folder_owner: canonical
  legacy_page_type: section
  page_ruling: none
  group-token: "t0N_<title> | t2N_<title> (legacy S-<desk>-Main-<Title> | S-<desk>-Appendix-<Title>)"
  outline:
    mode: resolved
    source: "2_theme/paper/venue/bank/1-QBv-desks/QBv*/QBv*.md"
    resolver: "cli/resolve-structure.py <QBv page> <section page> · prints structure-source (the bound QBv FILE) and structure-division (its `§<n> Sec-<n>-<Kind>` row)"
    marker: "section-page-template: 1"
    fallback: "paper/haipipe-paper-draft/ref/generic-template.md"
    shape: "current Story Section Narrative row overlaid on the resolved venue Sec- division or the explicit generic fallback"
---

# /haipipe-paper-draft · one paper Section as a draft Task

> **Working a Section follows JL's method** (261115): the structure loop, the draft loop and evidence beside them, [`ref/section-method.md`](ref/section-method.md); each step is a must-check row (haipipe-paper M-E01 to M-E09).

A paper Section is a draft Task (b32_draft s03, s41-D06; JL 261019: "we have the paper to combine the evidence and
draft together to make a draft task"). The base gives every theme the same three folders, one writer each; the paper
adds its rules to two of them:

```text
base (every theme)      paper adds                  one Section Task
haipipe-draft      ─▶   haipipe-paper-draft    ─┐   tNN_<section>/
haipipe-evidence   ─▶   haipipe-paper-evidence ─┼─▶ ├── draft/      plan and sentences (this skill)
haipipe-display    ─▶   (in paper-evidence)    ─┘   └── evidence/   cards (haipipe-paper-evidence); a display is
                                                                    its Board Task's, bound by `cited-in:`
```

Was `haipipe-paper-section` until 261019; that name is an alias, and a face's `page-type: section` resolves here
through `legacy_page_type: section` above.

> ⛔ **Generated files: never modify them directly; change the code that writes them (or its source), then rerun it** (hard rule, JL 260928; AGENTS.md rule 6). Here that means the Section's `delivery/latex/` and `delivery/word/` files: fix the Page, its Draft or the exporter, then rebuild.

For a Section Page update, load `haipipe-draft`, `haipipe-draft-workflow`, the
current Run Workflow/Spec owner, `haipipe-paper-workflow`, this PageType and
its relevant references in the shared set order. Read
`../haipipe-paper/ref/page-integration.md` when planning a Run or release.
Reading a proposed handoff alone allocates no Run.

Declare `task-type: draft`, `page-type: section` and `section_kind: <kind>`.
Reading this contract for a prospective Story handoff does not start a Run.
Proposed bindings may remain unresolved until the relevant owner supplies them;
do not invent Page paths, accepted Results, or a release to complete a proposal.

## Paper ownership and entry

This skill owns the Paper Section Page and its `page-type: section` contract below. Enter through gate G3: one draft
Task per Section row of its version face's `## Narrative` (that venue's layout; the Story's § 8 holds the shared
claims and no Section rows, and only an older Board still keeps Section rows there). The person signs the version's
Narrative first (`page.py sign-narrative`), then releases each row independently (the Release a Section card). A new Section is made by `haipipe-paper/scripts/paper_ladder.py task <version>
t0N_<title>` (the Add a Section card), with its reader-contract header; its `reports/` come with their first item.
Gate G4 marks the assembled build SUBMISSION-READY versus DRAFT; assemble
is a separately commissioned build, and runs anytime from `delivery/` on the Story's
compile-order block. `haipipe-paper-workflow` holds the full gate assertions; this block only
binds the Page owner. The page itself always runs through `/haipipe-draft` and
`haipipe-draft-workflow` (CONTEXT → OUTLINE ⇄ EVIDENCE → CONTENT → CHECK),
never a private lifecycle.

## 📄 Grain and authority

One Section Page owns one reader-ordered manuscript or appendix unit. Main and
appendix Sections use the same contract; numbering and venue treatment may
differ.

Authority order:

```text
Story Seed divisions (§1–§5: identity and evidence boundaries)
  → Story § 8, the shared narrative (title, story, claims C1..Cn and their numbers)
  → selected Venue rules
  → the version face's ## Narrative, signed (the layout: claims to displays, this Section's row)
  → venue × section-kind structure/template
  → landed Page-local evidence
  → current prose
```

Prose never outranks a changed § 8 claim, a changed Section row or a binding desk rule. A Section quotes the
claims by id from § 8; neither the version face nor the Section copies their wording.

## 📏 Requirement (b16 s13, JL 261007)

Description › Requirement is its own tab: the rules the Section is written to and the rubric it is judged by, read
from three places and copied from none. Read [`ref/requirement.md`](ref/requirement.md).

## 🚪 Opening stays with the reader

The rendered Section Opening is exactly one paragraph: the question and the
minimum orientation needed to enter the manuscript unit. It has no reader
drawer. Page-owned prose rules live in
`draft/records/<stem>-requirement.md` as authored `W<n>` records with `Rule`,
`Applies`, and `Source`, after the generated venue `V<n>` block. The Outline
workbench exposes both through one `📏 Requirement` lens for CONTEXT, OUTLINE,
CONTENT, and CHECK. A Section Page carries no `### Writing Style` block.
Post-paragraph notes and `## Stage Contract` remain source-side and do not
render on the manuscript review surface. This keeps writer instructions out
of the paper reading path without deleting their authority.

## 🏠 Runtime home (0.4.0)

```text
Paper-<Slug>/
└── jNN_writing_v<MMDD>_<desk>/   one version (j11 first): one send to one venue, named for the day it is sent (0.10.0)
    ├── t00_abstract/        the Abstract
    ├── t0N_<title>/         a Main Section, in reading order (t01-t19) · N = the H1's §N
    ├── t2N_<title>/         an Appendix Section, A = t21 (t20-t29) · its letter = the H1's Appendix L
    ├── t3N_<title>/         a letter (t30-t39): t31_cover-letter · t32_response; section_kind: letter
    └── reports/qNN_<kind>-<MMDD>/   a comments batch: a report of type comments, never a Task
```

Each Section Task holds its face, the Page workflow's `draft/`, `runs/` and `results/`, and its own
`reports/qNN_<topic>/` (the discussion questions kept while it is changed, each a row in the face's
`## Questions`, shown in Report › Questions as Question │ Work │ Report; b16 s13, JL 261007). It keeps no
`studio/` and no `delivery/` (b10 s09-D01, s03-D06; JL 261011: "for the section, we will do not have the
related studio and delivery"): its drawings (the logic by hand, the Section map, the reading of the Section as
last sent) are Board topics,
`sNN-<topic>/`, and its built output is the Board's `delivery/jNN_<version>/tNN_<section>/`.

A Section is a Task of its version, named by series (JL 261007: "no more S-xxx"): the number band says the
part (Main, Appendix, letters), the title is lowercase-kebab and says the page job, and the version folder
carries the desk. The older layout, `Ba-<desk>-Main/S-<desk>-Main-<N>-<Title>`, `Bb-<desk>-Appendix/
S-<desk>-Appendix-<L>-<Title>` and `Bc-<desk>-Round/RD<NN>-<event>`, stays readable;
`haipipe-paper/scripts/carry_over/rename_tasks.py` moves a version to the series names once, with a record. The version
face's compile-order block supplies manuscript order; `board.md` is the Page roster.
A Section is never renamed merely because another
section is inserted: the new one takes a free number in its band, and the version's compile order, not the
number, decides where it prints.

## ✂️ No semicolons in the paper's sentences (JL 261104)

Every Section, the Abstract, the Supplement and the letters use plain sentences, never a semicolon (JL 261104: "don't
use ';' make them as the normal sentences"). A sentence with three findings joined by semicolons becomes three
sentences, each with its own Bullet in `## 1 · Structure`. Write `(1.57-4.73) (Figure 2)`, not `(1.57-4.73; Figure 2)`.
Only what the journal fixes keeps them: citations in parentheses and the back matter's affiliation list. Check with
`haipipe-draft-review` `cli/anti_slop.py` (rule `semicolon`) before a build. Statistics follow what the venue's published papers print, read from its examples in the venue bank, never a style manual from memory (MISQ: `(SE = 1.07, 95% CI [0.69, 4.90], p = 0.009)`, JL 261104: "check other MISQ paper examples for this"). Otherwise statistics inside one parenthesis keep theirs, `(SE = 1.07; 95 percent CI, 0.69 to 4.90; p = 0.009)` (JL 261104: "could we use ';' here? as long as it is not the sentence").

No transition set off by commas either (JL 261104: "don't use things like ' , however ,', Try to make a sentence to be smooth"): `, however,`, `, therefore,` and their kin become a sentence that flows (rule `parenthetical-transition`).

The Introduction says its hypotheses in words, with no `H1` or `H2` label; the labels start where the theory section states them (JL 261104: "why we have the H1 here?").

## 📏 Paragraphs of 4 to 7 sentences (JL 261112)

A paragraph of a paper Section holds 4 to 7 sentences (JL 261112: "abstract should be okay. for other, unless having
good reason, we might make sure they are between 4~7 sentences"). The count is read from the paragraph heading
`### C<n>.P<m> · <name> · s<a> to s<b>` (b - a + 1), else from the Bullets (`- B<n> · ...`) under it. Exempt: the
Abstract (section_kind `abstract` or `summary`), appendix, supplement and Extended Data legends, letters and
responses, and a P0 title paragraph. A good reason is written as a `reason: <why>` line under the paragraph heading;
the paragraph is then accepted and shown muted, not as an error.

To fix one out of range: split a long paragraph at its natural turn. Join parallel sentences with "and" or "while",
never a semicolon. Add a framing sentence only when a split leaves 3. Change § 1 and § 3 in one edit, remap the
evidence items' targets, then run `page.py adopt --relayout`, `page.py export` and `page.py health`. The check is
`page.py health` row `paragraph` (WARN while writing, FAIL with `--final`), read by haipipe-draft
`src/paragraph_length.py`; haipipe-paper `scripts/paper_check.py` row W7 and `cli/anti_slop.py` finding
`paragraph-length` use the same range.

## 🏷️ Titles read like the text (JL 261112)

Part titles (C<n>), paragraph titles (C<n>.P<m>), plan Bullet labels, arcs and Narrative reader questions are
academic and understandable on the first read. They show on the Plan map and the Structure view, so they are read
like the text (JL 261112, on "Here we measure what scale buys for each use": "I don't know why here we use the word
of 'buy', you should call the subagent to review them to make sure they are academic and human understandable").
A blind reviewer subagent, never the writer, scores each title 1 to 10 on academic register, first-read
understanding, and naming what the paragraph is about. A title under 8 is rewritten, and the rewrite goes to the
§ 1 and § 3 headings together.

No metaphor or casual verb in a title or label: buy, bought, pay, paid, pays off, win, land, lands and their kin.
Name the measured quantity instead ("how error changes with scale for each task"). The check is `cli/anti_slop.py`
rule `title-metaphor` (category title), which reads heading lines, `arc:` lines and `[Label]` bullet labels, never
body prose; `in-group-shorthand` reads the same lines, and `money-metaphor` reads the prose.

## 📝 Writing patterns found on ScalingGlucose (261111-261112)

Each came from JL on Paper-ScalingGlucose-NatSeries2026, in the shape of a Board's `writing-patterns.md`: the
pattern, JL's words, our sentence, the fix, and the check that holds it where one can.

1. **Paragraphs of 4 to 7 sentences.** JL: "unless having good reason, we might make sure they are between 4~7
   sentences". Ours: Introduction P3 had 10, P5 had 13. Fix: split at the natural turn (10 into 4 + 6, 13 into
   6 + 6); the Abstract is exempt, and a `reason:` line under the heading accepts an exception (§ Paragraphs of 4
   to 7 sentences). Check: `page.py health` row `paragraph`, checklist W7, anti_slop `paragraph-length`.
2. **Titles reviewed blind.** JL: "you should call the subagent to review them to make sure they are academic and
   human understandable". Ours: 50 of 80 titles rewritten after review. Fix: a blind reviewer scores each title,
   label, arc and reader question; under 8 is rewritten in § 1 and § 3 together (§ Titles read like the text).
3. **No money metaphors.** JL: "I don't know why here we use the word of 'buy'". Ours: "Here we measure what scale
   buys for each use". Fix: name the measured quantity, "where scale reduces error", "how scale changes error for
   each task". Check: anti_slop `title-metaphor` (titles, labels, arcs) and `money-metaphor` (prose; a literal paid
   claim is not flagged).
4. **No in-group shorthand in titles.** Ours: "rolled forward", "head", "route", "grid", "roadmap", "use". Fix:
   "recursive rollout", "linear head on the frozen model", "the way data were added", "model sizes and
   configurations", "study design", "downstream task". Check: anti_slop `in-group-shorthand` (titles only).
5. **The research questions stated together.** JL: "where are the two questions? i didn't see it." Fix: ask them
   as questions with "?", one right after the other ("First, …? Second, …?"), never split by other sentences.
   No automatic check; the cold read looks for it.
6. **No post-hoc "We expected …" in the Introduction.** JL: "do we really have evidence for this?" Ours: an
   `[Expect]` Bullet with `Evidence: none`. Fix: ask the question, give the known prior result with its citation,
   leave the answer to the Results. Check: `page.py health` row `expect` (an Introduction's `[Expect]` Bullet whose
   Evidence line says none).
7. **The title paragraph holds the title.** JL: "could you put the title here?" Ours: C1.P0's Bullet read "The
   paper's title." Fix: write the paper's title in the `[Title]` Bullet. Check: `page.py health` row `title`.
8. **The whole paper's structure before a Section's plan.** The version's `## Narrative` is signed (`page.py
   sign-narrative`) and shown in Report › Structure beside the Board Story § 8 (the shared title, story and
   claims); a Section's plan follows its row. Check: `page.py health` rows `narrative` and `row`.
9. **Examples as one drawing per Section.** Each example paper is one area of the examples drawing (its screenshot,
   then its logic as a mind map), drawn by `excalidraw-read ref/section_screens.py draw <topic>` and read beside
   our own plan in Report › Structure (frame jump per paper).

## 🧑‍🤝‍🧑 Co-authors' patterns, every sentence, and the easier-to-read check (JL 261110)

JL 261110: "will you add it and update it to the /haipipe-paper?"; "ask the agent to read each sentences to see
whether it is easier to understand". When co-authors return a round (a Word file pulled by `word_round.py pull`,
their comments, a meeting), the paper keeps what they want and checks every sentence against it:

1. **The patterns live on the Board**: `<Board>/writing-patterns.md`, numbered `### N. <pattern>` with their own
   words, our sentence, theirs, the fix and its support; the Writing view shows it as "Writing patterns to avoid".
   The generic tells are `haipipe-draft-review` `ref/ai-tells.md` § 5; this file holds the paper's own.
2. **Their text is theirs**: a sentence that carries a co-author's tracked insertion is never rewritten; it gets a
   Review card with a suggestion. Their own sentences keep their register (a semicolon included); our rewrites still
   follow the house rules: no semicolons, no transition set off by commas, no longer than the original. Run
   `haipipe-draft-review` `cli/anti_slop.py audit` on the rewrites, before the easier-to-read check (JL 261110:
   the first round's kept rewrites scored worse than the originals on it, 26 against 19, and ran 9% longer).
3. **Every paragraph, then every sentence, is reviewed** (JL 261115: "review the paragraph level logics, to check
   whether the logic is correct or not"). First one blind reviewer per Section reads each paragraph as an argument
   (`haipipe-draft-review` `ref/paragraph-logic.md`: order with no A-B-A return, every conclusion resting on named
   sentences, no claim wider than its findings, no missing step); a move or a missing step is a Section question the
   person signs before any sentence changes. Then one blind reviewer per Section (never the writer), reading the round's newest
   text, scores each sentence 1 to 10 against `ai-tells.md` § 5, the Board's patterns and the comments in that
   Section; under 8 gets a rewrite that keeps every number, citation and claim. A round is a Job on the Board, not a
   `reports/` folder (JL 261110: "we will no long using the reports/ plesae use the job or studio"):
   `jNN_review_<who>_v<MMDD>/` (face `for: <writing Job>`), its Tasks `t01_sentence_review` (the comments as
   received in `result/feedback/`, the reviews in `result/review/review-<section>.md`), `t02_readability_check`,
   `t03_paragraph_logic` (`result/logic-<section>.md`, run before the sentence review although numbered after it,
   since it was added later) and `t04_tracked_word` (a round made before 261115 may hold it as `t03_tracked_word`). A Job named with "review" is never read as a writing version.
4. **The easier-to-read check**: before a rewrite becomes a Revise card's default, a fresh reader (not the
   reviewer, not the writer) reads it in place: the sentence before, then the original and the rewrite in random
   order as A and B, then the sentence after. It answers two questions per pair: which one is easier to
   understand on a first read, and do both say the same thing (numbers, citations, claim strength). A rewrite
   that is not easier, or that changes the meaning, is not proposed as written: it goes back to the reviewer, or the
   original stays. The pairs, the readers' verdicts, the key and the unblinded verdict per sentence are
   `t02_readability_check`'s Result.
5. **Back to the co-authors as tracked changes**: accepted cards are adopted into the Section, and the same edits
   go onto a copy of the co-authors' own latest file as tracked changes by the person who answers them
   (`excalidraw-draft/ref/track_changes.py` `write_tracked`): their comments and tracked changes stay. The edits are
   `t04_tracked_word/scripts/edits.yaml` (find, new, why), its Run writes `delivery/<writing Job>/word-tracked/`, the
   send's third paper beside the PDF and the Word file (JL 261110: "the Word-Change-Track, which is based on the
   previous change tracks from professors and you add the changes as well"). It is written locally;
   `word_round.py push` sends it only on the person's word.

## 🏷 The Abstract carries the title (JL 261111)

JL 261111: "the abstract should contains the title"; "you will have C1.P0 for S0 ... C1.P0 Title". An Abstract's Draft
opens with its own paragraph `### C1.P0 · Title · s0` holding one Bullet, `- B0 · s0 · <the paper's title>.`, and the
abstract proper follows as `### C1.P1 · <subject> · s1 to s<n>`. The title paragraph prints as its own line above the
abstract; the venue's word limit is counted on C1.P1 (state both counts on the Draft's `form:` line). Because s0 states
the claim, the last sentence of C1.P1 does not restate the title: it closes on what the reader should do or what it
means (JL 261111 on "We conclude that scaling laws are not universal …": "This sentence is kind of akward"; it became
"Builders should test scale task by task rather than assume one law."). The paper-wide title in
`delivery/<job>/paper-build.toml` and the version face's **Title:** line carry the same words; the version face is the
Story owner's to change. P0 and B0 are real numbers to `src/plan_shape.py` since 261111 (they were read as "no number"
and became P1 and B1).

## 🗣 Showing prose changes in a reply (JL 261113)

A reply never shows proposed or changed Draft prose as a paragraph (a quote, an indented block, a fenced
passage). JL 261113: "never return the things like this … Make it the same to the index in the UI, sentence by
sentence, and also show what changes you made compared to previous. You can report paragraph by paragraph."
Report it paragraph by paragraph, one line per sentence with the address the workbench shows (`C<n>.P<m> ·
<title>`, then `B<k> · s<n>` as in § 3 of the Draft), a mark (✅ kept, ✏️ changed, ➕ new, ➖ cut, ↪ moved) and,
for a changed sentence, its before and after in full, against a named version. The format and its example are
`response-format` § Prose changes: sentence by sentence, by address. The revise record (`draft/records/<stem>-revise.md`)
names each sentence by the same address, so chat, record and page agree.

## 📚 Examples first: a must (JL 261022; 261104)

**⛔ The first thing a session does on a Section, the Abstract or a letter, before Plan and before any word.** The Task's
📚 Examples card must show real readings. If it says "No example papers yet", make them, then continue. A session is
not finished, and never says "finished", "done" or "ready", while `page.py health --final <Task>` fails its `0 ·
Examples` row (JL 261104: "This is a must to do when you call the task for the /haipipe-paper-draft"; "update the
checklist and must to do before saying such a task session is finished").

Examples show **how other people write this part**: moves, order, lengths, how a number is reported. They are not related
work: a summary of what those studies found is not an example (JL 261104: "I don't know why you want to just describe
the related studies here. I think we should check how other people writing it"). A paper is chosen because it is the
**same article type in the same journal**; closeness of topic is the second test. A Research Letter is read against
Research Letters, never Original Investigations, and an article whose type is not confirmed on its page does not count.
A letter's Sections each get their own topic and face, and may read the same papers.

**What "ready" looks like (JL 261104: "for the exmaples here, we just want to have the screenshot intdouction to check"):**

| Step | Do | Tool |
|---|---|---|
| 1 Topic | `sNN-<task>-<venue>-examples` beside the Jobs, its face (For, Delivery type, Covers, Excluded, Topic) and its `related:` yaml filled; its first line names `<job>/<task>` | `/haipipe-studio` `new_topic.py topic` |
| 2 Screenshots | one picture per paper of **that Section and nothing else**, whole and readable: `reads/pNN-<author><year>/shots/section.jpg`; `reading.yaml` beside it with its size and moves | `read_paper.py paras` from the PDF; the article's page if no PDF is free |
| 3 Drawing | the screenshots one under the other, the shared pattern on top, where ours departs in red. No logic chains, no reference cards | `excalidraw-read ref/section_screens.py draw <topic>` |
| 4 The card | Work › Plan › 📚 Examples shows the drawing **embedded**; open the page and look | the Task's page |
| 5 The face | the Task's `examples:` names the topic | `page.py health`, `paper_check.py` W6 |

Counts or a list of papers without the screenshots is not ready.


A Section, the Abstract or a letter is written after reading how 3 to 4 published papers of the same venue write the
same part, never before: a Studio topic `sNN-<task>-<venue>-examples` (`/excalidraw read`; two papers close to the
topic, two the author guide quotes), named by the Section canvas's `examples:` line, so the canvas draws ours beside
them. The writer follows their moves and lengths and names each departure (haipipe-draft-writing `ref/writing.md` § 0).
JL 261022: "你应该先找 example，看看别人是怎么写 abstract 的，然后再看怎么写".

After the Examples, a Section starts at 1 · Plan and stays there until the person signs (JL 261111): the structure
versions are proposed against the examples and the Section's `## Narrative` row, the person's word is written by
`page.py sign --quote`, and Write, Evidence and Revise refuse an unsigned plan (haipipe-draft § The Plan gate). The
sign keeps the Section's Narrative row as text in `draft/records/<stem>-sign.md`; when that row changes after the
sign, `page.py health` gives `row` and the Section goes back to Plan.
The version's `## Narrative` is signed before that (`page.py sign-narrative <version> --quote "…"` writes
`narrative-approved:` and `story-at-sign:` on the version face and keeps the Story's § 8 as text in
`<version>/records/narrative-sign.md`). Health's `narrative` row warns while the version's Narrative is unsigned or
the Story's § 8 has changed since; `row` and `narrative` WARN, and FAIL with `--final`. Whole-paper structure choices
are the version's, seen in the version Job's Report › Structure view beside the Story's § 8 (workbench-paper); the
structure is a view, never a Task.

**Examples: one source, shown at two levels (JL 261111: "the examples to be shared across the job level and each
draft task").** Example papers belong to the version, because they are chosen by its venue. Read the same papers for
every Section of a version, each paper under the same `reads/pNN-<author><year>/` name in each Section's examples
topic. The Task's 📚 Examples card shows its own Section, as above. The version Job's Structure view adds a third
panel, Examples: each example paper's section layout beside our paper map, joined across the Sections' examples
topics by paper (`pNN-<author><year>`). Nothing is copied; a paper read for one Section only shows that one Section.

## ⚙️ Paper Section Run profile

Read [`../haipipe-paper/ref/run-naming.md`](../haipipe-paper/ref/run-naming.md)
and the shared Page Run names. New local Evidence uses full names such as
`run-citation-<slug>` or `run-value-<slug>`.
The Page owns the Evidence Item; the selected Task/Display worker does not
change that owner. Independent Supporting Runs keep their native Task or
Discovery identity and full path.

Human interaction uses a `run-structure-…` Run for SHAPE + SURVEY, then the
selected `run-section-…` or `run-paragraph-…` session. Feedback is a Step; same-target
reopening is a Version. Record the semantic `page:` and `paper_lane:` alongside
the native receipt. Older short names are retired; a reused Result keeps its
exact original path, and its owner and receipt are verified before reuse. Evidence acceptance never replaces human writing
acceptance. The Paper Workflow's `structure/write/evidence/deliver` Specs bind
these native Runs, without a wrapper Section Run.

**Where the words live (0.8.4 · JL 260907)**: on this page. The Section Page
compiles its own deliverable through the page-level delivery workbench,
`delivery/latex/<page>-master.tex` compiled to `<page>.pdf`, with its Bib at `selected-bibliography/<page>.bib`,
wrapping the body fragment `delivery/latex/<page>.tex` that the paper build
`\input`s; its `\includegraphics` paths resolve to its own accepted display units
(`results/<re-run>/payload/Display<n>-<slug>/assets/figure.pdf`; the stable Page id
owns the unit independently of printed section order; `S-Display-*`, `<PageID>-Display-*` and `Sec<N>-Display-*` are
retired, JL 260908) and its citation keys to
its own `selected-bibliography/<page>.bib`. The paper's `delivery/latex/` is regenerated FROM these
files by `haipipe-paper-assemble`, never the other way round: a correction goes
into this page and the paper folder is rebuilt whole. The old desk room
(`<N>-<desk><year>/sections/*.tex`) is not a current source of record.

**Mechanical assembly milestone**: this Page can supply a fragment to a draft
build when three things exist: the current outline table is explicitly approved
(`draft/<page>-draft-v*.md`, ticked), every display unit has its
`preview.pdf`, and the page PDF compiles under `delivery/latex/`. A page
missing any of the three is not ready, and the paper build says so.
Those files do not make the Section DONE. Only current Page CHECK closure under
the Section contract and accepted evidence bindings closes it; paper-level G4
and the human submission decision remain separate. Follow
`haipipe-paper-assemble` for exact-version admission and manifest checks.

## 📥 Required contract block

Record these fields in the Page before drafting:

```text
story-row           <version> ## Narrative / <stem> (an older Board: Story<Letter>-<desk>-<idea-slug> §8 / <section-id>
                    + the Story version); resolve the actual row
section_kind        abstract · introduction · literature-review · theory ·
                    methods · results · discussion · conclusion · appendix ·
                    venue-specific kind · UNDERSCORE, matching the header key
reader-question     the one question this Section answers
entry-state         what the reader already believes/knows
exit-state          what must be established on exit
claim-ids           exact Story claim / E ids from the row
venue-allocation    binding desk rules + observed pack guidance, distinguished
structure-source    the bound QBv page FILE, e.g. `paper/venue/bank/1-QBv-desks/
                    QBv1-misq/QBv1-misq.md`, or `ref/generic-template.md`; a
                    path, because `src/plan_shape.py` resolves it on disk
structure-division  the row inside it: `§8 Sec-4-Results` (EXACT), `§7
                    Sec-3-Methods · shared with another named Section` (SHARED), or the reason
                    the fallback was taken (ABSENT BY DESIGN · MISSING)
evidence-allowlist  typed Evidence Item ids and accepted local Result ids
transition-in/out   required joins to neighboring Sections
```

If the Section Narrative row is missing or stale, CONTEXT records its exact
source and returns `HOLD` to `haipipe-paper-story`, the owner of the Story page,
its § 8 shared narrative and the version face's `## Narrative` rows. If Venue
authority is missing or stale, it returns `HOLD` to
`haipipe-paper-venue`, the owning QBv bank Page Type; Venue is a shared reference library. After the exact owner repairs and versions the source, the
Section resumes at CONTEXT/PREPARE. Section work never repairs upstream
Story or Venue policy itself.

## 🧱 Content outline

**Outline mode (also in this file's frontmatter, which the Skill tool strips):**
`mode: resolved` · source = the bound QBv desk division (`structure-source:` +
`structure-division:`, via `cli/resolve-structure.py`) · fallback =
`ref/generic-template.md` · one `## C<n>` per Content division of the page, so a
flat section is `C1` with one paragraph group per move · one bullet per
sentence slot.

Resolve paragraph or move divisions from the QBv Venue Page named by the
governing Story §8 row's `target` column. **Address the division by grep, never by a
remembered name or number** (0.5.0):

```bash
grep -n '^### [0-9]* · Sec-' <venue-bank>/QBv<n>-<desk>/QBv<n>-<desk>.md
```

The heading is `### <n> · Sec-<n>-<Kind>: <tagline>`, so the token is followed
by a colon and prose; match the token, never the whole line. Its NUMBER moves
between desks: MISQ's abstract is §4, Nature Communications' is §3, and PNAS §3
is Sec-0-Significance with the abstract at §4. Cite the whole address in
`structure-source`, both the number and the `Sec-` token, so a re-read can
prove it.

**`cli/resolve-structure.py` does this and prints the verdict**, so no page has
to trust a remembered mapping:

```bash
python3 <skill>/cli/resolve-structure.py <QBv page>.md <section page>.md
python3 <skill>/cli/resolve-structure.py <QBv page>.md --all <group>/   # a board
```

### The kind-to-token map · not derivable by casing

Two of the nine differ from their kind by more than capitalization, which is
why an agent must read this table and never transform the string itself:

```text
section_kind        Sec- token              note
────────────────────────────────────────────────────────────────────────────
abstract            Sec-0-Abstract
introduction        Sec-1-Introduction
literature-review   Sec-2-Related-Work      ⚠️ different word · absent at MISQ,
                                            present at QBv9/10/12
theory              Sec-2-Theory            shares the number 2 with
                                            Related-Work across desks
methods             Sec-3-Methods
results             Sec-4-Results
discussion          Sec-5-Discussion
conclusion          Sec-6-Conclusion
appendix            Sec-A-Appendix          ⚠️ letter, not a digit
```

Raw pack `style.md` files and stage-era playbook material stay informative: they
may feed a typed PACK OBSERVATION on the QBv page, but they may not become
`structure-source`.

### The kind-to-division map · four relations, not one

`section_kind` does not equal a `Sec-` token, and the mismatch has four
different remedies. Naming only one of them is what made every Section fall
silently to the fallback:

```text
relation            what it looks like                     what to do
──────────────────────────────────────────────────────────────────────────────
EXACT               one kind, one Sec- division            resolve · cite the
                    abstract → Sec-0-Abstract              address
SHARED              one division serves several Pages      resolve · SPLIT the
                    methods → Sec-3-Methods (2 Pages)      division's word and
                    appendix → Sec-A-Appendix (6 Pages)    move budget on the
                                                           Story §8 row, never
                                                           give each Page the
                                                           whole budget
ABSENT BY DESIGN    the desk HAS no such unit and the      fallback · record the
                    paper keeps the section anyway         DEVIATION on the
                    literature-review at MISQ              Story §8 row · do NOT
                                                           raise a QBv gap
MISSING             the desk should have the division      fallback · raise the
                    but the page has not been written      gap on the QBv page
                    8 of 17 desks carry zero Sec- rows     · the desk owes it
```

**The ABSENT BY DESIGN row is the one 0.4.0 lacked.** MISQ publishes no
related-work unit, and a paper may still keep one as a deliberate deviation a
person ruled. Raising that as a gap tells the venue bank to invent a division
the desk does not have, which corrupts a consumer-neutral asset to suit one
paper. The deviation belongs on the Story's §8 row, where the target decision lives.

**Eight desks resolve to nothing today** (QBv5-jama, QBv7-jama-network-open,
QBv8-npj-digital-medicine, QBv9 partially, QBv11-nature-human-behaviour,
QBv14-diabetes-care, QBv15-grant, QBv16-patent, QBv17-wise carry zero `Sec-`
divisions). For those, `mode: resolved` is aspirational: every Section takes the
generic fallback and the gap is real. Say so in `structure-source` rather than
letting the page read as venue-resolved.

Each Content division states:

```text
reader move
claim ids advanced
evidence/citation/value/display bindings
expected prose or display placement
transition to the next move
known limitation or unresolved need
```

**A Section quotes, it never computes (0.20.0, JL 261110).** Every number in its prose is a value id of the value
Job, bound by id, and the Section names the value Run it quotes (its VALUE card or binding says the Run, never "the
newest"). A number with no id gets one in the value Job first; a binding goes stale when an id it quotes moves or leaves
in a newer value Run, and stays current when that Run only adds ids (haipipe-paper-evidence, The chain; `chain_check.py` says where it breaks).

**The plan is a list of sentence slots (0.5.3, JL 260831).** One bullet is one
sentence slot, `s<n> · <what the sentence does>` in 4 to 11 plain words;
paragraphs group by move (`### C2.P1 · Problem and question · s1 to s3`); a
finding carries its claim id plus a word (`s6 · C1: <the number and its unit>,
comparison owed`); one `Cut:` bullet names what leaves the section and where it
goes; a Note is one line and never the drafted sentence, which lives on the
page. The approved specimen is quoted in `workbench-task-draft` §✂️.

**Structure and Draft move together (JL 261102: "when you update the draft, you should also udpate teh structure as
well")**. A Draft Markdown's `## 1 · Structure` is the plan of its `## 3 · Draft`, so every edit to the sentences
makes the same change to the plan in that edit: a sentence added or cut adds or cuts its Bullet (`- B<k> · s<n> ·
[Role] what it does`, with its `Evidence:` line), a sentence moved moves its Bullet, a paragraph added, split, merged
or renamed changes its `### C<n>.P<m> · <title> · s<a> to s<b>` heading in sections 1, 2 and 3 and its entry in the
Structure Overview, and the S numbers and spans are renumbered to match. A new structure is a new draft version
(`draft-v<G>.<S+1>`, the older one moved to `draft/previous/`), never a section 3 rewritten under the old plan; its
Evidence Items and the face's `evidence-allowlist:` follow their sentences. `page.py health <Task>` checks it
(`structure`: `plan_layout.structure_draft_mismatches`, the paragraphs, titles, sentences and Overview spans of
sections 1 and 3) and fails until both agree.

## 🏷 Reader-facing subsection titles

During SHAPE and CONTENT revision, name each subsection for the substantive
subject or relationship its paragraphs develop. A reader scanning the titles
should recognize the actors, constructs, decisions, or contexts being studied
without knowing the planning vocabulary.

- Prefer concrete, concise noun phrases with parallel grammatical form across
  peer subsections. Preserve defined construct names and the venue's casing;
  do not shorten a title by changing the construct or making a stronger claim.
- Distinguish a reader-facing title from a paragraph job. `Resolve the rivalry`
  describes the writer's task; `Wait Times and Patient
  Satisfaction` names the subject. `Boundary tests and integrated model`
  is too generic when the actual subject is how an effect varies across clinical contexts.
  These examples illustrate the distinction, not a required outline or phrase list.
- Check title-to-body fit: the title covers the whole subsection, distinguishes
  it from its neighbors, and promises no unmeasured mediation, demonstrated
  causality, or material absent from its paragraphs. `Boundary`, `model`, and
  `competing predictions` are legitimate terms when they identify the actual
  subject; they are not banned words.
- Read the ordered titles alone, then inspect the corresponding paragraphs.
  Revise a vague title; do not reorganize an approved argument merely to fit
  a more attractive label. A genuine scope/order/claim change returns to SHAPE.
- For an authorized title-only clarification, synchronize the current Outline
  division, Page Content heading, and matching Aim heading; regenerate the
  Board and declared delivery and inspect both. Preserve historical plans and
  completed Run inputs. Apply the plan grammar's version rule: a mechanical
  relabeling with unchanged scope, order, Bullets, and evidence need not consume
  a version; record the rationale instead of disguising a Shape change as wording.

## 🃏 Evidence is haipipe-paper-evidence's

What backs a sentence (a citation, a value, a display) is made in the Board's evidence Jobs and bound in the
Section's `evidence/` (a display by its Task's `cited-in:`, JL 261113), under
`haipipe-paper-evidence` on top of the base `haipipe-evidence` and `haipipe-display` (moved there 261019). This skill
writes the words and keeps every consequential sentence one of three things, which the evidence skill checks:

- supported by an evidence card (or, on an older Page, a typed Evidence Item and its accepted local Result);
- explicitly framed as interpretation and bounded by its evidence;
- visibly marked as an open need that prevents closure.

## 🔁 Retargeting

On a venue change:

1. Bind the Section to the new Story Section Narrative row.
2. Re-resolve venue × kind structure and hard constraints.
3. Preserve Evidence Item/Result ids whose meaning and scope remain valid.
4. Return changed item meaning to OUTLINE/SHAPE, changed Run design to
   OUTLINE/SURVEY, and stale Results to EVIDENCE/LAND.
5. Run CONTENT/WRITE and CHECK the new built version.

## 🧾 Reworking a sent Section (0.12.0)

When a version follows a sent one whose review came back (its comments report, `haipipe-paper-comments`, holds
the Review Items), each Section first reads itself as sent, before OUTLINE/SHAPE, so the person sees how much
changes and why (JL 261014: "How much we will chnage them ... could you use /excalidraw read to work on each of
the section, and make each section (main section) to be a sNN tNN from the new job ... we can put thing there to
discuss").

```text
sent PDF (its delivery) ─▶ sNN-tNN-<section>/reading.yaml ─▶ the drawing: how much changes ·
                           section · parts · key · a verdict          your call · one frame a subsection
                           and next per passage                       (pages left, short notes right)
                                      │
                                      ▼
face "How much changes" (every paragraph) ─▶ CONTEXT cites it ─▶ SHAPE: KEEP carried, REWRITE redone,
                                                                  MOVE sent on, CUT never back
```

1. **One Board topic per Main Section**, `sNN-tNN-<section>/` beside the Jobs, tagged with the sent version
   (`draft-v<MMDD>`) and the Task stem; its **Feeds:** names the new Task and the comments report.
2. **Its `reading.yaml`** (excalidraw-read 0.7.0) reads the sent PDF: `section:` with `name`, `pages`, `from`,
   `until`, `parts` (the subsection headings) and `key` (the count line); each passage's `comment` begins with
   `KEEP`, `REWRITE`, `CUT` or `MOVE`, its `link` goes to the Review Item that hits it (`how` begins with the
   point ids) or to `new-<task>`, and its `next` says in 10 words what the new Section does with it.
3. **Its face's How much changes table** gives every paragraph of the sent Section a row (`¶ · page · starts
   with · verdict · why`), then the count line and an estimate of the words that survive, said as an estimate.
4. **The new Section uses it.** CONTEXT cites the topic as a bounded related link; SHAPE carries a KEEP row as a
   slot, rewrites a REWRITE row, sends a MOVE row to the Section it names, and never brings a CUT row back.
5. **Routes agree.** Every Review Item a reading links lands on this Section in the comments report's `lands on`
   column; a missing route is fixed in the report, never only in the reading.

Worked example: Paper-TestToLearn-MS2026, S10 to S16, the sent `j01_v0429_mansci` read for `j02_v1007_mansci`:
107 rows, 13 KEEP · 47 REWRITE · 26 CUT · 21 MOVE.

## ✉️ A cover letter's words (JL 261104)

| Rule | What it means |
|---|---|
| One idea per sentence | a long results sentence becomes several; JL split one into 3 |
| "Why this journal" is about its editor and readers | who acts on the finding, the tension it raises, and a real paper the journal published (verified, from the paper's own references); never "our readers are the best audience" |
| A related earlier paper is named with its DOI | it is not uploaded unless the journal asks. JL: "I think we don't need to upload it with the submission" |
| The paper's own words for its evidence | no "validated" unless the paper says so |

The build fills the facts and runs the letter's checks (`haipipe-paper-assemble` § The cover letter lane); the final
read covers the letter too (§ The final read there).

## ✅ A complete paper draft Task

The base list is `haipipe-draft` `ref/page-checklist.md` § 6 (one file per step, checked by `page.py health`'s
`steps` row). A paper Section, Abstract or letter also needs these before it is called complete (JL 261102: "why dont
you make them to be complete?"):

| What | Done when | Where |
|---|---|---|
| The contract block | every field of § 📥 Required contract block is on the face, none left as `<…>` | the face |
| The Requirement | `W<n>` rules for the Section's own writing; the venue's `V<n>` when its desk has a division, else the reason in `structure-division:` | `draft/records/<stem>-requirement.md` |
| 📚 Examples ⛔ first | before Plan: `examples:` names the topic of 3 to 4 published papers of the same article type, each Section read whole with its moves and lengths and each departure of ours named, or says `examples: none · <reason>` (a cover letter: journals publish none) | the face, `page.py health`'s `0 · Examples` row |
| 1 · Plan signed | the version's `narrative-approved: ✅` first (`page.py sign-narrative`), then `approved: ✅ … · in chat: "…"` by `page.py sign`, before any § 3 sentence; health shows no `order`, `row` or `narrative` row | the Draft Markdown, `page.py health` |
| Evidence for every number | each number, citation and display a sentence uses has an item, and each `Evidence:` line in § 1 names it | `draft/<stem>-evidence-items.md` |
| Its own delivery | web, LaTeX and Word built under `delivery/<job>/<task>/` (`page.py export`); a letter's face says `delivery-builder: <the paper's build.py>`, so its LaTeX and Word lanes are the letter as uploaded (date, addressee, signature), never a Section print | the Delivery tab |
| Into the paper | a Section: its LaTeX fragment in the version's paper build; a letter: the cover letter lane (`[coverletter] task`) builds it and the portal packet carries it | `delivery/<writing Job>/` |
| Content is the latest draft | `content:` names the current draft (adopt, or `adopt --relayout` when paragraphs changed; never typed by hand); no Delivery tab shows the ⚠️ "This prints …" warning | the face, the Delivery tab |
| The final gate | `page.py health --final` shows no FAIL (the printed PDF holds every § 3 sentence); its only WARN rows are the person's steps | the reply, before the word "finished" |

## ✅ Closing checks

- Exactly one current Story Section Narrative row governs the Page.
- Reader entry and exit states match neighboring rows.
- Every claim and consequential sentence has inspectable support or an open
  need.
- Every citation key resolves; every value has provenance; every cited display
  names an accepted artifact version.
- Venue rules are distinguished from pack observations.
- The generated TeX/PDF/DOCX reflects the accepted Page version.
- CHECK, not prose completion, closes the Section.
- The must-check gate passes (haipipe-paper `ref/must-check.md`): no rule fails without its id and reason named.

`page_ruling: none` is explicit for the per-Section Page. CHECK may close one
unit when its Section contract and artifact-specific gates pass. Paper gate G4
is separate and non-circular: it waits until every mapped Section is closed,
then governs whether the assembled paper is SUBMISSION-READY and receives the
paper-level human decision.

## 📏 Measuring the form · `cli/section-stats.py`

A Section's word and paragraph budget comes from the resolved `Sec-` division's
Format values. `cli/section-stats.py` measures what the prose ACTUALLY is and
writes the dated `# --- form:begin (generated) ---` block the pages carry:

```bash
python3 <skill>/cli/section-stats.py <page>.md [--date=YYMMDD] [--sentences]
```

It reads only `## Content` prose under the paper dialect's rules: `###` opens a
subsection, `####` opens a paragraph, the `(…)` line under a `####` is that
paragraph's job and not prose, a `>` line is an apparatus lane, and a `[Q-…]`
bracket is stripped before counting. `--sentences` adds a per-sentence bar; keep
it off except on a one-paragraph unit such as an abstract.

**Never hand-edit a form block.** A form table is wrong the moment one sentence
changes, and a wrong one is worse than none because it reads as measured. The
board's `check.py` reports `generated-block-stale` when the block's date is
older than the page's newest Log row; regenerate, do not retype.

This variant owns `cli/resolve-structure.py`, `cli/section-stats.py` and
`ref/generic-template.md`, the
explicit fallback that keeps every Section kind executable while venue templates
are migrated one by one.
