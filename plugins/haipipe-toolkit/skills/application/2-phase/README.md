# 2-phase -- DRAFT-PROBE-REVISE-CHECK (shared across lifecycle stages)

The **phase dimension** of the application skill architecture, mirroring `../../paper/2-phase/`. Phase workers are shared across all lifecycle stages (seed, claims, pitch, narrative, display, section-edit) and by the artifact composition in `3-build-deploy/`. Users never invoke phase workers directly -- stage skills drive them.

```
Per-stage lifecycle:  DRAFT 🤖 → PROBE 🤖 → REVISE 🤖 → CHECK 🧑

Status strip:
phase:   draft ✅  │  probe 🔥🚀  │  revise ⬜  │  check ⬜
```

## Structure

```
2-phase/
├── README.md                            ← you are here
├── 0-draft/haipipe-application-draft        settle stage-doc structure + sentences
├── 1-probe/haipipe-application-probe        the ONLY evidence door: BOOKKEEP → DISPATCH
│                                            (Agent(haipipe-probe-orchestrator-agent)) → TRANSLATE
├── 2-revise/haipipe-application-revise      venue+audience-quality text pass (single worker)
└── 3-check/haipipe-application-check        human gate: approve/revise/done + Gate Ledger
                                             (persona + attendance machinery; ex-gate skill)
```

## Phase automation

- **DRAFT** 🤖: agent + user settle content decisions together
- **PROBE** 🤖: agent-only (dispatch evidence needs aggressively, flag for CHECK, no human gate)
- **REVISE** 🤖: agent-only (change the text directly, leave why-comments, no comment-first)
- **CHECK** 🧑: human + agent (auto-checkers report, human decides; venue-scaled depth -- simple venues confirm inline, complex venues get full CHECK reports; personas stand in only in unattended mode)

## Deltas vs paper's 2-phase/

- One REVISE worker (paper splits content/humanizer/weaving/results for tex prose); split later only if application artifacts demand it.
- PROBE has no citation/values/display sub-SKILLS; those are venue-scaled hooks inside the probe worker (sectioned venues only).
- CHECK carries the application-only persona + attendance machinery (`3-check/haipipe-application-check/{gate-persona,attendance-modes}.md`).
