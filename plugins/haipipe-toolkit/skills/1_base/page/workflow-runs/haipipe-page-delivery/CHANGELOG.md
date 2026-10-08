## 0.3.0 · 2026-10-04 · Insight Pages export to LaTeX and Word (JL 261004)

- An Insight answering Page builds all three lanes: its receipt-bound VALUE and CITE items
  satisfy the evidence check (haipipe-page 0.122.0), and the shared reader
  (`servers/workbench-page/exporters/md2docx.py parse_page`) keeps its `#### 1.1 ·`
  subsections and its pipe tables (`folder-kind` data, information, knowledge or wisdom only;
  every other Page exports as before). LaTeX escapes a prose underscore outside math, code and
  a command's argument (`md2tex.escape_prose`); 36 of 38 paper Sections export byte-identical,
  the other two only gain `\_`. Tests: `exporters/test_md2docx.py`.
- The web lane is the reader the workbench shows, in reader mode.

## 0.2.1 · 2026-09-30 · The LaTeX lane keeps words it did not write

- md2tex refuses to overwrite a `<page>.tex` whose first line is not `% GENERATED from`
  (`servers/workbench-page/exporters/md2tex.py`, `GENERATED_MARK`). Found on 260930: a rebuild
  of Paper-TimeEventDM replaced six migrated Sections, 404 lines of prose, with the Pages'
  planning notes; the old guard only caught a lost citation key.

## 0.2.0 · 2026-09-28 · One fixed Run per lane, no hashes (JL 260928)

- 260929: the fixed names are spelled `run-delivery-webpage`, `run-delivery-latex`, `run-delivery-word` (the Page Run naming grammar, `src/run_names.py`); tickets sit in the flat `runs/`.
- One fixed Delivery Run per lane: `run_delivery_webpage`, `run_delivery_latex`, `run_delivery_word`
  (JL 260928: "we just need one run, it can be run_delivery_webpage, no need for rd01_web, rd02_web").
  A rebuild reruns the same Run through `page.py export`, which writes its ticket
  `runs/run_delivery_<lane>.sh`. No `runtime.yaml`, no attempt number, no RD allocation; the Runs panel
  shows `Done` while the lane is current and `Ready` when the Page changed. The "load
  haipipe-page-workflow first" step is gone: a rebuild needs only this file. Older `rdNN_<lane>` Runs
  stay as history.
- No lane manifest (JL 260928: "just delete them, it breaks the flow"). No code ever wrote
  `delivery/<lane>/build-manifest.json`, so agents typed it by hand (AGENTS.md rule 6), and the
  Delivery Space no longer reads it. The built files and their times are the record; `runtime.yaml`
  keeps status and exporter warnings. Same change in `haipipe-workbench-page/ref/delivery.md`,
  `ref/space-mapping.md`, `haipipe-page-revise` and `servers/workbench-page/runs.py`.
- An RD binds one source Page by path and version number. The build receipt names the source
  path and version, artifact paths and diagnostics, never a hash. The Delivery Workspace reports
  `pass`, `stale` or `not-built` per lane by file time.

## 0.1.1 · 2026-09-28

- ⛔ Hard rule under the title (JL 260928, AGENTS.md rule 6): never modify a generated file directly; change the code that writes it, then rerun.

## 0.1.0 · 2026-09-22

- New skill: the Delivery Run (`rdNN_<target>`) gets its own contract. Until
  now the `delivery` Run Spec row existed in the workflow table and the lanes
  had their tab contract, but no skill said when an RD is commissioned, what it
  binds, and what it may not touch.
