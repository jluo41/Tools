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
├── page-types/                     the TEN Page Type variants THIS family owns, each a
│   │                               registered skill loaded on top of `haipipe-page`
│   ├── haipipe-page-for-venue/     QBv<n> · one place a paper goes
│   ├── haipipe-page-for-narrative/ the claims, their order, and the section outline
│   ├── haipipe-page-for-section/   one reader-ordered unit, bound to its venue
│   │                               allocation · INCLUDES appendix units, lettered
│   ├── haipipe-page-for-display/   a unit a person must ACCEPT: figure, table, diagram
│   ├── haipipe-page-for-literature/ evidence, outward route: what is already KNOWN
│   ├── haipipe-page-for-value/     evidence, inward route: what this project HAS and
│   │                               PRODUCES · absorbed resource (JL 260809)
│   │                               ─ one DASH per multi-unit family above ─
│   ├── haipipe-page-for-dash-section/    which unit to work on next
│   ├── haipipe-page-for-dash-value/      binding rule · staleness · inventory
│   ├── haipipe-page-for-dash-display/    the wiring map · reader-order rehearsal
│   └── haipipe-page-for-dash-literature/ the gap contract · topic map
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
so the five variants describing a paper's own artifacts live here while the base
contract and the generic kinds stay in `../board/`. The board keeps
`for-stage` because a stage page is a board mechanism both the paper and
application families instantiate. ⚠️ Moving a variant does not move its installed
symlink: re-run `Tools/install.sh --global` afterwards or the skill stops
resolving.

The numbered S folders are the Paper family grammar. There is no `workers/`
directory anymore (dissolved 2026-08-05, thin-paper phase 2): page logic lives
in `../board/page-phases/`, the LaTeX-side craft lives in the stage folders as
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

## Stage to phase

```text
stage work        -> haipipe-paper (the door): resolve the stage from
                     haipipe-paper/stages/index.yml, load ONE stage.md, ensure
                     the S page exists, hand the page to haipipe-page
draft             -> ../board/page-phases/haipipe-page-draft (page logic)
                     + the stage's declared craft: files (citation · values · display)
probe             -> ../board/page-phases/haipipe-page-probe + probe/haipipe-probe
                     + haipipe-paper/probe/ (the family door's probe tooling)
revise            -> ../board/page-phases/haipipe-page-revise (page logic)
                     + the stage's declared craft: files (revise-place · revise-results)
check             -> ../board/page-phases/haipipe-page-check (page logic)
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
