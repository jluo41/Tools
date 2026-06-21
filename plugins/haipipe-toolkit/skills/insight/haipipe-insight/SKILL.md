---
name: haipipe-insight
description: "Insight archive orchestrator. Constructs the project's curated permanent knowledge base under examples/<project>/insights/ through review/apply and D/I/K/W card writers. Preferred path: review finished task/probe/discover/narrative/application material, then apply reviewed cards. Low-level writers remain available for explicit data/information/knowledge/wisdom filing. Never executes code, judges probe truth, or triggers probes."
argument-hint: "[verb] [args...]"
allowed-tools: Bash, Read, Write, Edit, Grep, Glob, Skill
metadata:
  version: "2.6.0"
  last_updated: "2026-06-20"
  summary: "Insight archive orchestrator — review, apply, file, index, audit."
  changelog:
    - "2.6.0 (2026-06-20): renamed user-facing archive flow to review/apply."
    - "1.0.0 (2026-05-31): baseline metadata added."
    - "2.0.0 (2026-06-11): DIKW producer partition; post-file accumulation check; 3-job design (route + check + dashboard); step-by-step protocol."
---

Skill: haipipe-insight (orchestrator)
======================================

The project's **permanent knowledge base** — curated D/I/K/W cards filed from
finished task, probe, discovery, narrative, and application material.

```
task / probe / discover        produce material
narrative / application ask    decide what is worth archiving
insight review                plans + files curated cards
paper / report / message / ui  cite K/W from the archive
```

Unlike task or probe, insight does not produce new evidence. It is the
archive interface:

```
review scope → INSIGHT_REVIEW.yaml → apply → file cards → index → audit
```

User-facing language:

```
review <folder>  = "show me what is worth keeping as insight cards"
apply <INSIGHT_REVIEW.yaml> = "write the reviewed cards into insights/"
```

Internally, this is the same review contract. `INSIGHT_REVIEW.yaml` is the
reviewable checklist between raw material and permanent cards.

For a beginner-friendly walkthrough, read `play/README.md`.


Where the insight base lives (project-level)
---------------------------------------------

```
examples/Proj-X/
├── tasks/                                  (task — execution)
├── probes/                                (probe — research)
└── insights/                               ← insight writes here
    ├── INDEX.md                            (auto: all entries + status)
    ├── views/                              (auto: topic/source/narrative/status views)
    │
    ├── D_data/                     "what we observed"        (one source observation)
    │   ├── D01_<slug>.md
    │   └── ...
    │
    ├── I_information/                         "what patterns emerged"     (cross-observation)
    │   ├── I01_<slug>.md
    │   └── ...
    │
    ├── K_knowledge/                        "what we now believe"       (one judged belief)
    │   ├── K01_<slug>.md
    │   └── ...
    │
    └── W_wisdom/                           "what we should do next"    (one K-backed action)
        ├── W01_<slug>.md
        └── ...
```

**Hard rule:** NO code, no Python, no notebooks, no plots, no session logs
inside insights/. That work belongs to task, probe, narrative, or
application folders. insight only stores curated markdown cards and derived
indices.


Who produces material vs who files cards
------------------------------------------------

DIKW levels are labels on archived cards, not workflow phases.

```
Card layer      Material comes from                         Filing decision
──────────────  ───────────────────────────────────────────  ─────────────────────
🟦 D data       task/discover observations                   review
🟩 I info       patterns across D or rich descriptive work    review
🟨 K knowledge  judged probe claim or vetted literature       review
🟧 W wisdom     K-backed next action / strategic synthesis    review
```

- A task does not produce K (no hypothesis testing — that's a probe).
- A probe does not directly file insight cards; it produces verdict material.
- Narrative/application ask/human review decides what becomes permanent KB.
- The low-level D/I/K/W skills are writer APIs called by review.

---

Three Jobs
-----------

This orchestrator has five jobs:

```
Job 1: REVIEW    inspect a scope and emit a reviewable INSIGHT_REVIEW.yaml
Job 2: ROUTE     dispatch explicit low-level D/I/K/W filing requests
Job 3: CHECK     after apply, check accumulation / stale / supersede signals
Job 4: DASHBOARD show the KB state when called with no args
Job 5: EXPORT    write derived OKF-compatible views from source cards
```

**Job 1 (Review/Apply)** is the preferred construction path: inspect finished
material, emit `INSIGHT_REVIEW.yaml`, apply it through card writers, then
review, index, and audit.

**Job 2 (Route)** is the low-level verb dispatch for explicit D/I/K/W filing.

**Job 3 (Check)** suggests promotion, stale, or supersede actions after a file
operation. It suggests; it does not trigger probes.

**Job 4 (Dashboard)** is the explore skill — shows what the KB has, what's promotable, what's missing.

**Job 5 (Export)** is the OKF compatibility view — writes a derived
`insights/okf/` bundle from the source cards without changing D/I/K/W files.

---

Commands
--------

Two styles: **path-based review** (give it a source path, auto-detect what to
inspect) or **verb-based** (explicit DIKW level).

```
# Preferred: user-facing review/apply
/haipipe-insight review <project|narrative|ask-session|probe|task>
/haipipe-insight apply <INSIGHT_REVIEW.yaml>

# Convenience: review then apply when explicitly requested
/haipipe-insight review <scope> --auto

# Path-based review shorthand
/haipipe-insight <task-folder-path>              review task material
/haipipe-insight <probe-folder-path>             review probe material
/haipipe-insight <task-group-path>               review task-group material

# Verb-based (explicit DIKW level)
/haipipe-insight data <source>                   D-level: file observation card + check accumulation
/haipipe-insight information [--scope <D*>]      I-level: synthesize pattern from ≥2 D cards
/haipipe-insight knowledge <source>              K-level: file judged belief + check for W
/haipipe-insight wisdom [--scope <K*>]           W-level: synthesize recommendation from K cards

# Dashboard
/haipipe-insight                                 dashboard (KB state overview)
/haipipe-insight explore [project-path]          coverage scan + promotion suggestions

# OKF compatibility export
/haipipe-insight export-okf [project-path]        write derived insights/okf/ bundle

# Natural language
/haipipe-insight "<natural language>"            infer, dispatch

(For question-driven sessions: → /haipipe-application ask)
(For session machinery (plan / gate / context): → application/)
```

Path-based review is the recommended entry — you don't need to remember the
verb. Just hand it the source folder and it produces the review checklist.
Same pattern as `/haipipe-task <path>` auto-detecting task type.

---

Specialists
-----------

```
haipipe-insight-data            D-LEVEL:  writer API for observation cards → D*.md
haipipe-insight-information     I-LEVEL:  writer API for cross-D patterns → I*.md
haipipe-insight-knowledge       K-LEVEL:  writer API for judged beliefs → K*.md
haipipe-insight-wisdom          W-LEVEL:  writer API for recommendations → W*.md
haipipe-insight-review         REVIEW/APPLY: decide which cards to archive, then call writers
haipipe-insight-explore         READ:     coverage scan + promotion readiness

(Session machinery — plan / gate / context — and the question-driven
 ask workflow live in application. insight only files cards into
 the permanent KB; it does NOT run sessions or hold per-question state.)
```

---

Agents
------

Two agent families in `insight/agents/`, per DIKW type:

```
insight/agents/
  creators/                                  the headless, agent-callable path
    card-creator-data-agent.md               🟦 called by apply or explicit writer use
    card-creator-information-agent.md        🟩 called by apply or explicit writer use
    card-creator-knowledge-agent.md          🟨 called by apply or explicit writer use
    card-creator-wisdom-agent.md             🟧 called by apply or explicit writer use
  reviewers/                                 per-type quality gate
    card-reviewer-data-agent.md              🟦 accuracy + D boundary
    card-reviewer-information-agent.md       🟩 accuracy + I boundary
    card-reviewer-knowledge-agent.md         🟨 accuracy + K boundary + probe gate
    card-reviewer-wisdom-agent.md            🟧 accuracy + actionability
    index-integrity-auditor-agent.md         🔗 cross-layer: sources↔ref_by, INDEX↔files
```

Each creator calls the dual-mode haipipe-insight-<layer> skill headless. The creator is the fan-out-able subagent_type; the skill holds the filing logic. The reviewer enforces accuracy + style against `ref/dikw-boundaries.md`.

---

Function Verb Map
------------------

```
VERB-BASED:
data, observations, D-level, raw findings       -> haipipe-insight-data
information, patterns, I-level, trend           -> haipipe-insight-information
knowledge, K-level, validated belief, claim     -> haipipe-insight-knowledge
wisdom, W-level, recommendation, what next      -> haipipe-insight-wisdom
review, collect, archive cards                  -> haipipe-insight-review
explore, coverage, scan, what can we synthesize -> haipipe-insight-explore
export-okf, okf, interchange, graph export       -> scripts/export_okf.py

PATH-BASED (auto-detect source type → review checklist):
tasks/<group>/<task>/  (has results/)           -> haipipe-insight-review review
tasks/<group>/         (has child task dirs)     -> haipipe-insight-review review
probes/<MMDD>_<slug>/  (has probe.yaml)         -> haipipe-insight-review review
narratives/<slug>/                              -> haipipe-insight-review review
applications/ask/<slug>/                        -> haipipe-insight-review review

(ask / question / session / plan / gate / context → /haipipe-application; NOT insight)
(report / stakeholder doc / message / ui         → /haipipe-application; NOT insight)
```

---

Step-by-Step Protocol
----------------------

Step 0: Read `ref/review-contract.md` and `ref/insight-md-schema.md` first.
Also read `ref/card-granularity.md` and `ref/card-lifecycle.md` before filing,
merging, superseding, or reviewing cards. Every card MUST conform to the schema,
granularity policy, and lifecycle policy; every archive construction should
pass through review unless the user explicitly asks for a low-level writer.

Step 1: Detect AUTO_MODE. Same contract as task: `--auto` in args, `CLAUDE_AUTO_HANDOFF=1`, or parent skill passed `--auto`. AUTO_MODE changes ASK steps into "accept best inference or return blocked."

Step 2: Resolve scope. Cascade (highest to lowest confidence):

  (1) REVIEW/APPLY — first positional is `review` or `collect`
      → dispatch to `haipipe-insight-review`. First positional `apply`
      → dispatch to `haipipe-insight-apply`.

  (2) EXPLICIT VERB — first positional is a verb (`data` / `information` / `knowledge` / `wisdom` / `explore`) → dispatch to that specialist.

  (3) PATH-BASED AUTO-DETECT — first positional is a filesystem path → default
      to review. If args include `--file-now` or an explicit layer
      verb, dispatch to a low-level writer.

  (4) QUESTION — first positional is a question ("?" / "does" / "is" / "why" opener) → redirect to `/haipipe-application ask`.

  (5) EXPORT — first positional is `export-okf` or `okf` → run
      `scripts/export_okf.py <project-or-insights-path>` and report artifacts.

  (6) NO ARGS → Job 4 (dashboard): run explore to show KB state.

  (7) STILL AMBIGUOUS → AUTO: `status: blocked`. Interactive: ASK.


Step 2a: Source-type detection (path-based review).

  Given a path, detect what kind of scope it is and route to review:

  ```
  Scope type      Path signal                                Dispatch to
  ───────────     ──────────────────────────────────────     ─────────────────────────
  task-folder     path under tasks/ + has results/<run>/     haipipe-insight-review
  task-group      path under tasks/ + has child task dirs    haipipe-insight-review
  probe-folder    path under probes/ + has probe.yaml        haipipe-insight-review
  narrative       path under narratives/                     haipipe-insight-review
  ask-session     path under applications/ask/               haipipe-insight-review
  ```

  Detection rules:
    - `ls <path>/results/*/metrics.json` succeeds → task-folder review scope
    - `ls <path>/*/results/*/metrics.json` succeeds → task-group review scope
    - `ls <path>/probe.yaml` succeeds → probe-folder review scope
    - path contains `/narratives/` → narrative review scope
    - path contains `/applications/ask/` → ask-session review scope
    - path contains `/tasks/` or `/probes/` → matching review scope

  Low-level direct filing is still available through explicit verbs:
  `/haipipe-insight data <task>`, `/haipipe-insight knowledge <probe>`, etc.
  The default path-based behavior should produce `INSIGHT_REVIEW.yaml`, not
  silently create permanent cards.


Step 3: Resolve project root.
  Infer from the source path (walk up to the `examples/Proj*/` ancestor) or from `--project` arg or from cwd.

Step 4: Dispatch to specialist:
  - review scope → `Skill("haipipe-insight-review", args="review <scope>")`
  - apply review → `Skill("haipipe-insight-review", args="apply <INSIGHT_REVIEW.yaml>")`
  - explicit D/I/K/W verb → `Skill("haipipe-insight-<layer>", args="...")`

Step 4a: Lifecycle action choice.

  Before creating a new card, check whether the candidate should update an
  existing one:

  ```
  same reusable unit + new evidence      → merge
  same reusable unit + metadata/refs     → update
  old unit false or wrong scope          → supersede
  genuinely different reusable unit      → file
  not reusable                           → skip
  missing evidence                       → blocked
  ```

  All non-file changes MUST append `## Change log` unless they are pure
  generated-index rebuilds.

Step 5: Post-file accumulation check (Job 2). Runs ONLY after a successful file (status=ok):

  After filing a 🟦 D card:
    (1) Count D cards in insights/D_data/ that share the same task-group or tag theme.
    (2) If count >= 3 and no I card already covers this group:
        → emit in `next:`: suggest `/haipipe-insight information --scope D{NN}..D{MM}`
    (3) Update INDEX.md (add the new D card entry).

  After filing a 🟨 K card:
    (1) Check if this K card is actionable (has concrete scope + confidence > low).
    (2) If actionable and no W card already derives from this K:
        → emit in `next:`: suggest `/haipipe-insight wisdom --scope K{NN}`
    (3) Update INDEX.md (add the new K card entry).

  After filing a 🟩 I card:
    (1) Update INDEX.md.
    (2) Note: I does NOT auto-suggest K — K requires a probe (the I→K gate).

  After filing a 🟧 W card:
    (1) Update INDEX.md.

  After applying `INSIGHT_REVIEW.yaml`:
    (1) Run all required per-card reviewers.
    (2) Rebuild relevant INDEX files.
    (3) Rebuild derived views under `insights/views/` when available.
    (4) Run index-integrity-auditor-agent.
    (5) Return card ids for the caller to cite.

Step 6: Emit the structured tail:

```
status:    ok | blocked | failed
summary:   2-3 sentences (what was filed + accumulation check result)
artifacts: [paths created / updated]
next:      suggested next command (promotion suggestion if threshold met, else explore)
```

---

The Review Funnel
---------------------

insight's flow is a funnel, not a pipeline. Finished material arrives at
different rates. Review decides what deserves permanent memory:

```
task/discover material ──▶ INSIGHT_REVIEW.yaml ──▶ D / I cards
probe/lit verdicts     ──▶ INSIGHT_REVIEW.yaml ──▶ K cards
K-backed actions       ──▶ INSIGHT_REVIEW.yaml ──▶ W cards
all cards              ──▶ index + audit ─▶ project KB
```

Key constraint: the I→K gate requires a controlled comparison (a probe). No amount of I-level patterns can be promoted to K without a probe confirming them. This is what makes K cards load-bearing for paper claims and W recommendations.

---

Boundary with probe and task
---------------------------------------

**Who produces material and who files permanent cards:**

```
task        → D/I material only
probe       → K/W material only
narrative   → story gaps and review intent
application ask → question-driven review intent
insight review → D/I/K/W cards + indices + graph audit
```

Each DIKW level is partitioned by scope. No layer files cards above its scope: a task does not produce K (no hypothesis testing), a probe does not produce I (no cross-probe view).

**Dependencies:**

```
insight is CALLED BY narrative/application ask/human review
insight OWNS filing: D/I/K/W cards, INDEX, graph audit
insight NEVER triggers probe (that's application's ask kind)
insight NEVER writes to tasks/ or probes/ directly
insight ONLY writes to insights/
task/probe do not mutate insights/ as part of their core lifecycle
```

---

Relation to other top-level skills
-----------------------------------

```
discover    feeds ideas → seeded questions handled in application ask
project     project umbrella → owns the examples/Proj-X/ shape
narrative   CALLS insight review when story gaps need permanent KB refs
task        PRODUCES D/I material; direct D filing is a low-level manual option
probe       PRODUCES K/W material; direct K filing is a low-level manual option
paper       READS K + W entries → academic publication
application CALLS insight review in ask Phase 4 → files D/I/K/W cards
              drives sessions (ask / message / ui / report) that read K/W

insight is the project's PERMANENT KB. It does NOT run sessions or
own per-question state. It files cards and synthesizes cross-cutting
patterns (I) and recommendations (W). Source of "what does this project KNOW".
```

---

Files owned by this umbrella
-----------------------------

```
SKILL.md                              (this file)
ref/insight-md-schema.md              canonical entry schema (D/I/K/W)
ref/card-granularity.md               card size, merge/split, and flat-folder rules
ref/card-lifecycle.md                 file/merge/update/supersede/change-log rules
ref/insight-context-loading.md        loading strategy for callers
ref/index-templates.md                INDEX.md / K-INDEX / W-INDEX templates
ref/dikw-boundaries.md                per-layer boundary + worked examples (in ../ref/)
ref/review-contract.md               how insights/ is constructed from finished material
ref/invocation-modes.md               dual-mode contract (in ../ref/)
ref/okf-compat.md                     OKF compatibility contract and export semantics
scripts/export_okf.py                 derived OKF-style bundle exporter
```

---

Schema authority
-----------------

Every insight entry under `examples/<project>/insights/` MUST conform to `ref/insight-md-schema.md`. The 4 layer skills (data / information / knowledge / wisdom) all reference this single file as their entry schema source.

Every construction of `insights/` SHOULD follow `ref/review-contract.md`:
review, apply, card review, index, audit. Card size and merge/split choices SHOULD
follow `ref/card-granularity.md`. Card updates SHOULD follow
`ref/card-lifecycle.md`. Direct D/I/K/W filing is allowed only when the caller
already knows the card is worth archiving.

When loading insight context for a query, follow `ref/insight-context-loading.md` — layer-cascading + tag-filtering + INDEX-as-gateway.

For generic catalog / graph consumption, follow `ref/okf-compat.md`. OKF is an
export view; the DIKW card files remain the source of truth.

---

Invocation examples
--------------------

```
# Preferred: review a scope, then apply the reviewed checklist
/haipipe-insight review examples/ProjA/narratives/01_film_story/
/haipipe-insight apply examples/ProjA/narratives/01_film_story/INSIGHT_REVIEW.yaml

# Convenience: review/apply in one run when explicitly requested
/haipipe-insight review examples/ProjA/applications/ask/03_film_ood --auto

# Low-level: explicit D card from a task
/haipipe-insight data examples/ProjA/tasks/B03_band4/01_eval_h24/

# Verb-based: synthesize I pattern from accumulated D cards
/haipipe-insight information --scope D01,D02,D03

# Verb-based: explicit K card from a probe
/haipipe-insight knowledge P.0602

# Verb-based: synthesize W recommendation from K cards
/haipipe-insight wisdom --scope K01

# Dashboard: show KB state
/haipipe-insight
/haipipe-insight explore

# OKF export: write derived insights/okf/ bundle
/haipipe-insight export-okf examples/ProjA
```

---

Risk Profile
-------------

CREATES files under `examples/<project>/insights/`. Never deletes cards — only adds new ones or updates INDEX.md. Review mode writes only `INSIGHT_REVIEW.yaml`; apply mode writes cards and derived indices.

`export-okf` deletes and rebuilds only derived `insights/okf/` output. It never
edits source cards under D/I/K/W.
