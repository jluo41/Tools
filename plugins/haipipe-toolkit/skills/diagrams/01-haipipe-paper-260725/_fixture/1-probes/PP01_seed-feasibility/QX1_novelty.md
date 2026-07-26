## QX1 — novelty of review-trait → prescribing

### q-executor
Has any published study measured a physician's personality or interpersonal traits from patient-review text AND linked those trait measures to that physician's prescribing behavior in administrative/claims data at the physician level?
Identify the closest prior art on each half — trait-to-prescribing links (however the trait is measured) and text-derived trait inference.
Deliverable: a prior-art digest naming the closest studies on each half, and naming any on-point title that could not be read in full as unresolved rather than dropping it.
Accepted: occupied (name the study) | unoccupied (name the nearest neighbors).

### q-consumer
* **Q-Seed-1** — Is the review-trait → prescribing angle novel?
  "Has any published study linked physician personality or traits measured from patient-review TEXT to prescribing behavior in administrative CLAIMS data?
  Is the review-text-exposure / administrative-claims-outcome combination unoccupied ground?"
  Stake: anchors the Motivations "has not been tested against independent clinical behavior" claim, the three Landscape sentences that stake the gap, and H1.
  If prior work already occupies this ground, the paper has no novel contribution and the seed collapses.

### bank binding
**route**: discovery
**bank**: run · discoveries/P02_misq-novelty/01_review-trait-to-opioid-rx-prior-art/
Originally reuse (the 2026-07-03 QA answered this q-executor at confidence medium). ESCALATED to run(1) and ENRICHED in place on 2026-07-20 under human `--depth 1+`, to close its two open verification gaps.
Enrich result: verdict UNOCCUPIED CONFIRMED, confidence RAISED medium -> medium-high; Bandi 2024 read + classified non-occupying; four near-neighbours (S012-S015) appended; 15/15 sources verified.
**target**: discoveries/P02_misq-novelty/01_review-trait-to-opioid-rx-prior-art/QA/1-prior-art.md
**state**: read

### a-executor

UNOCCUPIED (medium-high confidence).
Across a two-pass search — the 2026-07-03 session plus a 2026-07-20 enrich (run, depth-1, human-authorized) — no published study does both halves at once: derive a physician personality/interpersonal-trait measure from patient-review TEXT AND link it to that physician's prescribing in administrative/claims data at the physician level.
Fifteen sources now on file across one on-point line and several adjacent lines, all fifteen verified against identifiers; each nearest neighbour is missing exactly one leg.
The verdict is unchanged from 2026-07-03; the two weaknesses that had held it at *medium* are both closed, so confidence is now medium-HIGH (still not high — Scopus/WoS not queried directly, Semantic Scholar again partly rate-limited).

Closest prior art, half A — trait → prescribing, however the trait is measured:
* Kristensen et al. (2022), BMC Primary Care 23:243, doi:10.1186/s12875-022-01847-z — Danish GPs scored on the Jefferson Scale of Empathy (self-report survey), top vs bottom deciles, linked to their own antibiotic prescriptions in the Danish National Prescription Registry (2017); high-empathy GPs issued ~92 fewer prescriptions, penicillins driving the gap.
  The structural analog.
  Missing leg: the trait is survey-measured, not text-derived; empathy, not a broad inventory; antibiotics, not opioids.
* Morishita et al. (2025), Rheumatology 64(10):5269-5276, doi:10.1093/rheumatology/keaf288 — self-reported Big Five (TIPI-J) of rheumatologists vs patient-rated shared decision-making; higher conscientiousness and neuroticism tracked LOWER shared decision-making.
  Nearest published physician-Big-Five → clinical-behaviour study.
  Missing leg: survey trait, and the outcome is a patient-rated scale, not prescribing in claims.

Closest prior art, half B — text-derived trait inference:
* Luo, Han, Welivita, Di, Wu, Zhi, Agarwal & Gao (2025), arXiv:2510.03997 — LLM pipeline extracts Big Five plus patient-oriented judgments from 4.1M reviews of ~227K U.S. physicians across Healthgrades, Vitals, RateMDs and Yelp; human-benchmark agreement 0.72-0.89.
  The only at-scale review-text → physician-Big-Five work located.
  Missing leg: stops at trait measurement, no prescribing outcome, no claims linkage.
  (Self prior art — must be cited and differentiated.)
* Hrazdil, Novak, Rogo, Wiedman & Zhang (2020), J Bus Finance & Accounting 47(3-4):519-544, doi:10.1111/jbfa.12406 — machine scoring of Big Five from executives' unscripted conference-call speech, derived risk-tolerance validated against archival audit fees.
  The full text → trait → archival-outcome paradigm exists.
  Missing leg: the text is the subject's OWN speech, not third-party evaluations, and the domain is corporate finance.

RESOLVED this pass — the previously-unread on-point title does NOT occupy:
* Bandi, Dey & Rao (2024), SEEJPH XXV Suppl 1:2599-2615, doi:10.70135/seejph.vi.2497, "Impact of Physician Personality Traits on Drug Prescription Behaviour" — READ this pass (Crossref + OpenAlex + full-text PDF).
  Cross-sectional survey of 171 respiratory physicians, Telangana, India.
  Exposure = self-report Hogan MVPI questionnaire, NOT text-derived; outcome = self-reported anti-allergic prescribing on the same survey, NOT administrative/claims.
  Does NOT occupy on either leg (weaker than Kristensen on the outcome side).
  On-point title confirmed non-preempting.

Why the halves have not met — the intervening line connects patient-side signals to prescribing using NUMERIC metrics only, never a psychological construct from text, and reports mostly null:
* North et al. (2018), SAGE Open Medicine 6:2050312118782547 — panel satisfaction vs opioid prescribing volume; no significant association after adjusting for patient complexity.
* Carrico et al. (2018), J Am Board Fam Med 31(6):941-943 — physicians on satisfaction-based pay incentives reported an impact on their opioid prescribing 3x more often than non-incentivized peers (36% vs 12%, P=.004); self-report, not measured behaviour.
* Secrist et al. (2020), J Surg Orthop Adv 29(1):5-9, PMID:32223858 — Press Ganey vs opioid prescriptions across practice types; minimal association.
* Daskivich et al. (2018), JAMIA 25(4):401-407 — consumer star ratings vs Choosing Wisely adherence, readmissions, length of stay, cost, peer review; no meaningful associations.
* Okike et al. (2016), JMIR 18(12):e324 — surgeon online ratings vs 30-day risk-adjusted CABG mortality; no correlation (P=.13).
* Feizollah et al. (2025), JMIR 27:e72853 — scoping review of NLP on unstructured patient feedback; the field clusters on sentiment/topic/service themes and links no review-derived construct to objective physician behaviour.

Four near-neighbours appended by the 2026-07-20 enrich, each still short exactly one leg:
* Al Mohajer et al. (2025), Antimicrob Steward Healthc Epidemiol, doi:10.1017/ash.2025.194 — a provider characteristic (medical-school ranking) → that physician's antibiotic prescribing in Medicare Part D CLAIMS.
  Closest new instance of the exact outcome data type (the claims DV is reachable at physician level) — but from institutional pedigree, not a trait, not from text.
* Abrams et al. (2023), JMIR AI 2:e46317, doi:10.2196/46317 — ML extraction from online REVIEW TEXT → an administrative health outcome (drug-induced mortality).
  Closest new review-text → administrative-outcome instance INSIDE medicine — but the unit is facilities, not physicians; the outcome is population mortality, not prescribing; the text yields sentiment/topics, not a trait.
* Helgeson et al. (2024), JMIR Infodemiology 4:e56675, doi:10.2196/56675 — social-media text sentiment → drug prescribing across 48 hospitals.
  A text → prescribing link exists — but from anonymous population chatter, not reviews of a named physician; ecological, not physician-level.
* White et al. (2026), Health Communication, doi:10.1080/10410236.2026.2615865 — in-encounter physician communication conduct → opioid prescribing.
  Opioid-specific and about physician behaviour — but the exposure is observed conversation, not a review-text-derived trait; no claims outcome.

Provenance: 15 of 15 sources VERIFIED against DOI/PMID/arXiv id by the discovery layer (the former sole NEEDS-VERIFICATION source, Bandi 2024, was resolved by reading it this pass).
🔍 VERIFIED-by-discovery is identifier-level, NOT bibtex-level — every one stays unconfirmed for the .bib until a human checks it.

Caveats carried from the QA file:
* Two-session absence, not exhaustive: the negative rests on 2026-07-03 + the 2026-07-20 enrich.
* Residual channel gaps remain: Scopus and Web of Science PROPER still not queried directly (OpenAlex + Crossref proxied); gray-literature portals (SSRN/NBER/ResearchGate/ProQuest) attempted this pass but the web-scrape returned nothing; Semantic Scholar again partly rate-limited.
* The half-B nearest neighbour is a PREPRINT (arXiv:2510.03997); "published" in the strict peer-reviewed sense would exclude it.
* Half A's closest neighbour is a different drug class and health system (antibiotics, Denmark); generalization to opioids or U.S. claims was not assessed.
* Scope is prior-art OCCUPANCY only.
  It says nothing about whether review-derived trait scores measure personality as opposed to sentiment or satisfaction (a CLAIMS-stage construct-validity question).

Not-done (residual, after the 2026-07-20 enrich):
* Bandi, Dey & Rao (2024), SEEJPH, doi:10.70135/seejph.vi.2497 — RESOLVED/closed: read + classified non-occupying (survey exposure, self-reported outcome).
* Search sweep — PARTIALLY closed: a *direct* Scopus / Web of Science query and a working gray-literature sweep (SSRN/NBER/ResearchGate/ProQuest) remain open.
  Reduced, not eliminated.
* Appended neighbours S012-S015 were verified by identifier and classified from abstracts/metadata, not read in full — adequate for near-neighbour triangulation; note if any is cited directly.

