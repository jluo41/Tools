# b03 · inlab-human

board-kind: task-block
spine: The blueprint of the `plugins/inlab-human` package: in-lab human evaluation of deployed prediction endpoints, in two modes (a reader study and a clinician console), over one endpoint tool.
close: Every Job's questions have a report Page with an answer status, and every answered question names the skill, server or tool change that settled it.

## Topic

One blueprint Block per package in `plugins/` (261009). inlab-human has a reader-study protocol (bundle, review,
report), a clinician console (haichat-inlab), the endpoint-predict tool both use, an agent drawer, and a
de-identification boundary it does not enforce itself. One Job per part.

## Jobs

```text
j01_study           the reader study: bundle, blind then assisted review, report
j02_console         the clinician console: haichat-inlab, patient first
j03_endpoint        endpoint-predict: the endpoint as an MCP tool, one wire contract
j04_haichat         the agent drawer: Agent SDK, Allow or Deny per tool
j05_data_boundary   de-identified only; outcomes scrubbed; study data stays with the study
```

## Questions

```yaml
questions:
- id: Q01
  title: What does inlab-human own, and what belongs to the toolkit?
  question: The payload contract, the inference personas, the labeling reader and
    an agent drawer each exist both here and in haipipe-toolkit. Which side owns each,
    and how does the other read it?
  hypothesis: The toolkit owns contracts and personas; inlab-human owns the protocol,
    the console's routing and display, and its tests.
  acceptance: Answered when each shared piece has one owner and the other side imports
    or reads it.
  work: []
  report: reports/q01_ownership/q01_ownership.md
- id: Q02
  title: How is the plugin tested?
  question: 'inlab-human has no tests: what should a suite cover across the study,
    the console and the endpoint tool, and what can run without a live endpoint or
    real cases?'
  hypothesis: A synthetic patient store and a stub endpoint let the bundle invariants,
    the blinding, the payload contract and the console routes run in CI with no PHI.
  acceptance: Answered when one command runs a suite over all three parts on synthetic
    data and it fails on a broken bundle, a premature reveal and a payload change.
  work: []
  report: reports/q02_plugin_tests/q02_plugin_tests.md
```
