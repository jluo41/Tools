---
name: haipipe-application-themes
description: "Stage orchestrator for the intervention's 0-lifecycle/1b-themes/1b-themes.md: rung 1b of the venue-FREE evidence ladder (1a-descriptions -> 1b-themes -> 1c-claims -> 1d-advice). Thematic extraction: which patterns/topics emerge from the described data and the outside literature. Every theme cites at least one D id or discovery source. Discovery-probe lane. Markdown only. Trigger: themes, theme, topic space, what patterns emerge, thematic, /haipipe-application themes."
argument-hint: "[intervention-path]"
allowed-tools: Bash, Read, Write, Edit, Grep, Glob, Skill
metadata:
  version: "2.0.0"
  last_updated: "2026-07-15"
  summary: "Themes stage (rung 1b of the venue-FREE 1a–1d evidence ladder; the I rung) — grounded pattern-clusters extracted from 1a D ids + discovery sources, each theme carrying candidate-claim hooks that rung 1c consumes; ungrounded patterns go to Parked. Full D-consumption + counter-hunt; light discovery PROBE via 1-probes/. History: ./CHANGELOG.md."
---

Skill: haipipe-application-themes
==================================

Rung **1b** of the venue-FREE evidence ladder — the exploration frame between described data and committed claims.
It answers: which patterns/topics emerge from the described data and the field, grounded, and worth committing claims on?

```text
1a-descriptions   what the data looks like
1b-themes         what patterns/topics emerge      <- THIS RUNG
1c-claims         what generalizes (the ledger)
1d-advice         what the evidence advises (the deliverable)
```

Read first: `../../../PHILOSOPHY.md`, `../../../wiki/03-intervention-lifecycle.md`.


## What's special: three things make themes themes

**1. Themes are extracted, not invented — grounding first, naming second.**
Every **T<n>** cites >=1 `D<n>` id from 1a or a project-side discovery source.
An ungrounded pattern is a hunch: it goes to Parked, never listed as a theme.
Ids `T<n>` are ladder-local; rung 1c cites them as `C1 (T1)`.

**2. A theme is a question-space, not a claim.**
Direction and candidate-claim hooks live here; a claim's status lives only in 1c (`supported | weak | GAP`).
The theme hooks are exactly what rung 1c consumes — the exploration frame that spawns claims.
Venue-FREE: the pattern space does not change with the channel.

**3. Full D-consumption + a counter-hunt.**
Every 1a `D<n>` id is cited by >=1 theme or listed in Parked as context-only (with a why) — nothing described is silently dropped.
DRAFT sweeps three lenses — data patterns (from D entries), field patterns (discovery), counter-hunt (patterns AGAINST the seed hypothesis).
A null counter-hunt is recorded in Parked, not omitted.


## The four phases, in themes

```text
DRAFT   re-mine last round's Parked reservoir (did new D entries ground any?); read 1a-descriptions.md
        (the grounding floor); elicit taste on which directions matter; sweep the three lenses — data /
        field (discovery: "what messaging levers does the mhealth literature name?") / counter-hunt —
        drafting T slots with grounding + hooks
PROBE   mode LIGHT — the five-step loop raises field-pattern questions as SECTIONS in 1-probes/ and COLLECTS
        (→ discovery; task only for a quick in-data confirmation); each section's a-consumer lands grounding
        refs onto its T entry. Routing mechanics are the probe layer's:
        ../../../2-phase/1-probe/haipipe-application-probe/SKILL.md
REVISE  sharpen pattern sentences, merge overlapping themes, park the ungrounded
CHECK   every theme grounded (>=1 resolving D id or source) + carries a hook (or a context-only note);
        every 1a D id consumed; counter-hunt ran; Parked honest; no STALE tags; roster matches 1-probes/
```

Themes RECEIVES grounding, never PRODUCES it inline (LAW 1): it raises questions; `haipipe-application-probe` binds them.
When a theme's grounding refreshes (a `[STALE ...]` tag from 1a), re-confirm or revise the theme before CHECK.
A theme needing a number files the 1a D slot immediately and logs `[ROUTE -> descriptions]` — never wait for a gate to report it.
Rounds + back-routing (loop-until-dry for medium+ venues; `[ROUND n]` / `[ROUTE -> descriptions]` in `_LOG`) follow `../../../wiki/08-stage-gate.md`.
CHECK may be BATCHED into the ladder gate per the venue; announce every phase boundary in `_LOG`; CHECK is never implicit.


## The artifact

`0-lifecycle/1b-themes/1b-themes.md` — full skeleton in `ref/themes-template.md`:

```text
Themes   one **T<n>**: name, the pattern in one sentence, grounding (D ids and/or discovery sources),
         candidate-claim hooks (or an explicit "context-only" note)
Parked   patterns noticed but not pursued (one line + why); context-only D ids; the counter-hunt record;
         the reservoir the next DRAFT re-mines
Probes   this rung's roster: one line per PP (question + status), matching 1-probes/ on disk
```

Sidecar: `_LOG_1b-themes.md` (phase journal).
Formatting: `=====` title, `-----` sections, `**bold**` sub-items, one sentence per line; no `#`/`##`/`###`.
The Insight KB is optional context here, never a required source.


## Exits

```text
promote -> /haipipe-application claims   (rung 1c consumes the theme hooks)
```

End every reply with the closing block (stage line via `../../../haipipe-application/stage-strip.sh`).
