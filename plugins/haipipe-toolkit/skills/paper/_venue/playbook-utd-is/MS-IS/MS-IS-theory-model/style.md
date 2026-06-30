# MS-IS Theory / Model Style Guide

MS-IS papers use formal models more than MISQ or ISR. This section may be titled
"Model," "Theoretical Framework," "Theory and Hypotheses," or "Institutional
Background and Theory" depending on whether the paper is analytical, empirical, or
hybrid. The key differentiator is that MS-IS expects economic micro-foundations, not
IS-theory application (TAM, UTAUT).

## Section title conventions

| Paper type | Typical title | Subsections |
|------------|--------------|-------------|
| Analytical | "Model" or "The Model" | Setup / Assumptions / Benchmark / Extensions |
| Empirical (theory-led) | "Theory and Hypotheses" or "Background and Hypotheses" | Institutional context / Theory / H1 / H2 / H3 |
| Empirical (identification-led) | "Setting and Data" or "Institutional Background" | Background / Data / Variables |
| Hybrid (model + empirics) | "Model" then "Empirical Strategy" | Model section derives predictions; Empirical section tests them |

## Word budget

- Analytical: 3,000-5,000 words (the core of the paper)
- Empirical with theory: 1,500-2,500 words
- Empirical without formal theory: 500-1,000 words (institutional background only)

## Arc by paper type

### Analytical papers

```
2.1  MODEL SETUP
     State the agents, their decision variables, the information structure,
     and the timing. Every assumption stated explicitly and justified
     economically ("We assume X because [economic reason]").

2.2  BENCHMARK / FIRST-BEST
     Solve the benchmark case (full information, no friction, single period).
     State as Lemma or Proposition. This anchors the welfare comparison.

2.3  MAIN MODEL
     Introduce the friction, information asymmetry, or strategic interaction.
     Derive the equilibrium. State as numbered Proposition or Theorem.
     Provide comparative statics: "As [parameter] increases, [outcome]
     [increases/decreases]."

2.4  EXTENSIONS
     Relax assumptions one at a time. Each extension produces a Proposition.
     Welfare analysis: compare total welfare, consumer surplus, and producer
     surplus across regimes.

2.5  DISCUSSION / EMPIRICAL PREDICTIONS
     Translate propositions into testable predictions if the paper is hybrid.
```

### Empirical papers (theory-led)

```
2.1  INSTITUTIONAL BACKGROUND
     Describe the market, platform, or regulatory setting. Specific to the
     context, not a general literature review. Name the key institutional
     features that create the identification opportunity.

2.2  THEORETICAL FRAMEWORK
     Name the economic mechanism (information asymmetry, switching costs,
     moral hazard, complementarity, network effects, signaling). Derive
     directional predictions from the mechanism.
     MS prefers: "The mechanism suggests that..." over "Drawing on [theory],
     we hypothesize that..."

2.3  HYPOTHESES (if used)
     State as H1, H2, H3 with directional predictions. Each traces to a
     named economic mechanism. Keep the list short (2-4 hypotheses).
     Many MS-IS empirical papers skip formal hypotheses and state
     "predictions" informally in the introduction results preview.
```

### Empirical papers (identification-led, as in Cui et al.)

```
2.   SETTING AND [DATA/EXPERIMENTS]
     2.1  Institutional context (what is the technology/market/policy?)
     2.2  Data / Experimental design
     2.3  Variables and outcome measures

     No separate theory section. The economic logic is in the introduction
     (enumerated results) and the identification strategy justification.
```

## Signature moves

### Proposition/Theorem phrasing (analytical)
Numbered formally. State the result, then the intuition in plain language.

```
**Proposition 1.** In the unique symmetric equilibrium, the platform's optimal
commission rate r* is [expression]. Moreover, dr*/d[parameter] > 0.

*Intuition.* When [parameter] increases, [economic logic], leading the platform
to [action].
```

All proofs either in the body (short) or in the Online Appendix (long), with a note:
"All proofs are in the Online Appendix."

### Welfare analysis (market/platform papers)
State consumer surplus, producer surplus, and total welfare. Compare across regimes
(with/without the platform, before/after the policy, competitive vs. monopoly).

```
**Proposition 3** (Welfare). Total welfare under the platform regime exceeds the
direct-search benchmark if and only if [condition]. Consumer surplus is higher
under [regime] while producer surplus is higher under [other regime].
```

### Economic mechanism naming
MS-IS names mechanisms by their economics label, not by IS construct names:

| MS-IS (use this) | MISQ/ISR (avoid in MS) |
|------------------|------------------------|
| switching costs | lock-in, path dependency |
| information asymmetry | information gap |
| moral hazard | agency problem (acceptable in MS too) |
| complementarity | synergy |
| network effects | network externalities (both OK) |
| signaling | quality signaling (OK if formal) |
| adverse selection | market for lemons |
| search costs | search friction |
| two-sided market | multi-sided platform (both OK) |

### Assumption justification
Every modeling assumption explicitly stated AND economically justified. Not "we assume
X for tractability" alone, but "we assume X because [economic reason]; this is standard
in [cite]."

## Paragraph structure (theory-led empirical)

Each theory subsection follows a 4-step pattern per mechanism:

1. **Name the mechanism** (1 sentence): "We argue that [economic mechanism] operates in
   this context."
2. **Cite evidence the mechanism exists** (1-2 sentences): "[Cite] shows that [mechanism]
   affects [outcome] in [related context]."
3. **Argue why it applies HERE** (2-3 sentences): "In our setting, [specific feature]
   activates this mechanism because [logic]."
4. **State the prediction** (1 sentence): "This leads to our [first/second] prediction:
   [directional statement]." Or formally: "H1: [X] is [positively/negatively]
   associated with [Y]."

Citation density: ~0.40-0.50 citations per sentence (slightly lower than MISQ/ISR
because MS-IS relies more on derivation from the model than on citing established
relationships).

## Anti-patterns

- **No IS theory application without economic grounding.** "Drawing on TAM, we argue..."
  is not MS style. MS expects: "Information asymmetry between [agents] creates [friction],
  leading to [prediction]."
- **No long undifferentiated hypothesis lists.** If you have H1-H8, the paper reads as
  fishing. Keep to 2-4 hypotheses with clear economic logic connecting them.
- **No measurement method in the theory section.** How you operationalize the construct
  (LLM, survey, etc.) belongs in Methods. The theory takes the construct as given.
- **No tautological hypotheses.** "Users who value convenience will adopt convenient
  technology" is not a prediction; it is a definition.
- **No assumptions without economic justification.** "We assume for simplicity" is
  insufficient; state the economic reason the assumption is reasonable.

## Contrast with MISQ/ISR

| Dimension | MS-IS | MISQ | ISR |
|-----------|-------|------|-----|
| Dominant framing | Economic mechanism / formal model | IS theory (TAM, UTAUT, etc.) | Named mechanism + hypotheses |
| Formalism | Propositions/Theorems + proofs | Conceptual model + hypotheses | Research model + hypotheses |
| Welfare analysis | Required for platform/market papers | Not expected | Not expected |
| Assumptions | Stated and justified economically | Implicit | Sometimes stated |
| Jargon source | Economics, OR | IS, Psychology, Sociology | IS, Economics |
| Competing predictions | Formal: two regimes compared | Informal: "On the other hand..." | Competing H with evidence |

## Enrichment needs

- [x] Mine an analytical MS-IS paper (e.g., a platform economics or pricing paper) to
  capture exact Proposition/Theorem phrasing and welfare reporting format.
  **RESOLVED**: See Feng 2025 structural model patterns below.
- [x] Mine Shukla et al. (2021) to see how an empirical MS-IS paper with healthcare
  context structures its theory section (WOM mechanisms + physician choice).
  **RESOLVED**: See Huesmann 2025 and Chao/Larkin 2022 healthcare theory patterns below.
- [x] Mine Angst et al. (2010) for the adoption/diffusion identification framework
  used in a theory-led MS-IS empirical paper.
  **RESOLVED**: See Krakowski 2026 behavioral theory pattern below.

---

## Enriched from additional exemplars (2026-06-29)

Sources: 8 published MS papers (Huesmann 2025, Chao/Larkin 2022, Feng 2025, Cui 2025,
Krakowski 2026, de Kok 2025, Chen 2025, Burtch 2026).

### Section title conventions (additional patterns from published papers)

| Paper | Section title | Type |
|-------|-------------|------|
| Huesmann 2025 | "2. Literature and Hypotheses" | Lit review + formal hypotheses |
| Chao/Larkin 2022 | "2. Background" | Institutional background + lit review |
| Feng 2025 | "2. The Role of PBMs in Prescription Drug Markets" | Institutional background |
| Cui 2025 | "2. Setting and Experiments" | Identification-led (no theory section) |
| Krakowski 2026 | "2. Theoretical Background and Hypotheses" | Behavioral theory + hypotheses |
| de Kok 2025 | "2. Generative Large Language Models" | Technology background + comparison |
| Chen 2025 | "2. Literature Review" | Full standalone lit review |
| Burtch 2026 | "2. EnsembleIV: Theory and Algorithm" | Formal method derivation |

### Healthcare-domain theory section: "Literature and Hypotheses" pattern (Huesmann 2025)

Huesmann uses a combined literature-and-hypotheses section common in healthcare
management MS papers:

```
2.   LITERATURE AND HYPOTHESES
     2.1  Related Literature on [Topic]
          Cite the field (healthcare management + behavioral economics).
          State that evidence is mixed. Review positive findings,
          then negative/null findings. End with the unresolved question.

     2.2  Hypothesis Development
          State the economic mechanism informally (status utility,
          social comparison). Derive directional predictions step by step.
          State Hypothesis 1, then Hypothesis 2.
```

### Formal Hypothesis phrasing (from Huesmann 2025, Krakowski 2026)

MS healthcare papers use bold, italicized hypotheses with a descriptive parenthetical
title. The hypothesis statement is followed by sub-parts (a, b, c):

```
**Hypothesis 1** (Ranking System Design and Ability). *Adding a threshold
to a ranking system will affect individuals' effort choices. The direction
of the effect for a given individual depends on whether that individual
can meet the new threshold.*
  a. *For individuals who can reach outcomes both above and below the
     new threshold, effort increases.*
  b. *For individuals who cannot reach outcomes above the new threshold,
     effort decreases.*
  c. *For individuals who cannot reach outcomes below the new threshold,
     effort decreases.*
```

Krakowski uses a simpler format:
```
**Hypothesis 1.** *The combination of human and AI information processing,
all else equal, increases decision performance.*

**Hypothesis 2.** *Tailoring the human-AI interaction context (i.e.,
procedure, authority, training, incentives) to humans' cognitive styles
increases decision performance.*
```

### Formal Result phrasing (from Huesmann 2025)

Results in the body are also formatted as numbered bold/italic blocks that mirror
hypotheses:

```
**Result 1** (Ranking System Design and Ability). *A subject's effort
level depends on the ranking system design and on the subject's
ability type.*
  a. *Effort is increasing in the number of achievable thresholds...*
  b. *The presence of a threshold that a subject cannot surpass tends
     to decrease that subject's effort...*
  c. *The presence of a threshold that a subject is guaranteed to
     surpass does not significantly affect that subject's effort...*
```

### Structural model section (Feng 2025)

Feng 2025 demonstrates the full structural model arc for a healthcare/pharma paper:

```
4.   STRUCTURAL MODEL OF DRUG PRICING IN MARKETS WITH DEMAND INERTIA
     4.1  Model of Demand for Prescription Drugs with Inertia
          - Consumer utility specification with switching cost terms
          - Numbered equations (3), (4), (5) for utility, choice probs,
            market share recursion
          - Model summary figure (Figure 2) with agents and flows

     4.2  Formulary Choice Model
          - PBM objective function combining welfare, spending, exclusion
          - Numbered equation (8) for the optimization problem
          - Set notation for formulary arrangement

     4.3  Bidding for Formulary Placement
          - Manufacturer value function with dynamic programming
          - Numbered equation (10) for Bellman equation
          - Markov perfect equilibrium assumption stated and justified

     4.4  Discussion of Assumptions
          - Each assumption stated, then justified with economic reasoning
          - Limitations of simplifications acknowledged honestly
          - "This assumption is undesirable, but necessary because of
            data limitations and to make estimation feasible."
```

### Lemma/Assumption/Algorithm format (from Burtch 2026)

Methodological MS-IS papers use a formal mathematical structure with numbered
assumptions, lemmas, and algorithms:

```
**Assumption 1.** E[epsilon | X, W] = 0;

**Assumption 2.** Given X-hat^(i) = X + e^(i),
E[epsilon * e^(i) | X, W] = 0, for all i in {1,...,M}.

**Lemma 1** (Nevo and Rosen 2012). *Let Z-tilde = sigma_X * Z -
lambda * sigma_Z * X-hat, then Cov(Z-tilde, u) = 0.*

**Algorithm 1** (Instrumental Variable Transformation Procedure)
  1  **Input:** A pair of individual learners i != j, D_test, and D_unlabel;
  2  Deploy individual learners on D_test to get predictions...
  3  Set X-hat = X-hat_test^(i) and Z = X-hat_test^(j);
  ...
```

### Institutional background section: "Background" pattern (Chao/Larkin 2022)

When the paper exploits a policy change, the Background section serves as the
institutional foundation for the identification strategy:

```
2.   BACKGROUND
     2.1  [Domain Costs/Problem] and [Stakeholder] Interactions
          Describe the market, the actors, the dollar magnitude.
          Heavy citation density (~1 citation per sentence).

     2.2  [Policy/Mechanism] as a Remedy
          Describe the specific policy, its design, and when it was
          implemented. Name advocates and skeptics.

     2.3  Differences from Existing Studies
          For each close competitor (3-5 papers), state in 2-3 sentences:
          what they studied, what they found, and how this paper differs.
          This is a POSITIONING subsection, not a literature review.
```

### Technology background section: method-paper pattern (de Kok 2025, Chen 2025)

Methodological MS papers that introduce a new tool or model use the theory section
to educate the reader about the technology:

```
2.   [TECHNOLOGY NAME]
     2.1  What Are [Tools] and How Do They Work?
          Plain-language explanation for non-specialist readers.
          Basic mechanics in accessible terms.

     2.2  How Do [Tools] Relate to [Existing Methods]?
          Compare architectures, strengths, trade-offs.
          Use a comparison table (Table 1) to position the new
          method vs. existing approaches on key dimensions.

     2.3  Pros and Cons Relative to Current Methods
          2.3.1 Comparison with [Method A]
          2.3.2 Comparison with [Method B]
          Specific examples from prior papers for each comparison.

     2.4  Current Research Using [Tools]
          Survey of recent applications. Organized by task type.
```

Chen 2025 uses a comparison table as a positioning device:

| Method | Feature 1 | Feature 2 | Feature 3 | Feature 4 |
|--------|-----------|-----------|-----------|-----------|
| LDA | | | | |
| CTM | check | | | |
| STM | check | check | check | |
| STS (This paper) | check | check | check | check |

This "this paper fills all gaps" table is a common MS methodological contribution
device.

### Behavioral theory + hypotheses pattern (Krakowski 2026)

Krakowski demonstrates that IS-style behavioral theory IS acceptable in MS when
grounded in organizational design literature (not TAM/UTAUT):

```
2.   THEORETICAL BACKGROUND AND HYPOTHESES
     P1-P3  Name the technology phenomenon (AI augmentation).
            Cite management/org design literature, not IS adoption models.
            State that empirical evidence is "inconclusive."

     H1     Derive from augmentation literature + complementarity argument.
            "The combination of human and AI information processing...
            increases decision performance."

     P4-P6  Introduce the moderating mechanism (cognitive styles,
            microcontingency theory). Name the specific typology
            (Kirton's adaptor-innovator).

     H2     Derive the moderation: "Tailoring the human-AI interaction
            context... to humans' cognitive styles increases decision
            performance."
```

The key difference from MISQ-style behavioral theory: Krakowski cites organizational
design and micro-contingency theory rather than IS adoption models. The hypotheses are
stated in economic/operational terms ("decision performance"), not in IS constructs
("behavioral intention to use").
