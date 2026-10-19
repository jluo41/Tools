
Report drawing · show the report's answer and evidence
=====================================================

The report mode of `excalidraw-report` (SKILL.md, "A report drawing"). Merged from upstream 0.4.0
on 2026-10-06; the plot kit, renderer and picture helper are beside this file.

A report drawing should let a reader understand what we learned, the evidence for it and
why it matters. Content comes first: use the report's actual values, comparisons, tables,
figures and examples. A clean layout helps the reader see that content; it does not justify
removing it. Three large boxes with model names do not summarize a report that contains
training results, evaluation metrics and figures.

Keep a clear entry point and enough detail to inspect. The first frame gives the answer and
its strongest evidence; further named frames hold the comparisons, examples or explanation
needed to understand it. At overview zoom the reader sees the conclusion; on zooming in the
reader finds the numbers, units, evidence and reasoning. The drawing lives under the report's
`studio/` and is linked from its Evidence.

```text
report + cited Results + figures
    -> answer and the evidence needed to support it
    -> first frame: answer + key result + what it means
    -> other frames: detailed comparisons, figures, examples, logic
    -> clickable sources + measured / calculated / unmeasured labels
```


Before drawing
--------------

Read the full report, including its Answer, Evidence, tables, figure references and Limits.
Open the cited Result files and relevant source figures. A drawing planned from titles or
one-line summaries will miss the findings the reader came to see.

Make a short content plan in the builder's source or the response, using the existing files:

| Content in the report | What the drawing must preserve |
|---|---|
| Main answer | The conclusion, the evidence for it and why the result matters |
| Material values | Exact values, units, denominator, conditions and meaningful differences |
| Result table | The rows and metrics needed to judge the conclusion; a table or matching plots |
| Figure or screenshot | The actual figure, readable labels, caption and what it demonstrates |
| Method or concept | The problem, inputs, mechanism, outputs and the reason to consider it |
| Concrete example | A real input/output or case that makes the method or task understandable |
| Limit or missing result | What was measured, calculated, reported elsewhere or remains unknown |

Map each main finding to a frame and its source. Use only content relevant to this Question;
there is no quota of plots or frames. When evidence is missing, label the gap instead of
inventing a value or starting a new experiment. A conclusion based on accuracy and
calibration needs both represented; drawing only accuracy would change the report's meaning.


Rules
-----

0. **Enough evidence, then a clear overview.** The first frame has an answer headline and
   the key result, comparison, figure or example that supports it. Do not make an empty title
   page. Later frames supply the detail. There is no required count of big blocks, plots or
   rows; use the space the evidence needs. Expand the canvas or add a named frame before
   deleting meaningful content or making its labels too small.
1. **Show why and how.** A method or concept report explains the problem that makes the
   method worth considering, how it works and which evidence addresses that problem. For
   example: task requires choosing under uncertainty -> model scores candidate options ->
   probabilities guide a choice -> accuracy and calibration check different parts of the
   result. Ground every factual step in the report; a proposed benefit is labelled as a
   hypothesis. A list of method names is not an explanation.
2. **Use the display the content needs.** Plots show patterns and comparisons; tables keep
   exact multi-metric results; diagrams explain dependencies and reasoning; source figures
   show the evidence itself. Combine them when needed. Exact values may appear as labels,
   table cells or result call-outs; do not force every scalar into a decorative bar. A chart
   does not replace a table when the reader needs the full comparison.
3. **Make relationships readable.** Ordered workflows usually run top to bottom on a
   numbered spine, without wrapping back to the left. Comparison tables use matching rows;
   explanations may branch where the reasoning branches. Label important arrows with what
   changes or why one step leads to another. Do not connect different model families as if
   they were stages of one pipeline. Read names from their sources; unresolved names or
   aliases stay labelled as unresolved.
4. **Keep useful detail.** Short labels aid scanning, but explanations, table cells and
   captions may use several lines. Do not apply a one-line limit to scientific content.
   Keep units, definitions and limits close to the evidence they qualify. Supporting content
   is readable at normal inspection zoom, not all tiny gray text below oversized headings.
5. **Colour and tags carry meaning.** Reuse series colours across related plots. State dots
   and actor tags help a status or workflow frame; they are not required decoration on a
   result figure. Include a key for the colours whose meaning the reader needs. Emphasize
   the important result or trade-off, not always an orange next-action box.
6. **One Question, one drawing; one frame per useful view.** A report has exactly one
   `.excalidraw`. Add named frames to that file for further results, figures, examples or
   explanations, placed beside the existing frames; do not add a second drawing link. The
   first frame is the report preview, so it includes meaningful evidence. The Block road
   map stays in the Block's `studio/`; copy only the views this Question needs into its own
   drawing.
7. **Real values, clear sources.** Read measurements from the cited CSV, YAML, JSON or
   other Result file. Values reported in a paper or supplied document are identified with
   their source and location, not presented as our measurements. Derived values come from
   those inputs in the builder, with the formula and assumptions shown when needed. Keep
   units, sample size, dataset/split, model/configuration and block/job/run identity with
   run results. Each plot, table or figure has a specific clickable source label; a general
   report link alone does not tell the reader which file supplied its values.
8. **Generated, never patched.** Reuse the existing source builder and build command,
   whether `studio/_build/` lives in the report or in its Block. A shared Block builder may
   write several reports; read its targets and use a report-specific target when available.
   Keep each output `.excalidraw` and `.png` in the owning report's `studio/`. Update the
   builder or its inputs and rebuild; do not create a second writer just to move the script.
   Never patch a generated scene or preview. If the source cannot reproduce the drawing,
   report that problem before replacing it.
9. **Linked from the report, once.** The report's Evidence lists its one `.excalidraw`; the
   workbench shows its `.png` and opens all frames in the viewer. A second drawing link or
   standalone picture link is a finding in Check, not a second thumbnail. The existing Task
   and CoWork readers use `servers/workbench-work/task_questions.py`.
10. **Read it as evidence.** On the render, check both coverage and legibility: are the
    report's main findings visible, are numbers and sources correct, do the plots use fair
    scales, can a reader read the embedded figures, and does the logic explain why the
    evidence supports the answer? Then fix overlaps, clipping and crossed labels. A neat
    render that leaves out the results is incomplete. When visual inspection is part of the
    requested drawing work, render and inspect each frame; blank module-download renders
    may be retried once.
11. **Show the actual figures.** Put relevant source plots, screenshots and printed examples
    inside the drawing as image elements, with a caption explaining their meaning and a
    source link. Place a figure with the claim it supports or in a clearly named evidence
    frame; do not append unreadable screenshots just to count them as included. Preserve
    axes, legends, units and context. The builder rereads the image on every build. The
    default helper downsizes the long side to 1600 px; if labels become unreadable, use a
    larger image in the builder or named detail crops while keeping an overview and source.
    `picture()` below embeds images; `ref/add_pictures.py` adds a Pictures frame for drawings
    made by another builder. Keep the report's picture path as text under Evidence, not a
    second picture link.
12. **Compare like with like.** State the dataset, scorer and conditions that make a
    comparison meaningful. Show relevant changes and trade-offs, not just one favourable
    metric. Label measured timings separately from projections and externally reported
    results. A cases-per-second figure requires its hardware, batch/concurrency and timing
    basis; a million-case projection shows its formula and is not called measured saturated
    throughput. Use 'not measured' for missing runs, never zero or an invented point. When
    official and local benchmarks differ, explain the difference instead of ranking them
    on one shared axis.


Choosing the frames
-------------------

Choose frames from the evidence, rather than filling a fixed template. These are examples,
not a required set for every report:

| Report question | Useful views |
|---|---|
| What is this method, and why consider it? | Problem and purpose; concrete input/output; mechanism; supported differences from alternatives |
| Did fine-tuning help? | Main result; exact accuracy and calibration comparisons; task breakdown; training/evaluation conditions |
| How long would a million cases take? | Recorded timing and its basis; formula and projection; measured batch/size comparisons; gaps in the sweep |
| What does the dataset contain? | Split sizes; a real case and answer; task categories; labels and evaluation unit |
| What does a visual-agent demonstration show? | Actual demonstration image; observe/score/act loop; reported success, latency and what was not independently checked |

For a decision-model report, explain why probabilities over candidate actions are useful,
what the input and output look like, and what distinguishes the implementations. When the
report has benchmark results, put them in the drawing too. Keep claims about decision quality,
calibration and serving speed separate so the reader can see what each measurement answers.


Draw
----

First find the script that writes the report's drawing and its build command. Reuse it,
including a shared Block builder that writes to several report folders; identify which
outputs its command rebuilds. The example below uses a Block-level `studio/_build/`; a
report-level builder works the same way. Reuse its helpers and add frame-aware pieces:

```python
els, n = [], [0]
FRAME = [None]                      # every element drawn after frame() belongs to it

def base(kind, x, y, w, h, **kw):   # ... "frameId": FRAME[0], ...
    ...

def frame(fid, name, x, y, w, h):
    els.append({"id": fid, "type": "frame", "name": name, "x": x, "y": y, "width": w,
                "height": h, "frameId": None, ...})
    FRAME[0] = fid

def line1(x, y, color, label, rest, size=18):      # one row: dot, label, gray detail
    dot(x, y + 3, color); text(x + 30, y, label, size, INK)
    text(x + 30 + (len(label) + 2) * size * EM, y, rest, size, GRAY)

STEPS = [("Invite", "coordinator adds the participant's email", "coordinator"), ...]
path(79, Y0 + 20, [[0, 0], [0, DY * (len(STEPS) - 1)]], GREEN, width=3)   # the spine
for i, (name, detail, who) in enumerate(STEPS):
    y = Y0 + i * DY
    circle(60, y, 40); text(80, y + 9, str(i + 1), 18, GREEN, align="center")
    text(120, y + 8, name, 21, INK); text(300, y + 10, detail, 18, GRAY)
    if who: pill(1690, y + 20, who, ORANGE)
```

Put a picture inside (rule 11): an `image` element plus a `files` entry holding the PNG as a
data URL; the renderer and the workbench's viewer both read `files`.

```python
import base64, hashlib, io
from PIL import Image

def picture(path, x, y, width, files):              # returns the drawn height
    im = Image.open(path).convert("RGB")
    k = min(1.0, 1600 / max(im.size))
    if k < 1: im = im.resize((round(im.width * k), round(im.height * k)))
    buf = io.BytesIO(); im.save(buf, "PNG", optimize=True); raw = buf.getvalue()
    fid = hashlib.sha1(raw).hexdigest()
    files[fid] = {"mimeType": "image/png", "id": fid, "created": 1790900000000,
                  "dataURL": "data:image/png;base64," + base64.b64encode(raw).decode()}
    h = width * im.height / im.width
    base("image", x, y, width, h, fileId=fid, status="saved", scale=[1, 1])
    return h
# ... and write {"elements": els, "files": files, ...} into the .excalidraw
```

Rebuild one drawing and look at it. The `.png` is the preview the workbench shows in the
Report column, so render only the first frame, the one whose headline is the answer: four
frames side by side shrink to an unreadable strip, and the click still opens every frame.

```bash
source .venv/bin/activate
H=<Block>/studio; T=$(mktemp -d)
python $H/_build/build_<name>.py $T/<name>.excalidraw
python $H/_build/render_excalidraw.py $T/<name>.excalidraw $T/<name>.html $T/<name>.png --frame first
cp $T/<name>.excalidraw $T/<name>.png $H/
```


Plots
-----

For plots made from local result values, copy `ref/plot_kit.py` and
`ref/render_excalidraw.py` into the report's `studio/_build/`; the kit provides a `Doc` class
(`frame`, `text`, `rect`,
`line`, `dot`, `pill`, `headline`, `key`, `source`, `save`) plus seven plots, each made of
native Excalidraw rectangles, lines and text, so a plot stays editable and renders anywhere.

| The report says | Plot | Kit call |
|---|---|---|
| how big several things are | bars, largest first | `hbar(x, y, [(label, value)], highlight=, total=)` |
| A against B (two to four things) | big side-by-side bars, ratio between | `compare(x, y, [(label, value, color)], note="12.7×")` |
| how a whole splits | one 100% bar, shares inside, key below | `share_bar(x, y, [(label, value, color)])` |
| a count over time | one column per period, peak labelled | `columns(x, y, [(period, value)])` |
| when each thing starts and ends | spans on one year axis, a dot for the peak | `spans(x, y, [(label, first, last, peak)], start, end)` |
| done out of total | one gauge bar, "N of M" | `gauge(x, y, done, total, label)` |
| a value across ordered points | a line, first and last values | `trend(x, y, [(point, value)])` |

1. **Values from sources.** Read local measurements from their Result files and calculate
   derived values in the builder. For a published table or supplied document, cite the exact
   source and location. Do not type an unsupported number or turn an illustrative value into
   a measurement.
2. **Every mark labelled.** Each bar, segment and gauge carries its value (and share when
   `total=` is given); a plot without its numbers is not read.
3. **One colour means one thing.** Reuse a colour for the same model or group across plots.
   Highlight the important comparison and use a legend where needed; orange is an option,
   not a requirement.
4. **Fair scales and useful order.** Bars start at zero. Use the same scale for comparable
   panels and label any log scale. Preserve model order, batch order or time order when it
   matters; sort magnitude comparisons when that helps. Show exact values and differences
   beside the plot when similar bars hide a meaningful change. Keep important categories
   visible rather than merging them into "other" to meet a row limit. The kit's `hbar` sorts
   by value; use a table, ordered `columns`/`trend`, an embedded plot or another builder
   helper when that sorting would erase the comparison.
5. **A plot names its result.** Its title says what is compared; units and whether higher or
   lower is better sit near the axis or values. The frame's headline states the supported
   conclusion. Use separate panels for metrics with different units, plus a table when
   exact multi-metric comparison matters.
6. **Enough room for the evidence.** Arrange plots in a clear reading order, keeping their
   values and sources readable. Add named frames when the current one becomes crowded;
   there is no three-plot cap. Use the native kit for plots it supports, and embed an
   existing or standard plotting-tool figure when the kit would lose needed information.

```python
from plot_kit import Doc, BLUE, GRAY, ORANGE, fmt_n
doc = Doc()
doc.frame("f-rows", "Where the rows are", 0, 0, 1800, 1120)
doc.headline(60, 50, "One table, flowsheet_data, holds 45% of deid.derived's rows", "67 tables · 22.7B rows")
doc.share_bar(60, 245, [("flowsheet_data", 10_245_975_634, ORANGE), ("the other 66", 12_421_494_786, GRAY)])
doc.hbar(60, 490, rows_from_csv, highlight={"flowsheet_data": ORANGE}, total=22_667_470_420)
doc.source(60, 1030, "j01_table_census/t01_table_catalog/results/r01_deid_derived/table_catalog.csv")
doc.save("q01_table_list.excalidraw")
```

Worked examples (Project-Samsung, b13_smartwatch_connector/studio/_build/):
`build_connector_path.py` frame "Patient phone setup" (zones in visit order, steps 1 to 8 on
one spine, coordinator tags) and `build_q03_status.py` (frame "Q03 status" with a one-row
progress track, frame "Health Connect vs Samsung Health SDK" as a two-column comparison with
a dot per cell).

Plots (REACH-SPACE, Project-0-EHR-Description `work/b01_reach_jhu/reports/q01_table_list/
studio/_build/build_q01_table_list.py`): four frames, every value read from the two table
catalogs and the report's Evidence Item Results. "Two schemas" (three `compare` pairs: rows,
tables, columns, with the ratio between), "Where the rows are" (`share_bar` of all rows, then
`hbar` of the ten largest tables with shares), "Inside deid.omop" (`share_bar`, a `gauge` of
tables that hold rows, `hbar` with the vocabulary tables purple), "Q01 status" (`gauge`s for
acceptance parts, described columns and JL's gates). Its `.png` is the first frame.
