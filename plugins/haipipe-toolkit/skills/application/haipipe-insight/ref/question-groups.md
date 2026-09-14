# Question Groups · partition × DIKW target

A Question Group is the scheduling and status intersection of one Insight
partition scope and one requested DIKW target. It is derived from MT00 and the
four I1 registers; it is never another Folder, queue, or authority ledger.

```text
Question Group = partition scope × target rung

QG-F-D   full/template × Data
QG-B-I   partition B × Information
QG-C-K   partition C × Knowledge
QG-F-W   full/template × Wisdom
QG-X-K   cross-partition scope × Knowledge
```

## Axes and identity

The partition axis comes from MT00 in its declared order. `F` is the full
template. Registered audience partitions use their MT00 letters. `X` is a
derived cross-partition scope, not an audience partition; it exists only for a
question whose answer needs rows from two or more partitions. Since X owns no
raw rows, `QG-X-D` is invalid.

The target axis is fixed:

```text
D  Data          observe
I  Information   derive
K  Knowledge     claim
W  Wisdom        counsel / hand off
```

The canonical handle is `QG-<partition>-<rung>`. It is computed, not stored.
Changing a question's target moves its membership; changing MT00 partitions
recomputes the affected groups and reopens X where required.

## Membership

One question keeps one stable `QD|QI|QK|QW<n>` id and one register row. Its
eligible Queue cell under partition `P` belongs to `QG-P-<target>`.

```text
QI3 under B   belongs to QG-B-I
QW2 under F   belongs to QG-F-W
QK7 routed X  belongs to QG-X-K
```

A COLUMN question may therefore appear in several Question Groups through its
distinct partition cells without being duplicated. An X question belongs only
to the matching X group; dot cells in audience columns are routing marks, not
members. An F-only question belongs to the F group; its `🚫 F-only` audience
cells remain visible terminal receipts but dispatch no pages.

## State and dispatch

Question Group state is a projection of its cells:

```text
EMPTY      no eligible cells
RUNNABLE   at least one open cell has its next input and gate
BLOCKED    open cells exist, but every one names a missing input or gate
SETTLED    every eligible cell is ✅, 🚫 <reason>, or 🟡 <page> final
```

The group is a batch view, not the atomic transition. Dispatch still selects
one cell and one Page at a time. Status sorts groups by MT00 partition order,
then `D → I → K → W`; questions within a group stay in stable id order.

The same projection works in both layouts:

```text
rung-major       MT02 is the I-axis slice; each partition column exposes QG-*-I
partition-major  group B is the partition slice; its D/I/K/W pages expose QG-B-*
```

No `question-group.yaml`, duplicated question row, group state file, or new
Folder is written. MT00 plus MT01-MT04 remain the only authoritative records.
