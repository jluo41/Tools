# Patent Style Profile (imitate this)

Distilled language style and preferences to imitate when writing or editing a patent
filing (claims + specification). This is a STARTER from patent drafting conventions;
ENRICH it from the actual granted patents stored in `exemplars/` as they are added
(pull real claim sentences and spec paragraphs and mirror their shapes).

## Claims

- Each claim is ONE sentence, however long. No periods inside a claim; the claim ends
  with a single period.
- Antecedent basis: introduce an element with "a" / "an" on first use, then refer to
  it with "the" / "said" (CN: 所述) thereafter. Never use "the X" before "a X" has been
  introduced.
- Open transition "comprising" (CN: 包括) keeps the claim open to additional unrecited
  elements; "consisting of" is closed; "consisting essentially of" is intermediate.
  Default to "comprising" for breadth.
- Independent claim 1 is the broadest defensible statement of the core inventive
  concept; each dependent claim adds exactly one narrowing feature and recites its
  parent ("The method of claim 1, wherein..." / CN: "根据权利要求1所述的方法，其特征在于").
- Means-plus-function caution: functional language ("means for ...") invokes narrow
  statutory interpretation tied to the structure in the specification; prefer reciting
  concrete structure or steps unless the means-plus-function scope is intended.
- No relative or subjective terms without an in-spec definition ("rapid", "efficient",
  "substantially"); no result-to-be-achieved language that claims an outcome without
  the structure that produces it.

## Specification

- The specification supports the claims, not the other way around: every claim element
  must have explicit (or clearly inherent) written-description support.
- Consistent terminology is mandatory: same word for the same concept throughout; same
  component, same reference numeral, everywhere.
- Background states specific TECHNICAL deficiencies of the closest prior art; it is not
  a literature review and never admits the prior art is "superior" or "better".
- Summary mirrors the disclosure: technical problem -> technical solution (covering all
  claim elements) -> advantages framed structurally ("由于采用了...结构，因此具有...效果").
- Detailed Description gives at least one complete embodiment with reference numerals
  and enough detail for a POSITA to make and use the invention; add alternatives to
  support broader claim interpretation.

## Title and Abstract

- Title matches the broadest claim scope; no "improved" / "new" / "novel", no
  trademarks; concise (CN typically under 25 characters; US under 500 characters).
- Abstract: technical field -> problem -> core solution -> key advantage, within the
  jurisdiction word limit; no statements on merits or value (EP), no legal phrases (US).

## Tone & preferences

- Declarative, structural, and impersonal; describe the apparatus / steps, not the
  inventors' efforts or excitement.
- NO experimental results, accuracy metrics, or empirical evaluations anywhere in the
  specification (those are research-paper material, not invention properties).
- NO numerical performance claims in the advantages (e.g. "response time 105ms"); frame
  benefits qualitatively from the structure.
- Minimal hype; one idea per claim element; no buzzword stacks.

## Per-jurisdiction language notes

- **CN (CNIPA)**: Chinese; claim two-part form with "其特征在于"; use 所述 / 包括 / 等
  correctly; abstract <=300 Chinese characters; utility model (实用新型) uses
  apparatus/device claims only.
- **US (USPTO)**: English; single-clause claims with "comprising:"; strict antecedent
  basis ("a" -> "the"); drawings labeled "FIG. 1"; abstract <=150 words.
- **EP (EPO)**: English; two-part claim form "..., characterised in that ..." is
  MANDATORY for every independent claim (Rule 43(1)); a Reference Signs List is
  MANDATORY (Rule 42); abstract ~150 words with no statements on merits.

## To enrich from `exemplars/`

- [ ] Pull 3-5 real granted-patent claim-1 sentences; list them as patterns to mirror.
- [ ] Record each exemplar's independent / dependent claim hierarchy shape.
- [ ] Record the Summary's problem -> solution -> advantage phrasing actually used.
- [ ] Note recurring Background and Detailed-Description section moves per jurisdiction.
- [ ] Record the abstract word budget and arc actually used per jurisdiction.
