# Patent Exemplars - content to imitate

Store the CONTENT of similar GRANTED patents here (PDF, or extracted .md/.txt), so the
writing stages can imitate their **claim and specification language**. This is NOT a
prior-art list (that is `../references/README.md`); it is a style corpus.

## How to add

- Drop a PDF: `exemplars/<slug>.pdf` (e.g. `us10000000-b2-method.pdf` or
  `cn112345678-b.pdf`).
- Or store extracted text: `exemplars/<slug>.md` (claim 1 + the dependent claims + the
  Summary and a few Detailed-Description paragraphs are enough to capture style).
- Prefer GRANTED patents (the granted claims have survived examination) from the same
  jurisdiction and technical field as the target filing.

## What to capture per exemplar (feeds `../style-profile.md`)

- Claim 1 phrasing and the independent / dependent claim hierarchy shape.
- Antecedent-basis and transition-word usage ("comprising" / "包括").
- Summary arc: technical problem -> technical solution -> advantages.
- Detailed-Description structure: embodiment ordering, reference-numeral conventions.
- Title and Abstract phrasing within the jurisdiction word limit.
- Tone, sentence shape, jurisdiction-specific moves (CN 其特征在于 / EP characterised in
  that / US comprising).

## Candidate topics to source (similar to this filing)

granted patents in the filing's technical field and target jurisdiction; same patent
type (invention vs utility model); patents whose core inventive concept is structurally
analogous to the claimed invention.

## Status

- Empty. Populate by dropping granted-patent PDFs or fetching exemplars, then distill
  the recurring claim/spec style patterns into `../style-profile.md`.
