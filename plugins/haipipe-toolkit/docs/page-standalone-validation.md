# Standalone Page extraction · 2026-09-12

## Delivered boundary

The canonical Page family lives in `skills/page/`, outside `skills/board/`.
`haipipe-page/cli/page.py` provides `init`, `inspect`, `build` and `serve`.
Its file-backed runtime is standard-library Python 3.11+ and can run when only
the Page engine directory is copied, without Board modules or `board.md`.

One imported file becomes one byte-preserved editable copy beneath
`outline/evidence/materials/`. The Page Face declares `source-content:` and
`page.toml` records the binding. Both independent and Board rendering consume
that same source. Static exports are derived copies, never editable authority.

Board owns discovery, membership, groups, navigation, aggregate checking and
hosting adapters. Existing module paths forward to Page-owned implementations.
Old skill paths remain compatibility links; installed skill links were refreshed.
Existing Board discovery is bounded by its source tree; outside-folder membership
is not implemented by inventing copies or symlinks.

## Validation performed

- Page runtime and HTTP suite: 30 tests passed. Covers file fidelity, static
  assets, relocation, isolated runtime copy, hashes/conflicts, authentication,
  read-only mode, malformed writes, private files, traversal, symlinks,
  per-request source binding, opaque-origin HTML, and declared downloads.
- Browser exercise: imported HTML initially selected in Source; edited HTML
  through the browser, saved, refreshed and verified the rendered change;
  original input unchanged; test edit restored through the same editor.
- Desktop at 1280 px and mobile at 390 px: no script errors; mobile document
  has no horizontal overflow. HTML stylesheet loads and computed styling was
  checked. Test listeners were loopback-only and closed after verification.
- Moved workflow/content/export tests: 14 passed.
- Existing Outline preview/comment/logic tests: 34 passed.
- Registered Page/Board integration: 33 passed, plus 5 existing reroot tests.
  Fresh official Markdown/text/HTML imports build with relative and absolute
  Board roots and pass source-specific strict checking with zero findings
  (`--strict --no-template`). The default checker still includes the unrelated
  global template findings noted below.
- Full Board regression suite: 612 passed, the same 5 baseline failures remain.
  A legacy parser smoke test also passes on Python 3.9.6; registered Page
  features explicitly require Python 3.11+.
- Fresh-context Page skill tests used new HTML/CSS fixtures, the documented
  interpreter/CLI, scoped title edits, byte comparisons and export checks.
  Agents did not create a Board, research workflow, PDF, or invented acceptance
  for technical file intake. Main inspected process reports and browser evidence.
- Fresh-context integration testing caught short-Page length assumptions and
  registration/checker disagreement; these became focused regression tests.
- The final fresh-context Board/Page rerun passed both builds with exactly one
  Page and no editable-content duplication; source-specific findings were zero.
  It correctly reported the remaining global template strict-check failure
  instead of claiming an overall clean scholarly check or starting hosting.

## Preserved unrelated baseline failures

The broad Board suite has five pre-existing Task/Discovery contract failures.
They were verified against Tools HEAD
`6dd2ee81f07b348eed71b47a55078ef1c6bf1964` using the baseline assertions and
contract text in memory, without a checkout or modifications:

| Test | Baseline mismatch |
|---|---|
| `runs_is_optional_presenter_beneath_task_face` | Task skill lacks the asserted Runs presenter wording |
| `task_page_contract_is_owned_by_task_door` | Task skill lacks `legacy_page_type: task` |
| `x2_has_a_deterministic_task_inbox_packet` | Task skill lacks the asserted incoming candidates wording |
| `task_contract_uses_run_results` | Task skill lacks `Runs/Results` |
| `application_phase_family_is_complete` | Discovery workflow key does not end in `-workflow` |

These are not claimed as passing or repaired by the Page extraction.
The default aggregate checker additionally reports a pre-existing global
template-renderer mismatch and five template gaps. Baseline template bytes and
relevant checker/renderer logic match HEAD: its short `text` fences render as
diagrams while the checker expects `details.codef`. This was not repaired by
weakening legacy checks or rewriting unrelated templates.

## Hosting and scope

`build` makes a static reading bundle under `delivery/web/`; it does not start
a host. `serve` adds source saving and the shared Outline/Evidence workspaces.
Non-loopback writable serving requires authentication. Reader-facing URLs in
Physician-SPACE must use the configured Tailscale origin. No persistent service,
public deployment, private-source upload, commit or push was performed here.

Network resources are not downloaded. Static dependencies are copied within
the declared input directory; missing or escaping assets fail explicitly.
Runtime JavaScript imports/fetches, bundlers, SPA routing and application
backends are not automatically packaged. Advanced scholarly workflows retain
their own skills and gates; the standalone technical path does not invoke them.
