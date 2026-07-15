probe — Agent Roster
======================

The probe layer owns **ONE agent** — `haipipe-probe-q-executor-agent`, a stake-free, family-agnostic
QUESTION-LEVEL collector. Given a batch of q-executors it runs the stake-free middle of the loop
(② MATCH → ③ DISPATCH → ④ POINT) in an isolated context and returns the answered QA paths; the
stake-aware halves (① writing the q-executor + T1 LOCAL, ⑤ harvest) stay with the consumer/stage.
A probe is COMMUNICATION: it maps questions to answers and gets out of the way. It transports
evidence; it does not grade it.

The probe writes NO bank file. Its only files are the paper's own
`papers/<P>/1-probes/PPNN_<topic>.md` probe files. Execution artifacts live in `tasks/` and
`discoveries/`, authored by the executor (haipipe-probe/SKILL.md, R12 + CC-8).


Dispatch — the collector, then direct to the executors
-------------------------------------------------------

```
📄 the STAGE (in the CONSUMER session — a paper or an application)
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
📄 the STAGE again — ⑤ INTERPRET: reads each answered QA file and writes the claim's
   status into 0-lifecycle/1-claims/1-claims.md. No agent, no gate.
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
the constitution (probe file anatomy, path binding,   → ../haipipe-probe/SKILL.md
the QA/ contract, the qa verb, the two LAWS,             ⭐ START HERE
status derivation, the writer table)
the claim's status + claim_type overclaim check       → ../../<consumer>/1-lifecycle/1b-claims/
(authored by the consumer, from the answered QA file)   haipipe-{paper,application}-claims/SKILL.md
the qa verb's executor-side flow     → ../../task/haipipe-task/fn/qa.md  ·  the discovery twin
```


Registration
------------

Real files live here (toolkit source of truth) and the plugin discovers each agent from this
`agents/` folder — the `name:` frontmatter is what registers it as a callable `subagent_type`.
