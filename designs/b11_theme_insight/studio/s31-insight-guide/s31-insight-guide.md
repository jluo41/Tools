s31 · Insight Guide
===================

**Topic:** the insight workbench's Guide tab, cut by level, the way b16's s31-paper-guide cuts the paper's
(JL 261007: "follow this ... could you make the s31 for the insight guide as well?"), in the style of b03's
s31-guide: the four Views (Description · Method · RoadMap Draw · Related Paper), each body three folding
sections Block · Job · Task, cards in one shape per View; one frame per level, its section open, the other
two folded, "on disk" under each, then that level's open points in red.

**Feeds:** `reports/` q01_insight_ladder (and b03's q08_workbench_base: one shared base, a theme each).

**Source:** the builder is b16's, adapted (`build_s31_insight_guide.py`, b03's s31-guide screen and cards; was s03-guide). Each
level's content is its own file: `guide_block.py` · `guide_job.py` · `guide_task.py`. What is read live
(`insight_guide_live.py`): the six Space cards' third rows and run buttons from s11 · s12 · s13's screens
(until `insight_theme.py` exists), today's six steps and the method cards from `guide/method.md`, the papers
from `related/papers.md` by group, the drawings from b11's studio. What is typed, in red, is the proposal
under plan C (a Job = a Prototype release × a data version).


Files
-----

```text
s31-insight-guide/
├── s31-insight-guide.md            this notes file
├── build_s31_insight_guide.py      the builder (b16's, adapted); marks are kept on rebuild
├── insight_guide_live.py           what is read live, for the three level files
├── guide_block.py · guide_job.py · guide_task.py   each level's View items, on disk and open points
├── s31-insight-guide.excalidraw    the drawing: three frames, Block · Job · Task
└── s31-insight-guide.png           its preview
```

Rebuild: `python build_s31_insight_guide.py`, then render the png with haipipe-studio's `scripts/render_png.py`.


What each level says (proposed, red in the drawing)
---------------------------------------------------

1. Block: step 0 Make the Prototype (in its work Block: today's steps 1 and 2, a person signs the release),
   1 Add a data version, 2 Add a Job, 3 Read across Jobs (Coverage · Tracks · Consistency · Findings), then
   today's step 6 Hand off. Card: By protocol reuse. No card yet for reading across Jobs (replication, T8).
2. Job: 1 Launch, 2 Check the power, today's step 3 (run each partition), 4 Compare with the previous Job
   (the release's compare rule), 5 Close. Cards: By partition and power, By heterogeneity.
3. Task: today's steps 3 · 4 · 5 (run, check, write the page), then 6 Sign (Wisdom only). Cards: the five
   answering and three reading methods.


Open
----

1. The Prototype's steps live in its work Block: step 0 here, or a link to the work Guide?
2. `method.md` by level (Block · Job · Task tables) in place of today's one six-step table?
3. `papers.md` gets a level column, as the paper Guide's has?
4. `guide.yaml` `roadmap:` per level (today the Guide shows only s02)?
5. `insight_theme.py`: then the Space cards read the live frame, not s11–s13.

(write here, or mark the drawing in red)
