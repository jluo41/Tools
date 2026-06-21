# Paper Lifecycle Walkthrough

This is the story version of the paper lifecycle: how a topic becomes a paper,
how the paper talks to the project lifecycle, and what each folder/file is for.

Use this when explaining the system to someone who does not know HAI-Pipe.

## The one-sentence movie

> A project produces evidence; a paper turns selected evidence into a
> one-minute story, then into a venue-shaped manuscript, and every review finding
> loops back to the earliest layer that broke.

## Cast

Project-side characters:

- **Task**: does work and produces observations. It answers: what happened?
- **Probe**: tests a claim across controlled arms. It answers: can we believe
  this claim?
- **Insight**: archives D/I/K/W cards. It answers: what does the project know?
- **Narrative**: holds a living story line. It answers: what story might this
  evidence support?
- **Application / Ask**: opens a session to advance a question. It can trigger
  tasks, probes, and insight filing.

Paper-side characters:

- **Paper Folder**: the concrete paper repo/submodule; early folders may contain only prospectus files, while mature folders contain the manuscript scaffold.
- **Paper Pitch**: the one-minute public story for this specific paper.
- **Evidence Narrative**: the claim/evidence/limitation contract.
- **Architecture / Minimap**: the paper-shaped strategy.
- **Paper Plan**: the section, citation, figure, and page-budget execution map.
- **Display Contract**: the figure/table story-evidence layer.
- **Draft/Edit**: the LaTeX realization.
- **Review Gate**: the router that decides which earlier layer is broken.
- **Respond/Present**: external lifecycle after submission or acceptance.

## Stage 0 — Topic appears

Scene:

> The author says: "I think there is a paper about X."

At this point there may be no evidence. That is allowed.

Project-side state:

- Maybe no task exists.
- Maybe no probe exists.
- Maybe only literature notes or author intuition exist.
- Maybe a project narrative already exists.

Paper-side action:

- Do **not** write a full paper plan yet.
- Classify the topic as one of three states:
  - project seed: stay in project discovery
  - paper prospectus: create or attach an early paper repo/submodule with prospectus files
  - paper seed: enough evidence exists to promote toward pitch/narrative/plan

Question:

> Is there enough direction to start a paper prospectus container?

If no, stay in project lifecycle: use ask, discovery, task, or probe to sharpen
the topic. If yes, Stage 1 creates a concrete paper repo/submodule, but it may
start in prospectus mode only.

Done marker:

> Stage 0 is done when the decision is explicit: project-only, paper prospectus, or
> paper seed. For paper prospectus, the next action is to create
> `lifecycle/stage00_topic-appears/current.md` inside the paper repo/submodule.

## Stage 1 — Create the paper folder

Scene:

> We create the stage on which the paper will happen.

In project-backed HAI-Pipe work, a paper folder should be a Git repo attached
under the project, typically as a submodule:

```text
examples/<Project>/paper/Paper-<Slug>/
```

There are two modes.

### Prospectus mode

Use this when a paper-shaped direction exists but the claim is not yet
evidence-backed.

Files created:

```text
<paper>/
  README.md
  lifecycle/
    README.md
    stage00_topic-appears/
      current.md
      runs/
      feedback/
      assets/
    stage01_create-paper-folder/
      current.md
      runs/
      feedback/
      assets/
```

Meaning:

- `lifecycle/stage00_topic-appears/current.md` constrains discovery. It states
  the tentative question, claim shape, current evidence status, discovery
  constraints, narrative handoff, inquiry tracks, and promotion gate.
- `lifecycle/stage01_create-paper-folder/current.md` hands the prospectus to
  project narrative. Narrative then decides whether to trigger discover, probe,
  task, or insight work.
- Each `stageXX_slug/` folder acts like a durable stage branch: `current.md` is
  active state, `runs/` stores dated snapshots, `feedback/` stores comments, and
  `assets/` stores diagrams or support files.
- No LaTeX scaffold exists yet. No `0-sections/`, no compile scripts, no
  manuscript obligations.

The central rule:

> Paper repo can start early; manuscript obligations start late.

### Manuscript mode

Use this after the prospectus has been promoted to a paper seed, or when evidence
and venue are already clear.

Command shape:

```text
/haipipe-paper-structure folder <paper-root> --mode manuscript
```

Files created:

```text
<paper>/
  0-pitch/
  0-sections/
  0-display/
  1-feedback/
  1-compile.sh
  0-<paper>.tex
  0-<paper>.bib
```

Meaning:

- `0-` files are manuscript source of truth.
- `1-` files are process artifacts.
- The paper folder is not the whole project. It is one venue-facing manuscript.

Project interaction:

- The paper folder may point back to a project narrative or KB.
- It should not copy the entire project KB into the paper.

Promotion:

> A prospectus folder becomes an active paper workspace only when narrative can
> state a stable claim and point to the discovery/task/probe/insight evidence
> that supports it.

## Stage 2 — Write the seed pitch

Scene:

> Imagine stopping a random person for one minute. What would you say?

Command shape:

```text
/haipipe-paper-structure pitch <paper-dir>
```

Files changed:

```text
lifecycle/stage02_seed-pitch/
  current.md
  runs/
  feedback/
  assets/
```

In manuscript mode, the accepted pitch may also be mirrored into `0-pitch/`, but
the lifecycle branch remains the teaching and decision artifact.

Pitch answers:

- What is this paper about?
- Why should anyone care?
- What is surprising?
- So what changes if it is true?
- Why should we believe it?
- What is still fragile?
- What evidence should we get next?

Important rule:

> A seed pitch can be intuition. Later pitch shifts need sources.

Project interaction:

- If the pitch says "we believe X" but the project has no evidence, that becomes
  an upstream evidence need.
- Evidence can come from tasks, probes, discoveries, insights, literature review,
  or author decisions.

Loopback:

- If later the abstract, intro, or hero figure sells a different story, come
  back here.

## Stage 3 — Build the evidence-backed narrative

Scene:

> The one-minute story becomes an honest claim/evidence contract.

Command shape:

```text
/haipipe-paper-structure narrative <paper-dir>
```

Files changed:

```text
lifecycle/stage03_evidence-backed-narrative/
  current.md
  runs/
  feedback/
  assets/
```

Narrative answers:

- What are the core claims?
- What evidence supports each claim?
- Which claims are only partially supported?
- What limitations must stay visible?
- Which figures/tables may be needed?

Project interaction:

- Tasks produce D/I material: observations and patterns.
- Probes produce K/W material: validated claims and recommendations.
- Insights archive the material so the paper can cite it.
- If a claim needs K but only I exists, the paper must not pretend it has K.

Decision:

> Can every important claim trace to evidence?

If no, leave the paper lifecycle and go back to project work:

```text
paper narrative gap
  -> application ask
  -> task and/or probe
  -> insight cards
  -> narrative update
```

## Stage 4 — Design the paper architecture

Scene:

> We now decide how the story becomes a paper-shaped argument.

Command shape:

```text
/haipipe-paper-structure architecture <paper-dir>
```

Files changed:

```text
lifecycle/stage04_architecture-minimap/
  current.md
  runs/
  feedback/
  assets/
```

Architecture answers:

- What is the 5-act arc?
- What is the contribution emphasis?
- What belongs in main text versus appendix?
- What does each section need to accomplish?
- How does the venue change the story?

Difference from narrative:

- Narrative asks what is true enough to claim.
- Architecture asks how to tell it as a paper.

Loopback:

- If a section later feels unnecessary, or the paper lacks contribution focus,
  return here.

## Stage 5 — Write the paper plan

Scene:

> The architecture becomes an execution map.

Command shape:

```text
/haipipe-paper-structure plan <paper-dir>
```

Files changed:

```text
lifecycle/stage05_paper-plan/
  current.md
  runs/
  feedback/
  assets/
```

Plan answers:

- What sections exist?
- What does each section do?
- What figures/tables are needed?
- What citation work is needed?
- What is the page budget?
- What must go to appendix?

Difference from pitch:

- Pitch is what a random reader can repeat.
- Plan is how the authors will build the paper.

Loopback:

- If paragraphs have no job, or Results order is confusing, return here.

## Stage 5a — Create the display contract

Scene:

> The paper's figures and tables become story/evidence objects, not loose files.

Command shape:

```text
/haipipe-paper-structure display plan <paper-dir>
/haipipe-paper-structure display scaffold <paper-dir>
/haipipe-paper-structure display build <paper-dir>
/haipipe-paper-structure display audit <paper-dir>
```

Files changed:

```text
0-display/DISPLAY_INDEX.md
0-display/Figures/<fig-id>/DISPLAY.md
0-display/Figures/<fig-id>/figure.pdf
0-display/Figures/<fig-id>/float.tex
0-display/Figures/<fig-id>/preview.pdf
0-display/Tables/<tab-id>/DISPLAY.md
0-display/Tables/<tab-id>/table-body.tex
0-display/Tables/<tab-id>/float.tex
0-display/Tables/<tab-id>/preview.pdf
```

Display answers:

- What claim does this figure/table support?
- Where does the evidence come from?
- What should the reader learn in five seconds?
- Is it main text or appendix?
- Which section owns it?
- Is `float.tex` ready to input?
- Does `preview.pdf` compile?

Important rule:

> Do not bake captions into image PDFs. The clean asset is `figure.pdf`;
> the paper-ready block is `float.tex`; the review view is `preview.pdf`.

Project interaction:

- A display may come from a project `task` of type `display`.
- A table may summarize task/probe results.
- If the display needs a claim that the project has not validated, return to
  task/probe before inserting it.

Loopback:

- If a display has no claim, source, caption, label, or input path, return here.

## Stage 6 — Build or repair the skeleton

Scene:

> The folder becomes mechanically paper-shaped.

Command shape:

```text
/haipipe-paper-build-scaffold <paper-dir>
/haipipe-paper-build-check <paper-dir>
/haipipe-paper-build-restructure <paper-dir>
```

Files changed:

```text
0-sections/*.tex
0-display/
1-compile.sh
```

Skeleton answers:

- Do all section files follow naming rules?
- Are wrappers and leaves correct?
- Do `\input` paths exist?
- Does the paper compile structurally?

Loopback:

- If the paper will not compile because files are misplaced, repair skeleton
  before editing prose.

## Stage 7 — Write the draft

Scene:

> The design contract becomes LaTeX.

Command shape:

```text
/haipipe-paper-create <paper-dir>
/haipipe-paper-edit-write <paper-dir>
```

Files changed:

```text
0-sections/*.tex
0-<paper>.bib
```

Drafting rule:

> The draft should realize the pitch, narrative, architecture, plan, and display
> contract. It should not invent new claims to make prose smoother.

How displays enter:

```latex
\input{0-display/Figures/fig01-hero/float.tex}
\input{0-display/Tables/tab01-main-results/float.tex}
```

Project interaction:

- If writing exposes a missing fact, do not patch by rhetoric.
- Mark the gap and return to project lifecycle if evidence is required.

## Stage 8 — Run the edit cycle

Scene:

> The paper gets refined, but edits are routed by issue type.

Edit topics:

- content
- values/numbers
- citations
- consistency
- format
- typeset
- weaving / flow

Files changed:

```text
0-sections/*.tex
0-display/*/float.tex
0-display/*/preview.pdf
diff packages
edit comments
```

Rule:

> Local problems stay in edit. Structural problems do not.

Examples:

- Stale number: edit + values audit.
- Bad paragraph: edit.
- Paragraph has no job: return to plan.
- Figure supports the wrong claim: return to display / architecture.
- Claim unsupported: return to narrative and project evidence.
- Public story unclear: return to pitch.

## Stage 9 — Review gate

Scene:

> A skeptical reader decides where the paper is broken.

The review gate is not just another edit pass. It is a router.

Inputs:

```text
PDF
lifecycle/stage02_seed-pitch/current.md
lifecycle/stage03_evidence-backed-narrative/current.md
lifecycle/stage04_architecture-minimap/current.md
lifecycle/stage05_paper-plan/current.md
lifecycle/stage05a_display-contract/current.md
0-sections/*.tex
```

Verdict routes:

| Finding | Return to |
|---------|-----------|
| typo, clumsy sentence, stale cite | Edit |
| paragraph/section has no job | Plan |
| figure/table has no display contract | Display |
| wrong contribution emphasis | Architecture |
| claim too strong or unsupported | Narrative |
| story not understandable in one minute | Pitch |
| missing evidence | Project lifecycle: task/probe/insight |
| clean | Submit |

This is the key idea:

> Review does not ask "how do we patch this sentence?" first. It asks "which
> layer failed?"

## Stage 10 — Submit

Scene:

> The paper leaves the authoring loop and enters the venue world.

Files changed:

```text
submission bundle
final PDFs
venue checklist artifacts
```

Submission asks:

- Does it compile?
- Does it satisfy venue constraints?
- Are claims, citations, figures, tables, and supplement synchronized?
- Is anything under `1-` accidentally leaking into the submission?

After submission, the paper is temporarily frozen. The project may continue,
but the submitted artifact is a snapshot.

## Stage 11 — Respond / Revise

Scene:

> External reviewers tell us which layer they do not believe.

Files changed:

```text
1-feedback/<round>/
response letter
revision plan
revised sections
new display previews
```

Reviewer comments route like this:

| Reviewer says | Likely route |
|---------------|-------------|
| "unclear writing" | Edit |
| "missing baseline" | Project task/probe, then narrative/display/edit |
| "claim too broad" | Narrative |
| "contribution not clear" | Pitch / architecture |
| "table contradicts text" | Display / edit |
| "wrong venue framing" | Pitch / architecture |

Important:

> Rebuttal is not terminal. It can reopen the entire paper lifecycle.

## Stage 12 — Present

Scene:

> The paper is cashed out into talks, posters, slides, or demos.

Files changed:

```text
slides
poster
speaker notes
Q&A prep
```

Presentation reads:

- `lifecycle/stage02_seed-pitch/current.md` first.
- Then figures/tables from `lifecycle/stage05a_display-contract/` and
  materialized `0-display/`.
- Then the paper sections.

Why:

> Presentations reveal whether the pitch is actually understandable.

If a talk cannot explain the paper in one minute, the paper may still have a
pitch problem, even after submission.

## The project-paper handshake

The project lifecycle and paper lifecycle are not the same.

Project lifecycle:

```text
topic/question
  -> application ask
  -> task produces D/I
  -> probe validates K/W
  -> insight archives D/I/K/W
  -> narrative evolves
```

Paper lifecycle:

```text
paper seed
  -> paper pitch
  -> evidence narrative
  -> architecture
  -> plan
  -> display
  -> draft/edit
  -> review/submit/respond/present
```

They handshake at four points:

| Paper asks | Project provides |
|------------|------------------|
| Why should we believe this? | tasks, probes, insights |
| Is this claim valid? | probe claim + caveats |
| What display can show this? | display task output, result table, figure asset |
| What changed after new evidence? | insight update, narrative shift, pitch shift |

The paper should never fake project work. If a paper claim needs evidence, the
paper lifecycle pauses and asks the project lifecycle to produce or retrieve it.

## A full example in one pass

Scene:

> Topic: "Does method X reveal a robust patient trajectory signal?"

1. **Seed**: author thinks this might be a paper.
2. **Paper Folder**: create `Paper-XTrajectory-MISQ2026/`.
3. **Pitch**: "We show that patient trajectories are not noise; they contain a
   stable signal that changes decision-making."
4. **Narrative**: list claims:
   - Claim A: trajectory signal exists.
   - Claim B: it is robust across cohorts.
   - Claim C: it changes a downstream decision.
5. **Project gap**: Claim B only has one task result, no controlled probe.
6. **Project work**: run a probe with matched arms and seeds.
7. **Insight**: file K/W cards from the probe result.
8. **Narrative update**: Claim B becomes supported, with caveats.
9. **Architecture**: decide the paper arc:
   problem -> signal -> validation -> consequence -> limitations.
10. **Plan**: allocate sections and page budget.
11. **Display**:
    - Fig 1: hero trajectory schematic.
    - Fig 2: robustness plot from probe.
    - Table 1: cohort comparison.
12. **Draft**: write sections and input display `float.tex` blocks.
13. **Edit**: fix local prose, stale numbers, captions.
14. **Review gate**: reviewer says Fig 2 supports robustness but not causality.
15. **Loopback**: narrative downgrades causal language; display caption changes;
    Results prose updates.
16. **Submit**: venue-ready package.
17. **Respond**: reviewer asks for missing subgroup; project runs a task/probe;
    paper updates narrative/display/edit.
18. **Present**: slides start from the pitch and hero display.

## What each file is for

| File | Role |
|------|------|
| `lifecycle/stage02_seed-pitch/current.md` | The current one-minute public story. |
| `lifecycle/stage03_evidence-backed-narrative/current.md` | Claim/evidence/limitation contract. |
| `lifecycle/stage04_architecture-minimap/current.md` | Paper-shaped strategy and section minimap. |
| `lifecycle/stage05_paper-plan/current.md` | Execution plan for sections, figures, citations, page budget. |
| `lifecycle/stage05a_display-contract/current.md` | Figure/table contract and readiness state. |
| `lifecycle/stage05a_display-contract/displays/*.md` | One display item's claim, source, caption job, fragility. |
| `0-display/*/float.tex` | Ready-to-input LaTeX block once manuscript mode is active. |
| `0-display/*/preview.pdf` | Standalone review artifact for one display once materialized. |
| `0-sections/*.tex` | The actual paper prose. |
| `1-feedback/` | External comments, rebuttal, revision process. |

## The rule a newcomer should remember

```
Project lifecycle makes evidence reliable.
Paper lifecycle makes the story readable.
Review decides which layer needs to change.
```

If you know that, the whole system becomes legible.
