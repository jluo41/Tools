# NMI Discussion -- Section Style Guide

Extracted from 8 Nature Machine Intelligence exemplar papers. Supplements `style-profile.md`.

## Word budget

- 450-2,000 words. Highly variable across papers.
- mataraso-2025: ~450w (4 paras). gu-2026: ~450w (4 paras). chen-w-2025: ~650w (5 paras). mon-williams-2025: ~950w (6 paras). pontikos-2025: ~1,100w (7 paras). qiao-2025: ~1,100w (7 paras). doerig-2025: ~1,500w (~10 paras). serapio-garcia-2025: ~2,000w (with sub-headings).
- Discussion is typically much shorter than Results -- often 1/3 to 1/4 the length.
- Paragraph count: 4-10. Modal count is 4-7.

## Section title variants

Two patterns observed:
- **"Discussion"** as a standalone section, sometimes followed by a separate **"Conclusion"** section (serapio-garcia-2025, qiao-2025, pontikos-2025, doerig-2025, chen-w-2025, mataraso-2025)
- **"Discussion and conclusion"** as a combined section (gu-2026)
- Some papers have no explicit "Conclusion" heading but include "In conclusion,..." as the opening of the final paragraph (mon-williams-2025, pontikos-2025, qiao-2025)

## Arc

```
P1: Restate contribution at high level (what was done, what was demonstrated)
P2-P(n-2): Interpretation + positioning (what results mean, how they compare to prior work)
P(limit): Limitations (explicit, often with "several limitations" formula)
P(n): Conclusion / broader significance / future directions
```

The arc opens with a contribution restatement (not a repeat of the abstract, but a higher-level synthesis), moves through interpretation and positioning, addresses limitations explicitly, and closes with significance or future directions.

## Signature moves

1. **Contribution restatement opening.** The first Discussion sentence restates the contribution at a synthesis level, not repeating the abstract but framing what was accomplished:
   - "The goal of this work was to contribute a principled methodology to reliably and validly measure synthetic personality in LLMs..." [serapio-garcia-2025]
   - "We demonstrated COMET's ability to improve predictive modelling across various tasks through pretraining and transfer learning..." [mataraso-2025]
   - "Our results demonstrate that CSFM robustly generalizes across a wide range of clinical scenarios, devices and input configurations." [gu-2026]
   - "This work contributes to the growing field of generative artificial intelligence for science, with a specific application in cardiac imaging." [qiao-2025]
   - "We tested our methodology -- the ELLMER framework -- that combines..." [mon-williams-2025]
   - "Using a variety of techniques, including RSA, encoding models, linear decoding and ANN modelling, we have provided evidence for the hypothesis that..." [doerig-2025]
   - "In this study, we aim to enable rigorous data-driven scientific discoveries..." [chen-w-2025]

2. **Explicit enumeration of contributions in Discussion.** Some papers list contributions using "First...Second...Third...Finally" within the opening paragraph (unlike the Introduction, where this is uncommon):
   - "First, we developed MeshHeart...Second, we demonstrated MeshHeart's capability...Third, we investigated the latent vector...Finally, we propose a latent delta..." [qiao-2025]

3. **"Several limitations" formula.** Limitations are introduced with a stock phrase:
   - "There are several limitations to this study." [mataraso-2025]
   - "Although this work advances the science in personalized cardiac modelling, there are several limitations." [qiao-2025]
   - "Despite these promising results, our work has several limitations." [gu-2026]
   - Some papers embed limitations without this formula, weaving caveats into interpretive paragraphs (doerig-2025: "it cannot be fully ruled out", "it is important to note").

4. **Limitation-paired-with-future-direction.** Each limitation is immediately followed by a mitigation or future work suggestion:
   - "[limitation] restricted generating factors (age, sex, weight, height only) -> [future] future work will incorporate additional variables" [qiao-2025]
   - "[limitation] unknown generalization to different architectures -> [future] future work will focus on assessing generalizability" [mataraso-2025]
   - "[limitation] interpretability of deep models / black box -> [future] Future work should explore explanation generation" [gu-2026]
   - This creates a paired rhythm: gap-then-opportunity.

5. **Sub-headed Discussion (rare but present).** One paper uses explicit sub-headings within Discussion:
   - "Limitations and future work" -> "Broader implications" -> "Ethical considerations" -> "Conclusion" [serapio-garcia-2025]
   - This is the exception, not the rule. Most NMI Discussions are un-sub-headed.

6. **Positioning against prior work in Discussion.** While the Introduction identifies the gap, the Discussion is where direct comparison with prior methods happens:
   - "So far, only four previous studies have tried to apply AI to IRDs, all in much smaller datasets of fewer than 150 patients and across substantially fewer genes." [pontikos-2025]
   - "Our approach based on LLM embeddings should not be seen as a competitor to these lines of work, but rather as synergistic." [doerig-2025]

7. **"In conclusion" closing paragraph.** When present, the concluding paragraph begins with "In conclusion" and provides a single-sentence synthesis + forward look:
   - "In conclusion, this study presents MeshHeart, a generative model for cardiac shape modelling." [qiao-2025]
   - "In conclusion, Eye2Gene shows that next-generation phenotyping using AI is a promising approach to aid in the genetic diagnosis for individuals with IRDs..." [pontikos-2025]
   - "In conclusion, CSFM represents an advancement in cardiac sensing..." [gu-2026]

## Exemplar sentences (shape, not content)

**Closing sentences** (significance / forward-looking):
- "This work has important implications for AI alignment and harm mitigation, and informs ethics discussions concerning AI anthropomorphization, personalization and potential misuse." [serapio-garcia-2025]
- "As multimodal biomedical data availability grows, COMET provides a foundation for unravelling complex relationships between clinical phenotypes and molecular mechanisms and can change how we analyse data from omics studies." [mataraso-2025]
- "Overall, this work lays the groundwork for versatile cardiac monitoring tools poised to improve patient care and outcomes in cardiovascular medicine." [gu-2026]
- "These findings pave the way for future research on cardiac modelling and may inspire the development of generative modelling techniques for other types of biomedical data." [qiao-2025]
- "We believe that this powerful tool will pave the way for the broader deployment of ML models in scientific discovery and hypothesis validation." [chen-w-2025]
- "...we anticipate that LLM embeddings -- and ANN models capable of extracting such embeddings from visual inputs -- will open up fresh directions and yield new insights for both visual computational neuroscience and NeuroAI." [doerig-2025]

**Limitation sentences**:
- "ELLMER is based on two assumptions concerning computer vision: (1) a single-shot vision system to form an affordance map..." [mon-williams-2025]
- "The current focus is pairwise interactions; higher-order is important but combinatorially hard." [chen-w-2025]

## Anti-patterns

- Do NOT write a Discussion longer than Results. Discussion should be compact relative to the evidence presented.
- Do NOT introduce new results or data in the Discussion. All empirical evidence belongs in Results.
- Do NOT omit limitations. NMI expects explicit acknowledgment of limitations with future directions.
- Do NOT write limitations without paired future directions. Each limitation should pivot to an opportunity.
- Do NOT repeat the abstract verbatim as the opening of the Discussion. Restate the contribution at a higher synthesis level.
- Do NOT write a "Related Work" section disguised as Discussion. Brief comparison with prior work is fine, but the Discussion should not become a literature survey.
- Do NOT end on a limitation. End on significance, broader impact, or future potential.

## Paragraph structure

Typical 4-7 paragraph structure:

| Para | Job | Proportion |
|------|-----|-----------|
| P1 | Contribution restatement + summary | ~20% |
| P2-P3 | Interpretation + positioning against prior work | ~30% |
| P(limit) | Limitations + future directions (may be 1-2 paragraphs) | ~25% |
| P(n) | Conclusion / broader significance | ~15% |
| (Optional) | Ethical considerations (serapio-garcia-2025 only) | ~10% |

## Contrast with IS journals

- IS Discussions are typically 3,000-5,000 words with sub-sections (Theoretical Implications, Practical Implications, Limitations, Future Research). NMI Discussions are 450-2,000 words, usually without sub-sections.
- IS journals separate "Limitations" and "Future Research" into distinct sub-sections. NMI pairs each limitation immediately with a future direction.
- IS journals have a dedicated "Implications for Practice" subsection. NMI weaves practical implications into the closing paragraph.
- IS journals devote substantial discussion to theoretical contribution. NMI focuses on technical and scientific significance.
- IS Discussions do not include ethical considerations. NMI may include ethics within Discussion (serapio-garcia-2025) or as a subsection in Methods.
- IS Discussions are often the longest section. NMI Discussions are among the shortest.
