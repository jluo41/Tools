# Venue: Report

Formal stakeholder report. Structured sections, citations, data
tables/figures. The most paper-like venue in this reference family.


## Constraints

- **Length:** 600-2000 words (audience-dependent)
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
  terminal: accepted
```

## Phase use

### D1/D2 · bet and realize

Every finding, recommendation, table, and figure maps through the released
card grant. A load-bearing gap is preserved for D4 EMIT; Design never Probes.

### D2 · narrative requirement
Report arc depends on audience:
- Regulator: methodology → findings → limitations → recommendations
- Executive: bottom line → evidence → ask
- Partner: context → joint findings → next steps

### D2 · display requirement
Display map: tables (summary stats, comparisons), figures
(forest plots, trend charts), KPI callouts.

### D2 · section pass
Per-section review on the declared sections; paragraph-level jobs live in the
Unit's outline. This is the venue closest to an academic paper.

Default section structure (adjust per released card and audience):

```yaml
sections:
  - 01-subgroup-profile    # who the cohort is (D)
  - 02-exploration         # what was tried / examined (D/I)
  - 03-findings            # what the evidence shows (I/K)
  - 04-messages            # what we say / recommend (K/W)
  - 05-performance         # how it performed (I/K)
  - 06-gate-check          # settlement + caveats before shipping
```

### D3/D4 · judge and decide
Judge the formal report against the evidence bar and venue rails, render its
exact version under `delivery/render/`, then accept or emit.
