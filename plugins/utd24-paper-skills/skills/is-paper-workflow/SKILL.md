---
name: is-paper-workflow
description: Use for end-to-end writing of Information Systems research papers targeting UTD24 IS journals (MISQ, ISR, Management Science IS section). Invoke whenever the user is drafting, revising, or positioning an IS paper — covers contribution framing, theory selection, methodology design, and submission strategy. Use this skill proactively when the user mentions IS research, IT artifacts, digital systems, or any paper targeting MISQ, ISR, or Management Science.
---

# IS Paper Workflow

End-to-end workflow for Information Systems papers targeting MISQ, ISR, and Management Science (IS section).

## Stage 0 — Contribution Audit

Before writing a word, answer these four questions. If any is unclear, resolve it first.

1. **What is the central IT artifact or IS phenomenon?** IS papers must be grounded in a specific IT artifact (system, platform, algorithm, digital service) or IS phenomenon (adoption, use, IT-enabled change). Abstract "technology" stories fail.
2. **What is the theoretical contribution?** Choose one: (a) new theory, (b) extension of existing theory, (c) theory application to new context, (d) theory testing/replication. Know which — reviewers will ask.
3. **What is the empirical or design contribution?** Know the method and what it uniquely enables: survey, experiment, archival, design science, econometrics, simulation, qualitative.
4. **What does this paper change for IS research or practice?** If the honest answer is "not much," reframe or reconsider.

## Stage 1 — Venue Selection

Choose venue before deep drafting. Each journal has distinct tolerance for theory vs. empirics vs. design.

| Signal | Lean MISQ | Lean ISR | Lean MS-IS |
|--------|-----------|----------|------------|
| Theory-forward, pluralistic method | ✓ | | |
| Tight hypothetico-deductive, survey/experiment | | ✓ | |
| Causal identification, economics framing | | | ✓ |
| Design science, IT artifact evaluation | ✓ | | |
| Computational methods, large-scale data | | ✓ | ✓ |
| Behavioral theory, organizational IS | ✓ | ✓ | |
| Markets, platforms, economic mechanisms | | | ✓ |

See `misq-playbook`, `isr-playbook`, `ms-is-playbook` for venue-specific depth.

## Stage 2 — Theory Scaffolding

IS papers live or die on theory. Do this before writing the intro.

**Pick one primary theory.** Resist stacking 3–4 theories. Reviewers read stacked theories as conceptual confusion. One theory, used rigorously, outperforms three theories used loosely.

**Common IS theory families:**
- Behavioral/cognitive: TAM, TPB, social cognitive theory, cognitive fit
- Organizational: institutional theory, resource-based view, dynamic capabilities
- Economic: information asymmetry, transaction cost economics, signaling, two-sided markets
- Sociotechnical: structuration, sociomateriality, affordance theory
- Design-oriented: design science research methodology (DSRM), action design research

**Theory-to-contribution mapping:**
- If testing theory in new IS context → contribution is boundary condition or moderator evidence
- If extending theory with IS construct → contribution is theoretical refinement
- If theory predicts artifact design → contribution is design principle + evaluation
- If theory is wrong in IS context → contribution is theoretical challenge (high bar — must be airtight)

## Stage 3 — Paper Structure

### Introduction (1.5–2 pages)

Open with the IS phenomenon or practical problem. Establish that existing work does not fully address it. State your approach and contributions explicitly. End with a roadmap paragraph.

Do NOT open with generic "technology is everywhere" statements. Reviewers skip these. Open with the specific gap.

Contributions statement format:
```
This paper makes three contributions. First, ... Second, ... Third, ...
```
Be concrete. Avoid "we provide insight into" — state what you find and why it matters.

### Literature Review / Theoretical Background

Purpose: establish what is known, expose the gap, and introduce your theoretical lens.

- Review the IS literature, not the general management literature
- Cite the papers reviewers expect to see — missing a canonical IS paper is a rejection signal
- End with an explicit gap statement and research questions

### Hypotheses / Propositions / Design Principles

Match your theory to your method:
- Hypothetico-deductive → formal H1, H2, ... with theoretical justification per hypothesis
- Design science → design principles derived from kernel theory
- Qualitative/interpretive → research questions, not hypotheses

Each hypothesis needs: theoretical mechanism (why), directional prediction (what), and boundary conditions (when/who).

### Methodology

IS reviewers scrutinize methods. Address these proactively:

**For surveys/experiments:**
- Sample size, source, response rate
- Common method bias mitigation (Harman's test alone is no longer sufficient — use procedural remedies)
- Construct validity: convergent, discriminant, nomological
- Survey instrument: pilot, item sources, Likert anchors

**For archival/econometric:**
- Data source and time window
- Variable operationalization and proxies
- Endogeneity threats and identification strategy (IV, DiD, RD, matching)
- Robustness checks required

**For design science:**
- Problem instance and meta-requirements
- Artifact description (not just overview — enough to replicate)
- Evaluation against naturalistic or controlled setting
- Design principles formalized, not just implied

**For qualitative/interpretive:**
- Research site access and informant count
- Data triangulation
- Coding scheme and inter-rater reliability
- Theory-to-data linkage explicit

### Results

Report what the data show, not what you wanted to find. For quantitative work: effect sizes, confidence intervals, model fit statistics. For qualitative: representative quotes tied to codes and themes.

### Discussion

Structure: (1) summary of findings, (2) theoretical contributions, (3) practical implications, (4) limitations, (5) future research.

Do NOT merely restate results. Each contribution point must say something beyond "we found X" — it must say what X means for theory or practice.

### Conclusion

One tight page. Restate the central finding and its significance. No new material.

## Stage 4 — Revision Loop

IS journals have long revision cycles (12–24 months). Treat each R&R as a new submission.

**On receiving reviews:**
1. Read all three reviews before responding to any
2. Identify the shared concern (usually one meta-issue underlying multiple reviewer complaints)
3. Address the meta-issue structurally — do not patch surface comments without fixing the root

**Response letter format:**
- Separate response letter from revised manuscript
- Quote each reviewer comment verbatim, then respond
- Flag all manuscript changes with page/line numbers
- Use bold or color to mark text changes in the manuscript

**Tone:** Professional, collegial, never defensive. "We thank Reviewer 2 for raising this concern; it has led to a substantive improvement."

## Stage 5 — Pre-Submission Audit

Run `is-submission-audit` or check manually:
- [ ] Abstract within word limit (MISQ: 150 words; ISR: 150 words; MS: structured abstract)
- [ ] Blind review: all author identifiers removed from manuscript and properties
- [ ] References formatted per journal style (AIS style for MISQ/ISR; INFORMS for MS)
- [ ] Tables/figures embedded and also provided as separate files if required
- [ ] Cover letter states: contribution claim, why this journal, no concurrent submission elsewhere
- [ ] Manuscript within page limits (MISQ: no hard limit but 40–50 pages typical; ISR: similar; MS: ~35 pages)
