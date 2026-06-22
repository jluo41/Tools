---
name: haipipe-paper-structure-pitch
description: "Create or update the paper folder's 0-lifecycle/1-pitch/1-pitch.tex: a one-minute, evidence-constrained story for this concrete manuscript. Archives semantic old versions and appends PITCH_LOG.md entries when the pitch shifts. Use for paper pitch, one-minute story, hook/surprise/so-what, audience/venue fit, story trajectory, pitch provenance."
argument-hint: "[paper-dir] [--reason <slug>] [--source <path-or-note>...]"
allowed-tools: Bash, Read, Write, Edit, Grep, Glob
metadata:
  version: "1.2.0"
  last_updated: "2026-06-22"
  summary: "Maintain 0-lifecycle/1-pitch/ as the one-minute public-facing story and provenance layer for a concrete paper folder."
---

Skill: haipipe-paper-structure-pitch
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
6. **Hook is a question, not a summary.** Open with a vivid, curiosity-driven hook: a concrete scene or a sharp question that makes the reader want the answer and want to learn more. A flat statement of background is not a hook.

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
/haipipe-paper-structure folder <paper-root>
```

### Step 2: Ensure `0-lifecycle/1-pitch/` exists

Create missing files with the templates below:

Every pitch carries the full backbone: Hook, Surprise, Implication (so-what), Audience/Venue Fit, Why Believe (evidence per point), Still Fragile. The venue routing label (journal / conference / is) lives in STATUS.md; only the audience rationale lives here in the pitch. The body follows the sentence-format in `../../3-write-edit/_shared/sentence-format.md`: a paragraph banner per section, one sentence per line, each tagged `%% ---- Pn.Sm ----`.

```latex
% Layout follows ../../3-write-edit/_shared/sentence-format.md.
\section*{One-Minute Pitch}
% =========================================================
% Para [pitch.kernel] One-minute pitch
% =========================================================
%% ---- P1.S1 ----
One sentence a non-specialist can repeat after one minute.

\section*{Hook}
% =========================================================
% Para [pitch.hook] Hook -- a vivid, question-led opening that makes the reader curious
% =========================================================
%% ---- P2.S1 ----
A sharp question, or a concrete scene that ends in one, that makes the reader want the answer. Not a flat statement of background.

\section*{Surprise}
% =========================================================
% Para [pitch.surprise] Surprise -- the non-obvious turn
% =========================================================
%% ---- P3.S1 ----
The non-obvious turn, tension, or finding.

\section*{Implication}
% =========================================================
% Para [pitch.implication] Implication -- so what, and who can use it
% =========================================================
%% ---- P4.S1 ----
What changes if this story is true, and who can use it.

\section*{Audience and Venue Fit}
% =========================================================
% Para [pitch.audience] Audience -- who the venue reaches and why they care
% =========================================================
%% ---- P5.S1 ----
Who reads the target venue, and why this finding matters to that audience.

\section*{Why Believe}
% =========================================================
% Para [pitch.evidence] Why believe -- evidence for each point
% =========================================================
%% ---- P6.S1 ----
Evidence for each point above, citing a source per claim (or intuition if seed-stage).

\section*{Still Fragile}
% =========================================================
% Para [pitch.fragile] Still fragile -- the weakest point
% =========================================================
%% ---- P7.S1 ----
The weakest point or most important missing evidence.

\section*{Next Evidence Move}
% =========================================================
% Para [pitch.next] Next evidence move
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
4-figures-tables.tex + 0-displays/   display contract
    ↓
5-minimap.tex    paragraph jobs + evidence anchors
```

If a downstream stage disagrees with the pitch, either update the pitch with a
logged reason or revise the downstream stage. Do not let abstract, introduction,
hero figure, and discussion carry different stories.
