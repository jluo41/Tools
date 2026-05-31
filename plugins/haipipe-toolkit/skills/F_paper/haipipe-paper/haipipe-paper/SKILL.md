---
name: haipipe-paper
description: "Run any paper-lifecycle work. Parses intent (venue + phase) and dispatches to the right specialist (haipipe-paper-conference/-journal/-is/-rebuttal). Use for writing/revising/rebutting papers targeting any venue — ICLR, NeurIPS, ICML, Nature, PNAS, MISQ, ISR. Trigger: paper, write paper, paper pipeline, paper writing, rebuttal, reply to reviewers, 写论文, 论文流程, /haipipe-paper."
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
/haipipe-paper "<natural language>"         -> infer venue from keywords, dispatch
```

Examples:
```
/haipipe-paper conference "NARRATIVE_REPORT.md" — venue: ICLR
/haipipe-paper journal                       (no input → Nature default)
/haipipe-paper is "MISQ paper on AI adoption"
/haipipe-paper rebuttal "paper/" — venue: NeurIPS
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
```

Venue aliases (positional):
```
conf, conference, ml, neurips, iclr, icml  -> conference
journal, nature, pnas, nat                 -> journal
is, misq, isr, management-science, msis    -> is
rebuttal, reply, response, rev             -> rebuttal
```

---

Routing Logic
-------------

```
Step 1: Parse $ARGUMENTS.

Step 2: Resolve venue:
  - First positional matches a venue alias?           -> venue = that
  - Else scan keyword map across all positional args.
  - Phrase contains "reply to reviewers" / "rebuttal"
    / review-related verbs                            -> venue = rebuttal
  - Topic mentions ICLR/NeurIPS/ICML etc.             -> venue = conference
  - Topic mentions Nature/PNAS                        -> venue = journal
  - Topic mentions MISQ/ISR/IS journal                -> venue = is
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

Next: /haipipe-paper <venue> "<input>"
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
           /paper-plan, /paper-figure, /paper-write, or a re-invocation
           of /haipipe-paper for a different phase)
```

---

Relation to Lifecycle Stage Skills
-----------------------------------

The orchestrator and venue specialists in `0-workflow/` operate at the
**workflow** level. They internally call into the **stage** skills under
`E_paper/{1-narrative,2-plan,3-figure,4-write,5-revise,6-review,7-respond,8-present}/`:

```
1-narrative/  narrative-report, result-to-claim
2-plan/       paper-plan, paper-bootstrap, paper-architecture, paper-incubator
3-figure/     paper-figure, paper-illustration, figure-spec, figure-planner, …
4-write/      paper-write, scientific-writing, conference-paper-writing, paper-compile, overleaf-sync, …
5-revise/     paper-revise, manuscript-optimizer, auto-paper-improvement-loop, paper-diff-pdf, results-section-revision
6-review/     paper-claim-audit, citation-audit, citation-verifier, proof-checker, paper-reviewer, submission-audit, …
7-respond/    paper-rebuttal, rebuttal-response
8-present/    paper-slides, paper-poster
```

Power users can invoke a stage skill directly (e.g. `/paper-plan`,
`/paper-figure`) — those slash commands remain unchanged. The
orchestrator is the right entry point when you don't yet know which
stage you're in or which venue you're targeting.

---

Composing with Other Workflows
-------------------------------

```
/idea-discovery       → IDEA_REPORT.md
/run-probe       → experiment results
/auto-review-loop     → AUTO_REVIEW.md
/result-to-claim      → CLAIMS_FROM_RESULTS.md
/narrative-report     → NARRATIVE_REPORT.md  ← design contract
        │
        ▼
/haipipe-paper        ← you are here (router)
        │
        ├─► /haipipe-paper-conference  (ICLR/NeurIPS/…)
        ├─► /haipipe-paper-journal     (Nature/PNAS/…)
        ├─► /haipipe-paper-is          (MISQ/ISR/…)
        └─► /haipipe-paper-rebuttal    (any venue, post-review)
```
