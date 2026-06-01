# 4-edit — agents

Subagents the `paper-edit` orchestrator dispatches, one per edit-cycle stage. The
`paper-edit-annotator` is the **fan-out workhorse**: spawn many at once (one per
section, optionally per topic) to annotate a whole draft in parallel. The other
three mutate files and run **sequentially, one section at a time**.

| Stage | Agent | Mutates prose? | Parallel? |
|-------|-------|----------------|-----------|
| (1) format-check | `paper-edit-format-checker` | no (layout only) | no — one file at a time |
| (2) annotate | `paper-edit-annotator` | **no** (comments only) | **yes — fan out** |
| (3) feedback | *(human, in place)* | n/a | n/a |
| (4) improve | `paper-edit-improver` | yes (applies accepted) | no |
| (5) clean | `paper-edit-cleaner` | strips annotations | no |

All agents obey `../_shared/comment-protocol.md`, `../_shared/sentence-format.md`,
`../_shared/paragraph-indexing.md`, and `../_shared/tex-file-anatomy.md`. The
"what to look for" knowledge for each topic lives in the matching
`../paper-edit-<topic>/` sub-skill; the annotator loads it per dispatch.

## Fan-out pattern (stage 2)

```
orchestrator
  ├─ paper-edit-annotator(section=01_introduction, topic=content)   ─┐
  ├─ paper-edit-annotator(section=02-05_trait-rating, topic=content) ├─ run concurrently
  ├─ paper-edit-annotator(section=03-00_overview,    topic=content)  │   (each owns one file,
  └─ ...                                                             ─┘    or returns a comment list)
```

One annotator owns one file → no write conflicts. When several topics target the
same files, prefer **read-only annotators that return comment lists** and let the
orchestrator (single writer) insert them.
