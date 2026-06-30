# MISQ Abstract -- Section Style Guide

Extracted from MISQ Research Article exemplars. Supplements `style-profile.md`.

## Word budget

- 120-160 words (hard ceiling ~160). Liu (2021): ~150w. Gao (2015): ~155w. Yin (2014): ~120w.
- Unstructured prose paragraph, no labeled sections (unlike MS-IS which uses labeled fields).
- Italicized in the published PDF.

## Arc

```
phenomenon/question
  -> what is not known or not addressed
  -> approach (theory + method, one sentence each)
  -> key findings (directional, named constructs)
  -> contribution/implication close
```

The arc is **question-forward, method-light**. The abstract names the theoretical question first, mentions the method only enough to establish credibility, and spends the bulk on findings and contribution.

## Signature moves

1. **Open with the research question, not the method.** The first sentence frames the IS phenomenon or the question being examined, not "We use [method] to study [topic]." The method appears mid-abstract as an enabler clause.
   - Source: Liu (2021), Gao (2015), Yin (2014) all open this way.

2. **Enabler clause for the method.** When a novel method (deep learning, NLP, field experiment) is central, it appears as a subordinate enabling clause, not the headline: "It trains a deep learning model to infer a reviewer's personality traits. *This enables* analyses to reveal the role of personality traits in review helpfulness." [Liu 2021]

3. **Close on contribution or implication, not method.** The final sentence points forward to theoretical/practical value, not backward to the technique.
   - "Theoretical and practical implications are discussed." [Liu 2021]
   - "This study is the first to provide empirical evidence of the relationship between online ratings and the underlying consumer perceived quality, and extends prior research on online word-of-mouth to the domain of professional services." [Gao 2015]
   - "Our findings demonstrate the importance of examining discrete emotions in online word-of-mouth, and they carry important practical implications for consumers and online retailers." [Yin 2014]

4. **Named constructs in findings.** The findings sentence names the specific constructs and their directional relationships, not a generic "we find significant results": "higher review helpfulness is related to higher openness, conscientiousness, extraversion, and agreeableness and to lower emotional stability." [Liu 2021]

## Exemplar sentences (shape, not content)

**Opening move** (phenomenon/question first):
- "This work examines the question of who is more likely to provide future helpful reviews in the context of online product reviews by synergistically using personality theories and data analytics." [Liu 2021]
- "Consumer-generated ratings typically share an objective of illuminating the quality of a product or service for other buyers." [Gao 2015]
- "This paper explores the effects of emotions embedded in a seller review on its perceived helpfulness to readers." [Yin 2014]

**Gap/approach transition**:
- "While ratings have become ubiquitous and influential on the Internet, surprisingly little empirical research has investigated how these online assessments reflect the opinion of the population at large." [Gao 2015]
- "Drawing on frameworks in literature on emotion and cognitive processing, we propose that over and above a well-known negativity bias, the impact of discrete emotions in a review will vary." [Yin 2014]

**Findings sentence**:
- "We develop hypotheses on how personality traits are associated with review helpfulness, followed by hypotheses testing that confirms that higher review helpfulness is related to higher openness, conscientiousness, extraversion, and agreeableness and to lower emotional stability." [Liu 2021]
- "In sharp contrast to the widely voiced concerns by medical practitioners, we find that physicians who are rated lower in quality by the patient population are less likely to be rated online." [Gao 2015]

## Anti-patterns

- Do NOT lead with the method ("We use deep learning to..."). Lead with the question.
- Do NOT end on the method ("We demonstrate superior performance of our model"). End on contribution or implication.
- Do NOT use structured/labeled fields (Problem, Methodology, Results). MISQ uses a single unstructured paragraph.
- Do NOT include specific numerical results (coefficients, p-values) in the abstract. Name the constructs and directions.
- Do NOT exceed ~160 words. MISQ abstracts are tightly compressed.

## Paragraph structure

One paragraph only. No line breaks, no sub-sections, no bullet lists.

Sentence count: 4-7 sentences following this pattern:
1. What question/phenomenon (1 sentence)
2. What gap or what is not known (0-1 sentence, sometimes folded into sentence 1)
3. How we approach it -- theory + method (1-2 sentences)
4. What we find (1-2 sentences, named constructs + directions)
5. What it means (1 sentence, contribution or "implications are discussed")

---

## Enriched from additional exemplars (2026-06-29)

Source papers: Zhang (2025), Weng (2026), Ayabakan (2025), Raimi (2025), Liu-EBM (2025), Liu-HMM (2025). These 6 papers confirm and extend all patterns above. No existing pattern is contradicted.

### Updated word budget

- The 120-160w range is confirmed. Zhang (2025): ~175w (slightly long but within tolerance). Weng (2026): ~185w (longer, reflecting higher model complexity). Ayabakan (2025): ~155w. Raimi (2025): ~145w. Liu-HMM (2025): ~140w.
- Research Notes (Ayabakan 2025, Liu-HMM 2025) stay within the same budget; no separate norm exists.

### Additional signature moves

7. **Concrete numbers in abstract for healthcare/policy papers.** Healthcare-domain MISQ papers include specific quantitative results in the abstract, contrasting with the earlier "no specific numerical results" anti-pattern for behavioral papers. This is context-dependent: when the finding has direct policy relevance, concrete numbers add credibility.
   - "there was an 8.48% surge in the number of consulted patient inquiries from affected physicians" [Zhang 2025]
   - "the greater the EHR adoption by care providers, the less likely a claim is denied" [Ayabakan 2025]
   - "when a hospital's intra-hospital EHR single-sourcing rate increases from 80% to 90%, claim denial probability is reduced from 1.18% to 1.03%" [Ayabakan 2025]

8. **Counterintuitive-finding hook.** When the main result defies expectations, the abstract flags this explicitly with contrast language ("contrary to," "unexpectedly," "however") to heighten the contribution signal.
   - "contrary to common assumptions, consistently found that participants perceived a text-based chatbot as more judgmental than a human mental health care professional, even though the interactions were identical" [Raimi 2025]
   - "Second, and unexpectedly, we found that the contributions of affected physicians dropped dramatically after the policy window ended" [Zhang 2025]

9. **Multi-study summary sentence.** For multi-study papers, the abstract compresses the study sequence into one sentence naming how many studies and their types, rather than describing each.
   - "We conducted four experiments and a qualitative study" [Raimi 2025]

10. **Design science abstract variant.** For computational design papers, the abstract follows a modified arc: problem -> artifact name -> design principles -> evaluation results -> contribution. The method sentence names the artifact explicitly.
    - "we propose FastSR ... to automate the multistep, expertise-intensive SR process using minimal training data" [Liu-EBM 2025]

### Updated anti-patterns

- The "no specific numerical results" anti-pattern should be softened: healthcare/policy MISQ papers DO include effect sizes (percentage points, probability changes) when the number itself is the finding. Behavioral papers still avoid raw coefficients.
- Do NOT exceed ~185 words even for complex multi-study papers. Weng (2026) pushes this limit but is an outlier.

### Exemplar sentences from new papers

**Opening move**:
- "Incentives make or break user contributions." [Zhang 2025]
- "Many information technology (IT) projects fail to deliver the promised value within the initial budget and the estimated schedule." [Weng 2026]
- "Only a fraction of people with mental health issues seek medical care, in part because of fear of judgment" [Raimi 2025]

**Findings sentence (with numbers, healthcare)**:
- "We found that despite an increase in physician contributions during the policy window, the introductory incentives unintentionally decreased physician contributions after the policy window ended." [Zhang 2025]
- "we found that the greater the EHR adoption by care providers, the less likely a claim is denied." [Ayabakan 2025]

**Close on contribution/implication**:
- "Our work thus contributes to the IT project management literature by extending the nomological network of IT project risk and control and incorporating the people aspect into this framework." [Weng 2026]
- "This study provides significant theoretical insights into the information systems literature on HIT and offers practical implications for healthcare providers" [Ayabakan 2025]
