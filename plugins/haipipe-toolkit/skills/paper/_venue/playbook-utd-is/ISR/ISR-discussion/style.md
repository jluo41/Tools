# ISR Discussion / Contributions / Conclusion Style Guide

Distilled from two ISR exemplars. Quote the SHAPE, not the content.

## Word budget

- Target: 1,500-2,500 words total across Discussion + Conclusion (sometimes merged, sometimes split).
- Bao 2021: ~2,200 words across "Discussion" (S8, ~1,200w) + "Policy Implications" (S8.1, ~600w) + "Conclusions" (S9, ~600w, includes limitations).
- Zhang 2026: ~1,800 words in "Contributions and Future Work" (S7, combines discussion + limitations + future work).

## Section naming conventions

```
Pattern A [Bao 2021]:
  8. Discussion
  8.1 Policy Implications
  9. Conclusions [includes limitations]

Pattern B [Zhang 2026]:
  7. Contributions and Future Work [combined section]
```

## Arc (paragraph-level structure)

The ISR discussion follows a 5-beat arc:

```
Beat 1: Contribution restatement (what we showed + why it matters to IS)
Beat 2: Theoretical implications (what this adds to IS theory)
Beat 3: Practical / policy implications (what practitioners should do)
Beat 4: Limitations (explicit, honest, not defensive)
Beat 5: Conclusion (1-2 paragraphs restating the contribution crisply)
```

## Signature moves

### Opening: contribution restatement, literature-positioned
- [Bao 2021] "Our research contributes to the extant literature on business value of health IT in an emerging value-based healthcare environment. While prior research has primarily examined the performance implications of health IT at a hospital level, these studies do not examine the tradeoffs between different dimensions of performance..."
- [Zhang 2026] "In the present study, we developed a fine-tuned SLM specifically designed to extract service quality scores from physician reviews by utilizing a refined healthcare service quality evaluation framework, and then we empirically demonstrated that these quality dimensions significantly impact online consultation demand..."
- SHAPE: `Our research contributes to the extant literature on [stream]. While prior research has [what they did], [what they missed / did not examine]. [What we did to fill that gap].`

### "To the best of our knowledge" reprise in discussion
- [Bao 2021] "To the best of our knowledge, our study represents the first attempt to address the broader question: can health IT use improve organizational capabilities needed to pursue both efficiency and quality?"
- SHAPE: Restate the gap-filling claim with the same hedged language used in the introduction.

### Theoretical implications: name the theory, state what is added
- [Bao 2021] "Drawing on theories of virtual organizations and information processing, we show that the inter-organizational structure of ACOs necessitates effective use of IT to coordinate patient care... Hence, our research highlights the role of information integration as a critical mechanism..."
- [Zhang 2026] "Theoretically, we adopt and refine a quality evaluation framework for healthcare service... ensuring that our SLM purposefully analyzes online reviews with a focus on providers' service quality rather than random text mining."
- SHAPE: `Drawing on [theory], we show that [mechanism/finding]. This extends [prior understanding] by [specific extension].`
- Name the theory explicitly. ISR reviewers want to see what theoretical conversation the paper joins.

### Practical / policy implications: actionable, specific
- [Bao 2021] Dedicated subsection 8.1 with 4 paragraphs: (1) incentive design for ACOs, (2) DEA framework as a practical tool, (3) interoperability policy, (4) data standards.
- [Zhang 2026] "For physicians, understanding the relative contribution of each SEPTE dimension enables physicians to prioritize targeted improvements... The refined SEPTE framework, tailored for online consultations, can also serve as a foundation for integrating patient-specific data..."
- SHAPE: `For [stakeholder group], our findings [suggest/imply] that [specific actionable recommendation]. Specifically, [concrete policy/design/management action].`
- ISR wants implications that a practitioner could act on, not vague "managers should pay attention to..."

### Limitations: numbered, honest, scoped
- [Bao 2021] "Our study does have several limitations." Then 4 numbered limitation paragraphs, each following: (1) state the limitation, (2) acknowledge why it matters, (3) note what was done to mitigate (if anything), (4) suggest how future research could address it.
- [Zhang 2026] "Our study has several limitations that suggest future research." Then 4 limitation items.
- SHAPE per limitation: `[Limitation]. While we [mitigation attempt], future studies can [specific direction].`

### Exemplar limitation shapes
- [Bao 2021] "While meaningful use provides a reasonable proxy for effective health IT use, our data does not allow us to track the use of IT for specific care coordination practices... We acknowledge that our study provides the first step toward collecting such data for research and policymaking."
- [Bao 2021] "Fourth, our study is restricted to Medicare ACOs and may not be generalizable to other programs, such as ACOs for non-Medicare beneficiaries."
- [Zhang 2026] "First, our analysis relies exclusively on online platform data and does not incorporate offline clinical outcomes such as readmission rates, complication rates, or treatment success metrics."
- SHAPE: state the limitation, acknowledge its importance, note any mitigation, point to future work. Never defensive.

### Conclusion: 1-2 paragraphs, mechanism-first
- [Bao 2021] "In this study, we demonstrate the role of effective health IT use as an enabler of health information sharing capabilities necessary to achieve competing organizational objectives... Our research underscores the importance of well-designed incentive models to promote inter-organizational information sharing for efficient, high-quality care."
- [Zhang 2026] Combined into the same section; final paragraphs restate the algorithmic and empirical contributions.
- SHAPE: `In this study, we [demonstrate/show] the role of [mechanism] in [achieving outcome]. [One sentence on broader significance]. [One sentence on policy/design takeaway].`

## Paragraph structure

```
[Bao discussion arc]:
P1: Contribution to IT value literature (mechanism = info integration)
P2: Study positioned against prior health IT research
P3: ACO setting as unique contribution (value-based care)
P4-P7: Policy implications (incentive design, DEA tool, interoperability, data standards)

[Bao conclusion arc]:
P1: Main finding restated (IT use as enabler of info sharing)
P2-P5: Limitations (proxy measure, complementary investments, regulatory change, generalizability)

[Zhang discussion arc]:
P1: Summary of what was done and found
P2: Algorithmic advantages of Doc-BERT (3 points)
P3: Theoretical contribution (SEPTE framework)
P4: Methodological contribution (SLM approach)
P5: Practical implications for physicians and platforms
P6: Practical implications for platform operators
P7-P10: Limitations and future work
```

## Anti-patterns

- Opening the discussion with a methods summary ("In this paper we used DEA and OLS..."). Lead with the contribution, not the method.
- Limitations that are too vague ("our study has limitations"). Each limitation should name a specific threat.
- Overclaiming in the discussion that exceeds what the results showed. If H1 was not supported, do not imply it was.
- "Future research should..." as a substitute for limitations. State the limitation first, then the future direction.
- Missing the theoretical implication entirely (going straight from findings to practice). ISR requires explicit positioning in IS theory.
- No dedicated limitations paragraph/subsection. ISR expects honest, visible limitations.

## Acknowledgments

- [Bao 2021] "We gratefully acknowledge the guidance and constructive feedback from the editors and review team." Lists conference presentations and seminar audiences.
- [Zhang 2026] "The authors thank the senior editor, associate editor, and anonymous reviewers for constructive comments that significantly improved this manuscript."
- SHAPE: Thank editors + reviewers first. Then name conferences/seminars where earlier versions were presented. Then funding.

## Enriched from additional exemplars (2026-06-29)

Sources: Mousavi 2026, Saifee 2020, Yang 2022, Wang 2026, Wu 2025, Liu 2025, Shi 2025, Zhang-j 2026, Schecter 2025.

### Word budget (revised)

Across new papers, the range expands slightly:

| Paper | Discussion + Conclusion | Limitations location |
|---|---|---|
| Mousavi 2026 | ~850 (Discussion) + ~550 (separate Limitations S6) | Separate section |
| Saifee 2020 | ~1,500 (Conclusions 6.1 + 6.2) | Subsection 6.2 |
| Yang 2022 | ~2,200 (Discussion + Conclusion) | One paragraph within Discussion |
| Wang 2026 | ~2,500 (5.1 Summary + 5.2 Theoretical + 5.3 Managerial) | Embedded in Summary |
| Wu 2025 | ~2,800 (7.1 Contributions + 7.2 Implications + 7.3 Limitations) | Subsection 7.3 |
| Liu 2025 | ~2,800 | Last 2 paragraphs |

**Revised target: 850-2,800 words.** Papers with compact Discussions (~850) offset with a separate Limitations section. The structural choice is whether to merge or split limitations.

### Additional section naming patterns

```
Pattern C [Wang 2026]:
  5. Discussion and Conclusion
    5.1 Summary of Findings
    5.2 Theoretical Implications
    5.3 Managerial Implications

Pattern D [Wu 2025]:
  7. Conclusions
    7.1 Contributions
    7.2 Managerial Implications
    7.3 Limitations and Future Research

Pattern E [Mousavi 2026]:
  5. Discussion and Conclusion [no subsections]
  6. Limitations and Future Research [separate section]

Pattern F [Yang 2022 - design science]:
  6. Discussion + Conclusion [combined, with numbered named implications]
```

Patterns C and D are the most structured. Pattern E separates limitations into their own section number.

### Contribution mirroring

[Wang 2026] mirrors the 3-contribution structure from the Introduction in the Discussion:
- Intro: "Our study makes three key contributions. First, ... Second, ... Third, ..."
- Discussion (5.2): "Our study advances theory on digital platforms and professional behavior through three interconnected contributions, each illuminating how OHPs function as soft governance mechanisms..."
- SHAPE: The Discussion contribution block should echo the Introduction's contribution enumeration, but with deeper elaboration and connection to results. Same structure, richer content.

### Numbered, named implications

[Yang 2022] uses numbered implications with italicized provocative titles:
> (1) *Debunking the 'Brute Force AI' Fallacy*
> (2) *Design Science as a Mechanism for Middle-Ground Frameworks*
> (3) *Importance of Personality for Predicting Policy*
> (4) *Toward Proactive Personalization*
- Each gets a paragraph of elaboration.
- This converts the Discussion from summary into forward-looking argument.
- SHAPE: `(N) *[Provocative/memorable title]*. [One paragraph elaborating the implication].`

### Conceptual frame elevation in closing

The strongest ISR Discussion closings elevate the finding into a higher-order concept:
- [Wang 2026] "By making clinical values explicit, visible, and self-attributed, online platforms create accountability structures that complement formal regulation, not through external enforcement, but by activating the internal consistency pressures defining professional identity itself."
- [Mousavi 2026] "we advocate for the acceptance of LLMs as a standard for psychometric NLP in social science research."
- SHAPE: The final sentence should deliver the broadest conceptual claim, not a summary of findings. Elevate from "we found X" to "this means Y for the field."

### Stakeholder enumeration in implications

[Saifee 2020] closes the abstract and restates in Discussion: "Our findings have important ramifications for all stakeholders including hospitals, physicians, patients, payers, and policymakers."
- [Wu 2025] organizes implications by stakeholder: platform operators, physicians, patients, policymakers.
- SHAPE: `For [stakeholder], our findings suggest [actionable recommendation].` Repeat for each stakeholder group.

### Design insights as discussion output

[Mousavi 2026] converts results into "design insights" -- a numbered list of actionable principles:
- Three design insights for researchers using LLMs for text annotation
- These function as the practical counterpart to theoretical implications
- SHAPE for artifact/methods papers: `Our results yield [N] design insights. Design Insight 1: [principle]. Design Insight 2: [principle].`

### Advisory register for methodology papers

[Shi 2025] uses an advisory tone in the discussion:
- "We recommend empirical researchers carefully tune..."
- "We advise against applying DML to very small data..."
- "We emphasize that DML is not a 'magic bullet'..."
- SHAPE: For methods papers, the discussion can shift to direct recommendations using "We recommend..." and "We advise against..."

### Limitation placement patterns

Three ISR-standard approaches to placing limitations:

1. **Dedicated subsection within Conclusion** [Wu 2025: S7.3, Saifee 2020: S6.2]: ~1 page, 3-5 numbered limitations. This is the most common pattern.

2. **Separate top-level section** [Mousavi 2026: S6]: "Limitations and Future Research" as its own numbered section, ~550 words, 3 paragraphs. Gives limitations more prominence.

3. **Embedded in Summary** [Wang 2026]: Limitations appear in S5.1 (Summary), after the results summary and before Theoretical Implications. 4 limitations, each 1-2 sentences.

4. **One brief paragraph** [Yang 2022]: ~150 words, the most compact treatment. Opens with "Our work is not without its limitations." Lists 3-4 items in rapid succession, each framed as future work.

### Limitation formula variants

Beyond the existing "[Limitation]. While we [mitigation], future studies can [direction]":

- **"Our study has inherent limitations that, in turn, suggest promising avenues for future research."** [Mousavi 2026] -- links limitation to opportunity in one sentence.
- **"The study has several limitations that may motivate future works."** [Wu 2025] -- neutral framing.
- **"Despite its advantages, the [method] faces several limitations that merit careful consideration."** [Schecter 2025] -- method-focused.
- **"Our work opens new opportunities for future researchers."** [Zhang-j 2026] -- reframes limitations as opportunities without using the word "limitations."

### Limitation content patterns (from new exemplars)

Five recurring limitation types across new papers:

1. **Generalizability to other contexts**: "our analysis is based on [one platform/hospital/country], and it is not immediately known whether the results would be applicable to other [settings]." [Saifee 2020, Wu 2025, Wang 2026]

2. **Outcome measurement scope**: "we measure health outcomes in terms of [proxy], future studies should consider evaluating actual [direct outcomes]." [Liu 2025, Saifee 2020]

3. **Construct measurement proxy**: "we developed SES indicators based on patient occupation. Future studies can utilize patient characteristics such as education and income." [Wu 2025]

4. **Mechanism identification limits**: "a lack of data on how [actors] make decisions makes it difficult to pinpoint the exact mechanisms." [Saifee 2020]

5. **ML/AI scope**: "our design evaluation focused on [specific data types]. Other relevant documents that might warrant exploration include [other types]." [Yang 2022]

Each follows the pattern: State what was NOT measured/tested -> Note why it matters -> Point to future work that could address it.

### "Contrary to" framing for null results in Discussion

[Saifee 2020] carries the "Contrary to popular belief" framing from the abstract through to the Discussion:
- "Contrary to some earlier findings, we do not observe any evidence..."
- This is the correct ISR framing for a null result: the null IS the contribution when it is theoretically predicted and empirically robust.
- SHAPE: `Contrary to [prior findings/popular belief], our [robust] results indicate [null/opposite]. This is consistent with [theory] because [mechanism].`

### "Not a magic bullet" caveat for methods papers

[Shi 2025] and [Schecter 2025] both use this pattern:
- "We emphasize that whereas [method] is a powerful tool..., it cannot override the necessity of fundamental [assumptions]."
- [Schecter 2025] "Our results should not be read as claiming universal superiority of the robust estimator."
- SHAPE: For methods papers, explicitly state what the proposed method does NOT do. This builds credibility and preempts reviewer criticism.

### Updated anti-patterns

- **Limitations paragraph shorter than 100 words for empirical papers.** ISR expects 3-5 specific limitations, each with mitigation or future direction. The one-paragraph style [Yang 2022, ~150 words] works for design science but is too thin for empirical work.
- **Closing the paper on a limitation.** The final sentence should be a positive contribution restatement or conceptual elevation, never a caveat. [Wu 2025 closes on a future-research opportunity; Wang 2026 closes on the broadest conceptual claim.]
- **Discussion that only restates results.** ISR requires the Discussion to ADD something: theoretical positioning, conceptual elevation, or design insights. A pure summary is not a Discussion.
