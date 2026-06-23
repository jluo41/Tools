---
name: haipipe-application-venue
description: "Venue selection for the intervention lifecycle. Chooses the output modality (SMS, checklist, reminder, push, email, dashboard, UI card, report) and pins it in STATUS.md. The venue reshapes every downstream stage: which stages are required/skip, claims depth, content structure, and draft format. Runs after pitch, before claims. Modeled on haipipe-paper-venue. Trigger: venue, format, modality, what format, which channel, /haipipe-application venue."
argument-hint: "[venue-name] [intervention-path]"
allowed-tools: Bash, Read, Write, Edit, Grep, Glob, Skill
metadata:
  version: "1.0.0"
  last_updated: "2026-06-23"
  summary: "Venue selection — choose output modality, pin in STATUS.md."
  changelog:
    - "1.0.0 (2026-06-23): initial version modeled on paper-venue."
---

Skill: haipipe-application-venue
==================================

Chooses the output modality for the intervention and pins it in
STATUS.md. The venue determines which lifecycle stages fire, how
deep the claims stage goes, and what the draft looks like.

Runs between **pitch** and **claims** — same position as paper's
venue selection.


Available venues
=================

```
venue-sms               160-char SMS messages
venue-push              push notifications (< 50 char title)
venue-reminder          time-triggered recurring reminders
venue-checklist         actionable checklist (5-12 items)
venue-email             longer-form email with sections
venue-dashboard         data-rich provider dashboard
venue-ui-card           in-app card / widget
venue-report            stakeholder report (formal)
```


Stage requirements per venue
==============================

The venue profile declares which lifecycle stages are required,
optional, or skip:

```
                    seed   pitch   claims   narrative   display   minimap
                    ─────  ─────   ──────   ─────────   ───────   ───────
venue-sms           req    req     req      skip        skip      skip
venue-push          req    req     req      skip        skip      skip
venue-reminder      req    req     req      skip        skip      skip
venue-checklist     req    req     req      optional    skip      skip
venue-email         req    req     req      req         optional  skip
venue-dashboard     req    req     req      req         req       req
venue-ui-card       req    req     req      req         req       optional
venue-report        req    req     req      req         req       req
```

**seed, pitch, claims** are always required. They are the minimum
viable lifecycle — you always need to know why (seed), what (pitch),
and which evidence backs it (claims).

**narrative, display, minimap** scale with output complexity. Simple
venues (SMS, push) have fixed templates that answer these questions
implicitly. Complex venues (dashboard, report) need explicit design.


Claims depth per venue
========================

The claims stage is always present but its depth scales:

```
claims_depth    venues                     what it means
────────────    ──────────────────────     ────────────────────────────
light           sms, push, reminder        SELECT from existing K/W.
                                           List which K/W entries inform
                                           each part of the output.
                                           No probe planning.

medium          checklist, email           SELECT + gap check.
                                           Verify K/W covers all items.
                                           Optional probe if gap found.

full            dashboard, ui-card,        Full claim ledger.
                report                     GAP/weak/supported per claim.
                                           Probe plans for GAPs.
```

Light claims for SMS example:
```markdown
## Claims (light)
- Benefit sentence draws on: K03 (timing sensitivity)
- CTA draws on: W02 (recommend refill action)
- Personalization draws on: K07 (name improves engagement)
- No gaps — all K/W entries are active and supported.
```

Full claims for dashboard example:
```markdown
## Claims (full)
### C01: Refill timing predicts adherence
- Status: supported
- Evidence: K03
### C02: Provider dashboard reduces missed refills
- Status: GAP
- Probe plan: PP01_dashboard_effectiveness
```


Venue template (for simple venues)
=====================================

Simple venues (skip narrative/display/minimap) include a
**venue template** that replaces those stages. The template
defines the fixed output structure:

```
venue-sms template:
  Slot 1: greeting     ← personalization
  Slot 2: benefit      ← primary claim
  Slot 3: CTA          ← action + timing
  Slot 4: close        ← reassurance / opt-out
```

The draft skill reads this template directly when
narrative/display/minimap are skip.


Workflow
=========

```
Step 1: Read 1-pitch.md (channel field suggests venue).

Step 2: If venue obvious from pitch → propose it.
        If ambiguous → present shortlist with pros/cons.

Step 3: User confirms or overrides.

Step 4: Pin venue in STATUS.md:
          venue: sms
          venue_profile: _venue/venue-sms/

Step 5: Report which stages are required/skip for this venue.
```


Venue change rule
==================

Changing venue after claims exist is a **loopback** — it
invalidates claims and everything downstream. The skill warns
and asks for confirmation before re-pinning.


Definition of done
===================

```
[ ] STATUS.md has venue: <name> and venue_profile: <path>
[ ] User saw and confirmed stage requirements
```
