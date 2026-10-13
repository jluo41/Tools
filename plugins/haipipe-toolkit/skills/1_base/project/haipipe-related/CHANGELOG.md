haipipe-related · Changelog
===========================

**[0.2.0] · 2026-10-13 · Groups are kinds; a paper row opens on its PDF**

The Studio's Related bar now reads by what each item is (JL 261013: "this one should [be] things like
meeting, email, paper"): a file sits under its subfolder as before, and a row kept as a web link under
its `kind` instead of Untagged (`frame.py` `related_items`). What a paper bears on (the closest work, the
background, an idea or a research question) moves to a paper Board's `bears on` column, which Audience
Report › Related Papers groups by (`paper_theme.py` `_related_rows`; `group` still works without it).
A paper's PDF is kept when a free copy exists (JL 261013: "we want here to show the pdf attached"): an
open-licensed version anywhere, and in a private repository an arXiv preprint or PMC copy too, each
checked to carry the paper's title. Tests: `test_a_related_item_is_grouped_by_its_kind`,
`test_related_papers_by_bears_on_when_the_table_has_it`.

**[0.1.0] · 2026-10-11 · The Block's related/ gets its own skill**

New, beside haipipe-studio, haipipe-delivery, haipipe-report and haipipe-run (b10 s04-D09; JL
261011: "for the s04, do we need a haipipe-related skill for it?"). It owns the Block's `related/`
folder (meetings/, papers/, files/, and emails/, new the same day: "the related can have /emails as
well"), its table `related/related.md`, its groups (a subfolder is a group of its files, s04-D08)
and the Related view inside the Studio. The rule was spread over b10 s01-D27, s01-D34 and the
paper skills; the workbench's `run-add-related-<slug>` button now names this skill.
