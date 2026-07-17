# 2-phase -- DRAFT-PROBE-REVISE-CHECK (shared across lifecycle stages)

The **phase dimension** of the application skill architecture, mirroring `../../paper/2-phase/`. Phase workers are shared across all lifecycle stages (seed, the 1a-1d evidence ladder: descriptions/themes/claims/advice, pitch, narrative, display, section-edit) and by the artifact composition in `3-deliver/`. Users never invoke phase workers directly -- stage skills drive them.

```
Per-stage lifecycle:  DRAFT 🤖 → PROBE 🤖 → REVISE 🤖 → CHECK 🧑

Status strip:
phase:   draft ✅  │  probe 🔥🚀  │  revise ⬜  │  check ⬜
```

## Structure

```
2-phase/
├── README.md                            ← you are here
├── USAGE.md                             ← recipes, effort dial, phase restart
├── WIRING.md                            ← routing and dispatch
├── 0-draft/haipipe-application-draft        settle stage-doc structure + sentences
├── 1-probe/haipipe-application-probe        the ONLY evidence door: the five-step loop
│                                            ORGANIZE → MATCH → DISPATCH → POINT → INTERPRET
│                                            (thin deltas over the probe constitution; + check-probe-cards.sh, ref/)
├── 2-revise/haipipe-application-revise      venue+audience-quality text pass (single worker)
└── 3-check/haipipe-application-check        human gate: approve/revise/done + Gate Ledger
                                             (persona + attendance machinery; + checks.sh)
```

## Phase automation

- **DRAFT** 🤖: agent + user settle content decisions together
- **PROBE** 🤖: agent-only (dispatch evidence needs aggressively, flag for CHECK, no human gate)
- **REVISE** 🤖: agent-only (change the text directly, leave why-comments, no comment-first)
- **CHECK** 🧑: human + agent (auto-checkers report, human decides; venue-scaled depth -- simple venues confirm inline, complex venues get full CHECK reports; personas stand in only in unattended mode)

## The probe phase (COLLECT from the bank → HARVEST application-side)

Every open question is a SECTION in the flat pool `1-probes/`; its `q-executor` (the stake stripped out) is handed to `Agent(haipipe-probe-q-executor-agent)`, the stake-free collector that runs MATCH → DISPATCH → POINT over the task/discovery bank in clean context. That collector is the ONLY door for evidence. HARVEST is transcription of the pointers the answer landed (JL 2026-07-07 ruling, ported from paper): the harvest hooks never search, grep-discover, or dispatch tasks themselves.

Lanes are venue-scaled, and there are NO sub-worker skills — the lanes are hooks inside the one probe worker:

```
PROBE lanes (fire per pinned venue):
  values    → always                                     → harvest values:  → _VALUES_
  citation  → sectioned venues only                      → harvest sources: → _CITATION_ → 🔍 for CHECK
  display   → only when the venue's artifact has display units → link landed units → _DISPLAY_
```

Every firing lane's obligation is written into the section (`harvest: OWED → accepted`); `check-probe-cards.sh` FAILs an OWED lane or a `state: planned` section at VERIFY and again at the CHECK gate.

Hard boundary: the collector finds, the harvest hooks follow pointers, the human verifies in CHECK. The agent NEVER fabricates numbers, NEVER creates ad-hoc display units, NEVER searches inline during PROBE — "DRAFT may search; PROBE must dispatch".

## Deltas vs paper's 2-phase/

- One REVISE worker (paper splits content/humanizer/weaving/results for tex prose); split later only if application artifacts demand it.
- PROBE has no citation/values/display sub-SKILLS; those are venue-scaled hooks inside the probe worker (values always, citation sectioned venues only, display only with display units).
- CHECK carries the application-only persona + attendance machinery (`3-check/haipipe-application-check/{gate-persona,attendance-modes}.md`).
