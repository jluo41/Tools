---
name: dikw-knowledge
description: "DIKW K-level knowledge synthesis skill. Read D and I reports, synthesize validated insights, causal relationships, knowledge gaps. Use when the user asks to run a K-level task, synthesize knowledge, extract rules, find causal relationships, or says /dikw-knowledge. Trigger: knowledge synthesis, K-level, causal relationships, rules, insights, synthesis."
---

Skill: dikw-knowledge
======================

Runs during **`step=task`** of **`phase=K`**, once per K-task.
K-level knowledge synthesis: read D and I reports, synthesize validated insights.

On invocation, use `$ARGUMENTS` to get: task_name, snapshot_dir.
Format: `/dikw-knowledge <task_name> [snapshot_dir]`


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
  Context sources: insights/data/*/report.md + insights/information/*/report.md
  Does NOT read: raw data files (only reads what D and I produced)

---

Steps
-----

1. Parse arguments:
   - task_name from `$ARGUMENTS`
   - snapshot_dir: from args or cwd

2. Resolve the task folder name (K-level prefix is `K` + NN, e.g. K01, K02):
   - List existing `{snapshot_dir}/insights/knowledge/*/` folders
   - If one matches `K*-{task_name}/` → reuse (re-run)
   - Else → assign NN = next available two-digit index within the K-level
     (01, 02, …) and form folder name `K{NN}-{task_name}` (K01, K02, …)
   - Task folder: `{snapshot_dir}/insights/knowledge/K{NN}-{task_name}/`
     (example: `insights/knowledge/K01-pattern_synthesis/`)

3. Check if report already exists:
   - Path: `{snapshot_dir}/insights/knowledge/K{NN}-{task_name}/report.md`
   - If exists and non-empty: skip

4. Read all prior reports:
   - ALL D-level: `{snapshot_dir}/insights/data/*/report.md`
   - ALL I-level: `{snapshot_dir}/insights/information/*/report.md`

5. Synthesize knowledge:
   - Connect findings across D and I reports
   - Identify causal relationships (not just correlations)
   - Note knowledge gaps

6. Write report:
   - Path: `{snapshot_dir}/insights/knowledge/K{NN}-{task_name}/report.md`
   - Concise and accurate; max ~1000 words

Report format:

  Synthesis Summary — 3-5 key insights

  Validated Insights — each with: the insight, supporting evidence, confidence

  Causal Relationships — what causes what, mechanism, direction

  Knowledge Gaps — what is still unknown, what would help

  Synthesis Methodology — how D and I findings were connected

---

Rules
-----

- Read ALL D and I reports before writing: `insights/data/*/report.md`
  + `insights/information/*/report.md`
- Ground every claim in evidence from source reports
- No new data analysis — synthesize existing findings only
- No code execution — this is REASONING only
- Clearly distinguish causation from correlation
- K task folders contain only `report.md` (no code, no charts)
- Report MUST be written to: `insights/knowledge/K{NN}-{task_name}/report.md`

---

Example tasks
--------------

  rule_extraction
    Extract rules, principles, and causal relationships from D+I findings.

  knowledge_synthesis
    Connect D and I insights into coherent, validated knowledge.

  relationship_mapping
    Map causal and dependency relationships between entities.
