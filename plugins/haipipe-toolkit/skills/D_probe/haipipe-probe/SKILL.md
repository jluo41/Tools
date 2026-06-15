---
name: haipipe-probe
description: "Research probe pipeline — drives how tasks/runs in a project roll out. Each probe is a claim-directed research thread with a 5-stage lifecycle (Design → Materialize → Harvest → Judge → Insight) and loop-back from Judge → Explore → Design. Design has two modes: interactive (human) or auto (creator-reviewer agents). Insight stage files full DIKW cascade (D → I → K → W). Contains no code — pure steering layer on top of C_task execution. Feeds E_insight and F_paper. Trigger: probe, claim, hypothesis, drive probe, plan next runs, aggregate runs, statistical test, paired-t, coverage, propose next probe, review-loop, iterate until claim holds, implement the plan, deploy probes, /haipipe-probe."
argument-hint: [function] [probe_ref_or_path] [args...]
allowed-tools: Bash, Read, Write, Edit, Grep, Glob, Skill, Workflow
metadata:
  version: "3.0.0"
  last_updated: "2026-06-11"
  summary: "Research probe pipeline — 5-stage lifecycle + loop with DIKW cascade."
  changelog:
    - "1.0.0 (2026-05-31): baseline metadata added."
    - "1.1.0 (2026-06-01): document lightweight probe folder naming (`MM-NN_slug`) plus year archive folders."
    - "1.2.0 (2026-06-01): probe folder naming switches to date-based `MMDD_slug` + `P.MMDD` refs (same-day collisions get a letter suffix)."
    - "2.0.0 (2026-06-11): IPO workflow adoption — add workflow-plan-sample.yaml (6 domain phases) + probe-lifecycle.workflow.js (4-stage lifecycle). Lifecycle section in SKILL.md."
    - "3.0.0 (2026-06-11): 5-stage lifecycle (Design/Materialize/Harvest/Judge/Insight) with loop. Two-mode Design (A: human, B: auto agents). Insight files full DIKW cascade. Loop absorbed from haipipe-probe-loop."
---

Skill: haipipe-probe (orchestrator + lifecycle engine)
=======================================================

User-facing entry for the **research probe pipeline** and owner of the
**5-stage lifecycle engine** (`ref/probe-lifecycle.workflow.js`).

Naming note: the command and folder remain `/haipipe-probe` and
`probes/` for compatibility. Conceptually this layer is
**D_probe**: each probe folder is a focused probe that asks reality
whether a candidate claim survives contact with evidence.

Two pipelines live side-by-side in a project; this skill owns the
research side and never crosses into execution:

```
EXECUTION PIPELINE          (C_task)
  task / run = 做什么、怎么做
  artifacts:  code, notebooks, configs, runtime.yaml, metrics.json
  question:   "this run, did it work?"

RESEARCH PROBE PIPELINE     (D_probe ← this skill; project folder probes/)
  probe      = 朝哪个方向探索、为什么做、接下来做什么
  artifacts:  probe.yaml, daily logs, review.md, claim, DIKW cards
  question:   "across these runs, does the hypothesis hold?"
```

A **probe is a research thread**, not a claim repository. It
steers how tasks and runs roll out: designs hypothesis → materializes arms
into C_task → harvests results → judges honesty → files DIKW insights →
loops back if the claim doesn't hold. It contains NO code, NO notebooks,
NO metrics computation; all that lives in `tasks/`.

Strict one-way dependency: probes read task artifacts; tasks never reference probes.

---

Commands
--------

```
/haipipe-probe                                  dashboard (list probes + status)
/haipipe-probe <probe>                          full lifecycle (all 5 stages + loop)
/haipipe-probe <probe> --auto                   full lifecycle, auto mode (agent-designed follow-ups)
/haipipe-probe <probe> --rounds N               full lifecycle with max N loop rounds

/haipipe-probe design <probe>                   Stage 1 only (interactive Mode A)
/haipipe-probe materialize <probe>              Stage 2 only (bridge + deploy)
/haipipe-probe harvest <probe>                  Stage 3 only (link + aggregate + claim)
/haipipe-probe judge <probe>                    Stage 4 only (structural + integrity + claim verdict)
/haipipe-probe insight <probe>                  Stage 5 only (DIKW cascade: D → I → K → W)

/haipipe-probe design new <slug>                define new probe folder (Mode A: interactive)
/haipipe-probe design link <probe> <run-path>   link a run to an arm
/haipipe-probe result aggregate <probe>         compute stats + fill result block
/haipipe-probe result claim <probe>             write final claim sentence
/haipipe-probe review <probe>                   structural QA gate
/haipipe-probe review integrity <probe>         Codex fraud-pattern audit
/haipipe-probe review claim <probe>             Codex semantic verdict
/haipipe-probe bridge <probe>                   scaffold arms in C_task + deploy
/haipipe-probe explore [project-path]           coverage map + propose next probes
/haipipe-probe inspect [<probe> | <project>]    list / status / audit (read-only)
/haipipe-probe "<natural language>"             infer verb, dispatch
```

---

Five-Stage Lifecycle + Loop
-----------------------------

Orchestrated by `ref/probe-lifecycle.workflow.js`. The lifecycle is a **loop**,
not a line — Judge can send back to Design via Explore.

See `diagram/01-probe-lifecycle.txt` for the full architecture diagram.

```
Stage 1: DESIGN — "what question to ask reality?"
  Mode A (interactive, round 1 default):
    🧑 human writes hypothesis + arms via haipipe-probe-design skill
  Mode B (auto, round ≥2 default or --auto):
    💡 probe-idea-creator-agent generates probe.yaml
    🔍 probe-idea-reviewer-agent checks (falsifiable? dup? worth compute?)
    ↺ creator-reviewer loop (max 2 rounds)
  produces: probe.yaml (hypothesis + arms + aggregation spec)

Stage 2: MATERIALIZE — "scaffold arms and make them run"
    🌉 haipipe-probe-bridge scaffolds arms as C_task tasks
    📝 Run Script Reviewer agent checks code
    🚀 sanity arm first → deploy rest → link runs to arms
  ═══════ C_task handoff: D_probe is asleep while C_task runs ═══════
  produces: tasks/<arm>/ with configs/, runs/, results/

Stage 3: HARVEST — "what did reality answer?"
    📊 haipipe-probe-result links runs + aggregates stats + writes claim
    🛡️ probe-structural-reviewer checks (N≥3, arms paired, caveats)
  produces: probe.yaml result: block + claim: sentence

Stage 4: JUDGE — "is the answer honest?"
    3 sequential gates (each independent reviewer):
      🛡️ structural reviewer → review.md
      🔬 integrity auditor  → INTEGRITY_AUDIT.md (Codex)
      ⚖️  claim verifier    → CLAIMS_FROM_RESULTS.md (Codex)
    Fail at any gate → stop.
  verdict: yes → Stage 5 (Insight)
           partial/no → Explore → loop back to Stage 1 (Design)

Stage 5: INSIGHT — "what did we learn?" (full DIKW cascade)
    Step 1: 🟦 D_data — per-arm observations
      card-creator-data-agent → card-reviewer-data-agent
    Step 2: 🟩 I_information — cross-arm patterns (needs ≥2 D cards)
      card-creator-information-agent → card-reviewer-information-agent
    Step 3: 🟨 K_knowledge — validated belief from confirmed claim
      card-creator-knowledge-agent → card-reviewer-knowledge-agent
    Step 4: 🟧 W_wisdom — actionable recommendation (optional)
      card-creator-wisdom-agent → card-reviewer-wisdom-agent
    Final: 📋 index-integrity-auditor checks cross-ref graph
  produces: insights/D_data/ + I_information/ + K_knowledge/ + W_wisdom/
```

File ownership: Design touches only `probe.yaml`. Materialize touches only
`tasks/` (via C_task). Harvest touches only `probe.yaml` result/claim blocks.
Judge touches only `review.md`, `INTEGRITY_AUDIT.md`, `CLAIMS_FROM_RESULTS.md`.
Insight writes to `insights/` (crosses into E_insight territory — the only stage that does).

**DIKW at two granularities** — parallel with C_task Stage 5 (Insight):

```
C_task Insight:   🟦 D (per-run) + 🟩 I (cross-run)        per-task level
D_probe Insight:  🟦 D (per-arm) + 🟩 I (cross-arm)        per-probe level
                  + 🟨 K (claim) + 🟧 W (next step)
D_probe D reads C_task I as input (task patterns → probe observations).
C_task stops at I; D_probe goes D → I → K → W.
```

---

The Loop
---------

```
Judge verdict = partial/no
  → 🗺️ Explore (coverage map + propose next probes)
  → Mode A: 🧑 human gate (approve/reject proposals)
    Mode B: 💡 idea-creator + 🔍 idea-reviewer (auto-generate + auto-review)
  → Back to Stage 1 (Design) with the new probe
  → Repeat until converged or budget exhausted
```

Stop conditions:

```
✅ converged        verdict = yes AND structural errors = 0 → Insight
🟡 budget_exhausted hit --rounds N without converging
🔴 blocked          Mode A: user rejected  /  Mode B: agent rejected all proposals
⏸️  paused           user interrupt
```

Mode selection:

```
round == 1 && !args.auto  →  Mode A (human designs first probe)
round >= 2 || args.auto   →  Mode B (agents design follow-up probes)
args.interactive          →  Mode A always (override for manual steering)
```

---

Specialists
-----------

Each specialist owns one lifecycle stage:

```
Stage         Specialist              Role in lifecycle
───────────   ──────────────────────  ────────────────────────────────────────
1 DESIGN      haipipe-probe-design    write probe.yaml (Mode A: interactive)
              + probe-idea-creator    generate probe.yaml (Mode B: auto)
              + probe-idea-reviewer   check idea quality (Mode B: auto)
2 MATERIALIZE haipipe-probe-bridge    scaffold arms → C_task + deploy
3 HARVEST     haipipe-probe-result    link runs + aggregate + write claim
4 JUDGE       haipipe-probe-review    structural + integrity + claim verdict
5 INSIGHT     (E_insight agents)      DIKW cascade: D → I → K → W

LOOP-BACK    haipipe-probe-explore   coverage map + propose next (between rounds)
READ-ONLY    haipipe-probe-inspect   list / status / audit (no writes)
```

haipipe-probe-loop is **absorbed** — loop logic lives in `ref/probe-lifecycle.workflow.js`.

---

Agents
------

D_probe owns 6 agents in 3 families:

```
D_probe/agents/
├── creators/
│   └── probe-idea-creator-agent     Design Mode B — auto-generate probe.yaml
├── reviewers/
│   ├── probe-idea-reviewer-agent    Design Mode B — check idea quality
│   ├── probe-structural-reviewer    Harvest + Judge — arms paired, N≥3, caveats
│   ├── probe-integrity-auditor      Judge — 5 fraud patterns (Codex)
│   └── claim-verifier-agent         Judge — evidence supports claim? (Codex)
└── advancers/
    └── probe-explorer-agent         Loop-back — coverage + propose next
```

Stage 5 (Insight) borrows 9 agents from E_insight:

```
E_insight/agents/
├── creators/   card-creator-{data,information,knowledge,wisdom}-agent
├── reviewers/  card-reviewer-{data,information,knowledge,wisdom}-agent
└──             index-integrity-auditor-agent
```

Agents are THIN pointers — logic stays in specialist SKILL.md and ref/.

---

Function Verb Map
------------------

```
new, define, create, design, hypothesis           -> design (new)
link, attach, add run, assign run                 -> design (link)
bridge, deploy, scaffold, materialize, implement,
make-runnable, run the plan, 实现实验, 部署        -> materialize (bridge)
aggregate, compute, mean+std, paired-t            -> harvest (result aggregate)
claim, conclude, write statement                  -> harvest (result claim)
review, qa, quality check                         -> judge (review structural)
audit, integrity, fraud, fake-GT, phantom results,
honesty check, scope check, leakage check         -> judge (review integrity)
verdict, judge, supports?, semantic check         -> judge (review claim)
insight, file cards, DIKW, what did we learn      -> insight (DIKW cascade)
explore, coverage, gap, propose, suggest          -> explore (loop-back)
loop, iterate, until passes, auto-review-loop,
review-loop, keep improving, --auto               -> full lifecycle with loop
inspect, list, status, show probes           -> inspect
```

---

Files Owned by This Hub
------------------------

```
SKILL.md                       (this file)
ref/
  probe-lifecycle.workflow.js  5-stage lifecycle + loop engine
diagram/
  01-probe-lifecycle.txt       architecture diagram (all stages + loop + DIKW)

../ref/                        shared across specialists:
  probe-yaml-schema.md         probe.yaml field spec + validation rules
  probe-caveats-checklist.txt  8+ confound categories
  probe-entry-template.txt     per-probe entry template (project log)
  probe-headline-template.txt  headline scoreboard skeleton
  probe-run-dashboard-template.txt  campaign run dashboard (arms × runs)
  probe-cycle-audit-template.txt    CYCLE.md — per-probe closed-loop audit
  probe-status-template.txt    canonical campaign status tracker (4 sections)
  log-format.md                daily log format
  _legacy-scope-expmt.md       migrated content reference (read-only)
```

---

Where Probes Live (project-level)
-----------------------------------

```
examples/Proj-X/
├── probes/                            ← project-level folder
│   ├── INDEX.md                            (auto: list all probes)
│   ├── coverage.md                         (auto: /explore coverage output)
│   ├── propose.md                          (auto: /explore proposals)
│   ├── comparison.md                       (auto: /result render output)
│   ├── STATUS.md                           (optional: /inspect status persist)
│   ├── RUNS.md                             (optional: /inspect runs persist)
│   │
│   ├── 0601_framing_loss-aversion/        ← active folder-per-probe
│   │   ├── probe.yaml                      source of truth (claim + arms + result)
│   │   ├── review.md                       structural QA
│   │   ├── INTEGRITY_AUDIT.md              Codex fraud-pattern check
│   │   ├── CLAIMS_FROM_RESULTS.md          Codex semantic verdict
│   │   ├── CYCLE.md                        closed-loop audit (derived)
│   │   ├── LOOP_LOG.md                     iteration history (if loop ran)
│   │   └── logs/                           daily captain's-log
│   │       ├── 2026-06-01.md
│   │       └── 2026-06-02.md
│   │
│   └── 2026-archive/                       inactive/completed probes
│       └── 0501_social-norm/
│
├── tasks/...                               (execution, C_task owns)
├── insights/...                            (DIKW cards, E_insight owns)
└── paper/...                               (claims feed F_paper)
```

Naming: active probe folders use `<MMDD>_<short-name>/` where `MMDD` is
the creation date. Same-day collision gets a letter suffix (`0601` → `0601b`).
Canonical ref: `P.<MMDD>` (e.g. `P.0601`).
Resolver accepts: `P.0601 | 0601 | probes/0601_framing_loss-aversion/`.
Inactive probes move to `probes/<YYYY>-archive/`.

NO code in probe folders — figures/tables/notebooks live in tasks/ and
are referenced via `evidence:` in probe.yaml.

---

Routing Logic
--------------

```
Step 1: Parse $ARGUMENTS.
Step 2: If probe ref + no verb → full lifecycle (probe-lifecycle.workflow.js).
        If probe ref + --auto   → full lifecycle, auto mode.
        If verb                 → resolve to specialist via verb map.
        If no args              → dashboard (list probes + status).
Step 3: Validate target (probe ref/folder/path or project path).
Step 4: Dispatch:
        lifecycle → Workflow("probe-lifecycle.workflow.js", args={...})
        specialist → Skill("haipipe-probe-<specialist>", args="<verb> <rest>")
Step 5: Surface specialist tail or lifecycle summary.
```

---

Specialist Return Contract
---------------------------

```
status:    ok | blocked | failed
summary:   2-3 sentences
artifacts: [paths created / read]
next:      suggested next command
```

---

Relation to Other Layers
-------------------------

```
A_discover    feeds ideas  → suggested probes
C_task        provides runs → linked into probe arms
              Stage 5 files D + I per task → D_probe Insight reads as input
E_insight     receives DIKW cards from Stage 5 (Insight)
F_paper       consumes confirmed claims for paper writing

D_probe is the central research hub: reads from C_task, writes claims
and DIKW cards that feed E_insight (knowledge base) and F_paper (writing).
```
