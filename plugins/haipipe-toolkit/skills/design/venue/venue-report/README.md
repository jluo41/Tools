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
  terminal: adopted
```

## Phase use

### Commission and Generate

Every finding, recommendation, table, and figure maps through released
Commission inputs. A load-bearing gap returns as a named hold; Design never Probes.

### Generate · narrative requirement
Report arc depends on audience:
- Regulator: methodology → findings → limitations → recommendations
- Executive: bottom line → evidence → ask
- Partner: context → joint findings → next steps

### Generate · display requirement
Display map: tables (summary stats, comparisons), figures
(forest plots, trend charts), KPI callouts.

### Generate · section pass
Per-section review on the declared sections; paragraph-level jobs live in the
Unit's outline. This is the venue closest to an academic paper.

Default section structure (adjust per released Commission and audience):

```yaml
sections:
  - 01-subgroup-profile    # who the cohort is (D)
  - 02-exploration         # what was tried / examined (D/I)
  - 03-findings            # what the evidence shows (I/K)
  - 04-messages            # what we say / recommend (K/W)
  - 05-performance         # how it performed (I/K)
  - 06-gate-check          # settlement + caveats before shipping
```

### Verify and adopt
Judge the formal report against the evidence bar and venue rails, render its
exact version under `delivery/render/`, then adopt or decline.
