# Discovery Source Presentation Format (canonical)

This file owns how sources are presented. `paper-run-contract.md` owns where
durable source analysis lives.

## One source = one readable unit

Never put papers in a wide metadata table. Use one subsection/card per source,
with the full title visible. Tables remain legal for short-field analytical
matrices, not citation listings.

## Durable Paper/Source Result

The canonical durable presentation is:

```text
results/<RUNNAME>/<RUNNAME>.md
```

Required identity header:

```md
# Large Language Models are Zero-Shot Rankers for Recommender Systems

- run: r01_hou2024_zero_shot_rankers
- cite: @Hou2024ZeroShotRankers
- subject: doi:10.1007/978-3-031-56060-6_24
- venue: ECIR 2024
- verification: VERIFIED
```

Then follow the Result Card sections in `paper-run-contract.md`: Question,
Readout, Source access, Retrieval scope, Facts, optional Trigger claim audit,
Limits, and Reuse. `VERIFIED`
means exact title, authors, venue, and locator were confirmed against a trusted
publisher/index by a person. Anything less remains `NEEDS-VERIFICATION`.
That state does not prevent a technically complete Result when its Card,
facts, authoritative one-entry Bib, and runtime receipt are all present; it
does prevent the Discovery Task from claiming an epistemic `ok` or
`inconclusive` close. Keep the Task blocked/held and show the verification debt.

The short `run:` value is a local display stem. In a durable receipt or
cross-Folder reference, also show the full readable and compact BJTR addresses
(for example b01.j02.t03.r01 and b01j02t03r01); a bare rNN is never a global
identity. The old numbered skill-family labels are not substitutes for that
address; see `bjtr-alignment.md`.

Every new paper Result exposes clickable DOI/publisher, PubMed-or-query,
exact-title Google Scholar, exact-title Google, authoritative BibTeX, and any
lawful full-text route through `source-access.md`. Always name the actual
reading depth beside those links. A discovered full-text URL does not mean the
Run read the full text, and a Scholar/Google link is navigation rather than
evidence authority.

## Coverage declaration

Coverage belongs to the Task Page's source-map section, not to every Result.
It states channels searched, channels not searched, date, and candidate
selection rule:

```md
## Source map

Coverage: Semantic Scholar (S2) topic search + arXiv API, 2026-09-01.
Queries: "adaptive sampling" and "rare phenotype"; no citation-count filter.
Not searched: PubMed and citation-chain follow-up.
Admission: before screening, include studies that evaluate an adaptive method
for rare-phenotype detection; exclude generic sampling work with no such
application. Resolve canonical identity before opening a Paper Run.
Retrieval order: S2 citation count as indexed on 2026-09-01; used only to order
the S2 first-pass queue, not as an admission or quality criterion. arXiv
results remain in provider relevance order.
Boundary: first 30 unique candidates per channel; this is not exhaustive
coverage beyond the listed channels and screening limit.
```

A silent cap reads as complete coverage when it was not; always name the
boundary. Freeze the candidate rule at SCOPE and record it on the Task Page.
Provider rank, citation count, venue, and publication date describe retrieval
or source metadata. They do not, alone, establish relevance, study quality, or
support for a claim.

Keep one admission-decision receipt per screened candidate in the Task source
map. Each receipt names the frozen rule version/hash, candidate disposition
and rationale, evaluator, and timestamp. Link admitted candidates to their full
readable/compact Run identity. For excluded or unresolved candidates, retain
the exact result record that was screened by URI and SHA-256; these candidates
have no owning Run. Task outcome and any applicable confidence judgment link to the single
`discovery.yaml#report.assessment` receipt, which lists hashes of the frozen
scope, closed Page, and candidate decision set, plus all considered Run
identities.

## Topic source index

The Page may list completed Results as one subsection each:

```md
### r01_hou2024_zero_shot_rankers — Large Language Models are Zero-Shot Rankers for Recommender Systems

- [Readout](results/r01_hou2024_zero_shot_rankers/r01_hou2024_zero_shot_rankers.md)
- ECIR 2024 · doi:10.1007/978-3-031-56060-6_24
- role: adjacent method · cite: @Hou2024ZeroShotRankers
- finding: LLM rankings are sensitive to candidate position and popularity.
```

`sources.md`, when retained for an old folder or generated for an external
consumer, uses this same format and is a derived index. It is never the store
for the full reading or Bib authority. New per-source notes live in the paired
Result, not a monolithic `notes.md`.

## Non-paper source

A webpage, report, dataset, social post, or other source may be the Run Subject
when it is itself evidence. Use the same Result contract, an authoritative
one-entry `@online`/appropriate Bib entry, and `subject.kind` in runtime. When a
social post merely points to a paper, it stays Trigger provenance and the paper
is the Subject.

## One-off inline results

One-off calls create no folder and return a numbered list:

```text
1. Hou et al. (2024). Large Language Models are Zero-Shot Rankers for Recommender Systems.
   ECIR 2024 · arXiv:2305.08845 · verification: VERIFIED
```

If the user chooses to keep one, route it through `add`: resolve the canonical
Subject and scaffold a numbered Paper Run. Never turn an inline worker call
itself into a Run.
