---
name: haipipe-paper-edit
description: "Orchestrator for the 4-edit cycle. Knows the catalog of edit sub-skills (content/values/citation/consistency/format/typeset) and the stage agents in agents/, and drives one edit-cycle through 5 stages: (1) format-check, (2) annotate [fan out many agents in parallel], (3) human-AI feedback, (4) improve, (5) clean. Stage 2 inserts %% {CC-<topic>-vMMDD}: findings and changes NO text; the human replies with ========> {XX vMMDD}:; stage 4 applies only accepted comments. Use to edit a whole draft, fan out annotations across many sections, or coordinate the cycle. Trigger: edit paper, review draft, fan out edit, annotate, edit cycle, /haipipe-paper-edit."
metadata:
  version: "0.2.0"
  status: active
  stage: 4-edit
  role: orchestrator
---

# haipipe-paper-edit  (orchestrator)

The umbrella for the `4-edit` cycle. It knows what every edit sub-skill checks and
which stage agent does each job, builds the work grid, and drives one edit-cycle
through five stages — **fanning out annotators in parallel** at stage 2 so a whole
draft is reviewed at once. It edits no prose itself; it dispatches and coordinates.

> User-facing recipes (how to invoke, the reply grammar, the effort dial): `../USAGE.md`.

## The catalog it dispatches

**Topics** (the *what to check* — knowledge lives in each sub-skill):

| Topic | Sub-skill | Reviews |
|-------|-----------|---------|
| ① content | `haipipe-paper-edit-content` | structure, one-point paragraphs, claims, flow |
| ② values | `haipipe-paper-edit-values` | numbers vs `0-display/` source |
| ③ citations | `haipipe-paper-edit-citation` | `\cite` resolves / real / on-claim |
| ④ consistency | `haipipe-paper-edit-consistency` | terms, notation, `\label`/`\ref` |
| ⑤ format | `haipipe-paper-edit-format` | venue style, units, abbreviations |
| ⑥ typeset | `haipipe-paper-edit-typeset` | widows, orphans, overfull boxes |

**Stage agents** (the *who does it* — in `agents/`):

| Stage | Agent | Parallel? |
|-------|-------|-----------|
| 1 format-check | `paper-edit-format-checker` | no |
| 2 annotate | `paper-edit-annotator` | **yes — fan out** |
| 4 improve | `paper-edit-improver` | no |
| 5 clean | `paper-edit-cleaner` | no |

Shared contracts every dispatch obeys: `../_shared/comment-protocol.md`,
`../_shared/sentence-format.md`, `../_shared/paragraph-indexing.md`,
`../_shared/tex-file-anatomy.md`, `../_shared/edit-cycle.md`.

> Only `haipipe-paper-edit-content` is fully written today; the other five topics are
> self-contained stubs. The orchestrator dispatches whatever is active.

## The five-stage cycle it drives

```
(1) FORMAT-CHECK  → normalize files (banners + %% ---- Pn.Sm ----)   [format-checker, sequential]
(2) ANNOTATE      → fan out annotators; draft fills with comments     [annotator ×N, PARALLEL]
(3) FEEDBACK      → human appends ========> {XX}: replies; AI assists  [human + AI, in place]
(4) IMPROVE       → apply accepted comments, one section at a time     [improver, sequential]
(5) CLEAN         → strip annotations to the clean version            [cleaner, sequential]
```

Full definition: `../_shared/edit-cycle.md`. Stages 2–4 are the comment-protocol
rounds; stages 2–5 are collaborative and scale to the effort the user wants.

### How the orchestrator runs it

0. **ASK ACTORS** — before anything else, **ask the user for their initials**
   (their reply actor id) and the pass date `vMMDD`. The tool tags its own findings
   `CC`. Never assume the user's initials. Carry these into every annotator/digest.
1. **MAP** — enumerate leaf `.tex` files × active topics into the grid; pick this
   cycle's scope (default: topic ① content, all sections).
2. **Stage 1** — run `paper-edit-format-checker` on each in-scope file
   (sequentially) so every file is one-sentence-per-line with `Pn.Sm` tags.
3. **Stage 2 (fan out)** — dispatch `paper-edit-annotator` **one per section**
   (each owns its file), or read-only annotators + single writer when topics
   overlap files. Use the Agent tool for moderate drafts; a Workflow fan-out only
   if the user opted into multi-agent orchestration. Dispatch by **reading the
   spec `../agents/paper-edit-annotator.md` and passing it as the Agent prompt** —
   works with or without the agent being a registered `subagent_type` (see
   `../WIRING.md`). Then **verify each section with `scripts/check_comment_only.sh`
   (the diff must add only `%%` comment lines)** and present a per-section digest
   of open comments.
4. **Stage 3** — hand the commented draft to the human, who appends
   `========> {XX vMMDD}:` verbs. The orchestrator waits; it never acts on an
   `OPEN` comment. AI may answer `discuss:` threads.
5. **Stage 4** — run `paper-edit-improver` per section (sequentially), applying
   `accept`/`modify`, dismissing `reject`, leaving `OPEN`/`discuss`. Re-MAP:
   a content apply re-opens that section's values + citation cells.
6. **Stage 5** — when the author asks, run `paper-edit-cleaner` at the chosen
   level to produce the clean version, then build the between-cycles tracked-changes
   PDF with `haipipe-paper-edit-diffpdf` for co-author / advisor sign-off.

## Fan-out is stage 2 only

Stage 2 is read + comment with no shared writes → safe to parallelize. Stages 1,
4, and 5 mutate files and run sequentially, one section at a time. Dispatch one
annotator per section to avoid two agents writing one file.

## Dependency order (still holds)

```
① content → ② values → ③ citations → ④ consistency → ⑤ format → ⑥ typeset
```

Annotate (stage 2) many topics/sections at once, but advance topics through
improve (stage 4) in this order across cycles — applying a content edit moves the
numbers, cites, labels, and breaks the later topics check.

## When to use which entry

| Want | Use |
|------|-----|
| Drive the whole cycle / fan out annotations across a draft | **paper-edit** (here) |
| Do one topic's review on one section by hand | the matching `paper-edit-<topic>` sub-skill |
| Run a single stage on one file | the matching agent in `agents/` |
| Heavy sentence surgery / logic rewrite | finer annotate→improve rounds in `haipipe-paper-edit` (legacy `paper-revise` archived in `_archive/`) |

## Invariants

- **Stage 2 is comment-only — no prose changes** (`_shared/comment-protocol.md`).
- **Fan out stage 2; run stages 1/4/5 sequentially.**
- **No `OPEN` comment is ever applied** — silence is not consent.
- **Stable `[id]` and `\label` keys never churn**, in any stage.
