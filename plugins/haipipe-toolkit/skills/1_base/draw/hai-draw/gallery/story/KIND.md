---
name: story
part-of: hai-draw
description: "Draws a paper's story as one Studio topic: each research question a step down with its card, hypotheses and claims, marked answered, partly or not yet. Use to draw a story or see which questions are answered. Trigger: draw the story, story drawing, research questions as steps, /hai-draw story."
allowed-tools: Bash, Read, Write, Edit, Grep, Glob
metadata:
  version: "0.2.2"
  last_updated: "2026-10-26"
  # version history: ./CHANGELOG.md
---

# /hai-draw story · the story as its questions, each with what supports it

The script draws the whole drawing; the five-part drawing is not involved. A story is the list of research questions
the paper must answer, each with what supports it; the questions in order are the narrative.

```text
① 📖 the paper's question (main)          ② the narrative, if the questions are answered
   the paper's question, the key point     ✅ RQ1 card ─▶ RQ1 · what we expect, and why ─▶ RQ1 · what the paper can say
    └─▶ ✅ RQ1 · name · research question       why it matters   each hypothesis, its theory,    if answered; each claim,
         └─▶ 🔶 RQ2 · …                          now · theory     the E rows that test it          now, if it fails
              └─▶ ⬜ RQ3 · … (red, dashed)        · Runs          🔶 RQ2 card ─▶ … one row per question
      below, as stairs: from here to the send (until a plan exists) · the theory · what we will not claim · venues
```

It is s01's sibling: hai-draw ideation draws the ideas a paper could tell; this draws the one telling, as the
questions it must answer. Same look as hai-draw ideation (principles ① ③ ⑧), and like hai-draw job it is read from
disk on every build.


What it reads
-------------

Everything comes from the telling's face, `sNN-story-〈desk〉-〈idea〉/sNN-story-〈desk〉-〈idea〉.md` beside the Board's Jobs (an older Board: in `studio/`), in
hai-paper-story's form. Nothing is copied into a second words file.

| drawing | from the face |
|---|---|
| the title | the first line |
| the root, the main frame's key point | `**The paper's question**: …` (it may wrap onto several lines) |
| the main frame's size | three times every other frame (`MAIN_K`), words and boxes alike, a signboard the rest explain (principles ① ⑦) |
| each step's short label | each question block's `Name` (five words or fewer, itself a short question) |
| each step | the block's `Name` and its `Research question`, one long plain sentence (its sub-questions go in the card) |
| the questions, when the face has no blocks | the Board's Questions' reports (board.md `## Questions`, each `report:`), else an older §3 table `\| RQ \| question \| why the paper needs it \| … \| answer state \|` |
| each question's row | one wide frame, three panels read left to right, each 2,800 px wide with its words scaled up: **the card**, `Why it matters`, `Answer state` (Now), the §4 theories whose `questions` name it, its `T` rows; **what we expect, and why**, each hypothesis with its theory (the closing bracket of its sentence) and its E rows, marked; **what the paper can say**, `If answered`, then each claim with `Now` and `If it fails`. The frame is marked `canvas.columns` (principle ⑨) and large. The rows stand with the narrative top to bottom beside the main frame as a Job's results (hai-draw job `results_layout`); every other one a step right |
| the theory | §4's `\| theory \| the idea in one line \| … \| questions \| … \| role \| reference \|` table, as stairs by role (core, mechanism, tension, ethics, framing, governing, answering; set aside grey and dashed), each with the questions it serves and the hypotheses §3's `\| theory \| it says \| so here \| hypotheses \|` table gives it; its key is the `- **Theory**` bullet's one-line claim ("Said for a reviewer in one line:" or "The contribution:") |
| ② the narrative | `**The narrative, if the questions are answered**`: what the paper can say, step by step |
| the marks | an answer state's first mark (✅ 🔶 ⬜ ❗); an E row's `support state`; a T row's `state` |
| the answer so far | §2 Pitch's "The answer so far", heading the narrative frame (in the main frame when there is no narrative; the pitch frame shows only then) |
| what we will not claim | §5's `**We will not claim**:` list |
| where the story could go | §9's `| V |` table: each venue a step down, red and dashed when it has no desk record |
| the target venue's details | an optional `#### V1 · 〈title〉` bullet block under §9: one card under the venue list; each further `#### V1 · 〈title〉` block (how the paper meets the call, with its evidence; why it is doable by the deadline) is a frame of its own to the right of the venue list |
| how it fits together | with §4's theory table, inside the main frame: each step reads on to its right as one table, its theories, its hypotheses and its claims |
| from here to the send | §7's T rows not yet done (`work` or `name`, `where` or `feeds`, `starts`); red when `starts` says "〈person〉 starts" (new model calls); then G0 when the face's `**G0:**` is not ✅. Drawn only until the Board's studio holds a plan topic (`s03-paper-dataflow` or `s04-paper-workflow`), which owns the Runs and the dates; then one line under the main frame names it, with G0's mark |

A question block is `#### 3.N · Question N · RQn` with `- **Name**`, `- **Research question**`, `- **Question**`,
`- **Why it matters**`, `- **Answer state**`, `- **If answered**` and
the groups Hypotheses (`- **1a** · Short: sentence · tested by E3, E4`), Potential claims (`- **1a** · C1 · from
1a, 1b · Short: statement`, with `- **Now**`), Potential work (`- **T3** · for 1a`). A claim may come from several
hypotheses.


Use
---

```bash
S=Tools/plugins/haipipe-toolkit/skills/1_base/draw/hai-draw/gallery/story/scripts/story_drawing.py
.venv/bin/python $S make <Board>/s02-story-<desk>-<idea>     # once: the topic's forwarding builder
.venv/bin/python <Board>/s02-story-<desk>-<idea>/build_s02_story_<desk>_<idea>.py     # every redraw
```

1. **Write the face first**: the list of questions in reading order, one block per question, each number naming its
   Run. The drawing is a projection; a change to the story is a change to the face, then a redraw.
2. **Mark honestly**: an answer state starts ✅ only when a Run's Result answers it, 🔶 when a Run answers part of it
   or only one model, ⬜ when nothing does. A ⬜ is drawn red and dashed, so the missing shows at once.
3. **What is missing becomes Runs**: a ⬜ question names its T rows in §7 with who starts them; a Run that costs new
   model calls says `〈person〉 starts`, and nothing is started from the drawing.
4. **G0 is a mark, not a gate**: a story may exist before G0; the face's `**G0:**` line says whether the person has
   chosen it, and the path ends on G0 until then.
5. **Never edit the drawing by hand**: the builder's boxes are redrawn from the face (hai-draw SKILL.md § Redraw a
   topic).


Files
-----

```text
hai-draw/gallery/story/
├── KIND.md
├── CHANGELOG.md
├── scripts/story_drawing.py     draw <topic> · make <topic>
└── tests/test_story_drawing.py  a made-up telling: the reading, the marks, a drawing
```
