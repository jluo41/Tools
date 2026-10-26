## 0.104.15 · 2026-10-21 · 2 · Write is done only when § 3 holds a sentence

- `draft_steps.py::states` counted `## 3 · Draft` as written when it held only the `### C1.P1` headings an empty draft
  is laid out with, so ten Sections of Paper-AgreeableOpioid-Jama read `2 · Write ✓ done` with no sentence written.
  Write is now done only when a line under § 3 is neither a heading nor a comment; otherwise it is `next`.
- JL 261022: "在 write 的时候，你应该先找到相应的 example". 2 · Write opens the Section canvas first, ours beside the
  examples, titled "📚 Our text beside <n> published examples" (JL 261022, of s22: "I want things like this"; the
  examples' own topic when no canvas draws them; `_examples_card(..., own=True)`), its Input names the papers, and its prompt starts with them: read
  the examples and note each paragraph's or heading's move and length, write to that pattern, name each departure; with
  none, find and read 3 to 4 first (haipipe-draft-writing 0.26.0 `ref/writing.md` § 0).

## [0.104.16] — 2026-10-26

Links, commands and companions repointed at the helper skills merged into `haipipe-display` (now `_parts/<name>/PART.md`). (merge-parts 261026)

## 0.104.14 · 2026-10-21 · 5 · Revise: your comments on a sentence, answered by each pass; the text reads as prose

- JL 261021: "我选中一个句子，在 draft 那段的时候，可以让我加个注释（比如点个加号就能加注释），然后也放到 Revise 的那一栏
  里面"; "你每次改的时候，能不能通过我的 comments 来回复那种？"; "我还是在这个 review 里面加 comments。然后你的 change 怎么
  跟我的 comments 一起来做交互、解决我的 comments 呢？". A + beside each sentence (or 💬 Comment under selected words)
  opens a comment card among the Revise cards; `draft_steps.note_act` (`POST /_board/draft-comment`) writes
  `draft/records/<stem>-comments.md`: `### Comment <n> · S<k>`, `Quote:`, `State: open | answered | done`, then
  `- Note · <time>: …` and `- Reply · <time>: …` lines. A card with `Answers: Comment <n>` shows it, and the comment
  shows the card. ✓ Done, ↩ Reply, ↺ Reopen, 🗑 Delete (only before a reply). Operation's Input counts them; the
  Revise prompt answers them first; the cards' header copies a revise-with-my-comments prompt while one is open.
- JL 261021: "能不能把这个加号放到右边？"; "现在的 layout 读起来不是很舒服 ... 比较乱糟糟的 ... 把字体变大一些 ... 像 S5
  这种东西能不能放到最左边". The + and 💬 sit in a gutter on the right of each sentence (`.nt-gut`). The text column
  (CARDS_CSS `.rv-left`, every tab with text and cards) is 17px, has no bullets, hangs each S number in a left gutter
  (`_sentence`: `.s-no`, `.s-tx`; Write's typing handler writes into `.s-tx`), and shows `\citep{…}` as its keys in
  small grey (`.cite`). In 5 · Revise the evidence stays boxed, without its CITE labels (JL 261021: "in 2012,
  65% of US adults <--- I think we still need the box").
- JL 261021: "why I have this large margin". CARDS_JS `align` measured a card against its sentence on the screen;
  the text column is pinned and scrolls by itself, so re-placing the cards while the page was scrolled pushed one
  down by the scroll (1,541px at 1300px wide). It now measures each from its own column's top.
- JL 261021: "让 AI 也来评评每句话，作为一个 reviewer"; "每句话都要看一下上下文，review 它的逻辑关系是否通顺，并且给每句话打分";
  "你的这个 editing card 如果已经结束的话，就把它 hide 掉吧". The 📋 Revise Review Report shows the report's `Sentences:`
  lines (haipipe-draft-review 0.3.0 `ref/sentence-logic.md`) as a table, Each sentence, in its context: logic, read, the
  link from the one before, the problem, the smallest fix, with how many pass, and its `Flow P<k>:` lines. Cards written
  into the text and comments their person closed are hidden until "Show the <n> finished"; hidden cards are not placed.
  The Revise prompt asks for the lines and ends the loop only when every sentence passes.
- JL 261021: "未必一下子只给一种修改结果，也可以说可以用 A、B、C 几个不同的方法去修改". A card's `Option A (<approach>):
  <sentence>` lines show under its change, each as a word diff with its approach; the one in the card is marked, and
  ↳ Use B (`card_act` with `option`) makes B the card's Expected, `Chosen: B`, accepted. A written card that has
  options is not hidden as finished.
- JL 261021: "我想说自动的话就把它 hide 起来". 📋 Revise Review Report is folded until opened.
- JL 261021: "能不能我的鼠标一放上去的时候，它就自己打开了"; "鼠标移走的话，它就自动合上". A card opens over the cards
  below it when pointed at (they do not move) and folds when the pointer leaves; a click pins it; writing in one pins it.
- JL 261021: "叫 comments、logic、edit 这三块 ... accept all、show finished 之类的，我觉得就没必要加进去了 ... 这里最好也加一下
  evidence". Four chips (Comments, Logic, Edits, Evidence) show or hide each kind in any mix; Evidence cards
  (`_ev_side_card`) put each sentence's evidence rows beside it. Accept all and Show finished are gone.
- JL 261021: "如果我们有图片或者表格的话 ... PNG TO EMBED UNDER THAT SENTENCE". `_embed_displays` shows each display's
  preview.png under the first sentence that calls it (by its name or \\label) in Write, Evidence, Display and Revise.
- JL 261021: "这些 content 它是要存到 Markdown 上的，不能存到 HTML 里面". The rule is written down: every word lives in the
  Task's Markdown and YAML files; the page keeps nothing.
- JL 261021: "这个 edit 你能不能自动把这几个（比如 A、B、C）都列出来 ... D 是 drop it ... 点击确认 button 就可以了". An Edit or
  Review card is a choice: every option listed (A, B, C; one, "this change", when it has none), then the next letter,
  "drop it: keep the original"; a radio picks one (the picked row shows its change, the others read plain) and Confirm
  writes it through `card_act` (the option's words and `Chosen:`, accepted; or the card rejected). Picking what is
  already in the text writes nothing. Accept and Reject buttons are gone from these cards.
- JL 261021: "你这个 logic，你能不能说这 logic 的 quality 好还是坏呀？". A Logic card says its quality in a word before
  its scores, from the lower of the two: ✓ good (9-10), ✓ passes (8), ⚠ weak (7), ✗ needs work (6 or less), ✗ broken.
- JL 261021: "我需要 evidence 对应的是哪一个 paper ... 你得给个链接、给个 reference ... evidence 做的非常的不好". An Evidence
  card names its papers by author and year when closed; opened, each item shows the paper (who, year, title, venue,
  linked to its DOI, URL or arXiv page; `_bib_ref` reads the Run's one-entry .bib), each quoted sentence from its
  facts.md on its own line, the words it backs, and its Run address linked to the Run's Result Card (`_ev_item`).
- JL 261021: "我不知道这有啥用，要不然你把这个也都给删掉吧". "Copy: apply the accepted cards" is gone.
- JL 261021: "当我鼠标停在这个 sentence 上的时候，能不能把对应的这些 card 也高亮出来". Pointing at a sentence lights every
  card on it, of any kind (`sentlit`), with an orange frame; a paragraph's flow card stays unlit.
- JL 261021: "当我们只有点它的最左边的时候，它才会 show up"; "鼠标不小心碰到，它就又打开了 ... 容易太跳脱了". A card opens
  only from its label on the left (`.rv-handle`: an Edit card's title, a comment's pills, "Logic S3", "Evidence S7"),
  and only after the pointer rests there a quarter second; a pointer crossing the column opens nothing.
- JL 261021: "当鼠标移动到某一个句子上时 ... 卡片会移动到与该句子相齐平的位置，以这句话的中心为轴心，在上下方向展开". A sentence the
  pointer rests on (180 ms) becomes the focus: its cards of every kind are lit and slide (translateY, 0.22 s) so their
  group is centred on the sentence; the cards above make room upward, those below downward. The focus holds while the
  pointer goes to the cards, follows a scroll, is laid again after any re-placing, and ends when the pointer leaves
  the text and its cards (`focus`, `unfocus` in CARDS_JS).
- JL 261021: "鼠标放到这个 card 上它会自动展开；鼠标移开之后，新的 card 会展开，旧的 card 会合上". Inside the focus the
  cards are an accordion: the card the pointer rests on (160 ms, real pointer moves only) opens in place, the one
  opened before closes, and the group is laid again around the sentence; a click keeps an opened card open. Outside
  the focus a card still opens over the others from its label.
- Word export (`exporters/md2docx.py`): a Citation comment anchors on the last match of its year in the sentence,
  the in-text citation, not an earlier year ("in early 2026, ... (Gottfried et al. 2026)", t01_introduction v0.5, 261021).
- Delivery's build prompt runs the whole sequence a draft Task needs: `page.py bump` on the person's ok, `adopt`,
  `cards.py bib --write`, `export`, then a check that no citation prints as "?" (t01_introduction v0.5, 261021).
- JL 261021: "回复的时候，不应该有个 AI Reply 吗？ ... 这个我看着就真的很不像一个 modern 的 UI 设计". A comment card is a
  thread: the sentence and its state as pills on top (Open, AI replied, Resolved), each message with a round mark for
  who wrote it (You, or AI for a pass's reply, its words on a light bubble), and small text actions (Reply, ✓ Resolve,
  Reopen, Delete; Send and Cancel while typing). A new comment looks the same.
- JL 261021: "这个 sentence 应该当做一个新的 type。比如说 logic comments ... 应该是放到右边的". The report's `Sentences:` lines
  leave its table and become Logic cards (`_logic_card`), one beside every sentence, and its `Flow P<k>:` lines a
  Logic card under each paragraph's last sentence (`_flow_card`); Hide logic filters them. Every card in the column
  is one compact line until clicked (an Edit card's reason, a comment's last message, a Logic card's problem), and a
  card with options shows its chosen one until "<n> more options ▸". Cards follow the text's order, which an S number
  need not (`_reading_key`, and 3 · Evidence's `_text_rows`).
- JL 261021: "你这个东西 by default 它不能够 hide 吗？". Delivery's Deliveries (`delivery_cards`) are folded until
  opened: each lane is one line (`details.topic.dl-card`: its kind, its state, its files as links), and its preview
  (the web page, the PDF, Word's PDF twin) shows on a click.
- JL 261021, of the Abstract beside the Introduction ("你能不能跟这个 T01 比一比 ... 你看你到底差在哪儿了"): an Evidence
  card's line beside a sentence now names its values as the sentence says them ("1,983 requests", "60.1% · 18.1%"),
  never an item id ("VALUE 1.1 queries in fold00"), and a pending one says what it still needs; a citation card still
  names its paper (`draft_steps._ev_side_card`, given the sentence's words).
- JL 261021, of a `Section question · C2 · …` card running full width above the text: "我想知道它是不是应该也当成一个
  card 之类的，放到右边去？" A card on a whole part is now a card like the others, on the right at its part's first
  paragraph heading, before that paragraph's cards (`_first_para`, `_reading_key`, `_revise_card(..., at=)`).
- JL 261021: "比如说这个 paragraph 也可以加 comments 呢？" Each paragraph heading (`h4[data-p]`) gets a + as each
  sentence does; its comment is saved as `### Comment <n> · C<k>.P<n>` (note_act already took a paragraph) and its card
  carries `data-p`, so it sits at the heading, with a 💬 there while it waits.

## 0.104.13 · 2026-10-21 · ⏳ Running now under Operation ; 📜 Revise rules section

- JL 261021: "如果在跑的话，能不能在这个页面里面显示正在 running？ ... 在 operation 下面要不要加 status，说你现在正在 run？".
  `draft_steps._running` reads `draft/records/<stem>-running.md` (one `- [<step>] <what> · since <time>` line per open
  run) and shows each line under its step's Operation heading; the agent writes the line when a run starts and removes
  it when the run ends. A stale line still shows its start time.
- JL 261021: "可以在这里面再加一个 section，说明一下我们 revise 的规则是什么 ... 作者提出来的那些 revise 意见 ... 在这里也记录一下".
  5 · Revise's Result shows `draft/records/<stem>-revise-rules.md` as 📜 Revise rules, above Older versions: how a pass
  runs, and the author's rulings, each with his words and date; it survives every pass, and blind reviewers get it as
  constraints.

## 0.104.12 · 2026-10-21 · 5 · Revise: the report is scored, with Coherence and Anti-AI rows

- JL 261021: "你这个 rubric 怎么没有分数？而且里面没有提到句子连贯性、反 AI 写法之类的吗？... 你有没有拿那个来测试".
  Then "我觉得还是用十分制吧": out of 10, the bands in haipipe-draft-review's rubric (0.2.0); an older pass's /5 still
  reads. `_review_report` shows a score column (`<verdict> · <n>/10 · …`) and their mean ("a reading aid, never a pass mark"),
  two more rows (Coherence; Anti-AI writing, from haipipe-draft-review's `cli/anti_slop.py audit`), and a `Cards:` line,
  how the cards' own text scores on that audit. `RUBRIC_AXES`, `AXIS_NAME`. The Revise prompt asks for all of it.

## 0.104.11 · 2026-10-21 · 5 · Revise: the Revise Review Report is its own section

- JL 261021, after 0.104.9 put the report inside the cards' column: "不是，你为什么改得还不如之前的呢 ... 你给我改回去吧";
  "above the section of 'The text and its Revise cards' you should give me the section 'Revise Review Report' and tell
  me for each rubric, how you feel about this draft"; "把那些比较详细的 review report 单独作为一个新的 section ... 我还要
  之前的那个 revised card section". `draft_steps._review_report` is a fold above the text and its cards: reviewer,
  verdict, one row per rubric axis (Mechanics, Function, Evidence, Readability, Venue: verdict, how the draft reads,
  smallest fix), then the paragraphs now against proposed. The cards section is back as it was: whole-Section cards
  above the text, the full width; `_report_card` is gone.

## 0.104.10 · 2026-10-21 · 1 · Plan: the mind map never wraps a Point

- JL 261021: "怎么让这个 structure 的宽度能够无限延伸 ... 我就是想让它一直不要有这个 break". PLAN_CSS: a Point is one
  line (`white-space:nowrap`), the map is as wide as its widest Point (`width:max-content`, `auto` columns), and the
  §1 card scrolls sideways inside its own box, so the page never does. Measured: every Point 28 px tall (one line) on
  t00 and t01 at 1200, 2000 and 390 px; t00 at 1200 px scrolls 1,570 px inside a 1,074 px card. On a phone the map
  keeps its one column (`.pm{width:auto}`) and only the Points scroll.

## 0.104.9 · 2026-10-21 · 5 · Revise: the review report card; sentence rows keep reading order

- JL 261021: "先写一个 review report，然后再 propose"; "单独作为一个卡片放到 revise card 里面。名字你可以写 current draft
  review report". `draft_steps._report_card` shows a pass's `### Current draft review report` as the first card in the
  cards' column: reviewer, verdict, the paragraphs now against proposed (the Section question's table), findings; no
  buttons. Cards on the whole Section follow it in the column, no longer above the text.
- `_by_sentence`: a new sentence never goes to an old one before the one the sentence above it went to, so a short
  sentence split off S10 is no longer drawn back to S7 by a few shared words.

## 0.104.8 · 2026-10-21 · 3 · Evidence shows every open point

- JL 261021: "你能读读这个 session，然后你想想我们的 evidence 该怎么把这些不确定的 ... 都加上去？". `_open_points` reads what
  the text and its plan leave unsure: each ⟦…⟧ in §3 (check, pending, or to find) and each §1 point with `Evidence: none`.
  Each is OPEN <n>, a row in its sentence's card beside the text after the evidence rows, so a ✅ card and its ⟦check⟧
  sit together (t01 S1: CITE 1.1 ✅ Li 2021, OPEN 1 ❓ its citation not yet verified), and all of them in one fold.
  The Input row counts them; the prompt asks the evidence Run for an item per point. Found 87 in LLMRec j01's five
  Sections (t01: 5 to check, 1 to find, 12 with no evidence; t03: 4 waiting on a Run).

## 0.104.7 · 2026-10-20 · the Plan prompt asks for short paragraph names

- JL 261020: "you might want to update the content of this as well", on t01's paragraph boxes (names of 12 and 20
  words). The Plan prompt now reads "each paragraph a short name and each Point a short head, 4 to 8 words".

## 0.104.6 · 2026-10-20 · 3 · Evidence and 4 · Display laid out as 5 · Revise

- JL 261020: "我不想让句子跟句子之间有这么大的空格。我想要保证这个 draft 在 revise、evidence、display 这里都保持一样的风格 ... 所以
  句子跟句子之间不要有空格". `_text_rows` no longer makes a row per sentence: the text is one `_md` column in one
  `.rv-split` and the cards are in `.rv-right`, each placed at its sentence by CARDS_JS `align`, in the same `_fold` as
  Revise's; the `.ev-split` override is gone, so the text stays beside the cards and scrolls itself to a lit sentence.
  Measured 0 px between sentences on t01 and t03 in 3 · Evidence, 4 · Display and 5 · Revise alike.
- Beside the text an Evidence row is one line (its id, ✅ or ❓, the words and the value); what backs it shows on hover and
  in the card's own fold, so the cards keep nearer their sentences (t03: S12's card 47 px from S12 when lit).

## 0.104.5 · 2026-10-20 · 5 · Revise's text in one column, no space between sentences

- JL 261020: "我不想让句子跟句子之间有这么大的空格。我想要保证这个 draft 在 revise、evidence、display 这里都保持一样的风格
  ... 所以句子跟句子之间不要有空格". 5 · Revise's text is one column again, the same `_md` text as 2 · Write's: each card
  is placed at its sentence's line and pushed down only to clear the card above (`CARDS_JS` `align`, which works on any
  `.rv-split` whose `.rv-right .rv-card` names a sentence in `data-s`); the text never moves for a card. 0.104.3's rows
  (`_text_pieces`, `_card_anchor`) are gone; a Section card stays above the text, full width. Measured on t01: the gaps
  between sentences match 2 · Write's exactly (the only larger ones are the 3 paragraph headings).

## 0.104.4 · 2026-10-20 · 3 · Evidence a row per sentence; 4 · Display; Revise is 5 · Revise

- JL 261020: "I want it to be left to be the orignal text, and the right to be the evidence"; "I want s7 to be aligned
  with evidence item". 3 · Evidence is the text a row per sentence (`draft_steps._text_rows`, shared with 4 · Display),
  each sentence's Evidence card level with it; checked 0 px from card to sentence in all five LLMRec Sections. The text
  and the cards scroll as one page (no inner scroll).
- JL 261020: "should the evidence item have some index as well?". Each item is CITE 1.4, VALUE 2.1 (its card, its place
  there, in reading order), the same id on the text's mark; hovering a row lights its sentence, a sentence its rows.
- JL 261020: "To show each evidenence card seperately?". Each Evidence card has its own fold under the text
  (`_card_folds`), its items with the sentences they back.
- JL 261020: "cite 1's name is very weird ... make it into different cite with the topic"; "the work 1's name is not
  good". The cards come from haipipe-evidence 0.6.0: a card is a topic (the Task its items come from or would be made
  in), and WORK is VALUE (`INK["value"]`).
- JL 261020: "Or we want to have a new display view after the 3 - Evidence? ... Please do it". A new step, 4 · Display
  (`_display_step`, `_displays`, `_units`, `_calls`): each unit `display/Display<n>-<slug>/` (else in a display Run's
  newest pass) is DISPLAY <n>, set beside the first sentence that calls it (by `shown as:`, a Table or Figure in
  `label:`, its heading or Placement, or its `\label`), its picture, claim and state (⬜ planned, ✍ to accept, ✓
  accepted); a call no unit answers is not made yet; then each display folded on its own. Its chip is `✍ sign` while a
  built unit waits for `accepted:`. Checked on LLMRec t03 (Table 1 to Figure 3 = DISPLAY 1 to 5, planned) and MISQ t23
  (Table 8 with its picture, beside S1 by its `\ref`).
- Revise is 5 · Revise; `sub=4 · Revise` still opens it (`OLD_SUBS`), and "Build figure / table" moved to 4 · Display.
  b34 s41-D04 settles its Open 1.

## 0.104.3 · 2026-10-20 · 4 · Revise in rows, Accept all; every Operation folded

- JL 261020, on 4 · Revise's cards drifting far below their sentences (S12's card 1,200 px under S12): a row per card's
  place (`draft_steps._text_pieces`, `_card_anchor`): a sentence with cards starts a row, its cards level with it; a
  card on a sentence not yet in the text (S10a) sits with the one before it, a paragraph card by its heading, a Section
  card above the text, full width. Checked on t01 Pass 3: every sentence card starts level with its sentence (0 px).
- JL 261020: "I will just accept all the changes here". ✓ Accept all in the cards header posts each proposed card in
  turn (`CARDS_JS` `send`, scoped to `.rv-board`), so no two writes race on the cards file; it hides when none is left.
- JL 261020: "please make all the operation to be hidden by default". `_step_box` defaults to folded (every step, the
  paper Board's steps too), Delivery no longer opens its next box, and 1 · Plan's Scratch editor opens folded.
- JL 261020: "remove this Change it yourself in the Revise, as that will be in the Writing". 4 · Revise shows no editor;
  your own sentences are typed in 2 · Write. haipipe-draft's steps table says so.
- JL 261020, on 3 · Evidence: "the left to be the content, and the right to be the Evidence". The first split
  (`_text_and_evidence`, `_evidence_card`), and `CARDS_JS` lights several sentences per card; 3 · Evidence is now
  b32_draft_ui_design-phy-evidence's, which has since made it one row per sentence.

## 0.104.2 · 2026-10-20 · 1 · Plan's Result is one mind map of §1

- JL 261020, on the paragraph table and the folded Bullets table: "I want you to merge them together, how do you think
  you can draw the mind map for the plan? ... To show what is this paper about?". `draft_steps._plan_tree` reads §1 and
  its Structure Overview (part names, each paragraph's `→ C1.P2: …` question, each Bullet's Note); `_plan_map` draws
  the Section and its `arc:` in the middle, its parts when it has several, its paragraphs, and each Bullet as a leaf
  with its role and its Evidence cards (from `evidence/cards.yaml` `for:`), the wires drawn after layout (`PLAN_JS`).
  One column on a phone. Test: `test_the_plan_is_one_mind_map_of_section_one`.
- JL 261020: "how could I operate and edit it?", then "How could I add the P here or add the S here?". The map is
  edited in place: `plan_act` (`POST /_board/draft-plan` in `_host/serve.py`) writes one change into the newest
  draft's §1: words, role, paragraph name, question, arc; a point added (Enter or ＋ point, id after the point above
  it), taken out (emptied) or moved (drag its S label); a paragraph added after another (＋ paragraph; later
  paragraphs renumbered in §1, §2 and §3, the old hand-on question moved to the new paragraph, a Scratch slot added);
  a question typed into an empty slot. Refused (409) on stale words, a newer draft, or a signed §1.
- JL 261020: "能不能让它默认隐身，等我鼠标移过去的时候再显示出来". The ＋ point, ＋ paragraph and empty question marks
  are hidden until the mouse is over their paragraph or their gap (`PLAN_CSS`, `@media(hover:hover)`); they keep
  their room, so nothing moves, and a touch screen always shows them.
- JL 261020, on the rubric and 1 · Plan's Result: "这个 rubric 你有没有想过怎么能把它改得更好一些？比如找一些相关的论文，
  把它们是怎么写的也放到这下面，做成一个 review", "这里可不可以找一些 examples?", then "here I will expect it to be a
  frame of the sNN studio". New `📚 Examples` card (`_examples_card`): the Studio topic that reads the published
  papers (excalidraw-read's `reads/<pNN>/reading.yaml` under a topic naming the Task, or the topic a Section canvas
  names by `examples:`) opened as a frame onto its own drawing, as the Section canvas is; with none, the card copies
  the prompt that makes one. `📋 Requirement` became `📏 Requirement and Rubric` (`_rubric_card`): the desk rule,
  "Ours beside the examples" (size and each paragraph's move, ours against each paper, from `_examples`), a prompt
  to review against them, and the four axes as a table instead of the rubric file's raw text. A link to a file
  behind the root's `Tools/` link is left out (`_served`): the host does not serve it, and `_rel` raised on it,
  which took the page down once; each card now reports its own error instead.
- JL 261020, on the Plan prompt: "every time I copy it, and I paste it to any session, it will trigger that session
  to work". Every step's Copy prompt now ends, after `user feedback:`, with `session: <name> runs this Task. If you
  are not <name>, send this whole message to <name> with SendMessage and stop; if <name> is not running, do it
  here.` (`draft_steps._session`, `_prompt_box`; the shared copy script appends a button's `data-tail`,
  `servers/workbench/runs_panel.py`). The name is the Task face's `session:` line, else its Job face's; shown under
  the notes box as it is copied. The Studio tab shows each topic as its own card (no "The logic sketch" box around
  them), and a topic another one draws by `examples:` (s26 inside s22) is shown once, inside it: 1 · Plan's
  Examples card is then that Section canvas.
- JL 261020, of a paragraph name typed on the map and gone after a reload: "why the content is not saved here?". A
  new draft (v0.4) was written while the page held v0.3, and `plan_act` refused every save as "newer", said only in
  the map's corner. Now a change of words (words, role, paragraph name, question, arc, taking a point out) lands in
  the newest draft, still checked by its old words; only a change placed by S ids (add, move, a new paragraph) is
  refused, and then the map reloads and puts what was typed back in its paragraph, outlined red, so clicking away
  adds it to the newest draft. Every refusal is said beside the field, and the typed words stay. Each reply names
  the draft it wrote, which the page then holds.
- JL 261020, of a Point wrapping onto two lines on the map: "I think the buleet point should not be too large". The
  1 · Plan prompt now asks for each Point as a short head of 4 to 8 words, its numbers and wording in its Note,
  inside the plan's own 4–11-word rule (`head-too-long`), which 12 of t01's 18 Points broke.

## 0.104.1 · 2026-10-20 · a split sentence id counts in the step views

- `servers/workbench/workbench-task-draft/draft_steps.py`: `_paragraphs` and `_sentence` read `S<n>` with a letter
  suffix (`S3a`, `S5b`), as Pages written before the grammar settled number a split sentence; the MISQ Abstract's
  Plan view counted 4 of its 10 Bullets before.

## 0.104.0 · 2026-10-20 · A draft Task's Work is the six step tabs (b32 s41, JL 261020)

- JL 261020, on the abstract Task's Work: "I think we need to make this as what we exected to see". The s41 design is
  now the screen: Work is Studio · 1 · Plan · 2 · Write · 3 · Evidence · 4 · Revise · Delivery, each Operation (Input,
  Sign, Prompt with `user feedback:`) over Result; Report has the same tabs with the Results only, plus Table and
  Questions. New `servers/workbench/workbench-task-draft/draft_steps.py` reads the Task's files on every open;
  `task_draft.py` lays the tabs out and maps the old tab links (`OLD_SUBS`). Description is the face alone; its Plan,
  Requirement and Records are cards of 1 · Plan (s41 Open 3). The paper theme's SUB-* rows moved there too.
- Your own words in place: 2 · Write and 4 · Revise open, in Work and Report, with the Page's Revise boxes embedded (JL
  261020: "what if I want to revise it myself?"). A version's Work shows each Section's six chips (`task_draft.work_card`,
  through `frame.task_card`); ✎ Write opens the Section's Work. A Studio topic naming `jNN_…/tNN_…` counts only for those
  Tasks.
- Scratch moved to 1 · Plan, typed in place; the paragraph boxes save on leaving them (no Why · Reset · Save row); Report
  carries the prompts of 1 · Plan, 2 · Write and 4 · Revise (JL 261020).
- The paragraph box shows one sentence a row, a long one wrapping inside its row (an editable list over the hidden
  textarea that a Save still sends); the text is matched back to its Bullets by likeness on save (`outline_revise._text_to_bullets`), and
  the embedded editor fits its content (JL 261020; built in the Paper-LLMRecPhy-Jama session).
- 4 · Revise's Result: the Revise cards, then the text, then the Section canvas opened straight onto its drawing (JL
  261020: "No need to have box in box"; built in the Paper-LLMRecPhy-Jama session).
- The Revise cards sit between the text and the canvas, the latest pass only (JL 261020: "always keep the latest
  version"; the Revise prompt rewrites the file as one pass), each card old → new in red and green, its own light box
  with no frame around the pass ("I don't want this", of cards inside the pass's frame; "I still want each of them to
  have a card"), a Section question as now / proposed; the Revise prompt starts as the venue's reviewer.
- The cards act: ✓ Accept, ✗ Reject, ✎ Edit, ↺ Undo, without a reload, through `POST /_board/draft-card`
  (`draft_steps.card_act`, routed in `_host/serve.py`); a pass ends with "Copy: apply the accepted cards".
- One card for the text and its Revise cards, side by side, each card beside its sentence; each item its own box; a
  paragraph-plan question as a table; a change over several sentences as a row per sentence (JL 261020).
- Each Revise row shows its sentence id and names its Bullet (`data-b`, `data-s`); a row the person makes (Enter,
  paste) reads "new" and its Save makes a new Bullet with the id before it plus the next free letter (S2 → S2a), its
  point in `## 1 · Structure` and its sentence in `## 3 · Draft`, never renumbering (`outline_revise._rows_to_bullets`,
  `_new_ids`, `_insert_bullets`; JL 261020: "could we make each sentences to be auto generate the sentence id as
  well?"). "+ paragraph" adds an empty paragraph after one (`POST /_board/draft` `action: add-paragraph`,
  `outline_revise.add_paragraph`), which opens on one empty row (JL 261020: "How could I add a new paragraph?").

## 0.103.0 · 2026-10-16 · The draft Task type is one folder (JL 261016, s41-D15)

- `servers/workbench/workbench-task-draft/task_draft.py` now holds the draft Task's layout, moved out of `frame.py`: `draft_task_spaces`, `DRAFT_TASK_SUBS`, `DRAFT_TASK_RUNS`, `PAGE_RUN_NAMES`, `PAGE_TASK_VIEWS`, the Delivery cards, the Page views (`PAGE_VIEWS`, `with_page_views`) and `VIEW_METHODS` (from `frame_view.py`). `frame.task_layouts()` finds every `workbench-task-<type>/task_<type>.py` through `host_registry.task_folders()`, so a new Task type is a new folder, base or theme.

## 0.102.0 · 2026-10-16 · Renamed from workbench-page (JL 261016, s41-D14)

- The skill is `workbench-task-draft` (was `workbench-page`), named after the server folder it explains, `servers/workbench/workbench-task-draft/`. The folder moved from `skills/1_base/workbench/workbench-page/` to `skills/1_base/workbench/workbench-task-draft/`. `workbench-page` and `/workbench-page` stay as triggers in the description. Every live mention in Tools (skills, refs, tests, `guide/guide.yaml`, code comments) follows; older changelog entries keep the old name.

## 0.101.0 · 2026-10-16 · Moves to 1_base/workbench/ (JL 261016, s21-D05)

- The folder moved from `skills/1_base/draft/workbench-page/` to `skills/1_base/workbench/workbench-page/`. Relative links into `../../draft/` re-pointed; name-based lookups are unchanged.

## 0.100.1 · 2026-10-09 · Theme folders are singular

- Docs name the singular Theme folders (s01-D29, JL 261007): `work/`, `discovery/`, `paper/`, `insight/`,
  `design/`, `labeling/`, `ideation/`; the older plural names still read.

## 0.100.0 · 2026-10-07 · The Page views are the frame's Task Spaces (JL 261007)

- One Page Task's views were a route and a page each (draft, evidence, value, runs, pageruns, delivery, folderstat; outline the old name of draft). They are now subspaces of the frame's Task level, drawn in place: Description › Folder, Audience Report › Draft, Work Details › Evidence · Value, Runs › Page Runs, Delivery › Lanes (`servers/workbench/frame.py` PAGE_VIEWS). A theme keeps them beside its own subspaces.
- One route serves them: `/_board/workbench?view=<view>&path=<page .md>` (`frame_view.py`). The old addresses answer as it on a GET or HEAD (`serve.py` PAGE_VIEW_ROUTES); the POST twins keep theirs. `/w/<block>/<page>/<tab>` of a Task's Page opens its Space in the frame.
- Tests: `_host/tests/test_page_view_routes.py` (new), `_host/tests/test_frame.py`.

## 0.99.0 · 2026-10-07 · Renamed from haipipe-workbench-page (JL 261007)

- The skill is `workbench-page` (was `haipipe-workbench-page`), its folder `draft/workbench-page/`, its trigger `/workbench-page`; every live reference in Tools follows. Older entries below keep the old name.

## 0.98.0 · 2026-10-03 · RoadMap Draw holds two drawings

- Draft › RoadMap Draw is two cards (JL 261003: "please update the section maps and view as well"): **Logic**, the person's logic tree (`studio/<stem>-roadmap.excalidraw`, editable, read left to right, each Bullet a row, a Text column and evidence cards), and **Section map**, generated by `excalidraw-draft` (`studio/<stem>-sections.excalidraw`, view only, with a note when the plan or its Evidence Items changed after it was drawn). Only one canvas on the page is editable, so neither can save into the other.
- New run card `Page.section-map` and its Workbench Table row: Redraw the Section map (skill `excalidraw-draft`); `table-workbench --check --cards` PASS.

## 0.97.0 · 2026-10-03 · The Method page in Design's shape

- Guide › Method follows the shape agreed for Design (JL 261003: "the structure of the method is not smooth", "I want A to E… make the E to be the references"): the steps, then "The method in one picture" (the canvas, moved from the bottom to the top), then one document, A · what the work is (plain words, one made-up example, small diagrams), B · the methods (three families each named by one question, which method when, the seven cards), C · how it is checked, D · in the workbench (each step, its Space and run), E · Reference, folded (terms and people with checked Wikipedia links; Chinese with no page or settled translation marked as ours, and the loop in full).
- Removed: the file notes on screen (in the page and on the canvas), the opening loop table, the repeated loop text. The card families are renamed by their question; the canvas was redrawn after checking nobody had edited it. The shared renderer folds `E · Reference` and sizes parts above their `~~~` sub-sections.
- Then the steps became the spine (JL 261003, Design's second layout): "The method in one picture", 1 · the six steps in one table (what happens, methods, where in the workbench, who signs), then "Step N in depth" sections each with its method cards and its own tests, then Why it works, then Reference, folded. The loop, the workbench table and the "which method when" tree were each a copy of the steps and are gone; Guide's step list is hidden (`"only"`) and now names the same six steps. The canvas was redrawn from the new step table after checking it was unedited.
- Every part is a fold (JL 261003: "make each section collapsable"): the picture, the steps, each "in depth" section and Why it works open at first, Reference closed; the page keeps each reader's folds per family in the browser (`method-fold:<family>:<n>`).

## 0.96.0 · 2026-10-03 · A method page and its canvas

- Guide › Method is now a whole page, as Insight's and Design's are (JL 261003: "create a method canvas as they do"): the five steps, then `ref/page-method.md` (where it sits, the loop, three method families, the tests T0 to T5, what the evidence says) with seven method cards in `ref/methods/`, each card's papers from `ref/page-papers.md` (regrouped by method; `table-papers --online` PASS), then a new methods canvas, `ref/page-methods.excalidraw` (JL 261003: "I want a new excalidraw for it"), editable and saved back. Its first version was drawn by `servers/workbench-shared/studio/method-canvas.py` from the method file; the canvas is the source now.
- Served by the shared `/_board/guide?family=page&mode=method` (`workbench_guide.method_page_html`, keys `method_doc` and `method_drawing`); the canvas loads only near view, so Guide does not jump to it. Workbench Table: Guide › Method gains the run "Add a method".

## 0.95.0 · 2026-10-03 · The shared workbench shell, and a full Guide

- The Page workbench meets the shared rules (JL 261003: "update the haipipe-workbench-paper and haipipe-workbench-page to be consistent with workbench-shared's requirements"): `↑ Board level` under the title, no `all boards · board index` line (JL 261003: "I think we can delete this"), a band from the page (`_page_band`: page kind · state word · draft version; the state without its emoji, e.g. `Partial`, JL 261003: "I don't want 🟡"), plain Space names (Draft · Evidence · Delivery), each Space in one box, Insight's tab colors and sizes (`space_views.SPACE_CSS`, shared with Paper; the Draft View tabs too), and each Runs panel folded to the strip at first (`runs_panel.panel_markup/panel_html(folded=True)`, `data-fold=1`; Design and Guide keep their open default).
- Draft Space laid out as Guide's (JL 261003): the View row (Table · Reading · Scratch · Revise) comes first, with a rule under it and no "View" label; the Structure fold shows only in Table, the view that reads `## 1 Structure`; the "Reads draft/… · Table ## 1 Structure …" line is now the View row's tooltip.
- Draft › Table: the Bullet and Draft columns are 1 : 3 (`minmax(0,1fr) minmax(0,3fr)`, was 2 : 3), so the written draft gets the room (JL 261003); `test_outline_preview.py` reads the new ratio.
- Draft › RoadMap Draw holds the Section's logic (rules, first draw and check now in the skill `0_utils/draw-logic-tree`, JL 261003: "could you make a skill for it?") (JL 261003: "the logic just go to the roadmap draw", "make it deeper", "make the logic clear"): a top-down logic tree, claim → the reasons it rests on → Bullets as leaves, on an editable canvas (`edit=1`). The drawing is the source: `page_roadmap.py --logic <outline>` draws its first version and refuses to replace an existing one without `--force`; the run card is now "Draw the logic" (Person signs: the logic). Every Bullet starts on one shared row and a Bullet under a Bullet one row below (JL 261003: "make the Bullet point to be in the same start in the same level", as JL rearranged the Abstract's canvas, which is kept as saved). First tree: S-ManSci-Main-Abstract, B8 as the claim over three reasons (why a rule is needed, how messages are measured, what decides the choice), 48 elements.
- Draft › RoadMap Draw, a fifth View between Scratch and Revise (JL 261003: "add the excalidraw to show the structure of this section"): the Page's structure drawing `studio/<stem>-roadmap.excalidraw`, read-only at 640px, loaded the first time the View shows (`outline.page_roadmap_html`). New generator `haipipe-draft/cli/page_roadmap.py <page.md>` (`--check` writes nothing): a branching tree read top to bottom (JL 261003: "like a tree plot? up to bottom", "concise and high level", then JL's sketch of one parent over side-by-side children): the Section's title, each paragraph's one-line job, and its Bullets spread below it five to a row with org-chart connectors, each box role + gist; solid green when its evidence is verified, dashed orange while waiting; no separate evidence boxes. Studio style. New run card `Page.roadmap` (Redraw · Draft · views roadmap) and its Workbench Table row; first scene: S-ManSci-Main-Abstract (10 Bullets, 7 waiting, 36 elements). `test_outline_preview.py` reads the new view list.
- Guide: `description`, `ref/workbench-table.md` (17 rows; `table-workbench --check` PASS), `ref/page-papers.md` (8 papers; `table-papers --online` PASS), and RoadMap Draw's Workbench design: the hand-made `studio/page-workbench-design.excalidraw`, edited (JL 261003: "could you update your workbench design as well?"): a Part 0 for the shared shell, plain Space names, no Reads line or View label in Draft, the View row above Structure, a RoadMap Draw tab (370 elements). `page` leaves `GAPS` in `test_workbench_conformance.py`.
- Tests: host 37/37; `test_outline_v4_workspaces.py` reads the plain Space names; page suites keep their 5 earlier failures, board suite its earlier ones, none new.

## 0.94.2 · 2026-09-30 · Runs panel reads a Page's Evidence Items once

- `servers/workbench-page/runs.py`: `local_runs` and `_insight_runs` read the Page's Evidence Markdown (`read_items`) once and pass it to `_evidence_refs` as `ledger`; before, every run re-read it. On Paper-AgreeablePrescriptionDiscretion the Paper Workbench's Sections Space made 582 reads for 18 Pages (33 s of a 59 s open); now 18. The rendered page is byte-identical before and after; one warm open fell from 40-52 s on 5601 to about 7 s on a restarted 5599 (load average 40-80, so seconds are noisy). Tests: `test_runs_workbench.py`, `test_insight_items_integration.py`, `test_revise_run.py`, `test_outline_v4_workspaces.py`, `test_paper_workbench.py` (57 pass) and four haipipe-draft suites (36 pass).

## 0.94.1 · 2026-09-29 · outline/ to draft/ in current-layout prose (JL 260929)

- Paths that describe the current Page layout say `draft/`: the plan `draft/<stem>-draft-v<G>.<S>[.<E>].md`, records `draft/records/`, `draft/previous/`, `draft/skill/`, the Evidence Markdown `draft/<stem>-evidence-items.md`, `draft/evidence/bibex/` and `draft/evidence/materials/` (JL 260929: "it should be draft"). Mentions of legacy Pages, retired `outline/evidence/` lanes and the migration keep `outline/`, as do the OUTLINE stage, the Outline table and the `outline:` grammar key.
- Server `workbench-page` (JL 260929): `evidence.py` links a saved evidence view under the Page's real plan folder (`CTX.plan`, `draft/` since 0.118) instead of a fixed `/outline/evidence/`, which broke on every moved Page, and its empty-state line names that folder; `folderstat.py` gives `draft/evidence/supporting-runs` its 🧷 icon and derived flag (only the `outline/` label had them) and names `draft/evidence` as the flat lanes' destination; `export.py`, `outline.py`, `outline_feedback.py` docstrings say `draft/`.

## 0.94.0 · 2026-09-28 · The skill describes the workbench that ships

- Delivery Runs are named `run-delivery-<lane>` (`delivery.py::FIXED_RUNS`, `runs_panel.py::_FORMAT`, the run card's `^run-delivery-` button); `ref/delivery.md` and `ref/space-mapping.md` follow.
- A Section's LaTeX and Word title no longer prints the page id: `export.py::_page_title` drops a leading
  `<page id> · ` from the H1, so the PDF opens with `§7 Conclusion`, not `S-MISQ-Main-7-Conclusion · §7 Conclusion`
  (JL 260928: deliverables carry no process text). The file name keeps the page id. Test:
  `test_a_leading_page_id_is_not_printed_in_the_title`.
- Delivery: one fixed Run per lane in the Runs panel (`run_delivery_<lane>`), `Done` while the lane is current and `Ready` when the Page changed, from file times (`runs.py::_fixed_delivery_run`, no `runtime.yaml`). Older `rdNN_*` Runs stay on disk and in the All-runs view but not in the Delivery panel (`runs_panel.py`). The Checks view names the lane's Run in one line (`delivery.py::FIXED_RUNS`). `ref/delivery.md` rewritten to the live Delivery Space; `ref/space-mapping.md` RD rows updated. Checked in headless Chrome on a scratch copy of S-MISQ-Main-7-Conclusion.
- `SKILL.md` rewritten against the live code (751 → about 320 lines): three Spaces (Draft,
  Evidence, Delivery), each with its Runs panel on the right; the `draft/` folder and its
  three-section Draft Markdown; routes (`/w` → `/_board/draft`, `lens`, `view`, `focus`, `run`);
  what each Draft view and Evidence view does and writes; the Runs panel (run types from
  `run-cards.md` `🔘 BUTTON … · views`, target, run card, full run names, item-named evidence
  runs, copy-only); the concise-UI rule (JL 260927) with the list of removed items. Retired UI
  is no longer described as current: copy chips, evidence chips on Bullets, the plan card and
  its counts, the Sources line, Run Space as a Space.
- Refs follow `draft/`: `plan-grammar.md` (file name, `# <stem> · draft v…` head,
  `draft-version:`, `draft/previous/`, `plan_layout` folding), `record-shape.md`,
  `review-packet.md`, `folder.md`, `skill-record.md`, `content-preview.md`,
  `evidence/pagex.md`, `evidence/values.md`. `space-mapping.md`: the Spaces, renderers
  (`space_views.py`, `runs_panel.py`), request flow and write contract as built.
  `run-space.md`: the All-runs view (`lens=run`, no button). Delivery Run rows unchanged.
- The 📃 Page tab's tooltip says "Draft, Evidence, and Delivery spaces"
  (`page_workspace.py`, drawer `07-workbench-outline.js`).
- Revise saves show in the Runs panel: a Revise-view Save makes `rp-revise-NN_<C.P>`, which no
  button matched, so the panel filed it under "Other". New card `Page.revise` with the button
  `Revise edits · Draft · ^rp-revise- · views revise` (`haipipe-draft-workflow/ref/run-cards.md`).
  The save message reads `Saved · run-revise-01 · 1 sentence` (`outline_revise.py`; was the
  `rp-` id, the step and "→ Run Space").
- The All-runs view labels its writing section "Page Writing" (was "Paper Writing" on every
  Page; `runs.py`, 6 test assertions).
- A fresh-agent field test answered correctly but found seven doc gaps, now fixed: the run-type
  recipe (one prompt per card, first matching pattern wins, `No runs yet.`, `{run}` unfilled in
  `+ New Run`), a Revise save needs a reload to show in the panel, the three writers edit the
  current plan in place (the old "approved plan is never edited" line described the retired
  Bullet editor), a standalone `page.py serve` binds loopback, and `haipipe-workbench` (1.12.3)
  plus its `ref/roster.md` still described `outline/` and Run Space.
- A second field test (9 files read, was 13) found the hidden gate: `runs.py::_TICKET_NAME` lists
  which ticket names count as runs, so a new ticket prefix needs code in four places. The recipe
  now separates a new button (run-cards.md only) from a new prefix, and names the `item:` ticket
  line that Evidence-row selection reads and the page-wide `rp-revise-NN` numbering.
- A third field test (a new Run family; 21 files read) corrected two lines: selection reads a
  run's `target:` and Evidence item, never its name; a new Page writing prefix also needs
  `runs.py::_valid_page_run_id` (else Held), its label helpers and an owner skill. The recipe now
  lists every place and a search that finds them by mirroring `rp-revise`.
- Each run in the Runs panel names the skill it uses (JL 260928): every card in `run-cards.md` has a
  `🧩 SKILL` line (e.g. `haipipe-draft-writing · haipipe-writing`); a run whose ticket or runtime has
  a `skills:` line shows that instead; `+ New Run` shows its type's skills (`runs_panel.py`).
- `servers/workbench/workbench-task-draft/reader/tests/test_run_family_lists.py`: reads the RP and RE kind tokens from
  `page-run-families.md` and checks every list knows each kind (Space folder, `_TICKET_NAME`, a
  button, a full-word name, `_valid_page_run_id`). Its first run found `rp-auto` and `rp-embed`
  missing from `_valid_page_run_id` (their runs would show Held); `runs.py` now accepts and labels them.

- The studio drawing's new section "The runs of a Page" is built (JL 260929): Context joins the
  Draft Table view (was a Page-level run no Space showed); the Page-level Check button is gone (Check
  lives in Delivery › Checks); Displays name `haipipe-draft-evidence · haipipe-display` through a
  per-button `🧩 SKILL <label>: …` line; the Supporting Runs tab splits into `Task runs`
  (haipipe-task) and `Discovery runs` (haipipe-discovery).
- Readable run names end to end: `run-cards.md` patterns read `run-<kind>-…` and the older names;
  `runs.py` accepts, labels and gates readable names (an open run with only its ticket shows
  Running, not Held); `runs_panel.py` shows a readable name as it is and links renamed evidence
  runs to their items through the Evidence Markdown; the Revise and Scratch writers mint
  `run-revise-<MMDD>-<c1-p2>` / `run-scratch-…` and write `results/` only at close. Checked in
  headless Chrome on a renamed copy of S-MISQ-Main-5-Results: Save → Running, no result; close-run
  → Closed with its red/green ledger.

## 0.93.0 · 2026-09-28 · No content hashes (JL 260928)

- Evidence Result envelopes (`ref/item-table.md`, `ref/evidence/values.md`, `displays.md`,
  `pagex.md`, `ref/evidence-bundle.md`, `ref/record-shape.md`): `input`, `supporting_results`,
  `local_sources`, `provenance` and `Local Input` name paths and Run ids only; no `sha256` field,
  no `#<sha256>` suffix. A DISPLAY intake is stale when a source file is newer than it.
- Delivery Space (`ref/delivery.md`, `ref/space-mapping.md`): each lane is current, stale or not
  built by file time against the Page; no source or artifact hash.
- Run Space (`ref/run-space.md`) no longer lists hashes or checksums among the details it hides.
- `servers/workbench-page`: `export.py` writes `evidence-selection.json` v2 with paths only;
  `outline_feedback.py` writes no `version_sha256` / `input_sha256` in a Writing Run's
  `runtime.yaml` (an older file's sha256 keys are dropped on rewrite) and names `Prior Version`
  and `Base` by file name and saved time; `outline_preview.py` / `outline_revise.py` keep no
  `bullet-sha256` in Draft records; `plugview.py` no longer shows a probe proof's sha256;
  `delivery.py`'s prompt says "saved source version", not "fingerprint".

## 0.92.0 · 2026-09-28

- ⛔ Hard rule under the title (JL 260928, AGENTS.md rule 6): never modify a generated file directly; change the code that writes it, then rerun.
- Export (`servers/workbench-page/export.py`): an older paper-local CITE Result (`pj…`, or a `re-cite`
  without `payload.bibliography`) now yields its Bib: each `payload.sources[].cite` key is taken exactly
  from the one-entry `.bib` of a Supporting Result the Result names. A key found in none is refused by
  name (no paper-wide seed Bib, no key renaming). Paper-AgreeablePrescriptionDiscretion: 143 of 175 such
  keys resolve; the other 32 are 11 keys spelled differently from their Discovery Result
  (`liu2021assessing` vs `Liu_2021`) or with no Discovery Result (`luo2026mapping`).
- Runs panel (`runs_panel.py`, shared with the Paper Workbench): a type's count follows the selected
  target and view; the panel opens on a type with runs there; `panel_markup` is the reusable half of
  `panel_html`; a row may carry its own selection keys (`_keys`) and view filter (`_views`).
- The Page workbench route is `/_board/draft` (was `/_board/outline`, which still answers).
- A display float follows the PARAGRAPH that first cites it, never the sentence (S-MISQ-Main-5-Results,
  260928): after the citing sentence, the rest of the paragraph printed after the table as an orphaned
  paragraph. LaTeX (`export.py` `_paragraph_end_after`: the next blank line, heading or float) and Word
  (`md2docx.py` `place_due`: at the paragraph's end, in both `--join-paragraphs` and one-sentence modes)
  follow one rule; two tables cited in one paragraph follow it in citation order. Tests:
  `test_display_is_inserted_after_the_paragraph_that_first_cites_it`,
  `test_a_table_follows_the_whole_paragraph_that_first_cites_it` (fails on the old code).
- Word (`md2docx.py`): only a citation in PROSE places and numbers a display (S-MISQ-Main-5-Results,
  260928). A `\ref` inside a caption or note ("the pooled sample of Table 4") had counted as a first
  citation, so Table 4 printed and took its number before Tables 2 and 3. Numbers now follow the order
  prose first cites the displays (a pre-scan of every paragraph); a caption's forward `\ref` resolves to
  that number; a display cited only from a caption or note prints at the end of its page. Test:
  `test_a_ref_in_a_caption_never_places_or_numbers_a_table_early` (fails on the old code).
- Evidence Space has a fourth tab, Supporting Runs (JL 260928): the Runs every item's `Supporting Runs`
  line names, as Execution/Discovery > Block > Job > Task > Run, each Run with chips for the items it
  feeds; the Evidence Runs panel gains a `Supporting runs` type on that tab, and the panel's leftover
  bucket is now `Other` (it had been mislabelled `Supporting runs`).
  The tree reads like a file tree (JL 260928, "make it look more beautiful"): guide lines between levels,
  the level prefix (`b03` `j02` `t01` `r04`) in the accent colour, a status dot, rows without boxes, and
  one outlined type pill per kind followed by the item numbers (`DISPLAY E13 E14 · VALUE E01 E02`), so
  the busiest Run fits on one line.
- Delivery Space decides current or stale by file time alone (JL 260928, AGENTS.md rule 9: no hashes):
  a lane is current when its built files (`index.html`, `<page>.pdf`/`.tex`, `<page>.docx`) are at least as
  new as the Page, and the web copy reads the same as the Page. No `build-manifest.json` is needed, the
  `unverified` state is gone, and the screen shows "Page saved <time>" instead of a SHA-256 line.
  Paper-AgreeablePrescriptionDiscretion: 12 Sections read 3 current; Appendix D and F show real staleness.
- One short name for an Evidence Item on every surface (JL 260928): `Evalue01`, `Ecite25`, `Edisplay13`
  (`src/item_table.py::short_name`). The Evidence table's ID column, the Supporting Runs tree, the Runs
  panel (`run-Edisplay13`, was `run-display-E13`), the Run-binding cards and the Draft chips
  (`Edisplay13.CohortTbl`, was `E13D.CohortTbl`) all use it; the stored id `E13-DISPLAY-cohort-overview`
  and its number are unchanged, so no ledger, Result or sealed receipt moves. `item-table.md` states it.
- An older Paper-local run (`pj05t01r01`) named by an Evidence Run ticket's `legacy_run:` line joins that
  item's tab (`space_views.run_tabs`). Empirical Strategy's two display runs sat in `Other`, so its Displays
  tab looked as if the displays had no run; now Build figure / table lists 4 and `Other` holds 1 (was 16).
- A Run card with no local Result says "no result yet"; it had listed the working folder's files.

## 0.91.0 · 2026-09-25

- The Draft writer (`servers/workbench-page/outline_preview.py`) saves drafted Bullets
  Draft-first; Revise and Scratch saves keep that shape. The Structure card counts drafted
  points in either shape. The UI is unchanged: Table, Reading, Scratch and Revise render
  byte-identically for a Draft-first and a classic Outline, except the run-paragraph copy
  prompt, which quotes the file as it reads.
- `outline/` holds one current plan; superseded versions live in `outline/previous/`
  (`ref/plan-grammar.md` § Draft-first Bullets, § One current version).
- Structure card: an unaddressed `### ` heading (e.g. `### Cut · …`) is a side note, so it
  stays off the Structure text and moves with the paragraph above it; before, the card showed
  it as a line that its own Save then rejected. A renamed paragraph keeps its `· S<a> to S<b>`
  sentence span.
- `outline/` shows two authored files; the process records are in `outline/records/` and the
  Folder tab lists `outline/records` and `outline/previous` as their own rows.

## 0.90.0 · 2026-09-22

- Draft Space gets a fourth view, **Revise** (JL: "我想让每一个 paragraph 是一个方框，然后你把
  现在的 draft copy 过去"): one box per paragraph, pre-filled with its Draft one sentence per
  line, one Save. Lines map back to the Bullets in order; `action: revise`
  (`servers/workbench-page/outline_revise.py`) writes the changed Draft fields into the selected
  Outline and appends a change ledger Step to the paragraph's `rp-revise-NN_<C.P>` Run; Run
  Space renders it under Page Writing → Revise. Revise and the Structure box save only on
  `Save` / Cmd+Enter, never on a timer (one Save = one ledger Step); leaving the page with
  unsaved text asks first (`beforeunload`).
- The Structure card is plain text read from the Outline (`outline_structure.py`), one line per
  C/P heading, and the person clicks into it to edit like Scratch (JL: "我其实就只是想要一个文本而已
  … 主要是方便我来去 operate"): `action: structure` renames, reorders, adds paragraph lines and
  drops empty ones; points stay with their heading. No Mermaid (JL: "we don't use the mermaid");
  the SVG renderer, `<stem>-logic.mmd` reading, and the PNG fallback are gone; the Structure Run
  card in Run Space shows the same text.
- Copy buttons are `⧉ run-structure`, `⧉ run-section`, `⧉ run-paragraph` (JL), smaller, and
  the copied prompt is short: door, addresses, matching Run and next move, blockers, one rule,
  the paragraph's Outline block for run-paragraph only, `Feedback:`.

## 0.89.0 · 2026-09-22

- The Page's workbench tab is 📃 Page (was 🧭 Outline; JL: "could we change this to Page tab?").
  The route id `outline` and `/_board/outline` are unchanged; the `/w/<board>/<page>/page` tab
  word already resolved to it. Inside, the four spaces keep their names: Draft, Evidence, Run,
  Delivery. The Page section `## 🧭 Outline` in a Page file is a different thing and keeps its name.

## 0.88.0 · 2026-09-22

- Run Space's stepper is 📄 Page Runs: `pageruns.py` serves `run`/`start_run` (legacy `phase`
  read), `65-workbench-pageflow.js` lists context · structure · evidence · writing · check with no
  00–04 numbering; the Scratch door's payload field is `step` (save · finish), was `phase`.

## 0.87.0 · 2026-09-22

- Run Space gains the Revise card under Page Writing (`rp-revise-NN_<target>`,
  `haipipe-draft-revise`): before/after cards with a Decision line. The old sentence that
  review is never its own Run is replaced: review feedback stays input to the writing Run;
  Revise is a separate Run that owns decisions, never prose.

## 0.86.0 · 2026-09-22

- The Default Workbench Link is the short address `<DOMAIN>/w/<board-slug>/<page-id>[/<tab>]`
  (`<DOMAIN>/w` standalone). The server composes `path=` and `file=`; `file=` may be
  omitted on the long route too. `<DOMAIN>` is the reader's origin, never baked in.

## 0.85.0 · 2026-09-21

- Renamed from `haipipe-workbench-outline` to `haipipe-workbench-page`, the workbench
  contract paired with `servers/workbench-page`. The skill now owns every
  generic Page tab that workbench renders.
- Absorbed three sibling skills as lane references: `haipipe-workbench-runs`
  0.32.0 → `ref/run-space.md`, `haipipe-workbench-folder` 0.4.3 → `ref/folder.md`,
  and `haipipe-workbench-delivery` 0.6.2 → the compact `ref/delivery.md` (its four
  lane refs latex/word/slide/render are folded into that one file; the roster
  rows keep the storage and writer facts). `page-plugins/` (retired the next day) then held exactly
  `haipipe-workbench-page`, `haipipe-workbench-studio`, `haipipe-workbench-design`.
- The LaTeX/Word writers left `skills/` for `servers/workbench-page/exporters/`
  beside `export.py`, their only caller.
- 0.84.2 (same day): file paths repointed to the plugin-level `servers/` tree.

## 0.84.1 · 2026-09-20

- Clarify that Outline artifacts are consumed by Page Workflow Run Specs and do not define a Run on their own.

## 0.84.0 · 2026-09-20

- Document scoped Draft prompt copying, shared release decisions, current evidence selection, and the two-section reader face.

## 0.83.0 · 2026-09-15

- Make Scratch notes larger and let the manually triggered `Finish Scratch`
  action ask the AI to generate the closing Summary; remove the manual Summary
  form.

## 0.82.0 · 2026-09-15

- Add Draft Space's explicit Table, Reading, and Scratch views.
- Replace the retired Draft feedback composer with one inline Scratch control
  per Section or whole paragraph, backed by `## Scratch` plus paired Runs;
  B/symbol rows have no Scratch control.
- Keep Table/Reading read-only; Scratch closes only after a human Summary.

## 0.80.0 · 2026-09-15

- Make Draft, Evidence, and Run explicit projections of one Page Run Workflow
  Runtime rather than workflow phases.
- Keep Draft Space fully read-only; human feedback and revision history live in
  Page Writing Run Steps/Versions and are presented in Run Space.

## 0.79.0 · 2026-09-15

- Document the paragraph note thread as Draft Space's one browser write (§💬):
  what a note is, where it lands, which Run owns it, and what it never touches.
- `ref/content-preview.md` and `ref/space-mapping.md` now state the narrowed
  law: Draft Space is read-only for the plan; `action: feedback` appends to the
  owning RP journal under `results/`.

## 0.78.0 · 2026-09-14

- Remove `\\illustration{D_xxx}` and `\\diagram{D_xxx}` from Page-facing
  Evidence Label syntax; conceptual renderer outputs use `\\figure{D_xxx}`.

## 0.77.0 · 2026-09-14

- Standardize the Result `labels:` manifest and its one-Result-to-many-Labels
  join across VALUE, DISPLAY, and CITE evidence.
- Preserve authored Page tokens in Draft Space while showing resolved display
  values through expandable provenance details.

## 0.76.0 · 2026-09-14

- Make Role proposal part of Outline `PROPOSE`: the producer and
  `rp00_mermaid-structure` propose one open-ended, context-specific tag for
  every Bullet from the logic flow. Keep the renderer display-only and do not
  introduce a generic `[Boundary]` role.

## 0.75.0 · 2026-09-14

- Align Evidence Space with typed RE identities and `V_`/`D_`/`C_` labels;
  table and figure are now explicit `DISPLAY` label examples.

## 0.74.0 · 2026-09-14

- Hard-cut the retired `outline/evidence/` folder and generated
  `outline/<stem>-evidence.md` snapshot from the current Evidence surface.
  Move old material to `_archive/legacy-outline-evidence/`; the authored
  `outline/<stem>-evidence-items.md` contract remains current.

## 0.73.0 · 2026-09-14

- Append Draft Evidence routes directly after each Bullet statement.
- Remove the repeated `EVIDENCE` heading and visible `evidence: none` pill from
  source-free Draft rows while preserving the decision in Markdown metadata.

## 0.72.0 · 2026-09-14

- Split Evidence Space into Displays, Citations, and Values sections.
- Replace the flat Result table with collapsed, read-only Evidence Item cards
  that reveal Label, Item, Evidence Run, Supporting Runs, Result, and
  contract details on demand.

## 0.71.1 · 2026-09-14

- Make DISPLAY the umbrella for tables, figures, and algorithm blocks while
  retaining TABLE as a legacy alias.

## 0.71.0 · 2026-09-13

- Move Draft Space Plan/Draft source paths behind a collapsed `Sources`
  disclosure so the default reading surface stays focused on Mermaid,
  Bullets, and candidate prose.

## 0.70.0 · 2026-09-13

- Define the Evidence Item → RE → Result → Card → Labels relationship and
  present RP, RE, RD, and Supporting Runs in one read-only Run Space.

## 0.69.0 · 2026-09-13

- Restore compact, read-only Evidence route/card tags in the Draft Space
  Bullet column while keeping full Evidence item details in Evidence Space.
- Keep each Bullet's authored bracketed role visible, with `[Point]` as the
  explicit compatibility fallback for legacy plan heads.

## 0.68.0 · 2026-09-13

- Render Mermaid as a collapsed, native open/close disclosure above the
  read-only Draft table; opening it reveals only the rendered diagram.

## 0.67.0 · 2026-09-13

- Make Draft, Evidence, and Run projections intentionally read-only and remove
  editor, append, preview-form, and comment controls from the reader surface.
- Show each Space's source boundary inline: Draft reads `outline/` Markdown,
  Evidence reads `results/**/result.yaml`, and Run reads `runs/` plus paired
  Results and inspectable supporting references.
- Reject legacy Draft write actions at the Outline boundary while keeping
  Page/Run workflow writers and Markdown authority unchanged.

## 0.66.0 · 2026-09-13

- Reduce the visible Outline surface to exactly Bullet, Evidence, and Run
  workspaces; Context/process records remain safely on disk and in Folder.
- Make Evidence Result-first and mount Run P, Run E, and Supporting Runs inside
  Outline while retaining old deep-link aliases.

## 0.65.2 · 2026-09-13

- Correct remaining Mermaid Structure lifecycle references from the retired
  `rp01` identity to canonical `rp00_mermaid-structure`.

## 0.65.1 · 2026-09-13

- Remove the paragraph Comments composer and its active POST action from the
  Bullet Workspace. New candidate feedback stays in the Page Run; historical
  signed preview lanes remain preserved but unrendered.

## 0.65.0 · 2026-09-12

- Make a paragraph read-only after its canonical Page Run completes: render
  accepted candidate text without edit/comment controls and reject stale write
  requests until an explicit new Version reopens the Run.

## 0.64.0 · 2026-09-12

- Resolve the active Mermaid Structure review through the reserved
  `rp00_mermaid-structure` identity.

## 0.63.0 · 2026-09-12

- Resolve the live Mermaid Structure through `rp01_mermaid-structure`.
- Define paragraph rows and deep links against Page-global P identities.

## 0.62.0 · 2026-09-12

- Present the Page-wide Mermaid Structure above Bullet Workspace, expanded
  while `pr01_mermaid-structure` waits for feedback.
- Render a named missing-map blocker for an open `pr01` instead of silently
  omitting the Run's primary review artifact.

## 0.61.0 · 2026-09-12

- Make Bullet Workspace show every Bullet's bracketed role, using neutral
  `[Point]` only when the plan has no authored role.
- Show `Evidence: none · reason` as an inline `evidence: none` decision with
  the reason retained in detail, shared by standalone and Board hosts.

## 0.60.0 · 2026-09-12

- Give every `C.P.B` Bullet a stable direct link using
  `lens=div&focus=C<n>.P<m>.B<k>`, shared by Board and standalone Page hosts.
- Make compact Page addresses and Bullet Workspace addresses expose that route;
  opening it expands, scrolls to, and highlights the exact Bullet row.

## 0.59.0 · 2026-09-11

- Align preview/Content handoff with exact adoption of accepted Writing Steps. Preserve source comments, distinguish history snapshots from current editable prose, and qualify full rebuilds as formal checkpoints.

## 0.58.0 · 2026-09-11

- Own paragraph-bottom preview comments and the read-comments → revise → reply
  loop without auto-launch, Content promotion, or per-comment Shape versions.

## 0.57.0 · 2026-09-11

- Simplify pending-Evidence references in draft prose from styled status chips
  to ordinary parenthetical labels such as `(Ecite33.SystemStakes)`; retain the
  full placeholder in the source/editor and status/link details in the Bullet
  column.

## 0.56.0 · 2026-09-11

- Keep full pending-Evidence placeholders in authored preview Markdown and its
  editor while rendering only compact status-bearing labels in resting prose
  and paragraph read-throughs.

## 0.55.0 · 2026-09-11

- Make the derived Section logic card collapsible by default and support
  branched argument maps without changing the plan or preview authority.

## 0.54.0 · 2026-09-11

- Render an authored optional `<stem>-logic.mmd` as a read-only Mermaid
  argument map at the top of the live Bullet Workspace's `By part` lens,
  while keeping its source folded and separate from the plan/table authority.

## 0.53.0 · 2026-09-10

- Remove the visible add-Bullet control without removing Read paragraph or editors.
- Document direct working-Shape/preview Markdown editing and the optional,
  derived paragraph-level Mermaid argument map, separate from the reading table.

## 0.52.0 · 2026-09-10

- Require Section Bullet/sentence pairs, explicit function tags when authored,
  and joint revision within one unapproved working Shape rather than per-edit versions.
- Preserve ambiguous old Content without using it as a completed one-row candidate.

## 0.51.0 · 2026-09-10

- Require reading-first side-by-side Bullet/prose presentation even on phones;
  show editors only on demand, with safe Save/Cancel and folded metadata.

## 0.50.0 · 2026-09-10

- Own the authored preview record and edit-preview action; show actual candidate sentences beside Bullet/Evidence with paragraph read-through.

## 0.49.0 · 2026-09-09

- Make declarative Point writing the required style for new or edited Bullets;
  planner-imperative heads are compatibility-only legacy input.
- Require direct Bullet Workspace and Evidence Workspace links in
  Page-changing responses; embedded evidence iframes are secondary details.

## 0.48.0 · 2026-09-09

- Render the Bullet column as readable Point groups: `[n · Role]` plus a
  substantive statement, optional dash annotations, and a single transition
  arrow between adjacent points.
- Accept the Point form without changing legacy Bullet identities or the
  Markdown/evidence/approval boundary.

## 0.47.0 · 2026-09-08

- Make each `C<n>.P<m>` heading a native Bullet group that expands/collapses
  its own Bullets in the live Outline workspace.
- Add a server-backed Bullet editor and append control. The first write copies
  an approved Shape to the next unapproved bounded Shape version and preserves
  the approved file; later writes reuse the working version.
- Rename the compact Page table's `Planned move` column to `Bullet`.

## 0.46.3 · 2026-09-08

- Delegate Run namespaces and form budgets to the resolved owner; keep legacy
  material explicitly read-only and repair the illustrative Related Page link.
- Require one focusable card per Evidence identity with visible source-conflict
  details, and preserve distinct Run, Evidence, and Feedback destinations.
- Align VALUE examples with the common Result envelope and governed stores.

## 0.46.1 · 2026-09-06

## 0.46.2 · 2026-09-08
- ref/evidence/displays.md: under a Paper Section page the unit is `Display<n>-<slug>`; the page id carries the section index (JL 260908).

## 0.46.1 · 2026-09-08
- ref/evidence/displays.md: a Paper Section page names its display unit `Sec<N>-Display<n>-<slug>` / `App<L>-Display<n>-<slug>` from its H1 (JL 260908); other pages keep `<stem>-Display<n>-<slug>`.

- State that the Bullet Workspace's typed Evidence chip takes the same route
  as the compact Page chip (Evidence Workspace → Evidences, exact card) and
  opens no popover.
- Document that a `Routed:` value may name several rows separated by spaces,
  commas, or semicolons; one line per row stays canonical.

## 0.46.0 · 2026-09-06

- Make first `v1.0` approval wait until local evidence work is exhausted and
  name remaining secure-server or person gates.
- Expand the human review packet with version diffs, measured manuscript
  counts, display purpose/count, and the AI's own verdict.
- Allow one DISPLAY Item to name additional served Bullets while preserving
  one owning Target and no sibling evidence inheritance.
- Treat regenerate, Board rebuild, and rendered 🧭 inspection as one required
  completion step after SHAPE, SURVEY, or EMBED changes.

## 0.45.2 · 2026-09-06

- Make `v0.S.E` valid before approval in both interaction modes while Content
  remains closed.
- Define first approval as promotion of the selected Shape-and-evidence state
  and define a major redesign as an unapproved next-generation baseline.

## 0.45.1 · 2026-09-06

- Replace remaining live single-counter language in item-table and related
  presenter guidance with generation/Shape/evidence notation.

## 0.45.0 · 2026-09-06

- Define plans as `v<G>.<S>[.<E>]`: generation, Shape, and optional evidence
  revision, with a two-part version meaning evidence zero.
- Keep `v0.*` planning-only. From generation one onward, every version change
  refreshes Content; evidence revisions inherit the current Shape approval.
- Reserve generation changes for large structural revisions after substantial
  review rather than promoting every approved Shape edit.

## 0.44.0 · 2026-09-06

- Route the compact Page Outline table's Evidence chips through the same
  precise Outline hand-off as Feedback ids and Run tokens: one URL carrying
  `lens=workspace`, `seg=items`, and `focus=run-<item>` opens Evidence
  Workspace → Evidences at the exact item card, scrolled into view and
  highlighted. The compact Page no longer renders an Evidence popover or a
  second copy of the item's fields.
- Make the Evidence Workspace segment an explicit part of the route contract
  (`seg=runs` for a Run token, `seg=items` for an Evidence chip) instead of a
  value derived later from whether a Run was named; older links without `seg`
  still resolve.

## 0.43.0 · 2026-09-06

- Define the MISQ Section planning grain as five or six one-point sentence
  slots per paragraph unless a direct venue or paragraph constraint overrides.
- Keep compound definition, mechanism, boundary, and transition jobs out of a
  single slot so the word budget cannot force routine 35-word sentences.

## 0.42.0 · 2026-09-06

- State the non-inheritance rule on the presenting surface: paragraph and
  division cards group Bullets but own no Evidence Items.
- Let separate Bullet-level Items reuse a source or Supporting Run without
  collapsing their distinct claim-support contracts.

## 0.41.0 · 2026-09-06

- Make the Evidence column a complete per-Bullet decision surface: typed
  Evidence Item(s), explicit `none`, or a visible `missing` defect.
- Reserve `Evidence: none · <reason>` for source-free realizations and forbid
  citations, empirical values, figures, and tables on those Bullets.

## 0.40.0 · 2026-09-06

- Separate citation Evidence Items from citation sources and CONTENT
  placements: `Evidences` counts claim contracts, while `Citations` counts
  verified source entries; review reports placements, key mentions, and
  cited-sentence density as distinct units.
- Add the Section form audit to the human-review contract, including paragraph
  jobs, transitions, coherent word/sentence budgeting, venue citation density,
  and detection of standalone defensive prose.

## 0.39.0 · 2026-09-06

- Expand the compact Page Outline table to six columns by adding routed
  `Feedback` between Planned move and Evidence. Each feedback id is a deep link
  to its exact Context Workspace record rather than inert summary text.
- Route every Supporting and Local Run token to the exact real card in
  `Evidence Workspace → Runs`, with the card focused and scrolled into view.
  The ordinary path no longer opens a long nested popover on mobile.
- Make the one atomic `lens + focus + run` route win both routing races: the
  generic same-site Page router cannot consume the same click, and a pending
  default Outline refresh cannot overwrite the explicit destination.
- Keep a closable, viewport-bounded Run inspector only as a fallback when no
  matching Runs-lens card exists, including browsers without native Popover API.

## 0.38.1 · 2026-09-05

- Make every compact Outline-table Run link carry its workspace, Evidence Item,
  and exact Run address atomically into the Outline workbench. This removes the
  storage/reload race that returned an already-open workbench to Bullet Workspace.
- Add a small Run-inspector fallback for browsers without the native Popover API;
  tap, automatic deep-link open, close, and Escape remain available.

## 0.38.0 · 2026-09-05

- Migration rule for legacy integer plans (JL 260905, "we haven't made them
  from v0 to v1 yet"): a chain `v1 … vN` renumbers ONE TO ONE to
  `v0.1 … v0.N`; no legacy tick mints `v1.0`. The old tick resets to `⬜` and
  survives, with its quote, in that file's `status:` line and one page-log
  record. Only a fresh channel approval that names the version freezes `v1.0`
  (`ref/plan-grammar.md` §6).
- `ref/item-table.md`, `ref/review-packet.md`, `ref/record-shape.md` and the
  🧭 Current Shape line no longer allow a bare `v<N>`; the minor is mandatory
  (`v<N>.<k>`).
- `ref/specimen-section-plan.md` now reads in the grammar it teaches: the
  260831-approved Abstract plan is `v1.0`, `supersedes: v0.3`.
- Applied to the MISQ board: 19 pages, 74 plan files renumbered, 16 old ticks
  reset; the JAMA board's five Story pages still carry integer `v1`.

## 0.37.0 · 2026-09-04

- Render the plan-version ladder as explicit frozen `vN.0` baselines and
  unapproved `vN.1+` revisions. This matches the plan grammar and prevents an
  integer-looking review draft from appearing approved.

## 0.36.0 · 2026-09-04

- Distinguish approved integer plan versions from unapproved decimal review
  revisions. A channel approval promotes the selected `vN.k` content to the
  next frozen `v<N+1>`; evidence folds and later changes begin at `.1` beneath
  that approved baseline.
- Make approved majors immutable and render decimal revisions as the current
  plan when they are numerically newer.

## 0.35.5 · 2026-09-04

- Repair the five cross-family paths in the Display evidence reference so a
  fresh agent can resolve the shared unit contract, presenter, citation
  reader, drawer registration, and workbench roster directly.

## 0.35.4 · 2026-09-04

- Fix the common typed Evidence Item Result filename and keys at
  `<resolved-result>/result.yaml`; keep lifecycle facts in `runtime.yaml`.
- State the narrow consumer-serving exception for a PHI-safe admitted Page
  DISPLAY unit while preserving `$OUTPUT_ROOT` as the Result authority.

## 0.35.3 · 2026-09-04

- Resolve canonical Task Results through `$OUTPUT_ROOT`, preserving both
  self-serving and consumer-serving Task modes.
- Make the Page-owned DISPLAY unit the renderer's direct output destination;
  its governed Result envelope points to and hashes the unit instead of
  requiring an intermediate copy.

## 0.35.2 · 2026-09-04

- Resolve Run and Result locations through the Folder owner's dialect instead
  of assuming sibling `runs/` and `results/` paths.
- Define a DISPLAY unit as the bounded Page-facing projection of a governed
  local DISPLAY Result, with source Run, Result, and hash bindings.
- Separate the Evidence Item's authored `Acceptance` checks at LAND from the
  display unit's lowercase human `accepted:` gate administered by CHECK.

## 0.35.1 · 2026-09-04

- Make the Evidence Item `Local Run` field owner-native: Task routes use
  `bNNjNNtNN[rNN]`, Paper may reserve `pjNNtNNrNN`, and other Folder-local
  owners use their declared Folder/Run address instead of a Paper-only id.
- Define the LAND action transition: `new-run → registered → reuse` after the
  first accepted Result, or `rerun` after a failed, invalid, or stale attempt.

## 0.35.0 · 2026-09-04

- Fold the ranked Skill record contract into `ref/skill-record.md`; Outline is
  its only callable Workbench owner and public surface.
- Delete the Evidence and Probe compatibility skills. Evidence remains an
  internal workspace; Probe remains history handled through migration reads.

## 0.34.2 · 2026-09-04

- Add CITE-only `Verified` to the authored Evidence Item grammar and require
  it for `ready`; keep it separate from legacy BibTeX verification.
- State that auto cannot turn an unsigned branching Decide into `make`.

## 0.34.1 · 2026-09-04

- Replace the legacy Probe-card VALUE reference with the current typed local
  VALUE Result contract: Supporting Runs, one frozen Local Input, one local
  Run, one accepted Result, then EMBED.

## 0.34.0 · 2026-09-04

- Replace the former Plan Context and Page Records top-level groups with one
  Context Workspace containing Overview, Policy & Requirements, Related
  Information, Feedback & Decisions, and Records.
- Add generated `outline/<stem>-context.md` as the ninth process-record kind;
  `haipipe-draft-context` writes it and the Outline workbench presents it.
- Make Context, Bullet, and Evidence the three peer workspaces shared by the
  CONTEXT, OUTLINE, and EVIDENCE phases.
- Remove PageX from the active Evidence Workspace and Evidence Item grammar;
  keep its reference and lane read-only for migration only.
- Preserve typed item names, Supporting/Local Run separation, detailed Run
  popovers, and Paper-local `pjNNtNNrNN` addresses.

## 0.33.6 · 2026-09-04

- Expand compact Outline Run hover text with the actual Run filename,
  repository-relative Run/Result/Runtime paths, availability status, and next
  action; planned routes state that no Run has been allocated.

## 0.33.5 · 2026-09-03

- Mirror the Page's `SHAPE → SURVEY → LAND → EMBED` strip in the plan card.
- Remove the premature Shape-versus-Content alarm from the planning surface;
  structural conformance remains a phase-boundary check.

## 0.33.4 · 2026-09-03

- Rename the Evidence Items lens to Evidences and make its explanatory role explicit.
- Add a Runs lens grouped by Evidence, with one card per Run mapping and both
  mapping and unique-Run counts.

## 0.33.3 · 2026-09-03

- Give every Evidence Run popover a readable Purpose, or a Plan before
  allocation, without creating a second stored description authority.
- Separate path-derived Availability from the SURVEY Next action; replace the
  mixed `new` / `rerun` / `run only` / `ready` chip scale with concise action
  labels.

## 0.33.0 · 2026-09-03

- Separate Paper-local Run identity (`pjNNtNNrNN`) from typed Evidence labels
  and global `bNNjNNtNNrNN` Supporting Runs.
- Render a proposed Paper Run as `P jNN.tNN.rNN new`, preserving the full
  J/T/R index without claiming that a Ticket exists.

## 0.32.1 · 2026-09-03

- Make current Outline ownership explicit in the VALUE and DISPLAY references;
  Probe names remain legacy compatibility only.

## 0.32.0 · 2026-09-03

- Move the ranked Skills Page Record from sibling `skill/` to the explicit
  Outline-owned lane `outline/skill/`.
- Keep one store and one embedded editor; legacy sibling storage is read-only
  migration input.

## 0.31.0 · 2026-09-03

- Turn Feedback into a calm review queue: compact tally and main Ask first,
  requested change plus next Work visible per row.
- Collapse Round order/gate/source and row provenance/routing; suppress the
  generated instructional boilerplate from the live surface.

## 0.30.0 · 2026-09-03

- Add Skills to Page Records beside Files and Log.
- Embed the sibling ranked Skill editor without copying its primary
  `skill/<stem>.md` store into `outline/`.

## 0.29.0 · 2026-09-03

- Reframe the Outline surface as `Bullet Workspace + Evidence Workspace`.
- Group Requirement, Discussion, and Feedback under Plan Context; group Files
  and Log under Page Records, retaining their independent on-disk records.
- Require Folder to expose each `outline/evidence/<lane>/` explicitly instead
  of hiding all evidence under one aggregate Outline row.

## 0.28.5 · 2026-09-03

- Make the folder tree and authored file header use SURVEY's classify/declare
  vocabulary rather than the retired “register every Run” wording.

## 0.28.4 · 2026-09-03

- Remove remaining UI/writer language that required every SURVEY route to be
  registered; bounded `new-*` plans can close SURVEY and allocate in LAND.

## 0.28.3 · 2026-09-03

- Align the required Evidence Item reference with the complete `new-*`
  hierarchy and the SURVEY-versus-LAND ownership boundary.

## 0.28.2 · 2026-09-03

- Make the required Evidence Item grammar inventory-only in SURVEY and move
  allocation/scaffolding of `new-*` routes to LAND.
- Distinguish `registered` never-attempted Tickets from `rerun` attempted or
  stale Tickets; `Ticket only` is a Result-availability state, not an action.

## 0.28.1 · 2026-09-03

- State the exhaustive evidence storage contract: typed VALUE payloads remain
  at real Result paths, and no value or Probe copy lane is created.
- Define dotted Run addresses as linked presentation typography for the same
  canonical compact identity.

## 0.28.0 · 2026-09-03

- Make Outline the single Page planning/evidence authority: the main Page keeps
  one compact derived table, while the Outline workbench owns the detailed Shape,
  Evidence Workspace, and process materials.
- Nest citation, display, PageX, supporting-run lineage, and materials under
  `outline/evidence/`; Run/Result artifacts remain sibling folders.
- Retire the standalone Evidence tab and deep-link compact Run chips into the
  Outline Evidence Workspace.

## 0.27.6 · 2026-09-03

- Point every Outline Run token to its owning card in the unified
  `Evidence Items` panel and expose Run/Result paths there.
- Retain old `By bullet` and `Run links` routes as compatibility aliases only.

## 0.27.5 · 2026-09-02

- Restore real navigation on every Outline Run token. Supporting and planned
  routes now open the owning Evidence Item in `Evidence → Run links` instead
  of rendering as link-styled spans with no click target.

## 0.27.4 · 2026-09-02

- Render Evidence chips from an explicit 1–12 character authored `Label`
  instead of expanding the full item name. Legacy records use a bounded
  fallback, while immutable ids and full names remain visible on click.

## 0.27.2 · 2026-09-02

- Distinguish the compact five-column Page Outline table from the richer live
  Outline tab. Aggregate state counts and the broader sibling-material bundle
  remain live-tab responsibilities rather than extra columns on the Page.

## 0.27.1 · 2026-09-02

- Make the Page Outline a five-column grid by removing the redundant Status
  column. Evidence chips now fit their labels, wrap as a compact set, and keep
  derived state in colour plus the popover. CITE remains a typed Evidence item
  in the shared Evidence column, including multiple citations for one bullet.

## 0.27.0 · 2026-09-02

- Let `<stem>-requirement.md` hold both kinds of requirement under explicit
  ownership: generated venue `V<n>` records and authored page-writing `W<n>`
  records with `Rule`, `Applies`, and `Source`.
- `cli/requirement.py` refreshes only the generated V block and preserves the
  authored W records verbatim. Manuscript Sections keep no source-level
  `Writing Style` block and need no separate writing file.
- V1 is always generated; V2–V4 appear only when the bound venue source
  supplies format, refused-pattern, or move material, so missing source
  content is not replaced with invented requirements.

## 0.26.1 · 2026-09-02

- Make wall Evidence labels compact but previewable as
  `E<n><V/C/D>.<ShortNameNoSpaces>` while keeping the immutable typed id in the
  item popover.
- Replace the folded `Source / run` route with separate `Supporting Run` and
  `Local Run` columns so the two execution layers cannot be conflated.
- Remove the retired Evidence Bundle status vocabulary from the main contract;
  typed Evidence Item states now have one authority in `ref/item-table.md`.

## 0.26.0 · 2026-09-02

- Add `PageX Bindings` to the canonical Evidence Item record between
  Supporting Runs and Local Input. Each binding names an exact file or Result
  plus accepted authority; a whole Folder cannot satisfy an item.
- The Outline tab now exposes PageX source counts and authorities without
  counting them as Runs or Results. LAND readiness includes their validation.

## 0.25.3 · 2026-09-02

- Name citation keys and verification as Evidence authority after the Bibex
  Workbench contract was absorbed.

## 0.25.2 · 2026-09-02

- Retire the separate Page-authored Narrative map. The Page-facing Outline is
  only the current plan table derived from the authoritative `outline/` folder.

## 0.25.1 · 2026-09-02

- Make the Page-facing Outline review path explicit: open `🧭 Outline` by
  default, show the current-plan table first, and keep the optional Narrative
  map as the second, initially collapsed block.

## 0.25.0 · 2026-09-01

- Specify the Page-level `▤ Outline table` as a real five-column review grid.
  The plan's C/P hierarchy becomes group headers; B rows show the typed
  Evidence Item, its source/run route, and derived status without duplicating
  `outline/` records.

## 0.24.0 · 2026-09-01

- The Page now renders the current versioned plan as its `▤ Outline table`
  beside an optional narrative map under `🧭 Outline`. This is a read-only
  projection: `outline/`, its tab, and all eight canonical records are unchanged.

## 0.23.0 · 2026-09-01

- **Human review packet**: documents the four linked records a person sees in
  chat before an outline decision—current Shape, material Evidence Items,
  routed feedback/requirements/open threads, and the exact human choice.  The
  page-outline phase owns delivery; the tab stays read-only and authoritative.

## 0.22.0 · 2026-09-01

- Rename the authored ledger to `<stem>-evidence-items.md`. Each immutable id
  carries its type and name; SHAPE writes its expected ready evidence and
  acceptance, SURVEY plans Supporting/Local Runs, and LAND binds the local
  Result. The derived ladder is specified → planned → ready → folded → accepted.

## 0.21.0 · 2026-09-01
- Eighth record kind: `<stem>-items.md`, the item table (`ref/item-table.md`,
  new): one authored row per evidence mark (Need · Route · Run · Decide), the
  eight outcome words, the derived nine-word status ladder (owed → bound →
  landed → folded → accepted · stale · deferred · dropped · blocked). The
  evidence file becomes the table joined to the disk, Status first; the six
  bundle words retire.

## 0.20.3 · 260831
- Specimen narrative-row reads Story03 (SD/NA retired, JL 260831).

## 0.20.2 — 2026-08-31
- Evidence record heads carry the plan's words (record-shape 0.18.1);
  `Ref` its own row, only when one exists.

## 0.20.1 · 2026-08-31

Scope: outline/ is legal on any unit folder, task folders included (the unit
symmetry); same kinds and grammar, no venue requirement file owed there.



## 0.20.0 — 2026-08-31
Rewritten to one lane, "the folder and the tab": 846 → 194 lines, present
tense. The grammars a writer or parser needs are now FILES a phase loads
instead of paragraphs inside this skill:
- **`ref/plan-grammar.md`** (new): ONE plan grammar, with the Page Type as the
  switch (a Section page's bullet is a sentence slot `S<n> · …`, any other
  page's bullet is a point); heads 4 to 11 plain words; a Note ≤ 30 words (a
  wrapped source line is still one Note; the specimen's longest is 28); the
  marks; the freeze; the teeth. The "terse Capitalized LABEL, ≤ 10 words"
  head rule is DELETED: it coexisted with the approved shape in one section,
  and 19 of 20 MISQ plans were written to it (`Trait relevance`).
- **`ref/record-shape.md`** (new): the seven record kinds in one table (id,
  labels, writer, teeth) with the per-kind rules, the board-wide `D<nn>`
  allocation grep, and the three laws every kind keeps.
- **`ref/specimen-section-plan.md`** (new): SM00 v3, frozen as the approved
  example.
- **Retired from this file**: every "was / until / ruled" narration (the
  `## States` merge, the proof mark, the `✅ have it` mark, the 0.16.x thread
  and version arguments, the Aims-in-plan window), the count words in
  headings (`Seven chips`), and the documentation of legacy parses (the
  renderer's tolerance for pre-0.18 shapes is engine behaviour, not law).
- **From the SM01 field test**: `ref/plan-grammar.md` states one `## C<n>` per
  Content division, `🎯 P<n>` beside `🎯 A<n>.<m>`, a `Cut:` bullet only where
  something leaves (zero is normal), provenance (`Gordon #41`, `D05 b`) is not
  attribution, and the coverage wording for a bare mark;
  `ref/record-shape.md` states the `D<nn>` race under concurrent sessions
  (grep right before the write, again after; the later writer renumbers).

## 0.19.0 — 2026-08-31

- **Aims back on the page; the plan keeps no Aim rows** (JL 260831, QPf12
  row 2: "In the Page as well, and should map to the content"). §🗂 and the
  plan-shape section say so; `servers/workbench-page/outline.py plan_card` reads the page's
  `## Aims` first and lets a plan row fill only an id the page lacks.
- **Seventh kind, `<stem>-files.md`** (QPf12 row 3): the page's retired
  `## Files` as `### F<n>` records with `Path` and `Role`, a
  Related Board Page as `Role: related` with its row verbatim; 📎 Files chip
  (`_SIBLINGS`, physician-space-21).

## 0.18.3 — 2026-08-31

- **The plan never quotes the prose it plans** (JL, on SM00 plan v3: "too
  long, more like the sentences", then "I love this outline style" once the
  heads were 4 to 11 words and every Note one line): §✂️ gains the approved
  shape for a Section page, one bullet per sentence slot `S<n> · <what it
  does>`, groups by move, findings tagged `C1:`/`C2:`/`C3:` plus a word, a
  `Cut:` bullet for what leaves, terms defined inline the first time. A head
  that names nothing ("the question, with its two conditions named once") is
  the named failure.

## 0.18.2 — 2026-08-31

- **Paper-Personality-Opioid-MedJournal board carried into the record shape**
  (JL: "apply it for … MedJournal as well"): its 12 pages were in the original
  three-section shape (`## Aims` groups, `## States` with one ✅/🔨/🧠/⬜ row
  per Aim, `## Log`, no Discussion). Each Aim's state row became the plan
  row's tick and `**Now:** <emoji> <sentence>` (52 rows: 21 met, 31 open;
  three page Aims the plans lacked were appended); Log rows became records;
  every page keeps a `## Files` pointer and a `.pre-outline` backup; each
  outline/ folder gained an empty discussion (`(no open question)`), the
  requirement (venue-only, 0.18.1) and the evidence file. No thread ids were
  minted on that board.
- **JL's QPf12-outline rulings applied on both boards** (260831, rows 2 and 3):
  Aims are BACK ON THE PAGE as their only home (row 2: "In the Page as well,
  and should map to the content"): each page's `## Aims` rebuilt from the plan's
  rows as `- ✅/⬜ A<g>.<n> · head` + `Done when:` + `Now:` under `### A<g> · …`
  groups (group `A<n>` maps to Content division `<n>`); the latest plans keep no
  Aim rows (`.pre-revert` beside each); the 76 carried work items on SM03–SM07
  are dated log records, never Aims (0.16.1). `## Files` left every page for
  `outline/<stem>-files.md` (row 3: "A"), one `### F<n> · <label>` per file with
  `Path` and `Role` (reads · writes · checks · contract · archive · related);
  the 🧭 tab gains the 📎 Files chip (`servers/workbench-page/outline.py _SIBLINGS`). Engine
  teeth and contract text for both rulings: the MISQ-Board session.
- **The seven MISQ plans with bare Aim rows were assessed** (AM01–AM06, SM00:
  52 Aims, 20 met, 32 open, each with a `Now:` fact); `aim-without-state`
  reads 0 on the MISQ board.

## 0.18.1 — 2026-08-31

- **Requirement is venue-only, four records** (JL, reading SM00's 📏 tab:
  "requirement is very hard to read, make it concise and readable, and maybe
  focus on the venue is sufficient"): V1 Shape (+ the desk's ARC chain),
  V2 Size (Words · Citations · Displays, `measured …` folded), V3 Refused
  (one line per anti-pattern), V4 Moves (first four slot names in the head,
  exemplars folded). `N1`/`N2` (Narrative row and style) and `B1`/`B2` (board
  rules) are gone from the file; the Narrative page and
  `ref/writing-rules.md` keep them. A page with no `structure-source:` gets
  no file. `check.py` `requirement-*` teeth follow: venue desk only.
- **Feedback header is three lines and the Round is one text block** (JL:
  "these are too detailed and hard to read"): the law paragraph, `source:`
  and `received:` lines are gone; the Round's verdict, people, dates and a
  link sit on one line, then Ask · Order · Gate; each row's parent R-row
  concern is folded detail (`↳ R01 · …`) under the card, not a label row,
  so the chip count equals the routed rows.

## 0.18.0 — 2026-08-31

- **One record shape for every file in the folder** (JL 260831, reading the
  SM00 lenses: "really hard to read", "the discussion is not for human,
  rubbish", "the logging is very bad", "the design of all of them are very
  bad … we should unify the format"). New §🧾: `### <ID> · <HEADLINE>`, then
  `- **Label**: value` rows, detail indented and folded, signed `>` lanes kept.
  Ids and label sets per kind: discussion `D<nn>` Ask/Options/We lean/Decide;
  log `YYMMDD` headline; feedback `S<x>-PP<n>` From/State/Landed (0.17.4's
  Feedback/Work/Parent rows fit the same grammar); evidence `C.P.B` Has/Status;
  requirement `V/N/B` Rule/Source. `servers/workbench-page/outline.py _records` is the one
  renderer (id badge, headline, label grid, status pill, "more" fold) and
  still reads every pre-0.18.0 shape.
- **Discussion = open questions only, in plain words** (§💬 rewritten): a
  thread leaves the file when it settles and becomes one dated `-log.md`
  record, `D<nn> settled by JL: <ruling>`, argument kept under the fold.
  `check.py discussion-settled-thread` (proved 13 → 0 on the MISQ board).
  Board-wide id allocation now greps the log files too.
- **Log = a timeline of one-line records** (new §📜): `### YYMMDD · headline`
  (15 to 25 words), detail folded under. Restructuring an old row gives it a
  headline and moves its text under the fold verbatim; nothing is rewritten.
- **The requirement generator exists**: `cli/requirement.py` writes V (venue
  division: shape, moves, refusals, format values), N (Narrative row and
  Writing Style) and B (board hard rules, plain-English floor) records; run
  by `haipipe-draft-structure` ⓪ REQUIRE. Teeth: `requirement-missing`,
  `requirement-hand-edited`, `requirement-stale`. 15 MISQ section pages got
  their file; the 📏 chip now draws.
- **`### Stage Record` is a retired block** (`check.py retired-block`, JL:
  "why we have this? we should not have this"); 13 MISQ pages cut.
- Content: SM00, SM01, SM02, SM08 discussion and log rewritten (5/3/3/2 open
  threads; 20/19/25/22 log records); `.pre-0.18` backups beside each.
- Content, the other 16 MISQ pages (after the peer session's `## States` →
  `## Aims` merge): `## Aims`, `## Discussion` and `## Log` moved off every page
  into `outline/` records. Triage: a `Needs JL` or `Decision Now` row is a
  thread only if it has options, a lean, a ruling verb or a question mark (55
  threads, D43–D126); the other 76 rows are CC's own work and became
  `- [ ] A<g>.<n>` rows under `### A<g> · 📋 Open items carried off the page`
  in each plan; ticked rows and `### D<nn>` records with a decision became log
  records; page Aim rows merged their tick and `Now:` into the plan by id.
  `checks/outline.py` passes on every plan; `.pre-outline` backups beside each
  page; next free id D127.

## 0.17.4 — 2026-08-31

- **A feedback row carries the Round's words** (JL, reading SM00's 🗣 tab:
  "it lost a lot of informations"): `collect` now copies each §2B row's
  `Feedback:` and `Work:` sentences, the full concern of every parent R-row
  (`- **Parent R03**: … → routes SM00, SM03, SM06, SM08`) and the §2A
  proposed reader order, all verbatim. 0.17.0's head-and-ids-only rule
  confused "never AUTHOR here" with "never SHOW here"; a file regenerated
  whole cannot drift from its source. `landed:` still preserved by row id.
  Ledger-only rows (NA01) keep their closing quote in the head.

## 0.17.3 — 2026-08-31

- **One chip per sibling file on the 🧭 tab** (JL: "we should have more
  buttons here to host the content in the outline folder"): 📏 Requirement ·
  💬 Discussion · 🗣 Feedback · 🧾 Evidence · 📜 Log, each drawn only when its
  file exists, each read-only, with a row count on the chip. Verified in Chrome
  on SM01: `🧭 By part | 🚦 What is left | 💬 Discussion · 6 | 🗣 Feedback · 8 |
  🧾 Evidence · 28 | 📜 Log · 12`.

## 0.17.3 — 2026-08-31

- **`Routed:` is a folded line** beside `Note:`/`Answered:`/`Drawn:` (NA01
  field test: the phase named it in 0.11.0 and this file, both parsers, and
  the renderer did not know it; 8 of 16 lines vanished from the fold).
- The §📐 example reads `supersedes: none`, not the em-dash.
- Roster row updated to the six kinds; 0.17.1 and 0.17.2 had not touched it.

## 0.17.2 — 2026-08-31

- **`<stem>-evidence.md`, the sixth kind** (JL: "an evidence-status.md in the
  outline workbench, to check what is the current evidence status"): a dated
  snapshot of the 🧭 join, one bullet per line in the Evidence Bundle's six
  status words, written only by `cli/evidence-status.py` (imports
  `servers/workbench-page/outline.py`, so file and tab cannot disagree). Two `check.py` teeth,
  `evidence-stale` and `evidence-hand-edited`, each proven 0 → 1 → 0 on SM08.
  SM06 reports 37 owed / 0 landed, which is honest: its `probe/V01-…` and
  `display/S-Display-…` are retired shapes the contract cannot read.

## 0.17.1 — 2026-08-31

- **`<stem>-requirement.md`, the fifth kind** (JL 260830: "put the writing
  requirements as one subfolder as well"). FLAT, not a subfolder, because the
  0.17.0 layout rule reserves folders for many-files kinds and a requirement is
  one per page. GENERATED by the same `stage.py sync` that today pastes a
  sha256-stamped `### Writing Style` block into 17 MISQ pages (149 lines), from
  the venue row (`structure-source` + `structure-division`), the Narrative row
  (`style-from`) and `ref/writing-rules.md`; that page block is retired. Never
  authored (it would fork the consumer-neutral venue bank), never versioned
  (its sources carry their own); a page-specific deviation is a `D<nn>` thread,
  cited by id.

## 0.16.1 — 2026-08-30

Field test on SM08 (15 frictions, ledger 5 MATCH · 2 SKILL GAP · 0 EXPECTATION GAP):

- **`D<nn>` ids are BOARD-WIDE**, allocated from the board's max with a grep;
  the first run minted D01-D06 page-locally while SM06 owned D01/D05/D11, and
  `D16` was already duplicated between AM02 and SM04. A thread id is a
  cross-page address (cited from ten files), which is the same fact that keeps
  this file unversioned.
- **A live ask that owns no Aim becomes a 🔴 thread, never a minted Aim** (the
  run invented `A1.10`, a target nobody agreed to).
- The page keeps a `## Files` pointer at both moved files; header shape for
  both files; rows newest-first; `round: —` legal before the first Round.

## 0.16.0 — 2026-08-30

- **Three kinds in one folder** (JL: "outline workbench is a folder!!!!"): the plan
  `<stem>-outline-v<N>.md`, plus `<stem>-log.md` (what CHANGED, append-only) and
  `<stem>-discussion.md` (what was ARGUED, `D<nn>` threads with status/serves/
  round). `page.md` is the PRODUCT; this folder is the PROCESS. Neither new
  name may contain `outline` (the plan globs are `*-outline-*.md`).
- **`## States` is gone from the page**, finishing the 260819 merge: one Aim
  row carries tick + `Done when:` + `Now:`; live asks become the Aim's `Now:`.
- **The Aims stay with the plan and the page keeps no copy.**
- **The discussion is never versioned**: threads settle independently (D01
  closed while D05 stayed open), a thread id is a cross-page address, threads
  move between pages; `> ✎` already records edits; a status change owes one
  log row naming the id.

## 0.17.0 — 2026-08-31

- **Fourth kind: `<stem>-feedback.md`**, what OTHERS said, one file per Round
  (JL 260831: "it will have its own file and folder"). Rows are PROJECTED from
  the Round's §2A/§2B by `haipipe-block/cli/feedback.py collect`, never
  paraphrased; the page writes exactly one field, `landed:`. PULL, not push:
  the page collects during OUTLINE ⓪ and no Round writes into another page's
  folder. First run: 15 pages, 104 rows, from RD01 on the MISQ board.
- **The layout rule.** One-per-page kinds sit flat with the stem
  (`-requirement`, `-discussion`, `-log`); many-per-page kinds get a folder
  named by SOURCE (`<stem>-feedback.md`, `## RD01` inside). The plan is grandfathered flat.
- **Feedback ≠ discussion**, stated: discussion is authored here, feedback is
  received and may not be rewritten here.

## 0.16.1 — 2026-08-30

- Patched from the SM08 field test (15 frictions): `D<nn>` ids are BOARD-WIDE
  with the grep that allocates them (the run minted D01-D06 against SM06's
  D01/D05/D11; D16 was already doubled between AM02 and SM04); an ask owning
  no Aim becomes a THREAD, never a minted Aim; the page keeps a `## Files`
  pointer; header shape for both files; newest-first; `round: —` is legal.

## 0.16.0 — 2026-08-30

- **Three kinds in one folder** (JL: "outline workbench is a folder!!!!"): the
  plan, `<stem>-log.md` (what CHANGED) and `<stem>-discussion.md` (what was
  ARGUED). `## States` is gone from the page, finishing the 260819 merge; the
  Aims stay with the plan and the page keeps no copy. The discussion is never
  versioned: the unit that freezes is the THREAD, and a thread id is a
  cross-page address. Neither new name may contain `outline`.

## 0.15.0 — 2026-08-20

- **§✂️'s `Answered:` line gains the `· recount` tail** (JL: "看看哪里可以去
  优化"): it flags a value that counts the run's own artifacts so DRAFT knows
  the one kind of value it must re-read from the card instead of trusting the
  plan.

## 0.14.0 — 2026-08-19

- **The Aims live in the plan file** (JL: "Aims should be move together with
  outline"): §📐 gains the `## Aims` trailing section — one target plus its
  `**Done when:**` test per Aim — and the 🎯 tie diagram routes plan bullet →
  plan `## Aims` → page transcription → page `## States`. Before the move a
  renumbered plan pointed ids at the page's OLD Aims (nine of sixteen on
  QPw00 did).
- **§✂️ plain, common words** (JL, on `The control level.`: "不要用这样的词了"):
  a rare word fails even when apt; a technical term survives only as the
  thing's real name, defined at first use; metaphor vocabulary is rewritten
  to the plain thing it means.

## 0.13.0 — 2026-08-19

- **§✂️ concise bullets**: one bullet = a few-word HEAD (the point or the
  question) · evidence appends (`Answered:` / `Drawn:`, written by the fold
  when the card lands or the unit builds) · the end-anchored mark. The head
  never restates what lives behind its own mark (JL: "越 concise 越好…冒号后面
  的东西其实都有点喧宾夺主了").
- **Same night, the bullet's hidden detail**: every bullet folds a concise
  explanation behind a click — `Note:` (authored at OUTLINE) or the fold's
  `Answered:`/`Drawn:` — with NO disclosure marker; heads are terse labels or
  questions ("Figure for Whole Workflow Loop"). 131/131 bullets on QPw00
  carry one.
- **Levels styling**: paragraph rows show their own address + a short accent
  tick; one shared left-aligned address column aligns every title (JL picked
  the accent bar from four previews, then trimmed it to a tick).
- Coherence pass, same law: §🔒 qualified — the fold APPENDS `Answered:`/
  `Drawn:` (and `📮 PP<NN>` ids) into bullets in place, into the working file
  while `approved:` is ⬜ or into `v<N+1>` after a tick; §📐 counts FIVE
  display kinds (`illustration` added), its worked example now shows §✂️-style
  bullets (terse Capitalized head + folded `Note:`), and the ↩ example says
  "answered", not the retired "bound"; §🚧 no longer pins the sibling phase
  skill's version.

## 0.12.0 — 2026-08-19

- **📮 probe and 🧮 value are now SEPARATE marks** (JL: "You mean you put the
  probe and values together? I want to separate them"). 📮 = this point needs
  a QUESTION answered — bare before ② raises the card, `📮 PP<NN>` after; the
  answer may be a finding or a folder of numbers. 🧮 = this point QUOTES one
  value, `PP<NN>.v<n>`, out of an answered card's `## Values` block, and
  `checks/values.py` re-computes it. 📮 deliberately shares phase ②'s glyph
  (same concept) and is end-anchored in the scanners so prose about the phase
  never reads as a mark.

## 0.11.1 — 2026-08-19

- **🧮 widened from "a number" to "a probe-answered fact".** JL: "this point
  might need a probe to provide the evidence, do you get it?" — the mark IS
  the needs-a-probe mark, and the card already binds ANY answer by path; the
  `PP<NN>.v<n>` ids and `checks/values.py` recompute are the numeric
  specialization, not the definition. Bare 🧮 = probe needed · 🧮 PP<NN> =
  raised · ↩ ✓ = landed.

## 0.11.0 — 2026-08-19

- **The ✅ "have it" mark is RETIRED.** It asserted "backed on disk" without
  naming what backs it, so no machine could recheck it; an unmarked bullet
  already means "plain point, nothing owed"; and the glyph already works two
  other jobs (`approved: ✅` tick syntax, phase ⑦), which produced a phantom
  chip on a bullet that merely QUOTED the tick name. JL failed to read it
  three separate times. Zero plans carried it at retirement, so no alias is
  kept: an end-of-line ✅ in a plan is now just text. The mark grammar is
  four: 🧮 value · 📚 citation · 🖼 display · 🎯 aim.

## 0.10.1 — 2026-08-19

- **The value mark is 🧮** (JL: "🧮 maybe this one?" — he never liked 🔢).
  🔢 stays accepted as the legacy alias, so pre-260819 plans remain legal.
  The abacus was the proof mark retired earlier on 260819 and is revived with
  its new meaning: a recomputable number, which is what `checks/values.py`
  does to every one of them.

## 0.10.0 — 2026-08-19

- **Mark to workbench, written down once.** A mark names what a bullet OWES and a
  workbench names WHERE it is answered, so `🔢 value` is served by `probe/` and
  there is no workbench called `value`. JL asked for one on 260819; a fourth
  workbench would be a second home for one folder.
- **A paragraph carries 3 to 6 bullets.** The `### C<n>.P<n>` line is a brief
  the tab prints above them, and eight bullets under one brief means the brief
  cannot describe them. Split by idea, not by count.
- **🧮 proof RETIRED.** JL 260819: "我从开始到最后都没有说 proof，我一直说
  probe". The mark came from ONE transcribed quote ("citation, display, values
  and proofs") and no Log row ever ruled it. Going to a task folder or a
  discovery folder for the evidence behind a claim IS a probe, which is 🔢.
  It was the only mark with no workbench, no folder, no lane, no id and no
  backlink, and that was the symptom rather than a design.
  ⚠️ `proof/` the FOLDER is untouched: it belongs to a probe card.

- Six marks become FIVE: 🎯 aim · ✅ have it · 📚 citation · 🔢 value · 🖼 display.
- `servers/workbench-page/outline.py` drops 🧮 from `_MARK`, from `_live`, from the Evidence
  Bundle kinds and from the `owed` count. 48 marks stripped from 14 plan files.

## 0.9.1 — 2026-08-19

- **A bullet never carries a markdown heading mark.** JL objected twice in one
  session, to `####` inside a bullet and then to `` `## Opening` ``: they are the
  file's own syntax, so a reader parses them as structure before as a reference.
  Name the part in words or with the § anchor.
- The same rule stated for `## ` lines: only `## C<n> ·` is a division. A stray
  `## ` in a plan's preamble was counted as a phantom division and shifted every
  address below it by two. `servers/workbench-page/outline.py` now matches `^## C\d+` and nothing
  else, so the file and the renderer agree.

# CHANGELOG · haipipe-workbench-page

## 0.9.0 — 2026-08-17

Adds the derived Point-addressed Evidence Bundle. The outline surface joins
sentence scaffolds, Probe/Bibex/proof/Display resources, and owner feedback
without creating an `evidence/` copy or mutating the approved plan.

## 0.7.0 — 2026-08-17

**The plan is SKIMMED, so the evidence stops outweighing the sentence** (JL
260817, with a screenshot: "太肥太胖了 … 你把这些 outline 都给挤得不知道去哪儿
了"). 0.6.0 shrank the popover, which was the wrong target: the weight was in
the ROW.

```
                      was                          now
────────────────────────────────────────────────────────────────────────
chip placement        a sibling of .row's flex,    inside the sentence's
                      so each one was a COLUMN     own span, inline
                      that stole the text's width
chip shape            14px, 999px radius, 0 9px    10.5px monospace, 4px
                      → 22px tall, wrapped to      radius, 0 4px, nowrap
                      two lines beside a 19px row  → 17px tall, one line
note text             "Gray2021 in bibex/"         "Gray2021"
                      "no unit declared yet"       "owed"
                      "↩ PP04 serve this bullet    "↩ PP04 0/1"
                       · 0 of 1 answered"
row                   13px, 3px 0 1px padding      12px/1.4, 1px 0
addr column           62px, 600 weight             42px, right-aligned
```

Measured in Chrome at a 660px pane, same page, same 66 rows: document height
2017 → 1807 px, widest tag 143×22 → 124×17 px. The structural half (inline
instead of a flex column) is not in those two numbers, because CSS alone cannot
undo it; the screenshot pair is its evidence.

- 🚫 **No emoji inside a tag.** `⬜` and `📄` render at full glyph size in a
  10.5px tag and double its width. The dashed border and muted colour already
  say "not landed", so `PP01 answered 1📄 ⬜` is now `PP01 answered 1`.
- **A fact is never printed twice on one row.** The ↩ backlink is suppressed
  for a card the row already names as a chip, so `🔢 PP01 answered 1` no longer
  drags `↩ PP01 ✓` behind it. It still fires where it is the only speaker: a
  bare mark, or a bullet with no mark at all, which is the normal case since
  the plan is frozen before the card exists.
- **A plain bullet can now carry a ↩ too.** It used to `continue` before the
  backlink was computed, so a card serving an unmarked sentence showed nowhere.
- `&nbsp;` was written into a string that then went through `_e()`, so the plan
  card's header printed the five literal characters (`0 accepted &nbsp; aim 9`).
  Separators moved into the markup.

## 0.6.0 — 2026-08-17

**The evidence card is sized as a NOTE** (JL 260817: "现在我感觉这个 evidence
card 太大了"). It opens beside a 13px outline row, so a 34em/14px panel with
13/16 padding read as a modal. Measured in Chrome before and after:

```
🔢 PP01   512×131 px  →  339×120        📚 Deyo2015  367×86 px  →  327×64
🔢 PP03   512×109 px  →  339×101        width       34em/14px  →  25em/12.5px
```

- **A citation prints `Author et al.`**, not the author list. Six names is what
  made a 📚 panel twice a 🔢 panel's height, and the key in the panel's own
  title bar already carries the first author. `Dowell2022` went 235 → 144 chars.
- BibTeX's `---` prints as an EN dash, never three raw hyphens and never an
  em dash (JL's standing rule).
- **A chip no longer prints its id twice.** `🎯 A4.2 → A4.2` was visible in the
  260817 screenshot: with an id the note stays empty, and only a bullet with NO
  id spends the note on saying it is untracked.

Also in this pass, and it is the reason the size question got asked at all: the
🧭 join read a card's state through `raised`/`working`/`bound`, three words
`haipipe-workbench-probe` 0.7.0 had retired, so two ANSWERED cards on
`QC1-visitlbp` rendered `⬜ 0 of 1 bound`. The join now resolves through the
protocol's own ladder (`_pstate`), keeps the retired words as aliases, counts a
`read` card toward `accepted`, and prints `all answered` / `2 of 3 answered`.

## 0.5.0 — 2026-08-17

**🧮 proof earns NO folder**, closing the ⬜ this file opened on 260817. The
ruling is `haipipe-page-probe` §🧭's: a proof lands as prose, and the pulled
file a derivation rests on already lives in a probe card's `proof/`, so a
second home for the same material would be one thing filed twice. A 🧮 bullet
carries no id and no card backlinks it.

## 0.4.0 — 2026-08-17

**The PHASE moves out to `workflow-runs/haipipe-draft-structure`** (0.1.0, same
day). This file kept both the material and the phase's rules while the phase had
no home; now it states neither twice and points at the contract instead. DRAFT's
own §🗂 was trimmed at the same time and no longer owns the outline.

**Each evidence ref opens as the board's own evidence card** (JL 260817: "我想让
它有点像那个 evidence card 一样"). Chip in the line, popover panel beside it,
holding the THING itself as `haipipe-sentence` §🃏 requires: the reference as
printed, the probe card's own question, the display unit's own claim.

- Native `popover`, no script: deleting every `<script>` must leave the panel
  readable, and it is real body text rather than a `title=` attribute.
- The class is `.evchip`, NOT `.chip`: the lens toggle buttons already own
  `.chip` on this page, and reusing it made the two fight (found by driving it).
- Two parser bugs fixed the same way: BibTeX `{CDC}` protects capitalisation and
  is not part of the title, and a README `claim` wraps onto the next line.

## 0.3.1 — 2026-08-17

**📚 means a published work, never a sibling board page** (JL 260817 asked
whether C1 should have citations and why there were so few). It had NONE: the
page's `bibex/QC1-visitlbp.bib` held zero entries, and the three 📚 marks in its
plan pointed at `QB1`, `QB2`, `QB3`, which are board pages.

- `_disk_state` now reads `bibex/*.bib`, so a 📚 is checkable like 🔢 and 🖼:
  `in bibex/` · `🚨 not in bibex/` · `🚨 <id> is a board page, not a citation`.
- A cross-reference to a sibling page is a different act from a citation and is
  written in the bullet's own words, without the mark.

## 0.3.0 — 2026-08-17

**A bullet is a POINT, not a sentence** (JL 260817: "一个 bullet point 我们可能有几个 sentences 去 cover，所以我感觉可能还是 B 比较好"). The proof was in the plan's own text: one bullet listed six OLS specification families, which is plainly several sentences, not one.

- The address is `C<n>.P<n>.B<n>`. One `B` becomes 1..n `S` at REVISE, and
  `C<n>.P<n>` is shared with the sentence address so the link survives.
- `haipipe-sentence` keeps `S` on the rendered page. Neither redefines the other.
- `C` STAYS and is not decoration (JL asked why): Aims use `A` and page-wide uses
  `P` in that same slot, so dropping it would collide `C1` with `A1`. It prints
  ONCE on the section heading; the rows carry only `P<n>.B<n>`, the part that
  changes.

**A bullet with no mark is the normal case, not a defect.** 0.2.0 required a mark
on every line and flagged bare ones 🕳. That made the plan unreadable and buried
the few lines that actually owed something. A mark is now the exception, written
at the END of a bullet, because that is where the card will hang on the real
sentence.

**THE PAGE NOW folds shut** (JL 260817: "第二部分还有必要要吗？我感觉有点
confusing"). The tab shows two halves answering two different questions, and
neither was labelled: 🧭 THE PLAN, what the page said it would cover, and
📄 THE PAGE NOW, what is written today. Both are labelled now and the second
collapses to one line, since on a page whose aims carry no ids it was nine empty
cards in the reader's way.

- Empty-division wording fixed: "nothing lands here yet" read as "this part is
  fine". It now says "no aim, state or file on this page names this part", which
  is the actual reason.

## 0.1.0 — 2026-08-16

First contract for a workbench that had already SHIPPED without one.

- The engine, checker, and drawer JS landed in commit `711b964c` ("Ship the
  pagex and outline workbenches"), and QPf12's own state line recorded the gap:
  `open: marks on old pages, workbench skill`. Without a SKILL.md no agent could
  discover the surface or knew what `§N` meant, so pages kept being written
  with every aim unanchored.
- Records the four facets as built: storage NONE (live, storage-less, the QPf1
  folderstat precedent), writer NOBODY (rule-based, no model call at render
  time), surface `GET /_board/outline` with the 🧭 By division and 🚦 By
  progress lenses, boundary deliberately OFF the workbench roster as a meta-surface
  twinned with 📂 folder.
- Adds the DRAFT link (JL 260816, "is that before the draft, we should also have
  a outline for this page as well?"): this tab is WHERE a DRAFT outline is read
  and approved. DRAFT writes the material — divisions, `### A<n>` groups, `§N`
  anchors — and the surface reads it back. No outline phase and no outline file:
  a fifth phase would only take DRAFT's authority over what divisions exist.
- States the one-click test: a page whose 🧭 tab is one big 🌐 card has no plan
  yet, only prose.
## 0.45.1 · 2026-09-06

- Align the Evidence Item table's EMBED reference with the next
  `v<G>.<S>.<E+1>` evidence revision.
## 0.74.0 · 2026-09-14

- Hard-cut the retired `outline/*-evidence*.md` and `outline/evidence/*`
  locations: they are no longer compatibility inputs or renderer sources.
- Require old Evidence material to move to
  `_archive/legacy-outline-evidence/` before a Page is v4-ready; current
  Evidence reads only `results/**/result.yaml` and its payload metadata.
## 0.77.0 · 2026-09-14

- Align the Outline entry point with the minimal Run Space projection:
  Page Writing, Page Evidence, and Supporting Runs, with Value/Display/Citation
  labels matching the reader-facing cards.
