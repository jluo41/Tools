# ref/partition.md · the partition-major InsightBoard layout grammar

An InsightBoard reads ONE dataset either as one story or as several told the same way. When subgroup analysis is first-class, the same ladder climbed per subgroup under identical thresholds, the board lays out PARTITION-MAJOR: groups are partitions, rungs live inside each group. This file is the single source for that layout's grammar (JL 260823); it is a REFERENCE, not a verb, which is why it lives in `ref/` and not `fn/` (JL 260823). The default layout stays rung-major, groups `1-D-data/` through `4-W-wisdom/`, and nothing in this file applies to it.

## When each layout applies

```text
rung-major        A01 style · one data view · groups are the four rungs
                  pick when partitions are at most a COLUMN inside an I page
partition-major   A02 style · subgroups are first-class · groups are partitions
                  pick when each subgroup must produce its OWN K claims and W counsel
```

The choice is per board and is made once, at scaffold. A rung-major board whose I pages keep growing partition columns that readers ask K questions about is the signal to open a partition-major board, not to mutate the existing one.

## The grammar

```text
<board>/
├── board.md                  spine · close · store: (unchanged, see haipipe-task)
├── 0-MT-meta/                MT00 + the four question registers (unchanged shape)
├── 1-F-full/                 the TEMPLATE ladder · the whole extract, no filter
├── 2-<L>-<slug>/             one group per partition · mirrors 1-F-full slug for slug
└── <last>-X-cross/           the ONLY non-mirroring group · comparison lives here
```

1. **Page id = partition letter + rung letter + NN.** `BK01` reads: partition B, Knowledge, first page. The engine's `[A-Z]{1,2}\d` id grammar already parses this; no engine change exists or is needed. Within a group the rung letters D, I, K, W sort in climbing order, so `ls` reads as the ladder.
2. **F is the template.** Every partition group mirrors `1-F-full/` slug for slug: `FD02-funnel-counts` begets `BD02-funnel-counts`. The mirror is checkable by set-diff (`ls */?D01-*` style); a page missing from a partition group must be a registered refusal on the owning MT register, written `🚫` with a reason, never a silent gap.
3. **X is the only group allowed to compare.** A per-partition page may not carry a cross-partition sentence; the contrast is a new derivation and belongs to an X Information page, the heterogeneity claim to an X Knowledge page. X holds no data of its own and mirrors nothing.
4. **MT00 is the partition register.** One division lists every partition: letter, name, filter, group folder. One division states the shared-threshold rule: thresholds live in ONE file the task layer owns (`configs/_thresholds.yaml` beside the partition configs), every partition config references it, and no page or config may restate a value from it. No other page may define a partition.
5. **A partition is a CONFIG, never a code change.** The task layer is untouched: one task folder is one function, one partition is one `configs/<partition>.yaml`, and the board's `store:` routes results exactly as `haipipe-task` already rules. Adding a partition is one group folder mirroring F, one MT00 register row, and one config per task folder consulted.
6. **Question ids are partition-free.** A question is written once on its register and asked per partition; the register's Queue carries one COLUMN per partition (see `haipipe-page-for-question` 0.2.0). `QK1` spans all partitions; there is no `QK1-B`.

## The pooling verdict conditions every W page

A partition-major board exists to answer one question: one story or several. That answer is a Knowledge page in X, conventionally `XK02-pooling-verdict`, and every partition W page is CONDITIONED on it:

```text
XK02 verdict   consequence
────────────────────────────────────────────────────────────────────
POOL           every non-template W page DEFERS, explicitly and by id,
               to the template partition's W page
SPLIT          the differing partition's W page may counsel its own action,
               and XK02 becomes the birth certificate a child board must cite
```

A child InsightBoard for one partition may be opened ONLY by citing a SPLIT verdict page in its own MT00. A subgroup earns a board by having its own consumer, never by having its own numbers.

## What this layout does NOT change

```text
page types      FD01 declares page-type: data, XK01 declares page-type: knowledge;
                no page-type: partition exists and none may be invented
board.md        no new key; store:, spine:, close: as everywhere else
probe / qa      the rung's rules apply unchanged inside every partition group
engine          no regex, renderer or checker change; the id grammar already fits
```

## Worked example

`designs/Project-Application-SMSDesign/applications/A02_InsightBoard-SMSR2Partitioned/`: partitions F (full) and B (youngmale, `patient_gender=='M' AND age<=35.0`), X group `XI01-partition-contrast → XK01-heterogeneity → XK02-pooling-verdict`, registers MT01-MT04 carrying one column per partition, tasks reused from `tasks/D01_cohort_profile/` with one config per partition.
