---
name: ideation
part-of: hai-draw
description: "Draws an ideation as one Studio topic: every idea a step down from the paper's question, with small frames for the setting, a card per lead idea and the path to G0. Use to draw or redraw an ideation. Trigger: draw the ideation, ideation drawing, idea cards, path to G0, /hai-draw ideation."
allowed-tools: Bash, Read, Edit, Write, Grep, Glob
metadata:
  version: "0.1.1"
  last_updated: "2026-10-26"
  # version history: ./CHANGELOG.md
---

# /hai-draw ideation · an ideation as one drawing, its ideas as steps

One large main frame holds every idea as steps from the paper's question; small frames explain it (principle ①),
each a step lower and further right (principle ③). `ideation_drawing.py` draws it the same way for every paper.

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
2. **Small frames explain it** (principles ①, ③): the setting beside the question, each lead card beside its
   idea; the path to G0 below the main frame, set in.
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
  - {name: "🔍 Novelty", verdict: "✅ 8/10, PROCEED", by: "hai-novelty-check · ARIS novelty-check · 261014", note: "…"}
  - {name: "🎯 Journal fit", verdict: "⬜ not run", by: "hai-journal-fit", note: "…"}
  venues:                                                 # ambitious to fallback, as stairs joined by "if not"
  - {name: "Nature · Article, as a Registered Report", fit: "why it fits", rules: "from the venue contract"}
  - {name: "❓ a third target", fit: "…", rules: "…"}
  open: ["❓ …"]
```

For a paper's ideation, each lead card is a projection of the face's Idea division: `why` from Origin / Opportunity
or Hypothesis, `closest` and `new` from Core Claims / Novelty Check, `results` from Expected Outcomes, `now` from
Pilot Result; `path` from Next Evidence Queue and
Suggested Execution Order and G0 Readiness; the groups from Ideas (ranked) and Eliminated / Merged / Deferred;
`evaluation` from the Idea's test receipts (hai-ideation's novelty, pressure, journal-fit and Nature tests) and
its Journal / Venue Fit, each venue's `rules` only from a verified hai-paper-venue contract. The drawing makes
no decision the face does not hold.


Steps
-----

```bash
I=Tools/plugins/haipipe-toolkit/skills/1_base/draw/hai-draw/gallery/ideation/scripts/ideation_drawing.py
python $I make <topic folder> [--force]    # the forwarding builder, and a words yaml from a template if none
#   write <topic>-drawing.yaml from the face
python <topic folder>/build_sNN_<topic>.py  # redraw
python Tools/plugins/haipipe-toolkit/skills/1_base/project/hai-studio/scripts/render_png.py <x>.excalidraw <x>.png
python Tools/plugins/haipipe-toolkit/skills/1_base/draw/hai-draw/scripts/check.py <x>.excalidraw
```

`make --force` replaces a topic's own builder: move the old one to the topic's `_archive/` first. Then the reader
review (hai-studio `ref/reader-review.md`) asks these ideation questions, from the picture alone:

1. What does the paper ask, in one sentence?
2. Which ideas come first, and why those?
3. For each lead idea: why does it matter, and what would each finding mean?
4. Where does each lead idea stand today, with a real number or a named gap?
5. What runs next, what does "done" mean for each step, and who makes the G0 choice?


Worked examples
---------------

- `〈Project-SPACE〉` `examples-3-nlp/Project-LLMRec-Physician/paper/Paper-LLMRecPhy-Jama/s01-ideation/`: the origin,
  sixteen ideas in four groups, its state read from the face's table (`state: columns`).
- `〈Client-SPACE〉` `examples-4-learning/Project-ExpLearn-SMSDesign/paper/Paper-LoopExpLearning/s01-ideation/`:
  thirteen ideas, the loop's four parts as the lead group, the state in each idea's yaml.


Boundary
--------

This kind draws an ideation; it decides nothing. What a paper's ideation holds and when it changes is
`hai-paper-ideation`'s; the ideas, their tests and the selection are `hai-ideation`'s; how any drawing
looks is hai-draw SKILL.md's (§ The principles, § The draw.py look); the topic folder,
face and sessions are `hai-studio`'s. A Job's drawing is `hai-draw job`; a paper read against ours is
`hai-draw read`.
