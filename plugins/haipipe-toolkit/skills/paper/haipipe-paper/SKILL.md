---
name: haipipe-paper
description: "Run any paper-lifecycle work. Parses intent (venue + phase) and dispatches to the right specialist (haipipe-paper-conference/-journal/-is/-rebuttal/-create/-revise). Use for writing/revising/rebutting papers targeting any venue — ICLR, NeurIPS, ICML, Nature, PNAS, MISQ, ISR. Trigger: paper, write paper, paper pipeline, paper writing, draft paper, revise paper, polish tex, rebuttal, reply to reviewers, 写论文, 论文流程, /haipipe-paper."
argument-hint: "[venue] [phase] [args...]"
allowed-tools: Bash, Read, Grep, Glob, Skill
metadata:
  version: "1.0.0"
  last_updated: "2026-05-31"
  summary: "Run any paper-lifecycle work."
  changelog:
    - "1.0.0 (2026-05-31): baseline metadata added."
---

Skill: haipipe-paper (orchestrator)
====================================

User-facing entry for the paper lifecycle. Parses intent, dispatches to
the right venue specialist via `Skill()`. Lifecycle phase skills
(narrative, plan, figure, write, compile, revise, review, present) are
called by the specialist, not by this orchestrator directly.

```
/haipipe-paper                              -> venue dashboard + usage hints
/haipipe-paper <venue>                      -> dispatch to that specialist (no args)
/haipipe-paper <venue> "<topic-or-input>"   -> dispatch to specialist with input
/haipipe-paper rebuttal "<paper-path>"      -> dispatch to rebuttal specialist
/haipipe-paper create "<plan-dir>"          -> draft fresh tex paragraph-by-paragraph
/haipipe-paper revise "<tex-root>"          -> polish existing tex paragraph-by-paragraph
/haipipe-paper "<natural language>"         -> infer venue from keywords, dispatch
```

Examples:
```
/haipipe-paper conference "NARRATIVE_REPORT.md" — venue: ICLR
/haipipe-paper journal                       (no input → Nature default)
/haipipe-paper is "MISQ paper on AI adoption"
/haipipe-paper rebuttal "paper/" — venue: NeurIPS
/haipipe-paper create "papers/lhm-a/" — venue: iclr
/haipipe-paper revise "papers/lhm-a/"
```

---

Specialists
-----------

```
haipipe-paper-conference  ICLR/NeurIPS/ICML/ML conference paper pipeline
                          (narrative→plan→figure→write→compile→improve→audit)
haipipe-paper-journal     Nature/PNAS/biomedical journal manuscript workflow
                          (bootstrap→article-type→draft→revise→submit→rebuttal)
haipipe-paper-is          MISQ/ISR/Management Science IS journal paper
                          (contribution framing → theory → method → submission)
haipipe-paper-rebuttal    Submission rebuttal pipeline (venue-agnostic)
                          (parse reviews → strategy → draft → coverage check)
haipipe-paper-create      Fresh-draft pipeline, venue-agnostic at workflow
                          (narrative+plan → scaffold tex → paragraph-by-paragraph draft)
haipipe-paper-revise      Whole-paper polish pipeline, venue-agnostic
                          (discover sections → paragraph-by-paragraph polish
                           via paper-revise → cross-section audit → diff report)
```

---

Venue Keyword Map
------------------

```
conference, ML conference, NeurIPS, ICLR, ICML, CVPR,
ACL, AAAI, COLM, IEEE_CONF, AISTATS, KDD               -> conference
journal, Nature, Nature Methods, Nature Biotechnology,
PNAS, Science, biomedical journal, broad-impact        -> journal
IS, MISQ, ISR, Management Science, Information
Systems, IT artifact, digital systems, UTD24-IS        -> is
rebuttal, reply, response, OpenReview response,
reviewer comments, review-response, R1 revision        -> rebuttal
create, draft tex, write tex, from narrative,
new paper, scaffold paper, 写初稿                       -> create
revise, polish, polish tex, paragraph polish,
walk sections, whole-paper revision, 整篇润色           -> revise
```

Venue/task aliases (positional):
```
conf, conference, ml, neurips, iclr, icml  -> conference
journal, nature, pnas, nat                 -> journal
is, misq, isr, management-science, msis    -> is
rebuttal, reply, response, rev             -> rebuttal
create, draft, new, scaffold               -> create
revise, polish, walk                       -> revise
```

Note: `create` and `revise` are task aliases, not venues. They are
venue-agnostic at the workflow level — the underlying templates and
section playbooks know the venue.

---

Routing Logic
-------------

```
Step 1: Parse $ARGUMENTS.

Step 2: Resolve venue/task:
  - First positional matches a venue/task alias?      -> dispatch target = that
  - Else scan keyword map across all positional args.
  - Phrase contains "reply to reviewers" / "rebuttal"
    / review-related verbs                            -> target = rebuttal
  - Phrase contains "draft tex" / "new paper" /
    "scaffold" / "from narrative"                     -> target = create
  - Phrase contains "polish" / "revise" / "walk
    sections" / "paragraph polish"                    -> target = revise
  - Topic mentions ICLR/NeurIPS/ICML etc.             -> target = conference
  - Topic mentions Nature/PNAS                        -> target = journal
  - Topic mentions MISQ/ISR/IS journal                -> target = is
  - Default if a NARRATIVE_REPORT.md exists with no
    venue hint                                        -> ASK (don't guess)

Step 3: Decide handling:
  - No args                                           -> usage dashboard (inline)
  - venue resolved, no other args                     -> dispatch with "(none)"
  - venue + input/args                                -> dispatch with full args
  - input but no venue                                -> ASK which venue

Step 4: Dispatch:
    Skill("haipipe-paper-<venue>", args="<remaining_args>")

Step 5: Capture the specialist's structured tail (status / summary /
        artifacts / next), present it.
```

---

No-Arg Mode (usage dashboard, inline)
--------------------------------------

When invoked with no arguments, do not fan out. Emit a compact venue
chooser:

```
📄 haipipe-paper — pick a venue track:

  conference  → ICLR / NeurIPS / ICML / CVPR / ACL / AAAI
                Full automated pipeline: narrative → PDF (Phase 1-6 with audits)
                Best when you have a NARRATIVE_REPORT.md and want a submission-ready PDF.

  journal     → Nature portfolio / PNAS / biomedical journals
                Nature-style routing advisor: which skill to use next.
                Best for prose-first, story-driven manuscripts.

  is          → MISQ / ISR / Management Science (IS section)
                IS-specific contribution framing, theory selection.
                Best for behavioral / design-science / digital-systems papers.

  rebuttal    → any venue, post-review phase
                Parses reviews, drafts text-only rebuttal under venue limits.
                Best after external reviews land.

  create      → fresh draft from narrative + plan (venue-agnostic)
                Scaffolds tex root, walks sections, drafts paragraph-by-paragraph.
                Best when you have NARRATIVE_REPORT.md + PAPER_PLAN.md and want
                a compileable first draft.

  revise      → polish an existing tex (venue-agnostic)
                Discovers sections, walks each through haipipe-paper-edit-weaving's
                diagnose+plan+apply gates (G1/Q/G2), cross-section audit.
                Best when you have a draft and want to polish it paragraph-by-
                paragraph, optionally guided by reviewer feedback.

Next: /haipipe-paper <venue-or-task> "<input>"
```

---

Disambiguation Rules
---------------------

  - Venue unclear → list the 4 options, wait. Do NOT default to conference
    or journal silently — venue choice drives style file, page limit, and
    structure decisions that are expensive to redo.
  - User says "paper" with no venue + provides NARRATIVE_REPORT.md →
    ASK which venue.
  - User says "rebuttal" + provides paper path → dispatch to rebuttal
    immediately (rebuttal is venue-agnostic).
  - Multi-venue request ("port the ICLR paper to PNAS") → dispatch to
    journal with a note about source material from the conference draft;
    do NOT chain blindly.

---

Specialist Return Contract
---------------------------

Each specialist should return a tail block:

```
status:    ok | blocked | failed
summary:   2-3 sentences on what the specialist did
artifacts: [paths created, read, or modified]
next:      suggested next command (often a lifecycle stage skill like
           /haipipe-paper-structure-plan, /haipipe-paper-structure-figure, /haipipe-paper-edit-write, or a re-invocation
           of /haipipe-paper for a different phase)
```

---

Relation to Lifecycle Stage Skills, Sections, and Components
-------------------------------------------------------------

The orchestrator and venue specialists in `0-workflow/` operate at the
**workflow** level. Underneath they coordinate three kinds of skills:

**Lifecycle stages** — `paper/{1-structure,2-build,3-edit,6-respond,7-present}/`
(unified `haipipe-paper-<stage>-<topic>` names; 6-respond/7-present keep legacy slugs for now):

```
1-structure/  haipipe-paper-structure (orchestrator) routes to:
              haipipe-paper-folder (scaffold Paper-<Name>-<Venue><Year>/),
              -structure-narrative, -structure-architecture, -structure-plan,
              -structure-diagram, -structure-incubator, -structure-figure-planner,
              -structure-figure, -structure-figure-spec,
              -structure-illustration, -structure-illustration-image2
2-build/      haipipe-paper-build-scaffold, -build-restructure, -build-check
3-edit/       haipipe-paper-edit (orchestrator) + topic subs -edit-content, -edit-values,
              -edit-citation, -edit-consistency, -edit-format, -edit-typeset;
              tools: -edit-diffpdf, -edit-to-overleaf;
              drafting: -edit-write, -edit-write-scientific, -edit-write-conference, -edit-write-systems;
              revision: -edit-weaving, -edit-optimizer, -edit-improve-loop, -edit-results-revision;
              audits: -edit-claim-audit, -edit-reviewer, -edit-proof-checker, -edit-submission-audit,
              -edit-manual-review-citations, -edit-manual-review-values, -edit-check-reference
6-respond/    paper-rebuttal, rebuttal-response
7-present/    paper-slides, paper-poster
```

**Per-section playbooks** — `paper/sections/` (Dimension B, reference material):

```
section-intro / -methods / -results / -discussion /
section-abstract / -related-work / -appendix
```

These are guidance docs read by 3-write / 4-revise / 5-review when they
target a specific .tex file under `0-sections/` in the paper folder.

**Cross-cutting components** — `paper/components/`:

```
components/citation/  citation-audit, citation-verifier, reference-audit-guide
components/compile/   paper-compile
components/diff/      haipipe-paper-edit-diffpdf (one-PDF colored diff; SKILL.md lives in 3-edit/haipipe-paper-edit-diffpdf/),
                      paper-diff-folder (writes 1-diff/vs-<ref>/ tree)
```

(Figure skills moved to `1-structure/` under the `haipipe-paper-structure-figure*` /
`-illustration*` names; see the lifecycle stage list above.)

Components are invoked by multiple stages (figures touched during
write/revise/review; citations touched during write/review; etc.).

Power users can invoke any stage / section / component skill directly
via its slash command — stage 1-3 slugs follow the unified
`haipipe-paper-<stage>-<topic>` scheme; later stages keep their legacy
slugs until they are migrated. The orchestrator
is the right entry point when you don't yet know which stage you're
in or which venue you're targeting.

Paper-folder contract
----------------------

All paper skills assume their input is a paper folder following the
layout:

```
<paper>/
├── 0-<paper>.tex / .bib                    master shell
├── 0-sections/                             section + lettered-appendix .tex files
├── 0-display/{Figure,Table,                main + appendix display assets
│              AppendixFigure,AppendixTable}/
├── 0-extra/{cover_letter,IRB,news,...}/    submission accessories
├── 1-config.yaml                           paths + metric definitions
├── 1-compile.sh                            build script
├── 1-diff/vs-<ref>/                        diff packages (written by paper-diff-folder)
├── 1-feedback/v<date>/                     reviewer feedback by date
└── 1-review/{A-E,DECISIONS.md,HANDOFF.md}/ active review session pipeline
```

A revision **session** = a git branch (e.g. `review_v0325`); paper
skills are branch-agnostic at the file level.

---

Composing with Other Workflows
-------------------------------

```
/idea-discovery       → IDEA_REPORT.md
/run-probe       → experiment results
/auto-review-loop     → AUTO_REVIEW.md
/result-to-claim      → CLAIMS_FROM_RESULTS.md
/haipipe-paper-structure-narrative     → NARRATIVE_REPORT.md  ← design contract
        │
        ▼
/haipipe-paper        ← you are here (router)
        │
        ├─► /haipipe-paper-conference  (ICLR/NeurIPS/…)
        ├─► /haipipe-paper-journal     (Nature/PNAS/…)
        ├─► /haipipe-paper-is          (MISQ/ISR/…)
        ├─► /haipipe-paper-rebuttal    (any venue, post-review)
        ├─► /haipipe-paper-create      (narrative+plan → fresh tex)
        └─► /haipipe-paper-revise      (existing tex → polish via haipipe-paper-edit-weaving)
```
