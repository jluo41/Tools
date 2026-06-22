# Paper Skill

Canonical reference for the paper lifecycle. This file fixes the structure;
the `ref/` files carry the detail. If anything elsewhere disagrees with this
file or `ref/`, this file and `ref/` win.

## What the paper skill is

The paper skill is a delivery lifecycle. It owns one manuscript's story, claim
wording, displays, paragraph minimap, and section text. It is TeX-first and
maturity-oriented. It behaves like a claim/evidence contract, the same way a
probe does, not a loose writing folder.

Project-level evidence does not live in the paper. It lives in probes,
discoveries, tasks, and insights. When a paper hits a gap, it records a delivery
need and routes to the relevant evidence worker, then backfills the verdict.
There is no project-level narrative coordination layer; the paper owns its own
story.

## Paper-folder layout

Every paper folder follows this shape. See `ref/paper-lifecycle.md` for the
stage and maturity detail, and `ref/paper-rounds.md` for the rounds detail.

```text
<paper-root>/
├── STATUS.md            current layer, maturity, active round
├── 0-<paper>.tex/.bib   main manuscript shell
├── 0-lifecycle/         TeX-first maturation spine
│   ├── 0-seed/
│   ├── 1-pitch/
│   ├── 2-claims/
│   ├── 3-narrative/
│   ├── 4-display/
│   └── 5-minimap/
├── 0-sections/          manuscript prose .tex files
├── 0-displays/          reusable figure/table units, one folder per display
│   └── displayNN-<slug>/
├── 1-rounds/            dated work rounds (discussion, decisions, todo, applied)
│   ├── latest.md
│   └── vYYMMDD/
├── 1-config.yaml
└── 1-compile.sh
```

The `0-` prefix is source of truth, what the paper IS and how it is told. The
`1-` prefix is process, how the paper is built and revised.

## Skill-tree layout

The skill directory mirrors the lifecycle. See `ref/paper-skill-structure.md`
for the full target organization and the router rule.

```text
paper/
├── haipipe-paper/       router + Paper Console
├── PHILOSOPHY.md        design philosophy
├── README.md            this file
├── ref/                 lifecycle · rounds · lifecycle-map · dashboard · delivery-need · skill-structure
├── 0-enter/             Paper Console (haipipe-paper-enter)
├── 1-lifecycle/         the 6 stage procedures + figure/arch/plan/diagram helpers
├── 2-rounds/            dated work rounds (haipipe-paper-round)
├── 3-write-edit/        write, edit, self-review skills + section playbooks
├── 4-build-submit/      scaffold, restructure, check
├── 5-respond/           rebuttal, response
├── 6-present/           slides, poster
├── _venue/              venue profiles (conference/journal/is) + create/revise
└── components/          citation, compile, diff
```

## References

| File | Read it for |
|---|---|
| `ref/paper-lifecycle.md` | stage spine, maturity ladder, loopback rule, evidence-worker handoff |
| `ref/paper-rounds.md` | `1-rounds/` contract, file semantics, triage targets |
| `ref/paper-skill-structure.md` | skill-tree target, router rule, maturity rule |

## Retired names

These names were removed. Do not reintroduce them.

| Retired | Use instead |
|---|---|
| `1-feedback/` | `1-rounds/` |
| `lifecycle/stageNN_slug/current.md` + per-stage `runs/` `feedback/` `assets/` | `0-lifecycle/<N-stage>/<N-stage>.tex` + `1-rounds/vYYMMDD/` |
| old stage names: `architecture-minimap`, `paper-plan`, `display-contract` | folded into `2-claims`, `3-narrative`, `4-display`, `5-minimap` |
| `0-displays/Figures/<id>/`, `0-displays/Tables/<id>/` buckets | `0-displays/displayNN-<slug>/` units |
| project-level narrative coordination layer | the paper owns its own story; route gaps straight to evidence workers |
