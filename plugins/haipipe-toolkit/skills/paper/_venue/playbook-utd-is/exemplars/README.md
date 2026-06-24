# UTD-IS Exemplars - content to imitate

A style corpus of similar IS papers, so the writing stages can imitate their
**language style and preferences**. This is NOT a citation list (that is
`../references/README.md`).

## Where exemplars live (two layers)

The binary PDFs are large and often paywalled, and this repo is **public**, so they
do NOT live here. The split:

```
_WorkSpace/HAIToolLib/1-ExemplarLib/utd-is/<journal>/<slug>.pdf   # the PDFs (gitignored, local)
  ../../<this pack>/exemplars/<journal>/<slug>.md                  # extracted style text (in repo)
```

- **PDFs** -> the shared HAIToolLib asset root, `_WorkSpace/HAIToolLib/1-ExemplarLib/utd-is/<journal>/`.
  Local only, never committed. See `_WorkSpace/HAIToolLib/README.md` for the convention.
- **Extracted style text** (`<slug>.md`: abstract + contribution paragraph + a few
  Theory/Model and Discussion paragraphs) -> the journal subfolder *here* in the pack.
  Small, durable, version-controlled; this is what survives if the PDF is gone.
- The distilled patterns themselves live in `../style-profile.md` (the real payload).

Journals: `misq/` (MIS Quarterly), `isr/` (Information Systems Research),
`ms-is/` (Management Science, IS department).

## How to add

1. Put the PDF at `_WorkSpace/HAIToolLib/1-ExemplarLib/utd-is/<journal>/<slug>.pdf`
   (e.g. `.../misq/venkatesh-2003-misq-utaut.pdf`). Prefer open-access or
   author-provided copies.
2. Distill its style into `../style-profile.md` (tag by journal), and optionally
   drop the extracted text at `exemplars/<journal>/<slug>.md` for future re-mining.

## What to capture per exemplar (feeds `../style-profile.md`)

- Abstract arc and exact phrasing (MISQ/ISR prose <= 150 w; MS-IS structured < 200 w).
- How the contribution is stated in one sentence/paragraph (MISQ theoretical; ISR
  theoretical / empirical / methodological-IS; MS-IS economic / analytical).
- Hypothesis phrasing (mechanism -> directional prediction).
- For ISR/MS-IS empirical: how the identification strategy is stated and how causality
  is hedged. For MS-IS analytical: Proposition/Theorem phrasing and how welfare is
  reported.
- Discussion structure (contribution -> implications -> limitations -> conclusion).
- Tone, sentence length, jargon level, how it positions against IS literature (MS-IS:
  against economics / OR / management science).

## Candidate topics to source (similar to this paper)

- **misq/**: theory-forward IS empirics in the paper's domain; design-science
  exemplars if relevant; foundational construct papers the manuscript builds on.
- **isr/**: theory-driven IS empirics (platforms, IT adoption, digital markets, IT
  governance); causal-identification exemplars (DiD / IV / RD / matching / natural
  experiments); well-powered survey or experiment exemplars; computational/ML-for-IS
  exemplars if relevant.
- **ms-is/**: economics-of-IS empirics or analytical models (platform economics, IT
  investment and value, digital markets, privacy/security economics, sharing/gig
  platforms, AI/automation economics, FinTech, healthcare IT economics); hybrid
  model-plus-empirics exemplars; foundational IT-economics papers the manuscript
  builds on.

## Status

Seeded 2026-06-24 from `Paper-Personality2Opioid-MISQ2026/0-extra/sample-paper/`.
PDFs stored locally under `_WorkSpace/HAIToolLib/1-ExemplarLib/utd-is/` (gitignored):

| stored file (under 1-ExemplarLib/utd-is/) | paper | journal |
|---|---|---|
| `misq/liu-2021-misq-inferred-personality-review-helpfulness.pdf` | Liu, Li & Xu (2021), *Assessing the Unacquainted* | MISQ |
| `isr/bao-bardhan-2021-isr-aco-healthit-quality-efficiency.pdf` | Bao & Bardhan (2021), *ACO Performance & Health IT* | ISR |
| `isr/zhang-2026-isr-physician-reviews-slm-consultation-demand.pdf` | Zhang, Hao, Zhan & Wu (2026), *Physician Reviews & Consultation Demand* | ISR |

Recurring style patterns distilled into `../style-profile.md` (see "Mined from
`exemplars/`", tagged by journal).

## Fetch-list (exemplar candidates from discovery S01, 2026-06-24)

The Gao & Agarwal discovery surfaced 7 strong exemplar candidates (full corpus +
DOIs in `../references/README.md`). PDFs are paywalled, so they are NOT yet stored;
obtain an author/library/open-access copy and drop each at the target path (under
`_WorkSpace/HAIToolLib/1-ExemplarLib/utd-is/`), then distill its style into
`../style-profile.md` (tag by journal).

| target path (under 1-ExemplarLib/utd-is/) | paper | DOI | why fetch |
|---|---|---|---|
| `misq/gao-2015-misq-vocal-minority-silent-majority.pdf` | Gao, Greenwood, McCullough & Agarwal (2015), MISQ | 10.25300/MISQ/2015/39.3.03 | the closest MISQ anchor: validity/representativeness of online physician ratings |
| `misq/goh-2016-misq-online-health-community-social-value.pdf` | Goh, Gao & Agarwal (2016), MISQ | 10.25300/MISQ/2016/40.1.11 | MISQ digital-health "social value" theory-forward contribution |
| `misq/agarwal-2000-misq-cognitive-absorption.pdf` | Agarwal & Karahanna (2000), MISQ | 10.2307/3250951 | canonical MISQ construct -> belief prose (writing exemplar) |
| `isr/goh-2011-isr-adaptive-routinization-healthcare-it.pdf` | Goh, Gao & Agarwal (2011), ISR | 10.1287/isre.1110.0365 | ISR health-IT clinician-behavior framing |
| `ms-is/shukla-2020-mnsc-wom-doctor-appointment-booking.pdf` | Shukla, Gao & Agarwal (2020), Management Science | 10.1287/mnsc.2020.3604 | **fills the empty ms-is slot**; reviews -> behavior identification |
| `ms-is/wang-2023-mnsc-ai-worker-teaming.pdf` | Wang, Gao & Agarwal (2023), Management Science | 10.1287/mnsc.2021.00588 | MS-IS AI-in-healthcare-work exemplar |
| `ms-is/angst-2010-mnsc-social-contagion-emr-diffusion.pdf` | Angst, Agarwal, Sambamurthy & Kelley (2010), Management Science | 10.1287/mnsc.1100.1183 | MS-IS adoption/diffusion identification |

Fetching even one of the three `ms-is/` candidates closes the long-standing MS-IS gap
(no full-text MS-IS exemplar yet). More MISQ theory-forward exemplars also help.
