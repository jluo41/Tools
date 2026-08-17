---
name: haipipe-application-section-edit
description: "Stage 5 of the intervention lifecycle (venue-gated: sectioned venues only — report, dashboard spec; skipped for sms/push/reminder/checklist/email unless the venue profile says otherwise). Per-section DRAFT-EVIDENCE-REVISE-CHECK on the sections the VENUE PROFILE declares, syncing prose to 0-sections/. Renamed from haipipe-application-section-editing; the hardcoded 6-section report list moved to venue/venue-report (venue knowledge, not skill logic). Trigger: section-edit, section, §N, edit sections, refine sections, /haipipe-application section-edit."
argument-hint: "[section-name-or-§N] [intervention-path]"
allowed-tools: Bash, Read, Write, Edit, Grep, Glob, Skill
metadata:
  version: "0.5.4"
  last_updated: "2026-07-19"
  summary: "Section-edit stage (stage 5, venue-ALIGNED; sectioned venues only — report/dashboard spec): each section the VENUE PROFILE declares runs DRAFT → EVIDENCE → REVISE → CHECK, editing prose in 0-sections/ with per-section scaffolds under 0-lifecycle/5-section-edit/{section}/. Its EVIDENCE is a full-document probe — values + citation lanes per section, display lane where a section references units — raising gaps as entries in the flat pool 1-probes/PPNN_<topic>/. Keeps the comment→reply→apply convention and the six edit topics as REVISE/CHECK lenses. History: ./CHANGELOG.md."
---

Skill: haipipe-application-section-edit
========================================

The **section-edit** stage (stage 5, venue-ALIGNED) turns each section into venue-quality prose, one section at a time — for **sectioned venues only** (report, dashboard spec).
It answers: does each section's prose do its assigned job?
Each section runs its own DRAFT → EVIDENCE → REVISE → CHECK, with the edited prose living in `0-sections/`.

Read first: `../../../PHILOSOPHY.md`, `../../../haipipe-application/SKILL.md` (Stage Gate Protocol + Delivery Need Routing sections).


## What's special

**1. The section list comes from the VENUE PROFILE, never this skill.**
`venue/venue-<name>/README.md` declares the section structure (e.g. `venue-report` carries the report section list); a venue with no `sections:` block skips this stage entirely (check `STATUS.md | stages_skipped |`, and BLOCK if skipped).
The display stage's per-unit jobs say what each section must carry; this stage makes the prose deliver it.

**2. Venue-ALIGNED, so it rewrites on retarget.**
The pinned venue sets the style-profile and length limits each section conforms to; a new venue re-sections and re-writes, while the evidence ladder (1a–1d) underneath stays put.

**3. Its EVIDENCE is a full-document probe.**
values + citation lanes fire per section, and a display lane fires where the section references units.
The per-lane wording is the probe layer's — see `../../../2-phase/1-evidence/haipipe-application-evidence/ref/per-stage-dispatch.md`, "Section-edit worker logic".


## The four phases, in section-edit

```text
DRAFT   settle the section's outline + draft sentences against its assigned job, and end the outline with
        the evidence gaps it raises (haipipe-application-draft).  ⛔ STOP for the user's structure review.
EVIDENCE   trace numbers to task results and claims to the 1c ledger / K-W anchors; raise each real gap as a
        SECTION in the flat pool 1-probes/PPNN_<topic>/ (values + citation lanes per section, display lane
        where units are referenced), MATCH the bank, dispatch only what MATCH cannot close
        (haipipe-application-evidence; routing is the probe layer's).
REVISE  the comment → reply → apply cycle (below) + venue style-profile + audience conformance
        (haipipe-application-revise).
CHECK   ⛔ per-section exit: prose does its job, no open comments, flags resolved or parked
        (haipipe-application-check); section rows land in the stage _LOG, the stage Gate Ledger row is
        written when ALL sections pass.
```

Users invoke this stage; it dispatches the `2-phase/` workers.
Only DRAFT and CHECK involve the human; EVIDENCE and REVISE are agent-only.


## The comment → reply → apply cycle (REVISE convention)

```text
1. Annotate     insert `%% {CC-<topic>-v<DATE>}: <finding>` comments inline, one per finding
2. Human reply  `========> {JL v<DATE>}: accept | reject | revise <instructions>`
3. Apply        apply accepted comments, remove resolved comment blocks
4. Clean+diff   strip leftover scaffolding, write a diff summary to the _LOG
```

Six edit topics are the lenses REVISE writes against and CHECK verifies:
**tone** (voice matches the audience register — clinician / pharmacist / patient) · **length** (respects the venue profile's limits) ·
**citations** (claims trace to the 1c ledger anchors; flag unsupported assertions) ·
**reading-level** (patient-facing content at the audience's target grade) · **distinctiveness** (parallel elements — message variants, panels — actually differ) ·
**consistency** (terms, labels, metric names, cohort definitions agree across sections).


## The artifact

Per section, a folder `0-lifecycle/5-section-edit/{section}/`:

```text
{section}.md         the section outline + its assigned job — the per-section scaffold
_LOG_{section}.md    phase journal, one [PHASE]-tagged entry per round (newest on top)
```

There is no single stage template — each section's scaffold IS its outline, and the display stage's per-unit job spec is the map of what each section must carry.
Evidence gaps do NOT buffer here: they are raised as ENTRIES in the flat probe pool `1-probes/PPNN_<topic>/` (one file per TOPIC; each ENTRY is one `## QX<n>` q-executor carrying `### q-executor` / `### q-consumer` / `### bank binding` / `### a-executor`), states `planned | commissioned | answered | read | answered-local | failed`; the stake stays in the stage doc's Q-consumer.

Inputs read: `STATUS.md` (venue, stages_skipped) · `venue/venue-<name>/README.md` (section list + jobs) · `0-lifecycle/4-display/4-display.md` (element→section map) · `0-lifecycle/1c-claims/1c-claims.md` (the ledger; claims language must not outrun it) · `0-lifecycle/1d-advice/1d-advice.md` (the advice entries each section executes) · `0-sections/*` (the prose under edit).
Output: edited `0-sections/*` in place, plus the per-section scaffolds above; this stage does not modify upstream lifecycle docs — upstream problems become loopback suggestions.


## Questions this stage typically raises

DRAFT's RAISE+PLAN step raises what the draft cannot answer. These are the kinds this stage is prone to — read this list, then walk the draft against it.

```
🔢 owed number       A number in the prose with no named source. Worth going to get,
                     or cut the sentence?
⚓ owed source       An assertion about the world with nothing behind it.
🧩 unearned move     This paragraph makes a step the reader has not been given
                     grounds for. No sweep finds this — it is a missing argument,
                     not a missing token.
📛 norm conflict     The venue profile and the section's own convention disagree
                     here. Which wins, and on what evidence?
```

## Exits

```text
[ ] every venue-declared section has prose that does its job (per display's mapping)
[ ] no open (unreplied) comments in any section
[ ] format check passes (renders/compiles where applicable, labels resolve)
[ ] section rows logged; stage Gate Ledger row written on CHECK approve
promote -> /haipipe-application draft   compose the artifact from the settled sections
```

End every reply with the closing block (stage line via `../../../haipipe-application/stage-strip.sh`).
