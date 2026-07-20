# Application Skill Evaluation

How to judge whether the application skill is good. Evaluate it TOP-DOWN, in three steps.

A layered skill is a container of containers. Judge the outer container before its contents: a broken umbrella hides good stages, and a good umbrella cannot rescue a broken stage. So the order is fixed — umbrella, then phase, then stage — and you stop at the first level that fails, because a failure there changes what "good" means for everything below it.

## The three levels

| Step | Level | What it owns | Where it lives |
|---|---|---|---|
| 1 | Umbrella (orchestrate) | intent parsing + routing + frontier | `haipipe-application/`, `0-enter/`, `1-lifecycle/haipipe-application-lifecycle` |
| 2 | Phase | the shared HOW: DRAFT → PROBE → REVISE → CHECK | `2-phase/` |
| 3 | Stage | the WHAT each stage delivers | `1-lifecycle/<N-stage>/<skill>` |

The umbrella routes; the phase workers execute; the stages define the contract each execution fulfills.

## Step 1 — Is the umbrella good?

The umbrella is `haipipe-application` (router) + `haipipe-application-enter` (Console) + `haipipe-application-lifecycle` (spine orchestrator). It should ROUTE, never do stage work itself.

- Intent: a free-form request resolves to the right `(venue, stage)` pair.
- Routing: every lifecycle object reaches its owning skill (the Router Rule in `README.md` Router Rule).
- Frontier: the Console derives state from disk, not stored status, and reports both `current_layer` and `maturity` (the Maturity Rule).
- Coverage: every stage in the spine is reachable; no orphan verb, no dead route.
- Boundary: the umbrella dispatches and summarizes; it never drafts prose, judges a claim, or calls the bank inline (there is no `discover`/`task` proxy verb — the bank has its own door).

If routing is wrong, stop — you cannot trust any stage verdict reached through a broken door.

## Step 2 — Is the phase good?

The phase engine is `2-phase/`: DRAFT → PROBE → REVISE → CHECK, shared across every stage. A fix here improves all stages at once.

- Order: the four phases fire in sequence; no phase is skipped or reordered.
- Internal: phases are never user-invoked directly — a stage drives them.
- Evidence door: PROBE is the ONLY way evidence enters; it raises questions as entries in `1-probes/` and dispatches the `### q-executor` block verbatim through the clean collector agent (`1-lifecycle/haipipe-application-lifecycle/SKILL.md` Intervention Lifecycle Contract).
- Gates: DRAFT review and CHECK are the two human gates; the agent never self-advances past them (`haipipe-application/SKILL.md` Stage Gate Protocol). CHECK's mechanical teeth are `checks.sh` + the probe-file checker — a ❌/FAIL blocks the gate green at any venue depth.
- Stage-agnostic: the workers carry no stage-specific logic; the stage supplies the contract, the phase supplies the process.

If a phase leaks (evidence entering outside PROBE, an auto-advance past CHECK), stop — the stage's output is unearned.

## Step 3 — Is the stage good?

Each stage in `1-lifecycle/` (seed, the 1a–1d ladder: descriptions/themes/claims/advice, then venue, pitch, narrative, display, section-edit) is judged against its own contract.

- One question: the stage answers exactly one question (the table in `PHILOSOPHY.md`), nothing more.
- 1:1 mapping: one stage, one skill, with reads/writes/calls declared (`README.md` Router Rule).
- Ladder cite-chain: each DIKW rung anchors in the one above it (`T1 (D3)`, `C2 (T1; D3)`, `A ← C`); the ladder climbs to W (the deliverable), where paper stops at K.
- Venue boundary: venue-FREE stages (seed + the 1a–1d ladder) don't change on retarget; venue-ALIGNED stages (pitch onward) do. The pinned venue gates WHICH stages fire (`stages_skipped`) and HOW DEEP claims must settle (`claims_settlement`).
- **Template**: the stage's `ref/<stage>-template.md` is the contract mold — every real intervention's stage doc is stamped from it, so a bad template propagates everywhere. It must be concrete (real example values, not bare `<...>`), its sections must match what the SKILL declares, and its field vocabulary must be current (`state`, with the six-value state enum spelled in full). This is the single highest-leverage thing to check.
- Reservoir: the stage captures what it considered-and-dropped (1a Waivers, 1b Parked, 1c Declined hooks, 1d Rejected + No-action) — negative wisdom is first-class, so the next round does not re-derive it. (Seed has none: it is too early for considered-and-dropped wisdom; that accrues on the ladder rungs.)
- Artifact: produces its stage doc + `_LOG`, and updates `STATUS.md current_layer`.

A stage that answers two questions, ships a vague or stale template, skips its `_LOG`, or decides on the user's behalf is not good, however clean its prose.

## Running it

This is the ORDER; `/haipipe-skill-diagnose` is the MACHINERY (SCOPE → DIAGNOSE → REPORT → FIX → RESOLVE → COMMIT). Sweep the bucket top-down through these three levels, report the first broken level to the user, and fix only after their eyeball.

## Other scales

Every scale with this shape inherits the same three steps and the same order. `haipipe-paper` is the twin (umbrella = `haipipe-paper`, phase = its `2-phase/` DPRC, stage = the `1-resource → 1-claims` spine — it delivers K, this ladder delivers W). Evaluate any of them umbrella-first.
