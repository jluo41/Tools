probe — Agent Roster
======================

The probe layer owns **ONE agent** — `haipipe-probe-q-executor-agent`, a stake-free, family-agnostic
QUESTION-LEVEL collector. Given a batch of q-executors it runs the stake-free middle of the loop
(② MATCH → ③ DISPATCH → ④ POINT) in an isolated context and returns the answered QA paths; the
stake-aware halves (① writing the q-executor, ⑤ harvest) stay with the consumer/stage. A probe is
COMMUNICATION: it maps questions to answers and gets out of the way. It transports evidence; it
does not grade it. (The old gateway + judge agents were retired — see `./_archive/`.)

The probe writes NO bank file. Its only files are the paper's own
`papers/<P>/1-probes/PPNN_<topic>.md` probe files. Execution artifacts live in `tasks/` and
`discoveries/`, authored by the executor (haipipe-probe/SKILL.md, R12 + CC-8).


Dispatch — DIRECT, no gateway
-----------------------------

```
📄 the PROBE (in the CONSUMER session — a paper or an application)
   │
   │  ③ DISPATCH — hands the section's `q-executor` block, VERBATIM
   │               (LAW 1 — nothing else crosses: never `## Why`, never the paper)
   │
   ├──▶ Agent(haipipe-task-orchestrator-agent)        runs / code   ⚙️ probe-UNAWARE
   ├──▶ Agent(haipipe-discovery-orchestrator-agent)   literature    ⚙️ probe-UNAWARE
   │        both run the `qa` gate inside:  ① QA scan  ② digest  ③ P-B-E-R
   │        both return a PATH:  <task-folder>/QA/<n>-<slug>.md   ← the EXECUTOR authored it
   │
   └─ ⑤ INTERPRET — with the QA file in hand, the CONSUMER'S OWN session reads the answer and
      writes the claim's status into its 0-lifecycle/1-claims/1-claims.md. No agent, no gate.
```

THEIR CLEAN CONTEXT IS THE WALL. The old gateway was a third clean context standing in front
of two that already had one — a hop that bought nothing and cost a stake leak.


Knowledge home
--------------

Agents are THIN — every rule lives in its canonical home:

```
the constitution (probe file anatomy, path binding,   → ../haipipe-probe/SKILL.md
the QA/ contract, the qa verb, the two LAWS,             ⭐ START HERE
status derivation, the writer table)
the claim's status + claim_type overclaim check       → ../../<consumer>/1-lifecycle/1-claims/
(authored by the consumer, from the answered QA file)   haipipe-{paper,application}-claims/SKILL.md
the qa verb's executor-side flow     → ../../task/haipipe-task/fn/qa.md  ·  the discovery twin
```


Registration
------------

Real files live here (toolkit source of truth).
`.claude/agents/` holds symlinks so each is callable as a `subagent_type` by the harness.
Anything under `_archive/` is NEVER registered.
