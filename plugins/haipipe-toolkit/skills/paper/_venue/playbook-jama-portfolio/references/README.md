# JAMA Playbook - Exemplar References

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

## Exemplars (verified: authors + journal + year + DOI/PMID confirmed)

| # | Citation | DOI / PMID | Cat | What we borrow |
|---|---|---|---|---|
| 1 | Barnett ML, Olenski AR, Jena AB. "Opioid-Prescribing Patterns of Emergency Physicians and Risk of Long-Term Use." *N Engl J Med.* 2017;376(7):663-673. | 10.1056/NEJMsa1610524 · PMID 28199807 | 1, 2 | The canonical model for our design: within-hospital physician-level prescribing-intensity variation in **Medicare claims**, long-term use as outcome (aOR 1.30). Borrow the physician-as-quasi-random framing, intensity-quartile exposure, and the NEJM observational-claims IMRAD shape. |
| 2 | Schnell M, Currie J. "Addressing the Opioid Epidemic: Is There a Role for Physician Education?" *Am J Health Econ.* 2018;4(3):383-410. | 10.1162/ajhe_a_00113 (NBER w23645) | 1 | A measurable physician attribute (training quality / med-school rank) predicts opioid prescribing. Borrow: framing a physician trait as the explanatory variable. |
| 3 | Gray BM, Vandergrift JL, Gao G, McCullough JS, Lipner RS. "Website Ratings of Physicians and Their Quality of Care." *JAMA Intern Med.* 2015;175(2):291-293. | 10.1001/jamainternmed.2014.6291 | 3 | Links **online physician review-site ratings** to objective quality measures. Borrow: "online patient ratings as a physician-level signal," cautious-association tone, and precedent that review/IS-style data appears in JAMA IM. |
| 4 | Carrico JA, Mahoney K, Raymond KM, et al. "The Association of Patient Satisfaction-Based Incentives with Primary Care Physician Opioid Prescribing." *J Am Board Fam Med.* 2018;31(6):941-943. | 10.3122/jabfm.2018.06.180067 · PMID 30413550 | 5 | Satisfaction pressure -> opioid prescribing (incentivized PCPs 3x more likely to report satisfaction-driven prescribing). Borrow: the satisfaction-pressure mechanism that motivates why a patient-perceived "agreeableness" trait would push prescribing up. Research-letter format. |
| 5 | Deb P, Norton EC. "Modeling Health Care Expenditures and Use." *Annu Rev Public Health.* 2018;39:489-505. | 10.1146/annurev-publhealth-040617-013517 · PMID 29328879 | 4 | Canonical methods reference for **two-part / hurdle models** (extensive = any use vs intensive = level given use). Borrow: cite to justify the participation-vs-intensity specification. |

## To confirm before citing (UNVERIFIED: run PubMed / citation-audit first)

| # | Citation | Note | Cat |
|---|---|---|---|
| 6 | Schwartz TM, Tai M, Babu KM, Merchant RC. "Lack of Association Between Press Ganey ED Patient Satisfaction Scores and ED Administration of Analgesic Medications." *Ann Emerg Med.* 2014;64(5):469-481. | PMID/pages UNVERIFIED. Useful as counter-evidence (field debates the satisfaction->analgesic link). | 5 |
| 7 | Khanbhai M, Anyadi P, Symons J, et al. "Applying NLP and machine learning techniques to patient experience feedback: a systematic review." *BMJ Health Care Inform.* 2021;28(1):e100262. | DOI 10.1136/bmjhci-2020-100262 · PMID 33653690: author list UNVERIFIED. Methods anchor for NLP on free-text patient feedback. | 3 |

## Coverage gaps (useful for positioning)

- **Category 3 is sparse**: no verified JAMA-family paper applies an LLM/NLP to online reviews to derive a physician *trait*. In the wider literature this is genuinely thin (Gray 2015 uses ratings, not NLP): i.e. the measurement angle is uncommon in clinical venues. (For THIS paper the LLM measure is still treated as the enabler, since other ProjB papers own the method; see `_venue/playbook-clinical-medicine`.)
- **Category 4**: Deb & Norton is a methods review, not an applied opioid two-part model. An applied exemplar (e.g. Sacks et al., "Primary care providers' influence on opioid use," *J Public Econ* 2023) surfaced but is UNVERIFIED.

## Status

- Populated 2026-06-22 by a lit-search agent (web / Semantic Scholar). Rows 1-5 verified; rows 6-7 need confirmation.
