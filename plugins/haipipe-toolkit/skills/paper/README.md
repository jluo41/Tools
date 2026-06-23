# Paper Skill

Canonical reference. This file + `ref/` win over anything elsewhere.

A paper is a delivery contract, not a writing folder. It owns one manuscript's story, claims, displays, minimap, and prose. Evidence lives in probes/tasks/discoveries/insights at the project level. Claim gaps buffer in `1-probe-plans/` and batch-dispatch to probe (the universal evidence gateway; probe calls task/discover during Gather). Direct task/discover for non-claim utility work only.

## Paper-folder layout

```text
<paper-root>/
├── STATUS.md                current layer, maturity, active round
├── 0-<paper>.tex/.bib       main manuscript shell
├── 0-lifecycle/              TeX-first maturation spine
│   ├── 0-seed/  1-pitch/  2-claims/  3-narrative/  4-display/  5-minimap/
├── 0-sections/               manuscript prose .tex
├── 0-displays/displayNN-*/   figure/table units
├── 1-probe-plans/PPNN_*.md   evidence-need buffer -> batch-dispatch to probe
├── 1-rounds/vYYMMDD/         work rounds (discussion, decisions, todo, applied)
├── 1-config.yaml
└── 1-compile.sh
```

`0-` = source of truth (content). `1-` = process (build + revise).

## Skill-tree layout

```text
paper/
├── haipipe-paper/    router + Paper Console
├── 0-enter/          Paper Console (haipipe-paper-enter)
├── 1-lifecycle/      6 stage procedures + display renderers
│                     (-display-table, -display-figure, -display-diagram,
│                      -display-illustration, -display-illustration-gemini)
├── 2-rounds/         work rounds (haipipe-paper-round)
├── 3-write-edit/     write, edit, self-review + section playbooks
├── 4-build-submit/   scaffold, restructure, check
├── 5-respond/        rebuttal, response
├── 6-present/        slides, poster
├── _venue/           venue profiles (knowledge, not verbs) — see _venue/README.md
├── components/       citation, compile, diff
└── ref/              lifecycle, rounds, skill-structure, lifecycle-map
```

## References

| File | Read it for |
|---|---|
| `ref/paper-lifecycle.md` | stage spine, maturity ladder, loopback rule, evidence-worker handoff |
| `ref/paper-rounds.md` | `1-rounds/` contract, file semantics, triage targets |
| `ref/paper-skill-structure.md` | skill-tree target, router rule, maturity rule |
| `ref/lifecycle-map.md` | stage-to-procedure map with reads/writes/calls |

## Retired names

| Retired | Use instead |
|---|---|
| `1-feedback/` | `1-rounds/` |
| `architecture-minimap`, `paper-plan`, `display-contract` | `2-claims`, `3-narrative`, `4-display`, `5-minimap` |
| `0-displays/Figures/` `Tables/` buckets | `0-displays/displayNN-<slug>/` |
| project-level narrative coordination | paper owns its story; gaps route to probe |
| `haipipe-paper-{conference,journal,is}` | `_venue/playbook-<venue>` + lifecycle verbs |
| `haipipe-paper-{create,revise}` | `3-write-edit/haipipe-paper-edit-{write,weaving}` |
