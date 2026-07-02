---
name: haipipe-paper-pitch
description: "Create or update the paper folder's 0-lifecycle/2-pitch/2-pitch.md + _LOG_2-pitch.md: the venue-ALIGNED cover letter and one-minute story for this concrete manuscript. Absorbs the Editor's Chair Test, [primary] claim designation, and venue-specific RQ framing (migrated from claims). Archives semantic old versions in _LOG when the pitch shifts. Markdown only. Use for paper pitch, cover letter, one-minute story, hook/surprise/so-what, audience/venue fit, editor's chair, primary claim, RQ framing, story trajectory, pitch provenance."
argument-hint: "[paper-dir] [--reason <slug>] [--source <path-or-note>...]"
allowed-tools: Bash, Read, Write, Edit, Grep, Glob
metadata:
  version: "3.0.0"
  last_updated: "2026-07-01"
  changelog:
    - "3.0.0 (2026-07-01): pitch is now venue-ALIGNED = cover letter. Absorbs Editor's Chair Test, [primary] claim designation, and venue-specific RQ framing from claims. Claims is now venue-FREE (pure evidence inventory). Pitch reframes venue-neutral hypotheses (H1→RQ1) for the target editor."
    - "2.0.0 (2026-06-29): switched from .tex to .md + _LOG. PITCH_LOG.md merged into _LOG_2-pitch.md. Argument documents are markdown; only display compiles to PDF."
    - "v1.5.2: extracted template to ref/pitch-template.tex; inline replaced with reading-order summary"
    - "v1.5.1: added mandatory compile-after-edit rule; venue awareness note"
    - "1.5.0 (2026-06-22): added Title section, multi-hook candidates, template enforcement, quality gate; wired illuminate+gate+compile protocols"
    - "1.4.0 (2026-06-22): readability rules, section cues, hook catalog"
  summary: "Maintain 0-lifecycle/2-pitch/ as the venue-ALIGNED cover letter and one-minute story. Owns the Editor's Chair Test, [primary] claim designation, and venue-specific RQ framing. Carries readability rules, section cues, and a hook narrative-methods catalog (ref/pitch-readability.md)."
---

Skill: haipipe-paper-pitch
====================================

Maintain the **paper pitch** for a concrete manuscript folder (stage 2, venue-ALIGNED). The pitch is the **cover letter**: the venue-ALIGNED document that tells THIS editor why THIS paper fits THEIR journal. It can be sent to an editor as-is.

The pitch is not a paper plan, outline, or claim matrix. It is the version a person can understand in one minute:

```
What is this paper about?
What vivid question or scene pulls the reader in?
What is surprising?
So what changes if it is true?
Who reads the target venue, and why does this matter to them?
Will the editor publish this? (Editor's Chair Test)
Which claim is primary for THIS venue?
How do the hypotheses become RQs for THIS audience?
Why should we believe it?
What is still fragile?
How did the story get here?
```

## Artifact Spec

**Files produced:**
- `0-lifecycle/2-pitch/2-pitch.md` -- the cover letter (venue-ALIGNED)
- `0-lifecycle/2-pitch/_LOG_2-pitch.md` -- changelog with provenance

**Content structure (2-pitch.md):**
- Title -- <=15 words, specific, evocative
- One-Minute Pitch -- 4-6 sentences for a newcomer
- Hook -- >=2 candidate methods, one recommended lead
- Finding-Surprise -- the non-obvious turn
- Implication-So What -- what changes and who can act
- Editor's Chair Test -- venue question from playbook, one-sentence answer per primary claim
- Primary Claim + RQ Framing -- [primary] designation, H-to-RQ mapping for THIS venue
- Audience and Venue Fit -- who reads this journal, why they care
- Evidence-Why Believe -- source per claim
- Limitation-Still Fragile -- top 3 risks
- Next Evidence Move -- verb + artifact

**Done-criteria:**
- [ ] Editor's Chair Test passes (venue question answered)
- [ ] Readability rules pass (8 rules from ref/pitch-readability.md)
- [ ] [primary] claim designated for THIS venue
- [ ] RQ framing complete (H-to-RQ mapping with venue rationale)
- [ ] All labeled sections present (Title, Hook with >=2 candidates, Surprise, Implication, etc.)
- [ ] Readable in one minute

**DGPC applicability:**
- DRAFT: write the cover letter
- GATHER: consult venue pack + claims ledger for H-to-RQ mapping
- POLISH: apply readability rules, de-AI voice
- CHECK: Editor's Chair Test, template enforcement, quality gate

Illustration:
- `images/stage2-pitch-gate-image2.png` -- Stage 2 as a pitch gate: either return to narrative/project work or proceed to Stage 3 evidence-backed narrative.

Location:

```
<paper>/
└── 0-lifecycle/2-pitch/
    ├── 2-pitch.tex          current one-minute story (standalone-compilable contract)
    ├── PITCH_LOG.md         short provenance sidecar (optional)
    └── archive/             older semantic pitch snapshots (vNN_<reason>.tex)
```

Shared Protocols
-----------------

This stage follows three shared protocols. Read them once:

- `ref/stage-illuminate.md` -- illuminate + elicit taste before drafting
- `ref/stage-gate.md` -- exit criteria + confirm-before-advance gate
- `ref/tex-quality.md` -- self-contained compilable tex with Pn.Sm tags

Principles
----------

1. **One minute or it failed.** `2-pitch.tex` should be readable in one minute. Keep it short enough to fit on one screen.
2. **Pitch can start as intuition.** A seed pitch may cite author judgment, a research review, or a rough direction.
3. **Later shifts need sources.** Every semantic shift after the seed should cite a source: `discoveries/`, `tasks/`, `probes/`, `insights/`, reviewer feedback, venue strategy, or an explicit author decision.
4. **Archive semantic versions only.** Archive when the story state changes (`seed -> discovery-shift`, `accuracy -> robustness`, `method-first -> application-first`), not for typo edits.
5. **Do not write the paper here.** Abstract, intro, section plan, and LaTeX belong downstream. This skill only maintains the story kernel.
5b. **Pitch is the cover letter.** The pitch IS the venue-ALIGNED cover letter. It can be sent to the editor as-is. It tells THIS editor why THIS paper fits THEIR journal. Venue pinning (STATUS `venue`) must happen before or during pitch. If no venue is pinned, run `/haipipe-paper venue` first.
5c. **Editor's Chair Test lives here.** Read `_venue/playbook-<venue>` for the editor's chair question. Every primary claim must have a one-sentence answer. This test was migrated from claims (v3.0.0) because it is a venue question, not an evidence question.
5d. **[primary] claim designation lives here.** Read the claims ledger (venue-neutral H1, H2, H3) and designate ONE PRIMARY claim aligned to what THIS venue rewards. A result that is novel elsewhere but already established for this venue's readers is an enabler (Methods), not a primary claim. A venue change re-runs this designation.
5e. **RQ framing lives here.** Venue-neutral hypotheses (H1, H2, H3) live in claims. The pitch reframes them as venue-specific RQs: H1 -> RQ1 worded for what the editor rewards. Include an explicit H->RQ mapping with a "why this RQ for this venue" column.
6. **Each hook candidate is one move, not a stack of questions.** Each candidate hook should commit to ONE narrative move (not a stacked enumeration): a vivid concrete scene, a surprising or counterintuitive fact, a paradox tied to stakes, or one sharp question. Do not stack multiple rhetorical questions within a single candidate, which dilutes the punch and reads as undecided. The final artifact keeps all candidate hooks visible (>=2 candidates, one marked as recommended lead). A flat statement of background is not a hook. See `ref/pitch-readability.md`.
7. **Read it in one minute or rewrite it.** The pitch must be fast and easy to read; if a reader slows down to parse a sentence, rewrite that sentence. Follow the readability rules and per-section cues in `ref/pitch-readability.md`: short sentences, lead with the point, one idea per sentence, plain words, concrete numbers, no AI voice. Readability is part of the pitch done-gate.

Workflow
--------

### Step 0: Illuminate + Elicit

Before drafting, follow `ref/stage-illuminate.md`:

- Present the current state of this stage (what exists on disk, what could change).
- Identify 2-3 taste-bearing decisions for this stage.
- Ask the user before committing to choices that affect narrative direction.

### Step 1: Resolve paper folder

Accept either the paper root or any path inside it. Find the paper root by looking upward for one of:

- `0-lifecycle/2-pitch/`
- a `0-*.tex` master and `0-sections/`
- `1-compile.sh`

If no paper folder exists, ask the user to run:

```
/haipipe-paper-lifecycle folder <paper-root>
```

### Step 2: Ensure `0-lifecycle/2-pitch/` exists

The full template is in `ref/pitch-template.tex` (standalone-compilable, ~110 lines). Copy it to `0-lifecycle/2-pitch/2-pitch.tex` and fill in.

Every pitch carries the full backbone: Title, One-Minute Pitch, Hook (>=2 candidates), Finding-Surprise, Implication, Editor's Chair Test, Primary Claim and RQ Framing, Audience/Venue Fit, Evidence, Still Fragile, Next Evidence Move. The body follows the sentence-format in `../../3-write-edit/_shared/sentence-format.md`: a paragraph banner per section, one sentence per line, each tagged `%% ---- Pn.Sm ----`.

The pitch is venue-ALIGNED: it reads STATUS `venue` and consults `../../_venue/playbook-<venue>` to shape the Editor's Chair Test, the [primary] claim designation, the RQ framing, and the Audience section. A venue change means the pitch rewrites. (Claims stays unchanged because it is venue-free.)

Reading order of the template:

```text
1. Title                       ← <=15 words, specific, evocative
2. One-Minute Pitch            ← 4-6 sentences for a newcomer
3. Hook                        ← >=2 candidates, one recommended lead
4. Finding - Surprise          ← the non-obvious turn
5. Implication - So What       ← what changes and who can act
6. Editor's Chair Test         ← venue question from playbook; one-sentence answer per primary claim
7. Primary Claim + RQ Framing  ← [primary] designation + H→RQ mapping for THIS venue
8. Audience and Venue Fit      ← venue-ALIGNED: who reads this journal, why they care
9. Evidence - Why Believe      ← source per claim
10. Limitation - Still Fragile ← top 3 risks
11. Next Evidence Move         ← verb + artifact
```

**Template Enforcement:** A pitch is NOT complete unless it contains, as labeled `\section*` parts: Title, One-Minute Pitch, Hook (with >=2 candidates), Surprise, Implication, Editor's Chair Test, Primary Claim + RQ Framing, Audience/Venue Fit, Why Believe, Still Fragile. A pitch that is one flat paragraph missing these sections must be flagged and restructured before it can pass any gate.

```markdown
# Pitch Log

## v01 -- Seed

Archived:
- none

Source:
- Author intuition / initial review / early project direction.

Pitch:
- See `2-pitch.tex`.

Why this version:
- Initial public-facing story before the evidence base is stable.

Still fragile:
- No direct evidence may exist yet.

Next:
- Identify the first discovery, task, or probe that can strengthen or kill this story.
```

### Step 3: Update the current pitch

When the user gives a new pitch or asks for a pitch revision:

1. Read the current `2-pitch.tex`.
2. If the change is semantic, archive the old file first:
   `0-lifecycle/2-pitch/archive/vNN_<reason>.tex`.
3. Write the new `2-pitch.tex`.
4. Append a compact `PITCH_LOG.md` entry.

Log entry shape:

```markdown
## v02 -> v03 -- <reason>

Archived:
- archive/v02_<reason>.md

Source:
- <author decision / discovery / task / probe / insight / review>

Change:
- Old: ...
- New: ...

Why:
- ...

Still fragile:
- ...

Next:
- ...
```

### Step 3b: Quality Gate

Check the pitch against its rubric:

- [ ] Title section present with working title?
- [ ] Hook section with >=2 candidate methods, all retained?
- [ ] Surprise section with a non-obvious turn stated?
- [ ] Implication section with "so what" and audience stated?
- [ ] Editor's Chair Test present with venue question and one-sentence answer?
- [ ] Primary Claim + RQ Framing present with [primary] designation and H→RQ mapping?
- [ ] Audience/Venue Fit section names who reads this journal and why they care?
- [ ] Why Believe section with evidence pointers (>=1 per claim)?
- [ ] Still Fragile section with the weakest point named?

If any item fails, flag it and offer to fix before advancing.

### Step 4: Compile + Exit Gate

1. Present the exit criteria from `ref/stage-gate.md` with per-item check/fail.
2. Ask: "Stage pitch looks ready -- confirm to close and move to narrative?"
3. Only on user confirm: update `STATUS.md` `current_layer` and Gate Ledger.

### Step 5: Handoff

After updating pitch, report:

- current pitch version
- archived snapshot path, if any
- sources cited
- whether the current pitch is seed / working / reliable / paper-ready
- next structural command, usually:

```
/haipipe-paper narrative <paper-dir>   next stage: the design contract
```

End the reply with the stage strip (run `ref/stage-strip.sh`).

Relationship to other structure skills
--------------------------------------

`0-lifecycle/2-pitch/2-pitch.tex` is one stage of the lifecycle spine:

```
0-seed.md        why this paper might exist (venue-FREE)
    ↓
1-claims.md      claim/evidence inventory (venue-FREE)
    ↓
2-pitch.md       cover letter + one-minute story (venue-ALIGNED, this skill)
    ↓
3-narrative.md   evidence-backed arc (venue-ALIGNED)
    ↓
4-display.tex    display contract (venue-HEAVY)
```

Upstream: claims (0-lifecycle/1-claims/) provides the venue-neutral hypotheses (H1, H2, H3) and evidence status. Pitch reframes them for the target venue.

Downstream: narrative expands the pitch into a full section-mirrored arc. If a downstream stage disagrees with the pitch, either update the pitch with a logged reason or revise the downstream stage. Do not let abstract, introduction, hero figure, and discussion carry different stories.
