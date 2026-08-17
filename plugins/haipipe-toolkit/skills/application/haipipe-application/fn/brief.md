# `brief` · create or resume the application Brief

1. Resolve the application root and read `board.md`, `STATUS.md`, and the current venue pack when pinned.
2. Find the one `page-type: brief` Page. If absent, create `S-Brief-0-brief` through `haipipe-page` and load `haipipe-page-for-brief`.
3. For a legacy application, read Seed, Venue, and Pitch as compatibility inputs. Fold decisions into the Brief; do not delete or continue writing the old spine.
4. Resolve selected evidence only as settled Task/Insight Pages through PageX. Record absent knowledge as `missing insight`, never as a local Probe.
5. Run the Page lifecycle until the Intervention handoff is accepted or held on named missing insights.

Return the Brief path, venue, selected Insight bindings, missing Insight requests, and next Page phase.
