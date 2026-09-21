# Fresh-context validation observations

The eight-venue brief-only workflow is understandable and the ordinary contract/presenter path works. The uncommissioned proposal has eight registered items and zero Runs; the synthetic ordinary portfolio has 24 clean Run records and eight ready projections. Validation discovered a Delivery integrity bug, then confirmed the parent's repair with the same corruption specimen and unchanged assertions. All 20 final checks pass. Final narrow documentation rereads resolved the venue-list, word-budget, brief-only scope, reminder scope/reviewer boundary and fixture-goal findings; the historical fixture default is intentionally retained. No unresolved finding remains from this validation.

## 1. Ready delivery can expose changed, unverified bytes

**Priority at discovery: high; repaired and revalidated.** On the first run, `plugins/haipipe-toolkit/skills/board/haipipe-board/live/design.py:519`, `_verified_design`, selected an item by state and a completed Verify verdict, then returned the artifact's current text and stored hash at lines 542–544. `design_snapshot` populated ready before independently returning audit findings. `live/designboard.py:483` used `item.ready` for CSV inclusion without excluding invalid hashes.

The synthetic specimen was created with a passing Generate and Verify, then its `content/sms.txt` was explicitly changed as a corruption fixture. The checker correctly reported the changed artifact. Before repair, both the Page projection and actual CSV helper returned:

- State: `ready`.
- Text: `CORRUPTED AFTER VERIFICATION; this is not the approved artifact.`
- Reported hash: `30a3850884c26baa42f490313b04a20b4951e414b33627f43a6f981384204f72`.
- Actual artifact hash: `2e953567e6e2f14292c7c68137c95e72fba9280225cb4f62df1aa3a9b3ab4e30`.

That violated the stated exact-draft handoff and clean-records requirement in `design/haipipe-design/SKILL.md` under Closure. The parent repaired `_verified_design` to revalidate the Generate/Verify chain. The exact specimen now displays `records invalid`, `ready: null`, a named repair owner with the hash-mismatch reason, and zero CSV rows. The unchanged ordinary portfolio still has eight ready items, eight exported rows and no audit findings. The checker still reports the corruption, as expected.

Original evidence is preserved under [before-repair](/tmp/design-workflow-validation-20260920/checks/before-repair/executed-checks.json), including [the original CSV](/tmp/design-workflow-validation-20260920/checks/before-repair/tampered-export.csv) and [original hashes](/tmp/design-workflow-validation-20260920/checks/before-repair/tampered-export.json). Current evidence: [repaired behavior](/tmp/design-workflow-validation-20260920/checks/repaired-behavior.json), [snapshot](/tmp/design-workflow-validation-20260920/checks/tampered-ready-snapshot.json), [header-only CSV](/tmp/design-workflow-validation-20260920/checks/tampered-export.csv), and [CLI results](/tmp/design-workflow-validation-20260920/checks/cli-audits.json). The read-only reproduction invokes `design_snapshot` and `bundle_csv`, not a hand-built imitation of export logic.

The first whole-harness rerun exposed a harness isolation issue: the held fixture's later synthetic release remained on disk when recording its earlier held state. The harness now recreates only its own temporary `fixtures/edges/held` folder before constructing those two states; no assertion was weakened. The next full run passed all 20 checks.

## 2. Blocked/HOLD wording changed during validation

**Resolved on final reread.** The first `design/haipipe-design-workflow/SKILL.md` read said: `HOLD is a person's decision at Commission, and a blocked receipt shows as hold.` That conflicted with `references/run-profile.md`, the plugin state mapping, and `live/design.py:320`, which correctly display a separate blocked state.

The current text at `design/haipipe-design-workflow/SKILL.md:180` now says Commission HOLD displays as `commission held`, while blocked names the affected Run/repair owner and offers no release action. The fixture confirms the current behavior. This validator made no repository edit; the source changed concurrently, so the earlier conflict is not an outstanding finding.

## 3. Brief venue examples look like a restricted list

**Resolved on final narrow reread.** `design/haipipe-design-brief/SKILL.md:79` now explicitly lists all eight supplied guides: SMS, UI card, email, push, reminder, checklist, report and dashboard. This matches the eight-venue Brief and the already-validated parser/CSV behavior.

## 4. Venue defaults need explicit scope resolution for this scenario

**Resolved.** `design/venue/_SCHEMA.md:16` now requires the caller to resolve venue defaults to the requested audience/scope before release, with an explicit word budget and `unit.shape/count`. Its brief-only rule labels sample values and missing sources and forbids claiming accepted findings, live refresh or production readiness from examples. This directly supports the existing library Brief, scope/gap report and synthetic dashboard specification.

`design/venue/venue-reminder/style-profile.md:23` now makes 3–5 variants a rotating-set default and says the released shape/count fixes scope. Its checklist at line 34 checks the commissioned count. The final narrow reread confirms that `venue-reminder/README.md:53` places drafting under Commission and Generate, follows the frozen count, and keeps a commissioned single example single. Verify at line 58 checks every commissioned reminder against frozen shape/count and explicitly forbids drafting replacement variants. This matches the Unit contract and the existing one-example walkthrough.

**Report budget resolved.** `design/venue/venue-report/README.md:9` now labels 600–2000 words as typical full-report length, permits shorter audience-specific briefs, and instructs the caller to freeze one explicit budget instead of combining the range and cap. The executive cap in the style profile is therefore no longer an exactly-600-word constraint. The walkthrough already asks the caller to set an explicit budget and describes its short report as an excerpt; no artifact change is needed.

## 5. Fixture helper defaults can obscure the current workflow

**Historical default intentionally retained and documented.** `board/haipipe-board/tests/fixture_design_v2.py:59` still defaults `ItemSpec.stage` to `adopted`, with an explicit comment: `historical demo default; current cases choose "verified"`. This preserves historical fixtures rather than changing the current Commission → Generate → Verify workflow. The `JL` fixture label also remains; this simulation continues to override it with unmistakably synthetic actor labels. These retained defaults do not imply actual authorization and no longer constitute an unexplained current-workflow discrepancy.

**Goal mapping resolved.** The helper's `config` method at `fixture_design_v2.py:183` now writes `goal: spec.goal`, matching `design_intent.move` and the Unit contract. The existing eight specimens already used equal title and goal, so this correction does not invalidate their bytes or their prior 20/20 checks.

## 6. Paths and successful behavior

No broken explicit relative Markdown link was found in the selected Design skill/reference set (3 checked). All eight venue directories/profiles used exist. The scope of this check is recorded in [explicit-relative-links.json](/tmp/design-workflow-validation-20260920/checks/explicit-relative-links.json).

The following worked: brief-only basis without an InsightBoard; Brief list parsing; eight venue kinds; immutable held-decision preservation with a later Commission identity; distinct blocked state; completed review rejection routing; historical Adopt id/type preservation; declined item exclusion; v1 folder refusal; static Board download suppression; and presenter read-only behavior. The synthetic reviewer records establish none of actual independence, semantic quality, human authorization, visual quality, Page closure or readiness to send.

The final clarification passes reread only the relevant changed guidance/helper portions and compared them with the existing Brief and walkthrough; the last pass checked only the reminder Run guidance paragraph. They updated this observation record and the reminder guidance sentence in the walkthrough only. They did not regenerate fixtures, alter saved Run Results, rerun unrelated tests, or write repository files. The previously executed behavior suite remains 20/20.
