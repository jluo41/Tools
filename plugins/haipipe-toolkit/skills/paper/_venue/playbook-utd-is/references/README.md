# UTD-IS Playbook - Exemplar References

Verified, real exemplar papers in MISQ, ISR, and MS-IS (and adjacent top IS
journals) that this manuscript can model on. Each entry says what we borrow: the
contribution framing, a display or identification pattern, or the section structure.

RULE: store ONLY real, verifiable papers (DOI where possible). Never fabricate a
citation. Re-verify with `citation-audit` before any of these enters the manuscript
bibliography. Tag each entry with its journal (MISQ / ISR / MS-IS) so a chosen venue
pulls the matching exemplars.

## Search categories

1. Foundational IS theory in the paper's domain (the constructs and mechanisms it
   builds on); for MS-IS, foundational IT-economics / platform-economics work.
2. Theory-driven empirics with a comparable method and (for ISR/MS-IS) identification
   strategy (DiD / IV / RD / matching / natural experiment).
3. Design-science exemplars (MISQ, if the paper is design science); computational/
   ML-for-IS exemplars (ISR/MS-IS, if ML answers an IS question); analytical-model
   exemplars (MS-IS, if theory-led or hybrid model + empirics).

## Entries

Seeded from the verified bibliography of `Paper-Personality2Opioid-MISQ2026` (an
in-flight MISQ paper on LLM-perceived physician traits and prescriptions). Each is a
real, in-domain top-IS paper. The starred three are also stored as full-text style
exemplars in `../exemplars/`.

| key | cite | journal | borrowed for |
|---|---|---|---|
| `liu2021assessing` ⭐ | Liu, Li & Xu (2021), MISQ. *Assessing the Unacquainted: Inferred Reviewer Personality and Review Helpfulness.* DOI 10.25300/MISQ/2021/14375 | MISQ | Near-twin: Big-Five inferred from text via deep learning, then linked to an outcome. Contribution framing where the ML measure is an **enabler**, not the claim; "what we do / what is new / how" intro move; mechanism-then-Hn hypothesis phrasing. |
| `brynjolfsson2016crowd` | Brynjolfsson, Eggers & Gannamaneni (2016), MISQ. *Crowd-Squared: Amplifying the Predictive Power of Search Trend Data.* | MISQ | Computational-measure-from-data framing in a MISQ register; how a data-science method is positioned as IS contribution. |
| `adamopoulos2018impact` | Adamopoulos, Ghose & Todri (2018), ISR. *The Impact of User Personality Traits on Word of Mouth: Text-Mining Social Media Platforms.* | ISR | Personality text-mined -> behavioral outcome; ISR theory -> hypotheses -> evidence chain on social text. |
| `saifee2020online` | Saifee, Zheng, Bardhan & Lahiri (2020), ISR. *Are Online Reviews of Physicians Reliable Indicators of Clinical Outcomes? A Focus on Chronic Disease Management.* | ISR | Domain anchor: online physician reviews vs. clinical outcomes; how reviews-as-signal is positioned for IS. |
| `yang2023getting` | Yang, Lau & Abbasi (2023), ISR. *Getting Personal: A Deep Learning Artifact for Text-Based Measurement of Personality.* | ISR | Methodological-IS framing of a deep-learning personality measure; how a measurement artifact is validated as an IS contribution. |
| `lu2018can` | Lu & Rui (2018), Management Science. *Can We Trust Online Physician Ratings? Evidence from Cardiac Surgeons in Florida.* | MS-IS | MS-IS empirical health-IT exemplar: online ratings reliability with clean identification + a managerial/policy implication. |

Provenance: harvested 2026-06-24 from `0-Personality-Opioid-MISQ2026.bib`; the three
starred entries cross-checked against the stored PDFs. Re-verify with `citation-audit`
before any enters a NEW manuscript bibliography.

Coverage note: this first batch seeds MISQ/ISR; the corpus below adds the MS-IS slot.
Foundational IS work (DeLone & McLean, Venkatesh, Orlikowski, Walsham) should still
appear for MISQ/ISR when relevant; foundational platform / IT-economics work for MS-IS.

## Gao & Agarwal corpus (from discovery S01, 2026-06-24)

Verified corpus of Guodong (Gordon) Gao and Ritu Agarwal, the senior co-authors on this
project's sibling work (Luo et al. 2025). Source: `examples/ProjB-PhyTrait-OpioidRx/
discoveries/S01_is-venue-author-corpus/01_gao-agarwal-healthit-reviews/` (S-ids there).
`⭐` = also an exemplar candidate (fetch the PDF into `../exemplars/<journal>/`; see the
fetch-list in `../exemplars/README.md`). 18/20 VERIFIED with DOI; 2 NEEDS-VERIFICATION.

| cite (DOI) | journal | borrowed for |
|---|---|---|
| ⭐ Gao, Greenwood, McCullough & Agarwal (2015). *Vocal Minority and Silent Majority...* 10.25300/MISQ/2015/39.3.03 | MISQ | The field reference on whether online physician ratings are valid/representative; closest anchor. |
| ⭐ Goh, Gao & Agarwal (2016). *The Creation of Social Value... Online Health Community.* 10.25300/MISQ/2016/40.1.11 | MISQ | Theory-forward digital-health "social value" contribution structure. |
| ⭐ Agarwal & Karahanna (2000). *Time Flies When You're Having Fun: Cognitive Absorption...* 10.2307/3250951 | MISQ | Canonical MISQ construct -> belief -> prediction prose. |
| Angst & Agarwal (2009). *Adoption of EHR in the Presence of Privacy Concerns (ELM).* 10.2307/20650295 | MISQ | Individual-level persuasion mechanism; EHR adoption. |
| ⭐ Goh, Gao & Agarwal (2011). *Evolving Work Routines: Adaptive Routinization of IT in Healthcare.* 10.1287/isre.1110.0365 | ISR | Clinician-behavior / provider-discretion framing. |
| Agarwal, Gao, DesRoches & Jha (2010). *The Digital Transformation of Healthcare.* 10.1287/isre.1100.0327 | ISR | Near-mandatory "why health-IS matters" intro cite. |
| Anderson & Agarwal (2011). *The Digitization of Healthcare... Willingness to Disclose.* 10.1287/isre.1100.0335 | ISR | Why patients disclose / write reviews (data-generation framing). |
| Agarwal & Prasad (1998). *Personal Innovativeness in the Domain of IT.* 10.1287/isre.9.2.204 | ISR | Foundational individual-TRAIT cite (resonates with physician traits). |
| Agarwal & Dhar (2014). *Editorial: Big Data, Data Science, and Analytics.* 10.1287/isre.2014.0546 | ISR | Methods-legitimacy cite for ML/LLM text mining in IS. |
| ⭐ Shukla, Gao & Agarwal (2020). *How Digital Word-of-Mouth Affects Consumer Decision Making: Doctor Appointment Booking.* 10.1287/mnsc.2020.3604 | MS-IS | **Fills the empty ms-is exemplar slot**; reviews -> behavior identification (parallel to reviews -> prescribing). |
| ⭐ Wang, Gao & Agarwal (2023). *Friend or Foe? Teaming Between AI and Workers...* 10.1287/mnsc.2021.00588 | MS-IS | AI-in-healthcare-work exemplar. |
| ⭐ Angst, Agarwal, Sambamurthy & Kelley (2010). *Social Contagion and IT Diffusion: EMR Adoption...* 10.1287/mnsc.1100.1183 | MS-IS | Adoption/diffusion identification. |
| Gao, McCullough, Agarwal & Jha (2012). *A Changing Landscape... Online Ratings Over 5 Years.* 10.2196/jmir.2003 | JMIR | Earliest mapping of the exact data object (reviews over time). |
| Yaraghi, Wang, Gao & Agarwal (2018). *How Online Quality Ratings Influence Patients' Choice (controlled exp).* 10.2196/jmir.8986 | JMIR | Reviews causally shift patient choice (demand-side analog). |
| Wang, Luo, Dugas, Gao, Agarwal & Werner (2022). *Recency of Online Physician Ratings.* 10.1001/jamainternmed.2022.2273 | JAMA Intern Med | Data-quality caveat; includes this project's author Junjie Luo. |
| Gray, Vandergrift, Gao, McCullough & Lipner (2015). *Website Ratings of Physicians and Their Quality of Care.* 10.1001/jamainternmed.2014.6291 | JAMA Intern Med | "Do ratings track real clinical quality" validity check. |
| Angst, Agarwal, Gao, Khuntia & McCullough (2014). *IT and Voluntary Quality Disclosure by Hospitals.* 10.1016/j.dss.2012.10.042 | Decision Support Systems | Health-IT-and-transparency related work. |
| Agarwal, Dugas & Gao (2023). *Augmenting Physicians with AI...* 10.1111/jems.12555 | J Econ & Mgmt Strategy | AI-meets-clinician motivation; intro cite. |
| Gao, Greenwood, McCullough & Agarwal (2012). *A Digital Soapbox? The Information Value of Online Physician Ratings.* AOM Best Paper Proc. | proceedings | "Do reviews carry signal" framing. **NEEDS-VERIFICATION** (proceedings abstract; trace journal version). |
| Shukla, Agarwal, Goh, Gao & Agarwal (2023). *Catch Me If You Can: Fraudulent Physician Reviews with LLMs (GPT).* arXiv:2304.09948 | preprint | Closest LLM-on-physician-reviews work by these authors; positions this paper's novelty. **NEEDS-VERIFICATION** (preprint). |

Re-verify with `citation-audit` before any enters a manuscript bibliography.
