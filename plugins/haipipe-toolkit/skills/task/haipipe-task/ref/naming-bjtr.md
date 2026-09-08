# Naming rules for Block · Job · Task · Run

Every executable name follows one grammar:

```text
bNN_<noun>_<qualifier>   Block
jNN_<noun>_<qualifier>   Job
tNN_<noun>_<qualifier>   Task
rNN_<noun>_<qualifier>   Run
```

`NN` is a two-digit index unique within the parent. Names are snake_case and
contain no hidden mapping from level letters to computational type.

## N1 — the stranger test

A name must answer two questions without surrounding path context:

1. What concrete thing does this unit own or produce?
2. Which source, grain, scope, or variant separates it from siblings?

```text
weak   j01_candidate_pool
clear  j01_physician_candidates_by_region

weak   t01_analysis
clear  t01_physician_rankings_compared
```

## N2 — level and order are explicit

The first letter says the level; the index says order within its parent.
Do not encode a stage or Task type in the level letter. Do not use bare letters,
single-digit indices, or untagged numeric addresses.

## N3 — use project vocabulary

Use terms already defined by the Project's Board and data contracts. A clearer
name may expand an abbreviation, but must not create a synonym that forces
readers to maintain a translation table.

## N4 — siblings are unique

Block names are unique in `tasks/`; Job names are unique within a Block; Task
names are unique within a Job; Run names are unique within a Task. Cross-Job
references use full relative paths or full b/j/t/r addresses.

## N5 — shape words need a subject

Words such as `data`, `table`, `pipeline`, `analysis`, `pool`, `rank`, `set`,
and `baseline` may qualify a concrete noun but cannot stand alone.

## N6 — Run pairing is exact

The config and Ticket use the same `rNN_<run>` stem:

```text
scripts/config/r03_physicians_healthgrades.yaml
runs/r03_physicians_healthgrades.sh
```

The matching Result and notebook repeat that stem beneath the Task name.

## N7 — lookup names, do not reconstruct them

When a script needs an asset, Task, or config name, resolve the declared value
and raise if it is absent. Never derive a name by slicing Folder text or silently
fall back to a default.

## N8 — the tree is the inventory

Do not hand-maintain a second file listing every Task or Ticket. A status view
derives membership from disk at read time. If a presentation order is needed,
store only the explicit ordering decision, not a copied inventory.
