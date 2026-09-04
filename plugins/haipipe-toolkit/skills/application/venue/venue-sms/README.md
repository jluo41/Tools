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
  terminal: accepted
```

This is a venue reference pack, not a private lifecycle. D0-D5 remain the only
Design workflow phases. It never invents Seed, Pitch, Claims, deployment, or a
second status ladder.


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
    claim_source: card grant through the signed Wisdom handoff
    chars: ~60
  - slot: CTA
    job: specific action + deadline
    claim_source: GD0-closed Brief + signed Wisdom handoff
    chars: ~50
  - slot: close
    job: reassurance or opt-out
    claim_source: standard
    chars: ~20
```


## Phase use

### D0/D1 · frame and bet

Pin `kind: sms`, audience, job, one primary venue, CTA availability, opt-out
mechanism, and variables the system can actually supply. A card may grant only
the signed handoff/Brief/other sources allowed by the DesignBoard's `reads:`.
Design never reads D/I/K pages directly.

### D2 · realize

Follow the 4-slot template. Each slot is one sentence or phrase.
Total ≤ 160 chars for single-segment SMS.
Tone per audience profile (warm for patient, clinical for clinician).

### D3/D4 · judge, render, decide

Check every candidate or variant for character count, actionable single CTA,
opt-out, variable availability, audience language, and fidelity to the released
card. Render only to `delivery/render/`; acceptance names that exact render.

If a load-bearing premise or variable is missing, emit a BR00 need and its
Insight register question. Do not substitute “common knowledge,” open a private
ask session, or mark the SMS deployed. Shipping is downstream Task work.
