s33 · One page shape: Block, Job, Task
======================================

**Tags:** `UI`

**Stage:** explore

**For:** a deck, and one page shape for Block, Job and Task: answer, rows, next step, details, for the people who build the workbench

**Delivery type:** ui

**Topic:** one page shape for every level of the work workbench: answer line, a table of rows, the next step,
details folded last. A Block's rows are its Jobs, a Job's its Tasks, a Task's its Runs; clicking a row zooms in.
Why now (JL 261027): on b19 the Report and Work tabs showed the same page, three rows of tabs sat above the
content, and the first real number was four clicks deep. The Block's page is also what `slide/` would save.

**Feeds:** none yet; the `slide/` folder proposal for haipipe-block


Files
-----

```text
s33-one-page-shape/
├── s33-one-page-shape.md        this face
├── mock/one-page.html          the mock: b19 at three levels (#block, #job, #task), layouts ?layout=A|B|C
└── mock/img/                    s00 and s25 previews of b19, shrunk for the Studio section
```


Decided
-------

s33-D01 · Names are the folder names only, in the breadcrumb, titles and rows; no second title beside them (JL 261027: "why not just give the folder name? this is new and give us more confusions").
s33-D02 · Layout A, accepted (JL 261027: "I will just accept it"): top is where we are (the breadcrumb, folder names); left lists the siblings at the same layer, named; right is this page's sections as a line minimap, names on hover; one scrolling page, no tabs: Answer, Rows, Chart, Next, Studio, Related, Delivery, Timeline, Folder. B (a tree on the left) repeats the rows; C (sibling menus in the breadcrumb) hides the siblings until hover.
s33-D03 · Markdown is the source, HTML is rendered on each request and never saved (JL 261027: "we have the principle to render the md to the html, and we will not save the html"). The page, the Block's slide and every section are drawn live from the .md and the receipts; `slide/` keeps `slide.md` only. Old saved HTML (the Page export doors' `*-view.html`, `index.html` in delivery/) is migration debt, not changed by this topic. The mock in mock/ is a design sketch, not output.
s33-D04 · Every section's view buttons sit right under the title, above the Purpose, Studio's groups included; a section with one view keeps its bar, one button naming it, so the Purpose never moves (JL 261031, b10 r01 Q1: B, "The key thing is whether the purpose here is view based or the page based, if it is the view based, we will put it above the Purpose"; Q2 note: "why we don't have the view button list here?"). Code: `focus_page.py` render's `bar`.
s33-D05 · No count line under the title and no count in a rail item: no "3 topics", "2 Jobs" (JL 261031, b10 r01 Q4: "Don't add N topics, N jobs, they are useless, they will change along the way"). Code: `focus_page.py` `describe`, `page_shell`.
s33-D06 · Paper pages (a paper Board, a version, a Section) use the common width and no verb after the section word (JL 261031, b10 r01 Q2: A). The Section's width is the draft Task page's own look (`focus_draft.py` WIDE), changed by its owner.
s33-D07 · Labeling Job and Task pages move onto the shared page: their sections become view buttons (JL 261031, b10 r01 Q3: A, "it is very good, very clean, mark my prefernece here"). The labeling session builds it (`labeling_focus.py`).
s33-D08 · The three small fixes are not made: b35's delivery previews keep no right rail, and an old link without `layout=focus` still opens the old workbench (JL 261031, b10 r01 Q4: C).


Open
----

1. Does the one page shape read right at all three levels (JL to look at mock/one-page.html)?
2. The 4-count test on the mock: clicks to first number 0 · menu rows 1 · duplicate tabs 0 · Runs shown 9 of 9.
   Today's b19: 4 · 3 plus a rail · Report = Work · 1 of 10.
3. Then: the Block page saved as `slide/`, and the old Description, Report and Work tabs merged into it.
4. Agree its **For:** line and **Delivery type:** (ui), proposed by the agent 261030?

(write here, or mark the drawing in red)

Proposal: three clean pages (261027, waiting for JL)
-----------------------------------------------------

Read from `servers/workbench/frame.py` (`render()` 4263, `vanilla()` 367, the Studio's six parts 1735-2254),
`workbench-work/work_progress.py` (`spaces()` 1597) and both READMEs.

```text
today                                        proposed
Guide·Studio|Block·Job·Task|Delivery         breadcrumb  [Page] [Studio] [Delivery]  ?
Description|Report|Work|Runs                 (none)
Goal|Plan|Execution|Results                  (none)
content + side rail "Disk · Runs"            content
Studio: 8 closed folds (topics, Related,     Page: answer · rows · chart · next · details
  Delivery, Runs, Timeline, Folder)          Studio: topic thumbnails, then Related
                                             Delivery: output thumbnails
```

Code: one reader returns data (no HTML), three views draw it, previews and group writes move to their own
files, CSS and JS move to assets. A theme gives words and choices (row names, chart key), not its own HTML.
Old addresses keep working (`frame_redirect`, as for the older Block pages).

