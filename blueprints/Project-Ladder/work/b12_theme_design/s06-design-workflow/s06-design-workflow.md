s06 · The design workflow: from a signed goal to released designs, and back from the experiment
================================================================================================

**Tags:** `Workflow`

**Stage:** explore

**For:** a deck, and the design workflow as one map (who does each step, what it writes, the screen it lives on), for the people who write the design skills and build its workbench

**Delivery type:** skill

**Covers:** the whole design workflow in five areas, 18 steps: A set up the Block (1-4: write the goal and sign it, sign the shared rules, freeze an inputs version; a method version comes registered from the design skill) · B launch a Job (5-8: launch it on one goal × one method version × one inputs version, pin all three and build the fence, reason five more ideas than the goal asks for, the reviewer agent checks the fence and one Task opens per idea) · C write each design (9-11: write, check it for rules, sources and, when the method asks, a critique; redraft on a fail) · D rank and release (12-14: rank, keep as many as the goal asks, predict each in percentage points with a range, a pretest when the method asks; one Review and approve freezes the predictions and releases; the close) · E learn (15-18: the experiment's totals per arm, the scores and the method scorecard, the Block's questions, reports and one-page summary, a method change you sign); where the goal lives and travels; the loops back; a held Job; a design's state walk; the Map's compare; who makes, who checks, who signs.

**Excluded:** the screens themselves (j01's 3 × 3, s51 to s59); the ladder's folders (s01, s04); each Run's card and skill (s21; haipipe-design-workflow references/run-cards.md); the method cards (s03); where a method version is built (s05).

**Topic:** one map of how a design travels, as b11 s05 draws insight's workflow (JL 261102: "we have the workflow for the insight, could you make one for the design as well? try to make it to be vivid"). It starts from the goal (JL 261102: "Where is the Goal?"): written once in the Block's goal list (`board.md`, Goals) and signed by a person, pinned by every Job that works on it, copied into the Job's fence (`inputs/goal.md`) as all the design work may see, read by the rules check on every design and by the ranking. Each Job pins one signed goal, one registered method version and one frozen inputs version, so a changed answer has one cause. The designer agent makes, the reviewer agent checks (never what it made), and a person signs five things: the goal, the shared rules, a Job's Review and approve, its close, and a method change. What an experiment returns lands once at the Block and starts the next round. Every word is a full name, never a short id (excalidraw-studio, the look, rule 5; JL 261102). The steps are haipipe-design ref/design-ladder.md's rules and Runs and haipipe-design-workflow's routes and gates, checked against the workbench (servers/workbench-design); the words are written once in `s06-design-workflow-workflow.yaml`.

**Feeds:** `reports/` q01_design_ladder · q05_method_predictions · q06_design_method_ladder


Files
-----

```text
s06-design-workflow/
├── s06-design-workflow.md                  this face
├── build_s06_design_workflow.py            the five parts (Idea · Now · Design · Process · Delivery)
├── sketch_workflow.py                      its Design: the workflow as areas, one per act
├── s06-design-workflow-workflow.yaml       the sketch's words, written once: a short name a step
├── s06-design-workflow.excalidraw · .png   the drawing and its card
├── slides/idea-NN-<slug>.excalidraw        the deck: one editable Excalidraw drawing per slide, and its .png
├── slides/build_slides.py                  draws the slides, renders them, then topic_slides.py builds the deck
├── s06-design-workflow.slides.json         the deck's record (style excalidraw), one row per slide
├── s06-design-workflow.ideas.md            its ideas, one per slide
├── s06-design-workflow.mindmap.md          its mind map, from this face
└── delivery/                               deck/ and render.yaml (no piece yet)
```


Decided
-------

(none yet: a decision is one line, s06-D01 · <what was decided> (<who> <date>))


Open
----

1. ? Step 4: a method version is written in the Tools registry (`haipipe-design-method/methods/`), outside any Job or Run; only the proposal before it is a Block Run (`run-propose-method-<slug>`). s05 proposes a Task per version.
2. ? Between the proposal and the pin, the skill says the version is benched against the last version, reviewed by another agent and signed by a person; no Run type does the bench or that review yet.
3. ? The next Run is worked out only on the focus page (each Job's next move, `design_focus._job_next`); haipipe-design-workflow says no script prints it.

(write here, or mark the drawing in red)
