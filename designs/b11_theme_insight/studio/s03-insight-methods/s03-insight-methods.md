s03 · Insight methods
=====================

**Topic:** what the Insight methods are, where their code lives in Tools, and how much of them the
code runs today (JL 261007: "what is the methods? for the insight discovery? collect all the
related code in the Tools and then create the excalidraw"). Drawn in the shape of b03's
s04-studio-and-report.

**Two drawings, two scripts:**

- `build_s03_insight_methods.py` writes `s03-insight-methods.excalidraw`, this topic's design
  drawing. It reads the cards, `guide/method.md`, `related/papers.md` and the code files every
  build, and keeps a person's marks (through haipipe-studio's `scripts/canvas.py`).
- `methods_drawing.py` writes the product's own picture,
  `plugins/haipipe-toolkit/servers/workbench-insight/guide/methods.excalidraw`, shown in the
  Methods drawing fold of Guide › Method. Moved here from
  `plugins/haipipe-toolkit/servers/workbench-insight/studio/` (261007). It reads the cards in
  `guide/methods/` and the papers in `related/papers.md`.


Files
-----

```text
s03-insight-methods/
├── s03-insight-methods.md              this notes file
├── build_s03_insight_methods.py        the builder of this topic's drawing; marks are kept on rebuild
│                                       (reads the cards through ../_build/insight_ui.py)
├── s03-insight-methods.excalidraw      the drawing: six frames, a plain prototype
├── s03-insight-methods.png             its preview
├── methods_drawing.py                  writes servers/workbench-insight/guide/methods.excalidraw
├── build_s03_insight_unit.py           the builder of the catalog drawing below; marks are kept on rebuild
├── s03-insight-unit.excalidraw         one Insight question as a catalog: the six steps' parts and options,
│                                       then one row per method (the design-unit catalog's shape)
└── s03-insight-unit.png                its preview
```

Rebuild the catalog: `python build_s03_insight_unit.py`, then
`python ../../../../plugins/haipipe-toolkit/skills/1_base/project/haipipe-studio/scripts/render_png.py s03-insight-unit.excalidraw s03-insight-unit.png 0.5`.

Rebuild: `python build_s03_insight_methods.py`, then
`python ../../../../plugins/haipipe-toolkit/skills/1_base/project/haipipe-studio/scripts/render_png.py s03-insight-methods.excalidraw s03-insight-methods.png 0.5`.
After the cards or papers change, also run `python methods_drawing.py`.


What the drawing holds
----------------------

```text
1 · Three families          asking (step 1), answering (step 3), reading (step 5) side by side:
                            what each asks, its cards, where they live, the skills they name,
                            papers, tests, whether a file records the method used
2 · From card to screen     card files -> designboard.method_cards / related_papers.papers_page
                            -> insightboard._render_methods -> Guide › Method, Related Paper;
                            red: no card reaches a question's run
3 · Today                   today's Insight workbench: Guide › Method, Guide › Related Paper,
                            Insight › <partition>; "on disk" under each; the pop-outs
4 · The sixteen cards       each card's move, reads, returns, tests, source and named skill
5 · the logic tree          guide/method.md -> family -> skill (with its cards) -> the code
                            that runs or checks it, with the tests on each arrow
Questions                   what is still open
```


What it found (261007)
----------------------

1. 16 method cards: 8 asking (in the base skill `haipipe-question-asking`), 5 answering and
   3 reading (in the insight server's `guide/methods/`). Steps 2, 4 and 6 have no methods, only
   rules.
2. The methods are text the workbench shows. No code reads a card. `run_question.py`,
   `check_block.py`, `check_evidence.py` and `record_check.py` enforce the steps and T0-T6, not
   a method.
3. No file records which method a question used. `haipipe-question-asking` returns `method:`,
   but `question.md` has no field for it, and nothing names an answering or reading method.
4. 7 of the 16 cards name a skill that has no folder yet (`haipipe-insight-by-<method>`).
5. T7 (robustness) and T8 (replication) have no code. `rivals` is a plan field only, and the
   POOL · SPLIT verdict of By heterogeneity is described only in `ref/partition.md`.


Proposed (261007)
-----------------

The proposed screens are one topic per level (JL 261007: "s11, s12, s13 ... instead of nesting all
the things together"): `../s11-block-level/`, `../s12-job-level/`, `../s13-task-level/`. In short,
each question names its three methods in its plan (Task), each row carries them as chips under its
D · I · K · W heading with the partitions as the third row (Block and Job › Work Details), and a
Job lists the cards that fit its level. The screen helpers and the card reader are shared in
`../_build/insight_ui.py`.

Open
----

See the drawing's Questions frame (red).

(write here, or mark the drawing in red)
