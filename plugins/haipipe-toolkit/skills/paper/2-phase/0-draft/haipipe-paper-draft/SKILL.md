---
name: haipipe-paper-draft
description: "DRAFT phase worker (internal). Called by stage skills to produce the first-pass artifact. Reads the stage's artifact spec (from 1-lifecycle/) to know WHAT the result should look like, then runs the generic drafting process: consult upstream → settle structure → draft content → iterate with user → confirm. Users invoke stage skills (seed, claims, pitch...), not this skill directly."
argument-hint: "[stage-or-section] [paper-path]"
allowed-tools: Bash, Read, Write, Edit, Grep, Glob
metadata:
  version: "3.3.0"
  last_updated: "2026-07-03"
  summary: "DRAFT phase worker (internal). Called by stage skills to produce first-pass artifacts. Generic process, stage-specific output."
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

DRAFT = settle WHAT to say. The first pass at producing a stage's artifact. Content decisions, not polished prose.

Each stage has its own artifact spec (in `1-lifecycle/{stage}/SKILL.md`) that defines:
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
| seed | `1-lifecycle/0-seed/haipipe-paper-seed/SKILL.md` | `../ref/seed-template.md` |
| claims | `1-lifecycle/1-claims/haipipe-paper-claims/SKILL.md` | `../ref/claims-template.md` |
| pitch | `1-lifecycle/2-pitch/haipipe-paper-pitch/SKILL.md` | `../ref/pitch-template.md` |
| narrative | `1-lifecycle/3-narrative/haipipe-paper-narrative/SKILL.md` | `../ref/narrative-template.md` |
| display | `1-lifecycle/4-display/haipipe-paper-display/SKILL.md` | display-unit contracts in that skill's `ref/` |
| section name (e.g. `introduction`) | `1-lifecycle/5-section-edit/haipipe-paper-section-edit/SKILL.md` | `../ref/outline-format.md` |

(Template paths are relative to each stage skill's folder.)

### Step 2. Consult upstream artifacts

Each stage reads from its predecessors:

| Drafting... | Read upstream |
|---|---|
| seed | nothing (seed is the root) |
| claims | seed |
| pitch | seed + claims + venue |
| narrative | seed + claims + pitch |
| display | narrative + claims |
| section | z-structure + narrative + claims + section-type + venue pack |

**Venue guard.** For venue-ALIGNED stages (pitch, narrative, display, section), resolve the venue before drafting:

1. No `venue:` pinned in STATUS.md -> **STOP with an error**. Report `status: blocked` and tell the user to run `/haipipe-paper venue` first. Never draft a venue-ALIGNED artifact against an invented venue.
2. Venue pinned but no matching `_venue/playbook-*` pack -> **STOP with an error**. Name the pinned venue, list available packs, ask the user to fix the pin or add a pack.
3. Pack exists but lacks the per-section style file -> **proceed with a visible warning**: use the pack's general style-profile, flag the missing file in the draft output and `_LOG`, and surface it again in the CHECK report. Never silently invent word budgets or structure norms.

Venue-FREE stages (seed, claims) skip this guard entirely.

### Step 3. Settle structure

Present the structural plan to the user before writing content:
- **seed**: the three sections (question, motivations, claim shape)
- **claims**: the hypothesis list and claim matrix layout
- **pitch**: the cover letter sections (hook, finding, so-what, editor's chair)
- **narrative**: the section blocks and story beats
- **display**: the figure/table inventory
- **section**: the paragraph skeleton (how many subsections, how many paragraphs, what job each does)

### Step 4. Draft content

Fill in the structure with first-pass content:
- Write to settle WHAT is being said, not HOW it sounds
- Use rough prose, parenthetical citations "(Author Year)" where needed
- Flag uncertain content with `(?)` or `> CC: need to verify`
- One idea per sentence, one sentence per line (for sections)

### Step 5. Iterate with user

The user reads the draft and adds `> USER:` comments. Respond with `> CC:` underneath each. Iterate until content decisions are settled.

### Step 6. Confirm and hand off

When confirmed:
1. Move resolved comment threads to `_LOG` (if applicable)
2. Write a draft phase summary entry to `_LOG`
3. Mark draft ✅
4. Hand off to PROBE (or skip to REVISE if PROBE is n/a for this stage)


## Stage-specific notes

### seed
- Output: `0-lifecycle/0-seed/0-seed.md`
- PROBE: n/a (evidence inventory belongs in claims)
- Short document: seed question + motivations + tentative claim shape

### claims
- Output: `0-lifecycle/1-claims/1-claims.md`
- PROBE: link evidence sources, spawn probes for GAPs
- Hypotheses are venue-neutral (H1, H2, H3)

### pitch
- Output: `0-lifecycle/2-pitch/2-pitch.md`
- PROBE: citation audit for anchor papers
- Venue-ALIGNED: reads the pinned venue's playbook

### narrative
- Output: `0-lifecycle/3-narrative/3-narrative.md`
- PROBE: citation + display needs per beat
- Section-mirrored story with readiness tags

### display
- Output: `0-lifecycle/4-display/4-display.tex` (the ONLY stage with .tex)
- PROBE: route display units to task-folders
- Plan what figures/tables exist, which claims they serve

### section-edit
- Output: `0-lifecycle/5-section-edit/{section}/{section}.md`
- Format: paragraph outline per `ref/outline-format.md` in section-edit hub
- PROBE: citation + values + display (three parallel tracks)
- Reads section-type norms and venue pack for per-section style


## Where style guidance lives (NOT here)

DRAFT settles content, not style. Style inputs come from elsewhere:

| Guidance | Lives in | Used by |
|---|---|---|
| Venue style, word budget, arc | `_venue/playbook-<pack>/` | DRAFT reads budget; REVISE applies style |
| Per-section structure norms | `1-lifecycle/5-section-edit/section-type/` | DRAFT (structure) |
| Prose quality rules | `2-phase/REF/prose-quality.md` | REVISE |

Old venue LaTeX templates and the write-conference/scientific/systems style skills were archived to `2-phase/_archive/` (venue knowledge belongs in `_venue/` packs).


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
| haipipe-paper-display | 4-display.tex (figure/table plan) |
| haipipe-paper-section-edit | {section}.md (paragraph outline) |

## Sibling phase workers

| Phase | Worker | Called after |
|---|---|---|
| DRAFT (this) | haipipe-paper-draft | -- |
| PROBE | haipipe-paper-probe | DRAFT |
| REVISE | haipipe-paper-revise | PROBE |
| CHECK | haipipe-paper-check | REVISE |
