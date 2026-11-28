This file holds the `health` rows and the other closing checks, moved from `SKILL.md` § ✅ Closing checks (the final gate stays there).

- Before any claim that a Page Folder is current or complete, run
  `cli/page.py health <page-folder>` (several folders in one call are fine).
  It checks that the Folder agrees with itself: one current Outline, records
  in `draft/records/`, the `approved:`/`status:`/`arc:` header, every Bullet
  parseable (an unindented line silently empties a Bullet), each Page
  `realizes:` sentence equal to its Draft, Evidence ids declared and bound
  Result paths present, and delivery newer than the Page. Exit 1 on any FAIL;
  report its WARN rows rather than calling the Folder done. It judges no prose:
  Page CHECK still does that. `draft/evidence/bibex/` is live export output
  (`src/common.py::evidence_lane_dir`) and is not flagged as retired.
- Row `paragraph` (JL 261112): each paragraph holds 4 to 7 sentences, counted
  from its `### C<n>.P<m> · <name> · s<a> to s<b>` heading, else its Bullets.
  WARN while writing, FAIL with `--final`, naming each paragraph id and its
  count; a `reason: <why>` line under the heading accepts it. It runs only for
  a page whose face has `section_kind:` and skips the exempt kinds (abstract,
  summary, appendix and supplement legends, letters, responses, a P0 title).
  Its one reader is `src/paragraph_length.py` (`RANGE`, `EXEMPT`,
  `paragraphs()`, `off_range()`, `section_kind()`), shared with hai-paper
  W7 and hai-draft-review `paragraph-length`.
- Rows `expect` and `title` (JL 261112, from the same module): an
  Introduction's `[Expect]` Bullet whose Evidence line says none ("do we really
  have evidence for this?": ask the question, cite the prior result, leave the
  answer to the Results), and a `[Title]` Bullet that still holds a placeholder
  ("could you put the title here?"). Both WARN, FAIL with `--final`.
- For Page creation or whole-Page completion, apply `ref/page-checklist.md`
  and name unmet, deferred or untested checks; never promote a scaffold,
  a static build or an inferred human approval into completion.
- Every `folder-kind:` and `page-type:` value resolves directly to its owning
  Page or workflow contract; no central registry is consulted.
- Every heading passes `writing-rules.md`'s five lookup-key tests;
  `grep -n '^#\+ .*, '` returns only clauses that state a second rule.
- No section states a rule a cited authority owns (`board-form.md` §4,
  `page-template.md`, `writing-rules.md`, `workbench-task-draft`), except
  where this file adds what a machine may write.
- Every path this file names resolves on disk; each `##` section answers one
  reader question.
