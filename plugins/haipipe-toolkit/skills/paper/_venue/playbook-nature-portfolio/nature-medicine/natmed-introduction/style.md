# Nature Medicine Introduction -- Section Style Guide

Extracted from 14 Nature Medicine exemplar papers (2025-2026). Supplements `style-profile.md`.

## Word budget

- 350-1,200 words. Typical range: 750-1,000 words for Articles.
- bean-2026: ~900w (7 paras). brinton-2026: ~900w (5 paras). saab-2026: ~1,200w (6 paras). varoquaux-2026: ~800w (6 paras). osullivan-2026: ~900w (4 paras). lang-2026: ~750w (4 paras). nijman-2026: ~1,000w (5 paras). zhou-2026: ~800w (4 paras).
- Brief Communications have no labeled Introduction section; the opening ~350-500 words of body text serve this function (restrepo-2026: ~350w, 2 paras; levine-2026: ~500w, 4 paras).
- Paragraph count: 4-7 paragraphs. Modal count is 4-5.

## Arc

```
P1: Clinical problem / patient impact (why this matters to healthcare)
P2: Current approaches + their limitations (clinical or technical)
P3: (Optional) Additional background or deeper gap identification
P(n-1): "Here we..." or "In this study, we..." contribution pivot (name the study + system)
P(n): (Optional) Study scope preview (evaluation design, comparators, scale)
```

The arc is a **clinical funnel**: specific clinical problem narrows through current practice limitations, then opens to the study contribution. Unlike NMI which starts with broad domain importance, Nature Medicine starts with a specific patient-facing clinical challenge.

## Signature moves

1. **Clinical problem opening.** The first sentence establishes a clinical problem or public health burden, not a technology capability:
   - "Primary care facilities manage a wide range of acute and chronic conditions and serve as the foundation for continuity of care, coordination across health system levels and equitable service delivery." [brinton-2026]
   - "Healthcare delivery faces considerable challenges globally from aging populations and increasing care fragmentation through to clinician burnout and misalignment between clinical and financial incentives." [saab-2026]
   - "Lung cancer accounts for the highest proportion of cancer-related deaths in the United Kingdom (UK) and worldwide, primarily because it is common, is diagnosed at a late stage and/or late in the symptomatic period when patients have become too unwell for treatment." [varoquaux-2026]
   - "Recent breakthroughs in artificial intelligence (AI) research have the potential to democratize healthcare by expanding access to medical knowledge, bringing care closer to patients." [bean-2026]
   - "Infectious diseases account for the majority of the 2.5 million deaths that occur each year among children aged 1-59 months." [nijman-2026]
   - "Globally, there is a substantial shortage of specialized medical expertise." [osullivan-2026]
   - "The global rise in endocrine and metabolic diseases amid aging populations poses mounting challenges for healthcare systems." [zhou-2026]
   - "Breast cancer screening programs with digital mammography (DM) have been established for decades, with proven benefits in reducing breast cancer-related mortality." [lang-2026]

2. **Background-as-gap-identification.** Middle paragraphs survey current clinical practice and its limitations, then AI/technology approaches and their gaps. Each approach gets 1-3 sentences, ending with its limitation. The progression is typically: (a) clinical practice limitations, then (b) technology promise, then (c) technology limitations:
   - "However, prospective interventional evidence from real-world clinical studies, particularly in LMICs, remains limited." [brinton-2026]
   - "However, evidence validating the capabilities of LLMs for diagnostic conversations involving such multimodal data is scarce, revealing an important discrepancy between clinical needs and current technology." [saab-2026]
   - "It remains unclear whether LLMs possess the nuanced understanding and intricate knowledge base required to effectively replicate the decision-making process of experts in highly specialized medical fields." [osullivan-2026]
   - "Whether ChatGPT Health inherits these vulnerabilities or has mitigated them remains untested." [levine-2026]
   - "Neither vital signs nor danger signs reliably stratify risk." [nijman-2026]

3. **"Here we..." / "In this study, we..." contribution paragraph.** The contribution is introduced with a pivot phrase naming the study design (not just the system). Variants:
   - "Here we conducted a pragmatic, cluster-randomized trial in 16 primary care facilities in Kenya." [brinton-2026 abstract, echoed in intro]
   - "To address this, we introduce multimodal AMIE -- advancing the conversational diagnostic capabilities of the original system..." [saab-2026]
   - "In this study, we conducted a cluster-randomized trial to explore whether a generative artificial intelligence (AI)-powered...clinical decision support system...can improve the quality of care..." [brinton-2026]
   - "To understand whether LLMs can reliably support the general public and bring care closer to patients, we conducted a study with 1,298 UK participants." [bean-2026]
   - "This study probes the potential of LLMs to democratize subspecialist-level expertise by focusing on an indicative example..." [osullivan-2026]
   - "In this study, we aim to introduce Reti-Pioneer, a multitask framework, and conduct a biology-linked, stepwise, multi-site clinical validation study..." [zhou-2026]
   - "We conducted an independent, structured stress test of ChatGPT Health using clinician-authored vignettes..." [levine-2026]

4. **Figure 1 reference in contribution paragraph (for AI system papers).** When the paper presents a system, Fig. 1 shows the study design or system overview:
   - "Figure 1 provides an overview of our system's key components, our evaluation methodology and key findings." [saab-2026]
   - "Figure 1 shows the CONSORT diagram of participant and cluster progression throughout the trial." [brinton-2026]
   - No Fig. 1 reference in contribution paragraph for pure clinical trials where Fig. 1 is the CONSORT diagram.

5. **Dense clustered references.** References are superscript numbers, often in ranges (e.g., "refs 1-5", "refs 16-19"). No author names appear inline for Nature Medicine (all numeric). Reference density is highest in background paragraphs, drops in the contribution paragraph.

6. **No separate Related Work section.** All prior work positioning is embedded in the Introduction body. Some papers defer extended literature review to Supplementary Information.

## Exemplar sentences (shape, not content)

**Opening hooks**:
- "Primary care facilities manage a wide range of acute and chronic conditions and serve as the foundation for continuity of care, coordination across health system levels and equitable service delivery." [brinton-2026]
- "Lung cancer accounts for the highest proportion of cancer-related deaths in the United Kingdom (UK) and worldwide..." [varoquaux-2026]
- "Infectious diseases account for the majority of the 2.5 million deaths that occur each year among children aged 1-59 months." [nijman-2026]
- "The scarcity of subspecialist medical expertise poses a considerable challenge for healthcare delivery." [osullivan-2026]

**Gap sentences**:
- "However, prospective interventional evidence from real-world clinical studies, particularly in LMICs, remains limited." [brinton-2026]
- "It remains unclear whether LLMs possess the nuanced understanding and intricate knowledge base required to effectively replicate the decision-making process of experts in highly specialized medical fields." [osullivan-2026]
- "Key gaps persist, including the underrepresentation of multi-ethnic populations and the lack of sufficient validation for multidisease risk stratification." [zhou-2026]

**Contribution sentences**:
- "In this study, we conducted a cluster-randomized trial to explore whether a generative artificial intelligence (AI)-powered...clinical decision support system...can improve the quality of care..." [brinton-2026]
- "To address this, we introduce multimodal AMIE -- advancing the conversational diagnostic capabilities of the original system by integrating multimodal medical perception." [saab-2026]

## Anti-patterns

- Do NOT open with the technology ("We propose X to solve Y"). Open with the clinical problem or patient burden.
- Do NOT write a separate "Related Work" or "Background" subsection. Nature Medicine weaves all positioning into the Introduction body.
- Do NOT enumerate contributions as a bulleted list ("First...Second...Third"). State the study design and contribution in prose.
- Do NOT use author-year citation format. Nature Medicine uses superscript numbered references.
- Do NOT devote more than 2-3 sentences per prior work category. Brief characterization + limitation is the norm.
- Do NOT include results or data in the Introduction. The contribution paragraph states what the study does, not what it finds.
- Do NOT frame the contribution as a technical advance. Frame it as clinical evidence generation or clinical utility demonstration.

## Paragraph structure

Typical 4-5 paragraph structure:

| Para | Job | Example move |
|------|-----|-------------|
| P1 | Clinical problem / patient burden | Why this clinical problem matters to patients and healthcare systems |
| P2 | Current clinical practice + limitations | Standard of care, existing approaches, their shortcomings |
| P3 | Technology promise + evidence gap | AI/LLM potential, but lack of prospective/real-world evidence |
| P(n-1) | Contribution statement ("Here we...") | Name the study type, system, evaluation design, scale |
| P(n) | (Optional) Study scope | Datasets, sites, comparators, what was evaluated |

Some papers (saab-2026, bean-2026) expand to 6-7 paragraphs when the clinical background requires multiple approach categories.

## Contrast with NMI

- NMI introductions are 550-1,600 words (can be longer). Nature Medicine introductions are 350-1,200 words (shorter on average, more focused).
- NMI opens with domain importance (broad scientific field). Nature Medicine opens with specific clinical problem (patient-facing).
- NMI frames the contribution as a technical capability ("We introduce Diamond, an error-controlled interaction discovery method"). Nature Medicine frames it as a clinical study ("We conducted a cluster-randomized trial").
- NMI uses the contribution paragraph to name the system and reference Fig. 1 (architecture). Nature Medicine may reference Fig. 1 (study design/CONSORT) or omit figure references in the introduction.
- Both venues weave related work into the Introduction (no separate section).
- Both use superscript numbered references, but Nature Medicine tends to have fewer (15-40) because the introduction is shorter and more clinically focused.
- NMI backgrounds focus on technical approach categories (discriminative vs generative models). Nature Medicine backgrounds focus on clinical practice categories (current screening guidelines, standard of care, prior clinical trials).
