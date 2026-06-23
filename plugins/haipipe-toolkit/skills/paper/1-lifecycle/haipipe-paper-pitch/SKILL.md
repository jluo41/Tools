---
name: haipipe-paper-pitch
description: "Create or update the paper folder's 0-lifecycle/1-pitch/1-pitch.tex: a one-minute, evidence-constrained story for this concrete manuscript. Archives semantic old versions and appends PITCH_LOG.md entries when the pitch shifts. Use for paper pitch, one-minute story, hook/surprise/so-what, audience/venue fit, story trajectory, pitch provenance."
argument-hint: "[paper-dir] [--reason <slug>] [--source <path-or-note>...]"
allowed-tools: Bash, Read, Write, Edit, Grep, Glob
metadata:
  version: "1.5.0"
  last_updated: "2026-06-22"
  changelog:
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

Create missing files with the templates below:

Every pitch carries the full backbone: Hook, Surprise, Implication (so-what), Audience/Venue Fit, Why Believe (evidence per point), Still Fragile. The venue routing label (journal / conference / is) lives in STATUS.md; only the audience rationale lives here in the pitch. When a `../../_venue/playbook-<venue>` pack exists for STATUS `venue`, read its `README.md` `-> Claims`/framing for what that venue's readers reward, and let the Audience and Venue Fit section reflect it (who the venue reaches, why this finding matters to them). The body follows the sentence-format in `../../3-write-edit/_shared/sentence-format.md`: a paragraph banner per section, one sentence per line, each tagged `%% ---- Pn.Sm ----`.

```latex
% Layout follows ../../3-write-edit/_shared/sentence-format.md.
% Readability rules + section cues + worked before/after examples: ref/pitch-readability.md.
\section*{Title}
% =========================================================
% Para [pitch.title] Working title
% Cue: short, specific, evocative; <=15 words; updated as the story sharpens.
% =========================================================
%% ---- P0.S1 ----
Working title for the paper.

\section*{One-Minute Pitch}
% =========================================================
% Para [pitch.kernel] One-minute pitch
% Cue: a short plain-language paragraph (~4-6 short sentences) for a NEWCOMER with no
%      background. Open with a framing sentence ("We study whether/how X relates to Y"),
%      then the puzzle, the method in plain words, the surprising finding, and why it
%      matters, so they understand it and feel interested. Not a single terse sentence.
% =========================================================
%% ---- P1.S1 ----
We study whether / how X relates to Y.
%
%% ---- P1.S2 ----
Plain-language context or the puzzle a newcomer needs.
%
%% ---- P1.S3 ----
The method in plain words.
%
%% ---- P1.S4 ----
The surprising finding.
%
%% ---- P1.S5 ----
Why it matters, and who could use it.

\section*{Hook}
% =========================================================
% Para [pitch.hook] Hook -- multiple candidate openings, all retained
% Cue: >=2 candidate methods (e.g. Paradox, Vivid Scene, Surprising Fact, Stakes, Gap).
%       Each candidate is a \subsection* block, one per narrative method.
%       ALL candidates are kept permanently displayed -- never collapsed.
%       Mark one as "(recommended lead)" but do NOT hide the rest.
%       The author chooses the final lead at write time.
% Hook section must show >=2 candidate methods, all retained, with a recommended lead marked.
% =========================================================

\subsection*{Candidate A: Paradox (recommended lead)}
%% ---- P2a.S1 ----
A paradox or tension that sets expectation against reality. 2-4 short sentences.

\subsection*{Candidate B: Vivid Scene}
%% ---- P2b.S1 ----
A concrete moment with specifics that makes the reader feel it. 2-4 short sentences.

\subsection*{Candidate C: Stakes}
%% ---- P2c.S1 ----
What is at risk -- opens with consequence. 2-4 short sentences.

% Add more candidates as needed. Each commits to ONE narrative move.
% See ref/pitch-readability.md for the full method menu.

\section*{Finding - Surprise}
% =========================================================
% Para [pitch.surprise] Surprise -- the non-obvious turn
% Cue: put the unexpected result in sentence 1, then the tension.
% =========================================================
%% ---- P3.S1 ----
The non-obvious turn, tension, or finding.

\section*{Implication - So What}
% =========================================================
% Para [pitch.implication] Implication -- so what, and who can use it
% Cue: name what changes and who can act in the first two sentences.
% =========================================================
%% ---- P4.S1 ----
What changes if this story is true, and who can use it.

\section*{Audience and Venue Fit}
% =========================================================
% Para [pitch.audience] Audience -- who the venue reaches and why they care
% Cue: name the reader and their need before the venue format.
% =========================================================
%% ---- P5.S1 ----
Who reads the target venue, and why this finding matters to that audience.

\section*{Evidence - Why Believe}
% =========================================================
% Para [pitch.evidence] Why believe -- evidence for each point
% Cue: tie each sentence to a table/display/model/check/source; mark planned as planned.
% =========================================================
%% ---- P6.S1 ----
Evidence for each point above, citing a source per claim (or intuition if seed-stage).

\section*{Limitation - Still Fragile}
% =========================================================
% Para [pitch.fragile] Still fragile -- the weakest point
% Cue: list only the top three highest-risk weaknesses.
% =========================================================
%% ---- P7.S1 ----
The weakest point or most important missing evidence.

\section*{Next Evidence Move}
% =========================================================
% Para [pitch.next] Next evidence move
% Cue: start with a verb and name the artifact this move updates.
% =========================================================
%% ---- P8.S1 ----
What discovery, task, probe, or review should happen next.
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
- [ ] PDF compiled and current?

If any item fails, flag it and offer to fix before advancing.

### Step 4: Compile + Exit Gate

1. Compile the stage PDF per `ref/tex-quality.md` (pdflatex twice, clean aux).
2. Present the exit criteria from `ref/stage-gate.md` with per-item check/fail.
3. Ask: "Stage pitch looks ready -- confirm to close and move to claims?"
4. Only on user confirm: update `STATUS.md` `current_layer` and Gate Ledger.

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
