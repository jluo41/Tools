# Task Block Workbench

One `tasks/bNN_<block>/` folder with `board-kind: task-block` opens one live
Workbench on the existing shared host. Task owns Questions and execution;
Page owns readable reports; the Workbench reads those records.

## Spaces and Views

The shared **Guide** Space explains the family through Skill set, Methods,
Workbench, Folder map and RoadMap Draw. The **Task** Space has four Views:

| View | Content and source |
|---|---|
| Task | Stacked, independently collapsible Questions. Each opens three side-by-side columns: **Logic / Work / Report**. Logic comes from `board.md`; Work uses Paper's shared folding rows over native Block → Job → Task → Run records; Report reads its ordinary Page. |
| Roadmap Studio | Independent folding rows for `studio/*.excalidraw`. Open several drawings, edit with the native Excalidraw pen lock, or add another drawing. Freeform ideation, workflows and folder sketches; no required diagram types or hierarchy. |
| Related Paper | Papers, repositories and other external resources, their contribution and related Questions. Add resource writes the existing register in `board.md`. |
| Progress | The same Question reports, answer states, work counts, evidence warnings and next actions. A Question link returns to its Task card. |

Questions are content inside the Task View. Jobs and Tasks without a Question
remain visible under **Not under a Question**. An existing Block needs no
migration; an empty Question register does not hide its execution records.
Search, folding state, View selection and optional 30-second refresh are browser
state. **Copy context to session** carries a Question's goal, work paths,
report path, answer, limits and next action into a conversation. Automatic and
manual refresh pause while an embedded drawing is being edited, a resource
form has unsaved changes, or a Run result is open.

Work rows share Paper's type pill, short name, explanation and count styling
through `workbench-shared/work_items.py`. Expanding a row reveals plain indented
folder levels; expanding its Task reveals Runs. A Run opens its exact native
Result in a pop-out with an own-tab link. Technical links and audit findings
are under **Task details**. Work order follows the Question register; optional
`stage` supplies a display label and `role` explains its contribution. These
fields change no execution state. Without them, the row reads the Task's
`task-type` (or Task) and Opening. Shared work names its other Questions.

## Sources and authoring

```text
tasks/bNN_<block>/
├── board.md                         scope, Questions and related resources
├── studio/*.excalidraw              native freeform drawings
├── reports/qNN_<topic>/
│   ├── qNN_<topic>.md               report Page: Opening → Content
│   ├── page.toml                   explicit native Page registration
│   └── draft/, runs/, results/      created only by the owning Page workflow
└── jNN_<job>/tNN_<task>/            executable work, Tickets and Results
```

See the authoritative [Block Questions and Report contract](../../skills/task/haipipe-task/ref/block-questions.md)
for the optional fenced YAML registers, report metadata and authoring helper.
The helper creates an empty report Page and registers it; it allocates no
execution and writes no answer or accepted Content. Continue writing through
`haipipe-page`. The full report uses the existing Page reader and offers a Page Workbench
link for Draft, evidence and writing. This also works before a Draft exists.

Report Opening supplies the answer summary. Content divisions **Answer**,
**Evidence**, **Limits** and **Next** follow the ordinary Page writing flow.
`answer-status: open | partial | answered` describes the answer, separately
from Page `state:`. Linked local evidence newer than the declared `results-read`
time produces a review warning without changing either state. External or
unlinked changes cannot be checked by this projection. Page CHECK and release
remain with Page; Task execution closure remains with Task.

`workflow/report.yaml` is the Task's P-B-E-R execution report and stays under
Work. It is distinct from a Block Question's readable report under `reports/`.
A Question can use several Tasks, and a Task can support several Questions.
A reasoning-only Question can have an answer with no Job, Task or Run.

## Execution semantics

Run Specs are planned definitions. Build counts describe files that exist,
not code-review acceptance. Execution counts use allocated Task Tickets,
excluding superseded records and orphan Results. Page Runs remain separately
identified within native Run detail; receipt attempts do not allocate extra Runs.

A complete Run does not answer a Question or close its Task. Signed reading
counts only show recorded signatures and whether a Verdict Run resolves in
the same Task. They do not certify Page CHECK, adoption or release. Running is
the last recorded receipt state, not process liveness.

The shared Run reader resolves Job `src/config-defaults.yaml` stores and local
or historical Result locations. Declared external stores can supply summary
data; files outside the server root receive no static download URL. Evidence
freshness warnings cover only linked files accessible within the served root.

## Open on the shared host

This module depends on `servers/_host` and the same plugin's Page, Run, Paper
result presentation, shared Work/Guide and Studio modules. It has no separate server entrypoint. Use Python 3.12 or
newer with the shared host dependencies, including PyYAML.

```sh
python plugins/haipipe-toolkit/servers/_host/serve.py --root <root>
```

The root may be a SPACE, Project, `tasks/`, or Block folder.

- SPACE Home opens Task Blocks directly before a static Board build.
- `/w/<block-folder>` redirects to this Workbench.
- `/_board/task-board?path=<root-relative-block>/board.md&view=task` is canonical.
- View keys: `task`, `studio`, `related-paper`, `progress`.
- `/_board/task-board` opens the only Task Block or lists available Blocks.
- Add `format=json` for the same source snapshot as JSON.
- A generated Task Board offers **Task Block** in its Workbench menu. Rebuild
  an older static Board to receive the menu asset and board-kind attribute.

Task GET and HEAD read sources. POST with `action: add-resource` appends a
resource through the bounded authoring helper; a POST without an action
returns the existing Workbench URL. The endpoint uses normal host authentication
and does not opt into anonymous `--public-read`. Drawing creation and saving
use the host's existing native Excalidraw routes.

Use the **full host** for embedded drawing and Add drawing support, with its
Excalidraw service available. `--only task` omits Page links;
`--only task,page` includes Page, Runs and Folder drill-downs but omits the
Excalidraw editor routes. The restricted interface disables drawing controls.
All links are origin-relative, including those reached through Tailscale.

## Runnable synthetic example

```sh
python plugins/haipipe-toolkit/servers/workbench-task/checks/demo.py /tmp/task-workbench-demo
python plugins/haipipe-toolkit/servers/_host/serve.py --root /tmp/task-workbench-demo --host 127.0.0.1 --port 5652 --no-terminal
```

The generator creates a new `TaskWorkbench-Demo` project and refuses to
replace one that already exists. It includes three Questions (answered,
partial and open), ordinary report Pages, six Tasks, synthetic Run receipts,
one placeholder resource and three blank native drawings. These are illustrative
records, not actual project execution, evidence approval or Page CHECK.

## Editable design

[task-workbench-design.excalidraw](studio/task-workbench-design.excalidraw)
is the native design source in the Paper / Page / Insight Studio style.
Frames: Structure, Task, Studio, RelatedPaper, Progress and Guide. It uses
illustrative content and documents the implemented source ownership.
Edit its generator and regenerate:

```sh
python plugins/haipipe-toolkit/servers/workbench-task/studio/task-workbench-design.py
```

On a Studio-enabled host, open
`/_excalidraw/?board=<root-relative-scene-path>&frame=Task`.
