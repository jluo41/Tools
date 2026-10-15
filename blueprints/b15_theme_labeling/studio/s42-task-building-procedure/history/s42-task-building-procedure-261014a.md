s42 · Task building procedure: from talking with the corpus to a signed Handoff
===============================================================================

**Tags:** `Levels`

**Stage:** explore

**Topic:** every step of the 🏗 building Task (`task-type: labeling-building`, s13), drawn the way s41 drew the
items Task: one tab per step, Operation over Result, screens as the tab develops. Building takes the items Task's
items and ends at a signed Label Handoff that the 🔍 scanning Task reads. It starts with the person talking with the
corpus, so they get to know the items while they label (JL 261014: "we want the user to talk with the corpus and
during the process to make the labeling ... get familiar with the labeling"). The first real one is dices350
`t03_dices350_response_safety_labeling`. The law (who decides what, the gates, the verbs) stays
`haipipe-labeling-building`'s; this topic draws the screens and steps over it.

**Feeds:** `reports/` q02_building_scanning_gates


Files
-----

```text
s42-task-building-procedure/
├── s42-task-building-procedure.md            this face; the drawing's words are the yaml block below
├── build_s42_task_building_procedure.py      the builder (s41's, its words from here)
├── s42-task-building-procedure.excalidraw    ① the four steps; ② ③ Explore, ④ Contract, ⑤ ⑥ ⑦ Rounds, ⑧ Handoff
└── s42-task-building-procedure.png           its preview
```

```yaml
key: "The outcome: one person's meaning of a label: a guideline (G*) and their own gold labels (D_cal*), signed as the Handoff."
heading: ["① The building Task: four steps", "the items become one person's labels and the guideline behind them"]
steps:
- title: "💬 Step 1 · Explore"
  run: "rNN_explore · soft"
  does: ["hold back the sealed set", "talk with the corpus"]
  tab: "1 · Explore: what the items say"
- title: "📜 Step 2 · Contract"
  run: "rNN_contract · soft"
  does: ["the meaning, its values", "signed by the person"]
  tab: "2 · Contract: the label, signed"
- title: "🔁 Step 3 · Rounds"
  run: "round_<t>/ · one per round"
  does: ["release a card", "label one by one"]
  tab: "3 · Rounds: gold and guideline grow"
- title: "✍️ Step 4 · Handoff"
  run: "rNN_handoff · hard"
  does: ["G* and D_cal*, frozen", "signed"]
  tab: "4 · Handoff: what scanning reads"
then:
  title: "🔍 scanning"
  run: "the next Task"
  does: ["tests on the sealed set"]
  tab: ""
arrows: ["notes, questions", "the meaning", "gold, rules"]
shape: ["one tab, as s41:", "Operation: the step · Sign · the prompt", "Result: cards, titles only"]
rule: "Every label is the person's; the agent asks and records. The sealed set is held back before anyone reads an item."
open: "❓ Open: Explore's notes are labels too; may they become gold in round 1?"
screen:
  task: "Task · t03 · building"
  line: "Labeling · Block b01 · Task t03 · <label> on <dataset>"
  tabs: ["1 · Explore", "2 · Contract", "3 · Rounds", "4 · Handoff"]
tabs:
- act: "Act 2 · Work › 1 · Explore"
  step_arrow: "Step 1"
  key: "Before any rule: the sealed set is held back, then the person reads the items with the agent and labels as they go, as notes."
  states:
  - title: "② Work › 1 · Explore · 1 of 2: hold back, then talk"
    tab: "1 · Explore"
    step: "💬 Step 1 · Explore"
    chip: "→ next"
    boxes:
    - title: "Input"
      rows: {Items: "items-v3 · 350 items", Map: "<k> groups, from Step 3 of items", Sealed: "<n> items, drawn across the groups, never shown"}
    prompt: "/haipipe-labeling-building <task> explore: hold back the sealed set, then talk with me through the items, group by group."
    mark: "copy it, talk in Claude or Codex"
    arrow: "you and the agent talk"
  - title: "③ Work › 1 · Explore · 2 of 2: what we learned"
    tab: "1 · Explore"
    step: "💬 Step 1 · Explore"
    chip: "✓ done"
    folded: ""
    sections:
    - {t: "💬 The talk", new: true}
    - {t: "📍 Items read, on the map", new: true}
    - {t: "🏷 Your labels, as notes", new: true}
    - {t: "❓ Questions and hard cases", new: true}
    - {t: "🧭 The meaning, proposed", new: true}
    mark: "the agent keeps the talk and fills one card per topic"
    arrow: "the agent proposes"
- act: "Act 3 · Work › 2 · Contract"
  step_arrow: "Step 2"
  key: "What the person learned becomes the label's meaning: its values, what each means, which items, who decides."
  states:
  - title: "④ Work › 2 · Contract: sign the meaning"
    tab: "2 · Contract"
    step: "📜 Step 2 · Contract"
    chip: "✍ sign"
    boxes:
    - title: "Contract · rNN_contract"
      dashed: true
      button: "Sign"
      mark: "you read it and sign"
      rows: {Label: "is the AI's last reply unsafe?", Values: "unsafe · safe · unsure", Unsure: "<what it means here>", Items: "items-v3, the sealed set out", Decides: "<you>"}
    prompt: "/haipipe-labeling-building <task> contract: write the Contract from the Explore cards, and stop for my Sign."
    mark: "copy it, run it in Claude or Codex"
- act: "Act 4 · Work › 3 · Rounds"
  step_arrow: "Step 3"
  key: "Each round: you release its card, label item by item with the agent, accept or reject each rule; the checkpoint says if another round is owed."
  states:
  - title: "⑤ Work › 3 · Rounds · 1 of 3: release the card"
    tab: "3 · Rounds"
    step: "🔁 Round 1"
    chip: "✍ release"
    boxes:
    - title: "Round card · round_1"
      dashed: true
      button: "Release"
      mark: "you read it and release"
      rows: {Draw: "20 items, at random", Seed: "<seed>", Expect: "<what we think we will find>", Small models: "label first, sealed"}
    prompt: "/haipipe-labeling-building <task> round: prepare round 1 under the released card, and open my session."
    mark: "copy it, run it in Claude or Codex"
    arrow: "the session opens"
  - title: "⑥ Work › 3 · Rounds · 2 of 3: label, one by one"
    tab: "3 · Rounds"
    step: "🔁 Round 1 · item 7 of 20"
    chip: "→ label"
    boxes:
    - title: "Item · <item id>"
      rows: {Before: "Person: … AI: … Person: …", Judged: "<the AI's last reply>"}
    - title: "Your label"
      dashed: true
      button: "Save"
      mark: "you label it"
      rows: {Label: "unsafe · safe · unsure", Why: "<one line>", Agent asks: "<a question, when the guideline is unclear>"}
    arrow: "the round closes"
  - title: "⑦ Work › 3 · Rounds · 3 of 3: the checkpoint"
    tab: "3 · Rounds"
    step: "🔁 Round 1"
    chip: "✓ done"
    folded: ""
    sections:
    - {t: "🏷 Your gold, so far", new: true}
    - {t: "📜 Guideline, this version", new: true}
    - {t: "✍️ Rules you accepted", new: true}
    - {t: "🤝 Small models vs you", new: true}
    - {t: "🗂 Register: the hard regions", new: true}
    - {t: "⏭ Another round, or Stop", new: true, button: "Stop"}
    mark: "a round per card; Stop when no region is open"
- act: "Act 5 · Work › 4 · Handoff"
  step_arrow: "Step 4"
  key: "Nothing new is made: the last guideline and your gold are frozen and signed; scanning reads only this."
  states:
  - title: "⑧ Work › 4 · Handoff: sign it"
    tab: "4 · Handoff"
    step: "✍️ Step 4 · Handoff"
    chip: "✍ sign"
    boxes:
    - title: "Handoff · rNN_handoff"
      dashed: true
      button: "Sign"
      mark: "you sign it"
      rows: {Guideline: "G* · v<n>", Gold: "D_cal* · <n> items", Rounds: "<t> rounds", Sealed: "<n> items, still unseen"}
    prompt: "/haipipe-labeling-building <task> freeze: freeze the Handoff from the last checkpoint, and stop for my Sign."
    mark: "then 🔍 scanning"
```


1 · The steps
-------------

```text
💬 1 Explore ──▶ 📜 2 Contract ──▶ 🔁 3 Rounds (repeat) ──▶ ✍️ 4 Handoff ──▶ 🔍 scanning
hold back the    the meaning,       card · label · rules ·     G* + D_cal*,       tests the small
sealed set; talk its values,        checkpoint                  signed             models on the
with the corpus  signed                                                            sealed set
```

| step | the engine's operations (haipipe-labeling-building) | the person's gate |
|---|---|---|
| 1 Explore | test-reserve · definition-discussion · discovery-search | none: notes only |
| 2 Contract | corpus-contract · guideline-seed | meaning (Sign) |
| 3 Rounds | round-prepare · weak-prelabel · human-calibration · guideline-learn · round-measure · round-close | release · item · rule · stop |
| 4 Handoff | handoff-freeze | freeze (Sign) |


Decided
-------

s42-D01 · Talking with the corpus is building's first step, Explore, before the Contract, not a Task type of its own
    (261014; the agent's choice, JL asked "how do you think?"): the Contract needs what the person learned, and the
    engine already has a slot for it (definition-discussion, discovery-search in P0). One Task stays one meaning.
s42-D02 · The sealed set is held back at the start of Explore, before anyone reads an item, drawn across the map's
    groups; Explore and every round never show it (closes s41's Open 1 for building).
s42-D03 · Four tabs, the same shape as s41 (Operation over Result, titles only, one-line prompts with user feedback):
    1 · Explore · 2 · Contract · 3 · Rounds · 4 · Handoff. Contract, round cards, Stop and the Handoff wait for a
    person's Sign or Release.


Open
----

1. Explore's notes are labels too: may round 1 take them as gold once confirmed, or must every gold label come from a
   round?
2. The values for DICES: unsafe · safe · unsure, or the engine's H · L · N (and what LOW means)?
3. Where the labeling session runs: in the workbench (⑥ as drawn) or in the chat with the agent, the workbench showing it.
4. How many items a round draws (20 drawn), and the sealed set's size.

(write here, or mark the drawing in red)
