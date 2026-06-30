# Diabetes Care -- Discussion/Conclusions Style Guide

Distilled from 10 Diabetes Care papers: Galindo 2026 (RCT/Brief), Reaven 2026 (TTE), Bergenstal 2026 (GRADE), Lehmann 2026 (ML/Brief), Zheng 2025 (NLP), Kahkoska 2025 (e-Letter), He 2026 (e-Letter), Godneva 2026 (TIR), Ajjan 2026 (gDAC), Dupenloup 2026 (cost-effectiveness).

## Critical convention: section heading

Diabetes Care uses **CONCLUSIONS** (all caps) as the section heading for what other journals call "Discussion". This section contains full discussion-style content (interpretation, comparison to prior work, mechanisms, limitations) followed by a concluding statement. It is effectively a merged Discussion + Conclusion under the CONCLUSIONS heading.

This is a distinctive Diabetes Care convention. Never use "DISCUSSION" as the heading.

## Word budget

- Original Article: 1200-2500 words (5-12 paragraphs). Reaven 2026 runs ~12 paragraphs with named subsections; shorter papers run 5-8 paragraphs.
- Brief Report: 400-800 words (~3-5 paragraphs).
- e-Letters: ~200-400 words woven into body text, no separate heading.

### Contrast with JAMA

JAMA IM uses a "Discussion" heading with a clearly separated "Conclusions" subsection (colored heading, horizontal rule). Diabetes Care merges everything under CONCLUSIONS. JAMA IM Discussions have more explicit policy framing; Diabetes Care CONCLUSIONS focus more on clinical interpretation and ADA Standards context.

## Arc

```
P1: Principal findings (restate design + main result)
    |
P2-P4: Comparison to prior work + interpretation + mechanisms
    |
P5-P6: ADA Standards context + clinical implications
    |
P7: Strengths (optional, sometimes woven into prior work)
    |
P8: Limitations (1-2 paragraphs)
    |
P9: Final concluding paragraph ("In conclusion, ...")
```

For longer Original Articles (Reaven), CONCLUSIONS can have named subsections:
- Effects of CGM Initiation on Mortality
- Effects of CGM Initiation on Interim Outcomes
- Potential Mechanisms of Protection
- Limitations
- Conclusion

## Paragraph-by-paragraph structure

### Paragraph 1: Principal findings

Opens by restating the design, population, and main result.

**Template**: "In this [study design], we [demonstrated/found/showed] that [main finding]."

Exemplar opening sentences:
- "In this RCT, we demonstrated that using rtCGM for just 30 days improved glycemic control compared with CBG testing (SOC) in people with T2D undergoing hemodialysis." (Galindo).
- "We demonstrate, in a large national cohort, that initiation of CGM was associated with lower mortality in pwT1D" (Reaven).
- "Leveraging the growing ubiquity of smart devices with integrated microphones and noninvasive voice-based approaches may complement established methods for hypoglycemia detection, thereby furthering the care of people with diabetes." (Lehmann).
- "Our study is pioneering in using an NLP approach to extract glucose data from CGM reports stored as PDF files, which builds a strong foundation of secondary use of existing CGM data for population-based research to improve diabetes care." (Zheng).
- "Our analysis suggests that CGM with RPM is cost-effective and potentially cost-saving compared with CGM alone for a pediatric cohort newly diagnosed with type 1 diabetes." (Dupenloup).
- "In this study we have used a large deeply phenotyped cohort to gain a better understanding of the spectrum of normoglycemia as assessed by CGM devices..." (Godneva).

**Signature move**: Most papers open with "In this [design]" or "We demonstrate". ML/technology papers may lead with the clinical significance statement instead. Either way, the opening paragraph restates the main finding.

### Paragraphs 2-4: Comparison to prior work + interpretation

Contextualizes findings against prior literature and offers clinical interpretation.

Typical phrases:
- "For years, there has been a concern that patients with diabetes treated by hemodialysis are exposed to frequent hypoglycemia (1,2,6-8)." (Galindo).
- "Previous voice research in people with diabetes has linked chronic hyperglycemia and polyneuropathy to hoarseness, vocal strain, and changed pitch (10-12). Here, we show that voice can also signal an acute and hazardous health state..." (Lehmann).
- "These results were consistent with a report that use of real-time CGMs was associated with reductions in hypoglycemia leading to emergency department visits..." (Reaven).

**Signature move**: Comparison paragraphs contextualize findings within ADA Standards of Care or International Consensus recommendations. References to Battelino 2019 (Time in Range consensus) and ADA Standards are common anchor points.

### Mechanisms paragraph (optional)

Offers plausible explanations with hedging language.

Exemplar:
- "We hypothesized that participants using rtCGM patterns and predictive hypoglycemia alarms could take proactive measures, including adjusting their meal intake or medication dosing, to prevent glycemic excursions..." (Galindo).
- "The potential benefits of CGM began to appear by year 1 and slowly increased over the 4 years of follow-up... This translated into a number needed to treat of 49 to prevent one death event over 4 years." (Reaven).

**Signature move**: Mechanisms are framed as hypotheses ("we hypothesized") or possibilities ("may", "could"), never as established facts. Multiple competing explanations may be presented.

### ADA Standards context paragraph

Many Diabetes Care papers include a paragraph connecting findings to current ADA treatment recommendations.

Exemplar:
- "The American Diabetes Association 'Standards of Care in Diabetes' has recommended the inclusion of standard AGP reports for glucose assessment (6). These reports... should be considered a standard printout for all CGM devices." (Zheng).
- "these findings provide further support for CGM initiation as standard of care for adult-onset type 1 diabetes" (Reaven).

### Strengths paragraph (optional)

Sometimes woven into the comparison paragraphs:
- "The strength of our work lies in its interventional and prospective design, using venous BG values in standardized euglycemia and hypoglycemia as the gold standard for ML modeling." (Lehmann).
- "A strength of this study is the use of the VHA's comprehensive medical records and the TTE methodology..." (Reaven).
- "By contrast, strengths of the current solution include no-cost access to the existing CGM AGP reports, and minimal technical requirements to obtain valuable CGM glucose data." (Zheng).

### Limitations (1-2 paragraphs)

Limitations are embedded within the CONCLUSIONS section, not a separate section heading (with one exception: Reaven uses a named "Limitations" subsection within CONCLUSIONS).

Signaled by:
- "We acknowledge some limitations, including..." (Galindo).
- "The limitation of our approach is that..." (Zheng).
- "Our analysis has several limitations." (Dupenloup).
- "This study also has several limitations." (Godneva).
- "Limitations include a restricted study period and inclusion of Medicare Fee-for-Service only." (Kahkoska).

Common limitation types:
1. **Sample size**: "a small sample size, only including insulin-treated patients" (Galindo).
2. **Generalizability**: single center, specific population, geographic restriction.
3. **Data limitations**: claims data lacking clinical detail, CGM data availability.
4. **Measurement**: proxy outcomes, CGM accuracy in specific populations.
5. **Study design**: observational design, cross-sectional, residual confounding.
6. **Technology limitations**: algorithm scope, device specificity.

**Signature move**: Each limitation is often followed by a brief mitigation statement or acknowledgment of its bounded impact: "Although the ML model was built on data of young individuals with type 1 diabetes... the concept may extend to all people using treatments associated with a risk for hypoglycemia." (Lehmann).

### Final concluding paragraph

The CONCLUSIONS section ends with a paragraph that restates the main finding and offers a forward-looking clinical implication or call for future research.

Opening phrase: "In conclusion," is used by approximately half the papers. Others transition directly to the concluding statement.

Exemplar concluding paragraphs:
- "In conclusion, this study demonstrated that using rtCGM for 30 days in people with T2D and ESKF undergoing hemodialysis resulted in improved TIR and TAR. CGM should be considered an improved technological option for glycemic monitoring in this population, moving beyond the unreliable, but widely used HbA1c testing and the limited CBG testing approach." (Galindo).
- "To conclude, we present an ML-based approach to detect hypoglycemia from voice, potentially complementing current detection methods and improving self-management of people with diabetes in the future." (Lehmann).
- "This study demonstrates the feasibility and accuracy of using NLP to extract glucose data from existing CGM reports stored as PDF files, offering significant implications for clinical practice and diabetes research." (Zheng).
- "In conclusion, the findings of this study provide population references for the percentage of time across a variety of glycemic ranges in adults without diabetes..." (Godneva).

## Signature moves across the section

1. **No "Discussion" heading**: The heading is always CONCLUSIONS, even though the section contains full discussion content.

2. **"In conclusion" for the final paragraph**: Approximately half the papers use "In conclusion," to open the final paragraph, distinguishing it from the preceding discussion material.

3. **ADA Standards integration**: Findings are routinely connected to current ADA clinical recommendations.

4. **Hedging language**: "may", "could", "suggests", "one possible explanation", "we hypothesized". Observational studies never use causal verbs.

5. **Clinical translation**: Findings are translated to clinical significance: "a number needed to treat of 49 to prevent one death event over 4 years" (Reaven).

6. **Future work**: Many papers end with a forward-looking sentence: "Future studies with a larger sample size should determine whether improvements in glycemia... correlate with improved clinical outcomes." (Galindo).

## Anti-patterns

- Using "DISCUSSION" as the section heading (must be "CONCLUSIONS").
- Starting with a mechanism or interpretation before restating the principal findings.
- Using causal language ("our study proves", "CGM reduced mortality") for observational data. Use "was associated with" or "may".
- Including new analyses or results not presented in the Results section.
- Writing limitations as a single run-on sentence rather than listing specific limitations.
- Omitting the explicit design name from the concluding paragraph.
- Overstating clinical implications for null-result studies.
- Failing to connect findings to ADA Standards of Care when relevant.
- Using "In summary" or "In conclusion" at the start of a paragraph that is not the final concluding paragraph.
