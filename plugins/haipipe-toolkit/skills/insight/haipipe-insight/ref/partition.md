# ref/partition.md · the partition-major InsightBoard layout grammar

An InsightBoard reads ONE dataset either as one story or as several told the same way. When subgroup analysis is first-class, the same ladder climbed per subgroup under identical thresholds, the board lays out PARTITION-MAJOR: groups are partitions, rungs live inside each group. This file is the single source for that layout's grammar (JL 260823); it is a REFERENCE, not a verb, which is why it lives in `ref/` and not `fn/` (JL 260823). The default layout stays rung-major, groups `1-D-data/` through `4-W-wisdom/`, and nothing in this file applies to it.

## When each layout applies

```text
rung-major        one data view · groups are the four rungs
                  pick when partitions are at most a COLUMN inside an I page
partition-major   subgroups are first-class · groups are partitions
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
└── X-cross/                  the ONLY non-mirroring group · comparison lives here
                              (no index: letters sort last · legacy boards: 9-X-cross/)
```

X carries NO index: letters sort after digits, so `X-cross/` seats itself last in every listing, forever, and adding a partition renames nothing — a group rename would break exact parent-row lineage and frozen input paths. Partition groups take 2, 3, 4... in the order they are registered on MT00. Boards scaffolded before 260827 carry the legacy pin `9-X-cross/`; both forms are legal and a live board is never renamed for this. There is never a second X group: X is the one comparing group, however many columns it compares — and a board reaching past a handful of audiences is almost always misreading covariates as audiences (I-page columns) or holding several programmes that should be several boards.

1. **Page id = partition letter + rung letter + NN.** `BK01` reads: partition B, Knowledge, first page. The engine's `[A-Z]{1,2}\d` id grammar already parses this; no engine change exists or is needed. Within a group the rung letters D, I, K, W sort in climbing order, so `ls` reads as the ladder. Reserved letters: F names the template and X the cross group; Q, S and M may never name a partition, because they collide with question ids (a partition-Q data page would be `QD01`), the engine's S page class, and the MT head group.
2. **F is the template.** Every partition group mirrors `1-F-full/` slug for slug: `FD02-funnel-counts` begets `BD02-funnel-counts`. The mirror is checkable by set-diff (`ls */?D01-*` style); a page missing from a partition group must be a registered refusal on the owning MT register, written `🚫` with a reason, never a silent gap.
3. **X is the only group allowed to compare.** A per-partition page may not carry a cross-partition sentence; the contrast is a new derivation and belongs to an X Information page, the heterogeneity claim to an X Knowledge page. X holds no data of its own and mirrors nothing.
4. **MT00 is the partition register.** List letter, name, filter, group folder, and config; list X with no filter. Shared thresholds belong to the Task Job, for example `tasks/<block>/<job>/src/thresholds.yaml`. Every consulted Task config references that one source; no Page or config restates its values. Until the file exists, dependent work is PENDING.
5. **A partition is a config over shared code.** Current Tasks live at `tasks/<block>/<job>/<task>/`; partition inputs use `scripts/config/<partition>.yaml`, with native Tickets under `runs/`. F also needs an unfiltered config, commonly `full.yaml`. Adopt an existing name for the same cut. Resolve output through the Task owner's Job `src/config-defaults.yaml` `store:` binding and native runtime's recorded effective output. A Board's `store:` describes its store; it does not override the Task resolver. A stale config-local `store:` or the viewer process's `RESULT_STORE` cannot establish current output identity. Explicit per-invocation overrides remain valid only when recorded in the native Ticket/receipt and indexed by the Insight Runtime. Default results mirror `<store>/<block>/<job>/<task>/results/<run>/runtime.yaml`; preserve any owner's declared version dialect. Discovery prefers exact native Runtime references, then these current config/Job defaults. Historical `tasks/<group>/<task>/configs/` layouts and Probe receipts remain read-only compatibility inputs.
6. **Question ids are partition-free.** A question is written once on its register and asked per partition; the register's Queue carries one COLUMN per partition, plus an X column whenever the register holds an X-routed question, and X is the cross group, not a partition (see `haipipe-insight-question`). `QK1` spans all partitions; there is no `QK1-B`.

## The pooling verdict conditions every W page

A partition-major board asks whether the compared partitions support common counsel or require separate counsel. The answer is a Knowledge page in X, conventionally `XK02-pooling-verdict`; every partition W page is conditioned on its current outcome. The verdict cites the shared threshold source and version fixed before the comparison. A non-significant difference alone does not establish POOL. If the comparison is complete but cannot support either conclusion, use `UNDETERMINED`; missing inputs or unfinished comparisons remain pending and do not create a verdict.

```text
XK02 verdict   consequence
────────────────────────────────────────────────────────────────────
POOL           every non-template W page DEFERS, explicitly and by id,
               to the template partition's W page, which carries the board's
               one counsel and never defers; no new signature is required
SPLIT          eligible partition W pages may counsel within their own
               evidenced boundaries; XK02 is necessary but not sufficient to
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
Folder kinds   FD01 is Data, XK01 is Knowledge; legacy runtime pages
                may retain page-type: data/knowledge, but no partition kind exists
board.md        no new key; store:, spine:, close: as everywhere else
run / result    the rung's rules apply unchanged inside every partition group
engine          no regex, renderer or checker change; the id grammar already fits
```

## Worked example

Historical frozen instance (its kind-first board name is a compatibility
address, never a scaffold pattern):
`designs/Project-Application-SMSDesign/applications/A00_InsightBoard-SMSR2v1-260821/`.
It holds the template partition F in `1-F-full/` (config `full.yaml`) plus
registered subgroup partitions from `2-B-youngmale/` on, X group
`9-X-cross/` holding `XI01-partition-contrast → XK01-heterogeneity →
XK02-pooling-verdict` (a POOL verdict as of 260827, so every non-template W
defers), registers MT01-MT04 carrying one column per partition plus X where
routed, and tasks reused from `tasks/D01_cohort_profile/`.
