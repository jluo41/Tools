# JAMA Internal Medicine -- Abstract Style Guide

Distilled from 11 JAMA IM original investigations (Williams 2025, Desai 2026, Kurlander 2026, Fournier 2026, Hirshberg 2025, Berkowitz 2025, Boone 2026, Seamans 2018, Wen 2020, Taylor 2025, Kroenke 2015, Masterson 2025, Zhang 2026).

## Word budget

- Abstract body: 250-350 words (slightly shorter than JAMA flagship; some observational papers run as lean as 250).
- Key Points box: 3 labeled items, ~80-120 words total.
- The abstract is strictly structured; unstructured prose is never accepted.

## Structured abstract headings (in order)

1. **IMPORTANCE** -- one to two sentences. Clinical problem + knowledge gap.
2. **OBJECTIVE** -- one sentence starting with "To [verb]..."
3. **DESIGN, SETTING, AND PARTICIPANTS** (sometimes "DESIGN, SETTINGS, AND PARTICIPANTS") -- names the study design, data source, population, dates.
4. **EXPOSURES** or **INTERVENTIONS** (observational vs trial) -- one to two sentences. For trials, also separate **INTERVENTIONS** heading.
5. **MAIN OUTCOMES AND MEASURES** -- one to two sentences defining the primary outcome.
6. **RESULTS** -- sample size with demographics, then primary result with effect size and 95% CI, then key secondary results.
7. **CONCLUSIONS AND RELEVANCE** -- one to two sentences, cautious wording.
8. **TRIAL REGISTRATION** (trials only) -- ClinicalTrials.gov Identifier.

### Contrast with JAMA flagship

JAMA IM uses the same heading set as JAMA flagship. The main differences are:
- JAMA IM abstracts tend to be slightly shorter (many run 280-350 words vs JAMA flagship ~350).
- JAMA IM more commonly uses "EXPOSURE" (singular) for single-exposure observational studies.
- JAMA IM observational papers often have shorter DESIGN blocks (one long sentence vs two).
- JAMA IM trials are more likely to include TRIAL REGISTRATION as a final abstract element.
- JAMA IM sometimes uses sub-labels: "Original Investigation | LESS IS MORE" (deprescribing/stewardship), "Original Investigation | HEALTH EQUITY" (disparities/food insecurity), "Original Investigation | AI AND CLINICAL CARE" (LLM/AI studies), "Original Investigation | AGING AND HEALTH". These shape the framing but not the abstract structure.

## Key Points box

Appears above the abstract on the first page. Three labeled one-liners:

- **Question**: One interrogative sentence. Pattern: "Is [exposure] associated with [outcome]?" or "Does [intervention] [verb] [outcome] compared with [comparator]?" or "What is the [association/effect] of [X] on [Y]?"
- **Findings**: "In this [design] [of/including/analyzing] [N] [population], [main result with numbers]." Always names the design and N. Always includes the direction and magnitude of the primary finding.
- **Meaning**: One sentence, cautious. Pattern: "These findings suggest that..." or "This study suggests that..." or "Results of this study suggest that..." Never uses causal language for observational designs.

### Exemplar Key Points

Seamans 2018:
> **Question** Is prescription opioid use in one household member associated with increased risk of prescribed opioid use in other household members?
> **Findings** In a study comparing 12 695 280 commercial insurance beneficiaries with a household member who started a new prescription of opioids, to 6 359 639 beneficiaries with a household member who started a new prescription of nonopioid pain relievers, the 1-year risk of subsequent opioid use was 0.71% higher among individuals exposed to opioids through a household member's prescription.
> **Meaning** Prescription opioid use may spread within households.

Zhang 2026:
> **Question** Is reduced time pressure in primary care visits associated with care pattern changes in care comprehensiveness and quality?
> **Findings** In this cross-sectional study of 191 269 primary care visits across 311 physicians in an integrated health system, reduced time pressure visits included more diagnoses documented, more new prescriptions prescribed, and more diagnostic testing and similar preventive care (eg, immunizations) compared with regular time pressure visits.
> **Meaning** Results of this study suggest that reducing time pressure in primary care may modestly increase in the scope of issues addressed, particularly for patients with medical complexity.

## Arc

```
IMPORTANCE: burden + gap (1-2 sentences)
    |
OBJECTIVE: "To [examine/determine/evaluate/compare]..." (1 sentence)
    |
DESIGN: "[Design name] [using/of] [data source]...[dates]" (1-3 sentences)
    |
EXPOSURE/INTERVENTION: what varied (1-2 sentences)
    |
OUTCOMES: primary outcome defined (1-2 sentences)
    |
RESULTS: N + demographics -> primary effect (CI) -> secondary (1 long block)
    |
CONCLUSIONS: cautious takeaway (1-2 sentences)
```

## Signature moves

1. **IMPORTANCE opener**: Leads with prevalence/cost/mortality, then pivots with "however" or "but" to the gap. Pattern: "[Condition] affects [N] people... However, [what is unknown]."
   - Seamans: "Increases in prescription opioid use in the United States have been attributed to changing prescribing guidelines and attitudes toward pain relief; however, the spread of opioid use within households through drug diversion may also be a contributing factor."
   - Taylor: "Sepsis survivors experience high morbidity and mortality after discharge, but health systems lack effective approaches to improve recovery."
   - Zhang: "Primary care physicians face increasing pressure to deliver complex care within fixed, short visit durations. Prior evidence links higher time pressure to lower-quality care, but the effects of reduced time pressure on care delivery are not well understood."

2. **OBJECTIVE infinitive**: Always starts with "To" + a single verb: examine, investigate, determine, evaluate, compare, assess.
   - "To investigate whether individuals living in a household with a prescription opioid user are more likely to initiate prescription opioids themselves" (Seamans).
   - "To evaluate the effect of a sepsis transition and recovery (STAR) program compared with usual care on postdischarge outcomes" (Taylor).
   - "To compare the effectiveness adding mobile integrated health (MIH) to a transitions of care coordinator for improving health status and reducing 30-day all-cause readmissions" (Masterson).

3. **RESULTS lead sentence**: Always opens with sample size and key demographics. Pattern: "Among [N] [participants/patients] (median [IQR] age, [X] [Y-Z] years; [N] [sex] [%])..."
   - "Among 2003 participants (median [IQR] age, 67 [58-78] years; 1040 female [52%])..." (Masterson).
   - "Of 3548 patients enrolled, 1843 (52%) were women, and the median (IQR) age was 68 (57-77) years" (Taylor).

4. **Effect reporting**: effect size in clinical units with 95% CI in parentheses, not p-values alone. Format: "adjusted [measure], [value]; 95% CI, [lower]-[upper]" or "(95% CI, [lower] to [upper])".
   - "risk difference of 0.71% (95% CI, 0.68%-0.74%)" (Seamans).
   - "adjusted odds ratio, 1.05; 95% CI, 0.90-1.24; P = .53" (Taylor).
   - "mean difference, 0.11; 95% CI, 0.08-0.15" (Zhang).

5. **CONCLUSIONS AND RELEVANCE**: Opens with the design recap + main finding restated. Then one sentence of clinical implication. Pattern: "[In this/This] [design], [finding]. [Implication sentence]."
   - "In this randomized clinical trial, a multicomponent, navigator-led STAR program did not reduce the composite of all-cause readmission and mortality at 90 days after discharge" (Taylor).
   - "This randomized clinical trial found that MIH conferred no additional benefit on health status or 30-day readmissions for postacute patients with heart failure compared to TOCC alone" (Masterson).

## Anti-patterns

- Starting IMPORTANCE with "This study..." (the study has not been introduced yet).
- Using causal language ("caused", "led to", "reduced") for observational designs in CONCLUSIONS. Use "was associated with" or "appears to be associated with".
- Reporting p-values without effect sizes and CIs.
- Burying the sample size deep in RESULTS rather than leading with it.
- Omitting the study design name from DESIGN (e.g., just saying "We used data from...").
- Writing CONCLUSIONS that go beyond what the data show (avoid "will" and "should" for observational data; use "may" and "suggest").
- Including subgroup results in the abstract when primary is null (unless prespecified and significant).

## Paragraph structure

The abstract is a single block under each heading, not multiple paragraphs. Each heading is followed by continuous text until the next heading.
