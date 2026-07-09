---
name: haipipe-application-themes
description: "Stage orchestrator for the intervention's 0-lifecycle/1b-themes/1b-themes.md: rung 1b of the venue-FREE evidence ladder (1a-descriptions -> 1b-themes -> 1c-claims -> 1d-principles). Thematic extraction: which patterns/topics emerge from the described data and the outside literature. Every theme cites at least one D id or discovery source. Discovery-probe lane. Markdown only. Trigger: themes, theme, topic space, what patterns emerge, thematic, /haipipe-application themes."
argument-hint: "[intervention-path]"
allowed-tools: Bash, Read, Write, Edit, Grep, Glob, Skill
metadata:
  version: "1.0.0"
  last_updated: "2026-07-09"
  summary: "New rung skill from the ladder restage (SOP-ladder-restage.md): 1b = the I rung: themes extracted from 1a descriptions + discovery probes, each grounded by D ids or sources; the exploration frame that spawns 1c claims."
  # version history: ./CHANGELOG.md (skill-scoped, never loaded at invocation)
---

Skill: haipipe-application-themes
==================================

Stage orchestrator for **rung 1b** of the evidence ladder (venue-FREE). The user invokes this skill (or the `ladder` sweep); it drives the phases internally.

It answers one question:

```text
Which patterns and topics emerge from the described data and the field, worth committing claims on?
```

The evidence ladder (stage-1 family, all venue-FREE):

```text
1a-descriptions   what the data looks like
1b-themes         what patterns/topics emerge     <- THIS RUNG
1c-claims         what generalizes (the ledger)
1d-principles     what to do (the deliverable)
```

Themes are the exploration frame in the thematic-analysis sense: pattern-clusters extracted from described data and literature, not free-floating brainstorm topics. A theme with no grounding is a hunch -- it goes back to seed, not here.

## Artifact Spec

**Files produced:**
- `0-lifecycle/1b-themes/1b-themes.md` -- grounded themes
- `0-lifecycle/1b-themes/_LOG_1b-themes.md` -- phase progress journal
- `0-lifecycle/1b-themes/_PROBE/PPNN_*.md` -- probe cards (+ index row in `1-probe-plans/README.md`)

**Canonical template (source of truth for section order + placeholders):** `ref/themes-template.md`

**Content structure (1b-themes.md):**

```text
Themes            one **T<n>** per theme: name, the pattern in one sentence,
                  grounding (D ids and/or discovery sources), candidate-claim hooks
Parked            patterns noticed but not pursued, with a one-line why
```

- **One theme, one sub-item:** `**T1 - social influence**` / pattern sentence / `Grounding: D3, D7; discoveries/2026-07-01_sms-norms/sources.md S02.` / `Hooks: norm framing may lift response (-> claim candidate).`
- Every theme cites >=1 `D<n>` id from 1a or a project-side discovery source. Ungrounded themes are Parked, not listed.
- Ids `T<n>` are ladder-local; 1c claims cite them as `C1 (T1)`.

**Formatting:** `=====` title, `-----` sections, `**bold**` sub-items, one sentence per line. No `#`/`##`/`###`.

## Phase Orchestration

```
themes invoked
  |
  v
DRAFT --> read 1a-descriptions.md (the grounding floor); elicit taste on
          which theme directions matter for this intervention; draft T slots
          with grounding hooks; buffer discovery-probe plans for field
          patterns the data alone cannot show ("what messaging levers does
          the mhealth literature name?")
          (internally calls haipipe-application-draft with this artifact spec)
  |
  v
PROBE --> dispatch via haipipe-application-probe (mode light; discovery
          probes for field patterns, task probes only when a pattern needs a
          quick in-data confirmation); TRANSLATE lands grounding refs
  |
  v
REVISE -> sharpen pattern sentences, merge overlapping themes, park the
          ungrounded (internally calls haipipe-application-revise)
  |
  v
CHECK --> exit gate (may be BATCHED into the ladder gate per the venue,
          wiki/08-stage-gate.md): every theme grounded? parked list honest?
          no unresolved STALE tags? (internally calls haipipe-application-check)
```

Phase visibility: announce every phase boundary (reply line + `[PHASE]` entry in `_LOG`); skip a phase only by an explicit logged verdict; CHECK is never implicit.

## Done-criteria

- [ ] Every `**T<n>**` theme cites >=1 resolving `D<n>` id or project-side source
- [ ] Every theme carries at least one candidate-claim hook (or an explicit "context-only" note)
- [ ] Parked section lists dropped patterns with a why (may be empty)
- [ ] No unresolved `[STALE ...]` tags in this doc
- [ ] Every probe card read/verdicted with resolving refs (checker-verified)

## Principles

1. Themes are extracted, not invented: grounding first, naming second.
2. A theme is a question-space, not a claim -- direction and hooks live here, statuses live in 1c.
3. Venue-FREE: the pattern space does not change with the channel.
4. When a theme's grounding entry refreshes (STALE tag from 1a), re-confirm or revise the theme before CHECK.
5. Insight KB is optional context, not a required source (ladder restage R7).

## Handoff

On CHECK confirm (or ladder-gate batch): `promote -> /haipipe-application claims`. End the reply with the closing block (stage line via `../../../haipipe-application/stage-strip.sh`).
