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
Readout, Facts, optional Trigger claim audit, Limits, and Reuse. `VERIFIED`
means exact title, authors, venue, and locator were confirmed against a trusted
publisher/index. Anything less remains `NEEDS-VERIFICATION` and cannot produce
a `status: complete` Result.

## Coverage declaration

Coverage belongs to the Task Page's source-map section, not to every Result.
It states channels searched, channels not searched, date, and candidate
selection rule:

```md
## Source map

Coverage: arXiv API + OpenAlex journal index, 2026-09-01.
Not searched: PubMed and top-venue pass.
Admission: canonical identity resolved and directly relevant to the Topic.
```

A silent cap reads as complete coverage when it was not; always name the
boundary.

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
