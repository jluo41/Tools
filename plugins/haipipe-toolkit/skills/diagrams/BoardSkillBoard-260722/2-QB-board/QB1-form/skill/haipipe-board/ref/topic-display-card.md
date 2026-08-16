# Topic display companion

Use one hidden Display companion after each QA-probe on a Value or Literature page that declares `display: companion`.
The companion is a candidate display record, not a Board Page and not a final paper float.
It sits beside the topic page at `display/<topic page name>/<n>-<slug>.md`, with the same `<n>-<slug>` stem as its QA-probe.

```markdown
# <short candidate display title>
state: candidate | selected | paper-bound | parked | not-displayable
kind: value-table | value-figure | literature-matrix | literature-map
probe: <relative path to its QA-probe>

## Takeaway
<what a reader could learn in five seconds, without claiming more than the probe permits>

## Narrative use
claim: <C id or none>
role: <candidate punchline | support | boundary | background | none>

## Disposition
<why this display stays a candidate, is selected, moves to a Paper Display unit, is parked, or is not displayable>
```

Only a `selected` companion may file a Display request and become a formal Paper Display unit.
The formal unit, its render, human acceptance, caption, and manuscript placement stay owned by `haipipe-page-for-display`.
