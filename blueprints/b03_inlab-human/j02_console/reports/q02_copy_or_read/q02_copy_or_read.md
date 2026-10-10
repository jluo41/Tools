# Copy each human to json, or read the record store in place?
state: 🟡 DRAFT · written by g02 2026-10-09 from the built reader and its check; CHECK pending
answers: Q02
answer-status: answered
results-read: 2026-10-09T10:35:00-04:00

## Opening

Read the record store in place. The console now assembles each human's json per request from the record set
(`INLAB_RECORD_STORE`), and the per-human json copy is only the fallback where no record store is mounted. One
source of truth and no second copy of patient data to secure outweigh a parquet filter per request, which is cached
per human.

**Where this Page sits:** [Q02 · The engine reads one json per human, so a build step copies each RecSet into InLabStore/<dataset>/patients/ (a second copy that can go stale, and one more copy of patient data to secure); an adapter would read 2-RecStore per request instead (one source of truth, a parquet filter per request). Which way? (JL's question in diagram/09-workspace-wiring.txt; drawn in studio s02.)](../../j02_console.md).

**Why it matters:** Every DATA view, the run bar and the agent read a human through this path; a stale or extra copy
of patient data is a risk the console should not carry.

## Content

### Answer

The reader is `record_store.py`, beside the engine's json reader: the engine has one loader (`_load_patient`) and one
lister (`_patient_ids`), and every read in the engine, the console's routes, the case feed and the message step goes
through them. A record set under `INLAB_RECORD_STORE` becomes a dataset of the same name and wins over a json copy of
that name. The reader follows the layout the haipipe Record stage writes (`manifest.json`, `Human-<H>/Human2RawNum.parquet`,
`Record-<H>.<R>/RecAttr.parquet`, partitions `@i<k>n<n>`), learned from the haipipe code, not from any store.

It names no table and no column (JL 261009: "we might have any dataset with any type of table"): the human id is the
column every Record shares, a Record's time columns are its timestamp and date columns by type, a source table is the
Record's name with its time grain cut off (renamable by `INLAB_RECORD_TABLE_NAMES`), and the endpoints that can score a
human are those whose required tables it carries, triggered at its latest record time.

### Evidence

- The drawing: [s02 · the data lineage](../../studio/s02-data-lineage/s02-data-lineage.excalidraw), the fork decided.
- The reader: [record_store.py](../../../../../plugins/inlab-human/mcp-servers/endpoint-predict/record_store.py);
  the loader seam in [server.py](../../../../../plugins/inlab-human/mcp-servers/endpoint-predict/server.py).
- The check, on the five synthetic glucose humans (`fixtures/run_fixture.sh` then `--record`): every Individual view's
  API answer (patients, chart, source, record rows, cases, ▶ Run trigger, gaps and response) from the record store
  equals the json copy's: 116 equal. The 5 differences are all one: the record store also carries the one-row `Ptt`
  record in the record layer, which the copy left out.
- The wiring, rewritten for the decision: [09-workspace-wiring.txt](../../../../../plugins/inlab-human/servers/haichat-inlab/diagram/09-workspace-wiring.txt).

### Limits

- A record store has no raw layer: the Raw view says so in record mode (the files as they arrived are in the raw store).
- Checked on synthetic fixtures only (D1); a real record set's size, partitions and id types are untested here.
- Provenance is derived ("who can score"), not recorded ("who scored"): the record store does not hold the latter.
- The agent's own engine process serves one record set (`INLAB_RECORD_SET`, else the first), as it served one store before.

### Next

Point a console at a real `2-RecStore` behind the data boundary (j05) and retire the copy step for that dataset.
