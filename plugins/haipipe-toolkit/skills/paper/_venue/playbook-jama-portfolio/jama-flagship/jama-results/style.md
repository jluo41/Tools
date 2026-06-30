# JAMA Flagship Results -- Section Style Guide

Extracted from JAMA Original Investigation exemplars. Supplements `style-profile.md`.

## Word budget

- 800-1,800 words. Results are detailed but purely factual. Length depends on the number of outcomes and subgroup analyses.
- Krebs (2018): ~1,600w. Mathioudakis (2025): ~1,200w. Cipriani (2026): ~1,400w. Rotenstein (2026): ~1,800w.
- Results sections use titled subsections (red subheadings in published format).

## Arc

```
participant flow + enrollment + completion (opening)
  -> baseline characteristics (reference Table 1)
  -> primary outcome (with exact numbers, CI, P)
  -> secondary outcomes (same format)
  -> adverse events / safety
  -> subgroup / sensitivity analyses
```

## Subsection headings (from exemplars)

### RCT pattern:
- (no heading for opening flow paragraph, or **Study Participants** [Mathioudakis], **Trial Population** [Cipriani])
- **Pain and Health Outcomes** [Krebs] / **Primary Analysis** [Mathioudakis] / **Treatment Discontinuation** [Cipriani]
- **Secondary Outcomes** [Mathioudakis, Cipriani: "Efficacy"]
- **Adverse Outcomes and Potential Misuse** [Krebs] / **Adverse Events** [Mathioudakis] / **Safety** [Cipriani]
- **Exploratory Analyses** [Mathioudakis]
- **Intervention Adherence and Retention** [Krebs]
- **Subgroup and Sensitivity Analyses** [Krebs]

### Observational pattern (Rotenstein 2026):
- **Sample Characteristics**
- **Unadjusted EHR Time Expenditure and Visit Volume**
- **Difference-in-Differences Estimates of Changes in EHR Time Expenditure and Visit Volume**
- **Difference-in-Differences Estimates by Clinician Group**
- **Estimated E/M Revenue Increases With AI Scribe Adoption**

## Signature moves

1. **Open with participant flow referencing the CONSORT Figure.** The first sentence of Results states how many were enrolled, randomized, and completed, referencing the flow diagram.
   - "Of 265 enrolled patients, 25 withdrew prior to randomization and 240 were randomized (Figure). Follow-up rates were 92% at 3 months... and 98% at 12 months (117 in each group)." [Krebs 2018]
   - "Among 427 individuals screened for eligibility, 368 adults met eligibility criteria, were randomized, and were included in the primary analysis (Figure 1). The Table and eTable 3 in Supplement 2 summarize baseline characteristics..." [Mathioudakis 2025]
   - "Of the 520 eligible participants, 493 were included in the primary analysis (median age, 35 [IQR, 25 to 48] years; 300 [58%] were female)." [Cipriani 2026]
   - "The sample included 8581 clinicians, including 1809 clinicians who adopted AI scribes and 6772 clinicians who did not adopt AI scribes over 181 273 clinician-month observations (Table)." [Rotenstein 2026]

2. **Baseline characteristics described in text with Table reference.** After the flow, one paragraph summarizes demographics: "Mean age was [X] years... [N] ([%]) were women (Table 1)."
   - "Mean age was 58.3 years (range, 21-80) and 32 patients (13.0%) were women (Table 1). For primary pain diagnosis, 156 patients (65%) had back pain and 84 patients (35%) had hip or knee osteoarthritis pain." [Krebs 2018]
   - "Participants had a median (IQR) age of 58 (50-65) years and 70.7% were female, 27.2% were Black, 5.4% were Hispanic, and 61.0% were white." [Mathioudakis 2025]

3. **Primary outcome stated with the full statistical package.** The primary result sentence states: group means or proportions, the between-group difference, 95% CI, and P value. This is the most important sentence in the paper.
   - "There was no significant difference in pain-related function between the 2 groups over 12 months (overall P = .58). At 12 months, mean BPI interference was 3.4 in the opioid group (SD, 2.5) vs 3.3 in the nonopioid group (SD, 2.6); difference, 0.1 (95% CI, -0.5 to 0.7)." [Krebs 2018]
   - "The primary end point of achievement of a composite... was achieved by 31.8% of participants overall, with 58 of 183 participants (31.7%) in the AI-led DPP group and 59 of 185 participants (31.9%) in the human-led DPP group. The risk difference was -0.2% (1-sided 95% CI: -8.2%; Figure 2), demonstrating that the AI-led DPP intervention met the noninferiority margin of -15.0%." [Mathioudakis 2025]
   - "Of the 241 participants in the PETRUSHKA group, 41 (17%) discontinued their antidepressant at 8 weeks due to any cause (primary outcome) compared with 69 of 252 participants (27%) in the usual care group (adjusted RR, 0.62 [95% CI, 0.44-0.88]; P = .007)." [Cipriani 2026]
   - "AI scribe adoption was associated with 13.4 (95% CI, 9.1-17.7) fewer minutes of EHR time, 16.0 (95% CI, 13.7-18.3) fewer minutes of documentation time, and 0.49 (95% CI, 0.17-0.81) additional weekly visits delivered." [Rotenstein 2026]

4. **Secondary outcomes follow the same format, sometimes with explicit null statement.** Null results are stated plainly: "did not significantly differ," "was not statistically significant."
   - "Health-related quality of life did not significantly differ between the 2 groups (physical health overall: P = .23; ... mental health overall: P = .40)." [Krebs 2018]
   - "Electronic health record time outside work hours did not change significantly." [Rotenstein 2026]

5. **Figure and Table references are woven inline.** Every table and figure is referenced in the text at the point where its data are discussed. Format: "(Table 2)" or "(Figure 1)" or "(Figure 3 and eTable 14 in Supplement 2)."

6. **Subgroup and sensitivity results stated concisely.** Often formatted as: "Results were consistent in sensitivity analyses" or "Similar results were seen in sensitivity analyses that sequentially excluded each study site."

## Exemplar sentences (shape, not content)

**Participant flow opener**:
- "Of [N] enrolled [patients/participants], [n] [withdrew/were excluded] and [N'] were [randomized/included] (Figure [X])." [general pattern]

**Baseline demographics**:
- "Mean age was [X] years (range/SD, [Y]) and [N] ([%]) were [sex] (Table 1)." [general pattern]

**Primary outcome**:
- "[Outcome] was [X] in the [intervention group] (SD, [Y]) vs [Z] in the [control group] (SD, [W]); difference, [D] (95% CI, [L] to [U])." [general pattern for continuous]
- "[N] of [N'] participants ([%]) in the [group] [achieved/experienced outcome] compared with [n] of [n'] ([%]) in the [other group] (adjusted [RR/OR], [X] [95% CI, [L]-[U]]; P = [value])." [general pattern for binary]

**Null result**:
- "[Outcome] did not significantly differ between the 2 groups (overall P = [value]; difference at [time], [D] [95% CI, [L] to [U]])." [general pattern]

## Anti-patterns

- Do NOT interpret results in the Results section. Save "this suggests" or "consistent with" for Discussion.
- Do NOT report results without CI and P. Every primary/secondary outcome needs the full statistical package.
- Do NOT skip the participant flow. It is always the opening of Results.
- Do NOT describe a table/figure without referencing it by name: "(Table 1)," "(Figure 2)."
- Do NOT use causal language. Results are descriptive: "was associated with," "was observed," "occurred."
- Do NOT report subgroup results without stating whether the interaction test was significant.
- Do NOT combine favorable and unfavorable results in one sentence. State each result separately with its own statistics.

## Paragraph structure

| Block | Paragraphs | Job |
|-------|-----------|-----|
| Participant flow | 1-2 | Screened, enrolled, randomized, completed, referenced to flow figure |
| Baseline | 1 | Demographics summary, reference to Table 1 |
| Primary outcome | 1-2 | Main result with full statistics, reference to results table/figure |
| Secondary outcomes | 1-3 | Each secondary outcome stated, with nulls reported plainly |
| Adverse events | 1-2 | Safety data, serious adverse events |
| Subgroup/sensitivity | 1-2 | Consistency or variation across subgroups |
