# npj Digital Medicine Discussion -- Section Style Guide

Extracted from 9 npj Digital Medicine exemplar papers. Supplements `style-profile.md`.

## Word budget

- 800-2500 words. Median ~1500 words.
- wang-2026 (brief comm): ~1500w. momenzadeh-2026: ~2500w. lai-2026: ~2000w. he-2026: ~2000w. johnson-2026: ~1200w. xian-2026: ~800w (shorter, as results are extensive). iqbal-2026: ~1500w. yuan-2026: ~2000w. zhuang-2026: ~1500w.
- No subsection headings in most papers. Organized as flowing paragraphs.

## Arc

```
P1: Restate what was done + headline finding (clinical framing)
P2-P3: Interpret findings in clinical context (what this means for practice)
P3-P4: Compare to prior work (situate against existing evidence)
P5-P6: Clinical translation pathway (deployment, implementation)
P7-P8: Limitations (specific, numbered or paragraph-by-paragraph)
P9: Future directions
P-final: Concluding summary (1 paragraph, translational close)
```

The arc is **interpretation-forward, limitation-honest**: the Discussion opens by restating the clinical contribution, moves through interpretation and comparison, devotes substantial space to limitations, and closes on clinical deployment potential.

## Signature moves

1. **Clinical-contribution restatement.** The opening paragraph restates the core finding in clinical (not technical) terms:
   - "This work addresses longstanding challenges in inpatient glycemic management, where care remains largely reactive; current practices typically adjust treatment only after a hypoglycemic episode occurs...Our model shifts this paradigm by enabling real-time, proactive prediction using EHR data..." [momenzadeh-2026]
   - "In this retrospective-prospective study, we developed and validated TriageMaster-70B, an LLM-based system for chest pain triage in EDs." [wang-2026]
   - "This systematic evidence map suggests that clinical evaluations of LLM interventions remain in their early stages." [he-2026]
   - "This evidence gap map provides a structured overview of how DHIs have been evaluated for enhancing patient engagement across clinical contexts." [iqbal-2026]

2. **Clinical workflow integration discussion.** The Discussion addresses how the tool would fit into real clinical practice:
   - "EHR-integrated hypoglycemia risk tools have the potential to influence clinician behavior, such as increased modification of insulin doses. Rather than presenting interruptive alerts to all ordering clinicians, we envision integration of this model into a diabetes stewardship workflow, such as a prioritized list reviewed by a pharmacist." [momenzadeh-2026]
   - "The system integrates into hospital information systems and operates at FMC on patient narratives with vital signs in real time under clinician oversight." [wang-2026]
   - "By aligning the choice of graph and processing tool with the requirements of each emergency decision task, the AI agent delivers targeted decision support." [lai-2026]

3. **Head-to-head comparison with prior work (using specific numbers).** The Discussion compares results to published benchmarks with concrete metrics:
   - "In contrast, the LSTM in this study achieved precision 0.23 and recall 0.44 (F1 = 0.30), more than doubling precision while maintaining clinically meaningful sensitivity, corresponding to approximately 3.4 false positives per true alert." [momenzadeh-2026]
   - "Compared with the graph-free LLM baselines, GPT and DeepSeek yielded substantially lower accuracy and F1-scores, indicating that general-purpose language models struggle to capture structured triage patterns without the support of graph-derived clinical context." [lai-2026]

4. **Extensive, specific limitations.** Limitations are detailed and clinically relevant, often occupying 1-3 full paragraphs:
   - "Our study has several limitations. First, despite outperforming prior inpatient EHR-based models and non-sequential baselines, performance remains modest...Second, development and prospective evaluation cohorts were drawn from a single health system in Los Angeles...Third, prospective evaluation spanned only 2.5 weeks...Fourth, the model uses intermittent POC BG and may miss transient hypoglycemia...Fifth, time-series missingness was encoded as zero to mirror EHR information availability, but this conflates 'not measured' with 'not occurring'." [momenzadeh-2026]
   - "This study has several limitations that should be acknowledged. First, the prospective validation was conducted in a single country with all sites in China, and the modest sample size in the prospective validation cohort may restrict our model generalizability...Second, the model was trained and evaluated using only patient narratives and vital signs...Third, although comparator models such as ChatGPT were evaluated using de-identified data transmitted via official APIs, clinical deployment of cloud-based LLMs raises data sovereignty concerns..." [wang-2026]

5. **Future work with concrete next steps.** Future directions are specific and actionable:
   - "Several directions follow from these limitations. The most important next step is a prospective, ideally randomized, interventional study embedding the model in a diabetes stewardship workflow and measuring clinically meaningful endpoints..." [momenzadeh-2026]
   - "Our ongoing multicenter randomized controlled trial and planned international collaborations will help expand this external validation..." [wang-2026]
   - "We specifically recommend that trials: (a) pre-specify sample sizes adequate to detect clinically meaningful differences in patient-centred outcomes; (b) include diverse patient populations...; and (c) incorporate pre-planned analyses of performance errors..." [he-2026]

6. **Concluding paragraph with translational close.** The final paragraph is brief and clinically grounded:
   - "We developed and validated a real-time, deployable LSTM model that predicts inpatient hypoglycemia within a 24-hour horizon...Together, these results provide a practical foundation for EHR-integrated decision support, ideally embedded within stewardship workflows, to enable proactive interventions, reduce preventable hypoglycemia, and improve inpatient glycemic safety." [momenzadeh-2026]
   - "In summary, TriageMaster-70B demonstrates superior diagnostic accuracy for early ACS triage at FMC in EDs, outperforming both cardiologists and LLMs in multicenter cohorts." [wang-2026]
   - "In conclusion, the current evidence base for LLM interventions in clinical practice remains uneven." [he-2026]

## Exemplar sentences (shape, not content)

**Clinical interpretation**:
- "This equates to 16 alerts/day, with 3.4 false positives per true alert, and the opportunity to prevent 3.6 hypoglycemia events per day (44% of expected daily cases)." [momenzadeh-2026]
- "The broader clinical and financial implications of this are substantial; scaled nationally to ~900,000 hospital beds in the U.S., this would equate to prevention of nearly 4,000 inpatient hypoglycemia events daily." [momenzadeh-2026]

**Limitation sentence**:
- "The single center, single region setting constitutes a major limitation of the present work. Differences in data collection standards, coding systems (e.g., variations in ICD versions), clinical pathways, and medical culture across healthcare systems may affect the generalizability of our framework..." [lai-2026]

**Future direction**:
- "Future work could further leverage the analytical capabilities of LLMs by incorporating traceable subgraph information and key contributing nodes..." [lai-2026]

## Anti-patterns

- Do NOT restate the Results in detail. The opening paragraph should summarize the clinical contribution, not re-report numbers.
- Do NOT skip limitations or treat them superficially. npjDM reviewers expect extensive, specific limitations addressing generalizability, data quality, study design weaknesses, and deployment constraints.
- Do NOT frame limitations as only future work. Acknowledge genuine weaknesses before pivoting to what could be done next.
- Do NOT end the Discussion on a limitation or a vague statement. End on a concrete translational statement or clinical vision.
- Do NOT discuss only the technical aspects. The Discussion must address clinical workflow integration, deployment barriers, and patient impact.
- Do NOT use subsection headings in the Discussion (unlike Results). Organize as flowing paragraphs.

## Paragraph structure

6-10 paragraphs, no subsection headings. The flow:

1. **Restatement** (P1): What this study did and its headline clinical contribution. 1 paragraph.
2. **Clinical interpretation** (P2-P3): What the findings mean for patient care, clinical workflows, or policy. How the tool/finding would be used in practice. 1-2 paragraphs.
3. **Comparison to prior work** (P3-P5): How results compare to existing benchmarks, prior models, or clinical standards. With specific numbers. 1-2 paragraphs.
4. **Broader significance** (P5-P6): How this advance connects to larger trends in digital health, AI in medicine, or clinical practice transformation. 1 paragraph.
5. **Limitations** (P6-P8): Specific, numbered limitations addressing generalizability, data limitations, study design, and deployment constraints. 1-3 paragraphs.
6. **Future directions** (P8-P9): Concrete next steps, often tied to overcoming stated limitations. 1 paragraph.
7. **Concluding summary** (final P): Brief translational close. 1 short paragraph.

## Contrast with NMI

- NMI Discussion focuses on scientific contribution and methodological advance. npjDM Discussion focuses on clinical translation and workflow integration.
- NMI limitations are typically 1 paragraph. npjDM limitations are 1-3 paragraphs with more clinical specificity (generalizability across health systems, demographic subgroups, deployment constraints).
- NMI concluding paragraph emphasizes scientific impact. npjDM concluding paragraph emphasizes patient care impact.
- Both journals place Discussion BEFORE Methods (Nature house style).
