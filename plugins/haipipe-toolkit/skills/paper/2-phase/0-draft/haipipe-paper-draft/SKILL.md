---
name: haipipe-paper-draft
description: "DRAFT phase worker (internal). Called by stage skills to produce the first-pass artifact. Reads the stage's artifact spec (from 1-lifecycle/) to know WHAT the result should look like, then runs the generic drafting process: consult upstream → settle structure → draft content → iterate with user → confirm. Users invoke stage skills (seed, claims, pitch...), not this skill directly."
argument-hint: "[stage-or-section] [paper-path]"
allowed-tools: Bash, Read, Write, Edit, Grep, Glob, WebSearch, WebFetch
metadata:
  version: "3.9.0"
  last_updated: "2026-07-10"
  summary: "DRAFT phase worker (internal). Called by stage skills to produce first-pass artifacts. Generic process, stage-specific output. v3.9: citations are REAL \\citep{} keys grepped from the paper's .bib, \\cite{TOADD} when missing (supersedes [CITE:]/(Author Year)). v3.7: section drafts are REAL prose (complete sentences, {VAL:?} placeholders) per the stage's template; DRAFT ends at a hard STOP for the user's structure review (the stage logs the [GATE]). v3.4: inline WebSearch = drafting fuel only, never durable evidence."
  # version history: ./CHANGELOG.md (skill-scoped, never loaded at invocation)
---

Skill: haipipe-paper-draft (internal phase worker)
====================================================

DRAFT phase worker. Called by stage skills (seed, claims, pitch, narrative, display, section-edit) to produce the first-pass artifact. The stage defines WHAT the result looks like (artifact spec in `1-lifecycle/`). This skill defines HOW to get there.

**Not user-facing.** Users invoke stage skills:
```
/haipipe-paper seed       → seed skill calls this internally for DRAFT phase
/haipipe-paper claims     → claims skill calls this internally for DRAFT phase
/haipipe-paper section-edit §3  → section-edit skill calls this internally
```


## What DRAFT means

DRAFT = settle WHAT to say. The first pass at producing a stage's artifact. For argument docs (seed, claims, pitch, narrative) that means content decisions in working prose. For SECTIONS it means a REAL draft — complete academic sentences close to submission register, with real `\citep{key}` citations for keys already in the paper's .bib and `{VAL:?}` / `\cite{TOADD}` placeholders for everything unverified — because the user reviews structure by reading real prose, not a skeleton. In both cases: content-complete, unverified, unpolished (polish is REVISE's job).

Each stage has its own artifact spec (in `1-lifecycle/{stage}/haipipe-paper-{stage}/SKILL.md`) that defines:
- What files to produce
- What content structure to follow
- What done-criteria to meet
- Which DPRC phases apply

DRAFT reads that spec and produces the artifact.


## The generic drafting process

Same process for every stage, different content:

### Step 1. Identify the stage and read its artifact spec + template

Determine which stage is being drafted, then read TWO things from `1-lifecycle/`: the stage's SKILL.md artifact spec (WHAT to produce, done-criteria) and the stage's canonical template (section order, placeholders). This skill carries NO templates of its own -- the stage owns its format.

| Stage | Artifact spec | Template |
|---|---|---|
| seed | `1-lifecycle/0-seed/haipipe-paper-seed/SKILL.md` | `ref/seed-template.md` |
| claims | `1-lifecycle/1-claims/haipipe-paper-claims/SKILL.md` | `ref/claims-template.md` |
| pitch | `1-lifecycle/2-pitch/haipipe-paper-pitch/SKILL.md` | `ref/pitch-template.md` |
| narrative | `1-lifecycle/3-narrative/haipipe-paper-narrative/SKILL.md` | `ref/narrative-template.md` |
| display | `1-lifecycle/4-display/haipipe-paper-display/SKILL.md` | `ref/display-template.md` (unit contracts live in the same `ref/`) |
| section name (e.g. `introduction`) | `1-lifecycle/5-section-edit/haipipe-paper-section-edit/SKILL.md` | `ref/outline-format.md` |

(Template paths are relative to each stage skill's OWN folder — the same folder as its SKILL.md, e.g. `1-lifecycle/0-seed/haipipe-paper-seed/ref/seed-template.md`.)

### Step 2. Consult upstream artifacts

Each stage reads from its predecessors:

| Drafting... | Read upstream |
|---|---|
| seed | nothing (seed is the root) |
| claims | seed |
| pitch | seed + claims + venue |
| narrative | seed + claims + pitch |
| display | narrative + claims |
| section | z-structure + narrative + claims + section-type + venue (2-venue.md) |

**Venue guard.** For venue-ALIGNED stages (pitch, narrative, display, section), resolve the venue before drafting:

1. No `venue:` pinned in STATUS.md -> **STOP with an error**. Report `status: blocked` and tell the user to run `/haipipe-paper venue` first. Never draft a venue-ALIGNED artifact against an invented venue.
2. Venue pinned and the paper's `0-lifecycle/2-venue/2-venue.md` exists -> **read it FIRST** (the venue stage's compiled doc): Writing Principles + the Structural Blueprint block for the artifact being drafted. Direct `_venue/` pack reads are deep dives only, following the `[source: ...]` tags recorded there.
3. `2-venue.md` absent (venue stage not run) -> fall back to the pinned pack directly. No matching `_venue/playbook-*` pack either -> **STOP with an error**. Name the pinned venue, list available packs, ask the user to fix the pin, add a pack, or run `/haipipe-paper venue`.
4. Fallback pack exists but lacks the per-section style file -> **proceed with a visible warning**: use the pack's general style-profile, flag the missing file in the draft output and `_LOG`, and surface it again in the CHECK report. Never silently invent word budgets or structure norms.

Venue-FREE stages (seed, claims) skip this guard entirely.

### Step 3. Settle structure

Present the structural plan to the user before writing content:
- **seed**: the three sections (question, motivations, claim shape)
- **claims**: the hypothesis list and claim matrix layout
- **pitch**: the cover letter sections (hook, finding, so-what, editor's chair)
- **narrative**: the section blocks and story beats
- **display**: the figure/table inventory (+ the probe-plan rows it implies)
- **section**: the paragraph skeleton (how many subsections, how many paragraphs, what job each does)

### Step 4. Draft content

Fill in the structure with first-pass content:
- Write to settle WHAT is being said, not HOW it sounds
- Argument docs: working prose. Sections: REAL prose per the stage's template (`ref/outline-format.md`) — complete sentences, one per line, blank line between
- Citations real, never guessed: grep the paper's .bib (and `_CITATION_`) FIRST and write `\citep{key}` for keys that exist; `\cite{TOADD}` (+ a `_CITATION_` row naming the topic) where no key fits; `{VAL:? <what>}` for unverified numbers. A key that does not grep in .bib is an invented citation
- Never invent a number or citation to avoid a placeholder
- One idea per sentence

**Inline WebSearch is ALLOWED here -- as drafting fuel, NOT as evidence.**
DRAFT may search the web to orient (is this field crowded? does a dataset
exist? who are the anchor names?) and to sharpen the draft. But a seed is
allowed to be intuition (seed principle 1), so what that search produces has
exactly two legal destinations:
1. **PROSE** in the stage artifact (Motivations, Claim Shape, ...) -- phrased
   as orientation, with `\cite{TOADD}` slots, never as settled fact.
2. **BUFFERED probe plans** -- when the search reveals a gap the paper must
   later verify, write it as a PP-card SKELETON (Need / Why / Route, `status:
   planned`, EMPTY `refs:`) in `_PROBE/` + an index row, per the buffer
   convention `../../1-probe/haipipe-paper-probe/` reads. This HANDS the gap to
   the PROBE phase; it does not answer it.

FORBIDDEN in DRAFT: writing findings, `refs:`, or takeaways INTO a PP card, or
treating an inline result as a landed probe. Inline search results have no
project-side ledger -- per the probe contract, evidence gathered any way other
than the PROBE-phase orchestrator dispatch means "the PROBE phase did not
happen." The line is the CARD STATE: DRAFT leaves `status: planned` skeletons;
only PROBE flips them to `read` with resolving `discoveries/` refs. The CHECK
gate runs `check-probe-cards.sh` and cannot go green over planned/empty-ref
cards -- so DRAFT search can never masquerade as evidence.

### Step 5. ⛔ STOP — present for review, then iterate

Writing done → STOP and end the turn: present the draft (structure + where the placeholders are) and hand the floor to the user. The user reviews STRUCTURE and adds `> USER:` comments. Respond with `> CC:` underneath each (never delete or reword a user comment). Iterate until the user advances. Do NOT start PROBE, REVISE, or any commit on your own — the user's verb/"go" is the gate.

### Step 6. Confirm and hand off

When the user approves:
1. Move resolved comment threads to `_LOG` (if applicable)
2. Write a draft phase summary entry to `_LOG` + the `[GATE] draft-review: approved` line quoting the user
3. Mark draft ✅
4. Hand off to PROBE (or skip to REVISE if PROBE is n/a for this stage — logged verdict required)


## Stage-specific notes

### seed
- Output: `0-lifecycle/0-seed/0-seed.md`
- WebSearch-to-orient + buffer rule: see Step 4 (the one normative home); seed's
  buffered probes are the FEASIBILITY pair (novelty + external-data-obtainable).
- PROBE (seed): FEASIBILITY only -- "can this paper exist at all?" (is it
  novel? does the external labeled data exist?). Profiling OUR OWN data is
  claims-stage task work; register it as a `[FORWARD -> CLAIMS]` pointer in
  `_LOG`, do not dispatch it in seed. The claims stage CONSUMES these pointers
  at its open (reader clause in haipipe-paper-claims SKILL) -- an unconsumed
  pointer fails the claims done-criteria.
- Short document: seed question + motivations + tentative claim shape

### claims
- Output: `0-lifecycle/1-claims/1-claims.md`
- On open: grep seed `_LOG` for `[FORWARD -> CLAIMS]` pointers; each becomes a
  PP entry in the Probes section (or is explicitly declined in `_LOG`)
- PROBE: link evidence sources, spawn probes for GAPs
- Hypotheses are venue-neutral (H1, H2, H3)

### pitch
- Output: `0-lifecycle/2-pitch/2-pitch.md`
- PROBE: citation audit for anchor papers
- Venue-ALIGNED: reads the venue stage's 2-venue.md (pack fallback per the venue guard)

### narrative
- Output: `0-lifecycle/3-narrative/3-narrative.md`
- PROBE: citation + display needs per beat
- Section-mirrored story with readiness tags

### display
- Output: `0-lifecycle/4-display/4-display.md` (the BRAIN; `4-display.tex` is GENERATED from it by sync at REVISE — never drafted by hand); template `ref/display-template.md`
- DRAFT runs the stage's step-0 reconcile first (legacy probes/preview/tex-comments merge), then authors the md: Venue Set, Display Map, PROBE PLAN (S0/En/Rn rows, ▶ ready / ✋ gated-on-thread), one block per display with method candidates + ASCII sketch
- The ⛔ STOP presentation = the open threads + the Probe Plan; the user rules on threads and strikes rows; DRAFT proposes, PROBE executes after the gate (the display twin of section-edit's "Probes proposed by this draft" block)
- PROBE: step-0 cross-stage coverage sweep, then evidence lane (tasks/probes) + render lane (renderer skills, candidate mode) over the approved plan rows

### section-edit
- Output: `0-lifecycle/5-section-edit/{section}/{section}.md`
- Format: REAL prose per `ref/outline-format.md` in section-edit hub
- Ends with the "Probes proposed by this draft" block: every {VAL:?}/\cite{TOADD} rolled up with its expected source, display needs per paragraph, heavier needs (new task run, lit sweep) BUFFERED as planned PP skeletons in `_PROBE/` + index row. DRAFT proposes; PROBE executes after the gate. The STOP presentation includes this block.
- PROBE: citation + values + display (three parallel tracks)
- Reads section-type norms and 2-venue.md's per-section blueprint block for style (pack fallback per the venue guard)


## Where style guidance lives (NOT here)

DRAFT settles content, not style. Style inputs come from elsewhere:

| Guidance | Lives in | Used by |
|---|---|---|
| Venue style, word budget, arc | `0-lifecycle/2-venue/2-venue.md` (compiled from `_venue/playbook-<pack>/`; pack = fallback / deep dive) | DRAFT reads budget; REVISE applies style |
| Per-section structure norms | `1-lifecycle/5-section-edit/section-type/` | DRAFT (structure) |
| Prose quality rules | `2-phase/REF/prose-quality.md` | REVISE |

Old venue LaTeX templates and the write-conference/scientific/systems style skills were archived to the paper-root `_archive/` (venue knowledge belongs in `_venue/` packs).


## Relation to other phases

```
DRAFT (this)  →  PROBE   →  REVISE  →  CHECK
settle WHAT       collect     settle     verify
to say            evidence    HOW to     everything
                              say it
```

DRAFT produces the first-pass artifact. If the content is WRONG, fix it in DRAFT. If the content is RIGHT but sounds bad, fix it in REVISE.


## Who calls this skill

Stage skills call this as their DRAFT phase:

| Stage skill | What this skill drafts |
|---|---|
| haipipe-paper-seed | 0-seed.md (3 sections) |
| haipipe-paper-claims | 1-claims.md (hypothesis list + evidence matrix) |
| haipipe-paper-pitch | 2-pitch.md (cover letter) |
| haipipe-paper-narrative | 3-narrative.md (story beats) |
| haipipe-paper-display | 4-display.md (display map + probe plan + per-display blocks with candidates) |
| haipipe-paper-section-edit | {section}.md (paragraph outline) |

## Sibling phase workers

| Phase | Worker | Called after |
|---|---|---|
| DRAFT (this) | haipipe-paper-draft | -- |
| PROBE | haipipe-paper-probe | DRAFT |
| REVISE | haipipe-paper-revise | PROBE |
| CHECK | haipipe-paper-check | REVISE |
