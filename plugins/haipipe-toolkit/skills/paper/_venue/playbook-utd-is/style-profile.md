# UTD-IS Family Style Profile (imitate this)

Distilled language style and preferences to imitate when writing or editing a UTD-IS
manuscript for MISQ, ISR, or MS-IS. The shared IS style applies to all three; the
per-journal subsections capture where the outlets diverge. This is a STARTER from IS
conventions; ENRICH it from the actual papers stored in `exemplars/<journal>/` as
they are added (pull real sentences and mirror their shapes).

## Shared IS style (all three journals)

### Sentences
- Declarative, theory-forward; define IS constructs precisely on first use.
- Position against IS literature, not just management, economics, or CS.
- Minimal hype; no buzzword stacks; one idea per sentence.

### Contribution statement
- State the single contribution crisply (one sentence or one tight paragraph).
- Name what is new (construct / mechanism / moderator / boundary / first causal
  evidence / equilibrium / structural primitive).
- Avoid "future research should..." as a stand-in for actual contribution; avoid
  incremental restatements of an already-established mechanism.

### Hypotheses
- Each hypothesis traces to a named theoretical mechanism, then a directional
  prediction; add the boundary or scope condition if relevant.
- Pattern: "Drawing on [theory], we argue [mechanism / causal logic for why X leads to
  Y in this IS context]; thus H1: X is positively associated with Y."
- Avoid tautologies ("users who perceive ease of use will adopt"), hypotheses with no
  named theoretical antecedent, and long undifferentiated H1-H12 lists (reads as
  fishing).

### Causality honesty
- Match claim language to design. With clean identification (DiD, IV, RD, matching,
  natural experiment), state the causal claim and name the strategy.
- If causal identification is not achievable, frame as correlational with strong
  controls, discuss endogeneity threats directly, and position as motivation for
  future causal work. Never present correlations in Results and claim causality in
  Discussion. Reviewers prefer honesty over overclaimed causality.

### Psychometrics phrasing (surveys)
- Report CFA (not EFA alone); AVE, composite reliability, Cronbach's alpha per
  construct; discriminant validity by Fornell-Larcker AND HTMT; common-method-bias
  procedural remedies plus statistical checks; non-response (early vs late) checks.
- State each as a method executed, not a result narrated.

### Discussion
- Restate the contribution first, then implications for IS theory and practice, then a
  dedicated limitations paragraph, then conclusion.

### Tone & reporting
- Measured, theory-centered, discipline-aware.
- Method executed by its own standards: CMB checks for surveys; clean identification
  (parallel-trends / first-stage F / balance tables) for archival; power and
  manipulation checks for experiments; Hevner/Gregor for design science; complete
  proofs and justified assumptions for analytical models.

---

## Per-journal style notes

### MISQ (theory-forward, pluralistic)
- **Abstract**: <= 150 words, unstructured prose. Arc: IS phenomenon and why it
  matters -> what is not understood -> approach -> theoretical contribution +
  empirical finding. End on the contribution, not the method.
- **Contribution**: one crisp paragraph answering "what is the theoretical
  contribution?". Name the theory; say what is new (construct / mechanism / boundary /
  resolved tension).
- **Theory**: one primary theory used rigorously; resist stacking 3-4.
- **Cite** foundational IS work when relevant (DeLone & McLean, Venkatesh,
  Orlikowski, Walsham).

### ISR (tight theory -> hypotheses -> causal empirics)
- **Abstract**: <= 150 words, unstructured prose. Arc: IS phenomenon -> gap ->
  approach (data / identification strategy) -> theoretical + empirical contribution.
- **Contribution**, one crisp sentence by type:
  - Theoretical: "We identify [mechanism] as a previously overlooked driver of [IS
    phenomenon], and show that [moderator] changes this relationship under
    [condition]."
  - Empirical: "We provide the first large-scale causal evidence that [IT
    artifact/policy] affects [outcome], using [identification strategy]."
  - Methodological-IS: "We introduce [method/measure] that enables IS researchers to
    [capability], and validate it in the context of [IS phenomenon]."
- **Intro recipe**:
  ```
  [Important IS phenomenon and why it matters]. Prior work has established [what is known].
  However, [specific gap - mechanism, boundary condition, causal direction unclear, or no large-scale evidence].
  We address this by [approach], using [data/method]. We find [key result] and show that [implication for theory].
  ```
- Limitations are explicit about endogeneity threats and causality scope.

### MS-IS (economic / analytical / formal-model)
- **Abstract**: structured, labeled sections, under 200 words, 1-3 sentences each.
  Labels: Problem definition -> Academic/Practical Relevance -> Methodology ->
  Results -> Managerial Implications. End on what decision-makers should do, not on
  the method.
- **Contribution**: one crisp paragraph naming the economic mechanism or analytical
  result (characterized equilibrium / specified mechanism / identified causal effect /
  recovered structural primitive). For market/platform work state the welfare
  consequence (consumer surplus / total welfare), not just firm profit.
- **Intro recipe (use the matching one)**:
  - Analytical:
    ```
    [Market failure or coordination problem in an IS context].
    This problem matters because [economic significance].
    We model [agents, decisions, information structure] and characterize [equilibrium].
    We find [key result] and show that [managerial/policy implication].
    ```
  - Empirical:
    ```
    [Economic mechanism operating through an IT artifact or digital market].
    Prior work has [established X] but has not [identified causal effect / resolved mechanism / generalized].
    We exploit [natural experiment / identification strategy] using [data].
    We find [effect size and direction] and show that the mechanism operates through [channel].
    ```
- **Modeling and notation discipline**: model self-contained and internally
  consistent; all proofs in text or appendix; state every assumption explicitly and
  justify it economically; state results as numbered Propositions / Theorems; report
  comparative statics; provide welfare analysis for market/platform papers; derive
  managerial/policy implications FROM the formal results, not asserted separately.
- **Sentences**: mechanism-first; define constructs by their economic interpretation
  (adoption costs, switching costs, information uncertainty, complementarity). Avoid
  IS-insider language (TAM, UTAUT) in the abstract and introduction; MS readers may
  not know it. Position against economics / OR / management-science literature, not IS
  only.

---

## To enrich from `exemplars/` (tag findings by journal)

- [ ] Pull 3-5 real contribution sentences per journal (MISQ theoretical; ISR
  theoretical / empirical / methodological-IS; MS-IS economic); list them as patterns
  to mirror.
- [ ] Record each exemplar's hypothesis-phrasing pattern (mechanism -> prediction).
- [ ] Record how each ISR/MS-IS empirical exemplar states its identification strategy
  and hedges causality.
- [ ] Record each MS-IS analytical exemplar's Proposition/Theorem phrasing and how
  welfare is stated.
- [ ] Record the abstract word budget and arc actually used (MISQ/ISR prose <= 150 w;
  MS-IS structured < 200 w).
- [ ] Note recurring intro and discussion section moves specific to each journal.
