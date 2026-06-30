# NatComm Discussion -- Section Style Guide

Extracted from 11 Nature Communications exemplar papers (healthcare AI / clinical ML / LLM in medicine / prescribing). Supplements `style-profile.md`.

## Word budget

- 550-3,000 words. Highly variable across papers.
- ho-2026: ~550w (4 paras). buckley-2026: ~750w (6 paras). lin-2026: ~700w (3 paras). li-2026-benchmark: ~1,100w (6 paras). zhou-2026: ~1,150w (5 paras). abdallah-2026: ~1,200w (6 paras). gaudio-2026: ~1,400w (6 paras). xu-2026: ~1,800w (10 paras). adetunji-2026: ~2,200w (9 paras). salvatore-2026: ~2,700w (13 paras). chen-2026: ~2,800w (12 paras). li-2026-memorization: ~3,000w (16 paras).
- Discussion is typically shorter than Results -- often 1/3 to 1/2 the length.
- Paragraph count: 3-16. Modal count is 4-6.

## Section title variants

Three patterns observed:
- **"Discussion"** as a standalone section title (most papers: ho-2026, zhou-2026, abdallah-2026, chen-2026, salvatore-2026, li-2026-memorization, buckley-2026, lin-2026, gaudio-2026, adetunji-2026, larcher-2026)
- No separate "Conclusion" section in most NatComm papers. The closing paragraph of Discussion serves as the conclusion.
- Some papers use bold sub-headings within Discussion (xu-2026: "Limitations and Future Work"; li-2026-memorization: 5 sub-headed sections; chen-2026: 12 sub-headed paragraphs).

## Arc

```
P1: Restate contribution at high level (what was done, what was demonstrated)
P2-P(n-2): Interpretation + positioning (what results mean, comparison with prior work)
P(limit): Limitations + future directions
P(n): Broader significance / closing sentence
```

The arc opens with a contribution restatement (not a repeat of the abstract, but a higher-level synthesis), moves through interpretation and positioning, addresses limitations explicitly, and closes with significance or future directions.

## Signature moves

1. **Contribution restatement opening.** The first Discussion sentence restates the contribution at a synthesis level:
   - "In this paper, we presented GAME, a framework that successfully harmonizes heterogeneous EHR codes by jointly integrating institution-specific co-occurrence statistics, ontological structures, and LLM-derived semantics." [zhou-2026]
   - "This study examined fairness and interpretability in MRI-based dementia classification across multi-racial and multi-ethnic populations." [ho-2026]
   - "We developed the ClinDiag-Framework to assess the performance of large language models (LLMs) in real-world clinical diagnostics." [chen-2026]
   - "Most current AI systems still function primarily as tools used by physicians." [xu-2026] (field-level framing first, then own contribution)
   - "Clinical trial recruitment remains a major bottleneck in the development of new therapies." [abdallah-2026] (problem framing first, then own contribution)
   - "GLP-1 RAs, including semaglutide (e.g., Ozempic), have garnered widespread attention, largely due to media coverage of their substantial weight loss effects..." [salvatore-2026] (context framing first)
   - "Here, we systematically evaluated the capacity of large language models (LLMs) to support liquid-biopsy biomarker discovery and classifier construction." [gaudio-2026]
   - "This study highlights interactions of anthropometric, behavioral, and familial features that consistently signal elevated Type 2 Diabetes (T2D) risk across sub-Saharan African populations." [adetunji-2026]
   - Two opening styles: (a) direct restatement ("In this paper, we presented..." / "This study examined...") and (b) field-level context then pivot to own work ("Clinical trial recruitment remains...").

2. **Interpretation + positioning against prior work.** The middle paragraphs contextualize findings against the literature:
   - "Compared to existing state-of-the-art LLMs, DxDirector-7B achieves superior diagnostic accuracy while markedly reducing both the clinical workload." [xu-2026]
   - "TrialMatchAI achieves this level of performance using lightweight, open-source models, a significant advancement given the computational demands and expense typically associated with high-performance LLMs." [abdallah-2026]
   - "Our study extends beyond the work of Xie and colleagues..." [salvatore-2026]
   - Point-by-point comparison with specific prior studies is common in Discussion (more so than NMI).

3. **Explicit limitations paragraph.** Limitations are introduced with a stock phrase in nearly every paper:
   - "Our study has several limitations." [buckley-2026]
   - "Several limitations should be considered." [ho-2026, gaudio-2026]
   - "This study also has several important limitations." [salvatore-2026]
   - "Despite numerous strengths, our study is not devoid of limitations." [larcher-2026]
   - "Limitations and Future Work" [xu-2026] -- as a sub-headed section
   - "Limitations and future work" [li-2026-memorization] -- as a sub-headed section with 6 items
   - One exception: zhou-2026 distributes limitations across multiple paragraphs rather than collecting them in one dedicated paragraph.

4. **Limitation-paired-with-future-direction.** Each limitation is frequently followed by a mitigation or future-work suggestion:
   - "[limitation] Cross-sectional design precludes causality -> [future] Longitudinal studies would be needed" [adetunji-2026]
   - "[limitation] focused on structured codes -> [future] can be extended to incorporate unstructured clinical text" [zhou-2026]
   - "[limitation] Minoritized groups remain smaller -> [future] extending to multimodal biomarkers and longitudinal trajectories" [ho-2026]
   - "[limitation] prompt adherence varies across models -> [future] versioned prompts and explicit model identifiers" [gaudio-2026]
   - This creates a paired rhythm: gap-then-opportunity.

5. **Sub-headed Discussion (common in NatComm).** Unlike NMI where sub-headed Discussions are rare, NatComm papers frequently use bold sub-headings to organize Discussion:
   - xu-2026: "Limitations and Future Work" sub-section
   - chen-2026: 12 sub-headed paragraphs covering different aspects
   - li-2026-memorization: 5 sub-sections: (1) prevalent memorization, (2) distinct characteristics, (3) impact on development, (4) recommendations, (5) limitations
   - This pattern allows longer Discussions (2,000-3,000w) to remain navigable.

6. **Closing sentence on broader significance.** The final sentence projects forward:
   - "Its emphasis on transparency and semantic consistency ensures that EHR-driven machine learning can evolve equitably, supporting scalable and interpretable models across the heterogeneous landscape of global healthcare data." [zhou-2026]
   - "Overall, our results indicate that fairness-aware learning objectives such as RegAlign, combined with diverse training data and interpretable analyses, are important for developing fair and generalizable dementia classification models." [ho-2026]
   - "By combining high accuracy, interpretability, and privacy-preserving local deployment, TrialMatchAI sets a new standard for AI-driven clinical trial matching." [abdallah-2026]
   - "These findings reinforce the need to consider comorbidities, sex-specific risks, and pharmacogenomic variation in clinical decision-making and point toward the promise of precision prescribing in T2D and obesity care." [salvatore-2026]
   - "Collectively, these directions will contribute to a more comprehensive understanding of memorization and support the development of effective solutions for the safe and responsible adoption of LLMs in medicine." [li-2026-memorization]
   - "Continued exploration along these directions may transform the current healthcare paradigm..." [xu-2026]

## Exemplar sentences (shape, not content)

**Limitation sentences**:
- "First, it included retrospective data from a single large database..." [larcher-2026]
- "First, minoritized groups remain smaller than NHW in the full dataset, and scarcity can affect both model stability and attribution robustness despite harmonization and repeated resampling." [ho-2026]
- "Several limitations should be considered. First, prompt adherence varied across models and cohorts." [gaudio-2026]

**Closing sentences** (significance / forward-looking):
- "Ultimately, model performance is always dependent on context, and the next studies of multimodal models will need to leverage the distinct strengths of AI and physicians." [buckley-2026]
- "Through this initiative, we aim to promote the development of LLMs for general practice and contribute to the advancement and optimization of clinical decision support systems." [li-2026-benchmark]
- "Reproducible deployment will require versioned prompts, explicit model identifiers, and systematic logging of intermediate outputs and failure modes." [gaudio-2026]

## Anti-patterns

- Do NOT write a Discussion longer than Results. Discussion should be compact relative to the evidence presented.
- Do NOT introduce new results or data in the Discussion. All empirical evidence belongs in Results.
- Do NOT omit limitations. NatComm expects explicit acknowledgment of limitations, nearly always as a dedicated paragraph or subsection.
- Do NOT write limitations without paired future directions. Each limitation should pivot to an opportunity.
- Do NOT repeat the abstract verbatim as the opening of the Discussion. Restate the contribution at a higher synthesis level.
- Do NOT end on a limitation. End on significance, broader impact, or future potential.
- Do NOT write an excessively long Discussion without sub-headings. If Discussion exceeds ~1,500 words, consider using bold sub-headings for organization.

## Paragraph structure

Typical 4-6 paragraph structure (compact Discussion):

| Para | Job | Proportion |
|------|-----|-----------|
| P1 | Contribution restatement + summary | ~20% |
| P2-P3 | Interpretation + positioning against prior work | ~30% |
| P(limit) | Limitations + future directions (may be 1-3 paragraphs) | ~30% |
| P(n) | Broader significance / closing | ~20% |

Extended Discussion (10+ paragraphs):

| Block | Job | Proportion |
|-------|-----|-----------|
| Opening (1-2 paras) | Contribution restatement | ~15% |
| Interpretation (3-5 paras) | Point-by-point positioning | ~35% |
| Recommendations (1-2 paras) | Optional, common in policy-relevant papers | ~15% |
| Limitations (1-3 paras) | Dedicated subsection | ~20% |
| Closing (1 para) | Significance / forward-looking | ~15% |

## Contrast with NMI

- NMI Discussions are 450-2,000 words. NatComm Discussions have a wider range: 550-3,000 words.
- NMI rarely uses sub-headings in Discussion. NatComm frequently uses them for longer Discussions.
- NMI enumerates contributions in Discussion ("First...Second...Third"). NatComm does this less consistently.
- Both journals require explicit limitations with paired future directions.
- Both journals close on significance/forward-looking statements.

## Contrast with IS journals

- IS Discussions are typically 3,000-5,000 words with sub-sections (Theoretical Implications, Practical Implications, Limitations, Future Research). NatComm Discussions are 550-3,000 words.
- IS journals separate "Limitations" and "Future Research" into distinct sub-sections. NatComm pairs each limitation immediately with a future direction.
- IS journals have a dedicated "Implications for Practice" subsection. NatComm weaves practical implications into interpretation and closing paragraphs.
- IS journals devote substantial discussion to theoretical contribution. NatComm focuses on technical, clinical, and scientific significance.
- IS Discussions are often the longest section. NatComm Discussions are shorter than Results.
