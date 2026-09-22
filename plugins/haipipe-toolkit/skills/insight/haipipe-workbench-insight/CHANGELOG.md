## 0.1.0 · 2026-09-22

- New skill: the served face of the Insight family, paired with
  `servers/workbench-insight`. Until now the two 🔎 routes were named only in
  the Board skill's route table; the page grain was described inside
  `haipipe-page-insight` and the board grain inside `haipipe-insight`. This
  skill states the read-only contract of both grains in one place and leaves
  the domain with its owners.
