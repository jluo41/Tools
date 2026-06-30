# Nature Medicine Discussion -- Section Style Guide

Extracted from 14 Nature Medicine exemplar papers (2025-2026). Supplements `style-profile.md`.

## Word budget

- 750-1,800 words. Highly variable across papers.
- bean-2026: ~750w (4 paras). brinton-2026: ~1,500w (8 paras). saab-2026: ~1,800w (10 paras). varoquaux-2026: ~1,200w (10+ paras). osullivan-2026: ~1,500w (8 paras). tao-2026: ~1,100w. lang-2026: ~1,200w (7 paras). nijman-2026: ~1,600w (8 paras). lu-2026: ~1,200w. khasentino-2025: ~1,400w. bedi-2026: ~1,200w. vaidya-2026: ~800w. perez-2026: ~1,200w. yao-2026: ~1,500w. zhou-2026: ~1,600w (6 paras).
- Discussion is typically shorter than Results and often shorter than Methods. It is among the shortest sections.
- Paragraph count: 4-10. Modal count is 6-8.

## Section title variants

Two patterns observed:
- **"Discussion"** as a standalone section (dominant pattern in all 14 exemplars)
- No separate "Conclusion" section. Concluding sentences appear within the final Discussion paragraph, often beginning with "In conclusion,..." or "In summary,..."

## Arc

```
P1: Restate main finding or contribution in clinical context
P2-P(n-3): Clinical interpretation + positioning against prior evidence
  -> Process findings (documentation, workflow, clinical decision-making)
  -> Null-result explanation (when applicable)
  -> Mechanism / why it worked or did not
P(limit): Limitations (explicit, often with formulaic opening phrase)
P(n): Clinical implications + future directions / "In conclusion" close
```

The arc opens with a clinical-context restatement of the finding (not an abstract repeat), moves through interpretation positioned against prior clinical evidence, addresses limitations explicitly, and closes with clinical implications or future directions.

## Signature moves

1. **Clinical-context restatement opening.** The first Discussion sentence restates the main finding in clinical terms, embedding the study type and setting:
   - "Our findings highlight the challenges of public deployments of LLMs for direct patient care." [bean-2026]
   - "In this large-scale pragmatic randomized controlled trials of a generative LLM embedded in routine clinical workflows across the full spectrum of primary care, we found similar rates of 14-day treatment failure between groups, extending emerging evidence from recent randomized evaluations in other clinical settings." [brinton-2026]
   - "In this work, as illustrated in Fig. 1, we sought to address a key unmet need for medical AI systems to be able to understand, reason about and appropriately use information from multimodal medical data during the course of diagnostic conversations with patients." [saab-2026]
   - "This large, multisite randomized study has shown that AI prioritization of CXRs did not improve the speed of the lung cancer diagnostic pathway." [varoquaux-2026]
   - "In this study, we probe the ability of LLMs to provide additive support to generalists in the assessment of rare, life-threatening cardiac diseases that typically require subspecialty cardiac care." [osullivan-2026]
   - "The results from this prospective, paired, noninferiority clinical trial demonstrate that in a prospective setting it is safe to use AI to identify screening exams that can be automatically labeled as normal." [lang-2026]
   - "This multicountry prospective study, conducted in seven locations across Asia, developed and validated clinical prediction models that outperform the current standard of care for triage of febrile children in resource-constrained community settings." [nijman-2026]
   - "SPARK introduces a concept-centered framework for AI pathology tackling common limits of single-modality, task-specific models." [vaidya-2026]
   - "The results of this study provide strong evidence to support the potential of consumer-wearable data in estimating cardiorespiratory fitness and building remote monitoring methods for HF." [perez-2026]
   - "In this study of ~200,000 individuals with overweight (BMI 27-30 kg/m2) or obesity, we systematically investigated the performance of different data modalities..." [yao-2026]

2. **Formulaic limitations introduction.** Limitations are signaled with a stock phrase:
   - "This study has limitations." [vaidya-2026]
   - "The study had the following limitations:" [brinton-2026]
   - "Our study contains a number of important limitations, and the findings should be interpreted with appropriate caution and humility." [osullivan-2026]
   - "Several limitations must be discussed." [nijman-2026]
   - "Our study has the limitation of being a single-site investigation..." [lang-2026]
   - "The study has some limitations that merit consideration." [perez-2026]
   - "Some limitations should be acknowledged when interpreting our results." [yao-2026]
   - "While Reti-Pioneer's generalist capabilities are well validated, there are also several limitations that may merit further considerations." [zhou-2026]
   - "Several limitations warrant consideration when interpreting our findings." [tao-2026]
   - "Our work has several limitations." [khasentino-2025]
   - "A critical limitation of our work was that..." [lu-2026]

3. **Limitation-paired-with-mitigation.** Each limitation is followed by a contextualizing statement or future direction:
   - "[limitation] the trial was randomized at the level of the clinical officer -> [mitigation] the LLM-assisted interface was accessible only to intervention arm clinical officers, which helped limit cross-arm exposure." [brinton-2026]
   - "[limitation] text-report-only (not raw images) -> [future] future work will focus on direct image integration." [osullivan-2026]
   - "[limitation] single-site investigation -> [mitigation] the diversity within the site mitigates this concern." [lang-2026]

4. **Null-result explanation paragraphs.** When the primary outcome is null, 1-2 paragraphs explain why:
   - "The estimated effect corresponded to between 13 fewer and 1 additional treatment failures per 1,000 patients, indicating that any true effect, if present, is likely to be modest." [brinton-2026]
   - "The lack of improvement in AI prioritization is likely because, although the time to CXR report was shortened, it was not sufficiently reduced in the prioritization arm to influence the clinical pathway." [varoquaux-2026]

5. **Positioning against prior clinical evidence.** The Discussion compares results with prior trials and clinical studies:
   - "The improvement in process outcomes observed aligns with findings from both controlled and real-world studies." [brinton-2026]
   - "So far, only four previous studies have tried to apply AI to IRDs..." [analogous pattern from multiple papers]
   - "Our finding of no significant demographic bias contrasts with ref. 7, which reported race and sex effects in general-purpose LLMs." [levine-2026]

6. **"In conclusion" closing paragraph.** Most papers close with "In conclusion" or "In summary" as the opening of the final paragraph:
   - "In conclusion, this work advances AMIE to dynamically integrate multimodal reasoning within diagnostic conversations." [saab-2026]
   - "In summary, the intervention did not reduce short-term treatment failure, and no safety concerns were identified." [brinton-2026]
   - "In conclusion, AI triage and AI-supported screening that excludes low-risk mammograms from radiologist reading could be a safe and effective screening strategy..." [lang-2026]
   - "In conclusion, we developed and validated a risk prediction tool to identify individuals at high risk of developing obesity-related complications." [yao-2026]
   - "In conclusion, Reti-Pioneer represents a scalable and clinically translatable AI framework..." [zhou-2026]
   - "In conclusion, AMIE, a research LLM-based AI system, can improve general cardiologists' assessments of complex cardiac patients." [osullivan-2026]
   - Some papers omit "In conclusion" and use "In summary" [nijman-2026] or end on a forward-looking statement without the formula [bean-2026, vaidya-2026].

7. **Clinical implications emphasis.** Unlike NMI which emphasizes technical significance, Nature Medicine Discussion emphasizes what the findings mean for clinical practice and policy:
   - "We recommend that developers, as well as policymakers and regulators, consider human user testing as a foundation for better evaluating interactive capabilities before any future deployments." [bean-2026]
   - "CXR AI deployments should not include worklist prioritization in this context." [varoquaux-2026]
   - "The implications for clinicians are twofold..." [osullivan-2026]
   - "We envision OBSCORE to be implemented as a data-driven support tool for referral that complements existing frameworks." [yao-2026]

## Exemplar sentences (shape, not content)

**Opening sentences** (contribution restatement):
- "Our findings highlight the challenges of public deployments of LLMs for direct patient care." [bean-2026]
- "This large, multisite randomized study has shown that AI prioritization of CXRs did not improve the speed of the lung cancer diagnostic pathway." [varoquaux-2026]
- "In this study, we probe the ability of LLMs to provide additive support to generalists in the assessment of rare, life-threatening cardiac diseases that typically require subspecialty cardiac care." [osullivan-2026]

**Closing sentences** (clinical implications / forward-looking):
- "We recommend that developers, as well as policymakers and regulators, consider human user testing as a foundation for better evaluating interactive capabilities before any future deployments." [bean-2026]
- "Larger or adequately powered studies are needed to determine whether modest clinical benefits exist with greater precision." [brinton-2026]
- "these findings demonstrate progress toward AI systems that are capable of comprehensive clinical interactions." [saab-2026]
- "Our review offers a roadmap and recommendations for transforming this rapidly expanding but uneven evidence base into clinically meaningful progress." [lu-2026]

**Limitation sentences**:
- "Our study contains a number of important limitations, and the findings should be interpreted with appropriate caution and humility." [osullivan-2026]
- "Several limitations warrant consideration when interpreting our findings." [tao-2026]
- "A limitation is the use of a single AI product, which will inevitably have different performance characteristics from others." [varoquaux-2026]

## Anti-patterns

- Do NOT write a Discussion longer than Results. Discussion should be compact relative to the evidence presented.
- Do NOT introduce new data or statistical analyses in the Discussion. All empirical evidence belongs in Results.
- Do NOT omit limitations. Nature Medicine expects explicit, transparent acknowledgment of limitations.
- Do NOT end on a limitation. End on clinical implications, recommendations, or future directions.
- Do NOT repeat the abstract verbatim. Restate the contribution at a higher synthesis level with clinical context.
- Do NOT write limitations as a labeled subsection. Keep them woven into the Discussion flow as paragraph(s).
- Do NOT omit clinical implications. Nature Medicine expects the Discussion to state what findings mean for clinical practice, not just for the field.
- Do NOT use Discussion to conduct a comprehensive literature review. Brief positioning against prior clinical evidence is sufficient.
- Do NOT spin null results as positive. Acknowledge what was not found and explain why.

## Paragraph structure

Typical 6-8 paragraph structure:

| Para | Job | Proportion |
|------|-----|-----------|
| P1 | Main finding restatement in clinical context | ~15% |
| P2-P3 | Interpretation: what the finding means clinically | ~25% |
| P4-P5 | Positioning against prior evidence + mechanism | ~25% |
| P(limit) | Limitations + mitigations (1-2 paragraphs) | ~20% |
| P(n) | Clinical implications + "In conclusion" close | ~15% |

## Contrast with NMI

- NMI Discussions are 450-2,000 words (wide range). Nature Medicine Discussions are 750-1,800 words (similar range, slightly longer on average).
- NMI frames significance in terms of technical advance and broader scientific applicability. Nature Medicine frames significance in terms of clinical practice, patient care, and health policy.
- NMI sometimes enumerates contributions ("First...Second...Third") in the opening Discussion paragraph. Nature Medicine rarely does.
- Both venues pair limitations with future directions.
- Both venues use "In conclusion" or "In summary" to introduce the final paragraph.
- NMI may include ethical considerations as a Discussion sub-section (rare). Nature Medicine puts ethics in Methods.
- NMI Discussion never recommends specific clinical actions. Nature Medicine Discussion regularly makes clinical recommendations ("should not include worklist prioritization", "recommend human user testing").
- Nature Medicine Discussions explicitly engage with null results, explaining why interventions did not work. NMI rarely reports null results.
- Both venues position against prior work in the Discussion, but Nature Medicine compares against clinical trials while NMI compares against technical methods.
