---
name: haipipe-insight-gate
description: "Phase-transition gate of the haipipe-insight family. Runs between phases (D→I, I→K, K→W, W→report) during a session. Proposes one of three outcomes: approve (next phase), revise [feedback] (route back to plan + rewrite), or done (jump to final report). NO code. Use during /haipipe-insight-session, or standalone via /haipipe-insight-gate <phase>. Trigger: gate, review phase, approve, revise, /haipipe-insight-gate."
argument-hint: [phase: D|I|K|W] [--project <path>] [--auto]
allowed-tools: Bash, Read, Write, Edit, Grep, Glob, Skill
---

Skill: haipipe-insight-gate
============================

Phase transition gate. Reviews the artifacts produced during one phase
of a session and proposes the next move:

```
approve   → proceed to next phase (D→I, I→K, K→W, W→report)
revise    → re-plan with feedback; rewrite the plan and restart phase
done      → skip remaining phases, jump to final report
```

The gate's outcome is the ONLY routing vocabulary used by
`/haipipe-insight-session`. Three values, no others.


Input
-----

```
phase                                      D | I | K | W
plan-v{N}-<slug>.yaml                       (current active plan)
insights/D_observations/O*.md               (newly written this phase)
insights/I_patterns/P*.md                   (newly written this phase)
insights/K_knowledge/K*.md                  (newly written this phase)
insights/W_wisdom/W*.md                     (newly written this phase)
```

Read whatever is relevant to the phase being gated.


Output
------

A gate-outcome envelope (returned to caller, typically session orchestrator):

```yaml
gate:        G-D | G-I | G-K | G-W
outcome:     approve | revise | done
feedback:    "<text — empty unless outcome=revise>"
written_at:  <ISO>
```

The session orchestrator routes based on `outcome`:
- approve → next phase
- revise  → call /haipipe-insight-plan --revise N --feedback <text>
- done    → jump to /haipipe-insight-report


Workflow
--------

```
Step 1: Parse args
  - <phase>         D | I | K | W (required)
  - --auto          accept proposed outcome without ASK
  - --feedback      pre-fill revise feedback (used by session for chained revises)

Step 2: Load context
  - Active plan-v{N}.yaml
  - Phase-specific artifacts (D = insights/D_observations/O*.md newly written, etc.)

Step 3: Evaluate phase outcome
  Per-phase checks:
    D:  All planned O entries written? Each cites confirmed experiment?
        No fabricated numbers?
    I:  P entries cite ≥ 2 O entries? Non-confirming evidence engaged?
    K:  K entries cite supporting P + counter-evidence? Confidence justified?
        Supersedes chain coherent if any?
    W:  W entries actionable? Tied to K? Decay condition stated?

Step 4: Propose outcome
  - All checks pass + plan complete       → propose approve
  - Some checks fail OR new info found    → propose revise with feedback
  - Plan over-scoped (question already answered partway)  → propose done

Step 5: Present + ASK (unless --auto)
  Show: phase, checks-passed/-failed, proposed outcome, proposed feedback
  User: accept | override (pick a different outcome) | adjust feedback

Step 6: Emit outcome envelope
```


Per-phase check tables
-----------------------

```
G-D (D-phase gate):
  [ ] all plan.phases.D tasks have a corresponding O*.md
  [ ] every cited number traceable to an experiment.yaml or metrics.json
  [ ] no Python files were written under insights/

G-I (I-phase gate):
  [ ] all plan.phases.I tasks have a P*.md
  [ ] each P cites ≥ 2 O entries
  [ ] non-confirming evidence section non-empty (or "none found" with reason)
  [ ] back-links added to cited O entries

G-K (K-phase gate):
  [ ] all plan.phases.K tasks have a K*.md (new or updated)
  [ ] each K cites ≥ 1 P + counter-evidence section
  [ ] confidence (high/medium/low/contested) justified in body
  [ ] supersedes chain consistent (if any K marked superseded)

G-W (W-phase gate):
  [ ] all plan.phases.W tasks have a W*.md (or "no actionable W found"
      stated with reason)
  [ ] each W is actionable (passes "could I write the command?")
  [ ] tied to ≥ 1 K
  [ ] decay condition ("What would change our mind") populated
```


Proposed-outcome rules
-----------------------

```
all checks pass + plan complete              → propose approve
fewer than 50% checks pass for the phase     → propose revise with
                                                feedback listing failures
question already answered during this phase  → propose done (jump to report)
question seems unanswerable from data         → propose revise with feedback
                                                "scope question or trigger
                                                 new experiment"
```


Disambiguation
---------------

- phase = D but no plan.phases.D tasks defined → REFUSE; ask whether
  to run plan first
- no plan-v{N}.yaml exists → REFUSE; run /haipipe-insight-plan first
- AUTO mode with all-pass → emit approve silently
- AUTO mode with failed checks → emit revise with auto-derived feedback


Risk profile
-------------

READ-ONLY on insights/ artifacts. May write a single line to the active
plan-v{N}.yaml `gate_history:` section (audit trail). Does NOT modify
D/I/K/W entries.


Specialist tail
---------------

```
status:    ok
outcome:   approve | revise | done
feedback:  "<text or empty>"
artifacts: [plan-v{N}.yaml gate_history line appended]
next:      session orchestrator routes based on outcome
```
