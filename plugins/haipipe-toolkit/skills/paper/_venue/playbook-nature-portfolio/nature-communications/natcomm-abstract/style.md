# NatComm Abstract -- Section Style Guide

Extracted from 8 Nature Communications exemplar papers (healthcare AI / clinical ML / LLM in medicine / prescribing). Supplements `style-profile.md`.

## Word budget

- 110-280 words. Median ~200 words.
- chen-2026: ~110w. xu-2026: ~170w. zhou-2026: ~170w. ho-2026: ~200w. salvatore-2026: ~200w. li-2026: ~250w. abdallah-2026: ~280w.
- Unstructured single paragraph (most papers). Some preprint-formatted papers (li-2026) use two paragraphs, but the published NatComm convention is a single paragraph.
- No labeled sub-fields (no "Background / Methods / Results / Conclusions" headers). Never bulleted or numbered.

## Arc

```
clinical/scientific problem (why this matters broadly)
  -> gap or limitation (what current approaches cannot do)
  -> contribution pivot ("Here we..." / "We present..." / "In this work, we...")
  -> what the system/study does (1-2 sentences, high-level design)
  -> key results (headline numbers or directional claims)
  -> significance / implications close
```

The arc is **problem-forward, contribution-centered**. The abstract opens with a broad real-world challenge, not the method. The contribution pivot appears mid-abstract. Results are stated with concrete numbers (accuracy percentages, hazard ratios, sample sizes). The final sentence points to broader implications or clinical utility.

## Signature moves

1. **Problem-first opening.** The first sentence establishes a real-world clinical or scientific challenge, not the method:
   - "Clinical diagnosis in the real world often begins with ambiguous patient complaints that require iterative reasoning and testing." [xu-2026]
   - "Although Large Language Models (LLMs) possess extensive medical knowledge, they often struggle to emulate the complex, iterative process of real-world clinical diagnosis." [chen-2026]
   - "Glucagon-like peptide-1 receptor agonists (GLP-1 RAs) are increasingly prescribed for type 2 diabetes (T2D) and weight management, yet their real-world health impacts remain understudied." [salvatore-2026]
   - "Dementia, a degenerative disease affecting millions globally, is projected to triple by 2050." [ho-2026]
   - "The widespread adoption of electronic health records has created new opportunities for translational clinical research, yet this promise remains constrained by fragmented data across privacy-siloed institutions." [zhou-2026]
   - "Patient recruitment remains a major bottleneck in clinical trials, calling for scalable and automated solutions." [abdallah-2026]

2. **Contribution pivot with system name.** The method/system name is introduced at a clear pivot point, typically after the gap statement:
   - "Here we present DxDirector-7B, an agentic LLM designed to navigate the full diagnostic process through advanced slow thinking capabilities." [xu-2026]
   - "we present ClinDiag-GPT, a specialized LLM fine-tuned to execute full diagnostic procedures" [chen-2026]
   - "We present TrialMatchAI, an AI-powered recommendation system that automates patient-to-trial matching" [abdallah-2026]
   - "We introduce a graph-based framework that addresses this gap by treating data harmonization as a scalable representation learning problem." [zhou-2026]
   - "In this work, we investigate memorization of LLMs in medicine, assessing its prevalence, characteristics, volume, and potential downstream impacts." [li-2026]
   - "This study investigates performance discrepancies in dementia classification among 6,584 Non-Hispanic White, 1,263 Non-Hispanic African American, and 713 Hispanic White populations." [ho-2026]

3. **Concrete numbers in results.** Unlike NMI which uses directional claims, NatComm abstracts include specific quantitative results:
   - "DxDirector-7B achieves superior diagnostic accuracy compared to state-of-the-art medical and general-purpose LLMs with significantly fewer parameters." [xu-2026]
   - "diagnostic accuracy ranged from 29.32% to 39.76%" [chen-2026]
   - "per-protocol hazard ratio 0.31, 95% confidence interval (0.17-0.55)" [salvatore-2026]
   - "memorization ratios of consecutive 30 tokens range from 10% to 20%" [li-2026]
   - "92% of oncology patients had at least one relevant trial retrieved within the top 20 recommendations" [abdallah-2026]

4. **Close on implications, not the method.** The final sentence pivots from specific results to broader significance:
   - "offering a scalable solution to enhance diagnostic efficiency and accessibility." [xu-2026]
   - "demonstrating the utility of ClinDiag-GPT as a clinical assistant." [chen-2026]
   - "with implications for clinical decision-making and personalized prescribing." [salvatore-2026]
   - "improving the accuracy and equity of MRI-based dementia classification." [ho-2026]
   - "a robust, data-centric foundation for training and deploying clinical models across heterogeneous healthcare systems." [zhou-2026]
   - "a scalable solution for AI-driven clinical trial matching in precision medicine." [abdallah-2026]

## Exemplar sentences (shape, not content)

**Opening move** (problem/challenge first):
- "Large Language Models (LLMs) have demonstrated significant potential in medicine, with many studies adapting them through continued pretraining or fine-tuning on medical data." [li-2026]
- "Early and precise diagnosis is essential for effective treatment and improved quality of life." [ho-2026]

**Gap sentence**:
- "they currently lack the ability to autonomously drive this entire diagnostic workflow, limiting their potential to significantly alleviate physician workload." [xu-2026]
- "yet their real-world health impacts remain understudied." [salvatore-2026]
- "this promise remains constrained by fragmented data across privacy-siloed institutions and substantial heterogeneity in local coding practices." [zhou-2026]

**Findings sentence** (specific metric or claim):
- "We observed significant cross-group bias, particularly when models trained on one group are tested on another." [ho-2026]
- "semaglutide demonstrates reduced risk for genitourinary infections in women" [salvatore-2026]
- "memorization is prevalent and significantly higher than that in the general domain" [li-2026]

## Anti-patterns

- Do NOT use structured/labeled fields (Background, Methods, Results, Conclusions). NatComm uses one unstructured paragraph.
- Do NOT open with the method name. Open with the clinical problem or field importance.
- Do NOT end on the method or a specific metric. End on significance, implications, or clinical utility.
- Do NOT omit quantitative results. NatComm abstracts include specific numbers (accuracy percentages, hazard ratios, sample sizes), unlike NMI which stays more directional.
- Do NOT use passive-heavy construction. NatComm abstracts are active-voice ("We present", "We show", "We investigate").
- Do NOT exceed ~280 words. Most NatComm abstracts are under 220.

## Paragraph structure

One paragraph only (standard). No line breaks, no sub-sections, no bullet lists.

Sentence count: 6-12 sentences following this pattern:
1. Problem/importance (1-2 sentences)
2. Gap or what was not possible (1 sentence)
3. Contribution pivot + system/study name (1 sentence)
4. What the system does or study design (1-3 sentences)
5. Key results (2-4 sentences, with concrete numbers)
6. Significance / broader implications (1 sentence)

## Contrast with NMI

- NMI abstracts use "Here we..." pivot more consistently. NatComm uses a mix: "Here we present...", "We present...", "In this work, we...", "This study investigates..."
- NMI abstracts are more directional in results reporting. NatComm includes more specific numbers (percentages, hazard ratios, CIs).
- NMI papers are more method-centric (always name a system). NatComm accommodates both system papers (xu, chen, zhou, abdallah) and empirical/evaluation papers (salvatore, li, ho) where no system name is introduced.
- NMI abstracts rarely exceed 230w. NatComm can run to 280w.

## Contrast with IS journals

- MISQ abstracts are ~120-160 words (shorter). NatComm abstracts run 110-280 words.
- MISQ opens with the research question. NatComm opens with the domain problem.
- MISQ names theoretical constructs and directional relationships. NatComm names the system and its capability or the empirical investigation.
- MISQ closes on "implications are discussed." NatComm closes on broad significance or clinical utility.
- MISQ avoids any numbers. NatComm includes concrete metrics (accuracy, HR, CI).
