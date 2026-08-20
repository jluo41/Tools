probe — Agent Roster
======================

The probe layer owns **ONE agent** — `haipipe-probe-q-executor-agent`, a stake-free, family-agnostic
QUESTION-LEVEL collector. Given a batch of q-executors it runs the stake-free middle of the loop
(② MATCH → ③ DISPATCH → ④ POINT) in an isolated context and returns the answered QA paths; the
stake-aware halves (① writing the q-executor + T1 LOCAL, ⑤ harvest) stay with the consumer/stage.
A probe is COMMUNICATION: it maps questions to answers and gets out of the way. It transports
evidence; it does not grade it.

The agent writes no bank file and handles only the Task/Discovery QA branch of
the Probe family. A Board Page owns its local `probe/PP<NN>-<slug>/` card;
Task/Discovery owns the answering `QA/<n>-<slug>.md`. The sibling PageX branch
uses `pagex/` during OUTLINE and never reaches this agent.


Dispatch — the collector, then direct to the executors
-------------------------------------------------------

```
📄 the CONSUMER PAGE
   │  ① ORGANIZE (writes the q-executors) · T1 LOCAL (matches its OWN registries first)
   │
   │  hands the STILL-COLLECTING q-executors (state: planned/commissioned), VERBATIM
   │  (LAW 1 — nothing else crosses: never `## Why`, never the stake)
   ▼
🧭 Agent(haipipe-probe-q-executor-agent)   the COLLECTOR — ONE isolated context
   │  ② MATCH the bank (reuse + dedup)  ·  ④ POINT each section's target:
   │  ③ DISPATCH the MISSES only, VERBATIM:
   ├──▶ Agent(haipipe-task-orchestrator-agent)        runs / code   ⚙️ probe-UNAWARE
   ├──▶ Agent(haipipe-discovery-orchestrator-agent)   literature    ⚙️ probe-UNAWARE
   │        both run the `qa` gate inside:  ① QA scan  ② digest  ③ P-B-E-R
   │        both return a PATH:  <task-folder>/QA/<n>-<slug>.md   ← the EXECUTOR authored it
   ▼
📄 the CONSUMER PAGE again — ⑤ INTERPRET: reads each answered QA file,
   records the Page-specific meaning, and returns to OUTLINE. No collector gate.
```

A COLLECTOR, but NOT the old gateway. The retired gateway was a 1:1 hop — one question forwarded
to one executor, in front of a context that was already clean; it bought nothing. The collector
is BATCH-level: it MATCHES the bank first (so most questions REUSE and never reach an executor),
dedups, and runs that churn OFF the STAGE's context — it protects the STAGE's context, not the
executor's. Between it and the executors the dispatch is still direct: no second hop, no stake leak.


Knowledge home
--------------

Agents are THIN — every rule lives in its canonical home:

```
the probe layer (probe file anatomy, path binding,    → ../haipipe-probe/SKILL.md
the QA/ contract, the qa verb, the two LAWS,             ⭐ START HERE
status derivation, the writer table)
the consumer-specific interpretation                  → the owning Page Type
(authored after reading the answered QA file)           and Page EVIDENCE contract
the qa verb's executor-side flow     → ../../task/haipipe-task/fn/qa.md  ·  the discovery twin
```


Registration
------------

Real files live here (toolkit source of truth) and the plugin discovers each agent from this
`agents/` folder — the `name:` frontmatter is what registers it as a callable `subagent_type`.
