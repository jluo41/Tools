# Writing v2 implementation and validation

Date: 2026-09-20. Approved scope: Section 10 of
[the revised plan](writing-findings-and-fix-plan.md).

## Implemented

- `haipipe-writing` 0.20.0 is the shared draft/revise/evaluate worker for
  Page Section and Paragraph Runs and standalone file work.
- Page's bindings and Step template use the common request/return contract.
  The owning agent loads and executes the skill; YAML does not launch a model.
  Candidate, genuine changes, evaluation and method trace stay in the existing
  Run/Version/Step. Page owns adoption, delivery and human acceptance.
- Selected capabilities use a catalog and small adapters with explicit roles,
  availability, identity and output boundaries. Native writing needs no
  external method. Writing DNA and anti-slop reuse their existing adapters.
- Writing and Page CHECK share the Mechanics, Function, Evidence and
  Readability rubric. Writing records candidate-specific self-review and
  bounded revisions; CHECK retains independent whole-Page responsibilities.
- The standalone HAI humanizer's six tracked files are retired. Useful
  preservation rules, provenance and rhythm observations moved into Writing.
  The external academic-humanizer remains a separately resolved capability.
- Page uses clean Before/After records. Legacy Paper Note generation remains
  available; documentation explicitly states that `wdiff.py check` does not
  validate that format. Existing Board record behavior is preserved.

## Behavioral trials

Each session began in a fresh agent context with the skill path, raw request
and synthetic fixture inputs. Agents were not given expected verdicts or the
earlier bug report. They wrote only to their assigned temporary fixture.
External fixture skills were actual project-provided instructions read and
applied by the worker; these were same-agent method-assisted self-reviews,
not separate model reviews or calls to the unavailable upstream humanizer.

| Trial | Observed result |
|---|---|
| Section revision | Retained `rp-sec-01/v001/s002`; changed only “In order to” to “To”; reviewed both paragraph jobs and their join; executed initial/final anti-slop audits and fact-token comparison; used 1/1 revision passes and re-evaluated the final candidate. |
| Paragraph feedback, then “Keep the latest text as is” | Made exactly the requested phrase replacement, retained Run/Version and all other text; the follow-up returned the same candidate without a change card, rerating or invented Step id. |
| Two external evaluator entries | Resolved and applied both project skills through their catalog/adapters. Located changed causality, an incorrect percentage, missing raw means/citation and an unsupported inference. Returned `needs-work` without modifying the candidate. |
| Standalone native writing | Made only the requested phrase replacement without requiring Page artifacts or allocating a Run. |
| Required method missing | Returned `blocked` with the exact missing entry, no fabricated review and no revised candidate. |
| Optional method missing | Section trial recorded academic-humanizer as skipped and completed the native rubric and required anti-slop check. |
| Unsupported evaluator suggestion | Recorded and rejected a proposed randomized trial, invented numbers and replacement citation; preserved the authorized candidate exactly. |
| Missing evidence/job with zero revision budget | Marked the unrecorded 1,000-entry trial NOT VERIFIABLE, located the omitted limits/uncertainty job in C3.P2, returned the unchanged Section and owner-routed findings, and recorded zero revisions with a blocked disposition. |

Worker returns and raw inputs are retained in the temporary
[fixture directory](/private/tmp/writing-v2-g4y4par2/fixtures).
The parent checked actual outputs, exact permitted replacements and hashes of
all 28 supplied inputs; token equality was used only for preservation, not as
proof of semantic or factual correctness.

## Mechanical checks

| Check | Result |
|---|---|
| Anti-slop unit tests | 8 passed, including the migrated diagnostic-only rhythm percentages and empty input. |
| Existing diff round trips | All passed, including preservation of earlier signed records. Paper generator cases establish generation/preservation only, not Paper Note validation. |
| Skill metadata | All four changed skills passed `quick_validate.py`. |
| Agreement checker | Four skills; no version disagreements or path findings. |
| Markdown/catalog inspection | 28 changed/new Markdown files; no unresolved Markdown file links or unmatched fences; catalog parsed with unique ids and existing adapters. |
| Bash installer discovery | Executed its discovery function without installation; Writing yields only `haipipe-writing`. |
| PowerShell discovery | Statically inspected its recursive discovery and Writing candidates; only `haipipe-writing` is present. PowerShell is unavailable here, so Windows execution was not performed. |
| Whitespace | Targeted `git diff --check` passed. |
| Page interactive guards | 14 passed, 5 failed. The same 5 fail with the pre-Writing versions of touched files substituted. All five failures concern assertions about the separately edited `haipipe-run/SKILL.md`; no new guard failure was introduced by this patch. |

Commands, outputs and preservation checks are recorded in
[writing-v2-validation.json](writing-v2-validation.json).

## Practical limits and scope

- No genuine external academic-humanizer installation was found. Its adapter
  and unavailable-method behavior are implemented; upstream execution was not
  claimed. The two successful evaluator trials used explicitly supplied
  project fixture skills.
- This change implements agent-interpreted skill contracts and diagnostic
  behavior. It adds no automatic feedback listener or model scheduler, and
  does not claim an end-to-end browser execution test.
- Human acceptance and independent CHECK remain separate from self-review.
  A clear or fluent result cannot compensate for unsupported facts.
- Existing shared Page/Run edits and dirty reference submodules were preserved.
  W6's wider family topology remains outside the approved Writing v2 scope.
  Historical findings are superseded only where their replacement behavior
  was implemented and checked; this is not a blanket closure of all 15 findings.
