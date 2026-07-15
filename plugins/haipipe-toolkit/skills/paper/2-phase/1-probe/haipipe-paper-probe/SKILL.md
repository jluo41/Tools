---
name: haipipe-paper-probe
description: "PROBE phase worker (internal). Called by paper stage skills after DRAFT to collect the questions the draft raised (Q-papers) into PROBE FILES -- papers/<P>/1-probes/PPNN_<topic>.md, one file per TOPIC, each question one SECTION (serves / target / state / commission / reading) plus one '## Why' holding the stake, which never leaves the file. Runs the five-step loop ORGANIZE -> MATCH -> DISPATCH -> POINT -> INTERPRET. Binding is by PATH: a section's target: points at a QA file in the task/discovery bank. DISPATCH hands the commission block VERBATIM to Agent(haipipe-task-orchestrator-agent) / Agent(haipipe-discovery-orchestrator-agent) -- the probe GATEWAY is RETIRED and this worker never executes bank work inline. The three harvest lanes (citation/values/display) stay as sub-worker skills. Fully automatic, human review in CHECK only. Users invoke stage skills (seed, claims, pitch...), not this skill directly."
argument-hint: "[from-buffer <paper_root> [PPNN] | stage <stage-name>]"
allowed-tools: Bash, Read, Write, Edit, Grep, Glob, Skill, Agent
metadata:
  version: "4.2.0"
  last_updated: "2026-07-14"
  summary: "v4.2 — R19 HARDENING (four holes closed after the v4.1 review). (a) R14 IS SCOPED TO `state: answered`: a `working` file's ## Answer is EMPTY BY CONSTRUCTION, so it can never pass R14's literally-answers test, and applying R14 to it sends the reader straight back to DISPATCH — the exact duplicate run R19 exists to kill. A `working` file is matched on its `# Q —` line: if that restated question IS my question it is a HIT-IN-FLIGHT (commission + point, NO dispatch). (b) `owner:`/`eta:` ON THE IN-FLIGHT PATH ARE DERIVED, NEVER INVENTED: owner := the target's `by:` (or `bank`); eta := the target's `started:` + QA_CLAIM_TTL_HOURS. The checker's commissioned-liveness test and the QA claim's TTL become THE SAME CLOCK. (c) THE IN-FLIGHT LOOP IS CLOSED: a `commissioned` section whose target went `answered` (or `superseded`) is now a HARD FAIL — commissioned-target-answered / commissioned-target-superseded. Before this, a section sat GREEN over a landed answer until its eta expired. (d) A QA FILE WITH NO STATE LINE IS MALFORMED, NOT LEGACY: `state:` is MANDATORY, and the grandfather clause let an executor defeat qa-answered-empty BY OMISSION. New codes qa-no-state / read-target-no-state / commissioned-target-no-state. --- v4.1 — THE CONSUMER SIDE OF THE QA STATE LINE (constitution 8.2.0, R19/R20/R21; JL ruling 2026-07-14, Tools/plugins/haipipe-toolkit/diagram/260714-probe-qa/ PART 3b '>> CC0714'). A QA file is now a TICKET that becomes a RECEIPT: it carries ONE mutable `state:` line (working | answered | superseded-by: QA/<m>-<slug>.md) + `started:` (MANDATORY when working) + optional `by:`. ② MATCH LEARNS THE STATE — existence is no longer the signal, so the worker OPENS every candidate QA file and branches on its state line: `answered` = a T2 HIT; `working` = ⏳ IN FLIGHT, meaning THE QUESTION IS ALREADY BEING ANSWERED, so the section goes `state: commissioned` (with its unconditional BUILD-lane fields), `target:` points at that QA file, and there is NO SECOND DISPATCH — this is the whole point: two consumers asking the same question a week apart must not both pay for the same expensive P-B-E-R run; `superseded-by:` = FOLLOW THE CHAIN to the live answer and NEVER bind target: to a superseded file. ④ POINT: `ls` no longer settles the section's state — the TARGET'S state line does (absent|working ⇒ commissioned · answered ⇒ answered · superseded ⇒ re-point), and a `working` target still `working` past QA_CLAIM_TTL_HOURS=24 means the run is DEAD ⇒ re-dispatch. ⑤ INTERPRET reads ONLY a target that is `answered` and NOT superseded. THE INVARIANT, SAID OUT LOUD: ONE WRITER — the EXECUTOR, and nobody else, EVER. 'Write-once' was never the real rule; ONE WRITER was. This worker must NEVER create, claim, edit, complete or supersede a QA file — not even one it commissioned, not even to clear a zombie claim; a consumer-planted `working` file is the retired _ASK/ stub in a QA/ costume. check-probe-cards.sh GAINS FIVE TEETH, each catching a bug that was SILENT before: read-target-working · read-target-superseded (THE DAY-1/DAY-40 SILENT-FALSE-CLAIM BUG — every file internally consistent, the claim FALSE) · qa-working-no-started · qa-working-expired · qa-answered-empty; the new state-line logic is factored into ONE shared block (QA_STATE) used by both the section-target pass and the bank pass, exactly as the LAW-2 lint (LEAK_AWK) now is, because the two hand-copied twins drifted into identical bugs once already. Fixture-verified: clean+bait PASS exit 0 · legit in-flight (commissioned → working, fresh started) PASS exit 0 · all five teeth FAIL exit 1 · LAW-2 commission/bank lints still fire. --- v4.0 (Tools/plugins/haipipe-toolkit/diagram/260714-probe-qa/ v3, approved JL 2026-07-14 — R1-R18; mirrors haipipe-application-probe 4.0.0, paper deltas preserved). A PROBE is a PAPER-LEVEL document: papers/<P>/1-probes/PPNN_<topic>.md, one file per TOPIC, one SECTION per question (serves/target/state/commission/reading) + one '## Why' holding the stake. The 4-step card procedure (BOOKKEEP -> DISPATCH -> TRANSLATE -> VERIFY) is REPLACED by the FIVE-STEP LOOP: ORGANIZE -> MATCH -> DISPATCH -> POINT -> INTERPRET. R1 BINDING BY PATH — PP numbers are paper-local footnote numbers, no ledger, no PP id ever crosses to the bank. R2 THE BANK IS PROBE-UNAWARE — _ASK/, _ANS/, answers: and PP ids are DEAD; the DEFERRED-HANDOFF stub write is DELETED (it was a LAW-1 violation, and both banks now HARD FAIL an _ASK/ folder). The executor answers through its own `qa` verb and returns <leaf>/QA/<n>-<slug>.md. CC-8 the probe CAUSES a QA file, the EXECUTOR authors it (a bare results/ with no digest gets a DISPATCHED digest-only run, never an inline write). Dispatch goes DIRECT to Agent(haipipe-task-orchestrator-agent) / Agent(haipipe-discovery-orchestrator-agent) in THEIR input spelling (question/leaf/action/project); Agent(haipipe-probe-orchestrator-agent) is RETIRED and de-registered. Cost ladder T0 JOIN / T1 LOCAL / T2 REUSE / T3 ENRICH / T4 FRESH — only T3/T4 summon an agent, and MOST sections should land on T2. TWO LAWS: a consumer session never executes bank work inline; lint both surfaces. 'Verdict'/'verdicted' DELETED — claim status lives in 1-claims.md, and a `mode: full` section reaches it through Agent(haipipe-probe-reviewer-agent) at INTERPRET. PRESERVED: the PROOF-per-step enforcement, the RESOURCE STAGE INTAKE (Q -> section mint + `-> PP<NN>` backlink) and its WRITE-BACK (the Q's `A:`), the BUILD-lane `commissioned` state (owner/eta/blocks/cross-project, future-eta PASSES, overdue HARD FAILs), the three harvest-lane sub-workers, the display-request reroute, check-probe-cards.sh (KEEPS its filename, internals rewritten for question sections + the paper-only RESOURCE pass). v4.0.1: the Reference block points at `../../../haipipe-paper/fn/probes.md` (the file was renamed from fn/probe-plans.md)."
  # version history: ./CHANGELOG.md (skill-scoped, never loaded at invocation)
---

Skill: haipipe-paper-probe (PROBE phase worker, internal)
==========================================================

Called by stage skills (seed, resource, claims, pitch, narrative, display, section-edit) after
DRAFT, to collect the questions the DRAFT raised and bind each one to an answer.

The stage defines WHAT needs collecting; this skill defines HOW.

**Vocabulary is NOT this file's to invent.** The constitution is
`../../../../probe/haipipe-probe/SKILL.md` (v8.2.0). READ IT — never re-derive from memory.
Where this file and the constitution disagree, the constitution wins. Everything below is that
spec's operative form on the PAPER side. Papers and applications share the model EXACTLY (same
probe file, same `1-probes/` folder, same question sections, same commission → executor
dispatch); the paper deltas are only: `paper_root` vocabulary, the three harvest lanes as
SUB-WORKER SKILLS (citation / values / display), and the RESOURCE STAGE INTAKE.

Not user-facing: users invoke stage skills; stages call this.
Which stage runs which lanes/mode, seed/claims specifics, section-edit logic, phase-status
strips: `ref/per-stage-dispatch.md`.


PART 0 — What a probe is
=========================

**A probe is a PAPER-LEVEL document. Nothing else.**

```text
   📝 DRAFT stage        the questions are BORN here ({VAL:?}, GAP markers, open questions)
        │
        ▼  the PROBE phase (this worker) COLLECTS them
   📄 PAPER LEVEL — the probe lives HERE, and only here
   ══════════════════════════════════════════════════════════════════
   papers/Paper-X/1-probes/PP03_welldoc-feasibility.md    ← one file per TOPIC
   │
   │   ## Why   🔒 the stake (C6/C7, H2) — NEVER leaves this file
   │   ## Q1    one SECTION per question:  serves · target · state ·
   │   ## Q2                               commission · reading
   │
   │        binds by PATH ▼   (no PP id ever crosses)
   ══════════════════════════════════════════════════════════════════
   ⚙️ EXECUTOR LEVEL (task = discovery, same shape) — probe-UNAWARE
   tasks/A03_welldoc_cycle_check/01_column_scan/
   ├── workflow/plan.yaml       Q-general  code-oriented     (executor's own)
   ├── results/                 A-general  code-oriented     (executor's own)
   └── QA/1-cycle-indicator.md  A-general  READABLE, indexed (executor's own)
```

⛔ The words **"card"**, **"row"** and **"table"** are BANNED in this layer. It is a **probe
file**, holding question **SECTIONS**. And no markdown tables inside a probe file, ever.

**BINDING IS BY PATH, NOT BY ID (R1).** A section holds
`target: tasks/.../QA/1-cycle-indicator.md`. PP numbers are PAPER-LOCAL footnote numbers — two
papers may both carry a PP04 the way two books both carry a footnote 4. Nothing collides,
because no PP id ever crosses to the bank. No ledger, nothing to renumber, nothing to grep.

**THE BANK IS PROBE-UNAWARE (R2).** Under `tasks/` and `discoveries/` there is no `_ASK/`, no
`_ANS/`, no `answers:` field, and no PP id anywhere. The executor understands a plain QUESTION,
through its own `qa` verb — which takes general language in and gives a QA file back.


PART 1 — The probe file
========================

```text
   papers/Paper-CGMtoCyclePhase/1-probes/PP03_welldoc-feasibility.md
   ═══════════════════════════════════════════════════════════════════
   # PP03 — WellDoc data feasibility
   - mode: light | full

   ## Why            🔒 paper vocabulary, the STAKE:
                        "C6 dies if WellDoc has a cycle label; C7 needs enough CGM."
                        NEVER handed to any executor. NEVER copied anywhere.

   ## Q1 — cycle indicator                   ← one question, one SECTION
   - serves: 1-claims (C6)
   - target: tasks/A03_welldoc_cycle_check/01_column_scan/QA/1-cycle-indicator.md
   - state:  read                            ← DERIVED (PART 5), never asserted
   - commission: |                           ← Q-general, T1-translated, FROZEN
       Scan all 40 WellDoc CSV tables for menstrual/cycle/hormone columns and
       value-level terms. Report which exist, or none. Deliverable: QA digest +
       machine artifact. Do-not: no new data pulls. Accepted: present | absent.
   - reading: |                              ← the interpretation, written at harvest
       No cycle column in 40 tables; symptom table empty ⇒ C6 supported.
       → 1-claims.md C6 flips (status · confidence · claim_type · gates live THERE)

   ## Q2 — female CGM volume
   - serves: 1-claims (C7)
   - target: NEW tasks/A03_welldoc_cycle_check/02_female_cgm_volume
   - state:  planned
   - commission: |
       Count female patients with >=14d CGM in the WellDoc store; report the
       distribution. Accepted: any count — sufficiency is NOT yours to judge.
   - reading:                                ← empty until answered

   - values: … · sources: … · displays: …    ← the HARVEST LANES (PART 4 ⑤)
```

The FIVE section fields, exactly:

- **serves:** — which stage and/or claim of MY paper the question is for. The affinity field a
  stage gate greps ("what does 1-claims still owe?"), and what `--stage` filters on.
- **target:** — a PATH to the answering file. `NEW <leaf-path>` while the leaf does not exist
  yet; the QA-file path once it does. Point at the FILE, never the folder — a leaf that answered
  three things cannot tell you which of them is yours.
- **state:** — `planned | commissioned | answered | read | answered-local | failed`. DERIVED
  from disk (PART 5). Never asserted.
- **commission:** — the Q-general. Paper-agnostic, FROZEN once written. **This is the DISPATCH
  PAYLOAD, and nothing else is.**
- **reading:** — the interpretation, written at harvest. Empty until answered.

**HARVEST LANES** (`values:` / `sources:` / `displays:`) carry the pointers that feed MY
`_VALUES_` slot map, MY `.bib` / `_CITATION_` docs, and MY `0-displays/` units. Omit a lane
entirely when the return carries nothing for it.

**BUILD-LANE FIELDS** (JL rulings C4 + C6, 2026-07-14 — PRESERVED). A section whose answer
legitimately takes DAYS TO WEEKS (task-for-data / task-for-algo / task-for-fit, or a long
acquisition such as a DUA/IRB) additionally carries, and ONLY at `state: commissioned`:

```text
   - owner: <who is building it> · eta: YYYY-MM-DD · blocks: <the claim/demand ids it gates>
   - cross-project: <sibling-project path NAMED as a reuse candidate, or `none-found`>
```

`cross-project:` is MANDATORY on every BUILD-lane section: the MATCH may NAME a sibling-project
source but may not CONSUME it, and this line is how that candidate reaches the only human gate
whose job is authorizing SPEND. (Live case: a masked-LM CGM backbone was about to be costed at
GPU-weeks while its pipeline sat scaffolded in a sibling project.)

**NO "Verdict" (R7).** The word is DEAD and `verdicted` as a state is DELETED. The section's
`reading` carries the interpretation; the CLAIM's status (`supported | refuted | inconclusive`
+ confidence + claim_type + the G1/G2/G3 gates) lives in
`0-lifecycle/1-claims/1-claims.md`, judged per-claim, per-paper, PRIVATE. A `mode: full`
section reaches that judgment through `Agent(haipipe-probe-reviewer-agent)` at ⑤ INTERPRET —
the judgment lands in the CLAIM LEDGER, never in the probe file.
⚠️ A DISCOVERY's own `verdict.md` terminal file is a DIFFERENT thing. It is executor-native and
it SURVIVES. Do not delete it, do not rename it.


PART 2 — The QA file (the executor's side; this worker NEVER writes one)
========================================================================

```text
   Path:  tasks/<leaf>/QA/<n>-<slug>.md      discoveries/<leaf>/QA/<n>-<slug>.md
   <n> = creation order. `ls QA/` IS the index. SLUG ONLY — no PP id in a bank filename, ever.

   # Q — <the question, restated by the EXECUTOR in its own words>
   - state:   working | answered | superseded-by: QA/<m>-<slug>.md   ← the ONE mutable field
   - started: 2026-07-14T09:12          ← MANDATORY when state: working
   - by:      <run id | agent | human>  ← optional provenance
   ## Answer     EMPTY while state: working. Filled at REPORT.
                 plain words + [→ results/<file>] / [→ sources.md#S02] anchors
   ## Caveats    what this does NOT establish
   ## Not-done   what was asked but not resolved, and why
```

**R19 — A QA FILE IS A TICKET THAT BECOMES A RECEIPT** (JL ruling 2026-07-14). The EXECUTOR
writes it TWICE: the CLAIM (`state: working` + `started:`, empty `## Answer`) the moment the qa
gate decides to run ③ P-B-E-R, and the COMPLETION (`state: answered` + the `## Answer` body) at
REPORT. Gate paths ① SCAN and ② DIGEST never produce a `working` file — ① writes nothing, and
②'s facts already exist so its single write is instant and complete.

**⚠️ THE LOAD-BEARING INVARIANT IS *ONE WRITER*, NOT *WRITE-ONCE*.** Two writes by the same owner
is fine. What is forbidden is a SECOND WRITER:

```text
   ⛔ THIS WORKER MUST NEVER create, claim, edit, complete, or supersede a QA file.
      Not the state line. Not the body. Not "just this once". Not even to mark a file it
      commissioned. A CONSUMER-planted `working` file is the retired `_ASK/` stub wearing a
      `QA/` costume — the exact machinery deleted on purpose (R2), and the exact violation
      that put "C6"/"C7" into tasks/A03_welldoc_cycle_check/result.md (CC-8).
   ✅ THE ONLY WRITER IS THE EXECUTOR, in its OWN folder, and nobody else, EVER.
      This worker READS the state line. That is the whole of its relationship with it.
```

**QA_CLAIM_TTL_HOURS = 24** — the named constant. A `working` file whose `started:` is older than
it is STALE: the run that made it is dead, the EXECUTOR's next qa call may RECLAIM it, and
`check-probe-cards.sh` FAILs it (`qa-working-expired`). **This worker still does not touch it** —
a dead claim is re-dispatched (③), never repaired in place.

**R20 — SUPERSESSION.** A later run whose answer CHANGES does not edit the old file's body: the
EXECUTOR writes a NEW QA file and APPENDS `superseded-by: QA/<m>-<slug>.md` to the OLD one's
state line. That append is the file's OWN OWNER writing — never this worker.

**CC-8 — THE PROBE CAUSES A QA FILE; THE EXECUTOR AUTHORS IT.** Causing a file is not authoring
a file, and that difference is the entire wall:

```text
   📄 PROBE (has the stake)          🧱          ⚙️ EXECUTOR (never saw a paper)
   ─────────────────────────         WALL        ─────────────────────────────
   holds the question + ## Why                   holds results/ + the code
   commission  ───────── hands ONLY this ──────▶ 🤖 clean-context orchestrator
   (general language, no stake)                       │ reads results/ · runs the qa gate
                                                      ▼
                                                  WRITES QA/<n>-<slug>.md
   reads the QA file  ◀──────── path returns ────────┘   (author: EXECUTOR)
   writes `reading`
```

So when this worker meets a bare `results/` with NO digest, it does **not** write the digest
itself. It DISPATCHES a digest-only run (the qa verb's path ②): a clean-context agent reads
`results/` and writes the QA file. The file comes into existence by the probe's ACTION — through
the executor's HAND. That one hop is the whole wall. A probe-authored bank file is exactly how
`tasks/A03_welldoc_cycle_check/result.md` ended up carrying "C6"/"C7".

💀 **THE `_ASK/` HANDOFF STUB IS DELETED.** Earlier versions of this worker wrote
`_ASK/PPNN_<slug>.md` into the receiving `tasks/`/`discoveries/` folder — as "the ONLY
project-side write this worker is ever permitted". It is now permitted ZERO. The stub broke
LAW 1 and R2, no verb reads it any more, and both banks' reviewers HARD FAIL an `_ASK/` folder
on sight. The durable dead-session carrier is the `commission:` block IN the section (R6).


PART 3 — The `qa` verb (the door this worker dispatches into)
==============================================================

```text
   /haipipe-task qa "<question>" [<leaf>]   ·   /haipipe-discovery qa "<question>" [<leaf>]

   input: ONE question, GENERAL language — no PP id, no paper ref, no stake.

     ① QA SCAN   grep <leaf>/QA/*.md — already answered? → return the QA file PATH        ~0
                 (a `working` hit → "in progress since <started>"; it does NOT re-run)
     ② DIGEST    results/ (or sources.md / verdict.md) answer it, no readable digest?
                 → write QA/<n>-<slug>.md from EXISTING artifacts; run no code          cheap
                 ONE write, COMPLETE, `state: answered`. No claim — the write is instant.
     ③ P-B-E-R   neither → Plan→Build→Execute→Report at the SHALLOWEST depth
                 writes TWICE: the CLAIM (`state: working` + `started:`) at the moment it
                 decides to run, then the COMPLETION (`state: answered` + `## Answer`) at
                 REPORT.  ⇒ ONLY ③ ever produces a `working` file, and only transiently.
     🚫 REFUSE   out of scope for this executor/leaf → THIS WORKER RE-ROUTES (wrong leaf, or
                 task-shaped vs discovery-shaped) and the section goes `failed` if it cannot.
                 A REFUSE writes NO QA file, and RELEASES any claim it made.
```

The ENRICH DEPTH LADDER (R15) — depth 0 READ · 1 NEW RUN · 2 NEW SCRIPT · 3 NEW LEAF — is the
EXECUTOR's private business. **This worker never learns which depth was used, and never asks.**
It hands a question and gets back a QA-file path.

**WHY THIS WORKER CARES ABOUT ③'s CLAIM:** because it is what makes ② MATCH (PART 4) able to see
that a question is ALREADY BEING ANSWERED. Before it, the second consumer to ask saw no QA file
and dispatched THE SAME EXPENSIVE RUN AGAIN. The claim is written by the EXECUTOR — this worker
only READS it.


PART 4 — The Procedure: the FIVE-STEP LOOP
===========================================

`Skill("haipipe-paper-probe", args="from-buffer <paper_root> [PPNN]")` — the ONLY path that runs
the loop. Stage skills and the umbrella NEVER dispatch evidence agents directly.

**Each step ends with a PROOF this worker MUST show in its reply. A step whose proof is absent
did not happen, no matter what the prose claims.**

**STEP 0 — RE-INVOKE PER RUN.** Every PROBE phase invokes this skill fresh via the Skill tool,
even when its text is already in context from an earlier stage of the same session (the
stale-copy incident: a probe ran a 3-hour-old contract).

---

**① ORGANIZE — collect the DRAFT's questions into probe files, grouped by TOPIC.**

- **RESOURCE STAGE INTAKE (the Q → SECTION mint; JL Q-not-PP ruling, 2026-07-14).** Runs FIRST,
  and ONLY when the invoking stage is RESOURCE. Read
  `<paper_root>/0-lifecycle/1-resource/1-resource.md`. For every `Q<n>` that GATE 1 APPROVED —
  present in the artifact and NOT marked DECLINED in `_LOG_1-resource.md` — and that carries
  NEITHER an `A:` NOR a `-> PP<NN>` backlink, open ONE SECTION in a probe file under
  `1-probes/`, with `serves: resource` · `blocks: N<n>` (the Q's demand link, verbatim from
  `Q<n> (N<n>)`) · `target: NEW ?` · `state: planned`, and a `commission:` that is the Q
  RE-POSED as a self-contained evidence question (a resource question is already paper-agnostic
  — it asks what EXISTS, never which answer is wanted — but the T1 rules below still apply).
  Then WRITE THE BACKLINK into 1-resource.md: `**Q<n> (N<n>) -> PP<NN>**`. That backlink is the
  MECHANICAL PROOF the question was asked, and it is exactly what the CHECK gate tests
  (`check-probe-cards.sh --stage resource`). THE OWNERSHIP CHAIN:
  ```
  the STAGE asks (Q<n>) → the HUMAN approves at GATE 1 → THIS WORKER opens the section →
  ② MATCH resolves it or ③ DISPATCH commissions it → the answer lands →
  ⑤ INTERPRET writes the A back into the Q.
  ```
  The stage never mints a PP id. Skip this intake and the buffer is EMPTY, the dispatch is a
  no-op, and the gate greens over a stage that asked NOTHING.
- Resolve `project_root`: walk UP from `paper_root` to the FIRST ancestor containing
  `discoveries/`. Do NOT use `git rev-parse --show-toplevel` — repo-backed papers are their own
  git repos, so it returns paper_root itself. (`check-probe-cards.sh` resolves the same way;
  when in doubt, run it.)
- Read the DRAFT's open questions: `{VAL:?}` slots, `GAP` markers, the stage's explicit
  questions (for claims: every GAP/weak claim).
- GROUP them by TOPIC, and write ONE probe file per topic at
  `<paper_root>/1-probes/PPNN_<topic>.md`, with one SECTION per question and ONE `## Why` per
  file. Next free PP number = paper-local; `ls 1-probes/` is the authority.
- **WRITE THE COMMISSION AT ORGANIZE (T1).** Translating DOWN is a SEMANTIC rewrite, not a
  regex: strip the claim/hypothesis labels (H1/H2/C3…), strip the stage words (seed, pitch,
  narrative, claims-stage), strip the `## Why`, and strip ANY hint of which answer is wanted.
  What crosses is a SELF-CONTAINED evidence question a stranger with no access to the paper
  could answer. The commission is FROZEN once written — it is what survives a dead session with
  zero files on the bank side (R6: the paper is the memory).
  Two failures this prevents, both observed live (2026-07-11 seed incident):
  (a) CONTAMINATION — the discovery's own verdict.md/sources.md came back structured around the
      paper's H1/H2, so evidence meant to be reusable by *other* papers was paper-shaped and
      effectively single-use;
  (b) BIAS — a commission that says "H2 survives only if you find X" tells the agent which
      answer is wanted. Never disclose the stake.
- A legacy probe found in `1-probe-plans/` or a per-stage `0-lifecycle/*/_PROBE/` folder is
  MIGRATED into `1-probes/` in the new shape on first touch. Do not migrate what you did not
  touch.

PROOF 1: `project_root=<path>` + `ls <project_root>/discoveries/` + `ls <paper_root>/1-probes/`.

---

**② MATCH — per question, against the READABLE corpus. Cheapest door first.**

```text
  T0  JOIN     another stage's probe already asks this      → add my serves:       ~0
  T1  LOCAL    my OWN registries answer it                  → answered-local       ~0
  T2  REUSE    an existing QA file answers it               → point the section    1 grep + 1 read
  T3  ENRICH   the leaf exists, but was never asked this    → new section → ③      agent
  T4  FRESH    no leaf                                      → new section → ③      agent
```

- **T1 LOCAL SWEEP** — a CLOSED whitelist of the PAPER's OWN registries: sibling/prior
  `_CITATION_*.md` · `_VALUES_*.md` · `_EVIDENCE_*.md` · sections already `read` (their targets)
  · `0-displays/` units + index · the paper's `.bib`. These are indexes the lifecycle itself
  curated; reading them is pointer-following, not discovery. Fully answered → write the
  `reading`, set `state: answered-local`, do NOT dispatch. Partially answered → NARROW the
  commission to the remaining gap and dispatch that. Adopt the POINTER, never the verdict: a
  value reused from a sibling registry re-verifies against its ORIGINAL source at PLACE.
- **T2 REUSE** — `grep -rl "<terms>" <project_root>/{tasks,discoveries}/**/QA/*.md`, then
  **READ the hits**. This step may also call the `qa` verb in CHECK-ONLY mode
  (`/haipipe-task qa "<q>" --check-only`, `/haipipe-discovery qa "<q>" --check-only`): it
  detects ①/② and executes NOTHING.
- **⏳ READ THE STATE LINE OF EVERY CANDIDATE (R19/R21 ②). EXISTENCE IS NO LONGER THE SIGNAL.**
  A QA file that exists may be UNFINISHED or STALE. Open it and branch on its `state:`:
  ```text
    state: answered              ✅ HIT (T2). Point target: at it. Read it at ⑤.
    state: working               ⏳ IN FLIGHT — THE QUESTION IS ALREADY BEING ANSWERED.
                                 MATCH IT ON ITS `# Q —` LINE, NOT ON ITS ANSWER (the Answer
                                 is EMPTY by construction — see R14 below). If that restated
                                 question IS my question:
                                 · set THIS SECTION to `state: commissioned`
                                 · point `target:` at that QA file
                                 · ⛔ NO SECOND DISPATCH — an expensive P-B-E-R run is
                                   ALREADY RUNNING. This is the whole point of R19: two
                                   consumers asking the same question a week apart must not
                                   BOTH pay for it.
                                 · ⛔ DO NOT TOUCH THE FILE. Write only your own section.
                                 · the section carries the BUILD-lane fields at
                                   `commissioned` (owner/eta/blocks/cross-project) — no new
                                   exemption was carved for this way in. DERIVE them, never
                                   invent them (the two lines below).
                                 · re-check at the next gate: still `working` past
                                   QA_CLAIM_TTL_HOURS ⇒ the run is DEAD ⇒ re-dispatch (③).
    superseded-by: QA/<m>-…      🔗 FOLLOW THE CHAIN to the LIVE answer, and bind `target:` to
                                 THAT file (repeat until a file carries no `superseded-by:`).
                                 ⛔ NEVER bind target: to a superseded file — that is the
                                   day-1/day-40 SILENT-FALSE-CLAIM bug (the reading is true of
                                   an answer that is no longer true), and the checker FAILs it
                                   (`read-target-superseded`).
    no state line                MALFORMED — `state:` is MANDATORY. Do NOT bind `target:` at it
                                 (the checker FAILs `read-target-no-state`). Only its OWNER can
                                 add the line: dispatch (③) and let the executor's ① SCAN
                                 repair its own file.
  ```

  **⏳ DERIVING `owner:` AND `eta:` FOR A HIT-IN-FLIGHT.** This path does NOT dispatch, so there
  is no return to read them from — and an `eta:` invented at the gate is the very laundering the
  `eta:` test exists to prevent. Both come off the TARGET's own header, and from nowhere else:

  ```text
    owner:  := the target QA file's `by:` value  (or `bank` when `by:` is absent)
    eta:    := the target's `started:` + QA_CLAIM_TTL_HOURS, rendered YYYY-MM-DD
              — the claim's OWN expiry, the one date the bank actually asserts
    blocks: := the stage(s) this section serves        cross-project: := the usual sweep
  ```

  This makes the checker's `commissioned` liveness test and the QA claim's TTL THE SAME CLOCK: an
  overdue in-flight `eta:` now means exactly what `qa-working-expired` means — the run is dead,
  re-dispatch. Two clocks would have red-flagged honest work and hidden dead work.
- **R14 — MATCH ON THE ANSWER, NEVER ON THE TOPIC. (SCOPED TO `state: answered`.)** A hit counts
  ONLY if the QA file LITERALLY ANSWERS THIS question. The trap is live on disk:
  `tasks/A04_profile_welldoc_cohorts` and `tasks/A03_welldoc_cycle_check` both look like
  "characterize WellDoc" as TOPICS, but A04 holds ZERO cycle evidence while A03's answer IS claim
  C6's entire base. If an **`answered`** QA file does not answer the question, it is a T3 ENRICH —
  dispatch it, do NOT point at it.
  ⚠️ **R14 DOES NOT APPLY TO A `working` FILE.** A `working` file's `## Answer` is EMPTY BY
  CONSTRUCTION — that is what `working` MEANS, and the claim idiom writes it empty on purpose. So
  a `working` file can NEVER pass R14's literally-answers test, and applying R14 to it produces
  exactly the duplicate dispatch R19 exists to kill. **Match a `working` file on its `# Q —` line
  instead:** does that restated question BE my question? If yes it is a **HIT-IN-FLIGHT** — ⏳
  commission and point at it (the branch above). DO NOT DISPATCH.
- Sweeping `tasks/` / `discoveries/` for anything BEYOND the QA corpus — opening `results/`,
  reading a plan.yaml's outputs, grepping the code — is bank work, and doing it here breaks
  LAW 1. The QA corpus is a READABLE index the executor published FOR readers; that is why
  reading it is allowed and reading `results/` is not.
- **DISPLAY-SHAPED needs are REROUTED, not dispatched** (JL 2026-07-10: section-edit never
  creates displays). A question asking for a display unit that does not exist becomes a DR row
  in `0-lifecycle/4-display/_DISPLAY_REQUEST.md`; close the section `state: answered-local` with
  the `reading` "rerouted to display stage: DRNN". The display stage consumes the inbox.

**MOST SECTIONS SHOULD LAND ON T2.** The bank fills AUTONOMOUSLY from the executor side (R17):
in a healthy project most answers already exist before anyone asks. A commission is the
EXCEPTION, not the norm. A probe file whose every section is T3/T4 is a SMELL — either the MATCH
was lazy, or the bank is starving. Say which, in the reply.

PROOF 2: per question — the tier (T0-T4), and for T1/T2 the literal grep/ls hit lines that closed
it (for T2, the QA file path you READ **and its `- state:` line**).

---

**③ DISPATCH — the commission goes, VERBATIM, to the EXECUTOR ORCHESTRATOR.**

One call per open question (batch independent ones in one turn). **The keys below are the
orchestrators' OWN input spelling — do not invent variants; a prompt that matches none of their
declared input forms is undefined behaviour:**

```text
Agent(haipipe-task-orchestrator-agent, run_in_background=<true for fresh>, prompt="
  action: qa
  project: <project_root, from ①>
  question: |
    <the section's `commission:` block, VERBATIM. Nothing else.>
  leaf: <the section's target: — an existing leaf path, `NEW <path>`, or omit if unknown>
")
```

…or `Agent(haipipe-discovery-orchestrator-agent, ...)` for discovery-shaped work (literature,
prior art, landscape). THEIR CLEAN CONTEXT IS THE WALL. Inside, the orchestrator runs the qa
gate ①②③ and creates the leaf + its OWN plan.yaml if needed. The return is a PATH to the
answering QA file.

💀 **The probe GATEWAY agent is RETIRED.** `Agent(haipipe-probe-orchestrator-agent)` NO LONGER
EXISTS — archived and de-registered. Its SWEEP became step ② above; its dispatch is now this
direct Agent() call. (The `haipipe-probe-review` skill and `haipipe-probe-reviewer-agent`
SURVIVE — paper-side claim judging, invoked at ⑤.)

- **LAW 1 — A CONSUMER SESSION NEVER EXECUTES TASK/DISCOVERY WORK INLINE.** Dispatch means: hand
  the `commission` block, VERBATIM, and nothing else. **Never `## Why`. Never the probe file.
  Never the paper.** A consumer session that opens `results/` and starts writing in the bank has
  already broken this law, whatever it ends up writing.
- **LAW 2 — BACKSTOP LINT, ON TWO SURFACES.** Probe files: commission blocks carry no `C\d`, no
  `H\d`, no stake words ("rescue", "we want", "the hoped-for"). The bank: `QA/*.md` carry no
  consumer vocabulary (`C\d`, `H\d`, "claims-stage", "our paper"). LAW 2 is a BACKSTOP, not the
  mechanism — T1 is semantic and a regex provably misses real leaks. Never skip T1 on the theory
  that the lint will catch what it lets through.
- The orchestrator decides the SHAPE and the DEPTH in its own clean context. Never pre-chew it,
  never paste `results/` into the prompt, never tell it which answer is wanted. Audit-shaped
  scopes ("re-verify the set", "double-check the refs") go through this door too — never invent
  a side-channel worker (generic web-search agents etc.).
- Likely-fresh work (a new search, a landscape, a task run) dispatches `run_in_background=true`;
  a sync fresh run froze a session 25 minutes. When unsure, go background; ④ runs when it
  returns. RULE OF THUMB: if `<project_root>/discoveries/` is empty (or holds only `.gitkeep`),
  EVERY question is T4 — background them all. And do not REPORT a dispatch as background unless
  the call actually carried the flag: the label must match the call.
- Section `state: commissioned` — and a BUILD-lane section carries `owner:` + `eta:` + `blocks:`
  + `cross-project:` with it. WHY the BUILD lane exists: a 3-week build has not FAILED, it is
  WORKING; without a state that PASSES the gate it would red every downstream stage's CHECK for
  three weeks, on exactly the work JL ruled NON-BLOCKING. The `eta:` date test is the only thing
  standing between this state and a laundering token — a FUTURE eta PASSES, and the instant it
  passes with no QA file it is a HARD FAIL.
- **DEFERRED DISPATCH (no agent).** When the work is long-running, or the user drives a
  two-session workflow (one session on tasks, one on the paper), leave the section at
  `commissioned` with its BUILD-lane fields and STOP. The commission block IS the durable order
  — a later `/haipipe-task qa` session picks the question up, and a later PROBE re-run harvests
  the answer (④, async path). **This worker writes NOTHING project-side. Ever.** There is no
  stub, no mailbox, no order slip on the bank: the `_ASK/` container is DEAD (R2).

PROOF 3: per question — the literal `Agent(...)` call visible in the transcript, or (deferred)
the section's `commissioned` block showing owner/eta/blocks/cross-project.

---

**④ POINT — the section's `target:` → the answering QA FILE.**

The return is a PATH. Write it into `target:` (the FILE, not the folder), and verify it with
`ls <project_root>/<target>`. A return with NO QA-file path means the evidence never landed:
the section goes `state: failed` and the phase is NOT green. A `reading` with an empty or
unresolvable `target:` is the exact shortcut this contract exists to prevent.

⚠️ **`ls` NO LONGER SETTLES THE SECTION'S STATE — OPEN THE FILE.** A QA file that exists may be
`working` (unfinished) or carry `superseded-by:` (stale). The section's state is derived from
the TARGET'S STATE LINE, not from the target's existence:

```text
   target QA file is …            ⇒ the section is …
   ────────────────────────────   ─────────────────────────────────────────────────
   absent                         commissioned  (waiting — honest, until the eta passes)
   state: working                 commissioned  (LIVE — someone is answering it right now)
   state: answered                answered      → ⑤ INTERPRET it
   carries superseded-by: X       ⛔ re-point target: at X (follow the chain), then ⑤
   NO state line                  ⛔ MALFORMED. Do not bind. Dispatch (③); only the file's
                                     OWNER may add the line (checker: read-target-no-state)
```

ASYNC PATH (no live return — a `commissioned` section from an earlier session): on every run,
re-resolve each `commissioned` section's `target:`, `ls` its QA file, and READ its state line.
`answered` → ⑤ INTERPRET it exactly as a live return. `working` → the section stays
`commissioned` HONESTLY; report it as IN PROGRESS since `<started>`, never as failed — unless
`started:` is older than QA_CLAIM_TTL_HOURS, in which case the run is DEAD and the question
goes back through ③ DISPATCH. Absent → still `commissioned` (a hard fail once the eta passes).

⚠️ **THE ASYNC PATH IS MANDATORY, AND THE CHECKER NOW ENFORCES IT.** The MATCH→`working` route
issues NO DISPATCH by design, so those sections have NO live return, EVER — this re-resolve is
their ONLY road to `read`. A `commissioned` section whose target has since gone `answered` is a
HARD FAIL (`commissioned-target-answered`): the answer is on disk and the claim it serves is
still standing unsupported. Harvest it — write the `reading:`, flip the section — do not wait
for the eta.

PROOF 4: per question — the `target:` line, the `ls` that resolves it, and
`grep '^- state:' <target>` (the state line you branched on).

---

**⑤ INTERPRET — the `reading`, the claim flip, the harvest lanes.**

- **⛔ INTERPRET ONLY A QA FILE THAT IS `state: answered` AND CARRIES NO `superseded-by:`.**
  Reading a `working` file means reading an EMPTY `## Answer` — a paper claiming it read an
  UNFINISHED answer (checker: `read-target-working`). Reading a superseded file means a reading
  that is true of an answer that is no longer true (checker: `read-target-superseded` — the
  day-1/day-40 silent-false-claim bug). Both FAIL the gate. Neither is repairable by touching the
  QA file: the fix is to WAIT, or to FOLLOW THE CHAIN and re-read the live answer.
- **The `reading` (T2 translate-up).** The QA file speaks general; the section speaks paper.
  Map them HERE. The probe file is the ONLY bilingual document — it holds both vocabularies, and
  nothing else does.
- **The claim flip.** When a section `serves:` a claim, the claim ledger's C-line AND its
  Evidence Campaign row flip in the SAME pass, in `0-lifecycle/1-claims/1-claims.md` — that is
  where the claim's STATUS lives now (`supported | refuted | inconclusive` + confidence +
  claim_type + G1/G2/G3). It does NOT live in the probe file. There is no `## Verdict` block to
  write, and no `verdicted` state to set.
- **`mode: full` → JUDGE IT.** For a section on a `mode: full` probe file, dispatch
  `Agent(haipipe-probe-reviewer-agent, prompt="<the claim, the QA file path, the evidence>")`.
  It returns `supported | refuted | inconclusive` + confidence + claim_type + the G1/G2/G3
  gates, and **the caller lands that return in `0-lifecycle/1-claims/1-claims.md`** — never in
  the probe file. Judgment CONTENT is governed by
  `../../../../probe/haipipe-probe-review/SKILL.md`; only its landing site moved.
- **RESOURCE WRITE-BACK — the answer lands as the Q's `A:`** (JL Q-not-PP ruling). When a
  section carries `serves: resource`, write the landed reading BACK into
  `<paper_root>/0-lifecycle/1-resource/1-resource.md`, under the `Q<n>` its backlink names, as
  that Q's `A:` line — existence AND fitness, and what it KILLS ("probably fine" is a DEFECT,
  not an answer). A BUILD-lane section writes its A the moment the build is BOOKED, not weeks
  later when it lands: `A: COMMISSIONED · owner <who> · eta YYYY-MM-DD · blocks N<n> ·
  cross-project: <path|none-found>`, and the async path overwrites it with the real answer when
  the QA file arrives. BOTH receipts, always: the SECTION is the probe-layer receipt, the Q's
  `A:` is the CONSUMER-facing one — 1-resource.md is what the human reads at GATE 2 and what
  claims reads downstream, so a stage whose answers live only in probe files never sees its own
  answers. (This is a PAPER-side write, not a project-side one.)
- **LANE OBLIGATIONS — write the debt into the section FIRST, then pay it.** When the return
  carries harvestable content, IMMEDIATELY record it (this is what makes a skipped harvest
  checkable):
  ```
  - values:   tasks/T03/results/summary.csv · harvest: OWED     (values lane)
  - sources:  S01,S02,S03 · harvest: OWED                       (citation lane)
  - displays: 0-displays/fig-overview · harvest: OWED           (display lane)
  ```
  Then dispatch the lane's harvester SUB-WORKER (`haipipe-paper-probe-citation` /
  `-values` / `-display`; cheap tier, pointer-following only) and accept MECHANICALLY per
  `ref/harvest-acceptance.md` (run the greps, never eyeball). On acceptance flip the line:
  `harvest: accepted (<n> entries, <doc>)`. A lane line still saying `OWED` at the gate is a
  checker FAIL — the phase cannot go green over a skipped harvest.
- This worker reads no project files beyond the QA corpus; `ls` for existence only.

PROOF 5: per section — the `reading` line, the claim ledger diff (if it serves a claim), the
`grep -A2 'Q<n>' 1-resource.md` showing the `A:` written back (resource sections), and for every
lane line written, the harvester `Agent(...)` call + its acceptance-grep output.

---

**VERIFY** (deterministic; the stage CHECK gate re-runs the same script).

```
sh <this-skill-dir>/check-probe-cards.sh <paper_root> [<project_root>] [--stage <key>]
```

(The script KEEPS its filename — 65 refs across 33 files. Its INTERNALS are the new contract.)

Checks: section states resolve from disk; `read` sections have a resolving `target:`;
`planned` FAILs as probe-not-run; `commissioned` PASSes with owner + eta + blocks +
cross-project and a FUTURE eta, and HARD FAILs overdue; `harvest: OWED` lanes FAIL; LAW 2 on
BOTH surfaces (commission blocks carry no consumer vocabulary; the bank's `QA/*.md` carry none
either); no markdown tables in any probe file; `state: failed` surfaced; dead vocabulary
(`verdicted` / `## Verdict` / `## Takeaways` / `answers:` / `_ASK` / `_ANS`) FAILs.

**THE STATE-LINE TEETH (R19/R20) — five FAILs, each catching a bug that was SILENT before.**
The checker now OPENS every target and every bank QA file; existence proves nothing:

```text
   ❌ read-target-working      a section at `state: read` whose target: is `state: working`
                               ⇒ the paper claims it read an UNFINISHED answer
   ❌ read-target-superseded   a section at `state: read` whose target: carries `superseded-by:`
                               ⇒ the paper's reading is built on a STALE answer
                                 (THE DAY-1/DAY-40 SILENT-FALSE-CLAIM BUG: every file
                                  internally consistent, the claim FALSE, nothing caught it)
   ❌ qa-working-no-started    a `working` QA file with no `started:`   ⇒ an unexpirable claim
   ❌ qa-working-expired       a `working` QA file older than QA_CLAIM_TTL_HOURS ⇒ a zombie claim
   ❌ qa-answered-empty        `state: answered` with an EMPTY `## Answer` ⇒ a lying receipt
```

The last three are BANK-side. This worker does not FIX them — it cannot write a QA file. It
SURFACES them and re-dispatches (③) so the EXECUTOR resolves them in its own folder.
With `--stage resource` it ALSO runs the RESOURCE PASS over 1-resource.md: every `Q<n>` must
carry an `A:`, a `-> PP<NN>` backlink (to a probe file that EXISTS), or a DECLINED line in
`_LOG` — a Q with none of the three FAILs as `unasked-question`, and "no section serves stage
resource" while questions are still open FAILs as the VACUOUS GREEN instead of passing. That
pass is what makes the ① intake real.
Any FAIL → fix it or surface it; NEVER report a green PROBE over a FAIL.

PROOF 6: the checker output, pasted.


PART 5 — State: DERIVED per question, from the TARGET'S STATE LINE
==================================================================

No state is a claim about an agent (agents die; sessions end). Every state is checkable on disk.

⚠️ **STATUS IS NO LONGER DERIVED FROM MERE EXISTENCE (R19).** Before the state line, a QA file's
EXISTENCE meant "answered" and there was no third state — no way to say *someone is working on
this right now*. Now the reader MUST OPEN THE FILE. An `ls` is not enough.

```text
   state             disk fact
   ──────────────    ─────────────────────────────────────────────────────────
   planned           the section exists · the target leaf is missing (or `NEW …`)
   commissioned      EITHER the leaf + its plan.yaml exist · no QA file yet
                     OR     the target QA file exists and is `state: working`
                     — a LIVE question either way. NO SECOND DISPATCH.
   answered          the target QA FILE exists AND is `state: answered`
                     (a `working` target is NOT `answered`. It is `commissioned`.)
   read              the section's reading: is non-empty
                     (+ 1-claims.md flipped, if the section serves a claim)
                     — LEGAL ONLY against a target that is `state: answered` and
                       carries NO `superseded-by:`
   answered-local    target points into the paper's OWN registries; no dispatch
   failed            a reading with a dead target · the leaf was deleted · qa REFUSEd
   ──────────────    ─────────────────────────────────────────────────────────
   the probe FILE    the aggregate of its sections — the board renders it
   💀 "verdicted"    DELETED (R7) · 💀 "dispatched" DELETED (say `commissioned`)
```

⚠️ **THE BUILD-LANE FIELDS BIND AT `commissioned`, BOTH WAYS IN.** A section is `commissioned`
whether it got there by dispatching a fresh run or by pointing at someone else's `working` file.
Either way it carries `owner:` / `eta:` / `blocks:` / `cross-project:`. No exemption was carved
for the in-flight path: a section still `commissioned` when the gate runs is BY DEFINITION
build-lane, and `check-probe-cards.sh` has no lane test.


Hard boundaries (inherited by all stages)
==========================================

- **NEVER write anything under `tasks/` or `discoveries/`.** Not a QA file, not a stub, not a
  note. The probe CAUSES; the executor AUTHORS (CC-8). This is LAW 1, and it is absolute.
- **NEVER create, CLAIM, edit, complete or supersede a QA file** — not even one this worker
  commissioned, not even to mark it `working`, not even to append `superseded-by:`, not even to
  clear a zombie claim. **ONE WRITER: the EXECUTOR, and nobody else, EVER.** "Write-once" was
  never the rule; ONE WRITER was. A consumer-planted `working` file is the retired `_ASK/` stub
  in a `QA/` costume. This worker READS the state line and writes only its OWN section.
- NEVER generate bibtex or touch `.bib`; `_CITATION_` is plain text only.
- NEVER fabricate numbers; NEVER create ad-hoc plots inline.
- NO markdown tables in probe files, `_CITATION_`, or any probe/discovery document (JL standing
  rule) — bullet lines and sections only.
- NO inline search in the PROBE phase — durability is the whole point; the dispatch is the door.
  (DRAFT may WebSearch to orient; the difference is DURABILITY, not the search verb. DRAFT
  search feeds prose + `planned` sections; PROBE lands `read` sections with resolving targets.)
- A stage skill that calls `Agent(haipipe-task-orchestrator-agent)` or an evidence agent ITSELF
  is bypassing this contract: results land nowhere reviewable and die with the reply.
- All flags (🔍 unverified citations, ⚠️ uncertain values) resolve in CHECK, not here.


Return contract
================

```
status:    ok | blocked
stage:     <stage-name>
probes:    PPNN <n> sections · T0/T1 <n> · T2 <n> · T3/T4 <n> dispatched
lanes:     cite <status> │ val <status> │ disp <status>
next:      <suggested command>
```


Reference
==========

```
../../../../probe/haipipe-probe/SKILL.md        THE CONSTITUTION — probe anatomy, the QA/
                                                contract, the qa verb, the two LAWS. Read it.
../../../../probe/haipipe-probe-review/SKILL.md the judgment (G1/G2/G3, claim_type) for
                                                `mode: full` — lands in 1-claims.md
ref/per-stage-dispatch.md                       stage→mode map · seed/claims specifics ·
                                                section-edit logic · phase-status strips
ref/harvest-acceptance.md                       lane dispatch + the LITERAL acceptance greps
check-probe-cards.sh                            the VERIFY / stage-gate verifier (family-local)
../../../haipipe-paper/fn/probes.md             the 1-probes/ convention + the board
```

Siblings: DRAFT (haipipe-paper-draft) → PROBE (this) → REVISE (haipipe-paper-revise) →
CHECK (haipipe-paper-check).
DRAFT raises the questions; PROBE binds each to an answer; REVISE weaves the readings into the
prose; CHECK verifies every flag.
