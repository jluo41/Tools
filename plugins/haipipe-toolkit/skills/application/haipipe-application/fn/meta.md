# `meta` · create or resume the one InsightBoard Meta Page

1. Resolve the Application root and the InsightBoard. If `<DataSubject>-InsightBoard/board.md` is absent, create the board before the Page.
2. Find the I0 Folder (`folder-kind: meta`; legacy `page-type: meta` remains readable). If absent, create `<DataSubject>-InsightBoard/0-MT-meta/MT00-meta/MT00-meta.md` through `haipipe-folder` + `haipipe-page` and load `haipipe-insight-meta`.
3. Inventory every source: owner, path or table, run identity, dated extract.
   Bind cross-Folder evidence through accepted Supporting Run Results and one
   frozen Local Input per Evidence Item. A related Page link is Context only;
   a source with no resolvable evidence authority is a finding, not a row.
4. State unit and grain per source, how the sources join, the population with its exclusions, and the covered time window.
5. Give each source an as-of date and the staleness condition that reopens dependent D pages.
6. Record known limits: missingness, instrumentation gaps, suspected bias. Empty is a claim and needs a sentence saying so.
7. Ensure the group's four question registers exist beside this page, `MT01-question-data` through `MT04-question-wisdom` under `haipipe-insight-question`. Write no question into them from here: a Brief need lands through the `question` verb, and empty registers are a valid state, not a gap.
8. On a partition-major board (`ref/partition.md`) this page also carries the
   Partition Register and Shared Thresholds divisions. Recompute the derived
   `partition × D/I/K/W` Question Groups whenever the partition register moves;
   they are a status projection, not Meta content or new Folders.
9. Run one Page workflow pass until CHECK emits CLOSE or the Page names HOLD.

Describe only. A sentence that interprets, compares, ranks, or recommends belongs on a D, I, K or W page and fails here. Meta holds no question; the registers do.

Return the Meta Page path, source count, oldest as-of date, derived Question
Groups with open cells, and next phase.
