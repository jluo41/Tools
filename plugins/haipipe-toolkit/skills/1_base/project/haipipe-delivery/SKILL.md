---
name: haipipe-delivery
description: "Owns a Block's one delivery/ folder: where every level's built output goes, the Delivery view, moving old outputs in, and the rule that only a person marks a delivery sent; also a Page's Delivery Runs (build the PDF, Word file or web page, ref/page-delivery.md). Trigger: delivery, delivery/, where does the pdf go, build the docx, rebuild delivery, sent, pull from OneDrive, /haipipe-delivery, /haipipe-draft-delivery."
allowed-tools: Bash, Read, Write, Edit, Grep, Glob, Skill
metadata:
  version: "0.5.2"
  last_updated: "2026-10-26"
  # version history: ./CHANGELOG.md
---

# /haipipe-delivery · what a Block hands over

A Block thinks in its Studio, answers in its Reports and hands over through its Delivery
(JL 261010: "它们可以产生 delivery，但 delivery 需要放到 block level"). Studio and Delivery
exist once per Block and every level opens them; a Report belongs to each level.

```text
haipipe-studio    studio/sNN-<topic>/    think       one per Block, opened from every level
haipipe-report    reports/qNN_<topic>/   answer      every level its own
haipipe-delivery  delivery/              hand over   one per Block, opened from every level
```

Decided in b10 (Tools/blueprints/b10_project_workbench): s02-D14 (storage), s09-D02 (a Report at
every level), s09-D05 (Delivery is Block-level, like the Studio). Its design topic is
`studio/s03-delivery-workbench-skill/` (s03-D01 to D04).


The folder
----------

```text
<block>/delivery/
├── <lane>/                         the Block's own output (web · latex · word · ...)
├── jNN_<job>/                      a Job's output
│   └── tNN_<task>/<lane>/          a Task's output, under its Job
└── reports/qNN_<topic>/<lane>/     a Block Report's output
```

1. **Block only**: Jobs and Tasks make outputs but keep no `delivery/`; they keep their own Report.
2. **The path is the link**: an output sits under the address of what made it, so each subfolder
   leads back to its source (JL 261010): `delivery/jNN_<job>/` to the Job folder `jNN_<job>/`,
   `delivery/jNN_<job>/tNN_<task>/` to the Task folder. `delivery_source(output)` maps a subfolder
   back; `delivery_dir(folder)` maps a source forward. A Job or Task view shows its own part.
3. **One helper**: every writer and reader goes through `haipipe-draft/src/common.py`:
   `delivery_owner`, `delivery_dir`, `delivery_source`, `delivery_relative`,
   `delivery_lane_dir`, `delivery_read_lane_dir`. Never build a delivery path by hand.
4. **Runs stay home**: Runs and Results stay with their source; only built files land here.
5. **No Block, own root**: a standalone Page without a Block keeps its own output root; an orphan
   `jNN`/`tNN` must first join a Block.


Items and versions
------------------

One deliverable is one item on screen, however many files and versions it has (b10 s03-D10; JL
261014: "all of them should one Delivery Item, and within it, we can see different versions").

1. **Lanes fold in**: a Section's `web/`, `word/` and `latex/` builds, or a deck's `slide/` and its
   picture in `render/`, are one item, named by its part (`t04_methods`) or its file name.
2. **Name a version `-v<N>`**: save each new version beside the last (`Deck-v1.pptx`, `Deck-v2.pptx`);
   never write over a version that was sent. A renamed variant that keeps counting
   (`Deck-Visual-v12`) or an unnumbered variant of a numbered item (`Deck-Symmetric`) joins it.
3. **No number, no version**: `Paper-SI` stays its own item beside `Paper`; neither has a number.
4. **On screen**: a row of versions, newest picked, over that version's preview: a PDF, a web page,
   a render, a deck drawn slide by slide, or a Word file read from its package.
5. **The code**: `frame.version_roots` (the rule, shared with Related), `frame.delivery_items`,
   `frame.version_panes`, `frame.pptx_preview` (`?view=pptx`).


Sent is a person's word
-----------------------

A build makes files; it never sends them. A rebuild, a migration or a passing check grants no
acceptance, release, send or submission. Only a person marks a delivery sent, and the place
that records it is the Block's one table of sends, `delivery/delivery.md` (below).


On screen
---------

```text
Guide · Studio | Block · Job · Task | Delivery        top row: think → do → hand over
Description · Report · Work Details · Runs            second row: what each level owns
```

1. **Right end of the top row**: Delivery opens like Studio, only it selected, the second row
   hidden; the level buttons keep the place to go back to.
2. **From a Job or Task**: it opens the Block's Delivery, as Studio opens the Block's Studio; a
   source row (Block · jNN · tNN) has the open Job or Task picked and shows that source's part
   (b10 s03-D06, JL 261011: "apply it to all the workbench").
3. **From the Block**: its view ends with "By source" (part · from · files), each Job and Task
   part linking back to its folder (JL 261010; built 261011, `frame.delivery_by_source`).
4. **Inside the Studio**: the third folding part, under Related (what came in, then what went
   out): every result of the Block, as the same cards, each opened on its preview (b10 s03-D09,
   JL 261014; `frame.studio_delivery`).
5. **Second row**: Delivery is not there; the workbench frame is `servers/workbench/frame.py`.


Moving old local outputs
------------------------

1. **Old local lanes**: a Job's or Task's own `delivery/` is a read-only input, never a target.
2. **Rebuild first**: rebuild from source into the Block, then remove the generated old copy.
3. **Keep hand-owned files**: a fragment without its `% GENERATED from` first line holds words
   no source can rebuild; it stays until its words move into the Page and the Page adopts them
   (the old-layout papers kept 33 such TeX fragments on 261010).
4. **Find what is left**:

```bash
find <project> -type d -name delivery -path '*/j[0-9]*' -not -path '*/_archive/*'
```


One row per send: delivery.md
-----------------------------

A delivery folder keeps its source's name (`delivery/jNN_<job>/`, `tNN_<task>/` under it); there is
no `dNN` card or prefix (b10 s03-D05, JL 261011). Each send is one row of `delivery/delivery.md`:

```text
| date   | for        | from        | status |
| 261009 | NMI        | jNN_<job>/  | sent   |
| 261012 | co-authors | jNN_<job>/  | draft  |
| 261019 | back from Gordon Gao | word/<name>-v9.docx | back |
```

A resend or a second reader is a new row, never a copy of the folder. A build may add a `draft` row and a
read back a `back` row; only a person writes `sent`. `related/related.md` lists what came in (b10 s01-D34); this lists what
went out.


A round: send, render, read back
--------------------------------

A file we share goes round until a person says stop (b32 s41-D21, D23; JL 261019: "the render haved changed a
while, and we need to read it again, and start another round of changing, and then send it back").

```text
build ─▶ adopt (-v<N>) ─▶ render (pictures) ─▶ ✍ push, at a person's word ─▶ ⏳ they edit OneDrive
pull: their copy as -v<N+1>, rendered, new comments listed, a `back` row ─▶ the next round's plan
```

1. **One script**: `scripts/word_round.py` (`status`, `adopt`, `import`, `render`, `push`, `pull`), given the lane
   folder, the file's name and its OneDrive copy; a Block's own script may pass them fixed (`main(**fixed)`).
2. **Never written over**: each state is `<name>-v<N>.docx` with its PDF; OneDrive holds one copy, the one people edit.
3. **Render**: each version's pages go to `render/<name>-v<N>/p-<N>.png` beside the lane, the pictures a Section
   canvas shows as "the file today"; the same lane the Delivery view's 📱 Render lists.
4. **Read back** (`pull`): only when OneDrive's copy matches no version; else it says nothing came back.
5. **Rows**: `push` adds a `draft` row, `pull` a `back` row; only a person writes `sent`.


A Page's Delivery Runs
----------------------

A Page's lanes are built by one fixed Run each: `run-delivery-webpage`, `run-delivery-latex`,
`run-delivery-word`, rerun in place by `page.py export`; the built files are the result. This was the skill
haipipe-draft-delivery until 2026-10-16 (s41-D11); the text is `ref/page-delivery.md`, the Run names are
unchanged, and Pages made before then keep working.


Boundary
--------

| Owner | Owns |
|---|---|
| `haipipe-delivery` | the Block's `delivery/` folder, its paths and helpers, the Delivery view, sent by a person, moving old outputs |
| `haipipe-delivery` (`ref/page-delivery.md`) | building one Page's web, LaTeX and Word lanes (`page.py export`) |
| `haipipe-paper-assemble` | the whole paper, built from its Sections' lanes |
| `haipipe-design-delivery` | releasing a design Job: `designs.json`, `designs.md`, `screens/` |
| `haipipe-cowork` | an email or reply drafted and kept at `delivery/jNN_<job>/<date>-<what>/` |
| `haipipe-labeling-handoff` | the labeling handoff package |
| `haipipe-studio` | `studio/`, Delivery's twin: one per Block |
| `haipipe-related` | `related/`, the other twin: what came in, one row each in `related.md` |
| `haipipe-report` | `reports/`, at every level |


Files
-----

```text
haipipe-delivery/
├── SKILL.md
├── CHANGELOG.md
├── ref/page-delivery.md
├── scripts/word_round.py      a round: versions, render, push, read back
├── ref/history/haipipe-draft-delivery-CHANGELOG.md
└── agents/openai.yaml
```
