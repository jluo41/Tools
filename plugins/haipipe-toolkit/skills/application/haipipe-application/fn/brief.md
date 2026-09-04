# `brief` · create or resume the Application Brief

1. Resolve the Application root and read `board.md`, current Pages, and venue packs.
2. Find the D0 Folder (`folder-kind: brief`; legacy `page-type: brief` remains readable). If absent, create `<DesignTopic>-DesignBoard/0-BR-brief/BR00-brief/BR00-brief.md` through `haipipe-folder` + `haipipe-page` and load `haipipe-design-brief`.
3. Fold legacy Seed, Venue, and Pitch decisions as compatibility inputs without deleting or extending the old spine.
4. Define opportunity, audience set, behavior/outcome, venue scope, promise, and the insight needs this board raises, each with a stable id.
5. Bind already accepted core Pages through PageX; release unsettled rows to the matching MT question register (the `question` verb) rather than probing from Brief.
6. Write the initial Design Page roster, one row per audience × behavior job × primary venue. The InsightBoard's Meta Page rosters which Insight Page took each raised need.
7. Run the Page workflow until GD0 closes the Brief or holds on named needs.

Return the Brief path, raised need ids, core PageX bindings, Design roster, and next Page phase.
