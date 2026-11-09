# Labeling UI alignment verification

Checked 2026-11-08 against the current shared Work components. This record covers the blueprint clarification update; no runtime component or human gate was changed in this pass.

| Expected behavior | Verification | Result |
| --- | --- | --- |
| Every matrix Section has content requirements, source, layout and applicable skills. | Rendered all three matrices through `focus_page.ui_matrix_html` and inspected their button data. | 188 Section buttons have explanations. |
| Example links select the displayed View. | Parsed all distinct generated links and rendered each target with its actual Labeling adapter; checked the active View. | All 19 distinct routes select the requested View. Block/Job use Report; Task steps use Work. |
| Pending Task shared sections do not imply a completed migration. | Inspected Task overrides and their example mapping. | Marked pending; no example route is claimed for that target row. |
| Section explanation works in the real browser. | Opened Block UI → Signed releases and Task UI → Source Records. | Dialogs show source, layout, skills and the matching Delivery / Data link. |
| Delivery example opens real release content. | Opened the dialog’s example link. | Block Report → Delivery shows signed e02 under Review Content, followed by Around the Work. |
| Existing Labeling navigation and domain readers remain compatible. | Ran `test_labeling_focus`, `test_labeling_steps`, `test_labeling_theme`. | 50 tests passed. |
| Broader legacy compatibility is stated accurately. | Ran all workbench-labeling tests with current shared code. | 83 run: 80 passed, 2 failures and 1 error below. |

## Reproducible test commands

Use Python 3.10+ from the consuming workspace. From the Tools repository root:

```sh
PYTHONPATH=plugins/haipipe-toolkit/servers/_host:plugins/haipipe-toolkit/servers/workbench-labeling/tests python -B -m unittest test_labeling_focus test_labeling_steps test_labeling_theme -q
PYTHONPATH=plugins/haipipe-toolkit/servers/_host python -B -m unittest discover -s plugins/haipipe-toolkit/servers/workbench-labeling/tests -q
```

## Existing legacy Building gaps

- `test_other_labeling_pages_are_unchanged`: temporary fixture lacks a SPACE root `env.sh`; renderer exits while resolving the legacy page.
- `test_shell_and_rails_are_the_base_pages`: expected equality between the legacy Building rail and the newly shared base rail no longer holds.
- `test_unbuilt_steps_name_what_they_will_show_and_make_up_nothing` (staging): the numeric-content assertion sees `27` in the HTML entity `&#x27;` after stripping tags.

These same three problems were reproduced before this blueprint update. They are not marked passed and are outside the Block/Job design clarification. A fresh legacy Task migration review should address them together with the remaining Ground Truth, Building, Scanning and Score surfaces.

## Pending decisions

Task adoption of the combined Report frame remains pending. Checklist’s proposed To do / In progress / Ready for review / Passed workflow and evidence fields have not been implemented as a shared schema. Existing Markdown checklists are the current mechanism.

## Clickable Use Cases

The Block, Job and Task matrices now have clickable Use Cases using the shared `use_case_examples` template dialog. Applications remain separate from UI types. The Job label “Dataset × Label” names its business unit; all these Job cases use the same adapter.

| Level | Cases | Source basis |
| --- | --- | --- |
| Block | Response safety annotation; Clinical dialogue annotation; Symptom annotation | Authored Block spine, topic and child Job records. |
| Job | The three annotation cases; Rater label audit | Authored Job goal, topic and Tasks list, checked against child faces. |
| Items | Conversation items; Encounter transcripts; Post transcripts | Task face describes the transformation and carries `task-type: data` or `items`. |
| Meaning | Response safety definition; Rater label audit | Actual `task-type: labeling-meaning` and its goal. |
| Expression | Response safety execution | Actual `task-type: labeling-expression` and its goal. |

Public synthetic examples live in `view-guide.json` under `use_cases`; five mappings reuse the existing walkthrough. The 31 external mappings across three local SPACEs live only in the ignored `.server_config/workbench-examples.json`. Each SPACE supplies its own configured DOMAIN. Other themes’ matrix mappings are preserved. No external service was restarted and no cross-root file-serving route was added.

- All 13 Use Cases were opened and closed in the browser. Dialogs distinguish Dataset project from Blueprint example.
- Generated mappings resolve to existing page faces. All Task examples match the declared type; Job Tasks are real direct children.
- The response-safety Job dialog’s Tasks and Path were expanded across its source entries.
- A public Items Task link opened the existing Work page with its current recipe-signing state. This did not submit approval or run work.
- At 390px, the open Task case dialog with expanded Tasks and Path measured 358px wide; the page remained 390px wide, with no horizontal overflow.
- External browser probes returned an empty response, a connection reset and a connection refusal respectively. Their local entry labels record “connection check failed”. Source and configured route validity are verified; external live-page acceptance remains blocked by connectivity. These links do not claim the new UI is deployed there.
- The three shared use-case tests, seven matrix regression tests and 50 Labeling navigation/domain tests passed. Prior legacy Building failures remain as documented above.

Coverage limits: no distinct Meaning/Expression example is inferred from a legacy combined `labeling` Task. Those older Tasks remain visible as actual children of their Job. The Task matrix still covers Items, Meaning and Expression only; Ground Truth, Building, Scanning and Score have not been added as new verified columns. Missing local mappings show the shared “No linked examples yet” state rather than invented work.
