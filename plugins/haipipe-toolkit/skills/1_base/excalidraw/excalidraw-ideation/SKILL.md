---
name: excalidraw-ideation
description: >-
  An ideation drawn as one Studio topic: one large main frame with every idea as a step down from the paper's
  question, in groups (the lead group first, then neighbours, add-ons, on hold), and small frames that explain it,
  placed as stairs down and to the right: the setting in its real numbers, one card per lead idea (why it matters,
  if we find → it would mean, where it stands now), and the path from here to G0. Words in the topic's
  <topic>-drawing.yaml; the topic's builder forwards to scripts/ideation_drawing.py. haipipe-paper-ideation calls it
  for studio/s01-ideation/ whenever it is installed. Use to draw or redraw an ideation, to see a paper's ideas at a
  glance, or to give a new paper's s01 the same shape. Trigger: draw the ideation, ideation drawing, s01-ideation
  drawing, ideas as steps, idea cards, path to G0, /excalidraw-ideation.
allowed-tools: Bash, Read, Edit, Write, Grep, Glob
metadata:
  version: "0.1.0"
  last_updated: "2026-10-14"
  # version history: ./CHANGELOG.md
---

# /excalidraw-ideation · an ideation as one drawing, its ideas as steps

Asked 261013 on Physician-SPACE's Paper-LLMRecPhy-Quick s01-ideation, whose first drawing (19 equal frames in left-aligned
rows) was the counterexample:

1. **主次分明**: "一个很大的 frame，然后有一些小的 frame 是解释这些大的 frame 的".
2. **Stairs**: "一定要用阶梯状的结构 … 不能变成一个跟棋盘一样的东西".
3. **Never all left-aligned**: "你不能每一个都是朝左对齐".

Lifted from that topic's builder on 261014 so every paper draws its ideation the same way (JL 261014: "How do you
think we can add it to the themes/paper skills set"; "haipipe-paper-ideation will call it to draw when it is
available"). The shared script reproduces Paper-LLMRecPhy-Quick's drawing element for element.

```text
① 🪜 every idea as steps (main, large)                  ② the setting, in its real numbers (small)
   🎯 the key point
   the question ───────────────── the setting ────────▶
    └─▶ 🔥 the lead group ─ one box per idea ───────────▶   ③ 🔥 lead idea 1: why · if we find → means · now
         └─▶ the next group ─ names only                        ④ 🔥 lead idea 2 …
              └─▶ … down to on hold, or far                         ⑤ … one card each, a step lower and right
   │ then G0
   ▼
   ⑦ from here to G0 (small, below): steps, each "done when", lower and further right, then the person's choice
      │ G0 reads
      ▼
      ⑧ how it scores and where it goes (optional): each test's verdict, then the venues as stairs
```


The frames
----------

| frame | answers | read from |
|---|---|---|
| ① 🪜 every idea as steps | what the paper asks, every idea it has, which come first, which wait | `index` (heading, sub, key, question), `groups` (name, line, ideas), each idea's `short` |
| ② the setting | where the question lives, in numbers already on disk | `setting` (title, sub, key, `flow`, `numbers` as big/tag, `reading`) |
| ③ on, one per lead idea | why it matters, what it does, how new it is, what each finding would mean, where it stands | the lead group's ideas: `why`, `does`, `closest` and `new` (each optional), `results` (find → means, up to 3), `now`, `state` |
| the last, from here to G0 | what runs next and what "done" means, then the choice | `path` (title, key, `steps` with lines, `open`, `arrow`) |
| ⑧ how it scores, where it goes (optional) | what G0 reads: each test's verdict and who ran it, then the venues from ambitious to fallback | `evaluation` (title, sub, key, `checks`, `venues`, `open`, `arrow`) |

1. **One main frame**: every idea is on it, as a name on its group's step; only the lead group is in full weight
   (🔥). It may be large (`canvas.large`), never filled.
2. **Small frames explain it** (`canvas.explains`): the setting beside the question, each lead card beside its idea,
   each a step lower and further right; the path to G0 below the main frame, set in.
3. **Red is real**: an idea whose `now` starts with ❗ or ❓ is dashed on its step and its card's Now line is red;
   a path step or open line starting with ❓ is red. Never red for a guess.
4. **Numbers from disk**: every `big` in the setting is a number some file already holds; say where in its `tag`.
5. **The lead group is the first group**: reorder `groups` to change it; the cards follow.


The words
---------

`<topic>/<topic>-drawing.yaml`, beside the face:

```yaml
index:
  heading: "🪜 Thirteen ideas, from the loop to on hold"   # ①'s title
  frame: "① 🪜 Thirteen ideas, as steps"                   # ①'s frame name (default: ① + heading)
  sub: "…"                                                # grey, under the title
  key: "🔥 …"                                             # the key point, one sentence
  question: "…?"                                          # the root of the steps: the paper's question
  link: "the setting"                                     # the label on the arrow to ②
setting:
  title: "…"
  sub: "…"                                                # what each word below means
  key: "…"
  flow: ["🔑 what goes in", "⚙️ what happens", "👥 what comes out"]   # joined with →
  numbers: [{big: "444,691", tag: "what it counts, and where it was read"}]   # the first `show` (3) are drawn
  reading: "…"                                            # grey, the setting's reading
groups:                                                   # in order; the first is the lead group
- {name: "🔥 …", line: "why these come first", ideas: [i10, i01]}
- {name: "On hold, or far", line: "why they wait", ideas: [i08]}
ideas:
  i10:
    short: "…?"                                           # the idea as a short question: its name on the steps
    why: "…"                                              # Why it matters (lead ideas)
    does: "…"                                             # optional: the design in one line, under Why it matters
    closest: "…"                                          # optional: its novelty check's closest work, in one line
    new: "…"                                              # optional: what stays new against it, in one line
    results: [{find: "…", means: "…"}]                    # If we find → it would mean, up to 3 (lead ideas)
    now: "…"                                              # where it stands; ❗ or ❓ first makes it red
    state: "novelty: … · pilot: …"                        # the card's grey line (or read it from the face, below)
state:
  columns: {novelty: 2, pilot: 3}                         # optional: read the state from the face's Ideas table
path:
  title: "From here to G0"
  key: "…"
  steps: [{title: "…", lines: ["done when: …"]}]          # the last line of each step is drawn
  arrow: "then G0"
  open: ["❓ … (who decides)"]
evaluation:                                               # optional: ⑧, a step below the path
  title: "How it scores, and where it goes"
  key: "…"                                                # the verdict in one sentence, with the target
  checks:                                                 # one per test, two a row; ⬜ or ❓ first in verdict: red, dashed
  - {name: "🔍 Novelty", verdict: "✅ 8/10, PROCEED", by: "haipipe-novelty-check · ARIS novelty-check · 261014", note: "…"}
  - {name: "🎯 Journal fit", verdict: "⬜ not run", by: "haipipe-journal-fit", note: "…"}
  venues:                                                 # ambitious to fallback, as stairs joined by "if not"
  - {name: "Nature · Article, as a Registered Report", fit: "why it fits", rules: "from the venue contract"}
  - {name: "❓ a third target", fit: "…", rules: "…"}
  open: ["❓ …"]
```

For a paper's ideation, each lead card is a projection of the face's Idea division: `why` from Origin / Opportunity
or Hypothesis, `closest` and `new` from Core Claims / Novelty Check, `results` from Expected Outcomes, `now` from
Pilot Result; `path` from Next Evidence Queue and
Suggested Execution Order and G0 Readiness; the groups from Ideas (ranked) and Eliminated / Merged / Deferred;
`evaluation` from the Idea's test receipts (haipipe-ideation's novelty, pressure, journal-fit and Nature tests) and
its Journal / Venue Fit, each venue's `rules` only from a verified haipipe-paper-venue contract. The drawing makes
no decision the face does not hold.


Steps
-----

```bash
I=Tools/plugins/haipipe-toolkit/skills/1_base/excalidraw/excalidraw-ideation/scripts/ideation_drawing.py
python $I make <topic folder> [--force]    # the forwarding builder, and a words yaml from a template if none
#   write <topic>-drawing.yaml from the face
python <topic folder>/build_sNN_<topic>.py  # redraw; a person's marks are kept (canvas.write)
python Tools/plugins/haipipe-toolkit/skills/1_base/project/haipipe-studio/scripts/render_png.py <x>.excalidraw <x>.png
python Tools/plugins/haipipe-toolkit/skills/1_base/excalidraw/excalidraw-studio/scripts/check.py <x>.excalidraw
```

`make --force` replaces a topic's own builder: move the old one to the topic's `_archive/` first. Then read the
picture as a reader and call the reviewer (haipipe-studio `ref/reader-review.md`) with these questions, answered from
the picture alone:

1. What does the paper ask, in one sentence?
2. Which ideas come first, and why those?
3. For each lead idea: why does it matter, and what would each finding mean?
4. Where does each lead idea stand today, with a real number or a named gap?
5. What runs next, what does "done" mean for each step, and who makes the G0 choice?


Worked examples
---------------

- Physician-SPACE `examples-3-nlp/Project-LLMRec-Physician/paper/Paper-LLMRecPhy-Quick/studio/s01-ideation/`: the origin,
  sixteen ideas in four groups, its state read from the face's table (`state: columns`).
- DrFirst-SPACE `examples-4-learning/Project-ExpLearn-SMSDesign/paper/Paper-LoopExpLearning/studio/s01-ideation/`:
  thirteen ideas, the loop's four parts as the lead group, the state in each idea's yaml.


Boundary
--------

This skill draws an ideation; it decides nothing. What a paper's ideation holds and when it changes is
`haipipe-paper-ideation`'s; the ideas, their tests and the selection are `haipipe-ideation`'s; how any topic's
drawing looks is `excalidraw-studio`'s (this follows its principles and imports its `draw.py`); the topic folder,
face and sessions are `haipipe-studio`'s. A Job's drawing is `excalidraw-job`; a paper read against ours is
`excalidraw-read`.
