Cross-family note — the probe PLAN moves into DRAFT (constitution v9.2.0, 2026-07-19)
====================================================================================

FROM: the paper-family session (JL co-design). TO: whoever resumes the application-family probe work.

WHAT CHANGED (constitution `skills/probe/haipipe-probe/SKILL.md`, v9.1.0 → 9.2.0)
--------------------------------------------------------------------------------

The five-step loop is re-assigned to phases. The probe PLAN is now authored during DRAFT, beside the stage draft, so ONE human gate reviews draft + probe plan together (the plan-review gate is MERGED into the DRAFT gate — NOT a second gate).

- ① ORGANIZE + ② MATCH run at DRAFT. The consumer organizes each Q-consumer into a probe SECTION and ROOTS it to a SPECIFIC bank folder (a read-only bank grep is legal — LAW 1 bans the pen and the run, not the eye).
- ③ DISPATCH + ④ POINT + ⑤ INTERPRET run at PROBE, which RUNS FORWARD with no second gate (PROBE stays a milestone).

Two new SECTION fields, authored at DRAFT as part of the plan:
- `route:` — the dispatch door `task | discovery`, AUTHORITATIVE.
- `match:` — the ② MATCH result rooted to a SPECIFIC folder: `EXISTS · <folder>` (→ link) or `NONE → propose NEW <folder>`.

Heading id = the stage-doc Q-consumer id, CONSUMER-LOCAL (paper: `Q-Seed-1`, `Q-Claim-6`; application uses its own scheme — ids never collide because a Q-consumer id never crosses the wall; only `q-executor` is shared).

Mechanical change: the old "empty `target:` = not yet probed" DRAFT/PROBE discriminator retires (DRAFT now writes `target:`); `state:` / `a-consumer:` mark planned-but-unrun.

JL RULING — MODEL A (2026-07-19)
--------------------------------

`route:` and `match:` are AUTHORITATIVE. At PROBE, the collector agent DISPATCHES; it does NOT re-run ② MATCH (the executor orchestrator's own QA-gate still dedups against an existing answer). The alternative (agent re-verifies the match in clean context, "model B") was NOT chosen.

PAPER SIDE — DONE
-----------------

- `skills/probe/haipipe-probe/SKILL.md` → v9.2.0 (+ CHANGELOG [9.2.0]).
- `skills/probe/haipipe-probe/ref/probe-template.md` → ADOPTED (route/match, `Q-<Stage>-<n>` heading, no `q-consumer:` field).
- `skills/paper/2-phase/0-draft/haipipe-paper-draft/SKILL.md` → DRAFT authors the full plan.
- `skills/paper/1-lifecycle/0-seed/haipipe-paper-seed/SKILL.md` → DRAFT/PROBE blocks + principle 5b.
- `skills/paper/2-phase/1-probe/haipipe-paper-probe/SKILL.md` → v5.1.0 (runs ③④⑤; ①② are DRAFT's).
- `skills/paper/haipipe-paper/fn/probes.md` → loop diagram reattributed.

ACTION FOR APPLICATION (mirror the paper edits)
-----------------------------------------------

- `skills/application/2-phase/0-draft/haipipe-application-draft/SKILL.md` — DRAFT authors the plan (q-executor + route + match + target); still FORBIDDEN to write `a-consumer:`.
- `skills/application/2-phase/1-probe/haipipe-application-probe/SKILL.md` — runs ③④⑤; ①② are DRAFT's (model A).
- `skills/application/haipipe-application/SKILL.md` — the umbrella line "reaching the bank is the PROBE phase's job" is now imprecise (the read-only ② MATCH is DRAFT's; only the RUN/dispatch is PROBE's).
- the application `fn/probes.md` twin — loop diagram reattribution.

⚠️ STILL OWED — SHARED, needs a JOINT pass (both families)
----------------------------------------------------------

- `skills/probe/agents/haipipe-probe-q-executor-agent.md` (the collector agent, SHARED). Its description still says it runs ② MATCH + ③ DISPATCH + ④ POINT. Under model A it should DISPATCH + POINT only (no re-match). I did NOT change it unilaterally because it is shared with application — its update belongs in a joint pass. Until then it may do a harmless confirming match (leans B); no correctness bug.
- `skills/paper/2-phase/1-probe/haipipe-paper-probe/ref/per-stage-dispatch.md` — may still reference the old ① authoring at PROBE.


UPDATE 2026-07-19 — constitution v9.3.0: DRAFT SELF-REVIEW before the gate
=========================================================================

Before the DRAFT human gate, a review sub-agent (FRESH context — a creator/reviewer split, so the drafter does not grade its own work) self-checks the phase output: the draft vs the stage's artifact spec (Surface A), and the probe plan vs the constitution's new **DRAFT self-review checklist** (Surface B: q-executor LAW-2-clean · answerable+specific · route set · match ROOTED to a specific folder, read + judged on the answer · target agrees · heading id = Q-consumer id · one ## Why). It reports; the drafter fixes + re-reviews (bounded); the verdict rides to the gate. PRECEDES the gate, never replaces it. Complements `check-probe-cards.sh` (mechanical, at CHECK — the reviewer judges what a regex cannot).

PAPER SIDE DONE: constitution `skills/probe/haipipe-probe/SKILL.md` → v9.3.0 (+ CHANGELOG, the checklist section); `skills/paper/2-phase/0-draft/haipipe-paper-draft/SKILL.md` → v4.2.0 (new Step 4b; `Agent` added to allowed-tools).

ACTION FOR APPLICATION: the application DRAFT worker (`haipipe-application-draft`) should mirror Step 4b — dispatch a fresh-context reviewer running Surface A (its OWN artifact spec) + Surface B (the shared constitution checklist) before its DRAFT gate; add `Agent` to its allowed-tools.
