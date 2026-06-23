# Venue: SMS

Short message service. The simplest venue — 160-character segments,
plain language, single call-to-action.


## Constraints

- **Length:** 160 chars per segment; prefer 1 segment (≤ 160)
- **Language:** plain, 6th grade reading level
- **Links:** short URL only (≤ 30 chars)
- **Personalization:** patient name, medication name if available
- **CTA:** exactly one, specific and actionable
- **Opt-out:** required (STOP keyword or similar)


## Stage requirements

```yaml
stages:
  seed:       required
  pitch:      required
  claims:     required
  narrative:  skip
  display:    skip
  minimap:    skip

claims_depth: light
```


## Venue template

Replaces narrative/display/minimap for SMS:

```yaml
template:
  - slot: greeting
    job: establish identity + warmth
    claim_source: personalization
    chars: ~30
  - slot: benefit
    job: state the value proposition
    claim_source: primary claim (K/W)
    chars: ~60
  - slot: CTA
    job: specific action + deadline
    claim_source: action claim (W)
    chars: ~50
  - slot: close
    job: reassurance or opt-out
    claim_source: standard
    chars: ~20
```


## Lifecycle mappings

### → Claims (light)
Select from existing K/W. Each slot maps to one K/W entry.
No probe planning — if the KB lacks coverage, either use
common knowledge or trigger an ask session first.

### → Draft
Follow the 4-slot template. Each slot is one sentence or phrase.
Total ≤ 160 chars for single-segment SMS.
Tone per audience profile (warm for patient, clinical for clinician).

### → Review
Check: within char limit, CTA is actionable, opt-out present,
no jargon (if patient), cited_K in frontmatter.
