---
name: excalidraw-story
description: >-
  A paper's story drawn as one Studio topic: the story is the list of research questions it answers, and read in
  order the questions are its narrative. One large main frame shows the paper's question, then each research
  question as a step down and to the right, titled by its narrative question, with a card beside it: the answer so
  far, the claim it would make, and the evidence rows and Runs behind it, marked ✅ answered, 🔶 partly or ⬜ nothing
  yet (red, dashed). Small frames explain it as stairs: the pitch, what we will not claim, and below, the Runs still
  to make, who starts each, then G0. Read from the telling's face on every build (haipipe-paper-story's §2, §3, §5
  and §7), so the drawing never says what the story does not. haipipe-paper-story calls it for
  studio/sNN-story-<desk>-<idea>/. Use to draw or redraw a story, to see which research questions are answered and
  which are missing, or to give a new paper's story the same shape. Trigger: draw the story, story drawing, s02
  story, research questions as steps, which questions are answered, what supports each question, /excalidraw-story.
allowed-tools: Bash, Read, Write, Edit, Grep, Glob
metadata:
  version: "0.1.0"
  last_updated: "2026-10-19"
  # version history: ./CHANGELOG.md
---

# /excalidraw-story · the story as its questions, each with what supports it

JL 261019, on Paper-LLMRecPhy: "In the story studio s02-story, I think we might need to list the research questions,
and how could we support them"; "should we have a things named /excalidraw-story?"; "This is more like the story, do
you get it."; "please make the story, I think it should be composed a list of the questions to answer, and the
quesiton can be the narrative as well."

```text
① 📖 the paper's question (main, large)            ② the pitch (small)
   the story, as its questions: Q0 → Q1 → … → Q5      ③ what we will not claim
    └─▶ ✅ RQ0 · its narrative question ─▶ answer now · claim · E rows · T rows
         └─▶ 🔶 RQ1 · … ─▶ …
              └─▶ ⬜ RQ3 · … (red, dashed: nothing supports it yet)
      ④ from here to the send (small, below): each Run to make, who starts it, then 🙋 G0
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
| the title, the key | the first line; §2 Pitch's "The answer so far" item |
| the root | `**The paper's question**: …` |
| the chain under the key | each question block's `Name` (five words or fewer, itself a short question) |
| each step's title | `**The story, question by question**`: the numbered list of the questions in reading order |
| each step's card | the block's `Answer state`, its first claim, the E rows its hypotheses name, its `T` work rows |
| the marks | an answer state's first mark (✅ 🔶 ⬜ ❗); an E row's `support state`; a T row's `state` |
| ② the pitch | §2's numbered items |
| ③ what we will not claim | §5's `**We will not claim**:` list |
| ④ from here to the send | §7's T rows not yet done, with `starts`; then G0 when the face's `**G0:**` is not ✅ |

A question block is `#### 3.N · Question N · RQn` with `- **Name**`, `- **Question**`, `- **Answer state**` and
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
