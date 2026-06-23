# JAMA Exemplars - content to imitate

Store the CONTENT of similar-topic JAMA-family papers here (PDF, or extracted
.md/.txt), so the writing stages can imitate their **language style and
preferences**. This is NOT a citation list (that is `../references/README.md`);
it is a style corpus.

## How to add

- Drop a PDF: `exemplars/<slug>.pdf` (e.g. `barnett-2017-nejm-opioid-ed.pdf`).
- Or store extracted text: `exemplars/<slug>.md` (the abstract + a few Results and
  Discussion paragraphs are enough to capture style).
- Prefer open-access sources when fetching (JAMA Network Open, PubMed Central);
  paywalled PDFs come from the author.

## What to capture per exemplar (feeds `../style-profile.md`)

- Abstract structure and exact phrasing.
- How the primary association is stated (sentence shape, effect size + 95% CI, hedging).
- Results paragraph openings and ordering.
- Discussion structure (principal findings -> prior work -> mechanism -> limitations -> conclusion).
- Tone, sentence length, jargon level, title pattern.

## Venue rule (important)

Exemplars MUST be JAMA-family (same venue: JAMA, JAMA Internal Medicine, JAMA Network
Open, JAMA Pediatrics, ...). Adjacent-journal papers (NEJM, JMIR, NBER, AJHE) go to
`../references/` for citation, NOT here. Topic can be any **physician behavior in the
JAMA family** (it need not be the exact opioid/trait topic); style is what we imitate.

## Candidate topics to source (JAMA family)

physician behavior / decision-making generally; physician-level prescribing or
practice variation; physician characteristics and care; online ratings vs quality;
two-part / variance-decomposition designs in claims or EHR data.

## Article type (match the exemplar to ProjB's chosen type)

- Schroeder 2019 (JAMA IM) = **Original Investigation** (full article, 8 pp).
- Burns 2024 (JAMA Netw Open) = **Original Investigation** (full article).
- Gray 2015 (JAMA IM) = **Research Letter** (~3 pp, the short-format option).

Both stored PDFs are FULL Original Investigations. If ProjB is written as a Research
Letter instead, we still need a JAMA-family Research-Letter exemplar (Gray is the
candidate, but paywalled / not in PMC).

## Seeded exemplars (JAMA family) - real full text stored

PDFs (older articles have a render-PDF):
- `schroeder-2019-jamaim-dental-opioid.pdf` (+ `.md`) - **JAMA Internal Medicine**, the
  TARGET OUTLET, Original Investigation. Prescriber-exposure -> opioid outcome, matched
  claims cohort, "Association of ... With ..." title, structured abstract, absolute-risk
  + 95% CI. Author manuscript via Europe PMC (PMC6439650). Mirror this voice most closely.
- `burns-2024-jamanetworkopen-opioid-variation.pdf` (+ `.md`) - **JAMA Network Open**,
  Original Investigation, open access. Clinician contribution to opioid-administration
  variation (ICC decomposition). (PMC10792468.)

Full-text XML (2026 articles: no render-PDF yet, so JATS XML = the real full text):
- `jamanetworkopen-2026-antipsychotic-by-clinician-type.xml` (+ `.md`) - JAMA Network
  Open, Original Investigation. Clinician-TYPE -> prescribing in Medicare Part D;
  closest "clinician attribute -> prescribing in claims" match. (PMC13019238.)
- `jamanetworkopen-2026-peer-feedback-hospitalist-antibiotic.xml` (+ `.md`) - JAMA
  Network Open, Original Investigation. "Association Between [factor] and [prescribing]"
  title pattern + physician prescribing behavior. (PMC13126217.)

## Still wanted (could not fetch - truly paywalled)

- Gray 2015, *JAMA Intern Med* 175(2):291-293 (10.1001/jamainternmed.2014.6291) -
  online review-site ratings vs quality; closest review-signal precedent in JAMA. NOT
  in PMC (inEPMC=N), so no open copy exists. Drop the PDF here as
  `gray-2015-jamaim-website-ratings.pdf` if you have institutional access.

## Status

- 4 JAMA-family exemplars stored (all Original Investigations): Schroeder (JAMA IM, PDF),
  Burns (JAMA Netw Open, PDF), Kim + Witt (JAMA Netw Open, full-text XML). Each has a
  `.md` style note. Removed the Barnett (NEJM) and Madanay (JMIR) drafts: adjacent
  venues, citations only in `../references/`. Gray 2015 (JAMA IM Research Letter) still
  needs a PDF from you (paywalled, not in PMC). Next: distill recurring JAMA voice into
  `../style-profile.md`.
