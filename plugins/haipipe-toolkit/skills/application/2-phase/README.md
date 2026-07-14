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
├── USAGE.md                             ← recipes, effort dial, phase restart
├── WIRING.md                            ← routing and dispatch
├── 0-draft/haipipe-application-draft        settle stage-doc structure + sentences
├── 1-probe/haipipe-application-probe        the ONLY evidence door: the five-step loop
│                                            ORGANIZE → MATCH → DISPATCH → POINT → INTERPRET
│                                            (+ check-probe-cards.sh, ref/)
├── 2-revise/haipipe-application-revise      venue+audience-quality text pass (single worker)
└── 3-check/haipipe-application-check        human gate: approve/revise/done + Gate Ledger
                                             (persona + attendance machinery; + checks.sh)
```

## Phase automation

- **DRAFT** 🤖: agent + user settle content decisions together
- **PROBE** 🤖: agent-only (dispatch evidence needs aggressively, flag for CHECK, no human gate)
- **REVISE** 🤖: agent-only (change the text directly, leave why-comments, no comment-first)
- **CHECK** 🧑: human + agent (auto-checkers report, human decides; venue-scaled depth -- simple venues confirm inline, complex venues get full CHECK reports; personas stand in only in unattended mode)

## The probe phase (the five-step loop: bind every question to an answer)

A PROBE is an APPLICATION-LEVEL document: `1-probes/PPNN_<topic>.md`, one file per TOPIC, one SECTION per question (`serves` / `target` / `state` / `commission` / `reading`), plus one `## Why` holding the stake — which never leaves the file.

```
DRAFT raises the questions
  ① ORGANIZE   collect them into 1-probes/, grouped by topic; write each commission
  ② MATCH      grep the bank's QA corpus and READ the hits — match ON THE ANSWER, never
               on the topic. MOST QUESTIONS STOP HERE (T2 REUSE): the bank fills
               autonomously from executor sessions, so a commission is the EXCEPTION.
  ③ DISPATCH   only what is missing: the `commission` block, VERBATIM, to
                 Agent(haipipe-task-orchestrator-agent)
                 Agent(haipipe-discovery-orchestrator-agent)
               their clean context IS the wall. 💀 the probe GATEWAY agent is RETIRED.
  ④ POINT      target: → the answering QA file, <leaf>/QA/<n>-<slug>.md
  ⑤ INTERPRET  reading: → the claim's status flips in 1-claims.md → the lanes harvest
```

The bank is PROBE-UNAWARE: no `_ASK/`, no `_ANS/`, no `answers:`, no PP ids under `tasks/` or `discoveries/`. The executor answers plain questions through its own `qa` verb and writes the QA file itself. **The probe CAUSES a QA file; the EXECUTOR authors it.**

Lanes are venue-scaled, and there are NO sub-worker skills — the lanes are hooks inside the one probe worker:

```
PROBE lanes (fire per pinned venue):
  values    → always                                     → harvest value anchors → _VALUES_
  sources   → sectioned venues only                      → harvest source anchors → _CITATION_ → 🔍 for CHECK
  displays  → only when the venue's artifact has display units → link landed units → _DISPLAY_
```

Every firing lane's obligation is written into the SECTION (`harvest: OWED → accepted`); `check-probe-cards.sh` FAILs an OWED lane or a `planned` section at VERIFY and again at the CHECK gate.

Hard boundary — **LAW 1: a consumer session NEVER executes task/discovery work inline.** Dispatch means handing the `commission` block and nothing else; never the `## Why`, never the probe file. The agent NEVER writes under `tasks/` or `discoveries/`, NEVER fabricates numbers, NEVER creates ad-hoc display units, NEVER searches inline during PROBE — "DRAFT may search; PROBE must dispatch".

## Deltas vs paper's 2-phase/

- One REVISE worker (paper splits content/humanizer/weaving/results for tex prose); split later only if application artifacts demand it.
- PROBE has no citation/values/display sub-SKILLS; those are venue-scaled hooks inside the probe worker (values always, citation sectioned venues only, display only with display units).
- CHECK carries the application-only persona + attendance machinery (`3-check/haipipe-application-check/{gate-persona,attendance-modes}.md`).
