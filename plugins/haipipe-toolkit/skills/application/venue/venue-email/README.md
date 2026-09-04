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
  terminal: accepted
```

## Phase use

### D1/D2 · bet and realize

Each section's core move traces through the released card grant. If a
load-bearing section lacks support, record the gap for D4 EMIT rather than
opening a private evidence search.

### D2 · narrative requirement
Letter-style arc:
1. Context — why you're receiving this
2. Finding — what the evidence shows
3. Recommendation — what to do
4. Next steps — what happens next

### D2 · optional display
If the email includes data (chart, table, KPI), write a display
map. Otherwise skip — pure-text emails don't need it.

### D3/D4 · judge and decide
Subject line + sections following narrative arc.
Tone per audience profile. Check every factual move against the grant, render
to `delivery/render/`, then accept that version or emit the named gap.
