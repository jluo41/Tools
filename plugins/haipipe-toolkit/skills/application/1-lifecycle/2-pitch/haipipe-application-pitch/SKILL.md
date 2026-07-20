---
name: haipipe-application-pitch
description: "Stage 2 of the intervention lifecycle (venue-ALIGNED, first stage after the venue pin). Answers 'what is this intervention selling, to whom, through this channel?' One-minute goal + theory of change, framed for the pinned venue + audience. Same stage name as paper-pitch (the cover letter analog). Output: 0-lifecycle/2-pitch/2-pitch.md + _LOG_2-pitch.md. Markdown only. Trigger: pitch, goal, story, theory of change, what are we trying to do, /haipipe-application pitch."
argument-hint: "[intervention-path]"
allowed-tools: Bash, Read, Write, Edit, Grep, Glob, Skill
metadata:
  version: "5.4.0"
  last_updated: "2026-07-19"
  summary: "Pitch stage (stage 2, venue-ALIGNED, the FIRST stage after the venue pin) — the one-minute goal + theory of change told FOR the pinned venue + audience, and the home of the [primary] claim designation. Rewrites on retarget; the venue-FREE ladder it cites does not. History: ./CHANGELOG.md."
---

Skill: haipipe-application-pitch
==================================

Stage **2** of the intervention lifecycle, and the FIRST venue-ALIGNED stage.
It answers: what is this intervention selling, to whom, through this channel?

```text
1d-advice   what the evidence advises (the ladder's deliverable, venue-FREE)
[venue]     pins the modality in STATUS.md
2-pitch     the one-minute story, told FOR the pinned venue + audience   <- THIS STAGE
3-narrative how the claims compose into the output's arc (venue-ALIGNED)
```

Read first: `../../../PHILOSOPHY.md`, `../../haipipe-application-lifecycle/SKILL.md` (Intervention Lifecycle Contract).


## What's special: three things make the pitch the pitch

**1. First venue-ALIGNED stage — it rewrites on retarget.**
The pitch sits immediately after the venue pin; a venue re-pin REWRITES it (new framing, possibly a new primary claim) while the venue-FREE ladder it cites stays untouched.
It reads the pinned venue's Artifact Principles (`0-lifecycle/2-venue/2-venue.md`) + the audience profile, not the raw packs.
It NEEDS a pinned venue: STATUS.md with no venue → BLOCK, "run /haipipe-application venue first".

**2. It designates the [primary] claim.**
The claims ledger is venue-free and ranks nothing; the pitch names the ONE claim that carries the value proposition FOR this venue.
A result novel elsewhere but already assumed by this audience is an enabler, not the primary.
This designation lives HERE, not in the ledger, and a venue change re-runs it.

**3. One minute or it failed — it sells, it does not re-derive.**
The pitch is the one-minute story of what the intervention achieves and why it should work.
Its theory of change is a causal chain from message to behavior, each link anchored in a 1d advice entry (`A<n>`) or a supported ledger claim (`C<n>`) — no unanchored assertions.
Evidence is RECEIVED here, never produced (LAW 1): the ladder settled it upstream.


## The four phases, in pitch

```text
DRAFT   read 1d-advice.md (the entries it sells), 1c-claims.md (the evidence backstop), 0-seed.md,
        the pinned 2-venue.md Artifact Principles + the audience profile; settle the one-minute goal
        + theory of change with the user; designate the [primary] claim for THIS venue; write the pitch
PROBE   rare — a CITATION LANE only: anchor evidence for a theory-of-change link the ledger
        lacks, raised as a SECTION in 1-probes/PPNN_<topic>.md. Most pitches skip it (logged in _LOG).
REVISE  venue + audience framing pass — register, the ask, one-minute readability
CHECK   exit criteria below → Gate Ledger row
```

Pitch RECEIVES evidence, never produces it inline: a PROBE section binds through `haipipe-application-probe`, which hands the stake-stripped `q-executor:` to `Agent(haipipe-probe-q-executor-agent)` and points the section's `target:` at an answering QA file — there is no gateway skill and no per-stage `_PROBE/` folder.
Routing mechanics are the probe layer's: `../../../2-phase/1-probe/haipipe-application-probe/SKILL.md` (see its `ref/per-stage-dispatch.md`, the "2-pitch" rung).
A beat that exposes a NEW evidence gap routes back to `1c-claims`, never gathers here.


## The artifact

`0-lifecycle/2-pitch/2-pitch.md` — full skeleton in `ref/pitch-template.md`:

```text
One-sentence goal   what this intervention does, for whom, through the pinned channel; specific + testable
Theory of change    the causal chain from message to behavior; each link anchored in a 1d advice entry
                    (A<n>) or a supported ledger claim (C<n>)
Audience frame      how the pinned audience profile shapes the register and the ask
Primary claim       which ledger claim carries the value proposition — the [primary] designation lives
                    HERE, venue-aligned, NOT in the venue-free ledger
Why now             what makes this timely
Q-consumer          pitch-level evidence questions, one `## Q-Pitch-<n>` block each (Ask / Why / Answer; usually empty)
```

Sidecar: `_LOG_2-pitch.md` (phase journal + semantic-version provenance).
Formatting: `=====` title / `-----` sections; content uses no `#`, Q-consumer questions use `## Q-Pitch-<n>`; one sentence per line.


## Definition of done (read at CHECK)

```text
[ ] 0-lifecycle/2-pitch/2-pitch.md exists
[ ] one-sentence goal is specific and testable
[ ] theory of change cites 1d advice (A<n>) and/or supported ledger claims (C<n>) — no unanchored assertions
[ ] [primary] claim designated for THIS venue; audience frame matches the profile
```


## Questions this stage typically raises

DRAFT's RAISE+PLAN step raises what the draft cannot answer. These are the kinds this stage is prone to — read this list, then walk the draft against it.

```
🎯 audience fit      Has this audience responded to this kind of message before?
                     Name the comparable programme and its response rate.
📡 channel norm      What does this channel's convention allow — length, tone,
                     frequency? A pitch that violates it will not be read.
⚠️ framing risk      Which framing would read as alarming or presumptuous to this
                     audience, and what would we need to keep it?
🏁 competing message What else is this audience already receiving through this
                     channel? A message that collides gets ignored.
```

## Exits

```text
promote -> /haipipe-application narrative   (or straight to draft for simple venues — check STATUS.md stages_skipped)
```

A venue re-pin rewrites this stage; the claims ledger it cites stays unchanged.
WRITES the `2-pitch/` stage folder only.
End every reply with the closing block (stage line via `../../../haipipe-application/stage-strip.sh`).
