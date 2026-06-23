CODE REVIEW — Discovery Agent Triad
====================================

Reviewer: haipipe-discovery-reviewer-agent (self-review of definitions, not runtime output)
Date: 2026-06-23 (updated post-fixes)
Scope: 3 agent definition files + README + /haipipe-discovery SKILL.md
Verdict vocabulary: PASS / WARN / FAIL per check; overall verdict at end.


1. Role Separation
-------------------

Verdict: **PASS**

Creator, reviewer, orchestrator have clear non-overlapping roles:

- Orchestrator: coordinates lifecycle, dispatches the other two. Has Agent tool. Explicitly states "I do NOT own the creator or reviewer logic."
- Creator: produces artifacts (discovery.yaml, terminal files, report block). Has Skill tool (for bucket workers). No Agent tool. Explicitly states "I do NOT review my own work."
- Reviewer: evaluates creator output. No Skill or Agent tool. Explicitly states "I do NOT create discovery.yaml, sources.md, or terminal files" and "I do NOT search for or read papers."

No overlap detected. The triad mirrors probe and task patterns.


2. Lifecycle Coverage
---------------------

Verdict: **PASS**

All four stages are covered by both creator and reviewer:

```
Stage        Creator action                      Reviewer gate
Plan         writes discovery.yaml               checks question, type, strategy, criteria
Build (opt)  authors instrument under build/      checks rubric, operationalizability, scope
Execute      runs bucket workers, writes terminal spot-checks sources, verdict, ideas
Report       writes report block + status         checks accuracy, terminal exists, findings
```

README confirms the 4-stage structure. SKILL.md defines the same lifecycle (Plan -> Build(opt) -> Execute -> Report).


3. Three-Type Coverage
-----------------------

Verdict: **PASS**

All three types are handled by both creator and reviewer, with correct terminal files:

```
Type   Creator terminal                  Reviewer checks
搜     sources.md + notes.md             real papers, no fabrication, coverage, claim capture
析     verdict.md OR landscape.md        traced claims, no overstatement, camps covered, counter-evidence
创     ideas.md                          genuine novelty, novelty check run, grounded, feasibility
```

Both creator and reviewer mention all three types in descriptions, body text, and checklists. SKILL.md confirms the same terminal mapping.


4. Tool Consistency
-------------------

Verdict: **PASS** (previously WARN — resolved)

(a) Reviewer has Write + Edit tools but says it does NOT create artifacts.
    - Mitigant: return contract says `artifacts: [review notes if written]`, so Write is justified for review notes. Probe-reviewer also has Write + Edit. Consistent with sibling pattern.

(b) Reviewer citation verification section now specifies the Bash-based mechanism:
    "Verify 3-5 random citations from sources.md using Bash to call
     python research-toolkit/arxiv_fetch.py and python research-toolkit/semantic_scholar_fetch.py"
    No Skill tool needed; Bash is sufficient.

(c) Creator has Skill but not Agent. Correct: creator dispatches bucket workers via Skill, never dispatches other agents.

(d) Orchestrator has both Skill and Agent. Correct: orchestrator dispatches creator/reviewer via Agent.


5. Dispatch Chain
-----------------

Verdict: **PASS**

- Orchestrator description: "Dispatch target for probe-orchestrator or any skill needing external-evidence work done with clean context."
- Orchestrator dispatches: `haipipe-discovery-creator-agent` and `haipipe-discovery-reviewer-agent`. Names match actual filenames.
- Probe-orchestrator confirms: "status: not_started, type: discovery -> Dispatch discovery skill or agent."
- README cross-layer diagram matches.


6. Skill-Agent Boundary
------------------------

Verdict: **PASS**

Orchestrator explicitly states: "I do NOT replace the /haipipe-discovery skill for interactive use." Section "When to use me vs the skill" clearly separates:

```
/haipipe-discovery (skill)             interactive console, user in the loop
haipipe-discovery-orchestrator         non-interactive dispatch, clean context, returns results
```


7. Citation Discipline
-----------------------

Verdict: **PASS**

- Creator: "Always verify via arxiv_fetch.py + semantic_scholar_fetch.py before using externally. Record DOI, title, authors, year in sources.md. Flag any paper that cannot be verified as [UNVERIFIED]."
- Reviewer: "Verify 3-5 random citations from sources.md using Bash to call python research-toolkit/arxiv_fetch.py and python research-toolkit/semantic_scholar_fetch.py. Flag any [UNVERIFIED] papers the creator marked. Fail the review if >20% of spot-checked citations are fabricated."
- SKILL.md Review Output Contract: five rules including VERIFICATION FLAG per paper.

Both sides of the verification loop are defined. The [UNVERIFIED] flag protocol connects creator marking to reviewer checking.


8. Consistency with Task/Probe Patterns
----------------------------------------

Verdict: **PASS** (previously WARN — resolved)

(a) Naming convention: PASS. All three follow `haipipe-{layer}-{role}-agent` pattern.

(b) Return contract shape: PASS.
    - Orchestrator: `status: ok | blocked | failed` (matches task/probe orchestrators).
    - Creator: `status: ok | blocked | failed` (matches probe-creator).
    - Reviewer: `status: pass | revise | fail | blocked` (matches probe-reviewer).

(c) File duplication: PASS. Both `.claude/agents/` and toolkit source contain identical copies.


9. Directory Structure
-----------------------

Verdict: **PASS** (previously WARN — resolved)

(a) Chinese character consistency: PASS. Orchestrator now uses 创 (simplified) everywhere,
    matching creator, reviewer, and SKILL.md.

(b) Orchestrator return contract: PASS. Terminal field lists all four:
    "sources.md / verdict.md / landscape.md / ideas.md"

(c) 4-bucket directory structure: PASS. Directories now match DESIGN.md and SKILL.md:
    1_search/ (arxiv, semantic-scholar, exa-search)
    2_read/   (alphaxiv, deepxiv, paper-analyzer)
    3_review/ (research-lit, comm-lit-review, academic-researcher)
    4_idea/   (idea-creator, novelty-check)
    All .claude/skills/ symlinks resolve correctly.


Overall Verdict
===============

**PASS** — all checks clean. The triad is well-designed and internally consistent.

Previously had 4 WARNs; all resolved:
1. Reviewer citation verification: Bash path now documented explicitly. (check 4b)
2. Reviewer return contract: `blocked` status present. (check 8b)
3. Orchestrator Chinese characters: normalized to 创 (simplified). (check 9a)
4. Orchestrator return contract: landscape.md included. (check 9b)
5. Directory structure: restructured from 3-dir to 4-bucket layout matching design. (check 9c)
