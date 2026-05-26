---
name: dikw-report
description: "DIKW final report skill. Synthesize ALL DIKW findings into a comprehensive report answering the research questions. Use when the user asks to write the final report, summarize all findings, create DIKW report, or says /dikw-report. Trigger: final report, DIKW report, summarize findings, session report, write report."
---

Skill: dikw-report
====================

Runs during **`step=task`** of **`phase=report`** (the single task of that phase).
Synthesizes ALL DIKW findings into a comprehensive final report.

On invocation, use `$ARGUMENTS` to get: snapshot_dir, aim, questions.
Format: `/dikw-report [snapshot_dir] [aim]`

---

Steps
-----

1. Parse arguments:
   - snapshot_dir: from args or cwd
   - aim: from args (required; auto-generated at session creation as NN_{slug})

2. Read ALL available reports:
   - Exploration notes: `{snapshot_dir}/exploration/explore_notes.md` (snapshot-level)
   - D-level: `{snapshot_dir}/insights/data/*/report.md`
   - I-level: `{snapshot_dir}/insights/information/*/report.md`
   - K-level: `{snapshot_dir}/insights/knowledge/*/report.md`
   - W-level: `{snapshot_dir}/insights/wisdom/*/report.md`
   - Session question: `{snapshot_dir}/sessions/{aim}/question.md`

3. Write the final report:
   - Path: `{snapshot_dir}/sessions/{aim}/output/final_output.md`
   - Concise and accurate; **max ~1000 words** (matches the K/W /
     phase-skill cap used elsewhere in the plugin — short reports are
     fine when findings are clean)

Report structure:

  Executive Summary
    5-7 bullet points for someone who only reads this section

  Direct Answers to Research Questions
    Clear answer per question, supported by evidence

  Key Findings by Level
    D (Data): what the raw data showed
    I (Information): patterns and correlations
    K (Knowledge): validated insights and causal relationships
    W (Wisdom): strategic recommendations

  Top Actionable Recommendations
    3-5 specific, prioritized actions with rationale

  Data Quality Notes
    Issues and how they affect conclusions

  Limitations and Next Steps
    What this analysis cannot answer
    Recommended follow-up

---

Rules
-----

- Read ALL reports before writing — do not skip any
- When listing reports per level, sort by `{L}{NN}-` prefix (L=D/I/K/W, NN=execution order)
- Every claim must trace back to a specific D/I/K/W finding
  (cite task folder: "insights/data/D01-col_overview/report.md")
- Write for a decision-maker, not a data scientist
- Report MUST be written to: `sessions/{aim}/output/final_output.md`
- **Persona-aware tone.** Read `DIKW_STATE.gate_persona` if present.
  When `strictness >= 7`, lead with a "What we cannot claim" section and
  mark every directional claim as CI-limited. When `ambition >= 7`,
  expand the K/W synthesis into named hypotheses and follow-up
  questions. When both are low (`lenient`), keep the report tight to
  the executive summary + direct answers.
