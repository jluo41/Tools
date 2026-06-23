SESSION_STATE.json — Schema
============================

Single source of truth for the active session. Survives context
compaction, resume-after-crash, and orchestrator hand-off.

Lives at `applications/<kind>/<NN_slug>/SESSION_STATE.json` (for the
`ask` kind) or under the date-stamped artifact folder (for external
kinds).

Atomic write: write to `<file>.tmp` then `mv`. Never partial writes.


Top-level fields
=================

```json
{
  "status": "running",
  "kind": "ask",
  "aim": "03_film_test_od_generalization",
  "question": "Does FiLM hold on test-od?",
  "execution_mode": "inline",
  "current_phase": "observe",
  "current_step":  "task",
  "current_task":  "T1",
  "current_gate":  null,
  "plan_version": 1,
  "data_cut": "2026-05",
  "contract_path": "data/contract.yaml",
  "trimmed_by_contract": [],
  "completed_tasks": { ... },
  "pending_tasks":  { ... },
  "phase_history": [ ... ],
  "gates":         [ ... ],
  "revisions_count": 0,
  "probe_calls":      [ ... ],
  "task_calls":      [ ... ],
  "gate_persona":    { ... },
  "unattended_timeout": null
}
```


Field reference
================

```
status               running | complete
                     Set to "complete" only after the final gate accepts.

kind                 ask | message | ui | report
                     Locked at session creation; determines phase shape.

aim                  NN_<slug>, e.g. "03_film_test_od_generalization"
                     NN is the next-free index in applications/<kind>/.
                     Slug is intent-tagged (3-5 lowercase kebab tokens).

question             original user input (for ask) OR
                     parsed intent string (for message/ui/report).
                     Verbatim — never paraphrased.

execution_mode       inline | agent
                     inline = this session runs in the current claude pid
                     agent  = each task dispatched to a subagent
                     Locked at session creation.

current_phase        phase name from the kind's phase list
                     ask:      design | observe | claim | report | done
                     message:  init   | load    | draft  | review | write | done
                     (ui / report: similar — see kind's own SKILL.md)

current_step         task | gate
                     Every phase has 2 steps in order: task then gate.

current_task         non-null during step=task; null at gates
current_gate         non-null during step=gate (e.g. "G-design"); null otherwise

plan_version         integer ≥ 1; bumped on every `revise [feedback]` outcome.

completed_tasks      { phase: [{ name, status, plan_version }] }
                     status ∈ { done, reused, skipped, failed, invalidated }
                     - done       ran successfully this session
                     - reused     carried over from a prior session
                     - skipped    SKIP verdict from context loader
                     - failed     ran and failed
                     - invalidated dropped by later plan revision

pending_tasks        { phase: [name, ...] }
                     Recomputed after each plan write as:
                       new_plan[phase] − {done, reused, skipped} names

phase_history        ordered log of phase entries/exits + plan_version per entry
gates                ordered log of every gate firing
                     entry: { gate, plan_version, outcome, routes_to, timestamp }
revisions_count      number of `revise` outcomes so far
                     Hits MAX_REVISIONS = 3 → forced approve with audit banner.

probe_calls          [{ phase, probe_ref, via, ts, status }, ...]
                     Records every /haipipe-probe * invocation.
                     via ∈ { design, bridge, result, review }.

task_calls           [{ phase, task_path, via, ts, status }, ...]
                     Records every /haipipe-task * invocation.

gate_persona         { preset, strictness, ambition, notes }
                     Locked at session creation; see ref/gate-persona.md.

unattended_timeout   null | N (seconds) | 0
                     null = attended (wait forever)
                     N    = timed (auto-accept after N seconds)
                     0    = unattended (immediate auto-accept)
                     See ref/attendance-modes.md.
```


completed_tasks entry shape
============================

```json
{
  "name":         "T1",
  "status":       "done",
  "plan_version": 1,
  "yields":       ["D01", "I01"],
  "artifact_path": "tasks/E01_individual/02_od_filmcase/"
}
```

`yields` carries the DIKW card ids this task closes (D/I from task,
K/W from probe). Pre-gate artifact check verifies each yield
has a card filed in `insights/<layer>/`.


Pre-gate artifact check
========================

Before any gate fires, the orchestrator scans `completed_tasks[phase]`
entries with `status ∈ {done, reused}` and asserts:

```
ask kind:
  task that yields D## or I## → insights/D_data/D##_*.md OR I_information/I##_*.md exists
  task that yields K## or W## → probe.yaml has result.status == confirmed
                                AND insights/K_knowledge/K##_*.md OR W_wisdom/W##_*.md exists

message/ui/report kinds:
  artifact path exists and non-empty
```

If any check fails, the gate's outcome is overridden to:
`revise "task X missing <expected artifact>; re-run /haipipe-application-<kind>"`.


Recovery after compaction
==========================

On resume, read SESSION_STATE.json then:

1. State-vs-disk consistency check:
   - For each `done`/`reused` entry, verify expected artifact path exists.
   - Missing → demote entry status to `failed`, name returns to pending_tasks.
   - Log demotions to `tmp/recovery-<ISO>.log`.

2. Re-enter the orchestrator loop at (current_phase, current_step,
   current_task | current_gate).

3. Never re-run a task whose entry still satisfies the artifact contract.

4. `haipipe-application-context` is always re-run on resume — it's
   cheap and picks up any drift since the consistency check.
