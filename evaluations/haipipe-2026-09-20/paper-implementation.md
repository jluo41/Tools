# Paper implementation record · 2026-09-20

Implemented the authorized [findings and fix plan](paper-findings-and-fix-plan.md).
The original [evaluation](paper.md) and plan are retained without rewriting their
historical findings. This record describes the resulting working-tree changes;
no commit, installation, publication or manuscript release was performed.

## Routing and ownership

Paper and Page now explicitly route semantic ideation to `haipipe-ideation`
and the requested generation/testing/selection capability. For an actual Paper
Ideation Page, the Page owner loads the Paper adapter, which preserves the
semantic owner's cards, working/released/delivery surfaces and sole I3 decision.
A generic Page loads only its resolved owner and the needed dependencies.

The Paper umbrella names the conditional roles of Ideation, Discovery, Task,
Run, Page, Outline, Delivery, Display, Paper Plugin and Board. The canonical
Paper Workflow defines 11 parameterized Run Specs, native identities,
dependencies, routes and completion. The plugin projects that definition
through five Spaces. Setup, I3, routing, gates, Page controller passes and
CHECK remain controls unless a native contract commissions bounded work.

## Plan coverage

| Finding | Implemented change |
|---|---|
| F01 | Required config/schema and generated-path validation precede mutation; only generated `delivery/latex` is accepted as the room. Input overlap, traversal and symlink escape checks protect sources. The example includes `[pages]` and required output fields. |
| F02 | Canonical Run Spec/Runtime reference, native compile/response receipt profiles, updated umbrella/Workflow/PageTypes/README and removal of active P0–P4 UI labels. |
| F03 | Versioned contract interface and consumer preflight; all 17 bank Pages receive honest partial contracts with missing sources and CHECK receipts explicit. |
| F04 | Page-owned typed RE versus independent Supporting Runs; current RP/RE/RD identities and preserved legacy receipts. |
| F05 | Current Page loading, writing/release and owner contracts replace the obsolete adapter pin and new-allocation guidance. |
| F06 | Canonical 11-Spec inventory matches the plugin map; four explicit control rows include Story and Section routing. Round does not own substantive evidence Runs. |
| F07 | Current Venue template exposes seven content roles; pack-backed and CfP-only examples remain partial without fabricated observations. UNKNOWN and OWN ESTIMATE are explicit. |
| F08 | Current Venue entry/path, historical bank/template notices and migration inventory. Legacy research content remains available as source material. |
| F09 | MISQ style/profile/template/check messages distinguish measured patterns, local prescriptions and unverified official rules; healthcare/policy effect-size exception is consistent. |
| F10 | PNAS taste and Significance style are linked with distinct fit/writing roles. |
| F11 | Drawer describes all five Spaces including Delivery; copy-source documentation includes the JavaScript drawer file. |
| F12 | Ideation surfaces and sole I3 remain distinct; Round Page, controller round, writing Version and response commission are explained separately. |

Fresh-context validation also exposed two assembly integration defects. The
assembler now merges the Page's `delivery/latex/<page>-complete.bib`, paired
with the source fragment, instead of the retired bibliography lane. Missing
bibliography blocks an included cited fragment; an excluded DRAFT stub does
not require it. Citation acceptance still belongs to the Page's CITE Results.
Section identities remain stable when reading order changes; legacy indexed
IDs remain readable without automatic renaming. Printed-number checks remain.

Round validation clarified pending answer-build hashes, feedback routing,
matching human release approval and freeze/final-CHECK order. A returned
writing Version is not applied until checked and landed.

## Validation performed

### Automated checks

All checks ran locally against synthetic fixtures, without LaTeX or a real
manuscript build. Python 3.11 and already cached test dependencies were used;
no dependency installation was needed.

| Check | Result |
|---|---|
| Assembly engine and LaTeX-to-DOCX unit suites | **49 passed** |
| Paper plugin, Story blueprint, plan shape and feedback-route suites | **38 passed** |
| Skill creator `quick_validate` on nine Paper skills plus shared Page, Page Workflow and Ideation | **12 passed** |
| YAML contracts: 17 bank Pages, template, two profiles and skill example | **21 parsed and checked**; all explicitly partial |
| Canonical Spec-to-plugin-map comparison | **11 Specs and 4 controls aligned** |
| Newly introduced relative Markdown links | **27 resolved** |
| Scoped root diff and Venue submodule whitespace checks | **Passed** |

The assembly suite includes invalid room values, missing `[pages]`, unsafe
generated/input paths, symlink escapes, source sentinels, the corrected example,
current bibliography input, retired-lane exclusion and the unready DRAFT case.
The board checks cover definition/folder mapping and five-Space presentation.

Reproducible suite targets, using an environment with `pytest` and `python-docx`:

```sh
python3.11 -m pytest -q --rootdir=plugins/haipipe-toolkit/skills/paper/haipipe-paper-assemble/tests plugins/haipipe-toolkit/skills/paper/haipipe-paper-assemble/tests/test_build_delivery.py plugins/haipipe-toolkit/skills/paper/haipipe-paper-assemble/tests/test_latex_room_to_docx.py
python3.11 -m pytest -q --rootdir=plugins/haipipe-toolkit/skills/board/haipipe-board/tests plugins/haipipe-toolkit/skills/board/haipipe-board/tests/test_paper_plugin.py plugins/haipipe-toolkit/skills/board/haipipe-board/tests/test_story_blueprint.py plugins/haipipe-toolkit/skills/board/haipipe-board/tests/test_plan_shape.py plugins/haipipe-toolkit/skills/board/haipipe-board/tests/test_feedback_routes.py
```

### Fresh-context skill scenarios

Per the root README, two independent validation agents loaded the relevant
skills and simulated realistic requests without reading the parent evaluation
reports, editing the repository or performing external actions.

| Scenario | Observed behavior and corrections |
|---|---|
| Compare existing ideas through Paper/Page | Routed semantics to shared Ideation; preserved working/released/delivery differences and no second I3. |
| Same-target Section wording feedback | Used the matching RP session and internal feedback Step; evidence acceptance did not substitute for human writing acceptance. |
| Six reviewer concerns in one feedback batch | Used one Round ledger and affected owners; clarified pending answer identity, checked returned Versions and human approval before release freeze. |
| Proposed Story with two unrun studies | Preserved prospective C1–C8 content. Story CHECK did not claim study findings; one complete C8 row could be released independently subject to G3 and a current Venue contract. |
| Early DRAFT with unsafe legacy room and absent `[pages]` | Corrected configuration before invocation. Distinguished a commissioned build from a read-only audit; identified and repaired bibliography/identity drift and the excluded-DRAFT regression. |
| CfP-only workshop with supplied but unverified constraints | Produced honest UNKNOWN/source gaps, no invented exemplars, partial contract and deep-fit HOLD. |
| MISQ bank contract for a new Story release | Partial contract blocked release until source refresh and matching Page CHECK. |
| MISQ healthcare abstract with a central effect size | Permitted the meaningful effect size; distinguished local word targets/prescriptions from unknown current official limits. |

These are instruction-following simulations and focused regression checks,
not evidence of successful end-to-end rendering, external rule verification,
or human approval of a real paper.

## Compatibility and limits

- The physical `paper/workflow-phases/` path is retained for existing links,
  resolvers and installations; its four skills are PageTypes, not Phases.
- Historical Run IDs, family fields, frozen builds and source locators are
  preserved. Skill metadata versions do not promote any Page outline or approval.
- Nine Paper skill versions/changelogs were updated. Shared Page/Ideation
  changes are narrowly scoped routing additions; unrelated dirty work was retained.
- Venue source facts were not refreshed online. All 17 migrated contracts
  remain **partial**, so they cannot close deep fit, G0 or a new Story/Section
  release. Grant/patent summaries additionally need a concrete target/category.
- Unsafe build paths are rejected before mutation. A valid build still
  regenerates its generated room in place; atomic build replacement is not added.
- No new Setup Apply writer, general runtime executor or Page bibliography
  exporter was implemented. Compile/response allocation remains the caller's
  documented responsibility; the mechanical builder does not mint Runs.
- The Venue submodule worktree is modified. Its HEAD and root gitlink both
  remain `b7d3e51af3790381d00747a6356266356f0e2e51`; no pointer update or commit
  was made. Pre-existing unrelated root and reference-submodule work remains.
