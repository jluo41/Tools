# Venue: SMS

Short message service. The simplest venue — 160-character segments,
plain language, single call-to-action.


## Constraints

- **Length:** 160 chars per segment; prefer 1 segment (≤ 160)
- **Language:** plain, 6th grade reading level
- **Links:** short URL only (≤ 30 chars)
- **Personalization:** the reader's name, the item's name if available
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

This is a venue reference pack, not a private lifecycle. On the design ladder
(`haipipe-design/ref/design-ladder.md`) a Job pins a goal whose `venue:` is `sms`;
its design Runs (reason, generate, verify, rank) read this pack through the Job's
`inputs/` fence, and a person releases the kept designs (`haipipe-design-delivery`).
An older board's Commission → Generate → Verify reads it the same way.


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
    claim_source: a fence file (the signed Wisdom handoff) or own knowledge
    chars: ~60
  - slot: CTA
    job: specific action + deadline
    claim_source: the signed goal + the signed Wisdom handoff
    chars: ~50
  - slot: close
    job: reassurance or opt-out
    claim_source: standard
    chars: ~20
```


## Run guidance

### Goal and fence · frame and bet

The goal (`board.md ## Goals`: who, `venue: sms`, n) and the shared rules pin the
audience, the job, one primary venue, CTA availability, the opt-out mechanism, and
the variables the system can actually supply. The design work may use only the
files of the Job's `inputs/` fence (the signed handoff, the rules, what the method's
step ① sees). Design never reads D/I/K pages directly.

### generate ③ · realize

Follow the 4-slot template. Each slot is one sentence or phrase.
Total ≤ 160 chars for single-segment SMS.
Tone per audience profile (warm and plain for a general reader, exact for a professional).

### verify ④ (another agent)

Check every design for character count, actionable single CTA, opt-out, variable
availability, audience language, and fidelity to the signed goal and its rules (T0),
and every element's source against the fence (T1). Any preview stays inside the
verify's Result and is a Step, not a Run. An independent verify pass makes the draft
`passed`; t99 ranks the passed designs and a person releases the kept.

If a load-bearing premise or variable is missing from the fence, say so in the
review and name the input it needs: that is a new inputs version and a new Job (or
the design dropped), never a revise. Do not substitute “common knowledge” for a
missing source, open a private ask session, or mark the SMS deployed. Sending is
downstream.
