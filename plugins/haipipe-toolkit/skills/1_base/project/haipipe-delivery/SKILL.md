---
name: haipipe-delivery
description: >-
  Owns the Block's Delivery, shared across Block, Job and Task views: the one physical
  `delivery/` folder of a Block, where every level's built output is kept under its source
  path; the Delivery view at the right end of the top row (Studio | Block · Job · Task |
  Delivery); the rule that only a person marks a delivery sent; moving old local outputs into
  the Block; and the shared path helpers in haipipe-draft/src/common.py. How a file is built
  stays with its lane owner (haipipe-draft-delivery, haipipe-paper-assemble,
  haipipe-design-delivery, haipipe-cowork, haipipe-labeling-handoff). Use to find where an
  output goes, check that no Job or Task keeps its own delivery/, move old local outputs into
  the Block, or propose a delivery item. Trigger: delivery, Block delivery, delivery/, where
  does the pdf go, deliverable, handoff folder, send, sent, /haipipe-delivery.
allowed-tools: Bash, Read, Write, Edit, Grep, Glob, Skill
metadata:
  version: "0.2.3"
  last_updated: "2026-10-11"
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
4. **Second row**: Delivery is not there; the workbench frame is `servers/workbench/frame.py`.


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
```

A resend or a second reader is a new row, never a copy of the folder. A build may add a `draft` row;
only a person writes `sent`. `related/related.md` lists what came in (b10 s01-D34); this lists what
went out.


Boundary
--------

| Owner | Owns |
|---|---|
| `haipipe-delivery` | the Block's `delivery/` folder, its paths and helpers, the Delivery view, sent by a person, moving old outputs |
| `haipipe-draft-delivery` | building one Page's web, LaTeX and Word lanes (`page.py export`) |
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
└── agents/openai.yaml
```
