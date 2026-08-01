# Which skills earn their own Paper skill page first?
state: ✅ SETTLED · cohort chosen, all six pages written, every item ticked
owner: JL
method: follow the actual Paper control flow first; create a page only for a skill with an independent contract to inspect

## Opening
Which paper skills should receive first-class Q-Skill pages before the Board tries to inventory the whole family?

The paper folder contains many skills, but a one-page-per-folder catalog would be noise. The first pages should follow the actual control flow from a user request to a revised sentence: the front door selects the paper, lifecycle keeps the Board current, stage resolves the contract, DRAFT writes Board-renderable Markdown, PROBE connects open questions to the evidence bank, and REVISE makes the evidence, paragraph, and sentence academically sound. These have distinct rules, failure modes, and readers.

Scope: This page covers The first skill-page cohort for a Board-first paper lifecycle and venue-grounded scientific prose, and the criterion for adding another page. Neighbouring pages cover Board interaction belongs to `Q-Skill@boardform`; venue packs remain knowledge sources rather than callable skills. How a ruling becomes shipped text had a face of its own until 260727, when JL retired the three governance faces (graduation, versioning, per-skill status) into `_archive/`; the graduation rule itself still lives in `haipipe-board`'s own manual, which is where it was always stated.

## Diagram
```
paper request
     ▼
haipipe-paper                         main entry · resolve intent and paper
     ▼
haipipe-paper-lifecycle               S pages · Board rebuild · paper/Board linkage
     ▼
haipipe-paper-stage                   stage contract · phase/gate dispatch
     ▼
haipipe-paper-draft                   stage Markdown · Q-template · sentence apparatus
     ▼
haipipe-paper-probe ────────────────▶ haipipe-probe
     │                                  evidence bank and QA artifacts
     ▼
haipipe-paper-revise                 evidence → paragraph → sentence
     ├── value · display · citation   preserve or place verified bindings
     ├── paragraph                    accurate argument · warrant · sequence
     └── sentence                     venue register · SciWrite · no AI voice

haipipe-board       shared Board apparatus; owned by Boardform
venue playbooks      style sources, not callable skills
```

## Content
### The selection rule
A skill earns a dedicated page when a fresh agent must make a different kind of decision there: select the paper, keep Board state current, resolve a stage contract, write a Board-renderable draft, route evidence, or revise language. Reusable Board mechanisms and passive venue knowledge sources are linked from the relevant page instead of copied into this group.

### The first six pages
- **1. `haipipe-paper` → `Skill-0`**
  The main entrance. Its page records intent and paper-root resolution, dispatch ownership, and the refusal to guess a venue or bypass a stage.
- **2. `haipipe-paper-lifecycle` → `Skill-1`**
  The structural lifecycle router. Its page records the venue boundary, mandatory Board rebuild, and marker-report handoff after every S-page write.
- **3. `haipipe-paper-stage` → `Skill-2`**
  The stage executor. Its page records one-contract loading, Board identity, explicit `requires`/`style-from`, declared phases, gates, and spend ceiling.
- **4. `haipipe-paper-draft` → `Skill-3`**
  The Markdown author. Its page records Content plus Q-consumer ownership, one-sentence apparatus, and the exact handoff boundary to PROBE. Citation/value holes carry a Q id; a missing display unit becomes a Display Request rather than a generic Q-consumer.
- **5. `haipipe-paper-probe` → `Skill-4`**
  The evidence bridge. Its page records the five-step path from Q-consumer to QA file and back, plus the wall between the paper's judgment and the executor's evidence.
- **6. `haipipe-paper-revise` → `Skill-5`**
  The academic revision hub. Its page records direct versus candidate-diff modes and three layers of revision: evidence bindings; paragraph logic, warrant, and sequence; and sentence-level venue register, SciWrite clarity, and anti-AI voice.

### What does not get a new page yet
`haipipe-board` owns sentence apparatus, including `~~deleted~~` and `**added**` rendering, on Boardform's Q-Skill pages. The MISQ and UTD-IS venue files are style sources, not executable skills; the six pages above link to them rather than duplicate them. `check`, `check-evidence`, and the REVISE child workers remain inside the REVISE page until a separate contract question emerges.

## Items to Finish
- [x] 🗺️ Identify the first cohort
      Six skills now follow the real route from a user request to evidence-aware scientific revision: entry, lifecycle, stage, draft, probe, revise.
- [x] 📄 Create the main-entry page
      `Skill-0` now covers paper-root/intent resolution and route boundaries.
- [x] 📄 Create the lifecycle and stage pages
      `Skill-1` and `Skill-2` now separate Board refresh from contract/phase/gate control.
- [x] 📄 Create the DRAFT and PROBE pages
      `Skill-3` and `Skill-4` now expose the Q-consumer-to-QA path without letting a writer run bank work.
- [x] 📄 Create the REVISE page
      `Skill-5` now brings evidence integrity, paragraph logic, SciWrite, and candidate diffs under one revision contract.

## Where we are
The first cohort is now rendered as six named skill pages. It follows the Paper control path and treats Board rendering and evidence routing as first-class parts of writing, rather than adding a generic style tool after drafting.

- 260727 GPT-5 · JL reordered the cohort around the real control path: `haipipe-paper` → lifecycle → stage → draft → probe → revise. REVISE now owns the three writing layers in the map rather than splitting its child workers into premature top-level pages.
- 260727 GPT-5.6 Terra · Generated and authored all six named `Q-Skill-…` pages. The DRAFT page now distinguishes Q-consumers from Display Requests; the REVISE page makes candidate-diff mode a non-destructive review artifact.

## Files
- `haipipe-paper/`
  Main entry and intent router.
- `haipipe-paper-lifecycle/`
  Lifecycle router and Board rebuild owner.
- `haipipe-paper-stage/`
  Stage contract and phase dispatch.
- `haipipe-paper-draft/`
  Board-renderable stage Markdown and Q-consumer author.
- `haipipe-paper-probe/`
  Paper-side bridge to `haipipe-probe`.
- `haipipe-paper-revise/`
  Evidence, paragraph, and sentence revision hub.

## Law
Follow the Paper control flow when selecting Q-Skill pages. Create one when the skill owns a decision that another skill may not make, and link shared mechanisms and passive knowledge sources to their existing owners.

## Log
260727 · Audited against `board.md`'s decision-only rule. This page needed no judgement at all: all five items were already ticked and it still read 🟡, which is exactly `check.py`'s `partial-with-nothing-open` shape. Flipped with no ruling made.
260727 · Created from the anti-AI scientific-prose session. The first cohort initially began at stage; JL corrected it to the full control path from the main Paper entry through lifecycle, stage, draft, probe, and revise.
