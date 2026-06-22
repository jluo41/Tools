---
name: haipipe-paper-enter
description: "Open the Paper Console for a paper repo. Use for `/haipipe-paper`, `/haipipe-paper enter <paper-path>`, `/haipipe-paper status [paper-path]`, or when starting work in an existing paper folder. Derives current state from disk (not stored status), renders an open-needs dashboard with the lifecycle frontier, maturity, stable assets, claim/display/round gaps, loopback diagnosis, and next commands, records session state in .paper-console.yaml, and routes free-form follow-up input through the lifecycle in copilot mode."
argument-hint: "[paper-path] [free-form input]"
allowed-tools: Bash, Read, Grep, Glob, Write, Skill
metadata:
  version: "2.0.0"
  last_updated: "2026-06-22"
  summary: "Paper Console: derive-from-disk dashboard + lifecycle router."
  changelog:
    - "2.0.0 (2026-06-22): reframed as the Paper Console; added derive-from-disk frontier, free-form routing, copilot policy, and .paper-console.yaml session state."
    - "1.2.0 (2026-06-21): open-needs paper session loader."
---

# haipipe-paper-enter (Paper Console)

Open a concrete paper folder as the **Paper Console**: a context-aware working
session for one active paper. It mirrors the Probe Console.

The console:

```text
1. resolves the paper root
2. derives current state from disk, not from stored status
3. renders a dashboard panel (lifecycle frontier + maturity + open needs)
4. records session state in .paper-console.yaml at the paper root
5. routes later free-form user input through the lifecycle
```

The main job is to expose the paper's current debt board: open claim gaps,
display/table gaps, paragraph-placement gaps, round todo gaps, and evidence
needs that may require probe/discover/task/insight work. The user often does
not know the next stage in advance; the dashboard makes the next need visible.

Follow-up paper actions in the same session must treat that dashboard,
especially `current_layer`, `next_layer`, and open needs/gates, as the working
context. A fresh Claude/Codex session should run `enter` again.

Story ownership rule: this paper owns its own story, claim wording, narrative,
displays, and minimap. Shared evidence lives in project-level probes,
discoveries, tasks, and insights. Do not look for or require a project-level
narrative layer.

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

or any path inside a paper root. If no path is supplied, use the current
directory.

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
3. Stage TeX files:
   - `0-lifecycle/0-seed/0-seed.tex`
   - `0-lifecycle/1-pitch/1-pitch.tex`
   - `0-lifecycle/2-claims/2-claims.tex`
   - `0-lifecycle/3-narrative/3-narrative.tex`
   - `0-lifecycle/4-display/4-display.tex`
   - `0-lifecycle/5-minimap/5-minimap.tex`
4. Explicit need records in lifecycle TeX comments or markdown tables. Search
   for `NEED`, `GAP`, `TODO`, `blocked`, `missing`, and `open`.
5. `0-displays/README.md`
6. `0-displays/*/README.md`
7. `0-sections/README.md`
8. `0-sections/*.tex` names and short headers/comments only; do not read full
   long sections unless needed to diagnose minimap drift.
9. `1-rounds/latest.md`, then the referenced round README, `discussion.md`,
   `decisions.md`, `todo.md`, and `applied.md` if they exist.
10. Git state:
   - `git status --short --branch`
   - `git log --oneline --max-count=3`

## Diagnosis Rules

Derive the current layer from disk, following `../../ref/paper-dashboard.md`.
Read `STATUS.md` only as a hint: a stage is done only when its `.tex` resolves
on disk with real content (not the scaffold stub). The frontier is the first
stage whose disk predicate fails. If `STATUS.md` claims more progress than disk
shows, flag DRIFT and trust disk.

Per-stage inference when disk is the source of truth:

| Evidence | Current layer |
|---|---|
| only `README.md` / prospectus lifecycle | `0-seed` or `1-pitch` |
| `1-pitch.tex` exists but claims are absent/thin | `1-pitch -> 2-claims` |
| claims exist but narrative is absent/thin | `2-claims -> 3-narrative` |
| narrative exists but display units are missing | `3-narrative -> 4-display` |
| display plan exists but display units/canonical PDFs are missing | `4-display` |
| display units exist but paragraph placement is missing | `5-minimap` |
| minimap exists and displays are placed | ready for section edit/build/review |

Infer maturity separately from current layer:

| Evidence | Maturity |
|---|---|
| seed/pitch only | `prospectus` |
| lifecycle + sections + compile script | `scaffold` |
| explicit claim ledger | `claim-ledger` |
| display map exists | `display-map` |
| minimap maps paragraph jobs | `section-map` |
| section prose compiles | `draft` |
| checks/audits mostly pass | `submission-candidate` |
| active round after external/coauthor review | `revision` |

Need diagnosis is separate from lifecycle layer. Extract open needs from:

| Surface | Typical need |
|---|---|
| `2-claims` GAP/weak/unsupported rows | probe, discovery, task, insight |
| `4-display` missing display units | display or task |
| `5-minimap` empty paragraph/display slots | paper minimap or display |
| section comments/TODOs | paper edit or evidence need |
| round `todo.md` unresolved items | paper edit, probe, display, citation |

Classify each open item using the delivery-need interface:

```text
probe | discovery | task | display | insight | paper-edit
```

Loopback diagnosis follows the paper lifecycle:

| Symptom | Return to |
|---|---|
| wording, citation, format, stale number | edit cycle |
| paragraph has no job | `5-minimap` |
| figure/table unclear or lacks source/caption/preview | `4-display` |
| unsupported or too-strong claim | `2-claims` / `3-narrative` |
| story not compelling or abstract/intro disagree | `1-pitch` |
| paper no longer viable | `0-seed` |

## Output Format

LEAD with the lifecycle stage strip (the first line of the reply), then the
emoji-headed sections. Render the strip deterministically with the helper, never
hand-typed:

```sh
sh "$CLAUDE_SKILL_DIR/../../ref/stage-strip.sh" <paper-root>
```

It prints one line driven by `STATUS.md current_layer`, e.g.
`seed ✅  pitch ✅  …  →  write/edit ▶️  →  review ⬜`. This strip leads EVERY reply
in the session, not just the first dashboard (see the orchestrator's "Stage Strip"
rule). Then:

```markdown
seed ✅  pitch ✅  claims ✅  narrative ✅  display ✅  minimap ✅  →  write/edit ▶️  →  review ⬜

## 📄 Paper Session

| Field | Value |
|---|---|
| Paper | ... |
| Path | ... |
| Branch | ... |
| Current layer | ... |
| Next layer | ... |
| Maturity | ... |

## ✅ Stable

- ...

## ⚠️ Open Gates

- ...

## 🧾 Open Needs

| Need | Type | Source | Suggested route |
|---|---|---|---|
| ... | probe/display/discovery/task/insight/paper-edit | ... | ... |

## 🔁 Loopback Diagnosis

- ...

## 🎯 Recommended Next

1. `/haipipe-paper-lifecycle ...`
2. ...

## 📦 Artifacts Read

- ...
```

Keep the dashboard concise. The goal is to orient the session, not to rewrite
the paper.

## Free-form Routing

After the dashboard, route follow-up input through the lifecycle using the
command map in `../../ref/lifecycle-map.md`:

```text
seed                       -> /haipipe-paper seed       (haipipe-paper-seed)
pitch / story / sell       -> /haipipe-paper pitch      (haipipe-paper-pitch)
claim / claims / ledger    -> /haipipe-paper claims     (haipipe-paper-claims)
narrative / arc            -> /haipipe-paper narrative  (haipipe-paper-narrative)
figure / table / display   -> /haipipe-paper figures    (haipipe-paper-display)
minimap / paragraph plan   -> /haipipe-paper minimap    (haipipe-paper-minimap)
write / draft / edit / polish -> write/edit skills
review / audit / gate      -> review skills
round / todo / decisions   -> round skills
rebuttal / respond         -> haipipe-paper-rebuttal
slides / poster            -> present skills
```

If the input does not name a stage, route to the current frontier from the
dashboard. If the input is ambiguous, ask before acting.

## Copilot Policy

Default mode is copilot. The console may automatically read files, summarize the
frontier, classify input, draft or revise a stage `.tex`, plan section work, and
suggest routes.

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

Record the console session at the paper/project root (the nearest directory
containing the paper folder), not necessarily the repo root:

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

This is session state, not manuscript content. A fresh session re-derives it
from disk.

## Return Contract

End with a machine-readable tail:

```text
status: ok|blocked
paper_root: <path or none>
current_layer: <layer or unknown>
next: <single recommended command>
```
