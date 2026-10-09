# ref/partition.md · the partition-major InsightBoard layout grammar

> **Older layout (261008).** This is the register board's partition-major grammar. On the insight ladder the cuts
> belong to a release: read [release.md](release.md) § The cuts (the cuts, cross, power, the pooling verdict).

An InsightBoard reads ONE dataset either as one story or as several told the same way. When subgroup analysis is first-class, the same ladder climbed per subgroup under identical thresholds, the board lays out PARTITION-MAJOR: groups are partitions, levels live inside each group. This file is the single source for that layout's grammar (JL 260823); it is a REFERENCE, not a verb, which is why it lives in `ref/` and not `fn/` (JL 260823). The default layout stays level-major, groups `1-D-data/` through `4-W-wisdom/`, and nothing in this file applies to it.

**Since 261001 (page tickets).** A partition is a cut of the board's one
extract: one config per task (`rNN_<dataset>_<cut>`, its `population.where`),
one column on every register, one partition table in the workbench, and one
partition group folder (`1-full/`, `2-<partition>/`, `9-cross/`). The group
folder is the Job and each answering page in it the Task: the page's `.md` is
the report, its `runs/run_bNNjNNtNNrNN_<partition>_<task>.sh` tickets call the
task runs on that cut, and its `results/<ticket>/` hold what they wrote
(`ref/report.md`). The page-id rules below apply to every page.

## When each layout applies

```text
level-major        one data view · groups are the four levels
                  pick when partitions are at most a grouping COLUMN inside a run
partition-major   subgroups are first-class · groups are partitions
                  pick when each subgroup must produce its OWN K claims and W counsel
```

The choice is per board and is made once, at scaffold. A level-major board whose I pages keep growing partition columns that readers ask K questions about is the signal to open a partition-major board, not to mutate the existing one.

## The grammar

```text
<board>/
├── board.md                  spine · close · extract (no store: results live in pages)
├── 0-MT-meta/                MT00 + the four question registers (unchanged shape)
├── 1-full/                   the TEMPLATE ladder · the whole extract, no filter
├── <n>-<name>/               one group per partition · mirrors 1-full slug for slug
└── 9-cross/                  the ONLY non-mirroring group · comparison lives here
                              (pinned at 9 so it sorts last)
```

Partitions carry NO letters (JL 261001): a partition is named by its full name, one lowercase word, unique on the board, and never `meta` (`full`, `alpha`, `beta`, `cross`). Its group folder is `<n>-<name>/`. `cross` is pinned at `9-cross/` so it seats itself last in every listing, and adding a partition renames nothing — a group rename would break exact parent-row lineage and frozen input paths. Partition groups take 2, 3, 4... in the order they are registered on MT00. (History: boards made before 261001 used letter folders such as `1-F-full/`, `X-cross/` or `9-X-cross/` and letter page ids such as `FI02`.) There is never a second cross group: `cross` is the one comparing group, however many columns it compares — and a board reaching past a handful of audiences is almost always misreading covariates as audiences (I-page columns) or holding several programmes that should be several boards.

1. **Page id = level letter + NN + `-` + partition name.** `K01-alpha` reads: Knowledge, first page, partition alpha. The page folder is `<id>-<slug>/` holding `<id>-<slug>.md`: `<n>-<partition>/<L><NN>-<partition>-<slug>/<L><NN>-<partition>-<slug>.md`. Within a group the level letters D, I, K, W sort in climbing order, so `ls` reads as the ladder. No letter is reserved; a partition name must only be one lowercase word, unique, and not `meta`.
2. **`full` is the template.** Every partition group mirrors `1-full/` slug for slug: `D02-full-<slug>` begets `D02-alpha-<slug>`. The mirror is checkable by set-diff (`ls */D01-*` style); a page missing from a partition group must be a registered refusal on the owning MT register, written `🚫` with a reason, never a silent gap.
3. **`cross` is the only group allowed to compare.** A per-partition page may not carry a cross-partition sentence; the contrast is a new derivation and belongs to a cross Information page, the heterogeneity claim to a cross Knowledge page. `cross` holds no data of its own and mirrors nothing.
4. **MT00 is the partition register.** List name, filter, group folder, and the config stem every task uses for the cut (`rNN_<dataset>_<partition>`); there is no letter column; list `cross` with no filter. Shared thresholds belong to the Task Job, for example `work/<block>/<job>/src/thresholds.yaml`. Every consulted Task config references that one source; no Page or config restates its values. Until the file exists, dependent work is PENDING.
5. **A partition is a config over shared code.** The code lives in the Project's DIKW task Block (`work/b5N_<topic>_dikw/jNN_<level>_<topic>/tNN_<task>/`); a partition is `scripts/config/rNN_<dataset>_<cut>.yaml` with its ticket `runs/rNN_<dataset>_<cut>.sh`, the same stem. `full` needs an unfiltered config (`rNN_<dataset>_full`). The config names the extract, the cut and `answers:`; it never names a board or a result folder. An answering page calls the run through its own ticket, which sets `RESULT_DIR` to the page's `results/<ticket>/` and `RUN_TICKET` to itself, so the result lands at `<page>/results/<ticket>/runtime.yaml`, recording both tickets. Shared thresholds are one Job (or Block) `src/` file every config references; no config restates a value. Historical `work/<group>/<task>/configs/<call>.yaml` layouts with a config-local `store:` and Probe receipts remain read-only compatibility inputs.

## The pooling verdict conditions every W page

A partition-major board asks whether the compared partitions support common counsel or require separate counsel. The answer is a Knowledge page in cross, `K<NN>-cross-pooling-verdict`; every partition W page is conditioned on its current outcome. The verdict cites the shared threshold source and version fixed before the comparison. A non-significant difference alone does not establish POOL. If the comparison is complete but cannot support either conclusion, use `UNDETERMINED`; missing inputs or unfinished comparisons remain pending and do not create a verdict.

```text
cross verdict   consequence
────────────────────────────────────────────────────────────────────
POOL           every non-template W page DEFERS, explicitly and by id,
               to the template partition's W page, which carries the board's
               one counsel and never defers; no new signature is required
SPLIT          eligible partition W pages may counsel within their own
               evidenced boundaries; the cross verdict is necessary but not sufficient to
               open a child board, which also needs its own registered consumer
UNDETERMINED   no non-template W may defer as though POOL were proved or issue
               partition-specific counsel as though SPLIT were proved; the
               template W may counsel only for the full-extract scope and must
               state that subgroup applicability is unresolved. An unanswered
               partition W may close as `🟡 <page> final` only when it records
               why the answer cannot close and what evidence or decision could
               resolve it. That licensed non-answer has no GI5 handoff, no
               signature, and no Design binding; GI6 records the partial exit.
               No child board may be opened from this outcome
```

Execution order across groups is the Insight workflow's rule
(`haipipe-insight-workflow`), not this file's: this file rules the grammar only.

A child InsightBoard for one partition may be opened ONLY by citing a SPLIT verdict page in its own MT00. A subgroup earns a board by having its own consumer, never by having its own numbers.

## What this layout does NOT change

```text
Folder kinds   D<NN>-full is Data, K<NN>-cross is Knowledge; legacy runtime pages
                may retain page-type: data/knowledge, but no partition kind exists
board.md        no new key; spine:, close: as everywhere else (no store:)
run / result    the level's rules apply unchanged inside every partition group
engine          no regex, renderer or checker change; the id grammar already fits
```

## Worked example

A generic sketch: the template partition `full` in `1-full/` (config
`rNN_<dataset>_full`) plus registered subgroup partitions `2-alpha/`,
`3-beta/`, …, the cross group `9-cross/` holding
`I<NN>-cross-partition-contrast → K<NN>-cross-heterogeneity →
K<NN>-cross-pooling-verdict` (under a POOL verdict every non-template W
defers), registers MT01-MT04 carrying one column per partition plus `cross`
where routed, and every page ticket calling shared tasks in the DIKW Block.
