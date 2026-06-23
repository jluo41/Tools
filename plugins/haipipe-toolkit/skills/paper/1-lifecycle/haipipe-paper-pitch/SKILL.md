---
name: haipipe-paper-pitch
description: "Create or update the paper folder's 0-lifecycle/1-pitch/1-pitch.tex: a one-minute, evidence-constrained story for this concrete manuscript. Archives semantic old versions and appends PITCH_LOG.md entries when the pitch shifts. Use for paper pitch, one-minute story, hook/surprise/so-what, audience/venue fit, story trajectory, pitch provenance."
argument-hint: "[paper-dir] [--reason <slug>] [--source <path-or-note>...]"
allowed-tools: Bash, Read, Write, Edit, Grep, Glob
metadata:
  version: "1.4.0"
  last_updated: "2026-06-22"
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

Principles
----------

1. **One minute or it failed.** `PAPER_PITCH.md` should be readable in one
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
6. **Hook is one move, not a stack of questions.** Open with one curiosity-driving move: a vivid concrete scene, a surprising or counterintuitive fact, a paradox tied to stakes, or one sharp question. Commit to ONE move; do not stack multiple rhetorical questions, which dilutes the punch and reads as undecided. A flat statement of background is not a hook. See `ref/pitch-readability.md`.
7. **Read it in one minute or rewrite it.** The pitch must be fast and easy to read; if a reader slows down to parse a sentence, rewrite that sentence. Follow the readability rules and per-section cues in `ref/pitch-readability.md`: short sentences, lead with the point, one idea per sentence, plain words, concrete numbers, no AI voice. Readability is part of the pitch done-gate.

Workflow
--------

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
% Para [pitch.hook] Hook -- a vivid, question-led opening that makes the reader curious
% Cue: one sharp question, <=20 words, before any context sentence.
% =========================================================
%% ---- P2.S1 ----
A sharp question, or a concrete scene that ends in one, that makes the reader want the answer. Not a flat statement of background.

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

```markdown
# Pitch Log

## v01 -- Seed

Archived:
- none

Source:
- Author intuition / initial review / early project direction.

Pitch:
- See `PAPER_PITCH.md`.

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

### Step 4: Handoff

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
