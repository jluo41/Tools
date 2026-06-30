# MISQ Discussion -- Section Style Guide

Extracted from MISQ Research Article exemplars. Supplements `style-profile.md`.

Called "Discussion," "General Discussion," or split into titled subsections. This section restates contribution, draws out implications (research first, then practice), acknowledges limitations, and closes. MISQ discussions are substantial -- not a two-paragraph afterthought.

## Word budget

- 2,500-5,000 words (5-10 published pages two-column).
- Liu (2021): ~4,000w across "Discussion" with subsections (pp. 1128-1132, 5 pages).
- Yin (2014): ~3,000w across "General Discussion" with subsections (pp. 554-556, 3 pages).
- Gao (2015): discussion section is shorter at ~1,500w but the paper combines methodology/results.

## Arc

```
summary / contribution restatement (1-2 paragraphs)
  -> Implications for Research (2-4 paragraphs)
  -> Implications for Practice (2-3 paragraphs)
  -> Limitations and Future Research (2-4 paragraphs)
  -> Concluding Remarks (1 paragraph)
```

The arc is **contribution-first, limitations-second, close-forward**. The discussion OPENS by restating what was accomplished, not by hedging.

## Signature moves

1. **Summary paragraph restates the research question and key findings.** The discussion opens by reminding the reader what the paper set out to examine and what it found, in 3-5 sentences. This is a compressed version of the abstract, not a repeat of the results.
   - "This research sets out to examine the question of who will provide future helpful product reviews by integrating theories related to personality and data analytics into a four-step procedure." [Liu 2021]
   - "Together, the experiments in Studies 1 and 2 and the real-world investigation in Study 3 provide converging evidence for our framework." [Yin 2014]

2. **"Implications for Research" as a titled subsection.** MISQ discussions almost always have a titled "Implications for Research" or "Theoretical Implications" subsection. This is where the paper connects findings back to theory and names the specific theoretical contribution.
   - "Our work joins the burgeoning scientific investigations in various domains that apply new methods of assessing unacquainted individuals -- in our case, inferring their personality traits -- by mining online data (Brynjolfsson et al. 2016; Varian 2014)." [Liu 2021]
   - "Prior empirical investigations of online reviews have tended to focus on ratings and observable reviewer characteristics, leaving the textual content of reviews unexplored. Addressing this gap, we contribute to emerging research indicating that the rich information embedded in review text can itself be useful in explaining what constitutes a helpful review." [Yin 2014]

3. **Numbered research implications.** The "Implications for Research" section often enumerates multiple distinct theoretical contributions: "First, our research illustrates a new way to effectively evaluate personality... Second, our research illustrates how theories related to personality can guide feature selection in predictive models... Third, our research provides a promising new way to effectively evaluate personality at zero acquaintance." [Liu 2021]

4. **"Implications for Practice" as a separate titled subsection.** MISQ expects explicit practical implications, not just academic ones. This subsection addresses platform managers, policymakers, or practitioners with specific actionable guidance.
   - "Our work has useful implications for practice. In this work, we identified a connection between people's personality traits and their review helpfulness." [Liu 2021]
   - "Although review authors undoubtedly have numerous motivations, one of these is often the desire to assist future customers via helpful information regarding a seller, transaction, or product. Negative reviews have the potential to influence the attitude and behaviors of future customers to a greater extent than positive reviews." [Yin 2014]

5. **Ethical considerations within practice implications.** Liu (2021) notably includes an AI ethics discussion within the practice implications, organized around four principles (beneficence, non-maleficence, justice, explicability). This may be increasingly expected for MISQ papers using AI/ML methods.

6. **Limitations as specific threats, not generic hedges.** Each limitation is a concrete, named threat to validity, followed by the specific future work that would address it. The pattern is: "First, we use data from one review platform... future research should apply our approach to other data sources." [Liu 2021]
   - Liu (2021) lists four specific limitations: single platform, historical data (no causality), Big Five only, training data quality.
   - Yin (2014) lists: two emotions only (anxiety/anger), seller reviews not product reviews, assumptions about emotional state inference.

7. **Concluding Remarks as a single paragraph.** The paper closes with a short paragraph (3-5 sentences) that restates the contribution at the highest level and expresses hope for future impact. This is brief and forward-looking.
   - "This work discovers reviewers' personality through a deep learning-based NLP approach and demonstrates the power of a personality model for predicting future review helpfulness. It illustrates two routes for synergistically leveraging theory and data." [Liu 2021]
   - "In keeping with recent interest in the integration of affective factors into existing IS frameworks, we suggest that scholars will benefit greatly from a better understanding of the impact of discrete emotions." [Yin 2014]

## Exemplar sentences (shape, not content)

**Discussion opener (contribution restatement)**:
- "This research sets out to examine the question of who will provide future helpful product reviews by integrating theories related to personality and data analytics into a four-step procedure. We first trained a deep learning model to infer a reviewer's personality traits. Second, we developed hypotheses on how personality traits are associated with review helpfulness based on personality theories. Third, our hypothesis testing results show that..." [Liu 2021]
- "Together, the experiments in Studies 1 and 2 and the real-world investigation in Study 3 provide converging evidence for our framework. Extending traditional, valence-based approaches, these studies demonstrated the differential impact of discrete negative emotions on review helpfulness." [Yin 2014]

**Research implication (scope/generalization move)**:
- "Although we only apply the deep learning NLP algorithms for inferring personality traits in the context of online product review platforms, there is a wide scope of contexts where such methods are applicable." [Liu 2021]
- "Typical research on the effects of discrete emotions examines two or three emotions that are most relevant to the question being examined. In keeping with this approach, we restricted our focus to the emotions of anxiety and anger; however, our underlying logic could be used to predict the effects of a wide variety of emotions embedded in reviews on reader perceptions." [Yin 2014]

**Practice implication**:
- "Practically, our proposed method can effectively predict most helpful reviewers soon after they post a review and it therefore offers great value for review-centric sites and platforms." [Liu 2021]
- "At a broader level, review platforms themselves might utilize our findings in developing writing guidelines to encourage more useful seller reviews." [Yin 2014]

**Limitation (specific)**:
- "First, we use data from one review platform and we limit our sample to the restaurant category of the Yelp Academic Dataset. Although this is a widely used dataset and Yelp is a leading review platform, future research should apply our approach to other data sources and categories to test its validity." [Liu 2021]
- "Although our studies examined two particular emotions -- anxiety and anger -- that are prevalent in seller reviews, other emotions are also common (disappointment, happiness, surprise, etc.)." [Yin 2014]

**Concluding paragraph**:
- "This work discovers reviewers' personality through a deep learning-based NLP approach and demonstrates the power of a personality model for predicting future review helpfulness. It illustrates two routes for synergistically leveraging theory and data. ... We hope our work will stimulate more research on the use of data and theory via these routes." [Liu 2021]

## Anti-patterns

- Do NOT open the discussion with limitations. Open with the contribution restatement.
- Do NOT skip practical implications. MISQ reviewers expect explicit implications for practice, not just theory.
- Do NOT write generic limitations ("our study has several limitations"). Each limitation must be specific, named, and paired with a concrete future-work direction.
- Do NOT claim causality in the discussion if the design is correlational. If IV/identification was layered as robustness, maintain the same guarded language ("association," "consistent with") used in the results.
- Do NOT let the concluding paragraph become a second abstract. Keep it to 3-5 sentences that look forward.
- Do NOT omit ethical considerations when the paper uses AI/ML methods on user data. MISQ increasingly expects this.

## Paragraph structure

| Subsection | Paragraphs | Job |
|-----------|-----------|-----|
| Summary / Contribution Restatement | 1-2 | What the paper set out to do and found |
| Implications for Research | 2-4 | Numbered theoretical contributions, scope, generalization |
| Implications for Practice | 2-3 | Actionable guidance for managers/platforms/policymakers |
| [Optional: Ethical Considerations] | 1-2 | AI ethics, fairness, transparency (for ML papers) |
| Limitations and Future Research | 2-4 | Specific threats, each paired with future work |
| Concluding Remarks | 1 | 3-5 sentence forward-looking close |

## Tone

The discussion tone is measured and honest. Contributions are stated clearly but not oversold. Limitations are acknowledged without apologizing. The overall register is "we did this, here is what it means, here is what we could not do, here is where the field should go."

---

## Enriched from additional exemplars (2026-06-29)

Source papers: Zhang (2025), Weng (2026), Ayabakan (2025), Raimi (2025), Liu-EBM (2025), Liu-HMM (2025).

### Section naming variants (expanded)

- "Discussion and Conclusion" [Zhang 2025, Ayabakan 2025, Liu-HMM 2025] -- combined format is common for both Research Articles and Research Notes.
- "Discussion" [Weng 2026] with separate "Conclusion" subsection.
- "General Discussion" [Raimi 2025] -- used for multi-study papers where each study has its own mini-discussion.

### Updated word budget

- Zhang (2025): ~3,500w across "Discussion and Conclusion" with subsections.
- Weng (2026): ~4,000w across "Discussion" + "Conclusion".
- Ayabakan (2025, Research Note): ~1,500w for "Discussion and Conclusion." Research Notes are substantially shorter.
- Raimi (2025): ~3,500w for "General Discussion" (after per-study mini-discussions).
- Liu-HMM (2025, Research Note): ~1,800w for "Discussion and Conclusion."

### Additional signature moves

8. **"Managerial Implications" or "Practical Contributions" as a separate titled subsection.** The "Implications for Practice" pattern is now frequently titled "Managerial Implications" (Zhang 2025) or "Practical Contributions" (Weng 2026), reflecting a shift toward more concrete, stakeholder-specific guidance.

9. **Design-specific actionable guidance in managerial implications.** Healthcare and platform papers provide specific platform-design recommendations, not just generic "managers should consider" advice.
   - "instead of a complete cut-off the double incentives, we recommend that platforms take a gradual and stepwise approach to smooth out the deep drop in incentives ... e.g., 20% down in the first month, 30% down in the second month, etc." [Zhang 2025]
   - "policymakers might consider introducing policies for greater interoperability and data/interface standardization of EHR applications from different vendors" [Ayabakan 2025]

10. **Numbered theoretical contributions (strongly confirmed).** All 6 new papers number their theoretical contributions explicitly ("First, ... Second, ... Third, ..."). This is now a near-universal MISQ pattern, not just a common one.
    - Zhang (2025): 3 numbered contributions (dual impacts, mental accounting perspective, income source dependence).
    - Weng (2026): 4 numbered contributions (extending IT risk control framework, identifying trait-control pairings, identifying intervention points, meta-traits at team level).
    - Liu-HMM (2025): 3 numbered contributions (operationalizing ADF+IBLT, revealing polarization, demonstrating HMM as tool).

11. **Counterintuitive-findings emphasis in discussion.** When results contradict prior assumptions, the discussion opens by explicitly restating the surprise and its theoretical significance.
    - "We found no evidence to support our hypothesis that chatbots are perceived to be less judgmental than human healthcare providers. In fact, the results suggest an effect in the opposite direction." [Raimi 2025]
    - "Second, and unexpectedly, we found that the contributions of affected physicians dropped dramatically after the policy window ended" [Zhang 2025]

12. **"Polarization" and "dynamics" language for longitudinal findings.** Papers using longitudinal/dynamic methods (HMM, panel data) use language about polarization, feedback loops, and path dependence rather than static association language.
    - "We also found a potential polarization of delegation willingness developed throughout the adaptive process of continuous performance assessment and delegation." [Liu-HMM 2025]

13. **Healthcare-specific limitations.** Healthcare MISQ papers name domain-specific limitations: single-state data (Maryland), single-platform data (one OHC), PHI constraints on generalizability, inability to observe offline behavior.
    - "We acknowledge this unique context of Maryland as a limitation potentially impacting generalizability." [Ayabakan 2025]
    - "First, when exploring physicians' contributing behavior in OHCs, we did not account for their offline workload or schedule." [Zhang 2025]

14. **AI ethics and design implications.** Papers studying AI/chatbot behavior include a dedicated discussion of design implications for AI systems, going beyond the generic ethics section noted in Liu (2021).
    - "building a better chatbot is necessary, but not sufficient ... Healthcare providers need to address users' fundamental beliefs about chatbots before users use them" [Raimi 2025]
    - "solely focusing on reconciling human and AI decisions through transparent decision-making processes ... may be insufficient for mitigating the persistent reluctance exhibited by certain employee groups" [Liu-HMM 2025]

15. **Concluding Remarks paragraph pattern for Research Notes.** Research Notes use a single concluding paragraph that is shorter (3-4 sentences) and more forward-looking than Research Articles.
    - "There are numerous future research opportunities on the role of digital technologies in healthcare and other industries." [Ayabakan 2025]

### Per-study mini-discussion pattern (multi-study papers)

Raimi (2025) demonstrates a per-study discussion pattern:
- Each Study (1, 2, 3) has its own "Discussion" subsection (200-400w).
- Per-study discussions interpret findings, connect to the larger arc, and motivate the next study.
- The "General Discussion" section at the end synthesizes across all studies.
- Theoretical contributions are stated in the General Discussion, not in per-study discussions.

### Paragraph structure (expanded for Research Notes)

| Subsection | Paragraphs (Research Article) | Paragraphs (Research Note) |
|-----------|-----|-----|
| Summary / Contribution Restatement | 1-2 | 1 |
| Theoretical Contributions | 2-4 (numbered) | 1-2 (numbered, compressed) |
| Practical / Managerial Implications | 2-3 | 1-2 |
| Limitations and Future Research | 2-4 | 1-2 |
| Concluding Remarks | 1 | 1 (sometimes omitted; merged with limitations) |

### Updated anti-patterns

- Do NOT provide vague managerial implications ("managers should be aware of..."). MISQ now expects specific, actionable design recommendations (gradual incentive reduction, EHR standardization policies, chatbot design changes).
- Do NOT skip the counterintuitive-findings emphasis when results defy prior theory. This is the highest-value content in the discussion for MISQ reviewers.
- Do NOT write a 4,000w discussion for a Research Note. 1,500-1,800w is the norm.
- Do NOT present theoretical contributions without numbering. "First, ... Second, ... Third, ..." is now near-mandatory.

### Exemplar sentences from new papers

**Discussion opener**:
- "This paper examines the impact of introductory incentives on newly enrolled physicians in OHCs. Our results indicate that introductory incentives impose distinct effects on physician contributions during and after the policy window." [Zhang 2025]
- "Our work adds to the literature on IT project management and augments the understanding of how IT project managers can mitigate IT project risks by considering team personality." [Weng 2026]
- "Across four online or in-person experiments with samples drawn from a student population, as well as three separate online survey pools representative of the U.S. population, participants consistently reported that they perceived the chatbot to be more judgmental than the human mental health care professional" [Raimi 2025]

**Specific managerial implication**:
- "A good strategy could be using platform-issued digital wallets to disburse monetary incentives instead of relying on direct deposit to bank accounts (as routine salaries do)." [Zhang 2025]
- "we suggest that it is important to improve vendor interoperability among EHR applications within and across hospitals" [Ayabakan 2025]
- "When deciding on IT project process controls, project managers can preemptively consider how teams will perform differently based on their project team personality" [Weng 2026]

**Specific limitation**:
- "when implementing the policy, physicians were aware of the initiation and termination of the introductory incentives. Such awareness may have induced strategic behaviors when contributing to the OHC" [Zhang 2025]
- "we do not know why individual claims are denied. Also unknown to us is whether each denied claim is reprocessed for an appeal" [Ayabakan 2025]

**Concluding paragraph**:
- "User engagement is crucial for online communities; without active contributions from users, any online community will eventually wither." [Zhang 2025]
- "There have been few studies of the role of team personality in IT projects. However, 'the ability to achieve high IT project performance is contingent on the influence of technology, people and process'" [Weng 2026]
