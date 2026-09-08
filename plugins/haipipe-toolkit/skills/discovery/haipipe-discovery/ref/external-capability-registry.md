# External capability registry

This registry turns selected reference skills into HAI-safe capability inputs.
It is a routing aid, not a second workflow engine. Read the section for the
current Discovery family before invoking an external worker.

## Decision classes

| Class | Meaning | HAI rule |
|---|---|---|
| active | Already implemented in the HAI Discovery family | Use the local adapter; do not call the upstream copy just to duplicate it. |
| craft | Useful reasoning or extraction procedure | Use its output as an in-memory packet, then normalize it into the HAI contract. |
| audit | Verification or quality gate | Run after the relevant Result or Page artifact exists; it never allocates a Run. |
| infra | Optional retrieval infrastructure | It may supply context, but it never owns a Result, Bib, or Page. |
| out-of-scope | A different product or lifecycle | Do not route ordinary Discovery work to it. |

## 1_search · candidate acquisition

### Active HAI adapters

- `arxiv`, `semantic-scholar`, `Crossref/PubMed`, `medRxiv`, `exa-search`,
  `openalex`, and `gemini-search` provide candidate channels.
- `alphaxiv`, `deepxiv`, and `paper-analyzer` provide optional source reading
  after a candidate has been admitted.
- `openalex` and `gemini-search` remain optional scouts. Independent identity
  resolution still happens before a Run is opened.

### Accepted reference procedures

- `academic-paper-search` supplies a provider decision tree for arXiv, NBER,
  SSRN, Crossref, OpenAlex, Unpaywall, and Semantic Scholar. Use it to choose
  a missing search or access channel, not to write a second bibliography.
- ARIS `research-lit` supplies local-first search, alias expansion, citation
  chaining, and canonical-record resolution. Use it as a craft worker when the
  normal channel sweep needs help.
- AER `aer-literature` supplies the optional five-channel novelty pass and an
  antecedents map. Use it only for novelty or landscape questions where its
  economics-specific assumptions are appropriate.

### Normalized search packet

An external search result must be reduced to:

```text
query, channel, title, authors, year, venue, identifiers,
landing_url, full_text_url, access_state, relevance_note
```

The HAI search specialist deduplicates this packet, resolves the canonical
Subject, records channel coverage, and is the only component allowed to call
the Task Page's add operation.

## 2_review · one-Subject reading

### Accepted reference procedures

- K-Dense `literature-review` contributes extraction and appraisal dimensions:
  method, sample, outcome, limitation, reproducibility, conflict of interest,
  and confidence.
- `literature-source-tracing` contributes citation-to-source passage matching
  when a claim needs a primary-text locator. Its DOCX/highlighted-PDF output is
  not a HAI artifact; return evidence rows instead.
- `citation-fidelity` and `reference-verify` contribute page-level citation
  checks. They are audit workers and must preserve `pending` when the source
  cannot be located.
- PaperRAG is optional local context infrastructure for large PDF collections.
  It can retrieve chunks for a reviewer, but it cannot create a Run or Result.

### Normalized review packet

```text
subject_id, reading_depth, identity, question, methods,
claims, locators, limitations, disagreement, confidence,
verification_state, unresolved_items
```

The review specialist writes the packet into the existing same-stem Result
contract. It never infers a topic conclusion from one paper and never builds
the aggregate Bib.

## 3_synthesize · cross-Result integration

### Accepted reference procedures

- `research-genealogy` supplies a non-linear citation lineage for
  `landscape-review`; use it to propose relationships, then verify every edge
  against admitted Result metadata.
- K-Dense synthesis structures are usable as a choice among thematic,
  chronological, methodological, and theoretical organization. The Page
  question, not the external template, chooses the structure.
- ARIS `result-to-claim` contributes a support gate: supported, partial, or
  unsupported. Adapt it to Result-to-Page-Claim and retain the exact Result and
  cite key for every status.
- ARIS `citation-audit` is the cross-Result/Page post-synthesis check. It can
  hold the Page at CHECK, but cannot write a competing references file.
  `citation-fidelity` and `reference-verify` remain per-Result checks and must
  be resolved before a Result is promoted into synthesis.
- ARIS `prior-art-search` is available only for the `prior-art-verdict` route;
  patent/FTO conclusions require the route's explicit scope.

### Normalized synthesis packet

```text
claim_or_theme, supporting_result_ids, opposing_result_ids,
relationship, evidence_depth, citation_keys, gap, limit, next_move
```

The synthesis specialist uses this packet to write the shared Page CONTENT
phase. It never creates `runs/`, `results/`, a local `rNN`, or a second Bib.

## Non-adoption rules

- Do not import a whole external orchestrator such as `deep-research`,
  `academic-pipeline`, or `literature-survey-generator`.
- Do not bulk-install `auto-research-skills` or `awesome-journal-skills`;
  their catalogs and venue-specific workers are reference indexes only.
- Ideation, research refinement, venue selection, experiment auditing, and
  manuscript writing remain outside Discovery. Route semantic direction work
  to `haipipe-ideation` after accepted Results are available.
- Every external call is receipt detail. D1 `ACQUIRE` remains the sole Run
  commissioner, the Result owns its one-entry Bib, and Outline owns the derived
  Task Page Bib.
