# Propose a Block's structure from its material

`/haipipe-work propose <Block>`: the Block holds material that does not fit the fixed work frame (logs,
transcripts, notes, a pile of files). Read the material, then propose the Block's own sections and its Jobs.
The person ticks the proposal, and only then is it made. The fixed frame (Goal · Requirements · MindMap;
Data · Values · Displays) stays the default for a Block whose material does fit it. Never force-fit material into it.

```text
material ─▶ read ─▶ proposal ─▶ 🙋 the person ticks ─▶ make ─▶ check the four views
```

## 1. Read the material

List what is on disk (`board.md`, `src/`, `related/`, Studio topics, deliverables). Find the groups the
material itself uses: its fields (an `Area:` on every entry), its dates, its people, its open items.
A group the material already uses is a better section than one you invent. Count the entries in each group;
a group with one entry joins its neighbour.

## 2. Propose

Write one proposal with three parts, each line a candidate the person can tick:

| Part | Holds | Comes from |
|---|---|---|
| 📋 Overview sections | what a reader needs before the results: the goal, the span (a week, the phases), who took part, the main deliverable | the material's frame |
| 🔎 Findings sections | the results, one section per group of the material (a decision Area, a topic, a question), then what is still open | the material's own groups |
| 📈 Plan + Results Jobs | the work that turned the material into those sections: one Job per kind of work, its Tasks, and each Run that really ran | the scripts and agents that read and built it |

A Job needs Tasks and Runs, or it shows only "not run" bars. Record only Runs that happened. A Run
that happened before the Block existed gets a `run.yaml` with `status: done` and a `result/README.md`
naming what it returned. A Run you can repeat (a build script) gets a ticket and is run again now,
so its receipt is real.

Put the proposal to the person as a collection Run (`haipipe-interaction`, `question_collection.md`), with
your picks ticked. Applying the answer is this procedure's step 3.

## 3. Make

1. **Sections are files a script writes**: a build script writes one Markdown file per section, `# <emoji> <title>` on
   its first line, so a rebuild keeps them in step with the material. Do not hand-write what the material already says.
   A long list of entries (a decision log) is one list item per entry with its detail as sub-items: the page shows
   each entry as a card that opens. Write the sub-items as labels: `Session:` and `Area:` become chips, `Decided:`,
   `JL asked:` and `Built:` tinted blocks. A list whose items start with a bold time (`**12:53** · title`) is drawn
   as a timeline; an item bold all through (`**12:39 to 13:51 · title**`) is a phase on it, and the entries under a
   phase come after it.
2. **The face names them**: `board.md` gets `## Review Content` (the Overview), `## Plan + Results` (after the
   Jobs, numbered on: what happened when, such as one section per day) and `## Findings`. Each
   `### <emoji> <title>` is one numbered section; a line `embed: <path>` brings in a `.md`, rendered, or an `.svg` drawing, inline (hover titles work, scripts are stripped). When the material is many people or sessions over time, draw it first as a transit map (one line per person or session, a station per entry in time order, a shared entry joining the lines; the method of trace-canvas), as Overview's section 1. In those sections, a line `each: <glob>` makes one section per matching `.md`, titled by its `# ` line.
3. **Native sections, never a website**: page content maps to the Block's own sections as Markdown. A standalone
   `.html` page (a replay site, a dashboard) is never framed into a section, a Deliverable card or a Service
   (JL 261114: "map the content to the website structure of the workbench UI"); its content becomes sections.
4. **Jobs on the ladder**: `jNN_<job>/jNN_<job>.md` (`state:`, `goal:`, `emoji:`, `use-case:` and `## Tasks`), its Task
   faces, and the Runs from step 2. The face's `## Jobs` lists them in order. `use-case:` names the Plan + Results
   section that Job falls under.

The renderer is `servers/workbench/page/work_sections.py`. A face without these sections keeps the fixed frame.

## 4. Check

Run the ★ AI-eval (`haipipe-ui` rule 12): a fresh agent scores every section's readability into
`<Block>/ai-eval/readability.json`; fix any section under 7 and read it again. Then open the four views (`/wb <Block>`):
every proposed section is there, numbered, not empty, with its ★; Plan + Results shows
each Job with its Tasks and Runs ✅; no traceback; no console errors. Then rebuild once and open them again: the
sections must still match the material.

## First case

`blueprints/Project-Replay/work/b41_agreeablerx_replay`: 269 decisions from eleven sessions.

- **Overview**: Goal.
- **Plan + Results**: `j01_decision_logs` (two reading Runs) and `j02_replay_build` (the `src/build.py` Run), then
  one section per day: its phases, then each decision folded.
- **Findings**: Sessions, one section per decision Area, then Still open.
