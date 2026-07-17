# Venue: Report

Formal stakeholder report. Structured sections, citations, data
tables/figures. The most paper-like venue — all stages required.


## Constraints

- **Length:** 600-2000 words (audience-dependent)
- **Structure:** formal sections (exec summary, methodology,
  findings, recommendations, appendix)
- **Citations:** required (format per audience profile)
- **Data:** tables and figures with captions


## Stage requirements

```yaml
stages:
  seed:       required
  pitch:      required
  claims:     required
  narrative:  required
  display:    required
  section-edit:    required

claims_settlement: full
```


## Lifecycle mappings

### → Claims (full)
Full claim ledger. Every finding/recommendation must trace to
a supported claim. GAPs trigger probes.

### → Narrative (required)
Report arc depends on audience:
- Regulator: methodology → findings → limitations → recommendations
- Executive: bottom line → evidence → ask
- Partner: context → joint findings → next steps

### → Display (required)
Display map: tables (summary stats, comparisons), figures
(forest plots, trend charts), KPI callouts.

### → Section-edit (required)
Per-section DPRC on the declared sections; paragraph-level job
assignments live in each section's outline. This is the venue
closest to an academic paper.

Default section structure (adjust per intervention in 3-narrative;
the DIKW-spine layout below originated in the C-group report work):

```yaml
sections:
  - 01-subgroup-profile    # who the cohort is (D)
  - 02-exploration         # what was tried / examined (D/I)
  - 03-findings            # what the evidence shows (I/K)
  - 04-messages            # what we say / recommend (K/W)
  - 05-performance         # how it performed (I/K)
  - 06-gate-check          # settlement + caveats before shipping
```

### → Draft
Formal report following the narrative arc, assembled from 0-sections/
by haipipe-application-artifact. Full citations.
