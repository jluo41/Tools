# NatComm Introduction -- Section Style Guide

Extracted from 8 Nature Communications exemplar papers (healthcare AI / clinical ML / LLM in medicine / prescribing). Supplements `style-profile.md`.

## Word budget

- 600-2,500 words. Typical range: 800-1,500 words.
- chen-2026: ~600w (4 paras). ho-2026: ~750w (4 paras). xu-2026: ~1,200w (5 paras). salvatore-2026: ~1,200w (6 paras). zhou-2026: ~1,500w (8 paras). li-2026: ~1,500w (5 paras). abdallah-2026: ~2,500w (8 paras).
- Paragraph count: 4-8 paragraphs. Modal count is 4-6.
- NatComm introductions are longer than NMI (which caps around 1,600w). The broader scope allows more extensive background.

## Arc

```
P1: Domain importance / broad stakes (why this matters to the world)
P2-P(n-2): Background + gap identification (existing approaches, their limitations)
P(n-1): Gap summary + what is needed
P(n): "In this study/work, we..." contribution statement + study overview
```

The arc is a **funnel**: broad domain importance narrows through existing approaches and their limitations, then opens to the contribution. The contribution paragraph is always the last or second-to-last paragraph. NatComm introductions may include more background depth than NMI because the journal's scope is broader (methods + applications + empirical studies).

## Signature moves

1. **Opening hook via domain importance.** The first sentence establishes why the domain matters, not what the method does. NatComm favors a clinical or societal framing:
   - "Full-process clinical diagnosis encompasses the entire diagnostic workflow connected with clinical decision making, beginning with a patient's vague chief complaint." [xu-2026]
   - "Large language models (LLMs) have shown great promise in clinical diagnostic tasks, achieving high accuracy in standardized medical examinations and, in some cases, matching or surpassing physicians' performance." [chen-2026]
   - "Type 2 diabetes mellitus (T2D) is a pervasive chronic condition that affects millions globally, with devastating complications when poorly managed." [salvatore-2026]
   - "Dementia is a clinical condition characterized by a gradual decline in cognitive function that affects memory, reasoning, communication, and the ability to perform daily tasks." [ho-2026]
   - "Electronic health record (EHR) data play a central role in contemporary clinical and translational research." [zhou-2026]
   - "The advancement of personalized medicine relies heavily on clinical trials, which rigorously evaluate the efficacy and safety of novel therapeutic strategies." [abdallah-2026]
   - "Large language models (LLMs) represent a significant advancement in foundation models." [li-2026]

2. **Background-as-gap-identification.** Middle paragraphs survey existing approaches as a progressive narrowing toward the gap. Each approach is characterized in 1-3 sentences, followed by its limitation:
   - "However, the role of LLMs in real-world diagnosis is limited to functioning merely as tools for physicians." [xu-2026]
   - "However, these studies predominantly evaluate LLMs in static question-answering settings, where complete and structured patient data are readily available." [chen-2026]
   - "Despite their growing utilization and the media's portrayal of expected and unexpected benefits of GLP-1 RAs, there exists a paucity of real-world data examining their downstream health effects." [salvatore-2026]
   - "Nevertheless, AI-driven diagnostic systems may not generalize equally across racial and ethnic groups." [ho-2026]
   - "However, they remain bounded by the coverage and completeness of existing ontologies and do not fully capture the real-world coding variation and usage patterns." [zhou-2026]
   - "However, most existing LLM-based trial matching systems...rely heavily on proprietary, API-driven models, creating barriers related to cost, accessibility, reproducibility." [abdallah-2026]
   - References are clustered (2-6 per claim). Superscript numbered citations.

3. **Contribution paragraph at the end.** The contribution statement appears in the last or second-to-last paragraph:
   - "To address this challenge, we propose a paradigm shift in the role of LLMs in clinical diagnosis." [xu-2026]
   - "To address this gap, we propose a novel framework that evaluates LLMs' diagnostic capabilities within a two-agent architecture." [chen-2026]
   - "Our study extends beyond the work of Xie and colleagues by examining an even broader range of clinical outcomes." [salvatore-2026]
   - "In this work, we explore diagnostic discrepancies in dementia classification by analyzing MRI-derived features from White American, African American, and Hispanic populations." [ho-2026]
   - "To address these limitations, we develop GAME (Graph Alignment for Multi-institutional EHR Data), a scalable framework..." [zhou-2026]
   - "To address these limitations, we introduce TrialMatchAI, a fully open-source, locally deployable general-purpose clinical trial recommendation system." [abdallah-2026]
   - "In this study, we systematically examine the memorization of LLMs in medicine, focusing on three core aspects." [li-2026]

4. **System name + Fig. 1 reference.** The method/system name is introduced in the contribution paragraph, often with Figure 1:
   - "The overall study design is illustrated in Figure 1." [chen-2026]
   - "The overall framework is illustrated in Fig. 1." [zhou-2026]
   - "see Figure 1" [abdallah-2026]
   - Not all papers reference Fig. 1 in the Introduction (xu-2026 and li-2026 defer to Results).

5. **Study scope statement.** NatComm introductions often end with a paragraph summarizing the evaluation scope (datasets, comparisons, analysis types):
   - "We evaluated seven LLMs...across two diagnostic settings: static question answering and dynamic clinical diagnostic procedures." [chen-2026]
   - "We evaluate DxDirector-7B in the full-process clinical diagnosis setting using both real-world scenarios and four authoritative publicly available datasets." [xu-2026]
   - "This approach (Figure S1) allows for evaluating relative and absolute associations between GLP-1 RA prescription and a wide array of health outcomes in a demographically diverse population." [salvatore-2026]

6. **Dense clustered references.** References are superscript numbers, often in ranges (e.g., "refs 1-5", "refs 32-37"). No author names appear inline except when positioning against a specific prior study (salvatore-2026: "Xie, Choi & Al-Aly (2025)"). Reference density is highest in background paragraphs, drops in the contribution paragraph.

7. **Explicit prior-work positioning in Introduction.** Unlike NMI which defers detailed comparison to Results/Discussion, NatComm introductions sometimes include direct comparison with a specific prior study:
   - "Our study extends beyond the work of Xie and colleagues by examining an even broader range of clinical outcomes (up to 974 phenotypes)." [salvatore-2026]
   - The paper being extended is named and its scope described in 1-2 sentences.

## Exemplar sentences (shape, not content)

**Opening hooks**:
- "The growing patient demand continues to outpace the diagnostic capacity of physicians, underscoring the urgent need for more efficient and scalable diagnostic solutions." [xu-2026]
- "In recent years, artificial intelligence (AI) has shown promising potential in improving the accuracy of dementia diagnoses." [ho-2026]
- "A promise of EHR-based research is the potential for multicenter studies, which can include broader patient populations, improve generalizability, and uncover heterogeneity in associations across subgroups." [zhou-2026]

**Gap sentences**:
- "there exists a paucity of real-world data examining their downstream health effects." [salvatore-2026]
- "few studies have systematically evaluated LLMs within the context of real-world diagnostic workflows." [chen-2026]
- "a key question remains: to what extent do LLMs memorize medical training data" [li-2026]

**Contribution sentences**:
- "Building on this design, we introduce DxDirector-7B, an LLM with advanced deep thinking capabilities." [xu-2026]
- "we target the more complex task of clinical diagnostic procedure and introduce ClinDiag-GPT, a specialized LLM fine-tuned on 7,616 real-world cases to emulate the physicians' diagnostic workflows." [chen-2026]

## Anti-patterns

- Do NOT open with the method ("We propose X to solve Y"). Open with domain importance.
- Do NOT write a separate "Related Work" subsection in the introduction. NatComm weaves all positioning into the introduction body (though some papers defer extended lit review to Supplementary Materials).
- Do NOT enumerate contributions as a bulleted list in the introduction. State contributions in prose.
- Do NOT use author-year citation format. NatComm uses superscript numbered references (though occasional inline author names for specific positioned studies are acceptable).
- Do NOT include results or data analysis in the introduction. The contribution paragraph states what the paper does, not what it finds.
- Do NOT write more than ~2,500 words. Most NatComm introductions are under 1,500.

## Paragraph structure

Typical 4-6 paragraph structure:

| Para | Job | Example move |
|------|-----|-------------|
| P1 | Domain importance / broad stakes | Why this problem matters clinically or scientifically |
| P2 | Existing approaches + limitations | Survey of prior work by approach type, each ending with gap |
| P3 | (Optional) Deeper background or second approach category | May cover additional technical prerequisites |
| P(n-1) | Gap summary + what is needed | Consolidates the gap; some papers merge this with P(n) |
| P(n) | Contribution statement + study scope | Name the system, state what it does, evaluation summary |

Some papers (zhou-2026, abdallah-2026, li-2026) expand to 7-8 paragraphs when the background requires multiple approach categories or the contribution description is more detailed.

## Contrast with NMI

- NMI introductions are 550-1,600 words. NatComm introductions can run to 2,500 words -- generally longer.
- NMI rarely names specific prior authors inline. NatComm occasionally positions directly against a named prior study ("Xie and colleagues", "TrialGPT").
- NMI nearly always references Fig. 1 in the contribution paragraph. NatComm sometimes defers the figure reference to the first Results subsection.
- NMI has a tighter funnel (4-5 paragraphs typical). NatComm allows broader background (6-8 paragraphs for complex topics).
- Both use superscript numbered references and cluster them densely in background paragraphs.

## Contrast with IS journals

- MISQ/ISR introductions are 2,000-4,000 words. NatComm introductions are 600-2,500 words.
- IS journals open with the research question. NatComm opens with domain importance.
- IS journals have separate "Related Work" or "Theoretical Background" sections. NatComm weaves all positioning into the introduction.
- IS journals use author-year citation format. NatComm uses superscript numbers.
- IS journals enumerate contributions explicitly (often with "First...Second...Third"). NatComm states contributions in a single prose paragraph.
- IS journals frame contributions in terms of theoretical advancement. NatComm frames contributions as technical capabilities, empirical findings, or clinical utility.
