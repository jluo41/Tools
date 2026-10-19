---
name: excalidraw-task
description: >-
  A Task drawn as one Studio topic, a staircase (the same idea as excalidraw-job's): its question on top, each Run or
  video a step lower and further right in reading order (the current Run marked, reruns quiet), and each step's
  results outside the frame, small: charts, its numbers as a table, its curves, its figures, a video's screenshots,
  what to check in red. A small frame explains it: words to know, formulas, what to be ready to answer, what is open.
  Read from the Task page, the face and each Run's result on every build. Use to draw a Discovery or work Task, to
  read what its videos said or its Runs measured at a glance, or to give each Task of a Job its own topic. Trigger:
  draw the task, task drawing, each task a topic, task staircase, what did the video say, task results as charts,
  /excalidraw-task.
allowed-tools: Bash, Read, Edit, Write, Grep, Glob
metadata:
  version: "0.6.0"
  last_updated: "2026-10-13"
  # version history: ./CHANGELOG.md
---

# /excalidraw-task · a Task as one drawing

Asked 261012, on Proj10's `discovery/b51_llm_serve`, after a Job's results topic listed only its Runs' states: "I
cannot still read the content of it. … should we have each task to be a sNN and each from to describe what is the
video told about". The same day, in the Job skill's session: "we even need to have the excalidraw-task as well, to
show the details of each tasks". So a Task gets its own topic, and each of its sources gets a frame that says what it
told, in words short and large enough to read.

The staircase (0.5.0, the default since 261013; JL: "you should also think about how to update the /excalidraw-task as
well, we try to follow the same idea", after the Job drawing became a staircase: "主次分明 … 一个很大的 frame，然后有一些
小的 frame 是解释这些大的 frame 的", "一定要用阶梯状的结构 … 留出足够的空白", "你的 results 应该是图和表格呀"):

```text
① 🪜 t01 · its question (main, large)                                     outside, small, level with each step
   🎯 the reading
   🧩 t01 · what it is · why it matters
    └─▶ ✅ r03 · its name · its key point ───────────────────────────────▶ 📊 2 screenshots · say it · ❓ check · 🔗
          └─ then r04: what it adds ─▶ ✅ r04 📌 · ⚙️ what it ran ────────▶ 📊 charts · numbers · 📈 curves
   ❓ what is open → in ②
     └──▶ ② 📖 words to know · 🧮 formulas · 🎤 be ready to answer · ❓ open (small, canvas.explains)
            └──▶ ③ in detail: each source's board read, transcript and full frame (only with detail: true)
```

`layout: rows` (or `plain`) keeps the frames before 0.5.0: the idea frame, then one frame per source, three to a row,
and a video's transcript frame read with /excalidraw-read (0.4.0).


**A board or cover, read** (0.6.0, JL 261014: "you can try to add your comments and understanding for the readers"):
a video whose cover is its finished whiteboard (or, `kind: cover`, a paper video's first slide) gets the frame
"rNN · The board, read" before its transcript: the picture whole on the left, each part it teaches outlined and
numbered in teaching order, and one note per part on the right (Board shows · Our reading · → this Task). It reads
`reads/<rid>-<BV>/board.yaml`: `board` {kind, image, source, link}, `key`, optional `ours`, and `regions`, each
{id, label, box [x0, y0, x1, y1] in the picture's pixels, shows, comment, link}. No transcript is needed.

The frames
----------

| frame | answers | read from |
|---|---|---|
| ① 🪜 The staircase | what the Task asks, its sources in reading order as steps, what each one is, which Run to read | the face's `task.reading`, `idea.intro`/`what`, `idea.why`; else the page's `## Opening` and first division; per source `name`, `says` (else its `**rNN**:` line), `config`, `role` (else `**How the videos fit**`), `current` |
| 📊 results, outside ① | what each source showed or measured, small, level with its step | per source: `charts` (as excalidraw-job's, from its result), its `show` numbers as a table, its `plot` curves, its `shots` (two screenshots), the pictures its result holds; no face words: the numbers its result names, else its `summary.headline`; `hook`; `check` (else the page's `**Check before reuse**`) in red; its link |
| ② 📖 its words | the words to know, the formulas, what to be ready to answer, what is open | `idea.terms`, `idea.formula` (drawn by mathtext), `idea.questions` (else the page's `**Interview questions**`), `open` |
| ③ in detail | each source's board or cover read, its transcript, and its full frame, read up close | only with `detail: true`; the board frame only when the topic has `reads/<rid>-*/board.yaml` |

1. **The stairs**: each source a step 380 px lower and right; past four, several share a column; room on purpose.
2. **Level with its results**: each step is spaced to its results block, so a line runs straight across to it.
3. **Results are pictures**: charts, a table, curves, screenshots, figures; never a paragraph of numbers.
4. **Quiet reruns**: once a Run is marked `current: true`, the others are grey names with no results block.
5. **Nothing under 28 px in ①**: the reading words stay large; ② may be small (canvas.explains).
6. **Red is real**: ❓ marks what to check against the source and anything missing, never a guess.
7. **From disk, every build**: an edited page or face is a changed drawing; a person's marks stay (canvas.write).


The face's words
----------------

Asked 261012, after the short version: "the frame can be even larger, and with more details as possible, suppose we
know nothing about these type of knowledge … could we get the screenshot of the video … I want the formula etc things
and understand them as well". So each frame teaches from zero: what the screen showed, the words to know first, each
formula with every symbol and a worked example, the steps with why, and the Run itself. Type stays large (28 px or
more); a frame grows as tall as its words need (read down). A frame that holds a screenshot or a formula is a picture
under check.py, so ⑦'s 200 words do not bind it; a frame without any is still held to ⑦.

```yaml
task:
  name: j01_decoding_generation/t01_decoding_sampling   # the Task folder, from the topic's Block
  order: []          # its Runs in drawing order (the page's Core path, then its Extension); empty: How the videos fit's order
  reading: ''        # the idea frame's key point; empty: idea.question, else the page's Opening
  idea:
    question: …      # 14 words or fewer
    intro: …         # what it is, for someone who knows nothing yet: 70 words or fewer (else `what`, one sentence)
    terms:           # 3 to 8 words to know first
    - {term: …, means: …}               # means: 25 words or fewer, plain
    formula:         # 0 to 3 core formulas
    - name: …                           # 8 words or fewer
      tex: "p_i = \\frac{e^{z_i/T}}{\\sum_j e^{z_j/T}}"   # matplotlib mathtext (item 2 below; in yaml a backslash is written twice)
      means: …                          # what it says in words, 30 words or fewer
      symbols: [["z_i", "the score of token i"], …]   # every symbol: its tex, its meaning in 12 words or fewer
      example: …                        # a worked example with numbers, 60 words or fewer; the first formula's
                                        # goes end to end, input to output ("Made-up" when the numbers are)
    mechanism:       # 4 to 6 {point, why}: how it runs, in order (drawn in place of `how`)
    - {point: …, why: …}                # point: 10 words or fewer; why: 30 words or fewer
    details:         # 3 to 6 {point, why}: 🔍 why it is built this way (else the page's Design details)
    how: [ … ]       # 3 to 6 steps, 20 words or fewer each
    why: …           # 50 words or fewer
    questions: [ … ] # 3 to 6 interview questions, 12 words or fewer each, or {q, a} with a short answer
  videos:
    r04:
      name: …        # the frame's title, 6 words or fewer
      says: …        # the key point, 20 words or fewer
      role: …        # the arrow into its frame, 5 words or fewer
      shots:         # 2 to 8 screenshots, in time order, four to a row
      - {at: 45, says: …}               # at: seconds into the video; says: what the screen shows, 20 words or fewer
      terms: [{term: …, means: …}]      # 2 to 6, as idea.terms
      formula: [ … ]                    # 0 to 2, as idea.formula; only what the video shows or says
      steps:         # 3 to 6, in the video's order
      - {point: …, why: …}              # point: 10 words or fewer; why: 30 words or fewer
      hook: …        # 20 words or fewer
      check: [ … ]   # 1 to 3, 10 words or fewer each: what to confirm against the video
  open: []           # open points, drawn red under the idea
```

1. **Screenshots**: `python scripts/video_frames.py <video url>` downloads a video once into the SPACE's ignored
   `_WorkSpace/video_frames/<id>/` (Bilibili through its player API at 480p, YouTube through yt-dlp), keeps its distinct
   frames (`frames/t0045.jpg`, by second) and lays them on `sheet.jpg`. Pick from the sheet, open the picked frames to
   read their formulas, and list them as `shots`; a build copies each into the topic's `assets/`, its empty top and
   bottom cropped. Bilibili caps how often one machine asks (HTTP 412, 514, 532): the script waits and tries again;
   fetch many videos a few at a time.
2. **Formulas**: written in matplotlib's mathtext, a subset of LaTeX: `\frac`, `\sum`, `\prod`, `\sqrt`,
   `\log`, `\exp`, `\max`, Greek letters, `_{}` and `^{}`, `\mid`, `\mathrm{}` (not `\text{}`), no `align`. A
   formula that does not parse is drawn as its text and named on stderr. Each is drawn into `assets/tex-<hash>.png`.
3. **From the page and the video only**: no new facts, numbers or claims; keep the page's hedges. A worked example uses
   the video's or the page's own numbers. Anything the video shows only on screen and the page has not checked goes
   to `check`.
4. **The Run**: drawn from its receipts, not the face: its address and date, state, worker, transcript, result files.
5. **The short fields** (`points`, `what`) stay readable as a fallback: a video with no `steps` draws its `points`.

A work Task (an experiment; no videos) has Runs with results instead. Its face lists them under `runs:`, keyed by the
Run's folder name, with the same `name`, `says`, `role`, `terms`, `formula`, `steps`, `hook` (what it means), `check`
(what is still to check), plus three fields read from the Run's result on every build (haipipe-studio job_results'
`at` reader: `file:key.inside`, a list for before → after, `fmt: pct`):

```yaml
  runs:
    r06_grpo_qwen3_0_6b:
      config:        # ⚙️ what it ran: 3 to 8 settings
      - {label: model, at: "metrics.json:config.model.path"}
      - {label: learning rate, at: "metrics.json:config.train.actor_lr"}
      show:          # 📊 what it measured: 2 to 6 numbers, a list of two for before → after
      - {label: GSM8K accuracy, at: ["eval.json:base.acc", "eval.json:trained.acc"], fmt: pct}
      plot:          # 📈 how it moved: 0 to 2 curves, from a json list (key) or a log (regex with x and y groups)
      - {title: train reward, file: train.log, regex: "step:(\\d+).*?reward/mean:([\\d.]+)", x_label: step}
```

The page keeps the full text. `name` is also how excalidraw-job finds this topic: its Job drawing writes
`→ details: sNN` on the Task's box.


The staircase adds three fields to the face's `task:` yaml; every field above keeps its meaning:

```yaml
  runs:
    r04_fold00_six_models_p12: {name: …, says: …, current: true}   # 📌 the Run to read; the others go quiet
  charts:                       # per source, as excalidraw-job's: bars from its result (each/value/low/high, or bars)
    r04_fold00_six_models_p12:
    - {title: "Jaccard by model (95% interval)", each: metrics.by_model, value: jaccard_low.point, fmt: pct}
  detail: false                 # true: ③, each source's transcript and full frame, after ②
  layout: ""                    # empty: the staircase; rows (or plain): the frames before 0.5.0
```


Commands
--------

```bash
T=Tools/plugins/haipipe-toolkit/skills/1_base/excalidraw/excalidraw-task/scripts/task_drawing.py
python $T make <task folder | job folder> [--nn NN] [--dry-run]   # one topic per Task, studio/sNN-<tNN>-<task>/
python $T draw <topic folder>                                     # redraw one (what its builder calls)
python $T preview <task folder> <out.excalidraw>                  # draw a Task anywhere; its Block is not touched
python Tools/plugins/haipipe-toolkit/skills/1_base/excalidraw/excalidraw-studio/scripts/check.py <topic>.excalidraw
```

1. **Numbers**: `--nn NN` numbers the Tasks from NN on (a Job's Tasks get NN, NN+1, …); without it, the next free
   numbers in the runs band (s21-s29), then the concepts (s01-s09). Proj10's `discovery/b51_llm_serve` took s01 to s10
   for its 10 Tasks, because its runs band held its four Job topics (s21 to s24).
2. **One topic per Task**: `make` refuses a Task that a face already names, and says which topic.
3. **The words**: `make` writes the face with an empty `task:` yaml, so the first drawing reads the page; then write
   `idea` and `videos` in the face (an agent per few Tasks, from each page, within the limits) and redraw.
4. **Check**: `check.py` after every build (⑦ for every frame); open the preview and read it.
5. **Save the session**: haipipe-studio's `new_topic.py session <block> sNN`, a pass of `run-draw-<sNN>`.


Boundary
--------

| Owner | Owns |
|---|---|
| `excalidraw-task` | a Task's drawing: its frames, the face's `task:` yaml, `make`, `draw`, `preview` |
| `excalidraw-job` | the Job's drawing, pointing to each Task's topic; its page readers (`section`, `concept`, `first_para`, `plain`), imported here |
| `haipipe-studio` | the topic folder, numbering, groups, sessions, `canvas.write`, `render_png.py` |
| `excalidraw-studio` | the principles every frame follows (⑦ few words), `draw.py`, `check.py` |
| `haipipe-discovery`, `haipipe-task` | the Task pages and Runs it reads; it never writes them |


Files
-----

```text
excalidraw-task/
├── SKILL.md                 this file
├── CHANGELOG.md             its versions
├── agents/openai.yaml       Codex's card
├── scripts/task_drawing.py  the page reader, the frames before 0.5.0, make, draw, preview; draw_task sends a
│                            Task to the staircase unless the face says layout: rows or plain
├── scripts/task_stairs.py   the staircase, each source's results block, its words frame
├── scripts/video_frames.py  a source video's screenshots: download once, distinct frames, a contact sheet
└── tests/test_task_drawing.py   a Task made on a small Block, drawn, checked; the face's words win; one topic per Task
```

The first Tasks drawn: Knowledge-Base's Proj10-LLM-Baseline `discovery/b51_llm_serve`, s01 to s10, one per Task
(261012).
