# Where `size.csv` was extracted from

🚫 FABRICATED. Both the run and its output are invented.

This file exists because the extract next to it is a COPY, and a copy with no
recorded origin is a number nobody can check. It is the second kind of file a
`.data/` folder holds: not the product, but the evidence that lets a person audit
the product.

```text
  run          runs/260806-0900-corpus-census/
  output read  results/per-board-counts.csv          462 rows, one per page
  extracted    grouped to one row per board, 9 rows
  dropped      the per-page rows, which no consumer needs and which would
               put 462 lines of fabricated detail into this repository
  by           source/extract.py in that run, not by hand
  on           2026-08-06
```

## What makes this extract stale

Re-executing `runs/260806-0900-corpus-census/` for any reason. The extract is not
regenerated automatically, on purpose: a silent refresh would move numbers under
a figure a person already accepted. The QA returns to `working` and someone
re-extracts deliberately.

## Why the extract is stored here rather than linked

The run's own output may live somewhere this repository cannot reach, may be
pruned, or may be restricted. The extract is small, aggregated, and safe to keep,
so it is copied ONCE at this boundary. Everything upstream of this file may be
large, remote, or restricted; everything downstream of it is small, in this
repository, and resolvable by `unit.py check`.
