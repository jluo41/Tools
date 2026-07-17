---
name: haipipe-application-venue
description: "Venue selection for the intervention lifecycle — the decision gate between the venue-FREE stages (seed, the 1a-1d evidence ladder) and the venue-ALIGNED stages (pitch, narrative, display, section-edit). Chooses the output modality (sms, push, reminder, checklist, email, dashboard, ui-card, report), pins it in STATUS.md (venue + stages_skipped + claims_settlement), and produces 0-lifecycle/2-venue/2-venue.md with Artifact Principles — the concrete downstream contract (template/slots, limits, tone-by-audience, element types, section structure, gate depth) that pitch/display/section-edit/artifact all read. Runs AFTER the ladder (1d gate), BEFORE pitch. Re-pin re-couples pitch+; the ladder SURVIVES. Trigger: venue, format, modality, which channel, /haipipe-application venue."
argument-hint: "[venue-name] [intervention-path] [--no-pin]"
allowed-tools: Bash, Read, Write, Edit, Grep, Glob, Skill
metadata:
  version: "3.2.0"
  last_updated: "2026-07-17"
  summary: "Venue stage: recommends + pins the output modality and produces 2-venue.md (template ref/venue-template.md) — the decision gate between the venue-FREE ladder and the venue-ALIGNED stages; writes the three STATUS rows (venue / stages_skipped / claims_settlement) and Artifact Principles as the downstream channel-HOW contract. History: ./CHANGELOG.md."
  # version history: ./CHANGELOG.md (skill-scoped, never loaded at invocation)
---

Skill: haipipe-application-venue
==================================

The decision gate: which output modality carries this intervention, and how deep must the evidence settle for it?

```text
seed + 1a-descriptions -> 1b-themes -> 1c-claims -> 1d-advice   venue-FREE (the ladder)
[ venue ]   <- THIS STAGE: pins the modality, gates what follows
2-pitch -> 3-narrative° -> 4-display° -> 5-section-edit°         venue-ALIGNED (° = gated)
```

Read first: `../../PHILOSOPHY.md`; the pinned venue's pack `../../venue/venue-<name>/` (consult, never restate).


## What's special: three things make the venue the gate

**1. It splits venue-FREE from venue-ALIGNED.**
Everything upstream — seed and the 1a-1d ladder — is settled venue-free: data truth, patterns, claims, and content-level design advice do not change with the channel.
Everything downstream, pitch onward, couples to the pinned venue.
The venue packs are knowledge, not skills; this skill is the READER that turns one into a pinned contract, never editing a pack.

**2. The pin writes three STATUS.md rows the whole system reads.**
The strip, lifecycle router, claims gate, and artifact composer all read these:
```text
| venue | sms |
| stages_skipped | narrative display section-edit |
| claims_settlement | light |
```
Per-venue values (authoritative source: each `../../venue/venue-<name>/README.md`):
```text
                   narrative  display  section-edit  claims_settlement  gate depth
sms/push/reminder  skip       skip     skip          light              inline
checklist          optional   skip     skip          medium             inline
email              req        optional skip          medium             inline
dashboard          req        req      req           full               report
ui-card            req        req      optional      full               report
report             req        req      req           full               report
```
An `optional` stage is skipped by default and pulled in on user request (then removed from `stages_skipped`).

**3. Artifact Principles is the channel-HOW contract — distinct from 1d's content-WHAT.**
2-venue.md distills the pack + audience profile into concrete specs: template/slots or section structure, length limits, tone (register from the audience profile), element types, settlement + gate depth, compliance rails.
pitch, display, section-edit, and artifact read the shape here — no re-deriving from the pack per stage.
This is channel-HOW (how to shape the deliverable), distinct from 1d-advice's content-WHAT (what the evidence advises).


## The four phases, in venue

```text
DRAFT   read 1c-claims.md (the campaign shapes which venues fit) + 1d-advice.md (the advice the
        venue must carry) + seed's channel hunch; propose an obvious venue, or a shortlist with
        pros/cons (evidence depth vs venue demands, audience fit); on the user's confirm PIN the
        three STATUS rows and write 2-venue.md (Artifact Principles + Fit Assessment against the
        campaign). --no-pin = recommend only, write nothing.
PROBE   light, and often skipped — venue-level questions only (channel capability, compliance
        constraints, prior sends on this channel), raised as sections in 1-probes/PPNN_<topic>.md
        and dispatched via Agent(haipipe-probe-q-executor-agent). Routing mechanics are the probe
        layer's: ../../2-phase/1-probe/haipipe-application-probe/SKILL.md (see its
        ref/per-stage-dispatch.md, the "2-venue" entry).
REVISE  tighten Artifact Principles into concrete specs (no "see pack" hand-waves); sharpen the
        Fit Assessment's settlement delta.
CHECK   three STATUS rows present; Artifact Principles concrete; Fit Assessment names the
        settlement delta; user saw + confirmed the stage set and the settlement bar.
```

Retarget: changing venue later re-runs this stage — 2-venue.md rewrites with new Artifact Principles, and pitch/narrative/display/section-edit rewrite, artifacts re-compose.
The claims ledger SURVIVES; a new venue may RAISE `claims_settlement` (more settlement work on the SAME campaign, not invalidation) or relax it.
The skill states exactly what re-opens and asks before re-pinning.


## The artifact

`0-lifecycle/2-venue/2-venue.md` — full skeleton in `ref/venue-template.md`:

```text
Choice              which venue for which audience, one-line why, rejected shortlist
Fit Assessment      the pinned venue's settlement bar vs the current Evidence Campaign (1c):
                    what meets the bar, what must settle before draft
Artifact Principles the downstream contract — template/slots or section structure, length limits,
                    tone, element types, settlement + gate depth, compliance rails
Q-consumer          venue-level investigation questions (channel capability, compliance, prior sends)
```

Sidecar: `_LOG_2-venue.md` (phase journal).
Formatting per the template: `=====` title, `-----` sections, no `#` headings, one sentence per line.


## Exits

```text
promote  -> /haipipe-application pitch   frame the sell for the pinned venue + audience
retarget -> re-run venue                 new modality; the ladder survives, settlement re-scales
```

End every reply with the closing block (stage line via `../../haipipe-application/stage-strip.sh`; the venue slot renders ✅ from the pinned STATUS field).
