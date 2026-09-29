---
name: subjective-label-contract
description: >-
  The Data › Contract view skill of the subjective-label family: it
  sets up one labeling job: builds the fenced source, creates the P0 contract (corpus, fields, held-back test, G_00), and reads its status. Every Run in this view names this skill, and no other view uses it.
  Use for setting up a labeling job, fence_source, job.py create or status, the held-back test at setup, P0 integrity, or /subjective-label-contract.
metadata:
  version: "0.1.0"
  last_updated: "2026-09-29"
  # version history: ./CHANGELOG.md (skill-scoped, never loaded at invocation)
---

# /subjective-label-contract · Data Space › Contract

This skill owns the Runs of the labeling workbench's Data › Contract
view: every Run card there names it, and no other view uses it (JL 260929:
one skill per view). Load `subjective-label` (the family door),
`subjective-label-workflow` (the Run graph) and `label-building` (who decides what) first. Which Run
comes before and after these is in `label-building-workflow`.

## Runs in this view

```text
step  run                          state
 1    run-corpus-contract      built · engine/fence_source.py, then engine/job.py create
```

A Run is named `rlNN_<operation>_<target>` on disk and shown as
`run-<operation>-<target>` on the page. Its Ticket is `<Page>/runs/<run>.yaml`
and its Result `<Page>/results/<run>/`, beside `labeling/`.

The fenced source that `create` imports is built by `engine/fence_source.py`.
A fenced source is a corpus snapshot whose sealed test is reserved before any
development read. The tool does the test-reserve work before the job exists,
so it allocates no Run; the reservation reaches the job inside
`corpus-contract`. It draws the sealed ids with a declared seed, optionally
stratified evenly by one item-level field read from a side JSONL (a field with
two values for one item is refused). It requires a non-empty value in the
configured `corpus.text_field`, computes `text_hash` from that field, and
canonicalizes the configured source ID as `item_id`. Only eligible rows are
written to `corpus/items.jsonl`; sealed text is omitted from both the fenced
source and imported Page corpus. The public corpus manifest records counts,
while `test/sealed/manifest.protected.jsonl` contains sealed IDs and hashes
only. The custodian retains any raw source separately; the engine does not
provide a sealed-text release reader. `test/sealed/status.json` records the
custodian, frame rule, seed, strata, and access policy. The tool
renders G_00 `guideline.md` and `cheatsheet.md` from the config meanings (see
`../label-building/ref/ref-config.md` §3a). Like `create`, it is additive: an existing
different file is refused.

```bash
# Run from the repository root.
python3 plugins/subjective-label/engine/fence_source.py \
  --items <items.jsonl> --config <config.seed.yaml> --out <fenced-source> \
  --sealed-n <n> --seed <seed> --custodian <human> \
  [--stratify-jsonl <rows.jsonl> --stratify-field <field>]
```

Historical example: `S-Label-4-dices-unsafe-response` (DICES-350, target
`unsafe_response`) sealed 50 of 350 items, stratified by `safety_gold`, and
left 300 development items. That external example corpus is not bundled in
this repository; use the real local path supplied for the current project.

The canonical technical entry is `engine/job.py create`. It imports one
already-fenced corpus snapshot and its opaque sealed-test reservation into the
Page's direct `labeling/` lane, writes the five P0 artifacts through an
additive/idempotent writer, and leaves `authority.meaning_confirmed: false`.
It byte-copies the protected manifest as an opaque payload, but
never parses, prints, or renders it; it never copies a historical round, proxy
judgment, or model-derived gold. `engine/job.py status` checks, without writing, that the corpus,
opaque reservation, policy components, and P0 receipt are present and readable. It
never raises on a bad or unreadable file; it lists each defect in
`integrity_errors`. It reports `hold` and `hold_reason` from
`authority_hold(config)`, the one HOLD rule every host uses. It checks that the G0 receipt still matches the confirmed meanings, so
editing a meaning after G0 is caught. It refuses a
policy component name outside `POLICY_COMPONENTS` and any symlinked authority
file. A differing existing artifact is a hard refusal, not an overwrite. The
created `corpus-contract` Run is the first native Run. Its Result does not make
`round-prepare` eligible until G0 evidence from the identified human is valid
and bound to the current files; mere file presence or a bare boolean does not
satisfy that gate. A valid confirmation needs the human's receipt in
`config.yaml`.

`engine/job.py create` writes the P0 domain scaffold and allocates exactly one
completed `rlNN_corpus-contract_*` Ticket/runtime/Result envelope. It does not
speculatively allocate the optional or later operations above. Do not count
historical scaffold files as Runs; `engine/run_catalog.py plan` remains a
truthful planning tool for operations that have not been commissioned.

`create` is idempotent only while the P0 scaffold is unchanged. After the
human-confirmation action legitimately changes `config.yaml`, rerunning
`create` must refuse rather than roll the job backward; use `status` or resume
the phase API instead.

The create call must name the real Page source file; the API resolves it and
accepts only `<page-file.parent>/labeling` as `--job-root`. It refuses a
detached same-basename folder. The incoming sealed status must already carry a
valid custodian, frame, exclusion access policy, and invalidation state, with exactly one
opaque protected manifest beside it. `status` checks that all five authority
artifacts are present and readable.

```bash
# Run from the repository root.
python3 plugins/subjective-label/engine/job.py create \
  --source-job <fenced-source> \
  --page-file <page-home>/<page>.md \
  --job-root <page-home>/labeling \
  --job-id <id> --target <target> --human-id <human>
```

The read-only status invocation is exact and requires no Page-file argument:

```bash
python3 plugins/subjective-label/engine/job.py status \
  --job-root <page-home>/labeling
```

## Return

Return the Run address or `none`, the files written, and exactly one next
runnable Run or named human gate.
