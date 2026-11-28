s03 · Block Structure: DataPrep
================================================
view: overview

**Tags:** `Structure`

**Stage:** explore

**For:** the DataPrep folder, work organization and Studio responsibilities.

**Why:** How do responsibility, name and grouping connect to the source records?

**Topic:** A Job builds one prep-code version. Its Tasks define ordered steps. experiment, source and prepare are step names, not different Task types. The consuming Board prep Task runs the entire chain; execution Runs and outputs belong there.

**Feeds:** Q01 · Q04

Types
-----

No Job group: the Job is the version. Job type: Prep-code version. No Task group: steps are ordered directly. Task type: Prep step. The [type catalog](types.md) states each responsibility, what it holds, its real source fields and owning skills. Version ids and individual question or step names do not introduce types.

Views
-----

Structure / Job types / Task types / Draw / Skills. Structure shows Folder, Job-Task and Studio as vertical Folder Trees, with native expansion, branch lines and source links. Draw is separate; S71 requires one owned Excalidraw canvas. Each naming rule uses fixed contract names and 〈variable names〉. Its real example is folded under the relevant content, with a corner dot opening the owning Block. Job types and Task types are generated from types.md by the shared block_types_pages.py. Skills previews the owning SKILL.md files. This Studio has no owned Excalidraw canvas yet; its separate map binding remains a Draw gap (T44). Authored content stays in its source. No mindmap is bound to Structure.

Studio organization
-------------------

Ordinary Work numbering comes from hai-studio's writer: Concept s01–s09; Level s11–s19; Report s21–s29; Task procedure s41–s49; Guide s81–s89. Each topic stays with its Block, Job or Task; existing identifiers, including a concrete s99 Guide, stay unchanged. These are ordinary Work categories, not this Blueprint's Block Structure or UI Preview categories.

Proposed topic responsibilities: 〈Data conventions and chain〉 at Block; 〈Step interfaces〉 at Task; 〈Preparation limits〉 at Job; 〈Step code and review〉 at Task; 〈Using this prep version〉 at Block.

The rule tree shows these uses with 〈〉. The example reads only actual Studio folders and their configured bands or tags; it does not create any proposed topics. DataPrep currently has no actual Studio example. A topic is created only when needed, not to fill an empty group.

Sources
-------

- [Shared Studio Type: Block Structure](../../b17_theme_work/s71-studio-type-block-structure/s71-studio-type-block-structure.md)
- [Insight contract](../../../../../plugins/haipipe-toolkit/skills/3_theme/insight/workbench-insight/ref/block-structure.md)
- [Type catalog](types.md)
- [Generation source](../delivery/structure/build_structure.py)
- [Actual example](../../../insight/InsightDataPrep-Example/board.md)
- [Job UI preview](../s13-dataprep-job-preview/s13-dataprep-job-preview.md)

Decided
-------

No step or version is renamed. The Studio tab distinguishes proposed subjects from the example's actual absence of sNN topics.

History
-------

Former s03-insight-methods and its historical canvases were already removed from the working tree.
Their Git records are untouched. s05 workflow and s99 Guide retain the surrounding method material.

Open
----

- The shared Job reader still uses numeric grouping for prep versions and steps.
- Verify Structure trees and Draw separately on phone; keep normal text size and source links.

- Shared type pages describe For/Holds. Their member reader needs Insight source adapters and Block selection routes; actual membership is available in the Job-Task example.
