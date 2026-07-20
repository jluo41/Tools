1-probe — the PROBE phase
=========================

ONE skill: `haipipe-paper-probe`. Evidence work has exactly one exit, and this is it.

The MODEL — probe-file anatomy, the QA state-line contract, the cost ladder, the two LAWS, the derived states, the checker's FAIL codes — is owned by `../../../probe/haipipe-probe/SKILL.md`. This directory only runs it for a paper.

```
DRAFT authors the plan          PROBE runs it forward
  ① ORGANIZE  ② MATCH     →      ③ DISPATCH  ④ POINT  ⑤ INTERPRET
```

`haipipe-paper-probe` EXECUTES the plan DRAFT wrote; it never re-matches it. The `route` and `bank` verdicts in each entry are AUTHORITATIVE.

```
③ DISPATCH   entries whose target is NEW, handed as a SET to
             Agent(haipipe-probe-q-executor-agent). That agent sends each
             `### q-executor` VERBATIM to Agent(haipipe-task-orchestrator-agent) /
             Agent(haipipe-discovery-orchestrator-agent) and writes back each target.
             Its clean context IS the wall — it never sees the stake.
             This worker calls no orchestrator itself.
④ POINT      open the target QA file and read its `- state:` line. `answered` → ⑤;
             `working` → stays commissioned; no path → failed.
⑤ INTERPRET  copy the QA answer into `### a-executor`, then each Q-consumer writes its
             own a-consumer in its STAGE DOC, anchored `[source: PP<NN>]`.
             HARVEST is inline here: source anchors, values, display-unit paths ride
             along with the answer into the SAME `### a-executor`.
```

The probe FILE — `1-probes/PPNN_<topic>.md`, one file per TOPIC, one ENTRY per q-executor — is the single consumer-side source of truth. `_LOG_<stage>.md` is the only sidecar.

```markdown
## QX<n> — <slug>

### q-executor        the question in GENERAL language; the dispatch payload; FROZEN
### q-consumer        one bullet per stage-doc `Q-<Stage>-<n>` this serves
### bank binding      **route**: · **bank**: · **target**: · **state**:
### a-executor        the harvest sink — a copy of the QA answer, written at ⑤
```

The STAKE never enters a probe file; it lives in the stage-doc Q-consumer. A CLAIM's status lives in `0-lifecycle/1b-claims/1b-claims.md`, written by the author. A display-shaped need is REROUTED, not collected: it becomes a DR row in `0-lifecycle/4-display/_DISPLAY_REQUEST.md` and the entry closes `answered-local`.

Enforcement is mechanical — `check-probe-cards.sh`, run at the worker's VERIFY step and again by the CHECK gate. A `state: planned` entry FAILs (probe-not-run); an `answered` target with an empty `### a-executor` FAILs (answered-not-read); an unresolvable `target` FAILs; a markdown table in a probe file FAILs. A green PROBE over any of these is a defect. RUN it; never eyeball the entries.

Per-stage worker map, seed/claims/resource specifics, strip forms: `haipipe-paper-probe/ref/per-stage-dispatch.md`.

Not user-facing: users invoke stage skills (seed, claims, …); a stage calls `Skill("haipipe-paper-probe", args="from-buffer <paper_root> [PPNN]")`.
