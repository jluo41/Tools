---
name: haipipe-paper-section-edit
description: "Per-section editing hub under 0-lifecycle/5-section-edit/. Owns the full per-section lifecycle: DRAFT (structure, narrative, draft sentences) → PROBE (display, values, citation) → REVISE (venue-quality prose) → CHECK (checklist). Each section gets four files: outline .md, _LOG changelog, _CITATION_ citation map, _VALUES_ values registry. Dispatches to probe/, revise/, check/ phase workers. Venue-aware with section-type norm digestion. Dual status strip: paper-level + section-level. Trigger: editing, section edit, section scaffold, outline narrative, edit section, 5-section-edit, /haipipe-paper-section-edit."
argument-hint: "[section-name-or-number] [paper-path]"
allowed-tools: Bash, Read, Write, Edit, Grep, Glob, Skill, Agent
metadata:
  version: "3.2.0"
  last_updated: "2026-07-08"
  summary: "Per-section editing hub. Two-axis model: STAGES (1-lifecycle/) x PHASES (2-phase/). DPRC phases are shared across all lifecycle stages. PROBE is agent-only (flag, no human gate). REVISE works on both .md and .tex. CHECK is the human gate (6-axis verification). _LOG tracks cross-phase evolution with [PHASE] tags."
  # version history: ./CHANGELOG.md (skill-scoped, never loaded at invocation)
  predecessors:
    - "haipipe-paper-editing (1-lifecycle/, scaffold hub) — MERGED"
    - "haipipe-paper-edit (3-write-edit/, edit cycle orchestrator) — MERGED"
---

Skill: haipipe-paper-section-edit
==================================

Combined per-section editing hub. Owns the full per-section lifecycle from scaffold creation through final checklist. Each section the user wants to work on gets a folder under `0-lifecycle/5-section-edit/` with four files. Dispatches to layer workers in `probe/`, `revise/`, `check/` for execution.

```
/haipipe-paper-section-edit                     -> dashboard (all sections + layer status)
/haipipe-paper-section-edit <section>           -> open or create scaffold for that section
/haipipe-paper-section-edit log <section>       -> show recent changelog entries
/haipipe-paper-section-edit lesson [section]    -> SUBAGENT: harvest venue norms into venue pack
/haipipe-paper-section-edit digest [section]    -> SUBAGENT: summarize session changes into _LOG
/haipipe-paper-section-edit feedback [section]  -> SUBAGENT: capture corrections as memory files
```

## Artifact Spec

**Files produced per section:**
- `0-lifecycle/5-section-edit/{section}/{section}.md` -- outline (primary working document)
- `0-lifecycle/5-section-edit/{section}/_LOG_{section}.md` -- changelog with [PHASE] tags
- `0-lifecycle/5-section-edit/{section}/_CITATION_{section}.md` -- citation map (plain text, no bibtex)
- `0-lifecycle/5-section-edit/{section}/_VALUES_{section}.md` -- values registry
- `0-lifecycle/5-section-edit/{section}/_PROBE/` -- probe plans spawned by this section

**Output:**
- `0-sections/*.tex` -- venue-quality LaTeX prose with Pn.Sn markers (synced from revised outline)

**Content structure (outline .md):**
- Structure overview at top (subsections with paragraph counts)
- Per-subsection: `##` heading
- Per-paragraph: `###` heading with job description, parenthetical preview, narrative sentences (one per line)
- User inline comments as `> USER: comment text`

**Done-criteria (6-axis gate -- all must PASS):**
- [ ] structure: outline matches tex, Pn.Sn markers correct
- [ ] citation: no unresolved entries in _CITATION_, density >= venue norm
- [ ] values: no unverified entries in _VALUES_
- [ ] display: all referenced displays exist and captions match claims
- [ ] venue: word budget, style, formatting comply
- [ ] proof: (if applicable) math proofs verified

**DPRC applicability:**
- DRAFT: structure + draft sentences (content decisions)
- PROBE: citation map + values registry + display audit (agent-only, flag issues)
- REVISE: venue-quality prose rewrite, sync outline to tex
- CHECK: human verifies all flags, agent places verified items, 6-axis gate

## Four phases (DRAFT → PROBE → REVISE → CHECK)

Each section progresses through four phases. Not all probe tracks are needed for every section (e.g., pure theory may skip values/display).

```
Phase    What it does                             Where it lives
───────  ───────────────────────────────────────  ─────────────────────────
DRAFT    what to say: paper structure, section     z-structure scaffold +
         structure (¶ count, H placement), and     N-section.md
         draft sentences (content decisions)

PROBE    what to reference (3 parallel tracks):
  display   figures/tables for this section       → 0-displays/ units
  values    every number, source, verified?       _VALUES_N-section.md
  citation  what's cited where, journal tier      _CITATION_N-section.md

REVISE   how to say it well: rewrite draft        → dispatched to revise/ workers
         sentences to venue quality, weaving in
         probed citations/values/displays

CHECK    did we get it right: final verification  → dispatched to check/ workers
```

DRAFT = what to say (content decisions, including draft sentences)
PROBE = what to reference (evidence collection via probes)
REVISE = how to say it well (the draft sentences exist; revise rewrites them to venue quality)
CHECK = did we get it right (verification)

Progression gates:
- Draft settled (user confirms)? → PROBE (agent gathers evidence aggressively, flags issues)
- Probed (all tracks flagged)? → REVISE (agent revises .md then syncs to .tex)
- Revised? → CHECK (human verifies flags, agent places verified items, 6-axis gate)
- All 6 axes PASS? → section done. FAIL? → route back to failing phase.

Phase visibility per the Phase Transition Contract in `../../../wiki/08-stage-gate.md`: announce every phase boundary (reply line + `[PHASE]` entry in `_LOG` + phase-line 🔥 moves); skip a phase only by an explicit logged verdict (`[PROBE] skipped -- <reason>`, phase line shows `--`); CHECK is never implicit -- it opens by presenting the exit-criteria report and the approval ask.

Discovery and task are MECHANISMS feeding the probe phase: discovery finds citations, task produces figures and numbers. They route through per-stage `_PROBE/` folders. PROBE checks existing evidence FIRST, plans, then probes ONLY if information is missing.

**Format rule**: paper-level argument documents (seed, claims, pitch, narrative) are markdown + _LOG only. The display stage is the ONLY paper-level stage that compiles to .tex + PDF (you need to SEE rendered figures/tables). Section-level outline stays in .md throughout; tex is synced from revised outline during REVISE and updated during CHECK. Rule of thumb: if you need to SEE it rendered, .tex. If you need to READ and edit it, .md.

**The outline .md is the primary working document.** DRAFT creates it. PROBE annotates its tracking files. REVISE updates its sentences and syncs to tex. CHECK verifies everything matches. The outline is never "frozen after draft" -- it stays alive through all phases.

## Closing block (section-aware)

Every reply ends with the closing block defined in `../../../haipipe-paper/SKILL.md` (Closing Block section, the single source of truth). In section-edit the header and phase line carry the active section:

```
── 📄 paper · section-edit · §3-theory 🔥 ────────
status:  ok · section-edit · §3-theory
next:    <next action>
─────────────────────────────────────────────────────
stage:   seed ✅  claims ✅  venue ✅  pitch ✅  narrative ✅  display ✅  →  section-edit 🔥🚀  →  review ⬜
phase:   §3 draft ✅  │  probe: cite 🔥🚀  val --  disp --  │  revise ⬜  │  check ⬜
```

Markers and rendering rules live in the umbrella spec (stage line via `stage-strip.sh`, never hand-typed). Section-edit adds one local marker: ⚠️ = done but needs re-sync (outline changed after tex sync).

How to derive status from disk:
- draft ✅ if outline has structure block with ¶ counts AND narrative sentences
- cite ✅ if _CITATION_ all placed and density >= venue norm
- val ✅ if no values needed (--) OR _VALUES_ all verified
- disp ✅ if no displays needed (--) OR displays linked in 0-displays/
- revise ✅ if prose revised (tex synced from outline) and user confirmed
- check ✅ if _LOG has a checklist entry

## Dashboard (no-arg mode)

When invoked without a section argument, show all sections' layer status:

```
/haipipe-paper-section-edit

§   Section         DRAFT   PROBE                     REVISE   CHECK
──  ──────────────  ──────  ────────────────────────  ───────  ─────
§1  introduction    draft✅  cite⬜  val⬜  disp⬜      revise⬜  check⬜
§2  literature      draft✅  cite⬜  val⬜  disp⬜      revise⬜  check⬜
§3  theory          draft✅  cite🚀  val--  disp--      revise⚠️  check⬜
§4  measurement     draft✅  cite⬜  val⬜  disp⬜      revise⬜  check⬜
§5  empirical       draft⬜  cite⬜  val⬜  disp⬜      revise⬜  check⬜
§6  results         draft⬜  cite⬜  val⬜  disp⬜      revise⬜  check⬜
§7  discussion      draft⬜  cite⬜  val⬜  disp⬜      revise⬜  check⬜

-- = skipped (not applicable for this section)
```

## Per-stage tracking files

Each stage is self-contained with its own tracking files.

```
Paper-level stages (0-lifecycle/):

  0-seed/
    0-seed.md + _LOG                                (base only)

  1-claims/
    1-claims.md + _LOG
    _EVIDENCE_1-claims.md      what evidence backs each claim
    _PROBE/                    probe plans spawned by claim gaps

  2-pitch/
    2-pitch.md + _LOG
    _CITATION_2-pitch.md       citation map (pitch cites anchor papers)
    _PROBE/                    probe plans spawned by pitch needs

  3-narrative/
    3-narrative.md + _LOG
    _CITATION_3-narrative.md   citation map (narrative beats cite prior work)
    _DISPLAY_3-narrative.md    which display unit serves each beat
    _PROBE/                    probe plans spawned by narrative needs

  4-display/
    4-display.tex + pdf        (the ONLY compiled stage)
    _LOG_4-display.md
    _PROBE/                    probe plans spawned by display needs

Section-level stages (0-lifecycle/5-section-edit/):

  z-structure/
    z-structure.md + _LOG                           (base only)

  {section}/
    {section}.md               outline (draft: structure + narrative + sentences)
    _LOG_{section}.md          changelog (all phases, with [PHASE] tags)
    _CITATION_{section}.md     citation map (plain text, no bibtex)
    _VALUES_{section}.md       values registry
    _PROBE/                    probe plans spawned by this section
```

Summary table -- which tracking files each stage uses:

```
                     .md  _LOG  _CITATION  _VALUES  _EVIDENCE  _DISPLAY  _PROBE
  seed               ✅    ✅
  claims             ✅    ✅                          ✅                   ✅
  pitch              ✅    ✅    ✅                                         ✅
  narrative           ✅    ✅    ✅                               ✅        ✅
  display            ✅    ✅                                     ✅        ✅
  section-edit (×N)  ✅    ✅    ✅          ✅                    ✅        ✅
```

Tracking files are created lazily when the phase activates for that stage.

**Probe plan convention**: probe plans LIVE in the `_PROBE/` subfolder of the stage that spawned them. `1-probe-plans/README.md` is a cross-stage INDEX (links to per-stage `_PROBE/` folders; PP numbering authority). When creating a new probe plan: add the file to the stage's `_PROBE/` folder AND add a row to the index.

## Two-axis architecture: stages x phases

This skill is a STAGE (the WHAT: per-section editing). It dispatches to PHASE workers (the HOW) that live in `2-phase/`. Phases are shared across all lifecycle stages.

```
1-lifecycle/                          STAGES (the WHAT)
  5-section-edit/
    haipipe-paper-section-edit/       ← THIS SKILL (hub)
    section-type/                     per-section playbooks (knowledge)

2-phase/                              PHASES (the HOW, shared)
  0-draft/
    haipipe-paper-draft                 settle structure + draft sentences
                                        (venue style comes from 0-lifecycle/2-venue/2-venue.md;
                                         _venue/playbook-* packs = fallback + deep dive)
  1-probe/
    haipipe-paper-probe-citation        citation → _CITATION_.md (agent-only, flag)
    haipipe-paper-probe-values          values → _VALUES_.md (agent-only, flag)
    haipipe-paper-probe-display         display → 0-displays/ (agent-only, flag)
  2-revise/
    haipipe-paper-revise-content        content review (WHAT sentences say)
    haipipe-paper-revise-humanizer      de-AI audit (HOW sentences sound)
    haipipe-paper-revise-results  results-specific revision
  3-check/
    haipipe-paper-check               6-axis verification gate (human + agent)
    haipipe-paper-proof-checker         math proof verification (specialized)

3-build-submit/                       whole-paper tools (haipipe-paper-edit-*)
```

The phase workers use the pattern `haipipe-paper-{phase}-{what}` (e.g. `haipipe-paper-probe-citation`, `haipipe-paper-revise-content`). The phase name is the primary axis since these workers are shared across lifecycle stages, not just section-edit.

## Outline-narrative file

The working document for one section at the paragraph level.

```markdown
# Section N: Title — Structure

\```
§N.1 Subsection Title (K ¶)
  P1. Short paragraph job description                        N sentences
  P2. Short paragraph job description                        N sentences
\```

---

## §N.1 Subsection Title

### P1. What this paragraph does

(Semicolon-separated preview of key points.)

Narrative sentence one.

Narrative sentence two.
```

Rules:
- Structure overview at top (update whenever structure changes).
- `##` for subsections, `###` for paragraphs.
- Each paragraph: headline (job), parenthetical preview, narrative sentences.
- **Preview must be ONE SHORT LINE (~80-120 chars)**, not a mini-abstract. The preview is a scan hook: concept name + one distinguishing phrase. If it reads like a paragraph, compress it.
- One narrative sentence per line (→ `Pn.Sn` markers in tex).
- Target 5-6 sentences per paragraph (MISQ/ISR norm).
- User inline comments as `> USER: comment text`.

## _CITATION_ and _VALUES_ specs

**_CITATION_ is plain text only. No bibtex blocks.** _CITATION_ is the MAP (what to cite, where, why). .bib is the DATA (actual bibtex). Agent writes to _CITATION_; human writes to .bib (by copying from Google Scholar). Agent discovers the bibtex key by grepping .bib after the human adds it. See `2-phase/1-probe/haipipe-paper-probe-citation/SKILL.md` for the full format spec, provenance tracking, and sync protocol.

Status emoji:
- _CITATION_: `✅ placed` (in bib + tex), `📌 in bib` (not yet placed), `🔍 candidate` (not in bib, needs verification), `⚠️ issue` (wrong paper, drift), `❌ rejected` (kept as audit trail), `📋 pre-existing` (provenance unknown)
- _VALUES_: `✅ verified`, `⬜ unverified`, `⚠️ mismatch`, `🔍 source unknown`

Provenance source: `🧑 scholar-copied` (human added), `🤖 agent-found` (agent searched, human must verify), `📋 pre-existing` (was in .bib, unknown origin)

## _LOG changelog

Newest entry at top. Every entry carries a **[PHASE]** tag so you can grep by phase.

Format: `## YYYY-MM-DD #N ~HH:MM [PHASE]` + trigger quote + bullet changes.

```markdown
## 2026-07-03 #7 ~11:00 [CHECK]
> USER verified citations, approved displays
- citation: 3 🔍 → 2 ✅ + 1 ❌, placed \citep{} for 2 verified
- values: no numbers in intro (skipped)
- 6-axis: all PASS → section CHECK ✅

## 2026-07-02 #5 ~16:00 [REVISE]
> USER: "polish introduction"
- Revised outline P1-P6 (32 → 28 sentences)
- Synced → 0-sections/01_introduction.tex
- \citep{} placed for 11 keys already in .bib
- 3 parenthetical "(Author Year)" left for unverified

## 2026-07-02 #4 ~14:00 [PROBE]
> triggered by: draft confirmed
- citation: 5 gaps found, 3 🔍 candidates, density 0.44 → need 0.70
- values: scanned, no numbers in intro (skipped)
- display: no displays needed (skipped)

## 2026-07-01 #3 ~10:00 [DRAFT confirmed]
> USER: "looks good"
- 6 paragraphs, 32 draft sentences confirmed
- P6 stays at bottom (IS positioning)
```

Grep shortcuts:
- `grep '\[DRAFT\]' _LOG_*.md` → all drafting rounds
- `grep '\[PROBE\]' _LOG_*.md` → all probe rounds
- `grep '\[REVISE\]' _LOG_*.md` → all revise rounds
- `grep '\[CHECK\]' _LOG_*.md` → all check rounds

## Workflow

### DRAFT

1. **Consult venue**: read the paper's `0-lifecycle/2-venue/2-venue.md` FIRST -- this section's Structural Blueprint block (subsections, paragraphs per subsection, sentences per paragraph, sentence length, citation density, results detail, display units) plus the Writing Principles block (tone, citation style, results presentation). If `2-venue.md`'s recorded pack commit is behind the current `_venue` HEAD, note "venue contract stale -- consider /haipipe-paper-venue refresh" but still use it (never silently re-read packs).
   - Deep dive: follow the block's `[source: ...]` tag to `_venue/playbook-<pack>/<outlet>/<outlet>-<section>/style.md` for what the blueprint does not transcribe (arc, signature moves, exemplar sentences, anti-patterns).
   - Fallback (ONLY if `2-venue.md` is absent -- venue stage not yet run, or a pack-less venue): read `_venue/playbook-<pack>/style-profile.md` for general venue norms, then resolve the per-section style guide:
     - From `STATUS.md venue:` extract the outlet (e.g., "MISQ 2026" → outlet "MISQ", pack "playbook-utd-is")
     - Map the current section type to the outlet dir suffix (abstract→abstract, introduction→introduction, theory→theory, methods→methods, results→results, discussion→discussion, related-work→related-work, theory-model→theory-model)
     - Read `_venue/playbook-<pack>/<outlet>/<outlet>-<section>/style.md` if it exists
     - This file contains word budget, arc, signature moves, exemplar sentences, anti-patterns, and paragraph structure mined from real papers. It OVERRIDES the general style-profile.md for this specific section.
     - Example: editing MISQ theory → read `_venue/playbook-utd-is/MISQ/MISQ-theory/style.md`
     - Example: editing NMI results → read `_venue/playbook-nature-portfolio/NMI/NMI-results/style.md`
     - If no pack exists either, proceed without venue inputs.

2. **Create scaffold**: folder + outline + _LOG. Populate from existing tex if available.

3. **Settle structure**: subsections, paragraph count, hypothesis placement.

4. **Settle narrative**: paragraph headlines, previews, and draft sentences. The draft sentences capture content decisions (what each sentence says), not polished prose.

### PROBE (agent-only -- probe aggressively, flag issues)

The agent does all three tracks without waiting for human. Flag everything that needs human attention. Do NOT place \citep{} or weave values into tex during PROBE. Placement happens in CHECK after human verification.

5. **Citation**: create `_CITATION_` file. Audit gaps in the outline. Check existing .bib first. Search for candidates. Write 🔍 entries with Scholar links. Flag everything. Count density vs venue norm. If deeper search needed → write probe plan to `_PROBE/`. Do NOT wait for human, do NOT place \citep{}.

6. **Values**: create `_VALUES_` file. Scan every number in the outline/tex. Trace each to a source (task output, display CSV, script). Flag ⚠️ mismatches and 🔍 unknown sources. If source not found → write probe plan to `_PROBE/`. Do NOT wait for human.

7. **Display**: audit what displays this section needs. Check existing `0-displays/` units. Plan which display serves which claim. If display doesn't exist → route to `/haipipe-task`. Flag missing displays. Do NOT wait for approval.

**Probe escalation**: PROBE checks existing evidence FIRST, then plans, then probes ONLY if the information isn't already available. The flow is: check existing → audit gaps → plan → search (lightweight) → probe (heavyweight, only if needed).

### REVISE (agent-only -- works on BOTH .md and .tex)

8. **Revise outline .md**: sharpen draft sentences to venue-quality wording. Weave in citations that are ALREADY in .bib (place parenthetical "(Author Year)" for unverified candidates). Weave in verified values. Leave (?) for unverified values. Dispatch to `2-phase/2-revise/` workers for de-AI voice, venue style, paragraph flow.

9. **Sync to tex**: sync revised sentences from outline → `0-sections/*.tex` with `Pn.Sn` markers. Place `\citep{key}` only for keys already in `.bib`. Leave parenthetical for unverified candidates.

The outline .md is always the PRIMARY working document. The tex is the compiled output. Revise updates the outline first, then syncs to tex.

The comment-first protocol (used by revise workers):
- Round 1: insert `%% {CC-<topic>-vMMDD}: finding` comments, change NO prose
- Human replies: `========> {USER vMMDD}: accept|reject|modify|discuss`
- Apply round: act on accepted comments only

### CHECK (human + agent -- the GATE)

10. **Human reviews all flags**: present all 🔍 and ⚠️ entries from _CITATION_, _VALUES_, and display plans. The human:
    - Clicks Scholar links, verifies citations, copies bibtex → .bib, marks `> ✅ SEARCH`
    - Checks values against sources, confirms or corrects numbers
    - Reviews generated displays, approves or requests revision
    - May provide NEW information ("cite Smith 2020 here", "correct N is 83,230")

11. **Agent places verified items**: after human verification:
    - Discovers bibtex keys by grepping .bib for paper titles
    - Places `\citep{key}` in tex for verified citations
    - Updates _CITATION_ status: 🔍 → ✅
    - Weaves verified values into tex
    - Links approved displays

12. **6-axis gate** (all must PASS for section to be done):
    - ✅ structure: outline ↔ tex match, Pn.Sn correct
    - ✅ citation: no 🔍 or ⚠️ in _CITATION_, density ≥ venue norm
    - ✅ values: no ⬜ or ⚠️ in _VALUES_
    - ✅ display: all referenced, captions match claims
    - ✅ venue: word budget, style, formatting
    - ✅ proof: (if applicable) math proofs verified

    PASS → section done (check ✅). Log checklist entry in _LOG.
    FAIL → report which axis failed → route BACK to the failing phase.

13. **Compile**: run `./1-compile.sh`.

## Venue norm digestion

Section-type norms learned during editing flow into the venue pack:

1. Captured in `_LOG` during editing.
2. `lesson` subagent harvests norms → per-section `style.md` at `_venue/playbook-<pack>/<outlet>/<outlet>-<section>/style.md`.
3. Each outlet accumulates its own section-level style guides across papers (e.g., `MISQ/MISQ-theory/style.md`, `NMI/NMI-results/style.md`).
4. Future sessions reach the per-section style guide via the `[source: ...]` tags in `2-venue.md` (or directly, when no `2-venue.md` exists). A harvest that changes the pack leaves existing `2-venue.md` contracts stale -- refresh via `/haipipe-paper-venue refresh`.
5. The per-section files are mined from real exemplar PDFs stored in `_WorkSpace/HAIToolLib/1-ExemplarLib/<family>/<outlet>/`. See `_venue/_SCHEMA.md` for the full resolution path and section-type mapping.

## Subagent verbs: lesson, digest, feedback

Dispatch to background subagents via the Agent tool. Never run inline.

- **lesson**: harvest venue norms and structural decisions from _LOG → venue pack.
- **digest**: summarize session changes into _LOG from outline + tex + git diff.
- **feedback**: capture corrections and preferences as memory files.

The caller MUST include concrete file paths and context in the Agent prompt.

## Relation to other skills

```
1-lifecycle/ (STAGES)                    2-phase/ (PHASES, shared)
─────────────────────                    ────────────────────────
haipipe-paper-lifecycle                  0-draft/
  ├─► seed                                haipipe-paper-draft
  ├─► claims                              (venue style: 2-venue.md; packs = fallback)
  ├─► [venue gate]
  ├─► pitch                              1-probe/ (agent-only, flag)
  ├─► narrative                            haipipe-paper-probe-citation   → _CITATION_
  ├─► display                              haipipe-paper-probe-values     → _VALUES_
  └─► section-edit (THIS)                  haipipe-paper-probe-display    → 0-displays/
        │                                    ↓ escalation
        │   DRAFT → PROBE → REVISE → CHECK   _PROBE/ → /haipipe-probe → /haipipe-task
        │
        │   hub dispatches to              2-revise/ (agent-only, .md + .tex)
        │   2-phase/ workers                 haipipe-paper-revise-content (WHAT)
        │   based on frontier phase          haipipe-paper-revise-humanizer (HOW: de-AI)
        │
        │                                  3-check/ (human + agent gate)
        │                                    haipipe-paper-check (6-axis)
        │                                    haipipe-paper-proof-checker (math)
        │
        └── section-type/ (knowledge, consumed by all phases)
              section-intro, section-methods, section-results, ...
```

Human involvement by phase:
- **DRAFT**: agent + user (settle content decisions together)
- **PROBE**: agent only (probe aggressively, flag 🔍⚠️, no human gate)
- **REVISE**: agent only (revise .md, sync to .tex, comment-first protocol)
- **CHECK**: human + agent (human verifies all flags, agent places verified items, 6-axis gate)
