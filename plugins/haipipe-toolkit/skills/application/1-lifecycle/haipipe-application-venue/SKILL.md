---
name: haipipe-application-venue
description: "Venue selection for the intervention lifecycle — the decision gate between the venue-FREE stages (seed, claims) and the venue-ALIGNED stages (pitch, narrative, display, section-edit). Chooses the output modality (sms, push, reminder, checklist, email, dashboard, ui-card, report) and pins it in STATUS.md, writing venue + stages_skipped + claims_settlement. Runs AFTER claims, BEFORE pitch — same position as paper's venue. Re-pin re-couples pitch+; claims SURVIVES. Trigger: venue, format, modality, which channel, /haipipe-application venue."
argument-hint: "[venue-name] [intervention-path] [--no-pin]"
allowed-tools: Bash, Read, Write, Edit, Grep, Glob, Skill
metadata:
  version: "2.0.0"
  last_updated: "2026-07-06"
  summary: "Paper-aligned: venue moves AFTER claims (was after pitch); the pin writes three STATUS.md rows (venue, stages_skipped, claims_settlement) that the strip/lifecycle/gate all read; venue-change rule inverted (claims survives, settlement may deepen); minimap column retired."
  # version history: ./CHANGELOG.md (skill-scoped, never loaded at invocation)
---

Skill: haipipe-application-venue
==================================

Chooses the output modality for the intervention and pins it in STATUS.md. The venue gates which downstream lifecycle stages fire, how much of the claims ledger must SETTLE before artifact work, and what the artifact looks like.

Runs between **claims** and **pitch** -- the same position as paper's venue selection: the truth (seed, claims) is settled venue-free first; everything that SELLS or SHAPES it (pitch onward) is venue-aligned.

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
venue-report            stakeholder report (formal, sectioned)
```

What the pin writes (STATUS.md)
================================

Three rows the whole system reads (strip, lifecycle router, claims gate, artifact):

```
| venue | sms |
| stages_skipped | narrative display section-edit |
| claims_settlement | light |
```

Per-venue values (authoritative source: each `_venue/venue-<name>/README.md`):

```
                 narrative   display   section-edit   claims_settlement   gate depth
venue-sms        skip        skip      skip           light               inline
venue-push       skip        skip      skip           light               inline
venue-reminder   skip        skip      skip           light               inline
venue-checklist  optional    skip      skip           medium              inline
venue-email      req         optional  skip           medium              inline
venue-dashboard  req         req       req            full                report
venue-ui-card    req         req       optional       full                report
venue-report     req         req       req            full                report
```

**seed and claims** always fire (venue-FREE, already done by the time this runs). **narrative, display, section-edit** scale with output complexity: simple venues have fixed templates that answer those questions implicitly; complex venues need explicit design. An `optional` stage is skipped by default and pulled in on user request (then removed from `stages_skipped`).

Claims settlement (what the depth means)
==========================================

The ledger's CONTENT is venue-free and already exists; the venue sets the BAR the claims CHECK gate applies before artifact work (spec: claims skill §Settlement Gate):

```
light    every claim the artifact leans on tied to a named K/W or "common knowledge"
medium   primary claims supported or weak-with-caveat; load-bearing GAPs have probe cards
full     primary claims supported by judged verdicts; load-bearing GAPs verdicted
```

Venue template (simple venues)
================================

Simple venues include a **template** in their pack that replaces narrative/display/section-edit. The artifact skill reads it directly:

```
venue-sms template:
  Slot 1: greeting     ← personalization
  Slot 2: benefit      ← primary claim (K/W)
  Slot 3: CTA          ← action + timing (W)
  Slot 4: close        ← reassurance / opt-out
```

The K/W-to-slot mapping happens at draft (venue-ALIGNED), never in claims.

Workflow
=========

```
Step 1: Read 0-lifecycle/1-claims/1-claims.md (what evidence exists shapes what
        venues are viable) + 0-seed's channel hunch.
Step 2: If venue obvious → propose it. If ambiguous → present a shortlist with
        pros/cons (evidence depth vs venue demands; audience fit).
Step 3: User confirms or overrides (--no-pin = recommend only, write nothing).
Step 4: Pin in STATUS.md: | venue | + | stages_skipped | + | claims_settlement |
        (from the venue pack's README).
Step 5: Report which stages fire for this venue + whether the current ledger
        already meets the settlement bar (if not: name the claims work left).
```

Venue change rule (retarget)
=============================

Changing venue later re-couples the venue-ALIGNED stages ONLY: pitch, narrative, display, section-edit rewrite; artifacts re-compose. The claims ledger SURVIVES -- the new venue may raise `claims_settlement` (sms → dashboard: light → full), which is additional settlement work on the SAME ledger, not invalidation. The skill states exactly what re-opens and asks for confirmation before re-pinning.

Definition of done
===================

```
[ ] STATUS.md has | venue |, | stages_skipped |, | claims_settlement | rows
[ ] User saw and confirmed the stage requirements + settlement bar
[ ] If the ledger falls short of the new bar: the gap is named as claims work
```

End the reply with the closing block (stage line via `../../haipipe-application/stage-strip.sh`).
