s06 · Paper displays: what the reader sees, by the venue's rules
================================================================

**Tags:** `Plan`

**Stage:** shaping

**Venue:** venue

**Topic:** <n> displays carry the answers to <the questions>: <what the main ones show, in one sentence>. Each is
planned here once, made by a Run in `j01_evidence_display`, and checked against the venue's display rules
(`venues/venue/call.md`).

**Feeds:** `j01_evidence_display` (one pool Task per row, `display_plan.py seed`) and `s04-paper-workflow` (the
Sections that carry them).


### Displays

| Display | name | type | shows | answers | section | where | made by | state |
|---|---|---|---|---|---|---|---|---|
| Display A | <Outcome> by <group>, before and after | figure | <bars: one per group and period; colour = group> | RQ1 | Results | main | j01.t01.r01 | ✅ done |
| Display B | <Patients> at baseline | table | <one row per characteristic, one column per group> | RQ1 | Methods | main | <the Run that tables it> | ⬜ not started |
| Display C | <Placebo check> | figure | <the same model on a period with no policy> | RQ2 | Results | supplement | <a new figure Run after T5> | ⬜ not started |


### Sketches

#### Display A

```text
 <outcome>
   │  ▇▇      ▇▇
   │  ▇▇ ▇▇   ▇▇ ▇▇        before │ after
   └──────────────────     colour = group
```


Files
-----

```text
s06-paper-displays/
├── s06-paper-displays.md            this face: the plan, a sketch per display
├── s06-paper-displays.excalidraw    the plan drawn, with the venue check
├── s06-paper-displays.png           its preview
└── build_s06_paper_displays.py      forwards to excalidraw-workflow's displayplan_drawing.py
```


Decided
-------

(none yet: a decision is one line, s06-D01 · <what was decided> (<who> <date>))


Open
----

1. <the first open point>
