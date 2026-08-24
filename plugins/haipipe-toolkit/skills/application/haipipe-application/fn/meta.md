# `meta` · create or resume the one InsightBoard Meta Page

1. Resolve the Application root and the InsightBoard. If `<DataSubject>-InsightBoard/board.md` is absent, create the board before the Page.
2. Find the one `page-type: meta` Page. If absent, create `<DataSubject>-InsightBoard/0-MT-meta/MT00-meta/MT00-meta.md` through `haipipe-page` and load `haipipe-page-for-meta`.
3. Inventory every source: owner, path or table, run identity, dated extract. Bind accepted Task or Discovery Pages through PageX; a source with no resolvable run identity is a finding, not a row.
4. State unit and grain per source, how the sources join, the population with its exclusions, and the covered time window.
5. Give each source an as-of date and the staleness condition that reopens dependent D pages.
6. Record known limits: missingness, instrumentation gaps, suspected bias. Empty is a claim and needs a sentence saying so.
7. Ensure the group's four question registers exist beside this page, `MT01-question-data` through `MT04-question-wisdom` under `haipipe-page-for-question`. Write no question into them from here: a Brief need lands through the `question` verb, and empty registers are a valid state, not a gap.
8. On a partition-major board (`ref/partition.md`) this page also carries the Partition Register and Shared Thresholds divisions, per `haipipe-page-for-meta` 0.3.0; they are this page's content, not a register's.
9. Run the Page workflow until CHECK settles or holds the Page.

Describe only. A sentence that interprets, compares, ranks, or recommends belongs on a D, I, K or W page and fails here. Meta holds no question; the registers do.

Return the Meta Page path, source count, oldest as-of date, open register questions, and next phase.
