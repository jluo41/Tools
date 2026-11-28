# Draft Lab · the step cards and what each click writes

How the cards inside the draft Task's views behave: Draft Lab's sentences and cards, Plan's mind map,
Evidence's rows, Display's units, comments, and the files each click writes. The cards are the same on the
focus page (`1 · Draft`, `2 · Plan`, `3 · Evidence`, `4 · Display`) and on the classic `layout=frame` route; the
seven-tab layout named below is the classic route's (`classic/layouts.md`).

## The step cards

A Task whose face says `task-type: draft` opens in the frame with Work as seven step tabs, the s41 design:

```text
Description │ Report │ Work │ Runs
Work:   Studio · 1 · Plan · 2 · Write · 3 · Evidence · 4 · Display · 5 · Revise · Delivery
        each tab: Operation (Input · Sign · Prompt + user feedback) over Result (folded cards)
Report: the same seven, Results only · Table · Questions
```

- `draft_steps.py` draws the tabs; `task_draft.py` lays them out (`DRAFT_TASK_SUBS`, `DRAFT_TASK_RUNS`). Nothing here writes.
- Every open reads the files again: the newest `draft/<stem>-draft-v<N>.md` (its header, `## 1 · Structure`,
  `## 2 · Scratch`, `## 3 · Draft`, `approved:`), `draft/records/` (`<stem>-context.md`, `-requirement.md`,
  `-revise.md`, `-feedback.md`), `draft/previous/`, `evidence/cards.yaml` and `proposals.md` (hai-evidence
  `cards.py`), the Block's Studio topics whose face names the Task, and the Block's `delivery/<jNN>/<tNN>/`.
- Each tab's chip comes from those files: Plan is `✍ sign` until `approved:` starts with ✅; Revise counts passes
  by `draft/previous/`; Delivery is four boxes (build, render, check and Send, read back).
- A bare Work link opens the first step that waits (`→ next`, `✍ sign`, `✍ send`); the Studio is optional.
- Description is the face alone: its old Plan, Requirement and Records are cards of 1 · Plan. An old link
  (`sub=Draft-Scratch`, `Evidence-Value`, …) opens the step that took its place (`OLD_SUBS`).
- The prompt's notes stay in the browser and go out with Copy as `user feedback:`; a pasted image is not kept yet.
- Your own words: 2 · Write opens, in Work and in Report, with the Page's Revise boxes (`outline_revise.py`,
  embedded): one paragraph per box with no frame, one sentence a row (a long one wraps inside its row, a faint · where
  each row starts; Enter starts a row); on save the rows are cut into
  sentences and each Bullet
  takes the run of sentences that reads most like its old Draft (nothing dropped; a ⟦pending⟧ mark stays its own). It saves
  into `## 3 · Draft` when you leave it or press Cmd+Enter, Esc puts back what it held, and the first save on a paragraph
  opens `run-revise-<cN-pM>`.
  5 · Revise has no editor of its own. Every Operation box opens folded, its chip still showing the step's state.
- While an agent works on a step, a ⏳ Running now line sits under Operation (what, since when), read from
  `draft/records/<stem>-running.md`, one `- [<step>] <what> · since <time>` line per open run, which the agent writes
  when it starts and removes when it ends.
- 5 · Revise's Result is one card: the text on the left, its Revise cards on the right in reading order. The text is
  one column with no space between sentences, the same as 2 · Write's: each card
  is placed at its sentence's line and pushed down only to clear the card above (CARDS_JS `align`, for any `.rv-split`),
  the text never moves for a card and stays in view while the cards scroll. Above this card sits the pass's own
  section, 📋 Revise Review Report: the reviewer, the verdict, one row per rubric axis (Mechanics, Function, Evidence,
  Readability, Coherence, Anti-AI writing, and the venue's rule) with its verdict, a score out of 10, how the draft reads
  and the smallest fix, the mean score on top, then the paragraphs
  now against proposed; nothing to accept.
  Cards on the whole Section stay above the text, the full width. Hovering a card (or one of its rows)
  lights its sentence, and a sentence lights its rows. ✓ Accept all in the header accepts every card still proposed, one
  after another, and leaves the decided ones. Only the latest pass shows (the file keeps only it; older passes are in git). A card is one light box; a
  Section question on the paragraph plan is a table, now against proposed; a change over several sentences is a row per
  sentence. Each card has ✓ Accept · ✗ Reject · ✎ Edit · ↺ Undo; a click writes
  only that card's `State:` or `Expected:` in `draft/records/<stem>-revise.md` (`POST /_board/draft-card`,
  `draft_steps.card_act`; refused when the card changed on disk since it was shown). The text changes only when "apply
  the accepted cards" runs. Below it, the Section canvas, which may hold other
  papers' openings beside ours (hai-draw draft `examples:`).
- The text column reads as prose in 2 · Write, 3 · Evidence, 4 · Display and 5 · Revise alike: 17px type, no bullets, each
  sentence's number hung in a left gutter so every sentence starts on one line (`_sentence` gives the number and the
  words their own spans, `.s-no` and `.s-tx`), and `\citep{…}` read as its keys in small grey. In 5 · Revise only, the
  evidence stays boxed but its CITE labels go; 3 · Evidence keeps both.
- 📋 Revise Review Report also shows Each sentence, in its context: the report's `Sentences:` lines (hai-draft-review
  `ref/sentence-logic.md`) as a table of logic and read scores, the link from the sentence before, the problem and the
  smallest fix, then each paragraph's flow. Cards already written
  into the text, and comments their person closed, are hidden until Show the <n> finished.
- A card whose fix is a choice shows its options (`Option A (<approach>): <sentence>`, `Chosen: A`): the chosen one as
  its change, the others as plain sentences, each with ↳ Use <letter>. A comment is a
  thread with You and AI marks and small text actions. The review's sentence
  lines are Logic cards, one beside every sentence (logic and read scores, the link, the problem in one line, the fix
  on click), and each paragraph's flow sits under its last sentence; the report keeps only their sum. Every card is one compact line until clicked, as
  comments in a shared document are, so each stays beside its sentence. Hide comments, Hide logic and Hide edits
  filter the column.
- 5 · Revise's column holds four kinds of card, each switched on or off by its chip above the text, in any mix:
  Comments, Logic, Edits (only those still open: proposed, or with options) and Evidence (each sentence's items, the
  rows 3 · Evidence shows, named by their paper's key or value in one line). No Accept all, no Show finished. An Edit
  card is a choice: its options A, B, C, then "drop it: keep the original", one radio each, and Confirm. A Logic card
  says its quality in a word (good, passes, weak, needs work, broken) before its two scores. Resting the pointer on a
  sentence makes it the focus: its cards light up and slide level with it, centred on it. A card
  opens over the cards below when pointed at and folds when the pointer leaves; a click pins it.
- A Table or Figure the text calls shows under the first sentence that calls it, in Write, Evidence, Display and
  Revise alike (`_embed_displays`): the unit's preview.png, opened full
  size on click; a link to preview.pdf when only that exists; "not built yet" when the unit has no picture. The unit in
  display/ and the Run that made its asset stay the source; LaTeX takes its PDF, Word and the web its PNG.
- Every word on 5 · Revise lives in a Markdown file, never in the page: the text in `draft/<stem>-draft-v<N>.md`, the cards and the report in
  `draft/records/<stem>-revise.md`, the comments and their replies in `<stem>-comments.md`, the rulings in
  `<stem>-revise-rules.md`. A click writes only those files (`card_act`, `note_act`, `plan_act`); the page is built
  from them on every open and keeps nothing itself, no browser storage. What is shown or hidden, open or folded, is
  the view's own and is not saved.
- A person's comments live in 5 · Revise, among the cards. A + on the right of each sentence, shown on hover, or 💬 Comment
  under words selected in one sentence, opens a comment card in the right column, in reading order before the cards on
  that sentence; Save writes it to `draft/records/<stem>-comments.md` (`POST /_board/draft-comment`,
  `draft_steps.note_act`: add · reply · done · reopen · delete, refused when its state changed on disk). A sentence a
  comment still waits on shows 💬. Each pass answers the open comments (hai-draft-writing ref/revise.md): the card
  that changes the sentence says `Answers: Comment <n>` and shows 💬 answers Comment <n>, the comment shows ↳ that card
  and the pass's Reply, and its person closes it with ✓ Done or ↩ Reply (it opens again). No copy button hands the
  comments to an agent (removed 261115): a pass, or the page's chat, reads them from that file.
- 3 · Evidence's Result is laid out as 5 · Revise's: the text one column with no space between sentences, and at each
  sentence on the right its card, a one-line row per Evidence item that backs it, what backs it on hover. A card sits at its sentence's line, pushed down only to clear
  the card above (CARDS_JS `align`); the text stays beside the cards and scrolls itself to the sentence a card lights. Each item has an id, its card and
  its place there, CITE 1.4 or VALUE 2.1, the same id on the
  text's mark; hovering a row lights its sentence and a sentence its rows. Under it each Evidence card has its own fold, then the Asks. A card is a topic, the Task its items come from or would
  be made in (hai-evidence `cards.py by_topic`); VALUE was WORK until 261020.
- 3 · Evidence also shows every point still open, card or no card: each ⟦…⟧ in §3 (⟦check: …⟧ a source not yet verified, ⟦pending …⟧ or a one- or two-word ⟦x⟧ a value a
  Run has not given, any other a source still to find) and each §1 point whose line says `Evidence: none · <why>`. Each is
  OPEN <n> in reading order, a row in its sentence's card after the evidence rows (❓ to check or find, ⏳ waits on a
  Run, ⚪ no evidence), and all of them in one fold, `❓ Open points`, the ones to check or find first. Input counts them,
  the prompt asks for an item for each (or leaves the paper's own reasoning), and one to check, find or wait for keeps
  the chip `🔶 asked` (`draft_steps._open_points`).
- 4 · Display: the Section's
  displays, each a unit `display/Display<n>-<slug>/` (hai-display), else a unit still in a display Run's newest
  pass. A unit is DISPLAY <n>, linked to the sentences that call it by what its README calls it (`shown as:`, else a
  Table or Figure in `label:`, its heading or its Placement) or by its `\label`; a call no unit answers shows as not made
  yet. The Result is laid out as 3 · Evidence's, each display's card at the first sentence that calls it (its
  picture, its claim, ⬜ planned, ✍ to accept or ✓ accepted), then each display folded on its own, full width with its
  kind, layout, built_on, status and files. Its chip is `✍ sign` while a built unit waits for `accepted:` (only a person
  writes it), `· optional` when the text calls no Table or Figure. Revise moved to 5 · Revise; `sub=4 · Revise` still
  opens it (`OLD_SUBS`).
- 1 · Plan holds the Scratch (`outline_scratch.py`, embedded): a note per paragraph, `## 2 · Scratch`. Report shows the prompts of 1 · Plan, 2 · Write and 5 · Revise too.
- 1 · Plan's Result is §1 as one mind map (`draft_steps._plan_map`): the Section and its `arc:` in the
  middle, its parts (`C1`, `C2`, …) when it has several, each paragraph with the Structure Overview's `→ C1.P2: …`
  question on the arrow to the next, each Bullet a leaf (S number, role, words, its Evidence cards); a Bullet's Note
  shows on hover, a ⟦check⟧ in it in red. It replaced the paragraph table and the Bullets table.
- The map is edited in place: a point's words or role, a paragraph's name, a
  question, the arc; Enter after a point or ＋ point adds one (`S4a`, after the point above it), emptying a point takes it
  out, dragging its S label moves it; ＋ paragraph adds one after a paragraph, named first, and the paragraphs after it
  move down a number in §1, §2 and §3; an empty question slot takes a new one. Each change is one `POST /_board/draft-plan` (`draft_steps.plan_act`) into the newest draft's §1, refused
  when the words changed on disk, a newer draft exists, or §1 is signed.
- 1 · Plan's Result also holds the examples, as the Section canvas that draws them beside ours (a topic named by
  another's `examples:` is shown once, inside it), else a frame onto the topic that reads them (hai-draw read's
  `reads/<pNN>/reading.yaml`), and `📏 Requirement and Rubric` (the desk rule, ours beside each example paragraph
  by paragraph, the four axes).
- A step's Copy prompt ends with the Task's session (`session:` on the Task face, else the Job face): pasted into
  any session, it tells that session to send it on to the named one, or to do it when that one is not running.
- A Section's Studio topic is one whose face names the Task; a face naming `jNN_…/tNN_…` paths counts only for those
  (two versions often share a Section's name).
