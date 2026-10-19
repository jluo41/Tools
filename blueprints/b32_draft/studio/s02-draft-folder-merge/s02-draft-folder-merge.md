s02 · One draft folder: page and writing
========================================

**Tags:** `base` · `folders`

**Stage:** shaping

**Topic:** JL 261014: "we need to handle Tools/plugins/haipipe-toolkit/skills/1_base/writing and
Tools/plugins/haipipe-toolkit/skills/1_base/page ... we might want to merge them into one,
1_base/draft". s01 renamed the skill (`haipipe-page` became `haipipe-draft`), but its folder stayed
`1_base/page/`, and the prose worker `haipipe-writing` sat apart in `1_base/writing/`. This topic
draws how the draft's Runs call the writer, who else calls it without a draft, and the one
`1_base/draft/` folder both now live in (moved 261014).

**Feeds:** none (the Studio records this, not a Question report)


Files
-----

```text
s02-draft-folder-merge/
├── s02-draft-folder-merge.md          this face
├── s02-draft-folder-merge.excalidraw  the drawing: who calls the writer, then the folders before and now
├── s02-draft-folder-merge.png         its preview
└── build_s02_draft_folder_merge.py    the builder (counts and the "now" tree read from disk on every build)
```


The words the drawing reads
---------------------------

```yaml
key: 'Done 261014: writing/ lives inside draft/, because the draft workflow''s writing step is this writer.
  It keeps the name haipipe-writing, because other skills call it on files with no draft.'
draft_chain:
- title: haipipe-draft
  lines: [the door, folder and face, page.py]
- title: haipipe-draft-workflow
  lines: [context, structure, evidence, writing, check]
- title: the writing Runs
  lines: [haipipe-draft-writing (Content), haipipe-draft-scratch, haipipe-draft-revise]
chain_labels: [runs, dispatches]
writer:
  title: haipipe-writing
  lines: [the draft workflow's writing step, draft, revise or evaluate one slice, owns no plan]
style: {title: 1_style, lines: [writing-dna-skill, the voice before]}
evaluate: {title: 2_evaluate, lines: [humanizer, academic-humanizer, findings after]}
request_label: a Writing request
outside_label: 'files that name haipipe-writing, by skill: no draft needed'
clash: ❓ haipipe-draft-writing already exists, so the writer cannot take that name
before_tree: |
  1_base/page/      310 files
    ├── haipipe-draft/   181 files
    ├── haipipe-draft-workflow/ 14 files
    ├── haipipe-folder/  2 files
    ├── haipipe-page  ─▶ link to haipipe-draft
    ├── haipipe-sentence/ 2 files
    ├── pages-example/   52 files
    ├── workbench/       32 files
    ├── workbench-page/  19 files
    ├── workbench-studio/ 5 files
    └── workflow-runs/   21 files

  1_base/writing/   61 files
    ├── CHANGELOG.md     its versions
    ├── README.md
    ├── 1_style/         22 files
    ├── 2_evaluate/      9 files
    └── haipipe-writing/ 28 files
links_now: |
  1_base/page       gone: 174 tickets rebuilt, sources fixed (✎ 261014)
  1_base/writing    gone: nothing used it (✎ 261014)
steps:
- {title: ✅ Block renamed, lines: [old name b51_base_draft, now b32_draft]}
- {title: ✅ s02 drawn, lines: [this topic]}
- {title: ✅ moved and swept, lines: [page/ is draft/, writing/ is draft/writing/, 147 files rewritten]}
- {title: ✅ installed and tested, lines: [skill links in 5 SPACEs, same 29 old test failures, none new]}
open:
- '❓ b10 is told first: workbench, workbench-page and workbench-studio may move out to 1_base/workbench/'
- '❓ 39 old FairGlucose tickets (runs/delivery-run/run_delivery_*.sh) still name 1_base/page; no writer makes them now'
- '❓ some Physician run notes and scripts name skills/page/haipipe-page, a path gone before this move'
```


Decided
-------

s02-D01 · The Block is `b32_draft` (was `b51_base_draft`), in the b3x row beside `b31_excalidraw`; the
old name was swept in this Block, b10's s01 face and its history, three skill CHANGELOGs and one memory
note (JL 261014: "go ahead, rename to b32_draft and draw s02")

s02-D02 · `1_base/page/` is now `1_base/draft/`, and `1_base/writing/` is now `1_base/draft/writing/`;
`haipipe-writing` keeps its name; links at `1_base/page` and `1_base/writing` keep old paths working
(JL 261014: "please go ahead and do it. Tools/plugins/haipipe-toolkit/skills/1_base/page change this to draft")

s02-D03 · Every path in Tools was rewritten (147 files, `../` links recomputed per file); generated
drawings were rebuilt by their builders, never edited; the skill links were remade by `install.sh`
globally and in WellDoc, DrFirst, Knowledge, REACH and jluo41-repo (JL 261014)


s02-D04 · The `1_base/writing` link is removed: no file in Tools or the six SPACEs and no skill link
used it; the writer stays grouped in `draft/writing/` (haipipe-writing with its vendored 1_style and
2_evaluate), not spread across draft/ (JL 261014: "we don't need this anymore ... merge this totally to
1_base/draft")


s02-D05 · The `1_base/page` link is removed. Before that: 174 delivery tickets in the other SPACEs were
rewritten by haipipe-draft's own `write_ticket` (ticket only, no build; 45 flat ones moved into their
Run folders, as every export now does), 8 context records by `context-record.py`, and 16 hand-written
files (READMEs, AGENTS.md, build scripts, board.md) by hand; then 19 workbench hosts were restarted
with their own arguments on their SPACE's `.venv` (JL 261014: "we should remove this one as well, right?")


Open
----

1. The workbench skills (`workbench`, `workbench-page`, `workbench-studio`) are the shared screen
   that b10 owns: move them out to `1_base/workbench/` only after b10 agrees.
2. `workflow-runs/` keeps its name; `1_runs/` was only a proposal.
3. 39 FairGlucose tickets from an older layout (`runs/delivery-run/run_delivery_*.sh`) still name
   `1_base/page` and would fail if run; the current tickets beside them (`runs/run-delivery-*/`) work.
   No code writes the old ones now (s01-D05 kept them as history): delete them, or keep them as history?
4. Not from this move: Physician run notes, two `run_delivery.py` scripts and an old `board.js` name
   `skills/page/haipipe-page`, a path gone since the 1_base layout; the 5654 preview host served a
   folder removed on 261002 and was not restarted.

(write here, or mark the drawing in red)
