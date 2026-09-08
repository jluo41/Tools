# Ideation evidence bundle

The bundle is the frozen input contract for one ideation unit. It records
where evidence lives and what it is allowed to support. It does not become a
second Task or Discovery Result store.

## Required shape

```yaml
version: 1
kind: ideation-evidence-bundle
direction:
  address: b01.j01.t01
  question: "What research direction should be pursued?"
  scope: "population, data, setting, and time boundary"
  decision_rule: "what must be true before handoff"
sources:
  internal:
    - id: int01
      kind: task-result | task-qa | task-report | task-page
      path: "tasks/.../results/.../report.md"
      address: bNN.jNN.tNN.rNN | bNN.jNN.tNN
      locator: "metric/table/section or QA heading"
      role: signal | method | feasibility | boundary
      status: complete | answered | reported | pending | blocked
      digest: "short description of what this source establishes"
  external:
    - id: ext01
      kind: discovery-result | discovery-page | discovery-qa
      result_path: "discoveries/.../results/rNN_.../rNN_....md"
      bib_path: "discoveries/.../results/rNN_.../rNN_....bib"
      runtime_path: "discoveries/.../results/rNN_.../runtime.yaml"
      address: bNN.jNN.tNN.rNN | bNN.jNN.tNN
      cite: "@CanonicalKey"
      locator: "Card section/fact/page/figure or QA heading"
      role: prior-art | method | theory | boundary | counterevidence
      status: complete | verified | pending | blocked
      digest: "short description of what this source establishes"
policy:
  local_first: true
  no_copy: true
  unverified_is_support: false
  conflicts_preserved: true
created_at: "2026-09-07T12:00:00-04:00"
updated_at: "2026-09-07T12:00:00-04:00"
```

The exact path is resolved against the project root. `address` is always the
full owner-native readable BJTR address: `bNN.jNN.tNN.rNN` for a Run/Result or
`bNN.jNN.tNN` for a Page, report, or QA artifact. A bare `rNN` or an empty
address is never sufficient. If an owner artifact cannot be mapped to a full
address, hold the bundle instead of inventing one.

For a Discovery Result, `result_path`, `bib_path`, `runtime_path`, and `cite`
are required for load-bearing use. `runtime_path` points to the same-stem
Result's owner receipt; it is not a second evidence source. Its `operation`
must match the owner contract: `paper-analysis` for a paper Subject or
`source-analysis` for another source Subject. The Card's `cite: @Key` must
equal the sole key in the Result Bib. The file at `runtime_path` must show
`family: discovery`, that matching operation, and the person's
`bib.verification` receipt. The Discovery Task's derived
`outline/evidence/bibex/<task>.bib` may be listed as an additional convenience
reference, but never as the only external lineage.

A Bib file is a citation projection, not a source entry. Do not encode a
Bib-only item as `kind: discovery-bib`; point to its owning Discovery Result
and runtime instead.

For internal Task evidence, point to the owner’s Result, report, or QA file and
retain its full address, status, and a locator. A bundle may contain a Task QA
entry, a Task Result entry, or both; when both are used, keep them as separate
sources. `task-result` is an execution output; `task-qa` is the Task owner’s
answer to one general question. Never merge a QA answer and a Result into an
invented composite source. A Task QA answer is not permission for an ideation
card to state more than the answer establishes.

## Provenance rules

1. **Owner stays owner.** Task owns internal execution and QA; Discovery owns
   external Subjects, Runs, Results, and Bibs; Ideation owns only this manifest,
   cards, semantic receipts, and handoff.
2. **Pointers over copies.** Do not paste Result Cards, facts, reports, QA
   answers, or BibTeX into the bundle. A short digest is an interpretation and
   must not replace the source path and locator.
3. **Separate evidence from inference.** A card labels direct observation,
   cross-source interpretation, and proposed hypothesis separately. An
   inference cites all sources that led to it.
4. **Status travels with the claim.** `complete` or `verified` is never inferred
   from a filename. Pending citation verification or an unresolved Run keeps
   the support provisional and cannot satisfy a handoff claim gate.
5. **Contradictions remain visible.** Record both paths and describe the
   population, measure, or method difference. Do not silently pick the more
   convenient source.
6. **Search is not evidence.** Candidate rows, search URLs, snippets, and
   Discovery aggregates are leads/navigation. Only an admitted, analyzed,
   completed owner Result can support a factual card claim.
7. **Changed inputs reopen work.** If a source, question, acceptance contract,
   or material interpretation changes, refresh the bundle and re-run the owning
   workflow. Do not edit a frozen Run or Result in place; the owner’s
   `supersedes:` rule applies.

## Request/reuse protocol

When a card needs external evidence:

```text
bundle scan
  ├─ exact completed Result satisfies question → reuse Result/Bib pointers
  ├─ related Result, changed question/acceptance → Discovery new Run with supersedes:
  └─ no adequate Result → Discovery source-map/source-reading request
                                      → canonical Subject(s)
                                      → one Discovery Run/Result per Subject
                                      → refresh bundle
```

The local workflow receipt records the request question, required channel
coverage, Discovery Task path, returned Result paths, and any unresolved gap.
It must not add consumer fields to `discovery.yaml`. Discovery search retains
its channel law and independently resolves identity; an optional scout or
search URL never becomes a Result/Bib by itself.

The request must instantiate the channel set required by the frozen scope; the
lists in the receipt example are illustrative, not defaults. A durable
literature sweep includes the Discovery-required preprint and journal-index
channels; a clinical/biomedical sweep adds the relevant medRxiv and PubMed
coverage. Optional scouts remain optional and never replace those channels.

Reuse is permitted only when all of these match the frozen ideation demand:

- the canonical Subject identity and Result scope are the same;
- population, data/setting, time boundary, and requested reading depth cover
  the current question;
- the operation, required channel coverage, and claim-support requirements
  are the same (or the old Result is strictly deeper);
- the Result is complete, its Card/Bib keys agree, and its citation is verified
  when the source is load-bearing; and
- the acceptance contract has not materially changed.

A matching DOI or title alone is not reuse evidence. Treat a change as
material when it changes any of identity, population, data/setting, time
boundary, reading depth, operation, required channels, or the acceptance /
claim-support rule. A material change requires a new owner Run with the
owner’s `supersedes:` link. A related but insufficient Result may remain in the
bundle as provisional context, but it cannot satisfy a claim gate.

Use the Discovery reading-depth order `metadata < abstract < full-text`.
An older Result is “strictly deeper” only when it reaches a later level in this
order and its locators actually support the current claim; a title/DOI match,
an abstract link, or a larger citation count is not deeper evidence.

When internal feasibility is missing, the symmetric route is `haipipe-task qa`
for an existing answer or a new Task Run when the work passes the four
`haipipe-run` tests. The bundle records the returned owner path either way.
