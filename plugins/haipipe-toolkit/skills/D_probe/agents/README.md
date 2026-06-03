D_probe — Agent Roster
======================

D_probe agent-ifies its JUDGMENTS and its ADVANCER, but **not its builders** —
a deliberate departure from C_task. Read the asymmetry note first; it's the
whole point of applying the pattern *thoughtfully* instead of copying it.

Why no `creators/` here (unlike C_task)
---------------------------------------

```
C_task builders  →  became agents   because authoring code is BATCHABLE
                                     (spec → produce → review) and fans out
                                     per task TYPE.
D_probe builders →  STAY skills      because designing a probe is INTERACTIVE
                                     and deliberate — hypothesis, arms, and
                                     claim_target need human steering — and
                                     there is no "type" axis to fan out
                                     (one probe.yaml shape). Probe volume is
                                     low; the parallelism is DOWNSTREAM: the
                                     bridge fans arms into C_task, which fans
                                     out there.
```

So the builders remain interactive skills:

```
haipipe-probe-design   writes probe.yaml (hypothesis + arms plan)   ← interactive, you steer
haipipe-probe-result   aggregates metrics → result block + claim     ← interactive / light
haipipe-probe-bridge   materializes arms into C_task                 ← orchestration
```

What DID become agents
-----------------------

```
reviewers/   independent judgments (builder ≠ judge; dispatchable; Codex-backed where noted)
advancers/   the third role C_task doesn't have — proposes research direction
```

reviewers/ (3 — gate a probe before its claim ships)
----------------------------------------------------

| Agent | Gate | Reviewer | Sole deliverable | Does NOT do (→ who) |
|-------|------|----------|------------------|---------------------|
| `probe-structural-reviewer-agent` | structural | self (checklist) | `review.md` | per-run (→C_task auditor); fraud (→integrity); claim (→verifier) |
| `probe-integrity-auditor-agent`   | integrity  | **Codex** (out-of-family) | `INTEGRITY_AUDIT.md` | structural; claim |
| `claim-verifier-agent`            | claim      | **Codex** (out-of-family) | `CLAIMS_FROM_RESULTS.md` | author the claim (→result skill); structural; integrity |

Order: structural → integrity → claim. `integrity = fail` blocks `claim`.
Integrity & claim are Codex-backed — the probe's builder never judges its own
work (the executor passes only file paths; Codex reads and rules).

advancers/ (1 — D's unique third family)
----------------------------------------

| Agent | Step | Sole deliverable | Does NOT do (→ who) |
|-------|------|------------------|---------------------|
| `probe-explorer-agent` | coverage + propose next | ranked next-probe list + coverage map | write probe.yaml (→design skill); judge claims (→reviewers) |

Three families, one axis each
-----------------------------

```
builder   (skills, not agents — interactive)   design · result · bridge
reviewer  agents JUDGE                          structural · integrity · claim
advancer  agents PROPOSE direction              explore
```

Knowledge home
--------------

Agents are THIN pointers — the judgment logic stays in its canonical home and
is NOT duplicated here:
- per-probe checklist + caveats + Codex prompts → `../haipipe-probe-review/SKILL.md`
- confound walk → `../ref/probe-caveats-checklist.txt`
- probe.yaml schema → `../ref/probe-yaml-schema.md`
- coverage/propose logic → `../haipipe-probe-explore/SKILL.md`

Registration & invocation
--------------------------

Real files live here; the plugin top-level `agents/` holds flat symlinks so
each is callable as a `subagent_type` (used by `haipipe-probe-loop` and by
`G_application` when a session needs an independent verdict). Like C_task, the
nested folders are for humans; the top-level symlinks are for the harness.
