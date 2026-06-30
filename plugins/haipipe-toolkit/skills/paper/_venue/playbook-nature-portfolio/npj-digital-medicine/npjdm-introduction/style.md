# npj Digital Medicine Introduction -- Section Style Guide

Extracted from 9 npj Digital Medicine exemplar papers. Supplements `style-profile.md`.

## Word budget

- 600-1500 words. Median ~900 words. Range varies by article type.
- wang-2026 (brief comm): ~600w (3 paragraphs). momenzadeh-2026: ~1500w (6 paragraphs). lai-2026: ~900w (4 paragraphs). he-2026: ~700w (4 paragraphs). johnson-2026: ~800w (5 paragraphs). xian-2026: ~900w (4 paragraphs). iqbal-2026: ~800w (5 paragraphs). yuan-2026: ~1200w (8 paragraphs). zhuang-2026: ~1000w (5 paragraphs).
- 3-8 paragraphs. No formal subsections or headings within the Introduction.

## Arc

```
P1: Clinical/health problem + magnitude + patient impact
P2: Current approaches + their limitations in practice
P3: (optional) Technical opportunity (what new capabilities enable)
P4: Gap statement: what has not been done / why current solutions fail
P5: "Here/In this study, we..." contribution paragraph (what we did, how, and what we found)
```

The arc is **clinical-need-forward**: it opens with a health problem that matters to patients and clinicians, narrows through existing approaches and their practical shortcomings, and arrives at the contribution. The introduction is a funnel from bedside problem to technical solution.

## Signature moves

1. **Clinical prevalence/burden opening.** The first sentence or paragraph establishes the health problem with concrete epidemiological data:
   - "Chest pain is a common presentation in the emergency department (ED), and 10-15% of these patients are ultimately diagnosed with acute coronary syndrome (ACS). The time-critical nature of ACS care is well recognized..." [wang-2026]
   - "Inpatient hypoglycemia, defined as a blood glucose (BG) level below 70mg/dL, is the most common adverse event during diabetes treatment in hospitalized patients. In the U.S., inpatient hypoglycemia affects individuals with and without diabetes, occurring in approximately 20% of patients receiving insulin..." [momenzadeh-2026]
   - "Patient engagement denotes a collaborative process in which patients, caregivers, and healthcare professionals co-produce improvements in care. Patient engagement is increasingly recognized as a core component of high-quality, patient-centered care." [iqbal-2026]

2. **Practice-gap framing (not just knowledge-gap).** The gap is framed as a clinical workflow problem, not purely a scientific unknown:
   - "...many state-of-the-art automated techniques depend on machine learning models trained on structured ECG and laboratory data, whereas in actual practice, triage typically begins with the patient's narrative and basic vital signs. This mismatch has encouraged the development of artificial intelligence systems..." [wang-2026]
   - "Current care is usually reactive, supporting the adjustment of treatment plans only after a hypoglycemic event has already occurred." [momenzadeh-2026]
   - "...data fragmentation and heterogeneity...can severely limit model generalizability...Second, real-world evidence sometimes contradicts randomized trials...Third, the rapid generation of clinical data often outpaces guideline updates..." [lai-2026]

3. **Prior work as stepping stones, not targets.** Prior work is cited to show progress and establish what new capabilities are now available, rather than to attack specific papers:
   - "Recent years have witnessed rapid development in medical LLMs across multiple languages and scales." [zhuang-2026]
   - "The recent emergence of large language models (LLMs) suggests that risk stratification and diagnosis of ACS may be performed directly from patients' narrative information..." [wang-2026]
   - "Data representation methods, a type of unsupervised learning approach, including matrix decomposition, Latent Dirichlet Allocation (LDA), and modern neural network approaches such as autoencoders, have been increasingly used..." [xian-2026]

4. **Explicit contribution enumeration.** The final paragraph often lists numbered contributions:
   - "Our contributions are threefold: (1) End-to-end EMR processing... (2) 301MedQA benchmark... (3) AI4Doc-LLM..." [zhuang-2026]
   - "This study advances the field in several ways. First, we emphasize interpretability... Second, we perform longitudinal external validation... Third, we assess model performance across demographic subgroups..." [momenzadeh-2026]

5. **"In this study, we..." pivot sentence.** The contribution paragraph opens with a clear pivot phrase:
   - "In this study we introduce TriageMaster-70B, a 70-billion-parameter LLM adapted for FMC triage." [wang-2026]
   - "To address these critical gaps, we developed the first LSTM-based model for predicting inpatient hypoglycemia within a 24-hour horizon..." [momenzadeh-2026]
   - "Here, we created a knowledge-graph-driven embedding store named ClinVec..." [johnson-2026]
   - "Here, we conducted a large-scale analysis of EHR data to explore the interplay among phenotypes, genetics, and demographic factors." [xian-2026]

## Exemplar sentences (shape, not content)

**Opening move** (epidemiological grounding):
- "Chest pain is a common presentation in the emergency department (ED), and 10-15% of these patients are ultimately diagnosed with acute coronary syndrome (ACS)." [wang-2026]
- "Inpatient hypoglycemia, defined as a blood glucose (BG) level below 70mg/dL, is the most common adverse event during diabetes treatment in hospitalized patients." [momenzadeh-2026]
- "Electronic health records (EHRs) have great potential for revolutionizing healthcare delivery and research by providing comprehensive data on patient demographics, clinical diagnoses, laboratory results, medications, and procedures." [xian-2026]

**Gap sentence** (practice-gap, not knowledge-gap):
- "Despite these advances, LLMs exhibit significant limitations when applied to complex clinical scenarios that require contextual understanding and practical expertise." [zhuang-2026]
- "However, 77% of published hypoglycemia prediction models have been developed using continuous glucose monitoring device data from outpatient populations with Type 1 diabetes mellitus." [momenzadeh-2026]
- "Yet adherence to these standards remains limited, undermining transparency and reproducibility." [he-2026]

**Contribution pivot**:
- "In this study we introduce TriageMaster-70B, a 70-billion-parameter LLM adapted for FMC triage. We evaluated its performance in multicenter retrospective and prospective cohorts of patients presenting to the ED with chest pain." [wang-2026]
- "We introduce AI4Doctor, a unified framework that unlocks the clinical value of electronic medical records (EMRs) through a sequence of methodical innovations." [zhuang-2026]

## Anti-patterns

- Do NOT open with a technical/methodological statement ("Deep learning has shown..."). Open with a clinical problem that affects patients.
- Do NOT frame the gap as purely a scientific curiosity. Frame it as a clinical need: patients are harmed, workflows are broken, resources are wasted.
- Do NOT attack prior work. Position prior work as valuable progress that has not yet addressed the specific clinical need.
- Do NOT omit concrete epidemiological data (prevalence, mortality, cost) from the opening paragraph.
- Do NOT use the introduction to review the full literature. Save detailed prior work for the Discussion or a Related Work paragraph.
- Do NOT end the introduction without stating the key finding or design of the study. The reader should know what was done and the headline result before turning to Results.

## Paragraph structure

3-8 paragraphs, typically 4-5. The structure follows a funnel:

1. **Clinical problem** (P1): Epidemiological burden, patient impact, clinical stakes. 1 paragraph.
2. **Current approaches and limitations** (P2-P3): What clinicians/systems currently do. Where they fall short in practice. 1-2 paragraphs.
3. **Technical opportunity** (P3-P4, optional): New capabilities that make an advance possible (e.g., LLMs, large EHR datasets, new sensors). 0-1 paragraph.
4. **Gap statement** (P3-P4): What has not been done. Why current solutions are insufficient for the stated clinical problem. 1 paragraph (may be merged with P2).
5. **Contribution** (final P): "In this study / Here, we..." followed by what was done, how it was validated, and the headline finding. Often includes enumerated contributions. 1 paragraph.

## Contrast with NMI

- NMI introductions may open with a scientific/technical domain ("Deep learning has transformed..."). npjDM opens with a clinical problem and patient-facing statistics.
- NMI introductions are shorter (400-700 words). npjDM introductions are longer (600-1500 words) with more extensive clinical context.
- NMI rarely includes epidemiological data in the introduction. npjDM regularly cites prevalence, incidence, mortality, or cost data.
- NMI introductions are more focused on the technical advance. npjDM introductions are focused on the clinical workflow gap that motivates the advance.
