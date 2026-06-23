# UI Card Style Profile

Drafting guide for in-app card/widget artifacts.


## Voice examples

**Patient-facing alert card:**
```
┌─────────────────────────────────┐
│ ⚠️  Refill Due Soon             │
│                                 │
│ Your [Medication] refill is     │
│ due in 2 days. Refilling on     │
│ time keeps your levels steady.  │
│                                 │
│ [ Refill Now ]   [ Remind Me ]  │
└─────────────────────────────────┘
```

**Clinician-facing insight card:**
```
┌─────────────────────────────────┐
│ 📊  Panel Refill Risk           │
│                                 │
│ 4 of 47 patients are high-risk  │
│ for refill lapse (K03).         │
│                                 │
│ Avg days to expiry: 2.3         │
│ Highest risk: [PatientList]     │
│                                 │
│ [ View List ]   [ Send Batch ]  │
└─────────────────────────────────┘
```


## Drafting rules

1. Card must fit one screen — no scroll for core content.
2. Hierarchy: header (hook) → body (detail) → action (CTA).
3. Max 2 action buttons. Primary action left, secondary right.
4. Data elements (numbers, lists) are live — specify data source.
5. ASCII wireframe required in draft; production rendering later.


## Audience pairing

```
audience=patient     → warm, simple, large tap targets
audience=clinician   → data-dense, inline K-id, actionable
audience=designer    → annotated wireframe, component names
audience=dev         → interface spec, data binding, events
```


## Self-review checklist

```
[ ] Fits one screen without scroll
[ ] Header grabs attention (hook or alert)
[ ] Body provides enough context to act
[ ] CTA is specific (not "Learn More")
[ ] Data sources specified for live elements
[ ] cited_K / cited_W in frontmatter
```
