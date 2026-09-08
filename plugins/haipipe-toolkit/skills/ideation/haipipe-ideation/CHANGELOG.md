# haipipe-ideation — Changelog

Skill-scoped changelog (read on demand; not loaded at invocation).

## 0.3.1 · 2026-09-08

- Closed the second fresh-context field-test gaps: added Paper Page context,
  owner-state normalization, exact novelty/pressure receipt schemas, and
  explicit output-fenced Paper projection behavior.
- Extended the mechanical Test gate to validate linked novelty and pressure
  receipt identity, shape, coverage state, claim mapping, and pilot projection.

## 0.3.0 · 2026-09-08

- Split Ideation into Discovery-style numbered capability families:
  `1_generate`, `2_test`, and `3_select`.
- Added directly invocable specialists for candidate generation, test
  orchestration, claim-level novelty checks, feasibility pressure testing,
  journal fit, Nature-family editorial review, and human selection.
- Added a deterministic stage-gate checker and an end-to-end specimen so the
  family is executable rather than schema-only.
- Added the I1/I2 `paper-ideation-sync` adapter so one evergreen Paper P0 Page
  continuously presents the Discovery Landscape, Opportunity Map, changing
  Idea portfolio, and Test Matrix before selection.
- Kept `workflow/selection.yaml` as the single human decision authority; the
  final handoff lets Paper project verdict/target/`went to` without creating a
  second G0 decision.
- Closed the first fresh-context field-test gaps with manifest/Generate/sync
  schemas, context-only evidence entries, claim-to-matrix projection,
  receipt-linked matrix rows, and clearer HOLD/checker behavior.

## 0.2.2 · 2026-09-08

- Updated the Paper P0 handoff target to `haipipe-paper-ideation` after the
  Ideation contract moved into the Paper journey-phase family.

## 0.2.1 · 2026-09-07

- Closed fresh-agent retrofit gaps: canonical zero-padded Idea aliases,
  explicit PROCEED WITH CAUTION selection mapping, retrospective-pilot rules,
  broad-only Venue candidates, and legacy Story role/path bindings.
- Defined a bounded read-only audit mode that reports missing owner receipts as
  HOLD without recursively crawling Page machinery or inventing history.
- Made Venue-contract currentness machine-testable and aligned intended-target
  ownership at G0 with Story-owned operational confirmation and later rebinds.

## 0.2.0 · 2026-09-07

- Added a two-pass Idea × Venue Fit protocol: every admitted idea receives a
  broad screen, while live finalists receive evidence-bound deep fit against
  current versioned Venue contracts.
- Added explicit journal-family, article-type, desk-risk, missing-evidence,
  reroute, and human target-decision fields without converting venue fit into
  a prestige score or acceptance prediction.
- Extended the selection and Paper handoff gates so each selected idea carries
  its own human-selected target/category and Venue Fit/contract paths.

## 0.1.9 · 2026-09-07

- Consume the live Discovery Search → Review → Synthesize contract.
- Remove the claim that Discovery Idea pages or the old `haipipe-discovery-idea`
  route remain readable; Discovery now rejects that family and hands only
  checked synthesis Pages into semantic ideation.

## 0.1.8 · 260907

- Defined admission at stable `iNN` assignment: admitted cards remain durable,
  while rejected pre-admission framings may be recorded without invented
  cards or divisions.

## 0.1.7 · 260907

- The Paper P0 handoff target is `haipipe-page-ideation` (renamed from
  `haipipe-paper-ideation`, now under `paper/page-types/`). Written by Claude Peer.

## 0.1.6 · 2026-09-07

- Made the candidate set explicitly dynamic and separated comparison order
  from human selection.
- Made `novelty_check` an explicit per-Core-Claim record and added distinct
  Story routes when several cards are selected.

## 0.1.5 · 2026-09-07

- Link the semantic layer to the Discovery BJTR retrofit and clarify that
  ideation may reuse bNN/jNN/tNN naming but never commissions a local Run.

## 0.1.4 · 2026-09-07

- Removed Bib-only source entries from the bundle schema; Bib remains a
  projection linked through its owning Discovery Result and runtime.

## 0.1.3 · 2026-09-07

- Defined Discovery reading-depth ordering for safe Result reuse.
- Closed the novelty gate: unresolved claims can defer or abandon, but cannot
  enter a selected Paper handoff; partial deltas require an explicit risk.

## 0.1.2 · 2026-09-07

- Bound Discovery runtime operations to the paper/source Subject contract.
- Defined material reuse changes and clarified when a Task QA can serve as a
  feasibility receipt.

## 0.1.1 · 2026-09-07

- Made the external runtime receipt an explicit same-stem bundle/return pointer.
- Clarified that Task QA and Task Result may appear independently or as
  separate sources, and that Discovery channel lists are instantiated from
  Scope.

## 0.1.0 · 2026-09-07

- Added the top-level semantic ideation door between Task/Discovery execution
  and Paper P0.
- Defined pointer-based internal+external evidence bundles, provenance and
  reuse/request rules for Discovery search, Direction/Idea Cards, the semantic
  pressure-test boundary, and the human-gated Paper handoff.
- Preserved owner-native BJTR, Run/Result, and Bib contracts; legacy Discovery
  `3_idea` history remains readable.
