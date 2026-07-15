---
name: haipipe-application-advice
description: "Stage orchestrator for the intervention's 0-lifecycle/1d-advice/1d-advice.md: rung 1d of the venue-FREE evidence ladder (1a-descriptions -> 1b-themes -> 1c-claims -> 1d-advice) and the ladder's DELIVERABLE. Design advice: actionable, evidence-derived guidance entries (W-shaped), each derived from >=1 claim in the 1c ledger. Advice is counsel, not mandate: downstream venue-ALIGNED stages ADOPT or DECLINE entries per venue+audience (declined entries stay for the next round). Distinct from venue Artifact Principles (channel-how); these are content-what. Markdown only. Trigger: advice, advise, design advice, recommendations, what should the message do, principles (legacy), /haipipe-application advice."
argument-hint: "[intervention-path] [--deposit <Ann>]"
allowed-tools: Bash, Read, Write, Edit, Grep, Glob, Skill
metadata:
  version: "1.3.0"
  last_updated: "2026-07-09"
  summary: "1.3.0 (breadth round, JL adoption 2026-07-09): explore|exploit role tags (bars scope to exploit; explore = tagged bet naming its settling C + rails; graduates via iterate), full C-consumption, negative advice first-class, Rejected as reservoir, multi-round DPRC + mid-phase back-routing. 1.2.0 (bench finding, 01_sms_young_male): stage doc gains a Probes roster section (uniform across all rungs, mirroring seed; rare here, may be empty). 1.1.0 (JL ruling 2026-07-09): renamed principles -> ADVICE (folder 1d-advice, ids A<n>, maturity `advised`) -- advice is counsel downstream stages adopt or decline. 1.0.0: new rung skill from the ladder restage; W rung, derivation + actionability tests."
  # version history: ./CHANGELOG.md (skill-scoped, never loaded at invocation)
---

Skill: haipipe-application-advice
==================================

Stage orchestrator for **rung 1d** of the evidence ladder (venue-FREE) -- the ladder's **deliverable rung**. The user invokes this skill (or the `ladder` sweep); it drives the phases internally.

It answers one question:

```text
What does the evidence advise this intervention to do, and which claims ground each entry?
```

The evidence ladder (stage-1 family, all venue-FREE):

```text
1a-descriptions   what the data looks like
1b-themes         what patterns/topics emerge
1c-claims         what generalizes (the ledger)
1d-advice         what the evidence advises (the deliverable)   <- THIS RUNG
```

Paper delivers K (defended claims); application delivers W (an artifact that acts). This rung climbs the last step: it turns the ledger's claims into advice the artifact work can execute. An advice entry without a claim behind it is vibes -- the exact fabrication mode the ladder exists to prevent.

**Advice is counsel, not mandate (JL ruling 2026-07-09: "later we can use them or not use them").** This rung writes ALL the guidance the evidence supports; the venue-ALIGNED stages (pitch/design/artifact) then SELECT -- each records which `A<n>` it adopts and which it declines, with a one-line why. Declining is a design choice, not a failure; a declined entry is not deleted, it waits for the next venue or round. Adoption records live DOWNSTREAM (keeping this doc venue-FREE): claim-audit traces artifact -> adopted A -> C -> anchor, and no rule says every entry must be used.

**Not the venue's Artifact Principles.** `2-venue.md` Artifact Principles are channel-HOW (length, cadence, format for THIS modality; venue-ALIGNED, rewritten on retarget). This doc is content-WHAT (what the intervention's content should do to work; venue-FREE, survives retarget). Downstream stages read both; they never merge.

## Artifact Spec

**Files produced:**
- `0-lifecycle/1d-advice/1d-advice.md` -- the design-advice ledger
- `0-lifecycle/1d-advice/_LOG_1d-advice.md` -- phase progress journal
- `0-lifecycle/1d-advice/_PROBE/PPNN_*.md` -- probe cards (rare; + index row in `1-probe-plans/README.md`)

**Canonical template (source of truth for section order + placeholders):** `ref/advice-template.md`

**Content structure (1d-advice.md):**

```text
Advice            one **A<n>** per entry: the guidance in one sentence, role
                  (exploit | explore), derivation (>=1 C id), scope/boundary, status
Rejected          entries considered and dropped, with the refuting C id or reason
Probes            this rung's probe roster: one line per PP (question + status),
                  matching _PROBE/ on disk (rare here; may be empty)
```

- **One entry, one sub-item:** `**A1 - majority framing where compliance is high - exploit - active**` / `Use descriptive-norm framing only where cohort compliance > 50%.` / `Derivation: C1 (supported), C2 (weak - boundary caveat).` / `Scope: adult cohort; revisit if C2 settles.`
- **Role tag `exploit | explore` (JL adoption 2026-07-09, breadth round -- resolves the parked derivation-bars thread):** exploit entries rest on settled evidence and take the settlement bars below. An explore entry is a deliberate test-to-learn bet: it MAY derive from weak/GAP claims PROVIDED it (a) carries the explore tag visibly, (b) names which `C<n>` the deployed arm will settle (`Settles: C<n> via iterate`), and (c) states the compliance rails it stays inside. The A/B result flows back (iterate -> 1a backfill -> C flips) and the entry graduates to exploit or moves to Rejected -- deploy itself becomes an evidence probe. Advice may also be NEGATIVE (`avoid X`), derived from a refuted claim; negative advice is exploit-role (the refutation IS settled evidence).
- **W-actionability test:** an entry must be executable -- "could the artifact stage write the exact message move from this line?" If not, it is a claim restated, not advice; push it back to 1c.
- An entry citing only `weak` claims carries the caveat inline; whether that passes the gate is venue-scaled (see gate below).
- Ids `A<n>` are ladder-local; artifact/claim-audit trace artifact -> adopted A -> C -> anchor.

**Formatting:** `=====` title, `-----` sections, `**bold**` sub-items, one sentence per line. No `#`/`##`/`###`.

## Phase Orchestration

```
advice invoked
  |
  v
DRAFT --> re-mine the reservoir (last round's Rejected entries -- did a
          refuting C flip?); read 1c-claims.md (statuses + campaign) and
          1b-themes.md; elicit taste on guidance priorities; CONSUME every
          supported/weak claim -- an A entry, a Rejected entry, or a
          no-action line with a why; consider explore bets on promising
          weak/GAP claims; record Rejected candidates with reasons
          (internally calls haipipe-application-draft with this artifact spec)
  |
  v
PROBE --> rarely fires: derivation is in-stage work. An entry exposing a
          NEW evidence gap routes back as a 1c-claims/_PROBE/ card, never
          gathers here (internally calls haipipe-application-probe when it does)
  |
  v
REVISE -> actionability pass (every A survives the test), scope tightening,
          caveat wording (internally calls haipipe-application-revise)
  |
  v
CHECK --> the LADDER GATE lands here for light/medium venues (batched per
          wiki/08-stage-gate.md): every exploit A derived from >=1 C at/above
          the venue's settlement bar? every explore A tagged + settling C
          named + rails stated? actionability passed? no unresolved STALE
          tags? user confirms -> Gate Ledger row(s) -> advance to venue/pitch
          (internally calls haipipe-application-check)
```

Phase visibility: announce every phase boundary (reply line + `[PHASE]` entry in `_LOG`); skip a phase only by an explicit logged verdict; CHECK is never implicit.

Rounds + routing (breadth contract, wiki/08-stage-gate.md): REVISE ends with a self-assessment -- did this round surface new entries, consumption gaps, or evidence needs? If yes, run another DRAFT->PROBE->REVISE lap (`[ROUND n]` in `_LOG`); CHECK fires only when a round comes up dry (venue-scaled: full loops-until-dry). Mid-phase back-routing is legal: an entry exposing a new evidence gap files the 1c probe card immediately and logs `[ROUTE -> claims]` -- never wait for a gate to report a discovery.

## Settlement coupling (venue-scaled, read at CHECK)

The venue's `claims_settlement` bar applies through the derivation chain to EXPLOIT entries. Explore entries are exempt from the bar BY CONTRACT, not by leniency: tag visible + settling C named + rails stated, or the entry fails CHECK regardless of venue.

```
light    an exploit A may cite weak claims with inline caveat; GAP-derived exploit forbidden
medium   load-bearing exploit A cite supported-or-weak-with-caveat; others may caveat
full     every exploit A cites supported claims (judged verdicts) only
```

## Done-criteria

- [ ] Every `**A<n>**` has a guidance sentence, role (exploit | explore), derivation (>=1 resolving C id), scope, status
- [ ] Every A passes the W-actionability test
- [ ] Exploit derivations meet the venue's settlement bar (or the provisional `light` bar if unpinned); every explore entry names its settling C and its rails
- [ ] Every supported/weak C is consumed: cited by an A, refuted into Rejected, or a no-action line with a why
- [ ] Rejected section lists dropped entries with reasons (may be empty)
- [ ] Probes section lists every `_PROBE/` card with its current status (roster matches disk; may be empty)
- [ ] No unresolved `[STALE ...]` tags in this doc

## Principles

1. Derivation is mandatory: no A without a C. The ladder's whole point.
2. Actionable or it is not advice -- push claim-restatements back to 1c.
3. Advice is counsel, not mandate: adoption/decline happens downstream (venue-ALIGNED), recorded with a why; this doc never tracks per-venue adoption.
4. Venue-FREE: what the content should do survives retarget; only HOW it renders (venue Artifact Principles) rewrites.
5. Negative wisdom is first-class: a Rejected entry with a refuting claim saves the next round from re-deriving it.
6. Deposit to the insight KB is ON-REQUEST only (`--deposit <Ann>` files a W card via the insight door); the ladder doc is the primary record (ladder restage R7).
7. Explore is a strategy, not a loophole: the visible tag, the named settling C, and the rails are what separate a bet from vibes.

## Handoff

On CHECK confirm (this is usually the ladder gate): `promote -> /haipipe-application venue` (pin modality), or `-> /haipipe-application pitch` if venue already pinned. End the reply with the closing block (stage line via `../../../haipipe-application/stage-strip.sh`).
