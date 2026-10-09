# j02 · The console

job-of: b03_inlab-human (261009)
spine: CONSOLE mode: `/inlab-human-console` (0.1.0) and `servers/haichat-inlab` (FastAPI routers and a React SPA, built by HAIChat-SPACE as a per-thread iframe).
close: Each recorded question has a report Page with an answer status, and every answered question names the change that settled it.

## Topic

Patient first: pick a patient, read the chart as of the index date, pick a model, run it; the score comes from
the endpoint verbatim. Its routers: console_api (patients, models, predict), message_api (compose a patient
message, judge it, record the human's verdict), labeling_api (read a subjective-label project's artifacts),
tasks_api (a project's task folders), haichat_api (the agent drawer, j04).

## Questions

```yaml
questions:
- id: Q01
  title: What does the console own, and what is the toolkit's?
  question: message_api composes and judges with the toolkit's individual-inference report and judge personas, but
    the clinician-brief persona lives only in the console and patient-friendly only in the toolkit; labeling_api
    reads the toolkit's labeling artifacts. Where should each piece live?
  hypothesis: Personas live with their skill in the toolkit and the console reads them; the console keeps only routing
    and display.
  acceptance: Answered when every persona has one home and the console reads it, never copies it.
  work: []
  report: reports/q01_console_vs_toolkit/q01_console_vs_toolkit.md
```
