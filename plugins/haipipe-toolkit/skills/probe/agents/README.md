probe — Agent Roster
======================

The probe layer is a PAPER-LEVEL DOCUMENT plus a set of rules — not a place, and (since
2026-07-14) not a gateway either. **ONE live agent remains.**

```
haipipe-probe-reviewer-agent   🔍 REVIEW — thin Judge SHELL: invokes Skill(haipipe-probe-review)
                                          headless (the governed G1/G2/G3 rulebook) and RETURNS
                                          its judgment as text, never written to files. Runs on
                                          the CONSUMER side (paper OR application), dispatched by
                                          that side's PROBE-phase worker at ⑤ INTERPRET for a
                                          `mode: full` section; the CALLER lands the claim's
                                          status in its own 0-lifecycle/1-claims/1-claims.md.
```

The probe writes NO bank file. Its only files are the paper's own
`papers/<P>/1-probes/PPNN_<topic>.md` probe files. Execution artifacts live in `tasks/` and
`discoveries/`, authored by the executor (haipipe-probe/SKILL.md, R12 + CC-8).


Dispatch — DIRECT, no gateway
-----------------------------

```
📄 the PROBE (in the CONSUMER session — a paper or an application)
   │
   │  ③ DISPATCH — hands the section's `commission` block, VERBATIM
   │               (LAW 1 — nothing else crosses: never `## Why`, never the paper)
   │
   ├──▶ Agent(haipipe-task-orchestrator-agent)        runs / code   ⚙️ probe-UNAWARE
   ├──▶ Agent(haipipe-discovery-orchestrator-agent)   literature    ⚙️ probe-UNAWARE
   │        both run the `qa` gate inside:  ① QA scan  ② digest  ③ P-B-E-R
   │        both return a PATH:  <leaf>/QA/<n>-<slug>.md   ← the EXECUTOR authored it
   │
   │  ⑤ INTERPRET — with the QA file in hand, and only for a `mode: full` section
   │
   └──▶ Agent(haipipe-probe-reviewer-agent)           G1/G2/G3 claim judging
                                                      (consumer-side; reads the QA file, judges
                                                       MY claim, returns TEXT — writes nothing.
                                                       The caller lands it in 1-claims.md.)
```

THEIR CLEAN CONTEXT IS THE WALL. The old gateway was a third clean context standing in front
of two that already had one — a hop that bought nothing and cost a stake leak.


Retired
-------

```
haipipe-probe-orchestrator-agent   🎯 the GATEWAY. RETIRED 2026-07-14 (Tools/plugins/haipipe-toolkit/diagram/260714-probe-qa/ v3,
   → ./_archive/                      CC-6 / JL-13). Its SWEEP became the paper-side MATCH; its
                                      dispatch became a direct Agent() call; its _ASK/ stub is a
                                      spec violation now (the bank is probe-unaware, R2).
                                      De-registered from ~/.claude/agents/ + <repo>/.claude/agents/.
                                      Do NOT re-symlink. See ./_archive/README.md.

haipipe-probe-creator-agent        produced probe.yaml / evidence.md / status.md — none of which
   → ../_archive/_old/                exist in the folderless model.
```

The reviewer also absorbed three earlier Judge agents (merge predates folderless, 2026-06-23):

```
RETIRED                              MERGED INTO
probe-structural-reviewer-agent  →  haipipe-probe-reviewer-agent (G1)
probe-integrity-auditor-agent    →  haipipe-probe-reviewer-agent (G2)
claim-verifier-agent             →  haipipe-probe-reviewer-agent (G3)
```


Knowledge home
--------------

Agents are THIN — every rule lives in its canonical home:

```
the constitution (probe file anatomy, path binding,   → ../haipipe-probe/SKILL.md
the QA/ contract, the qa verb, the two LAWS,             ⭐ START HERE
status derivation, the writer table)
Judge gate logic (G1/G2/G3)          → ../haipipe-probe-review/SKILL.md   (the reviewer calls it headless)
G2 integrity computation             → ../haipipe-probe-review/g2_integrity_check.py   (deterministic)
confound / caveats walk              → ../haipipe-probe-review/probe-caveats-checklist.txt
the qa verb's executor-side flow     → ../../task/haipipe-task/fn/qa.md  ·  the discovery twin
gateway-era + folder-era rationale   → ./_archive/  ·  ../_archive/  (history only)
```


Registration
------------

Real files live here (toolkit source of truth).
`.claude/agents/` holds symlinks so each is callable as a `subagent_type` by the harness.
Anything under `_archive/` is NEVER registered.
