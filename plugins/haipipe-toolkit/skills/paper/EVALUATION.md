# Paper Skill Evaluation

How to judge whether the paper skill is good. Evaluate it TOP-DOWN, in three steps.

A layered skill is a container of containers. Judge the outer container before its contents: a broken umbrella hides good stages, and a good umbrella cannot rescue a broken stage. So the order is fixed — umbrella, then phase, then stage — and you stop at the first level that fails, because a failure there changes what "good" means for everything below it.

## The three levels

| Step | Level | What it owns | Where it lives |
|---|---|---|---|
| 1 | Umbrella (orchestrate) | intent parsing + routing + frontier | `haipipe-paper/`, `0-enter/`, `1-lifecycle/haipipe-paper-lifecycle` |
| 2 | Phase | the shared HOW: DRAFT → PROBE → REVISE → CHECK | `2-phase/` |
| 3 | Stage | the WHAT each stage delivers | `1-lifecycle/<N-stage>/<skill>` |

The umbrella routes; the phase workers execute; the stages define the contract each execution fulfills.

## Step 1 — Is the umbrella good?

The umbrella is `haipipe-paper` (router) + `haipipe-paper-enter` (Console) + `haipipe-paper-lifecycle` (spine orchestrator). It should ROUTE, never do stage work itself.

- Intent: a free-form request resolves to the right `(venue, stage)` pair.
- Routing: every lifecycle object reaches its owning skill (the Router Rule in `README.md`).
- Frontier: the Console derives state from disk, not stored status, and reports both `current_layer` and `maturity` (the Maturity Rule).
- Coverage: every stage in the spine is reachable; no orphan verb, no dead route.
- Boundary: the umbrella dispatches and summarizes; it never drafts prose or judges a claim.

If routing is wrong, stop — you cannot trust any stage verdict reached through a broken door.

## Step 2 — Is the phase good?

The phase engine is `2-phase/`: DRAFT → PROBE → REVISE → CHECK, shared across every stage. A fix here improves all stages at once.

- Order: the four phases fire in sequence; no phase is skipped or reordered.
- Internal: phases are never user-invoked directly — a stage drives them.
- Evidence door: PROBE is the ONLY way evidence enters; it raises questions as entries in `1-probes/` and dispatches the `q-executor:` block verbatim (`ref/03-paper-lifecycle.md`).
- Gates: DRAFT review and CHECK are the two human gates; the agent never self-advances past them (`ref/08-stage-gate.md`).
- Stage-agnostic: the workers carry no stage-specific logic; the stage supplies the contract, the phase supplies the process.

If a phase leaks (evidence entering outside PROBE, an auto-advance past CHECK), stop — the stage's output is unearned.

## Step 3 — Is the stage good?

Each stage in `1-lifecycle/` (seed, resource, claims, venue, pitch, narrative, display, section-edit) is judged against its own contract.

- One question: the stage answers exactly one question (the table in `PHILOSOPHY.md`), nothing more.
- 1:1 mapping: one stage, one skill, with reads/writes/calls declared (`ref/04-lifecycle-map.md`).
- Venue boundary: venue-FREE stages (seed, resource, claims) don't change on retarget; venue-ALIGNED stages (pitch onward) do.
- Artifact: produces its stage doc + `_LOG`, and updates `the S pages current_layer`.
- Taste: the stage illuminates what exists and elicits a taste-bearing choice (`ref/09-stage-illuminate.md`).

A stage that answers two questions, skips its `_LOG`, or decides on the user's behalf is not good, however clean its prose.

## Running it

This is the ORDER; `/haipipe-skill-diagnose` is the MACHINERY (SCOPE → DIAGNOSE → REPORT → FIX → RESOLVE → COMMIT). Sweep the bucket top-down through these three levels, report the first broken level to the user, and fix only after their eyeball.

## Other scales

Every scale with this shape inherits the same three steps and the same order. `haipipe-application` mirrors it exactly: umbrella = `haipipe-application`, phase = its `2-phase/` DPRC, stage = the `1-lifecycle/` ladder (1a-descriptions → 1d-advice). Evaluate any of them umbrella-first.
