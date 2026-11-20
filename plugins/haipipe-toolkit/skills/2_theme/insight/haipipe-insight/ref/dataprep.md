DataPrep: the code that turns a raw export into a folder ready for insight
==========================================================================

(261116, redesigned 261120; workbench-insight topics T10-T26.) The ladder has three Blocks. The **Question Book**
holds the questions' code, one signed question version at a time. The **DataPrep** Block holds the data's code: the
chain of steps that turns a raw export into a folder ready for insight, one signed prep version at a time (JL 261120:
"they are code only … the real data processing and real question processing are in the insight block"). The
**insight Board** runs both. A data Job runs a prep version on the Board's raw export and makes the Board's next data
version; a question Job runs a question version on a data version. Each Job moves one clock.

Read this before making, growing or running a DataPrep Block. The Question Book and the Board's question Jobs stay as
[insight-ladder.md](insight-ladder.md) draws them.

The trees
---------

```text
<Project>/insight/InsightDataPrep-<Set>/         the code for a Set: a family of datasets made the same way
├── board.md                                     board-kind: insight-dataprep · workbench: insight · set: <Set> ·
│                                                store: <SPACE-relative folder the ready folders go to> ·
│                                                serves: [insight/Insight-<D>, <a Board in another Project>] ·
│                                                references: [{name, path, version, why}] · ## Background
├── background/                                  the source's documents and the data owner's answers; never a row
├── runs/                                        soft: run-open-version-prep-v<K>
└── jNN_prep-vK_<slug>/                          one prep version: the chain, frozen once a person signs it
    ├── jNN_prep-vK_<slug>.md                    prep · state: open | closed · signed: ✅ <YYMMDD> · hash · from
    ├── src/                                     code two or more steps share
    ├── runs/                                    soft: run-review-steps-prep-v<K> · run-sign-prep-v<K>
    └── tNN_<step>/                              one step (experiment · source · prepare …), code only
        ├── tNN_<step>.md                        its page's goal line
        ├── step.md                              the spec: step · script · reads · writes · checks · agreed
        └── scripts/<script>.py                  run(ctx), and nothing else that runs

<Project>/insight/Insight-<D>/                   the Board: one dataset
├── board.md                                     … · raw: <SPACE-relative raw export> · cut: {…} ·
│                                                dataprep: <the DataPrep Block> · versions: [{version, folder,
│                                                frozen, prep, made-by}]
└── jNN_prep-vK-<slug>_data-vM/                  a data Job: prep-vK on this Board's raw export, making data-vM
    ├── jNN_prep-vK-<slug>_data-vM.md            prep · dataprep · prep-hash · data · raw · state · made
    └── tNN_<step>/runs/r01_<dataset>/           the same steps, one hard Run each: run.sh (calls ref/run_prep.py),
                                                 run.yaml, result/ (runtime.yaml, provenance/, the card or heavy.yaml)
```

The rules
---------

1. **A Set, not a dataset.** `<Set>` names a family of datasets made by the same code; it carries no version. A
   dataset belongs to its Board: `datasource <Board> --raw … --dataprep …` names its raw export and the DataPrep Block
   it runs, which must name the Board in `serves:`.
2. **A prep version is code, signed, then frozen.** `prep` opens the next one from the newest; `--steps a,b,c` names
   its steps in order (a kept step moves to its new number, a new one is made empty, one left out is not carried). A
   step is `step.md` and `scripts/<script>.py` exposing `run(ctx)`; it holds no Run, no config and no output. `sign`
   needs every step agreed by an agent that did not write it (run-review-steps) and every script exposing `run(ctx)`;
   it pins `hash:` over `src/` and every step's face, spec and scripts.
3. **A step reads only what `ctx` gives it.** `ctx.raw` is the Board's raw export, `ctx.prev` the earlier step's
   output, `ctx.refs` the Block's `references:` (each read at the version named there), `ctx.cut` the Board's cut. No
   cache, no other pipeline's store, no shared source stage is an input; a library a step imports is code, recorded in
   the receipt (T25: pinned by the signature).
4. **A step writes only `ctx.out`, and no page shows a record value.** The first step writes its Run's `result/`; the
   last step writes the ready folder `<store>/<dataset>@prep-vK`; one between them writes the Run's heavy folder under
   `_WorkSpace/ProjectResult/…` (the Result keeps `heavy.yaml`). A Result, a dictionary, a manifest or a summary
   carries shapes, counts and names: no sample column, no first value, no `head()` of a table. The runner fails a
   ready folder whose dictionary has a sample column; `audit <Block>` names each script line that takes a record's
   value (`records`).
5. **A Board runs a prep version in a data Job.** `datajob <Board> --prep prep-vK` refuses an unsigned version, or one
   whose code changed since its signature, and opens `jNN_prep-vK-<slug>_data-vM/`: one Task per step, the same names,
   one hard Run each. Question Jobs and data Jobs share one count. `ref/run_prep.py <Job>` runs the steps in order and
   stops at the first that refuses or fails; a step's own `run.sh` runs that step alone, refused until the step before
   it is done. Each Run copies the exact scripts and their sha256 into `result/provenance/`.
6. **The last step makes the data version.** When it finishes, the ready folder becomes the Board's next data version
   `{version, folder, frozen, prep, made-by}` and the Job closes. A folder a data version names is frozen: no data Job
   writes it again. A data version made before this (b01's, by hand) names its prep with `data … --prep prep-vK`.
7. **The experiment card comes first.** Each prep version's first step reads only `ctx.raw`: the export's rows and the
   documents that describe the experiment. It writes `experiment_card.json` and `.md` in its Result, aggregates only:
   - **settings:** experiment ids and names, arms and their counts, batches, message content;
   - **time:** the invitation range in UTC and in local time, active and calendar days, gaps, daily volume, send hours.
   Its checks compare what is stated with what is observed, and a mismatch stops the Run. A dataset with no documents
   gets a card marked "nothing stated", never a guess. A document stamped with a pull's time (`YYYY-MM-DD-HH-MM`) is
   compared only with the export carrying the same stamp; one from another pull is listed, shown and not checked. A
   setting the rows cannot test is "not checkable", never passed. The runner fails a first step that wrote no card,
   refuses every later step until it is done, and copies the card into the ready folder.

What prep does, and what a question does
----------------------------------------

```text
prep (a step's check)                              a Data question (D)
is the data fit to use? stops if not               what does the data say? a finding on the page
row counts, date range, keys unique, arms          the shape a reader quotes: who is in it, how the
balanced as assigned, no column read from          arms compare at baseline, which fields are thin
the future of a row
```

A derivation moves from a question version's `src/` to a prep step only when it makes one column per row, reads no
outcome, and is the same for every question. Rates, tests, privacy blanking and the groupings that define segments
stay with the questions. A signed question version is never edited: the next prep version adds the column (a data Job,
then a question Job with `moved: data`), and the next question version drops its own copy (`moved: code`).

`ctx`
-----

```text
ctx.raw      Path   the Board's raw export (board.md raw:)
ctx.out      Path   where this step writes (rule 4)
ctx.prev     Path   the earlier step's ctx.out; None for the first step
ctx.cut      dict   the Board's cut: (dates, a sub-cohort), applied by the step that cuts
ctx.refs     dict   {name: Path}, the DataPrep Block's references:
ctx.dataset  str    the Board's dataset;  ctx.prep  the prep version;  ctx.result  the Run's result/
ctx.refuse(reason)  stops the step: the Run is refused, with its reason, and the chain stops
```

Scripts
-------

```text
insight_ladder.py dataprep   <Project>/insight/InsightDataPrep-<Set> --set <Set> --serves <Board>[,…] [--store …] [--title …]
insight_ladder.py reference  <dataprep> <name> --path <SPACE-relative> --version <v> [--why …]
insight_ladder.py prep       <dataprep> --slug <what-it-is> [--steps a,b,c]
insight_ladder.py step       <prep version> <slug> [--ask "what it does"]
insight_ladder.py sign       <prep version> --date YYMMDD
insight_ladder.py audit      <dataprep>      serves · references · scripts · records · agreed · hash
insight_ladder.py datasource <Board> --raw <SPACE-relative raw export> --dataprep <DataPrep Block> [--cut key=value,…]
insight_ladder.py datajob    <Board> --prep prep-v<K>
python ref/run_prep.py       <data Job>            (or <data Task> r01_<dataset>, which its run.sh does)
insight_ladder.py data       <Board> data-v<M> --data-folder … --prep prep-v<K>   (a version made by hand)
```

The DataPrep commands live in `scripts/insight_ladder_prep.py` (its checks in `insight_ladder_prep_checks.py`), the
Board's in `scripts/insight_ladder_datajob.py`, the runner in `ref/run_prep.py`; `tests/test_dataprep.py` keeps them.
The cards are `haipipe-insight-workflow/ref/run-cards.md` § Data Prep, Prep, Step and Data Job.
