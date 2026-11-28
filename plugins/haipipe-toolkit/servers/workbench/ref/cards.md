# Item cards: marks and cards on any item of a page

Every item a workbench page draws (a Draft sentence, a Research Question row, a Job, Task or Run row, a design, an
insight question or cell, a labeling rule or item) can carry marks after it, the way a Draft Lab sentence does. A click
on a mark opens that kind of card under the item. This file is the contract every workbench follows. The mockup the
design came from: example A to E of the "Marks Pop-Out" mockup (2026-11-14).

## 1. The principle

- Content lives only in Markdown. Cards are Markdown too, beside the page, keyed by the item's address.
- The website only renders. A click writes back to that Markdown through one shared writer; nothing is kept in a
  database, in the browser, or in a page's own JSON.
- People and AI write the same files in the same format. An agent's review is cards in the file, not a new view.

## 2. Which items carry marks

Only content a person reads and judges carries marks and cards; structure does not (JL 261114: "for some of the
session content, it is the structure, maybe we don't need the element emoji cards ... but for some text content, we
might want to add them").

A content item is a **Brick** (JL 261117): its types, its three places (file, cards, page), 📍 and its life are in
[`hai-paper/ref/bricks.md`](../../../skills/3_theme/paper/hai-paper/ref/bricks.md).

| Content: marks and cards | Structure: no marks of its own |
| --- | --- |
| a Draft sentence, the paper's question, a Research Question row | the list of Sections, a fold, a tab, a view bar |
| a design, a rule or goal, an idea | a file list, Skills, a breadcrumb, a rail |
| an insight question and its answer cell | a table of contents, a mind map of the ladder |
| a labeling rule and a labeled item | a section bar (it shows only the roll-up below) |
| a decision, a finding, a term, a written note | |
| a Job, Task or Run row in Plan + Results | |

- A Job, Task or Run row is content (JL 261116: "for the plan + results, we can make each BJTR as the sentence card"):
  after its state mark it carries 🙋 N (the questions waiting at it or below; its card is the question form itself,
  answered in place), ℹ️ N (things to know there) and its own 💬 📝 ✓. Its address is its place from the Block
  (`j02.t01.r05`) and its cards live in the Block's `records/`, so the Block, Job and Task pages show one thread.
  `servers/workbench/page/element_marks/ladder_cards.py` draws them.
- A left tab that holds content (a value table, a map, a question, a design) is content too: its marks sit after its
  name and its cards open at the top of its content on the right (`ui_parts._side_tabs(..., cards=(page, root,
  prefix))`, `tab_cards.py`). Its address is `<prefix>.<its name>` (`findings.values.Main-estimates`). Tabs that
  only switch views, files or skills pass no `cards`.
- A paragraph or a one-line list item of a page's own sections is content once it has an id: marks at its end, its
  cards under it (`paragraph_cards.py`). Its address is `<view>.<id>` (`findings.p32`); the id is written once by
  `/hai-work update` (`servers/workbench-work/paragraph_ids.py`), never by a click.
- Any other structure row that links to another page shows at most the orange roll-up of that page (🙋 N, 📝 N).
- When unsure, ask: would a person comment on these words, or change them? If yes, it is content.

## 3. Addresses

An address names one item inside the page that owns it.

| Item | Address | Comes from |
| --- | --- | --- |
| Draft Section, paragraph, sentence, plan bullet | `C1`, `C1.P2`, `C1.P2.s8`, `s8`, `B9` | Draft ids (never reused) |
| Ladder rows | `j02`, `j02.t01`, `j02.t01.r05` | folder number prefix only, never the slug |
| Research question, the paper's question | `RQ.H2`, `RQ.RQ1`, `RQ.Q` | the table's first cell; `RQ.Q` for the question above it |
| Design, idea, rule, goal, method step | `j01.d03`, `j01.I04`, `r1.2`, `g01`, `M01.m2.3` | Task folder, ideas.yaml `id:`, design-goal.md |
| Insight question, cell | `K01`, `K01.<segment>` | front matter `question:`, partitions.md key |
| Labeling item, rule, collection question | `ex-26`, `R-refusal-help`, `r08.Q2` | corpus item_id, a minted rule id, `## Q2` |
| Section and its entries | `<view>.<id>`, `<view>.<section id>.<id>` | the heading's `{#id}` or `<!-- id: x -->` |
| Other named things | `term.SNF`, `fn.make_cohort`, `decision.<id>` | the name already on disk |

Rules:

1. Segments are joined by `.`; each segment matches `[A-Za-z0-9_-]+`. A name holding a dot or a slash (a model id
   such as `qwen2.5-7b`) is addressed by its file stem or a minted id.
2. Matching is exact-case (`d03` is a design, `D03` a Studio decision), with one exception: a sentence id is written
   `s8` and an older `S8` is read as the same sentence (the shared `sid()` helper), so cards written before the
   switch keep matching.
3. Never a position ("row 3", `@unsafe/0`) and never an auto-generated hash.
4. No version in the address (no `mNN`, `question-vN`, `data-vM`, draft `v2.7`). The owning folder carries the version;
   the card records which version or words it saw.
5. An item with no name on disk gets an invisible `<!-- id: x -->`, written by whoever writes the content (the agent or
   the build) and kept across versions. The page checker reports an item that needs an id and has none.
6. Across pages the full form is `<page path>:<address>`.

## 4. Who owns a card

- A card lives with the page where the item's id is minted, not where it is shown: a design's cards with its Task, a
  rule's with the Board, a question's wording with the Question Book Task, an answer cell with that Board Job's Task,
  a labeling item with the items Task.
- Other pages show the thread by reading the owner's files and write back to the owner. A parent page rolls the marks
  up by reading its children; it never copies a card.
- Card files sit in the owner's `records/` folder (`draft/records/` for a draft Task, as today). A Project's own cards:
  `<Project>/records/project-comments.md`.

## 5. Marks

| Mark | Meaning | Source |
| --- | --- | --- |
| 💬 N | comments | stored: `<stem>-comments.md` |
| 📝 N | edit cards waiting for Accept or Reject (orange) | stored: `<stem>-revise.md` |
| ✓ | the person checked this item | stored: `<stem>-checked.md`; a person only, never AI |
| 🙋 N | a decision waiting for the person (orange) | derived: a collection Run, a sign or close action |
| ★ N | a review score (lowest of its parts) | derived: a review Run's Markdown result |
| 📊 ❝ 🖼️ 📎 | values, citations, displays, other evidence | derived: Evidence Items, Results, receipts |
| 🕘 N | earlier versions | derived: drafts, passes, the same item in an earlier Job |

- Orange marks (📝, 🙋) wait on the person. They roll up to the section bar (`ui_parts.word_span`, the bar 📝 💬 marks
  in `focus-assets/focus.js`) and to the page's 🙋 tray. A count sits only in the mark; a label never carries one.
- A mark with nothing behind it is not drawn.
- Card marks sit in their own slot after the item, apart from a workbench's own state marks (✅ 🏃 ⬜).
- ★ is the AI's judgement and ✓ the person's. They are never merged.

## 6. Card file format

The three files keep Draft Lab's existing format (`workbench-task-draft/revise_steps/draft_step_revise_notes.py`), so the MISQ
records and the skills that write them stay as they are.

`<stem>-comments.md`:

```markdown
### Comment 3 · RQ.H2
Quote: Who are the billers, beside physicians who do the same service without AI?
State: open
- Note · 2026-11-14 10:20 · Reviewer: "non-billers" needs a definition.
- Reply · 2026-11-14 11:02: Same specialty and ZIP; added to the row.
```

`<stem>-revise.md`: `## Pass k · …` sections, newest first; each card a `### Edit · <address> · <why>` with `By:`,
`Why:`, `Original:`, `Expected:` (or `(cut)`), `State:` proposed, accepted, rejected, applied, superseded or done.

`<stem>-checked.md`: one line per check, `- <address> · <time> · <the words it saw>`. A check lapses when the words
change.

A card may add `Kind:` (comment, edit, decision, evidence, score) and `Seen:` (the version or draft it read) when its
heading does not say. A decision card names its `Options:` and the chosen one, or points at the record that holds the
decision: `Decision: runs/r08_collect_release_choices` or the sign action. A decision is never copied into a card.

## 7. The shared part

It lives in `servers/workbench/page/`:

- `item_cards.py`: the pure parser and writer of the three files (lifted from `draft_step_revise_notes.py`: `_comments`,
  `note_act`, `card_act`, the checked lines). `cards(page) -> {address: [card]}`, cached by file mtime.
- `item_address.py`: resolves an address on a page to its item and its owner page; lists the cards whose address no
  longer resolves.
- `item_marks.py`: `marks(address, cards, derived)` draws the mark strip; `card_slot(address)` the cards under the
  item. A table row gets a full-width row under it; a sentence keeps Draft Lab's layout.
- One JS asset keyed by `data-addr`, not by `.sx-row` or `data-s`.
- One writer endpoint, `POST /_board/item-card {page, address, act, n, was, text}`, with the same-origin check.
  `/_board/draft-comment` and `/_board/draft-card` stay as aliases. `/_board/card` and `/_board/comment` are retired
  (405) and are not reused.
- A workbench plugs in by putting `data-addr` on each item it draws and calling `item_marks.marks()`; nothing else.
- Accept is a per-kind adapter: a sentence rewrites its `- Bn · Sn ·` line, a table row rewrites the row keyed by its
  first cell. It refuses when the item's words differ from the card's `Original:`.
- Signs, releases and labeling answers keep their own endpoints (`design-ladder-act`, `/_board/labeling/act`,
  `insight-act`). A 🙋 card links to them.

## 8. Safety

- Writes: an advisory lock beside the file (`fcntl.flock`), write to a temporary file then rename, append-only
  headings, and the existing `was` guard on a card's state (409 when it changed).
- Never written by a click: a signed or released file (`mNN.approved.yaml`, a released design), and any generated
  file. An 📝 on generated content becomes an instruction to the next Run that writes it.
- A closed Job still takes comments; its close receipt does not hash `records/`.
- Growth: decided cards move to `<stem>-revise-history.md` and closed comments to `<stem>-comments-closed.md`.
- Renames: a card whose address no longer resolves shows in a "moved" list at the end of its section; it never
  disappears. A rename tool rewrites addresses in bulk.
- Privacy: a card's `Quote:` never pastes a data row. Exports skip `records/` by default.
- Speed: each card file is read once per page and cached by mtime; never one read per row.

## 9. Order of work

| Phase | What | Owner | Done when |
| --- | --- | --- | --- |
| 0 | This contract; the shared part (`item_*.py`, `/_board/item-card`); the RQ table pilot | Project, Paper | ✅ 2026-11-14 |
| 1 | Finish the pilot: the person writes one real comment; `RQ.Q` id in the Story; an edit card rolls up to the bar; `note_act`/`card_act` read-modify-write inside the lock; card reading costs under 5% of a page render | Paper, Project, Draft Lab owner | all five checked live |
| 2 | Each workbench's content items, most valuable first (§2): Paper (Story by Section, Evidence Items, citations, values); Design (designs, rules, goals); Insight (questions, cells); Labeling (rule ids replace positions first, then rules and items); Work (decisions, findings, sections; ★ JSON becomes a review Run's Markdown); Project (Decisions, Terms). Structure rows get `rollup()` only | each workbench's owner, in parallel | per workbench, below |
| 3 | The writers: the skills whose agents review or comment (draft review, paper story, design reviewer, insight reviewer, labeling) write their findings as cards in these files | skill owners | an agent's review shows as marks with no hand step |
| 4 | Retire what the cards replace (separate comment lists, per-view note boxes); commit per workbench | each owner | nothing shows a thing twice |

A workbench's phase 2 is done when: its tests pass; no file reaches 700 lines; every content item in §2 has an address
(the page checker finds none missing); structure rows show only the roll-up; a comment and a ✓ written on a copy
persist after a reload; Chrome shows no console error; the pages answer 200 on the live server.
