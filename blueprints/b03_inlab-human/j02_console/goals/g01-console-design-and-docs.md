g01 · Document and design the In-Lab Console the way the toolkit's workbench is
================================================================================

One goal prompt for one session (written 261009 from the plan in the b03 session, JL: "make the UI to be well
documented ... have the UI element as well"). Every decision is made below; run it without asking unless a Stop
rule fires. Run it as:

```text
Run Tools/blueprints/b03_inlab-human/j02_console/goals/g01-console-design-and-docs.md
```


What this is
------------

The In-Lab Console (`Tools/plugins/inlab-human/servers/haichat-inlab/`: a React + Vite app over five FastAPI
routers) is inlab-human's own workbench. Give it the design treatment the toolkit's theme Jobs got (for example
`Tools/blueprints/b01_haipipe-toolkit/j11_theme_insight/studio/`): screens per level with what each reads on disk,
an element-UI gallery shot from the live console, a map from each run-bar step to its owner, a UI review, a runtime
page, and the Questions they raise. Fix the docs that have drifted from the code. Build nothing new in the console.


Read first
----------

- The console: `README.md`, `diagram/00-index.txt` … `09-workspace-wiring.txt`, `main.py`, the five `*_api.py`,
  `web/src/views.ts`, `actions.ts`, `Console.tsx`, `useConsole.ts`, and the opening comment of every component in
  `web/src/components/` (each says what the element is).
- The engine: `Tools/plugins/inlab-human/mcp-servers/endpoint-predict/server.py`.
- The blueprint: `Tools/blueprints/b03_inlab-human/board.md`, `studio/s01-two-modes-map/`, and the Job faces
  `j02_console/j02_console.md`, `j04_haichat/j04_haichat.md`.
- The pattern to mirror: `Tools/blueprints/b01_haipipe-toolkit/j11_theme_insight/studio/` (s01 ladder, s11 · s12 ·
  s13 levels, s21 runs and skills, s32 element UI, s33 UI issues) and
  `j03_project_workbench/studio/s32-element-ui/build_s32_element_ui.py` (its `PICK_JS` and `shoot()`: Playwright
  screenshots of one element per CSS selector, plus each element's computed style in `facts.json`).
- How studio topics work: the `haipipe-studio` skill (`new_topic.py`, `canvas.write`, `render_png.py`); the shared
  lines-only helper `Tools/blueprints/_build/mapdraw.py`.


Decisions (made; follow them)
-----------------------------

D1. Synthetic data only. No real patient, case, label or study file is read, rendered or shot. Every screenshot
    comes from the synthetic store of Part A. If a real store turns up on a path the console would mount, do not
    open it; use the fixtures.
D2. The fixtures live with the console: `servers/haichat-inlab/fixtures/` holds a synthetic store (three data
    types, five humans each: a 5-minute glucose timeline with meals and insulin, a doctor–patient dialogue, a
    physician review), a stub endpoint (`stub_endpoint.py`: a fixed score, and a fixed forecast for the glucose
    type, from the engine's own wire contract), its registry json, and `run_fixture.sh`, which builds the front end
    if needed and starts the stub and the console on loopback ports. Every fixture file says "synthetic" in its
    first line. These fixtures are also inlab-human's first test fixture (b03 Q02).
D3. Docs about the code stay beside the code (`README.md`, `diagram/`). Design drawings go to
    `Tools/blueprints/b03_inlab-human/j02_console/studio/`. `diagram/canvas-inlab-design.excalidraw` stays where it
    is.
D4. Code docs that list code are generated, never hand-kept: `diagram/build_ui_docs.py` writes
    `diagram/10-ui-elements.txt` (every view in `views.ts` with its group and banner, then every component with the
    first paragraph of its opening comment) and `diagram/11-routes.txt` (every route the FastAPI app mounts, read from
    `main.app.routes`, with its router). The README's API table is replaced by one line pointing to `11-routes.txt`;
    `04-backend-api.txt` says five routers and names `message_api` (compose · judge · feedback). These two are hand
    edits of sources, which is allowed; the two generated files are rewritten only by their script.
D5. The shooting code is shared, not copied: lift `PICK_JS` and `shoot()` from j03's s32 builder into
    `Tools/blueprints/_build/shoot.py` (a page list and a selector list in, screenshots and `facts.json` out). The
    console's s32 builder imports it. Do not edit j03's builder; leave a one-line note in this Job's report that it
    can switch to the shared helper.
D6. The design topics, in `j02_console/studio/`, each with a builder that redraws from disk and keeps a person's
    marks (black lines and boxes; red for open points; a green `✎ <date>` note for each change):
    - s01-console-ladder: Dataset → Human → Case → Score or Label; the rail groups as the console's Spaces.
    - s02-data-lineage: Raw · Source · Record · Case, each view to its store, and the copy-or-read-in-place fork in
      red (JL's open question in `diagram/09-workspace-wiring.txt`).
    - s11-group-scope · s12-individual-scope · s13-case-builder: one frame per view at that scope, a screenshot of the
      view on the fixtures, and under it the "on disk" tree it reads (the env var, the folder, the file).
    - s21-run-bar: each step of `PipelineBar` (▶ Run · Interpret · Message · Judge · Feedback) to who does it (the
      endpoint, which toolkit skill or persona, the human), and every HaiChat tool to the `ConsoleAction` it
      dispatches.
    - s32-console-element-ui: one frame per element (top bar and its pickers, nav rail, tab strip and dock, patient
      card, data panels, record chart, model card, run bar, forecast chart, Annotate, Checklist, HaiChat drawer with
      an approval card, Health), each a screenshot and its computed style; beside it the toolkit frame's matching
      element where one exists (top tabs, view row, tables), so a common look can be judged.
    - s33-console-ui-issue: the review, the same way as `j11_theme_insight/studio/s33-ui-issue/`: every view at both
      scopes, every link, ranked worst first (where · what is wrong · what it should be · evidence · owner).
    - s51-console-runtime: standalone (:8091, the drawer shown) and embedded (an iframe in a HAI-Chat thread, the
      drawer hidden): processes, ports, env mounts, and what HAIChat-SPACE builds from this folder.
D7. Questions are recorded, not answered (each a register entry in the Job face's `## Questions` and an open report
    frame `reports/qNN_<topic>/qNN_<topic>.md` + `page.toml`, in the same shape as the existing frames):
    - j02 Q02 "Copy each human to json, or read the record store in place?" (the diagram 09 fork; both options and
      their costs, no choice made).
    - j02 Q03 "How does the tasks feed read the project ladder?" (`tasks_api.py` reads `examples/Project-*/tasks/`
      and the letter series `A01_*`; today's projects are `examples-N-*/Project-*/tasks/bNN_*/jNN_*/tNN_*`).
    - j02 Q04 "One look for the console and the workbench?" (evidence: s32's side-by-side).
    - j02 Q05 "Build or drop the placeholder views?" (Internal, External, Checklist, and the group-scope stubs).
    - j04 Q02 "Can the console's action list become an MCP that drives a workbench?" (the two-drivers, one-reducer
      design of `actions.ts`; link `Tools/blueprints/b01_haipipe-toolkit/j05_chat` Q02 both ways).
D8. Processes: the stub and the console run on free loopback ports (try 8191 and 8192), started by
    `run_fixture.sh`, which prints their PIDs. Stop them at the end by those PIDs only. Never stop a process by a
    name pattern (`pkill -f`, `killall`): on 261009 that stopped six workbench hosts and open apps.
D9. `npm install` may run in `web/` (network). `web/node_modules/` and `web/dist/` are already git-ignored; never
    commit them.
D10. At the end, commit to Tools `main` (only the paths this goal touched, named one by one with `git add`) and push.
    Never commit or push DrFirst-SPACE; leave its Tools pin for JL.


Steps
-----

A. Fixtures (D1, D2, D8, D9). Write the synthetic store from the shapes the engine reads (`tool_list_patients`,
   `tool_get_patient`, the registry, the trigger record) and the stub endpoint. Run `run_fixture.sh`; check
   `/api/health`, `/api/datasets`, `/api/patients?dataset=<each>`, one chart, `/api/models`, and one `POST
   /api/predict` per data type. Each must answer from the fixtures.
B. Code docs (D4). Write `diagram/build_ui_docs.py`, run it, edit `README.md` and `04-backend-api.txt`. Check: every
   route the app mounts is in `11-routes.txt`, and every view in `views.ts` and every file in
   `web/src/components/` is in `10-ui-elements.txt`.
C. Shoot (D5). Write `_build/shoot.py`; shoot every view at both scopes and every element of s32 against the
   fixture console; keep the shots in each topic's `shots/`.
D. Draw (D6). Make the topics with `new_topic.py` (band level for s11–s13, run for s21, guide for s32–s33, server
   for s51, concept for s01–s02), write each builder, build, render each preview, and read each preview yourself.
E. Questions (D7). Add the register entries and frames; add the cross links to j05_chat.
F. Review (s33). Walk every view and link on the fixture console and write the ranked list into s33's face and
   builder.
G. Stop the processes by PID (D8). Commit and push (D10).


Stop rules (the only ones)
--------------------------

- A real patient, case or label file would have to be opened to continue (D1): stop and report what asked for it.
- A live session is editing `servers/haichat-inlab/` right now: check ListAgents, message any whose work names it,
  and wait for its answer.
- `npm install` or the build fails (no network, a toolchain error): skip C and the screenshots, draw every topic from
  the code alone with "not shot" in red where a screenshot belongs, and report it.


Never
-----

- Change the console's behaviour, its routes or its components (fixes come later, one Question at a time).
- Hand-edit a generated file (`10-ui-elements.txt`, `11-routes.txt`, drawings, previews, `facts.json`).
- Write an absolute `/Users/…` path, a real person's name, or a project or study name into a Tools file.
- Stop a process by a name pattern; commit `node_modules/` or `dist/`; commit or push DrFirst-SPACE.


Done when
---------

- The fixture console answers every API check of step A, on synthetic data only.
- `10-ui-elements.txt` and `11-routes.txt` are generated and complete; the README and diagram 04 match the code.
- j02's studio holds s01, s02, s11, s12, s13, s21, s32, s33 and s51, each with its builder, drawing and preview,
  and every screenshot comes from the fixtures.
- Five Questions are recorded with frames, and j05_chat and j04 link each other.
- Every process this goal started is stopped by PID; Tools `main` is pushed.
- A short report: files changed (one line each), check counts, the s33 top five, and what is left (the Questions).
