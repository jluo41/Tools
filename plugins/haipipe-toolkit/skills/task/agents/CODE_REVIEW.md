# CODE REVIEW — task agent definition files

- overall_verdict: warn
- gate: 1 (pre-run / definition review)
- dialect: agent-definition (not Python or Stata)
- reviewed_at: 2026-06-23
- files reviewed:
    - .claude/agents/haipipe-task-orchestrator-agent.md  (v1.0.0 2026-06-23)
    - .claude/agents/haipipe-task-creator-agent.md       (v2.0.0 2026-06-09)
    - .claude/agents/haipipe-task-reviewer-agent.md      (v1.0.0 2026-06-08)
    - Tools/plugins/haipipe-toolkit/skills/task/agents/README.md

---

## Findings


### 1. Role Separation: WARN

evidence: haipipe-task-reviewer-agent.md line 43

intent: reviewer "I do NOT" section should redirect code authorship to the
correct agent name, haipipe-task-creator-agent.

code: "author code → haipipe-task-builder-agent (builder ≠ judge)"

detail: The reviewer agent was consolidated when haipipe-task-builder-agent
was renamed to haipipe-task-creator-agent (creator changelog entry v2.0.0
2026-06-09). The reviewer's "I do NOT" cross-reference was not updated. This
is a stale name — haipipe-task-builder-agent no longer exists as a declared
agent. A reader following this pointer will find no matching file.

fix: Replace "haipipe-task-builder-agent" with "haipipe-task-creator-agent"
in the reviewer's "I do NOT" block.


### 2. Lifecycle Coverage: WARN

evidence:
  - haipipe-task-reviewer-agent.md scope block: "serves_gates: GATE 1 (pre-run) + GATE 2 (post-run)"
  - haipipe-task-reviewer-agent.md body: only documents Gate 1 (code review) and Gate 2 (result audit)
  - README.md line 53: reviewer listed at stages 1, 2, 4
  - haipipe-task-orchestrator-agent.md lines 88, 101: orchestrator dispatches reviewer for "plan check" (Stage 1) and "report check" (Stage 4)

intent: reviewer should cover plan-check (Stage 1) and report-check (Stage 4)
in addition to Gate 1 code review (Stage 2) and Gate 2 result audit (Stage 3).

code: reviewer body has zero documentation for how it evaluates plan.yaml
(Stage 1) or report.yaml (Stage 4). The README and orchestrator both expect
this behavior, but the reviewer agent itself provides no procedure, checklist,
or format for those two sub-tasks.

detail: The orchestrator will dispatch the reviewer with a plan or report
artifact and expect a verdict. The reviewer has no documented behavior for
that path — it will fall back to ad-hoc judgment. This is a coverage gap:
two of four lifecycle stages lack reviewer procedures.

fix: Add two sections to haipipe-task-reviewer-agent.md — "PLAN check
(Stage 1)" and "REPORT check (Stage 4)" — each with an explicit checklist
and return format. Update "serves_gates" scope line to reflect all four
stages (not just Gate 1/Gate 2 terminology).


### 3. Tool Consistency: PASS

evidence:
  - orchestrator tools: Read, Write, Edit, Grep, Glob, Bash, Skill, Agent
  - creator tools: Read, Write, Edit, Grep, Glob, Bash, Skill
  - reviewer tools: Read, Write, Grep, Glob, Bash, mcp__codex__codex, mcp__codex__codex-reply

detail: Each agent has the tools it needs for its role. Orchestrator has Agent
(required to dispatch sub-agents). Creator has Write + Edit (required to
produce artifacts). Reviewer has Read + Write (required to consume code and
produce audit files). Reviewer omits Edit — appropriate since it writes new
files rather than modifying existing ones. Reviewer omits Agent — appropriate
since it does not dispatch sub-agents. No missing tools detected.

note: Reviewer has model pinned to "sonnet" while orchestrator and creator
use "model: inherit". This is intentional (Codex MCP calls require a specific
model context) and not a defect.


### 4. Dispatch Chain and Agent Name Consistency: WARN

evidence: haipipe-task-reviewer-agent.md line 43 (same as Check 1)

intent: all cross-references between agent files and the README should use
the canonical agent names declared in the frontmatter name: field.

code:
  - orchestrator dispatches "haipipe-task-creator-agent" and
    "haipipe-task-reviewer-agent" — matches frontmatter names. PASS.
  - creator paired_with "haipipe-task-reviewer-agent" — matches. PASS.
  - README uses same three names throughout. PASS.
  - reviewer "I do NOT" block references "haipipe-task-builder-agent" — does
    NOT match any declared agent name. FAIL on this reference.

detail: One stale cross-reference in the reviewer. All other dispatch
references are consistent. Assessed WARN (not FAIL) because the stale
reference is in a "do not" advisory, not in an active dispatch path — it
affects documentation clarity, not runtime routing.


### 5. Return Contract Compatibility: FAIL

evidence:
  - haipipe-task-creator-agent.md lines 140-151: loop contract includes
    verdict == "revise" as a distinct state that causes retry with feedback
  - haipipe-task-reviewer-agent.md return contract: "verdict: pass | warn | fail"
    — no "revise" state declared

intent: the orchestrator-managed creator-reviewer loop must close cleanly.
Creator says: "if verdict == revise: reviewer_feedback = verdict.feedback".
Reviewer must therefore be able to return revise as a verdict.

code: reviewer return contract enumerates only {pass, warn, fail}. "revise"
is absent. The creator's loop logic branches on revise. If the reviewer
never returns revise, the creator loop described in the creator's own contract
cannot trigger the feedback retry path — the loop will always break at pass
or fail, making the retry mechanism dead code.

detail: This is a semantic contract mismatch. Either:
  (a) reviewer must add "revise" to its return contract with a "feedback"
      field populated, OR
  (b) creator's loop contract must be revised to remove the revise branch
      and use a different retry signal (e.g., fail + issues list).
This requires a decision from the agent author. Assessed FAIL because the
described retry mechanism is structurally broken as written.

fix: Pick one of the two options above. If option (a): add to reviewer
return contract — "verdict: pass | warn | fail | revise" and
"feedback: <string> (populated when verdict=revise)".


### 6. Cross-layer Consistency (orchestrator <-> probe-orchestrator): WARN

evidence:
  - haipipe-task-orchestrator-agent.md description: "Dispatch target for
    probe-orchestrator or any skill needing task work done with clean context"
  - README.md: documents probe-orchestrator -> task-orchestrator dispatch
    relationship with a diagram
  - haipipe-task-orchestrator-agent.md return contract: {status, summary,
    results, artifacts, next}

intent: probe-orchestrator needs to be able to parse task-orchestrator's
return contract. The return contract should be documented in a way that the
probe layer can rely on without reading the task layer internals.

code: the orchestrator return contract is defined inside the orchestrator
agent file. No reciprocal mention exists in the orchestrator of what fields
probe-orchestrator reads, nor any versioning of the cross-layer interface.
The README documents the dispatch relationship but not the interface contract.

detail: This is a documentation gap rather than a hard breakage. If
probe-orchestrator is already written to parse {status, results, artifacts},
this is fine in practice. The gap becomes a problem if either side is
updated without updating the other. Assessed WARN (not FAIL) because no
active mis-match is visible — only an undocumented cross-layer contract.

fix: Add a "Cross-layer interface" note to the README (or the orchestrator
file) specifying which return fields probe-orchestrator depends on and a
minimal version marker.

---

## Summary table

| # | Check | Verdict |
|---|-------|---------|
| 1 | Role separation | WARN — stale agent name in reviewer "I do NOT" |
| 2 | Lifecycle coverage | WARN — Stage 1 plan-check + Stage 4 report-check undocumented in reviewer |
| 3 | Tool consistency | PASS — all agents have correct tools for their role |
| 4 | Dispatch chain / name consistency | WARN — same stale name as Check 1; all runtime dispatch references correct |
| 5 | Return contract compatibility | FAIL — reviewer missing "revise" verdict breaks creator retry loop |
| 6 | Cross-layer (probe) consistency | WARN — relationship documented, interface contract not versioned |

Overall verdict: warn (one FAIL + four WARNs; no blockers to running existing
tasks, but the revise-verdict gap means the retry loop is dead code and
lifecycle coverage gaps leave two stages with undocumented reviewer behavior)
