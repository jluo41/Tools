A Run's report: what one Run's result shows, in a few sentences
================================================================

(261120; workbench-insight T31, T32.) A hard Run's `result/` holds what its code made: tables, figures, `metrics.json`, the
receipt, and the generated `tables.md` (the ask and the tables, laid out). None of it says what the numbers mean.
After each Run, an agent reads only that Run's result and writes the Run's report; another agent checks it. Opening a
Run shows its reading first, and the Task's page is built from its Runs' reports.

```text
<Job>/tNN_<L><NN>_<slug>/runs/rNN_<segment>/
├── run.sh · run.yaml                 the ticket and the Run's card
├── result/                           the ticket's: cleared and rewritten on every rerun
│   ├── <tables>.csv · fig_*.png · partition_power.csv · runtime.yaml · provenance/
│   └── tables.md                     generated from the tables (report.md before 261120)
└── report.md                         the Run's report: an agent's, kept across reruns
```

The report
----------

`report.md` holds a headline (one line: what this segment's result shows), a few sentences, each citing the result
file its numbers come from, and a caveat when one holds (thin, refused, not checkable). Its front keeps the same, with
`result-sha256` (the result it read), `written-by` and `check`. It says no more than its question's level allows: a
Data Run says what the data holds, never why; an Information Run what differs and by how much; a Knowledge Run
whether it holds against its threshold. No record value appears in it, only shapes, counts, rates and names.

- **A refused Run** gets one too: the refusal's reason in plain words, with the numbers it rests on
  (`partition_power.csv`). A failed Run gets none: fix and rerun its ticket.
- **The prep Task's Run** (t01, ref/dataprep.md) gets one: the experiment card and each step's checks in a few
  sentences, citing `experiment_card.json` and `steps/<step>/metrics.json`.
- **A rerun keeps the report** (the ticket clears only `result/`). When the result changes, its hash no longer matches
  `result-sha256`: the report is stale, the Run's page marks it ❗, and the Task's page refuses to be written over it.
- **A Run whose result equals an earlier Job's** (same question, same segment, same hash, its report checked) carries
  that report over, `carried-from:` naming it, with no new writing.

Who writes it, who checks it
----------------------------

```text
run-report-j<NN>  · run-report-t<NN>           hai-insight-agent: writes a spec per Run, run_report.py lays it out
run-check-report-j<NN> · run-check-report-t<NN>  hai-insight-reviewer-agent: each sentence against the tables;
                                               run_report.py check traces every number into the file it cites
```

The writer's spec:

```yaml
headline: <one line>          # it gives only numbers its sentences give
sentences:
  - {text: "<sentence>", file: <a file of result/, such as grouping_audit.csv>}
  - text: "17 of the 29 groupings have a thin level; zip3's 23,535 thin rows are 44.1% of the segment's 53,342"
    files: [grouping_audit.csv, partition_power.csv]     # a sentence may join files
    derived:                                             # a number no cell holds, with the rule that makes it
      - {value: 17, how: "count rows in grouping_audit.csv where n_levels_suppressed > 0"}
      - {value: 29, how: "count rows in grouping_audit.csv"}
      - {value: 44.1%, how: "23535 / 53342"}
caveat: <one line>            # optional
```

Every number has one source:

- **In a cited file**, as written, rounded to the sentence's decimals; a percent may be a share. A small number (0, 1,
  2) is found in almost any table, so this is a floor: the checker still reads each sentence against its row.
- **Derived**, under the sentence's `derived:` with its rule, computed by the tool from the files the sentence cites:
  `count rows`, or `sum | min | max | mean <column>`, each with `in <file>` when the sentence cites two tables and
  `where <column> <op> <value> [and …]`; or arithmetic (`+ - * /`) over numbers the report gives or the files hold. A
  derived number is computed, never looked up: one that a cell elsewhere happens to hold no longer passes for it.
- **The headline** gives only numbers its sentences give, since the Task's page quotes it.

`write` refuses a derived number its rule computes to another value, and a derived value the sentence does not give.
`check` refuses the agent that wrote the report, a stale report, a derived number its rule does not give, and a number
with no source. A number the checker confirms by hand against the tables, or one whose rule the tool cannot read, is
passed with `--accept`, and the report keeps it in `accepted:`. `--reject "why"` returns the report (`check: ❗ …`) to
be written again. The rules are `ref/run_report_numbers.py`.

The Task's page
---------------

`write_answer_page.py` reads each Run's report: a division with no `takeaway:` takes its Run's headline, and a stale
or returned report stops the page. The Task's `takeaways:` are then those headlines, or the writer's sharper line.
Until the page is written, the workbench shows each Run's headline where the takeaway would be.

Commands
--------

```text
python ref/run_report.py todo  <Job | Task | Run>               missing · stale · returned · unchecked
python ref/run_report.py carry <Job | Task>                     carry checked reports of the same result
python ref/run_report.py write <Run> <spec.yaml> --by <agent>
python ref/run_report.py check <Run> --by <agent> [--accept 9,22] [--reject "why"]
python ref/run_report.py tables <Job | Task | Run>              a Run made before 261120: its generated
                                                                result/report.md renamed result/tables.md
```

`tests/test_run_report.py` keeps it.
