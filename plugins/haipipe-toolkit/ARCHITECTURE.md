haipipe-toolkit — Architecture (the whole world)
==================================================

Rewritten 2026-07-14 against `Tools/plugins/haipipe-toolkit/diagram/260714-probe-qa/` v3 (APPROVED by JL, rulings R1-R18). This is
the TOP-LEVEL vision: how the pieces fit together, from evidence to deliverable. Read this
FIRST. Per-layer contracts live in the skills themselves — this doc says only what no single
SKILL.md can say, because it is about the relationships BETWEEN them.

The one thing to get right is the **probe** — the paper-level Q/A map that binds a paper's
questions to the project's evidence bank. It has its own section, and it is the center of
gravity of the whole system. Its constitution is `skills/probe/haipipe-probe/SKILL.md`; where
this file and that file disagree, **that file wins**.


TL;DR — one loop, two banks
============================

There is a KNOWLEDGE BANK and a DELIVERY BANK, and one map between them.

```
   🧠 KB — what the project KNOWS               📰 DELIVERY — what the project SAYS
        tasks/      discoveries/        ⇄        papers/  applications/
       (inside)      (outside)        📄 probe   (each: 0-lifecycle stages, DPRC phases)
                                     (paper-side)
```

Everything else is one-way plumbing. This link is the only double arrow, and it is the engine:

- **KB → Delivery (induction).** A returned finding ignites an angle you had not planned.
  Facts tell you the story.
- **Delivery → KB (deduction).** A stage hits a claim whose evidence is GAP or weak, so it
  commissions a question. The story tells you which evidence to go get.

Either direction alone breaks:

- KB only (run everything, then invent a story) = a heap of results nobody can sell.
- Delivery only (fix the story, then go find data) = hunting for evidence to fit a conclusion.

Walking on two legs — alternating — is what "research" means here. In the live machinery, that
alternation is literally the stage loop — every stage runs the same four phases:
`DRAFT → PROBE → REVISE → CHECK` (DPRC). DRAFT raises the question; PROBE maps it to the bank;
REVISE weaves the answer in; CHECK is the human gate.


THE PROBE — a paper-level Q/A map (v3, 2026-07-14)
===================================================

**A probe is a PAPER-LEVEL DOCUMENT. Nothing else.** It is not a bridge with a foot on each
bank, it is not a gateway agent, it is not a folder in the execution tree. It is a file that
lives on the delivery side and NOWHERE else:

```
   papers/<Paper-X>/1-probes/PPNN_<topic>.md          ← one file per TOPIC
   applications/<App-X>/1-probes/PPNN_<topic>.md      ← identical shape
```

It is GENERATED in the PROBE phase, from the questions the DRAFT stage raised (the Q-papers:
`{VAL:?}` slots, GAP markers, open questions). Each Q-paper becomes ONE SECTION of the file.

⛔ The words **"row"** and **"table"** are BANNED in this layer. It is a **Q-paper**, in its own
**SECTION**. No markdown tables inside a probe file, ever.


The anatomy, in one screen
--------------------------

```
   # PP03 — WellDoc data feasibility
   - mode: light | full

   ## Why            🔒 ONE per file. The STAKE ("C6 dies if WellDoc has a cycle label").
                        Paper vocabulary. NEVER leaves this file. NEVER dispatched.

   ## Q1 — cycle indicator                      ← one Q-paper, one SECTION
   - serves:  1-claims (C6)                        which stage / claim of MY paper
   - target:  tasks/A03_welldoc_cycle_check/01_column_scan/QA/1-cycle-indicator.md
   - state:   read                                 DERIVED from disk, never asserted
   - commission: |                                 the Q-general — T1-translated,
       Scan all 40 WellDoc CSV tables for          paper-agnostic, FROZEN.
       menstrual/cycle/hormone columns …          👉 THE DISPATCH PAYLOAD, and nothing else is.
   - reading: |                                    the A-paper — T2 interpretation,
       No cycle column in 40 tables ⇒ C6           written at harvest.
       supported → 1-claims.md C6 flips

   ## Q2 — female CGM volume  …

   - values: … · sources: … · displays: …       ← the HARVEST LANES (feed _VALUES_, .bib, displays)
```

**The field set** (this is the whole closed list — `check-probe-cards.sh` recognises these 13 keys
and nothing else):

```
   FILE       mode:                              light | full
   ─────────  ─────────────────────────────────  ────────────────────────────────────
   CORE ×5    serves: target: state:             every section, always
              commission: reading:
   ─────────  ─────────────────────────────────  ────────────────────────────────────
   HARVEST    values: sources: displays:         OPTIONAL — the lanes that feed
                                                 _VALUES_ / .bib / the display units
   ─────────  ─────────────────────────────────  ────────────────────────────────────
   BUILD LANE owner: eta: blocks:                MANDATORY at `state: commissioned`
              cross-project:                     (see THE BUILD LANE below — the
                                                 checker HARD FAILs a commissioned
                                                 section without all four)
```

(`Takeaways` is DEAD → it is `reading`. `Verdict` is DEAD entirely — see below.)


R1 — BINDING IS BY PATH, NOT BY ID
-----------------------------------

A section's `target:` is a PATH to the answering FILE. **PP numbers are PAPER-LOCAL footnote
numbers** — two papers may both carry a PP04 the way two books both carry a footnote 4. Nothing
collides, because **no PP id ever crosses to the bank**. There is no ledger, no shared namespace,
nothing to renumber, nothing to grep.

Point at the FILE, never the folder: a leaf that answered three things cannot tell you which of
them is yours.


R2 — THE BANK IS PROBE-UNAWARE (but not question-deaf)
-------------------------------------------------------

```
   under tasks/ and discoveries/ there is:
   ❌ NO _ASK/ folder     ❌ NO _ANS/ folder     ❌ NO `answers:` field     ❌ NO PP id, anywhere

   ✅ its own plan.yaml / discovery.yaml           Q-general, code-oriented   (executor's own)
   ✅ its own results/ · sources.md / verdict.md   A-general, code-oriented   (executor's own)
   ✅ an OPTIONAL QA/ folder                       A-general, READABLE        (executor's own)
```

**The QA/ folder is the readable A-general.** It applies to BOTH banks — task and discovery are
both EXECUTORS, same shape, same rules:

```
   tasks/A03_welldoc_cycle_check/01_column_scan/    discoveries/L03_cycle/01_prior_art/
   ├── workflow/plan.yaml     Q  code               ├── discovery.yaml           Q  spec
   ├── results/               A  code               ├── sources.md · verdict.md ·
   └── QA/                    A  readable           │   landscape.md             A  raw
       ├── 1-cycle-indicator.md                     └── QA/               A  readable
       └── 2-female-cgm-volume.md                       └── 1-cycle-prior-art.md

   NAMING IS THE INDEX:  QA/<n>-<slug>.md, n = creation order.  `ls QA/` IS the index.
   SLUG ONLY — a PP id in a bank filename is R2 broken.
   WRITE-ONCE — a later question ADDS QA/<n+1>-<slug>.md; nothing frozen is ever edited.

   each file:   # Q — <the question, self-contained, general language>
                ## Answer    plain words + [→ results/<file>] / [→ sources.md#S02] anchors
                ## Caveats   what this does NOT establish
                ## Not-done  what was asked but not resolved, and why
```

Three reasons a QA file may exist (there is no fourth): **commissioned** (a dispatch named it) ·
**digest-only** (the artifacts already answer it; write the digest, run no code) ·
**executor's own** (a session judged a finding worth digesting — including proactive
answerability work).


The `qa` verb — the executor's question door
--------------------------------------------

The bank answers questions without ever learning who asks, or why. That is what the `qa` verb is:

```
   /haipipe-task qa "<question>" [<leaf>]     ·     /haipipe-discovery qa "<question>" [<leaf>]

   input: ONE question, in GENERAL language — no PP id, no paper ref, no stake.

     ① QA SCAN   grep <leaf>/QA/*.md — already answered?  → return the QA file PATH        ~0
     ② DIGEST    results/ (or sources.md) answer it, but no readable digest exists?
                 → write QA/<n>-<slug>.md from EXISTING artifacts, run no code           cheap
     ③ P-B-E-R   neither → Plan→Build→Execute→Report at the SHALLOWEST depth that answers
                 it, then write the QA file
     🚫 REFUSE   out of scope for this executor / this leaf → the caller RE-ROUTES

   the ENRICH depth ladder (the EXECUTOR picks; the probe NEVER learns which):
     depth 0 📖 READ        enter at R:  write the QA file · nothing runs
     depth 1 ⚙️ NEW RUN     enter at E:  + configs/<new>.yaml + runs/<new>/
     depth 2 🔧 NEW SCRIPT  enter at B:  + <new>.py + plan-script-<new>.yaml
     depth 3 🌱 NEW LEAF    full P-B-E-R from P: a sibling leaf
   scope test (2 vs 3): does it fit THIS leaf's plan.yaml IPO — same inputs, same process family?

   THREE CALLERS, one door:
     📄 the PROBE's DISPATCH     — via the executor orchestrator agents
     🧑 a HUMAN, directly        — the everyday "go explore this direction" verb
     🤖 the ORCHESTRATOR itself  — self-directed answerability work
```

💀 The old probe-AWARE `asks` verb (read `_ASK/` stubs, resolved PPNN ids) is DEAD. `qa` is its
probe-UNAWARE rebirth.


Who writes what — the writer table (R12)
-----------------------------------------

```
   file                                    writer            reader
   ─────────────────────────────────────   ───────────────   ─────────────────
   papers/X/1-probes/PPNN_<topic>.md       this paper        this paper
   papers/X/1-claims.md                    this paper        this paper
   tasks/<leaf>/workflow/plan.yaml         the task layer    task · probe(match)
   tasks/<leaf>/results/ · QA/*.md         the task layer    task · probe(harvest)
   discoveries/<leaf>/terminal · QA/*.md   discovery layer   disc · probe(harvest)
   ⇒ no shared writes anywhere. Paper and executor sessions run weeks apart, lock-free.
```

**CC-8 — the PROBE CAUSES a QA file; the EXECUTOR AUTHORS it.** Causing is not authoring, and
that difference IS the wall. A probe session has `## Why` in its context; if it opens `results/`
and writes the digest itself, the stake travels into the bank — that is literally how
`tasks/A03_welldoc_cycle_check/result.md` ended up carrying "C6", "C7" and "claims-stage".

So when a probe meets a bare `results/` with no digest, it does NOT write the digest. It
DISPATCHES a digest-only run (qa path ②): a clean-context agent reads `results/` and writes
`QA/<n>-<slug>.md`. The file the probe wanted comes into existence BY the probe's action — but
through the executor's hand. That one hop is the entire wall.


TWO SESSION MODES (R17) — and why most probes should cost nothing
==================================================================

This is the ruling that makes the whole thing affordable. **The executor session is NOT
question-driven.** (Orientation convention, kept from JL 2026-07-12: execution on the LEFT,
consumer on the RIGHT — matching the two-terminal workflow.)

```
   ⚙️ LEFT — executor session                📄 RIGHT — consumer session
   ═══════════════════════════              ═══════════════════════════
   just runs P-B-E-R                        asks questions
   train · sweep · profile · review         DRAFT raises Q-papers →
   — no question needed, no ask.            PROBE collects, matches,
   this IS the project's research           commissions
        │                                        │
        ▼                                        ▼
   the bank grows AUTONOMOUSLY   ◀────  probes mostly land HERE (T2 REUSE):
   plan.yaml · results/ · sources.md    in a healthy project most answers
        │                               ALREADY EXIST before anyone asks
        │
        └─ 🆕 ANSWERABILITY WORK — also executor-session work, probe-unaware:
           · write QA/ digests for notable findings
           · build / refactor code so future questions are CHEAP to answer
           it does not know WHICH questions will come. It makes the bank
           EASIER TO ASK. That is task-native work, not probe work.
```

Consequence: **a commission is the EXCEPTION, not the norm.** A probe file whose every section
is a fresh commission is a smell — either the MATCH was lazy, or the bank is starving.


The five-step loop, and the cost ladder
========================================

```
  📝 DRAFT      raises the Q-papers ({VAL:?}, GAP, open questions)
                       │
  ① ORGANIZE   PROBE phase: collect them → probe files, grouped by TOPIC
                       │
  ② MATCH      per Q-paper, against the READABLE corpus:
               grep {tasks,discoveries}/**/QA/*.md   (+ the qa verb, CHECK-ONLY mode)
                       │
       ┌───────────────┼──────────────────┬───────────────────┐
       ▼               ▼                  ▼                   ▼
   ✅ HIT          🟡 PARTIAL         🟠 LEAF EXISTS       🔴 NOTHING
   a QA file       answers Q1,        never asked this     no leaf
   answers it      not Q2                 │                   │
       │               └───────┬──────────┘                   │
       │                       ▼                              ▼
       │        ③ DISPATCH  the `commission` block goes, VERBATIM, to the EXISTING
       │                    executor orchestrators — there is NO gateway:
       │                      Agent(haipipe-task-orchestrator-agent)
       │                      Agent(haipipe-discovery-orchestrator-agent)
       │                    THEIR CLEAN CONTEXT IS THE WALL. Inside, each runs
       │                    the qa gate: ① answered → path  ② digest  ③ P-B-E-R.
       │                    Returns: a PATH to the answering QA file.
       │                       │
       └──────────┬────────────┘
                  ▼
  ④ POINT     the section's target: → the answering QA FILE (not the folder)
                  ▼
  ⑤ INTERPRET the section's reading: (T2) · 1-claims.md flips · the lanes harvest
```

**The cost ladder (R13).** Cheap doors first; only T3/T4 summon an agent.

```
  T0  JOIN     another stage's probe already asks this Q-paper  → add my serves:      ~0
  T1  LOCAL    my own registries answer it                      → answered-local      ~0
  T2  REUSE    an existing QA file answers it                   → point the section   1 grep + 1 read
  T3  ENRICH   the leaf exists, but was never asked this        → new section → ③     agent
  T4  FRESH    no leaf                                          → new section → ③     agent
```

**R14 — MATCH ON THE ANSWER, NEVER ON THE TOPIC.** Two probes can look like the same topic
("characterize WellDoc") and want completely different facts. A HIT counts ONLY if the QA file
LITERALLY ANSWERS THIS Q-paper. **Read the QA file.** Topic similarity is not evidence; if it
does not answer the question, it is a T3 ENRICH — dispatch it, do not point at it.


The two LAWS (the wall is a DISPATCH rule, not a file rule)
===========================================================

The live leak that proves it: `tasks/A03_welldoc_cycle_check/result.md` carries a paper's claim
ids — written with NO probe file, NO mailbox, NO stub, NO id involved anywhere. The stake
traveled through a paper session's own CONTEXT, because that session did bank work INLINE.

```
   ✅ paper ──▶ 🤖 executor ORCHESTRATOR (clean context, gets ONLY the commission)
              ──▶ qa verb ──▶ bank                                        WALL HOLDS
   ❌ paper session RUNS bank work or WRITES bank files itself,      WALL NEVER EXISTED
      stake in context

   ✅ LEGAL, and REQUIRED: a READ-ONLY grep of {tasks,discoveries}/**/QA/*.md.
      That IS ② MATCH. Nothing leaves the paper; nothing is written; no code runs.
      The wall bans the PEN and the RUN, not the EYE.
```

**LAW 1 — A CONSUMER SESSION NEVER EXECUTES TASK/DISCOVERY WORK INLINE.**
Dispatch means: hand the `commission` block, VERBATIM, and nothing else. Never `## Why`. Never
the probe file. Never the paper. The law names the ACT, not the tool: a consumer session breaks it
the moment it RUNS bank work (a script, a P-B-E-R stage) or WRITES a bank file — including a QA
digest it thinks it is being helpful by authoring. Reading the QA corpus to MATCH is not that.

**LAW 2 — BACKSTOP LINT, ON TWO SURFACES.**

```
   📄 probe files:  commission blocks carry no C\d, no H\d, no stake words
                    ("rescue", "we want", "the hoped-for", "the probe that could save …")
   ⚙️ the bank:     QA/*.md carry no consumer vocabulary
                    (C\d, H\d, "claims-stage", "the paper" meaning *our* paper)
```

LAW 2 would have caught A03. The v1 `_ASK` bridge pass never could — A03 had no `_ASK`.
⚠️ LAW 2 is a BACKSTOP, not the mechanism. T1 (translate-down) is SEMANTIC; a regex provably
misses real leaks. Never delete T1 on the theory that the lint will catch what slips past.

Mechanically enforced by `check-probe-cards.sh` (which KEEPS its filename; only its internals
were rewritten for question sections).


Statuses are DERIVED from disk, never asserted
===============================================

```
   state             disk fact
   ──────────────    ─────────────────────────────────────────────────────────
   planned           the section exists · the target leaf is missing (or `NEW …`)
   commissioned      the leaf + its plan.yaml exist · the QA file is absent
   answered          the target QA FILE exists
   read              the section's reading: is non-empty
                     (+ 1-claims.md flipped, if the section serves a claim)
   answered-local    target points into the paper's OWN registries; no dispatch
   failed            a reading with a dead target · the leaf was deleted · qa REFUSEd
   ──────────────    ─────────────────────────────────────────────────────────
   the probe FILE    the aggregate of its sections — the board renders it
   💀 "verdicted"    DELETED
```

**THE BUILD LANE.** Some sections legitimately take DAYS TO WEEKS (task-for-data / -algo / -fit,
a long acquisition). Those sit at `commissioned` for a long time, and that is HONEST. The price
of passing the gate is a DATE: at `state: commissioned` a section MUST carry
`owner:` · `eta: YYYY-MM-DD` (still in the FUTURE) · `blocks:` · `cross-project:`. An eta in the
future PASSES; an eta PASSED with no QA file is a HARD FAIL. Without that test, `commissioned`
becomes the state every un-run section wears, and the mechanism ships as a laundering token.

⚠️ **A section still `commissioned` WHEN THE GATE RUNS is BY DEFINITION build-lane.** There is
no "fast commission" exemption — a minutes-long dispatch that has actually returned is `answered`
(its QA file exists) or `read`, not `commissioned`. So the four fields are unconditional at that
state, and `check-probe-cards.sh` enforces them with no lane test: `commissioned-no-owner` /
`-no-eta(need YYYY-MM-DD)` / `-no-blocks` / `-no-cross-project(path or 'none-found')`.

**NO "Verdict".** The word is dead. The section's `reading` carries A-paper; the CLAIM's status
(`supported | refuted | inconclusive` + confidence + claim_type + the G1/G2/G3 gates) lives in
`1-claims.md` — per-claim, per-paper, PRIVATE. Two papers judging the same A-general against
their own claims run two reviews. That is correct spend, not duplication.
⚠️ A DISCOVERY's own `verdict.md` (the Review-type terminal file) is a DIFFERENT thing. It is
executor-native and it SURVIVES.


The layers
==========

```
Layer        Role                  Unit                          Lifecycle / phases            Folder
──────────── ───────────────────── ───────────────────────────── ───────────────────────────── ──────────────
task         inside execution      one task-folder               Plan → Build → Execute →      tasks/
             code, runs, metrics                                 Report   (+ the `qa` door)
discovery    outside evidence      one topic-folder              same 4 stages ×               discoveries/
             literature, prior art                               Search | Review | Idea
── KB = the two above: the project's single source of truth about facts ──
probe        the paper's Q/A map   one PPNN probe file           organize → match → dispatch   papers/<P>/1-probes/
             (paper-side ONLY)     (one topic, N sections)       → point → interpret           applications/<A>/1-probes/
── the double arrow: KB ⇄ Delivery ──
paper        academic delivery     one manuscript                7 stages × DPRC phases        papers/
application  non-academic delivery one report / message / UI     same stage model              applications/
```

Four things worth saying plainly, because agents get them wrong:

- **The probe owns no folder in the EXECUTION tree.** Its only files are the paper's own
  `1-probes/PPNN_<topic>.md`. There is no `probes/` directory, no `probe.yaml`, no `_ASK/`,
  no `_ANS/`. (Legacy `probes/` dirs still on disk in older projects are dead history: nothing
  reads them, nothing writes them, nothing deletes them.)
- **There is no probe GATEWAY agent.** `haipipe-probe-orchestrator-agent` was RETIRED 2026-07-14:
  its SWEEP became the paper-side MATCH, and its dispatch became a direct `Agent()` call on the
  two executor orchestrators. It was a third clean context standing in front of two that already
  had one. What SURVIVES is the `haipipe-probe-review` skill + `haipipe-probe-reviewer-agent` —
  paper-side claim judging.
- **Narrative is not a layer.** It is one stage inside a paper (`0-lifecycle/3-narrative/`).
  Likewise seed, resource, claims, venue, pitch, display, section-edit.
- **There is no insight layer.** RETIRED 2026-07-12 (JL). No `insights/`, no D/I/K/W cards, no
  `/haipipe-insight*`. It was a design promise never practiced — zero K and zero W cards were
  ever written, in any project — so retiring it cost nothing. What a K card was meant to be is
  now split correctly in two: the general, reusable FACT is the bank's `QA/<n>-<slug>.md`; the
  paper-specific JUDGMENT is that paper's own `1-claims.md` entry. Legacy `insights/` dirs on
  disk are dead history.


Two rulers (why the tree and the story disagree)
------------------------------------------------

```
Ruler A — control flow ("who drives whom") — best for TEACHING
   paper stage → probe → task / discovery → back to the stage
   start from the question; it commissions the work; the probe carries the answer home.

Ruler B — dependency ("who cannot live without whom") — best for the FILESYSTEM
   source → task / discovery → paper / application
   no run, no metric to aggregate; no evidence, no claim to make.
```

Both are true. They are different axes, not competing orders — don't conflate them.


Delivery = the cash-out layer
=============================

    delivery = one act that cashes evidence out into something real.

A paper cashes out into academic credit; a message into a patient intervention; a report into a
decision. Different shapes, same move: read the KB → produce a deliverable. Two axes classify
every one of them:

```
                  COMMUNICATION (output is words)     INTERVENTION (output acts on a person)
               ───────────────────────────────────   ────────────────────────────────────────
  reads KB      paper · report · slides               message · UI · treatment
  writes KB     ——  nothing here.  A consumer NEVER writes the bank (LAW 1). Evidence enters
                    the KB from the EXECUTOR side only — autonomously (R17), or through a
                    commission that an executor orchestrator answers with its own hand.
```

`papers/` is not special by machinery — it is the (communication) container, and it happens to
be the most built-out. The genuinely different cell is **intervention**: its output acts on a
real person, and that person's reaction is measurable.


The flywheel (why this is not a pipeline)
-----------------------------------------

Communication deliverables end at the deliverable. Intervention deliverables, once deployed,
GENERATE NEW DATA:

```
  source → KB → delivery(message) → deployed to a patient
     ▲                                      │
     └────────── reaction = new source data ┘
                ("does this message work?" is itself new evidence)
```

So "let's see if the message works" is not the end of a deliverable — it is the start of the
next turn of source data. **A paper has no return path (it only communicates); a message has one
(it intervenes).** That return path is what makes the whole thing a flywheel rather than a line.


One project, many of everything
================================

The container contract (owner `/haipipe-project`, which owns ONLY the top level — every
subfolder's internals belong to its own skill family):

```
examples/<Project>/            Project-* = repo-backed submodule · ProjX-* = plain directory
│
├── tasks/                     owner /haipipe-task — inside execution
│   └── {G}{NN}_{group}/{NN}_{task}/            TWO levels; group letters are PROJECT-specific
│       ├── {NN}_{task}.py · configs/ · runs/ · notebooks/
│       ├── results/<run>/metrics.json          A-general, code-oriented
│       ├── workflow/plan.yaml · report.yaml    Q-general, code-oriented
│       └── QA/<n>-<slug>.md                    A-general, READABLE   ← OPTIONAL, executor-written
│
├── discoveries/               owner /haipipe-discovery — outside evidence
│   └── {S|L|P}{NN}_{group}/{NN}_{topic}/       S source-base · L landscape · P proof/prior-art
│       ├── discovery.yaml · sources.md · notes.md · verdict.md · landscape.md · ideas.md
│       └── QA/<n>-<slug>.md                    A-general, READABLE   ← OPTIONAL, executor-written
│
├── papers/                    owner /haipipe-paper-* — each paper its own submodule
│   └── Paper-<Name>/
│       ├── STATUS.md          state · maturity · active round · gate ledger
│       ├── 0-lifecycle/       0-seed · 1-resource · 1-claims · 2-venue · 2-pitch ·
│       │                      3-narrative · 4-display · 5-section-edit
│       │                      (each runs DPRC phases; resource/claims share the
│       │                       number 1, as venue/pitch already share 2)
│       ├── 1-probes/          README.md (campaign + generated board) + PPNN_<topic>.md probes
│       ├── 1-rounds/ · 0-displays/ · 0-sections/ · 0-<name>.tex · 0-<name>.bib
│
├── applications/              owner /haipipe-application-* — report / message / UI
│                              same 0-lifecycle stage model + its own 1-probes/
└── diagram/                   project-level ASCII/Excalidraw story
```

⚠️ NOTHING under `tasks/` or `discoveries/` is allowed to carry an `_ASK/` folder, an `_ANS/`
folder, an `answers:` field, or a PP id. That is R2, and it is the scaffold's job to never mint
one.

Three iron rules:

1. **The KB is ONE shared copy, flat. Hierarchy is expressed by REFERENCE, never by nesting.**
   Two papers both need the same run or discovery → neither copies it; each points its own
   section's `target:` at the artifact. Evidence is a project asset, not any paper's private
   property. This is not a slogan — it is the *reason* the commission must be paper-agnostic (a
   discovery shaped around one paper's H1/H2 stops being a shared asset), and the reason a
   landed answer is consumed from where it landed, never re-commissioned.

2. **One project, many papers; one QA file, many readers.** A QA file is general by
   construction, so a second paper reads it against its OWN claim and writes its OWN `reading`.
   Two papers may both carry a PP04 — no collision, because no PP id ever crosses.

3. **The paper folder is the LIVING unit** — not a frozen render. Its claims, its probes, its
   rounds and its gate ledger all live inside it. Retargeting to another venue is a stage-level
   operation: seed, resource and claims are venue-FREE and survive; pitch, narrative, display and
   section-edit are venue-ALIGNED and get rewritten.


Where to go from here
=====================

```
the probe (constitution)              skills/probe/haipipe-probe/SKILL.md          ⭐ THE CONTRACT
claim judging (G1/G2/G3)              skills/probe/haipipe-probe-review/SKILL.md
the container contract                skills/project/haipipe-project/SKILL.md
inside execution (+ the qa door)      skills/task/haipipe-task/SKILL.md
outside evidence (+ the qa door)      skills/discovery/haipipe-discovery/SKILL.md
academic delivery                     skills/paper/haipipe-paper/SKILL.md
non-academic delivery                 skills/application/haipipe-application/SKILL.md
the skill-folder map                  skills/STRUCTURE.md
the design of record (rulings R1-R18) Tools/plugins/haipipe-toolkit/diagram/260714-probe-qa/
```

Note on the application family: it shares the probe model exactly (`applications/<A>/1-probes/`,
same anatomy, same laws), but it trails the paper family by a wave on the DPRC-phase internals.
Read the paper family as the reference implementation until that sync lands.
