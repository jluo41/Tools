# Paper Architecture — MISQ2026 Personality-to-Opioid

**Version:** v03 (2026-06-08)
**Status:** All choices locked. Ready for writing.

## Configuration

| Field          | Value                                                                          |
|----------------|--------------------------------------------------------------------------------|
| Type           | Empirical (behavioral validation)                                              |
| Venue          | MISQ Research Article (55 pages max, double-spaced 12pt TNR)                   |
| C1 (60%)      | Behavioral validation — perceived agreeableness predicts opioid Rx in indep. claims |
| C2 (40%)      | LLM trait measurement + validation — self-contained (npj DM under review)      |
| Implications   | Monitoring, doctor-shopping, governance (discussion only, not contributions)    |
| Samples        | LBP N=746K (main) + VisitWithOpioid N=1.09M (broader, cross-sample attenuation)|
| Constraint     | IV = supplementary not causal; npj DM under review; no npj DM cite in paper    |

## Key Numbers

| Spec                    | Outcome                   |           Coeff |      p |
|-------------------------|---------------------------|----------------:|-------:|
| OLS trait_l2            | mme_ttl                   |           +8.88 | <0.001 |
| OLS trait_l5            | mme_ttl                   |          +12.68 | <0.001 |
| OLS trait_l2            | is_high_mme_daily (logit) |  +0.185 (OR1.20)| <0.001 |
| OLS trait_l2            | is_hdld (logit)           |  +0.046 (OR1.05)| <0.001 |
| OLS trait_l2            | is_high_mme_total (logit) |  +0.076 (OR1.08)| <0.001 |
| IV county_loo_zip       | mme_ttl                   |          +1,487 | <0.001 |
| IV county_loo_physician | mme_ttl                   |            +178 |  0.019 |

8/8 OLS specs p<0.001. 8/8 IV specs p<0.05.

## 5-Act Story Arc

1. **Gap:**       LLMs extract physician traits at scale; patients act on them. Do they predict REAL behavior? Unknown.
2. **Setup:**     Link perceived agreeableness (226K physicians) to Medicare opioid Rx (746K LBP + 1.09M broader).
3. **Discovery:** Strong positive in LBP (p<0.001 all outcomes). Broader attenuates — context-dependent.
4. **Mechanism:** Accommodation pathway — agreeable physicians prioritize rapport where guidelines are silent.
5. **Impact:**    LLM profiles are behavioral diagnostics. Enables monitoring but also doctor-shopping risk. Governance needed.

## Section Minimap — Main Body (~32 pages)

### §1 Introduction (4 pages, 6 paras)

| P | Role            | Content                                                                                |
|---|-----------------|----------------------------------------------------------------------------------------|
| 1 | 🧩 Puzzle        | Opioid Rx varies wildly; physician-level factors understudied                          |
| 2 | 🤖 Context       | LLMs are changing how patients choose physicians; trait profiles are de facto criteria  |
| 3 | ❓ Gap           | Do these algorithmically derived traits carry real behavioral signal? Untested          |
| 4 | 📐 This paper    | Link perceived agreeableness to Medicare opioid Rx: LBP (746K) + broader (1.09M)      |
| 5 | 📊 Preview       | LBP strong (p<0.001); broader attenuates; IV corroborates                              |
| 6 | 💡 Contributions | C1 behavioral validation + C2 LLM measurement. Discussion: monitoring + governance     |

Locked: B (broad framing — LLMs changing physician choice).

---

### §2 Literature Review (5 pages, 5 subsections)

| Sub  | Content                                         | Pages | Status                       |
|------|-------------------------------------------------|------:|------------------------------|
| §2.1 | Opioid variation + physician heterogeneity     |   1.5 | Keep                         |
| §2.2 | Big Five + agreeableness duality in healthcare |   1.0 | Keep                         |
| §2.3 | LLM trait extraction from text                 |   1.0 | Self-contained, no npj DM cite|
| §2.4 | Review platforms as data source                |   0.5 | Trim                         |
| §2.5 | Research gaps                                  |   1.0 | Sharpen: no one has linked LLM traits to independent behavior |

Locked: B-variant (self-contained LLM lit, no npj DM cite since unpublished).

---

### §3 Theoretical Framework (5 pages, 4 subsections)

| Sub  | Content                                                                        | Pages |
|------|--------------------------------------------------------------------------------|------:|
| §3.1 | Competing predictions: accommodation vs norm adherence                        |   1.0 |
| §3.2 | Accommodation pathway: empathic responsiveness, conflict avoidance, need      |   1.5 |
| §3.3 | LBP as max-ambiguity context (primary sample justification)                   |   1.5 |
| §3.4 | H1 (LBP association) + contextual prediction (broader attenuates) — testable |   1.0 |

Locked. Both samples make the theory fully testable.

---

### §4 LLM Trait Extraction (4 pages, 2 subsections)

Self-contained — reviewer cannot check npj DM. Full validation details in Appendix A+B.

**§4.1 Review Data & Pipeline (2 pages)**

| P | Role         | Content                                                               |
|---|--------------|-----------------------------------------------------------------------|
| 1 | 📄 Data       | 4 platforms, 587K physicians, 226K with 5-100 reviews, 4.1M reviews  |
| 2 | 🤖 Method     | Two LLM agents, chain-of-thought, 5-level anchored Likert            |
| 3 | 🏆 Selection  | 6 LLMs benchmarked; Gemini-2.5-Flash selected on cost-accuracy       |
| 4 | 🎯 Focus      | Agreeableness: highest cross-model consistency; trait_l2 (>=0.75)=49%|

**§4.2 Validation (2 pages)**

| P | Role            | Content                                                            |
|---|-----------------|--------------------------------------------------------------------|
| 5 | 🔬 Multi-model   | 1,197 physicians x 10 traits; MAE = 0.095 (details in Appendix B) |
| 6 | 👥 Human-rater   | 500 physicians; LLM-human consistency confirmed (details Appx B)   |
| 7 | 📊 Discriminant  | Traits != sentiment (partial r = 0.25, all p<0.001)               |
| 8 | 📊 Distribution  | Score distribution: Table 1                                        |
| 9 | 🔗 Bridge        | "§6 provides predictive validity against independent claims"       |

Locked. Trim P7/P9 if space tight; core is P1-P6 + P8.

---

### §5 Data & Variables (4 pages, 3 subsections)

| Sub  | Content                                                                         | Pages |
|------|---------------------------------------------------------------------------------|------:|
| §5.1 | CMS data sources: NPPES, PDE, Part A/B                                        |   1.0 |
| §5.2 | Data construction: LBP N=746K + broader N=1.09M, 1st-pair, af14d, exclusions |   2.0 |
| §5.3 | Control variables: physician + patient + area + FE (details in Appendix C)    |   1.0 |

Locked. Both samples described. Variable details → Appendix C.

---

### §6 Empirical Analysis (4 pages, 4 subsections)

| Sub  | Role             | Content                                                   | Table   | Pages |
|------|------------------|-----------------------------------------------------------|---------|------:|
| §6.1 | 📊 Main          | LBP OLS: 5 nested specs, trait_l2/l5, 4 outcomes, p<0.001| Table 3 |   1.5 |
| §6.2 | 🔀 Cross-sample  | Broader attenuates — descriptive side-by-side             | Table 4 |   1.0 |
| §6.3 | 📐 IV            | County-peer, F=63 (robust), 1st+2nd stage tables, LATE   | Table 5 |   1.0 |
| §6.4 | 🛡️ Robustness    | Summary + refs to Appendix D (IV clustered) + E (alts)   |    —    |   0.5 |

Locked: §6.2 = A (descriptive), §6.3 = B (moderate with tables).
Full IV clustered SEs → Appendix D. Alternative thresholds/windows → Appendix E.

---

### §7 Discussion (4 pages, 4 subsections)

| Sub  | Role             | Content                                                                | Pages |
|------|------------------|------------------------------------------------------------------------|------:|
| §7.1 | 📊 Interpretation | LBP accommodation + broader attenuation + IV direction consistent     |   1.0 |
| §7.2 | 💡 Theoretical    | LLM traits as behavioral signal; accommodation + discretion; IS angle |   1.0 |
| §7.3 | 🔧 Practical      | (a) monitoring, (b) doctor-shopping (1 para), (c) system redesign    |   1.0 |
| §7.4 | 🛡️ Limitations    | IV robust vs clustered, perception != personality, single trait, x-sec|   1.0 |

Locked: §7.3 = A (doctor-shopping brief, 1 para as implication + future work).

---

### §8 Conclusion (1 page, 6 sentences)

| P | Role              | Content                                                                  |
|---|-------------------|--------------------------------------------------------------------------|
| 1 | 📊 Main finding    | LLM-derived perceived agreeableness predicts opioid Rx in indep. claims |
| 2 | 📐 Key number      | +8.88 MME (p<0.001), 746K LBP encounters                               |
| 3 | 🔀 Context effect  | Broader sample attenuates — trait effects concentrate where discretion high |
| 4 | 🛡️ Corroboration   | IV corroborates with directionally consistent estimates                  |
| 5 | 💡 Contribution    | LLM-derived traits are a validated behavioral signal                     |
| 6 | ❓ Open question   | As LLMs mediate physician discovery, governing these signals is urgent   |

---

## Appendix Plan (~17 pages)

| App | Content                                                                            | Pages |
|-----|------------------------------------------------------------------------------------|------:|
| A   | LLM prompts: full Big Five + patient-oriented agent templates, scoring rubrics     |     4 |
| B   | LLM validation: multi-model comparison tables, human-rater agreement, score dists  |     3 |
| C   | Variable construction: physician, patient, prescription, control variable details  |     3 |
| D   | IV analysis: clustered SEs (all 3 instruments), first-stage diagnostics, alt specs |     3 |
| E   | Robustness: alternative thresholds, outcome windows (af7d vs af14d), trait forms   |     3 |
| F   | Extended literature: additional references for reviewer depth                      |     1 |

## Language Guide

**Use:** "associated with", "predicts", "patient-perceived agreeableness", "supplementary evidence", "directionally consistent", "behavioral signal"

**Avoid:** "causes", "causal effect", "physician personality", "our LLM framework", "strong instrument" (without qualifier), "surveillance"

## Page Budget Summary

| Component       | Pages |
|-----------------|------:|
| Main body       |    32 |
| Appendix        |    17 |
| References      |     4 |
| Buffer          |     2 |
| **Total**       |**55** |
