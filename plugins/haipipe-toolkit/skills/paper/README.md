# Paper skill family

`haipipe-paper` turns a research argument into a paper delivery. It owns the
story, claims, display decisions, prose, and submission artifacts. It does not
run analysis or search evidence directly.

## Canonical skill structure

```text
paper/
├── haipipe-paper/                  public router and paper-wide conventions
├── S01-opening/                    seed, venue, pitch
├── S02-work/                       resource, claims, narrative
├── S03-literature/                 runtime store for discovery-backed topic entries
├── S04-value/                      runtime store for task-backed topic entries
├── S05-display/                    reader-facing displays
├── S06-main/                       main manuscript sections
├── S07-appendix/                   appendix material
├── S08-present/                    empty; paper-slides and paper-poster live in ../display/skills/
├── S09-build/                      compile and delivery
├── S10-round/                      review and response rounds
├── container/                      folder and conformance (scaffold, restructure retired to _old/container-merged/)
├── workers/                        flat LaTeX-side phase workers (page logic lives in ../board/page-phases/)
├── _old/                           retired skills, moved never deleted (see _old/README.md)
└── venue/                          venue knowledge packs
```

The numbered S folders are the Paper family grammar. `workers/` and
`container/` are capability groupings, not a second lifecycle.

## Runtime paper structure

```text
<paper-root>/
├── 0-lifecycle/
│   ├── S01-opening/ … S10-round/   paper state as Board S pages
│   ├── S03-literature/             direct topic pages + nested discovery entries
│   └── S04-value/                  direct topic pages + nested task entries
├── sections/                        generated manuscript prose
├── appendices/                      generated appendix prose
├── displays/                        the only home of visual assets
└── 2-src/compile.sh                 build entrypoint
```

S03 and S04 use the same topic-entry grammar:

```text
direct S topic page:  canonical Q-consumer register and paper interpretation
nested probes/ entry: one Q-executor, consumer trace, bank binding, and answer
```

There is no live top-level `1-probes/`; legacy probe material belongs only in
`0-lifecycle/_archive/1-probes/`.

## Stage to worker

```text
stage work        -> haipipe-paper-stage
draft             -> ../board/page-phases/haipipe-board-page-draft (page logic)
                     + workers/haipipe-paper-draft-citation · -draft-values · -draft-display
probe             -> workers/haipipe-paper-probe
revise            -> ../board/page-phases/haipipe-board-page-revise (page logic)
                     + workers/haipipe-paper-revise-place · -revise-results
check             -> ../board/page-phases/haipipe-board-page-check (page logic)
                     + workers/haipipe-paper-check-evidence · -proof-checker
build and deliver -> S09-build/
review round      -> S10-round/
```

Stage contracts live beside their named S01, S02, S05, and S06 workers.
`haipipe-paper-stage/stages/index.yml` resolves the eight current
user-facing stages; S03 and S04 are their shared runtime evidence stores.

See `haipipe-paper/fn/probes.md` for the delivery-to-engine contract and
`workers/haipipe-paper-probe/ref/topic-entry-contract.md` for validation
rules.
