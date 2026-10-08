s21 · insight Run and skill
===========================

**Topic:** every insight Run type and the skills behind them, and the plan to make the skills carry plan C
(JL 261007: "we should have a s21-skills to show all the skills related to this … s21 should be s21-run-skill,
it should include both runs and skills"; then "you should follow this one", b16's `s21-paper-run-skill`). Drawn
in that shape: lines-only tables in black, a decision in green and dated, red only for work another owner
must do. Named `s21-insight-run-skill`, as the paper's is `s21-paper-run-skill`.

**Source:** read from disk on every build:

- the run types each Space shows in s11 · s12 · s13 (their builders' `SCREENS`, imported, never run)
- today's run types with agent, skill and sign: `workbench-insight/ref/workbench-table.md`
- the live insight theme (`servers/workbench-insight/insight_*.py`) and the base frame (`servers/workbench/`)
- the skills in `skills/2_theme/insight/` (version, callers, how often each still writes a plan-C-retired name)
- the base skills insight borrows, found by name; the agents, checked on disk
- the Runs in the Project insight folders (`tasks/b5*_dikw`, `insights/*-InsightBoard`), counted by type and
  DIKW level; no Board, dataset or partition name is drawn

Typed, since they are the proposal: the Prototype Block's run types (no level drawing shows that Block yet), each
skill's job and its plan-C change, the owner and name of a run type with no table row, and the plan.

**Feeds:** `../../reports/q01_insight_ladder/` (run types per level) and the proposed Q06 (the Prototype and data
versions).


Files
-----

```text
s21-insight-run-skill/
├── s21-insight-run-skill.md            this notes file
├── build_s21_insight_run_skill.py      the builder
├── s21-insight-run-skill.excalidraw    the drawing; marks are kept on rebuild
└── s21-insight-run-skill.png           preview
```

Rebuild: `python build_s21_insight_run_skill.py`, then
`python ../../../../plugins/haipipe-toolkit/skills/1_base/project/haipipe-studio/scripts/render_png.py s21-insight-run-skill.excalidraw s21-insight-run-skill.png`.


What the drawing holds
----------------------

```text
Runs by level          Prototype (typed) · Block · Job · Task: Run · button · Space › view · today · who does it ·
                       who checks · skill; then today's table rows no level screen shows
one Job, in order      open a version → ask · plan · script → sign → add a data version → add a Job → run the
                       partitions → write · check pages → read across Jobs → counsel · handoff; proposals loop back
the skills             the 13 insight skills (owns · Runs that use it · old names · under plan C), the borrowed
                       base skills, the agents
skill folders          before → after: today's tree beside the proposed one, one row per changed file
skill x Run            which skill each run type loads; x ? = decided owner, no card yet
Runs on disk           the Runs in the Project insight folders by type and DIKW level (counts only)
skill update plan      six phases: each skill, what it learns, the run types it gains, done when
```

"today" says where a run type stands: **table** (a row of the workbench table names its skill, agent and sign),
**base** (the shared frame runs it), **live** (the insight theme shows the button, but no row says who runs it),
**drawn** (only in the drawing).


Decided (261007)
----------------

1. The Prototype Block's run types are typed here: Take the proposals, Open a version, Ask, Review the questions,
   Plan the evidence, Review the evidence plan, Set the cuts, Write the script, Review the script, Draw the question
   map, Sign a release, Carry a board over.
2. A cut is set in the release (Set the cuts, haipipe-insight); the Board only proposes one (Propose a cut), with
   the s11 session. No new `haipipe-insight-partition` skill.
3. `haipipe-insight-bind` has no ladder Run: it stays for register boards and retires with the last one.
4. A run type with no table row gets its owner (the skill whose folder it writes) and its `run-<type>-<target>`
   name here; phase 2 gives each its card.
5. The Guide's Add a method and Add a paper stay the Guide's own Runs.
6. A button the shared frame also has keeps the frame's Run name (haipipe-run `ref/run-types-by-space.md`,
   b03 261007): `run-add-<jNN>`, `run-ask-<qNN>`, `run-report-<qNN>`, `run-check-<qNN>`, and Idea Studio's one
   button `run-draw-<sNN>`. Insight-only buttons keep theirs. Owners match the live theme's `SKILLS` map.
7. Drawn in haipipe-studio 0.2.0's palette: black, red for open `?`, green for changes. The gray is now black
   (canvas.write applies the palette); a tree file with no change word beside it is kept. The builder prints anything off the palette.


Open (another owner)
--------------------

- The Prototype Block has no level drawing: a session drawing it (as s11 · s12 · s13 do) should show these buttons.

(write here, or mark the drawing in red)
