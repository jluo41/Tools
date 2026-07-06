probe — Agent Roster
======================

Folderless probe (since 2026-07-05): the probe layer is a PHASE + a GATEWAY, not a place.
Two live agents remain; the creator is retired because there are no probe files to create.

```
haipipe-probe-orchestrator-agent   🎯 GATEWAY — dispatch target for /haipipe-paper + /haipipe-application;
                                              SWEEPs insights/ + discoveries/ + tasks/, decides shape
                                              (reused | enriched | fresh), dispatches execution + the
                                              reviewer, RETURNS anchored takeaways + (full) verdict. Writes nothing.
haipipe-probe-reviewer-agent       🔍 REVIEW  — thin Judge SHELL: invokes Skill(haipipe-probe-review)
                                              headless (the governed G1/G2/G3 rulebook) and RETURNS its
                                              judgment as text, not written to files.
```

The gateway owns no folders; the caller's per-stage `_PROBE/PPNN` card is the single source of truth
for contract + receipt + verdict. Execution artifacts land in `discoveries/` and `tasks/`.

Retired (moved to `../_archive/_old/`)
---------------------------------------

```
haipipe-probe-creator-agent     produced probe.yaml / evidence.md / status.md — none exist under folderless;
                                linking absorbed by the gateway, presentation by the caller's return contract.
```

The reviewer also absorbed three earlier Judge agents (merge predates folderless, 2026-06-23):

```
RETIRED                              MERGED INTO
probe-structural-reviewer-agent  →  haipipe-probe-reviewer-agent (G1)
probe-integrity-auditor-agent    →  haipipe-probe-reviewer-agent (G2)
claim-verifier-agent             →  haipipe-probe-reviewer-agent (G3)
```

Cross-layer dispatch
--------------------

```
/haipipe-paper ──▶ probe-orchestrator (gateway) ──┬──▶ discovery-orchestrator   (external evidence)
                                                  ├──▶ task-orchestrator        (runs / code)
                                                  └──▶ probe-reviewer           (full mode: Skill(haipipe-probe-review) G1/G2/G3)
```

Knowledge home
--------------

Agents are THIN — the judgment logic lives in its canonical home:

```
layer contract + PPNN card anatomy   → ../haipipe-probe/SKILL.md
Judge gate logic (G1/G2/G3)          → ../haipipe-probe-review/SKILL.md   (the reviewer agent calls it headless)
G2 integrity computation             → ../haipipe-probe-review/g2_integrity_check.py   (deterministic)
confound / caveats walk              → ../haipipe-probe-review/probe-caveats-checklist.txt
folder-era rationale (history)       → ../_archive/  (DESIGN, PHILOSOPHY, MENTAL_MODEL, SKILLSET_REVIEW)
```

Registration
------------

Real files live here (toolkit source of truth).
`.claude/agents/` holds copies so each is callable as a `subagent_type` by the harness.
