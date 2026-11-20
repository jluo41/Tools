DataPrep: the code that turns a raw export into a folder ready for insight
==========================================================================

(261116, redesigned 261120; workbench-insight topics T10-T30.) A Board Job pins three versions (JL 261120: "I think it
should be three versions"):

```text
data version      the raw data: a raw export, its cut and params (board.md versions:)       on the Board
prep version      the DataPrep Block's code: a chain of steps, signed                      in the DataPrep Block
question version  the Question Book's code: the questions and their scripts, signed        in the Question Book
```

A Job `jNN_data-vM_prep-vK_question-vN/` runs them: its first Task runs the prep version on the data version's raw
export and writes a ready folder; the question version's Tasks follow and read that folder. One version moves per Job,
so a change in an answer keeps one cause.

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
        ├── step.md                              the spec: step · script · goal · reads · writes · checks · cut · params ·
        │                                        agreed (cut and params: the keys of ctx.cut, ctx.params it reads)
        └── scripts/<script>.py                  run(ctx), and nothing else that runs

<Project>/insight/Insight-<D>/                   the Board: one dataset
├── board.md                                     … · dataprep: <the DataPrep Block> ·
│                                                versions: [{version: data-vM, raw, cut: {…}, params: {…}, frozen}]
└── jNN_data-vM_prep-vK_question-vN/             a Job of three versions
    ├── jNN_data-vM_prep-vK_question-vN.md       data · prep · prep-hash · dataprep · release · hash · moved · ready
    ├── t01_prep-vK_<slug>/runs/r01_<dataset>/   the whole prep version, one Run (run.sh calls ref/run_prep.py):
    │                                            result/ runtime.yaml (a line per step), provenance/, the card,
    │                                            steps/<step>/metrics.json, heavy.yaml; it writes the ready folder
    │                                            <store>/<dataset>_data-vM@prep-vK/
    └── tNN+1_<L><NN>_<slug>/runs/rNN_<segment>/  the question version's Tasks, one place after their release number,
                                                 reading the ready folder (ref/run_job.py)
```

The rules
---------

1. **A Set, not a dataset; a data version is raw data.** `<Set>` names a family of datasets made by the same code; it
   carries no version. A Board names its DataPrep Block (`datasource <Board> --dataprep …`, which must list the Board
   in `serves:`) and its data versions: `data <Board> data-vM --raw … --cut … --param …` adds the raw export, its cut
   and its params as a row of `versions:`, frozen. New raw data is the next data version; an older row that names only
   a folder made by hand gains its raw, cut and params once.
2. **A prep version is code, signed, then frozen.** `prep` opens the next one from the newest; `--steps a,b,c` names
   its steps in order (a kept step moves to its new number, a new one is made empty, one left out is not carried). A
   step is `step.md` (its goal line among its fields) and `scripts/<script>.py` exposing `run(ctx)`, as a question
   is `question.md` and its scripts; it holds no face of its own, no Run, no config and no output. `sign`
   needs every step agreed by an agent that did not write it (run-review-steps) and every script exposing `run(ctx)`;
   it pins `hash:` over `src/` and every step's face, spec and scripts.
3. **A step reads only what `ctx` gives it.** `ctx.raw` is the data version's raw export, `ctx.prev` the earlier step's
   output, `ctx.refs` the Block's `references:` (each read at the version named there), `ctx.cut` and `ctx.params` the
   data version's cut and settings (`data … --cut … --param …`, frozen with it). A step declares the
   cut and params keys it reads (`step.md` `cut:` and `params:`); `job` and the runner refuse a data version's key no step
   declares. A step refuses an unknown key in a dict it reads (cut or params) rather than ignore it, and leaves a dict
   it does not read alone: every step sees the whole ctx (T28). No cache, no other
   pipeline's store, no shared source stage is an input. A library a step imports pins its sha256 in the step's own
   code, so the signature covers the pin, and the step refuses when the library differs (T25).
4. **A step writes only `ctx.out`, and no page shows a record value.** The first step writes its Run's `result/`; the
   last step writes the ready folder `<store>/<dataset>@prep-vK`; one between them writes the Run's heavy folder under
   `_WorkSpace/ProjectResult/…` (the Result keeps `heavy.yaml`). Every step may also write one light
   `ctx.result / "metrics.json"` (its shapes, counts and check outcomes, under 256 KB), what a reader opens first; a
   middle or last step writes nothing else into `result/`, which is the runner's (T29). A Result, a dictionary, a manifest or a summary
   carries shapes, counts and names: no sample column, no first value, no `head()` of a table. The runner fails a
   ready folder whose dictionary has a sample column; `audit <Block>` names each script line that takes a record's
   value (`records`).
5. **A Job pins three versions.** `job <Board> --data data-vM --prep prep-vK --release question-vN` refuses an unsigned
   prep or question version, a prep version whose code changed since its signature, a data version with no raw export,
   a key no step reads, and a Job that moves more than one version from the Job before it. It opens
   `jNN_data-vM_prep-vK_question-vN/`: `t01_prep-vK_<slug>/` with one hard Run, then the question version's Tasks one
   place after their release number. Every Job on a Board shares one count.
6. **t01 runs the whole prep version in one Run and makes the ready folder.** `ref/run_prep.py <Job>` runs every step
   in order inside t01's Run and stops at the first that refuses or fails. The Run keeps a line per step in
   `runtime.yaml`, the exact scripts and their sha256 in `provenance/`, the experiment card, each step's light
   `metrics.json`, and `heavy.yaml`. On success it writes the ready folder `<store>/<dataset>_data-vM@prep-vK/` and the
   Job face's `ready:`; a done Run is never run again. The question Runs read `ready:` and are refused until it is
   there. A later Job with the same data and prep versions reuses the ready folder, its t01 done. `drop-datajob <Job>`
   undoes a Job of the withdrawn shape (`jNN_prep-vK-<slug>_data-vM/`, a Task per step).
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
stay with the questions. A signed question version is never edited: the next prep version adds the column (a Job with `moved: prep`), and the next question version drops its own copy (`moved: code`).

`ctx`
-----

```text
ctx.raw      Path   the data version's raw export (board.md versions: raw)
ctx.out      Path   where this step writes (rule 4)
ctx.data     str    the data version
ctx.prev     Path   the earlier step's ctx.out; None for the first step
ctx.cut      dict   the data version's cut: (dates, a sub-cohort), applied by the step that cuts
ctx.params   dict   the data version's params: (the settings its steps read, such as source_fn); {} when none
ctx.refs     dict   {name: Path}, the DataPrep Block's references:
ctx.dataset  str    the Board's dataset;  ctx.prep  the prep version
ctx.result   Path   the Run's result/: one light metrics.json may go there (rule 4)
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
insight_ladder.py datasource <Board> --dataprep <DataPrep Block>
insight_ladder.py data       <Board> data-v<M> --raw <SPACE-relative raw export> [--cut k=v,…] [--param k=v,…]
insight_ladder.py job        <Board> --data data-v<M> --prep prep-v<K> --release question-v<N>
python ref/run_prep.py       <Job>                 (or <Job>/t01_prep-vK… r01_<dataset>, which its run.sh does)
insight_ladder.py drop-datajob <Board Job of the withdrawn shape>
```

The DataPrep commands live in `scripts/insight_ladder_prep.py` (its checks in `insight_ladder_prep_checks.py`), the
Board's (the data version, the Job of three versions) in `scripts/insight_ladder_datajob.py`, the runner in `ref/run_prep.py`; `tests/test_dataprep.py` keeps them.
The cards are `haipipe-insight-workflow/ref/run-cards.md` § Data Prep, Prep, Step and Data Job.
