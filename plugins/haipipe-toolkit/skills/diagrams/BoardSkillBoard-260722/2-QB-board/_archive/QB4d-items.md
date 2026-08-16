# Page Items to Finish: the testable gap
state: 🟡 PARTIAL · rules settled on QB4, carved 260729; face awaits JL
owner: CC
method: every checkbox is a condition another person can judge; a tick means verified

## Question
What makes `## Items to Finish` a definition of done rather than a task list, how may its conditions be categorized, and what does a tick mean?
A checkbox is a condition another person can judge true or false, the heading counts automatically, and a tick means the condition was VERIFIED, never merely attempted (`SKILL.md`'s sync rule: never tick what was not verified).
On S pages each Q-consumer stays one complete record and closes only after its answer is interpreted and woven into Content.


## Boundary
- ✅ Covered here
  Checkbox semantics, context-named subsections, per-subsection and overall counts, the verified-tick rule, and the Q-consumer record shape inside the list.
- ↪ Covered elsewhere
  The write-back trigger (work done ⇒ tick in the same round): `SKILL.md`'s sync verb, enforced by `check.py`'s `open-with-done-items`.
  Where the answer behind a Q-consumer comes from: the probe layer (`/haipipe-probe`).

## Diagram

```
example for a skill-family design page

🎯 Items to Finish                                      5/9
├── 🧠 Choose the skill family                          1/2
│   ├── ☑ choose the page hierarchy
│   └── ☐ decide the durable-path policy
├── 🛠 Materialize the accepted structure               2/3
├── 🧪 Prove routing on real questions                  2/2
└── ⏳ Waiting on the Page contract                     0/2

QB4d / Items to Finish / Choose the skill family  [⧉ Copy] [🤖 Chat]
```

/_excalidraw/?board=Tools/plugins/haipipe-toolkit/skills/diagrams/BoardSkillBoard-260722/board.excalidraw&frame=QAa4

## Content
### 1 · What Items to Finish conveys
```
🎯 Items to Finish · answers: what, testably, separates now from done?
──────────────────────────────────────────────────────────────
conveys   the definition of done, as conditions a second person can judge
holds     - [ ] boxes, auto-counted in the heading · optional ### topic
          groups, each badged with its own done/total
source    one judgeable condition per box, grouped under contextual names,
          never generic ones · S: each Q-consumer stays one full record
rules     a tick means VERIFIED, never merely attempted · a Q-consumer
          closes only after its answer is interpreted and woven into
          Content · never invent a row to fill a group
omit      never · without a testable gap the page cannot say what done is
```
Items to Finish is the testable definition of done, not a loose task list.
Every checkbox must describe a condition that another person can judge true or false, and the heading reports the completed count automatically.
On S, each Q-consumer remains one complete record and closes only after its answer is interpreted and integrated into Content.
Under the base/variant model on `QB4`, this section is frame: a page kind may contribute a record shape into the list, which is what the S Q-consumer record is, and the checkbox semantics, the auto count, and the verified-tick rule hold for every kind.

### 2 · Context-named subsections
Items may be grouped under non-empty `###` headings so unlike gaps do not look interchangeable.
The heading names the actual work on this page, not a global type.
`Decisions`, `Build`, `Verify`, and `Dependencies` are examples that explain possible purposes; a real page should prefer names such as `Choose the skill family`, `Materialize the accepted structure`, and `Prove routing on real questions`.
A page kind may contribute a specific record shape, but it may not impose a shared category list or weaken the verified-tick rule.

The section heading keeps the overall completed count; each rendered subsection shows its own count.
An empty subsection is omitted rather than displayed as a zero-row box.
The subsection heading receives the same generated Copy and Chat path as every other page subsection.
The counts half shipped 260731 (`render_items()` in `page_question.py`); the Chat path half remains open.

### 3 · The source: testable completion
Write `## Items to Finish` as checkboxes that another person can judge true or false.
Optional `###` headings group the following checkboxes until the next heading.
Their names come from the page context.
The rendered heading counts them automatically.
On S, each former Q-consumer stays together as one recognizable record and closes only after its answer is interpreted and integrated into Content.

## Items to Finish
### The renderer half
- [ ] 🧮 Render subsection counts without changing the overall count
      PROPOSED: shipped 260731 (`render_items()` in `page_question.py`): optional `###` headings group the boxes, each visible group badges its own `done/total`, empty groups are omitted, and this very list is the worked example.
- [ ] 🧭 Give each subsection a copyable Chat path
      Reuse the heading-focus contract on `QB5d`; copying or chatting from a contextual heading must identify this page, section, subsection, and source file.

### The ruling half
- [ ] 🏷 Settle the contextual naming rule
      A subsection must summarize the actual gap shared by its items; generic words such as Decisions or Build are examples, not required headings.
- [ ] 🧠 JL confirms this face owns Items to Finish
      Carved 260729 from QB4 §4 with the text verbatim; the history stays on `QB4`.

## Where we are
The base checkbox semantics and overall auto count ship.
The 260730 design added optional context-named subsections with per-group counts and heading-level Chat focus.
On 260731 the counts half shipped on JL's discussion ask: `render_items()` groups the boxes under `###` topic headings, badges each group `done/total`, omits empty groups, and the sidebar outline lists the groups with their counts.
This page's own list is regrouped as the worked example; heading-level Chat focus remains open.

- 260731 CC · 🧹 The convention was swept across the whole board
  JL: "could you go through all the pages to make them follow what we want ... especially for the subsections in the Where we are, Aims to Finish and Files."
  Seven agents, one per group folder, read every page and grouped the lists that earned it: 33 of 51 pages now carry `###` topic groups in Items.
  The other 18 were judged deliberately flat, because the convention grants that to a list of three or fewer, or to one coherent shipment such as `QB3`'s five ticked rows for a single 260724 landing.
  Every row moved verbatim and no box changed state, which the matrix's 🎯 column confirms page by page.

### Decision Now
- [ ] 🧮 Tick the shipped group counts
      PROPOSED: the renderer half landed 260731 (`render_items()`, the rail rows, and this page's own grouped list); a tick closes the matching Items row.
- [ ] 🧠 Confirm this face owns Items to Finish
      Carved 260729 from QB4 §4 verbatim; a tick here also closes the same row in Items to Finish.

## Files
- `src/page_question.py`
  The auto-counted heading and checklist rendering.
- `check.py`
  `open-with-done-items` / `partial-with-nothing-open`.

## Discussion
> JL: "Items to Finish" section should also have the subsection as well, each aim subsection should be categorized into different subsection topics.
> CC: Shipped 260731: `###` topic groups inside Items render with per-group `done/total` counts (`render_items()`), the sidebar outline lists them, and this page's own list is regrouped as the worked example.

## Log
260801 · §1 renamed "What Items to Finish conveys" and opened with the five-row protocol face diagram (conveys · holds · source · rules · omit) on JL's ask; master view on QB4 §0
260731 · The counts half shipped on JL's discussion ask: render_items() groups boxes under ### topic headings with per-group done/total, empty groups omitted; this page's Items regrouped as the worked example (0.70.0)
260730 · Corrected categories into contextual headings: Decisions, Build, Verify, and Dependencies remain examples only; each page names the real gap shared by its items
260730 · Designed typed Items to Finish subsections: Decisions, Build, Verify, and Dependencies, each with its own count and copyable Chat path
260729 · Marked frame under the base/variant model on QAa0: a kind contributes a record shape, never the checkbox semantics
260729 · Opened by carving QA4 §4 out to its own face, text verbatim
