2-phase — wiring (application)
===============================

How the `haipipe` plugin discovers and exposes the application phase workers, and how they get invoked at runtime (thin mirror of `../../paper/2-phase/WIRING.md`).

Discovery model (convention-based)
-----------------------------------

Same plugin conventions as paper: `.claude-plugin/plugin.json` lists nothing explicitly — skills auto-discover from `skills/**/SKILL.md` with a `name:` frontmatter and are invoked by name via the Skill tool. Skills created or renamed mid-session are not hot-loaded; they appear after the next Claude Code reload.

What registers from 2-phase/
-----------------------------

One worker per phase folder — no hub/sub-worker split (paper's citation/values/display sub-skills are venue-scaled hooks INSIDE the probe worker here):

| Folder | Worker | Rides along (not registered) |
|--------|--------|------------------------------|
| `0-draft/` | `haipipe-application-draft` | — |
| `1-probe/` | `haipipe-application-probe` | `check-probe-cards.sh` (VERIFY + gate checker), `ref/` (per-stage dispatch, harvest acceptance) |
| `2-revise/` | `haipipe-application-revise` | — (single worker; no content/humanizer/results split) |
| `3-check/` | `haipipe-application-check` | `checks.sh` (markdown-safe deterministic checks), `gate-persona.md`, `attendance-modes.md` |

Dispatch chain (who calls whom)
--------------------------------

**Phase workers are internal, called by stage skills via the Skill tool; they are not user entry points.**

```
user → /haipipe-application <stage>            stage skills live in 1-lifecycle/
        (seed | claims | venue | pitch | narrative° | display° | section-edit°)    ° = venue-gated
             │
             ▼  the stage skill drives the phase engine, in order:
       haipipe-application-draft    → drafts the stage doc from the stage's template (may WebSearch; buffers planned PPNN skeletons)
       haipipe-application-probe    → BOOKKEEP → DISPATCH (Agent(haipipe-probe-orchestrator-agent) per card) → TRANSLATE → VERIFY (check-probe-cards.sh)
       haipipe-application-revise   → venue+audience text pass
       haipipe-application-check    → re-runs the card checker + runs checks.sh, seeds > CHECK: threads in stage docs, gates the human (CHECK 🧑)
```

DRAFT/PROBE/REVISE run automatic; CHECK is the only human gate (venue-scaled depth, `../wiki/08-stage-gate.md`). The probe worker is the ONLY exit for evidence work; stage skills never call `/haipipe-probe`, discovery agents, or task agents directly.

Related, but not in 2-phase/
-----------------------------

- Artifact composition, review, claim-audit, and deploy live in `3-build-deploy/`; post-deploy A/B refinement in `4-iterate/` — same discovery convention, different scope.
- The section-edit stage hub is `1-lifecycle/5-section-edit/haipipe-application-section-edit/`; its per-intervention working files land in the intervention's `0-lifecycle/5-section-edit/`.
- The venue pin (`1-lifecycle/haipipe-application-venue`) writes `0-lifecycle/2-venue/2-venue.md` plus the STATUS.md venue rows that scale probe lanes and gate depth for every phase worker.
