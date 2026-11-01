s13 · Labeling Task: six types in one Job
==========================================

**Tags:** `Levels`

**Stage:** shaping

**For:** a deck, and the six types of Task inside one labeling Job, for the people who write the toolkit skills

**Delivery type:** skill

**Topic:** the types a labeling Job's Tasks come in. A labeling Job is one dataset × one label; inside it the
Tasks have different jobs, the way a design Job's do (b12 s13: `t00` reason ideas · `tNN_d<NN>` one design ·
`t99` review whole). Here there are five: items, ground truth, building, scanning, score, each read from the Task
face's `task-type:` line, never from its number (ground truth and score are optional, so numbers shift). Building and
scanning meet only at the signed Label Handoff, the engine's one crossing. Asked by JL 261014; the workbench
shows the types since the same day (`servers/workbench-labeling/labeling_theme.py`, `TYPES`). On 261101 the slide
deck's newer process (version 12: Steps 0 to 7, two loops, the round report) was placed on the types: one map from
each step to its Task, its views, the files it writes and the person's gate (JL 261101: "go ahead and update them");
the same day building split into its two loops, 🧭 meaning and 🛠 expression, so the types became six (s13-D12).

**Feeds:** `reports/` q01_labeling_ladder · q02_building_scanning_gates


Files
-----

```text
s13-labeling-task/
├── s13-labeling-task.md                 this face
├── build_s13_labeling_task.py           the builder (261101): five parts; its Design is the step map
├── s13-labeling-task.excalidraw         the drawing: the map, the round loop, the first drawing kept below
├── s13-labeling-task.png                its card
├── result/first-drawing.excalidraw      the first drawing (261014), kept whole
├── result/first-drawing-builder/        its builder, reading the yaml block below
└── shots/                               the two screens, from the Physician host on 261014
    ├── job-work-dices350.png            Job › Work: each Task's type and state, the score Task still to make
    └── items-itemization-dices350.png   t01 › Report › Itemization
```

Rebuild: `python build_s13_labeling_task.py`.


The steps on the six types
--------------------------

```text
step (slides v12)           Task             its views                          your part
0 corpus into items         📦 items          Data · Items · Embedding · Split   ✍️ sign the recipe
1 frame the task            🧭 meaning        Frame                              🙋 interaction: 3 questions
2 investigate               🧭 meaning        Report                             (agent work)
3 collect preferences       🧭 meaning        Preferences                        🙋 interaction: the cards
4 update and check          🧭 meaning        Update                             (agent work)
5 execute, evaluate         🛠 expression     Rewrite · Run · Evaluate           (never asks you)
6 freeze, release check     🛠 expression     Release                            ✍️ sign the release
7 label at scale, audit     🔍 scanning       Batches · Audit · Final labels     ✍️ accept the delivery
evaluation                  📊 score          Agreement
(input)                     📏 ground truth   Labels                             fenced: only score reads it
```

Two loops, two Tasks (JL 261101: "we have the meaning-loop and expression-loop"). 🧭 meaning runs Loop 1, 2 …
(Report → Preferences → Update), each making a meaning version m01, m02 …, and is the only place the person is asked:
each loop's Report is one interaction report, written by the agent with /haipipe-labeling-interaction as one
/haipipe-interaction collect Run, `runs/rNN_collect_report_mNN/`; you answer it in Preferences, and Update records which
answer made which rule, so every meaning version points back to the interaction that produced it (the meaning history).
The guideline itself is a mind map of rules, one version per loop. 🛠 expression runs rounds e01, e02 … (Rewrite → Run →
Evaluate) under one approved meaning and never asks: a wording issue starts the next expression round, a rule or label
issue goes back as the round report to the next meaning Report, and when the criteria are met the version goes to
Release. Train develops the wording; Test is labeled, scored and audited, and
its issues go to meaning, never to the rewriting. Scanning's new meaning issues also go back to meaning.


The five types, as first drawn (261014)
---------------------------------------

```text
type        task-type line       what it does                                         its skill
📦 items     data                 raw rows become items; the ground truth kept apart   haipipe-task-for-data
📏 ground    raw                  the dataset's own labels; optional; fenced           haipipe-task-for-raw
   truth
🏗 building  labeling-building    Contract → Rounds → G0 → Freeze → signed Handoff     haipipe-labeling-building
🔍 scanning  labeling-scanning    reads the Handoff: Test → Scan → Audit → final labels haipipe-labeling-scanning
📊 score     eval                 final labels against the ground truth and raters' spread     haipipe-task-for-eval
(today)     labeling             one Page that is building and scanning at once
```

A Job needs items, building and scanning to close; once it has ground truth, it needs score too. G0 is the gate where
the person confirms what each label means; the Label Handoff is the frozen, signed guideline plus the person's
gold labels.

```yaml
key: "One Job = one dataset × one label; each Task is one of six types. The two loops are two Tasks: 🧭 meaning asks you, 🛠 expression never does; the round report links them."
close: "To close: items + meaning + expression + scanning; score too once ground truth exists."
sub: "dataset × label · each Task typed by its task-type line, never its number"
unshown: "❓ their screens: not drawn (the labeling Page is never opened in a browser)"
relate: "same raw rows"
types:
- id: items
  title: "📦 items"
  line: "task-type: data"
  does: ["raw rows become items", "ground truth kept apart"]
  screen: "Report: Itemization · Embedding"
- id: building
  title: "🏗 building"
  line: "task-type: labeling-building"
  does: ["Contract · Rounds with the person", "G0 · Freeze"]
  screen: "Work: Definition · Rounds · Guideline"
- id: scanning
  title: "🔍 scanning"
  line: "task-type: labeling-scanning"
  does: ["Test on the sealed set", "Scan · Audit · final labels"]
  screen: "Work: Test · Evaluation · Scan · Audit"
- id: score
  title: "📊 score"
  line: "task-type: eval"
  does: ["final labels vs the ground truth", "within the raters' spread"]
  screen: "needed once the Job has ground truth"
ground_truth:
  title: "📏 ground truth"
  line: "task-type: raw"
  does: ["the dataset's own labels", "optional"]
  fence: "fenced: only score reads it"
arrows: ["items to label", "🔒 signed Label Handoff", "final labels"]
today: "today: one Page is both (task-type: labeling)"
open: "❓ Open 1 (JL): split the real labeling Pages?"
screens:
- file: shots/job-work-dices350.png
  title: "② dices350 j01 today, Job › Work"
  sub: "each Task's type and state from its face; the type the Job still lacks, dashed"
  read: "✅ t01 items, 4 Runs · ✅ t02 ground truths, 1 Run · 🔶 t03 building + scanning on one Page, 0 Runs · ⬜ t04 score, not made yet"
- file: shots/items-itemization-dices350.png
  title: "③ the items Task, Report › Itemization"
  sub: "read from its face and its newest Run's result/; Embedding beside it"
  read: "350 items from 350 chats · 43,050 ratings kept apart · experts' gold Yes 175 / No 175 · made by r04_main_text_rebuild"
glossary:
  title: "④ Words, Jobs, what is open"
  sub: "one line each; the steps from haipipe-labeling-building and -scanning, P0 to P5"
  words:
  - ["Contract (P0)", "one valid job: the corpus, the label, the person who decides, the sealed set reserved; it makes no label"]
  - ["G0", "the gate where the person confirms what each label means, before the first round"]
  - ["Round (P1)", "one closed checkpoint with the person: the gold labels they confirm and the guideline so far"]
  - ["Freeze (P2)", "packs what is closed into the signed Label Handoff; it adds nothing new"]
  - ["Label Handoff", "the frozen guideline plus the person's gold labels, signed; scanning reads only this"]
  - ["sealed set", "items held back from the start, never shown while building; the Test scores on them"]
  - ["executor", "a weak model that labels under the frozen guideline; never a source of gold"]
  - ["route", "one executor with its prompt and settings; it qualifies only by passing every floor"]
  - ["Test (P3)", "the person's gold on the sealed set scores the executors; one route qualifies, or none"]
  - ["Scan (P4)", "the qualified route labels every item in scope"]
  - ["Audit (P5)", "the scanned labels checked; on pass they become the final labels"]
  - ["ground truth", "the dataset's own labels; fenced, so building and scanning cannot copy them"]
  - ["raters' spread", "how the dataset's many raters split on each item (DICES-350: 123 raters)"]
  jobs:
  - ["dices350 · response safety", "✅ t01", "✅ t02: raters' majority = experts on 65.5%", "🔶 t03 one Page, OPEN", "⬜ needed"]
  - ["redsm5 · depression symptoms", "✅ t01", "none", "⏸️ t02 one Page, HELD", "optional"]
  - ["aci_bench · authority appeal", "✅ t01", "none", "🔶 t02 one Page, OPEN", "optional"]
  opens:
  - "❓ 1 · JL: split the real Jobs' labeling Page into building and scanning Tasks, or keep one Page until the engine holds two lanes?"
  - "❓ 2 · JL: where a scanning Task's test, scan and audit records live (Q03)"
  - "❓ 3 · JL: a new Handoff version: a new scanning pass, or a new scanning Task?"
  - "❓ 4 · JL: should the items Task own the embedding?"
  - "❓ 5 · the meaning, expression and scanning screens are drawn (b15 j01 s58), not built: the real labeling Page is never opened in a browser"
```


Decided
-------

s13-D12 · Building splits into two Tasks, one per loop: 🧭 meaning (Steps 1 to 4: Frame · Report · Preferences · Update,
    turns m01, m02 …) and 🛠 expression (Steps 5 and 6: Rewrite · Run · Evaluate · Release, turns e01, e02 … under one
    approved meaning); the round report sends expression back to meaning; only meaning carries interactions, one
    collect Run per turn, and its Update keeps the meaning history. Six Task types. (JL 261101: "we have the
    meaning-loop and expression-loop"; "we hope that the interaction is only available in the meaning loop task".)
s13-D11 · (Replaced by s13-D12: building is two Tasks.) The slide deck's Steps 0 to 7 (version 12) map onto the five types: items holds Step 0 (Data · Items ·
    Embedding · Split); building holds Steps 1 to 6 (Frame · Decide · Changes · Staging · Release), since Steps 2 to 5
    loop round by round until release; scanning holds Step 7 (Batches · Audit · Final labels); score holds the
    evaluation (Agreement); ground truth keeps the dataset's own labels (Labels). The signed Label Handoff becomes the
    Step 6 release. (Proposed by Claude 261101 as a step map; JL 261101: "go ahead and update them".)
s13-D10 · The type once called keys is ground truth (📏; JL 261014: "could we do not use the term of key, is this
    widely used or not?"): papers say ground truth or gold labels, not keys. Its `task-type: raw` line is unchanged.
s13-D01 · (Six types since s13-D12.) One labeling Job = one dataset × one label; its Tasks come in five types, items · ground truth · building ·
    scanning · score, each named by its face's `task-type:` line (data · raw · labeling-building ·
    labeling-scanning · eval), never by its number (JL 261014: "one job is a data+labeling ... in the job, we
    might have different types of tasks").
s13-D02 · (Building is meaning and expression since s13-D12; the Handoff is expression's Release.) Building and scanning split at the signed Label Handoff, the engine's one crossing; today's
    `task-type: labeling` Page counts as both, so the three real Jobs read as they are (proposed by Claude
    261014; the real Jobs keep their folders until JL says).
s13-D03 · Job › Work shows each Task's type and state, then a dashed card for each type the Job still lacks
    (items, building, scanning; score once it has ground truth), ground truth and score as optional otherwise (JL 261014: "I
    think the kind things is here, right? To prepare these tasks to be finished"; built 261014).
s13-D04 · The items Task's Report opens on Itemization · Embedding (JL 261014: "we can call them Itemization,
    and Embedding"): Itemization reads the face's Data, Method and Result parts and the newest Run's
    `result/manifest.yaml` and `metrics.json`; Embedding reads the labeling job's embedding state and opens its
    Embedding view (built 261014). No Draft tab beside them (JL 261014: "we don't need draft").
s13-D07 · The items Task: Report shows the results only, one tab per step: 1 · Data · 2 · Item · 3 · Item list
    (ids and sizes, never an item's text) · 4 · Embedding (the map once built, framed from the Labeling
    workbench); Work has the same four tabs, one step each: read the raw data (hard) · choose what one item is
    (soft) · make the items (hard) · embed the items (hard), each with its state chip, a "Prompt for this step"
    row with Copy prompt (open on the step to do now), its result in full and a link to the next step; no
    Folders, Evidence or Value views (JL 261014: "report will just show the results ... Work will show the steps,
    and the step's results"; "Result1-Data, Result2-Item, Result3-ItemList, and Result-4-Embedding"; "I want
    here to show the results 1, 2, 3, 4 ... in the work"; built 261014). Older Itemization links open 1 · Data.
    Item text stays out: the old item table showed it only after the sealed set was held back, each showing
    recorded, so the Item list shows ids and sizes.
s13-D09 · The items Task's procedure moved to its own topic, s41-task-items-procedure (261014): three steps and
    tabs 1 · Data · 2 · Items · 3 · Embedding, which replace D07's four; D07 and D08 stay as the record.
s13-D08 · Step 1's result is the raw file's Table Card (haipipe-task-for-description), from a `rNN_raw_read` Run:
    what one row is and its checks, every column by meaning group, what to watch out for, and a sample made up
    in the real columns (synth_df), never a real row: a chat's text is a future item and its answers are ground truth
    (JL 261014: "you should also show what is the sample of the data, so people can view it"). The Step 1 prompt
    names haipipe-task-for-description; it named haipipe-task-for-raw, which extracts from a database. First Run:
    dices350 t01 r05_raw_read, 43,050 rows × 41 columns, started by JL pasting the prompt (261014).
s13-D05 · Scan moves from a Task's Delivery into Work (a scanning step); Delivery keeps Handoff and Final
    labels (261014).
s13-D06 · The old Labeling workbench's Job data card read Runs from the flat `runs/rNN_*.sh` +
    `results/<run>/`; it now reads one folder per Run, `runs/<run>/result/` (since 261010), the flat layout
    still read (fixed 261014, `labeling.py` `_task_runs`).


Open
----

1. Split the three real Jobs' labeling Page (aci_bench, dices350, redsm5) into meaning, expression and scanning
   Tasks, or keep one Page until the engine can hold their lanes?
2. Items for several labels on one dataset: one items Task at the Block, or one per Job as today?
3. Release (Step 6): inside the expression Task, or a Task of its own?
4. A new release (h02): a new pass of the scanning Run, or a new scanning Task?
5. Embedding sits on the labeling job's lane today; should the items Task own it, since it embeds the items?
6. Agree its **For:** line and **Delivery type:** (skill), proposed by the agent 261030?

(write here, or mark the drawing in red)
