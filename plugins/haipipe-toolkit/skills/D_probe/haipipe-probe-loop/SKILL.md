---
name: haipipe-probe-loop
description: "Iteration specialist of haipipe-probe. Chains review → explore (propose) → design (materialize) → re-review in an adversarial loop until the claim verdict reaches ✅ or a round budget is hit. The 'is this research strong enough yet?' loop driver. Called by /haipipe-probe orchestrator. Direct invocation works for loop-scoped work."
argument-hint: "[start|continue|status] [probe_ref_or_project] [args...]"
allowed-tools: Bash, Read, Write, Edit, Grep, Glob, Skill, mcp__codex__codex, mcp__codex__codex-reply
metadata:
  version: "1.4.0"
  last_updated: "2026-06-01"
  summary: "Iteration specialist of haipipe-probe."
  changelog:
    - "1.0.0 (2026-05-31): baseline metadata added."
    - "1.1.0 (2026-05-31): convergence files the K card (card-creator-knowledge-agent), closing the probe-cycle."
    - "1.2.0 (2026-05-31): convergence also files the per-probe W (card-creator-wisdom-agent, optional ◇) scoped to the new K — returns K+W to the narrative."
    - "1.3.0 (2026-06-01): update probe loop examples for lightweight `MM-NN_slug` probe folders."
    - "1.4.0 (2026-06-01): probe folders + refs switch to date-based `MMDD` / `P.MMDD`; materialize passes `--date MMDD`."
---

Skill: haipipe-probe-loop
===============================

The **iteration driver**. Where `-review` and `-explore` are stateless
single-shot operations, this skill **chains them into a loop** with
state — "review the current state, propose fixes, materialize them,
re-review, repeat until ✅ or N rounds reached."

Models the same adversarial-iteration pattern as the legacy
`/auto-review-loop`, but uses the D_probe specialists as
primitives instead of duplicating their logic.


Commands
--------

```
/haipipe-probe loop start <probe> [--rounds N]
  Begin a fresh loop on <probe>. Default rounds=4.

/haipipe-probe loop continue <probe>
  Resume an in-progress loop from its last LOOP_LOG.md entry.

/haipipe-probe loop status <probe>
  Show: round count, latest verdict, pending fixes, next action.

/haipipe-probe loop start project [--rounds N]
  Loop over ALL probes in the project that have status != confirmed.
```


Loop body (one round)
---------------------

```
Step 1: STRUCTURAL REVIEW
  Skill("haipipe-probe-review", args="probe <probe>")
  → collect errors / warnings / caveats

Step 2: SEMANTIC VERDICT
  Skill("haipipe-probe-review", args="claim <probe>")
  → Codex verdict: yes | partial | no + reasoning + suggested next probes
  → writes CLAIMS_FROM_RESULTS.md

Step 3: STOP CHECK
  if verdict == yes AND structural errors == 0:
      → FILE INSIGHT (close the probe cycle / L0): the probe is now confirmed,
        so its claim is a validated belief — file its 🟨 K, then its 🟧 W:

        (a) ◆ FILE K (required) — dispatch the K filer so the narrative has a
            🟨 K card to read —
              Agent(agent_type="card-creator-knowledge-agent",
                    prompt="<probe_ref> --project <project>")
              → files the 🟨 K card from this probe's `claim` (headless).
                Read the returned `card:` path to recover the new K id (e.g. K07).

        (b) ◇ FILE W (optional) — the K's twin: this probe's concrete next-step.
            If the confirmed probe implies a concrete next action (a re-test, a
            pivot, a stop-doing-X), chain the W filer scoped to the just-filed K —
              Agent(agent_type="card-creator-wisdom-agent",
                    prompt="--scope <new-K-id> --project <project>")
              → files one per-probe 🟧 W from that single K (headless).
            SKIP if the probe implies no concrete next-step (don't fabricate one).

        The 🟦 D observations come from this probe's task-cycles
        (card-creator-data per arm); 🟩 I (cross-D pattern) and STRATEGIC W
        spanning many K stay cross-cycle synthesis (ask report phase /
        haipipe-insight-explore) — the per-probe W here is the single-K next-step.
        (Without (a) the loop converges but never updates insights/, leaving the
        narrative blind; (b) hands the narrative the recommended next whip-crack.)
      exit loop with status = converged
  if round_count >= max_rounds:
      exit loop with status = budget_exhausted

Step 4: PROPOSE
  Skill("haipipe-probe-explore", args="propose <probe>")
  → coverage map across (arch × data × training)
  → ranked list of next probes to fill gaps
  Optionally also synthesize: Codex's "next_probes_needed" +
  -explore's coverage gaps → unified ranked proposal.

Step 5: HUMAN GATE (optional, on by default)
  Present the proposal. Wait for user approval before materializing.
  --auto skips the gate.

Step 6: MATERIALIZE
  For each approved proposal:
    a) Write the new probe.yaml:
       Skill("haipipe-probe-design", args="new <slug> [--date MMDD]")

    b) Resolve arms — either link existing OR scaffold new via bridge:
       • Existing runs satisfy the proposal:
           Skill("haipipe-probe-design", args="link <new_probe> <run-path>")
       • New runs needed:
           Skill("haipipe-probe-bridge", args="<new_probe>")
           → bridge scaffolds tasks in C_task, invokes Run Script Reviewer
             (pre-flight code review), runs sanity arm, deploys remaining
             arms, and links completed runs back to <new_probe>.

  IMPORTANT: design alone only writes yaml — runs are NOT created.
  For any proposal needing new runs, bridge MUST be called or the loop
  will spin on an empty arm list.

Step 7: LOG + CONTINUE
  Append round outcome to LOOP_LOG.md
  Increment round_count
  Goto Step 1
```


State file: `LOOP_LOG.md`
-------------------------

Per-probe loop history. Lives in the probe's own folder:

```
examples/<project>/probes/<MMDD>_<slug>/LOOP_LOG.md
```

Per-folder isolation prevents multiple probes' loops from clobbering
each other (a probe is a research thread; the loop log is that
thread's iteration history).

```markdown
# LOOP_LOG — probe P.0601

## Round 1 — <timestamp>
- structural: 2 warnings, 0 errors
- claim verdict: partial (confidence: medium)
- weaknesses: <list>
- proposed: <ranked list>
- approved: <subset>
- materialized: <probe IDs created>

## Round 2 — <timestamp>
- structural: 0 warnings, 0 errors
- claim verdict: yes (confidence: high)
- exit: converged
```


Stop conditions
---------------

```
✅ converged         verdict = yes AND structural errors = 0
🟡 budget_exhausted  hit max_rounds without converging
🔴 blocked           user rejected all proposals OR runs failed to materialize
🛑 paused            user invoked /haipipe-probe loop pause <probe>
```


Disambiguation
---------------

  - No verb → `status` (safest default — show state, don't start a loop).
  - "start" + existing in-progress loop → ASK whether to reset or continue.
  - "continue" + no in-progress loop → bail with "no loop in progress for <probe>".
  - "start project" with N probes → confirm before iterating all.


Risk profile
-------------

WRITES heavily:
- `probes/<MMDD>_<slug>/LOOP_LOG.md` (per-probe iteration history)
- `CLAIMS_FROM_RESULTS.md` (via review claim each round)
- New probe yamls (via design new each round)
- Triggers C_task task creation via bridge (Step 6 calls
  `haipipe-probe-bridge` for any proposal needing new runs)
- Triggers E_insight filing on convergence (Step 3 dispatches
  `card-creator-knowledge-agent` → writes `insights/K_knowledge/` from the
  probe's claim, then optionally `card-creator-wisdom-agent` → writes
  `insights/W_wisdom/` the per-probe next-step), closing the probe cycle
  (probe → task → insight · L0) with both 🟨 K and 🟧 W the loop previously
  left open

Calls external LLM (`mcp__codex__codex`) once per round in Step 2.
For multi-round loops, this is the dominant cost — budget accordingly
via `--rounds`.


Relation to legacy /auto-review-loop
------------------------------------

The research-toolkit's `/auto-review-loop` does this same pattern but
with internal review logic and direct code-modification fixes (not
probe-yaml materialization). This specialist is more aligned with
the D_probe design — it never modifies code or runs directly; it
proposes new PROBES, which then route through C_task for
execution.

If your loop needs to fix code (not propose new runs), `/auto-review-loop`
in research-toolkit is still the right tool. If your loop needs to
strengthen evidence by running more probes, this is the right tool.


Specialist tail
---------------

```
status:    ok | blocked | failed | converged | budget_exhausted
summary:   "P.0601 loop: round 3/4, verdict=partial→yes, converged"
artifacts: [probes/<MMDD>_<slug>/LOOP_LOG.md, CLAIMS_FROM_RESULTS.md, new probe IDs]
next:      if converged → K (+ optional per-probe W) filed via
                          card-creator-{knowledge,wisdom}-agent (L0 closed),
                          then /haipipe-paper-structure-narrative (start paper write-up)
          if budget_exhausted → /haipipe-probe review claim <probe> manually
          if blocked → triage rejected proposals
```
