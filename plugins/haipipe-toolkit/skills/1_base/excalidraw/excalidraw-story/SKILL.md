---
name: excalidraw-story
description: >-
  A paper's story drawn as one Studio topic: the story is the list of research questions it answers, and read in
  order the questions are its narrative. One large main frame shows the paper's question, then each research
  question as a step down and to the right, titled by its narrative question, with one wide frame beside it, three
  panels read left to right: its card (why it matters, the answer so far, its theories, its Runs), what we expect and why (each
  hypothesis with the theory it comes from and the evidence rows that test it), and what the paper can say (its
  claims), marked ✅ answered, 🔶 partly or ⬜ nothing yet (red, dashed). Small frames explain it as stairs: the
  theory (§4's table, by role), what we will not claim, the venues, and the Runs still to make until the paper's
  plan (haipipe-paper-plan) takes them over. Read from the telling's face on every build (haipipe-paper-story's §2,
  §3, §4, §5 and §7), so the drawing never says what the story does not. haipipe-paper-story calls it for
  studio/sNN-story-<desk>-<idea>/. Use to draw or redraw a story, to see which research questions are answered and
  which are missing, or to give a new paper's story the same shape. Trigger: draw the story, story drawing, s02
  story, research questions as steps, which questions are answered, what supports each question, /excalidraw-story.
allowed-tools: Bash, Read, Write, Edit, Grep, Glob
disable-model-invocation: true
metadata:
  version: "0.2.1"
  last_updated: "2026-10-26"
  # version history: ./CHANGELOG.md
---

# /excalidraw-story · the story as its questions, each with what supports it

JL 261019, on Paper-LLMRecPhy-Jama: "In the story studio s02-story, I think we might need to list the research questions,
and how could we support them"; "should we have a things named /excalidraw-story?"; "This is more like the story, do
you get it."; "please make the story, I think it should be composed a list of the questions to answer, and the
quesiton can be the narrative as well."

```text
① 📖 the paper's question (main)          ② the narrative, if the questions are answered
   the paper's question, the key point     ✅ RQ1 card ─▶ RQ1 · what we expect, and why ─▶ RQ1 · what the paper can say
    └─▶ ✅ RQ1 · name · research question       why it matters   each hypothesis, its theory,    if answered; each claim,
         └─▶ 🔶 RQ2 · …                          now · theory     the E rows that test it          now, if it fails
              └─▶ ⬜ RQ3 · … (red, dashed)        · Runs          🔶 RQ2 card ─▶ … one row per question
      below, as stairs: from here to the send (until a plan exists) · the theory · what we will not claim · venues
```

It is s01's sibling: excalidraw-ideation draws the ideas a paper could tell; this draws the one telling, as the
questions it must answer. Same look (excalidraw-ideation's boxes and small frames, one main frame, stairs, white
space; JL 261013), and like excalidraw-job it is read from disk on every build.


What it reads
-------------

Everything comes from the telling's face, `studio/sNN-story-<desk>-<idea>/sNN-story-<desk>-<idea>.md`, in
haipipe-paper-story's form. Nothing is copied into a second words file.

| drawing | from the face |
|---|---|
| the title | the first line |
| the root, the main frame's key point | `**The paper's question**: …` (it may wrap onto several lines) |
| the main frame's size | three times every other frame (`MAIN_K`), words and boxes alike, marked `canvas.signboard` so it may hold 600 words: the signboard the rest explain (JL 261020: "它是主，其他都是次，我们要做到主次分明") |
| each step's short label | each question block's `Name` (five words or fewer, itself a short question) |
| each step | the block's `Name` and its `Research question`, one long plain sentence (its sub-questions go in the card) |
| the questions, when the face has no blocks | the Board's Questions' reports (board.md `## Questions`, each `report:`), else an older §3 table `\| RQ \| question \| why the paper needs it \| … \| answer state \|` |
| each question's row | one wide frame, three panels read left to right, each 2,800 px wide with its words scaled up (JL 261020: "could we just have one frame, one very wide frame for each RQ?"): **the card**, `Why it matters`, `Answer state` (Now), the §4 theories whose `questions` name it, its `T` rows; **what we expect, and why**, each hypothesis with its theory (the closing bracket of its sentence) and its E rows, marked; **what the paper can say**, `If answered`, then each claim with `Now` and `If it fails`. The frame is marked `canvas.columns` (⑨ judged per panel) and large. The rows stand with the narrative top to bottom beside the main frame as a Job's results (excalidraw-job `results_layout`); every other one a step right |
| the theory | §4's `\| theory \| the idea in one line \| … \| questions \| … \| role \| reference \|` table, as stairs by role (core, mechanism, tension, ethics, framing, governing, answering; set aside grey and dashed), each with the questions it serves and the hypotheses §3's `\| theory \| it says \| so here \| hypotheses \|` table gives it; its key is the `- **Theory**` bullet's one-line claim ("Said for a reviewer in one line:" or "The contribution:"). JL 261020: "for the s02, of the MISQ, where is the theory? ????" |
| ② the narrative | `**The narrative, if the questions are answered**`: what the paper can say, step by step |
| the marks | an answer state's first mark (✅ 🔶 ⬜ ❗); an E row's `support state`; a T row's `state` |
| the answer so far | §2 Pitch's "The answer so far", heading the narrative frame (in the main frame when there is no narrative; the pitch frame shows only then) |
| what we will not claim | §5's `**We will not claim**:` list |
| where the story could go | §9's `| V |` table: each venue a step down, red and dashed when it has no desk record |
| the target venue's details | an optional `#### V1 · <title>` bullet block under §9: one card under the venue list; each further `#### V1 · <title>` block (how the paper meets the call, with its evidence; why it is doable by the deadline) is a frame of its own to the right of the venue list (JL 261020: "再多加一些 evidence，去说它怎么 work 的 ... 为什么这是一个 plausible work") |
| how it fits together | with §4's theory table, inside the main frame: each step reads on to its right as one table, its theories, its hypotheses and its claims (JL 261020: "做个 table 之类的 ... 其实可以放到这个大里面去") |
| from here to the send | §7's T rows not yet done (`work` or `name`, `where` or `feeds`, `starts`); red when `starts` says "<person> starts" (new model calls); then G0 when the face's `**G0:**` is not ✅. Drawn only until the Board's studio holds a plan topic (`s03-paper-dataflow` or `s04-paper-workflow`), which owns the Runs and the dates; then one line under the main frame names it, with G0's mark (JL 261020: "is this more like the plan? right? Maybe we can drop it") |

A question block is `#### 3.N · Question N · RQn` with `- **Name**`, `- **Research question**`, `- **Question**`,
`- **Why it matters**`, `- **Answer state**`, `- **If answered**` and
the groups Hypotheses (`- **1a** · Short: sentence · tested by E3, E4`), Potential claims (`- **1a** · C1 · from
1a, 1b · Short: statement`, with `- **Now**`), Potential work (`- **T3** · for 1a`). A claim may come from several
hypotheses.


Use
---

```bash
S=Tools/plugins/haipipe-toolkit/skills/1_base/excalidraw/excalidraw-story/scripts/story_drawing.py
.venv/bin/python $S make studio/s02-story-<desk>-<idea>     # once: the topic's forwarding builder
.venv/bin/python studio/s02-story-<desk>-<idea>/build_s02_story_<desk>_<idea>.py     # every redraw
```

1. **Write the face first**: the list of questions in reading order, one block per question, each number naming its
   Run. The drawing is a projection; a change to the story is a change to the face, then a redraw.
2. **Mark honestly**: an answer state starts ✅ only when a Run's Result answers it, 🔶 when a Run answers part of it
   or only one model, ⬜ when nothing does. A ⬜ is drawn red and dashed, so the missing shows at once.
3. **What is missing becomes Runs**: a ⬜ question names its T rows in §7 with who starts them; a Run that costs new
   model calls says `JL starts`, and nothing is started from the drawing.
4. **G0 is a mark, not a gate**: a story may exist before G0 (JL 261019: "there are not s02, why????"); the face's
   `**G0:**` line says whether JL has chosen it, and the path ends on G0 until then.
5. **Never edit the drawing by hand**: a person's marks on the canvas are kept (haipipe-studio canvas.write); the
   builder's boxes are redrawn from the face.


Files
-----

```text
excalidraw-story/
├── SKILL.md
├── CHANGELOG.md
├── scripts/story_drawing.py     draw <topic> · make <topic>
└── tests/test_story_drawing.py  a made-up telling: the reading, the marks, a drawing
```
