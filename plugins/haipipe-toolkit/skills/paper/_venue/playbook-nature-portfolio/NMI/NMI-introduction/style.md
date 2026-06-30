# NMI Introduction -- Section Style Guide

Extracted from 8 Nature Machine Intelligence exemplar papers. Supplements `style-profile.md`.

## Word budget

- 550-1,600 words. Typical range: 650-1,100 words.
- mataraso-2025: ~550w (4 paras). doerig-2025: ~650w (4 paras). pontikos-2025: ~900w (5 paras). qiao-2025: ~900w (4 paras). chen-w-2025: ~900w (5 paras). gu-2026: ~950w (5 paras). mon-williams-2025: ~1,100w (6 paras). serapio-garcia-2025: ~1,600w (8 paras).
- Paragraph count: 4-8 paragraphs. Modal count is 4-5.

## Arc

```
P1: Domain importance / broad stakes (why this matters to the world)
P2-P(n-2): Background + gap identification (existing approaches, their limitations)
P(n-1) or P(n): "Here we..." contribution statement (name the system, state what it does)
P(n): Experiment preview + claims (optional, some papers fold this into the contribution paragraph)
```

The arc is a **funnel**: broad domain importance narrows through existing approaches and their limitations, then opens to the contribution. The contribution paragraph is always the last or second-to-last paragraph. There is NO separate "Related Work" section -- all prior-work positioning is embedded in the introduction body.

## Signature moves

1. **Opening hook via domain importance.** The first sentence establishes why the domain matters, not what the method does. Two hook styles observed:
   - **Clinical/scientific significance**: "The heart is one of the most important and vital organs within the human body." [qiao-2025]; "Cardiovascular diseases are among the leading causes of morbidity and mortality worldwide..." [gu-2026]; "Inherited retinal diseases (IRDs) are a group of rare monogenic conditions affecting 1 in 3,000 people..." [pontikos-2025]
   - **Provocative rhetorical question**: "If Deep Blue (the first computer to win a chess match against a reigning world champion) was truly intelligent, then should it not be able to move its own pieces when playing chess?" [mon-williams-2025]
   - **Field transformation claim**: "Large language models (LLMs) have revolutionized everyday search, writing and chatbot systems..." [serapio-garcia-2025]; "Machine learning (ML) has emerged as a critical tool in many application domains..." [chen-w-2025]

2. **Background-as-gap-identification.** Middle paragraphs survey existing approaches not as a literature review but as a progressive narrowing toward the gap. Each approach is characterized in 1-2 clauses, immediately followed by its limitation. The pattern is "X methods exist [refs], but they fail at Y." References are clustered (2-4 per claim).
   - "Machine learning techniques have received increasing attention...but their application to personalized normative modelling of the heart from population data remains underexplored." [qiao-2025]
   - "So far, no work has addressed how to systematically measure and psychometrically validate LLM personality." [serapio-garcia-2025]
   - "Late fusion approaches struggle to learn cross-modal interactions." [mataraso-2025]
   - "Existing foundation models are predominantly based on ECG data and are largely confined to standard 12-lead configurations." [gu-2026]

3. **"Here we..." contribution paragraph.** The contribution statement appears in the last or second-to-last paragraph, introduced by a pivot phrase:
   - "Here, we provide an endeavour to create a personalized normative model..." [qiao-2025]
   - "Our work answers the open question: Do LLMs mimic human personality traits..." [serapio-garcia-2025]
   - "We introduce clinical and omics multimodal analysis enhanced with transfer learning (COMET)..." [mataraso-2025]
   - "We have leveraged this resource to develop a deep learning model, Eye2Gene..." [pontikos-2025]
   - "To address these challenges, we develop a foundation model, the cardiac sensing foundation model (CSFM; Fig. 1)..." [gu-2026]
   - "In this Article, we explore the hypothesis that..." [doerig-2025]
   - "In this study, we introduce an error-controlled interaction discovery method...named Diamond." [chen-w-2025]
   - "Embodied LLM-enabled robot (ELLMER) is a framework that integrates approaches..." [mon-williams-2025]

4. **System name + figure reference in contribution paragraph.** The method/system name is introduced with its acronym expansion, often accompanied by "(Fig. 1)" pointing to the architecture/overview figure:
   - "...the cardiac sensing foundation model (CSFM; Fig. 1)..." [gu-2026]
   - "The overall system diagram is presented in Fig. 1." [mon-williams-2025]
   - "We contribute a methodology for administering an established psychometric personality test to LLMs (Fig. 1)." [serapio-garcia-2025]

5. **Dense clustered references.** References are superscript numbers, often in ranges (e.g., "refs 1-5", "refs 16-23"). No author names appear inline (all numeric). Typically 15-40 references appear across the introduction. Reference density is highest in background paragraphs, drops to near-zero in the contribution paragraph.

6. **Extended lit review deferred to supplement.** When the related work is extensive, a note defers to the supplement: "we further detail related work in Supplementary Note A.2" [serapio-garcia-2025]; "Supplementary Section 1 provides more background on state-of-the-art approaches" [mon-williams-2025].

## Exemplar sentences (shape, not content)

**Opening hooks**:
- "The visual system provides the brain with a wealth of information about the physical environment." [doerig-2025]
- "Rapid advancements in omics technologies have revolutionized biological understanding." [mataraso-2025]
- "Machine learning (ML) models are powerful tools for detecting complex patterns, yet their 'black-box' nature limits their interpretability, hindering their use in critical domains like healthcare and finance." [chen-w-2025]

**Gap sentences**:
- "...a quantitative approach for studying how the brain extracts and represents complex scene information has remained elusive." [doerig-2025]
- "...their application to personalized normative modelling of the heart from population data remains underexplored." [qiao-2025]
- "...timely identification of the underlying genetic cause through targeted genetic testing remains challenging." [pontikos-2025]

**Contribution sentences**:
- "We train the proposed generative model, MeshHeart (Fig. 1a), on a large-scale population-level imaging dataset with 38,309 participants from the UK Biobank." [qiao-2025]
- "We have applied Diamond to various simulated and real datasets to demonstrate its empirical utility." [chen-w-2025]

## Anti-patterns

- Do NOT open with the method ("We propose X to solve Y"). Open with domain importance.
- Do NOT write a separate "Related Work" subsection in the introduction. NMI weaves all positioning into the introduction body.
- Do NOT enumerate contributions as a bulleted list in the introduction. State contributions in prose within the contribution paragraph. (Enumerated contributions may appear in the Discussion, not the Introduction.)
- Do NOT use author-year citation format. NMI uses superscript numbered references.
- Do NOT devote more than one paragraph per approach category. Brief characterization + limitation in 2-3 sentences per approach is the norm.
- Do NOT include results or data analysis in the introduction. The contribution paragraph states what the paper does, not what it finds.

## Paragraph structure

Typical 4-5 paragraph structure:

| Para | Job | Example move |
|------|-----|-------------|
| P1 | Domain importance / broad stakes | Why this problem matters to the world |
| P2 | Existing approaches + limitations | Survey of prior work, organized by approach type, each ending with its gap |
| P3 | (Optional) Deeper background or additional approach category | May cover a second line of work or technical prerequisite |
| P(n-1) | Contribution statement ("Here we...") | Name the system, state what it does, reference Fig. 1 |
| P(n) | (Optional) Experiment preview | What datasets, what was demonstrated, scope of evaluation |

Some papers (serapio-garcia, mon-williams) expand to 6-8 paragraphs when the background requires multiple approach categories or the gap needs careful staging.

## Contrast with IS journals

- MISQ/ISR introductions are 2,000-4,000 words. NMI introductions are 550-1,600 words -- much shorter.
- IS journals open with the research question. NMI opens with domain importance.
- IS journals have separate "Related Work" or "Theoretical Background" sections. NMI weaves all positioning into the introduction.
- IS journals use author-year citation format. NMI uses superscript numbers.
- IS journals enumerate contributions explicitly (often with "First...Second...Third"). NMI states contributions in a single prose paragraph.
- IS journals frame contributions in terms of theoretical advancement. NMI frames contributions as technical capabilities and empirical demonstrations.
- IS journals rarely reference figures in the introduction. NMI commonly references Fig. 1 in the contribution paragraph.
