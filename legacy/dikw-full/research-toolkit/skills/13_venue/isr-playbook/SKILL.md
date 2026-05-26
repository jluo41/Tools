---
name: isr-playbook
description: Use when preparing or positioning a paper for Information Systems Research (ISR). Invoke for venue fit assessment, framing decisions, and ISR-specific reviewer expectations around theory-driven empirics, causal identification, and quantitative rigor. Use proactively when the user is writing an IS paper with survey, experiment, archival, or econometric methods targeting ISR.
---

# ISR Playbook

## Overview

Information Systems Research (ISR), published by INFORMS, is the premier outlet for rigorous theory-driven empirical IS research. It sits closer to the social science and economics end of the IS spectrum than MISQ.

ISR values tight theory-hypotheses-evidence chains and strong methodology. Pluralism exists but is narrower than MISQ — interpretive work appears rarely, and design science even less. The dominant mode is: derive hypotheses from theory, test with clean data, interpret findings back to theory.

Average time to first decision: 3–5 months. Average R&R cycles: 2–3.

## When ISR Is the Right Venue

ISR is right when:
- The paper has tight hypotheses derived from economic, behavioral, or organizational theory
- The empirical strategy is strong: causal identification, large-scale archival data, well-powered experiment
- The theoretical contribution is in specifying mechanisms, moderators, or boundary conditions — not building new theory wholesale
- Computational or algorithmic methods are used to answer an IS research question (not just a methods paper)
- The phenomenon is empirically important in IS (platforms, IT adoption, digital markets, IT governance)

ISR is NOT right when:
- The primary contribution is theoretical framework building without strong empirics
- The method is qualitative or interpretivist
- The paper is design science focused
- The contribution is mostly practical with thin theory

## Theory and Hypothesis Standards

ISR requires that every hypothesis traces to a clear theoretical mechanism.

**Required per hypothesis:**
1. The theoretical basis (name the theory, cite the core source)
2. The causal logic (why does X lead to Y in this IS context)
3. The directional prediction (H1: X is positively associated with Y)
4. The boundary condition or scope condition if relevant

**Avoid:**
- Hypotheses that are tautological ("users who perceive ease of use will adopt")
- Hypotheses without a named theoretical antecedent
- Long lists of hypotheses (H1–H12) without tight theoretical organization — this signals fishing

## Methodology Standards by Method Type

### Survey Research

ISR reviewers apply strict psychometric standards:
- CFA (confirmatory factor analysis) required; EFA alone insufficient
- Report AVE, composite reliability, Cronbach's alpha per construct
- Discriminant validity: Fornell-Larcker criterion AND HTMT ratio
- Common method bias: procedural remedies (temporal separation, confidentiality assurance) plus statistical checks (CFA marker variable, ULMC)
- Sample: minimum 200+ for structural models; report power analysis or justify
- Non-response bias: early vs. late respondent comparison required

### Lab and Field Experiments

- Report power analysis and achieved power
- Manipulation checks required with statistics
- Control conditions clearly described
- CONSORT-style flow diagram for participant allocation recommended
- Demand artifact checks for lab studies

### Archival / Econometric

ISR has raised its causal identification bar significantly since 2015. Correlational findings with OLS and controls alone are increasingly insufficient for top IS journals.

Preferred identification strategies:
- Difference-in-differences (DiD): parallel trends test required, event study preferred
- Instrumental variables (IV): first-stage F > 10, exclusion restriction justified theoretically
- Regression discontinuity (RD): bandwidth sensitivity, McCrary density test
- Matching (PSM, CEM): balance tables before and after matching, ATT vs. ATE clarity
- Natural experiments: clearly articulated exogenous variation source

If causal identification is not achievable, be explicit: frame as correlational with strong controls, discuss endogeneity threats directly, and position as motivation for future causal work. Reviewers prefer honesty over overclaimed causality.

### Computational and ML Methods

ISR increasingly accepts papers that use ML/AI methods to answer IS questions. Standards:

- The IS research question must drive the methodology, not the other way around
- Interpretability matters: black-box prediction alone is not a contribution; explain what the model reveals about the IS phenomenon
- Benchmark against IS-relevant baselines, not just ML benchmarks
- Validate on held-out data; report out-of-sample performance
- Theory must frame what patterns the model is expected to find and why

## Framing the Contribution

ISR contributions are typically framed as:

**Theoretical:** "We identify [mechanism] as a previously overlooked driver of [IS phenomenon], and show that [moderator] changes this relationship under [condition]."

**Empirical:** "We provide the first large-scale causal evidence that [IT artifact/policy] affects [outcome], using [identification strategy]."

**Methodological-IS:** "We introduce [method/measure] that enables IS researchers to [capability], and validate it in the context of [IS phenomenon]."

ISR intro recipe:
```
[Important IS phenomenon and why it matters]. Prior work has established [what is known]. 
However, [specific gap — mechanism, boundary condition, causal direction unclear, no large-scale evidence]. 
We address this by [approach], using [data/method]. We find [key result] and show that [implication for theory].
```

## Submission Mechanics

- **Submission system**: INFORMS PubsOnline (Manuscript Central)
- **Abstract**: 150 words maximum; structured abstract not required
- **Blind review**: strict — remove all identifiers
- **Style guide**: INFORMS journal style (author-date citations, reference format)
- **Page limit**: ~35 pages double-spaced text excluding references and appendices; appendices for robustness checks and instrument items
- **Cover letter**: contribution claim, target department if applicable (IS, OM, or MS for hybrid), confirmation of no concurrent submission

## Common Rejection Reasons

1. Hypotheses not derived from theory — just predictions based on intuition
2. Endogeneity not addressed in archival studies
3. Survey psychometrics incomplete (missing discriminant validity, CMB checks)
4. Effect sizes small with no theoretical or practical significance argument
5. Contribution incremental — mechanism already established in related work
6. Literature review engages management journals but misses key IS papers
7. Results discussion overclaims causality from correlational design
8. Robustness checks absent or superficial
