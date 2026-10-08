# Venue: Report

Formal stakeholder report. Structured sections, citations, data
tables/figures. The most paper-like venue in this reference family.


## Constraints

- **Length:** a full report typically uses 600-2000 words; audience-specific
  briefs may be shorter (see the style profile). Freeze one explicit budget
  when the Job is set up rather than combining a default range with an audience cap.
- **Structure:** formal sections (exec summary, methodology,
  findings, recommendations, appendix)
- **Citations:** required (format per audience profile)
- **Data:** tables and figures with captions


## Design profile

```yaml
design_profile:
  evidence_bar: full
  narrative: required
  display: required
  section_edit: required
```

## Run guidance

### Inputs and generate ③

Every finding, recommendation, table, and figure maps through the Job's inputs/
fence (its manifest). A load-bearing gap returns as a named hold; Design never Probes.

### generate ③ · narrative requirement
Report arc depends on audience:
- Regulator: methodology → findings → limitations → recommendations
- Executive: bottom line → evidence → ask
- Partner: context → joint findings → next steps

### generate ③ · display requirement
Display map: tables (summary stats, comparisons), figures
(forest plots, trend charts), KPI callouts.

### generate ③ · section pass
Per-section review on the declared sections; paragraph-level jobs live in the
Unit's outline. This is the venue closest to an academic paper.

Default section structure (adjust per the pinned goal · method version · inputs version and audience):

```yaml
sections:
  - 01-subgroup-profile    # who the cohort is (D)
  - 02-exploration         # what was tried / examined (D/I)
  - 03-findings            # what the evidence shows (I/K)
  - 04-messages            # what we say / recommend (K/W)
  - 05-performance         # how it performed (I/K)
  - 06-gate-check          # settlement + caveats before shipping
```

### verify ④ (another agent)
Judge the formal report against the evidence bar and venue rails, render its
exact version inside the current Run's result/. A passed verify ④, then t99's rank ⑤ and a person's release, put it in delivery/.
