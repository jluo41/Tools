probe/agents/_archive — Tombstone
==================================

Dead agents. Never registered, never dispatched, never resurrected. Kept for history only.


haipipe-probe-orchestrator-agent.md — the EVIDENCE GATEWAY
-----------------------------------------------------------

RETIRED 2026-07-14 (Tools/plugins/haipipe-toolkit/diagram/260714-probe-qa/ v3, rulings CC-6 / JL-13, approved by JL).

```text
   what it did                          where that job went
   ──────────────────────────────────   ────────────────────────────────────────────
   SWEEP the evidence base              → the PAPER-SIDE MATCH (haipipe-probe PART 4 ②):
   (discoveries/ + tasks/)                grep {tasks,discoveries}/**/QA/*.md, in the
                                          consumer's own session. No agent needed for a grep.

   shape: reused | enriched | fresh      → the COST LADDER (R13: T0 JOIN · T1 LOCAL ·
                                          T2 REUSE · T3 ENRICH · T4 FRESH), decided by
                                          the probe; and the qa gate (R11: ① scan ②
                                          digest ③ P-B-E-R), decided by the executor.

   write the _ASK/PPNN stub              → 💀 DEAD. The bank is PROBE-UNAWARE (R2): no
                                          _ASK/, no _ANS/, no PP ids. The `commission`
                                          block inside the probe file's question SECTION
                                          replaces the stub entirely.

   dispatch the execution agents         → a DIRECT Agent() call from the probe:
                                            Agent(haipipe-task-orchestrator-agent)
                                            Agent(haipipe-discovery-orchestrator-agent)
                                          Their clean context IS the wall. The gateway was
                                          a THIRD clean context in front of two that
                                          already had one — a hop that bought nothing.

   dispatch the reviewer (full mode)     → still Agent(haipipe-probe-reviewer-agent), called
                                          from the paper side. ✅ THAT AGENT SURVIVES.
```

Still live, do not confuse with this: `../haipipe-probe-reviewer-agent.md` and the
`../../haipipe-probe-review/` skill — paper-side claim judging (G1/G2/G3). They were never
part of the gateway and were not retired with it.

De-registered from `~/.claude/agents/` and `<repo>/.claude/agents/` at retirement. Do not
re-symlink: the file's instructions describe `_ASK/` stubs, `answers:` returns and PP ids
crossing to the bank — all three are now spec violations (haipipe-probe/SKILL.md PART 9).
