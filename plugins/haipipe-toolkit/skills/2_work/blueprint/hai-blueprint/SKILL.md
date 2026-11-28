---
name: hai-blueprint
description: "Coordinate a Work Block (Blueprint)'s tool, skill and workbench changes: bind the owning contracts, implementation, example and validation. Use to develop or revise reusable tooling in its blueprint Block."
---

# Blueprint

Read [CONSTITUTION.md](CONSTITUTION.md) and the repository's principle and guidance.
A Work Block (Blueprint) develops reusable tooling. Its entry skill coordinates the change;
the owning level and theme skills keep their formats, writers and acceptance rules.

## Resolve the owner and the problem

Read the Work Block (Blueprint)'s face, relevant Studio topics, current traces and the
example it names. Identify the reader's task and the concrete behavior to change.
Use [hai-ladder](../../../1_base/project/hai-ladder/SKILL.md) when the work's
placement is unclear. A software or data execution request without a tooling-definition
change goes to [hai-work](../../work/hai-work/SKILL.md).

A Blueprint belongs under `〈Project〉/blueprint/bNN_〈block〉/`. Locate an existing
owner before proposing a new Block. A domain example remains in its own theme;
being used as an example does not turn it into a Blueprint. Opening or inspecting
either page uses [workbench](../../../1_base/workbench/hai-workbench/SKILL.md).

## Make the change reviewable

Read the owning constitutions before editing. Trace a demonstrated problem from
the real page or command to the contract and implementation that govern it. For
a new capability, state the intended behavior and a concrete acceptance case.

| Part | What to bind |
|---|---|
| Work Folder | Real input, output and records the example needs |
| Work UI | The reader's action and the shared component that shows those records |
| Define Folder | Owning skill contract, code and checks affected by the change |
| Define UI | The Blueprint topic and example through which the change is reviewed |

Use this map to find affected files, not to manufacture four artifacts for every
small edit. A folder-kind change must align its contract, rendering, Blueprint
definition and validation. A skill-only correction can reuse the existing page.

Include the Trace path in the exact file plan and record it through
[hai-trace](../../../0_utils/hai-trace/SKILL.md). Writing the Trace itself follows
the active repository and session approval boundary; permission to record a plan
authorizes that record only. Obtain the required confirmation before implementation.
Preserve other sessions'
changes; re-read shared targets before editing. Identify scope conflicts before
touching shared code. Use the available authorized coordination mechanism when
another session owns the same change; a trace alone does not reserve a file.

## Implement through the owners

- Use [hai-block](../../../1_base/project/hai-block/SKILL.md),
  [hai-job](../../../1_base/project/hai-job/SKILL.md),
  [hai-task](../../../1_base/task/hai-task/SKILL.md) and
  [hai-run](../../../1_base/project/hai-run/SKILL.md) when their records
  are actually needed. Do not invent a Job/Task type from a responsibility label.
- Use [hai-studio](../../../1_base/project/hai-studio/SKILL.md) for the
  design discussion, type requirements and actual skill-file bindings. Its
  `skills_views.py` generates Skills views from the real skill directories.
- Use [hai-ui](../../../1_base/workbench/hai-ui/SKILL.md) for page rules
  and the owning theme's constitution for specialized content. Reuse the shared
  Block renderer, including previews. Jobs and Tasks stay inside their Block.
- Keep one source for a rule or record. Examples read the current owner and pages
  read real files. Do not retire a skill until runtime imports, references and
  installed entry points have been examined.

New skill content describes the current contract. Retain provenance in its
constitution and Trace; keep migration history out of the operational instructions.
Rule maintenance across owners can use [hai-stack](../../../0_utils/hai-stack/SKILL.md)
within the confirmed scope.

## Verify and hand over

Repeat the case that motivated the change. Run the checks appropriate to the
affected contract; test meaningful behavior, not merely the presence of wording.
Validate skill changes from a fresh context as the root README requires. For a
page change, drive the live example and verify the reader's action, preview content
and Block route. A passing source check alone is not a live-page acceptance.

Record what passed, what remains unresolved and what prevents recurrence. A topic
whose case passes without a guard remains open under the owning topic rules.
Update the trace's actual changed files, checks and summary before closing it.
Return the owning Block link and any necessary rerun or reload instruction.
Coordinate a necessary shared-service restart explicitly; this skill does not
grant deployment, release, sending or restart authority by itself.
