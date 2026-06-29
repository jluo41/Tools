---
name: haipipe-paper-editing
description: "Per-section editing scaffolds under 0-lifecycle/5-editing/. Each section gets a folder with four files: outline-narrative .md (structure + content), _LOG changelog, _CITATION_ citation map, and _VALUES_ values registry. Seven editing layers per section: (1) paper structure, (2) section structure, (3) content, (4) discovery, (5) task, (6) citation, (7) values. Venue-aware, outline-first, with citation density and values verification gates. Trigger: editing, section scaffold, outline narrative, edit section, 5-editing, /haipipe-paper-editing."
argument-hint: "[section-name-or-number] [paper-path]"
allowed-tools: Bash, Read, Write, Edit, Grep, Glob, Skill, Agent
metadata:
  version: "1.3.0"
  last_updated: "2026-06-29"
  summary: "Per-section editing scaffolds (outline + _LOG + _CITATION_ + _VALUES_) under 0-lifecycle/5-editing/. Seven editing layers: paper structure, section structure, content, discovery, task, citation, values. Venue-aware, outline-first workflow, citation density + values verification gates. Subagent verbs: lesson, digest, feedback."
  changelog:
    - "1.3.0 (2026-06-29): added _VALUES_ file as fourth standard scaffold companion; documented 7-layer editing model (structure-paper, structure-section, content, discovery, task, citation, values); layers 4+5 route to probe plans; updated workflow to reflect layered progression; updated relation-to-other-skills map."
    - "1.2.0 (2026-06-29): added _CITATION_ file as standard scaffold companion; venue consultation step; citation density gate; outline-first workflow (no tex sync before user confirms outline); Scholar search list as citation discovery output."
    - "1.1.0 (2026-06-26): added lesson/digest/feedback subagent verbs; these dispatch to background Agent, never run inline."
    - "1.0.0 (2026-06-26): created from live MISQ literature editing session."
---

Skill: haipipe-paper-editing
=============================

Per-section editing scaffolds that bridge lifecycle planning and prose
writing. Each section the user wants to work on gets a folder under
`0-lifecycle/5-editing/` with four files: an outline-narrative, a
changelog, a citation map, and a values registry. This replaces minimap
as the final lifecycle stage.

```
/haipipe-paper-editing                          -> dashboard (list sections, show status)
/haipipe-paper-editing <section>                -> open or create scaffold for that section
/haipipe-paper-editing log <section>            -> show recent changelog entries
/haipipe-paper-editing lesson [section]         -> SUBAGENT: harvest what we learned (venue norms, structural decisions, exemplar patterns)
/haipipe-paper-editing digest [section]         -> SUBAGENT: summarize session changes into the _LOG
/haipipe-paper-editing feedback [section]       -> SUBAGENT: capture corrections and preferences as memory files
```

## Seven editing layers

Each section progresses through seven layers. Not all layers are needed for
every section (e.g., a pure-theory section has no values), but the progression
is roughly top-to-bottom. Layers 1-3 live in the outline file. Layers 4-5
route to `1-probe-plans/` as PP probes. Layers 6-7 have dedicated tracking files.

```
Layer                  What it does                          Where it lives
─────────────────────  ────────────────────────────────────  ─────────────────────────
1. Structure of paper  how many sections, what order          z-structure scaffold
2. Structure of section  subsections, ¶ count, H placement   N-section.md (structure block)
3. Content of section  narrative sentences, prose quality     N-section.md (body)
4. Discovery of section  literature/evidence needed           → PP probe → /haipipe-discovery
5. Task of section     data/computation needed                → PP probe → /haipipe-task
6. Citation of section  what's cited where, journal tier      _CITATION_N-section.md
7. Values of section   every number, source, verified?        _VALUES_N-section.md
```

Progression gates:
- Structure settled? → then content
- Content settled? → then discovery + task (can run in parallel)
- Discovery done? → then citation
- Task done? → then values
- All settled? → sync to tex → compile

## Folder structure

```
0-lifecycle/5-editing/
  z-structure/                              layer 1 (paper-level)
    z-structure.md
    _LOG_z-structure.md
  1-introduction/                           layers 2-7 per section
    1-introduction.md              outline-narrative (layers 2+3)
    _LOG_1-introduction.md         changelog (all layers)
    _CITATION_1-introduction.md    citation map (layer 6)
    _VALUES_1-introduction.md      values registry (layer 7)
  2-literature/
    2-literature.md
    _LOG_2-literature.md
    _CITATION_2-literature.md
    _VALUES_2-literature.md
  3-theory/
    3-theory.md
    _LOG_3-theory.md
    _CITATION_3-theory.md
    _VALUES_3-theory.md
  ...
```

Each folder is one section that the user wants to treat as a unit.
The numbering and naming are flexible per the user's choice.
The four files are: outline (structure + content), _LOG (what changed and why),
_CITATION_ (what's cited where), _VALUES_ (every number and its source).
Create files lazily: _CITATION_ and _VALUES_ are added when those layers
become active, not on initial scaffold creation.

## Outline-narrative file

The outline-narrative is the working document for one section, at the **paragraph level**. Each paragraph is a unit with its own job.

The file starts with a **structure overview** block at the top, showing all subsections and paragraphs with sentence counts at a glance. This is the first thing you see when opening the file.

```markdown
# Section N: Title — Structure

\```
§N.1 Subsection Title (K ¶)
  P1. Short paragraph job description                        N sentences
  P2. Short paragraph job description                        N sentences

§N.2 Subsection Title (K ¶)
  P3. Short paragraph job description                        N sentences
  ...
\```

---

## §N.1 Subsection Title

### P1. What this paragraph does (one-line job description)

(Semicolon-separated preview of key points in this paragraph.)

Narrative sentence one.

Narrative sentence two.

### P2. What the next paragraph does

(Preview.)

Narrative sentence one.

...
```

Rules:
- **Structure overview at top**: `# Section N: Title — Structure` followed by a code block listing all subsections and paragraphs with sentence counts. Update this block whenever the structure changes.
- `##` for subsections within the section.
- `###` for each paragraph within a subsection.
- Each paragraph gets: headline (its job), parenthetical preview, narrative sentences.
- One narrative sentence per line (these become the paragraph sentences in tex, marked with `Pn.Sn`).
- Target 5-6 sentences per paragraph (MISQ/ISR norm from exemplar analysis).
- User adds inline comments as `> JL: comment text`.
- Agent addresses comments, then removes the `> JL:` line once resolved.

## _CITATION_ citation map

Tracks every citation in the section: what paper, where it's placed, what it says, and whether it's verified. One file per section, organized by paragraph.

```markdown
# §N Title: Citation Map

Current: X citations / Y sentences (Z). Target: ~0.50 (venue norm).

## By paragraph

### P1. Paragraph headline (K sentences)

| Sn | Assertion | Key | Journal | Status | Summary |
|----|-----------|-----|---------|--------|---------|
| S2 | what the sentence claims | bibtex_key | JPSP | ✅ placed / pending / ⚠️ fix | one-line: what the paper says |

## Status summary

| Status | Count |
|--------|-------|
| ✅ placed | N |
| pending | N |
| ⚠️ fix needed | N |
```

Rules:
- One row per citation placement (a paper cited at two sentences gets two rows).
- Status: `✅ placed` (in bib + tex), `pending` (need Scholar verification + bib entry), `⚠️ missing from .bib`, `⚠️ WRONG paper in .bib`.
- Summary: one line describing what the paper says and why it supports this sentence.
- Update status as citations are verified and placed.
- When citation gaps are found, create a probe plan (PP) in `1-probe-plans/` for discovery.

## _VALUES_ values registry

Tracks every concrete number in the section: statistics, sample sizes,
percentages, effect sizes, thresholds. Each value is linked to its source
(task output, probe result, paper table, external report) and marked as
verified or pending. One file per section, organized by paragraph.

```markdown
# §N Title: Values Registry

## By paragraph

### P1. Paragraph headline

| Sn | Value | What it is | Source | Status |
|----|-------|-----------|--------|--------|
| S3 | N = 746,328 | LBP analytic sample size | C01 case pipeline log | ✅ verified |
| S5 | 49% | physicians with score >= 0.75 | trait distribution table | pending |

## Status summary

| Status | Count |
|--------|-------|
| ✅ verified | N |
| pending | N |
| ⚠️ needs recompute | N |
```

Rules:
- One row per number that appears in the section prose.
- Source: where the number comes from (task output path, table, log file, external paper).
- Status: `✅ verified` (traced to source, confirmed), `pending` (stated but not traced), `⚠️ needs recompute` (source changed or value is stale).
- Sections with no concrete numbers (e.g., pure theory) may skip this file.
- When unverified values are found, create a probe plan (PP) in `1-probe-plans/` for verification (e.g., PP04 for §4 measurement numbers).
- Values from PHI sources: record the source path but note "server-only" -- do not paste raw PHI data into this file.

## _LOG changelog

Simple changelog, newest entry at top. Each entry:

```markdown
## YYYY-MM-DD #N ~HH:MM

JL (source): "user's comment verbatim"
- Change one.
- Change two.
```

Rules:
- Newest at top.
- Number entries sequentially within a date (#1, #2, ...).
- Add timestamp (~HH:MM) when available.
- Log JL's comments that triggered changes. Source = where the comment came from: `(outline L1)`, `(tex P3.S2)`, `(chat)`. Quote the comment.
- Bullet points for changes, as short as possible.
- No commentary, summaries, or "Context:" labels.

## Workflow

The workflow follows the seven layers top-to-bottom. Each layer has a gate:
the user confirms before the next layer begins. Not all layers apply to
every section.

### Layer 1-2: Structure

1. **Consult venue**: read `_venue/playbook-<venue>/style-profile.md` for section-specific writing norms. For example, the theory section has norms on paragraph density (3-6 per subsection, 5-8 sentences), mechanism-derivation structure, hypothesis placement, citation density (~0.50/sentence), and top-journal preference. Apply these norms when building the outline structure.

2. **Create scaffold**: create the folder + outline + _LOG. Populate the outline-narrative from the existing tex if one exists. Add _CITATION_ and _VALUES_ files lazily when those layers become active.

3. **Settle structure**: iterate on subsections, paragraph count, paragraph jobs, and hypothesis placement with the user. The structure overview block at the top of the outline must be stable before moving to content.

### Layer 3: Content

4. **Outline first, tex later**: iterate on narrative sentences paragraph by paragraph. Monitor `> JL:` inline comments and address them. Do NOT sync to tex or compile PDF until the user confirms the outline content is settled. This prevents double-work when user feedback changes the prose.

### Layers 4-5: Discovery + Task (parallel)

5. **Discovery and task needs**: after content is settled, identify what evidence the section needs from outside. Literature gaps → discovery probes. Data/computation gaps → task probes. Create probe plans (PP) in `1-probe-plans/` and dispatch via `/haipipe-paper probe run`. These can run in parallel.

### Layer 6: Citation

6. **Citation density gate**: count citations/sentence and compare to the venue norm (~0.50 for MISQ/ISR). If below target:
   - Create `_CITATION_` file with paragraph-by-paragraph map
   - Identify which sentences need citations (construct definitions, established relationships, clinical/institutional facts; inference and hypothesis statements stay uncited)
   - Create a probe plan (PP) in `1-probe-plans/` for citation discovery
   - Dispatch via `/haipipe-paper probe run`
   - Results produce a Scholar search list (`PP_scholar_search.md`) for user to verify BibTeX manually
   - Update `_CITATION_` file as citations are verified and placed
   - Prefer top-tier journal references when possible (per venue style-profile)

### Layer 7: Values

7. **Values verification gate**: scan every concrete number in the section (sample sizes, effect sizes, percentages, thresholds, p-values). For each:
   - Create `_VALUES_` file with paragraph-by-paragraph registry
   - Trace each number to its source (task output, table, log, external paper)
   - Mark as verified or pending
   - If unverified values are found, create a probe plan (PP) for verification
   - PHI-sourced values: record source path but note "server-only"

### Sync + Compile

8. **Sync to tex**: when the user confirms ALL active layers are settled, update the corresponding `0-sections/*.tex` to match the outline. The tex uses `Pn.Sn` markers per the manuscript convention.

9. **Compile**: run `./1-compile.sh` after tex changes.

## Subagent verbs: lesson, digest, feedback

These three verbs MUST dispatch to a background subagent via the Agent tool. They never run inline in the main session. The main thread stays focused on prose; the subagent reads files, harvests context, and writes outputs independently.

### lesson

Harvest what was learned during this editing session. The subagent reads:
- The outline-narrative and _LOG for the target section
- The venue pack (`_venue/playbook-*/`) if consulted
- Exemplar papers if referenced
- The conversation context (via the prompt)

It produces project-type memories about structural decisions, venue norms, or exemplar patterns that will be useful in future sessions. Example outputs: "MISQ papers don't use standalone Research Gap subsections (from exemplar analysis)" or "L2 should cover communication styles broadly, not just agreeableness definition."

Dispatch pattern:
```
Agent({
  description: "editing lesson harvest",
  prompt: "Read [section scaffold path] and [_LOG path]. Harvest structural decisions, venue norms, and exemplar patterns learned during this editing session. Save each as a project-type memory file under the memory directory. Do NOT save ephemeral task details or things derivable from the code.",
  run_in_background: true
})
```

### digest

Summarize the session's changes into the _LOG changelog. The subagent reads:
- The outline-narrative (current state)
- The corresponding tex file (current state)
- The _LOG (to avoid duplicating existing entries)
- The git diff for the section files

It appends a new _LOG entry with: what changed, what JL comments were addressed, what decisions were made, and what's next. Uses the _LOG format (date, numbered entry, bullet changes).

Dispatch pattern:
```
Agent({
  description: "editing digest to LOG",
  prompt: "Read [outline], [tex], [_LOG], and run git diff on both. Write a new _LOG entry summarizing changes since the last entry. Follow the _LOG format exactly. Do not duplicate existing entries.",
  run_in_background: true
})
```

### feedback

Capture corrections and preferences from this session as memory files. The subagent reads:
- The conversation context (via the prompt, which should include key corrections)
- Existing memory files (to avoid duplicates)

It produces feedback-type memories about how to approach future editing work. Example: "L2 should open with communication styles broadly, not jump straight to agreeableness definition" or "No standalone Research Gap subsection in MISQ; fold gap into last literature stream."

Dispatch pattern:
```
Agent({
  description: "editing feedback capture",
  prompt: "From this editing session, capture the following corrections/preferences as feedback-type memory files: [list the key corrections from the conversation]. Check existing memories first to avoid duplicates. Each memory gets its own file with frontmatter.",
  run_in_background: true
})
```

### Prompt construction for subagents

The caller (main session) MUST include concrete context in the Agent prompt because the subagent has no access to the conversation history. Include:
- File paths to read
- Key decisions or corrections made (summarized from conversation)
- The memory directory path (`/Users/jluo41/.claude/projects/.../memory/`)
- What NOT to save (ephemeral details, things already in the code)

## Relation to other skills

```
haipipe-paper-lifecycle (orchestrator)
  ├─► seed → pitch → claims → narrative → display
  └─► editing (this skill, replaces minimap as stage 5)
        │
        │   7 layers map to skills:
        │
        ├── L1 structure of paper     this skill (z-structure scaffold)
        ├── L2 structure of section   this skill (per-section outline)
        ├── L3 content of section     this skill (narrative sentences)
        │     └─► hands off to 3-write-edit/ for prose polishing:
        │         haipipe-paper-edit-content, -edit-weaving, -edit-write
        ├── L4 discovery of section   → 1-probe-plans/ PP → /haipipe-discovery
        ├── L5 task of section        → 1-probe-plans/ PP → /haipipe-task
        ├── L6 citation of section    this skill (_CITATION_) + haipipe-paper-edit-citation
        └── L7 values of section      this skill (_VALUES_) + haipipe-paper-edit-values
```

The editing scaffold is the HUB that tracks all seven layers per section.
Layers 1-3 and 6-7 are managed directly in the scaffold files. Layers 4-5
route outward to evidence workers via probe plans and return results that
update layers 6-7. The 3-write-edit/ skills handle prose-level polish AFTER
the scaffold layers are settled.
