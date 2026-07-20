---
name: haipipe-paper-enter
description: "Open the Paper Console for a paper repo. Use for `/haipipe-paper`, `/haipipe-paper enter <paper-path>`, `/haipipe-paper status [paper-path]`, or when starting work in an existing paper folder. GET-OR-CREATE: a missing path offers to create the paper (confirm-gated, repo-backed inside Project-* repos). Derives state from disk (not stored status), renders an open-needs dashboard (frontier, maturity, claim/display/round gaps, loopback diagnosis, next commands), records session state in .paper-console.yaml, and routes free-form input through the lifecycle in copilot mode."
argument-hint: "[paper-path] [--org <owner>] [free-form input]"
allowed-tools: Bash, Read, Grep, Glob, Write, Skill
metadata:
  version: "4.1.1"
  last_updated: "2026-07-19"
  summary: "Paper Console: a derive-from-disk dashboard + lifecycle router, and THE home of the dashboard spec (golden rule, frontier predicates, glyphs, shallow check, render skeleton). Renders the 9-stage spine (seed · resource · claims · venue · pitch · narrative · display · section-edit · review) and a four-glyph DPRC phase strip; the resource predicate honours the `n/a` exemption for pre-2026-07-14 papers. History: ./CHANGELOG.md."
  # version history: ./CHANGELOG.md (skill-scoped, never loaded at invocation)
---

# haipipe-paper-enter (Paper Console)

Open a concrete paper folder as the **Paper Console**: a context-aware working session for one active paper.
It mirrors the Probe Console.

The console:

```text
1. resolves the paper root
2. derives current state from disk, not from stored status
3. renders a dashboard panel (lifecycle frontier + maturity + open needs)
4. records session state in .paper-console.yaml at the paper root
5. routes later free-form user input through the lifecycle
```

## Missing path = get-or-create (the ONLY way papers are created)

There is no separate create verb.
When the given path does not exist, do NOT fail -- offer to create, but CONFIRM FIRST (repo creation is outward-facing; never create off a typo):

```text
1. CONFIRM: "<path> 不存在。要建这个 paper 吗？" -- and resolve --org (flag or ask,
   NEVER assume; the paper's owner may differ from the project's org).
2. Parent is a Project-* repo -> paper is REPO-BACKED: follow the papers-inside
   recipe in project/haipipe-project/fn/repo-project.md (gh repo create
   <org>/<Paper-Name> --private + git submodule add at the PROJECT's papers/).
   Plain projects: just the folder.
3. Scaffold contents via Skill("haipipe-paper-lifecycle", args="folder <path>").
4. Repo-backed: double-bump (paper push -> project pointer -> workspace pointer).
5. Continue straight into the console (steps 1-5 above) -- one command from
   nothing to dashboard.
```

The main job is to expose the paper's current debt board: open claim gaps, display/table gaps, section-edit phase gaps, round todo gaps, and evidence needs that may require probe/discover/task work.
The user often does not know the next stage in advance; the dashboard makes the next need visible.

Follow-up paper actions in the same session must treat that dashboard, especially `current_layer`, `next_layer`, and open needs/gates, as the working context.
A fresh Claude/Codex session should run `enter` again.

Story ownership rule: this paper owns its own story, claim wording, narrative, displays, and section editing.
Shared evidence lives in project-level tasks and discoveries.
Do not look for or require a project-level narrative layer.

Read first:

```text
../../PHILOSOPHY.md
../../1-lifecycle/ref/04-lifecycle-map.md
```

The dashboard spec itself lives in this file (Dashboard Spec, below) — this skill owns it.

Then, when the task touches lifecycle shape or rounds:

```text
../../1-lifecycle/ref/03-paper-lifecycle.md
../haipipe-paper-round/SKILL.md          ("Rounds contract")
../../README.md                           (skill-tree layout, Router Rule, Maturity Rule)
```

When creating or interpreting explicit need records, use `../../haipipe-paper/SKILL.md` ("Delivery Need Routing").

## Input

Accept either:

```text
<paper-root>
```

or any path inside a paper root.
If no path is supplied, use the current directory.

## Resolve Paper Root

Look upward from the supplied path until one of these signatures is found:

- `STATUS.md`
- `0-lifecycle/`
- `0-*.tex` and `0-sections/`
- `1-compile.sh` and `0-sections/`

If no paper root is found, report `status: blocked` and suggest:

```text
/haipipe-paper seed "<paper-path>"
/haipipe-paper-lifecycle folder "<paper-path>"
```

## Read Order

Read only files that exist, in this order:

1. `STATUS.md`
2. `0-lifecycle/README.md`
2b.
`0-lifecycle/2b-pitch/2b-pitch.tex` (or `.md`) -- HIGH PRIORITY for dashboard header.
Extract the `\section*{One-Minute Pitch}` paragraph and the `\section*{Hook}` paragraph.
These become the 2-3 sentence "what this paper is about" summary at the top of the dashboard.
If the file does not exist or lacks these sections, the dashboard says "pitch not yet written".
3. Stage TeX/MD files (remaining):
   - `0-lifecycle/0-seed/0-seed.tex`
   - `0-lifecycle/1a-resource/1a-resource.md` (venue-FREE prerequisite contract; absent on every pre-2026-07-14 paper -- see the resource exemption below)
   - `0-lifecycle/1b-claims/1b-claims.tex` (or `.md`)
   - `0-lifecycle/3-narrative/3-narrative.tex`
   - `0-lifecycle/4-display/4-display.tex`
4. Section-edit sections: scan `0-lifecycle/5-section-edit/` for per-section `.md` files and their `_LOG_*` files.
   Derive per-section DPRC status from what exists on disk.
4b. `1-probes/PP*.md`: the paper's open questions. Per entry read its `**state**` and whether `### a-executor` is filled — this is what the phase strip's `probe` glyph is derived from.
5. Explicit need records in lifecycle TeX comments or markdown tables.
   Search for `NEED`, `GAP`, `TODO`, `blocked`, `missing`, and `open`.
6. `0-displays/README.md`
7. `0-displays/*/README.md`
8. `0-sections/README.md`
9. `0-sections/*.tex` names and short headers/comments only; do not read full long sections unless needed to diagnose section-edit drift.
10. `1-rounds/latest.md`, then the referenced round README, `discussion.md`, `decisions.md`, `todo.md`, and `applied.md` if they exist.
11. Git state:
   - `git status --short --branch`
   - `git log --oneline --max-count=3`

## Dashboard Spec

THE single source of truth for the behavior of `/haipipe-paper` with no arguments inside a paper, and for the panel this Console renders.
The dashboard is a derive-from-disk preflight. It orients the session before the Console or any lifecycle stage acts.

### Golden Rule

```text
Never report a stage as done because STATUS.md says so.
A stage is done only when its expected artifact resolves on disk with real
content (not the scaffold stub).
When stored status and disk disagree, disk wins and the gap is flagged DRIFT.
```

### Lifecycle frontier

The dashboard uses the paper lifecycle spine:

```text
0-seed -> 1-resource -> 1-claims -> venue -> 2-pitch -> 3-narrative -> 4-display
-> 5-section-edit -> review
```

(`1-resource` and `1-claims` share the number 1, deliberately, exactly as `2-venue` and `2-pitch` already do. The number is decoration; the spine key is the bare name `resource`, and `stage-strip.sh` strips the digit before matching.)

The frontier is the first stage whose disk predicate fails.

| Stage | Done when | Next action if frontier |
|---|---|---|
| `0-seed` | `0-lifecycle/0-seed/0-seed.md` has question / motivations / claim-shape content | `/haipipe-paper seed` |
| `1-resource` | `0-lifecycle/1a-resource/1a-resource.md` exists with its two sections (Demand, Questions); **`n/a` counts as a PASS** -- see the resource exemption in Diagnosis Rules | `/haipipe-paper resource` |
| `1-claims` | `0-lifecycle/1b-claims/1b-claims.md` ledger non-empty, each row has a status (anchor `planned` still counts as a status; unmaterialized evidence is an open need, not a stage fail) | `/haipipe-paper claims` |
| `venue` | STATUS.md `venue:` pinned to a playbook pack | `/haipipe-paper venue` |
| `2-pitch` | `0-lifecycle/2b-pitch/2b-pitch.md` has a one-line pitch | `/haipipe-paper pitch` |
| `3-narrative` | `0-lifecycle/3-narrative/3-narrative.md` has an arc | `/haipipe-paper narrative` |
| `4-display` | `4-display.tex` maps claim -> display and display units exist | `/haipipe-paper figures` |
| `5-section-edit` | `0-lifecycle/5-section-edit/<section>/` scaffolds exist and `0-sections/*.tex` compile to PDF | `/haipipe-paper section-edit` |
| `review` | audits pass and venue checks pass | `/haipipe-paper review` |

Glyphs:

```text
OK       done on disk
ACTIVE   current frontier
TODO     not reached
DRIFT    STATUS.md claims progress but the disk predicate fails
BLOCKED  explicit blocker (open need / failed gate)
```

### Shallow check

For each paper:

```text
1. Read STATUS.md (current_layer, maturity, active_round) as a hint only.
2. For each stage, test its disk predicate above.
3. Set current_layer to the first failing stage (the frontier).
4. If STATUS.md current_layer is ahead of the disk frontier, flag DRIFT.
5. Surface open needs from 1-claims GAP rows, 4-display missing units,
   5-section-edit open checklist items, section TODOs, and
   1-rounds/<round>/todo.md.
```

### Render skeleton

Lead with a paper header, then a one-line Story, then the progress spine. This is the panel a session sees on enter. Keep it tight; open needs follow below it.

```text
📄 <paper-folder-name>  ·  <venue>

  Story: <one plain sentence: the angle + the surprising mechanism + scope/caveat,
         compressed from 2b-pitch.md (fallback 3-narrative). Append "(关联,非因果)"
         when 1-claims marks the claim observational.>

  进度  seed ─ resource ─ claims ─ venue ─ pitch ─ narrative ─ display ─ section-edit ─ review
         <g>    <g>        <g>      <g>     <g>     <g>         <g>       <g>            <g>
                                                       🔥 这里(<one-clause why this is the frontier>)
```

Per-stage glyph (derive-from-disk; show each stage's TRUE state, not a blanket todo downstream):

```text
✅ done       the stage predicate passes AND the artifacts it references resolve
(草稿)         the artifact exists but is rough / incomplete (e.g. sections drafted but thin)
⬜ todo       absent, empty, or its referenced anchors do not resolve
🔥 frontier   the FIRST stage that is not ✅; overlay it and annotate "← 这里"
⚠️ drift      STATUS.md claims this stage done but the disk predicate fails
```

Worked example (MedJournal, derived from disk on 2026-06-22):

```text
📄 Paper-Personality-Opioid-MedJournal  ·  medical journal (IMRAD)

  Story: 患者感知的医生"可亲和性"(LLM 从评论里测)越高 → 腰背痛阿片处方强度越高,
         主要走"已开药者剂量"而非开药人数,双重资格人群更明显。(关联,非因果)

  进度  seed ─ resource ─ claims ─ venue ─ pitch ─ narrative ─ display ─ section-edit ─ review
         ✅     n/a        ✅       ✅      ✅      ✅          🔥        (草稿)          ⬜
                                                              ← 这里(0-displays 只有 display00,01-04 没建)
```

(`resource n/a` = the exemption in Diagnosis Rules. This paper was seeded before the resource stage shipped, so the frontier walks past resource to claims; `n/a` is a PASS and is NOT drift.)

Frontier = display: `4-display.tex` names Display 01-04 but `0-displays/` has only display00. section-edit shows (草稿) because `0-sections/*.tex` have rough prose while their display anchors are unbuilt.
The Story line is the compressed 2-pitch one-liner; if the pitch is only a flat summary, compress it but keep it one sentence.

Field sources:

```text
<venue>   STATUS.md  venue_frame   (fallback: venue_target, then 1-config.yaml)
<paper>   the paper folder name
Story     one sentence (may wrap ~2 lines), in the paper's working language;
          compressed from 2b-pitch.md P1 + the mechanism + the scope clause;
          append "(关联,非因果)" iff 1-claims marks the claim observational
```

Open needs block (printed directly under the panel; short, it is "what to do next", not a report). Route each per Delivery Need Routing in `../../haipipe-paper/SKILL.md`:

```text
Open needs (from 1-rounds/<round>/todo.md + 1-claims planned/GAP rows + missing displays):
  - <gap> -> <route>     e.g. Materialize Display 01-04 -> /haipipe-task-for-display
  - <gap> -> <route>     e.g. Backfill C1-C5 evidence anchors -> /haipipe-paper probe "<need>"
                              (opens a question ENTRY in 1-probes/; the PROBE phase MATCHes
                               the bank first, and commissions only if nothing answers it)
```

Round todo items and claim/display gaps are first-class open needs, not afterthoughts. The dashboard lists them with a suggested route (probe/discovery/task/display/paper-edit).

## Diagnosis Rules

Derive the current layer from disk, following the Dashboard Spec above.
Read `STATUS.md` only as a hint: a stage is done only when its `.tex` or `.md` resolves on disk with real content (not the scaffold stub).
The frontier is the first stage whose disk predicate fails.
If `STATUS.md` claims more progress than disk shows, flag DRIFT and trust disk.

Per-stage inference when disk is the source of truth:

| Evidence | Current layer |
|---|---|
| only `README.md` / seed lifecycle | `0-seed` |
| seed exists but resource is absent/thin (and NOT exempt -- see below) | `0-seed -> 1-resource` |
| resource settled (or exempt) but claims are absent/thin | `1-resource -> 1-claims` |
| claims exist but venue is not pinned in STATUS.md | `1-claims -> venue` |
| venue pinned but pitch is absent/thin | `venue -> 2-pitch` |
| pitch exists but narrative is absent/thin | `2-pitch -> 3-narrative` |
| narrative exists but display units are missing | `3-narrative -> 4-display` |
| display plan exists but display units/canonical PDFs are missing | `4-display` |
| display units exist and placed | ready for `5-section-edit` |

**Resource exemption -- `n/a` COUNTS AS PASS (binding).**
The resource stage shipped 2026-07-14; every paper already on disk predates it and none will get a `1a-resource.md` written retroactively.
So for the resource predicate, `n/a` is an ACCEPTED PASS: a paper whose seed gate closed BEFORE the stage existed passes by exemption and the frontier walks straight past it to claims.
Without this, every live paper's frontier REGRESSES to `resource` and the console reports DRIFT on seeds JL personally approved.
The exemption is per-paper and backwards-only -- a paper seeded after 2026-07-14 gets no exemption, and an absent `1a-resource.md` is a real frontier.

(The stage strip renders such a paper `resource ⬜` -- that is the strip's artifact-on-disk test, not a frontier claim.
`⬜` on an exempt paper is NOT drift; do not flag it.)

Infer maturity separately from current layer -- read it from artifacts, never assumed:

| Evidence | Maturity |
|---|---|
| seed / pitch only | `seed` |
| 1-resource settled: every demand HAVE+FIT, COMMISSIONED, or SCOPE CUT | `resource` |
| demand is real but the resource is in flight / behind a DUA -- nothing to do but wait (resource's `park` exit) | `resource-blocked` |
| lifecycle + sections + compile script | `scaffold` |
| 1-claims has explicit claims | `claim-ledger` |
| 4-display maps claim -> display | `display-map` |
| section-edit scaffolds with DPRC in progress | `section-edit` |
| sections compile with prose | `draft` |
| checks/audits mostly pass | `submission-candidate` |
| frozen PDF + submission metadata | `submitted` |
| active 1-rounds round after external/coauthor review | `revision` |
| final external state | `accepted/published` |

Need diagnosis is separate from lifecycle layer.
Extract open needs from:

| Surface | Typical need |
|---|---|
| `1-resource` unanswered `Q<n>` (no **A**), or a BUILD section whose `eta:` has passed | probe (the PROBE worker opens the SECTION and routes it -- the stage only ASKS) |
| `1-claims` GAP/weak/unsupported rows | probe, discovery, task |
| `4-display` missing display units | display or task |
| `5-section-edit` sections with incomplete DPRC phases | section-edit work |
| section comments/TODOs | paper edit or evidence need |
| round `todo.md` unresolved items | paper edit, probe, display, citation |

Classify each open item using the delivery-need interface:

```text
probe | discovery | task | display | paper-edit
```

Loopback diagnosis follows the paper lifecycle:

| Symptom | Return to |
|---|---|
| wording, citation, format, stale number | section-edit cycle |
| figure/table unclear or lacks source/caption/preview | `4-display` |
| unsupported or too-strong claim | `1-claims` / `3-narrative` |
| the claim's data/checkpoint/producing-code does not exist, or exists but cannot CARRY the claim | `1-resource` |
| story not compelling or abstract/intro disagree | `2-pitch` |
| every demand row is unobtainable -- the paper cannot be written as seeded | `0-seed` (resource's `reseed` exit) |
| paper no longer viable | `0-seed` |

## Output Format

The dashboard leads with WHAT THE PAPER IS ABOUT, then WHERE IT STANDS, then WHAT TO DO NEXT.
Operational details come after orientation.

Render the stage strip deterministically with the helper, never hand-typed:

```sh
sh "${CLAUDE_SKILL_DIR:-.}/../../haipipe-paper/stage-strip.sh" <paper-root>
```

It prints one line driven by `STATUS.md current_layer`, over the 9-stage spine `seed resource claims venue pitch narrative display section-edit review`.
Real output (Paper-ScalingGlucose-NatSeries2026, 2026-07-14):

```text
seed ✅  resource ⬜  claims ✅  venue ✅  pitch ✅  narrative ✅  display ✅  →  section-edit 🚀  →  review ⬜
```

(`resource ⬜` on a live paper is the EXEMPTION, not drift -- the stage postdates the paper.
See the resource exemption in Diagnosis Rules.)

This strip appears twice: once near the top (orientation) and once as the VERY LAST LINE of the reply (closing every reply in the session, not just the first dashboard; see the orchestrator's "Stage Strip" rule).

Per the Lifecycle TeX Quality Standard (`../../3-deliver/haipipe-paper-deliver/SKILL.md`), a stale PDF is a defect: flag any stage whose `.tex` is newer than its `.pdf` as a stale deliverable in the Open Needs section.

Body order -- sections MUST appear in this sequence:

```markdown
## Paper Identity

| Field | Value |
|---|---|
| Paper | <title from STATUS.md> |
| Venue | <venue from STATUS.md> |
| Path | ... |
| Branch | ... |

## What This Paper Is About

<2-3 sentence summary distilled from the \section*{One-Minute Pitch} paragraph
and the \section*{Hook} paragraph of 0-lifecycle/2b-pitch/2b-pitch.tex.
If no pitch exists, print: "Pitch not yet written -- run /haipipe-paper pitch.">

## Focus Strip (two lines)

The strip uses two markers to show both where we are and how far the paper has reached. Full convention in the haipipe-paper umbrella SKILL.md, Closing Block section (the single source of truth).

| Marker | Meaning |
|---|---|
| 🔥 | **Active now** -- the stage/phase we are currently working on |
| 🚀 | **Frontier** -- the farthest stage/phase the paper has ever reached |

Every line carries EXACTLY one 🔥 and EXACTLY one 🚀, never zero. "Reached" means entered, not completed: a virgin paper working its first phase renders `draft 🔥🚀`, not `draft 🔥`. The markers split only on loopback (🚀 stays at the frontier slot while 🔥 moves back); when they land on the same item, collapse to `🔥🚀`.

**Line 1 (stage):** all lifecycle stages. 🔥 marks the active stage, 🚀 marks the frontier. If the active stage is section-edit, append the specific section name in parentheses.

**Line 2 (phase):** the DPRC phase status within the 🔥 stage. 🔥 marks the active phase, 🚀 marks the farthest phase reached at the frontier stage. Four glyphs, one per phase, the same at every stage.

Examples:

Working at the frontier -- THE default case, e.g. a fresh paper in seed/DRAFT (active = frontier, markers collapse):
```
stage:   seed 🔥🚀  resource ⬜  claims ⬜  venue ⬜  pitch ⬜  narrative ⬜  display ⬜  →  section-edit ⬜  →  review ⬜
phase:   draft 🔥🚀  │  probe ⬜  │  revise ⬜  │  check ⬜
```

Working the resource stage (the venue-FREE prerequisite stage between seed and claims):
```
stage:   seed ✅  resource 🔥🚀  claims ⬜  venue ⬜  pitch ⬜  narrative ⬜  display ⬜  →  section-edit ⬜  →  review ⬜
phase:   draft 🔥🚀  │  probe ⬜  │  revise ⬜  │  check ⬜
```

Frontier at section-edit (section name appended; probe shows sub-tracks). `resource ⬜` here is the EXEMPTION -- this paper predates the stage, and that is a PASS, not drift:
```
stage:   seed ✅  resource ⬜  claims ✅  venue ✅  pitch ✅  narrative ✅  display ✅  →  section-edit (§1 introduction) 🔥🚀  →  review ⬜
phase:   draft 🔥🚀  │  probe ⬜  │  revise ⬜  │  check ⬜
```

Loopback: redoing seed while paper has reached section-edit (🚀 stays at the frontier; seed has no probe sub-tracks):
```
stage:   seed 🔥  resource ✅  claims ✅  venue ✅  pitch ✅  narrative ✅  display ✅  →  section-edit 🚀  →  review ⬜
phase:   draft 🔥  │  probe ⬜  │  revise ⬜  │  check 🚀
```

Loopback to pitch while frontier is display:
```
stage:   seed ✅  resource ✅  claims ✅  venue ✅  pitch 🔥  narrative ✅  display 🚀  →  section-edit ⬜  →  review ⬜
phase:   draft ✅  │  probe ⬜  │  revise 🔥  │  check 🚀
```

How to derive:
- 🔥 stage = what the user is actively working on (explicit request or current task).
- 🚀 stage = the lifecycle frontier (farthest stage whose disk predicate passed). If the user specifies a section ("work on §3"), the section name appears in parentheses after the stage.
- The section name comes from the outline file name (e.g., `1-introduction.md` -> `§1 introduction`, `3-theory.md` -> `§3 theory`).
- Phase status is derived from disk (same rules as before):
  - draft ✅ if the stage doc / section .md has its structure block + real prose, and every hole is FILLED or OWNED (each `\cite{TOADD}` / `{VAL:?` carries a `[Q-<Stage>-<n>]` id); 🕳️ N if N holes are unowned
  - probe ✅ if every entry serving this stage has a resolving `**target**` and a non-empty `### a-executor`; 📨 N if N are still open (`planned` / `commissioned` / `answered`-but-unharvested); -- if the stage raised no questions
  - revise ✅ if prose revised (tex synced from the .md)
  - check ✅ if _LOG has a check entry
- Every stage reads the same four glyphs. `probe` is ONE track: the phase strip never splits it.

DPRC phase automation:
- DRAFT, PROBE, REVISE are automatic (🤖) -- agent runs without stopping for human input
- TWO human gates (🧑): DRAFT ends at a STOP for structure review, and CHECK presents its report for user review; the user's verb advances a gate, never the agent
- When user says "work on §N", run DPR automatically, then present the CHECK report

Only show the FOCAL stage/section, not a grid of all sections. The user sees one clear focus point, not a spreadsheet.

## Current State

| Field | Value |
|---|---|
| Current layer | ... |
| Next layer | ... |
| Maturity | ... |
| Active round | <vYYMMDD or none> |

## Stable

- ...

## Open Needs

| Need | Type | Source | Suggested route |
|---|---|---|---|
| ... | probe/display/discovery/task/paper-edit | ... | ... |

## Loopback Diagnosis

- ... (omit if none)

## Recommended Next

1. `/haipipe-paper-lifecycle ...`
2. ...

## Artifacts Read

- ...

(return-contract tail here)

stage:   seed 🔥  resource ✅  claims ✅  venue ✅  pitch ✅  narrative ✅  display ✅  →  section-edit 🚀  →  review ⬜
phase:   draft 🔥  │  probe ⬜  │  revise ⬜  │  check 🚀
```

The two-line focus strip is the VERY LAST thing, placed after the return-contract tail.
It appears at the top of the dashboard AND as the last two lines of every reply.
Keep the dashboard concise.
The goal is to orient the session, not to rewrite the paper.
Full marker convention in the haipipe-paper umbrella SKILL.md, Closing Block section.

## Free-form Routing

After the dashboard, route follow-up input through the lifecycle using the command map in `../../1-lifecycle/ref/04-lifecycle-map.md`:

```text
seed                       -> /haipipe-paper seed         (stage key: seed)
resource / prereq /        -> /haipipe-paper resource      (stage key: resource)
  do we have the data /
  does the checkpoint exist
claims / ledger            -> /haipipe-paper claims        (stage key: claims)
venue / journal            -> /haipipe-paper venue         (stage key: venue)
pitch / story / sell       -> /haipipe-paper pitch         (stage key: pitch)
narrative / arc            -> /haipipe-paper narrative     (stage key: narrative)
display / figure / table   -> /haipipe-paper display       (stage key: display)
section / edit / §N        -> /haipipe-paper section-edit  (stage key: section-edit)
check §N                   -> /haipipe-paper-check
round / todo               -> round skills
rebuttal / respond         -> rebuttal skills
```

If the input does not name a stage, route to the current frontier from the dashboard.
If the input is ambiguous, ask before acting.

## Copilot Policy

Default mode is copilot.
The console may automatically read files, summarize the frontier, classify input, draft or revise a stage `.tex`, plan section work, and suggest routes.

It must ask before:

```text
calling costly task/PHI/full-data work
committing a claim verdict or downgrading a claim
editing prose across many sections at once
compiling-to-submit or packaging a submission
opening or closing a revision round destructively
landing a settled claim status in 0-lifecycle/1b-claims/1b-claims.md
```

## Session State

Record the console session at the paper/project root (the nearest directory containing the paper folder), not necessarily the repo root:

```text
.paper-console.yaml
```

Suggested fields:

```yaml
paper_root: <path>
active_paper: <Paper-Name>
current_layer: <frontier stage>
maturity: <maturity rung>
active_round: <vYYMMDD or none>
open_needs: <count>
updated: <YYMMDD>
```

This is session state, not manuscript content.
A fresh session re-derives it from disk.

## Return Contract

Every reply from a paper specialist (and every enter dashboard) MUST end with the closing block defined in `../../haipipe-paper/SKILL.md` (Closing Block section, the single source of truth).
Omitting it is a protocol violation.
Shape:

```text
── 📄 paper · seed 🔥 ─────────────────────────
status:  ok · seed
next:    <single recommended command>
──────────────────────────────────────────────
stage:   seed 🔥  resource ✅  claims ✅  venue ✅  pitch ✅  narrative ✅  display ✅  →  section-edit 🚀  →  review ⬜
phase:   draft 🔥🚀  │  probe ⬜  │  revise ⬜  │  check ⬜
```

`status` merges the state and the active stage on one line: `ok` (dashboard rendered, session ready) · `blocked` (missing paper root or unresolvable state) · `failed` (read error or inconsistent disk state).
NO `paper_root` or `current_layer` lines in the tail -- the header rule and the stage line already carry them.
Render the stage line with `../../haipipe-paper/stage-strip.sh`; the closing block is the very last thing in every reply.
