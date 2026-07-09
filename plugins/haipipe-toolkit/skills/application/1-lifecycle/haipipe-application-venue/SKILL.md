---
name: haipipe-application-venue
description: "Venue selection for the intervention lifecycle — the decision gate between the venue-FREE stages (seed, claims) and the venue-ALIGNED stages (pitch, narrative, display, section-edit). Chooses the output modality (sms, push, reminder, checklist, email, dashboard, ui-card, report), pins it in STATUS.md (venue + stages_skipped + claims_settlement), and produces 0-lifecycle/2-venue/2-venue.md with Artifact Principles — the concrete downstream contract (template/slots, limits, tone-by-audience, element types, section structure, gate depth) that pitch/display/section-edit/artifact all read. Runs AFTER claims, BEFORE pitch. Re-pin re-couples pitch+; claims SURVIVES. Trigger: venue, format, modality, which channel, /haipipe-application venue."
argument-hint: "[venue-name] [intervention-path] [--no-pin]"
allowed-tools: Bash, Read, Write, Edit, Grep, Glob, Skill
metadata:
  version: "3.0.0"
  last_updated: "2026-07-06"
  summary: "Port of paper venue 2.0.0 (765696f): venue becomes an artifact-producing stage — 2-venue/2-venue.md + _LOG + _PROBE/ with Artifact Principles as the downstream contract. Still writes the 3 STATUS rows (strip/lifecycle/gate read those). Dual-2 numbering mirrors paper (2-venue + 2-pitch)."
  # version history: ./CHANGELOG.md (skill-scoped, never loaded at invocation)
---

Skill: haipipe-application-venue
==================================

Chooses the output modality for the intervention, pins it in STATUS.md, and DISTILLS the venue pack + audience profile into a stage document the downstream stages consume. The venue gates which stages fire, how much of the claims campaign must settle, and what the artifact looks like.

Runs between **claims** and **pitch** -- the truth (seed, claims) is settled venue-free first; everything that SELLS or SHAPES it (pitch onward) is venue-aligned. The venue packs are knowledge, not skills; this skill is the READER that turns them into a pinned contract. It never edits a pack.

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

## Artifact Spec

**Files produced:**
- `0-lifecycle/2-venue/2-venue.md` -- venue stage document (choice + Artifact Principles + fit + probes)
- `0-lifecycle/2-venue/_LOG_2-venue.md` -- phase progress journal
- `0-lifecycle/2-venue/_PROBE/` -- venue-level probe cards (channel capability, compliance constraints, prior sends on this channel)
- `STATUS.md` -- the three pinned rows (below)

**Content structure (2-venue.md):**

```text
2-venue: <intervention name>
=============================

Venue Choice            which venue, one-line why, backup options
Venue Profile           audience, channel mechanics, what this venue rewards
Artifact Principles     concrete specs that downstream stages consume
Fit Assessment          claims campaign vs venue demands + settlement-bar delta
Probes                  venue-level investigation needs
```

**Artifact Principles section (the key downstream contract):**
- Template/slots or section structure: the output's fixed shape (slots for simple venues; section list for sectioned venues)
- Length limits: char/word budgets per slot/section/segment
- Tone: register from the audience profile (reading level, jargon rules, citation visibility)
- Element types: which display elements the venue supports (sectioned venues)
- Settlement + gate depth: the claims bar this venue demands and whether CHECK runs inline or as a report
- Compliance rails: opt-out, PHI, program guardrails

This section is what pitch, display, section-edit, and artifact all read. Once venue is pinned, Artifact Principles tells you concretely how to shape the deliverable -- no re-deriving from the pack per stage.

**Formatting (artifact):** `=====` title / `-----` sections, no `#` headings; one sentence per line.

**Canonical template (source of truth for 2-venue.md section order + placeholders):** `ref/venue-template.md`.

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

An `optional` stage is skipped by default and pulled in on user request (then removed from `stages_skipped`).

Workflow
=========

```
Step 1: Read 0-lifecycle/1c-claims/1c-claims.md (the campaign shapes which venues
        are viable) + 0-lifecycle/1d-principles/1d-principles.md (the directives
        the venue must carry) + 0-seed's channel hunch.
Step 2: If venue obvious → propose it. If ambiguous → present a shortlist with
        pros/cons (evidence depth vs venue demands; audience fit).
Step 3: User confirms or overrides (--no-pin = recommend only, write nothing).
Step 4: Pin in STATUS.md (three rows, from the venue pack's README) AND write
        0-lifecycle/2-venue/2-venue.md: distill the pack + audience profile
        into Artifact Principles; run the Fit Assessment against the campaign.
Step 5: Report which stages fire + whether the campaign already meets the
        settlement bar (if not: name the claims work left). Venue-level probes
        (channel capability, compliance) buffer in 2-venue/_PROBE/.
```

Venue change rule (retarget)
=============================

Changing venue later re-couples the venue-ALIGNED stages ONLY: 2-venue.md rewrites (new principles), pitch/narrative/display/section-edit rewrite, artifacts re-compose. The claims ledger SURVIVES -- the new venue may raise `claims_settlement`, which is additional settlement work on the SAME campaign, not invalidation. The skill states exactly what re-opens and asks for confirmation before re-pinning.

**Done-criteria:**
- [ ] STATUS.md has | venue |, | stages_skipped |, | claims_settlement | rows
- [ ] 2-venue.md exists with Artifact Principles filled with concrete specs (no "see pack" hand-waves)
- [ ] Fit Assessment maps the claims campaign to the venue's demands; settlement delta named
- [ ] User saw and confirmed the stage requirements + settlement bar

End the reply with the closing block (stage line via `../../haipipe-application/stage-strip.sh`; the venue slot renders ✅ from the pinned STATUS field).
