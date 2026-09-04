# writing

The prose layer: realizing an approved outline/evidence packet as prose, or
rewriting what someone already wrote so a reader whose English is weak can
follow it, and leaving a word-level record of every edit under the sentence it
changed.

```
writing/
├── haipipe-writing/                 the worker: realize/rewrite → record → check
└── haipipe-paper-revise-humanizer/  the academic-venue dialect (moved here from paper/, 260805)
```

**Why a bucket of its own.** Every other family owns a KIND of artifact: `paper`
owns manuscripts, `board` owns pages, `application` owns reports. This one owns
the prose realization layer, not the plan or evidence authority. Its consumer
is prose in any host, and its test does not care what file the prose is in.

When a host already has an approved outline and evidence, read
`haipipe-writing/ref/realize-from-plan.md`. The host keeps ownership of the
outline, claims, and evidence; this worker turns one bounded plan slice into
reviewable prose and applies the shared change-record contract.

**The paper-facing dialect.** `haipipe-paper-revise-humanizer` (in this bucket
since 260805) rewrites academic
prose for a venue and writes `%%` comments into LaTeX. Different reader,
different host, same machinery. It should become a consumer of
`haipipe-writing/cli/wdiff.py` rather than grow a second copy of it; until then
the two dialects are written down together in `ref/change-record.md` §3.
