# QBt3-for-display

## Reader Takeaway
A display unit is produced in four lanes, and the two steps a machine may take
are both in BUILD. Every step in ACCEPT is a person's.

## Claim Supported
`QBt3-for-display.md` §Content, the acceptance ladder: rungs ① to ⑤ are not
symmetric, because ④ is the only rung whose actor cannot be a script. The figure
carries that asymmetry as colour rather than as a sentence, so a reader who
skips the prose still cannot miss it.

## Evidence Source
`source/source_data.csv`, 11 rows, columns `lane,order,label,artifact,actor`.
Every box, every label under it, and every actor mark is READ from that file at
draw time. `source/gen_display_pipeline.py` hardcodes exactly one thing, the
lane order, because that is the axis.

The rows are not measured data and do not claim to be. They are the pipeline
this unit itself came out of, and each row names a real path or a real rung that
a reader can check against the folder beside this page. That is the whole reason
the figure is a workflow and not a chart: a specimen group has no findings, so a
chart here would have to be invented, and a reader could not tell an invented
number from a real one.

## Placement
`_fixture/sections/01_page_types.tex`, which `\input`s this unit's shipped
`float.tex`. That `\input` line is the only place the SECTION shape and the UNIT
shape touch, which is why the specimen has both.

## Caption Job
Say what the four lanes are, say what white and grey mean, and name the one rule
the colours exist to show. The caption must NOT restate the eleven steps: they
are legible in the figure, and a caption that lists them is the third place the
same fact lives.

## Fragility
The figure is drawn at a fixed 9.6 by 4.2 inches and the box width is sized for
the longest artifact string in the CSV. Adding a row whose `artifact` is longer
than `source/gen_*.py + source_data.csv` will overflow its box. The first cut
did exactly that, at 7.4 inches, and also clipped the whole third column outside
the axis. There is no test for it: the check is to open `preview.png` and look.

## Status
③ RENDERED, 260807. `preview.pdf` compiled from the paper root and
`preview.png` written beside it. NOT accepted: rung ④ is a person's, and no
machine may set it, which is the rule this figure is about.
