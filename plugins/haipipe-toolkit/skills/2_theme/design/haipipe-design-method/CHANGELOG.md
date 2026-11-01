# haipipe-design-method · version history

- 261022 · M05 m3 (version unchanged): `methods/M05-raw-data-agent/aggregate_query.py`, the raw-data agent's one door to a raw extract. The dictionary decides what may be asked (identity refused, free text only as its length, a time only as hour, weekday, date or month, a many-valued number only in fifths); an answer is grouped counts and rates, a group under 11 hidden, at most 60 groups; each answer is `q<NN>.yaml` with its receipt; a budget (30) caps the queries; an error never echoes a value. `m3.md` cites answers as `from: query q<NN>`. `tests/test_aggregate_query.py` (synthetic data). A column whose name holds a colon (`<col>:unique_join`) is asked as itself. The registry listings now name every version.
- 261012 · `ref/scorecard.md`: predicted and observed are both pp; a frozen prediction in another unit is never edited, the scorer states how it read it or scores it `?`.
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

