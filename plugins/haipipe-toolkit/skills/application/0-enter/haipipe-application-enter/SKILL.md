---
name: haipipe-application-enter
description: "Open the Intervention Console for an intervention folder. Use for `/haipipe-application`, `/haipipe-application enter <path>`, `/haipipe-application status [path]`, or when starting work in an existing intervention. GET-OR-CREATE: a missing path offers to scaffold the intervention (confirm-gated; plain folder, no repo backing) and continues into the console. Derives current state from disk (not stored status), renders an open-needs dashboard with the lifecycle frontier, maturity, venue/audience, claim/display/round gaps, loopback diagnosis, and next commands, records session state in .intervention-console.yaml, and routes free-form follow-up input through the lifecycle in copilot mode."
argument-hint: "[intervention-path] [free-form input]"
allowed-tools: Bash, Read, Grep, Glob, Write, Skill
metadata:
  version: "2.1.0"
  last_updated: "2026-07-14"
  summary: "Intervention Console rewritten on the paper-enter model: paper-aligned spine (claims before venue), Gate Ledger awareness, get-or-create, closing block inheritance. Replaces the pre-v4 maturity ladder (rationale/design/variants/delivery-plan). v2.1.0 (probe redesign, Tools/plugins/haipipe-toolkit/diagram/260714-probe-qa/ v3 approved JL 2026-07-14): probe state is DERIVED from 1-probes/PP*.md on disk -- per question SECTION, its state (planned | commissioned | answered | read | answered-local | failed), resolved by ls-ing its target:. Never a stored status. An OVERDUE commissioned section is a loud open need. Scaffolding creates 1-probes/ instead of the retired 1-probe-plans/README.md index."
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
   STATUS.md (venue unpinned, current_layer 0-seed, empty Gate Ledger),
   0-lifecycle/ (stage folders absent-until-written), 0-artifacts/,
   1-rounds/, 1-probes/ (empty; probe files are created when the first question is raised).
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
../../wiki/03-intervention-lifecycle.md
../../wiki/05-intervention-dashboard.md
```

When creating or interpreting explicit need records: `../../wiki/11-delivery-need.md`.

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
3. Remaining stage docs: `0-lifecycle/0-seed/0-seed.md`, `1-claims/1-claims.md`, `3-narrative/3-narrative.md`, `4-display/4-display.md`
4. Section-edit scaffolds (sectioned venues): scan `0-lifecycle/5-section-edit/` for per-section outline `.md`, `_LOG*` files; derive per-section DPRC status from disk.
5. Probe state: DERIVED from `1-probes/PP*.md` on disk — per question SECTION, its `state:` (planned | commissioned | answered | read | answered-local | failed), resolved by `ls`-ing its `target:`. Never a stored status. An OVERDUE `commissioned` section (eta passed, no QA file) is an open need, and a loud one.
6. Explicit need records: search stage docs for `NEED`, `GAP`, `TODO`, `blocked`, `missing`, `open`.
7. `0-artifacts/` -- artifact versions, `REVIEW-*`, `CLAIM_AUDIT.md`; deployed markers.
8. `1-rounds/latest.md`, then the referenced round README, `discussion.md`, `decisions.md`, `todo.md`, `applied.md` if they exist.
9. Git state: `git status --short --branch`, `git log --oneline --max-count=3` (when inside a repo).

## Diagnosis Rules

Derive the current layer from disk. Read `STATUS.md` only as a hint: a stage is done only when its `.md` resolves on disk with real content (not a scaffold stub) AND its Gate Ledger row is confirmed. The frontier is the first non-skipped stage whose disk predicate fails. If `STATUS.md` claims more progress than disk shows, flag DRIFT and trust disk.

Per-stage inference (venue-skipped stages are passed over, never counted as gaps):

| Evidence | Current layer |
|---|---|
| only README / seed doc | `0-seed` |
| seed exists but claims absent/thin | `0-seed -> 1-claims` |
| claims exist but venue not pinned in STATUS.md | `1-claims -> venue` |
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
| seed + claims ledger with C-slots | `claim-ledger` |
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
| `1-claims` GAP/weak rows below the venue's required settlement | probe, discovery, task |
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
| unsupported or too-strong claim | `1-claims` / `3-narrative` |
| theory of change wrong / goal fuzzy | `2-pitch` |
| venue wrong for audience | `venue` (re-pin; pitch+ re-couple; claims survives) |
| A/B shows no effect | `2-pitch` or `1-claims` |
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
claims / ledger            -> /haipipe-application claims
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
committing a claim verdict or downgrading a claim
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
stage:   seed ✅  claims 🔥🚀  venue ⬜  pitch ⬜  narrative --  display --  section-edit --  →  draft ⬜  →  review ⬜  →  deploy ⬜
phase:   draft ✅  │  probe 🔥🚀  │  revise ⬜  │  check ⬜
```

`status` merges the state and the active stage on one line: `ok` (dashboard rendered) · `blocked` (missing root or unresolvable state) · `failed` (read error / inconsistent disk state). NO `intervention_root` or `current_layer` lines in the tail -- the header rule and the stage line already carry them. Render the stage line with `../../haipipe-application/stage-strip.sh`; the closing block is the very last thing in every reply.
