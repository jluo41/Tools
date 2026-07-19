---
name: haipipe-application-advice
description: "Stage orchestrator for the intervention's 0-lifecycle/1d-advice/1d-advice.md: rung 1d of the venue-FREE evidence ladder (1a-descriptions -> 1b-themes -> 1c-claims -> 1d-advice) and the ladder's DELIVERABLE. Design advice: actionable, evidence-derived guidance entries (W-shaped), each derived from >=1 claim in the 1c ledger. Advice is counsel, not mandate: downstream venue-ALIGNED stages ADOPT or DECLINE entries per venue+audience (declined entries stay for the next round). Distinct from venue Artifact Principles (channel-how); these are content-what. Markdown only. Trigger: advice, advise, design advice, recommendations, what should the message do, principles (legacy), /haipipe-application advice."
argument-hint: "[intervention-path] [--deposit <Ann>]"
allowed-tools: Bash, Read, Write, Edit, Grep, Glob, Skill
metadata:
  version: "1.8.0"
  last_updated: "2026-07-18"
  summary: "Advice stage (rung 1d of the venue-FREE 1a–1d evidence ladder; the W rung and the ladder's DELIVERABLE) — design advice, one A<n> per entry (exploit|explore role) derived from >=1 claim in the 1c ledger; counsel not mandate (venue-ALIGNED stages adopt or decline downstream); content-WHAT, distinct from the venue's channel-HOW Artifact Principles. History: ./CHANGELOG.md."
---

Skill: haipipe-application-advice
==================================

Rung **1d** of the venue-FREE evidence ladder, and the ladder's **deliverable rung**.
It answers: what does the evidence advise this intervention to do, and which claims ground each entry?

```text
1a-descriptions   what the data looks like
1b-themes         what patterns/topics emerge
1c-claims         what generalizes (the ledger)
1d-advice         what the evidence advises (the deliverable)   <- THIS RUNG
```

Read first: `../../../PHILOSOPHY.md`, `../../../haipipe-application/SKILL.md` (Stage Gate Protocol).


## What's special: advice is the ladder's deliverable

**1. It delivers W, and every entry is derived from a claim.**
Paper stops at K (defended claims); the application climbs one rung further to W — advice the artifact work can execute.
Derivation is mandatory: an advice entry without a claim behind it is vibes, the exact fabrication the ladder exists to prevent.
Every entry must pass the W-actionability test — "could the artifact stage write the exact message move from this line?" — or it is a claim restated, and pushes back to 1c.

**2. Advice is counsel, not mandate.**
This rung writes ALL the guidance the evidence supports; the venue-ALIGNED stages (pitch/narrative/display/artifact) then SELECT, each recording which `A<n>` it adopts or declines with a one-line why.
Declining is a design choice, not a failure — a declined entry waits for the next venue or round.
Adoption records live DOWNSTREAM, keeping this doc venue-FREE; claim-audit traces artifact -> adopted A -> C -> anchor, and no rule says every entry must be used.

**3. Content-WHAT, not the venue's channel-HOW.**
`2-venue.md` Artifact Principles are channel-HOW (length, cadence, format for THIS modality; venue-ALIGNED, rewritten on retarget).
This doc is content-WHAT (what the content should do to work; venue-FREE, survives retarget).
Downstream stages read both; they never merge.

**4. Every entry carries an exploit|explore role.**
Exploit entries rest on settled evidence and take the settlement bars below; negative advice ("avoid X", derived from a refuted claim) is exploit-role — the refutation IS settled evidence.
An explore entry is a deliberate test-to-learn bet: it MAY derive from weak/GAP claims provided it (a) carries the explore tag visibly, (b) names the `C<n>` its deployed arm will settle (`Settles: C<n> via iterate`), and (c) states its compliance rails — miss the contract and it fails CHECK regardless of venue.
The A/B result flows back (iterate -> 1a backfill -> C flips) and the entry graduates to exploit or moves to Rejected; deploy itself becomes an evidence probe.
Explore is a strategy, not a loophole: the visible tag, the named settling C, and the rails are what separate a bet from vibes.


## The four phases, in advice

```text
DRAFT   re-mine last round's Rejected reservoir (did a refuting C flip?), read 1c-claims.md (statuses +
        campaign) and 1b-themes.md, elicit taste on guidance priorities; CONSUME every supported/weak C —
        an A entry, a Rejected entry, or a No-action line with a why; consider explore bets on promising weak/GAP
PROBE   rarely fires: derivation is in-stage work. An entry exposing a NEW evidence gap routes BACK to 1c-claims
        (raised there as a question SECTION in 1-probes/), never gathers here. Mechanics:
        ../../../2-phase/1-probe/haipipe-application-probe/SKILL.md
REVISE  actionability pass (every A survives the test), scope tightening, caveat wording
CHECK   the LADDER GATE for light/medium venues (batched per the Stage Gate Protocol): every exploit A meets the venue's
        settlement bar, every explore A is tagged + names its settling C + states rails, actionability passed,
        every supported/weak C consumed, no unresolved STALE tags; user confirms -> Gate Ledger row(s) -> advance
```

Advice RARELY probes: a new evidence gap is not gathered here but routed back to 1c-claims, whose PROBE phase binds it.
Each phase runs its worker (`haipipe-application-draft` / `-probe` / `-revise` / `-check`); announce every phase boundary and never let CHECK go implicit.
Rounds + back-routing (loop-until-dry for medium+ venues, `[ROUND n]` / `[ROUTE -> claims]` in `_LOG`) follow `../../../haipipe-application/SKILL.md` (Stage Gate Protocol).
The ladder doc (`1d-advice.md`) is the record; adopted/declined A-ids with a why live there.


## The artifact

`0-lifecycle/1d-advice/1d-advice.md` — full skeleton in `ref/advice-template.md`:

```text
Advice      one A<n>: guidance in one sentence + role (exploit|explore) + derivation (>=1 C id) + scope/boundary
            + status; close with a No-action line (every supported/weak C consumed by no entry, each with a why)
Rejected    entries considered and dropped, one sub-item each with the refuting C id or reason (the reservoir; may be empty)
Q-consumer  the questions this rung raises, one `## Q-Advice-<n>` block each (Ask / Why / Answer; rare — derivation is in-stage work; may be empty);
            APPROVE adds each -> 1-probes/ pointer + state
```

One entry, one sub-item: `**A1 - majority framing where compliance is high - exploit - active**` / `Use descriptive-norm framing only where cohort compliance > 50%.` / `Derivation: C1 (supported), C2 (weak - boundary caveat).` / `Scope: adult cohort; revisit if C2 settles.`
An entry citing only weak claims carries the caveat inline; whether that passes the gate is venue-scaled (below).
Sidecar: `_LOG_1d-advice.md` (phase journal).
Ids `A<n>` are ladder-local; artifact and claim-audit trace artifact -> adopted A -> C -> anchor.
Formatting: `=====` title, `-----` sections, `**bold**` sub-items, one sentence per line; content sections use no `#`, Q-consumer questions use `## Q-Advice-<n>`.


## Settlement coupling (venue-scaled, read at CHECK)

The venue's `claims_settlement` bar (`STATUS.md`) applies through the derivation chain to EXPLOIT entries.
Explore entries are exempt from the bar BY CONTRACT, not by leniency: tag visible + settling C named + rails stated, or the entry fails CHECK regardless of venue.

```text
light    an exploit A may cite weak claims with an inline caveat; GAP-derived exploit forbidden
medium   load-bearing exploit A cite supported-or-weak-with-caveat; others may caveat
full     every exploit A cites supported (judged) claims only
```

Absent `claims_settlement` (venue unpinned) → apply `light` provisionally.


## Exits

```text
promote -> /haipipe-application venue    pin the modality (or -> pitch if venue already pinned)
```

This CHECK is usually the ladder gate; end every reply with the closing block (stage line via `../../../haipipe-application/stage-strip.sh`).
