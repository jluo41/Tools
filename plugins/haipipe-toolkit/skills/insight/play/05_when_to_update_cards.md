# When To Update Cards

Cards are not frozen forever. They are stable references, but new evidence can
change them.

The review step decides whether new material should create a new card or modify
an existing card.

## File

Use `file` when the material contains a new reusable unit.

Example:

```text
New K: "Validation gain does not transfer to OOD."
```

## Merge

Use `merge` when new evidence supports the same card.

Example:

```text
Existing K03: "Validation gain does not transfer to OOD."
New probe: same claim, second OOD split.
Action: merge evidence into K03.
```

The card keeps its ID. Its `## Change log` gets a new entry.

## Update

Use `update` when the card needs metadata or status changes, but the core claim
does not change.

Example:

```text
Add a new narrative reference to `ref_by`.
```

## Supersede

Use `supersede` when new evidence makes an old card misleading or wrong.

Example:

```text
Old K03: "Validation gain does not transfer to OOD."
New stronger probe: gain transfers across five OOD splits.
Action: mark K03 as superseded and create a replacement K card.
```

Do not delete the old card. Link it to the replacement so old narratives and
reports still have an evidence trail.

## Skip

Use `skip` when the material is too raw, too small, duplicated, or not reusable.

Example:

```text
"Run finished successfully."
```

That belongs in task logs, not permanent memory.

## Blocked

Use `blocked` when the candidate is promising but not ready.

Example:

```text
Candidate mixes three separate claims.
Action: blocked until split into three cards.
```

## Change Log Rule

Every meaningful card edit should append `## Change log`.

The change log should answer:

```text
What changed?
Why did it change?
Which new source caused the change?
Did confidence or status change?
```
