## 0.8.4 · 2026-09-07

- After Build, return the four-surface user-check packet: evidence to open now,
  whether Revise ran (a first draft is never presented as final), then the
  Page-level PDF as the delivery surface.
- The receipt no longer carries a `delivery_report`; when an owning build emits
  one, it names the single `delivery/build-manifest.json`, with no delivery-QA
  sibling.

## 0.8.3 · 2026-09-07

- Load the Task Page companion and require its display inventory and
  table/figure/diagram gate during CONTENT drafting and Build.

## 0.8.2 · 2026-09-07

- Require CONTENT/Build to return the shared user-check packet with the
  Outline Board URL, current Display PDFs, and current Page-level PDF.

## 0.8.1 · 2026-09-07

- Apply the Section owner's subsection-title contract during revision and
  synchronize authorized naming repairs without expanding their scope.

## 0.8.0 · 2026-09-06

- Permit explicit draft mode after local evidence work is exhausted: use an
  old accepted value plainly or one visible `[E## pending]` marker for a named
  server/person gate; final mode rejects every marker.
- Keep workflow vocabulary out of manuscript prose and shape normal paragraphs
  as 4–6 one-point sentences with a median near 21 words.
- Require a humanizer pass and fresh-context MISQ style verdict before Build;
  add writing-only review for drafts with unresolved values.
- On complete-version requests, deliver the requested PDF/LaTeX and Word,
  report pages and viewer link, and trim figure PDF margins.

## 0.7.0 · 2026-09-06

- Admit only generation `G>=1` plans to CONTENT; every `v0.*` state remains
  planning-only.
- Refresh Content for every Shape or evidence version change. Evidence-only
  revisions inherit Shape approval and revalidate only affected realizations.

## 0.6.1 · 2026-09-06

- Treat sentence length as a distribution: an 18–24-word median is a readable
  MISQ house-style center, while 30+ words triggers review rather than an
  automatic split or writing blocker.
- Split long sentences only when they stack distinct reader moves or obscure
  the main claim; preserve coherent longer relations and varied prose rhythm.

## 0.6.0 · 2026-09-06

- Add a formal OUTLINE → CONTENT entry check before any Division Writing Run.
- Separate hard authority/evidence gates from manuscript-form warnings.
- Require Section name/structure, paragraph and sentence-slot budgets, expected
  sentence length, and citation-density units to be reported distinctly.
- Measure existing and drafted prose with `haipipe-paper-section/cli/section-stats.py`;
  never present pre-draft estimates as actual prose measurements.
- Follow only the current Evidence Items' selected Local Result pointers and
  stop once each checklist row has a supported verdict.

## 0.5.0 · 2026-09-06

- Make one point per Section sentence binding during WRITE.
- For MISQ, target the outline's 23–26-word center, split routine 30+ word
  clause stacks, and avoid formulaic connective ladders and AI-style framing.

## 0.4.0 · 2026-09-06

- Forbid paragraph-level and sibling-Bullet evidence inheritance during WRITE.
  Reused sources still trace through a distinct CITE Item at every realizing
  Bullet.

## 0.3.0 · 2026-09-06

- Enforce evidence at the realization address: a citation or concrete value in
  CONTENT must have a CITE or VALUE Evidence Item on that same Bullet.
- Treat `Evidence: none` as a binding source-free contract and route any later
  material need back to OUTLINE/SHAPE.

## 0.2.1 · 2026-09-04

- Route CONTENT through the exact Page Face owner and load a canonical family
  owner only once when it also owns the Folder.

## 0.2.0 · 2026-09-04

- Remove the retired DRAFT and REVISE redirect skills and agent identities.
- Preserve their receipt tokens only in the lifecycle auditor; all current
  dispatch is CONTENT/WRITE.

## 0.1.1 · 2026-09-04

- Use the canonical Page dependency order and carry the target cycle separately
  from the phase route in CONTENT receipts.

## 0.1.0 · 2026-09-04

- Add the unified `03 CONTENT` phase with one `WRITE` cycle.
- Fold Draft, Revise, Build, and Pre-check into internal movements rather than
  separate Page phases.
- Define one normal Level-4 `Page · Division Writing` Run per commissioned
  Content division, with candidate, trace, runtime, and promotion contracts.
- Keep `04 CHECK` independent and solely authorized to close a Page.
