---
name: haipipe-paper-minimap
description: "Create or update the paper folder's 0-lifecycle/5-minimap/5-minimap.tex: the paper IN MINIATURE. Each manuscript paragraph becomes 4-5 sentence-points (one point = one manuscript sentence) tagged with the claim it carries, closed by a lean narrative note and any advisor-feedback line, with the real display floats rendered inline as boxed thumbnails. Venue-shaped (section order + abstract form from _venue/playbook-<venue>), rendered with ref/minimap-template.tex. Use for paragraph minimap, sentence-point spine, evidence anchor, section map, paper-in-miniature, 5-minimap."
argument-hint: "[paper-dir]"
allowed-tools: Bash, Read, Write, Edit, Grep, Glob, Skill
metadata:
  version: "2.0.0"
  last_updated: "2026-06-24"
  summary: "Maintain 0-lifecycle/5-minimap/5-minimap.tex as the paper-in-miniature: venue-shaped sentence-point spine + inline display thumbnails + advisor feedback."
  changelog:
    - "2.0.0 (2026-06-24): REWRITE. The minimap is the paper-in-miniature (sentence-points + lean notes + inline display thumbnails + advisor feedback), not a job table. Added ref/minimap-template.tex (venue-neutral macros) + CHECKLIST.md; venue-shaped examples live in _venue/playbook-<venue>. Encoded 7 build rules from the 2026-06-24 digest. Added venue label->pack resolution + an upstream-drift guard; fixed shared-protocol refs to ../../ref/."
    - "1.2.1: added mandatory compile-after-edit rule; venue awareness note"
    - "1.2.0 (2026-06-22): added illuminate+gate+compile protocol"
    - "1.1.0 (2026-06-22): absorbed architecture + plan blueprints as ref/ material"
    - "1.0.0 (2026-06-22): baseline (job-table form, now superseded)"
---

Skill: haipipe-paper-minimap
======================================

Maintain the **minimap** of a concrete paper folder: the last stage of the lifecycle spine before prose. The minimap is the **paper in miniature**. It answers one question:

```text
What does each paragraph say, what evidence anchors it, and how does the spine answer the claims, the displays, and the advisor's comments?
```

It is NOT a job table. Every manuscript paragraph appears as 4-5 sentence-points (one point = one manuscript sentence, the literal opener the prose grows from), each tagged with the claim it carries, closed by a lean narrative note and any advisor-feedback line, with the real display floats rendered inline as boxed thumbnails. The write stage realizes this spine instead of inventing new claims.

Two homes, one neutral one venue-shaped
---------------------------------------

```text
ref/minimap-template.tex     VENUE-NEUTRAL: the LaTeX macros + content checklist + vanilla placeholders. WHAT a minimap covers.
_venue/playbook-<venue>      VENUE-SHAPED: the section order + abstract form + hypotheses-or-not + page budget. HOW to shape it.
   README "-> Minimap"
```

Copy `ref/minimap-template.tex` to `5-minimap.tex`, then SHAPE it to the pinned venue using `_venue/playbook-<venue>`'s `-> Minimap` mapping (theory-forward IMRAD + woven hypotheses for utd-is/MISQ; structured-abstract IMRAD for jama-portfolio). Heavier arc/page-budget design lives in `ref/architecture-blueprint.md` and `ref/plan-outline.md`. (The old `ref/architecture-examples/` are the legacy job-table examples, superseded by the `_venue` minimap mappings.)

Read first: `../../PHILOSOPHY.md`, `../../ref/lifecycle-map.md`. For paragraph ID conventions see `../../3-write-edit/_shared/paragraph-indexing.md`.

Shared Protocols
----------------

Read once (they live at the paper-skill-root `ref/`, hence `../../ref/`): `../../ref/stage-illuminate.md` (illuminate + elicit taste before drafting), `../../ref/stage-gate.md` (exit criteria + confirm-before-advance), `../../ref/tex-quality.md` (self-contained compilable tex). The stage strip helper is `../../ref/stage-strip.sh`. The done-gate is the skill-local `CHECKLIST.md`.

Location
--------

```text
<paper>/0-lifecycle/5-minimap/5-minimap.tex   standalone-compilable stage contract
```

Compile from the PAPER ROOT (so the inline `\input{0-displays/...}` thumbnails resolve), bundled pdflatex twice, then clean aux.

Principles
----------

1. Every paragraph is 4-5 sentence-points; one point = one manuscript sentence. A paragraph with a one-line job but no sentence-points is the OLD job-table form and is a defect.
2. Every sentence-point that carries a claim is tagged `\cl{Cn}`; every planned display is placed via `\dcall` + `\input` of its real float (a thumbnail).
3. The minimap follows the VENUE arc (not the live `0-sections` if they disagree); if upstream disagrees, follow the venue arc and flag the mismatch as a `\wt`, do not silently mirror a stale section structure.
4. The minimap is a map, not prose; sentence-points are terse planned sentences, not finished paragraphs.

### Build rules (from the 2026-06-24 minimap digest)

```text
R1 TITLE        \title = the paper title only, SHORT, shaped to the STATUS venue; no descriptive subtitle.   [title-short-fit-venue]
R2 CLAIM TAGS   \cl{Cn} shows a CONTENT gloss [C1: <phrase>], never a bare [C1]; seed clg@Cn from 2-claims.tex titles.   [claim-tags-show-content]
R3 NOTES LEAN   \nnote = one sharp clause (~10-15 words), and NO "verb, role." editorial prefix (no keep/add/demoted).   [narrative-notes-lean]
R4 PARAGRAPH    aim 4-5 sentence-points per paragraph (not too many or too few; ~6 is the hard ceiling, compress not split).   [PREFERENCES.md]
R5 NO COVERAGE  do NOT emit a Coverage Check crosswalk by default; run it as a SILENT lint (warn on an orphan claim/display).   [drop-coverage-check]
R6 SUPPLEMENT   the eAppendix is DERIVED FROM and kept IN SYNC with the real SI: glob 0-sections/{A..}*.tex + 0-Supplementary-*.   [supplement-sync]
R7 ADVISOR      bake advisor feedback below the note it concerns via \pfb{status}{comment}{resolution}; pull from 3-narrative.tex \fb; roll still-open ones into Write-Time Reconciliations.   [bake-advisor-feedback]
```

Workflow
--------

### Step 0: Illuminate + Elicit

Follow `../../ref/stage-illuminate.md`. Present the current state and the venue-shaped plan. Surface the 2-3 taste-bearing forks (e.g. numbered hypotheses vs a single proposition; abstract shape; which displays are main-text vs SI). Ask, wait.

### Step 1: Resolve paper folder

Accept the paper root or any path inside it (look upward for `0-lifecycle/`).

### Step 2: Gather upstream + venue shape

First RESOLVE the STATUS `venue` label to its `_venue` pack folder (the label rarely equals the folder name). Common map: `MISQ` / `ISR` / `MS-IS` -> `_venue/playbook-utd-is` (per-journal delta inside it); `JAMA` / `JAMA-IM` -> `playbook-jama-portfolio`; `PNAS` -> `playbook-pnas`; `Nature*` -> `playbook-nature-portfolio`; `clinical` -> `playbook-clinical-medicine`; `grant` -> `playbook-grant`; `patent` -> `playbook-patent`. The authoritative label->pack map is owned by `/haipipe-paper-venue`; if the STATUS label matches no folder, resolve it there rather than guessing.

Then gather:

```text
venue shape   <resolved pack>/README "-> Minimap": section order, abstract form, hypotheses-or-not, page budget
claims        2-claims.tex: claim ids + titles  -> seed the \cl{Cn} gloss lookup (R2)
narrative     3-narrative.tex: the beats + the \rev notes (-> \nnote, R3) and the \fb advisor lines (-> \pfb, R7)
displays      4-display.tex / 0-displays/: the units to render inline as thumbnails
supplement    0-sections/{A..}*.tex + any 0-Supplementary-*.tex -> the eAppendix (R6)
arc/budget    ref/architecture-blueprint.md, ref/plan-outline.md (if arc is stale)
```

Drift guard: the live `0-sections/` may be mid-reflow and contradict the venue arc (extra standalone sections, a different count). Shape the minimap to the VENUE arc, and record the mismatch as a `\wt` (the manuscript reflow happens at the write stage); do not mirror a stale `0-sections` structure into the minimap.

### Step 3: Write the minimap

Copy `ref/minimap-template.tex` to `0-lifecycle/5-minimap/5-minimap.tex`. Shape the section order + abstract form to the venue (Step 2). Fill every `<...>` placeholder, applying R1-R7. Per section: a `\pspine` head, 4-5 `\cl`-tagged sentence-points, the inline `\dcall`+`\input` thumbnail where the display is first discussed, a lean `\nnote`, and any `\pfb` advisor line(s). When this is a REBUILD over an existing `5-minimap.tex`, preserve any hand-edited `%% {JL}` comments and ask before clobbering substantive hand content.

Silent coverage lint (replaces the printed Coverage Check, R5): confirm every `supported` claim in `2-claims` and every planned display in `4-display` appears in at least one paragraph; report an orphan as a `\wt`, do not print a crosswalk.

### Step 4: Compile + Exit Gate

1. Compile `5-minimap.pdf` from the paper root (pdflatex twice, clean aux); a stale PDF is a defect, recompile after every edit without being asked.
2. Run the `CHECKLIST.md` done-gate; present each item check/fail.
3. Ask: "Stage minimap looks ready -- confirm to close and move to write?"
4. Only on user confirm: update `STATUS.md` `current_layer` + Gate Ledger.

### Step 5: Handoff

Report the summary (paragraph count, any orphan claim/display, open `\wt` items) and the next command:

```text
write the draft -> /haipipe-paper write <paper-dir>
```

Update `STATUS.md` (`current_layer`, `maturity: section-map`). End with the stage strip (`../../ref/stage-strip.sh`).
