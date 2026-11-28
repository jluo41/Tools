s01 · Block Structure: Work
===========================
view: overview
emoji: 🛠️

**Tags:** `Structure`

**Stage:** shaping

**For:** the folder content, Job / Task organization and Studio organization of a Work Block.

**Delivery type:** structure

**Covers:** Folder; Job-Task; Studio.

**Excluded:** UI layout and interaction design, owned by s11–s13; changing the owning theme's folder contract.

**Topic:** Work shows meaningful responsibility categories and named Jobs/Tasks from the CSV-tool example. Folder reads existing storage; organization does not create new folders or canonical Job types.

Views
-----

- Structure: Folder, Job-Task, Studio; Job and Studio names follow the Block type. Job-Task shows Job Type, Job Name, Task Type and Task Name; each name links to an existing record.
- Draw: the same three models as expandable structural diagrams.
- Examples: existing Blocks, opened through the shared Block framework.
- Skills: the actual owning contracts, read in this topic.

Files
-----

- `studio-views.json`: the view and content bindings.
- `../delivery/structure/work-organization.html`: the three content models.
- `../delivery/structure/build_organization.py`: their common builder.
- [Previous structure](result/structure-before-organization-261127.md): the complete face before this refinement.
- [Original topic](result/structure-replaced-261127.md): earlier decisions and references. Existing canvases, annotations and builders remain unchanged.

Decision
--------

2026-11-27: use s01 Work, s02 Blueprint, s03 CoWork, s04 Discovery. This band defines structure and required content; s1N remains UI. The user's requested content is Folder, Job-Task, Studio. Execution authorized in the current session; request, plan and evidence: `../trace/261127/1021_structure_folder_organization.md`.

2026-11-27 refinement: Studio defines topic types for this Block type, not Block / Job / Task ownership levels. Job topics and names also follow the Block type; generic slots use Example 1 / Example 2. See `../trace/261127/1048_organization_by_block_type.md`.

2026-11-27 correction: Job-Task must show the four explicit type/name columns and matching Draw relationships. Responsibility categories are this structural proposal; existing record fields remain inspectable evidence and are not silently rewritten. No Job 1 / Task 1 / Example 1 placeholder tree. The CoWork example/contract Task conflict is recorded explicitly.


Studio organization
-------------------

The Work Studio groups topics by Work Design, Implementation Design, Results Discussion. Topic names depend on the work; bracketed names in the diagram are examples. Empty groups are omitted.

[Studio organization](../delivery/structure/work-organization.html#studio-rules) · [Band contract](../delivery/page-spec/studio-bands-by-block-type.md). Structure → Studio uses a collapsible Folder Tree: Band → 〈Studio topic〉. Draw retains the existing drawing.
