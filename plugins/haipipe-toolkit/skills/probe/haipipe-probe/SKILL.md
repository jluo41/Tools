---
name: haipipe-probe
description: "Research probe pipeline — sandwich lifecycle around discovery/task evidence work. Probe-open designs the research contract and dispatches discovery refs plus task contracts; discoveries and task run independently; Probe-post resumes after completion to harvest and judge the claim. Insight/DIKW export is deferred. Contains no code — pure steering/interpretation layer. Trigger: probe, claim, hypothesis, drive probe, plan next runs, dispatch tasks, dispatch discoveries, aggregate runs, statistical test, paired-t, coverage, propose next probe, review-loop, iterate until claim holds, /haipipe-probe."
argument-hint: [function] [probe_ref_or_path] [args...]
allowed-tools: Bash, Read, Write, Edit, Grep, Glob, Skill, Workflow
metadata:
  version: "3.2.0"
  last_updated: "2026-06-19"
  summary: "Research probe pipeline — sandwich lifecycle: Probe-open → discoveries/tasks → Probe-post; insights deferred."
  changelog:
    - "1.0.0 (2026-05-31): baseline metadata added."
    - "1.1.0 (2026-06-01): document lightweight probe folder naming (`MM-NN_slug`) plus year archive folders."
    - "1.2.0 (2026-06-01): probe folder naming switches to date-based `MMDD_slug` + `P.MMDD` refs (same-day collisions get a letter suffix)."
    - "2.0.0 (2026-06-11): IPO workflow adoption — add workflow-plan-sample.yaml (6 domain phases) + probe-lifecycle.workflow.js (4-stage lifecycle). Lifecycle section in SKILL.md."
    - "3.0.0 (2026-06-11): 5-stage lifecycle (Design/Materialize/Harvest/Judge/Insight) with loop. Two-mode Design (A: human, B: auto agents). Insight files full DIKW cascade. Loop absorbed from haipipe-probe-loop."
    - "3.1.0 (2026-06-19): reframe lifecycle as sandwich: Probe-open (Design/Dispatch) → task execution pause → Probe-post (Harvest/Judge); insights deferred."
    - "3.2.0 (2026-06-19): add discoveries/ as external-evidence work, sibling to tasks/ and referenced by probes."
---

Skill: haipipe-probe (orchestrator + lifecycle engine)
=======================================================

User-facing entry for the **research probe pipeline** and owner of the
**sandwich lifecycle engine** (`ref/probe-lifecycle.workflow.js`).

Naming note: the command and folder remain `/haipipe-probe` and
`probes/` for compatibility. Conceptually this layer is
**probe**: each probe folder is a focused probe that asks reality
whether a candidate claim survives contact with evidence.

Three work areas live side-by-side in a project; this skill owns the claim
contract and never crosses into execution:

```
DISCOVERY PIPELINE          (discover artifacts)
  discovery = 外部世界已经知道什么
  artifacts:  discoveries/<id>/{discovery.yaml,sources.md,notes.md,verdict.md}
  question:   "what does prior work / web evidence say?"

EXECUTION PIPELINE          (task)
  task / run = 做什么、怎么做
  artifacts:  code, notebooks, configs, runtime.yaml, metrics.json
  question:   "this run, did it work?"

RESEARCH PROBE PIPELINE     (probe ← this skill; project folder probes/)
  probe      = 朝哪个方向探索、为什么做、接下来做什么
  artifacts:  probe.yaml, status.yaml, site.md, review.md, claim verdict sidecars
  question:   "across these runs, does the hypothesis hold?"
```

A **probe is a research contract**, not a container for tasks. It is the
bread around the task sandwich:

```
PROBE-OPEN     design the question + dispatch executable task contracts
MIDDLE WORK    discoveries check external evidence; tasks run internal work
PROBE-POST     resume later; harvest, judge, decide next probe
```

The probe opens a question, hands external-evidence work to `discoveries/` and
execution work to task, then pauses. When linked discoveries/tasks finish,
the probe resumes and interprets the evidence. It contains NO code, NO
notebooks, NO metrics computation; all that lives in `tasks/`. It also should
not store literature bodies; those live in `discoveries/`.

Strict one-way dependency: probes read discovery/task artifacts; discoveries
and tasks never interpret probe claims.

---

How to Use the Sandwich
-----------------------

Think of a probe as a claim-level bracket around evidence work:

```
Probe-open
  "I believe claim C might be true. To test it, I need discoveries A/B and tasks C/D."
  writes: probe.yaml hypothesis, evidence plan, success criteria, dispatch refs
  ends:   status=waiting_for_evidence

Discovery
  "I check the outside world."
  writes: sources.md, notes.md, verdict.md

Task
  "I run our internal code/data/model work."
  writes: runtime.yaml, metrics.json, reports, audits

Probe-post
  "Given those discovery/task artifacts, is claim C supported?"
  writes: result block, claim sentence, review/verdict sidecars
```

Do not put discoveries or tasks inside the probe mentally. The probe does not
own the work; it owns the question before the work and the interpretation
after the work.

Use it like this:

1. `/haipipe-probe open <probe|new>` when you know the claim to test.
2. Run or wait for dispatched discoveries and task work to finish.
3. `/haipipe-probe post <probe>` to harvest evidence artifacts and judge the claim.
4. If the verdict is weak, open the next probe; if it is strong, return to Narrative-post.

In one sentence: **Probe asks, discoveries/tasks answer, Probe judges.**

---

Commands
--------

```
/haipipe-probe                                  dashboard (list probes + status)
/haipipe-probe open <probe|new>                 probe-open: design + dispatch, then pause
/haipipe-probe post <probe>                     probe-post: harvest + judge after evidence finishes
/haipipe-probe resume <probe>                   alias for post
/haipipe-probe <probe>                          full sandwich, only for small/auto runs
/haipipe-probe <probe> --auto                   auto follow-up design after post verdict needs more work
/haipipe-probe <probe> --rounds N               max N sandwich cycles

/haipipe-probe design <probe>                   Open stage 1 only (interactive Mode A)
/haipipe-probe dispatch <probe>                 Open stage 2 only (bridge + task handoff)
/haipipe-probe harvest <probe>                  Post stage 1 only (link + aggregate + claim)
/haipipe-probe judge <probe>                    Post stage 2 only (structural + integrity + claim verdict)
/haipipe-probe insight <probe>                  deferred export; not part of core N/P/T stack

/haipipe-probe design new <slug>                define new probe folder (Mode A: interactive)
/haipipe-probe design link <probe> <run-path>   link a run to an arm
/haipipe-probe result aggregate <probe>         compute stats + fill result block
/haipipe-probe result claim <probe>             write final claim sentence
/haipipe-probe review <probe>                   structural QA gate
/haipipe-probe review integrity <probe>         Codex fraud-pattern audit
/haipipe-probe review claim <probe>             Codex semantic verdict
/haipipe-probe bridge <probe>                   scaffold/dispatch task arms
/haipipe-probe explore [project-path]           coverage map + propose next probes
/haipipe-probe inspect [<probe> | <project>]    list / status / audit (read-only)
/haipipe-probe "<natural language>"             infer verb, dispatch
```

---

Sandwich Lifecycle + Loop
--------------------------

Orchestrated by `ref/probe-lifecycle.workflow.js`. The lifecycle is not a
continuous parent-child flow. It is a contract/resume flow:

See `diagram/01-probe-lifecycle.txt` for the full architecture diagram.

```
PROBE-OPEN A: DESIGN — "what question to ask reality?"
  Mode A (interactive, round 1 default):
    🧑 human writes hypothesis + arms via haipipe-probe-design skill
  Mode B (auto, round ≥2 default or --auto):
    💡 probe-idea-creator-agent generates probe.yaml
    🔍 probe-idea-reviewer-agent checks (falsifiable? dup? worth compute?)
    ↺ creator-reviewer loop (max 2 rounds)
  produces: probe.yaml (hypothesis + arms + aggregation spec)

PROBE-OPEN B: DISPATCH — "what evidence work must exist to answer it?"
    🔍 discover artifacts become discoveries/ refs for external evidence
    🌉 haipipe-probe-bridge scaffolds arms as task task contracts
    📝 Run Script Reviewer agent checks code
    🚀 optionally sanity-check/deploy, then link known run paths to arms
  produces: discovery refs + task refs + run refs in probe.yaml
  terminal state: status=waiting_for_evidence

══════ Evidence interval: probe is paused while discoveries/tasks run ══════
    ✋ discover owns search/read/review outputs in discoveries/
    ✋ task owns plan/build/execute/report
    ✋ Discovery/task results are readiness signals, not child objects inside probe
  produces: discoveries/<id>/{sources.md,notes.md,verdict.md}
  produces: tasks/<arm>/results/<run>/{runtime.yaml,metrics.json,...}

PROBE-POST A: HARVEST — "what did reality answer?"
    📊 haipipe-probe-result reads discovery verdicts + links runs + aggregates stats + writes claim
    🛡️ probe-structural-reviewer checks (N≥3, arms paired, caveats)
  produces: probe.yaml result: block + claim: sentence

PROBE-POST B: JUDGE — "is the answer honest?"
    3 sequential gates (each independent reviewer):
      🛡️ structural reviewer → review.md
      🔬 integrity auditor  → INTEGRITY_AUDIT.md (Codex)
      ⚖️  claim verifier    → CLAIMS_FROM_RESULTS.md (Codex)
    Fail at any gate → stop.
  verdict: yes → close probe or return to Narrative-post
           partial/no → Explore → new Probe-open cycle

DEFERRED EXPORT: INSIGHT / DIKW
    Not part of the current Narrative/Probe/Task core stack.
    Later, a separate export layer may turn closed probes into DIKW cards.
  produces now: probe.yaml result + claim + verdict sidecars
```

File ownership: Design touches only `probe.yaml`. Dispatch may request
discoveries and task artifacts and write refs back to `probe.yaml`, but
discovery work remains discover-owned and execution remains task-owned.
Harvest touches only `probe.yaml` result/claim blocks. Judge touches only
`review.md`, `INTEGRITY_AUDIT.md`, `CLAIMS_FROM_RESULTS.md`. Insights/DIKW are
parked for a later export layer.

**Core boundary** — task produces execution artifacts; probe interprets them:

```
discover output: discoveries/<id>/{sources.md,notes.md,verdict.md}
task output:     runtime.yaml + metrics.json + workflow/report*.yaml + RUN_AUDIT.md
probe output:    result block + claim sentence + integrity/claim verdict
Narrative reads:   probe verdicts and claim sidecars directly for now.
```

Discovery artifact schema authority:
`discover/haipipe-discover/ref/discovery-yaml-schema.md`.

---

The Loop
---------

```
Probe-post verdict = partial/no
  → 🗺️ Explore (coverage map + propose next probes)
  → Mode A: 🧑 human gate (approve/reject proposals)
    Mode B: 💡 idea-creator + 🔍 idea-reviewer (auto-generate + auto-review)
  → New Probe-open cycle
  → Repeat until converged or budget exhausted
```

Stop conditions:

```
✅ converged        verdict = yes AND structural errors = 0 → close / narrative-post
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
OPEN DESIGN   haipipe-probe-design    write probe.yaml (Mode A: interactive)
              + probe-idea-creator    generate probe.yaml (Mode B: auto)
              + probe-idea-reviewer   check idea quality (Mode B: auto)
OPEN DISPATCH haipipe-probe-bridge    scaffold/dispatch arms → task, then pause
POST HARVEST  haipipe-probe-result    link runs + aggregate + write claim
POST JUDGE    haipipe-probe-review    structural + integrity + claim verdict
DEFERRED      (future export layer)   optional DIKW/insight filing

LOOP-BACK    haipipe-probe-explore   coverage map + propose next (between rounds)
READ-ONLY    haipipe-probe-inspect   list / status / audit (no writes)
```

haipipe-probe-loop is **absorbed** — loop logic lives in `ref/probe-lifecycle.workflow.js`.

---

Agents
------

probe owns 6 agents in 3 families:

```
probe/agents/
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

Deferred Insight export would borrow agents from insight:

```
insight/agents/
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
bridge, deploy, scaffold, dispatch, implement,
make-runnable, run the plan, 实现实验, 部署        -> open dispatch (bridge)
open, pre, plan-and-dispatch, start probe         -> probe-open
post, resume, close, summarize after task         -> probe-post
aggregate, compute, mean+std, paired-t            -> harvest (result aggregate)
claim, conclude, write statement                  -> harvest (result claim)
review, qa, quality check                         -> judge (review structural)
audit, integrity, fraud, fake-GT, phantom results,
honesty check, scope check, leakage check         -> judge (review integrity)
verdict, judge, supports?, semantic check         -> judge (review claim)
insight, file cards, DIKW, what did we learn      -> deferred export
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
  probe-lifecycle.workflow.js  sandwich lifecycle + loop engine
diagram/
  01-probe-lifecycle.txt       architecture diagram (open/task/post loop)

../ref/                        shared across specialists:
  probe-yaml-schema.md         probe.yaml field spec + validation rules
  probe-caveats-checklist.txt  8+ confound categories
  probe-entry-template.txt     per-probe entry template (_haipipe project log)
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
├── _haipipe/
│   ├── project.log.jsonl                  single append-only event log
│   ├── project.status.yaml                project snapshot
│   └── project.site.md                    project dashboard
│
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
│   │   ├── status.yaml                     current probe snapshot
│   │   ├── site.md                         human-readable probe page
│   │   └── CYCLE.md                        closed-loop audit (derived)
│   │
│   └── 2026-archive/                       inactive/completed probes
│       └── 0501_social-norm/
│
├── discoveries/...                         (external evidence, discover owns)
├── tasks/...                               (internal execution, task owns)
├── insights/...                            (deferred export layer; not core N/P/T)
└── paper/...                               (claims feed paper)
```

Naming: active probe folders use `<MMDD>_<short-name>/` where `MMDD` is
the creation date. Same-day collision gets a letter suffix (`0601` → `0601b`).
Canonical ref: `P.<MMDD>` (e.g. `P.0601`).
Resolver accepts: `P.0601 | 0601 | probes/0601_framing_loss-aversion/`.
Inactive probes move to `probes/<YYYY>-archive/`.

NO code in probe folders. Literature/source evidence lives in discoveries/.
Figures/tables/notebooks live in tasks/. Both are referenced from probe.yaml.

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
discover    provides discoveries/ → external evidence linked into probe evidence_refs
task        provides tasks/runs   → internal execution linked into probe evidence_refs
              neither layer interprets probe claims
insight     deferred export layer (parked while focusing on N/P/T)
paper       consumes confirmed claims for paper writing

probe is the central research hub: opens research contracts, pauses while
discoveries/tasks run, resumes to write claims/verdicts that feed Narrative-post.
```
