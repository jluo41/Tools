# Design Run guidance follow-up

Date: 2026-09-21. Scope: the Design Page and Design Board plugin family, in the existing local Tools-SPACE checkout.

## Changes

Each Space now has an expandable **Run types in this Space** section. The Run Type catalogue describes the plain name, canonical Type, bounded purpose, owner Skill, worker Skill/dispatcher, actor role and prerequisites. A separate section lists current matching records with their real Run IDs, actors, status and outcome. The complete historical ledger remains in Run Space.

| Space | Applicable Design Run Types | Capability shown |
|---|---|---|
| Goal | `Design.commission` | Shown here · read-only |
| Design | `Design.commission`, `Design.generate`, `Design.verify` | Start here for eligible live Page controls; Copy request → paste and send for eligible Generate/Verify work; otherwise Shown here · read-only |
| Insight | Commission, Generate, Verify as consumers of allowed sources | Shown here · read-only |
| Run | Commission, Generate, Verify, with the existing actual Run ledger | Shown here · read-only |
| Delivery | Generate and independent Verify supporting ready items | Shown here · read-only |

The Board offers contextual chat copy for eligible items in Design Space and links to the Page's native item controls. The Board does not allocate Design Runs. Its existing task-list and folder operations retain their separate scope.

### Each Design Item

The open Page-level item states its next eligible Run and actor:

- **Commission · person**: release or hold the item's exact goal, rules and sources.
- **Generate · agent**: create or revise the released design, then check every rule.
- **Verify · independent agent**: review the exact completed draft against the released criteria.

The explanation includes the selected item/target, canonical Type, `haipipe-design-workflow` owner, worker `haipipe-design-unit` where applicable, prerequisites, released Commission, latest complete draft, and latest matching Run/status. Commission is a human decision with no worker Skill. The agent dispatcher is identified separately in the worker description.

Eligibility reads the existing `_ALLOWED` state mapping and held-Commission rule. The native Release/Hold, Queue Generate, Queue revise, Queue Verify and stale-queue replacement controls remain the actions. Queueing explicitly means recording work for the dispatcher; it does not claim an agent already executed it.

Queued/running items explain their current Run. Blocked, unresolved, invalid-record and ready items gain no start action. Existing reasons and repair owners are retained. Historical Adopt records retain their real IDs and historical labels, and do not enter the current Type catalogue.

Board Item rows provide the same explanation in an expandable cell, use their own folder's human context, and link to **Open item controls** on that item's Design Space. Page and Board ledger rows now include canonical Type and bounded target beside the plain Run name.

### Contextual chat copy

The Page and Board Design Spaces now offer **Copy prompt to chat** for an eligible next Generate/Verify, or one compatible planned Run already queued for the item. The prompt preview and copied text identify the exact Board, Folder, Page, item, target, canonical Type, actor role, owner/worker Skills and their paths, prerequisites, released Commission, current matching Run/receipt and next permitted action. Board prompts use each item's own Folder snapshot.

| State or condition | Chat copy |
|---|---|
| Commissioned / revise requested | New Generate, subject to rereading the owner gate |
| Generated / repaired Verify-invalid state with a clean audit | New Verify, subject to fresh independent review |
| Generate queued / Verify queued | Reuse the one compatible planned Run by its exact id |
| Revision needs feedback | Use the native queue form first; then copy the queued revision |
| Commission, running, stale, blocked, unresolved, invalid records, ready or declined | No prompt |
| Folder audit findings, missing/blocked Insight bindings, legacy or static view | No prompt |

The audit suppression is conservative: any finding in the owning Folder suppresses its chat prompts, including findings on another item. It does not change the native state or gate behavior.

The prompt requires chat to reread state and the owner contract before acting, reuse compatible queued work, report running/completed work without duplicating it, and stop when state or prerequisites no longer match. It forbids inferred Commission release/hold, requires a genuinely fresh independent reviewer for Verify, uses frozen base/feedback for queued revisions, and stops after one Run with its actual id, Ticket/Result/receipt paths, status and verdict/route. It cannot silently advance through the workflow.

### Side effects and ownership

Reading or expanding the guide only renders the existing snapshot. Copying changes only the clipboard, with explicit paste-and-send instructions and a manual-copy preview fallback. It performs no allocation, repository write, queue, dispatch or send. The copy button is separate from native mutation buttons and has no action endpoint. The existing shared clipboard helper is reused unchanged.

The existing mutation dispatcher, action implementations and gates were not changed. Static Page cards now omit item mutation forms, consistently with their read-only guidance and the existing static batch suppression. Live native controls are preserved. Delivery remains read-only and creates no Run.

## Files changed

| File | Change |
|---|---|
| [servers/workbench-design/design.py](../../plugins/haipipe-toolkit/servers/workbench-design/design.py) | Design-only type descriptions and item guidance; contextual prompt eligibility/composition and clipboard binding; Space integration; canonical Type/target in ledger; static card control suppression |
| [servers/workbench-design/designboard.py](../../plugins/haipipe-toolkit/servers/workbench-design/designboard.py) | Space guidance; per-folder actor and chat context; item-control links; canonical Type/target in ledger |
| [Page SKILL.md](../../plugins/haipipe-toolkit/skills/design/haipipe-workbench-design/SKILL.md) | Guidance contract, native action boundaries and canonical Type/Skill naming; version 0.11.2 |
| [Page mapping](../../plugins/haipipe-toolkit/skills/design/haipipe-workbench-design/ref/space-mapping.md) | Space applicability, matching records and static/live capabilities |
| [Page changelog](../../plugins/haipipe-toolkit/skills/design/haipipe-workbench-design/CHANGELOG.md) | 2026-09-21 follow-up record |
| [Board SKILL.md](../../plugins/haipipe-toolkit/skills/design/haipipe-workbench-design/SKILL.md) | Board Run guidance, contextual clipboard copy and native item-control routing; version 0.7.2 |
| [Board mapping](../../plugins/haipipe-toolkit/skills/design/haipipe-workbench-design/ref/space-mapping.md) | Run catalogue versus actual instances and Page control links |
| [Board changelog](../../plugins/haipipe-toolkit/skills/design/haipipe-workbench-design/CHANGELOG.md) | 2026-09-21 follow-up record |
| This report | Scope, behavior, changed files and validation limits |

The four Design owner/worker skills remain at 0.4.0. No package, installer or marketplace inventory changes were required.

## Review and validation limits

**No tests were added or run**, as explicitly requested. No browser session, fixture execution, syntax compilation or fresh-context skill test was run for this follow-up. The prior Design repair's test results do not certify these new changes.

Review consisted of reading the current owner contracts, native controls and state gates, inspecting the scoped source diff, and running `git diff --check` for these eight changed files; the whitespace check returned no findings. Runtime behavior and visual layout remain unverified in this follow-up.

The existing checkout was used throughout. Pre-existing Labeling edits and dirty submodules were left untouched. No worktree was created, no branch was switched, and no commit or push was made.

## Shared work

No shared change is required for the scoped Design implementation. Shared UI helpers, styles and central Run catalogue files were left untouched. The existing `servers/_host/assets/js/05-prompt-copy.js` is loaded unchanged; Design-specific composition, eligibility and binding live in the existing Design-family module and are consumed only by the Design Page/Board presenters. The preview uses existing text styling.

If a future shared catalogue consumes Design metadata, its required interface is: `Design.commission`, `Design.generate`, `Design.verify`; owner `haipipe-design-workflow`; human Commission with no worker; Generate/Verify worker `haipipe-design-unit`; independent actor requirement for Verify; item-specific eligibility from the native state mapping; and navigation to the selected item's Design Space. It must not allocate a fourth Delivery Run, restore Adopt writes, or substitute a generic send/start action for the native controls.
