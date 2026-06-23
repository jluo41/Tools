# ISR Style Profile (imitate this)

Distilled language style and preferences to imitate when writing or editing an ISR
manuscript. This is a STARTER from ISR conventions; ENRICH it from the actual papers
stored in `exemplars/` as they are added (pull real sentences and mirror their
shapes).

## Abstract

- <=150 words, unstructured prose (not headed sections).
- Arc: IS phenomenon and why it matters -> what is not understood -> approach
  (data / identification strategy) -> theoretical contribution + empirical finding.
- End on the contribution, not the method.

## Contribution statement

- One crisp sentence by type:
  - Theoretical: "We identify [mechanism] as a previously overlooked driver of [IS
    phenomenon], and show that [moderator] changes this relationship under
    [condition]."
  - Empirical: "We provide the first large-scale causal evidence that [IT
    artifact/policy] affects [outcome], using [identification strategy]."
  - Methodological-IS: "We introduce [method/measure] that enables IS researchers to
    [capability], and validate it in the context of [IS phenomenon]."
- Say what is new (mechanism / moderator / boundary / first causal evidence); avoid
  incremental restatements of an already-established mechanism.

## Hypotheses

- Each hypothesis traces to a named theoretical mechanism, then a directional
  prediction; add the boundary or scope condition if relevant.
- Pattern: "Drawing on [theory], we argue [causal logic for why X leads to Y in this
  IS context]; thus H1: X is positively associated with Y."
- Avoid tautologies ("users who perceive ease of use will adopt"), hypotheses with
  no named theoretical antecedent, and long undifferentiated H1-H12 lists (reads as
  fishing).

## Causality honesty

- Match claim language to design. With clean identification (DiD, IV, RD, matching,
  natural experiment), state the causal claim and name the strategy.
- If causal identification is not achievable, be explicit: frame as correlational
  with strong controls, discuss endogeneity threats directly, and position as
  motivation for future causal work. Reviewers prefer honesty over overclaimed
  causality.

## Psychometrics phrasing (surveys)

- Report CFA (not EFA alone); AVE, composite reliability, Cronbach's alpha per
  construct; discriminant validity by Fornell-Larcker AND HTMT; common-method-bias
  procedural remedies plus statistical checks; non-response (early vs late) checks.
- State each as a method executed, not a result narrated.

## Sentences

- Declarative, theory-forward; define IS constructs precisely on first use.
- Position against IS literature, not just management or economics.
- Minimal hype; no buzzword stacks; one idea per sentence.

## Discussion

- Restate the theoretical contribution first, then implications for IS theory and
  practice, then a dedicated limitations paragraph (endogeneity threats, causality
  scope), then conclusion.

## Intro recipe

```
[Important IS phenomenon and why it matters]. Prior work has established [what is known].
However, [specific gap - mechanism, boundary condition, causal direction unclear, or no large-scale evidence].
We address this by [approach], using [data/method]. We find [key result] and show that [implication for theory].
```

## Tone & preferences

- Measured, theory-centered, identification-aware.
- Cite foundational IS work when relevant; engage IS literature, not only adjacent
  fields.
- Reporting: method executed by its own standards (psychometrics for surveys; clean
  identification with parallel-trends / first-stage F / balance tables for archival;
  power and manipulation checks for experiments).

## To enrich from `exemplars/`

- [ ] Pull 3-5 real ISR contribution sentences (theoretical / empirical /
  methodological-IS); list them as patterns to mirror.
- [ ] Record each exemplar's hypothesis-phrasing pattern (mechanism -> prediction).
- [ ] Record how each exemplar states its identification strategy and hedges
  causality.
- [ ] Record the abstract word budget and arc actually used.
- [ ] Note recurring intro and discussion section moves specific to ISR.
