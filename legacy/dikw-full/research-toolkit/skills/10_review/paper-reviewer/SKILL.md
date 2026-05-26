---
name: paper-reviewer
description: Use when acting as a journal or grant reviewer and writing formal reviewer-side evaluations focused on methodology, statistics, reporting standards, reproducibility, and constructive feedback.
---

# Scientific Critical Evaluation and Peer Review

## Overview

Peer review is a systematic process for evaluating scientific manuscripts. Assess methodology, statistics, design, reproducibility, ethics, and reporting standards. Apply this skill for manuscript and grant review across disciplines with constructive, rigorous evaluation.

## When to Use This Skill

This skill should be used when:
- Conducting peer review of scientific manuscripts for journals
- Evaluating grant proposals and research applications
- Assessing methodology and experimental design rigor
- Reviewing statistical analyses and reporting standards
- Evaluating reproducibility and data availability
- Checking compliance with reporting guidelines (CONSORT, STROBE, PRISMA)
- Providing constructive feedback on scientific writing

## Visual Enhancement with Scientific Figures

**When creating documents with this skill, consider adding diagrams when they clarify a workflow, architecture, or evaluation framework.**

If the document does not already contain suitable figures:
- Use the **inno-figure-gen** skill to generate publication-style diagrams.
- Describe the desired figure in natural language and specify academic style constraints.
- Iterate prompts until the figure is clear, readable, and suitable for review materials.

**Example command:**
```bash
uv run ~/.codex/skills/inno-figure-gen/scripts/generate_image.py \
  --prompt "Publication-style diagram of the review workflow; white background; clean labels; colorblind-friendly palette; high contrast" \
  --filename "figures/review-workflow.png" \
  --resolution 2K
```

Requires `GEMINI_API_KEY` or an explicit `--api-key`.

**When to add figures:**
- Peer review workflow diagrams
- Evaluation criteria decision trees
- Review process flowcharts
- Methodology assessment frameworks
- Quality assessment visualizations
- Reporting guidelines compliance diagrams
- Any complex concept that benefits from visualization

For detailed guidance on creating figures, refer to the `inno-figure-gen` skill documentation.

---

## Peer Review Workflow

Conduct peer review systematically through the following stages, adapting depth and focus based on the manuscript type and discipline.

### Stage 1: Initial Assessment

Begin with a high-level evaluation to determine the manuscript's scope, novelty, and overall quality.

**Key Questions:**
- What is the central research question or hypothesis?
- What are the main findings and conclusions?
- Is the work scientifically sound and significant?
- Is the work appropriate for the intended venue?
- Are there any immediate major flaws that would preclude publication?

**Output:** Brief summary (2-3 sentences) capturing the manuscript's essence and initial impression.

### Stage 2: Detailed Section-by-Section Review

Conduct a thorough evaluation of each manuscript section, documenting specific concerns and strengths.

#### Abstract and Title
- **Accuracy:** Does the abstract accurately reflect the study's content and conclusions?
- **Clarity:** Is the title specific, accurate, and informative?
- **Completeness:** Are key findings and methods summarized appropriately?
- **Accessibility:** Is the abstract comprehensible to a broad scientific audience?

#### Introduction
- **Context:** Is the background information adequate and current?
- **Rationale:** Is the research question clearly motivated and justified?
- **Novelty:** Is the work's originality and significance clearly articulated?
- **Literature:** Are relevant prior studies appropriately cited?
- **Objectives:** Are research aims/hypotheses clearly stated?

#### Methods
- **Reproducibility:** Can another researcher replicate the study from the description provided?
- **Rigor:** Are the methods appropriate for addressing the research questions?
- **Detail:** Are protocols, reagents, equipment, and parameters sufficiently described?
- **Ethics:** Are ethical approvals, consent, and data handling properly documented?
- **Statistics:** Are statistical methods appropriate, clearly described, and justified?
- **Validation:** Are controls, replicates, and validation approaches adequate?

**Critical elements to verify:**
- Sample sizes and power calculations
- Randomization and blinding procedures
- Inclusion/exclusion criteria
- Data collection protocols
- Computational methods and software versions
- Statistical tests and correction for multiple comparisons

#### Results
- **Presentation:** Are results presented logically and clearly?
- **Figures/Tables:** Are visualizations appropriate, clear, and properly labeled?
- **Statistics:** Are statistical results properly reported (effect sizes, confidence intervals, p-values)?
- **Objectivity:** Are results presented without over-interpretation?
- **Completeness:** Are all relevant results included, including negative results?
- **Reproducibility:** Are raw data or summary statistics provided?

**Common issues to identify:**
- Selective reporting of results
- Inappropriate statistical tests
- Missing error bars or measures of variability
- Over-fitting or circular analysis
- Batch effects or confounding variables
- Missing controls or validation experiments

#### Discussion
- **Interpretation:** Are conclusions supported by the data?
- **Limitations:** Are study limitations acknowledged and discussed?
- **Context:** Are findings placed appropriately within existing literature?
- **Speculation:** Is speculation clearly distinguished from data-supported conclusions?
- **Significance:** Are implications and importance clearly articulated?
- **Future directions:** Are next steps or unanswered questions discussed?

**Red flags:**
- Overstated conclusions
- Ignoring contradictory evidence
- Causal claims from correlational data
- Inadequate discussion of limitations
- Mechanistic claims without mechanistic evidence

#### References
- **Completeness:** Are key relevant papers cited?
- **Currency:** Are recent important studies included?
- **Balance:** Are contrary viewpoints appropriately cited?
- **Accuracy:** Are citations accurate and appropriate?
- **Self-citation:** Is there excessive or inappropriate self-citation?

---

## Writing Review Feedback Constructively

The author will read every word of your review and will quote your
exact sentences in their rebuttal. Two writing habits avoid friction
without softening rigorous assessment.

**1. Write each concern as a complete, quotable sentence.** Authors
will quote your sentence verbatim in the response letter. A clear,
self-contained sentence yields a clean back-and-forth; a half-finished
thought or run-on paragraph forces the author to paraphrase, which
they should not do (see `paper-rebuttal/ref/principles.md` Principle 12)
and which invites avoidable disagreement.

  Good: "The IRB exemption does not establish ToS compliance with the
        source platforms; the manuscript should address platform terms
        of service separately."

  Bad:  "Ethical issues remain. Platforms? Consent? IRB scope is
        addressed but other concerns are not. Please discuss."

**2. Frame each concern as the diagnostic question or specific change
you want.** A diagnostic question lets the author respond with data;
a specific-change request lets the author commit to a revision.
Vague displeasure makes both impossible and tends to be answered with
defensive prose rather than a real fix.

  Good: "Is it possible (for example) that the LLM is largely echoing
        sentiment, so reviews with positive language get high trait
        scores and also get high star ratings?"
        (specific diagnostic; author can run a partial-correlation
        analysis to address it)

  Bad:  "The high correlations are concerning."
        (no specific test; invites a hand-wave reply)

**3. Distinguish hard-blocking concerns from preferences.** Mark
weaknesses you consider must-fix vs. nice-to-have, so the author knows
where to invest effort. Mixing the two without labels produces
exhausting rebuttals that lose the editor's attention.

**4. Keep tone professional and direct.** State disagreements as
substantive critiques, not as judgments of the authors' competence or
honesty. "The claim is not supported by the data shown" is a strong
criticism; "the authors clearly do not understand X" is not — it
moves the discussion away from the data.

**5. Do not invent quoted phrases.** If you put text in quotation
marks, those words must appear in the manuscript. Inventing a phrase
("the authors claim ...") that the manuscript never used wastes the
author's response budget on disclaiming language they never wrote.
