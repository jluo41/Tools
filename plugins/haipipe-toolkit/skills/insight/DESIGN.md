insight — The Archive Layer (DESIGN)
========================================

Status: v2.5.0 (2026-06-20) — review contract established.
        task/probe/discover produce material; narrative/application/human
        review decides what becomes permanent KB; insight files reviewed
        D/I/K/W cards, indices, and graph audits.
Owner:  jluo41

Read ARCHITECTURE.md + MENTAL_MODEL.md first. This doc designs the AGENT
and INVOCATION structure for insight, bringing it to parity with task
and probe — which both have `agents/` + a top-level design doc; E had
neither. The pattern is applied THOUGHTFULLY (the way probe departed
from task), not copy-pasted.


Why this doc exists (the gap)
=============================

insight had the SKINS but no SKELETON:

```
task    DESIGN.md       + agents/{creators, reviewers}
probe   MENTAL_MODEL.md + agents/{reviewers, advancers}
insight  — none —        + — none —          ← only 6 SKILL.md + ref/
```

E is the only one of C/D/E with neither a design doc nor an agents/ layer.
This doc adds the skeleton.


E's nature (recap — the librarian)
==================================

insight does NOT compute or claim. It ARCHIVES. It is called at review
boundaries to turn finished material into curated permanent memory.

```
called by:  narrative review
            application ask Phase 4
            human/manual review
owns:       review → apply → card review → index → audit
writes:     insights/ only (D/I/K/W cards + INDEX + audits + derived exports)
NEVER:      writes tasks/ or probes/ ; triggers a probe ; judges claim truth
```

DIKW folders are flat. Topic/source/narrative grouping is generated as views,
not encoded as subfolders. Card growth is controlled by review review using
`ref/card-granularity.md`: one card = one reusable knowledge unit; use merge
for reinforcing evidence, split for broad candidates, and skip for raw/noisy
material.

Cards are not write-once. `ref/card-lifecycle.md` controls how they evolve:
stable card ids, merge/update for same-unit evidence, supersede for refuted or
wrong-scope claims, and `## Change log` for meaningful edits.


Who produces material vs who files memory
================================================

DIKW layers are card labels in the archive, not lifecycle stages.

```
Card layer     What it is                                   Filing decision
─────────────  ───────────────────────────────────────────  ─────────────────
🟦 D data      one named dataset's profile (in-sample)      review
🟩 I info      a pattern inside that same dataset           review
🟨 K knowledge does the pattern generalize, + confidence    review
🟧 W wisdom    a K-backed action, risk-tuned to K confidence review
```

The principle: **D/I describe one dataset (in-sample, named); K is the
generalization claim where p/CI/confidence live; W acts on K, tuned to its
confidence. Review decides archival value; insight files and maintains the graph.**

- D and I require a `dataset:` and carry no inferential numbers.
- K has NO probe gate — a generalization basis (significance / robustness / vetted
  claim) plus an honest confidence is enough; low-confidence and negative K are recorded.
- Narrative/application ask/human review is the construction boundary.
- The D/I/K/W layer skills are low-level writers used by review.


The asymmetry note (E vs C vs D) — apply, don't copy
====================================================

probe's README warns: apply the agent pattern *thoughtfully*. Each layer
answers "is the BUILD batchable/headless, or interactive?" differently:

```
          builder family          reviewer family            advancer
─────────────────────────────────────────────────────────────────────────
task    creators/ (per TYPE)    reviewers/ (fixed 2)       — none —
          ∵ code authoring is     type-agnostic, gate all
          batchable, fans out

probe   SKILLS (no creators)    reviewers/ (3)             advancers/ (1)
          ∵ probe design is       structural/integrity/      explore =
          interactive, low-vol    claim                      propose next

insight creators/ (per DIKW)    reviewers/ (4 per-type     deferred
          ∵ "the HEADLESS path    + 1 cross-layer): one      (explore skill
          an AGENT calls", not    card-reviewer per D/I/K/W   already covers
          C's "batchable code"    + index-integrity (graph)  the read side)
```

Two reframes settled this session:
1. **E's creators exist for a different reason than C's** — not because filing
   is mechanical, but because we need a headless, full-args path an agent can
   call with zero human-in-the-loop. The creator IS that path.
2. **E's reviewers go PER-TYPE** — a deliberate departure from C/D's
   type-agnostic reviewers. Each DIKW card has a genuinely different boundary
   (D names a dataset + traces · I is an in-sample pattern, no p/CI · K is a
   generalization claim with confidence + full counter-evidence, no probe gate · W
   must be actionable), so each gets its own card-reviewer enforcing accuracy +
   style against `ref/dikw-boundaries.md`. Only `index-integrity` stays shared
   (the cross-layer graph cannot be per-type).


The dual-mode invocation contract (the core)
============================================

Both a HUMAN and an AGENT call the same skill. The mode is chosen by
INPUT COMPLETENESS, not by who calls — verbatim the contract task
already ships in `task/haipipe-task/ref/invocation-modes.md`.

```
              ┌─────────────────────────────────────────────┐
 human  ─────▶│  haipipe-insight-<layer>  (one body)         │
 (often        │  input gate: card requisites complete?       │
  partial)     │    ✅ yes → SILENT  (produce card, no ASK)    │◀── card-creator-<layer>-agent
               │    ❌ no + user → ASK only the missing fields │    (always full spec → SILENT)
 agent  ─────▶│    ❌ no + no user → status: blocked, missing │
 (full spec)   │            (caller re-dispatches; never hang) │
               └─────────────────────────────────────────────┘
                  every call ends with a structured return block
```

Branch 3 (missing input + no user = agent path) is the load-bearing one:
the skill must NEVER hang on an ASK in a headless run — it returns
`status: blocked` + `missing: [field]`, and the calling agent fills it and
re-dispatches. Never invent a required field.

What "complete" means per layer when review calls a writer:

```
D (Data)        source_id (namespaced task/probe/discover/lit ref) + headline + Numbers table + tags
I (Information)  sources:[D..] (>=1) + pattern + direction + pattern stmt
K (Knowledge)    sources:[probe/lit refs] MUST be judged + claim + confidence
W (Wisdom)       sources:[K..] + rec + rec_type + cost + how-to-act
```


Insight's role in the loop architecture
===================================

The system runs as nested loops, but insight is not a loop driver. It is the
archive step after a meaningful boundary:

```
task/probe/discover finish material
        ↓
narrative or application ask reviews
        ↓
insight files D/I/K/W cards
        ↓
narrative/application/paper cite card ids
```

The concrete paths into insight:

```
Path A (application ask):  Phase 4 → review → D/I/K/W cards + report refs
Path B (narrative):        post/fill → review → K/W refs in claims.md
Path C (manual):           user calls review on project/probe/task scope
Path D (low-level):        explicit data/information/knowledge/wisdom writer
```

Review is the preferred path because it can deduplicate, skip, supersede, and
audit before the permanent KB changes.

insight never DRIVES a loop. It is always the callee. Narrative/application
decide "go round again"; insight only archives when called.

The headless filing requirement still holds: L1 runs round after round;
L2 can fan out several probes at once. You cannot human-in-the-loop every
card. Headless E filing is a structural requirement, not a nicety.


Proposed structure (the skeleton to build)
===========================================

```
insight/
├── DESIGN.md                       (this file)
├── CHANGELOG.md                    🆕 parity with C/D
├── ref/
│   ├── review-contract.md        🆕 how insights/ is constructed
│   ├── card-granularity.md        🆕 card size + merge/split/skip rules
│   ├── card-lifecycle.md          🆕 file/merge/update/supersede history rules
│   ├── invocation-modes.md         🆕 the dual-mode contract + per-DIKW table
│   ├── dikw-boundaries.md          🆕 each layer's boundary + worked examples (reviewers enforce)
│   ├── insight-md-schema.md        ✅ exists (reviewers point here, no dup)
│   ├── insight-context-loading.md  ✅ exists
│   └── index-templates.md          ✅ exists
├── agents/
│   ├── README.md                   🆕 roster + this asymmetry note
│   ├── creators/                   🆕 the headless, agent-callable path
│   │   ├── _TEMPLATE.md
│   │   ├── card-creator-data-agent.md
│   │   ├── card-creator-information-agent.md
│   │   ├── card-creator-knowledge-agent.md
│   │   └── card-creator-wisdom-agent.md
│   └── reviewers/                  🆕 one card-reviewer per DIKW type + 1 cross-layer
│       ├── _TEMPLATE.md
│       ├── card-reviewer-data-agent.md          🟦 Codex accuracy + D boundary/style
│       ├── card-reviewer-information-agent.md    🟩
│       ├── card-reviewer-knowledge-agent.md      🟨 + the ★ probe gate
│       ├── card-reviewer-wisdom-agent.md         🟧
│       └── index-integrity-auditor-agent.md     🔗 cross-layer: sources<->ref_by, INDEX<->files
└── haipipe-insight*/SKILL.md       ♻️ each gains a dual-mode body + structured return
    haipipe-insight-review/SKILL.md 🆕 review/apply archive construction
```

Growth axes: creators grow per DIKW layer (+1 creator per layer). E DEPARTS
from C's "reviewers fixed/type-agnostic" rule — reviewers ALSO grow per layer
(+1 card-reviewer per layer), because each layer's boundary genuinely differs;
only index-integrity is shared. Adding a card type = +1 creator AND +1 reviewer.


Decisions settled
==================

Session 1 (2026-05-31):
- E gets a DESIGN.md + agents/ (parity with C/D).            ✅
- Dual-mode by input completeness; agent-missing → blocked.  ✅
- creators/ per DIKW (4) = the headless agent path.          ✅
- reviewers/ per DIKW (4) + cross-layer index-integrity.     ✅
- E never triggers probes / drives loops; always callee.     ✅
- E closes the probe cycle (L0) that probe-loop skips.        ✅

Session 2 (2026-06-11):
- **Previous direct-producer model established.** D was modeled as task-stage
  output; K was modeled as probe-convergence output; I + W stayed synthesis
  layers. This closed the loop technically, but it made the archive too eager. ✅
- **Low-level writer APIs validated.** `haipipe-insight-data` and
  `haipipe-insight-knowledge` can file cards from complete specs. These remain
  useful under apply, but are no longer the preferred public entry. ✅
- **L0 loop cell had a concrete path.** Superseded by Session 3's review gate:
  task/probe/discover produce material; review decides permanence. ✅

Session 3 (2026-06-20):
- **Review contract established.** task/probe/discover produce material;
  narrative/application/human review decides what becomes permanent KB;
  insight writers file cards under a review/apply/card-review/index/audit protocol. ✅
- **Direct task/probe filing downgraded to low-level/manual API.** The
  preferred construction path is `/haipipe-insight review ...`. ✅


Open questions
===============

Q1. [RESOLVED — build both] Creator is a SEPARATE thin agent AND the
    underlying skill stays: each card-creator-<layer>-agent calls the
    dual-mode haipipe-insight-<layer> skill headless.

Q2. [RESOLVED — review gate] probe/task/discover material can become K/D, but
    not automatically. `/haipipe-insight review ...` decides whether the
    material is archive-worthy, deduplicates it, and then calls the writer APIs.
    🟩 I and strategic 🟧 W accumulate via application/narrative/manual review.

Q3. Does E need an advancer (synthesis proposer)? Deferred — explore skill
    covers the read/coverage side. Review planning can suggest I-level
    synthesis when D card count >= 3 in a coherent scope, which partially fills
    this role.

Q4. [RESOLVED — per-type] Each DIKW card gets a specific card-reviewer
    enforcing accuracy + style against ref/dikw-boundaries.md.


Next steps
==========

DONE:
  ✅ 1. ref/invocation-modes.md + ref/dikw-boundaries.md
  ✅ 2. agents/ (4 creators + 5 reviewers + README + templates)
  ✅ 3. dual-mode blocks in all 4 DIKW skills
  ✅ 4. review contract documented (`ref/review-contract.md`)
  ✅ 5. review skill skeleton added (`haipipe-insight-review/SKILL.md`)
  ✅ 6. DIKW writer APIs kept as low-level apply targets
  ✅ 7. probe/task direct filing model superseded by review gate

Remaining:
  - I-level auto-synthesis trigger: review can suggest it; decide
    whether application ask should apply it automatically or require review.
  - Dogfood: run a real task/probe/narrative scope through review → apply
    → reviewer pass → index-integrity pass.
  - Tighten old layer writer docs so they all point back to review as the
    preferred entry.
