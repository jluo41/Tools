Probe Agent Triad -- Code Review
==================================

Date:     2026-06-23
Scope:    haipipe-probe-orchestrator-agent, haipipe-probe-creator-agent,
          haipipe-probe-reviewer-agent, README.md, SKILL.md
Reviewer: probe-reviewer-agent (self-review of definition files, not a probe claim)


1. Role Separation
-------------------

**Verdict: PASS**

Creator explicitly states "I do NOT: Judge whether evidence supports the claim"
(line 49) and "Review my own plan or evidence completeness" (line 50). It owns
Plan/Gather/Read only.

Reviewer explicitly states "I do NOT: Create probe.yaml, evidence_refs, or
evidence.md" (line 41) and "Run task scripts or gather evidence" (line 42). It
owns quality gates + Judge G1/G2/G3.

Orchestrator delegates cleanly: creator for Plan/Gather/Read production,
reviewer for quality gates and Judge. No role bleeding detected.

README confirms: "Creator never reviews. Reviewer never creates."


2. Lifecycle Coverage
----------------------

**Verdict: PASS**

All 5 stages accounted for:

```
Plan:    creator writes probe.yaml (orch Step 2) -> reviewer checks plan
Gather:  creator calls/links (orch Step 3)       -> reviewer checks completeness
Read:    creator writes evidence.md (orch Step 4) -> reviewer optional
Judge:   reviewer runs G1+G2+G3 (orch Step 5)
Deposit: user confirms (orch line 52: "Run Deposit (user confirms)")
```

The creator's lifecycle table (lines 31-36) matches the orchestrator's workflow
steps. The skill SKILL.md lifecycle (lines 70-79) matches identically. No gaps.

Note: Orchestrator Step 4 (Read) does NOT dispatch the reviewer for a Read
review, which is consistent with the reviewer marking Read review as "(optional)"
in its own definition (line 79). The creator's lifecycle table also shows
"(reviewer optional)" for Read. Consistent across all three.


3. Tool Consistency
--------------------

**Verdict: WARN**

Expected vs declared tools:

```
Agent           Expected                          Declared
orchestrator    Read,Write,Edit,Grep,Glob,        Read,Write,Edit,Grep,Glob,
                Bash,Skill,Agent                  Bash,Skill,Agent           -- OK

creator         Read,Write,Edit,Bash,Skill,       Read,Write,Edit,Grep,Glob,
                Agent,Grep,Glob                   Bash,Skill,Agent           -- OK

reviewer        Read,Grep,Glob,Bash,Write         Read,Write,Edit,Grep,
                                                  Glob,Bash                  -- WARN
```

**Warning: Reviewer declares Edit but should not need it.** The reviewer writes
verdict.md (new file via Write) and updates probe.yaml.verdict. The Edit tool
implies modifying existing files, which is consistent with updating probe.yaml.
However, the reviewer's "I do NOT" list says it does not create probe.yaml --
it only sets the verdict block inside it. Edit is actually needed for this.
Downgrading concern: Edit is justified for probe.yaml.verdict updates.

**Warning: Reviewer does NOT declare Skill or Agent.** The retired
probe-integrity-auditor-agent and claim-verifier-agent both declared
mcp__codex__codex and mcp__codex__codex-reply for Codex-backed review. The
merged reviewer has neither Codex MCP tools nor Agent tool. This means:

- The reviewer CANNOT delegate to Codex for integrity audit (category A-E)
  or claim verification, which was the architectural intent of the retired
  agents ("Codex reads the files; I only hand it paths").
- The builder-is-not-judge principle relied on Codex as an out-of-family
  reviewer. Without Codex, the merged reviewer judges its own reading of
  evidence, weakening the independence guarantee.

This is a design trade-off (simpler agent, fewer tool dependencies) but it IS
a capability regression from the retired agents. The README and reviewer
definition are silent on why Codex was dropped.

**Recommendation:** Either (a) add mcp__codex__codex + mcp__codex__codex-reply
to the reviewer's tool list, or (b) explicitly document in the reviewer that
Codex delegation is deferred/optional and the builder!=judge principle is now
enforced by the creator/reviewer split alone rather than by Codex independence.


4. Dispatch Chain
------------------

**Verdict: WARN**

Orchestrator dispatches:

```
Step 2 (Plan):      haipipe-probe-creator-agent      -- correct, file exists
                    haipipe-probe-reviewer-agent      -- correct, file exists
Step 3 (Gather):    haipipe-task-orchestrator-agent   -- correct, file exists
Step 4 (Read):      haipipe-probe-creator-agent       -- correct
Step 5 (Judge):     haipipe-probe-reviewer-agent      -- correct
```

Creator dispatches during Gather:

```
type: task, missing: haipipe-task-creator-agent       -- correct, file exists
```

**Warning: Discovery dispatch is vague.** Orchestrator line 105-106 says:
"Dispatch discovery skill or agent" without naming a specific agent. The file
`haipipe-discovery-orchestrator-agent.md` exists. The orchestrator should name
it explicitly for deterministic dispatch, consistent with how it names
`haipipe-task-orchestrator-agent`.

**Recommendation:** Change line 105-106 from "Dispatch discovery skill or
agent" to "Dispatch haipipe-discovery-orchestrator-agent".


5. Judge Gates vs Retired Agents
---------------------------------

**Verdict: WARN**

Comparison of merged reviewer G1/G2/G3 against their retired originals:

**G1 (Structural) vs probe-structural-reviewer-agent:**

- Checklist items match: evidence exists, roles comparable, results match
  comparison, caveats cover confounds, discovery verdicts accounted for.
- Retired agent references `../../fn/judge.md` and
  `../../ref/probe-caveats-checklist.txt` as canonical logic sources. Merged
  reviewer does NOT reference these. Loss of traceability to the shared
  canonical procedure.
- Retired agent had a severity taxonomy (error/warning/info). Merged reviewer
  does not. Minor: the merged reviewer's binary pass/fail is simpler but loses
  the warning tier.
- Retired agent's next-step was explicit: "if clean -> probe-integrity-auditor-
  agent, then claim-verifier-agent". Merged reviewer handles this internally
  with "Run sequentially. G2 blocks G3." Functionally equivalent.

**G2 (Integrity) vs probe-integrity-auditor-agent:**

- All 5 fraud categories (A-E) are preserved verbatim. Match.
- Gating logic preserved: integrity fail blocks G3. Match.
- CRITICAL DIFFERENCE: Retired agent used Codex MCP for independence. Merged
  reviewer does not. See Check 3 above.
- Retired agent wrote to INTEGRITY_AUDIT.md. Merged reviewer writes to the
  "integrity section of verdict.md". File name change is fine (consolidation)
  but the skill's SKILL.md still mentions INTEGRITY_AUDIT.md as an optional
  file (line 223). Minor inconsistency.
- Retired agent had a "warn" tier that auto-capped claim confidence to medium.
  Merged reviewer only has pass/fail for integrity. The warn->confidence-cap
  logic is LOST.

**G3 (Claim) vs claim-verifier-agent:**

- Verdict values match: yes/partial/no/blocked. Match.
- Confidence tiers match: high/medium/low. Match.
- Scope supported/unsupported preserved. Match.
- CRITICAL DIFFERENCE: Retired agent required a recent INTEGRITY_AUDIT.md and
  consumed integrity warn to cap confidence. Merged reviewer says "if integrity
  = fail, block G3" but does NOT mention integrity warn capping confidence.
  Loss of the warn-tier interaction.
- Retired agent wrote to CLAIMS_FROM_RESULTS.md. Merged reviewer writes to the
  "claim section of verdict.md". File name change is fine (consolidation) but
  skill SKILL.md still mentions CLAIMS_FROM_RESULTS.md as optional (line 224).
- Retired agent used Codex MCP. Merged reviewer does not. See Check 3.
- Retired agent had routing guidance (yes->Return, partial->narrow, no->pivot,
  blocked->resolve). Merged reviewer's return contract uses "deposit" instead
  of "Return". Consistent with the 4.0.1 rename.

**Recommendations:**
1. Add canonical logic references (fn/judge.md, ref/probe-caveats-checklist.txt)
   to the merged reviewer.
2. Restore the integrity warn tier and the confidence-capping interaction.
3. Document or restore Codex delegation (see Check 3).
4. Update SKILL.md optional file names (INTEGRITY_AUDIT.md, CLAIMS_FROM_RESULTS.md)
   to note these are legacy names; merged reviewer writes verdict.md sections.


6. Skill-Agent Boundary
-------------------------

**Verdict: PASS**

Orchestrator explicitly addresses this (lines 28-35):

```
/haipipe-probe (skill)          interactive console, user in the loop, copilot
haipipe-probe-orchestrator      non-interactive dispatch, clean context, returns results
```

"The skill is for the user typing `/haipipe-probe P.0623a`. I am for when
/haipipe-paper dispatches Agent()."

The orchestrator's "I do NOT" list (line 49) says "Replace the /haipipe-probe
skill for interactive use."

**However:** The skill's SKILL.md does NOT mention the agents at all. There is
no cross-reference from the skill to the agent triad. A user reading SKILL.md
would not know the agents exist. This is not a functional bug but IS a
documentation gap.

**Recommendation:** Add a brief section to SKILL.md (e.g., under Boundaries or
as a new section) noting: "For non-interactive / programmatic dispatch, use
haipipe-probe-orchestrator-agent. See Tools/plugins/haipipe-toolkit/skills/
probe/agents/README.md."


7. Return Contracts
--------------------

**Verdict: PASS**

All three agents define return contracts. Compatibility check:

```
Orchestrator returns:   status (ok|blocked|failed), summary, evidence path,
                        verdict path, probe_ref, next
Creator returns:        status (ok|blocked|failed), summary, artifacts list,
                        stage, next
Reviewer returns:       status (pass|revise|fail|blocked), gate, summary,
                        feedback, artifacts, next
```

Orchestrator consumes creator's and reviewer's returns. The status vocabularies
differ but are compatible:

- Creator: ok/blocked/failed (production outcomes)
- Reviewer: pass/revise/fail/blocked (evaluation outcomes)
- Orchestrator: ok/blocked/failed (aggregated outcomes)

The reviewer's "revise" maps to the orchestrator's loop logic ("Loop if reviewer
says revise", line 88). The reviewer's "pass" maps to the orchestrator advancing
to the next step.

The skill's return contract (lines 318-323) uses the same ok/blocked/failed
vocabulary as the orchestrator. Compatible.

One minor note: the reviewer's Gather gate uses "incomplete" as a verdict
(line 76) rather than "revise". This is a fourth status value not in the return
contract's status enum (pass|revise|fail|blocked). Functionally it maps to
"revise" but the vocabulary is inconsistent within the reviewer itself.

**Recommendation:** Align the Gather review verdict to use "revise" instead of
"incomplete", or add "incomplete" to the return contract enum.


8. Cross-Layer Dispatch
------------------------

**Verdict: WARN**

Orchestrator references:

```
haipipe-task-orchestrator-agent       -- EXISTS at .claude/agents/
haipipe-discovery-orchestrator-agent  -- EXISTS at .claude/agents/ but NOT
                                         named explicitly (see Check 4)
```

README cross-layer diagram (lines 36-40) shows:

```
/haipipe-paper -> probe-orchestrator -> task-orchestrator
```

This diagram is correct but INCOMPLETE. It does not show discovery dispatch.
The orchestrator workflow (line 105) does handle discovery evidence items but
the dispatch target is vague ("discovery skill or agent").

Creator (line 79) dispatches haipipe-task-creator-agent for building missing
tasks. This is correct -- the creator builds the task definition, then reports
back so the orchestrator can dispatch the task-orchestrator to run it.

**Warning:** Creator does NOT have a parallel path for building missing
discovery definitions. Line 86-87 just says "Report 'discovery needed'
(orchestrator dispatches discovery)". If a discovery definition does not exist
yet, there is no equivalent of "dispatch haipipe-discovery-creator-agent to
build it" in the creator's Gather flow. This is asymmetric with the task path.

**Recommendations:**
1. Name haipipe-discovery-orchestrator-agent explicitly in the orchestrator.
2. Add discovery-creator dispatch to the creator's Gather flow, mirroring the
   task-creator pattern.
3. Add discovery to the README cross-layer diagram.


Summary
--------

```
Check                            Verdict   Issues
1. Role Separation               PASS      --
2. Lifecycle Coverage             PASS      --
3. Tool Consistency               WARN      Codex MCP tools dropped; no doc on why
4. Dispatch Chain                 WARN      Discovery dispatch not named explicitly
5. Judge Gates vs Retired         WARN      Integrity warn tier lost; no canonical
                                            logic refs; Codex independence dropped
6. Skill-Agent Boundary           PASS      SKILL.md lacks agent cross-ref (doc gap)
7. Return Contracts               PASS      Minor: "incomplete" not in status enum
8. Cross-Layer Dispatch           WARN      Discovery path asymmetric with task path
```

**Overall verdict: PASS with 4 WARNs.**

The triad is structurally sound and internally consistent on role separation,
lifecycle coverage, and return contracts. The main risks are:

1. **Codex independence dropped** (Checks 3 + 5): The strongest concern. The
   retired agents used Codex as an out-of-family reviewer for integrity and
   claim gates. The merged reviewer judges everything itself. Either restore
   Codex tools or document the new independence model explicitly.

2. **Integrity warn tier lost** (Check 5): The retired integrity auditor had a
   three-tier verdict (pass/warn/fail) where warn capped claim confidence. The
   merged reviewer only has pass/fail, losing the nuanced interaction.

3. **Discovery dispatch vague** (Checks 4 + 8): Task dispatch is fully named
   and symmetric (creator builds, orchestrator runs). Discovery dispatch says
   "skill or agent" without naming haipipe-discovery-orchestrator-agent, and the
   creator has no discovery-creator build path.

None of these block deployment. They are design trade-offs (Codex) or minor
gaps (discovery naming, warn tier) that should be addressed in a follow-up
revision.
