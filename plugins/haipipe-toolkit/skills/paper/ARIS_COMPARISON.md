# HAI-Pipe Paper Skill vs ARIS Workflow

This document compares the HAI-Pipe paper skill mental model with the ARIS
research workflow in `references/aris`.

Short version:

> ARIS is an autonomous research workflow: idea, experiment, review, paper,
> rebuttal, resubmit, talk.
>
> HAI-Pipe paper is a manuscript-state system: pitch, narrative, architecture,
> plan, draft, edit, review, respond, present, with explicit loopback to the
> earliest broken layer.

They are compatible, but they organize the work differently.

## One-minute comparison

| Question | ARIS answer | HAI-Pipe paper answer |
|----------|-------------|-----------------------|
| What is the system optimizing? | Autonomous research progress and cross-model audit | Reliable paper story evolution |
| Main unit | Workflow stage | Paper folder state |
| Main motion | W1 -> W1.5 -> W2 -> W3 -> W4/W5/W6 | Seed -> pitch -> narrative -> architecture -> plan -> draft -> edit -> review, with loopbacks |
| Story state | Mostly `NARRATIVE_REPORT.md`, `PAPER_PLAN.md`, review logs | First-class `0-pitch/`, then narrative, architecture, plan |
| Evidence state | Experiment logs, research wiki, claim audits | HAI-Pipe discoveries/tasks/probes/insights feeding paper narrative |
| Review model | Cross-model adversarial reviewer is central | Review gate routes the paper back to pitch/narrative/plan/edit |
| File philosophy | Stage outputs + latest/timestamped artifacts | Concrete manuscript folder with current story plus provenance |
| Failure handling | Resume stage, rerun loop, reviewer gate | Diagnose earliest broken layer and loop back there |

## ARIS mental model

ARIS presents the research lifecycle as six major workflows:

```
W1   Idea Discovery
W1.5 Experiment Bridge
W2   Auto Review Loop
W3   Paper Writing
W4   Rebuttal
W5   Resubmit
W6   Conference Talk
```

Its most important design commitments are:

- **Autonomy:** the system can run overnight and keep moving through idea,
  experiment, review, and writing stages.
- **Cross-model review:** executor and reviewer should be different model
  families; the reviewer reads artifacts cold in fresh threads.
- **Stage artifacts:** each stage emits durable files such as
  `IDEA_REPORT.md`, `EXPERIMENT_PLAN.md`, `EXPERIMENT_LOG.md`,
  `NARRATIVE_REPORT.md`, `PAPER_PLAN.md`, `REVIEW_STATE.json`, and audit
  reports.
- **Submission assurance:** paper readiness is not the executor's self-judgment;
  it is gated by audits such as experiment audit, claim audit, citation audit,
  and kill-argument.
- **Recovery:** long runs persist state so a crashed or compacted session can
  resume.

In plain language: ARIS asks, "How do we get from a research direction to a
better paper with less human orchestration?"

## HAI-Pipe paper mental model

HAI-Pipe paper skill treats a paper as a concrete manuscript whose story evolves
as evidence accumulates.

The current lifecycle is:

```
0. Seed
1. Paper Folder
2. Paper Pitch
3. Evidence-Backed Narrative
4. Architecture / Minimap
5. Paper Plan
6. Build Skeleton
7. Write Draft
8. Edit Cycle
9. Review Gate
10. Submit
11. Respond / Revise
12. Present
```

Its most important design commitments are:

- **Paper pitch is first-class:** `0-pitch/PAPER_PITCH.md` stores the current
  one-minute story. It should be understandable to a random reader in about one
  minute.
- **Story shifts have provenance:** `0-pitch/PITCH_LOG.md` and
  `0-pitch/archive/` preserve why the story changed.
- **Evidence constrains narrative:** the paper can start from intuition, but
  later claim/story changes should be tied to discoveries, tasks, probes,
  insights, reviews, or author decisions.
- **Paper files represent layers:** pitch, narrative, architecture, plan, draft,
  and review each own different kinds of failure.
- **Loopback is diagnostic:** a review finding should return to the earliest
  broken layer, not merely the most recent stage.

In plain language: HAI-Pipe asks, "How do we keep the paper's public story
readable, honest, and traceable as the evidence changes?"

## Workflow-to-workflow comparison

This is the most direct comparison between the two systems.

ARIS workflow:

```
research direction
  -> W1 idea discovery
  -> W1.5 experiment bridge
  -> W2 auto review loop
  -> W3 paper writing
  -> W4 rebuttal
  -> W5 resubmit
  -> W6 talk
```

HAI-Pipe paper workflow:

```
seed / upstream research signal
  -> paper folder
  -> paper pitch
  -> evidence-backed narrative
  -> architecture / minimap
  -> paper plan
  -> skeleton
  -> draft
  -> edit cycle
  -> review gate
  -> submit
  -> respond / revise
  -> present
```

The difference is not just naming. ARIS's workflow is designed around
**autonomous forward motion**. HAI-Pipe paper workflow is designed around
**state correction and story reliability**.

| Workflow property | ARIS | HAI-Pipe paper |
|-------------------|------|----------------|
| Entry point | Broad research direction | A concrete paper seed or manuscript folder |
| Main question | "What should the agent do next?" | "Which paper layer is currently true or broken?" |
| Default movement | Move forward through W stages | Move forward, but loop back whenever a lower layer breaks |
| Paper writing starts from | `NARRATIVE_REPORT.md` | `0-pitch/` plus narrative, architecture, and plan |
| Review output means | Fix weaknesses and rerun | Diagnose route: edit, plan, architecture, narrative, pitch, or upstream evidence |
| Experiments live in | Workflow stages and logs | Outside paper, then imported as evidence |
| Story evolution lives in | Narrative/review artifacts, implicitly | `0-pitch/PAPER_PITCH.md`, `PITCH_LOG.md`, archive, narrative |
| Human readability target | Final reports/paper artifacts | The pitch should be readable in one minute at all times |

### Key workflow difference

ARIS treats paper writing as Workflow 3:

```
/paper-plan -> /paper-figure -> /paper-write -> /paper-compile -> /auto-paper-improvement-loop
```

HAI-Pipe splits that same area into more explicit manuscript layers:

```
paper pitch
  -> evidence narrative
  -> architecture / minimap
  -> paper plan
  -> display contract
  -> write / edit
  -> review gate
```

So the equivalent of ARIS Workflow 3 is not one HAI-Pipe stage. It is the whole
paper-folder convergence loop.

### Why HAI-Pipe should not simply copy ARIS Workflow 3

ARIS Workflow 3 assumes the hard work of story formation has mostly already
happened in `NARRATIVE_REPORT.md`.

For our paper skill, that assumption is too coarse. We want to know:

- what the current one-minute pitch is,
- when the pitch changed,
- which evidence caused the change,
- whether the paper architecture still matches the pitch,
- whether the section plan still fits the evidence,
- whether figures/tables are ready as story-evidence display objects,
- whether review findings are prose problems or story problems.

That is why HAI-Pipe needs `0-pitch/` before `NARRATIVE_REPORT.md` and before
`PAPER_PLAN.md`.

### Workflow loopback difference

ARIS loopback mostly means:

```
review -> fix -> rerun / recompile -> review again
```

HAI-Pipe loopback means:

```
review finding
  -> identify earliest broken layer
  -> update that layer
  -> regenerate downstream artifacts only as needed
```

Examples:

| Review finding | ARIS-like response | HAI-Pipe response |
|----------------|-------------------|-------------------|
| "The intro is unclear" | Rewrite intro | Check pitch first; if pitch is unclear, update `0-pitch/`, then intro |
| "Claim is too strong" | Soften text or add support | Update narrative claim/evidence contract, then plan/edit |
| "Need more ablation" | Run experiment or add limitation | Create upstream task/probe; after result, update narrative and maybe pitch |
| "Paper lacks contribution focus" | Rewrite abstract/intro | Reopen pitch and architecture |
| "Result table is confusing" | Fix table/caption | Usually edit/plan only, unless it changes evidence interpretation |

This is the practical distinction: ARIS is very good at improving artifacts;
HAI-Pipe should be very good at preserving why the artifact changed.

## Stage mapping

ARIS and HAI-Pipe can be mapped, but they do not have one-to-one stages.

| ARIS stage | Closest HAI-Pipe layer | Notes |
|------------|------------------------|-------|
| W1 Idea Discovery | Outside paper -> Seed / Pitch / Narrative | ARIS generates candidate ideas and pilots; HAI-Pipe would store resulting shifts in `0-pitch/` and `NARRATIVE_REPORT.md`. |
| W1.5 Experiment Bridge | Outside paper -> tasks/probes -> Narrative | ARIS implements and runs experiments; HAI-Pipe treats experiment output as evidence entering the paper through narrative. |
| W2 Auto Review Loop | Review Gate plus outside research loop | ARIS loops research, experiments, and paper fixes; HAI-Pipe would route each finding to edit, plan, narrative, pitch, or upstream tasks/probes. |
| W3 Paper Writing | Pitch -> Narrative -> Architecture -> Plan -> Draft/Edit | ARIS compresses paper production into a pipeline; HAI-Pipe splits the paper state into more explicit layers. |
| W4 Rebuttal | Respond / Revise | Similar purpose. HAI-Pipe emphasizes that rebuttal can reopen pitch, narrative, plan, or edit. |
| W5 Resubmit | Submit / Respond / Architecture | ARIS has strong hard constraints for resubmission; HAI-Pipe should keep this as a venue/architecture-level transformation. |
| W6 Conference Talk | Present | Similar endpoint. HAI-Pipe should read the pitch first, because talks/posters need the one-minute story. |

## File-state mapping

| ARIS artifact | HAI-Pipe equivalent | Design implication |
|---------------|---------------------|--------------------|
| `IDEA_REPORT.md` | Seed notes, upstream `discoveries/`, paper pitch seed | Do not copy the whole brainstorm into the paper folder unless it affects this paper's pitch. |
| `IDEA_CANDIDATES.md` | Project-level possibilities, not paper-local | Candidate pools belong upstream of a concrete paper. |
| `EXPERIMENT_PLAN.md` | `tasks/`, `probes/`, or paper plan only if it directly affects manuscript evidence | Keep experiment execution outside paper; import only evidence and claims. |
| `EXPERIMENT_LOG.md` | task/probe logs feeding narrative | Paper should cite evidence summaries, not become an experiment run log. |
| `NARRATIVE_REPORT.md` | `NARRATIVE_REPORT.md` | Strong overlap. HAI-Pipe should preserve it as the claim/evidence/limitation contract. |
| `PAPER_PLAN.md` | `PAPER_PLAN.md` | Strong overlap. In HAI-Pipe, plan is downstream of pitch and architecture. |
| `figures/`, `latex_includes.tex` | `0-display/DISPLAY_INDEX.md`, per-item `DISPLAY.md`, `float.tex`, `preview.pdf` | HAI-Pipe should treat figures/tables as display contracts, not only generated assets. |
| `AUTO_REVIEW.md` / `REVIEW_STATE.json` | review reports, edit logs, `1-feedback/` | HAI-Pipe should route review findings by layer rather than treating them all as edit tasks. |
| audit JSON/MD files | Review Gate artifacts | Compatible. HAI-Pipe can adopt the verdict discipline without adopting ARIS's whole folder layout. |
| `research-wiki/` | HAI-Pipe project KB / discoveries / insights | Similar role, but HAI-Pipe's story path is more explicit: discovery/task/probe -> insight -> narrative/pitch. |

## What is the same

Both systems agree on these principles:

- Research writing is not a single pass.
- Evidence matters more than fluent prose.
- Review should not be self-acquittal.
- Long workflows need durable files because chat context is unstable.
- Rebuttal and resubmission are lifecycle stages, not one-off editing chores.
- The system should preserve enough trace to explain why a claim, story, or
  revision exists.

## What is different

### 1. Workflow-first vs state-first

ARIS is workflow-first. It says: run W1, then W1.5, then W2, then W3.

HAI-Pipe paper is state-first. It says: at any moment, know which layer of the
paper is broken:

```
pitch -> narrative -> architecture -> plan -> draft -> edit -> review
```

This matters because papers rarely fail only at the current stage. A bad
paragraph may be a prose problem, but it may also reveal a broken claim, weak
evidence, or wrong pitch.

### 2. ARIS has strong automation; HAI-Pipe has stronger story provenance

ARIS is very strong at autonomous operation:

- run experiments,
- review code,
- improve paper,
- resume after crashes,
- audit submission readiness.

HAI-Pipe should borrow this discipline, especially around reviewer independence
and audit gates.

HAI-Pipe is stronger at representing the story trajectory:

- current pitch,
- pitch archive,
- pitch log,
- evidence-backed narrative,
- architecture/minimap,
- plan,
- display contract.

This is the part ARIS does not make explicit enough for our use case.

### 3. ARIS paper plan is earlier than HAI-Pipe paper plan

In ARIS, `/paper-plan` is the main bridge from narrative/results to paper
outline.

In HAI-Pipe, `PAPER_PLAN.md` should not be the first paper thinking artifact.
It should come after:

```
0-pitch/PAPER_PITCH.md
NARRATIVE_REPORT.md
vNN-architecture-minimap.md
```

The reason is practical: before section planning, the paper needs a one-minute
story and a paper-shaped strategy.

### 4. ARIS review loops are mostly improvement loops; HAI-Pipe review is a router

ARIS review loops tend to ask:

> What is weak, and how do we fix it?

HAI-Pipe review gate should ask first:

> Which layer is actually broken?

Then:

| Finding | HAI-Pipe route |
|---------|----------------|
| local wording/citation/number | Edit |
| paragraph has no job | Plan |
| section order or contribution emphasis wrong | Architecture |
| claim not supported | Narrative, then upstream evidence work |
| public story unclear | Pitch |
| whole direction no longer viable | Seed / new paper |

This keeps the system from patching prose when the real failure is story or
evidence.

## What HAI-Pipe should borrow from ARIS

1. **Reviewer independence.** Reviewers should read the current artifact cold.
   Do not tell them "we fixed X"; the files should show it.
2. **Assurance levels.** Draft mode and submission mode should behave
   differently. Submission mode needs blocking audits.
3. **Verdict schemas.** Use explicit states such as `PASS`, `WARN`, `FAIL`,
   `BLOCKED`, `ERROR`, `NOT_APPLICABLE`.
4. **Resumable long runs.** Edit/review/rebuttal loops should persist state.
5. **Edit whitelists for constrained phases.** Resubmit and camera-ready modes
   should constrain what files and operations may change.
6. **Generated views are not canonical.** Markdown/TeX/source files stay
   canonical; rendered PDFs/HTML/slides are views.

## What HAI-Pipe should not copy directly

1. **Do not make the paper folder a project-wide research cockpit.** Upstream
   idea pools, experiment queues, and broad literature maps should remain at the
   project level.
2. **Do not collapse pitch into narrative.** A one-minute pitch is a distinct
   artifact from an evidence-backed narrative report.
3. **Do not treat `PAPER_PLAN.md` as the first planning file.** It should be
   downstream of pitch, narrative, and architecture.
4. **Do not route every reviewer criticism into editing.** Some criticisms
   require upstream evidence work or story reframing.
5. **Do not treat display generation as display readiness.** A plot or table is
   not ready until it has a claim, evidence source, caption, label, input block,
   and preview.
6. **Do not overbuild bureaucracy.** The pitch layer should remain readable in
   one minute.

## Suggested integration model

Use ARIS as an upstream engine and audit discipline. Use HAI-Pipe as the paper
state model.

```
ARIS-like research work
  idea discovery
  experiment bridge
  auto review
  research wiki / logs
        |
        v
HAI-Pipe paper folder
  0-pitch/PAPER_PITCH.md
  0-pitch/PITCH_LOG.md
  NARRATIVE_REPORT.md
  vNN-architecture-minimap.md
  PAPER_PLAN.md
  0-display/DISPLAY_INDEX.md
  0-sections/*.tex
  review / feedback / rebuttal artifacts
```

When upstream research produces new evidence, update paper state in this order:

1. Does the one-minute story change? If yes, update `0-pitch/`.
2. Do claims/evidence/limitations change? If yes, update `NARRATIVE_REPORT.md`.
3. Does the paper-shaped argument change? If yes, update architecture/minimap.
4. Does section/figure/page execution change? If yes, update `PAPER_PLAN.md`.
5. Do display jobs, captions, labels, sources, or preview status change? If yes,
   update `0-display/DISPLAY_INDEX.md` and the relevant display item folders.
6. Then edit the TeX.

## Bottom line

ARIS is a strong reference for autonomous execution and adversarial audit.

HAI-Pipe paper should keep its own center of gravity:

> a paper is the evolving, evidence-constrained public story of a concrete
> manuscript.

The key addition HAI-Pipe makes over ARIS is the explicit story trajectory:

```
seed intuition
  -> current one-minute pitch
  -> evidence-backed narrative
  -> paper architecture
  -> execution plan
  -> draft
  -> review-routed loopback
```

That is the part we should protect as the paper skill grows.
