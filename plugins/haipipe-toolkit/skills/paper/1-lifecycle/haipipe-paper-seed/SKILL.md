---
name: haipipe-paper-seed
description: "Create or update the paper folder's 0-lifecycle/0-seed/0-seed.tex: the earliest stage contract that keeps a paper possibility alive before evidence is mature. States why the paper might exist, current evidence status, open evidence needs (routed to probe/discover/task/insight), a promotion gate, and kill criteria. Use for paper seed, prospectus, why this paper, project seed, kill criteria, 0-seed."
argument-hint: "[paper-dir] [--source <path-or-note>...]"
allowed-tools: Bash, Read, Write, Edit, Grep, Glob
metadata:
  version: "1.1.0"
  last_updated: "2026-06-22"
  summary: "Maintain 0-lifecycle/0-seed/0-seed.tex as the paper-possibility contract."
  changelog:
    - "1.1.0 (2026-06-22): added illuminate+gate+compile protocol (ref/stage-gate.md, ref/stage-illuminate.md, ref/tex-quality.md)"
    - "1.0.0 (2026-06-22): baseline."
---

Skill: haipipe-paper-seed
===================================

Maintain the **seed** stage of a concrete paper folder. This is the first
stage of the lifecycle spine and the contract at `prospectus` maturity.

It answers one question:

```text
Why might this paper exist?
```

The seed is not a pitch, claim ledger, or outline. It keeps a paper-shaped
possibility alive while the evidence is still forming, and it states the
conditions under which the paper is promoted or dropped.

Read first: `../../PHILOSOPHY.md`, `../../ref/lifecycle-map.md`.

Shared Protocols
----------------

This stage follows three shared protocols. Read them once:

- `ref/stage-illuminate.md` -- illuminate + elicit taste before drafting
- `ref/stage-gate.md` -- exit criteria + confirm-before-advance gate
- `ref/tex-quality.md` -- self-contained compilable tex with Pn.Sm tags

Location
--------

```text
<paper>/0-lifecycle/0-seed/0-seed.tex   standalone-compilable stage contract
```

The file is TeX-first and should compile on its own (the standalone preamble
comes from the scaffold). This skill owns its body.

Principles
----------

1. A seed may be intuition. It does not require evidence yet.
2. The seed must name what evidence would make the paper worth pursuing, and
   what would kill it.
3. Open evidence needs route out to project workers; the seed never fakes them.
4. Do not create `0-sections/`, displays, or compile obligations from the seed.
   Those start at manuscript maturity.

Workflow
--------

### Step 0: Illuminate + Elicit

Before drafting, follow `ref/stage-illuminate.md`:

- Present the current state of this stage (what exists on disk, what could change).
- Identify 2-3 taste-bearing decisions for this stage.
- Ask the user for their take. Wait for input before proceeding.
- For a re-walk: surface what is ALREADY there and ask "keep / change / reframe?" per element.

### Step 1: Resolve paper folder

Accept the paper root or any path inside it. Find the root by looking upward for
`0-lifecycle/`, a `0-*.tex` master, or `1-compile.sh`. If none exists, ask the
user to run `/haipipe-paper-lifecycle folder <paper-root>`.

### Step 2: Ensure `0-lifecycle/0-seed/0-seed.tex` exists

Copy the canonical template and fill it. The template is the single source of
truth for section order and the standalone preamble:

```text
ref/seed-template.tex
```

Body section structure (fixed order; inside the standalone document):

```latex
\section*{Seed Question}
The one paper-shaped question this seed exists to answer.

\section*{Motivations}
Why this is interesting (puzzle / gap / surprise), what makes the angle novel
or feasible now, and to whom it is interesting (name the audiences and why each
cares).

\section*{Tentative Claim Shape}
What the paper may eventually argue, phrased as a hypothesis, not a finding.

\section*{Current Evidence Status}
Task/probe/discovery/insight state. Say plainly when this is not yet a paper seed.

\section*{Open Evidence Needs}
What to get next, each with a route: probe / discover / task / insight.

\section*{Promotion Gate}
Concrete conditions for promoting to an active paper seed (then to pitch).

\section*{Kill Criteria}
What evidence would make this paper not worth pursuing.
```

Do not add a "Parent Project" section; the parent project is recorded in
`STATUS.md`, not the seed.

### Step 3: Route open needs

For each open evidence need, emit a delivery need using
`../../ref/delivery-need.md` and suggest the route:

```text
claim needs a verdict/robustness check   -> /haipipe-probe open <need>
claim needs outside context/citation     -> /haipipe-discovery <question>
needs a run or data artifact             -> /haipipe-task <contract>
finished evidence needs reusable K/W     -> /haipipe-insight <artifact>
```

Do not run that work here. Record the need and hand off.

### Step 4: Compile + Exit Gate

1. Compile the stage PDF per `ref/tex-quality.md` (pdflatex twice, clean aux).
2. Present the exit criteria from `ref/stage-gate.md` with per-item check/fail.
3. Ask: "Stage seed looks ready -- confirm to close and move to pitch?"
4. Only on user confirm: update `STATUS.md` `current_layer` and Gate Ledger.

### Step 5: Handoff

Report current seed state and the next command:

```text
promote     -> /haipipe-paper pitch <paper-dir>
get evidence-> /haipipe-probe | /haipipe-discovery | /haipipe-task
drop        -> archive the seed and stop
```

Update `STATUS.md` (`current_layer`, `maturity: prospectus`).

End the reply with the stage strip (run `ref/stage-strip.sh`).
