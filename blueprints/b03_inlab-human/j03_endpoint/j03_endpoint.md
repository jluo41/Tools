# j03 · The endpoint tool

job-of: b03_inlab-human (261009)
spine: `mcp-servers/endpoint-predict` (server.py, predict_cli.py): an endpoint URL as an MCP tool and a CLI; local Flask, Databricks or SageMaker, one wire contract.
close: Each recorded question has a report Page with an answer status, and every answered question names the change that settled it.

## Topic

It lists patients and models, prepares the payload (the required tables and the trigger record), POSTs it and
returns the score with a data-gaps report. Its payload code is its own (_rows_to_columnar, _build_cgm_payload,
_build_payload_for), not the toolkit's haipipe-individual-inference src (build_payload, _df_to_columnar,
slice_last_window); both changed on 2026-10-08.

## Questions

```yaml
questions:
- id: Q01
  title: One source for the payload contract?
  question: 'Two implementations of the same Endpoint_Set wire contract can drift: should endpoint-predict import
    the toolkit''s build_payload, the toolkit import this one, or a contract test pin them together?'
  hypothesis: A contract test first (the same patient gives the same payload both ways), then one implementation
    imported by the other.
  acceptance: Answered when one test proves both build the same payload, or one implementation is gone.
  work: []
  report: reports/q01_payload_contract/q01_payload_contract.md
```
