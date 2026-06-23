---
name: haipipe-paper-pitch
description: "Create or update the paper folder's 0-lifecycle/1-pitch/1-pitch.tex: a one-minute, evidence-constrained story for this concrete manuscript. Archives semantic old versions and appends PITCH_LOG.md entries when the pitch shifts. Use for paper pitch, one-minute story, hook/surprise/so-what, audience/venue fit, story trajectory, pitch provenance."
argument-hint: "[paper-dir] [--reason <slug>] [--source <path-or-note>...]"
allowed-tools: Bash, Read, Write, Edit, Grep, Glob
metadata:
  version: "1.5.2"
  last_updated: "2026-06-23"
  changelog:
    - "v1.5.2: extracted template to ref/pitch-template.tex; inline replaced with reading-order summary"
    - "v1.5.1: added mandatory compile-after-edit rule; venue awareness note"
    - "1.5.0 (2026-06-22): added Title section, multi-hook candidates, template enforcement, quality gate; wired illuminate+gate+compile protocols"
    - "1.4.0 (2026-06-22): readability rules, section cues, hook catalog"
  summary: "Maintain 0-lifecycle/1-pitch/ as the one-minute public-facing story and provenance layer for a concrete paper folder. Carries readability rules, section cues, and a hook narrative-methods catalog (ref/pitch-readability.md)."
---

Skill: haipipe-paper-pitch
====================================

Maintain the **paper pitch** for a concrete manuscript folder.

The pitch is not a paper plan, outline, or claim matrix. It is the version a
person can understand in one minute:

```
What is this paper about?
What vivid question or scene pulls the reader in?
What is surprising?
So what changes if it is true?
Who reads the target venue, and why does this matter to them?
Why should we believe it?
What is still fragile?
How did the story get here?
```

Illustration:
- `images/stage2-pitch-gate-image2.png` — Stage 2 as a pitch gate: either return
  to narrative/project work or proceed to Stage 3 evidence-backed narrative.

Location:

```
<paper>/
└── 0-lifecycle/1-pitch/
    ├── 1-pitch.tex          current one-minute story (standalone-compilable contract)
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

1. **One minute or it failed.** `1-pitch.tex` should be readable in one
   minute. Keep it short enough to fit on one screen.
2. **Pitch can start as intuition.** A seed pitch may cite author judgment,
   a research review, or a rough direction.
3. **Later shifts need sources.** Every semantic shift after the seed should
   cite a source: `discoveries/`, `tasks/`, `probes/`, `insights/`, reviewer
   feedback, venue strategy, or an explicit author decision.
4. **Archive semantic versions only.** Archive when the story state changes
   (`seed -> discovery-shift`, `accuracy -> robustness`, `method-first ->
   application-first`), not for typo edits.
5. **Do not write the paper here.** Abstract, intro, section plan, and LaTeX
   belong downstream. This skill only maintains the story kernel.
5b. **Research questions belong in claims, not pitch.** The pitch is
   venue-independent (the one-minute story). RQs are venue-coupled (their
   wording depends on what the target editor rewards). RQs are defined in
   `2-claims.tex` with an explicit RQ-to-claim mapping. Do not add RQs to
   the pitch.
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

Accept either the paper root or any path inside it. Find the paper root by
looking upward for one of:

- `0-lifecycle/1-pitch/`
- a `0-*.tex` master and `0-sections/`
- `1-compile.sh`

If no paper folder exists, ask the user to run:

```
/haipipe-paper-lifecycle folder <paper-root>
```

### Step 2: Ensure `0-lifecycle/1-pitch/` exists

The full template is in `ref/pitch-template.tex` (standalone-compilable,
~110 lines). Copy it to `0-lifecycle/1-pitch/1-pitch.tex` and fill in.

Every pitch carries the full backbone: Title, One-Minute Pitch, Hook (>=2
candidates), Finding-Surprise, Implication, Audience/Venue Fit, Evidence,
Still Fragile, Next Evidence Move. The body follows the sentence-format in
`../../3-write-edit/_shared/sentence-format.md`: a paragraph banner per section,
one sentence per line, each tagged `%% ---- Pn.Sm ----`.

The pitch is venue-AWARE (Audience section names who reads the target journal)
but NOT venue-COUPLED (RQs and claim framing live in `2-claims.tex`). When a
`../../_venue/playbook-<venue>` pack exists for STATUS `venue`, read its
`README.md` for what that venue's readers reward, and let the Audience section
reflect it.

Reading order of the template:

```text
1. Title                    ← <=15 words, specific, evocative
2. One-Minute Pitch         ← 4-6 sentences for a newcomer
3. Hook                     ← >=2 candidates, one recommended lead
4. Finding - Surprise       ← the non-obvious turn
5. Implication - So What    ← what changes and who can act
6. Audience and Venue Fit   ← venue-aware, not venue-coupled
7. Evidence - Why Believe   ← source per claim
8. Limitation - Still Fragile ← top 3 risks
9. Next Evidence Move       ← verb + artifact
```

**Template Enforcement:** A pitch is NOT complete unless it contains, as labeled
`\section*` parts: Title, One-Minute Pitch, Hook (with >=2 candidates), Surprise,
Implication, Why Believe, Still Fragile. A pitch that is one flat paragraph missing
these sections must be flagged and restructured before it can pass any gate.

```markdown
# Pitch Log

## v01 -- Seed

Archived:
- none

Source:
- Author intuition / initial review / early project direction.

Pitch:
- See `1-pitch.tex`.

Why this version:
- Initial public-facing story before the evidence base is stable.

Still fragile:
- No direct evidence may exist yet.

Next:
- Identify the first discovery, task, or probe that can strengthen or kill this story.
```

### Step 3: Update the current pitch

When the user gives a new pitch or asks for a pitch revision:

1. Read the current `1-pitch.tex`.
2. If the change is semantic, archive the old file first:
   `0-lifecycle/1-pitch/archive/vNN_<reason>.tex`.
3. Write the new `1-pitch.tex`.
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
- [ ] Why Believe section with evidence pointers (>=1 per claim)?
- [ ] Still Fragile section with the weakest point named?
- [ ] `1-pitch.pdf` recompiled and current (a stale PDF is a defect; recompile after every edit without being asked).

If any item fails, flag it and offer to fix before advancing.

### Step 4: Compile + Exit Gate

1. Compile the stage PDF per `ref/tex-quality.md` (pdflatex twice, clean aux).
2. Present the exit criteria from `ref/stage-gate.md` with per-item check/fail.
3. `1-pitch.pdf` recompiled and current (a stale PDF is a defect; recompile after every edit without being asked).
4. Ask: "Stage pitch looks ready -- confirm to close and move to claims?"
5. Only on user confirm: update `STATUS.md` `current_layer` and Gate Ledger.

### Step 5: Handoff

After updating pitch, report:

- current pitch version
- archived snapshot path, if any
- sources cited
- whether the current pitch is seed / working / reliable / paper-ready
- next structural command, usually:

```
/haipipe-paper claims <paper-dir>      next stage: the claim ledger
/haipipe-paper narrative <paper-dir>   once claims are stable
```

End the reply with the stage strip (run `ref/stage-strip.sh`).

Relationship to other structure skills
--------------------------------------

`0-lifecycle/1-pitch/1-pitch.tex` is one stage of the lifecycle spine:

```
1-pitch.tex      one-minute public-facing story (this skill)
    ↓
2-claims.tex     claim ledger: supported / weak / GAP
    ↓
3-narrative.tex  evidence-backed arc
    ↓
4-display.tex + 0-displays/   display contract
    ↓
5-minimap.tex    paragraph jobs + evidence anchors
```

If a downstream stage disagrees with the pitch, either update the pitch with a
logged reason or revise the downstream stage. Do not let abstract, introduction,
hero figure, and discussion carry different stories.
