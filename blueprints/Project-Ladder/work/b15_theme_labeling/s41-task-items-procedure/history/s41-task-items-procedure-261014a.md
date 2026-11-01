s41 · Task items procedure: the items Task, step by step
========================================================

**Tags:** `Levels`

**Stage:** shaping

**Topic:** every detail of the 📦 items Task (`task-type: data`, s13), designed before more is built: its steps,
each step's Run, what it reads and writes on disk, what its tabs show in Work and in Report, the prompt that runs
it, how its state is read, and the rules that keep item text and keys out of sight. The first real one is dices350
`t01_dices350_items`. Asked by JL 261014 ("I think we should have a b15 s14-TaskItem-Procedure, and design every
details"). One topic per Task type, named `sNN-task-<type>-procedure` in the s41-s49 band (JL 261014: "so we
will have, Task-xxxx-procedure"; "it should be a new series"): s41 items, then keys, building, scanning and score. The screens built so far that day are the
first draft this topic replaces.

**Feeds:** `reports/` q01_labeling_ladder · q02_building_scanning_gates


Files
-----

```text
s41-task-items-procedure/
├── s41-task-items-procedure.md            this face; the drawing's words are the yaml block below
├── build_s41_task_items_procedure.py      the builder; a person's marks are kept on rebuild
├── s41-task-items-procedure.excalidraw    ① the three steps, ② ③ ④ the screens they made, on dices350
├── s41-task-items-procedure.png           its preview
└── shots/                                 three screens from the Physician host, 261014
```

```yaml
key: "Three steps, each one tab named the same in Work and Report. Work adds the step's prompt and its details; Report shows only the results."
steps:
- title: "📥 Step 1 · Read the raw data"
  run: "rNN_raw_read · hard"
  does: ["reads the raw files once", "writes their Table Card"]
  tab: "1 · Data: one row as cards"
  changed: "raw rows shown as they are, folded"
- title: "🧱 Step 2 · Make the items"
  run: "rNN_items · hard"
  does: ["the recipe, signed first", "the items, then the item check"]
  tab: "2 · Items: one item, the list"
  changed: "real items shown; the recipe step folded in"
- title: "🗺 Step 3 · Embed the items"
  run: "rNN_embedding_<model> · hard"
  does: ["vectors, a map, its groups"]
  tab: "3 · Embedding: the map"
  changed: "this Task's own Run; r06 ticket ready"
then:
  title: "🏗 building"
  run: "the next Task"
  does: ["holds back the sealed set"]
  tab: ""
arrows: ["the raw rows", "items.jsonl", "the items"]
shape: ["one tab:", "top bar: state · Copy prompt", "① big numbers, one sentence", "② the picture", "③ details, folded (Work)"]
rule: "Real rows and real items show when you open them; the card's sample stays made up (synth_df)."
rule_changed: "real rows and items shown, on JL's ask"
open: "❓ Open (JL): the sealed set is drawn from items you have now seen"
screens:
- file: shots/work-1-data-dices350.png
  title: "② Work › 1 · Data, dices350"
  read: "43,050 rows · 41 columns · 350 items · 123 raters; one row drawn as six cards; the real raw rows in a fold"
- file: shots/work-2-items-dices350.png
  title: "③ Work › 2 · Items, dices350"
  read: "350 items · 14.5 words judged · 3 turns before; the first real item drawn, then the real items"
- file: shots/report-2-items-dices350.png
  title: "④ Report › 2 · Items, dices350"
  read: "the same numbers and picture, no prompt and no details: the results only"
```


1 · The steps (proposed: three)
-------------------------------

```text
📥 Step 1 · Read the raw data ──▶ 🧱 Step 2 · Make the items ──▶ 🗺 Step 3 · Embed the items ──▶ 🏗 building
   hard rNN_raw_read                hard rNN_items                  hard (one Run per model)        holds back the
   Table Card of the raw file       recipe signed, then items       a map of the items              sealed set
```

1. **Step 1 · Read the raw data**: one hard Run, `rNN_raw_read` (`haipipe-task-for-description`). It reads the raw
   files once and writes their Table Card. It makes no items.
2. **Step 2 · Make the items**: one hard Run, `rNN_items` (`haipipe-task-for-data`). It holds the recipe (what one
   item is) and makes every item from it. The recipe is typed in the Run's config and the face's Method part, and
   a person signs it before the Run starts; the sign is a gate inside the step, not a step of its own (JL 261014:
   "2 · Item, should this creating items?").
3. **Step 3 · Embed the items**: hard, one Run per model (`run-labeling-embedding-<job>` today, on the labeling
   job's lane; Open 2). It writes the vectors, the map and its groups.
4. **Then**: the 🏗 building Task takes the items, holds back the sealed set (its Contract, P0) and starts its rounds.

The 261014 draft had four steps, with "Choose what one item is" as a separate soft Run. Proposed: fold it into
Step 2, because the recipe only proves itself when the items exist, and the config that runs is the recipe.


2 · What each step reads and writes
-----------------------------------

```text
t01_<dataset>_items/
├── t01_<dataset>_items.md            face: Data · Method (the recipe, signed) · Result parts
├── scripts/
│   ├── raw_read.py                   Step 1 worker
│   ├── items_transform.py            Step 2 worker
│   └── config/rNN_<run>.yaml         per Run: source, the recipe or the card's typed meanings
└── runs/
    ├── rNN_raw_read/                 Step 1: <run>.sh · run.yaml · result/description.json, metrics.json
    └── rNN_items/                    Step 2: <run>.sh · run.yaml · result/manifest.yaml, metrics.json
_WorkSpace/LabelingStore/<project>/<dataset>/
├── <raw>/                            the raw files, never changed
└── items-vN/                         Step 2 output: items.jsonl, items.ground-truth.jsonl, items.raters.jsonl
```

| step | reads | writes (Result) | writes (store) | done when |
|---|---|---|---|---|
| 1 | the raw folder | `description.json` (Table Card), `metrics.json` | nothing | its Run is complete and the card is there |
| 2 | the raw folder, the signed recipe | `manifest.yaml`, `metrics.json` | `items-vN/` | its Run is complete with `manifest.yaml` |
| 3 | `items-vN/items.jsonl` | the build record | vectors, map, groups | one build is complete |

A new recipe makes a new items version (`items-v4`) by a new Run; a closed Run and its items are never rewritten.


3 · What the tabs show
----------------------

One shape for every step tab (proposed 261014, after "it is so hard to read"):

```text
Work   top bar      step title · state chip · Run · [Copy prompt] (prompt folded; open only on the next step)
       ① at a glance three or four big numbers and one sentence
       ② the picture the one thing to look at
       ③ folded      the tables, closed until opened
Report ① and ② only: results, no prompt
```

| tab | ① at a glance | ② the picture | ③ folded |
|---|---|---|---|
| 1 · Data | rows · columns · units (chats) · raters; "one row is …" | one row as group cards, made-up values | the columns by group · the checks · the file and its Run |
| 2 · Items | items · median words judged · median turns before | one made-up item drawn (before → **main** → after), then the item list (id, words, turns) | the recipe as signed · what the Run recorded · files · earlier Runs |
| 3 · Embedding | models built · groups | the map | the builds and their settings |

The tabs are named for the step, the same in Work and Report, so a switch keeps the step. Older links (Itemization,
1 · Data, 3 · Item list) open the matching new tab.


4 · State and prompts
---------------------

1. **State, from disk**: done (the step's Run is complete with its required files), next (the first not done),
   not yet (after it). Nothing is typed by hand.
2. **The prompts**, one per step, copied from Work:

```text
Step 1  /haipipe-task-for-description <task>: a new rNN_raw_read Run that reads the raw files once and writes their
        Table Card to result/description.json: one row, the columns by meaning group, a synth_df, what to watch
        out for. It makes no items.
Step 2  /haipipe-task-for-data <task>: a new rNN_items Run of scripts/items_transform.py under the recipe signed in
        the face's Method part and typed in its config: one item per unit, the ground truth in its own files, and
        the item check as its result gate; it writes result/manifest.yaml and metrics.json.
Step 3  /haipipe-labeling-embedding <labeling Page>: build the embeddings of these items, one folder and one Run per
        model; a person starts the build.
```


5 · What shows, and what it costs
---------------------------------

1. **Real rows and real items** show when opened (s41-D07): the raw rows with every column, the items with their
   text.
2. **What that costs**: the raw rows carry the experts' and raters' answers (the keys), and the items include the
   ones the building Task will later hold back as the sealed set; a person who has read them is no longer blind
   to them.
3. **The Table Card's sample** stays made up (`synth_df`), so the card itself is shareable.


Decided
-------

s41-D01 · Each Task type gets its own procedure topic, `sNN-task-<type>-procedure`, in a new band, s41-s49 (JL
    261014: "it should be a new series"; s50s were asked, but s51-s59 is the server band, so the free 40s were
    taken). This one was made as s14-items-task-procedure, then s14-task-items-procedure, the same day.
s41-D02 · Three steps: 1 Read the raw data (hard `rNN_raw_read`) · 2 Make the items (hard `rNN_items`, its recipe
    signed in the face's Method part and typed in its config) · 3 Embed the items; Open 1, taken as proposed (JL
    261014: "go ahead and do it").
s41-D03 · Each step is a tab, named the same in Work and Report: 1 · Data · 2 · Items · 3 · Embedding. Work: the
    step's title, state chip and Copy prompt, then ① at a glance (big numbers, one sentence), ② the picture, ③ the
    details folded. Report: ① and ② only. Older links (Itemization, 2 · Item, 3 · Item list, 4 · Embedding) open
    the matching tab. The scoreboard and the cards are shared base looks, `.stat-row` and `.card-row` in
    `servers/workbench/frame.py` WORK_CSS, so a theme still carries no stylesheet (built 261014).
s41-D04 · The pictures: 1 · Data draws one row as one card per column group, its values made up (synth_df);
    2 · Items draws one made-up item (context_before │ main │ context_after, main marked) and the first 20 items by
    id and size; 3 · Embedding frames the map once built (built 261014).
s41-D05 · Item text before the sealed set exists: never; ids and sizes only (Open 3, taken as proposed).
s41-D06 · The item check (unique ids, the context before the main text, no key inside an item) is Step 2's result
    gate, named in its prompt (Open 4, taken as proposed).
s41-D07 · Real data shows (JL 261014: "for the data I want to see the raw data ... to present the raw data as it is if we
    want"; "here we want to put the real items to look, the real things"): 1 · Data has a fold, The raw rows, as
    they are (the first 10, every column, the answers included), in Work and Report; 2 · Items draws the first real
    item and lists the real items. This replaces D05; the Table Card's sample stays made up.
s41-D08 · Step 3 is the items Task's own Run, `rNN_embedding_<model>` (`scripts/embed_items.py`, the engine's encoder,
    groups and map on items.jsonl): the map and groups to result/, the vectors to the store; 3 · Embedding draws the
    map and its groups (JL 261014: "we want to see the embeddings results as well"; Open 1 settled: this Task owns
    it). dices350's ticket, r06_embedding_minilm, is ready and planned; a person presses Run (AGENTS rule 2).


Open
----

1. The sealed set is drawn from items a person may now have read (D07): hold back items nobody opened, or accept it?
2. Who signs the recipe, and where the sign is kept: the face's Method part, or the Run's card (`signs:`)?
3. A dataset whose items lack `context_before` and `main` needs its own item drawing.

(write here, or mark the drawing in red)
