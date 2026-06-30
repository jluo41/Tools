# NMI Methods -- Section Style Guide

Extracted from 8 Nature Machine Intelligence exemplar papers. Supplements `style-profile.md`.

## Word budget

- 1,200-3,000 words, spanning 2.5-4 pages.
- mataraso-2025: ~1,200w (14 subsections). serapio-garcia-2025: ~2,500w (12 subsections). qiao-2025: ~2,500w (8 subsections). gu-2026: ~2,500w (8 subsections). pontikos-2025: ~2,000w (11 subsections). doerig-2025: ~2,500w (16 subsections). chen-w-2025: ~2,000w (7 subsections). mon-williams-2025: ~1,500w (7 subsections).
- Methods is the second-longest section after Results, but shorter than Results.

## Placement

Methods is placed AFTER Discussion (and Conclusion if separate), at the very end of the main text. This is mandatory Nature-family ordering:

```
... -> Discussion [-> Conclusion] -> Methods -> Data availability -> Code availability -> References
```

All 8 exemplars confirm this placement. Methods is never between Introduction and Results.

## Arc

```
Model/system architecture (what it is)
  -> Training / optimization details (how it was trained)
  -> Loss functions / objectives (what was optimized)
  -> Dataset descriptions (what data was used)
  -> Evaluation methodology (how performance was measured)
  -> Baselines / comparisons (what it was compared against)
  -> Reporting summary (Nature checklist reference)
  -> Data availability
  -> Code availability
```

The Methods section reads as a recipe: architecture first, then training protocol, then evaluation protocol, then data provenance. Data and Code availability always appear as the final subsections.

## Signature moves

1. **Granular subsection hierarchy.** Methods is divided into 7-16 subsections, each covering one methodological component. Sub-subsections are common, using bold-inline headings:
   - "Embedding process" -> "Onset of labour." / "Cancer mortality." [mataraso-2025]
   - "Downstream evaluation" -> "Classification or univariate regression." / "Dense sequence to sequence regression." [gu-2026]
   - "Administering psychometric tests to LLMs." / "Reliability." / "Convergent and discriminant validity." [serapio-garcia-2025]
   - "Model training" / "Evaluation" / "Conformal prediction" / "Human benchmarking" [pontikos-2025]

2. **Equations appear here, not in Results.** Formal numbered equations are placed in Methods. The number of equations varies by paper type:
   - 0 equations: serapio-garcia-2025, mon-williams-2025, doerig-2025 (empirical/applied papers)
   - 3 equations: gu-2026, mataraso-2025
   - 6 equations: chen-w-2025
   - 10 equations: qiao-2025 (methods-heavy generative model paper)
   - Equations are presented as centered display equations, introduced with prose setup, followed by variable definitions. Some papers number equations (Eq. 1, 2, ...), others do not.

3. **Exhaustive hyperparameter specification.** Training details are precise enough for exact replication:
   - "learning rate was set to 0.0001; batch size was set to 16; Dropout probability was fixed at 50%; Training was completed within 8 h for each neural network training on a single 3090 24 GB GPU." [pontikos-2025]
   - "AdamW, weight decay 5x10^-2, betas {0.9, 0.95}, cosine warmup 5% of training" [gu-2026]
   - "Adam optimizer with a fixed learning rate of 10^-4 for 300 epochs" [qiao-2025]
   - "a pyramid-shaped MLP model with the exponential linear unit activation and four hidden layers, each having neuron sizes of 2p, p, p/2, and p/4" [chen-w-2025]

4. **Dataset provenance with split rationale.** Dataset descriptions include: source, size, preprocessing pipeline, train/val/test split ratios, and the splitting strategy (patient-wise, subject-wise, stratified):
   - "80/20 train/test, family-aware" [pontikos-2025]
   - "15,000 train (Cheadle), 2,000 validation, 4,000 test (three sites)" [qiao-2025]
   - "80% training, 10% validation, 10% testing" [gu-2026]
   - "subject-wise splitting to prevent data leakage" [gu-2026]

5. **Software version pinning.** Exact software versions are listed:
   - "Python 3.10.6, NumPy 1.23.3, Pandas 1.5.0, SciPy 1.9.1, scikit-learn 1.1.2, PyTorch 1.12.1, Gensim 4.3.0" [mataraso-2025]
   - GPU model and memory: "NVIDIA RTX A6000 (48 GB)" [qiao-2025]; "NVIDIA RTX 2080 utilizes ~225 W" [mon-williams-2025]

6. **Data and Code availability as mandatory closing subsections.** Every NMI paper ends Methods with these two labeled subsections:
   - Data availability: URL or access instructions (often tiered: public subset + restricted full data)
   - Code availability: GitHub URL + Zenodo DOI for archival
   - "The source code for model architecture training and inference is available at https://github.com/Eye2Gene/Classification. The code can also be run online via the CodeOcean capsule." [pontikos-2025]
   - "Code available via GitHub at https://github.com/guxiao0822/Cardiac-Sensing-FM" [gu-2026]
   - "added to a public data storage bucket for wider public use" [serapio-garcia-2025]

7. **Reporting summary reference.** A brief "Reporting summary" subsection points to the Nature Portfolio Reporting Summary checklist (a standardized 3-4 page form appended to the paper covering statistics, data, ethics, life sciences study design).

8. **Heavy use of supplement for extended details.** When Methods would become too long, detail is deferred:
   - "described in detail in Supplementary Note A.7.2" [serapio-garcia-2025]
   - "Supplementary Note A.3.4 discusses the prompt design motivation" [serapio-garcia-2025]
   - Main Methods gives the conceptual framework + key decisions; supplement has item-level procedural details.

## Exemplar sentences (shape, not content)

**Architecture description**:
- "CoAtNet0 architecture from the keras-cv-attention-models pypi library was used, where the final output layer was replaced by a dropout layer, followed by a linear layer with 63 outputs and softmax normalization." [pontikos-2025]
- "The model consists of three GCN layers and one FC layer, with four attention heads, a feed-forward size of 1,024, and a dropout rate of 0.1." [qiao-2025]

**Loss function prose**:
- "cross entropy loss...using additional class-weighting inversely proportional to gene frequency" [pontikos-2025]
- "the modelled data, y, consist of the captions embeddings (n images x 768 MPNet_dimensions) and the predictors, X, consists of brain activity measurements (n images x p voxels)" [doerig-2025]

**Ethics subsection** (present in some papers):
- "Ethics" as a standalone subsection within Methods [pontikos-2025]
- Ethical considerations discussed within Discussion [serapio-garcia-2025]

## Anti-patterns

- Do NOT place Methods before Results. Nature-family ordering puts Methods at the end.
- Do NOT combine Methods with Results in a single section. They are always separate.
- Do NOT omit hyperparameters. NMI expects exact reproducibility details (learning rate, batch size, optimizer, GPU, epochs).
- Do NOT omit Data/Code availability subsections. These are mandatory.
- Do NOT put all dataset descriptions in a single prose paragraph. Each dataset or cohort gets its own sub-subsection with provenance, size, and split details.
- Do NOT put primary equations in Results. Equations belong in Methods (or supplement).
- Do NOT write Methods in passive voice exclusively. NMI Methods uses a mix: "We used Adam optimizer..." and "The model was trained for 300 epochs..."

## Paragraph structure

Methods subsections are typically 1-3 paragraphs each, 100-300 words per paragraph. Each subsection covers one methodological component completely. The internal structure:

1. **What** (1 sentence): name the component
2. **How** (2-5 sentences): describe the implementation with hyperparameters
3. **Why** (0-1 sentences): optional rationale for design choices (often deferred to supplement)

## Contrast with IS journals

- IS Methods sections appear between Introduction/Theory and Results. NMI Methods appear after Discussion.
- IS Methods focus on research design, variable operationalization, and econometric specification. NMI Methods focus on architecture, training protocol, and dataset provenance.
- IS journals rarely include equations in Methods (equations appear in Theory). NMI puts equations in Methods.
- IS journals do not have Data/Code availability subsections. NMI requires them.
- IS Methods describe the sample and measurement instruments. NMI Methods describe the neural network architecture and training recipe.
- IS Methods do not include a Reporting Summary. NMI includes a standardized Nature checklist.
