# haipipe-design-method · version history

- 261007 · review fixes (version unchanged): ④ runs T0 and T1 always and T2 when the version lists it; T3 runs inside t99's rank; ② makes N + 5 ideas unless the version says otherwise (stated once in haipipe-design-unit reason.md); run-score is the reviewer agent's and keeps scores.csv in its own folder; the scorecard counts only scored rows.

0.4.0 current · 261007 · First version (JL 261007, b12 s00 · s11 · s12 · s21) (the Design family version is frozen)
- The method registry: `methods/MNN-<slug>/` with `method.md` (name · type · family · card · versions) and one
  frozen file per version `m<k>.md` (steps ① – ⑤ · sees · runs-it · loops). M01 – M05 registered, matching the design
  workbench's reader; each typed by one of the Guide's 13 cards, which stay in servers/workbench-design/guide/methods/.
- Runs: run-setup-method-j<NN> (`scripts/pin_method.py`: copy the version into the Job's inputs/method.md, record
  method-sha), run-propose-method-<slug>, run-add-observed-e<NN>, run-score-e<NN> (`scripts/score_exp.py`).
- `ref/scorecard.md`: observed/eNN, scores.csv, the sum per method version.
- `tests/test_method_registry.py`.

## 0.4.1 · 2026-10-09 · Theme folders are singular

- Docs name the singular Theme folders (s01-D29, JL 261007): `work/`, `discovery/`, `paper/`, `insight/`,
  `design/`, `labeling/`, `ideation/`; the older plural names still read.

