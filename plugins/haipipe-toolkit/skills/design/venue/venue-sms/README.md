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


## Design-workflow profile

```yaml
design_profile:
  evidence_bar: light
  narrative: none
  display: none
  section_edit: none
```

This is a venue reference pack, not a private lifecycle. The Design Workflow is a list of
Commission, Generate and Verify Runs. Delivery is the ready projection after
independent Verify passes.


## Venue template

Replaces narrative/display/section-edit for SMS:

```yaml
template:
  - slot: greeting
    job: establish identity + warmth
    claim_source: personalization
    chars: ~30
  - slot: benefit
    job: state the value proposition
    claim_source: Commission input through the signed Wisdom handoff
    chars: ~60
  - slot: CTA
    job: specific action + deadline
    claim_source: released Brief + signed Wisdom handoff
    chars: ~50
  - slot: close
    job: reassurance or opt-out
    claim_source: standard
    chars: ~20
```


## Run guidance

### Commission · frame and bet

Pin `kind: sms`, audience, job, one primary venue, CTA availability, opt-out
mechanism, and variables the system can actually supply. A Commission may use only
the signed handoff/Brief/other sources allowed by the DesignBoard's `reads:`.
Design never reads D/I/K pages directly.

### Generate · realize

Follow the 4-slot template. Each slot is one sentence or phrase.
Total ≤ 160 chars for single-segment SMS.
Tone per audience profile (warm for patient, clinical for clinician).

### Verify

Check every candidate or variant for character count, actionable single CTA,
opt-out, variable availability, audience language, and fidelity to the released
Commission. Any preview stays inside the current Result and is a Step, not a
Run. Independent Verify pass makes the exact message ready for Delivery.

If a load-bearing premise or variable is missing, emit a BR00 need and its
Insight register question. Do not substitute “common knowledge,” open a private
ask session, or mark the SMS deployed. Shipping is downstream Task work.
