---
name: dikw-report
description: "DIKW final report skill. Synthesize ALL DIKW findings into a comprehensive report answering the research questions. Use when the user asks to write the final report, summarize all findings, create DIKW report, or says /dikw-report. Trigger: final report, DIKW report, summarize findings, session report, write report."
---

Skill: dikw-report
====================

Final session report. Synthesize ALL DIKW findings into a comprehensive report.

On invocation, use `$ARGUMENTS` to get: project path, aim, questions.
Format: `/dikw-report [project_dir] [aim]`

---

Steps
-----

1. Parse arguments:
   - project_dir: from args or cwd
   - aim: from args or "default"

2. Read ALL available reports:
   - Exploration notes: `{project_dir}/sessions/{aim}/exploration/explore_notes.md`
   - D-level: `{project_dir}/reports/data/*.md`
   - I-level: `{project_dir}/reports/information/*.md`
   - K-level: `{project_dir}/reports/knowledge/*.md`
   - W-level: `{project_dir}/reports/wisdom/*.md`

3. Write the final report:
   - Path: `{project_dir}/sessions/{aim}/output/final_output.md`
   - Minimum 600 words

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
- Every claim must trace back to a specific D/I/K/W finding
- Write for a decision-maker, not a data scientist
- Report MUST be written to: sessions/{aim}/output/final_output.md
