# Section Outline Format Spec

The outline is the primary working document for section-edit. It lives at `0-lifecycle/5-section-edit/{section}/{section}.md`. DRAFT creates it, PROBE annotates its tracking files, REVISE updates its sentences and syncs to tex, CHECK verifies everything matches.

## File structure

```markdown
# Section N: Title -- Structure

\```
§N.1 Subsection Title (K paragraphs)
  P1. Short paragraph job description                        N sentences
  P2. Short paragraph job description                        N sentences
  P3. Short paragraph job description                        N sentences
\```

---

## §N.1 Subsection Title

### P1. What this paragraph does

(Semicolon-separated preview of key points; short, not a mini-abstract.)

> USER: comment text
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

## Three elements per paragraph

1. **Heading + preview**: what this paragraph does and why it's here
2. **Comments**: USER/CC discussion about structural decisions (preserved verbatim)
3. **Draft sentences**: one sentence per line, capturing CONTENT decisions

## Rules

- **Structure overview at top** (update whenever structure changes)
- `##` for subsections, `###` for paragraphs
- **Preview must be ONE SHORT LINE** (~80-120 chars), not a mini-abstract. It's a scan hook: concept name + one distinguishing phrase.
- **One draft sentence per line** (these become `Pn.Sn` markers when synced to tex)
- **Target 5-6 sentences per paragraph** (MISQ/ISR norm; consult section-type for venue-specific)
- **USER comments as `> USER:` text**, CC responses as `> CC:` text
- **Comment lifecycle**: comments live in the working .md while active; when user confirms resolved, the thread moves to `_LOG`; each phase starts with a clean file
- **Parenthetical citations** like "(Author Year)" are content markers, not verified bibtex keys. PROBE/citation will audit and verify them later.

## Draft sentences are NOT

- NOT polished prose (that's REVISE)
- NOT LaTeX (that's sync-to-tex after all phases)
- NOT verified citations (that's PROBE/citation)
- NOT verified numbers (that's PROBE/values)

Draft sentences are rough prose that captures what each sentence SAYS, not how it sounds. REVISE rewrites them to venue quality later.

## Populating from existing tex (backward fill)

When the section already has prose in `0-sections/*.tex`:

1. Read the tex file
2. Extract paragraph structure (from `% Para [id]` banners or `%% ---- Pn.Sn ----` markers)
3. For each paragraph: extract the sentences, create the heading + preview + draft sentences in the outline
4. Preserve any existing `> USER:` comments from prior editing rounds
5. Present the populated outline to the user for review

This is a BACKWARD FILL: tex -> outline. The outline becomes the working document for structural decisions, and tex gets updated when the section syncs after all phases.

## Inputs for section drafting

1. **z-structure**: `0-lifecycle/5-section-edit/z-structure/z-structure.md` (paper-level architecture)
2. **Narrative**: `0-lifecycle/3-narrative/3-narrative.md` (the story beats)
3. **Existing tex**: `0-sections/NN_section.tex` (if the section already has prose)
4. **Section-type**: `section-type/section-{type}/SKILL.md` (structure norms for this section type)
5. **Venue pack**: `_venue/playbook-<pack>/<outlet>/<outlet>-<section>/style.md` (word budget, paragraph count, style norms)
6. **Claims**: `0-lifecycle/1-claims/1-claims.md` (what claims this section needs to support)

Resolution path for venue:
- From `STATUS.md venue:` extract the outlet (e.g., "MISQ 2026" -> outlet "MISQ", pack "playbook-utd-is")
- Read `_venue/playbook-<pack>/<outlet>/<outlet>-<section>/style.md` if it exists
- This file contains word budget, arc, signature moves, exemplar sentences. It OVERRIDES the general style-profile.md for this section.

## Done-criteria for section DRAFT

- [ ] Every paragraph has a heading, preview, and draft sentences
- [ ] Structure overview matches the paragraph blocks
- [ ] User has confirmed the outline (no open structural `> USER:` questions)
- [ ] _LOG has a draft summary entry

## _LOG entry format for DRAFT

```markdown
## draft  YYYY-MM-DD

### [section or heading where comment lived]
> USER: original comment
> CC: response
-> applied / rejected / deferred

### Summary
- Created outline with N paragraphs, M sentences
- Key decisions: [structural choices from resolved comments]
```

## Relation to REVISE

```
DRAFT                                 REVISE
-----                                 ------
settle WHAT to say                    settle HOW to say it
one sentence per line, rough prose    venue-quality LaTeX, \citep{}, Pn.Sn
parenthetical "(Author Year)"        verified \citep{key} from .bib
content decisions                     language quality, voice, flow
the outline .md file                  the tex file in 0-sections/
```

The draft sentences are the INPUT to REVISE. If a draft sentence says the wrong thing, fix it in the outline (DRAFT). If a draft sentence says the right thing but sounds bad, fix it in tex (REVISE).
