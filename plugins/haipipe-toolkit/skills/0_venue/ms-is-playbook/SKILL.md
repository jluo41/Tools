---
name: ms-is-playbook
description: Use when preparing or positioning a paper for the Information Systems department of Management Science (MS). Invoke for venue fit assessment, framing the economic or analytical angle of IS research, and MS-specific reviewer expectations around formal modeling, causal econometrics, and market/platform mechanisms. Use proactively when the user is writing an IS paper involving platforms, digital markets, IT economics, mechanism design, or analytical models.
---

# Management Science — IS Section Playbook

## Overview

Management Science (MS), published by INFORMS, is a top-ranked interdisciplinary journal covering Operations Research, Operations Management, Marketing, Finance, and Information Systems. The IS department of MS sits at the intersection of economics, decision science, and information technology.

MS-IS papers are typically more analytical or economics-oriented than MISQ or ISR. The journal rewards rigorous formal modeling AND/OR credible causal identification. Behavioral surveys without strong economic framing rarely fit MS-IS.

Average time to first decision: 2–4 months. Average R&R cycles: 2.

## When MS-IS Is the Right Venue

MS-IS is right when:
- The paper uses formal economic modeling (game theory, mechanism design, contract theory, information economics)
- The empirical strategy features strong causal identification with economic framing (platforms, markets, IT investment, pricing)
- The IS phenomenon is best explained through economic mechanisms (incentives, information asymmetry, two-sided markets, network effects)
- The paper bridges IS with operations management, supply chain, or finance through IT
- The paper involves algorithmic or optimization contributions motivated by an IS research question
- Computational social science at scale with clear economic or behavioral mechanism

MS-IS is NOT right when:
- The primary frame is behavioral IS theory (TAM, social cognitive) without economic modeling
- The method is qualitative/interpretive
- The contribution is a new IS construct or measurement scale
- The paper is design science

## Theory and Modeling Standards

MS-IS papers often use formal models. Standards differ significantly from MISQ/ISR.

**For analytical/theory papers:**
- Model must be self-contained and internally consistent — all proofs either in text or appendix
- Assumptions must be stated explicitly and justified economically
- Results stated as numbered Propositions or Theorems with proofs
- Comparative statics required — show how equilibria change with key parameters
- Welfare analysis often expected (not just firm profit — consumer surplus, total welfare)
- Managerial and policy implications derived from formal results, not asserted separately

**For empirical papers:**
- Causal identification is the norm, not the exception
- Economic theory should motivate both the hypotheses AND the identification strategy
- Structural estimation increasingly valued — recover primitives, not just reduced-form effects
- Reduced-form papers remain acceptable if identification is credible and theory tightly frames the mechanism

**For hybrid (model + empirics):**
- Model generates predictions; empirics test them
- This is the gold standard for MS-IS; if data can validate model predictions, do so

## Key IS Topics at MS

MS-IS editors have historically been receptive to:
- **Platform economics**: two-sided markets, platform design, multi-homing, network effects
- **IT investment and value**: returns to IT, IT and firm performance, complementarity with HR/org factors
- **Digital markets and e-commerce**: pricing, recommendation systems, review platforms, search
- **Privacy and security economics**: data sharing, breach economics, regulation effects
- **Sharing economy and gig platforms**: labor markets, algorithmic management, pricing mechanisms
- **AI and automation economics**: labor displacement, firm-level AI adoption, human-AI collaboration
- **FinTech and digital finance**: blockchain, robo-advisors, digital payments
- **Healthcare IT economics**: EHR adoption, telemedicine value, health information exchange

If your IS paper has economic mechanisms in any of these areas, MS-IS is a strong candidate.

## Framing the Contribution

MS-IS readers come from economics, OR, and management science. Frame contributions using their vocabulary.

**Analytical paper intro recipe:**
```
[Market failure or coordination problem in an IS context]. 
This problem matters because [economic significance]. 
We model [agents, decisions, information structure] and characterize [equilibrium]. 
We find [key result] and show that [managerial/policy implication].
```

**Empirical paper intro recipe:**
```
[Economic mechanism operating through an IT artifact or digital market].
Prior work has [established X] but has not [identified causal effect / resolved mechanism / generalized to context].
We exploit [natural experiment / identification strategy] using [data].
We find [effect size and direction] and show that the mechanism operates through [channel].
```

Avoid IS-insider language (TAM, UTAUT) in the abstract and introduction — MS readers may not know these. Use constructs with economic interpretations: adoption costs, switching costs, information uncertainty, complementarity.

## Structured Abstract

MS requires a structured abstract with three labeled sections:

```
**Problem definition**: [The IS phenomenon and why it poses an economics/decision problem]
**Academic/Practical Relevance**: [Why this matters for theory and practice]  
**Methodology**: [Modeling approach and/or data and identification strategy]
**Results**: [Key findings, equilibrium characterizations, effect sizes]
**Managerial Implications**: [What decision-makers should do with this]
```

Each section: 1–3 sentences. Total abstract: under 200 words.

## Submission Mechanics

- **Submission system**: INFORMS PubsOnLine
- **Structured abstract**: required (see above)
- **Blind review**: strict — remove all identifiers
- **Style guide**: Management Science style (author-year citations, INFORMS reference format)
- **Page limit**: ~35 pages text; online appendix for proofs, robustness, instrument items
- **Area submission**: select Information Systems area when submitting
- **Cover letter**: state the IS phenomenon, modeling/empirical approach, and primary contribution; note if cross-listed (e.g., IS + OM) and why

## Common Rejection Reasons

1. Economic mechanism missing — empirical finding without formal theory or micro-foundation
2. Identification strategy insufficient — endogeneity not addressed, instrument weak, DiD parallel trends violated
3. Analytical model without empirical validation when data are feasibly available
4. Behavioral IS framing (TAM-based) without economic grounding
5. Contribution to IS literature only — does not speak to broader MS readership in economics or decision science
6. Welfare analysis absent for market/platform papers
7. Proofs incomplete or model assumptions unjustified
8. Results section presents correlations; Discussion section claims causality
