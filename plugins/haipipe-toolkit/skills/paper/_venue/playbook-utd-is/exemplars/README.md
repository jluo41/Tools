# UTD-IS Exemplars - content to imitate

Store the CONTENT of similar IS papers here (PDF, or extracted .md/.txt), so the
writing stages can imitate their **language style and preferences**. This is NOT a
citation list (that is `../references/README.md`); it is a style corpus.

## Tag by journal (subfolders)

Because this is a FAMILY pack, keep exemplars separated by outlet so a chosen venue
pulls the right style corpus:

```
exemplars/
  misq/    MIS Quarterly exemplars
  isr/     Information Systems Research exemplars
  ms-is/   Management Science (IS department) exemplars
```

## How to add

- Drop a PDF into the journal subfolder: `exemplars/<journal>/<slug>.pdf`
  (e.g. `exemplars/misq/venkatesh-2003-misq-utaut.pdf`,
  `exemplars/isr/author-year-isr-did-platform.pdf`,
  `exemplars/ms-is/author-2022-mnsc-platform-pricing.pdf`).
- Or store extracted text: `exemplars/<journal>/<slug>.md` (the abstract +
  contribution paragraph + a few Theory/Model and Discussion paragraphs are enough to
  capture style).
- Prefer open-access or author-provided PDFs.

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

- Empty. Populate by dropping PDFs into the journal subfolders or fetching exemplars,
  then distill the recurring style patterns into `../style-profile.md` (tag each
  pattern by journal).
