---
name: haipipe-paper-enter
description: "Open the Paper Console for a paper repo. Use for `/haipipe-paper`, `/haipipe-paper enter <paper-path>`, `/haipipe-paper status [paper-path]`, or when starting work in an existing paper folder. Derives current state from disk (not stored status), renders an open-needs dashboard with the lifecycle frontier, maturity, stable assets, claim/display/round gaps, loopback diagnosis, and next commands, records session state in .paper-console.yaml, and routes free-form follow-up input through the lifecycle in copilot mode."
argument-hint: "[paper-path] [free-form input]"
allowed-tools: Bash, Read, Grep, Glob, Write, Skill
metadata:
  version: "3.0.0"
  last_updated: "2026-07-02"
  summary: "Paper Console: derive-from-disk dashboard + lifecycle router."
  changelog:
    - "3.0.0 (2026-07-02): lifecycle reorder (seed -> claims -> venue -> pitch -> narrative -> display -> section-edit); claims is stage 1 (venue-free), pitch is stage 2 (venue-aligned); minimap removed; section-edit replaces write/edit with per-section DGPC status grid (DRAFT/GATHER/POLISH auto, CHECK human); updated file paths, stage strip, diagnosis rules, free-form routing, and dashboard format."
    - "2.1.0 (2026-06-22): dashboard leads with pitch summary + stage strip before operational details; read order prioritizes 1-pitch.tex; return contract enforces structured tail + failed status; stale-deliverable flag from ref/tex-quality.md."
    - "2.0.0 (2026-06-22): reframed as the Paper Console; added derive-from-disk frontier, free-form routing, copilot policy, and .paper-console.yaml session state."
    - "1.2.0 (2026-06-21): open-needs paper session loader."
---

# haipipe-paper-enter (Paper Console)

Open a concrete paper folder as the **Paper Console**: a context-aware working session for one active paper. It mirrors the Probe Console.

The console:

```text
1. resolves the paper root
2. derives current state from disk, not from stored status
3. renders a dashboard panel (lifecycle frontier + maturity + open needs)
4. records session state in .paper-console.yaml at the paper root
5. routes later free-form user input through the lifecycle
```

The main job is to expose the paper's current debt board: open claim gaps, display/table gaps, section-edit phase gaps, round todo gaps, and evidence needs that may require probe/discover/task/insight work. The user often does not know the next stage in advance; the dashboard makes the next need visible.

Follow-up paper actions in the same session must treat that dashboard, especially `current_layer`, `next_layer`, and open needs/gates, as the working context. A fresh Claude/Codex session should run `enter` again.

Story ownership rule: this paper owns its own story, claim wording, narrative, displays, and section editing. Shared evidence lives in project-level probes, discoveries, tasks, and insights. Do not look for or require a project-level narrative layer.

Read first:

```text
../../PHILOSOPHY.md
../../ref/lifecycle-map.md
../../ref/paper-dashboard.md
```

Then, when the task touches lifecycle shape or rounds:

```text
../../ref/paper-lifecycle.md
../../ref/paper-rounds.md
../../ref/paper-skill-structure.md
```

When creating or interpreting explicit need records, use:

```text
../../ref/delivery-need.md
```

## Input

Accept either:

```text
<paper-root>
```

or any path inside a paper root. If no path is supplied, use the current directory.

## Resolve Paper Root

Look upward from the supplied path until one of these signatures is found:

- `STATUS.md`
- `0-lifecycle/`
- `0-*.tex` and `0-sections/`
- `1-compile.sh` and `0-sections/`

If no paper root is found, report `status: blocked` and suggest:

```text
/haipipe-paper prospectus "<paper-path>"
/haipipe-paper-lifecycle folder "<paper-path>"
```

## Read Order

Read only files that exist, in this order:

1. `STATUS.md`
2. `0-lifecycle/README.md`
2b. `0-lifecycle/2-pitch/2-pitch.tex` (or `.md`) -- HIGH PRIORITY for dashboard header. Extract the `\section*{One-Minute Pitch}` paragraph and the `\section*{Hook}` paragraph. These become the 2-3 sentence "what this paper is about" summary at the top of the dashboard. If the file does not exist or lacks these sections, the dashboard says "pitch not yet written".
3. Stage TeX/MD files (remaining):
   - `0-lifecycle/0-seed/0-seed.tex`
   - `0-lifecycle/1-claims/1-claims.tex` (or `.md`)
   - `0-lifecycle/3-narrative/3-narrative.tex`
   - `0-lifecycle/4-display/4-display.tex`
4. Section-edit outlines: scan `0-lifecycle/5-section-edit/` for per-section outline `.md` files, `_CITATION_*`, `_VALUES_*`, and `_LOG*` files. Derive per-section DGPC status from what exists on disk.
5. Explicit need records in lifecycle TeX comments or markdown tables. Search for `NEED`, `GAP`, `TODO`, `blocked`, `missing`, and `open`.
6. `0-displays/README.md`
7. `0-displays/*/README.md`
8. `0-sections/README.md`
9. `0-sections/*.tex` names and short headers/comments only; do not read full long sections unless needed to diagnose section-edit drift.
10. `1-rounds/latest.md`, then the referenced round README, `discussion.md`, `decisions.md`, `todo.md`, and `applied.md` if they exist.
11. Git state:
   - `git status --short --branch`
   - `git log --oneline --max-count=3`

## Diagnosis Rules

Derive the current layer from disk, following `../../ref/paper-dashboard.md`. Read `STATUS.md` only as a hint: a stage is done only when its `.tex` or `.md` resolves on disk with real content (not the scaffold stub). The frontier is the first stage whose disk predicate fails. If `STATUS.md` claims more progress than disk shows, flag DRIFT and trust disk.

Per-stage inference when disk is the source of truth:

| Evidence | Current layer |
|---|---|
| only `README.md` / prospectus lifecycle | `0-seed` |
| seed exists but claims are absent/thin | `0-seed -> 1-claims` |
| claims exist but venue is not pinned in STATUS.md | `1-claims -> venue` |
| venue pinned but pitch is absent/thin | `venue -> 2-pitch` |
| pitch exists but narrative is absent/thin | `2-pitch -> 3-narrative` |
| narrative exists but display units are missing | `3-narrative -> 4-display` |
| display plan exists but display units/canonical PDFs are missing | `4-display` |
| display units exist and placed | ready for `5-section-edit` |

Infer maturity separately from current layer:

| Evidence | Maturity |
|---|---|
| seed only | `prospectus` |
| seed + claims | `claim-ledger` |
| lifecycle + sections + compile script | `scaffold` |
| display map exists | `display-map` |
| section-edit outlines with DGPC in progress | `section-edit` |
| section prose compiles | `draft` |
| checks/audits mostly pass | `submission-candidate` |
| active round after external/coauthor review | `revision` |

Need diagnosis is separate from lifecycle layer. Extract open needs from:

| Surface | Typical need |
|---|---|
| `1-claims` GAP/weak/unsupported rows | probe, discovery, task, insight |
| `4-display` missing display units | display or task |
| `5-section-edit` sections with incomplete DGPC phases | section-edit work |
| section comments/TODOs | paper edit or evidence need |
| round `todo.md` unresolved items | paper edit, probe, display, citation |

Classify each open item using the delivery-need interface:

```text
probe | discovery | task | display | insight | paper-edit
```

Loopback diagnosis follows the paper lifecycle:

| Symptom | Return to |
|---|---|
| wording, citation, format, stale number | section-edit cycle |
| figure/table unclear or lacks source/caption/preview | `4-display` |
| unsupported or too-strong claim | `1-claims` / `3-narrative` |
| story not compelling or abstract/intro disagree | `2-pitch` |
| paper no longer viable | `0-seed` |

## Output Format

The dashboard leads with WHAT THE PAPER IS ABOUT, then WHERE IT STANDS, then WHAT TO DO NEXT. Operational details come after orientation.

Render the stage strip deterministically with the helper, never hand-typed:

```sh
sh "$CLAUDE_SKILL_DIR/../../ref/stage-strip.sh" <paper-root>
```

It prints one line driven by `STATUS.md current_layer`, e.g. `seed ✅  claims ✅  venue ✅  pitch ✅  narrative ✅  display ⏳  section-edit ⏳`. This strip appears twice: once near the top (orientation) and once as the VERY LAST LINE of the reply (closing every reply in the session, not just the first dashboard; see the orchestrator's "Stage Strip" rule).

The enter skill reads `ref/tex-quality.md` and flags any stage whose `.tex` is newer than its `.pdf` as a stale deliverable in the Open Needs section.

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
and the \section*{Hook} paragraph of 0-lifecycle/2-pitch/2-pitch.tex.
If no pitch exists, print: "Pitch not yet written -- run /haipipe-paper pitch.">

## Focus Strip (two lines)

The strip shows the FOCAL point: which stage, and which phase within that stage. Always two lines, always at the top of the dashboard and as the last two lines of every reply.

**Line 1 (stage):** all lifecycle stages with the focal one marked 🚀. If the focal stage is section-edit, append the specific section name in parentheses.

**Line 2 (phase):** the DGPC phase status within the focal stage.

Examples:

```
stage:   seed ✅  claims ✅  venue ✅  pitch ✅  narrative ✅  display ✅  section-edit (§1 introduction) 🚀
phase:   draft ✅  │  cite 🔍5  val --  disp --  │  polish ⬜  │  check ⬜
```

```
stage:   seed ✅  claims ✅  venue ✅  pitch 🚀  narrative ⬜  display ⬜  section-edit ⬜
phase:   draft ✅  │  cite ⬜  val --  disp --  │  polish 🚀  │  check ⬜
```

```
stage:   seed ✅  claims ✅  venue ✅  pitch ✅  narrative ✅  display ✅  section-edit (§3 theory) 🚀
phase:   draft 🚀  │  cite ⬜  val --  disp --  │  polish ⬜  │  check ⬜
```

How to derive:
- The focal stage is the lifecycle frontier (first stage not ✅). If the user specifies a section ("work on §3"), the focal becomes that section.
- The section name comes from the outline file name (e.g., `1-introduction.md` → `§1 introduction`, `3-theory.md` → `§3 theory`).
- Phase status is derived from disk (same rules as before):
  - draft ✅ if outline .md has structure block + draft sentences
  - cite ✅ if _CITATION_ all placed and density >= venue norm; 🚀 if in progress; 🔍 N if N candidates unverified
  - val ✅ if _VALUES_ all verified; -- if skipped (section has no numbers)
  - disp ✅ if all displays linked; -- if skipped (section has no displays)
  - polish ✅ if prose polished (tex synced from outline)
  - check ✅ if _LOG has a check entry
- For non-section-edit stages (seed, claims, pitch, etc.), phase status is derived from the stage's artifact spec done-criteria.

DGPC phase automation:
- DRAFT, GATHER, POLISH are automatic (🤖) -- agent runs without stopping for human input
- CHECK is the only human-involved phase (🧑) -- present a CHECK report for user review
- When user says "work on §N", run DGP automatically, then present the CHECK report

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
| ... | probe/display/discovery/task/insight/paper-edit | ... | ... |

## Loopback Diagnosis

- ... (omit if none)

## Recommended Next

1. `/haipipe-paper-lifecycle ...`
2. ...

## Artifacts Read

- ...

(return-contract tail here)

stage:   seed ✅  claims ✅  venue ✅  pitch ✅  narrative ✅  display ✅  section-edit (§1 introduction) 🚀
phase:   draft ✅  │  cite 🔍5  val --  disp --  │  polish ⬜  │  check ⬜
```

The two-line focus strip is the VERY LAST thing, placed after the return-contract tail. It appears at the top of the dashboard AND as the last two lines of every reply. Keep the dashboard concise. The goal is to orient the session, not to rewrite the paper.

## Free-form Routing

After the dashboard, route follow-up input through the lifecycle using the command map in `../../ref/lifecycle-map.md`:

```text
seed                       -> /haipipe-paper seed         (haipipe-paper-seed)
claims / ledger            -> /haipipe-paper claims        (haipipe-paper-claims)
venue / journal            -> /haipipe-paper venue         (haipipe-paper-venue)
pitch / story / sell       -> /haipipe-paper pitch         (haipipe-paper-pitch)
narrative / arc            -> /haipipe-paper narrative     (haipipe-paper-narrative)
display / figure / table   -> /haipipe-paper display       (haipipe-paper-display)
section / edit / §N        -> /haipipe-paper section-edit  (haipipe-paper-section-edit)
check §N                   -> /haipipe-paper-section-edit-checker
round / todo               -> round skills
rebuttal / respond         -> rebuttal skills
```

If the input does not name a stage, route to the current frontier from the dashboard. If the input is ambiguous, ask before acting.

## Copilot Policy

Default mode is copilot. The console may automatically read files, summarize the frontier, classify input, draft or revise a stage `.tex`, plan section work, and suggest routes.

It must ask before:

```text
calling costly task/PHI/full-data work
committing a claim verdict or downgrading a claim
editing prose across many sections at once
compiling-to-submit or packaging a submission
opening or closing a revision round destructively
filing insight memory as accepted knowledge
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

This is session state, not manuscript content. A fresh session re-derives it from disk.

## Return Contract

Every reply from a paper specialist (and every enter dashboard) MUST end with the structured tail block followed by the stage strip as the very last line. This is enforced by the orchestrator; omitting it is a protocol violation.

```text
status:        ok | blocked | failed
paper_root:    <path>
current_layer: <layer>
next:          <suggested command>

stage:   seed ✅  claims ✅  venue ✅  pitch ✅  narrative ✅  display ✅  section-edit (§1 introduction) 🚀
phase:   draft ✅  │  cite 🔍5  val --  disp --  │  polish ⬜  │  check ⬜
```

The `status` field uses three values: `ok` (dashboard rendered, session ready), `blocked` (missing paper root or unresolvable state), `failed` (read error or inconsistent disk state). The two-line focus strip is the very last thing in every reply. The section name in parentheses comes from the outline file name on disk.
