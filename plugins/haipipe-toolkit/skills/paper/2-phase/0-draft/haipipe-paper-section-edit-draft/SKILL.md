---
name: haipipe-paper-section-edit-draft
description: "DRAFT phase of section-edit: settle WHAT each paragraph says, sentence by sentence, in the section outline. Creates/updates {section}.md with structure overview + per-paragraph blocks (heading, preview, JL/CC comments, draft sentences). Draft sentences capture content decisions, not polished prose. Consults section-type for structure norms and venue pack for word budget. Gate: user confirms outline → draft ✅, then GATHER can begin. Trigger: draft section, outline section, settle structure, draft sentences, what to say, /haipipe-paper-section-edit-draft."
argument-hint: "[section-name-or-number] [paper-path]"
allowed-tools: Bash, Read, Write, Edit, Grep, Glob
metadata:
  version: "2.0.0"
  last_updated: "2026-07-02"
  summary: "DRAFT phase worker. Settle what each paragraph says (structure + draft sentences) in the section outline. Content decisions first, polished prose later."
  changelog:
    - "2.0.0 (2026-07-02): complete rewrite. Old skill was a cold-start LaTeX paper generator (ICLR/NeurIPS templates, DBLP bibtex, etc.) -- archived to _archive/SKILL-v1.1.0-cold-start-writer.md. New skill focuses on outline creation: structure + draft sentences per paragraph. Matches the DRAFT phase of DRAFT→GATHER→POLISH→CHECK lifecycle."
    - "1.1.0 (2026-06-05): renamed from paper-write to haipipe-paper-section-edit-write."
    - "1.0.0 (2026-05-31): baseline metadata added."
---

Skill: haipipe-paper-section-edit-draft
========================================

DRAFT phase of `haipipe-paper-section-edit`. Settle WHAT each paragraph says, sentence by sentence, before gathering citations/values/displays or polishing prose.

The working document is `{section}.md` in `0-lifecycle/5-editing/{section}/`.

```
/haipipe-paper-section-edit-draft <section>              → create or open outline
/haipipe-paper-section-edit-draft structure <section>    → settle paragraph structure only
/haipipe-paper-section-edit-draft sentences <section>    → draft sentences for settled structure
```


## What DRAFT means

DRAFT = settle WHAT to say. Each paragraph gets three elements:

```
### P6. IS domain positioning and healthcare system implications

(IS tie-in per Ritu v0627; extends IS research on health IT
+ online reviews; healthcare system implication; IS theory lens.)

> JL: Should this paragraph to be at the top? Instead at the bottom?
> CC: Recommend keeping at bottom. Problem (P1) is a stronger hook
  than "IS research has examined...". MISQ editor asks "is this
  interesting?" first, then "is this IS?" P6 at bottom = the landing
  after contributions. JL confirmed: keep as is.

This work extends IS research on health information technology
and online platforms, where prior studies have examined how EHR
systems shape prescribing decisions (Saifee et al. 2019) and
whether physician online reviews predict clinical outcomes
(Saifee et al. 2020; Lu & Rui 2018).

We advance this stream by showing that review-derived behavioral
signals predict physician actions in independent administrative data.

For the healthcare system, the disposition-situation framework
identifies where overprescription risk concentrates: in clinically
ambiguous contexts where physician traits have room to influence
prescribing.
```

Three elements per paragraph:
1. **Heading + preview**: what this paragraph does and why it's here
2. **Comments**: JL/CC discussion about structural decisions (preserved verbatim)
3. **Draft sentences**: one sentence per line, capturing CONTENT decisions

Draft sentences are rough prose with parenthetical citations (Author Year), not polished LaTeX. They capture what each sentence SAYS, not how it sounds. POLISH rewrites them to venue quality later.

DRAFT is done when: every paragraph has settled draft sentences, the user has confirmed the structure, and the section's story reads coherently sentence by sentence.


## DRAFT is NOT

- NOT polished prose (that's POLISH)
- NOT LaTeX generation (that's sync-to-tex after all phases)
- NOT citation gathering (that's GATHER/citation -- draft may have parenthetical refs like "(Saifee et al. 2019)" but these are content markers, not verified citations)
- NOT figure/table planning (that's GATHER/display)
- NOT value verification (that's GATHER/values)


## Inputs

1. **z-structure**: `0-lifecycle/5-editing/z-structure/z-structure.md` (paper-level architecture)
2. **Narrative**: `0-lifecycle/3-narrative/3-narrative.md` (the story beats)
3. **Existing tex**: `0-sections/NN_section.tex` (if the section already has prose)
4. **Section-type**: `section-type/section-{type}/SKILL.md` (structure norms for this section type)
5. **Venue pack**: `_venue/playbook-<pack>/<outlet>/<outlet>-<section>/style.md` (word budget, paragraph count, style norms)
6. **Claims**: `0-lifecycle/1-claims/1-claims.md` (what claims this section needs to support)


## Outline file format

The outline lives at `0-lifecycle/5-editing/{section}/{section}.md`:

```markdown
# Section N: Title -- Structure

```
§N.1 Subsection Title (K paragraphs)
  P1. Short paragraph job description                        N sentences
  P2. Short paragraph job description                        N sentences
  P3. Short paragraph job description                        N sentences
```

---

## §N.1 Subsection Title

### P1. What this paragraph does

(Semicolon-separated preview of key points; short, not a mini-abstract.)

> JL: comment text
> CC: response text

Draft sentence one, capturing the first content decision.

Draft sentence two, with a parenthetical citation (Author Year) if known.

Draft sentence three.

---

### P2. What this paragraph does

(Preview of key points.)

Draft sentence one.

Draft sentence two.
```

Rules:
- **Structure overview at top** (update whenever structure changes)
- `##` for subsections, `###` for paragraphs
- **Preview must be ONE SHORT LINE** (~80-120 chars), not a mini-abstract. It's a scan hook: concept name + one distinguishing phrase.
- **One draft sentence per line** (these become `Pn.Sn` markers when synced to tex)
- **Target 5-6 sentences per paragraph** (MISQ/ISR norm; consult section-type for venue-specific)
- **JL comments as `> JL:` text**, CC responses as `> CC:` text
- **JL comments stay until JL confirms** they're resolved (never remove, never compress)
- **Parenthetical citations** like "(Author Year)" are content markers, not verified bibtex keys. GATHER/citation will audit and verify them later.


## Workflow

### Step 1. Consult upstream

Read these to understand the section's role:

1. **z-structure**: how this section fits in the paper's overall architecture
2. **Narrative**: what story beats belong in this section
3. **Claims**: which claims this section must support
4. **Section-type**: structure norms (paragraph count, required elements, hooks, failure modes)
5. **Venue pack**: word budget, style norms, per-section style guide if it exists

Resolution path for venue:
- From `STATUS.md venue:` extract the outlet (e.g., "MISQ 2026" → outlet "MISQ", pack "playbook-utd-is")
- Read `_venue/playbook-<pack>/<outlet>/<outlet>-<section>/style.md` if it exists
- This file contains word budget, arc, signature moves, exemplar sentences. It OVERRIDES the general style-profile.md for this section.

### Step 2. Settle structure

Decide the paragraph skeleton:

1. How many subsections? What are their titles?
2. How many paragraphs per subsection? What job does each do?
3. Where do hypotheses, contributions, or key claims land?
4. What displays are referenced? (Noted in preview, not generated)

Write the structure overview block at the top of the outline. Present it to the user for confirmation before writing draft sentences.

### Step 3. Draft sentences

For each paragraph in the settled structure:

1. Write the heading: `### P#. What this paragraph does`
2. Write the preview: `(semicolon-separated key points)`
3. Write draft sentences, one per line
4. Each sentence captures ONE content decision
5. Use parenthetical citations "(Author Year)" where the content needs support, even if the exact paper is not yet verified
6. Flag uncertain content with `(?)` or `> CC: need to verify this claim`

### Step 4. Iterate with user

The user reads the outline and adds `> JL:` comments. Respond with `> CC:` underneath each comment. Iterate until the structure and content decisions are settled.

Typical discussion topics:
- Should this paragraph be moved?
- Is this the right hook?
- Does this claim belong here or in another section?
- Is this paragraph doing two jobs? Split?
- Is this paragraph redundant with another section?

### Step 5. Confirm draft

When all paragraphs have draft sentences and the user confirms, mark draft ✅ in the status.

Update `_LOG_{section}.md` with:
```markdown
## YYYY-MM-DD #N ~HH:MM
> JL: "draft introduction"
- Created outline with N paragraphs, M sentences
- Structure: [brief description of paragraph roles]
- Key decisions: [any structural choices from JL comments]
```


## Populating from existing tex

When the section already has prose in `0-sections/*.tex`:

1. Read the tex file
2. Extract paragraph structure (from `% Para [id]` banners or `%% ---- Pn.Sn ----` markers)
3. For each paragraph: extract the sentences, create the heading + preview + draft sentences in the outline
4. Preserve any existing `> JL:` comments from prior editing rounds
5. Present the populated outline to the user for review

This is a BACKWARD FILL: tex → outline. The outline becomes the working document for structural decisions, and tex gets updated when the section syncs after all phases.


## When to STOP and hand off

DRAFT is done when:
- [ ] Every paragraph has a heading, preview, and draft sentences
- [ ] Structure overview matches the paragraph blocks
- [ ] User has confirmed the outline (no open structural `> JL:` questions)
- [ ] _LOG has a draft summary entry

Hand off to GATHER (citation + values + display) which works on the settled outline. POLISH comes after GATHER, and rewrites draft sentences to venue-quality LaTeX.


## Relation to POLISH

```
DRAFT                                 POLISH
─────                                 ──────
settle WHAT to say                    settle HOW to say it
one sentence per line, rough prose    venue-quality LaTeX, \citep{}, Pn.Sn
parenthetical "(Author Year)"        verified \citep{key} from .bib
content decisions                     language quality, voice, flow
the outline .md file                  the tex file in 0-sections/
```

The draft sentences are the INPUT to POLISH. If a draft sentence says the wrong thing, fix it in the outline (DRAFT). If a draft sentence says the right thing but sounds bad, fix it in tex (POLISH).


## Relation to other skills

| Need | Use |
|---|---|
| Settle what to say (this skill) | haipipe-paper-section-edit-draft |
| Gather citations for settled outline | haipipe-paper-section-edit-citation |
| Gather values for settled outline | haipipe-paper-section-edit-values |
| Plan displays for settled outline | haipipe-paper-section-edit-display |
| Rewrite draft sentences to venue prose | haipipe-paper-section-edit-content, -humanizer, -weaving |
| Section-level orchestration | haipipe-paper-section-edit (hub) |
| Paper-level structure | z-structure in 5-editing/ |
