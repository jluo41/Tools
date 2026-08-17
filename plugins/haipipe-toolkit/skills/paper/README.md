# Paper skill family

`haipipe-paper` turns a research argument into a paper delivery. It owns the
story, claims, display decisions, prose, and submission artifacts. It does not
run analysis or search evidence directly.

## Canonical skill structure

```text
paper/
├── haipipe-paper/                  THE one door, and the family's only registered VERB:
│   ├── stages/                     index.yml + CONTRACT.md + section-kinds.yml
│   ├── probe/                      family probe tooling (check-probe-cards.sh,
│   │                               check_topic_entries.py, topic-entry-contract.md,
│   │                               per-stage-dispatch.md)
│   ├── ref/                        cross-stage references (stage gate, folder anatomy,
│   │                               prose quality, comment protocol, enter console,
│   │                               diffpdf/ class presets + known bugs, …)
│   ├── fn/                         internal verb procedures: probes · feedback · digest ·
│   │                               folder · conform · compile · diffpdf · project ·
│   │                               to-overleaf · to-word
│   ├── scripts/                    verb tooling: check_structure.sh · diffpdf/ ·
│   │                               project/ · to-word/
│   └── create-page.py              the public S-page creator (+ check-contracts.py)
├── page-types/                     the FIVE live Page Type variants this family owns;
│   │                               each loads on top of `haipipe-page`
│   ├── haipipe-page-for-opening/   one per paper · identity, RQ, source Pages,
│   │                               venue position, editor promise, Narrative handoff
│   ├── haipipe-page-for-venue/     QBv<n> · one reusable venue knowledge page
│   ├── haipipe-page-for-narrative/ one per paper · claim roles, reader journey,
│   │                               Section map, PageX source allocation
│   ├── haipipe-page-for-section/   one reader-ordered unit executing one Narrative row
│   ├── haipipe-page-for-dash/      regenerated rollup; `dash_family:` selects family
│   └── _archive/                   retired display, literature, value, and four
│                                   per-family dash contracts; readable, not installed
├── S01-opening/                    seed, venue, pitch (stage.md + template.md each)
├── S02-work/                       resource, claims, narrative
├── S03-literature/                 runtime store for discovery-backed topic entries
│                                   + citation-craft.md (DRAFT citation lane)
├── S04-value/                      runtime store for task-backed topic entries
│                                   + values-craft.md (DRAFT values lane)
├── S05-display/                    display stage + draft-craft.md (DRAFT display lane)
├── S06-main/                       section-edit stage + revise-place-craft.md ·
│                                   revise-results-craft.md · check-evidence-craft.md
├── S07-appendix/                   appendix material
├── S08-present/                    empty; paper-slides and paper-poster live in ../display/skills/
├── S09-build/                      the proof-checker/ craft pack (build verbs live in the
│                                   door's fn/ + scripts/)
├── S10-round/                      round stage (round/stage.md + template.md) +
│                                   rebuttal-craft.md
├── _old/                           retired skills, moved never deleted (see _old/README.md)
└── venue/                          venue knowledge packs
```

**`page-types/` is this family's own, and that is the rule (JL 260809).** A Page
Type variant ships under the `page-types/` folder of the skill set that OWNS it,
so the five live variants describing a paper's own artifacts live here while the base
contract and the generic kinds stay in `../board/`. The board keeps
`for-stage` because a stage page is a board mechanism both the paper and
application families instantiate. ⚠️ Moving a variant does not move its installed
symlink: re-run `Tools/install.sh --global` afterwards or the skill stops
resolving.

The numbered S folders are the Paper family grammar. There is no `workers/`
directory anymore (dissolved 2026-08-05, thin-paper phase 2): page logic lives
in `../board/page-workflows/`, the LaTeX-side craft lives in the stage folders as
`*-craft.md` data files each `stage.md` declares under `craft:`, and the probe
tooling lives in the door's `probe/` folder. Thin-paper phase 3 (2026-08-06)
collapsed the remaining registered skills into the door: folder/conform and the
five build verbs became `fn/` procedures with tooling under `scripts/`, and
round/rebuttal became the `round` stage's data under `S10-round/`.

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
direct S evidence page: canonical E<n> divisions (one per Q-executor) and paper interpretation
nested probes/ entry: one Q-executor, consumer trace, bank binding, and answer
```

There is no live top-level `1-probes/`; legacy probe material belongs only in
`0-lifecycle/_archive/1-probes/`.

The target paper-control flow is:

```text
Opening ── accepted handoff ──▶ Narrative ── one row each ──▶ Section pages
   ▲                                  ▲
   └──── existing Pages via PageX ────┘

Task / Discovery folders ── Probe ──▶ their owning evidence Pages
```

PageX and Probe are parallel in this design. PageX reads existing Pages; Probe
reaches Task and Discovery folders. Opening and Narrative therefore use
`pagex/` rather than owning local evidence discovery. Legacy Seed, Venue,
Pitch, and Claims runtime pages remain compatibility inputs until a separate
migration is run.

## Stage to phase

```text
stage work        -> haipipe-paper (the door): resolve the stage from
                     haipipe-paper/stages/index.yml, load ONE stage.md, ensure
                     the S page exists, hand the page to haipipe-page
draft             -> ../board/page-workflows/haipipe-page-draft (page logic)
                     + the stage's declared craft: files (citation · values · display)
probe             -> ../board/page-workflows/haipipe-page-evidence + probe/haipipe-probe
                     + haipipe-paper/probe/ (the family door's probe tooling)
revise            -> ../board/page-workflows/haipipe-page-revise (page logic)
                     + the stage's declared craft: files (revise-place · revise-results)
check             -> ../board/page-workflows/haipipe-page-check (page logic)
                     + the stage.md's checker: script; pre-submission adds
                     check-evidence-craft.md, and proofs add S09-build/proof-checker/
build and deliver -> the door's fn/ verbs (compile · diffpdf · project ·
                     to-overleaf · to-word), tooling under haipipe-paper/scripts/
review round      -> the round stage (S10-round/round/ + rebuttal-craft.md)
```

Stage contracts live beside their named S01, S02, S05, S06, and S10 stage
folders. `haipipe-paper/stages/index.yml` resolves the nine current user-facing
stages; S03 and S04 are their shared runtime evidence stores.

See `haipipe-paper/fn/probes.md` for the delivery-to-engine contract and
`haipipe-paper/probe/topic-entry-contract.md` for validation rules.
