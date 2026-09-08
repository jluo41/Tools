# Discovery Page Types

A Discovery Page Type is the article form of one Level-3 Discovery `tNN_` Task
Page. It is a domain field in `discovery.yaml`, not a Board `page-type:` key,
not a Folder level, and not a Run family.

```text
one Job inquiry -> one or more typed Task Pages
one Task question -> one tNN_ Page Folder -> one discovery_type
one admitted evidence Subject -> one rNN_ Paper/Source Run
```

All seven canonical forms are live Discovery surface. Search finds candidate
Subjects, Review inspects one admitted source at a time, and Synthesize
combines accepted Results into a topic article. Semantic direction and idea
work is owned by the separate `haipipe-ideation` skill, not by a Discovery Page
Type. The numbered layout and its BJTR retrofit are defined in
`bjtr-alignment.md`.

Changing the article form does not change what earns a Run. Search queries,
candidate lists, synthesis passes, outline revisions, and direction generation are
Page workflow. A selected canonical paper/source becomes a Run only when the
Topic commissions a durable analysis of that Subject.

## Canonical types

| `discovery_type` | Specialist | Reader promise | Typed Task-side record | Evidence Run policy |
|---|---|---|---|---|
| `source-map` | Search | show what relevant sources exist and the coverage boundary | none | one Run per admitted source |
| `source-reading` | Review | explain what one selected source says and what it supports | none | one Run per analyzed source |
| `topic-summary` | Synthesize | synthesize what is known about one bounded topic | optional `summary.md` | one Run per cited source |
| `prior-art-verdict` | Synthesize | decide whether a named claim already exists | optional `verdict.md` | one Run per closest-prior-work source |
| `counterevidence-review` | Synthesize | preserve and weigh evidence against a named claim | optional `verdict.md` | one Run per admitted counter/source |
| `landscape-review` | Synthesize | map approaches, clusters, disagreements, and gaps | optional `landscape.md` | one Run per cited source |
| `benchmark-landscape` | Synthesize | compare datasets, tasks, metrics, and evaluation setups | optional `landscape.md` | one Run per cited benchmark/source |

The root `<task-folder-name>.md` is always the human-facing article. A typed record is a
compact Task-side synthesis receipt used by the specialist and may be absent
when the Page itself is sufficient. It never replaces the Page and is never a
Level-4 Result.

## Permitted normalization

Existing manifests may use a permitted old `type` + `role` pair. Normalize it
to the canonical field without rewriting the article automatically:

| legacy `type` / `role` | canonical `discovery_type` |
|---|---|
| `Search / source_gather` | `source-map` |
| `Search / source_read` or `search_and_read` | `source-reading` |
| `Review / topic_summary` | `topic-summary` |
| `Review / prior_art_check` | `prior-art-verdict` |
| `Review / counterevidence` | `counterevidence-review` |
| `Review / landscape_review` | `landscape-review` |
| `Review / benchmark_landscape` | `benchmark-landscape` |

New manifests write only `discovery_type`. Specialists derive their route from
the table above. A manifest that carries both forms must normalize to the same
type or the Topic is invalid.

## Page Face contract

The Page keeps the shared `haipipe-page` frame: Opening, optional Diagram,
Content, and Aims. Its Content makes four promises, with headings chosen for the
subject rather than copied mechanically:

The root Page writes `folder-kind: discovery`. It does not write
`page-type: task`: Discovery owns both Folder faces, while the empirical
technical-report grammar belongs only to `folder-kind: task`.

1. **Question and boundary**: define the Topic, population/time/venue boundary,
   channels searched, and admission rule.
2. **Type payload**: source map, source reading, summary, verdict, landscape,
   or benchmark guide.
3. **Evidence map**: link every factual support to completed Result Cards and
   exact cite keys; preserve disagreement and unresolved evidence.
4. **Limits and next move**: state what the Page does not establish and whether
   the honest route is gather, revise, extend, hold, or close.

The Page synthesizes Results many-to-many. It may quote or compress them, but
must not become a pasted `notes.md` ledger or imply one paper per paragraph.
`Aims` judge whether the article keeps its reader promise; Paper Run status is
derived separately from runtime receipts.

## Type changes

Change `discovery_type` in place only when the Topic question and evidence
population stay the same and the Page is still before CLOSE. After CLOSE, a
materially different reader promise opens a new `tNN_` Task Page and may reuse
completed Results by global Run reference. Never relabel a completed verdict as
a landscape Page merely to avoid a new address.
