# ISR Abstract Style Guide

Distilled from two ISR exemplars. Quote the SHAPE, not the content.

## Word budget

- Target: 120-180 words (unstructured prose, single paragraph).
- Bao 2021: ~160 words. Zhang 2026: ~180 words.
- No labeled subheadings (unlike MS-IS). Pure flowing prose.

## Arc (sentence-level structure)

The ISR abstract follows a 5-beat arc:

```
Beat 1: IS phenomenon + why it matters (1-2 sentences)
Beat 2: Gap or research question (1 sentence, often "we study whether...")
Beat 3: Approach = data + method/identification strategy (1 sentence)
Beat 4: Key finding(s) (2-3 sentences, guarded language)
Beat 5: Implication for theory or policy (1 sentence, closes the abstract)
```

## Signature moves

### Opening on the IS phenomenon, not the method
- [Bao 2021] Opens with the institutional context: "Accountable Care Organizations (ACO) were established under the Affordable Care Act to address systemic problems..."
- [Zhang 2026] Opens with the practical tension: "Large language models (LLMs) are advancing rapidly but remain expensive to train and deploy, especially in specialized domains such as healthcare."
- SHAPE: `[Institutional/practical context that sets the stakes] + [why this matters to IS].`
- Anti-pattern: opening with "In this paper, we..." or leading with the method.

### Research question as a compound "whether (a)... and (b)..." structure
- [Bao 2021] "we study whether (a) there are potential tradeoffs between ACO efficiency and quality, and (b) effective use of health IT enables ACOs to balance competing efficiency and quality objectives."
- SHAPE: `We study whether (a) [main effect] and (b) [moderator/mechanism].`

### Method stated in one compressed sentence
- [Bao 2021] "We test our models with a nationwide sample of ACO data using a two-stage approach based on data envelopment analysis and econometric estimation."
- [Zhang 2026] "Using a panel data set from one of China's largest online physician review and consultation platforms, we show that higher service-quality scores are associated with greater consultation demand."
- SHAPE: `We [test/estimate/analyze] [what] with [data description] using [identification strategy].`

### Findings use guarded verbs
- [Bao 2021] "We observe that..." (used 3 times). Never "we prove" or "we demonstrate" for the main association.
- [Zhang 2026] "we show that..." for the primary relationship.
- ISR-safe verbs: observe, find, show, demonstrate (for method performance), identify. Avoid: prove, establish, confirm.

### Closing on policy/practice implication
- [Bao 2021] "Our findings imply that value-based incentives alone are not sufficient to resolve tradeoffs... and healthcare policy needs to incorporate appropriate incentives..."
- [Zhang 2026] "...offering actionable guidance for healthcare professionals and administrators seeking to optimize services and increase uptake."
- SHAPE: `Our findings imply that [actionable takeaway for policy/practice].`

### Contribution statement compressed into the abstract
- [Zhang 2026] Embeds the 3-way contribution directly: "Our research contributes in three ways. Methodologically, we develop... Theoretically, we adapt... Empirically, we identify..."
- [Bao 2021] Does NOT enumerate contributions in the abstract; saves the labeled list for the introduction.
- Both patterns are acceptable. If space permits, the labeled 3-way is the stronger ISR signal.

## Exemplar shapes (anonymized)

```
[Bao shape]:
[Phenomenon + institutional context].
[Why it matters]. To develop a better understanding of [IT role],
we study whether (a) [main effect] and (b) [moderating mechanism].
We test our models with [data] using [method].
We observe that [finding 1]. Further, we observe that [finding 2].
Our findings imply that [policy implication].

[Zhang shape]:
[Practical tension: powerful but expensive technology].
[We address this by developing + operationalizing].
[Data + main result]. Our research contributes in three ways.
Methodologically, [method contribution].
Theoretically, [theory contribution].
Empirically, [empirical contribution].
```

## Anti-patterns

- Starting with "In this paper..." or "This study examines..." (too generic).
- Method bragging: devoting 3+ sentences to the algorithm architecture in the abstract.
- Overclaiming causality: using "effect" or "impact" without naming the identification strategy.
- Ending on "future research should..." instead of a concrete implication.
- Structured/labeled abstract format (that belongs to MS-IS, not ISR).

## Paragraph structure

Single paragraph, no line breaks. Keywords line follows (ISR format):
`Keywords: [term 1] . [term 2] . [term 3] . ...` (separated by centered dots or bullets).

## Enriched from additional exemplars (2026-06-29)

Sources: Mousavi 2026, Saifee 2020, Yang 2022, Shi 2025, Wang 2026, Wu 2025, Liu 2025, Zhang-j 2026, Schecter 2025.

### Word budget (revised)

The original 120-180 range was based on only 2 papers and is too narrow. Across 10 ISR papers the observed range is **150-300 words**, with most landing at 200-250.

| Paper | Abstract words |
|---|---|
| Shi 2025 | ~200 |
| Zhang-j 2026 | ~200 |
| Schecter 2025 | ~200 |
| Saifee 2020 | ~250 |
| Mousavi 2026 | ~250 |
| Wang 2026 | ~250 |
| Wu 2025 | ~250 |
| Liu 2025 | ~250 |
| Yang 2022 | ~300 |

**Revised target: 200-250 words.** Papers under 200 are commentaries; papers at 300 tend to embed contributions.

### Additional opening shapes

Beyond "IS phenomenon" and "practical tension," three more opening shapes emerge:

- **Task + audience importance** [Mousavi 2026]: "Extracting psychological constructs from text is increasingly essential for social science researchers who study attitudes, perceptions, and traits across digital communication."
- **Trend + behavior** [Saifee 2020]: "Current trends on patient empowerment indicate that patients who play an active role in managing their health also seek and use information obtained from online reviews of physicians."
- **Stakeholder desire** [Yang 2022]: "Analysts, managers, and policymakers are interested in predictive analytics capable of offering better foresight."
- **Phenomenon + gap fused** [Wang 2026]: "Digital platforms are reshaping professional service delivery, yet how online engagement feeds back into offline clinical practice remains unclear."
- **Although-tension** [Wu 2025]: "Although hospital-affiliated online health communities (OHCs) provide enormous potential for health promotion, their application can create uncertainty and complexities for existing off-line healthcare systems in terms of quality and equity concerns."
- **Genre label + method** [Shi 2025]: "This research commentary introduces double/debiased machine learning (DML), a novel methodological framework, to the information systems (IS) research community..."
- SHAPE: `[Although/Despite] [positive phenomenon], [tension/gap remains].` or `[Task/Activity] is increasingly essential for [audience] who [do X].`

### Additional closing shapes

- **Stakeholder enumeration** [Saifee 2020]: "Our findings have important ramifications for all stakeholders including hospitals, physicians, patients, payers, and policymakers."
- **Conceptual frame elevation** [Wang 2026]: "Overall, the findings position digital platforms as a form of 'soft governance' that complements formal oversight by activating intrinsic professional motives for consistency between online identity and offline practice."
- **Practical deliverable** [Mousavi 2026]: "To support immediate application, we also provide a researcher-friendly cookbook (in the Online Appendix) for using LLMs to annotate text data in practice."
- **Aspirational purpose** [Shi 2025]: "By promoting a deeper understanding and appropriate use of DML, this commentary aims to empower empirical research in IS."
- SHAPE: The strongest closings deliver a conceptual reframing or name a concrete deliverable, not just "implications for practice."

### Additional arc variants

**Commentary abstract** [Shi 2025] opens with genre self-identification: "This research commentary introduces [method]..." This is acceptable for methodology tutorials but not for empirical papers.

**Mechanism-branded abstract** [Wang 2026] names the coined mechanism (IBDC) in the abstract itself: "via an Identity-Based Digital Commitment (IBDC) mechanism." When a paper introduces a branded mechanism, embedding its name in the abstract strengthens recall.

**Negative-result abstract** [Saifee 2020]: "Contrary to popular belief, our study finds that there is no clear relationship between online reviews of physicians and their patients' clinical outcomes." Null findings are framed with "Contrary to..." to signal the result is surprising and therefore worth publishing.

### Additional guarded verbs (from new exemplars)

- [Wu 2025] "Our empirical results show..." / "results suggest..." / "findings indicate..."
- [Wang 2026] "This study demonstrates that..." (acceptable for well-identified effects)
- [Mousavi 2026] "we advocate for..." (advocacy verb acceptable in closing)
- ISR-safe additions: demonstrate (for well-identified results), advocate (closing only), highlight, underscore. Still avoid: prove, establish, confirm.

### Updated anti-patterns

- **Overclaiming for null results**: when the finding is null, frame as "Contrary to..." or "no clear relationship," not "we find no effect" (which sounds like a power problem). [Saifee 2020]
- **Missing the mechanism name**: if the paper coins a mechanism, the abstract should name it. [Wang 2026]
