---
name: haipipe-display-method
description: "Method displays: figures that show HOW a study works, not what it found, so a reader such as an advisor understands the design at a glance. Main kind 🕒 timeline: the study on one clock (each unit's timeline as bars with the event as one grey band, the periods and what each window is for, the comparison as boxes, treated minus control). Also 🗺 workflow (one row per step from raw data to the analysis file, with the file's real columns and made-up example rows) and 🧮 design (the difference in differences, the models as equations, what each piece removes). Drawn from a YAML spec by scripts/method_display.py; shown in a paper's Method group (group: method). Trigger: method figure, study design figure, how the dataset is built, workflow map, explain the methods, design of the regression, /haipipe-display-method."
metadata:
  version: "0.2.0"
  last_updated: "2026-11-06"
allowed-tools: Bash(*), Read, Write, Edit, Grep, Glob, Agent
---

# /haipipe-display-method · show how the study works

A method display answers "how was this done?", never "what was found?" (JL 261106: "add a skill like
/haipipe-display-method, to illustrate how these methods work"; "I want things like this, more like the real
workflow"). It is drawn the way the study runs: units on a clock, then the windows, then the comparison. A reader who
has not seen the code can say, from the picture alone, who is compared with whom, on which dates, and what the
estimate subtracts. It is one more renderer behind `/haipipe-display`, and every rule there still holds: the unit
folder, the one colour scheme, `preview.pdf`, and the blind-review loop.

```text
the ask                                   kind          looks like
how the study runs, who is compared       🕒 timeline   A units on one clock │ B periods │ C boxes: treated − control
how raw data becomes the analysis file    🗺 workflow   one row per step │ the file's columns, made-up rows │ file, Run
what the regression subtracts             🧮 design     A one unit's clock │ B 2x2 difference │ C equations │ D removes
```

Start with 🕒 timeline: it is the one a reader asks for first. Add 🗺 workflow when the reader must trust how the file
was built, and 🧮 design when the reader must see the model.

## One figure per large step, on simulated data

A reader understands a method fastest by watching the data move along time (JL 261106: "we just want the figures, and
plot, try to show the idea, you can also simulate how the data is manipulated along the time"; "for each large step
... describing the methods"). So beside the one-clock timeline, a study gets one figure per large step of its
pipeline, each a plot of SIMULATED data under the study's real rules:

```text
step                       what the plot shows (simulated, fixed seed)
find the event             one unit's daily activity, the gap, why the threshold is what it is
choose the controls        candidates' timelines and why each is kept or out; the nearest on the matching trait
attach the people          each person's events as ticks along time; who is kept by the selection rule
build the periods          one person's events cut into periods, scaled by time at risk
estimate                   each group's mean path, minus its baseline, then the difference with its CI
```

1. **Simulated, and said so**: every caption ends "Simulated data, to show the method; not study results." A seed
   is fixed, so the figure redraws the same; no value is read from the study's data.
2. **The real rules, drawn**: the thresholds, windows and selection rules are the study's own, so a reader can check
   the plot against the Methods; a number derived from a rule (a minimum gap from a volume floor) is computed, not typed.
3. **Plots, not tables or equations**: bars, ticks along time, lines and dots; words only as short labels.
4. **Where the code lives**: the study's own display Job (a `method_sim.py` with one function per step), since the
   simulation is study-specific; each step is a display Task with `group: method`, its Run drawing the figure and
   writing `float.tex` and `method.md`, then `build_preview.py`.

## The rules

1. **Real names, made-up values.** Step names, rules, file names, column names, Runs and counts are the study's own.
   Values in example rows are invented (`P1`, `K7`, `03 Feb 2020`); never a real ID, date of a real person, or a
   row copied from data. The script reads no data.
2. **Counts come from returned results.** A count on a figure is read from a Run's result or the Results text, and
   the spec says where in a comment. No count is better than a guessed one.
3. **One clock.** The event is one grey band through every panel that has time. Treated is the accent colour,
   controls the control colour, the run-up its own shade: the paper's `colour-scheme.yaml` (`--colours`).
4. **Rules go in words, not ticks.** "365 days, at least 52 billing days" sits on an arrow over the span it governs.
5. **The comparison is boxes.** Treated change − control change = the difference, with the sample counts in the boxes
   and where the difference is shown (which figure or table).
6. **Plain words for the reader named.** An advisor or editor, not the analyst: no variable names on the timeline,
   no Run ids in the boxes (they go in `method.md`).
7. **One comparison, one unit.** A study with two control groups (or two matching rules) gets one unit folder per
   comparison, the second a copy of the first spec with only that step's words changed; its message says so.
8. **Run ids stay off the figure.** `made_by` and `numbers` go to `method.md` only; with no Run yet, write what
   the counts were read from (a Results page, a returned table).

## Make one

```bash
S=~/.claude/skills/haipipe-display-method/scripts/method_display.py
P=~/.claude/skills/haipipe-display/scripts/build_preview.py
python $S <spec.yaml> <dir> --colours <paper>/j01_evidence_display/colour-scheme.yaml
python $P <dir>                      # the same <dir>: it holds float.tex, so preview.pdf is page 1 the display, page 2 method.md
```

`<dir>` is the display's unit folder: in a paper, the display Task's Run `result/`
(`j01_evidence_display/tNN_display-x-<slug>/runs/rNN_draw/result/`). The script writes `figure.pdf`, `figure.png`,
`float.tex` (title as caption, legend under it) and `method.md` there.

1. **Copy an example**: `examples/timeline-example.yaml` (main), `workflow-example.yaml`, `design-example.yaml`. Each
   is a made-up clinic-closure study; replace every line with the study's own.
2. **Fill it from the Methods text and the Run cards**, one fact per line, each count with a comment naming its source.
3. **Draw it** with the commands above; open `figure.png` and look before anything else.
4. **Place it**: in a paper, a display Task in `j01_evidence_display/` with `group: method` on its face, so the
   workbench lists it under Displays › Method (beside Main and Supplement); its Run's ticket calls the script.
5. **Review it**: the revise loop in `~/.claude/skills/haipipe-display/../ref/display-revise-loop.md`: a fresh
   general-purpose agent (never the maker) gets that file's reviewer brief and the figure only, and is told who the
   reader is ("an advisor who has not read the code") and the question it must answer ("who is compared with whom,
   on which dates?"); its text goes to `<unit>/review/rNN.md`. Pass: overall 8/10 or more. Not reviewed means not done.

## The spec

```text
every kind  title (the caption), legend (under it: what is drawn, not the finding), label (\label, default fig:method)
            message, data, sample, method, outcomes, made_by, numbers: method.md's parts, in build_preview.py's order
timeline    clock {start, end}: where the event begins and ends, 0-1 along the clock (not to scale: say so in legend)
            units {title, spans_above [from, to, label], event_label, rule: "what makes a control a control"
                   (printed under the bars: matching traits, the nearest-neighbour rule),
                   rows [label, treated: true, gap: true (no bar during the event),
                         later: "own absence 2-3 years later" (drawn past the clock's right end)]}
            periods {title, axis, segments [label, to, shade: run_up | event], spans_below [from, to, label]}
                   a segment runs from the previous one's end to its `to:` (an anchor or a 0-1 fraction of the clock)
            comparison {title, treated, control, result, note}: counts go in the treated and control text
                   ("211 absences; 1,519 pairs"); result names where the difference is shown ("Difference in Table 2")
            x anchors: left, start, end, right, or a number 0-1. spans_above only in units, spans_below only in periods
workflow    steps [name, rule, columns, rows (made up), file, made_by, count, highlight: true]
design      clock {title, axis, start_gap, segments [label, width, shade, start_after, treated_dashed], groups, note}
            did {treated, control, before, after, example} · models [eq (matplotlib math), what] · models_note
            removes [piece, removes, left_in: true]
```

## Files

```text
haipipe-display-method/
├── SKILL.md
├── CHANGELOG.md
├── scripts/method_display.py     spec → figure.pdf, figure.png, float.tex, method.md (matplotlib, PyYAML)
└── examples/                     timeline, workflow, design: one made-up study
```
