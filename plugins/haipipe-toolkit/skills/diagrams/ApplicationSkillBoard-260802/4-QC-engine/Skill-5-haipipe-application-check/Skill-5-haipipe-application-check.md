# haipipe-application-check · v0.4.3
state: 🔴 OPEN
owner: JL
method: three managed spans sync from the skill folder; everything else is written by hand

## Opening
haipipe-application-check is a shipped unit: what does it still owe, and is it healthy?

Write here what this unit is for in one paragraph a stranger could follow, why it exists on its own rather than as part of its neighbour, and what would have to be true for it to be considered finished.
The generated sections answer what it IS; only this one can answer whether it is any good.
`Opening` is the lead section's ONE name on every page kind (JL 260731: "just one single Opening"); `Question` survives only as a legacy alias for pages written before the rename.

## Writing Style
English only. One sentence per source line. Describe the shipped unit factually and keep generated inventory separate from human health judgment.

## Diagram
<!-- haipipe:skill:tree:start 60d19b76ffbf1d2c application/2-phase/3-check/haipipe-application-check -->

**What `haipipe-application-check` ships**: every file in the folder, with the one-line purpose each one states for itself.

```
haipipe-application-check/
  attendance-modes.md   122 ln  Attendance Modes — Who Clicks "Accept" at Each CHECK
  CHANGELOG.md           44 ln  haipipe-application-check — Changelog
  checks.sh             160 ln
  gate-persona.md       112 ln  Gate Persona — Reviewer Voice for SOFT Gates
  SKILL.md              167 ln  Skill: haipipe-application-check (CHECK phase worker)
```

<!-- haipipe:skill:tree:end -->

```
WORKFLOW  (authored: a folder can be read off disk, an intent cannot)
Draw how this skill is actually used: the entry point, what it reads,
what it writes, and where it hands off. Delete this fence if the tree
above is the whole story.
```

## Content
<!-- haipipe:skill:body:start 60d19b76ffbf1d2c application/2-phase/3-check/haipipe-application-check -->

**haipipe-application-check** · `0.4.3` · last shipped 2026-08-04

- folder   `application/2-phase/3-check/haipipe-application-check/`
- tools    Bash, Read, Write, Edit, Grep, Glob, Skill
- summary  Application-specific CHECK worker layered on haipipe-page-check; runs local checkers, seeds findings, and applies the application's declared human gate.

### SKILL.md



Skill: haipipe-application-check (CHECK phase worker)
======================================================

CHECK phase worker -- the 🧑 phase. Reviews the artifacts produced during one lifecycle stage's DRAFT-PROBE-REVISE and proposes the next move:

**LOAD THE PAGE LAYERS FIRST:** `../../../../board/page-types/haipipe-page-for-stage/SKILL.md`, then `../../../../board/page-workflows/haipipe-page-check/SKILL.md`.
The generic contract owns judgment and phase routing.
This file adds the application's deterministic checks, comment surface, and Gate Ledger.

```
approve   → Gate Ledger row + advance current_layer to the next non-skipped stage
grow      → GROW-loop rungs (1a-1d) only (JL 2026-07-09: "after the check, they
            can think about adding more probes in the draft"): the gate ASKS
            "which data topics / probes are still missing?" -- the user's
            questions are the strongest lens; grow converts them to new slots
            + planned probe skeletons and re-opens DRAFT as [ROUND n+1].
            Approve at these rungs means: saturated AND the user added nothing.
revise    → loop back with feedback (same stage; the restarted phase reads the
            stage-doc > CHECK: threads + > USER: replies; upstream problems are
            named as loopback suggestions, the user decides)
done      → early exit: jump to draft (artifact) with remaining stages waived
            (recorded in the ledger notes)
```

A stage is only "done" when this approval is EXPLICIT. The system never auto-advances. Full protocol: `../../../haipipe-application/SKILL.md` (Stage Gate Protocol section).

Before any of that, CHECK opens with a MECHANICAL Run step (next section): a ❌ from `./checks.sh` or a FAIL from the probe-file checker means the gate CANNOT go green -- at any venue depth, under any persona.

Mechanical checks (step 1 -- Run)
==================================

Two checkers open every CHECK, before the judgment ask. They fire at EVERY venue depth -- venue scaling governs how the report is presented (inline vs full), never whether the checkers run.

1. Deterministic markdown checks -- `./checks.sh <artifact-or-dir> [--md <working-doc>] ...` (this folder; `--md` repeatable, `--depth N` widens the dir scan). Em-dash (❌, house rule), AI-voice tells (⚠️), TODO/FIXME (❌), bibtex-in-markdown (❌). Paste its ✅/⚠️/❌ lines into the CHECK report verbatim; exit 0 = no ❌. Paper's tex checks (`\cite`/`\ref`/`\label`, Pn.Sn, `--compile`) are deliberately absent -- application artifacts are markdown.

2. Probe-file invariants -- `sh "$CHK" <intervention_root>` (resolve `$CHK` per *Locating the probe-file checker* below). Any FAIL line (a `state: planned` section, a dangling ref, a `harvest: OWED` lane, dead vocabulary) means the gate CANNOT go green: a planned section surviving to CHECK is a probe that never ran.

A mechanical ❌/FAIL is not a judgment call: no persona preset, no `--unattended` timeout, and no venue-profile override can approve over it. Fix (revise), re-run, then proceed to the judgment ask.

Locating the probe-file checker
================================

Installed skills flatten the tree, so the hard-coded relative path (`../../1-probe/...`) is NOT reliable, and TWO files named `check-probe-cards.sh` exist on disk (paper's under `haipipe-paper-probe/`, application's under `haipipe-application-evidence/`). Glob for it, FILTER on the path so it cannot resolve to the paper family, and FAIL LOUDLY when nothing matches:

```sh
CHK=$(find -L ~/.claude/skills ./.claude/skills "${CLAUDE_PLUGIN_ROOT:-/nonexistent}" -maxdepth 4  \
        -path "*haipipe-application-evidence*" -name check-probe-cards.sh 2>/dev/null | head -1)
[ -n "$CHK" ] || { echo "FAIL: application probe-file checker not found"; exit 1; }

sh "$CHK" <intervention_root>    # whole-pool section pass
```

A missing checker is a FAIL, never a silent skip: a gate that cannot run its checker has not checked anything.


`> CHECK:` comment seeding (stage docs ONLY)
=============================================

Every flagged item that lives in a 0-lifecycle stage doc (0-seed.md, 1a-descriptions.md, 1c-claims.md, ...) is planted as ONE `> CHECK:` comment at its exact spot -- one line stating the issue + the judgment needed, with concrete values, never an abstract description. The chat report is the map; the in-file threads are what the human walks.

0-artifacts/*.md are NEVER annotated: the artifact IS the deliverable text (unlike paper's .tex, where % comments never render), so a seeded comment would ship. Artifact-level findings go into the Gate Ledger notes column instead, quoted with file:line so they stay actionable (R2c RULED, JL 2026-07-07).

The human replies `> USER:` under each thread. On revise, the restarted phase (DRAFT/EVIDENCE/REVISE) reads the stage-doc `> CHECK:` threads + their `> USER:` replies and responds to each -- an unanswered `> CHECK:` comment is surfaced back, never silently dropped. Resolved threads archive to the stage `_LOG`.

Gate Ledger (STATUS.md)
========================

On approve, append/update the row and bump `current_layer`:

```
## Gate Ledger

| Stage | Confirmed | Date | By | Notes |
|-------|-----------|------|----|-------|
| seed | yes | 2026-07-06 | JL | kill criteria set |
| claims | yes | 2026-07-06 | JL | settlement: light met |
| draft | yes | 2026-07-07 | JL | artifact: em-dash sms.md:4 fixed pre-approve |
```

`By` records who approved: the human (copilot mode) or `persona:<preset>` (unattended mode). The stage strip's ✅ means "confirmed in this ledger", NOT "artifact exists on disk". The Notes column is also where artifact-level checker findings land (0-artifacts/*.md are never annotated in-file -- see comment seeding above).

Venue-scaled depth (when CHECK fires)
======================================

```
simple (sms, push, reminder)      INLINE — present the exit criteria as one short
                                  checklist in the reply; user's "ok" = approve.
medium (checklist, email)         INLINE by default; full report on request (--report).
complex (dashboard, ui-card,      FULL — render the complete CHECK report (criteria
report)                           + evidence spot-checks + flags) before the ask.
```

The venue profile's README can override with `gate: inline | report`. Depth scales the REPORT, not the mechanics: `./checks.sh` + the probe-file checker run even for inline/simple venues (an sms message text still gets the em-dash/AI-voice/TODO scan).

Per-stage exit criteria
========================

```
seed:          kill criteria present? audience hunch specific? >=1 evidence path named?
descriptions:  every **D<n>** entry anchored (statistic + resolving pointer + as-of
               date)? no raw data / inline computation? no unconsumed
               [FORWARD -> CLAIMS] pointer in seed's _LOG?
themes:        every **T<n>** grounded (>=1 D id or project-side source)? hooks or
               context-only note per theme? Parked honest? no unresolved [STALE] tags?
claims:        every claim a **C<n>** line with theme tag + role + status + → PP ref?
               theme tags resolve to 1b? every probe a **PP<nn>** plan? Evidence
               Campaign complete (dispatch order + deps, no load-bearing GAP without a
               row)? settlement bar met against the campaign for the pinned depth
               (light/medium/full — claims skill §Settlement Gate)? no [STALE] tags?
advice:        every **A<n>** derived from >=1 resolving C id at/above the settlement
               bar? W-actionability passed? Rejected section honest? no [STALE] tags?
               (the LADDER GATE lands here for light/medium venues — batching per
               Stage Gate Protocol; one approval writes the batched rungs' ledger rows)
pitch:         one-sentence goal testable? mechanism (theory of change) plausible?
               venue + audience named?
narrative:     arc follows venue rules? all load-bearing claims mapped to beats?
display:       every primary claim has a content element? every element has a job +
               evidence anchor? materialization routed (task refs) where needed?
section-edit:  every section's prose does its assigned job? flagged NEEDs resolved
               or explicitly parked?
draft:         venue self-review checklist passes? audience constraints met? artifact
               cites only adopted advice entries (adopted_A resolve: A -> C -> anchor)?
```

Persona presets (unattended stand-in ONLY)
============================================

```
preset       strictness  ambition  default outcome
─────────    ──────────  ────────  ───────────────
strict       8           4         revise
balanced     5           5         revise
creative     3           8         approve
lenient      2           3         approve
```

In copilot mode (default) the human decides and personas only SHAPE the report's recommendation. In `--unattended[=Ns]` runs the persona decides after the timeout and the ledger records `persona:<preset>`. Full schema: `./gate-persona.md`; attendance modes: `./attendance-modes.md`.

Return contract
================

```
status:     approved | revise | done | awaiting-user
stage:      <stage-name>
mechanical: checks.sh <n ✅ / n ⚠️ / n ❌> · probe-files <PASS | FAIL>
seeded:     <n> > CHECK: comments (stage docs; artifact findings → ledger notes)
criteria:   <n passed> / <m total> (+ per-item marks in the report)
ledger:     <row written or "pending user">
next:       <next stage command or the revise instruction>
```

Risk profile
=============

READ-ONLY on 0-artifacts/*.md -- the deliverable text is never annotated or modified. Writes: `> CHECK:` comments in 0-lifecycle stage docs (at flag sites), the STATUS.md Gate Ledger + current_layer (on approve), and a `[CHECK]` entry in the stage `_LOG`.

### The other files

3 files besides `SKILL.md` and `CHANGELOG.md`, each with the purpose it states about itself. They are described here, not reproduced: the folder is the copy.

```
attendance-modes.md     122 ln  Attendance Modes — Who Clicks "Accept" at Each CHECK
checks.sh               160 ln
gate-persona.md         112 ln  Gate Persona — Reviewer Voice for SOFT Gates
```

<!-- haipipe:skill:body:end -->

## Aims
### P · Page-level health ruling
- P1 · Rule this skill's health.
  **Done when:** `state:` records a human judgment: stable, in flux, needs work, or parked.

## States
### P · Page-level health ruling
- ⬜ P1 · Page generated 260802 1200; nothing ruled yet.

## Log
260802 1200 · page generated from `application/2-phase/3-check/haipipe-application-check/` by `skillpage.py new`

<!-- haipipe:skill:log:start 60d19b76ffbf1d2c application/2-phase/3-check/haipipe-application-check -->

Converted from the skill's own `CHANGELOG.md`: 9 releases.

260804 · `0.4.3`
      - Layers the application checker on the Stage Page Type and generic `haipipe-page-check` routing contract.
      - Leaves application checkers, comment seeding, and the Gate Ledger local while the shared phase owns judgment boundaries.
260724 · `0.4.2`
      Renumbered under the 0.x policy — the whole haipipe-toolkit is pre-1.0 until JL says otherwise (was 4.2.0; older entries below keep their original numbers).
260717 · `4.2.0`
      - Back-port paper-check's checker hardening: replace the fragile hard-coded `../../1-probe/...check-probe-cards.sh` path with a layout-agnostic `find … -path "*haipipe-application-probe*" -name check-probe-cards.sh` glob (path-filtered so it cannot resolve to the paper family's checker) + a not-found FAIL. A missing checker is a FAIL, never a silent skip.
260531 · `1.0.0`
      - baseline.
260623 · `2.0.0`
      - venue-gated; updated stage names to paper vocabulary; simplified for lifecycle model.
260706 · `3.0.0`
      - renamed from haipipe-application-gate, re-homed shared/ -> 2-phase/3-check/ as the CHECK phase worker; Gate Ledger protocol (STATUS.md, By column); stage list on the new spine; persona/attendance kept (unattended stand-in only) (paper-alignment refactor, SOP archived in haipipe-application/CHANGELOG.md §5.0.0).
260706 · `3.1.0`
      - 765696f port: claims exit criteria read the Evidence Campaign (C<n>/PP<nn> sub-items, dispatch order + deps) instead of the old prose-subsection/_EVIDENCE_ shape.
260707 · `4.0.0`
      - paper-check 1.7.0 enforcement port (alignment round 2, SOP §3 R2 / §4 rows 4-5): step 1 Run now executes `./checks.sh <artifact-or-dir> [--md ...] [--depth N]` (NEW in-folder script, markdown-safe subset of paper's: em-dash ❌ house rule, AI-voice tells ⚠️ with the mawk-safe tolower()+boundary-class grep, TODO/FIXME ❌, bibtex-in-markdown ❌; tex machinery — \cite/\ref/\label orphans, Pn.Sn sequence, --compile — deliberately NOT ported) AND the probe-card checker `../../1-probe/haipipe-application-probe/check-probe-cards.sh <intervention_root>`; any ❌/FAIL blocks the gate green, and no persona preset, --unattended timeout, or venue override can approve over it (mechanics fire at every venue depth; scaling governs report verbosity only).
      - `> CHECK:` comment seeding in 0-lifecycle STAGE DOCS ONLY (R2c RULED, JL 2026-07-07: stage-docs-only over artifact HTML-comments and over keeping check fully read-only): 0-artifacts/*.md stay clean because the artifact IS the deliverable text; artifact-level findings land in the Gate Ledger notes column with file:line; on revise the restarted phase reads the stage-doc threads + `> USER:` replies (paper's restart pattern); resolved threads archive to the stage `_LOG`. Risk profile updated (was fully READ-ONLY on stage docs); return contract gains `mechanical:` + `seeded:` lines.
      - Kept untouched: persona presets (gate-persona.md), attendance modes (attendance-modes.md), venue-scaled gate depth, Gate Ledger row format. Housekeeping: 3.1.0 landed in this changelog without a frontmatter bump; resolved by this version.
260709 · `4.1.0`
      - New `grow` verdict for GROW-loop rungs (JL: "after the check, they can think about adding more probes in the draft"): the gate asks "which data topics / probes are still missing?"; grow converts the user's answers to new slots + planned probe skeletons and re-opens DRAFT as [ROUND n+1]. Approve at these rungs = saturated AND the user added nothing.

<!-- haipipe:skill:log:end -->
