# Workflow Design Principle · Labeling field test

This is a non-production design fixture. It exercises the new
`Workflow Definition → Workflow Runtime → Run Spec → Run` model against the
current `S-Label-1-labeling-lab` job without writing to that job.

The fixture intentionally stops at the first real frontier:

```text
existing Run: rl01_corpus-contract_job-v1 · complete
Runtime:      wfr01_job-v1                         · proposed
frontier:     building.round.prepare               · waiting
control:      G0 human meaning confirmation        · pending
current Run:  none
```

`P0` and `P1` are retained only as domain labels in `domain_view`. They do not
create Runtime or Run identities. `G0` is a Runtime control decision, not a
separate Gate Run.
