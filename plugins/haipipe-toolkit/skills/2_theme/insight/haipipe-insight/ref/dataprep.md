DataPrep: the Block that makes a Set's data versions
=====================================================

(261116, workbench-insight topic T10.) The ladder has three clocks, one Block each. The **Question Book** moves the
question clock (a question version, `question-vN`). The **DataPrep** Block moves the prep clock: the tools that turn a
Set of raw datasets into analysis-ready data (a prep version, `prep-vK`). The **insight Board** pairs them: each Job
runs one question version on one data version, and each data version names the prep version that made it. Before
this kind existed, a data version was a folder built somewhere else. Its Board recorded no code, no prep version and
no receipt, so nobody could rebuild it or tell which tools a change of answer came from.

Read this before making, growing or carrying a DataPrep Block. The Question Book and the Board stay as
[insight-ladder.md](insight-ladder.md) draws them.

The tree
--------

```text
<Project>/insight/InsightDataPrep-<Set>/         one Set: a family of related datasets (DrFirstExp: SMSAll, SMSR2, SMSR3 …)
├── board.md                                     board-kind: insight-dataprep · workbench: insight · set: <Set> ·
│                                                store: <SPACE-relative folder the Runs write the rows to> ·
│                                                serves: [insight/Insight-<D>, <SPACE-relative Board in another Project>] ·
│                                                datasets: [{name, raw, why}] · references: [{name, path, version, why}] ·
│                                                ## Background
├── background/                                  the source's documents, message content, the data owner's answers;
│                                                never a row of data
├── runs/                                        soft: run-open-version-prep-v<K>
└── jNN_prep-vK_<slug>/                          one prep version: the tools, frozen once a person signs it
    ├── jNN_prep-vK_<slug>.md                    prep · state: open | closed · signed: ✅ <YYMMDD> · hash · from ·
    │                                            carried-from (the folder the first tools came from)
    ├── src/                                     code two or more steps share
    ├── runs/                                    soft: run-review-steps-prep-v<K> · run-sign-prep-v<K>
    └── tNN_<step>/                              one step (join · cut · derive · document · compare), a Task by the
        ├── tNN_<step>.md                        haipipe-task contract: step · worker · reads · writes · checks · agreed
        ├── scripts/<worker>.py · config/rNN_<dataset>.yaml   the config IS the Run: its env and its output folder
        └── runs/rNN_<dataset>/                  hard: the Task ticket (haipipe-task ref/run-sh-template.sh), run.yaml,
                                                 result/ (receipt, checks, dictionary); the rows land in the store
```

The rules
---------

1. **A Set, not a dataset.** `<Set>` names a family of datasets made by the same tools; it carries no version. A
   dataset of the Set is a `datasets:` row (`insight_ladder.py dataset … --raw`); a Board still holds one dataset.
2. **A prep version is signed, then frozen.** `prep` opens the next one from the newest. It copies every step's face,
   script and config, never its Runs or what they made (`runs/`, `results/`, `notebooks/`), and clears each step's
   `agreed:`. `--steps experiment,source,prepare-cohort`
   names the new version's steps in their order: a kept step moves to its new number (`t03_prepare-cohort`), a new
   one is made empty, and one left out is not carried. A copied step keeps one Run config per dataset, the newest,
   and the first `run <step> dataset <name>` in the new version takes it. `sign` needs every step agreed by an agent
   that did not write it (run-review-steps). It pins `hash:` (the first 12 hex of a sha256 over `src/` and every step's
   face, scripts and config) and closes the version.
3. **A step is a Task; a Run is a dataset.** A step's hard Run `rNN_<dataset>` is made by `run <step> dataset <name>`:
   the Task ticket with `TASK_NAME` set to the step's `worker:`, its card (`type: dataset`, `prep:`) and its config.
   The ticket runs in `insight/` only for an `InsightDataPrep-*` Block and only for a `jNN_prep-vK` Job. It exports
   `HAIPIPE_CONFIG`, never a config's `env:`: the worker reads which dataset and which output folder from that file
   and stops without them. A worker never defaults to a dataset, since a default builds the wrong data without a
   word. A carried worker that reads environment variables keeps its maker's env export in its tickets until the next
   prep version reads its config.
   **A step reads only its dataset's `raw:` folder** in the raw store, the earlier steps of the same prep version, and
   the Block's `references:` (tables every dataset may join, such as an area or a prescriber table, each read at the
   version named there: `insight_ladder.py reference`). No cache, and no other pipeline's store, is an input. A shared source stage is not a way in either: given
   `raw_data_path`, it copies the raw export into the shared raw store and overwrites the shared source cache,
   whatever `use_cache` says. So a step loads the raw export itself and writes anything it builds in between under its
   own `@prep-vK` place. `audit` names any config with `raw_data_path`, `source_config`, `save_cache` or `use_cache`
   (`inputs`), any dataset whose `raw:` folder is gone (`raw`), which is rebuilt from a new export, never from a
   cache, and any reference that names no version or is not there (`references`).
4. **The rows stay in the store, in a new folder.** A Run writes the analysis-ready rows to a folder named for its
   prep version, `<store>/<name>@prep-vK` (`output.prepare_dir`, and `env.OUT_NAME` when a carried worker names its
   folder from it). It never writes a folder made before, which other work may read, and never one a Board's data
   version names, which is frozen. A config that names no output folder is refused too, since its worker writes
   wherever it likes (a summary at the store's root). `audit <Block>` lists each such config (`outputs`), `sign`
   refuses while one is left, and the next prep version re-aims every copied config at its own `@prep-vK` folders. A
   step that compares datasets reads only its own prep version's folders. The Block holds code, receipts, checks,
   dictionaries and background, never a row. Patient-level data stays on approved storage; the Board and the
   Question Book see only aggregates.
   **What a page can show holds no record value.** A Result, a notebook, and every dictionary, manifest or summary
   written beside the rows (the Board's Description › Dataset shows them) carry shapes, counts and names: no sample
   column, no first value, no `head()` of a table. Top-N counts of a column are counts, not records. `audit` names each
   worker line that takes a record's value and each dictionary with a sample column (`records`); the step review reads
   each one.
5. **A data version names its prep.** `data <Board> data-vM --data-folder <the Run's output> --prep <prep version or
   its Run>` refuses an unsigned prep version and writes `prep:` on the versions row. `audit` gives each Board that a
   DataPrep Block `serves:` a `prep` row: the data versions that name no prep. A Board no DataPrep serves owes none.
6. **One clock per Board Job, still.** A new prep version reaches a Board only through a new data version
   (`moved: data`), so a change in an answer keeps one cause.
7. **The experiment card comes first.** Each prep version's first step reads only the dataset's `raw:` folder: its
   rows and the documents that describe the experiment (settings, data descriptions, timelines). It writes an
   experiment card in its Result, aggregates only:
   - **settings:** experiment ids and names, arms and their counts, batches, message content;
   - **time:** the invitation range in UTC and in local time, active and calendar days, gaps, daily volume, send hours.
   Its checks compare what is stated with what is observed: the stated range, ids and daily volumes against the rows,
   send times inside a stated blackout, more arms than stated. A mismatch stops the Run. A dataset with no documents
   gets a card from the rows marked "nothing stated", never a guess. Questions cite the card; the Data questions stay
   the reader's description of the data.
   - **A description is checked against its own pull** (JL 261119). A document stamped with a pull's time
     (`YYYY-MM-DD-HH-MM` in its file name) is compared only with the export carrying the same stamp. One stamped for
     another pull goes on the card as "describes the <stamp> pull, not this export", its stated values shown and not
     checked; when either file has no stamp, they are compared.
   - **A setting the rows cannot test is said so.** A local-time blackout with no time zone in the rows is "not
     checkable" on the card, never passed.
   - The card is `result/experiment_card.json` and `.md` in each first-step Run, and the same two files in the
     dataset's `@prep-vK` folder once every check passes. `sign` refuses a version whose first step has a Run without
     its card, or no Run (`audit` row `card`); a carried version owes none.

What prep does, and what a question does
----------------------------------------

```text
prep (a step's check)                              a Data question (D)
is the data fit to use? blocks if not              what does the data say? a finding on the page
row counts, date range, keys unique, arms          the shape a reader quotes: who is in it, how the
balanced as assigned, no column read from          arms compare at baseline, which fields are thin
the future of a row
```

A derivation moves from a question version's `src/` to a prep step only when it makes one column per row, reads no
outcome, and is the same for every question (a message's template, an area code). Rates, tests, privacy blanking and
the groupings that define segments stay with the questions (insight-ladder.md rule 4). A signed question version is
never edited. The move takes two Board Jobs: the next prep version adds the column (a new data version,
`moved: data`), then the next question version reads it and drops its own copy (`moved: code`).

Carrying an existing maker
--------------------------

A work Task that already makes the data (one worker, one config per dataset) comes in as the first prep version:
`prep <Block> --slug carried --from <its Project-relative folder>`. Then `step` per tool, its worker and configs
copied in, and `run … dataset <name>` per config. The work Block stays as it was, the record of the Runs it made;
the Boards' existing `folder:` paths keep working. The carried Runs never write the maker's folders: each config's
output becomes `…@prep-v1`, the carried tools run into it, and the new folder is compared with the one it reproduces
(rows, columns, a hash of the sorted rows). A match goes on the Run's card, and the Board's existing data version may
then name prep-v1 by hand. A difference is written down, never hidden. From the signature on, only the DataPrep Block
makes a new data version.

A carried version reproduces, so it may read what its maker read (an existing source cache, say), and it writes no
experiment card. Its face names those inputs, and it still runs no shared source stage and writes only `@prep-v1`.
Rules 3 and 7 hold from the next version on: it reads only `raw:` and the references, its first step writes the
card, and a dataset whose export is gone comes back as a new dataset from its new export. The person who signs the
carried version approves both exceptions with that signature; the step review does not return a carried step for
them.

A second Run of a dataset
-------------------------

A Run that ran is not run again, and its Result is never deleted by hand. `run <step> dataset <name> --again` makes
the next Run of that dataset: it names the newest in `supersedes:` and starts from its ticket and config. Once it has
run, haipipe-run `prune_runs.py <step> --apply --only <step>/<old Run>` removes the old Run (a Run that failed
replaces nothing). Its output folder is the same `@prep-vK` one, rebuilt; a folder a Board's data version names is
still refused (rule 4).

Scripts
-------

```text
insight_ladder.py dataprep <Project>/insight/InsightDataPrep-<Set> --set <Set> --serves <Board>[,…] [--store …] [--title …]
insight_ladder.py dataset  <dataprep> <Name> --raw <SPACE-relative raw folder> [--why …]
insight_ladder.py prep     <dataprep> --slug <what-it-is> [--from <carried-from folder>] [--steps a,b,c]
insight_ladder.py step     <prep version> <slug> [--ask "what it does"]
insight_ladder.py reference <dataprep> <name> --path <SPACE-relative> --version <v> [--why …]
insight_ladder.py run      <step> dataset <name> [--again]   (and run <prep version> review-steps · sign)
insight_ladder.py sign     <prep version> --date YYMMDD
insight_ladder.py audit    <dataprep>      serves · raw · references · workers · configs · outputs · inputs · records ·
                                           card · notebooks · agreed · hash
insight_ladder.py data     <Board> data-v<M> --data-folder … --prep <prep version or its Run>
```

The commands live in `scripts/insight_ladder_prep.py`, the checks and the audit in
`scripts/insight_ladder_prep_checks.py`; `tests/test_dataprep.py` keeps them. The cards are
`haipipe-insight-workflow/ref/run-cards.md` § Data Prep, Prep and Step.
