probe — Archive (folder-era, retired 2026-07-05)
================================================

Everything here is FOLDER-ERA HISTORY, kept for rationale and provenance only.
It describes the retired model where a probe was a PLACE (`probes/<slug>/` folders
with probe.yaml / evidence.md / verdict.md / deposit.md) driven by a Probe Console.

The LIVE contract is folderless:
- `../haipipe-probe/SKILL.md`        the layer contract + PPNN card anatomy
- `../agents/haipipe-probe-orchestrator-agent.md`   the evidence gateway
- `../agents/haipipe-probe-reviewer-agent.md`       the full-mode Judge

Do not treat anything below as current. A probe now = a PHASE (each stage's PROBE step)
plus a GATEWAY agent; the consumer's per-stage `_PROBE/PPNN` card is the single source of truth.

Contents and where each came from
---------------------------------

```
DESIGN.md                     was probe/DESIGN.md            folder-era design/rationale (its Authority block
                                                            pointed at the now-deleted ref/ + fn/)
PHILOSOPHY.md                 was probe/PHILOSOPHY.md        folder-era core position (Console + Lifecycle Map)
MENTAL_MODEL.md               was probe/MENTAL_MODEL.md      folder-era intuition doc
SKILLSET_REVIEW.md            was probe/SKILLSET_REVIEW.md   the diagnosis-of-record that motivated going folderless
CODE_REVIEW.md                was probe/agents/CODE_REVIEW.md   one-time 2026-06-23 review of the old agents
03-probe-aware-entrypoint.txt was probe/haipipe-probe/diagram/  folder-era sketch (minimap / arms / Return vocab)
_old/                         was probe/agents/_old/         4 retired agents: creator + the 3 pre-merge Judge reviewers
agents-feedback/              was probe/agents/feedback/     2026-06-23 orchestrator-failure post-mortems (Codex-era)
skill-feedback/               was probe/haipipe-probe/feedback/  2026-06-22/23 folder-era lessons (Return, Gather-phase,
                                                            probe-id letters, dashboard, atomic-vs-comparison)
```

Note: two lessons in `skill-feedback/` are arguably not probe's (`venue-editor-chair-test` reads paper-side;
`task-scripts-missing-conventions` reads task-side). Left here as history; re-home if either is still needed live.
