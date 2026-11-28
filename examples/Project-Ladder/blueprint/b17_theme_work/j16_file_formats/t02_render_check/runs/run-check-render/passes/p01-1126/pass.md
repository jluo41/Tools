# first render round

## Ask

render every file of the 8 kinds under examples/

## Summary

16 of 769 files fail, all one kind of problem: a Job or Task page of the cowork, discovery and labeling themes does not show its goal: line (8 Job faces, 8 Task faces). Block faces, Run cards, rounds, traces, Studio topics and page specs all render; b17 alone has none. 47 s over all of examples/. The 16 belong to those themes' own pages, so they go to their sessions.

## Changed

- `plugins/haipipe-toolkit/servers/workbench/checks/render_check.py`
- `examples/Project-Ladder/blueprint/b17_theme_work/delivery/page-spec/file-formats.md`

## Results

```text
✅ Block face: 21 files, 0 problems
❗ Job face: examples/Project-Ladder/cowork/b01_example_cowork/j00_people/j00_people.md: does not show its goal (Who to ask for help in this Block, by ro…)
❗ Job face: examples/Project-Ladder/cowork/b01_example_cowork/j01_data_access_request/j01_data_access_request.md: does not show its goal (The partner office sends the extract wit…)
❗ Job face: examples/Project-Ladder/cowork/b01_example_cowork/j02_review_board_amendment/j02_review_board_amendment.md: does not show its goal (The review board approves the amendment …)
❗ Job face: examples/Project-Ladder/cowork/b01_example_cowork/j03_kickoff_meeting/j03_kickoff_meeting.md: does not show its goal (The partner office and our team agree wh…)
❗ Job face: examples/Project-Ladder/discovery/b01_example_discovery/j01_policy_effect_inquiry/j01_policy_effect_inquiry.md: does not show its goal (Read the earlier studies of <the policy>…)
❗ Job face: examples/Project-Ladder/discovery/b01_example_discovery/j02_subgroup_effect_inquiry/j02_subgroup_effect_inquiry.md: does not show its goal (Find earlier work that looked at <the po…)
❗ Job face: examples/Project-Ladder/labeling/b01_labeling_example/j01_example_response_safety/j01_example_response_safety.md: does not show its goal (Run the two loops on 30 synthetic chats.…)
❗ Job face: examples/Project-Ladder/labeling/b02_labeling_walkthrough/j01_example_response_safety/j01_example_response_safety.md: does not show its goal (Run the two loops on 30 synthetic chats.…)
❗ Job face: 52 files, 8 problems
❗ Task face: examples/Project-Ladder/cowork/b01_example_cowork/j02_review_board_amendment/t01_data_use_plan/t01_data_use_plan.md: does not show its goal (The data-use plan the review board reads…)
❗ Task face: examples/Project-Ladder/discovery/b01_example_discovery/j01_policy_effect_inquiry/t01_policy_prior_work/t01_policy_prior_work.md: does not show its goal (What did earlier work find about <the po…)
❗ Task face: examples/Project-Ladder/discovery/b01_example_discovery/j02_subgroup_effect_inquiry/t01_subgroup_prior_work/t01_subgroup_prior_work.md: does not show its goal (Did any earlier work look at the effect …)
❗ Task face: examples/Project-Ladder/labeling/b01_labeling_example/j01_example_response_safety/t03_example_meaning/t03_example_meaning.md: does not show its goal (Loop by loop, ask the person how flagged…)
❗ Task face: examples/Project-Ladder/labeling/b01_labeling_example/j01_example_response_safety/t04_example_expression/t04_example_expression.md: does not show its goal (Rewrite the wording under the approved m…)
❗ Task face: examples/Project-Ladder/labeling/b02_labeling_walkthrough/j01_example_response_safety/t01_example_items/t01_example_items.md: does not show its goal (Turn the Job's 30 synthetic chats into t…)
❗ Task face: examples/Project-Ladder/labeling/b02_labeling_walkthrough/j01_example_response_safety/t03_example_meaning/t03_example_meaning.md: does not show its goal (Loop by loop, ask the person how flagged…)
❗ Task face: examples/Project-Ladder/labeling/b02_labeling_walkthrough/j01_example_response_safety/t04_example_expression/t04_example_expression.md: does not show its goal (Rewrite the wording under the approved m…)
❗ Task face: 76 files, 8 problems
✅ Run card: 124 files, 0 problems
✅ Run round (pass): 104 files, 0 problems
✅ Trace: 141 files, 0 problems
✅ Studio topic face: 234 files, 0 problems
✅ Page spec views table: 17 files, 0 problems
❗ render check: 16 problems in 47 s
```
