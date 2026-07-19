---
name: haipipe-application-enter
description: "Open the Intervention Console for an intervention folder. Use for `/haipipe-application`, `/haipipe-application enter <path>`, `/haipipe-application status [path]`, or when starting work in an existing intervention. GET-OR-CREATE: a missing path offers to scaffold the intervention (confirm-gated; plain folder, no repo backing) and continues into the console. Derives current state from disk (not stored status), renders an open-needs dashboard with the lifecycle frontier, maturity, venue/audience, claim/display/round gaps, loopback diagnosis, and next commands, records session state in .intervention-console.yaml, and routes free-form follow-up input through the lifecycle in copilot mode."
argument-hint: "[intervention-path] [free-form input]"
allowed-tools: Bash, Read, Grep, Glob, Write, Skill
metadata:
  version: "2.3.1"
  last_updated: "2026-07-19"
  summary: "Intervention Console (mirrors the Paper Console): resolve the intervention root, derive state from disk (not stored status), render an open-needs dashboard (frontier + maturity + venue/audience + claim/display/round gaps + releasable probes + loopback), record session state in .intervention-console.yaml, and route free-form follow-up through the lifecycle in copilot mode. Get-or-create scaffolds a missing path (confirm-gated). History: ./CHANGELOG.md."
  # version history: ./CHANGELOG.md (skill-scoped, never loaded at invocation)
---

# haipipe-application-enter (Intervention Console)

Open a concrete intervention folder as the **Intervention Console**: a context-aware working session for one active intervention. It mirrors the Paper Console (`../../../paper/0-enter/haipipe-paper-enter/`).

The console:

```text
1. resolves the intervention root
2. derives current state from disk, not from stored status
3. renders a dashboard panel (lifecycle frontier + maturity + venue/audience + open needs)
4. records session state in .intervention-console.yaml at the intervention root
5. routes later free-form user input through the lifecycle
```

## Missing path = get-or-create (the ONLY way interventions are created)

There is no separate create verb. When the given path does not exist, do NOT fail -- offer to create, but CONFIRM FIRST (never create off a typo):

```text
1. CONFIRM: "<path> does not exist. Scaffold this intervention?"
2. Interventions are plain folders (no repo backing, unlike papers). Scaffold:
   STATUS.md (venue unpinned, current_layer 0-seed, empty Gate Ledger).
   0-lifecycle/ with the venue-FREE spine EAGER (bench ruling 2026-07-09:
   "why don't we have the correct folders at the beginning?"):
   0-seed/ 1a-descriptions/ 1b-themes/ 1c-claims/ 1d-advice/ -- folders only,
   NO stub .md (the console judges progress by real doc content, so an empty
   rung reads as not-started, never done).
   Venue-ALIGNED stages (2-venue/2-pitch/3-narrative/4-display/5-section-edit)
   stay absent-until-written: which exist depends on the pinned venue.
   Also: 0-artifacts/, 1-rounds/, and 1-probes/ (the flat probe pool; its
   README board is created on the first probe).
   Default home: <project>/applications/interventions/<NN>_<slug>/.
3. Continue straight into the console (steps 1-5 above) -- one command from
   nothing to dashboard.
```

The main job is to expose the intervention's current debt board: open claim gaps, display/element gaps, artifact/review gaps, round todo gaps, and evidence needs that may require probe/discover/task work. The user often does not know the next stage in advance; the dashboard makes the next need visible.

Follow-up actions in the same session must treat that dashboard, especially `current_layer`, `next_layer`, venue gating, and open needs/gates, as the working context. A fresh session should run `enter` again.

Story ownership rule: this intervention owns its own story, claim wording, narrative, displays, and artifact text. Shared evidence lives in project-level discoveries and tasks.

Read first:

```text
../../PHILOSOPHY.md
../../1-lifecycle/haipipe-application-lifecycle/SKILL.md   (Intervention Lifecycle Contract)
```

When creating or interpreting explicit need records: `../../haipipe-application/SKILL.md` (Delivery Need Routing section).

## Dashboard Contract (derive from disk)

THE single source of truth for what the Console reads and how the dashboard is rendered. The Console reads the intervention folder and derives state. It NEVER trusts STATUS.md alone — disk wins; STATUS.md drift is flagged.

**Stage frontier detection**

```python
spine = ["0-seed", "1a-descriptions", "1b-themes", "1c-claims", "1d-advice", "venue", "2-pitch", "3-narrative", "4-display", "5-section-edit"]
skipped = read_status_row("stages_skipped")          # written at venue pin
for stage in spine:
    if stage in skipped: continue                    # venue-skipped: passed over, never a gap
    if stage == "venue":
        if not status_hasvenue(): frontier = "venue"; break
    elif not stage_doc_has_content(f"0-lifecycle/{stage}/{stage}.md") or not gate_confirmed(stage):
        frontier = stage; break
else:
    frontier = "draft" if no_artifact() else "review" if not_reviewed() else "deploy"
```

**Open needs detection**

```
Source                                        Need type
───────────────────────                       ──────────────
1a-descriptions: entry stale or undated       data refresh → raise a 1a section
1b-themes: theme without grounding            ungrounded theme → ground or park
1c-claims: status=GAP below settlement bar    claim gap → raise a probe section
1c-claims: status=weak (load-bearing)         weak claim → optional probe
1d-advice: A below settlement bar             under-derived advice → settle its claims
any ladder doc: unresolved [STALE] tag        staleness → re-confirm or revise the entry
1-probes/ section: state=planned              unstarted probe section
1-probes/ section: state=commissioned         in-progress probe (await the QA answer)
4-display: element without task ref           unmaterialized element
5-section-edit: DPRC phase incomplete         section work
0-artifacts/REVIEW-*: verdict=revise          artifact needs revision
1-rounds/latest: status=open                  open round with todo
```

**Dashboard rendering**

Body order per the Output Format section below (Identity → About → Focus Strip → Current State → Stable → Open Needs → Loopback → Next → Artifacts Read). Compact shape:

```
Intervention: 03_refill_reminder
Venue:        sms · audience: patient · settlement: light
Theory:       <one sentence from 2-pitch, or "(pitch not yet written)">

stage:   seed ✅  descriptions ✅  themes ✅  claims 🔥🚀  advice ⬜  venue ⬜  pitch ⬜  narrative --  display --  section-edit --  →  draft ⬜  →  review ⬜  →  deploy ⬜
phase:   draft ✅  │  probe 🔥🚀  │  revise ⬜  │  check ⬜

Claims:     5 total: 2 supported, 1 weak, 2 GAP (bar: light — 1 load-bearing GAP open)
Probes:     2 planned, 1 commissioned, 0 answered, 0 read
Artifacts:  0 drafted, 0 reviewed, 0 deployed
Round:      v260620 (open, 2 todo remaining)

Open needs:
  C2   GAP   "timing matters for refill"  → probe PP01 (commissioned)

Next:
  /haipipe-application probe run PP01
```

**Strip symbols**

The stage line is rendered ONLY by `../../haipipe-application/stage-strip.sh` (🔥 active · 🚀 frontier · ✅ ledger-confirmed · ⬜ not started · `--` venue-skipped). Marker convention: `../../haipipe-application/SKILL.md` Closing Block, the single source of truth. The old ▶️ frontier symbol is retired.

**Session state file (.intervention-console.yaml)**

Written by the Console on entry; a fresh session re-derives everything from disk. Schema: see the Session State section below.

## Input

Accept either an `<intervention-root>` or any path inside one. If no path is supplied, use the current directory.

## Resolve Intervention Root

Look upward from the supplied path until one of these signatures is found:

- `STATUS.md`
- `0-lifecycle/`
- `0-artifacts/`

If no intervention root is found, report `status: blocked` and offer get-or-create (above).

## Read Order

Read only files that exist, in this order:

1. `STATUS.md` (venue, stages_skipped, claims_settlement, current_layer, maturity, Gate Ledger)
2. `0-lifecycle/2-pitch/2-pitch.md` -- HIGH PRIORITY for the dashboard header: extract the goal/theory-of-change paragraph as the 2-3 sentence "what this intervention is about" summary. If absent, the dashboard says "pitch not yet written".
3. Remaining stage docs: `0-lifecycle/0-seed/0-seed.md`, the ladder (`1a-descriptions/1a-descriptions.md`, `1b-themes/1b-themes.md`, `1c-claims/1c-claims.md`, `1d-advice/1d-advice.md`), `3-narrative/3-narrative.md`, `4-display/4-display.md`
4. Section-edit scaffolds (sectioned venues): scan `0-lifecycle/5-section-edit/` for per-section outline `.md`, `_LOG*` files; derive per-section DPRC status from disk.
5. Probe state: the flat pool `1-probes/PPNN_<topic>.md` -- section states (planned/commissioned/answered/read) derived from disk; the README board regenerates from the files.
6. Explicit need records: search stage docs for `NEED`, `GAP`, `TODO`, `blocked`, `missing`, `open`.
7. `0-artifacts/` -- artifact versions, `REVIEW-*`, `CLAIM_AUDIT.md`; deployed markers.
8. `1-rounds/latest.md`, then the referenced round README, `discussion.md`, `decisions.md`, `todo.md`, `applied.md` if they exist.
9. Git state: `git status --short --branch`, `git log --oneline --max-count=3` (when inside a repo).

## Diagnosis Rules

Derive the current layer from disk. Read `STATUS.md` only as a hint: a stage is done only when its `.md` resolves on disk with real content (not a scaffold stub) AND its Gate Ledger row is confirmed. The frontier is the first non-skipped stage whose disk predicate fails. If `STATUS.md` claims more progress than disk shows, flag DRIFT and trust disk.

## Legacy layout = offer the one-shot migration (confirm-gated)

Pre-ladder interventions (scaffolded before 2026-07-09) show `0-lifecycle/1-claims/` and no rung folders. Flag LAYOUT DRIFT on the dashboard and OFFER the migration -- never migrate silently, and never let a rung skill scaffold `1a-descriptions/` NEXT TO a stale `1-claims/` (the bench hit exactly this: "we should have 1a-descriptions!!!!"). On the user's yes:

```text
1. rename 0-lifecycle/1-claims/ -> 0-lifecycle/1c-claims/
   (inside: 1-claims.md -> 1c-claims.md, _LOG_1-claims.md -> _LOG_1c-claims.md)
2. scaffold the missing rungs 1a-descriptions/ 1b-themes/ 1d-advice/
3. migrate any legacy per-stage `_PROBE/` cards into the flat pool `1-probes/`
   in the new section shape; a section's `serves:` sets its rung affinity
   (data-profile questions serve 1a-descriptions, settling D ids; claim
   questions serve 1c-claims) -- the path no longer carries the stage
4. the board regenerates from 1-probes/ on disk (no separate index to update)
5. consume seed [FORWARD -> CLAIMS] pointers per the 1a contract; log the migration
   in each touched rung's _LOG (worked example: designs/Project-Application-SMSDesign/
   applications/01_sms_young_male, _LOG_1a-descriptions.md v260709)
6. STATUS.md keeps its Gate Ledger; the move marks nothing as done
```

Per-stage inference (venue-skipped stages are passed over, never counted as gaps):

| Evidence | Current layer |
|---|---|
| only README / seed doc | `0-seed` |
| seed exists but ladder absent/thin | `0-seed -> 1a-descriptions` (suggest the `ladder` sweep) |
| descriptions exist but themes absent/thin | `1a-descriptions -> 1b-themes` |
| themes exist but claims absent/thin | `1b-themes -> 1c-claims` |
| claims exist but advice absent/thin | `1c-claims -> 1d-advice` |
| ladder gated but venue not pinned in STATUS.md | `1d-advice -> venue` |
| venue pinned but pitch absent/thin | `venue -> 2-pitch` |
| pitch exists but narrative absent (venue requires it) | `2-pitch -> 3-narrative` |
| narrative exists but display absent (venue requires it) | `3-narrative -> 4-display` |
| display exists but sections absent (venue requires them) | `4-display -> 5-section-edit` |
| lifecycle done for this venue, no artifact | ready for `draft` |
| artifact exists, no review pass | `draft -> review` |
| reviewed, not shipped | `review -> deploy` |

Maturity, derived separately from disk:

| Evidence | Maturity |
|---|---|
| seed only | `prospect` |
| 1a with anchored D entries | `data-described` |
| 1c ledger with C-slots | `claim-ledger` |
| 1d with derived A entries (ladder gate passed) | `advised` |
| venue pinned in STATUS.md | `venue-pinned` |
| pitch onward per venue's required stages | `pitched` / `narrated` / `display-mapped` / `section-edit` |
| 0-artifacts/ has >=1 artifact | `drafted` |
| review pass completed | `reviewed` |
| artifact shipped to channel | `deployed` |
| post-deploy round open with A/B results | `iterating` |
| kill criterion met | `retired` |

Need diagnosis is separate from lifecycle layer. Extract open needs from:

| Surface | Typical need |
|---|---|
| `1a-descriptions` stale/undated entries; unresolved `[STALE]` tags in any ladder doc | data refresh (1a probe) |
| `1b-themes` ungrounded themes | ground or park |
| `1c-claims` GAP/weak rows below the venue's required settlement | probe, discovery, task |
| `1d-advice` under-derived A entries | settle the cited claims |
| `4-display` elements without materialized output | display task |
| `5-section-edit` sections with incomplete DPRC phases | section-edit work |
| artifact review flags / claim-audit failures | revise or loop back |
| round `todo.md` unresolved items | edit, probe, display, deploy |

Classify each open item using the delivery-need interface: `probe | discovery | task | display | edit`.

Loopback diagnosis:

| Symptom | Return to |
|---|---|
| wording, tone, stale number in artifact | `draft` (artifact) or `5-section-edit` |
| content element does not carry its claim | `4-display` |
| unsupported or too-strong claim | `1c-claims` / `3-narrative` |
| advice entry does not follow from its claims | `1d-advice` |
| theory of change wrong / goal fuzzy | `2-pitch` |
| venue wrong for audience | `venue` (re-pin; pitch+ re-couple; the ladder survives) |
| A/B shows no effect | `2-pitch` or `1c-claims` (backfill A/B data into `1a` first) |
| kill criterion met | `0-seed` -> STATUS.md `retired` |

## Output Format

The dashboard leads with WHAT THE INTERVENTION IS ABOUT, then WHERE IT STANDS, then WHAT TO DO NEXT.

Render the stage strip deterministically with the helper, never hand-typed:

```sh
sh "$CLAUDE_SKILL_DIR/../../haipipe-application/stage-strip.sh" <intervention-root>
```

Body order -- sections MUST appear in this sequence:

```markdown
## Intervention Identity

| Field | Value |
|---|---|
| Intervention | <name from STATUS.md> |
| Venue | <venue or "unpinned"> |
| Audience | <audience> |
| Path | ... |

## What This Intervention Is About

<2-3 sentences from 2-pitch, or "Pitch not yet written -- run /haipipe-application pitch.">

## Focus Strip (two lines)

<stage line via stage-strip.sh; phase line from the 🔥 stage's DPRC progress.
Full marker convention: haipipe-application/SKILL.md Closing Block (the single
source of truth). Venue-skipped stages render `--` and never carry 🔥/🚀.>

## Current State

| Field | Value |
|---|---|
| Current layer | ... |
| Next layer | ... |
| Maturity | ... |
| Claims settlement | <required by venue> · <actual: N supported / M weak / K GAP> |
| Active round | <vYYMMDD or none> |

## Stable

- ...

## Open Needs

| Need | Type | Source | Suggested route |
|---|---|---|---|
| ... | probe/display/discovery/task/edit | ... | ... |

## Releasable Probes

<from the probe pool read (1-probes/ section states). Releasable =
`state: planned` AND dependencies met -- these are held for the user's APPROVE
(the probe worker's ORGANIZE advances only approved questions). One row per
section; never bury this in Recommended Next (feedback 2026-07-09: "you should
let me know what probes to release"). Omit the section only when zero questions exist.>

| PP | Stage | Mode | Need (one line) | Deps | Release |
|---|---|---|---|---|---|
| PPNN | ... | light/full | ... | met / blocked on <what> | `/haipipe-application probe run PPNN` |

<then one summary line for the rest of the roster: `commissioned: PPNN ... · read: PPNN ...`>

## Loopback Diagnosis

- ... (omit if none)

## Recommended Next

1. `/haipipe-application ...`
2. ...

## Artifacts Read

- ...

(return-contract tail here, then the two-line focus strip as the very last lines)
```

Keep the dashboard concise. The goal is to orient the session, not to redo the intervention.

## Free-form Routing

After the dashboard, route follow-up input through the lifecycle:

```text
seed                       -> /haipipe-application seed
ladder / 1a-1d sweep       -> /haipipe-application ladder
descriptions / profile     -> /haipipe-application descriptions
themes / patterns          -> /haipipe-application themes
claims / ledger            -> /haipipe-application claims
advice / recommendations   -> /haipipe-application advice
venue / channel            -> /haipipe-application venue
pitch / goal               -> /haipipe-application pitch
narrative / arc            -> /haipipe-application narrative
display / elements         -> /haipipe-application display
section / §N               -> /haipipe-application section-edit
draft / write the <venue>  -> /haipipe-application draft
review / audit             -> /haipipe-application review | claim-audit
deploy / ship              -> /haipipe-application deploy
round / todo               -> /haipipe-application round
iterate / A/B              -> /haipipe-application iterate
probe / evidence           -> /haipipe-application probe [...]
```

If the input does not name a stage, route to the current frontier from the dashboard. If the input is ambiguous, ask before acting.

## Copilot Policy

Default mode is copilot. The console may automatically read files, summarize the frontier, classify input, draft or revise a stage `.md`, and suggest routes.

It must ask before:

```text
calling costly task/PHI/full-data work
committing or downgrading a claim's status in 1c-claims.md
deploying to a live channel
opening or closing a revision round destructively
```

## Session State

Record the console session at the intervention root:

```yaml
# .intervention-console.yaml
intervention_root: <path>
active_intervention: <name>
venue: <pinned venue or "">
current_layer: <frontier stage>
maturity: <maturity rung>
active_round: <vYYMMDD or none>
open_needs: <count>
updated: <YYMMDD>
```

This is session state, not content. A fresh session re-derives it from disk.

## Return Contract

Every reply from an application specialist (and every enter dashboard) MUST end with the closing block defined in `../../haipipe-application/SKILL.md` (Closing Block section, the single source of truth). Omitting it is a protocol violation. Shape:

```text
── 🎯 application · claims 🔥 ─────────────────
status:  ok · claims
next:    <single recommended command>
──────────────────────────────────────────────
stage:   seed ✅  descriptions ✅  themes ✅  claims 🔥🚀  advice ⬜  venue ⬜  pitch ⬜  narrative --  display --  section-edit --  →  draft ⬜  →  review ⬜  →  deploy ⬜
phase:   draft ✅  │  probe 🔥🚀  │  revise ⬜  │  check ⬜
```

`status` merges the state and the active stage on one line: `ok` (dashboard rendered) · `blocked` (missing root or unresolvable state) · `failed` (read error / inconsistent disk state). NO `intervention_root` or `current_layer` lines in the tail -- the header rule and the stage line already carry them. Render the stage line with `../../haipipe-application/stage-strip.sh`; the closing block is the very last thing in every reply.
