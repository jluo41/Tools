---
name: workbench-design
description: "Read the Design Board and Design Method Book in the shared Block workbench: execution Jobs, method Jobs, Task roles, sources and human release gates. Use for Design UI or Studio changes. Trigger: design workbench, Design Studio, design Job UI, /workbench-design."
metadata:
  version: "0.18.0"
  last_updated: "2026-11-27"
  # version history: ./CHANGELOG.md (skill-scoped, never loaded at invocation)
---

# /workbench-design · Design in the shared Block frame

Read [CONSTITUTION.md](CONSTITUTION.md) first, then load [workbench](../../../1_base/workbench/hai-workbench/SKILL.md).
The shared owner defines navigation, Bands, top views, left items and content. This skill defines Design content
and actions. Read [the ladder](../hai-design/ref/design-ladder.md) for folders and writer ownership.
Keep the metadata version unless the user explicitly authorizes a version change.

## Start from the Block

Resolve a folder containing `board.md` and read its `board-kind:`. Open that Block with `/wb`; retain its title
and route while selecting Jobs and Tasks. Do not deliver an independent Job, Task or static structure page as
the default entry. Use the running host's configured origin; when returning a reachable preview, prefer its
verified Tailscale origin. Never bake a deployment address into repository content or configuration defaults.

To review this theme, open `examples/Project-Ladder/blueprint/b12_theme_design` in Studio. To inspect real work,
use `examples/Project-Ladder/design/Design-Example` or `DesignMethodBook-Example`. Read current files before
reporting implementation coverage. A source-level render does not prove what a running service has loaded.

## Two Block contracts

| Block | What one Job owns | Main | Tasks |
|---|---|---|---|
| Design Board | One signed goal × pinned method version × frozen inputs version | Brief, Tasks, kept designs, Ranking, predicted/observed results, release gate or Delivery, Workflow and Runs, as populated | Reason ideas; each design; review whole |
| Design Method Book | One method identity with signed versions | Method, Steps, Versions, Used by, attributed proposals and existing Runs, as populated | No execution Task layer |

A Book version is a file inside the method Job, not a new Job. Its recipe steps do not create Book Tasks.
In the Board, a revision is a Run of the same design Task. Preserve the exact source Run and result paths.

Board Jobs group by the pinned method's registry family. Without a family, the reader falls back to the goal,
then Goals. Book Jobs group by authored family, registry family, then Methods. A Board Job button shows jNN,
goal id, method version and inputs version; a Book button shows jNN, method id and title. Task groups are
Ideas / Designs / Review. Groups are not types: Task faces declare `design-reason`, `design-item`, `design-whole`.
The current example Job faces do not declare a separate `job-type:` enum; do not fabricate one for a diagram.

The shared selector retains Job topic → Job → Main or Task topic → Task. Main hides the Task row. A selected
Task exposes all of its role's step tabs and its existing Runs:

- Reason ideas: inputs, chains, ideas and fence check.
- Design: draft, verification, revision and state-related evidence, including predictions when present.
- Review whole: ranking, coverage and kept designs.

`design_jobs.py` supplies these bodies through the shared Jobs selector. Empty result sections are omitted.
Board Main consolidation into Overview / Tasks / Findings is an approved design that is not implemented by this
skill edit. Verify it in code and on the running page before reporting it live. Track remaining work in
[ref/topics.md](ref/topics.md).

## Report, actions and sources

Board Report views are Designs, Goals, Inputs, Rounds, Tests and MindMap. Book Report views are Method, Versions,
Ideas, Scorecard and MindMap. Results and their actions share the current Report content. Supporting sections
use the shared frame's ordering and empty-section behavior. Explicit `view:` assignment wins; otherwise a linked
Topic must match the selected view. Do not infer assignment from a Run name or move files to fill a view.

| Content | Source |
|---|---|
| Goal and rules | `board.md ## Goals`, signed `design-goal.md`, Job goal pin |
| Method | Job method/version pin, `inputs/method.md`, Book signed `mK.md` files |
| Allowed inputs | Job `inputs/manifest.yaml`, frozen Block inputs version |
| Ideas and reasoning | t00 hard Run's `result/ideas.yaml` and `chains.yaml` |
| Design and verification | Task face, projected elements, generate/verify Results and revise passes |
| Ranking and predictions | t99 `ranking.csv`, projected `prediction.yaml` with its basis |
| Observation | Block `observed/` and score Run outputs, linked by Job and design |
| Released output | Block `delivery/`, retaining Job/Task source identity |

A copied prompt requests work; it does not approve it. The `Review and approve` control appears beside the
release content when the Job is ready. A person reads every kept design and prediction, attests and signs.
The existing `/_board/design-ladder-act` handler checks the release before writing and records both freeze and
release Runs. Never submit that action during preview validation. Opening a page grants no release approval.

Hard Runs own immutable closed `result/`; soft Runs retain `passes/`. The workflow owner projects Results into
Tasks; the delivery owner releases them. Display those records without writing or inventing a Result.

## Blueprint Studio

Use the shared `studio_types.py` and `studio_tabs.py`. Band names and order come from
`examples/Project-Ladder/blueprint/b17_theme_work/delivery/page-spec/studio-bands.json`;
Studio Type requirements come from their authored topics independently of that registry.
A Band is an outer classification, and a Studio Type defines a topic's content. Shared definitions are referenced,
not copied. A theme may define a needed type of its own; omit empty groups. Actual Work Blocks show their topics
without a mandatory type catalogue. Task procedures belong with the relevant Task type and skill; theme guidance
belongs with Theme Guide. Do not remove or renumber a real procedure or guide topic to change type definitions.

b12 has two Block Structure instances and two Block Job UI Preview instances:

| Topic | Content |
|---|---|
| s01-design | Design Board naming rules, real example and owning skills |
| s02-workbench-ui | Design Method Book naming rules, real example and owning skills |
| s11-design-job-preview | Live Board Job rows and Main content from Design-Example |
| s12-methodbook-job-preview | Live Method Job content from DesignMethodBook-Example |

For Block Structure, top views are Structure / Draw / Skills. Folder, Job / Task Organization and Studio
Organization contain rules with expandable real examples; a named example entry embeds its actual Block.
Draw uses the shared mindmap implementation. Names filled in by a work item use 〈brackets〉 in rules; actual
examples retain their recorded names. Skills opens actual owning `SKILL.md` files in the shared preview.
Keep human drawings and true folder ownership. Edit the generator before rebuilding output.

For Block Job UI Preview, Page embeds the existing real Block and Effect contains a proposal when one exists.
Do not add separate Delivery or Instances top views for this type. Keep outputs reachable in the appropriate
preview or Files. Use the existing Checklist for implementation comparisons. Do not claim checklist coverage
or a highlighted target is working merely because a preview URL returns a page.

## Validate the reader and the skill

1. Read the current reader, layout and selected example records. Record a concrete, confirmed file plan in Trace.
2. Run `python scripts/current_contract_check.py` from this skill folder. It checks the approved current-entry
   scope, owning links, manifest bindings, types against real examples and shared Band sourcing.
3. Run the relevant existing Design tests. For Studio source changes also run b12's
   `delivery/structure/build_organization.py --check` with the SPACE Python environment.
4. In the actual Block, expand and collapse nodes, switch Jobs/Main/Tasks and verify source links, Draw and Skills.
   Observe readability at the real frame width. Keep release controls untouched; do not restart a shared host
   without coordination.
5. For a changed skill, use README's fresh-context subagent invocation check. Give it a realistic task and no
   implementation hints; confirm it selected the right owners and respected their gates.

The main reader files are `servers/workbench-design/design_reader.py`, `design_jobs.py`, `design_book.py`,
`design_focus_layout.py` and `design_context.py`; release actions are in `design_ladder_act.py`.
`ref/workbench-table.md` is generated by `scripts/cards_table.py` from the workflow Run cards; edit its source
before regenerating it. No generated table is hand-maintained.

Open Files → Trace on b12 to read prompts, approved paths, changes and checks. A Trace is a recorded work episode,
not automatic full-chat capture. Keep conversation provenance there; current skill instructions state the rule.
