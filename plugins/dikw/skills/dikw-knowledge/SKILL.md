---
name: dikw-knowledge
description: "DIKW K-level knowledge synthesis skill. Read D and I reports, synthesize validated insights, causal relationships, knowledge gaps. Use when the user asks to run a K-level task, synthesize knowledge, extract rules, find causal relationships, or says /dikw-knowledge. Trigger: knowledge synthesis, K-level, causal relationships, rules, insights, synthesis."
---

Skill: dikw-knowledge
======================

K-level knowledge synthesis. Read D and I reports, synthesize validated insights.

On invocation, use `$ARGUMENTS` to get: task_name, project path.
Format: `/dikw-knowledge <task_name> [project_dir]`


DIKW Boundary — What K-level IS and IS NOT
--------------------------------------------

  K-level answers: WHY do these patterns exist?

  K IS:
    - Explaining causal mechanisms behind I-level patterns
    - Validating whether correlations represent real relationships
    - Synthesizing rules and principles from multiple findings
    - Identifying knowledge gaps (what we still don't know)
    - Connecting findings across D and I into coherent understanding
    - Distinguishing causation from correlation

  K IS NOT:
    - Running code or analyzing raw data (that's D/I)
    - Describing what's in the data (that's D)
    - Finding new patterns (that's I)
    - Recommending actions (that's W)

  K output is EXPLANATIONS: "duplicates are caused by the retry mechanism —
    when delivery fails, the system re-sends, creating duplicate invitation records"
  NOT patterns: "42% duplication rate correlates with message_type"
  NOT recommendations: "disable retries to reduce duplicates"

  Execution mode: LLM REASONING (reads reports, synthesizes, no code execution)
  Reads: D-level reports + I-level reports
  Context sources: reports/data/*.md + reports/information/*.md
  Does NOT read: raw data files (only reads what D and I produced)

---

Steps
-----

1. Parse arguments:
   - task_name from `$ARGUMENTS`
   - project_dir: from args or cwd

2. Check if report already exists:
   - Path: `{project_dir}/reports/knowledge/{task_name}.md`
   - If exists and >100 bytes: skip

3. Read all prior reports:
   - ALL D-level: `{project_dir}/reports/data/*.md`
   - ALL I-level: `{project_dir}/reports/information/*.md`

4. Synthesize knowledge:
   - Connect findings across D and I reports
   - Identify causal relationships (not just correlations)
   - Note knowledge gaps

5. Write report:
   - Path: `{project_dir}/reports/knowledge/{task_name}.md`
   - Minimum 400 words

Report format:

  Synthesis Summary — 3-5 key insights

  Validated Insights — each with: the insight, supporting evidence, confidence

  Causal Relationships — what causes what, mechanism, direction

  Knowledge Gaps — what is still unknown, what would help

  Synthesis Methodology — how D and I findings were connected

---

Rules
-----

- Read ALL D and I reports before writing
- Ground every claim in evidence from source reports
- No new data analysis — synthesize existing findings only
- No code execution — this is REASONING only
- Clearly distinguish causation from correlation
- Report MUST be written to: reports/knowledge/{task_name}.md

---

Example tasks
--------------

  rule_extraction
    Extract rules, principles, and causal relationships from D+I findings.

  knowledge_synthesis
    Connect D and I insights into coherent, validated knowledge.

  relationship_mapping
    Map causal and dependency relationships between entities.
