# Venue: Email

Longer-form email. Sections, links, optional inline visuals.
More room for evidence-backed argumentation than SMS/push.


## Constraints

- **Length:** 200-800 words (audience-dependent)
- **Sections:** 3-5 (context → findings → recommendation → next steps)
- **Links:** allowed; use descriptive anchor text
- **Images:** optional inline (charts, diagrams)
- **Subject line:** ≤ 60 chars, specific


## Stage requirements

```yaml
stages:
  seed:       required
  pitch:      required
  claims:     required
  narrative:  required
  display:    optional
  minimap:    skip

claims_depth: medium
```


## Lifecycle mappings

### → Claims (medium)
Select + gap check. Each section's core statement should trace to
a K/W entry. If a section has no backing, flag the gap.

### → Narrative (required)
Letter-style arc:
1. Context — why you're receiving this
2. Finding — what the evidence shows
3. Recommendation — what to do
4. Next steps — what happens next

### → Display (optional)
If the email includes data (chart, table, KPI), write a display
map. Otherwise skip — pure-text emails don't need it.

### → Draft
Subject line + sections following narrative arc.
Tone per audience profile. Citations per audience rules.
