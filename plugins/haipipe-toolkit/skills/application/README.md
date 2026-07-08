# Application Skill

Canonical reference. This file + `wiki/` win over anything elsewhere. Structural twin of `../paper/` (same spine, same phases, same probe door); deltas listed at the bottom.

An intervention is a delivery contract, not a drafting folder. It owns one deliverable's story, claims, displays, and artifact text. Evidence lives in tasks/discoveries/insights at the project level; each stage's `_PROBE/PPNN` card carries contract + receipt + verdict. Claim gaps buffer per-stage and batch-dispatch to probe (the universal evidence gateway; probe calls task/discover during Gather). Direct task/discover for non-claim utility work only.

## Intervention-folder layout

```text
<intervention-root>/
├── STATUS.md                 venue, stages_skipped, Gate Ledger, current layer, maturity
├── 0-lifecycle/              maturation spine (md + _LOG + per-stage _PROBE/)
│   ├── 0-seed/  1-claims/  2-venue/  2-pitch/  3-narrative/  4-display/  5-section-edit/
│   │   (1-claims: Claims/Probes/Campaign + _VALUES_; 2-venue: choice + Artifact Principles)
├── 0-sections/               sectioned-venue prose (report/dashboard-like venues only)
├── 0-artifacts/              deliverables: <slug>-v{N}.md, REVIEW-*, CLAIM_AUDIT.md
├── 1-probe-plans/README.md   cross-stage INDEX of _PROBE/ cards (index only, no bodies)
├── 1-rounds/vYYMMDD/         work rounds (discussion, decisions, todo, applied)
└── data/contract.yaml        input-data contract (when the venue consumes data)
```

`0-` = source of truth (content). `1-` = process (build + revise). Stages 3-5 exist only when the pinned venue requires them.

## Skill-tree layout

```text
application/
├── haipipe-application/   router + Intervention Console front door + stage-strip.sh
├── 0-enter/               Intervention Console (haipipe-application-enter) + haipipe-application-round
├── 1-lifecycle/           stage procedures, one numbered folder per stage
│                          0-seed / 1-claims [venue-FREE] · venue · 2-pitch / 3-narrative / 4-display / 5-section-edit [venue-ALIGNED]
├── 2-phase/               shared phase workers: DRAFT-PROBE-REVISE-CHECK (DPRC)
│                          haipipe-application-{draft,probe,revise,check}
├── 3-build-deploy/        haipipe-application-{artifact,review,claim-audit,deploy}
├── 4-iterate/             post-deploy refinement (A/B results -> refine)
├── _venue/                venue profiles (knowledge, not verbs) — output modality
├── _audience/             audience profiles (knowledge) — tone within structure
└── wiki/                  lifecycle, dashboard, skill-structure, stage-gate, delivery-need
```

## References

| File | Read it for |
|---|---|
| `wiki/03-intervention-lifecycle.md` | stage spine, venue gating, maturity ladder, loopback rule, evidence handoff |
| `wiki/06-application-skill-structure.md` | skill-tree target, router rule, stage-to-procedure map |
| `wiki/08-stage-gate.md` | Gate Ledger protocol, venue-scaled gate depth, exit criteria |
| `wiki/11-delivery-need.md` | application <-> probe/evidence interface |
| `../paper/wiki/00-evidence-principles.md` | the four evidence principles (shared root doctrine) |

## Deltas vs paper (intentional, not drift)

| paper | application |
|---|---|
| venue = journal playbook | venue = output modality (sms/email/dashboard/report/...) + `_audience/` axis |
| all stages always fire; claims always fully settled | venue gates stages 3-5 and sets claims SETTLEMENT depth (light/medium/full) |
| 0-sections/ TeX -> compile -> submit | 0-artifacts/ markdown -> draft(artifact) -> review -> deploy |
| respond (rebuttal) / present | iterate (A/B results -> refine) |
| papers repo-backed inside Project-* repos | interventions are plain in-project folders |

## Retired names

| Retired | Use instead |
|---|---|
| `haipipe-application-ask` (+ SESSION_STATE machinery) | `/haipipe-application enter` console; ad-hoc questions -> `/haipipe-probe "<question>"` |
| `haipipe-application-minimap` (stage 5) | unit jobs live in `4-display` per-unit contracts |
| `haipipe-application-gate` | `2-phase/3-check/haipipe-application-check` (the CHECK phase) |
| `haipipe-application-draft` as artifact generator | `3-build-deploy/haipipe-application-artifact` (verb stays `draft`) |
| spine `seed → pitch → [venue] → claims → ... → minimap` | `seed → claims → [venue] → pitch → narrative → display → section-edit` |
| flat `0-lifecycle/N-stage.md` files | stage FOLDERS `0-lifecycle/N-stage/` (md + _LOG + _PROBE/) |
| `1-probe-plans/PP##_*.md` plan bodies; `/haipipe-probe plan from-need` | per-stage `_PROBE/PPNN_*.md` cards; `1-probe-plans/README.md` = index; `/haipipe-application probe` buffer + `probe run` |
| verdict word `confirmed` | `supported \| refuted \| inconclusive` (PPNN enum) |
| `applications/ask/<NN>/` case files | dead history: nothing reads, nothing writes |
