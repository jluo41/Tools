# Which skills earn their own Paper skill page first?
state: ✅ SETTLED · the rule still picks correctly; five of its six pages retired with their skills on 260806
owner: JL
method: follow the actual Paper control flow first; create a page only for a skill with an independent contract to inspect

## Opening
Which paper skills should receive first-class Q-Skill pages before the Board tries to inventory the whole family?

The paper folder contains many skills, but a one-page-per-folder catalog would be noise. The first pages should follow the actual control flow from a user request to a revised sentence: select the paper, keep the Board current, resolve the stage contract, write Board-renderable Markdown, connect open questions to the evidence bank, and make the evidence, paragraph, and sentence academically sound. Each of those steps has its own rules, failure modes, and readers.

Six skills carried those six steps when this page was ruled. Since 260805 one skill carries them all, so the same rule now admits one paper page instead of six.

Scope: This page covers The first skill-page cohort for a Board-first paper lifecycle and venue-grounded scientific prose, and the criterion for adding another page. Neighbouring pages cover Board interaction belongs to the Boardform board's own pages under `../BoardSkillBoard-260722/_archive/`; venue packs remain knowledge sources rather than callable skills. How a ruling becomes shipped text had a face of its own until 260727, when JL retired the three governance faces (graduation, versioning, per-skill status) into `_archive/`; the graduation rule itself still lives in `haipipe-board`'s own manual, which is where it was always stated.

## Diagram
```
LIVE · one registered skill, one mirror page

paper request
     ▼
haipipe-paper 0.7.0                   the only registered paper skill · intent + paper root
     │ resolves haipipe-paper/stages/index.yml
     ▼
paper/S01-opening … S10-round         stage DATA · stage.md contract + craft + checker
     │ hands the S page over
     ▼
haipipe-page 0.21.0             TYPE x PHASE · CREATE / WORK ON / RUN
     ├── DRAFT                        stage Markdown · sentence apparatus
     ├── PROBE ──────────────────────▶ probe/haipipe-probe
     │                                  QA-probe to QA-bank; the stake never crosses
     ├── REVISE                       evidence → paragraph → sentence
     └── CHECK                        judge one version, route the next authority

RETIRED 260805-260806 · skills to paper/_old/, pages to _archive/QCskill-retired-260806/

  -enter · -lifecycle · -stage        routers, now internal steps of the one door
  -draft · -revise · -check           phase hubs, now board/page-phases/ contracts
  -probe                              worker, now the PROBE phase plus the probe layer

haipipe-board 0.124.x                 shared Board apparatus; owned by Boardform
paper/venue/ playbooks                style sources, not callable skills
```

## Content
### The selection rule
A skill earns a dedicated page when a fresh agent must make a different kind of decision there: select the paper, keep Board state current, resolve a stage contract, write a Board-renderable draft, route evidence, or revise language. Reusable Board mechanisms and passive venue knowledge sources are linked from the relevant page instead of copied into this group.

### The first six pages, and where each one is now
- **1. `haipipe-paper` → `Skill-0`**
  The main entrance. Its page records intent and paper-root resolution, dispatch ownership, and the refusal to guess a venue or bypass a stage.
  Live: `7-QCskill-engine-skill/Skill-0-haipipe-paper/Skill-0-haipipe-paper.md`, mirroring `../../paper/haipipe-paper/` at 0.7.0.
- **2. `haipipe-paper-lifecycle` → `Skill-1`**
  The structural lifecycle router. Its page recorded the venue boundary, mandatory Board rebuild, and marker-report handoff after every S-page write.
  Retired 260806: page in `_archive/QCskill-retired-260806/`, skill in `../../paper/_old/haipipe-paper-lifecycle/`.
- **3. `haipipe-paper-stage` → `Skill-2`**
  The stage executor. Its page recorded one-contract loading, Board identity, explicit `requires`/`style-from`, declared phases, gates, and spend ceiling.
  Retired 260806: page in `_archive/QCskill-retired-260806/`, skill in `../../paper/_old/haipipe-paper-stage/`.
- **4. `haipipe-paper-draft` → `Skill-3`**
  The Markdown author. Its page recorded Content plus Q-consumer ownership, one-sentence apparatus, and the exact handoff boundary to PROBE. Citation and value holes carry a Q id; a missing display unit becomes a Display Request rather than a generic Q-consumer.
  Retired 260806: page in `_archive/QCskill-retired-260806/`, skill in `../../paper/_old/phase-hubs/haipipe-paper-draft/`.
- **5. `haipipe-paper-probe` → `Skill-4`**
  The evidence bridge. Its page recorded the five-step path from Q-consumer to QA file and back, plus the wall between the paper's judgment and the executor's evidence.
  Retired 260806: page in `_archive/QCskill-retired-260806/`, skill in `../../paper/_old/workers/haipipe-paper-probe/`.
- **6. `haipipe-paper-revise` → `Skill-5`**
  The academic revision hub. Its page recorded direct versus candidate-diff modes and three layers of revision: evidence bindings; paragraph logic, warrant, and sequence; and sentence-level venue register, SciWrite clarity, and anti-AI voice.
  Retired 260806: page in `_archive/QCskill-retired-260806/`, skill in `../../paper/_old/phase-hubs/haipipe-paper-revise/`.

### What the rule admits after the one-door collapse
The rule outlived its own cohort. A skill earns a page when a fresh agent must make a decision there that no other skill may make, and on 260805-260806 five of these six stopped making any decision of their own.
Their decisions did not vanish. Stage resolution and the lifecycle became internal steps of the one door; DRAFT, PROBE, REVISE, and CHECK became the four contracts under `../../board/page-phases/`; the per-stage rules became data in `stage.md`. None of those is a skill, so none of them takes a page.
One paper page remains, `Skill-0`, and the next one is due only when the paper family registers a second skill.

### What does not get a new page yet
`haipipe-sentence` 0.3.1 owns the sentence apparatus, including `~~deleted~~` and `**added**` rendering, and `haipipe-board` 0.124.x renders it; both are mirrored on the Boardform board's own pages, not here. The MISQ and UTD-IS venue files under `../../paper/venue/playbook-utd-is/` are style sources, not executable skills; a page links to them rather than duplicating them. `check`, `check-evidence`, and the REVISE child workers never earned a page of their own, and on 260805-260806 they were retired into `../../paper/_old/` without ever getting one.

## Aims
- [x] 🗺️ Identify the first cohort
      Six skills followed the real route from a user request to evidence-aware scientific revision: entry, lifecycle, stage, draft, probe, revise. One of the six is still a registered skill.
- [x] 📄 Create the main-entry page
      `Skill-0` covers paper-root and intent resolution and route boundaries, and is the one page of this cohort still live.
- [x] 📄 Create the lifecycle and stage pages
      `Skill-1` and `Skill-2` separated Board refresh from contract, phase, and gate control; both moved to `_archive/QCskill-retired-260806/` when their skills folded into the one door.
- [x] 📄 Create the DRAFT and PROBE pages
      `Skill-3` and `Skill-4` exposed the Q-consumer-to-QA path without letting a writer run bank work; both moved to `_archive/QCskill-retired-260806/` when DRAFT and PROBE became phase contracts.
- [x] 📄 Create the REVISE page
      `Skill-5` brought evidence integrity, paragraph logic, SciWrite, and candidate diffs under one revision contract; it moved to `_archive/QCskill-retired-260806/` with the REVISE phase.

## States
The cohort was rendered as six named skill pages and stands at one, `Skill-0`. It followed the Paper control path and treated Board rendering and evidence routing as first-class parts of writing, rather than adding a generic style tool after drafting. Every page that left did so because its skill left, so the criterion itself was never the thing that failed.

- 260727 GPT-5 · JL reordered the cohort around the real control path: `haipipe-paper` → lifecycle → stage → draft → probe → revise. REVISE now owns the three writing layers in the map rather than splitting its child workers into premature top-level pages.
- 260727 GPT-5.6 Terra · Generated and authored all six named `Q-Skill-…` pages. The DRAFT page now distinguishes Q-consumers from Display Requests; the REVISE page makes candidate-diff mode a non-destructive review artifact.

## Files
- `../../paper/haipipe-paper/`
  The one door at 0.7.0: intent, paper root, stage resolution from `stages/index.yml`, page handoff.
- `../../paper/S01-opening/` through `../../paper/S10-round/`
  Stage data: one `stage.md` contract per stage, plus craft files, templates, and checker scripts.
- `../../board/haipipe-page/`
  The page engine at 0.21.0, which now runs what four of the retired skills used to run.
- `../../board/page-phases/`
  DRAFT, PROBE, REVISE, and CHECK as contracts rather than skills.
- `../../paper/_old/`
  Every retired paper skill, kept readable: the three routers, the phase hubs, and the workers.
- `_archive/QCskill-retired-260806/`
  `Skill-1` through `Skill-5`, the five mirror pages this ruling produced and 260806 retired.

## Law

- Follow the Paper control flow when selecting Q-Skill pages. Create one when the skill owns a decision that another skill may not make, and link shared mechanisms and passive knowledge sources to their existing owners.

## Log
- 260806 2223 · [REVISE-CC] swept to the 260806 architecture; the six-page cohort now reads as one live page plus five retired ones, with the diagram, Files paths, and the sentence-apparatus owner corrected.
260727 · Audited against `board.md`'s decision-only rule. This page needed no judgement at all: all five items were already ticked and it still read 🟡, which is exactly `check.py`'s `partial-with-nothing-open` shape. Flipped with no ruling made.
260727 · Created from the anti-AI scientific-prose session. The first cohort initially began at stage; JL corrected it to the full control path from the main Paper entry through lifecycle, stage, draft, probe, and revise.
