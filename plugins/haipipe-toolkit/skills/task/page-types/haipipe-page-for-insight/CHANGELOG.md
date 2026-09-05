## 0.7.0 — 2026-09-04

- Reparent the Insight Page Type directly to `haipipe-page` after retirement
  of the standalone Task Page variant.
- Replace active Probe/PageX intake with the shared Supporting Run, frozen
  Local Input, and local Evidence Item Run graph.
- Align runtime storage and lifecycle language with the Outline-owned Context,
  Bullet, and Evidence workspaces and the five Page phases.

## 0.6.4 — 2026-08-31

- Make the consumption boundary explicit: RF is unsigned, consumer-neutral
  evidence. An Application may use it only through its own I1-registered,
  contextual, human-signed I5 bridge; it never binds RF directly to Design.

## 0.6.3 — 2026-08-31

- Align the agent discovery manifest with the task-only contract: Task Insight
  Page, consumer-neutral DIKW, and Reusable Findings rather than an
  Application-local Design Handoff.

## 0.6.2 — 2026-08-31

- Remove the retired Application scope completely. This Page Type is now one
  task-only, consumer-neutral D→I→K→W chain ending in Reusable Findings;
  downstream workflows borrow it through PageX and own their own handoffs.

## 0.6.1 — 2026-08-31

- Replace retired Application Page-Type references with the phase-owned
  I2-I5 Folder contracts under `haipipe-insight-workflow`.
- Show Probe, PageX, and Display under their canonical `evidence/` parent.

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
