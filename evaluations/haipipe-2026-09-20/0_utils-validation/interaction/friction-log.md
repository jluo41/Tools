# Interaction validation friction log

Fixture preflight start: 2026-09-20T17:40:26-0400 (date command receipt). Source-reading overhead preceded this stamp and is not included in a runtime claim.

1. [2026-09-20T17:43:31-0400] **Unclear, minor, remote-error generic reply.** `0_utils/remote-error/SKILL.md`, reply shape, requires `// was` and `// now` inside a block “in the language of the file,” while generic fixes must match the file's style. Python does not accept `//` comments. The representative reply uses Python-native `# was`/`# now`; the source fragments themselves match the file. Literal generic marker handling could be clarified.
2. [2026-09-20T17:43:31-0400] **Self-contradictory, minor, response-format example.** `0_utils/response-format/SKILL.md`, File changes, says “End ANY turn that changed files with a ... File Changes section,” but its Example puts “What I Need From You” after File Changes. Followed the explicit rule and placed the inventory last.
3. [2026-09-20T17:43:31-0400] **Scenario limitation, not a shipped skill defect.** `0_utils/field-test/SKILL.md`, commission item ②, requires “a live artifact with history and debt — never a toy fixture”; this supplied validation explicitly requests an isolated synthetic report. Prepared a rehearsal commission and did not claim a real field run.
4. [2026-09-20T17:43:31-0400] **Missing scenario evidence, not a shipped skill defect.** `insight/haipipe-insight-workflow/ref/authorization.md` requires an actual person's source, board/runtime, bounded targets/actions and expiry. No concrete standing grant was supplied. Prepared evidence-preservation instructions and applied the already supplied direct /tmp task scope; no active Insight grant was fabricated, no approval was requested again, and no FIELD run was dispatched.
5. [2026-09-20T17:43:31-0400] **No friction, Whoop missing-checkout branch.** `0_utils/whoop-connect/SKILL.md`, Preflight, directly covers the missing configured path and stops before developer-app setup. Missing local checkout is an expected prerequisite failure, not an OAuth or token failure.

Close: 2026-09-20T17:44:59-0400 (date command receipt). Tokens: unavailable; no task usage receipt or /cost was provided. No cost estimate is asserted.

## Read-only recheck, 2026-09-20T17:48:21-0400

- Finding 1: resolved. remote-error's WHAT contract now gives valid language-specific comments and a diff fallback. The existing Python reply needs no marker workaround.
- Finding 2: resolved. response-format's example now ends with File Changes.
- Findings 3 and 4 remain scenario limitations; item 5 remains the expected missing-checkout outcome. No standing grant was supplied or applied, no FIELD run was dispatched, and no Whoop success path was exercised.

Recheck timestamps came from `date`; exact current source hashes and mechanical-check results are in validation-receipt.json. Repository sources were not modified by this validation agent.
