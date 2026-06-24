---
name: haipipe-paper-narrative
description: "Generate 0-lifecycle/3-narrative/3-narrative.tex, the design contract for /haipipe-paper: a one-page evidence-tracked story that mirrors the paper's real sections (Introduction, Methods, Results, Discussion), with every beat carrying a readiness tag ([READY]/[PENDING]/[INFER]/[LIT]/[GAP]) and a small-font interrogation comment. Reads upstream research artifacts (IDEA_REPORT, AUTO_REVIEW, CLAIMS_FROM_RESULTS, experiment results, repo source). Use when transitioning from research/experiment phase to writing phase, or when the user says 'write narrative report', '生成 narrative', '/haipipe-paper-narrative'."
argument-hint: "[project-dir-or-topic]"
allowed-tools: Bash(*), Read, Write, Edit, Grep, Glob
metadata:
  version: "1.5.0"
  last_updated: "2026-06-24"
  summary: "Generate 0-lifecycle/3-narrative/3-narrative.tex, the section-mirrored, readiness-tagged design contract for /haipipe-paper."
  changelog:
    - "1.5.0 (2026-06-24): added the \\fb{name}{status}{feedback}{resolution} macro for EXTERNAL reviewer comments threaded per beat (post + comments model; maroon, distinct from internal gray \\rev), with a slim footer line for no-beat comments; added the short-plain-sentence rule for all comment text (\\rev, \\fb resolutions, footer); both wired into ref/narrative-template.tex"
    - "1.4.0 (2026-06-23): output is now 0-lifecycle/3-narrative/3-narrative.tex (section-mirrored: Intro/Methods/Results/Discussion, each beat readiness-tagged + interrogation comment), retiring the markdown NARRATIVE_REPORT.md form; extracted ref/narrative-template.tex carrying the readiness legend + comment vocabulary; points to the ProjB exemplar"
    - "v1.3.1: added mandatory compile-after-edit rule; venue awareness note"
    - "1.3.0 (2026-06-22): added per-beat subagent interrogation protocol (keep/move/demote/cut + small-font comments)"
    - "1.2.0 (2026-06-22): added illuminate+gate+compile protocol (ref/stage-gate.md, ref/stage-illuminate.md, ref/tex-quality.md)"
    - "1.1.0 (2026-06-05): renamed from narrative-report to haipipe-paper-narrative (haipipe-paper-* name unification)."
    - "1.0.0 (2026-05-31): baseline metadata added."
---

# Narrative Report Generator

The narrative report is **not** a draft of the paper. It is the **design contract**
that the paper writes from. Every claim, figure, and citation in the final PDF
should trace back to a line in this file. If something is not in the narrative,
the downstream pipeline (`/haipipe-paper-minimap → /haipipe-paper-display-figure → /haipipe-paper-edit-write`) will not
invent it.

If the paper folder has `0-lifecycle/1-pitch/1-pitch.tex`, read it before composing the
narrative. The pitch is the one-minute public-facing story for this concrete
paper; this narrative expands it into evidence-backed claims, figures, and
limitations. If the evidence forces a different pitch, update
`0-lifecycle/1-pitch/1-pitch.tex` through `/haipipe-paper-lifecycle pitch` and log the
shift instead of silently diverging.

## Shared Protocols

This stage follows three shared protocols. Read them once:

- `ref/stage-illuminate.md` -- illuminate + elicit taste before drafting
- `ref/stage-gate.md` -- exit criteria + confirm-before-advance gate
- `ref/tex-quality.md` -- self-contained compilable tex with Pn.Sm tags

## Context: $ARGUMENTS

## When to Use

- Research / experiment phase is essentially done — results are in, story is
  approximately settled
- Before invoking `/haipipe-paper` or `/haipipe-paper-minimap` (they consume this file)
- After `/auto-review-loop` finishes, as the handoff to writing
- When the project has accumulated `IDEA_REPORT.md`, `AUTO_REVIEW.md`,
  experiment logs, and figures but no single document tells the story

Do **not** use when:
- Experiments are still running (the narrative would be premature)
- You only have a vague topic — use `/idea-discovery` or `/haipipe-probe judge` first
- A current `0-lifecycle/3-narrative/3-narrative.tex` already exists; edit it directly and recompile

## Inputs (in priority order)

The skill discovers whichever of these exist in the project tree:

0. **`0-lifecycle/1-pitch/1-pitch.tex`** (paper folder, if present) — current
   one-minute paper story. Use it as the reader-facing framing constraint, not
   as evidence.
1. **`CLAIMS_FROM_RESULTS.md`** (best) — validated claim ↔ evidence map from
   `/haipipe-probe judge`. If present, use as the spine of the narrative; every
   listed claim becomes a section in the report.
2. **`IDEA_REPORT.md`** — chosen idea, hypothesis, novelty justification (from
   `/idea-discovery`). Supplies the problem statement and intended contribution.
3. **`review-stage/AUTO_REVIEW.md`** (fall back to `./AUTO_REVIEW.md`) — review
   history, weaknesses fixed, remaining limitations (from `/auto-review-loop`).
   Supplies the limitations section and reframings.
4. **Experiment results** — JSON / CSV / TSV under `figures/`, `results/`,
   `outputs/`, `probes/`. These are the raw evidence for every quantitative
   claim. Each number that ends up in the narrative must trace back to one of
   these files.
5. **`EXPERIMENT_LOG.md` / `probe-log.txt`** — comparison-first experiment
   ledger. Useful for cross-probe deltas and baseline-vs-method tables.
6. **Repo source** — for the method summary (what was actually built; not
   what was originally proposed). One short paragraph, not a code dump.

If multiple inputs disagree (e.g. `IDEA_REPORT` says "X improves Y by 5%" but
`CLAIMS_FROM_RESULTS` says "no improvement on test-od"), **trust the latest /
most data-grounded source** (CLAIMS_FROM_RESULTS > experiment files >
AUTO_REVIEW > IDEA_REPORT) and surface the discrepancy as a note in the report.

## Output: `0-lifecycle/3-narrative/3-narrative.tex`

The narrative is a self-contained LaTeX file that compiles to `3-narrative.pdf` (one page for a conference paper, a few for a journal). It is NOT markdown and NOT a `NARRATIVE_REPORT.md`; that older markdown form is retired. Scaffold from `ref/narrative-template.tex` and fill the placeholders. A filled, real-world exemplar to read first: `examples/ProjB-PhyTrait-OpioidRx/paper/Paper-Personality-Opioid-MedJournal/0-lifecycle/3-narrative/3-narrative.tex`.

The file mirrors the paper's REAL sections, in reading order, and has five structural parts:

1. **Readiness legend (top).** Five color-coded tags, defined once via the macros in the template, applied to every beat:
   - `[READY]` (green): evidence in hand (a confirmed probe or a run we trust).
   - `[PENDING]` (orange): data exists but a render/check/probe is still open.
   - `[INFER]` (purple): an inference, grounded in the evidence, reaching one reasoned step beyond, never measured (no probe will confirm it).
   - `[LIT]` (blue): rests on outside literature, citation-audit pending.
   - `[GAP]` (red): no evidence yet, needs a probe.

   The tag is not decoration: `[PENDING]` and `[GAP]` beats ARE the open evidence needs, and they route to `/haipipe-probe`.

2. **Spine (throughline).** One paragraph, an arrow chain, the whole paper in one breath: problem, the move this paper makes, the core finding, the so-what. Every beat below must serve this line.

3. **One block per paper section** (Introduction, Methods, Results, Discussion, in reading order), each with:
   - a `\section*` heading plus a plain-language subtitle (for example "what is known, the gap, and the bet");
   - a **Flow:** line, the section's own arrow chain;
   - a **grounded prose paragraph**, draft-quality and in plain language, written one sentence per `%% ---- Pn.Sm ----` tag. This paragraph is the literal opener the manuscript grows from.
   - a **Key points to cover** enumerate, where each beat is `[TAG] **Label:** one to three sentences`.

4. **Per-beat comments.** Every beat carries a small-font (`\rev`) interrogation comment of the form `verb · role` then one sharp sentence on why the beat is here or what breaks without it. Verbs: `keep · add · demoted · cut · added by author`. Roles: `stakes · validity · contribution · guardrail · safety · defense · mechanism · grounded opener · no-blame anchor · so-what` (extend as the venue needs). These are authored by the interrogation subagent, not self-authored (see below). When an EXTERNAL named reviewer comments on the paper, their comment is threaded onto the same beat with a small-font (`\fb`) line (`name · status · verbatim feedback · short resolution`); see "External Reviewer Comments" below. All comment text uses short plain sentences (one idea each); the `\fb` quoted feedback stays verbatim.

5. **Footer ledger.** Small-font lines: **Reviewer-flagged gaps** (each known reviewer concern and which section beat now threads it, or marked Remaining and routed to a probe), **Arc** (one line: what each section lands on after demotions/parks/folds, and how the spine's peak claim is defended), **Awaiting review** (beats authored since the last interrogation pass that still need a verdict), and, when an external review has been threaded, an **External review (`<name>, <date>`)** line that points to the `\fb` comments above and carries any comment with no home beat (e.g. "see Overleaf") plus the source file path.

This form absorbs the old markdown buckets: the claim-evidence matrix becomes the readiness-tagged beats; the figure/table inventory becomes Methods/Results beats (a Table 1 beat, a STROBE-flow beat); limitations become Discussion beats; the pitch alignment stays a constraint read from `0-lifecycle/1-pitch/1-pitch.tex`, not a printed section.

Per-Beat Interrogation (subagent review)
-----------------------------------------

After drafting the narrative, EACH beat/item in every section is interrogated
by an independent subagent. The drafting agent does NOT self-author inclusion
justifications (self-authored "why it's here" comes out limp and circular).

Protocol:
  1. Dispatch ONE reviewer subagent that sees ALL beats so it can also judge
     flow, redundancy, and gaps.
  2. The reviewer returns, per item: verdict (keep | move-to-section |
     demote-to-Supplement | cut) + one sharp venue-aware comment.
  3. The drafting agent integrates the returned comments in SMALL FONT
     (\footnotesize) attached to each beat, visibly subordinate to the beat.
  4. Recompile the stage PDF after integrating comments.

The reviewer subagent JUDGES; the drafting agent INTEGRATES. Builder != judge.

External Reviewer Comments (`\fb`, threaded per beat)
-----------------------------------------------------

`\rev` is the INTERNAL interrogation pass (above). `\fb` is for an EXTERNAL named
reviewer: a co-author, advisor, or referee who comments on the paper. When such a
review arrives, thread each comment onto the beat it concerns (post + comments
model), not into one summary footer paragraph. This makes a review pass trackable
at the point where the change must happen, and lets the narrative double as a
progress tracker.

Macro (in `ref/narrative-template.tex`, maroon so it reads apart from gray `\rev`):

```latex
\fb{reviewer name}{status}{their feedback, verbatim}{how we addressed it}
```

- **name** — the reviewer (e.g. `Ritu`).
- **status** — `done` | `part` | `open`, judged against THIS narrative contract
  (not the manuscript prose): `done` = the comment's substance is in the narrative
  arc/beats; `part` = the arc handles it but a manuscript reflow or an open
  decision is still pending; `open` = not yet addressed.
- **feedback** — their words, VERBATIM. Do not paraphrase, compress, or translate.
  Exception: escape LaTeX specials (`% & _ $ # { }`) so the file still compiles;
  escaping for compilation does NOT count as altering the words.
- **resolution** — OUR words, in SHORT PLAIN sentences (see the comment-style rule
  below). One idea each.

Placement and ordering: a comment that maps to a beat threads onto that beat. When
a beat carries both, order is beat text → `\rev` (internal) → `\fb` (external).
A comment with no single home beat (e.g. "see comments in Overleaf") stays in the
footer ledger, on the `External review (<name>, <date>)` line, with the source
file path.

Multiple reviewers: give EACH reviewer its own footer `External review (<name>,
<date>)` line; on the beats, both reviewers' `\fb` lines simply coexist (each
carries its own name). Keep the footer label exactly `External review (...)` so it
is not confused with the internal `Reviewer-flagged gaps` line.

## Workflow

### Step 0: Illuminate + Elicit

Before drafting, follow `ref/stage-illuminate.md`:

- Present the current state of this stage (what exists on disk, what could change).
- Identify 2-3 taste-bearing decisions for this stage.
- Ask the user for their take. Wait for input before proceeding.
- For a re-walk: surface what is ALREADY there and ask "keep / change / reframe?" per element.

### Step 1: Discover inputs

```bash
ls 0-lifecycle/1-pitch/1-pitch.tex CLAIMS_FROM_RESULTS.md IDEA_REPORT.md review-stage/AUTO_REVIEW.md AUTO_REVIEW.md EXPERIMENT_LOG.md probe-log.txt 2>/dev/null
find results outputs experiments figures -maxdepth 3 -type f \
    \( -name '*.json' -o -name '*.csv' -o -name '*.tsv' -o -name '*.jsonl' \) 2>/dev/null | head -50
```

Report what was found vs missing. If `CLAIMS_FROM_RESULTS.md` is missing,
suggest running `/haipipe-probe judge` first — the narrative is significantly
stronger when claims are pre-validated.

### Step 2: Build the claim ↔ evidence map

- If `CLAIMS_FROM_RESULTS.md` exists, use its claims as the spine.
- Otherwise, extract claims from `IDEA_REPORT.md` + `AUTO_REVIEW.md`, then map
  each to result files. Flag any claim with no matching result file.

For each claim, pin:
- one or more raw-result file paths
- the specific number(s) that support the claim
- the baseline being compared against

### Step 3: Inventory figures

Scan `figures/` for existing PDFs / PNGs / SVGs.
For each section in the plan, decide:
- already exists → `exists`
- can be auto-generated from a result file → `auto` (note the script if any)
- needs hand drawing (architecture, qualitative concept, schematic) → `manual`

### Step 4: Write `3-narrative.tex`

Scaffold from `ref/narrative-template.tex` (copy it to `0-lifecycle/3-narrative/3-narrative.tex`), then fill every `<...>` placeholder using the five-part structure above. Keep it tight: one page for a conference paper, a few for a journal. Density beats length: every beat should name a claim, an evidence file, or context the reader needs for the next beat. Tag every beat with its readiness ([READY]/[PENDING]/[INFER]/[LIT]/[GAP]); leave no beat untagged.

After writing, run the per-beat interrogation protocol (see above). Do not advance to the exit gate until interrogation comments are integrated and the PDF is recompiled.

### Step 5: Compile + Exit Gate

1. Compile the stage PDF per `ref/tex-quality.md` (pdflatex twice, clean aux).
2. Present the exit criteria from `ref/stage-gate.md` with per-item check/fail.
3. `3-narrative.pdf` recompiled and current (a stale PDF is a defect; recompile after every edit without being asked).
4. Ask: "Stage narrative looks ready -- confirm to close and move to minimap?"
5. Only on user confirm: update `STATUS.md` `current_layer` and Gate Ledger.

### Step 6: Handoff

Print the suggested next command:

```
3-narrative.tex written and compiled to 3-narrative.pdf.

Next stage:
    /haipipe-paper-minimap        (paragraph jobs + evidence anchors)

To revise:
    edit 0-lifecycle/3-narrative/3-narrative.tex directly, recompile, then re-run downstream stages
```

End the reply with the stage strip (run `ref/stage-strip.sh`).

## Composing with other workflows

```
Upstream                          This skill                  Downstream
────────                          ──────────                  ──────────
/idea-discovery   ──► IDEA_REPORT ─┐
                                   ├──► /haipipe-paper-narrative  ──► 3-narrative.tex     ──► /haipipe-paper
implement + experiments            │                                                       │
                                   │                                                       ├──► /haipipe-paper-minimap
/auto-review-loop ──► AUTO_REVIEW ─┤                                                       ├──► /haipipe-paper-display-figure
                                   │                                                       ├──► /haipipe-paper-edit-write
/haipipe-probe judge  ──► CLAIMS_…    ─┘                                                       ├──► /paper-compile
                                                                                           └──► /haipipe-paper-edit-improve-loop
```

Also invoked as Stage 5 of `/research-pipeline`. Standalone is fine when you
already have the upstream artifacts and only need the narrative.

## Rules

- **Claim ↔ evidence is non-negotiable.** Every quantitative line in the
  narrative must have a traceable file path. Numbers without sources will
  fail `/haipipe-paper-edit-claim-audit` later anyway, so catch them here.
- **Every beat carries a readiness tag.** No beat is untagged. `[PENDING]` and
  `[GAP]` beats are the paper's live evidence worklist: surface them and route
  them to `/haipipe-probe`; never quietly upgrade a beat to `[READY]` without
  the evidence in hand.
- **Do not invent claims the data doesn't support.** If `CLAIMS_FROM_RESULTS`
  says partial, do not round up to "yes" in the narrative.
- **Honest limitations save the paper.** Round-2 reviewers (human or auto)
  punish overclaiming far harder than they punish modest claims.
- **The narrative is editable.** Treat the first generation as a draft —
  expect a human pass before `/haipipe-paper` consumes it.
- **One narrative per paper**, not per probe. Multi-probe projects
  collapse into one story or split into separate papers; don't try to fit two
  stories into one narrative.
- **Venue-aware arc.** Read STATUS `venue` and consult
  `_venue/playbook-<venue>` for what the venue rewards in terms of narrative
  arc and argument structure. The venue playbook shapes which beats are
  expanded (theory-forward for MISQ, clinical-impact-forward for JAMA) and
  which are condensed.
- **Comment text is short and plain.** All comment text (`\rev` interrogation,
  `\fb` resolutions, footer ledger lines) uses short declarative sentences, one
  idea each. No run-on lines chained by semicolons, no stacked parentheticals;
  compress rather than nest, split rather than join. In `\footnotesize` a long
  compound line is unreadable, and the comment thread exists to scan at a glance.
  Same readability discipline as the pitch. (Reviewer feedback quoted in `\fb` #3
  stays verbatim; only OUR resolution prose follows this rule.)
- **External reviewer comments thread per beat (`\fb`).** When a named reviewer
  comments on the paper, attach each comment to the beat it concerns via `\fb`
  (name · status · verbatim feedback · short resolution); do not collapse them
  into one footer paragraph. `\rev` = internal interrogation; `\fb` = external
  named reviewer. A comment with no home beat stays in the footer.
