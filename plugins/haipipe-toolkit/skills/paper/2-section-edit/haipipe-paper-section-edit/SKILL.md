---
name: haipipe-paper-section-edit
description: "Per-section editing hub under 0-lifecycle/5-editing/. Owns the full per-section lifecycle: DRAFT (structure, narrative, draft sentences) → GATHER (display, values, citation) → POLISH (venue-quality prose) → CHECK (checklist). Each section gets four files: outline .md, _LOG changelog, _CITATION_ citation map, _VALUES_ values registry. Dispatches to gather/, polish/, check/ phase workers. Venue-aware with section-type norm digestion. Dual status strip: paper-level + section-level. Trigger: editing, section edit, section scaffold, outline narrative, edit section, 5-editing, /haipipe-paper-section-edit."
argument-hint: "[section-name-or-number] [paper-path]"
allowed-tools: Bash, Read, Write, Edit, Grep, Glob, Skill, Agent
metadata:
  version: "2.1.0"
  last_updated: "2026-06-29"
  summary: "Combined per-section editing hub. DRAFT-GATHER-POLISH-CHECK lifecycle with 4 phases (6 tracks). Dual status strip (paper + section). Per-stage _PROBE/ folders with cross-paper index."
  changelog:
    - "2.1.0 (2026-06-29): renamed phases PLAN→DRAFT, WRITE→POLISH (DRAFT includes draft sentences, POLISH is venue-quality rewrite not cold-start). Added dual status strip (paper-level + section-level). Added section dashboard showing all sections' layer status. Per-stage _PROBE/ folders with 1-probe-plans/ as cross-paper index. Added _EVIDENCE_ for claims, _DISPLAY_ for narrative."
    - "2.0.0 (2026-06-29): combined haipipe-paper-editing + haipipe-paper-edit into one skill."
    - "1.4.0-1.0.0: see prior changelog."
  predecessors:
    - "haipipe-paper-editing (1-lifecycle/, scaffold hub) — MERGED"
    - "haipipe-paper-edit (3-write-edit/, edit cycle orchestrator) — MERGED"
---

Skill: haipipe-paper-section-edit
==================================

Combined per-section editing hub. Owns the full per-section lifecycle from
scaffold creation through final checklist. Each section the user wants to
work on gets a folder under `0-lifecycle/5-editing/` with four files.
Dispatches to layer workers in `gather/`, `polish/`, `check/` for execution.

```
/haipipe-paper-section-edit                     -> dashboard (all sections + layer status)
/haipipe-paper-section-edit <section>           -> open or create scaffold for that section
/haipipe-paper-section-edit log <section>       -> show recent changelog entries
/haipipe-paper-section-edit lesson [section]    -> SUBAGENT: harvest venue norms into venue pack
/haipipe-paper-section-edit digest [section]    -> SUBAGENT: summarize session changes into _LOG
/haipipe-paper-section-edit feedback [section]  -> SUBAGENT: capture corrections as memory files
```

## Four phases (DRAFT → GATHER → POLISH → CHECK)

Each section progresses through four phases. Not all gather tracks are needed
for every section (e.g., pure theory may skip values/display).

```
Phase    What it does                             Where it lives
───────  ───────────────────────────────────────  ─────────────────────────
DRAFT    what to say: paper structure, section     z-structure scaffold +
         structure (¶ count, H placement), and     N-section.md
         draft sentences (content decisions)

GATHER   what to reference (3 parallel tracks):
  display   figures/tables for this section       → 0-displays/ units
  values    every number, source, verified?       _VALUES_N-section.md
  citation  what's cited where, journal tier      _CITATION_N-section.md

POLISH   how to say it well: rewrite draft        → dispatched to polish/ workers
         sentences to venue quality, weaving in
         gathered citations/values/displays

CHECK    did we get it right: final verification  → dispatched to check/ workers
```

DRAFT = what to say (content decisions, including draft sentences)
GATHER = what to reference (evidence collection via probes)
POLISH = how to say it well (the draft sentences exist; polish rewrites them to venue quality)
CHECK = did we get it right (verification)

Progression gates:
- Draft settled? → then gather (display + values + citation in parallel)
- Gathered? → then polish (rewrite draft sentences with gathered materials woven in)
- Polished? → check
- All settled? → sync to tex → compile

Discovery and task are MECHANISMS feeding the gather phase: discovery finds
citations, task produces figures and numbers. They route through per-stage
`_PROBE/` folders.

**Format rule**: paper-level argument documents (seed, claims, pitch, narrative)
are markdown + _LOG only. The display stage is the ONLY paper-level stage that
compiles to .tex + PDF (you need to SEE rendered figures/tables). Section-level
prose syncs to .tex at the end of the per-section lifecycle (after all layers
settled). Rule of thumb: if you need to SEE it rendered, .tex. If you need to
READ it, .md.

## Dual status strip

Every reply shows TWO strips: paper-level progress AND section-level progress.

```
── 📄 paper · section-edit · §3-theory 🔥 ────────
status:        ok
paper_root:    <path>
section:       3-theory
phase:         gather / citation
next:          <next action>
─────────────────────────────────────────────────────
paper:  seed ✅  claims ✅  pitch ✅  narrative ✅  display ✅  →  section-edit 🚀  →  review ⬜
§3:     draft ✅  │  display --  values --  citation 🚀  │  polish ⬜  │  check ⬜
```

Strip markers:
- ✅ complete (user confirmed)
- 🚀 current (frontier)
- ⬜ not started
- ⚠️ done but needs re-sync
- -- skipped (not applicable for this section type)

How to derive status from disk:
- draft ✅ if outline has structure block with ¶ counts AND narrative sentences
- display ✅ if no displays needed (--) OR displays linked in 0-displays/
- values ✅ if no values needed (--) OR _VALUES_ all verified
- citation ✅ if _CITATION_ all placed and density >= venue norm
- polish ✅ if prose polished and user confirmed
- check ✅ if _LOG has a checklist entry

## Dashboard (no-arg mode)

When invoked without a section argument, show all sections' layer status:

```
/haipipe-paper-section-edit

§   Section         DRAFT   GATHER                       POLISH  CHECK
──  ──────────────  ──────  ─────────────────────────────  ──────  ─────
§1  introduction    draft✅  display⬜  values⬜  citation⬜  polish⬜  check⬜
§2  literature      draft✅  display⬜  values⬜  citation⬜  polish⬜  check⬜
§3  theory          draft✅  display--  values--  citation🚀  polish⚠️  check⬜
§4  measurement     draft✅  display⬜  values⬜  citation⬜  polish⬜  check⬜
§5  empirical       draft⬜  display⬜  values⬜  citation⬜  polish⬜  check⬜
§6  results         draft⬜  display⬜  values⬜  citation⬜  polish⬜  check⬜
§7  discussion      draft⬜  display⬜  values⬜  citation⬜  polish⬜  check⬜

-- = skipped (not applicable for this section)
```

## Per-stage tracking files

Each stage is self-contained with its own tracking files.

```
Paper-level stages (0-lifecycle/):

  0-seed/
    0-seed.md + _LOG                                (no tracking files)

  1-pitch/
    1-pitch.md + _LOG                               (no tracking files)

  2-claims/
    2-claims.md + _LOG
    _EVIDENCE_2-claims.md      what evidence backs each claim
    _PROBE/                    probe plans spawned by claim gaps

  3-narrative/
    3-narrative.md + _LOG
    _DISPLAY_3-narrative.md    which display unit serves each beat
    _PROBE/                    probe plans spawned by narrative needs

  4-display/
    4-display.tex + pdf        (the ONLY compiled stage)
    _LOG_4-display.md
    _PROBE/                    probe plans spawned by display needs

Section-level stages (0-lifecycle/5-editing/):

  z-structure/
    z-structure.md + _LOG                           (no tracking files)

  {section}/
    {section}.md               outline (draft: structure + narrative + sentences)
    _LOG_{section}.md          changelog (all layers)
    _CITATION_{section}.md     citation map (citation)
    _VALUES_{section}.md       values registry (values)
    _PROBE/                    probe plans spawned by this section
```

Tracking files are created lazily when the layer becomes active.

**Probe plan convention**: probe plans LIVE in the `_PROBE/` subfolder of the
stage that spawned them. `1-probe-plans/README.md` is a cross-paper INDEX
(links to per-stage `_PROBE/` folders). When creating a new probe plan: add the
file to the stage's `_PROBE/` folder AND add a row to the index.

## Phase workers (in 2-section-edit/)

This skill dispatches to workers organized by phase:

```
2-section-edit/                      section-level skills (haipipe-paper-section-edit-*)
  haipipe-paper-section-edit/        ← THIS SKILL (combined hub)
  gather/                             gather workers (one skill per working doc)
    ...-section-edit-display                display  0-displays/ units
    ...-section-edit-values                 values   _VALUES_.md
    ...-section-edit-citation               citation _CITATION_.md
  polish/                             polish workers
    ...-section-edit-write                  fresh draft from outline
    ...-section-edit-write-conference       conference style
    ...-section-edit-write-scientific       scientific style
    ...-section-edit-write-systems          systems style
    ...-section-edit-content                content review (WHAT sentences say)
    ...-section-edit-humanizer              de-AI audit (HOW sentences sound)
    ...-section-edit-weaving                paragraph flow (HOW paragraphs connect)
    ...-section-edit-results-revision       results-specific revision
  check/                              check workers
    ...-section-edit-proof-checker          proof verification
  tools/
    ...-section-edit-diagram                paragraph-level ASCII diagrams
  sections/                           per-section playbooks
  scripts/                            section-level utilities
  _shared/                            contracts (comment-protocol, sentence-format, etc.)

3-build-submit/                      whole-paper skills (haipipe-paper-edit-*)
  haipipe-paper-edit-claim-audit            claims traceable to evidence
  haipipe-paper-edit-consistency            terms, \label/\ref, notation
  haipipe-paper-edit-format                 venue style, headings, units
  haipipe-paper-edit-typeset                widows, orphans, overfull
  haipipe-paper-edit-reviewer               mock journal reviewer
  haipipe-paper-edit-submission-audit       final submission check
  haipipe-paper-edit-diffpdf                tracked-changes PDF
  haipipe-paper-edit-improve-loop           autonomous improve loop
  haipipe-paper-edit-optimizer              claim/evidence optimizer
  haipipe-paper-edit-to-overleaf            Overleaf sync
```

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
- User inline comments as `> JL: comment text`.

## _CITATION_ and _VALUES_ specs

See the file format examples in the dashboard. Status values:
- _CITATION_: `✅ placed`, `pending`, `⚠️ missing from .bib`, `⚠️ WRONG paper`
- _VALUES_: `✅ verified`, `pending`, `⚠️ needs recompute`

## _LOG changelog

Newest entry at top. Format: `## YYYY-MM-DD #N ~HH:MM` + JL quote + bullet changes.

## Workflow

### DRAFT

1. **Consult venue**: read `_venue/playbook-<pack>/style-profile.md` for general venue norms. Then resolve the per-section style guide:
   - From `STATUS.md venue:` extract the outlet (e.g., "MISQ 2026" → outlet "MISQ", pack "playbook-utd-is")
   - Map the current section type to the outlet dir suffix (abstract→abstract, introduction→introduction, theory→theory, methods→methods, results→results, discussion→discussion, related-work→related-work, theory-model→theory-model)
   - Read `_venue/playbook-<pack>/<outlet>/<outlet>-<section>/style.md` if it exists
   - This file contains word budget, arc, signature moves, exemplar sentences, anti-patterns, and paragraph structure mined from real papers. It OVERRIDES the general style-profile.md for this specific section.
   - Example: editing MISQ theory → read `_venue/playbook-utd-is/MISQ/MISQ-theory/style.md`
   - Example: editing NMI results → read `_venue/playbook-nature-portfolio/NMI/NMI-results/style.md`

2. **Create scaffold**: folder + outline + _LOG. Populate from existing tex if available.

3. **Settle structure**: subsections, paragraph count, hypothesis placement.

4. **Settle narrative**: paragraph headlines, previews, and draft sentences. The draft sentences capture content decisions (what each sentence says), not polished prose.

### GATHER (parallel via probes)

5. **Display**: identify figures/tables for this section. Link to `0-displays/` units.

6. **Values**: create `_VALUES_` file. Trace numbers to sources. PP probe for unverified values.

7. **Citation**: create `_CITATION_` file. Count density vs venue norm. PP probe for gaps → Scholar search list for user verification. Prefer top-tier journals.

### POLISH

8. **Polish**: rewrite draft sentences into venue-quality prose, weaving in gathered displays, values, and citations. Dispatch to `polish/` workers for de-AI voice, venue style, comment-first annotation cycle.

The comment-first protocol:
- Round 1: insert `%% {CC-<topic>-vMMDD}: finding` comments, change NO prose
- Human replies: `========> {JL vMMDD}: accept|reject|modify|discuss`
- Apply round: act on accepted comments only

### CHECK

9. **Check**: dispatch to `check/` workers. Verify displays referenced, values sourced, assertions cited, venue style matched. Log result in _LOG.

### Sync + Compile

10. **Sync to tex**: when all phases settled, update `0-sections/*.tex` with `Pn.Sn` markers.

11. **Compile**: run `./1-compile.sh`.

## Venue norm digestion

Section-type norms learned during editing flow into the venue pack:

1. Captured in `_LOG` during editing.
2. `lesson` subagent harvests norms → per-section `style.md` at `_venue/playbook-<pack>/<outlet>/<outlet>-<section>/style.md`.
3. Each outlet accumulates its own section-level style guides across papers (e.g., `MISQ/MISQ-theory/style.md`, `NMI/NMI-results/style.md`).
4. Future sessions consult the per-section style guide at draft phase, supplementing the general `style-profile.md`.
5. The per-section files are mined from real exemplar PDFs stored in `_WorkSpace/HAIToolLib/1-ExemplarLib/<family>/<outlet>/`. See `_venue/_SCHEMA.md` for the full resolution path and section-type mapping.

## Subagent verbs: lesson, digest, feedback

Dispatch to background subagents via the Agent tool. Never run inline.

- **lesson**: harvest venue norms and structural decisions from _LOG → venue pack.
- **digest**: summarize session changes into _LOG from outline + tex + git diff.
- **feedback**: capture corrections and preferences as memory files.

The caller MUST include concrete file paths and context in the Agent prompt.

## Relation to other skills

```
haipipe-paper-lifecycle (orchestrator)
  ├─► seed → claims → pitch → narrative → display
  └─► section-edit (this skill)
        │
        │   DRAFT → GATHER → POLISH → CHECK
        │
        │   DRAFT (this skill directly):
        ├── draft                     z-structure + outline (structure + narrative)
        │
        │   GATHER (one skill per working doc, each: AUDIT→SEARCH→CANDIDATE→[HUMAN]→PLACE→REVIEW):
        ├── display                   gather/section-edit-display (0-displays/)
        ├── values                    gather/section-edit-values (_VALUES_.md)
        ├── citation                  gather/section-edit-citation (_CITATION_.md)
        │
        │   POLISH (via polish/ workers):
        ├── polish                    section-edit-content (WHAT)
        │                             section-edit-humanizer (HOW: de-AI)
        │                             section-edit-weaving (HOW: flow)
        │                             section-edit-write (fresh draft)
        │
        │   CHECK (section-level):
        └── check                     section-edit-proof-checker
                                      (whole-paper checks → 3-build-submit/)
```
