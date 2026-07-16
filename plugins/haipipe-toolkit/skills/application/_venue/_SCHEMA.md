# Venue Profile Schema

Every venue profile is a uniform pack (modeled on paper's venue
packs under `paper/_venue/_SCHEMA.md`).

```
venue-<name>/
├── README.md           hub: constraints, stage requirements,
│                       venue template, lifecycle mappings
├── style-profile.md    voice/format examples to imitate
└── exemplars/          real artifacts to pattern-match
```

Venue profiles are **knowledge, not skills**. They are consulted
by path, never invoked as skills. The venue selection skill
(`haipipe-application-venue`) pins one venue in STATUS.md; every
downstream stage reads the pinned venue's profile.


Stage requirements block (in README.md)
=========================================

Every venue README.md MUST include a `stages:` block declaring
which lifecycle stages are required, optional, or skip:

```yaml
stages:
  seed:       required
  pitch:      required
  claims:     required
  narrative:  required | optional | skip
  display:    required | optional | skip
  section-edit: required | optional | skip
```

seed, claims, pitch are ALWAYS required — they are the minimum viable
lifecycle (spine order: seed → claims → [venue pin] → pitch; seed and
claims are venue-FREE and already exist when the venue is pinned).
At pin time `haipipe-application-venue` translates this block into the
STATUS.md `| stages_skipped |` row.


Claims settlement (in README.md)
==================================

```yaml
claims_settlement: light | medium | full
```

The venue-FREE claims ledger always has the same shape; this field sets
the SETTLEMENT BAR its CHECK gate applies before artifact work
(spec: claims skill §Settlement Gate):

- **light**: every claim the artifact leans on tied to a named K/W or
  "common knowledge"; GAPs allowed if not load-bearing
- **medium**: primary claims supported or weak-with-caveat; load-bearing
  GAPs have a campaign row (an open question in 1-probes/)
- **full**: primary claims supported by judged answers; load-bearing
  GAPs settled


Venue template (in README.md)
===============================

For venues that skip narrative/display/section-edit, the venue template
replaces those stages with a fixed output structure (the K/W-to-slot
mapping happens at draft, venue-ALIGNED — never in claims):

```yaml
template:
  - slot: greeting
    job: establish identity + warmth
    claim_source: personalization
  - slot: benefit
    job: state the value proposition
    claim_source: primary claim
  - slot: CTA
    job: specific action + deadline
    claim_source: action claim
  - slot: close
    job: reassurance + opt-out
    claim_source: standard
```


Lifecycle mappings (in README.md)
===================================

Each venue declares how it affects the lifecycle stages that DO fire:

```
→ Claims:       the settlement bar (what counts as settled for this venue)
→ Narrative:    arc structure (if required)
→ Display:      available element types + unit-job granularity (if required)
→ Section-edit: section list + per-section jobs (sectioned venues)
→ Draft:        format constraints + style from exemplars/
```


Stage requirements summary
============================

```
                    seed   claims   pitch   narrative   display   section-edit
                    ─────  ──────   ─────   ─────────   ───────   ────────────
venue-sms           req    req      req     skip        skip      skip
venue-push          req    req      req     skip        skip      skip
venue-reminder      req    req      req     skip        skip      skip
venue-checklist     req    req      req     optional    skip      skip
venue-email         req    req      req     req         optional  skip
venue-dashboard     req    req      req     req         req       req
venue-ui-card       req    req      req     req         req       optional
venue-report        req    req      req     req         req       req
```


Available venues
=================

```
venue-sms               160-char SMS messages (light claims)
venue-push              push notifications (light claims)
venue-reminder          time-triggered recurring reminders (light claims)
venue-checklist         actionable checklist, 5-12 items (medium claims)
venue-email             longer-form email with sections (medium claims)
venue-dashboard         data-rich provider dashboard (full claims)
venue-ui-card           in-app card / widget (full claims)
venue-report            stakeholder report, formal (full claims)
```


Relation to _audience/
========================

Venue and audience are orthogonal but coupled:
- **Venue** determines structure, constraints, delivery mechanism
- **Audience** determines tone, language, evidence depth, citation format

Both are consulted. Venue is primary (structure), audience is
secondary (style within structure). A patient can receive an SMS
or a push notification; a clinician can receive a dashboard or
an email. The venue profile says WHAT the output looks like;
the audience profile says HOW it sounds.
