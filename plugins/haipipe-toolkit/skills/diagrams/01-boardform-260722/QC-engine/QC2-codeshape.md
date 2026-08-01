# The code's shape: one Law, three files

state: 🟡 PARTIAL · two files split and settled, the live layer's last item open
owner: JL
method: every split is a mechanical move under an output-identical gate, features second; a module is named for what it renders or serves, never for its layer (JL 260724)

## Question
The board's code keeps growing, and three files each crossed the size where one function nobody wants to open hides the next feature: `build.py`, the `src/` render modules, and `serve.py`.
How does the Python stay manageable as features keep landing, without breaking the two Laws the whole skill rests on?
This face is the split family's front door; each file's own move lives on its sibling faces.

The one hard part is shared by all three: the cure must not break the static invariant (one command, one self-contained board.html, no build toolchain) or one-grammar (every consumer imports the skill's parser, nobody rewrites it).
So the move is always the same shape, applied to a different file, which is why these are one topic and not three.

## Boundary
- ✅ Covered here
  The shared Law: what a split may and may not change, and why the three files are one question.
- ↪ Covered elsewhere
  `build.py` → `assets/`: `QC2a`. The `src/` render split: `QC2b`. `serve.py` → `live/`: `QC2c`.
  What SKILL.md exports about all this: `QC1`. The round trip the split files sit inside: `QC4`.

## Diagram

```
   one Law ── "mechanical move under an output-identical gate, features second"
        │
        ├── 🏗  build.py  →  assets/*.css *.js       QC2a  ✅ the template out of the parser
        ├── 🧩  src/ modules, named by what they render QC2b  ✅ page_question.py page_stage.py
        └── 🔌  serve.py  →  live/ mixins + thin CLI   QC2c  🟡 the live layer, moved area by area
```

## Content
### §1 Why one Law, three files
`QC2a` moved the CSS/JS out of `build.py` so the grammar stayed but the 800-line JS string left.
`QC2b` split the render Python into `src/` modules named for the page they render, giving each future feature a seat before it is written.
`QC2c` is `QC2b`'s deferred half: the same move on `serve.py`, held back only while the live layer was still forming.
Each face records its own gate; this page records only that the gate is the same one every time.

## Items to Finish
- [x] 🧪 build.py's template split out under a byte-identical gate (QC2a)
- [x] 🧪 the src/ render split, modules named by what they render (QC2b)
- [ ] 🧠 the live layer's last sequencing item (QC2c) closes before this topic is done

## Where we are
Two of three files are split and settled; the live layer split is built and serving, with one sequencing item left because QD2's chat is about to be rewritten as a session host.

### Decision Now
- [ ] 🧠 JL confirms the split family reads as one topic now that the three pages sit under QC2

## Files
- `build.py` · `src/` · `serve.py`
  The three files the Law is applied to.
- `QC2a-buildsplit.md` · `QC2b-srcsplit.md` · `QC2c-livesplit.md`
  The family, one file each.

## Log
260801 0140 · Repointed sibling ref QC7 -> QC4 after the full renumber (JL 260801)
260801 0130 · Opened as the split family's parent overview when QC2/QC3/QC8 were regrouped into QC2a/QC2b/QC2c (JL 260801)
