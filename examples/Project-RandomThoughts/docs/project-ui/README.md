# Project UI

Status: proposed. This is the Project-level blueprint, above its Themes.

`board.md` declares `ui-project: examples/Project-Ladder`. The Project UI button
shows `project-preview.html`, the `project-views.md` matrix, the existing Project
page, and its walkthrough slot. The preview is a design artifact, not a replacement
for the live Project renderer.

## Shape

One Project page. Project and the present Themes are its view buttons. No Work /
Report mode switch. Every Theme has Purpose, Plan, Blocks and Handoffs. Project
uses Themes in place of Blocks. Around the Work keeps the shared eight sections.
The preview's plans and flows are proposed examples. Links open existing sources;
it does not manufacture states, approvals, dependencies or execution records.
Theme-local Studio storage is not introduced. Preview context links open current
aggregate pages; production view-scoped context is not implemented by this mock.

## Ownership

- Project identity, mission and Theme boundary: hai-project.
- Theme plans and Blocks: the Theme's hai-* and workbench-* contracts.
- Handoffs: hai-delivery plus producer and consumer contracts.
- Studio and decisions: hai-studio. Forms: hai-interaction.
- Shared context, files and navigation: workbench and hai-ui.
- The section definitions and per-view skills: view-guide.json.

## Review

The preview supports Theme buttons, keyboard navigation, collapsed sections and
source links. Actual Project migration, dependency bindings and persisted plan
editing are separate implementation work after the design is settled.
