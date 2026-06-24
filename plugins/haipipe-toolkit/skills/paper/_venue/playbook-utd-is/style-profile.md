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

## Mined from `exemplars/` (real patterns to mirror, tagged by journal)

Distilled 2026-06-24 from the three stored exemplars. Quote the SHAPE, not the
content. Each pattern names the exemplar it came from; the `exemplars/<journal>/...`
tags are short slugs whose PDFs live locally under
`_WorkSpace/HAIToolLib/1-ExemplarLib/utd-is/<journal>/` (gitignored). Open them there
to re-mine.

### MISQ -- Liu, Li & Xu (2021), *Assessing the Unacquainted* [`exemplars/misq/liu-2021-...`]

The closest analogue in the corpus: Big-Five inferred from text via deep learning,
then linked to a behavioral outcome. Mirror it for this paper's MISQ submission.

- **ML-measure is the ENABLER, not the claim.** The abstract leads with the question
  ("who is more likely to provide future helpful reviews"), then: "It trains a deep
  learning model to infer a reviewer's personality traits. *This enables* analyses to
  reveal the role of personality traits in review helpfulness." The method enables; the
  theoretical relationship is the contribution. This is the family's enabler rule shown
  in practice.
- **Intro "what is new" move (MISQ signature).** The intro closes its framing with one
  literal sentence: "Below, we introduce what we do, what is new, and how we do it."
  Then it delivers exactly those three.
- **Abstract**: ~150 w, unstructured prose, question -> approach -> findings, ends on
  "Theoretical and practical implications are discussed." No method bragging at the end.
- **Hypothesis phrasing (mechanism -> directional prediction), one construct per H**:
  define the construct (1-2 sentences, cite McCrae/Costa) -> route through a named
  mechanism stream (the paper uses three: knowledge-sharing propensity, reviewer
  persuasiveness, opinion-leadership propensity) -> "Therefore, we expect that reviewers
  high in openness will be more likely to become opinion leaders, meaning that their
  reviews will be perceived as more helpful." -> "**H1: Reviewer openness is positively
  related to review helpfulness.**" Clean, directional, no H1-H12 fishing list.
- **Discussion** leads "Implications for Research": "Our work joins the burgeoning
  scientific investigations ... that apply new methods of assessing unacquainted
  individuals," then a scope/generalization paragraph ("Although we only apply ... there
  is a wide scope of contexts where such methods are applicable").

### ISR (empirical, identification-honest) -- Bao & Bardhan (2021), *ACO Performance & Health IT* [`exemplars/isr/bao-bardhan-2021-...`]

- **Abstract arc**: phenomenon (ACO under the ACA) -> "we study whether (a) ... and (b)
  ..." -> data + method ("a nationwide sample of ACO data using a two-stage approach
  based on data envelopment analysis and econometric estimation") -> "We observe that
  ..." -> ends on policy implication ("healthcare policy needs to incorporate
  appropriate incentives ...").
- **Gap / first-study move**: "To the best of our knowledge, ours is one of the first
  studies to explore ..." (state the void, then claim the slot precisely, not grandly).
- **Contribution sentence**: "We contribute to the extant literature on the role of
  effective IT use in value-based healthcare delivery ... Our context-specific
  conceptualization of health IT use highlights the role of IT-enabled information
  integration as *the primary mechanism* in resolving tradeoffs ..." -- one named
  mechanism, foregrounded.
- **Causality honesty (the ISR move to imitate)**: results use guarded language
  ("positive association," "we observe"); a dedicated **Endogeneity Concerns**
  subsection states the threat in the reviewer's voice ("One may argue that MU
  achievement is endogenous ..."), then "To mitigate endogeneity concerns, we deploy an
  instrument variable (IV) approach," names the two instruments, and **reports the
  weak-instrument test statistic** (15.64, p < 0.01). Identification is layered as
  robustness (IV + Heckman + a Difference-in-Differences analysis on ACO participation +
  propensity-score matching), not asserted once.

### ISR (methodological-IS, labeled 3-way contribution) -- Zhang, Hao, Zhan & Wu (2026), *Physician Reviews & Consultation Demand* [`exemplars/isr/zhang-2026-...`]

Same domain as this paper (physician reviews + a language model that scores them).

- **Structured 3-way contribution (a clean ISR template)**: "Our research contributes
  in three ways. **Methodologically**, we develop an SLM (Doc-BERT) ... and demonstrate
  that a task-aligned, domain-tuned SLM can outperform a wide range of existing NLP
  approaches, including recent general LLMs ... **Theoretically**, we adapt and refine a
  healthcare service quality assessment framework ... rarely applied in information
  systems research. **Empirically**, we identify specific dimensions of service quality
  that most strongly predict online consultation demand, offering actionable guidance
  ..." Label each contribution by TYPE.
- **Measurement-model-as-enabler**: "Our SLM operationalizes a quality evaluation
  framework ... to extract providers' service quality scores from online physician
  reviews, *and then* we estimate the relationship between the quality scores and the
  online consultation demand." The model produces the measure; the estimated
  relationship is the empirical contribution.
- **Abstract**: prose (ISR style), opens on the practical tension (LLMs powerful but
  expensive in specialized domains), closes on actionable guidance for practitioners.

### MS-IS

- Not yet mined as a full-text exemplar. `references/lu2018can` (online physician
  ratings, cardiac surgeons) is the nearest pointer; add a stored PDF to
  `exemplars/ms-is/` to mine Proposition/Theorem phrasing and welfare reporting.

---

## To enrich from `exemplars/` (tag findings by journal)

- [x] Pull 3-5 real contribution sentences per journal -- done for MISQ (Liu) and ISR
  (Bao; Zhang's labeled 3-way). MS-IS pending an `exemplars/ms-is/` PDF.
- [x] Record each exemplar's hypothesis-phrasing pattern -- MISQ mechanism -> "H1: X is
  positively related to Y" captured from Liu.
- [x] Record how each ISR empirical exemplar states its identification strategy and
  hedges causality -- captured from Bao (Endogeneity Concerns subsection + IV +
  weak-instrument F + DiD + PSM, guarded "association" language).
- [ ] Record an MS-IS analytical exemplar's Proposition/Theorem phrasing and how welfare
  is stated -- blocked until a stored MS-IS exemplar exists.
- [x] Record the abstract word budget and arc actually used -- MISQ (Liu) and ISR (Bao,
  Zhang) prose arcs captured above.
- [x] Note recurring intro and discussion section moves -- MISQ "what we do / what is
  new / how" + "Implications for Research"; ISR "to the best of our knowledge, one of
  the first" gap move.
