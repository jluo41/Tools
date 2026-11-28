s01 · Design Board Structure
============================
view: findings

**Tags:** `Structure`

**Stage:** shaping

**For:** the Design Board work hierarchy and Studio organization, with live examples and owning skills

**Delivery type:** structure

**Why:** which Job group, Job name, Task group and Task name make a Design Board different from a Design Method Book and every other Block?

**Topic:** one application in one channel. One kind of Job, grouped by its method's family; a Job name is one goal × one pinned method version × one inputs version. Task groups are Ideas, Designs and Review; a Design Task is named for its design, and generate, verify and revise are Runs inside it. Structure shows naming rules with the corresponding real Design-Example records and live Block; Draw shows the rules.

**Feeds:** Q01 · Q02 · Q03


Views
-----

- Structure: Folder, Job / Task Organization and Studio Organization, each with its naming rule and expandable real example ([spec](delivery/structure.md)); the Design-Example entry opens the live Block.
- Draw: the same three naming rules, using the shared drawing controls.
- Skills: the owning skills, read through the shared file viewer.


Sources
-------

- [Type contract](../../../../../plugins/haipipe-toolkit/skills/3_theme/design/hai-design/ref/design-ladder.md)
- [Structure source](../delivery/structure/build_organization.py)
- [Current example](../../../design/Design-Example/board.md)
- [Job UI preview](../s11-design-job-preview/s11-design-job-preview.md)


Decided
-------

- Job group, Job name, Task group and Task name, drawn as b17's folder tree; the groups are not types (trace 261127/1305).
- Jobs group by their method's family from the method registry (trace 261127/1235).
- Board Tasks carry `task-type: design-reason`, `design-item` or `design-whole`; Ideas, Designs and Review are groups. No new schema field is introduced by this Studio.


History
-------

The 261007 face (the design ladder at a glance, Q01 to Q03 not yet answered) and its drawing and deck are in
`../_archive/20261127/s01-design-overview/`.


Open
----

1. `delivery/structure.md` § Main and a selected Task changes once Job Main as Overview, Tasks, Findings lands (trace 261127/0921).
