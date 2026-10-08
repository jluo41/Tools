# UI Card Style Profile

Drafting guide for in-app card/widget artifacts.


## Voice examples

**General-reader alert card:**
```
┌─────────────────────────────────┐
│ ⚠  <Item> Due Soon              │
│                                 │
│ Your <item> is due in 2 days.   │
│ <One plain reason it matters>.  │
│                                 │
│ [ <Act Now> ]   [ Remind Me ]   │
└─────────────────────────────────┘
```

**Professional insight card:**
```
┌─────────────────────────────────┐
│ 📊  <List> Risk                 │
│                                 │
│ 4 of 47 <items> are flagged     │
│ for <the risk>.                 │
│                                 │
│ Avg days to <deadline>: 2.3     │
│ Highest: [ItemList]             │
│                                 │
│ [ View List ]   [ Send Batch ]  │
└─────────────────────────────────┘
```


## Drafting rules

1. Card must fit one screen — no scroll for core content.
2. Hierarchy: header (hook) → body (detail) → action (CTA).
3. Max 2 action buttons. Primary action left, secondary right.
4. Show sample data and name the source with `data-bind`; do not claim live integration.
5. A wireframe may guide drafting. Visual checks require the actual HTML screen
   rendered into the current Result, with the picture and manifest named in it.


## Audience pairing

```
audience=general      → warm, simple, large tap targets
audience=professional → data-dense, source map in the Job's records, actionable
audience=designer     → annotated wireframe, component names
audience=dev          → interface spec, data binding, events
```


## Self-review checklist

```
[ ] Fits one screen without scroll
[ ] Header grabs attention (hook or alert)
[ ] Body provides enough context to act
[ ] CTA is specific (not "Learn More")
[ ] Data sources specified for live elements
[ ] Job and Task ids, the pinned goal · method · inputs, and the Run's result/ paths resolve
[ ] Any render manifest binds the exact source and picture inside its Run's result/
```
