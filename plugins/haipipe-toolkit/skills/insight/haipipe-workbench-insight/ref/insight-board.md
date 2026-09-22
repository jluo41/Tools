# Insight Board · one cell, five Spaces, seven gates

**LOAD `../SKILL.md` (`haipipe-workbench-insight`) FIRST.** This reference is
the Board grain of the Insight workbench, served at `/_board/insight-board`
by `servers/workbench-insight/insightboard.py`.

## The unit · a cell

A cell is one register question on one partition, written `QW1 × F`. Every
Space below reads the same selected cell; selecting another cell re-reads the
board on disk. The board stays authoritative: this surface only reads the
register pages (their ASCII cell grids), the answering D/I/K/W pages, and the
`runtime.yaml` receipts a page names.

## The five Spaces

| Space | What it shows for the selected cell |
|---|---|
| Scope | the register the cell sits in: MT00 Meta (data cuts, extract, thresholds), MT01–MT04 Question rows, one cell per data cut |
| Run | the receipts behind the cell: frozen Run Specs (support · evidence · structure · write · deliver), their state, who is waited on; never an execute door |
| Insight | the page that answers the cell, by ladder level: D counts and rows · I results · K claims with strength · W DO and DO NOT rules |
| Evidence | the chain down to the extract: each hop bound to exact source evidence |
| Check | the seven gates of the cell, read from owner receipts; handoff eligibility is shown, never granted |

## The seven gates, read not judged

Check Space is where board grooming is presented (`haipipe-insight`: "an
audit, not a hidden writer"). It reports the current frontier, partial or open
register cells, dead or malformed references, and which Wisdom Handoffs are
actually bindable, each linked to the exact source path. It may show a next
Question Group or a safe repair as text; the Insight workflow performs them.

## Boundary

No allocation, no promotion, no rewrite, no `signed:` row, no handoff grant.
The Page-level Design workbench reads only a DesignBoard's declared `reads:`
InsightBoard and accepts only a currently eligible signed Wisdom Handoff with
exact owner receipts; it never binds directly to D, I, or K.
