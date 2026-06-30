# MS-IS Discussion / Conclusion Style Guide

MS-IS papers handle the discussion differently from MISQ/ISR. Many MS empirical papers
include an inline Discussion subsection (4.4 or similar) within the Results section
that covers identification limitations, then end with a short "Conclusion" section.
Analytical papers typically end with "Discussion" or "Concluding Remarks." The final
section is shorter and more action-oriented than MISQ/ISR discussions.

## Section title conventions

| Paper type | Typical title | Location |
|------------|--------------|----------|
| Empirical (many MS papers) | Inline "Discussion" (4.4) + final "Conclusion" (6 or 7) | Discussion inside Results; Conclusion at end |
| Empirical (some MS papers) | "Discussion and Conclusion" | Final section |
| Analytical | "Discussion" or "Concluding Remarks" | Final section |

## Word budget

- Inline Discussion (within Results): 500-1,000 words (2-4 paragraphs)
- Final Conclusion: 500-1,000 words (2-4 paragraphs)
- Combined (if one section): 1,000-1,500 words (4-6 paragraphs)

MS-IS discussions are substantially shorter than MISQ discussions (~2,000-3,000 w).
The MS philosophy: the results speak; the discussion translates them into action.

## Arc

### Two-part structure (common in MS empirical papers)

**Part 1: Inline Discussion (inside Results section)**
```
4.4  DISCUSSION
     P1   IDENTIFICATION INTERPRETATION
          What does the estimate mean? (LATE vs ATE, external validity)
          State clearly what the design CAN and CANNOT identify.
     P2   THREATS TO INTERNAL VALIDITY
          Each threat stated and addressed. If unresolved, state honestly.
     P3   EXTERNAL VALIDITY / GENERALIZABILITY
          To what settings do these results transport?
     P4   MANAGERIAL TRANSLATION
          What should a manager do with these estimates? What decisions
          change? (Optional here; may wait for Conclusion.)
```

**Part 2: Final Conclusion**
```
6.   CONCLUSION
     P1   ONE-PARAGRAPH SUMMARY
          Restate the question, method, and key finding in 3-4 sentences.
     P2   CONTRIBUTION (if not fully stated in introduction)
          What the paper adds to the literature. One specific claim.
     P3   MANAGERIAL / POLICY IMPLICATIONS
          Actionable guidance. "Our findings suggest that managers should..."
          "Policymakers designing [X] should consider..."
          For platform/market papers: welfare consequence stated.
     P4   LIMITATIONS AND FUTURE WORK (1-2 sentences each)
          Honest about what this paper cannot do. Future work framed as
          opportunities, not hedges.
```

### Single-section structure (analytical or combined)

```
6.   DISCUSSION / CONCLUDING REMARKS
     P1   RESTATE THE CONTRIBUTION
          "We have [modeled/identified/characterized] [X] and shown that [Y]."
     P2   MAIN INSIGHT IN PLAIN LANGUAGE
          Translate the formal result into intuition a non-specialist can
          absorb. This is the "elevator pitch" of the finding.
     P3   MANAGERIAL / POLICY IMPLICATIONS
          Actionable guidance derived FROM the formal results, not asserted
          independently. "Proposition 2 implies that firms should..."
     P4   WELFARE STATEMENT (for market/platform papers)
          "Our welfare analysis shows that [policy/design] [improves/reduces]
          [consumer surplus / total welfare] by [mechanism]."
     P5   LIMITATIONS
          2-3 sentences. Honest, specific, actionable.
     P6   FUTURE DIRECTIONS
          1-2 sentences. Name the next question, not a laundry list.
```

## Signature moves

### Identification interpretation (inline Discussion)
MS empirical papers use the inline Discussion to be precise about what the estimate
means, distinguishing LATE, ATT, ATE, and ITT.

From Cui et al. (4.4): "First, due to imperfect compliance, we rely on instrumental
variables (IV) estimation, which identifies a LATE. The LATE represents an average
treatment effect (ATE) for a potentially selected subset of individuals -- namely,
those whom the encouragement designs successfully convince to adopt Copilot."

### Managerial translation (not restatement)
The MS signature: translate results into what a decision-maker should DO. Not "our
results show X" but "managers should [action] because [result implies consequence]."

From Cui et al. (4.4): "we caution that managers may not want to use the adoption
rates from early in our experiment to forecast future adoption. Indeed, given the
rapid adoption of coding assistants in the industry (Bick, Blandin, and Deming 2024),
the LATE estimates may serve as better benchmarks for managerially relevant
productivity gains."

### Welfare statement (platform/market papers)
For papers involving markets, platforms, or policy, the discussion must state the
welfare consequence explicitly. This is a distinguishing MS-IS requirement not found
in MISQ or ISR.

Pattern: "Our analysis shows that [policy/design] increases [consumer surplus / total
welfare] by [mechanism], while [producer surplus] [increases/decreases]. On net,
[total welfare is higher/lower]."

### Honest limitations
MS values frank limitations over hedging. State what you CANNOT claim and why.

From Cui et al.: "Our only empirical indication of the direction of this selection
comes from our DiD estimates, which identify an average treatment effect on the
treated (ATT) under the additional assumption of parallel trends. Under this
assumption, the ATT is lower than the LATE at Microsoft but higher at Accenture,
suggesting that the direction of selection may differ across firms."

### Short future directions
MS future work is 1-2 sentences naming the next concrete question, not a paragraph
of speculative extensions.

Pattern: "An important question for future research is [specific question] -- for
example, [concrete study design]."

Anti-pattern: "Future research should explore the role of [X, Y, Z, W] in
different contexts and industries." (Too vague, too many items.)

## Sentence shapes to imitate

Contribution restatement:
- "We have [provided the first / identified / characterized / recovered] [X] using [Y]."
- "Our analysis [documents / reveals / demonstrates] that [finding]."

Managerial implications:
- "Our findings suggest that [managers/policymakers] should [specific action]."
- "Platform designers can [improve efficiency / increase welfare] by [design change]."
- "[Policy] that [action] would [consequence], according to our estimates."

Limitations:
- "Our estimates are [specific limitation]. To the extent that [condition], our
  results may [overstate/understate] the true effect."
- "We caution that [qualifier]."

Future work:
- "An important question for future research is whether [specific question]."
- "We believe that [topic] is a fruitful avenue for future research."

## Anti-patterns

- **No restating all results.** The conclusion does not walk through H1-H6 again.
  One-paragraph summary, then forward-looking.
- **No generic implications.** "Our findings have important implications for IS research
  and practice" is empty. Name the specific implication and the specific action.
- **No "future research should..." laundry list.** One or two concrete directions, not
  five vague ones.
- **No overclaiming in Discussion what was hedged in Results.** If Results says
  "association," Discussion cannot say "causes."
- **No lengthy literature re-engagement.** MISQ discussions re-engage with 2-3
  literature streams in detail. MS-IS states the contribution, gives the action
  implication, and stops.
- **No missing welfare statement for platform/market papers.** If the paper involves
  a two-sided market, pricing, or platform design, the Discussion MUST state the
  welfare consequence.

## Contrast with MISQ/ISR discussions

| Dimension | MS-IS | MISQ | ISR |
|-----------|-------|------|-----|
| Length | Short (500-1,500 w) | Long (2,000-3,000 w) | Medium (1,500-2,000 w) |
| Structure | Inline Discussion + Conclusion | Single Discussion section | Discussion + Conclusion |
| Lit re-engagement | Minimal | Deep (2-3 streams) | Moderate |
| Implications focus | Managerial / policy ACTION | IS theory implications | Theory + empirical implications |
| Welfare statement | Required (market/platform) | Not expected | Not expected |
| Limitations style | Frank, 2-3 sentences | Dedicated paragraph | Dedicated subsection |
| Future work | 1-2 sentences | Paragraph | 1-3 sentences |

## Enrichment needs

- [x] Mine a published MS-IS conclusion to capture exact phrasing of the managerial
  implications paragraph (the published version, not the preprint).
  **RESOLVED**: See published discussion patterns below from all 8 papers.
- [x] Mine an analytical MS-IS discussion to capture how formal propositions are
  translated into managerial guidance ("Proposition 2 implies that...").
  **RESOLVED**: See Feng 2025 counterfactual-to-policy pattern below.
- [x] Mine Shukla et al. (2021) for a healthcare-domain MS-IS discussion to see how
  physician/patient welfare implications are stated.
  **RESOLVED**: See Huesmann 2025, Chao/Larkin 2022 healthcare discussion patterns below.

---

## Enriched from additional exemplars (2026-06-29)

Sources: 8 published MS papers (Huesmann 2025, Chao/Larkin 2022, Feng 2025, Cui 2025,
Krakowski 2026, de Kok 2025, Chen 2025, Burtch 2026).

### Section title conventions (additional from published papers)

| Paper | Discussion/Conclusion title | Structure |
|-------|---------------------------|-----------|
| Huesmann 2025 | "5. Implications and Discussion" + "6. Concluding Remarks" | Implications first, then conclusion |
| Chao/Larkin 2022 | "5. Discussion" (5.1 Summary, 5.2 Limitations, 5.3 Managerial Implications) | Three-part discussion, no separate conclusion |
| Feng 2025 | "7. Conclusion" | Single short conclusion |
| Cui 2025 | "4.4 Discussion" (inline) | Inline only, no final conclusion section |
| Krakowski 2026 | "6. Discussion" (6.1 Contributions, 6.2 Future Research, 6.3 Practical Implications) | Three-part discussion, no separate conclusion |
| de Kok 2025 | "5. Discussion" (5.1-5.5 topical subsections) + "6. Conclusion" | Discussion with many subsections + short conclusion |
| Chen 2025 | Final paragraph of Section 5 | Folded into the illustration section |
| Burtch 2026 | "6. Discussion and Conclusion" | Combined single section |

### Healthcare "Implications and Discussion" pattern (Huesmann 2025)

Huesmann uses a distinctive structure where implications lead and limitations follow:

```
5.   IMPLICATIONS AND DISCUSSION
     P1-P3  MAIN IMPLICATIONS FOR CLINICAL LEADERS
            "Our lab-in-the-field experiment sheds light on how the
            design of a ranking system, in conjunction with an individual
            physician's level of ability, affects effort provision."
            Translate each main result to a recommendation:
            - "A threshold near the top of the range is necessary to
              motivate high-ability physicians"
            - "lower thresholds are also needed to motivate low-ability
              physicians who have no chance of reaching the top rank"
            Application to specific clinical activities named.

     P4     GENERALIZABILITY SCOPE
            "For a given clinical team, the appropriate level for the
            topmost threshold will depend on the mix of abilities..."

     5.1    Features of the Experimental Design
            Address the stated-effort method critique honestly.
            "One might argue that the stated-effort method... may not
            adequately capture the field setting..."
            Give "good reasons" for design choices (3 numbered reasons).

     5.2    Generalizability
            Broader applications beyond the experiment.
            Name specific clinical areas where results apply.
            "more than 80% of the physicians participating in the
            experiment indicated a clinical task that would resemble
            the stylized decision problem"

     5.3    Replicability
            Pilot experiment results consistent with main results.
            "our pilot experiment, which had a smaller subject pool
            (N = 116)... yielded patterns similar to those in Results 1
            and 2"

6.   CONCLUDING REMARKS
     One short paragraph (6 sentences). Restate the main practical
     takeaway and name the contribution to experimental methodology.
     "Taken together, our results provide clinical leaders with valuable
     insights into the design of performance-feedback mechanisms that
     could directly affect the delivery of care."
```

### Healthcare policy discussion pattern (Chao/Larkin 2022)

```
5.   DISCUSSION
     5.1  Summary (1 paragraph)
          Restate the question, design, and key finding in 4-5 sentences.
          "This paper uses a state-level policy change to evaluate
          whether mandated disclosure of payments from pharmaceutical
          companies changed physician prescribing."

     5.2  Limitations (2-3 paragraphs)
          Each limitation stated specifically, then scoped:
          - "Most importantly, we do not observe prepolicy payment
            data for the treatment group"
          - "Like any paper using difference-in-differences, we cannot
            definitively show that the treatment estimate is caused by
            the adoption of policies."
          - "Finally, we cannot say for certain how our treatment
            estimates would hold for nonacademic doctors."

     5.3  Managerial Implications (2 paragraphs)
          Name the decision-maker and the action:
          "For healthcare managers and officials concerned with the
          effects of pharmaceutical marketing on prescription drug costs,
          increasing the coverage of disclosure or making disclosed
          payments more salient... may be an effective method for
          changing physician behavior."
          Extend to adjacent policy domains:
          "Other physician conflicts of interest may also benefit from
          disclosure."
          Name specific campaigns and movements as examples.
```

### Field experiment discussion pattern (Krakowski 2026)

Krakowski uses the most structured discussion with labeled subsections:

```
6.   DISCUSSION
     6.1  Contributions to the Literature
          Three numbered contributions, each 1 paragraph:
          "First, we contribute a human-centered approach to AI..."
          "Second, our findings address discrepancies between
          theoretical assumptions and empirical observations..."
          "We also contribute to the understanding of learning effects
          in human-AI interaction..."

     6.2  Future Research
          3-4 specific directions, each 1-2 sentences.
          "Future research could also explore the cost of tailoring..."
          "It would also be relevant to explore how our findings apply
          to newer AI technologies, such as generative AI..."
          Honest power limitation: "Our results are power-constrained
          and should therefore be interpreted with caution."

     6.3  Practical Implications
          Connect to the broader AI-implementation discourse.
          "AI experts and practitioners increasingly advocate for
          human-centered AI..."
          State the practical insight: "the implementation of an
          advanced AI system can yield inferior outcomes even when
          compared with a technologically inferior IT system"
          Close with the managerial lesson: "managers [need] to adopt
          a comprehensive, human-centered perspective when implementing
          AI systems"
```

### Methodological paper discussion (de Kok 2025)

Tutorial/tool papers have topical discussion subsections addressing concerns the
reader/reviewer would raise:

```
5.   DISCUSSION
     5.1  GLLM Training Data: Biases, Source Material, and Recent Events
     5.2  Replicability
     5.3  Data Privacy and Copyright
     5.4  Current GLLM Developments
     5.5  Using GLLMs for Writing and Programming

6.   CONCLUSION (1 paragraph)
     "GLLMs offer significant potential for academic research analyzing
     textual data." Restate the framework contribution, the case study
     result, and the practical guidance.
```

### Methodological paper conclusion (Burtch 2026)

```
6.   DISCUSSION AND CONCLUSION
     P1   Restate the problem and the contribution:
          "We have presented a novel method... that leverages
          instrumental variables (IV) to address the measurement
          error problem."
     P2   Name the three key ingredients of the method.
     P3   Theoretical properties: consistency, asymptotic normality.
     P4   Empirical evidence: simulation results + real-world validation.
     P5   Practical tools: diagnostic procedure, cross-fitting, etc.
     P6   Limitations and scope: "The validity of EnsembleIV depends on
          the satisfaction of two key assumptions..."
     P7   Future directions: "Interesting potential extensions include..."
```

### Published sentence shapes

**Contribution restatement**:
- "Taken together, our results provide [stakeholders] with valuable insights into
  [design question]." (Huesmann)
- "Altogether, our results provide an important counter to those claiming that
  [intervention] is ineffective." (Chao/Larkin)
- "We contribute a human-centered approach to AI that contrasts with prior work
  emphasizing AI as a replacement for humans." (Krakowski)

**Managerial implications (healthcare)**:
- "For healthcare managers and officials concerned with [problem], [increasing/changing
  X] may be an effective method for [changing behavior]." (Chao/Larkin)
- "We anticipate, for example, that clinical leaders could apply our findings in
  providing structured relative performance feedback during individual performance
  review meetings." (Huesmann)
- "Health executives attempting to curb pharmaceutical influence on drug costs may
  consider widening the scope of payments covered by disclosure." (Chao/Larkin)

**Honest limitations (healthcare)**:
- "Most importantly, we do not observe prepolicy payment data for the treatment group,
  and we do not observe any payment data for the control group." (Chao/Larkin)
- "One might argue that the stated-effort method used in our experiment may not
  adequately capture the field setting and the psychological forces involved in
  exerting actual effort." (Huesmann)
- "We caution against causal interpretations due to power constraints." (Krakowski)

**Future work (specific, 1-2 sentences)**:
- "Future research could also explore the cost of tailoring, which was not addressed
  in this study." (Krakowski)
- "It remains for future research to test whether disclosure is effective in settings
  where [norms are different]." (Chao/Larkin)

### Alternative mechanisms section (Chao/Larkin 2022)

Healthcare policy papers include a dedicated "Alternative Mechanisms" subsection
(4.6) that systematically considers and rules out competing explanations:

1. **Industry-driven change**: "it could be that industry... instigated these changes...
   However, this appears unlikely for several reasons."
2. **Concurrent policy**: "Another possible interpretation could be that effects are
   due to the Massachusetts healthcare bill... However, if this bill affected
   prescriptions, it would likely be predominantly in the year the bill took effect."
3. **Insurance change**: "a final alternative mechanism could be that these changes were
   driven by a state-specific health insurance change... However, AQCs covered only
   about 8% of physicians..."

Each alternative mechanism is stated, then refuted with specific evidence. This
systematic mechanism-elimination is a hallmark of healthcare MS causal papers.

### Key differences from the original guide

1. **"Implications and Discussion" (not just "Discussion")**: Huesmann titles the
   section to foreground implications, not limitations. This is a healthcare MS
   convention.

2. **Three-subsection Discussion is common**: Contributions / Future Research /
   Practical Implications (Krakowski) or Summary / Limitations / Managerial
   Implications (Chao/Larkin). The guide's description of a "short" Discussion is
   accurate for some papers but not universal.

3. **Discussion word budget may be larger than estimated**: Chao/Larkin's Discussion
   spans 4 full pages (~2,500 words) with alternative mechanisms. The guide's
   500-1,500 word range understates healthcare policy papers. Revised range:
   500-2,500 words for Discussion alone, depending on how many alternative mechanisms
   need to be addressed.

4. **Concluding Remarks can be very short**: Huesmann's "6. Concluding Remarks" is a
   single paragraph (6 sentences, ~120 words). Some papers omit a concluding section
   entirely (Krakowski ends with 6.3 Practical Implications).
