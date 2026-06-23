# MS-IS Style Profile (imitate this)

Distilled language style and preferences to imitate when writing or editing a
Management Science (IS department) manuscript. This is a STARTER from MS-IS
conventions; ENRICH it from the actual papers stored in `exemplars/` as they are
added (pull real sentences and mirror their shapes).

## Abstract

- Structured, three-plus labeled sections; total under 200 words; 1-3 sentences each.
- Labels: Problem definition -> Academic/Practical Relevance -> Methodology ->
  Results -> Managerial Implications.
- End on what decision-makers should do with the result, not on the method.

## Contribution statement

- One crisp paragraph naming the economic mechanism or analytical result.
- Say what is new: a characterized equilibrium, a specified mechanism, an identified
  causal effect, or a recovered structural primitive.
- For market/platform work, state the welfare consequence (consumer surplus / total
  welfare), not just firm profit.

## Intro recipe (use the matching one)

Analytical paper:
```
[Market failure or coordination problem in an IS context].
This problem matters because [economic significance].
We model [agents, decisions, information structure] and characterize [equilibrium].
We find [key result] and show that [managerial/policy implication].
```

Empirical paper:
```
[Economic mechanism operating through an IT artifact or digital market].
Prior work has [established X] but has not [identified causal effect / resolved mechanism / generalized].
We exploit [natural experiment / identification strategy] using [data].
We find [effect size and direction] and show that the mechanism operates through [channel].
```

## Modeling and notation discipline

- Model self-contained and internally consistent; all proofs in text or appendix.
- State every assumption explicitly and justify it economically.
- State results as numbered Propositions / Theorems; report comparative statics.
- Provide welfare analysis for market/platform papers, not firm profit alone.
- Derive managerial and policy implications FROM the formal results, not asserted
  separately.

## Identification honesty (empirical)

- Economic theory motivates both the hypotheses AND the identification strategy.
- Be explicit about the identifying variation; test parallel trends for DiD, report
  the first stage and instrument relevance for IV, show the discontinuity for RD.
- Prefer structural estimation when feasible (recover primitives); reduced form is
  acceptable when identification is credible and theory tightly frames the mechanism.
- Never present correlations in Results and then claim causality in Discussion.

## Sentences

- Declarative, mechanism-first; define constructs by their economic interpretation
  (adoption costs, switching costs, information uncertainty, complementarity).
- Position against economics / OR / management-science literature, not IS only.
- Avoid IS-insider language (TAM, UTAUT) in the abstract and introduction; MS readers
  may not know it.
- Minimal hype; no buzzword stacks; one idea per sentence.

## Discussion

- Lead with managerial and policy implications derived from the results, then a
  dedicated limitations paragraph, then conclusion.

## Tone & preferences

- Measured, economics-centered, decision-science-aware.
- Cite foundational platform / IT-economics work when relevant.
- Reporting: model executed by its own standards (complete proofs, justified
  assumptions, comparative statics, welfare); empirics by clean, theory-motivated
  identification.

## To enrich from `exemplars/`

- [ ] Pull 3-5 real MS-IS economic-contribution sentences; list them as patterns to mirror.
- [ ] Record each exemplar's Proposition/Theorem phrasing and how welfare is stated.
- [ ] Record each empirical exemplar's identification-and-mechanism sentence pattern.
- [ ] Record the structured-abstract section budget and arc actually used.
- [ ] Note recurring intro and discussion section moves specific to MS-IS.
