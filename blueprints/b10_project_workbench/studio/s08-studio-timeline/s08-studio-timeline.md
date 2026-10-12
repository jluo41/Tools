s08 · Timeline: what moved when, down one axis
==============================================

**Stage:** agreed

**Tags:** `UI` · `Structure`

**Topic:** the Studio's third folding part, Timeline, under the topic cards and Related: what moved in this
Block's Studio and when, drawn as a real timeline, one axis down the page with a dot per day, at three
levels of detail. Started from JL 261011 ("for the layout of the studio, I think we can also add another
section of the Timeline"), then: "I want it to be a real timelne, and make it very concise ... Like the
timeline with a axis down", "it should also be up to done [down]", "we can show different level of
details", "We should create a new sNN for it, and show the UI".

**Feeds:** `reports/` q09_studio_report_on_screen


What it shows
-------------

```text
Days (a chart)   s01 s02 s03 s04 … s32      changes
Tue 06 Oct  ●    ●                          ▬ 14
Wed 07 Oct  ●    •   •           … • •      ▬▬ 36
Sat 10 Oct  ●    •   ⬤   •       … •        ▬▬▬▬▬ 88
            ▼
Topics           s02 studio-workbench-skill  ▬▬▬▬▬▬ 52   (decided · session · note)
Everything         decided  s04-D07 Related uses the Studio's group bar …
```

1. **One axis down**: the oldest day at the top, the newest at the bottom, a dot per day.
2. **Days, a chart**: a row per day, a column per topic group (by group, the default) or per topic (by
   topic), a bubble sized by how much moved that day, and the day's total as a bar. A group's column or
   bubble picks that group in the bar and shows its topics; clicking topics (a column's sNN or a bubble)
   picks them, and their decisions, sessions and notes show under the chart on the same axis.
3. **Topics**: under each day, a line per topic and a stacked bar of its kinds: decided, session, note.
4. **Everything**: under each topic, each decision, session and drawing note, one line each.
5. **Follows the group bar**: pick a group above the topics and only its columns and lines stay; a
   day left empty hides and the bars are recounted. The level picked is kept in this browser.

It writes nothing. It reads what a topic already keeps: each decision `sNN-DNN · … (JL 261011)` by the first
date in it, each session `runs/run-draw-<sNN>/passes/pNN-<MMDD>/` (the year from its notes), and the green
change notes `✎ <YYMMDD> …` in the topic's drawings. Decisions with no date are listed under the axis.
Code: `servers/workbench/frame.py` `timeline_events`, `studio_timeline` and the page script's `timeline()`.


Files
-----

```text
s08-studio-timeline/
├── s08-studio-timeline.md            this face
├── build_s08_studio_timeline.py      the builder; reads the events through frame.timeline_events
├── s08-studio-timeline.excalidraw    two frames in a row: where a line comes from --> the screen
├── s08-studio-timeline.png           its preview
└── .s08-studio-timeline.seed.json    generated snapshot for keeping marks
```

Rebuild: `python build_s08_studio_timeline.py`, then `render_png.py` for the preview.


Decided
-------

s08-D01 · A topic of its own for the Studio's Timeline, s08-studio-timeline, beside s02 Studio and s04
    Related (JL 261011: "We should create a new sNN for it, and show the UI").
s08-D02 · A real timeline: one axis down the page, the oldest day at the top and the newest at the bottom,
    one dot per day, an arrowhead at the end (JL 261011: "a real timelne ... with a axis down", "up to down").
s08-D03 · Three levels of detail, Days (the default) · Topics · Everything; the browser keeps the pick
    (JL 261011: "we can show different level of details").
s08-D04 · Read, never written: dated decisions, run-draw passes and green change notes, filtered by the
    Studio's group bar (built 261011; a drawing's sample of a note must not start with ✎, or it is read as one).
s08-D05 · Days is a chart, Topics a bar per topic: drawn in the page itself (HTML and CSS, no chart
    library, so it follows the light and dark colours and the group bar), JL 261011: "it is not that
    beautiful, how could we have better version? like using the versualiaation tools?".
s08-D06 · Stage → agreed: the Timeline is done and in use (JL 261011: "I think we can close the timeline
    now, I think it is very good to use"). The four open points wait under Later; none blocks it.
s08-D07 · The chart's columns are the topic groups by default, by topic one click away; a group's bubble adds
    up its topics, so a topic in two groups counts in both, while the day's bar counts each change once (JL
    261011: "I think here the columns can also be the topic groups"). Stage stays agreed.
s08-D08 · The header says only "Timeline", no counts (JL 261011, on "129 decided · 15 sessions · 105 drawing
    notes · since 2026-10-06 · 174 shown in Structure": "I don't need this, we can delete this part as well").
s08-D09 · Pick topics in the chart, read them under it: a click on a topic's column or bubble picks it, its
    items show below on the same axis, Clear drops the picks; the topic's name there opens its row (JL
    261011: "Or we can select the topics we are interest in we show there content").


Open
----

(none: agreed 261011, s08-D06)


Later
-----

Not needed now; each comes back as a new point if it is wanted.

1. The newest day is at the bottom: open the Timeline scrolled to it?
2. A Report answered, a Run closed: dots on this axis too?
3. 13 decisions carry no date (s01-D01 to D10 and D12, s04-D02, s21-D02): date them, or put them on the topic's
   first day?
4. A Block with many more topics: a chart library that zooms and pans, or a column per group?

(write here, or mark the drawing in red)
