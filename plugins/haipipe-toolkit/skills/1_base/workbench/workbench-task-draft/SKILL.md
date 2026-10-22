---
name: workbench-task-draft
description: >-
  The Page workbench of one Page, paired with servers/workbench/workbench-task-draft: three
  Spaces (Draft, Evidence, Delivery), each with its content on the left and
  its own Runs panel on the right, over the Page's draft/ folder. Draft reads
  the three-section Draft Markdown (Table, Reading, Scratch, Revise); Evidence
  reads the Evidence Markdown and its Results (Citations, Displays, Values,
  Supporting Runs); Delivery shows the built web, LaTeX, Word and slides
  files. The Runs panel lists each view's run types from run-cards.md and
  copies prompts; it starts nothing. Also owns the 📂 Folder tab. Trigger:
  page workbench, workbench link, Draft Space, Evidence Space, Delivery
  Space, Runs panel, run type, run card, add a run button, draft folder, plan
  file, record shape, evidence bundle, delivery tab, folder tab, stale
  workbench, workbench-page, /workbench-page, /workbench-task-draft.
metadata:
  version: "0.104.15"
  last_updated: "2026-10-20"
  # version history: ./CHANGELOG.md (skill-scoped, never loaded at invocation)
---

# /workbench-task-draft · three Spaces, Runs on the right

Code: `servers/workbench/workbench-task-draft/` (this skill is its manual; it was called `workbench-page` until 2026-10-16, s41-D14).
The folder holds the whole draft Task type: `task_draft.py` lays out the frame's Spaces for a Task whose face says
`task-type: draft`, and the other modules are the views it embeds (s41-D15: one folder per Task type, `workbench-task-<type>/`).

## 🪜 A draft Task on the frame · seven step tabs (b32 s41, built 2026-10-20)

A Task whose face says `task-type: draft` opens in the frame with Work as seven step tabs, the s41 design
(JL 261015: "So it is the Studio, 1, Plan, ..... and Delivery as the last one"):

```text
Description │ Report │ Work │ Runs
Work:   Studio · 1 · Plan · 2 · Write · 3 · Evidence · 4 · Display · 5 · Revise · Delivery
        each tab: Operation (Input · Sign · Prompt + user feedback) over Result (folded cards)
Report: the same seven, Results only · Table · Questions
```

- `draft_steps.py` draws the tabs; `task_draft.py` lays them out (`DRAFT_TASK_SUBS`, `DRAFT_TASK_RUNS`). Nothing here writes.
- Every open reads the files again (s41-D28): the newest `draft/<stem>-draft-v<N>.md` (its header, `## 1 · Structure`,
  `## 2 · Scratch`, `## 3 · Draft`, `approved:`), `draft/records/` (`<stem>-context.md`, `-requirement.md`,
  `-revise.md`, `-feedback.md`), `draft/previous/`, `evidence/cards.yaml` and `proposals.md` (haipipe-evidence
  `cards.py`), the Block's Studio topics whose face names the Task, and the Block's `delivery/<jNN>/<tNN>/`.
- Each tab's chip comes from those files: Plan is `✍ sign` until `approved:` starts with ✅; Revise counts passes
  by `draft/previous/`; Delivery is four boxes (build, render, check and Send, read back).
- A bare Work link opens the first step that waits (`→ next`, `✍ sign`, `✍ send`); the Studio is optional.
- Description is the face alone: its old Plan, Requirement and Records are cards of 1 · Plan. An old link
  (`sub=Draft-Scratch`, `Evidence-Value`, …) opens the step that took its place (`OLD_SUBS`).
- The prompt's notes stay in the browser and go out with Copy as `user feedback:`; a pasted image is not kept yet.
- Your own words: 2 · Write opens, in Work and in Report, with the Page's Revise boxes (`outline_revise.py`,
  embedded): one paragraph per box with no frame, one sentence a row (a long one wraps inside its row, a faint · where
  each row starts; Enter starts a row; JL 261020: "howto make this each sentence a row?"); on save the rows are cut into
  sentences and each Bullet
  takes the run of sentences that reads most like its old Draft (nothing dropped; a ⟦pending⟧ mark stays its own). It saves
  into `## 3 · Draft` when you leave it or press Cmd+Enter, Esc puts back what it held, and the first save on a paragraph
  opens `run-revise-<cN-pM>` (JL 261020: "How could I write my own changes?"; "what if I want to revise it myself?"; "i
  don't like the box, could you remove it?"; "How could we make the editing to be more easier and free style here?").
  5 · Revise has no editor of its own (JL 261020: "remove this Change it yourself in the Revise, as that will be in the
  Writing"). Every Operation box opens folded, its chip still showing the step's state ("please make all the operation
  to be hidden by default").
- While an agent works on a step, a ⏳ Running now line sits under Operation (what, since when), read from
  `draft/records/<stem>-running.md`, one `- [<step>] <what> · since <time>` line per open run, which the agent writes
  when it starts and removes when it ends (JL 261021: "如果在跑的话，能不能在这个页面里面显示正在 running？").
- 5 · Revise's Result is one card: the text on the left, its Revise cards on the right in reading order. The text is
  one column with no space between sentences, the same as 2 · Write's (JL 261020: "句子跟句子之间不要有空格"): each card
  is placed at its sentence's line and pushed down only to clear the card above (CARDS_JS `align`, for any `.rv-split`),
  the text never moves for a card and stays in view while the cards scroll. Above this card sits the pass's own
  section, 📋 Revise Review Report: the reviewer, the verdict, one row per rubric axis (Mechanics, Function, Evidence,
  Readability, Coherence, Anti-AI writing, and the venue's rule) with its verdict, a score out of 10, how the draft reads
  and the smallest fix, the mean score on top, then the paragraphs
  now against proposed; nothing to accept (JL 261021: "把那些比较详细的 review report 单独作为一个新的 section").
  Cards on the whole Section stay above the text, the full width. Hovering a card (or one of its rows)
  lights its sentence, and a sentence lights its rows. ✓ Accept all in the header accepts every card still proposed, one
  after another, and leaves the decided ones (JL 261020: "I will just accept all the changes here") (JL 261020: "merge them together, one in the left, and one in the right? so we can link to the original
  text"). Only the latest pass shows (the file keeps only it; older passes are in git). A card is one light box; a
  Section question on the paragraph plan is a table, now against proposed; a change over several sentences is a row per
  sentence ("this should be sentence by sentence"). Each card has ✓ Accept · ✗ Reject · ✎ Edit · ↺ Undo; a click writes
  only that card's `State:` or `Expected:` in `draft/records/<stem>-revise.md` (`POST /_board/draft-card`,
  `draft_steps.card_act`; refused when the card changed on disk since it was shown). The text changes only when "apply
  the accepted cards" runs (JL 261020: "我想要那种可以交互的感觉"). Below it, the Section canvas, which may hold other
  papers' openings beside ours (excalidraw-draft `examples:`).
- The text column reads as prose in 2 · Write, 3 · Evidence, 4 · Display and 5 · Revise alike (JL 261021: "现在的
  layout 读起来 ... 比较乱糟糟的"; "把字体变大一些"; "像 S5 这种东西能不能放到最左边"): 17px type, no bullets, each
  sentence's number hung in a left gutter so every sentence starts on one line (`_sentence` gives the number and the
  words their own spans, `.s-no` and `.s-tx`), and `\citep{…}` read as its keys in small grey. In 5 · Revise only, the
  evidence stays boxed but its CITE labels go ("I think we still need the box"); 3 · Evidence keeps both.
- 📋 Revise Review Report also shows Each sentence, in its context: the report's `Sentences:` lines (haipipe-draft-review
  `ref/sentence-logic.md`) as a table of logic and read scores, the link from the sentence before, the problem and the
  smallest fix, then each paragraph's flow (JL 261021: "每句话都要看一下上下文 ... 给每句话打分"). Cards already written
  into the text, and comments their person closed, are hidden until Show the <n> finished ("如果已经结束的话，就把它 hide
  掉吧").
- A card whose fix is a choice shows its options (`Option A (<approach>): <sentence>`, `Chosen: A`): the chosen one as
  its change, the others as plain sentences, each with ↳ Use <letter> ("可以用 A、B、C 几个不同的方法去修改"). A comment is a
  thread with You and AI marks and small text actions ("不应该有个 AI Reply 吗？ ... modern 的 UI"). The review's sentence
  lines are Logic cards, one beside every sentence (logic and read scores, the link, the problem in one line, the fix
  on click), and each paragraph's flow sits under its last sentence ("这个 sentence 应该当做一个新的 type ... logic
  comments ... 应该是放到右边的"); the report keeps only their sum. Every card is one compact line until clicked, as
  comments in a shared document are, so each stays beside its sentence. Hide comments, Hide logic and Hide edits
  filter the column.
- 5 · Revise's column holds four kinds of card, each switched on or off by its chip above the text, in any mix
  (JL 261021: "叫 comments、logic、edit 这三块，然后我们选中其中一个，或者把那三个全都选中 ... 这里最好也加一下 evidence"):
  Comments, Logic, Edits (only those still open: proposed, or with options) and Evidence (each sentence's items, the
  rows 3 · Evidence shows, named by their paper's key or value in one line). No Accept all, no Show finished. An Edit
  card is a choice: its options A, B, C, then "drop it: keep the original", one radio each, and Confirm. A Logic card
  says its quality in a word (good, passes, weak, needs work, broken) before its two scores. Resting the pointer on a
  sentence makes it the focus: its cards light up and slide level with it, centred on it. A card
  opens over the cards below when pointed at and folds when the pointer leaves; a click pins it.
- A Table or Figure the text calls shows under the first sentence that calls it, in Write, Evidence, Display and
  Revise alike (`_embed_displays`; JL 261021: "PNG TO EMBED UNDER THAT SENTENCE"): the unit's preview.png, opened full
  size on click; a link to preview.pdf when only that exists; "not built yet" when the unit has no picture. The unit in
  display/ and the Run that made its asset stay the source; LaTeX takes its PDF, Word and the web its PNG.
- Every word on 5 · Revise lives in a Markdown file, never in the page (JL 261021: "这些 content 它是要存到 Markdown
  上的，不能存到 HTML 里面"): the text in `draft/<stem>-draft-v<N>.md`, the cards and the report in
  `draft/records/<stem>-revise.md`, the comments and their replies in `<stem>-comments.md`, the rulings in
  `<stem>-revise-rules.md`. A click writes only those files (`card_act`, `note_act`, `plan_act`); the page is built
  from them on every open and keeps nothing itself, no browser storage. What is shown or hidden, open or folded, is
  the view's own and is not saved.
- A person's comments live in 5 · Revise, among the cards (JL 261021: "我选中一个句子 ... 点个加号就能加注释 ... 放到
  Revise 的那一栏里面"; "我还是在这个 review 里面加 comments"). A + on the right of each sentence ("能不能把这个加号
  放到右边"), shown on hover, or 💬 Comment
  under words selected in one sentence, opens a comment card in the right column, in reading order before the cards on
  that sentence; Save writes it to `draft/records/<stem>-comments.md` (`POST /_board/draft-comment`,
  `draft_steps.note_act`: add · reply · done · reopen · delete, refused when its state changed on disk). A sentence a
  comment still waits on shows 💬. Each pass answers the open comments (haipipe-draft-writing ref/revise.md): the card
  that changes the sentence says `Answers: Comment <n>` and shows 💬 answers Comment <n>, the comment shows ↳ that card
  and the pass's Reply, and its person closes it with ✓ Done or ↩ Reply (it opens again). The cards' header has
  Copy: revise with my <n> open comments while one is open ("你的 change 怎么跟我的 comments 一起来做交互").
- 3 · Evidence's Result is laid out as 5 · Revise's: the text one column with no space between sentences, and at each
  sentence on the right its card, a one-line row per Evidence item that backs it, what backs it on hover (JL 261020: "I
  want it to be left to be the orignal text, and the right to be the evidence"; "我想要保证这个 draft 在 revise、evidence、
  display 这里都保持一样的风格 ... 所以句子跟句子之间不要有空格"). A card sits at its sentence's line, pushed down only to clear
  the card above (CARDS_JS `align`); the text stays beside the cards and scrolls itself to the sentence a card lights
  ("I want s7 to be aligned with evidence item"). Each item has an id, its card and
  its place there, CITE 1.4 or VALUE 2.1 ("should the evidence item have some index as well?"), the same id on the
  text's mark; hovering a row lights its sentence and a sentence its rows. Under it each Evidence card has its own fold
  ("To show each evidenence card seperately?"), then the Asks. A card is a topic, the Task its items come from or would
  be made in (haipipe-evidence `cards.py by_topic`); VALUE was WORK until 261020.
- 3 · Evidence also shows every point still open, card or no card (JL 261021: "我们的 evidence 该怎么把这些不确定的 ...
  都加上去"): each ⟦…⟧ in §3 (⟦check: …⟧ a source not yet verified, ⟦pending …⟧ or a one- or two-word ⟦x⟧ a value a
  Run has not given, any other a source still to find) and each §1 point whose line says `Evidence: none · <why>`. Each is
  OPEN <n> in reading order, a row in its sentence's card after the evidence rows (❓ to check or find, ⏳ waits on a
  Run, ⚪ no evidence), and all of them in one fold, `❓ Open points`, the ones to check or find first. Input counts them,
  the prompt asks for an item for each (or leaves the paper's own reasoning), and one to check, find or wait for keeps
  the chip `🔶 asked` (`draft_steps._open_points`).
- 4 · Display (JL 261020: "a new display view after the 3 - Evidence? ... Please do it"; b34 s41 Open 1): the Section's
  displays, each a unit `display/Display<n>-<slug>/` (haipipe-display), else a unit still in a display Run's newest
  pass. A unit is DISPLAY <n>, linked to the sentences that call it by what its README calls it (`shown as:`, else a
  Table or Figure in `label:`, its heading or its Placement) or by its `\label`; a call no unit answers shows as not made
  yet. The Result is laid out as 3 · Evidence's, each display's card at the first sentence that calls it (its
  picture, its claim, ⬜ planned, ✍ to accept or ✓ accepted), then each display folded on its own, full width with its
  kind, layout, built_on, status and files. Its chip is `✍ sign` while a built unit waits for `accepted:` (only a person
  writes it), `· optional` when the text calls no Table or Figure. Revise moved to 5 · Revise; `sub=4 · Revise` still
  opens it (`OLD_SUBS`).
- 1 · Plan holds the Scratch (`outline_scratch.py`, embedded): a note per paragraph, `## 2 · Scratch` (JL 261020: "I think
  we should move the scratch here"). Report shows the prompts of 1 · Plan, 2 · Write and 5 · Revise too ("for the plan
  here, I cannot see the input").
- 1 · Plan's Result is §1 as one mind map (`draft_steps._plan_map`; JL 261020: "merge them together, how do you think
  you can draw the mind map for the plan? ... To show what is this paper about?"): the Section and its `arc:` in the
  middle, its parts (`C1`, `C2`, …) when it has several, each paragraph with the Structure Overview's `→ C1.P2: …`
  question on the arrow to the next, each Bullet a leaf (S number, role, words, its Evidence cards); a Bullet's Note
  shows on hover, a ⟦check⟧ in it in red. It replaced the paragraph table and the Bullets table.
- The map is edited in place ("how could I operate and edit it?"): a point's words or role, a paragraph's name, a
  question, the arc; Enter after a point or ＋ point adds one (`S4a`, after the point above it), emptying a point takes it
  out, dragging its S label moves it; ＋ paragraph adds one after a paragraph, named first, and the paragraphs after it
  move down a number in §1, §2 and §3; an empty question slot takes a new one ("How could I add the P here or add the S
  here?"). Each change is one `POST /_board/draft-plan` (`draft_steps.plan_act`) into the newest draft's §1, refused
  when the words changed on disk, a newer draft exists, or §1 is signed.
- 1 · Plan's Result also holds the examples, as the Section canvas that draws them beside ours (a topic named by
  another's `examples:` is shown once, inside it), else a frame onto the topic that reads them (excalidraw-read's
  `reads/<pNN>/reading.yaml`), and `📏 Requirement and Rubric` (the desk rule, ours beside each example paragraph
  by paragraph, the four axes).
- A step's Copy prompt ends with the Task's session (`session:` on the Task face, else the Job face): pasted into
  any session, it tells that session to send it on to the named one, or to do it when that one is not running.
- A Section's Studio topic is one whose face names the Task; a face naming `jNN_…/tNN_…` paths counts only for those
  (two versions often share a Section's name).

> ⛔ **Generated files: never modify them directly; change the code that writes them (or its source), then rerun it** (hard rule, JL 260928; AGENTS.md rule 6). Here that means the workbench views and the `delivery/` artifacts its export doors write (`*-view.html`, `.tex`, `.pdf`, `.docx`, `index.html`): fix `servers/workbench/workbench-task-draft/` or the Page source, then rebuild.

> ⛔ **No content hashes** (hard rule, JL 260928; AGENTS.md rule 9). A version is its number and date; staleness is file time. Never write, check or compare a sha256 in a Page, Result, record or workbench view.

**LOAD `workbench` FIRST.** It owns what any workbench is: storage,
surface, writer, boundary. This file owns the Page workbench's delta: what the
three Spaces show, what the Runs panel does, what `draft/` holds, and who
writes each file. `Space` is the name for a user-facing surface; `Workspace`
survives only in old routes and internal ids.

```text
📃 <page title>
↑ Board level
[ band: page kind · state · draft version ]
[Guide] [Draft] [Evidence] [Delivery]
┌ one box per Space: tabs, Views, content ──────────────┐ ┌ Runs, right ──────────────┐
│ Draft     Table Reading Scratch RoadMap-Draw Revise · ▸ Structure │ │ the run types of THIS view │
│ Evidence  Citations Displays Values Supporting Runs         │ │ + New Run                  │
│           View: All items · Card · Source                   │ │ one run: name · state ·    │
│ Delivery  Web LaTeX Word Slides (each with its state)       │ │ Rerun · ▸ Prompt (Copy) ·  │
│           View: Preview · Artifacts · Checks                │ │ process · results          │
└──────────────────────────────────────────────────────┘ └──── ▸ folds to a strip ──┘
```

**Shared shell (JL 261003).** The page wears the shell every workbench shares
(`servers/README.md` "Adding a workbench"; `_host/tests/test_workbench_conformance.py`):
the title, the `↑ Board level` link when the Board has a Board-level workbench
(no `all boards · board index` line, JL 261003), a band read from the page (`page-type`, `state`, the
latest draft version), then the Space row with the shared Guide first and plain Space
names. Each Space's Views and content sit in one box (`.space-split>.space-main`), and
its Runs panel starts folded to the strip until the person opens it (`panel_html(...,
folded=True)`; a person's own fold or open is remembered). The shell's colors and tab
sizes are the Insight workbench's, kept once in `space_views.SPACE_CSS`, which Page and
Paper share. Guide reads the `page` entry of `workbench/guide_families.py`:
`description`, the Workbench Table `ref/workbench-table.md`, the papers
`servers/workbench/workbench-task-draft/related/papers.md` (`table-papers`),
Method's page `servers/workbench/workbench-task-draft/guide/method.md` with its cards in `guide/methods/` and its editable
methods canvas `guide/methods.excalidraw` (the canvas is the source), and RoadMap Draw's **Workbench design**,
`servers/workbench/workbench-task-draft/studio/page-workbench-design.excalidraw`, the design authority
below (hand-made; Part 0 is the shared shell).

Design authority: `servers/workbench/workbench-task-draft/studio/page-workbench-design.excalidraw`.
Change the drawing and the code together, and check every view in real Chrome at
about 2000px wide (a narrow window is not the test).

## 🧼 UI rule · as concise as possible (JL 260927)

Show content and the controls that act on it. Before adding a hint, count, id,
status line or breadcrumb, ask whether JL would click or read it; if not, leave
it out and put the explanation in docs. Removed on JL's request, never to
return: the Page bar, `⧉ run-*` copy chips, evidence chips under paragraphs
(`E01 ✓`), run sub-lines (`targets · v001 · s001`), the Structure jump line
(`C1 › P1 · P2`), sentence counts, the Runs header crumbs and totals, and short
`rp-` ids on screen (since 260928 the names on disk are readable too).

## 🔗 Link and routes

Return the short address by default: `<DOMAIN>/w/<board-slug>/<page-id>` for a
Board-hosted Page, `<DOMAIN>/w` for a standalone one. `<DOMAIN>` is the origin
the reader uses (AGENTS.md § Board serving). The Board host (`serve.py`) reads it
from `.server_config/settings.env`; a standalone `page.py serve <page> --port N`
binds `127.0.0.1` unless started with `--host` and `--public-url`, so only a
loopback or port-forwarded link reaches it. The server redirects it to
`/_board/draft?path=…&file=…` and composes `path` and `file` itself; the old
`/_board/outline` address still answers. Label it `Workbench Link`. Follow the
redirect and read one real value off the response before returning any link.

The Page views are the frame's Task Spaces (JL 261007: "why not merge them into the base"). A
Task's Page opens in the base frame, `/_board/workbench?path=<task>`, and each view is a subspace
drawn in place: Description › Folder, Audience Report › Draft, Work Details › Evidence · Value,
Runs › Page Runs, Delivery › Lanes. A tab link of a Task's Page (`/w/<block>/<page>/<tab>`) opens
that Space; a Page outside a Task folder keeps its own view. One route serves every view,
`/_board/workbench?view=<draft|evidence|value|runs|delivery|folder|pageruns>&path=<page .md>`;
the old addresses (`/_board/draft`, `/_board/runs`, `/_board/folderstat`, ...) answer as it on a
GET, and each POST twin keeps its address.

```text
lens=div | evidence | delivery | run      which Space opens (run = the All-runs view)
view=table | reading | scratch | revise   the Draft view
focus=C<n>.P<m>.B<k>                      Bullet permalink: opens, scrolls to, marks that Bullet
run=<exact run id>                        opens the All-runs view at that Run
/w/runs · /w/delivery · /w/folder · /w/evidence   tab words ride on the short address
```

A writing Step handoff follows `../../draft/haipipe-draft/ref/user-check-packet.md`.

The Page shell's tab strip is 📃 Page (this workbench, first and default),
📤 Delivery (the full lane surface, `ref/delivery.md`) and 📂 Folder
(`ref/folder.md`); a Page with `labeling/` adds 🏷 Labeling.

## 🗂 The folder · product beside process

`<page>.md` is the PRODUCT: what the Page asserts. `draft/` is the PROCESS:
how it came to assert it (Page skill 0.118). The same layout is legal on any
unit, Task folders included.

```text
<page>/
├── <page>.md                          the Page Face; Delivery reads it
├── draft/
│   ├── <stem>-draft-v<G>.<S>[.<E>].md the ONE current plan: three sections (below)
│   ├── <stem>-evidence-items.md       Evidence Item contracts: ## Citations · ## Displays · ## Values
│   ├── records/                       context · requirement · discussion · feedback · files · log
│   ├── previous/                      every superseded plan version
│   ├── skill/                         ranked Page Skills (ref/skill-record.md)
│   └── _archive/                      old Outline evidence; migration only, never read
├── runs/<name>.md                     one ticket per run, flat (written when it opens)
├── results/<name>/                    one folder per run, the same name (written when it closes)
├── delivery/                          web/ latex/ word/ slide/ (generated)
├── workflow/                          machine receipts
└── studio/                            the person's own drawings and notes
```

The Draft Markdown has three sections that repeat one skeleton
(`### C<n>.P<m>` headings, `- B<k>` numbers); `haipipe-draft` SKILL.md
§ "The Draft Markdown and Runs beside the content" owns it:

```text
## 1 · Structure · Bullet Point Table   ### Structure Overview, then each Bullet's Point and plan lines
## 2 · Scratch · What to write here     rough notes under each paragraph heading
## 3 · Draft · Reading and Revise       the sentences, one line per Bullet
```

Readers never parse the sections themselves: `src/plan_layout.py::to_canonical`
folds them into the one grammar in `ref/plan-grammar.md`, and every writer hands
its edited plan to `from_canonical`. `src/outline_version.py::plan_dir` finds
`draft/` first and still reads an unmigrated Page's `outline/`;
`page.py draft-layout <page>` migrates one Page or a whole tree. Every record is
found through `record_path`. No run list, date or history belongs in either
Markdown.

**Evidence names.** The stored id keeps its form (`E13-DISPLAY-cohort-overview`,
sealed Results carry it). People read the type-first short name
`Edisplay13`, `Ecite25`, `Evalue01` (`src/item_table.py::short_name`, JL 260928).

## 📝 Draft Space

The View row comes first, as Guide's (a rule under it, no "View" label; the file
and section each view reads is its tooltip); the Structure card shows in Table only.

1. **Structure card**: one folded line, `▸ Structure`. Open, it shows the
   Structure Overview (a division by its title, a paragraph by its title, its
   sentences and job, and the question leading on). Click the text to edit it
   as a box; Save (`action: structure`) renames or reorders headings in all
   three sections and saves the `→` lines. A paragraph that holds points cannot
   be dropped or re-addressed here; that is `run-structure` work.
2. **Reads**: which file and section each view reads, as the View row's tooltip.
3. **Table**: each Bullet's Point (section 1) beside its sentence (section 3). Read-only.
4. **Reading**: the sentences as prose (section 3). Read-only.
5. **Scratch**: the person's rough notes (section 2). Clicking a heading opens
   its note form; the first note opens `run-scratch-<c1-p2>` (its ticket
   only); later autosaves change only the notes; `Finish Scratch` asks for a
   short Summary and is the close (`results/`, one log line). It never edits
   Draft prose.
6. **RoadMap Draw**: the Section's logic as a tree (JL 261003: "the logic just go to the
   roadmap draw"), on an editable canvas at a fixed 640px height, read left to right: the
   claim at the left, each box splitting into the reasons it rests on, the Bullets as
   leaves (role and gist; solid green when their Evidence Items are verified, dashed
   orange while one waits). Each Bullet is its own row in one column, a Bullet that
   supports another just under it, stepped in, and the space right of the column stays
   free for writing (JL 261003).
   The drawing `studio/<stem>-roadmap.excalidraw` is the source of the logic: an agent
   draws its first version (Runs › Draw the logic; skill `0_utils/draw-logic-tree`, which
   owns the tree's rules and its `--check-scene`), then the person edits it here and every
   stroke saves through Studio. It never replaces an existing RoadMap without `--force`.
   With no drawing the View says so; rendering writes nothing.
7. **Revise**: one box per paragraph, pre-filled with its Draft (or the Page's
   own sentences where no Draft exists), one sentence per line, a blank line
   between points. `Save` or Cmd+Enter (`action: revise`) writes the changed
   Draft fields only. The first Save on a paragraph opens its Revise run,
   `run-revise-<c1-p2>` (`haipipe-draft-writing (ref/revise.md)`), whose ticket keeps the
   text before; later Saves change only the Draft; `page.py close-run` writes the
   Before / After ledger when the person says close. The status line under the
   box says `Saved · run-revise-0929-c1-p2 · 1 sentence` at once; the Runs panel is
   built with the page, so the run appears under Revise edits after a reload. No
   timer save; leaving with unsaved text asks first.
   Adding or removing points is Structure work.

Clicking a paragraph (its header in any view but Scratch, or a line in
Reading) selects it: the paragraph is outlined and the Runs panel narrows to
it; a second click clears it. The header click selects and does not fold (the
Scratch opener in `outline_scratch.py` cancels the fold outside Scratch view; a
read-only host has no Scratch opener, so there it also folds).

## 🔎 Evidence Space

1. **Reads line**: `draft/<stem>-evidence-items.md`.
2. **Tabs**: Citations · Displays · Values, each with its item count, then Supporting Runs.
3. **All items**: a table (ID · Item · Used by · State · Card), one row per item.
4. **Card**: the Result-first evidence page (`/_board/evidence`) in a frame,
   showing only the current tab's kind; its duplicate header and count row are hidden.
5. **Source**: that tab's section of the Evidence Markdown.

Selecting a row, or opening a card in Card view, selects that item: its row is
outlined and the Runs panel shows its runs. Switching to Card with a row
selected opens and scrolls to that card; a `Card` button on a row does both.
Used by is the item's Bullet address, from the Result, else the ledger target.

**Supporting Runs** (JL 260928) shows the work the items stand on. It reads
each current item's `Supporting Runs` line (`Execution · reuse · b03j02t01r04;
…`), resolves every address through `live.runs.supporting_task_runs`, and draws
one tree: Execution or Discovery > Block > Job > Task > Run, each Run by its
ticket name with its state and one chip per Evidence Item it feeds. A chip
opens that item on its own tab; a Run selected in the tree narrows the Runs
panel, whose `Task runs` (haipipe-task) and `Discovery runs` (haipipe-discovery)
types list the same Runs with their Result files. An unknown address shows under `Not found`. A Supporting Run's owner
stays its Task or Discovery folder, never this Page.

Five layers stay distinct (full binding contract:
`../../draft/haipipe-draft/ref/page-run-families.md`):

```text
Evidence Item   authored obligation: what this Bullet needs        draft/<stem>-evidence-items.md
RE              Page-local run that makes the item ready           runs/run-<value|citation|display>-<slug>.md
Result          canonical fact and payload                         results/<re-run>/result.yaml
Evidence Card   read-only view of the current Result               Card view
Evidence Labels inline anchors into that Result: $V_x$ · \cite{C_x} · \figure{D_x} · \table{D_x} · \algorithm{D_x}
```

One item has one current RE lineage and one Card; one Result may expose many
Labels, and a Label never creates an item. External evidence stays at the
Supporting Run's real Result path and is referenced, never copied. The old
`outline/evidence/` folder and `*-evidence.md` snapshots are retired: move them
to `draft/_archive/legacy-outline-evidence/`; nothing reads them.

## 📤 Delivery Space

Tabs Web · LaTeX · Word · Slides, each with its state word (`pass`, `stale` or
`not built`, by file time against the Page); views Preview · Artifacts · Checks.
Nothing is edited in Delivery: a wrong word in a built file is fixed in the
Page or its exporter, then rebuilt. Lanes, writers and doors:
`ref/delivery.md`.

## ▶️ Runs panel · one per Space

1. **Place**: a column on the right at every page width; `▸` folds it to a
   strip, `◂` opens it; the choice is remembered per Space in this browser.
   The folded strip turns green when a run awaits the person.
2. **Run types**: the `🔘 BUTTON` lines of
   `../../draft/haipipe-draft-workflow/ref/run-cards.md`, as `label · Space · ticket
   pattern · views <names>`. A view or tab shows only the buttons that name it,
   each with its run count for the current target, then `+ New Run`.
3. **Target**: the selected paragraph or item narrows every list; nothing
   selected means the whole Page.
4. **Run card**: an id strip when there are two or more runs, the name, a state
   badge (Closed · Held · Awaiting you · Running), Rerun, the skill it uses
   (`Skill haipipe-draft-writing · haipipe-draft`: a `skills:` line in its ticket
   or runtime, else its card's `🧩 SKILL` line; JL 260928), a folded `▸ Prompt`
   with Copy, the running process, and the Results folder with its files.
5. **Starts nothing**: Rerun, `+ New Run` and Copy copy a prompt (the
   `💬 PROMPT` line with `{page} {plan} {target} {button} {run}` filled in).
   The person runs it in a Claude or Codex session, which records who started it.

The panel opens on a type with a run awaiting the person, else the view's
first type with runs. The Evidence Supporting Runs tab adds `Task runs` and
`Discovery runs`; a run no button claims shows under `Other`.

**Which runs, where, in what order, with which skill** is the studio drawing's
section "The runs of a Page": 1 Context, 2 Structure revise, 5 Evidence embed
(Draft › Table) · 3 Task and Discovery runs (Evidence › Supporting Runs) · 4 one
run per Evidence item (Citations · Displays · Values) · 6 Auto write (Draft ›
Reading) · 7 Section revise, 8 Paragraph revise (Draft › Revise) · adopt (code) ·
9 Build (Delivery) · 10 Check (Delivery › Checks); Scratch and Revise edits any
time. Every card in `run-cards.md` carries the same Space, view and skill.

**Run names** (`src/run_names.py`, JL 260928): `run-<kind>-<slug>`, the
name on disk and on screen alike (`run-section-0927-readability-cleanup`,
`run-paragraph-0928-c1-p2`, `run-value-0928-score-validation`); a taken name gets
`-2`. The three Delivery runs have one fixed name each, `run-delivery-webpage`,
`-latex`, `-word`, rebuilt in place. An older name (`rp-sec-07`, `re-value-07_x`,
`pj06t11r01_x`) still reads and is shown by `display_name` / `_name_by_item` until
`page.py run-names <page>` renames the Page once (flat `runs/`, `results/`, every
mention inside the Page; then `page.py export`).

**Records at the two ends** (JL 260928, AGENTS.md rule 3): `page.py open-run <page>
--kind <kind> --slug <words> [--target C1.P2] [--goal …]` writes the one ticket
(`status: open`); while open only the Page's text changes and the panel shows the
run as Running with no result; `page.py close-run <page> <run>` writes
`results/<name>/`, marks the ticket closed and adds one log line. The workbench's
own writers follow it: the first Revise Save on a paragraph opens
`run-revise-<c1-p2>` (its ticket keeps the text before), and Finish Scratch
is the close of a Scratch run.

**To add a run type** for runs that already exist (a known ticket prefix), edit
`run-cards.md` only; the page rereads it on every load:

1. **Own prompt, own card**: every button in a card shares that card's first
   `💬 PROMPT` (`runs_panel.py::run_types`); a button that needs its own prompt
   gets its own `## \`…\`` card.
2. **Patterns never overlap**: a run joins the FIRST button, in card order, whose
   pattern matches its ticket name, so `re-value-check-` would fall under `^re-value-`.
3. **No runs yet**: a button with no runs shows `No runs yet.`; its prompt is
   copied from `+ New Run`, where `{run}` is not filled, so a new-run prompt never uses it.
4. **Selection**: a selected paragraph or row finds a run through the run's
   `target:` (a Bullet `C1.P2.B3` also counts for `C1.P2`) and its Evidence item
   (an `item: E<NN>-…` line near the top of its `.md` ticket), never its name
   (`runs_panel.py::_targets`).

**A new ticket prefix is a new Run family.** Prefer a Step inside an existing
Run when the work belongs to it. A new family needs all of:

1. **Owner skill or ref page** under `../../draft/` (run-cards.md leaves Run authority
   to it) and its card in `run-cards.md`.
2. **`../../../../servers/workbench/workbench-task-draft/runs.py`**: `_TICKET_NAME` (else the run
   never appears); for a Page writing run also `_valid_page_run_id` (else it shows
   Held) and the label helpers `_page_run_label`, `_page_writing_subspace`,
   `_run_name`, `_run_action`.
3. **`runs_panel.py::_DISPLAY`**: its full-word name (`run-…-NN`); a family
   already named in full words (`run-delivery-latex`) needs none.
4. **`../../draft/haipipe-draft/src/run_folders.py::_KINDS`**: its `runs/<space>-run/` folder.
5. **Docs**: `../../draft/haipipe-draft/ref/page-run-families.md`, `../../draft/haipipe-draft-workflow/`
   (SKILL.md, `ref/interactive-writing-run.md`), `../../project/haipipe-run/ref/run-catalog.md`,
   and a case in `servers/workbench/workbench-task-draft/reader/tests/test_runs_panel.py`.

Cross-check by mirroring the newest family: `grep -rnE "rp-revise|_REVISE_RUN|revise\)"`
over `servers/workbench/workbench-task-draft`, `skills/page` and `skills/run` lists every place it is registered.

A new tab or view needs `space_views.py`.

The All-runs view (`lens=run`, reached by a `?run=` link, no button) is the
older full Run presenter: `ref/run-space.md`.

## ✍️ Who writes what

```text
file                         written by                                         regenerate with
───────────────────────────────────────────────────────────────────────────────────────────────────
plan (draft-v*.md)           run-structure (SHAPE/SURVEY); evidence embed appends; never
                             the Structure card, Scratch and Revise saves
evidence-items.md            SHAPE/SURVEY item contract                           never (authored)
records/context              CONTEXT (haipipe-draft-logic (ref/context.md))                       haipipe-draft-logic (ref/context.md)
records/requirement V | W    V: cli/requirement.py · W: the author, kept verbatim cli/requirement.py <page>.md
records/discussion           any Run or the page chat, as D<nn> records           never (authored)
records/feedback             cli/feedback.py collect; the Page writes Landed      cli/feedback.py collect
records/files · log          any Run or the page chat; log is append-only         never (authored)
<page>.md ## Content         page.py adopt, from the Draft                        page.py adopt
delivery/*                   the exporters (export.py, exporters/)                rebuild the lane
```

The workbench calls no model and writes only through `POST /_board/draft`:
`action: scratch` (notes and a Scratch Run), `action: revise` (Draft fields and
a Revise Run Step), `action: structure` (headings, logged in `records/log`).
Without an action the POST only registers the tab. `edit-preview`,
`edit-bullet` and `append-bullet` are refused: sentences are edited in Revise,
Bullets and structure through `run-structure`. All three write the current plan
file in place and do not check `approved:`: Scratch and Revise change only
sections 2 and 3, the Structure card only headings and the Overview. A new
Shape version (`approved: ⬜`, `supersedes:`) is `run-structure`'s job.

## 🔒 Versions · generation · Shape · evidence

```text
v0.16       pre-Content Shape 16            v1.0.1   same approved Shape, evidence fold 1
v0.16.1     same Shape, evidence fold 1     v1.1     bounded Shape revision in generation 1
v1.0        first approved generation       v2.0     major redesign after a review round
```

The version is `v<G>.<S>[.<E>]`; no `E` means zero. `G=0` never touches
Content. A Shape change increments `S` and resets `E`; an evidence fold
increments `E` and inherits its Shape's approval (`shape-base:`). `approved:`
is a person's act; a machine only transcribes it. At release,
`../../draft/haipipe-draft/ref/release-decisions.md` decides profile precedence.

## 🤝 Review packet

When a person asks to review or approve a plan, the structure Run answers with
one linked packet (current Shape, evidence owed, what shaped it, the decision
asked) and the Draft and Evidence links: `ref/review-packet.md`. It writes
nothing.

## 📂 Files

- `ref/plan-grammar.md` · the canonical plan grammar every reader parses
- `ref/item-table.md` · Evidence Item identities, Run graph, derived status
- `ref/record-shape.md` · the six records: ids, labels, writers, rules
- `ref/specimen-section-plan.md` · an approved Section plan, frozen
- `ref/evidence-bundle.md` · the derived per-Bullet evidence join
- `ref/evidence/citations.md` · `values.md` · `displays.md` · `pagex.md` · per-kind authority
- `ref/space-mapping.md` · UI Space → renderer → Markdown or Result
- `ref/run-space.md` · the All-runs view (`lens=run`)
- `ref/delivery.md` · the Delivery lanes, writers and doors
- `ref/folder.md` · the 📂 Folder tab: live inventory and rebuild pills
- `ref/content-preview.md` · candidate prose storage and the CONTENT handoff
- `ref/review-packet.md` · the review packet
- `ref/skill-record.md` · the ranked Page Skills store
- `../../draft/haipipe-draft-workflow/ref/run-cards.md` · the run types and prompts the panel shows
- `../../../../servers/workbench/workbench-task-draft/outline.py` · the page shell, the Spaces, the Draft views
- `../../../../servers/workbench/workbench-task-draft/space_views.py` · Evidence and Delivery tabs, views, selection
- `../../../../servers/workbench/runs_panel.py` · the Runs panel
- `../../../../servers/workbench/workbench-task-draft/outline_structure.py` · `outline_scratch.py` · `outline_revise.py` · the three writers
- `../../../../servers/workbench/workbench-task-draft/evidence.py` · `delivery.py` · `export.py` · `exporters/` · `runs.py` · `folderstat.py`
- `../../../../servers/workbench/workbench-task-draft/studio/page-workbench-design.excalidraw` · the design drawing
- `../../draft/haipipe-draft/src/plan_layout.py` · `outline_version.py` · `item_table.py` · `page_question.py`
