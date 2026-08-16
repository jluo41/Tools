# Q — Which directories named `1-probes` exist in this repository, who owns each one (paper or application folder), and how many PP-numbered entries does each hold?
- state:   answered
- started: 2026-08-16T10:33
- by:      haipipe-task-orchestrator-agent

## Answer

Three `1-probes` directories exist under the repository root, holding 3 PP-numbered entries in total [→ results/scan/probes_dirs.json].

1. `plugins/haipipe-toolkit/skills/diagrams/01-haipipe-paper-260725/_fixture/1-probes`
   - owner: `.../01-haipipe-paper-260725/_fixture` — a paper-shaped folder (contains `misq-slice.tex`, `misq-slice.bib`, `displays/`)
   - PP entries: 2 — `PP01_seed-feasibility`, `PP03_results-values`

2. `plugins/haipipe-toolkit/skills/diagrams/01-haipipe-application-260802/_fixture/1-probes`
   - owner: `.../01-haipipe-application-260802/_fixture` — an application-shaped folder (contains `0-artifacts/`, `0-lifecycle/`, `1-rounds/`, `STATUS.md`)
   - PP entries: 0 — the directory holds only a `.gitkeep`

3. `plugins/haipipe-toolkit/skills/probe/haipipe-probe/test/fixture/proj/papers/Paper-Fx/1-probes`
   - owner: `.../test/fixture/proj/papers/Paper-Fx` — a paper folder inside a test-fixture project
   - PP entries: 1 — `PP01_states`

All three owners are fixture/test folders inside skill packages; no live project-level paper or application folder in this repository carries a `1-probes` directory.

## Caveats

- PP entries were matched as child DIRECTORIES named `PP<digits>_<slug>`; a stray PP-named file would not be counted (none were observed).
- `.git`, `node_modules`, and `.venv` subtrees were excluded from the walk.
- The paper fixture numbers its entries PP01 and PP03 — the PP02 slot is absent, so counts reflect entries present, not the highest index.

## Not-done

- Did not open or summarize the contents of any PP entry; this is a location/count inventory only.
- Did not scan nested git submodules' ignored content beyond the normal directory walk (the walk does descend into checked-out submodule trees).
