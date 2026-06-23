# JAMA Portfolio - Exemplar References

Verified, real exemplar papers in the JAMA family (and adjacent top clinical
journals) that this manuscript can model on. Each entry says what we borrow:
the primary-claim framing, a display pattern, or the section structure.

RULE: store ONLY real, verifiable papers (DOI / PMID where possible). Never
fabricate a citation. Re-verify with `citation-audit` before any of these enters
the manuscript bibliography.

## Search categories

1. Physician characteristics / behavior and opioid (or general) prescribing.
2. Physician-to-physician variation in opioid prescribing.
3. Patient online reviews or NLP / LLM applied to physician behavior, quality, or prescribing.
4. Two-part / hurdle models of prescribing or utilization in claims/EHR data.
5. Patient-satisfaction pressure and opioid prescribing.

## Verified references (DOI/PMID confirmed)

STYLE EXEMPLARS (imitate the writing) must be JAMA-family: rows 3, 6, 8 below, plus
the files in `../exemplars/`. All other rows are CITATION candidates only (adjacent
venues: NEJM, JMIR, AJHE, JABFM, ARPH), borrowed for design / method / evidence, NOT
for style imitation.

| # | Citation | DOI / PMID | Cat | What we borrow |
|---|---|---|---|---|
| 1 | Barnett ML, Olenski AR, Jena AB. "Opioid-Prescribing Patterns of Emergency Physicians and Risk of Long-Term Use." *N Engl J Med.* 2017;376(7):663-673. | 10.1056/NEJMsa1610524 · PMID 28199807 | 1, 2 | **ADJACENT (NEJM, not JAMA): citation + DESIGN template only, NOT a style exemplar.** The canonical design model: within-hospital physician-level prescribing-intensity variation in **Medicare claims**, long-term use as outcome (aOR 1.30). Borrow the physician-as-quasi-random framing and intensity-quartile exposure (design, not prose). |
| 2 | Schnell M, Currie J. "Addressing the Opioid Epidemic: Is There a Role for Physician Education?" *Am J Health Econ.* 2018;4(3):383-410. | 10.1162/ajhe_a_00113 (NBER w23645) | 1 | A measurable physician attribute (training quality / med-school rank) predicts opioid prescribing. Borrow: framing a physician trait as the explanatory variable. |
| 3 | Gray BM, Vandergrift JL, Gao G, McCullough JS, Lipner RS. "Website Ratings of Physicians and Their Quality of Care." *JAMA Intern Med.* 2015;175(2):291-293. | 10.1001/jamainternmed.2014.6291 | 3 | Links **online physician review-site ratings** to objective quality measures. Borrow: "online patient ratings as a physician-level signal," cautious-association tone, and precedent that review/IS-style data appears in JAMA IM. |
| 4 | Carrico JA, Mahoney K, Raymond KM, et al. "The Association of Patient Satisfaction-Based Incentives with Primary Care Physician Opioid Prescribing." *J Am Board Fam Med.* 2018;31(6):941-943. | 10.3122/jabfm.2018.06.180067 · PMID 30413550 | 5 | Satisfaction pressure -> opioid prescribing (incentivized PCPs 3x more likely to report satisfaction-driven prescribing). Borrow: the satisfaction-pressure mechanism that motivates why a patient-perceived "agreeableness" trait would push prescribing up. Research-letter format. |
| 5 | Deb P, Norton EC. "Modeling Health Care Expenditures and Use." *Annu Rev Public Health.* 2018;39:489-505. | 10.1146/annurev-publhealth-040617-013517 · PMID 29328879 | 4 | Canonical methods reference for **two-part / hurdle models** (extensive = any use vs intensive = level given use). Borrow: cite to justify the participation-vs-intensity specification. |
| 6 | Schroeder AR, Dehghan M, Newman TB, Bentley JP, Park KT. "Association of Opioid Prescriptions From Dental Clinicians for US Adolescents and Young Adults With Subsequent Opioid Use and Abuse." *JAMA Intern Med.* 2019;179(2):145-152. | 10.1001/jamainternmed.2018.5419 | 1 | **JAMA IM style template (our target outlet).** Prescriber-exposure -> downstream opioid outcome in a matched claims cohort; the "Association of [exposure] With [outcome] Among [population]" title, structured abstract, STROBE flow. Borrow the title pattern and the associational framing directly. (verified via JAMA Network 2026-06-23) |
| 7 | Madanay F, Tu K, Campagna A, Davis JK, Doerstling SS, Chen F, Ubel PA. "Classification of Patients' Judgments of Their Physicians in Web-Based Written Reviews Using Natural Language Processing: Algorithm Development and Validation." *J Med Internet Res.* 2024;26:e50236. | 10.2196/50236 | 3 | **ADJACENT (JMIR, not JAMA): methods citation only, NOT a style exemplar.** Fine-tuned RoBERTa on Healthgrades reviews to classify physician interpersonal manner vs technical competence (90% acc). Borrow: precedent that physician attributes are extractable from reviews by NLP; cite in Methods to support the LLM measure. Open access. (verified via JMIR 2026-06-23) |
| 8 | Burns ML, Hilliard P, Vandervest J, et al. "Variation in Intraoperative Opioid Administration by Patient, Clinician, and Hospital Contribution." *JAMA Netw Open.* 2024;7(1):e2351689. | 10.1001/jamanetworkopen.2023.51689 | 1, 2 | **JAMA-FAMILY STYLE EXEMPLAR (JAMA Network Open, open access).** Decomposes opioid-administration variation into clinician / hospital / patient via ICCs. Borrow the structured-abstract format, the cohort-study voice, and the clinician-contribution-to-variation framing. Seeded in `../exemplars/burns-2024-jamanetworkopen-opioid-variation.md`. (verified via JAMA Network 2026-06-23) |

## To confirm before citing (UNVERIFIED: run PubMed / citation-audit first)

| # | Citation | Note | Cat |
|---|---|---|---|
| 9 | Schwartz TM, Tai M, Babu KM, Merchant RC. "Lack of Association Between Press Ganey ED Patient Satisfaction Scores and ED Administration of Analgesic Medications." *Ann Emerg Med.* 2014;64(5):469-481. | PMID/pages UNVERIFIED. Useful as counter-evidence (field debates the satisfaction->analgesic link). Adjacent venue. | 5 |
| 10 | Khanbhai M, Anyadi P, Symons J, et al. "Applying NLP and machine learning techniques to patient experience feedback: a systematic review." *BMJ Health Care Inform.* 2021;28(1):e100262. | DOI 10.1136/bmjhci-2020-100262 · PMID 33653690: author list UNVERIFIED. Methods anchor; adjacent venue. | 3 |

## Coverage gaps (useful for positioning)

- **Category 3 is partially filled**: Madanay 2024 (row 7, JMIR) is a verified NLP-from-reviews precedent (RoBERTa on Healthgrades classifying interpersonal manner vs competence). But it sits in JMIR, not a clinical venue, and classifies judgment categories rather than a Big-Five *trait*. So the specific gap remains: no verified JAMA-family paper derives a physician *personality trait* from reviews (Gray 2015 uses star ratings, not NLP). That gap is the paper's measurement novelty, but for THIS paper the LLM measure stays the enabler (other ProjB papers own the method; see `_venue/playbook-clinical-medicine`).
- **Category 4**: Deb & Norton is a methods review, not an applied opioid two-part model. An applied exemplar (e.g. Sacks et al., "Primary care providers' influence on opioid use," *J Public Econ* 2023) surfaced but is UNVERIFIED.

## Recent physician-online-review literature (recency anchors; adjacent venues)

The online-review / NLP-on-reviews angle is recent (2024-2025) but lives in JMIR /
informatics, NOT the JAMA family. Cite these to anchor recency in related work (as the
measurement enabler, not as JAMA style exemplars):

- Madanay et al. 2024, *J Med Internet Res* 26:e50236 (10.2196/50236) - RoBERTa on
  Healthgrades, interpersonal manner vs competence (row 7). Verified.
- Feizollah A, Lin CY, O'Malley L, Thompson W, Listl S, Byrne M. "The Use of Natural
  Language Processing to Interpret Unstructured Patient Feedback on Health Services:
  Scoping Review." *J Med Internet Res.* 2025;27:e72853 (10.2196/72853). Open access;
  verified 2026-06-23. Current scoping review of NLP on patient feedback.
- "Patients Speak, AI Listens: LLM-based Analysis of Online Reviews ..." arXiv
  2503.20981 (2025). UNVERIFIED preprint; recent LLM-from-reviews method (urgent care).
- Nearest recent JAMA-family touchpoint: "Public Perception of Physicians Who Use
  Artificial Intelligence," *JAMA Netw Open* 2025 (article 2836557) - tangential
  (perception of AI, not review-NLP). UNVERIFIED.

## Status

- Populated 2026-06-22 by a lit-search agent (web / Semantic Scholar). Rows 1-8 verified (rows 6-8 added 2026-06-23 via web + DOI confirm); rows 9-10 still need PubMed / citation-audit. Run `citation-audit` before any enters the manuscript.
- JAMA-family STYLE exemplars = rows 3 (Gray, JAMA IM), 6 (Schroeder, JAMA IM), 8 (Burns, JAMA Netw Open). The rest are citation-only (adjacent venues).
- 2026-06-23: stored real JAMA-family exemplars in `../exemplars/`: Schroeder 2019 (JAMA IM, row 6, PDF) and Burns 2024 (JAMA Netw Open, row 8, PDF); plus 2 more JAMA Network Open Original Investigations as full-text XML (2026 articles have no render-PDF yet): Kim et al. "Shifts in Antipsychotic Prescribing by Clinician Type for Medicare Part D Beneficiaries" (10.1001/jamanetworkopen.2026.3410) and Witt et al. "Association Between Peer Comparison Feedback and Hospitalist Antibiotic Prescribing" (10.1001/jamanetworkopen.2026.9504). Gray 2015 (row 3) is not in PMC, needs institutional access. Barnett (NEJM) / Madanay (JMIR) stay citation-only (adjacent venues).
