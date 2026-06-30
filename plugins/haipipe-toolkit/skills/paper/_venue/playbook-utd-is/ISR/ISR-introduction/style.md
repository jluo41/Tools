# ISR Introduction Style Guide

Distilled from two ISR exemplars. Quote the SHAPE, not the content.

## Word budget

- Target: 1,800-2,500 words (4-6 pages double-spaced, or 2-3 pages single-column).
- Bao 2021: ~2,200 words across 4 pages (pp. 3-6). Zhang 2026: ~1,800 words across 2 column-pages.
- The ISR intro is LONGER than MISQ because it must preview the identification strategy and data, not just the theory.

## Arc (paragraph-level structure)

The ISR introduction follows a 7-paragraph arc:

```
P1: IS phenomenon + institutional stakes (the world this paper lives in)
P2: What is known + what creates the tension/tradeoff
P3: Gap statement ("To the best of our knowledge...")
P4: Context differentiation (why THIS setting is distinct)
P5: Research questions (explicit, often lettered)
P6: Data, method, and key findings preview
P7: Contribution statement + policy/managerial implication
```

Bao 2021 uses all 7 beats across ~8 paragraphs. Zhang 2026 compresses P4-P5 but hits the same beats.

## Signature moves

### Opening sentence: declarative, institutional, cited
- [Bao 2021] "The U.S. healthcare system is characterized by a fragmented delivery model with misaligned financial incentives that lead to excess expenditures, low patient satisfaction, poor care quality, and inefficient care delivery (Nattinger et al. 2018)."
- [Zhang 2026] "Large language models (LLMs) have been advancing rapidly since the introduction of the transformer architecture (Vaswani et al. 2017); however, they remain costly to train and deploy..."
- SHAPE: `[Domain X] is characterized by [problem/tension] that leads to [consequences] (cite).`
- Anti-pattern: opening with a question, a quote, or a sweeping claim without citation.

### Gap statement: "To the best of our knowledge..."
- [Bao 2021] "To the best of our knowledge, ours is one of the first studies to explore the tradeoffs involved in balancing competing organizational objectives in the context of value-based healthcare, and the impact of effective IT use on the strength of the association between ACO efficiency and quality."
- [Zhang 2026] "To the best of our knowledge, the present study is among the first in the information systems field to employ this framework."
- SHAPE: `To the best of our knowledge, [ours is one of the first / the present study is among the first] to [specific void filled].`
- The phrasing is hedged ("one of the first"), never "we are the first." ISR reviewers punish absolutism.

### Research questions: explicit, lettered
- [Bao 2021] "We focus on two research questions: (a) Is ACO efficiency positively associated with quality? and (b) Does effective use of health IT enable ACOs to mitigate quality-efficiency tradeoffs?"
- [Zhang 2026] Does not letter RQs explicitly but states the two-step question: "how online reviews reflect physicians' service quality, and how this, in turn, influences the demand for online consultations."
- SHAPE: `We focus on [N] research questions: (a) [X]? and (b) [Y]?`

### Data + method preview: one dense paragraph
- [Bao 2021] "In this study, we focus on the Medicare Shared Savings Program (MSSP)... Our study is based on a nationwide sample of ACO data from 2013 to 2018. We supplement this dataset with data reported by the CMS meaningful use (MU) program... We also utilize the American Hospital Association (AHA) IT supplement..."
- [Zhang 2026] "We assembled a data set from HaoDF.com... which includes millions of reviews on 936,975 physicians from 10,526 major hospitals across China."
- SHAPE: `In this study, we focus on [program/setting]. Our study is based on [data scope: nationwide/platform sample] from [source] covering [time period]. We supplement with [additional data sources].`
- Key: name every data source in the intro so the reader knows the empirical scope before entering the theory section.

### Findings preview: compressed, guarded
- [Bao 2021] "We observe that efficient ACOs do not exhibit any tradeoffs with respect to care quality. Further, we find that effective use of health IT across ACO providers has a positive effect on the association between ACO efficiency and quality."
- [Zhang 2026] "we show that higher service-quality scores are associated with greater consultation demand."
- SHAPE: `We [observe/find] that [main finding]. Further, we [observe/find] that [moderating/mechanism finding].`

### Contribution statement: labeled by type
- [Zhang 2026] "Our study makes several contributions. Methodologically, we develop an SLM (Doc-BERT) tailored to the healthcare context... Theoretically, we adapt and refine a quality evaluation framework... Empirically, we identify specific dimensions of service quality that most strongly predict online consultation demand..."
- [Bao 2021] "We contribute to the extant literature on the role of effective IT use in value-based healthcare delivery... Our context-specific conceptualization of health IT use highlights the role of IT-enabled information integration as the primary mechanism..."
- SHAPE (Zhang template, preferred): `Our research contributes in [N] ways. **Methodologically**, we [method contribution]. **Theoretically**, we [theory contribution]. **Empirically**, we [empirical contribution].`
- SHAPE (Bao template): `We contribute to the extant literature on [stream] by [specific addition]. Our [conceptualization/framework] highlights the role of [mechanism] as [the primary/a critical] mechanism in [resolving/enabling outcome].`
- The labeled 3-way (methodological/theoretical/empirical) is the cleaner ISR template.

## Exemplar shapes (paragraph arc)

```
[Bao intro arc]:
P1: U.S. healthcare fragmented + ACO as institutional response (cite)
P2: Literature documents quality-efficiency tradeoffs (cite, cite)
P3: GAP: "To the best of our knowledge, ours is one of the first..."
P4: ACO incentives differ from FFS and HVBP (context differentiation)
P5: Two research questions, lettered (a) and (b)
P6: Data (MSSP + MU + AHA), method (two-stage DEA + econometric), findings preview
P7: Contribution to IT value literature + policy implication

[Zhang intro arc]:
P1: LLMs advancing but expensive for specialized domains
P2: Online consultations as study instance; reviews reduce info asymmetry
P3: GAP: existing NLP lacks theory-supported framework + latest NLP
P4: We adopt SEPTE framework + develop SLM
P5: Data (HaoDF.com) + method + finding preview
P6: 3-way contribution (methodological / theoretical / empirical)
```

## Anti-patterns

- Burying the gap on page 4. The gap should appear by paragraph 3 (within the first page).
- Contribution list longer than 3 items (reads as fishing; ISR expects 2-3 tight contributions).
- No data/method preview in the intro. ISR readers expect to know the identification strategy before entering the theory section.
- Overclaiming: "we are the first" without "to the best of our knowledge."
- Ending the intro with "The rest of the paper is organized as follows..." without a contribution statement. (Both exemplars skip the roadmap sentence entirely.)

## Paragraph structure

- 6-8 paragraphs, each 5-10 sentences.
- First sentence of each paragraph is a topic sentence that advances the arc.
- Citation density: ~0.5 cites/sentence (half the sentences carry at least one citation).
- Footnotes used sparingly for institutional details (Bao uses footnotes for ACO program specifics).

## Enriched from additional exemplars (2026-06-29)

Sources: Mousavi 2026, Saifee 2020, Yang 2022, Shi 2025, Wang 2026, Wu 2025, Liu 2025, Zhang-j 2026, Schecter 2025.

### Word budget (revised)

Across 10 ISR papers the range is **1,350-2,800 words**, wider than the original 1,800-2,500.

| Paper | Intro words | Notes |
|---|---|---|
| Mousavi 2026 | ~1,350 | Compact; theory carries weight |
| Shi 2025 | ~2,200 | Commentary genre |
| Yang 2022 | ~2,200 | Design science, includes roadmap |
| Wang 2026 | ~2,500 | Flat (no subsections) |
| Saifee 2020 | ~2,800 | Subsectioned (1.1-1.3) |
| Wu 2025 | ~2,800 | 12 paragraphs |
| Liu 2025 | ~2,800 | 11 paragraphs |

**Revised target: 1,800-2,800 words.** Some papers go shorter (~1,350) when the theory section is heavyweight.

### Additional opening shapes

Beyond "declarative, institutional, cited," three more opening patterns emerge:

- **Platform-as-transformation** [Wang 2026]: "The rise of online healthcare question-and-answer (Q&A) platforms has fundamentally transformed how medical expertise is produced, shared, and accessed."
- **Societal sweep** [Yang 2022]: "We live in an era of great socio-economic uncertainty. At the same time, datafication, democratization, consumerization, and the ubiquity of social media have created a seemingly insatiable appetite for real-time analysis, insights, forecasts, and scrutiny."
- **Market universality** [Saifee 2020]: "Online consumer reviews play an important role in almost every market today, and the healthcare industry is no exception."
- **Innovation definition** [Wu 2025]: "Online health communities (OHCs) are an important technological innovation in primary care that affords physicians an expanded channel for offering diversified healthcare services to patients online, a trend that is reshaping the healthcare delivery system."
- **General empirical setting** [Shi 2025]: "In many empirical settings, the outcome variable of interest is potentially affected by a large array of factors in an intricate manner."
- SHAPE: `[Platform/technology/market] has [transformed/reshaped] [domain], [yet/but/however] [tension remains].`

### Introduction with subsections

Some ISR papers subsection the introduction itself:
- [Saifee 2020] 1.1 Theoretical Background, 1.2 Practical Relevance, 1.3 Research Overview
- [Zhang-j 2026] 1.1 Related Work, 1.2 Key Contributions and Implications, 1.3 Notation
- This pattern is acceptable when the introduction is long (>2,500 words) and needs internal structure.

### Additional gap phrases

Beyond "To the best of our knowledge," ISR papers use:
- [Wang 2026] "What remains underexplored is whether and how physicians' online consultations influence the actual clinical practice in offline settings."
- [Wu 2025] "remains an open empirical question" / "little is known about" / "surprisingly little attention is paid to" / "is a critical yet underexplored question" / "there is a notable lack of evidence concerning"
- [Liu 2025] "Previous research in this area has mainly investigated... Our study adds to this body of work by focusing on..."
- [Saifee 2020] "This is precisely where we contribute."
- [Yang 2022] "This is precisely the research gap we aim to address with our proposed framework."
- SHAPE: `What remains [underexplored/unknown] is [specific question].` or `[Topic] remains [an open empirical question / a critical yet underexplored question].`
- The "This is precisely where we contribute" sentence is a strong positioning move used in multiple papers.

### Research questions vs. hypotheses in the introduction

The original guide assumes lettered RQs: "(a) X? and (b) Y?" The new exemplars show two additional patterns:

- **Bold-labeled RQs** [Saifee 2020]: "**RQ1.** Are online reviews reliable indicators in the case of chronic disease care?" with sub-questions RQ1a, RQ1b, RQ2.
- **Bold + italic RQs** [Yang 2022]: "**Research Question 1.** *Relative to existing NLP methods, how effectively can DeepPerson detect personality dimensions from user-generated text?*"
- **Threefold objectives** [Shi 2025]: "The objectives of this research commentary are threefold. Firstly, we aim to... Secondly, we carry out... Lastly, we provide..."
- **No explicit RQs** [Wang 2026, Liu 2025]: research questions stated in prose ("This study addresses this gap by investigating whether...") without a formal RQ label.

### Why-the-effect-is-non-obvious move

[Liu 2025] lays out three specific reasons the effect direction is unclear, each with "First... Second... Third..." This preempts reviewer objections by showing the result is not trivially predictable:
- "First, the demand for general healthcare is often infrequent..."
- "Second, the Q&A service... may just be shifting the demand from other doctors..."
- "Third, on-demand healthcare platforms also have an impact on offline clinic and hospital visits."
- SHAPE: `[It is ex ante unclear whether X leads to Y for several reasons.] First, [reason 1]. Second, [reason 2]. Third, [reason 3].`

### Contribution enumeration variants

Beyond the 3-way (methodological/theoretical/empirical), ISR papers use:

- **Four contributions** [Wu 2025]: "First, it contributes to the literature on multichannel healthcare by... Second, it supplements the literature on... Third, this study adds additional value to... Finally, we contribute to the stream of literature on OHC engagement by..."
- **Three-fold** [Yang 2022]: "The main contributions of our work are three-fold. First, we propose... Second, we design... Third, we offer..."
- **Per-stream naming** [Wang 2026]: "Our study makes three key contributions. First, we advance theory on cognitive consistency... Second, we enrich the medical professionalism literature... Third, we extend the health information technologies (HIT) literature..."
- Each contribution explicitly names the literature stream it extends. This is a strong ISR norm across all new exemplars.
- **Revised guideline**: 3-4 contributions is the ISR range. More than 4 reads as fishing.

### Roadmap paragraph (revised anti-pattern)

The original guide says "Both exemplars skip the roadmap sentence entirely." This needs revision. Several new exemplars include a roadmap:
- [Yang 2022] Full section-by-section roadmap: "The remainder of the article is organized as follows. In the ensuing section, we discuss prior work... In Section 3, we introduce our proposed framework..."
- [Shi 2025] Forward pointers woven into the intro
- **Revised guideline**: A roadmap paragraph is acceptable but optional. If used, it should be the final paragraph of the intro, AFTER the contribution statement. Never use a roadmap as a substitute for the contribution statement.

### Motivating example as hook

[Shi 2025] opens Section 1 with a concrete, replicable example (published dataset, Table 1 showing specification sensitivity) before introducing any theory. This "problem-first" opening is effective for methodology papers:
- "Among these results, which one (if any) should we trust, and what can we reliably conclude...? This is arguably a very challenging question."
- SHAPE for methods papers: `[Concrete example showing the problem] -> [Why existing approaches fail] -> [What we propose]`

### Updated paragraph structure

- **6-12 paragraphs** (revised from 6-8). Papers with subsectioned introductions reach 12+ paragraphs.
- [Saifee 2020] ~18 paragraphs across subsections 1.1-1.3
- [Wu 2025] 12 paragraphs in a flat introduction
- [Liu 2025] 11 paragraphs with an internal "three concerns" structure
