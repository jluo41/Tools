# Paper Skill

Canonical reference. This file + `wiki/` win over anything elsewhere.

A paper is a delivery contract, not a writing folder. It owns one manuscript's story, claims, displays, minimap, and prose. Evidence lives in tasks/ and discoveries/ at the project level; the paper's `1-probes/PPNN_<topic>.md` probe files hold its QUESTIONS, one SECTION each, and BIND each one BY PATH to the answering `<task-folder>/QA/<n>-<slug>.md` in that bank. Claim gaps become sections there; MATCH closes most of them for free, and only the rest are dispatched (the `commission:` block, verbatim) to the task/discovery orchestrators. The paper reaches the bank only through a stage's PROBE phase; a standalone utility question uses the bank's own `/haipipe-task qa` door, typed by a human.

## Paper-folder layout

```text
<paper-root>/
├── STATUS.md                current layer, maturity, active round
├── 0-<paper>.tex/.bib       main manuscript shell
├── 0-lifecycle/              maturation spine (md + _LOG; display = tex + pdf)
│   ├── 0-seed/  1-resource/  1-claims/  2-pitch/  3-narrative/  4-display/  5-editing/
├── 0-sections/               manuscript prose .tex
├── 0-displays/displayNN-*/   figure/table units
├── 1-probes/PPNN_<topic>.md   the paper's questions, one SECTION each -> bound BY PATH to a QA file
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
├── 1-lifecycle/      stage procedures (seed, claims, pitch, narrative, display)
│                     + display renderers (-table, -figure, -diagram, -illustration)
├── 2-phase/          shared phase workers: DRAFT-PROBE-REVISE-CHECK (DPRC)
│                     haipipe-paper-{draft,probe,revise,checker} + sub-workers
├── 3-build-submit/   scaffold, restructure, check, compile, edit family
├── 4-respond/        rebuttal, response
├── 5-present/        slides, poster
├── _venue/           venue profiles (knowledge, not verbs) — see _venue/README.md
└── wiki/             lifecycle, rounds, skill-structure, lifecycle-map
```

## References

| File | Read it for |
|---|---|
| `wiki/03-paper-lifecycle.md` | stage spine, maturity ladder, loopback rule, evidence-worker handoff |
| `wiki/07-paper-rounds.md` | `1-rounds/` contract, file semantics, triage targets |
| `wiki/06-paper-skill-structure.md` | skill-tree target, router rule, maturity rule |
| `wiki/04-lifecycle-map.md` | stage-to-procedure map with reads/writes/calls |

## Retired names

| Retired | Use instead |
|---|---|
| `1-feedback/` | `1-rounds/` |
| `architecture-minimap`, `paper-plan`, `display-contract` | `2-claims`, `3-narrative`, `4-display`, `5-minimap` |
| `0-displays/Figures/` `Tables/` buckets | `0-displays/displayNN-<slug>/` |
| project-level narrative coordination | paper owns its story; gaps route to probe |
| `haipipe-paper-{conference,journal,is}` | `_venue/playbook-<venue>` + lifecycle verbs |
| `haipipe-paper-{create,revise}` | `3-write-edit/haipipe-paper-edit-{write,weaving}` |
