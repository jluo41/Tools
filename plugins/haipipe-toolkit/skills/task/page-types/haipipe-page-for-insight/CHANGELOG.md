## 0.4.0 — 2026-08-20

- Moved the runtime home to `<DataSubject>-InsightBoard/1-I-insights/` under the
  two-board split, beneath the new `page-type: meta` head page.
- Added the Meta Page to the boundary block: Meta says what data exists, this Page
  makes claims from it.
- Dropped Artifact from the no-Probe list; the type was retired on 260820.

## 0.3.0 — 2026-08-20

- Moved the Page Type from the Task skill set into the Application skill set.
- Kept Task-backed source, run, staleness, human-reading, and Probe authority.
- Reframed the grain as one Application Insight question and added the fixed
  Application Need, Question, Source Map, DIKW, and Design Handoff divisions.
- D/I/K stay evidence-led; W is explicitly application-contextual.

## 0.2.0 — 2026-08-19

- **A SUBCLASS of `haipipe-page-for-task`.** New `parent:` key (JL 260819: "we
  will make it a special subclass of task folder, and we will also have the
  D, I, K, W for the insight page as well").
- It INHERITS one-page-per-folder, the run-bound verdict, the trace rule and the
  read-it closing rule. It REPLACES only the division grammar: task's
  `Why · Concept · Data · Method · Result · Meaning(last)` becomes the DIKW chain
  `Data → Information → Knowledge → Wisdom`, which this contract already carried.
- Wisdom is the one division that may be absent, and an empty one is a status.
