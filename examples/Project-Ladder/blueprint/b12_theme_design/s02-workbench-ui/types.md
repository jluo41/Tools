# Design Method Book types

example: examples/Project-Ladder/design/DesignMethodBook-Example
block-kind: design-method-book
owner: [hai-design-method](../../../../../plugins/haipipe-toolkit/skills/3_theme/design/hai-design-method/SKILL.md)

Sources: [Design ladder](../../../../../plugins/haipipe-toolkit/skills/3_theme/design/hai-design/ref/design-ladder.md); [design_jobs.py](../../../../../plugins/haipipe-toolkit/servers/workbench-design/design_jobs.py); [example Block](../../../design/DesignMethodBook-Example/board.md).
A semantic Job contract is not a serialized `job-type:` value. Only declared Task values are listed as such.
Group labels and grouping criteria do not establish a separate group-type enum. No example record is changed
by this inventory. Unknown group types are left undeclared instead of adding a type named None or Unknown.

## Job group type

presence: grouping exists; a distinct group-type list is not defined by the current contract.
field: Job `family:` when authored; otherwise its `method:` resolves the registry's `family:`.
for: browse registered method identities by family.
holds: method Jobs, each with its own signed versions; executions remain in Design Boards.
named: 〈Method family〉; the fixed fallback is Methods when neither source supplies a family.
source: [design_jobs.py](../../../../../plugins/haipipe-toolkit/servers/workbench-design/design_jobs.py) `topic()`; [method registry](../../../../../plugins/haipipe-toolkit/skills/3_theme/design/hai-design-method/methods).
owner: [workbench-design](../../../../../plugins/haipipe-toolkit/skills/3_theme/design/workbench-design/SKILL.md) for grouping; [hai-design-method](../../../../../plugins/haipipe-toolkit/skills/3_theme/design/hai-design-method/SKILL.md) for family values.

The example's j01 and j02 name M01 and M02. Their Job faces do not author `family:`, so the reader uses the
registry. No separate `job-group-type:` is stored; a family name does not create a method-execution Job type.

## Job type

field: no separate `job-type:` value on the current Job faces; the entry below is a semantic contract.

### Method type
for: maintain one registered method identity and the signed versions that Design Board executions pin.
holds: a Job face with method, title and versions, signed m〈K〉.md files, and links to uses; proposals belong to the Book's proposals directory.
name: `jNN_M0x-〈method〉/`; the method id and title identify the Job.
source: [Design ladder](../../../../../plugins/haipipe-toolkit/skills/3_theme/design/hai-design/ref/design-ladder.md); [example method Job](../../../design/DesignMethodBook-Example/j01_M01-goal-only/j01_M01-goal-only.md).
owner: [hai-design-method](../../../../../plugins/haipipe-toolkit/skills/3_theme/design/hai-design-method/SKILL.md) for registry, versions and proposals; [hai-design](../../../../../plugins/haipipe-toolkit/skills/3_theme/design/hai-design/SKILL.md) for Book scaffolding.
members: j01_M01-goal-only contains m2.md; j02_M02-overall-performance contains m1.md.

M01 and M02 identify different methods within this contract. They are not new serialized Job-type values,
and m1/m2 are versions, not Tasks. The Board pins a method version when it creates an execution Job.

## Task group type

presence: absent; this Block has no execution Task layer and therefore no Task groups.
field: none.
for: not applicable; method steps are contents of a method version.
holds: no execution Tasks in a method Job.
source: [Design ladder](../../../../../plugins/haipipe-toolkit/skills/3_theme/design/hai-design/ref/design-ladder.md); the example method Job directories.
owner: [hai-design-method](../../../../../plugins/haipipe-toolkit/skills/3_theme/design/hai-design-method/SKILL.md).

Do not add Ideas / Designs / Review or empty Task selectors to a Method Book.

## Task type

presence: absent; no execution Task types are declared for a Method Book.
field: none; the example contains no Task faces or tNN directories.
for: not applicable; execution happens in Design Boards that pin the method version.
holds: no execution Tasks. Signed version files remain directly inside their method Job.
source: [Design ladder](../../../../../plugins/haipipe-toolkit/skills/3_theme/design/hai-design/ref/design-ladder.md); [example Book directory](../../../design/DesignMethodBook-Example).
owner: [hai-design-method](../../../../../plugins/haipipe-toolkit/skills/3_theme/design/hai-design-method/SKILL.md).

The empty list is intentional, not a missing implementation. No None/Unknown placeholder type is declared.

## Studio organization

The actual Book example has no sNN topic directories and its face declares no numbered Studio Band scheme.
Do not show an empty Band or copy Blueprint Bands into the Book. A method-specific topic may be added when
there is actual work to discuss, following its owning Studio contract; no new topic is created by this inventory.
The reusable Book Studio organization remains an explicit contract question, separate from this empty example.

## Validation boundary

Require this file and the Board inventory explicitly; a scan finding no files cannot certify compliance.
Compare the method identities and signed version files, and assert that no execution Task directory exists.
The shared checker currently insists on nonempty lists for all four levels and cannot represent this absent
Task layer. Record that limitation; do not invent Task types or claim a passing shared check.
Job serialization, actual-Block Studio organization and inventory-generated views remain open under T08/T20.
