# npj Digital Medicine Abstract -- Section Style Guide

Extracted from 9 npj Digital Medicine exemplar papers. Supplements `style-profile.md`.

## Word budget

- 100-250 words. Median ~150 words. Range is wide: brief communications run ~80-100w, full articles ~150-250w.
- wang-2026 (brief comm): ~80w. momenzadeh-2026: ~250w. he-2026: ~150w. lai-2026: ~150w. johnson-2026: ~120w. xian-2026: ~180w. iqbal-2026: ~150w. yuan-2026: ~150w. zhuang-2026: ~220w.
- Unstructured single paragraph. No labeled sub-fields (no "Background / Methods / Results / Conclusions" headers). Never bulleted or numbered.

## Arc

```
clinical problem + stakes (why this matters for patients/clinicians)
  -> gap in current practice or evidence (what is missing or failing)
  -> "Here/In this study, we..." contribution pivot (name the tool/method/study)
  -> what was done (data scale, approach, validation design)
  -> key results (headline performance numbers with CIs or effect sizes)
  -> clinical translation close (what this means for practice)
```

The arc is **clinical-problem-forward, translation-oriented**. The abstract opens with a patient care problem, not a technical gap. Results include concrete numbers (AUC, sensitivity, sample sizes). The close pivots to clinical deployment or practice impact, not theoretical contribution.

## Signature moves

1. **Clinical stakes opening.** The first sentence grounds the work in a real clinical problem, not a technical domain:
   - "Acute coronary syndrome triage at first medical contact begins with patient narratives, while definitive diagnosis often requires waiting for cardiac troponin or electrocardiogram results..." [wang-2026]
   - "Inpatient hypoglycemia is associated with increased morbidity, mortality, length of stay, and healthcare costs, yet current management remains reactive..." [momenzadeh-2026]
   - "Large language models (LLMs) are being deployed in clinical settings despite an underdeveloped evidence base regarding their real-world effectiveness." [he-2026]
   - "Digital health interventions (DHIs) are increasingly used to strengthen patient engagement." [iqbal-2026]

2. **Concrete data scale at pivot.** The contribution sentence specifies the data volume, giving the reader immediate credibility anchors:
   - "...a large language model using only patient narratives and vital signs. In 16,428 retrospective and 512 prospective cases..." [wang-2026]
   - "...a real-time long short-term memory (LSTM) model to predict hypoglycemia within 24 hours using electronic health record (EHR) data from 143,124 adult inpatient admissions across three hospitals..." [momenzadeh-2026]
   - "...we performed unsupervised clustering and characterized 100,272 patients in the Electronic Medical Records and GEnomics (eMERGE) Network." [xian-2026]

3. **Headline numbers with statistical detail.** Unlike NMI abstracts which stay directional, npjDM abstracts include specific performance metrics:
   - "...an F1 score of 0.30 (95% CI 0.296-0.305), precision of 0.23, recall of 0.44, and AUPRC of 0.23 at a decision threshold of 0.7..." [momenzadeh-2026]
   - "...it showed high sensitivity, with per-case processing 39% faster than independent retrospective cardiologist review." [wang-2026]
   - "...average improvements over state-of-the-art baselines of 23.13% in ED triage, 13.05% in drug-drug interaction detection, 1.58% in readmission prediction, and 5.47% in medication recommendation..." [lai-2026]

4. **Translation-oriented close.** The final sentence points to clinical deployment potential, not just scientific significance:
   - "...TriageMaster-70B may support rapid, accurate, and interpretable triage in emergency departments." [wang-2026]
   - "This real-time deployable LSTM model provides a clinically interpretable prediction of inpatient hypoglycemia and may support proactive glycemic stewardship workflows in hospitalized patients." [momenzadeh-2026]
   - "...necessitating standardized core outcome sets, mandatory use of specialized reporting guidelines, and robust clinical trials to ensure the safe integration of LLMs." [he-2026]

## Exemplar sentences (shape, not content)

**Opening move** (clinical problem first):
- "Inpatient hypoglycemia, defined as a blood glucose (BG) level below 70mg/dL, is the most common adverse event during diabetes treatment in hospitalized patients." [momenzadeh-2026]
- "Medical knowledge accumulation and clinical practice form a closed loop, yet enabling effective cooperation between the two elements...remains challenging, especially in the emergency department (ED)." [lai-2026]
- "Electronic health records (EHRs) contain extensive multidimensional patient data, presenting challenges for the discovery of novel and meaningful clinical patterns." [xian-2026]

**Gap sentence**:
- "...yet current management remains reactive due to the lack of real-time prediction tools." [momenzadeh-2026]
- "However, despite its rapid growth, DHIs remain unevenly evaluated and poorly standardized." [iqbal-2026]
- "...most evaluations benchmark model outputs against expert answers rather than real-world clinical endpoints, limiting their clinical relevance." [he-2026]

**Findings sentence** (concrete metrics):
- "The best-performing LSTM model achieved an F1 score of 0.30 (95% CI 0.296-0.305), precision of 0.23, recall of 0.44, and AUPRC of 0.23 at a decision threshold of 0.7, outperforming all baseline models." [momenzadeh-2026]
- "We identified 70 clusters defined by distinct comorbidity patterns." [xian-2026]

## Anti-patterns

- Do NOT use structured/labeled fields (Background, Methods, Results, Conclusions). npjDM uses one unstructured paragraph.
- Do NOT open with the method or system name. Open with the clinical problem.
- Do NOT omit concrete numbers. npjDM abstracts typically include sample sizes, performance metrics, or effect sizes. Vague directional claims alone are insufficient.
- Do NOT end on "implications are discussed." End on clinical translation or practice impact.
- Do NOT exceed ~250 words for full articles. Brief communications may be under 100 words.
- Do NOT use purely technical framing without connecting to patient care or clinical workflow.

## Paragraph structure

One paragraph only. No line breaks, no sub-sections, no bullet lists.

Sentence count: 4-10 sentences following this pattern:
1. Clinical problem / stakes (1-2 sentences)
2. Gap in current practice or evidence (1 sentence)
3. "Here/In this study/To address this, we..." contribution pivot + method/study name (1 sentence)
4. What was done: data scale, design (1-2 sentences)
5. Key results with headline numbers (1-3 sentences)
6. Clinical translation / practice implication (1 sentence)

## Contrast with NMI

- NMI opens with the scientific domain. npjDM opens with the clinical problem and patient impact.
- NMI may include only directional claims ("outperforms"). npjDM includes specific numbers (AUC, sensitivity, 95% CI, sample sizes).
- NMI closes on broad scientific significance. npjDM closes on clinical deployment or practice change.
- NMI always names a branded system (COMET, Eye2Gene). npjDM sometimes names a system but also accommodates observational studies and reviews without a named tool.
- NMI abstracts run longer (160-270w). npjDM abstracts are more variable (80-250w), with brief communications being very short.
