---
name: haipipe-application-draft
description: "Single draft skill for the intervention lifecycle. Reads the pinned venue profile (template, constraints, style-profile, exemplars), the audience profile, and the claims (K/W selections), then generates the artifact. No venue-specific sub-skills — the venue profile IS the instruction set. For simple venues (SMS): reads venue template + claims → generates artifact directly. For complex venues (dashboard): reads narrative + display + minimap → generates spec. Trigger: draft, write, create, generate, make the SMS, draft it, /haipipe-application draft."
argument-hint: "[intervention-path]"
allowed-tools: Bash, Read, Write, Edit, Grep, Glob, Skill
metadata:
  version: "2.0.0"
  last_updated: "2026-06-23"
  summary: "Single generic draft skill — venue profile is the instruction set."
  changelog:
    - "2.0.0 (2026-06-23): removed format specialist dispatch; venue profile carries all drafting instructions."
    - "1.0.0 (2026-06-22): initial version with format specialist dispatch."
---

Skill: haipipe-application-draft
==================================

One skill, all venues. The venue profile carries the drafting
instructions — template, constraints, style guide, exemplars.
No venue-specific sub-skills needed.


How it works
=============

```
1. Read STATUS.md → pinned venue + audience
2. Load venue profile:
     _venue/venue-<name>/README.md      constraints + template
     _venue/venue-<name>/style-profile.md   voice + drafting rules
     _venue/venue-<name>/exemplars/     real artifacts to imitate
3. Load audience profile:
     _audience/profile-<audience>/README.md   tone + citation rules
4. Load claims:
     0-lifecycle/2-claims.md            K/W selections or claim ledger
5. Load lifecycle artifacts (if venue required them):
     0-lifecycle/3-narrative.md         arc structure (if exists)
     0-lifecycle/4-display.md           content elements (if exists)
     0-lifecycle/5-minimap.md           widget jobs (if exists)
6. Generate the artifact following all of the above.
7. Write to 0-artifacts/<slug>-v{N}.md
```


Simple venues (SMS, push, reminder)
======================================

For venues that skip narrative/display/minimap, the draft skill
reads the venue template directly:

```
Input:   claims(light) + venue template + audience profile
Output:  one artifact following the template slots

Example (venue-sms):
  Slot 1 (greeting):  "Hi [Name], your [Medication]..."  ← personalization
  Slot 2 (benefit):   "Refilling on time helps..."       ← K03
  Slot 3 (CTA):       "Reply REFILL to start"            ← W02
  Slot 4 (close):     "Reply STOP to opt out"             ← standard
```

The venue template + style-profile.md give enough structure to
draft directly from claims. No intermediate lifecycle artifacts.


Complex venues (dashboard, report)
=====================================

For venues that require narrative/display/minimap, the draft skill
reads all lifecycle artifacts:

```
Input:   claims(full) + narrative + display + minimap
         + venue style-profile + audience profile
Output:  spec document with structure from minimap,
         content elements from display, arc from narrative
```


Artifact output
================

```
<intervention-root>/0-artifacts/<slug>-v{N}.md
```

Version N increments on re-draft (after round feedback).
Previous versions kept for diff.


Artifact frontmatter
=====================

```yaml
---
kind: intervention
venue: <pinned venue>
audience: <audience>
intent: "<from pitch>"
created: YYYY-MM-DD
cited_K: [K03, K05]
cited_W: [W02]
status: draft | reviewed | deployed
---
```


Self-review (built into draft)
================================

After generating, run the venue's self-review checklist from
`style-profile.md`. If any check fails, note it in the artifact
as a `## Review notes` section and set `status: draft`.


Workflow
=========

```
Step 1: Read STATUS.md → venue, audience.
        If no venue pinned → BLOCK ("run /haipipe-application venue first").

Step 2: Load venue profile (README.md + style-profile.md + exemplars/).

Step 3: Load audience profile.

Step 4: Load claims (2-claims.md).

Step 5: Load lifecycle artifacts (narrative/display/minimap if they exist).

Step 6: Generate artifact following:
        - Venue template/structure (from README.md)
        - Voice and drafting rules (from style-profile.md)
        - Exemplar patterns (from exemplars/)
        - Tone and citation format (from audience profile)
        - Evidence backing (from claims K/W selections)

Step 7: Run self-review checklist from venue style-profile.md.

Step 8: Write to 0-artifacts/<slug>-v{N}.md (atomic).

Step 9: Report: "Drafted <venue> artifact for <audience>. Status: draft.
        Run /haipipe-application review to check."
```


Definition of done
===================

```
[ ] 0-artifacts/<slug>-v{N}.md exists
[ ] Frontmatter complete (venue, audience, cited_K, cited_W)
[ ] Content follows venue template/structure
[ ] Tone matches audience profile
[ ] Self-review checklist run (issues noted if any)
```


Risk profile
=============

WRITES one artifact to `0-artifacts/`. READ-ONLY on everything else.
