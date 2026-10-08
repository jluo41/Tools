# Venue: Email

Longer-form email. Sections, links, optional inline visuals.
More room for evidence-backed argumentation than SMS/push.


## Constraints

- **Length:** 200-800 words (audience-dependent)
- **Sections:** 3-5 (context → findings → recommendation → next steps)
- **Links:** allowed; use descriptive anchor text
- **Images:** optional inline (charts, diagrams)
- **Subject line:** ≤ 60 chars, specific


## Design profile

```yaml
design_profile:
  evidence_bar: medium
  narrative: required
  display: optional
  section_edit: none
```

## Run guidance

### Inputs and generate ③

Each section's core move traces through the Job's inputs/ fence (its manifest). If a
load-bearing section lacks support, return a named hold rather than
opening a private evidence search.

### generate ③ · narrative requirement
Letter-style arc:
1. Context — why you're receiving this
2. Finding — what the evidence shows
3. Recommendation — what to do
4. Next steps — what happens next

### generate ③ · optional display
If the email includes data (chart, table, KPI), write a display
map. Otherwise skip — pure-text emails don't need it.

### verify ④ (another agent)
Subject line + sections following narrative arc.
Tone per audience profile. Check every factual move against the fence,
render inside the current Run's result/ when visual checks require it. A passed verify ④, then t99's rank ⑤ and a person's release, put
that exact version in delivery/.
