# ISR Theory / Hypotheses Development Style Guide

Distilled from two ISR exemplars. Quote the SHAPE, not the content.

## Word budget

- Target: 3,000-5,000 words (the largest section in the paper).
- Bao 2021: ~4,500 words across two sections: "Related Literature" (S3, ~1,500w) + "Research Hypotheses" (S4, ~3,000w).
- Zhang 2026: ~2,500 words across "Literature Review" (S2, ~1,200w) + "Model and Hypotheses Development" (S3, ~1,300w).
- ISR separates lit review from hypothesis derivation. These are different sections with different jobs.

## Section naming conventions

ISR uses one of two naming patterns:

```
Pattern A [Bao 2021]:
  3. Related Literature
    3.1. [Topic 1]
    3.2. [Topic 2]
  4. Research Hypotheses
    4.1 [Construct/relationship 1]
    4.2 [Construct/relationship 2]

Pattern B [Zhang 2026]:
  2. Literature Review
    2.1. [Topic 1]
    2.2. [Topic 2]
  3. Model and Hypotheses Development
    3.1. [Framework name]
    3.2. [Model + Hypotheses]
```

Both patterns separate the surveying job (lit review) from the deriving job (hypotheses).

## The lit review vs. theory distinction

### Literature Review section: surveys what others found
- Job: establish the landscape, identify the void.
- Every paragraph surveys a topic: "X et al. found that...", "Prior research has...", "The literature has documented..."
- [Bao 2021] S3 has two subsections: "Quality-Efficiency Tradeoffs" and "Health IT & Virtual Organizations." Each surveys existing findings, ending with the gap that motivates the hypotheses.
- [Zhang 2026] S2 has two subsections: "Online Consultations and Physician Reviews" and "NLP for Multidimensional Healthcare Sentiment Analysis." Pure survey, no predictions.
- SHAPE per paragraph: `[Topic sentence naming the stream]. [What X found (cite)]. [What Y found (cite)]. [How this stream relates to the present study]. [What remains unclear / unexplored].`

### Theory / Hypotheses section: derives what should be true and why
- Job: name a mechanism, argue it applies in this context, derive a directional prediction.
- [Bao 2021] S4 subsections named by the relationship being derived: "Efficiency and Quality of Care" (4.1) and "Effective Use of Health IT" (4.2). Each subsection is 4-6 paragraphs of argument leading to a hypothesis.
- [Zhang 2026] S3.1 defines the SEPTE framework (construct definitions), S3.2 states the model equation and hypotheses.
- SHAPE per paragraph: `[Name the mechanism or causal logic]. [Cite evidence the mechanism exists]. [Argue why it applies in THIS context]. [State the directional consequence]. [Repeat for next step of the argument].`

## Hypothesis derivation pattern

### Subsection-per-hypothesis structure
- [Bao 2021] Each subsection (4.1, 4.2) derives one or two hypotheses. H1 closes 4.1; H2 and H3 close 4.2.
- [Zhang 2026] All five hypotheses (H1-H5) are stated together in S3.2 after the framework is defined, with one sentence per dimension.
- The Bao pattern (one subsection per hypothesis, full derivation) is the stronger ISR move. Zhang's compressed format works when hypotheses are parallel (same mechanism, different dimensions).

### Hypothesis statement format
- [Bao 2021] "H1: Efficient ACOs are more likely to exhibit greater quality based on their patients' health outcomes, compared to inefficient ACOs."
- [Bao 2021] "H2: Effective use of health IT is associated with greater ACO quality, measured in terms of patient health outcomes."
- [Bao 2021] "H3: Effective IT use has a positive interaction effect on the association between ACO quality and efficiency."
- [Zhang 2026] "We hypothesize that all five dimensions of physician service quality positively influence online consultation demand."
- SHAPE: `H[N]: [Construct A] is [positively/negatively] associated with [Construct B], [boundary condition if any].`
- Always directional. ISR does not use "H1a/H1b" competing hypotheses unless the theory genuinely supports both directions.

### Mechanism naming
- [Bao 2021] Names "IT-enabled information integration" as the mechanism, introduced mid-theory and used throughout.
- [Zhang 2026] Names the SEPTE framework dimensions (Safety, Effectiveness, Patient-centeredness, Timeliness, Efficiency) as constructs.
- SHAPE: the mechanism gets a proper noun name, introduced once and reused. Not described vaguely each time.

### Construct definition pattern
- [Zhang 2026] Each SEPTE dimension gets 2-3 sentences of definition grounded in the AHRQ framework: "Safety measures refer to the provider's responsibility to avoid harm to patients when providing the care that is intended to help them, which reflects a physician's technical skills."
- [Bao 2021] Constructs defined through their operationalization context: "MU achievement is a multi-dimensional construct that captures different dimensions of effective EHR use."
- SHAPE: `[Construct] refers to [definition grounded in authoritative source] (cite framework). [How it manifests in this context].`

## Paragraph structure within theory subsections

Each subsection contains 4-8 paragraphs following this internal arc:

```
Para 1: Framing (why this relationship matters in this context)
Para 2-3: Mechanism derivation (cite theory + evidence the mechanism exists)
Para 4-5: Application to THIS context (argue why the mechanism applies here)
Para 6: Therefore / Hence sentence + formal hypothesis statement
```

- [Bao 2021] S4.1 follows this arc across 6 paragraphs, ending with H1.
- Each paragraph is 5-8 sentences, with ~0.5 citations per sentence.

## Conceptual model figure

- [Bao 2021] Figure 1 appears right after all hypotheses, showing the conceptual model with boxes, arrows, and hypothesis labels (H1+, H2+, H3+).
- [Zhang 2026] Figure 1 appears within S3.2, showing the SEPTE framework dimensions with H1-H5 arrows to the outcome.
- SHAPE: One conceptual model figure with constructs as boxes, hypotheses as labeled arrows with (+) or (-) direction.
- Placement: immediately after the last hypothesis, before the methods section.

## Citation density

- ~0.50 citations per sentence in theory paragraphs (same as the family-level profile).
- Higher in lit review subsections (~0.60), lower in derivation paragraphs (~0.40).
- Hypothesis statements themselves carry zero citations.

## Anti-patterns

- Mixing survey and derivation in the same section (blurs lit review and theory).
- Defining constructs through their measurement method in the theory section. How you measure it belongs in Methods. Theory takes the construct as given and derives what it predicts.
- Hypothesis lists longer than 5 items without distinct mechanisms (reads as fishing).
- "Based on the above discussion, we hypothesize..." without naming the specific mechanism that warrants the prediction.
- Competing hypotheses (H1a/H1b) without genuine theoretical grounding for both directions.
- Forgetting to argue why the mechanism applies in THIS specific context (not just that the mechanism exists in general).

## Enriched from additional exemplars (2026-06-29)

Sources: Mousavi 2026, Saifee 2020, Yang 2022, Shi 2025, Wang 2026, Wu 2025, Liu 2025, Zhang-j 2026, Schecter 2025.

### Word budget (revised)

The original 3,000-5,000 range holds for combined lit review + theory. Across new papers:

| Paper | Lit Review | Theory/Framework | Combined |
|---|---|---|---|
| Mousavi 2026 | ~1,600 (Background) | ~2,800 (Framework) | ~4,400 |
| Saifee 2020 | ~1,800 | ~2,500 (Research Framework) | ~4,300 |
| Yang 2022 | ~3,500 (Related Work) | embedded in Related Work | ~3,500 |
| Wang 2026 | embedded | ~2,500 (Theoretical Framework) | ~2,500 |
| Wu 2025 | embedded | ~5,500 (Theoretical Motivation) | ~5,500 |
| Liu 2025 | ~1,100 | (no separate theory) | ~1,100 |
| Shi 2025 | N/A (commentary) | ~6,500 (method exposition) | ~6,500 |

**Revised target: 2,500-5,500 words** for the combined theory block. Papers with named mechanisms or theory synthesis tend toward 4,000+. Empirical papers with minimal new theory (Liu 2025) can go as low as ~1,100 for lit review alone.

### Additional section naming patterns

Beyond Patterns A and B, ISR papers use:

```
Pattern C [Wang 2026]:
  2. Theoretical Framework
    2.1. [Theory 1]
    2.2. [Theory 2]
    2.3. [Named Mechanism] (IBDC)
    2.4. Related Literature

Pattern D [Wu 2025]:
  2. Theoretical Motivation
    2.1. Related Literature
    2.2. Theory and Hypotheses
      2.2.1. [Relationship leading to H1]
      2.2.2. [Relationship leading to H2]
    2.3. [Moderator for H3]
    2.4. [Boundary condition for H4]

Pattern E [Mousavi 2026]:
  2. Background (pure survey)
  3. Theory-Guided Framework (derives hypotheses from synthesized theory)

Pattern F [Yang 2022 - design science]:
  2. Related Work
    2.1-2.4 (four topic subsections, gap at end of 2.4)
  3. Framework [derives artifact + kernel theory, no H1/H2]
```

**Pattern C** (theory-first, lit review after) inverts the standard order: build the mechanism first from theories, then position against prior work.

### Hypothesis format variants

The original guide covers `H[N]: [directional statement]`. New exemplars reveal 5 additional formats:

**1. Numbered + parenthetical title + italic body + rationale clause** [Mousavi 2026]:
> **Hypothesis 1(a)** (Aggregate Performance of LLMs). *LLMs will outperform existing methods for identifying psychometric constructs in text, given [rationale].*
- Sub-hypotheses use parenthetical letters: H1(a), H1(b), H2(a), H2(b), H3(a), H3(b)
- Arrow notation in title: "(Cognitive Ability -> Resilience Perception)"
- 8 hypotheses organized in a 3-stage framework

**2. Italic, directional, single-sentence, preceded by lead-in** [Wu 2025]:
> *Hypothesis 1.* *Physicians' OHC participation has a positive impact on their off-line care quality.*
- Lead-in: "We, therefore, propose the following."
- Each hypothesis at the end of the subsection that builds the argument for it

**3. Research Questions instead of hypotheses** [Saifee 2020]:
> **RQ1.** "Are online reviews reliable indicators in the case of chronic disease care?"
> - a. Are physicians who receive better online reviews... more likely to deliver better clinical outcomes?
> - b. Are physicians who receive more positive online reviews... more likely to deliver better clinical outcomes?
- Bold label, yes/no question format, sub-questions decompose by variable type
- Used when the theory does not predict the direction (credence goods setting)

**4. No formal hypotheses; predictions derived from named mechanism** [Wang 2026]:
> "Our framework predicts that potential discrepancies between publicly articulated positions and private practice generate consistency pressure, motivating alignment through (1) more cost-conscious medication prescribing and (2) convergence of LOS toward guideline standards."
- The mechanism name (IBDC) carries the predictive weight, not numbered H statements
- Predictions stated as "our framework predicts that..." or "Our IBDC framework predicts that..."
- Falsifiable conditional form: "If patient sorting were the primary mechanism, we would expect..."

**5. Formal mathematical constructs for methodology papers** [Zhang-j 2026, Schecter 2025]:
> **Theorem 1** (Consistency). *Under Assumption 1, any estimator... is a consistent estimator of theta_0.*
> **Proposition 1** (Hausman-Type Specification Test).
> **Corollary 1** (Asymptotic Power Comparison).
- No H1/H2 at all. Instead: Assumptions, Theorems, Propositions, Corollaries, Remarks
- Numbered Remarks serve as interpretive asides connecting formal results to practice

**Decision rule**: Formal H1/H2 for empirical papers with directional theory. RQ format when direction is ambiguous. Named-mechanism predictions when the paper coins a new concept. Theorems/Propositions for methodology papers.

### Theory synthesis as a core move

[Wang 2026] demonstrates a distinctive ISR move: synthesizing multiple existing theories into a single novel mechanism with a coined name:
- Festinger's cognitive dissonance theory (1957)
- Cialdini's commitment-consistency principle (1984)
- Cruess et al.'s professional identity formation framework (2015, 2016)
- Synthesis -> IBDC (Identity-Based Digital Commitment)
- Architecture: Foundation (dissonance) -> Amplifier (commitment) -> Convergence channel (identity) -> Empirical precedent (healthcare)
- SHAPE: `[Theory A] establishes [base mechanism]. [Theory B] argues [amplifier]. [Theory C] provides [the domain-specific convergence channel]. We integrate these to propose [Coined Name]: [one-sentence definition].`

### Theory-as-design-lever

[Mousavi 2026] uses dual-process theory not just to explain results but to generate a design artifact:
> "Drawing on this insight, we introduce a cognitive-affective prompting strategy for LLMs that emulates these human strengths, yielding performance gains beyond state-of-the-art prompting methods."
- SHAPE: theory predicts -> observation confirms -> design implication follows from the same theory. This closes the loop between theoretical contribution and practical contribution.

### Design science framing for technical papers

[Yang 2022] and [Schecter 2025] anchor ML/DL work in design science vocabulary as a legitimating frame:
- "kernel theory" (the theoretical foundation guiding artifact design)
- "design artifact" (the system being built)
- "operational utility" (the practical value metric)
- "Following the design science approach, we evaluate..." [Yang 2022]
- "Following the computational design science research paradigm (Abbasi et al. 2024)..." [Schecter 2025]
- This vocabulary signals ISR alignment and is expected for papers proposing algorithms or artifacts.

### Literature review canonical openers

Beyond the existing SHAPE, new canonical first sentences for lit review sections:
- [Saifee 2020] "Our study is related to several key streams of literature."
- [Wu 2025] "In this section, we review related studies from three streams of literature: [A], [B], and [C]."
- [Yang 2022] "Prior IS research has studied the importance of [topic]."
- These are formulaic and interchangeable. The roadmap variant (Wu) is the clearest.

### Literature review gap closers

The final paragraph of the lit review should declare the gap explicitly:
- [Yang 2022] "However, integrating [X], [Y], and [Z] into a single unified artifact, has not been explored. This is precisely the research gap we aim to address with our proposed framework."
- [Wu 2025] "Consequently, how [phenomenon] directly affects [outcome] remains an open empirical question."
- [Saifee 2020] "We differ from this stream in a number of ways."
- SHAPE: `[What has NOT been done]. This is precisely [the gap / where we contribute].`

### Credence goods as theoretical anchoring example

[Saifee 2020] demonstrates how a single economic theory (search-experience-credence goods trichotomy) can serve as the entire theoretical backbone:
- The theory appears in Introduction (1.1), Literature Review (2.4), Research Framework (3), and Conclusions (6)
- A null result is EXPLAINED by the theory rather than apologized for
- SHAPE for theory-explains-null: `[Theory] predicts that [phenomenon is ineffective] in [this context] because [mechanism]. Our empirical results are consistent with this prediction.`

### Hypothesis count norms (revised)

The original guide says "longer than 5 items without distinct mechanisms reads as fishing." Revised guidance from new papers:
- [Mousavi 2026]: 8 hypotheses (H1a-H3b), but organized in a 3-stage framework with distinct mechanisms per stage
- [Wu 2025]: 4 hypotheses, each closing a subsection
- [Wang 2026]: 0 formal hypotheses (uses mechanism predictions)
- [Saifee 2020]: 0 formal hypotheses (uses RQs)
- **Revised guideline**: 2-8 hypotheses is the full ISR range. More than 5 requires clear organizational structure (stages, levels, or distinct mechanisms). Using 0 formal hypotheses (RQs or mechanism predictions instead) is also acceptable.

### Updated anti-patterns

- **Mixing theory synthesis with literature survey in the same subsection.** Synthesis (building a new mechanism from existing theories) deserves its own subsection. Survey (what others found) is a different subsection. [Wang 2026 exemplifies clean separation]
- **Generic hypothesis lead-in.** "Based on the above discussion, we hypothesize..." is weaker than "We, therefore, propose the following." [Wu 2025] or deriving from a named mechanism [Wang 2026].
- **Missing the "why HERE" argument for design science papers.** Design science papers need to argue why this context requires an artifact, not just that an artifact could be built. [Yang 2022, Schecter 2025]
