Skill Maturity Lifecycle
=======================

How a plugin grows from cold start to autonomous operation.

Every plugin progresses through three phases. Each phase has a different actor
in the lead, a different thing being evaluated, and a different exit condition.

```
  Phase 1              Phase 2              Phase 3
  SKILL                HUMAN + SKILL        AGENT + SKILL
  ─────────────────    ─────────────────    ─────────────────
  The skill itself     Human drives         Agent drives
  Does it work?        Skill assists        Human audits
                       Knowledge grows      Can it work alone?
```


Phase 1 — Skill (does the skill work?)
---------------------------------------

The skill exists: SKILL.md, ref/, agents/, fn/. The question is whether it can
complete its protocol end-to-end. No human in the loop yet — this is about the
TOOL, not the collaboration.

**What exists:**
  - SKILL.md (the protocol)
  - ref/ (architecture, schemas)
  - agents/ (subagents)
  - fn/ (verb definitions — ready but untested)

**What does not exist yet:**
  - lesson/ (no domain knowledge accumulated)
  - feedback/ (no usage history)
  - PREFERENCES.md (no behavioral tuning)
  - Eval baselines

**Eval: protocol completion**

Can each verb/entry-point run to completion without errors? This is smoke
testing — the cheapest, most basic eval.

```
  Test                           Pass/Fail
  ────                           ─────────
  /sl-init creates a project     ?
  /sl-iterate runs one loop      ?
  /sl-validate benchmarks        ?
  /sl-scale labels a batch       ?
  State machine transitions      ?
  Agents communicate correctly   ?
  Output files match schemas     ?
```

For each skill verb:
  1. Can it start? (inputs parsed, context loaded)
  2. Can it finish? (outputs produced, state updated)
  3. Are the outputs well-formed? (match ref/ref-schema.md, ref/ref-assets.md)

This is NOT about whether the outputs are GOOD — that requires a human (Phase 2)
or a metric (Phase 3). This is about whether the machinery runs.

**Artifacts:**
  - eval/smoke/ (one test script per verb, pass/fail + error log)

**Exit condition:** every verb completes without errors on a test input. The
skill is mechanically sound and ready for a human to use.


Phase 2 — Human + Skill (is the collaboration productive?)
-----------------------------------------------------------

The human drives, the skill assists. The question shifts from "does it work?" to
"is it USEFUL?" and "is it LEARNING?"

This is where the knowledge layer builds up. Three machinery pieces do the
accumulation:

  **Lessons** — domain/methodology gotchas discovered during use.
    "Cohen's kappa is undefined when one rater uses only one category."
    "dbutils.notebook.run() doesn't inherit env vars."
    Each lesson is a guardrail: BEFORE acting, the agent MUST scan lesson/
    and flag relevant ones. The skill gets smarter not by changing code but
    by accumulating knowledge that shapes future behavior.

  **Feedback** — complaints about the skill itself (not the domain).
    "sl-iterate retrains the classifier every time, too slow."
    "lesson 04 is missing the --no-cache workaround."
    Filed in feedback/ with status tracking (open/fixed). Self-limiting:
    same-topic complaints merge instead of duplicating.

  **Digest** — bulk harvester run at end of session.
    Scans the session transcript, distills discrete items, classifies each
    as [LESSON] or [FEEDBACK], dedups against existing items, confirms with
    the human, then routes to lesson/ or feedback/. Nothing is lost.

  **PREFERENCES.md** — global behavioral tuning discovered during co-pilot.
    "Always show a diagram instead of prose." Not a lesson (not domain),
    not feedback (not a defect) — a preference about how the agent works.

**Eval: knowledge accumulation + human override rate**

The skill is productive if knowledge grows and the human needs to intervene less
over time.

```
  Metric                              Healthy trend
  ──────                              ─────────────
  New lessons per session             High early, tapering off
  Feedback open count                 Trending down (defects getting fixed)
  Lesson hits (warnings fired         Increasing (the skill warns BEFORE
    before gotcha encountered)          the human hits the gotcha)
  Human override rate                 Decreasing (human approves more,
                                        overrides less)
  Digest yield per session            Decreasing (less unfiled knowledge
                                        left on the table)
```

The key signal: **lesson hits**. When the skill warns "Lesson 05 applies here"
and the human says "yes, good catch" — that is the knowledge layer paying off.
When the human says "I already knew that" — the lesson is redundant but
harmless. When the human says "that's wrong" — the lesson needs updating.

**Artifacts:**
  - lesson/ (accumulated guardrails, dated with YYMMDD)
  - feedback/ (skill defect inbox, status-tracked)
  - PREFERENCES.md (behavioral tuning)
  - eval/copilot-metrics/ (per-session: lesson count, hit rate, override rate,
    digest yield)

**Exit condition:** the lesson/ folder has stabilized (few new lessons per
session), feedback open count is trending down, and the human finds themselves
approving the skill's suggestions more than overriding them. The skill has
absorbed enough domain knowledge to potentially run on its own.


Phase 3 — Agent + Skill (can it work alone?)
----------------------------------------------

The agent drives, the human audits. The question: without a human generating
friction (corrections, overrides, "no not that"), how do you know the skill is
still working?

Four evaluation methods, each catching a different failure mode:


### Eval A — Replay Audit (decision drift)

Save co-pilot session decisions as gold traces. In autopilot, the skill makes
the same decisions on the same inputs. Diff against gold traces.

```
co-pilot session         autopilot replay
────────────────         ────────────────
input_1 → decision_A    input_1 → decision_A  ✓ match
input_2 → decision_B    input_2 → decision_C  ✗ drift
input_3 → decision_D    input_3 → decision_D  ✓ match
```

What it catches: the skill diverging from established human judgment on known
cases. Regression detection.

What it misses: novel inputs the co-pilot never saw. The gold traces are frozen;
the domain is not.

Artifacts:
  - eval/gold-traces/ (saved during Phase 2 co-pilot sessions)
  - eval/replay-results/ (generated during autopilot)
  - eval/replay-diff.md (the comparison)


### Eval B — Lesson-Violation Detection (guardrail compliance)

The lessons ARE the eval. Each lesson says "when X, do Y not Z." Check whether
the skill's autopilot behavior violates any lesson.

```
Lesson 05: "dbutils.notebook.run() loses env vars — set them per notebook"

Autopilot action: used dbutils.notebook.run() without per-notebook env setup
→ VIOLATION of Lesson 05
```

What it catches: the skill repeating mistakes that were already documented. The
most embarrassing failure mode — "we knew about this and did it anyway."

What it misses: novel gotchas not yet captured as lessons. But that is what
Eval D is for.

Artifacts:
  - lesson/*.md (the assertions — accumulated during Phase 2)
  - eval/lesson-compliance/ (per-session violation report)


### Eval C — Outcome Metrics (end-to-end quality)

Domain-specific metrics that measure whether the skill's output is good,
regardless of HOW it got there.

```
subjective-label:  kappa convergence speed (iterations to converge)
                   panel-internal kappa trajectory
                   category D ratio at convergence

learn-infra:       deployment success rate
                   time-to-deploy vs co-pilot baseline
                   number of gotchas hit that had existing lessons

haipipe-paper:     review score trajectory
                   claims-supported ratio
                   compile success on first attempt
```

What it catches: overall quality regression. The skill might follow every lesson
and match every gold trace but still produce worse outcomes (because the lessons
are incomplete or the traces are stale).

What it misses: WHY quality changed. Outcome metrics are a thermometer, not a
diagnosis.

Artifacts:
  - eval/metrics.yaml (metric definitions per domain)
  - eval/baseline.yaml (co-pilot baseline values from Phase 2)
  - eval/autopilot-metrics/ (per-session measurements)


### Eval D — Digest-on-Autopilot (unknown unknowns)

Run digest on autopilot session transcripts. If it produces NEW lessons or
feedback, the skill encountered something it did not already know.

```
digest on autopilot session → 0 new items   → knowledge base is sufficient
digest on autopilot session → 2 new lessons → domain shifted or KB incomplete
digest on autopilot session → 1 new feedback → skill has a new rough edge
```

What it catches: the frontier — things the skill does not know that it does not
know. Early warning that the knowledge base needs expansion.

What it misses: silent failures where the skill is confidently wrong and the
transcript shows no friction (because there is no human to push back). This is
the fundamental limit of autopilot: no human friction = no signal for digest.

Artifacts:
  - eval/autopilot-digests/ (digest output per session)
  - eval/new-items-log.md (running count of new lessons + feedback from autopilot)


Eval Summary (all three phases)
-------------------------------

```
  Phase   What is evaluated    Eval method               Signal source
  ─────   ─────────────────    ───────────               ─────────────
  1       The SKILL            Protocol completion       Smoke tests
                               (does it run?)            (pass/fail per verb)

  2       HUMAN + SKILL        Knowledge accumulation    Lesson/feedback growth
                               (is it learning?)         Override rate
                               Human override rate       Lesson hit rate
                               (is it useful?)           Digest yield

  3       AGENT + SKILL
          A                    Decision drift            Gold traces from Ph 2
          B                    Guardrail compliance      Lessons from Ph 2
          C                    Outcome quality           Domain metrics
          D                    Unknown unknowns          Digest on autopilot
```

Phase 1 eval is cheap (smoke tests). Phase 2 eval emerges naturally from use
(the knowledge layer IS the eval data). Phase 3 eval requires all four methods
because there is no human friction to rely on — each method covers a different
blind spot.


Folder Structure (per plugin)
-----------------------------

```
plugin/
├── skills/<skill>/
│   ├── SKILL.md
│   ├── PREFERENCES.md        ← Phase 2+
│   ├── fn/
│   │   ├── lesson.md          ← verb: capture/list/search
│   │   ├── feedback.md        ← verb: capture/list/move
│   │   └── digest.md          ← verb: harvest → lesson/ + feedback/
│   ├── lesson/                ← Phase 2+ (accumulated guardrails)
│   ├── feedback/              ← Phase 2+ (skill defect inbox)
│   │   └── README.md
│   └── eval/
│       ├── smoke/             ← Phase 1 (protocol completion tests)
│       ├── copilot-metrics/   ← Phase 2 (knowledge growth, override rate)
│       ├── gold-traces/       ← Phase 3 Eval A (saved from Phase 2)
│       ├── replay-results/    ← Phase 3 Eval A
│       ├── lesson-compliance/ ← Phase 3 Eval B
│       ├── metrics.yaml       ← Phase 3 Eval C
│       ├── baseline.yaml      ← Phase 3 Eval C (from Phase 2)
│       ├── autopilot-metrics/ ← Phase 3 Eval C
│       └── autopilot-digests/ ← Phase 3 Eval D
└── ref/                       ← factual architecture docs (all phases)
```

Each phase's eval feeds the next: Phase 1 smoke tests confirm the skill runs.
Phase 2 co-pilot sessions produce lessons, feedback, gold traces, and baselines.
Phase 3 consumes all of those as eval inputs.


Applying to Existing Plugins
-----------------------------

```
  Plugin             Current phase   What is missing
  ──────             ─────────────   ───────────────
  learn-infra        Phase 2         eval/ (Phase 1 smoke implicit,
                                     Phase 3 not started)
  haipipe-toolkit    Phase 2         eval/ (Phase 1 smoke implicit,
                                     Phase 3 not started)
  subjective-label   Phase 1         fn/, lesson/, feedback/,
                                     PREFERENCES.md, eval/
  chronicle          Phase 1         fn/, lesson/, feedback/,
                                     PREFERENCES.md, eval/
```
