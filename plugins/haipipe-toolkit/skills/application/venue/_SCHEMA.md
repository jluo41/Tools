# Venue Profile Schema

Every venue profile is a uniform Design reference pack:

```text
venue-<name>/
├── README.md           constraints · Design profile · output grammar · phase use
├── style-profile.md    voice/format examples and self-review rails
└── exemplars/          optional real artifacts to pattern-match
```

Venue profiles are **knowledge, not skills and not workflows**. D0 pins one
primary venue in the Brief roster; D1-D4 read the pack. No venue creates Seed,
Pitch, Claims, Narrative, Display, Draft, deployment, or another lifecycle.
Those retired Application stages must never reappear in a venue pack.


Design profile block (required in every README)
================================================

```yaml
design_profile:
  evidence_bar: light | medium | full
  narrative: required | optional | none
  display: required | optional | none
  section_edit: required | optional | none
  terminal: accepted
```

The three composition fields describe what the D2 Unit must contain; they are
not phases. `evidence_bar` narrows the released card's grant:

- **light** — every load-bearing move resolves through the card grant; a
  non-load-bearing convention may be labeled as a venue convention.
- **medium** — every primary section/item/move maps to the grant; every open
  load-bearing gap emits a BR00 need and Insight register question.
- **full** — every displayed fact, metric, recommendation, and decision unit
  maps to an accepted source in the grant; no load-bearing gap remains hidden.

The grant stays inside board `reads:`. Design binds signed Wisdom handoffs and
other explicitly allowed sources through PageX; it never opens D/I/K pages or
raw Task results to manufacture support. If the bar cannot be met, D4 emits —
it does not substitute “common knowledge” or open a private ask session.


Phase use (required in every README)
====================================

Each pack states only its delta inside the shared workflow:

```text
D0 frame      pin audience × job × venue, outcome, guardrail, kill, variables
D1 bet        compile the venue rails into each named card packet
D2 realize    author the exact content/spec/layout the profile requires
D3 judge      test every candidate/variant against rails and evidence bar
D4 decide     write delivery/render/, then accept or emit
D5 page down  reread affected prose; the venue adds no independent work
```

Acceptance names the exact file under `delivery/render/`. `accepted` is the
Application terminal. Build, deploy, distribute, allocate, and measure are
downstream Task-Face work in another Folder.


Venue template (when useful)
============================

A fixed template may describe output slots, but a slot's evidence source is
always one of:

```text
personalization/variable contract
GD0-closed Brief requirement
released card grant through a signed Wisdom handoff
venue convention, explicitly labeled and non-load-bearing
```

Never name a retired Claims stage or direct K/W lookup as the slot source.


Available venues
================

```text
venue-sms               160-character SMS messages · light
venue-push              push notifications · light
venue-reminder          recurring reminders · light
venue-checklist         actionable checklist, 5-12 items · medium
venue-email             longer-form email with sections · medium
venue-dashboard         data-rich provider dashboard · full
venue-ui-card           in-app card/widget · full
venue-report            formal stakeholder report · full
```


Audience
========

Venue and audience are orthogonal but coupled. Venue determines structure;
audience determines tone, language, evidence depth, accessibility, and visible
citation style. The style profile's tone-by-audience rows are the audience axis;
there is no separate audience lifecycle or directory.
