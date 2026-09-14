# Venue Profile Schema

Every venue profile is a uniform Design reference pack:

```text
venue-<name>/
├── README.md           constraints · Design profile · output grammar · phase use
├── style-profile.md    voice/format examples and self-review rails
└── exemplars/          optional real artifacts to pattern-match
```

Venue profiles are **knowledge, not skills and not workflows**. The released
Brief roster pins one primary venue; each Commission compiles the selected
pack into frozen criteria. No venue creates its own lifecycle.


Design profile block (required in every README)
================================================

```yaml
design_profile:
  evidence_bar: light | medium | full
  narrative: required | optional | none
  display: required | optional | none
  section_edit: required | optional | none
  terminal: adopted
```

The three composition fields describe what the generated Unit must contain;
they are not phases. `evidence_bar` narrows the Commission's allowed inputs and
criteria:

- **light** — every load-bearing move resolves through Commission inputs; a
  non-load-bearing convention may be labeled as a venue convention.
- **medium** — every primary section/item/move maps to the grant; every open
  load-bearing gap emits a BR00 need and Insight register question.
- **full** — every displayed fact, metric, recommendation, and decision unit
  maps to an accepted source in the grant; no load-bearing gap remains hidden.

The grant stays inside board `reads:`. Design freezes signed Wisdom handoffs and
other explicitly allowed sources by exact path/version/hash; it never opens
D/I/K pages or raw Task results to manufacture support and never creates a new
PageX lane. If the bar cannot be met, the Run returns a named gap or hold; it
does not substitute “common knowledge” or open a private ask session.


Phase use (required in every README)
====================================

Each pack states only its delta inside the shared workflow:

```text
Commission  pin audience × job × venue and compile rails before release
Generate    author the exact content/spec/layout the profile requires
Verify      independently test every candidate against rails and evidence bar
Preview     write delivery/render/ from exact immutable Result members
Adopt       a person selects or declines exact verified preview versions
```

Adoption names the exact file under `delivery/render/`. `adopted` is the
Application terminal. Build, deploy, distribute, allocate, and measure are
downstream Task-Face work in another Folder.


Venue template (when useful)
============================

A fixed template may describe output slots, but a slot's evidence source is
always one of:

```text
personalization/variable contract
released Brief requirement
Commission input through a signed Wisdom handoff
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
