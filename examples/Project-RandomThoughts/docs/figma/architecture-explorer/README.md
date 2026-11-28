# File System, UI System and Mapping

[Open the Figma design](https://www.figma.com/design/O4RtsPP31Dh1xNp77Ri1Fi?node-id=2-875) · [Open the clickable local preview](preview.html)

The draft follows one saved Chat through a file explorer, a Block page, and the read/write mapping between them. Switching views keeps the same example in focus. Skill and Session details extend the three main views.

## Screens

| Screen | Purpose | Figma frame |
| --- | --- | --- |
| File System | Locate Skill folders and the Block's Job, Studio and Chat siblings; inspect the Chat file | `2:875` |
| UI System | See the QA element on a Block page and find its source | `2:980` |
| Mapping | Follow creation, refresh, reading and navigation | `2:1061` |
| Session detail | Read concise questions, outputs and changed-file references | `2:1139` |
| Skill structure | See the contract, writer scripts and checks that produce the record | `2:1197` |

## Source and interpretation

- [PRINCIPLE.md](../../../../../PRINCIPLE.md) now places `cNN` beside `jNN` and `sNN` inside a Block. It supersedes the earlier Project-level Chat storage suggestion in this conversation.
- The example is the real c01 Chat record (b10, removed 261126).
- [hai-chat](../../../../../plugins/haipipe-toolkit/skills/1_base/project/hai-chat/SKILL.md) owns the concise QA contract. A native conversation remains with its provider; the Block record is not a raw transcript.
- Mockup QA text is shortened in English. Refer to the source record for original wording.
- The end-of-answer workflow describes the intended configured behavior. This draft does not install a hook or establish automatic capture for every provider.
- Jobs and Studio appear as folder kinds. They are not fabricated execution records.

The UI is an architecture design tool, so filenames, readers and writers are useful content. This is not a proposal to expose implementation details throughout every end-user page.

## Figma verification and remaining work

Five editable screens and 39 cross-screen prototype links were created. Structural inspection confirmed text, frames and reusable component instances; the screens contain no flattened image of the UI. The design uses Simple Design System tabs, buttons, surface/spacing/radius variables, and local role and typography definitions.

The File System screenshot revealed oversized reusable tree rows, clipping the lower tree. Figma's Starter-plan MCP limit then blocked the correction and further screenshot checks. The live Figma file therefore still needs that layout fix and visual review of the other screens. [finish-layout.js](finish-layout.js) records the targeted correction for the existing nodes; it has **not** been applied.

The local preview provides the compact tree and working view navigation independently of the Figma API quota. It reads static sample content and does not write repository files or implement a new session service.

Browser review checked all five views, the File → UI → Session → Mapping navigation, and QA expansion. The File and UI layouts and the Mapping view were inspected visually. JavaScript syntax and source-link existence checks passed. The browser is left on File System. Mobile breakpoints are authored but were not separately browser-tested.

Only this preview directory is served on loopback. Its `sources/` folder contains the specific reference snapshots used by the controls; `sources/manifest.json` records their canonical locations and hashes.

## Files

- `build.js`: the creation script used through `use_figma`. Do not rerun it in the existing file; it creates new nodes.
- `finish-layout.js`: the unapplied targeted repair for the created component nodes.
- `figma.json`: file, session and frame identifiers.
- `preview.html`, `preview.css`, `preview.js`: the local interactive companion.

Created 2026-11-22. The Project's inbox, existing Blocks and saved source archives remain in place.
