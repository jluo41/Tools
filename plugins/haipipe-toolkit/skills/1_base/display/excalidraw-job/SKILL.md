---
name: excalidraw-job
description: >-
  A Job drawn as one Studio topic, in few words: why it exists (its aim, each Task's question, when it is done), then
  what goes in, its Tasks in order with what each found, and what comes out, with the Job's reading as the key point.
  Two frames, read from disk on every build, by excalidraw-studio's principles (⑦: few words in a workflow). Each
  Task's detail is its own topic (excalidraw-task), pointed to from the Job's workflow. Use to draw a Job, to turn a
  Job's results topic (job_results.py) into the whole Job, or to see what a Job means at a glance. Trigger: draw the
  job, job drawing, the whole job, job aim plan results, what goes in and out, what did the job find, /excalidraw-job.
allowed-tools: Bash, Read, Edit, Write, Grep, Glob
metadata:
  version: "0.4.0"
  last_updated: "2026-10-12"
  # version history: ./CHANGELOG.md
---

# /excalidraw-job · a Job as one drawing

Asked 261012: "show the sNN as the excalidraw as the job, to make the job's aim, plan and results", then, on a Block
whose Job topics showed only their Runs' states, "我想在这个桌上把这个 job 的所有内容都展示出来" (what goes in and comes
out, what it concluded, its tables and figures). The same day: "add at least of words … when drawing the workflow" and
"make the draft to be less of wordy and concise" (excalidraw-studio ⑦). So the Job drawing says the whole Job in few
words, and each Task's detail (its videos, answers, tables, formulas) is the Task's own topic (excalidraw-task).

```text
Act 1 · the Job   ① 🎯 why: a mind map ─planned as─▶ ② 🔁 in → 🧩 t01 → 🧩 t02 → out, and what it found
                                                        each Task: its Runs' state · 💡 its finding · → sNN
                                                        🎯 the reading (the key point) · 📍 where it stands
```


The frames
----------

| frame | answers | read from |
|---|---|---|
| ① 🎯 Why | what the Job is for: its aim in the centre, each Task's question, when it is done, its Block | the face's `job.aim`, else the Job face's `goal:`; each Task page's `## Opening`; the Job face's `close:`, `answers:`; the Block's `spine:` |
| ② 🔁 In → Tasks → out, and what it found | what goes in, each Task with its Runs' state and its finding in one sentence, what comes out; the reading as the key point; 📍 where the Job stands | each Run's receipt (state, subject, platform); each page's first division: `**Why it matters**`, else `**Answer**`, `**Findings**`, `**What it is**`; the face's `job.reading`, `job.conclusions`, `job.open` (the first one); a Task topic whose face names the Task |
| ④ 🖼️ Its pictures | only when the Job has pictures | `.png` and `.jpg` in the Job's folders and Results (not `studio/`, `history/` or hidden) |

1. **Few words**: each frame is a map under ⑦: at most 200 words, at most a quarter of them a detail (under 28 px).
2. **Detail elsewhere**: a Task's videos, answers, tables and formulas are its own topic's; ② writes `→ details: sNN`
   on the Task's box when a face's `task:` yaml names it (`name: <jNN_job>/<tNN_task>`).
3. **From disk, every build**: a page edited is a drawing changed on the next build; the face holds only the aim, the
   reading, a Task's finding when the page's own is not the right one, and open points.
4. **Red is real**: a ❓ names something missing on disk (no goal, no close, no Question), never a guess.
5. **More than three Tasks**: ② lists them in one box, each with its pointer, and leaves the findings to their topics.


The face's words
----------------

```yaml
job:
  name: j01_math_classic_ml      # the Job folder, in the topic's Block
  aim: "…"                       # the Job's meaning in one sentence; empty: its face's goal: line
  reading: "…"                   # what it found: ②'s key point
  conclusions: {}                # per Task (t01 or its folder name): its finding, one sentence
  open: []                       # open points; the first is drawn red under ②, all stay in the face
  show: {}                       # per Run, values to read from its result (as job_results.py's show)
  # ③ "explained from zero" is drawn when any of these is written (asked 261012: "this is very thin … If I am a
  # reader, will this answer my questions for this job"):
  intro: "…"                     # what the Job is for and why the Block needs it, for a newcomer (70 words)
  terms: [{term: …, means: …}]   # 3 to 8 words to know first (means: 25 words)
  inputs: [ … ]                  # what goes in: real data, models, files, with counts (1 to 5); also ②'s 📥 box
  outputs: [ … ]                 # what comes out: files, rows, sizes, checkpoints (1 to 5); also ②'s 📤 box
  formula: [ … ]                 # 0 to 2, as excalidraw-task's: {name, tex, means, symbols, example}
  tasks:                         # every Task folder: what it asked, did and found (with its real numbers)
    t01_<task>: {asked: …, did: …, found: …}
  sure: "…"                      # how sure the reading is, and why (50 words)
  design:                        # the design, asked 261013: each Task's Runs as grids, one mark per Run, from disk
    frames:                      # a frame of grids each; a grid is one sweep (rows × cols of Runs)
      - title: "…"
        grids:
          - {task: t01_<task>, title: "…", rows: [1m, 10m], cols: ["0.1", "1"], ticket: "<path with {row} {col}>",
             evals: ["<path>", "<path>:<key>"], failed: [{row: "*", col: "1", why: "…"}]}
  open: [{item: …, closer: …}]   # each open point and exactly what would close it (strings still work)
```

③ reads answer first: [What this Job is for | What it concluded, and how sure], then [Words to know | What goes in |
What comes out], the formula, one box per Task (asked, did, its Runs' state, its numbers from disk, found, → details:
sNN), then [What is open, and what would close it] in red. It is marked a detail frame (excalidraw-studio's
`Drawing.detail`), held to ⑥'s floor at its type size. Then read it as a reader and call the reviewer:
haipipe-studio `ref/reader-review.md`.

A topic adopted from `job_results.py` keeps its `results:` yaml's reading and open points: `adopt` carries them into
`job:`. Write the aim and the reading from the Job's own pages; say in the face's Decided line that they were drafted.


Commands
--------

```bash
J=Tools/plugins/haipipe-toolkit/skills/1_base/display/excalidraw-job/scripts/job_drawing.py
python $J make <job folder> [--nn NN] [--dry-run]   # the Block's topic studio/sNN-<jNN>-<job>/ (s21-s29), drawn
python $J draw <topic folder>                       # redraw one (what the topic's builder calls)
python $J adopt <topic folder> [--aim '…']          # a one-Job results topic, now drawn as the whole Job
python $J preview <job folder> <out.excalidraw>     # draw a Job anywhere; its Block is not touched
python Tools/plugins/haipipe-toolkit/skills/1_base/display/excalidraw-studio/scripts/check.py <topic>.excalidraw
```

1. **One topic per Job**: `make` refuses a Job that already has one (a results topic or a whole-Job topic), and
   haipipe-studio's `job_results.py` reads a face's `job: name`, so neither makes a second.
2. **Adopt**: rewrites the builder and the face's Topic, Words and Files; keeps the folder's name and its Decided and
   Open lists, so links to the topic still work.
3. **Check**: `check.py` after every build; open the preview and read the whole picture, not a crop.
4. **Save the session**: haipipe-studio's `new_topic.py session <block> sNN`, a pass of `run-draw-<sNN>`.


Boundary
--------

| Owner | Owns |
|---|---|
| `excalidraw-job` | the Job's drawing: its frames, the face's `job:` yaml, `make`, `draw`, `adopt`, `preview` |
| `excalidraw-task` | a Task's own topic: its videos or Runs, its answers, tables, formulas (built by the Proj10 session, 261012) |
| `haipipe-studio` | the topic folder, numbering, sessions, `canvas.write`; `job_results.py`, a group of Jobs' results |
| `excalidraw-studio` | the principles every frame follows (⑦ few words), `draw.py`, `check.py` |
| `haipipe-job` | the Job face itself (`goal:`, `close:`, `answers:`, its Tasks in order); this skill only reads it |
| `haipipe-discovery`, `haipipe-task` | the Task pages and Runs it reads; it never writes them |

Its readers (`labelled`, `section`, `concept`, `tables`, `formulas`, `aims`, `task_info`, `table`) are for
excalidraw-task to import too, so a Task's page reads the same in both drawings.


Files
-----

```text
excalidraw-job/
├── SKILL.md                this file
├── CHANGELOG.md            its versions
├── agents/openai.yaml      Codex's card
├── scripts/job_drawing.py  the frames, the readers, make, draw, adopt, preview
└── tests/test_job_drawing.py   a Job made on a small Block, drawn, checked; one topic per Job; a Task's pointer
```

The first Jobs drawn: Knowledge-Base's Proj10-LLM-Baseline `discovery/b01_ml_foundations` s21 to s23 (adopted
261012). Its own Studio topic is Tools' `blueprints/b31_excalidraw/studio/s06-excalidraw-job/`.
