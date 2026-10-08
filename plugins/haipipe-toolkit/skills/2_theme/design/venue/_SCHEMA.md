# Venue Profile Schema

Every venue profile is a uniform Design reference pack:

```text
venue-<name>/
├── README.md           constraints · Design profile · output grammar · Run guidance
├── style-profile.md    voice/format examples and self-review rails
└── exemplars/          optional real artifacts to pattern-match
```

Venue profiles are **knowledge, not skills and not workflows**. A goal's
`venue:` (board.md ## Goals) names its one venue; the Job's pinned method
version reads the selected pack into its frozen checks. No venue creates its
own lifecycle.

The Job's set-up resolves venue defaults against the goal's audience and N
before any design is made, including one explicit word budget. The worker
follows that frozen contract. A goal-only mockup or specification
labels sample values and missing sources; it cannot claim accepted findings,
live refresh, or production readiness from a venue example.


Design profile block (required in every README)
================================================

```yaml
design_profile:
  evidence_bar: light | medium | full
  narrative: required | optional | none
  display: required | optional | none
  section_edit: required | optional | none
```

The three composition fields describe what the generated Unit must contain;
they describe content, not execution units. `evidence_bar` narrows what the Job's inputs/ fence (its
manifest) must carry and how the checks read it:

- **light** — every load-bearing move resolves through the Job's inputs/ fence (its manifest); a
  non-load-bearing convention may be labeled as a venue convention.
- **medium** — every primary section/item/move maps to a file in the fence; every open
  load-bearing gap returns a hold naming the missing input; a new input is a new inputs version, so a new Job.
- **full** — every displayed fact, metric, recommendation, and decision unit
  maps to an accepted source in the fence; no load-bearing gap remains hidden.

The input scope is the Job's inputs/ fence: the pinned inputs version freezes signed Wisdom handoffs and
other sources by exact path and sha; the design work never opens D/I/K pages or raw Task results to
manufacture support. If the bar cannot be met, the Run returns a named gap or hold; it does not
substitute “common knowledge” or open a private ask session.


Run guidance (required in every README)
====================================

Each pack states only its delta inside the method's steps (haipipe-design/ref/design-ladder.md):

```text
① see input   the Job's inputs/ fence: the goal, the shared rules, this pack, the pinned inputs version
② reason      ideas that fit this venue's shape and budget
③ generate    author the exact content/spec/layout the profile requires
④ verify      another agent tests each design against the rails and the evidence bar
⑤ rank        t99 ranks the passed designs and keeps N
release       a person releases the kept designs into delivery/
```

A Workflow is a list of Runs. A pack supplies guidance for these steps; it does
not add lifecycle states. A passed verify ④, then t99's rank ⑤ and a person's
release, put a design in delivery/. Render/preview is an internal Step: write
pictures and measurements in the current Run's result/ and pin its render
manifest. The presenter reads them without worker writes to delivery/. Build,
deploy, distribute, allocate and measure belong to downstream work.


Venue template (when useful)
============================

A fixed template may describe output slots, but a slot's evidence source is
always one of:

```text
personalization/variable contract
the signed goal (board.md ## Goals) and the shared rules (design-goal.md)
a fence file through a signed Wisdom handoff
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
