# A01 · Every Delivery item names its artifact

**Need.** JL reads a paper Board's Delivery panel to open and share the built paper: the LaTeX PDF, the Word file, and
the changes PDF that marks what changed since the last round. Each item must say which file it is, in a name he can
repeat to a co-author (JL 261121: "call it Paper-Latex, and Paper-Latex-Diff").

**Now (before).** `board_writing.py` built each item with a full name ("The paper · LaTeX", "The paper · LaTeX diff",
"The paper · Word", …) and `TAB_GROUPS` showed a shortened tab name under each kind heading: "The paper" under LaTeX,
"The paper" again under Word, "Changes since the last round" for the diff.

**Gap.** The shortened names dropped the artifact: two items read "The paper", and the diff was described, not named.
Nothing checked how an item is named, so any new item could arrive the same way.

**Methods.** Name each item by its artifact as Kind-Lane[-Variant] (Paper-Latex, Paper-Latex-Diff, Paper-Word,
Paper-Word-Tracked, Supplement-Latex, Supplement-Word, Combined-Latex, Cover-Letter, Portal) and show that same name in
the list; the kind heading (LaTeX, Word, Submission) stays as the grouping.

**Update.** `servers/workbench-paper/board_writing.py`: every item's full name and `TAB_GROUPS`;
`tests/test_version_and_jobs.py` follows; `tests/test_delivery_item_names.py` (new) checks every item;
hai-paper-assemble `ref/latex-diff.md` names the diff item. Verified on the served Paper Board after a host restart.

**Never again.** The test fails on any item whose name is not an artifact name, whose shown name differs from its full
name, or on an old generic name written back; the article is rerun by `haistack/scripts/constitution.py --check`.
