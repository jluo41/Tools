s01 · Draft and Page
====================

**Tags:** `naming` · `base`

**Stage:** explore

**Topic:** What the base layer under every theme's writing really is, and its name. JL 261011:
"haipipe-page is more like the haipipe-draft, which contains the logic, sentences, and evidence,
and have a subfolder of draft to work on." On disk the work already is a draft: the plan's
`## 1 · Structure` (logic), its `## 3 · Draft` (sentences) and `<stem>-evidence-items.md`
(evidence) all live in `draft/`; the face `<stem>.md` holds only the Opening, the Aims and a copy
of the sentences, and the built output goes to the Block's `delivery/`. So the skill became
`haipipe-draft`, the word Page stays for what a reader opens, and "Task = Page" went.

**Feeds:** none (JL 261011: the Studio records this, not a Question report)


Files
-----

```text
s01-draft-and-page/
├── s01-draft-and-page.md          this face
├── s01-draft-and-page.excalidraw  the drawing: folder -> draft -> face -> delivery
├── s01-draft-and-page.png         its preview
└── build_s01_draft_and_page.py    the builder
```


Decided
-------

s01-D01 · The work behind a Page is a draft: its logic (the plan's `## 1 · Structure`), its
sentences (`## 3 · Draft`) and its evidence (the Evidence Items), kept in the folder's `draft/`;
the Page is the face `<stem>.md` and its built output in the Block's `delivery/` (JL 261011, option A)

s01-D02 · `haipipe-page` is renamed `haipipe-draft`, with `haipipe-draft-workflow`, the 8 Run
skills `haipipe-draft-<run>` and the 8 agents `haipipe-draft-*-agent`; `/haipipe-page` stays an
alias and a `haipipe-page` link keeps old paths working; the Page server (since 261014
`servers/workbench/workbench-task-draft/reader`, s02 and s03),
`haipipe-page-task`, `haipipe-page-insight` and the `.haipipe-page-export` marker keep their names
because they serve or own a Page face (JL 261011: "go ahead and do it")

s01-D03 · "Task = Page" goes: a Task may hold a draft, and a Task is not a Page; haipipe-task
1.13.0 and haipipe-folder 0.8.0 say so, and b10 records it as s01-D36 (JL 261011, asked in b16)

s01-D04 · Replies carry no Related question line; this Studio topic, not a Question report,
records the outcome (JL 261011: "use the Studio only")

s01-D05 · The sweep left sealed Results, receipts, chat transcripts and the older Delivery
tickets kept as history (`runs/delivery-run/run_delivery_*.sh`) unchanged; generated files were
rebuilt by their code (tickets by `write_ticket`, context records by `context-record.py`), and
drawings by their builders, twice where the sweep had touched a seed (JL 261011)


Open
----

1. `## 3` of the plan is named Draft inside `<stem>-draft-v<N>.md` inside `draft/`: rename it
   `## 3 · Sentences`? (one parser, `src/plan_layout.py`, plus 82 plan files)
2. Where `draft/` lives: b16's answer is beside the face it drafts (`tNN/draft/`,
   `reports/qNN/draft/`), never at a Block or Job root, and not moved to the Block like Studio,
   Related and Delivery; on disk today 102 Task drafts, 6 report drafts, 0 at a root. JL to confirm.
3. 5 drafts sit inside SHIFT studio topics (`b31_prep_ai/studio/s04-task31-updated-draft/draft/`
   and others): stay there, or become a Task or a report once the text is sent?
4. `page.py adopt` refuses a freshly set-up Page, because its Content is still empty, so a new
   Page cannot reach Content through adopt.
5. REACH, Physician and DrFirst Projects still name `haipipe-page`; they work through the link
   and the alias; sweep them, then remove the `haipipe-page` link.
6. No code rewrites 13 FairGlucose Sections' `runs/delivery-run/run_delivery_*.sh` or 4 old
   `board/_assets/board.js` files, so they keep the old name.

(write here, or mark the drawing in red)
