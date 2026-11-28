s32 · UI Plugin: Trace
======================
view: overview
emoji: 🧵

**Tags:** `All pages`

**Stage:** shaping

**For:** the 🧵 Trace item in every work page's section menu (Block, Job, Task), as screen previews in `delivery/ui/`, for JL to decide and for the workbench code (`servers/workbench/side_pane/files_tree/trace_section.py`, `page/job_task_views/work_frame.py`)

**Delivery type:** ui

**Covers:** the Trace section: which traces a page shows, how they group into topics, the left list and the right reading side; the `topic:` line every trace carries

**Excluded:** the traces on the Files tree and the metro map (s31-files-pane); what a trace file holds (hai-ui A07)

**Why:** with a hundred traces in one Block, can a reader find the work behind one piece of design, and read one trace from its aim to its summary?

**Topic:** a trace (`trace/<YYMMDD>/<HHMM>_<slug>.md`) is one piece of work; its `topic:` line names the Studio topic it serves (`topic: s31-files-pane`). Many traces serve one topic, so the Trace section groups them by topic: the topic's name on top, its traces under it newest first, a trace with no topic under "No topic". The Files pane (s31) shows traces on the tree; this section reads them one at a time.

**Feeds:** none


Files
-----

```text
s32-trace-section/
├── s32-trace-section.md          this face
├── s32-trace-section.html        the previews page
└── delivery/ui/
    ├── trace-metro.html          the metro map wide, three variants (?v=wide, topic, read)
    └── trace-topics.html         earlier: a list grouped by topic (not wanted)
```


Decided
-------

- s32-D01 · Traces are grouped into topics by their `topic:` line; a topic is a Studio topic (JL 261127: "I want to make the trace to be things like trace topics, some traces can be grouped into one topic, right?")
- s32-D03 · The Trace section is the metro map, wide and flexible to review (zoom, drag, pick a topic, read a trace), not a list (JL 261127: "I don;t like this timeline ... I just want to have [the metro map] things here, where we can review teh trace metromap more flexible")
- s32-D04 · A trace's group is its day by default, so every trace has one; the Studio topic stays a switch (JL 261127: "I think the topic can be genearetd per date")
- s32-D02 · The Trace section is an item of the page's section menu, beside Timeline (JL 261127: "for there, do you think we can add the a trace here?")


Open
----

1. (eased by s32-D04: a trace with no `topic:` line still has its day)
2. Should `hai-trace new` refuse a trace with no topic, and its check flag a topic with no folder?
3. A Job or Task page: only the traces with a file under its folder, or also its Block's topics?
