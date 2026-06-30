# NMI Abstract -- Section Style Guide

Extracted from 8 Nature Machine Intelligence exemplar papers. Supplements `style-profile.md`.

## Word budget

- 160-270 words. Median ~200 words.
- mon-williams-2025: ~160w. mataraso-2025: ~175w. pontikos-2025: ~175w. serapio-garcia-2025: ~195w. chen-w-2025: ~220w. doerig-2025: ~230w. qiao-2025: ~230w. gu-2026: ~270w.
- Unstructured single paragraph. No labeled sub-fields (no "Background / Methods / Results / Conclusions" headers). Never bulleted or numbered.

## Arc

```
clinical/scientific problem (why this matters broadly)
  -> gap or limitation (what was not possible / not understood)
  -> "Here we..." contribution pivot (name the method/system)
  -> what the method does (1-2 sentences, high-level mechanism)
  -> key results (headline numbers or directional claims)
  -> significance / broader applicability close
```

The arc is **problem-forward, contribution-centered**. The abstract opens with broad stakes, not the method. The method name appears mid-abstract at the contribution pivot. Results are summarized with 1-2 headline metrics or directional findings. The final sentence points to significance or broad applicability, not the method.

## Signature moves

1. **"Here we..." pivot.** The contribution is introduced with a formulaic phrase that marks the turn from gap to this paper's advance. Variants observed:
   - "Here, we present a comprehensive psychometric methodology..." [serapio-garcia-2025]
   - "Here we present a cardiac sensing foundation model (CSFM)..." [gu-2026]
   - "Here we report an embodied large-language-model-enabled robot (ELLMER) framework..." [mon-williams-2025]
   - "Here we test whether the contextual information..." [doerig-2025]
   - "Here, to this end, we developed a conditional generative model, MeshHeart..." [qiao-2025]
   - "We introduce clinical and omics multimodal analysis enhanced with transfer learning (COMET)..." [mataraso-2025]
   - "We demonstrate a deep learning algorithm, Eye2Gene..." [pontikos-2025]
   - "In this study, we introduce Diamond..." [chen-w-2025]

2. **System/method name introduced at the pivot.** The branded name (COMET, Eye2Gene, MeshHeart, CSFM, ELLMER, Diamond) always appears at or immediately after the contribution pivot sentence, with its acronym expansion in parentheses. Never in the opening sentences.

3. **Close on significance, not the method.** The final sentence pivots from specific results to generalizability or broader impact:
   - "This framework can be broadly applied to the analysis of multimodal omics studies and reveals more powerful biological insights from limited cohort sizes." [mataraso-2025]
   - "This demonstration marks progress towards scalable, efficient and 'intelligent robots' able to complete complex tasks in uncertain environments." [mon-williams-2025]
   - "This highlights its potential as a versatile and scalable foundation for comprehensive cardiac monitoring." [gu-2026]
   - "Eye2Gene is accessible online (app.eye2gene.com) for research purposes." [pontikos-2025]

4. **Hedged result language.** Results in the abstract are stated as demonstrated findings, not as universal claims. Verbs: "we found that", "we showed that", "we demonstrate", "we show that". Never "we prove" or "our method achieves state-of-the-art."

## Exemplar sentences (shape, not content)

**Opening move** (problem/importance first):
- "The advent of large language models (LLMs) has revolutionized natural language processing, enabling the generation of coherent and contextually relevant human-like text." [serapio-garcia-2025]
- "Cardiovascular diseases remain a major contributor to the global burden of healthcare, highlighting the importance of accurate and scalable methods for cardiac monitoring." [gu-2026]
- "Understanding the structure and motion of the heart is crucial for diagnosing and managing cardiovascular diseases, the leading cause of global death." [qiao-2025]
- "Completing complex tasks in unpredictable settings challenges robotic systems, requiring a step change in machine intelligence." [mon-williams-2025]

**Gap sentence**:
- "Omics studies produce a large number of measurements, enabling the development, validation and interpretation of systems-level biological models." [mataraso-2025] (the limitation -- small cohorts -- follows immediately)
- "Rare eye diseases such as inherited retinal diseases (IRDs) are challenging to diagnose genetically." [pontikos-2025]

**Findings sentence** (headline metric or directional claim):
- "Applying this method to 18 LLMs, we found that: (1) many LLMs manifest personality traits in a reliable and valid way..." [serapio-garcia-2025]
- "Latent space features are discriminative for cardiac disease classification, whereas latent delta exhibits strong correlations with clinical phenotypes in phenome-wide association studies." [qiao-2025]
- "CSFM outperforms traditional approaches and maintains robust performance across varying lead configurations..." [gu-2026]

## Anti-patterns

- Do NOT use structured/labeled fields (Background, Methods, Results, Conclusions). NMI uses one unstructured paragraph.
- Do NOT open with the method name. Open with the problem or the field's importance.
- Do NOT end on the method or a specific metric. End on significance or applicability.
- Do NOT include detailed statistics (p-values, confidence intervals, regression coefficients) in the abstract. Name the direction or a single headline metric.
- Do NOT use passive-heavy construction. NMI abstracts are active-voice ("We show", "We introduce", "Here we report").
- Do NOT exceed ~270 words. Most NMI abstracts are under 230.

## Paragraph structure

One paragraph only. No line breaks, no sub-sections, no bullet lists.

Sentence count: 6-10 sentences following this pattern:
1. Problem/importance (1-2 sentences)
2. Gap or what was not possible (1 sentence)
3. "Here we..." contribution pivot + method name (1 sentence)
4. What the method does, high-level (1-2 sentences)
5. Key results (1-3 sentences, directional or headline metric)
6. Significance / broader applicability (1 sentence)

## Contrast with IS journals

- MISQ abstracts are ~120-160 words (shorter). NMI abstracts run 160-270 words.
- MISQ opens with the research question. NMI opens with the domain problem.
- MISQ names theoretical constructs and directional relationships. NMI names the system and its capability.
- MISQ closes on "implications are discussed." NMI closes on broad applicability or significance.
- MISQ never names a method in the abstract. NMI always introduces the system name at the pivot.
- MISQ avoids any numbers. NMI may include a single headline metric (accuracy, sample size).
