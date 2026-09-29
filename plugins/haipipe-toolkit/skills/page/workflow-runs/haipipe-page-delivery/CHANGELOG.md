## 0.2.0 · 2026-09-28 · No content hashes (JL 260928)

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
