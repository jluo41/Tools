# Comprehensive review: View Page, resource unit, Display, and consumer contracts

Date: 260811

Mode: review only; no View skill, specimen, or application semantics changed.

## Verdict

The core architecture should be retained:

```text
QA Probes ──▶ one canonical <ViewStem>.md ──▶ 0..n first-class Displays
                         │
                         └──────────────────▶ 0..n downstream Consumers

views/<ViewStem>/         authored resources
_fixture/                 regenerated, source-free distribution
```

The skill is not yet ready to be called complete or applied to the MISQ paper. The normal path is green, but the validator does not yet enforce several contracts that the prose claims it enforces.

## Evidence collected

- Board strict check: 10 Pages, 0 findings.
- Both View skills pass quick validation.
- Existing View unit tests: 3 passed.
- Current QBt1 validates and its fixture passes freshness checking.
- A fresh Codex agent discovered `haipipe-view` and `haipipe-page-for-view` without being told their paths.
- Nine deliberately invalid View scenarios were then tested. All nine were incorrectly accepted.
- The path-traversal scenario returned build success and then failed an immediate `build --check`, proving build/check inconsistency.

## Must fix before application

| Priority | Gap | Current false-green behavior | Required contract |
|---|---|---|---|
| P0 | Canonical Page identity | Missing `page-type: view`, wrong/missing `view-unit`, and Page/manifest title disagreement pass | Validate the Page header, exact resource path, and one title source of truth |
| P0 | Display intake contract | View validates only flat `display_id` and `kind`; QBt1 does not satisfy the generic nested provenance/snapshot schema | Parse the generic intake schema and invoke its kind-aware validator |
| P0 | Path confinement | `preview_image` and `preview_pdf` may escape the Display folder with `../` | Require safe basenames or confined normalized relative paths before build |
| P0 | Card semantics | A Card anchor may be absent from its adjacent sentence; a Display may bind nonexistent Card IDs; an evidence Card may bind `_fixture` | Build a Card index, validate exact adjacent spans, uniqueness, Card IDs, and authored-source boundaries |
| P0 | Consumer handoff | Duplicate Consumer IDs and `handed-off` status pass while View/Display gates remain waiting | Compute consumer-specific eligibility from `uses`; block handoff unless every relevant gate is accepted |
| P1 | View Content structure | Required divisions are checked only as substrings, so duplicates and wrong order pass | Parse exactly one ordered sequence: QA inputs, View body, Displays, Consumers |
| P1 | Probe readiness | A declared “answered” Probe may be empty | Require nonempty, parseable Probe content or an explicit readiness field |
| P1 | Build transaction | Replacement deletes the current owned fixture before the staged copy completes | Replace by rename/swap so the previous valid fixture survives copy failure |

## Contract contradictions to resolve

1. The generic Display intake template uses `schema: haipipe-display-intake/v1`, nested `display`, `origin`, and `snapshot` records. The View engine and QBt1 specimen use a simpler private schema.
2. Generic renderer assets are kind-specific (`table-body.tex`, `figure.pdf`, `figure.svg`, or `figure.png`), while the specimen uses partly different names and the View engine does not validate kind-specific assets.
3. The View engine allows `text` and `ledger` as rendered Display kinds, but the generic Display family currently defines renderer contracts only for table, figure, diagram, and illustration. Either define renderer/output contracts for text and ledger or keep them as View-body/Card material rather than renderer-complete Display kinds.
4. The Page Type template correctly declares `page-type: view` and `view-unit`, but the canonical QBt1 specimen omits both; the generic Board checker cannot infer the omission.
5. The Base Page contract specifies emoji-bearing Aim group headings, while the View template and specimen omit them. Decide one rule and validate it consistently.

## Browser and receipt integrity

- `check_cards.py` embeds one machine's Tailscale address. It should derive the Board URL from `HAIPIPE_BOARD_URL` or accept `--url`.
- The checked-in QBt1 browser report is stale: it still records the former `QS-consumers/S-Main-4-results.md` route although the current Page uses `QBt-page-types/consumer/S-Main-4-results.md`.
- The receipt proves successful clicks only. Add at least one failure-injection browser test for a missing or ambiguous Card span.
- Historical `_runs/skill-forward/` receipts contain obsolete layouts. Preserve them as history, but mark/index them as legacy so fresh agents do not treat them as current contracts.

## Skill discovery and routing

Natural skill discovery works. A fresh agent selected both View skills. However, it also selected the paper-specific `haipipe-page-for-display` for a View-owned table. The View skill should explicitly route each Display kind to the generic renderer family and state that paper-specific Display Pages are downstream adapters, not View authoring dependencies.

## What should remain unchanged

- One canonical `<ViewStem>.md`; no duplicate `view.md`.
- Same-named `views/<ViewStem>/` resource folder.
- Multiple QA Probes, zero or more draft Displays, one or more deliverable Displays when needed, and multiple consumers.
- View-owned readable body plus Citation, Value, Display, and Consumer Cards.
- Display-owned artifact and independent human acceptance.
- `_fixture/` as regenerated, source-free distribution with bibliography collision protection.
- Consumer-owned prose placement.

## Recommended repair order

1. Write negative tests for all nine accepted-invalid scenarios and make them fail for the right reason.
2. Repair Page identity, path confinement, Card indexing, ordered divisions, and consumer gate computation.
3. Replace the View-private Display intake checks with the generic Display contract and kind-specific renderer validation.
4. Refresh QBt1 to satisfy the repaired contract, regenerate its fixture, and rerun browser acceptance with a portable URL.
5. Run a fresh-context skill execution again. Only then mark the View skill complete and begin the MISQ application inventory.

## Review boundary

This review did not change the MISQ paper, the View skill, the specimen, or generated application files. It only added this review receipt.
