---
name: haipipe-probe
description: "The probe layer's constitution. A PROBE is a PAPER-LEVEL document — papers/<P>/1-probes/PPNN_<topic>.md — generated in the PROBE phase from the questions the DRAFT stage raised. One file per TOPIC; each question is one SECTION (serves / target / state / commission / reading) plus one '## Why' holding the stake, which never leaves the file. Binding is by PATH, never by id: a section's target: points at a QA file in the task/discovery bank. The bank is PROBE-UNAWARE — no _ASK/, no _ANS/, no answers:, no PP ids — and answers questions only through its own `qa` verb (/haipipe-task qa, /haipipe-discovery qa), which returns <task-folder>/QA/<n>-<slug>.md. A QA file is a TICKET that becomes a RECEIPT: it carries ONE mutable `state:` line (working | answered | superseded-by:) written ONLY by its own owner, the executor — the probe CAUSES a QA file, the EXECUTOR authors it, and a consumer NEVER writes one. Owns: probe file anatomy, path binding, the QA/ contract, the state line + claim lifecycle + TTL + noclobber race guard + supersession, the qa verb contract, the five-step loop, the cost ladder, the two LAWS, status derivation, the writer table, the checker's FAIL conditions. Trigger: probe, probe file, PPNN, commission, reading, QA file, qa verb, state, working, claim, superseded, evidence, Q-paper, /haipipe-probe."
argument-hint: "[contract | anatomy | status | \"<question>\"]"
allowed-tools: Bash, Read, Grep, Glob, Agent, Skill
metadata:
  version: "8.3.0"
  last_updated: "2026-07-14"
  summary: "v8.3 = R19 HARDENING — four holes the v8.2 rollout left open, closed in the constitution and mirrored into every twin. (a) R14 IS SCOPED TO `state: answered`. A `working` file's `## Answer` is EMPTY BY CONSTRUCTION, so it can NEVER satisfy R14's literally-answers test — and R14's stated remedy is DISPATCH. Following the text as written, consumer #2 re-dispatches the SAME expensive run consumer #1 is three hours into, with a different slug so `set -C` never fires: the exact failure R19 exists to kill, executed by obeying R19's own words. THE STATE LINE IS NOW READ FIRST, BEFORE the literally-answers test, on EVERY reader (consumer MATCH + both executor ① SCANs); a `working` file is matched on its `# Q —` LINE and is a HIT-IN-FLIGHT (commission + point, NO dispatch). (b) THE IN-FLIGHT LOOP IS CLOSED: `commissioned-target-answered` / `commissioned-target-superseded`. The MATCH→working path issues NO dispatch, so it has NO live return, EVER — without a tooth on the `commissioned` state a section sits GREEN over an answer already on disk until its eta expires. `owner:`/`eta:` on that path are DERIVED from the target (owner := its `by:` or `bank`; eta := its `started:` + QA_WORKING_TTL_HOURS), so the checker's commissioned-liveness clock and the claim's TTL clock become ONE clock instead of two. (c) `state:` IS MANDATORY, ALWAYS — a QA file with no state line is MALFORMED, not 'legacy'. The grandfather clause let an executor defeat qa-answered-empty BY OMISSION (drop one line, ship an empty Answer, gate green) and had zero beneficiaries. New codes: qa-no-state · read-target-no-state · commissioned-target-no-state. (d) WRITE-ONCE IS RETIRED IN THE REVIEWERS TOO, replaced by BODY FROZEN — the old check would have REVISEd the completion (`working` → `answered`) and the supersession append, i.e. every gate-③ Report, on day 1. --- v8.2 = THE QA FILE GAINS ONE MUTABLE FIELD — a `state:` line — and becomes a TICKET that becomes a RECEIPT (JL ruling 2026-07-14, Tools/plugins/haipipe-toolkit/diagram/260714-probe-qa/ PART 3b '>> CC0714'). THE HOLE IT CLOSES: two consumers ask the same question a week apart; the first dispatches an expensive P-B-E-R run; the second, while that run is STILL GOING, sees no QA file and dispatches THE SAME RUN AGAIN — because until now a QA file was written ONCE, at REPORT, complete, and its EXISTENCE was the only signal ('answered'), with no way to say 'someone is working on this right now'. R19 THE CLAIM: a QA file now carries `state: working | answered | superseded-by: QA/<m>-<slug>.md` + `started: YYYY-MM-DDTHH:MM` (MANDATORY on a working file — a claim that cannot expire is a zombie by construction) + optional `by:`. The EXECUTOR writes it TWICE — the CLAIM at the qa gate's (3) decision, the COMPLETION at REPORT. THE LOAD-BEARING INVARIANT IS *ONE WRITER*, NOT *WRITE-ONCE*: two writes by the same owner is fine; a CONSUMER creating/claiming/editing a QA file is the retired _ASK/ stub in a QA/ costume and is FORBIDDEN (LAW 1). Only gate path (3) P-B-E-R ever produces a `working` file — (1) SCAN writes nothing, (2) DIGEST writes once, complete, `answered`. TTL: the named constant QA_WORKING_TTL_HOURS = 24; past it a working file is STALE and RESTARTABLE, and the checker FAILs it. RACE GUARD: create the claim under `set -C` (noclobber) — the loser re-runs (1) SCAN and defers; the residual same-instant/different-slug collision is NON-FATAL and must NOT be over-engineered (no lock dirs, no lease servers, no ledgers). R20 SUPERSESSION (subsumes the day-1/day-40 staleness hole): a later run whose answer CHANGES writes a NEW QA file and APPENDS `superseded-by:` to the OLD one's state line — by the file's OWN OWNER, never a consumer. R15 'ENRICH never mutates' still holds FOR THE BODY: only the state line is ever mutable. STATUS now reads the STATE LINE, not mere existence (no file = not answered · working = IN PROGRESS since <started> · answered = answered · superseded-by = answered but STALE, the live answer is X); a probe MATCH that meets a `working` file sets its SECTION to `commissioned`, points target: at that file, and does NOT dispatch a second time. THE CHECKER'S NEW TEETH (stated as LAW in PART 6): read-target-working · read-target-superseded (THE DAY-1/DAY-40 SILENT-FALSE-CLAIM BUG — every file internally consistent, the claim FALSE, nothing caught it before) · qa-working-no-started · qa-working-expired · qa-answered-empty. --- v8.1 = v8.0 + two ambiguities closed. (a) LAW 1 now names the ACT, not the tool: a consumer session breaks it by RUNNING bank work or WRITING a bank file — a READ-ONLY grep of QA/*.md IS step ② MATCH and is explicitly LEGAL (PART 4 told the agent to grep; PART 5's wall diagram read as if that grep were the violation). (b) PART 2 states the rule the checker actually enforces: a section still `commissioned` when the gate runs is BY DEFINITION build-lane, so owner/eta/blocks/cross-project are UNCONDITIONAL at that state — there is no 'fast commission' exemption (check-probe-cards.sh has no lane test). v8.0 (Tools/plugins/haipipe-toolkit/diagram/260714-probe-qa/ v3, approved JL 2026-07-14 — R1-R18 adopted). A probe is a PAPER-LEVEL Q/A map and nothing else: papers/<P>/1-probes/PPNN_<topic>.md, one file per TOPIC, one SECTION per question (serves/target/state/commission/reading) + one '## Why' holding the stake. R1 BINDING BY PATH — PP numbers are paper-local footnote numbers, two papers may both carry a PP04, no ledger, nothing to renumber, no PP id ever crosses to the bank. R2 THE BANK IS PROBE-UNAWARE — _ASK/, _ANS/, answers: and PP ids are DEAD; the executor answers plain questions through its own probe-unaware `qa` verb (R11: /haipipe-task qa, /haipipe-discovery qa — gate 1 QA SCAN, 2 DIGEST, 3 P-B-E-R, or REFUSE), which returns <task-folder>/QA/<n>-<slug>.md (R9: numbered = the index; on BOTH banks). CC-8 the probe CAUSES a QA file, the EXECUTOR authors it — a probe-authored bank file IS the A03 C6/C7 leak. Dispatch goes DIRECT to haipipe-task-orchestrator-agent / haipipe-discovery-orchestrator-agent; the probe GATEWAY agent is RETIRED (the probe-review skill + reviewer agent survive). Five-step loop ORGANIZE-MATCH-DISPATCH-POINT-INTERPRET; cost ladder T0 JOIN / T1 LOCAL / T2 REUSE / T3 ENRICH / T4 FRESH (only T3/T4 summon an agent); R14 MATCH ON THE ANSWER, never on the topic; R15 ENRICH depth ladder (read | new run | new script | new task-folder — the executor picks the shallowest, the probe never learns which). R17 TWO SESSION MODES (the executor session runs P-B-E-R for its own sake and does answerability work; only the consumer session asks) so most probes hit T2 REUSE and commissions are the exception. R18 TWO EXPLORERS (human + orchestrator, both probe-unaware). TWO LAWS: a consumer session never executes bank work inline; lint both surfaces. 'Verdict'/'verdicted' DELETED (claim status lives in 1-claims.md; a discovery's own verdict.md survives). The BUILD-lane `commissioned` state (JL C4+C6, 2026-07-14) is PRESERVED: owner/eta/blocks/cross-project, passes the gate, HARD FAIL once eta passes with no QA file. Retired: probes/ folders, _ASK/_ANS mailboxes, answers:, the asks verb, the gateway agent, the insight layer."
  # version history: ./CHANGELOG.md (skill-scoped, never loaded at invocation)
---

Skill: haipipe-probe — the probe layer's constitution
=====================================================

Spec of record: `Tools/plugins/haipipe-toolkit/diagram/260714-probe-qa/` (v3, APPROVED by JL 2026-07-14, rulings R1-R18,
plus the 2026-07-14 QA-state ruling — the `>> CC0714` block in PART 3b — landed here as
R19/R20/R21). This SKILL is that spec's operative form. Everything else in the toolkit cites
THIS file for its vocabulary; where they disagree, this file wins.

⚠️ **ONE SOURCE FOR THE VOCABULARY.** The task and discovery twins, the `qa` verbs, the probe
workers and `check-probe-cards.sh` all COPY the canonical strings from this file — the `state:`
values, the field names (`state:` / `started:` / `by:`), the TTL constant `QA_WORKING_TTL_HOURS`,
the timestamp format `YYYY-MM-DDTHH:MM`, and the `set -C` start idiom. They drifted before. Do
not let them: change it HERE, then propagate.


PART 0 — The definition
========================

**A probe is a PAPER-LEVEL document. Nothing else.**

It COLLECTS this paper's questions (the Q-papers, born in the DRAFT stage), GROUPS them by
topic, and LINKS each one to a general QA in the task/discovery bank. The bank never learns
that probes exist.

```text
   📝 DRAFT stage        Q-papers are BORN here ({VAL:?}, GAP markers, open questions)
        │
        ▼  the PROBE phase COLLECTS them
   📄 PAPER LEVEL — the probe lives HERE, and only here
   ══════════════════════════════════════════════════════════════════
   papers/Paper-X/1-probes/PP03_welldoc-feasibility.md    ← one file per TOPIC
   │
   │   ## Why   🔒 the stake (C6/C7, H2) — NEVER leaves this file
   │   ## Q1    one SECTION per Q-paper:  serves · target · state ·
   │   ## Q2                              commission · reading
   │
   │        binds by PATH ▼   (no PP id ever crosses)
   ══════════════════════════════════════════════════════════════════
   ⚙️ EXECUTOR LEVEL (task = discovery, same shape) — probe-UNAWARE
   tasks/A03_welldoc_cycle_check/01_column_scan/
   ├── workflow/plan.yaml       Q-general  code-oriented     (executor's own)
   ├── results/                 A-general  code-oriented     (executor's own)
   └── QA/1-cycle-indicator.md  A-general  READABLE, indexed (executor's own)
```

Applications are identical in shape: `applications/<A>/1-probes/PPNN_<topic>.md`.

**R1 — BINDING IS BY PATH, NOT BY ID.** A question section holds
`target: tasks/.../QA/1-cycle-indicator.md`. PP numbers are PAPER-LOCAL footnote numbers:
two papers may both carry a PP04 the way two books both carry a footnote 4. Nothing collides,
because **no PP id ever crosses to the bank**. There is no ledger, no shared namespace,
nothing to renumber, nothing to grep.

**R2 — THE BANK IS PROBE-UNAWARE, BUT NOT QUESTION-DEAF.** Under `tasks/` and `discoveries/`
there is no `_ASK/`, no `_ANS/`, no `answers:` field, and no PP id anywhere. What the executor
DOES understand is a plain QUESTION — through its own `qa` verb (PART 3b), which takes general
language in and gives a QA file back. Probe-unaware is not unreachable: the executor answers
questions without ever learning who asks, or why.


PART 1 — The theory: four quadrants, two translations
======================================================

```text
        PAPER-SPECIFIC                              PAPER-AGNOSTIC
   ┌──────────────────────────┐              ┌──────────────────────────┐
   │  Q-paper                 │              │  Q-general               │
 Q │  "H2 dies unless the     │──── T1 ─────▶│  "what is α?"            │──▶ executor
   │   exponent is < 0.5"     │   ABSTRACT   │  = the commission        │    reads
   │                          │   drop the   │  → becomes the task-folder's    │    (never sees
   │                          │   stake      │    OWN plan.yaml         │     a paper)
   └──────────────────────────┘              └──────────────────────────┘
              ▲                                            │
              │  closes the loop                           │  executor works
              │                                            ▼
   ┌──────────────────────────┐              ┌──────────────────────────┐
   │  A-paper                 │              │  A-general               │
 A │  "α=0.34 < 0.5 ⇒ H2      │◀─── T2 ──────│  "α = 0.34 ± 0.02"       │◀── executor
   │   supported"             │  INTERPRET   │  = QA/<n>-<slug>.md      │    writes
   │  = the reading           │  add the     │    [→ results/fit.json]  │
   │  → 1-claims.md C3 flips  │  stake back  │                          │
   └──────────────────────────┘              └──────────────────────────┘
```

**R3 — the PAPER owns BOTH translations.** T1 is a semantic REWRITE (the Q-paper is born
paper-specific; the stake is stripped out). T2 adds the stake back. The executor translates
NOTHING — which is exactly what makes A-general reusable: Paper-A reads "α=0.34" as
"H2 supported"; Paper-B reads the SAME file as "C4 inconclusive". Same fact, two readings.
Correct.

**R4 — consumer ⟷ probe ⟷ executor never talk directly.** The probe IS the map: T1 and T2
live inside each question section, as `commission` and `reading`.


PART 2 — The probe file: one topic, question SECTIONS
======================================================

**R5 — one file per TOPIC; each Q-paper is ONE SECTION.** The topic groups; the section
matches. The file is GENERATED in the PROBE phase, from the questions the DRAFT stage raised.

⛔ The words **"row"** and **"table"** are BANNED in this layer. It is a **Q-paper**, in its
own **SECTION**. And no markdown tables inside a probe file, ever.

```text
   papers/Paper-CGMtoCyclePhase/1-probes/PP03_welldoc-feasibility.md
   ═══════════════════════════════════════════════════════════════════
   # PP03 — WellDoc data feasibility
   - mode: light | full

   ## Why            🔒 paper vocabulary, the STAKE:
                        "C6 dies if WellDoc has a cycle label; C7 needs enough CGM."
                        NEVER handed to any executor. NEVER copied anywhere.

   ## Q1 — cycle indicator                   ← one Q-paper, one SECTION
   - serves: 1-claims (C6)                      (from DRAFT: the C6 gap marker)
   - target: tasks/A03_welldoc_cycle_check/01_column_scan/QA/1-cycle-indicator.md
   - state:  read                            ← DERIVED (PART 6), never asserted
   - commission: |                           ← Q-general, PRE-TRANSLATED (T1), FROZEN
       Scan all 40 WellDoc CSV tables for menstrual/cycle/hormone columns and
       value-level terms. Report which exist, or none. Deliverable: QA digest +
       machine artifact. Do-not: no new data pulls. Accepted: present | absent.
   - reading: |                              ← A-paper (T2), written at harvest
       No cycle column in 40 tables; symptom table empty ⇒ C6 supported.
       → 1-claims.md C6 flips (supported · confidence · claim_type · gates live THERE)

   ## Q2 — female CGM volume
   - serves: 1-claims (C7)
   - target: NEW tasks/A03_welldoc_cycle_check/02_female_cgm_volume
   - state:  planned
   - commission: |
       Count female patients with ≥14d CGM in the WellDoc store; report the
       distribution. Accepted: any count — sufficiency is NOT yours to judge.
   - reading:                                ← empty until answered

   - values: … · sources: … · displays: …    ← the HARVEST LANES (see below)
```

The five section fields:

- **serves:** — which stage and/or claim of MY paper this Q-paper is for. The affinity field a
  stage gate greps ("what does 1-claims still owe?").
- **target:** — a PATH to the answering file (R1). `NEW <task-folder-path>` while the task-folder does not
  exist yet; the QA-file path once it does. Point at the FILE, never the folder — a task-folder that
  answered three things cannot tell you which of them is yours.
- **state:** — `planned | commissioned | answered | read | answered-local | failed`. DERIVED
  from disk (PART 6). Never asserted.
- **commission:** — the Q-general. T1-translated, paper-agnostic, FROZEN once written. This is
  the DISPATCH PAYLOAD, and nothing else is.
- **reading:** — the A-paper. The T2 interpretation, written at harvest. Empty until answered.

**HARVEST LANES.** `values:` / `sources:` / `displays:` carry the pointers that feed MY
`_VALUES_` slot map, MY `.bib` / `_CITATION_` cards, and MY `0-displays/` units. They are
written when a return carries harvestable content, and are paid by the citation / values /
display harvesters (transcription only, pointer-following). Omit a lane entirely when the
return carries nothing for it.

**BUILD-LANE FIELDS** (JL rulings C4 + C6, 2026-07-14 — preserved, unchanged in substance).
A section whose answer legitimately takes DAYS TO WEEKS (task-for-data / task-for-algo /
task-for-fit, or a long acquisition) additionally carries, and ONLY at `state: commissioned`:

```text
   - owner: <who is building it> · eta: YYYY-MM-DD · blocks: <the claim/demand ids it gates>
   - cross-project: <sibling-project path NAMED as a reuse candidate, or `none-found`>
```

⚠️ **THERE IS NO "FAST COMMISSION" EXEMPTION.** A section still sitting at `state: commissioned`
WHEN THE GATE RUNS is BY DEFINITION build-lane — a dispatch that actually returned is `answered`
(its QA file exists) or `read`, not `commissioned`. So at VERIFY/CHECK the four fields are
UNCONDITIONAL at that state, and `check-probe-cards.sh` enforces them with no lane test:
`commissioned-no-owner` / `-no-eta(need YYYY-MM-DD)` / `-no-blocks` / `-no-cross-project`.
Write them the moment you set `state: commissioned`; do not wait to be failed.

`cross-project:` is MANDATORY on every such section: the MATCH may NAME a sibling-project
source but may not CONSUME it, and this line is how that candidate reaches the only human gate
whose job is authorizing SPEND. See PART 6 for the eta enforcement.

**R6 — the commission lives IN the section.** It is what survives a dead paper session with
ZERO files on the bank side: the paper is the memory. A section still `planned` with an empty
target two weeks later ⇒ any later session re-dispatches from the commission text, verbatim.
("A live agent is NOT the bridge — a FILE is." That ruling holds; in v1 the file was simply on
the wrong bank.)

**R7 — there is NO "Verdict".** The word is DEAD; `verdicted` as a state is DELETED. The
section's `reading` carries A-paper. The CLAIM's status — `supported | refuted | inconclusive`,
plus confidence, claim_type, and the G1/G2/G3 gates — lives in `1-claims.md`, judged per-claim,
per-paper, PRIVATE. A second paper judging the same A-general against ITS claim re-runs the
review: two consumers, two reviews, correct spend. (Judgment CONTENT is still governed by
`../haipipe-probe-review/SKILL.md`; only its landing site changed.)

⚠️ A DISCOVERY still has its own `verdict.md` terminal file for Review-type work. That is a
DIFFERENT thing, it is executor-native, and it SURVIVES. Do not delete it.

**R8 — the probe file is the ONLY bilingual document.** `## Why` and `reading` speak paper;
`commission` speaks general. That is what makes commission blocks a lint surface (LAW 2).


PART 3a — The executor side: QA/, on BOTH banks
================================================

**R9 — every executor task-folder MAY carry a `QA/` folder — task AND discovery.** Optional; not every
task-folder has one. Task and discovery are BOTH executors: same shape, same rules.

```text
   WHY: plan.yaml / results/ / sources.md are code- and evidence-oriented.
        QA/ is the executor's READABLE digest of what it has established.
   📌 precedent: tasks/A03_welldoc_cycle_check/result.md grew ORGANICALLY —
      exactly this file, ungoverned (and contaminated with C6/C7).
      QA/ formalizes an existing practice. It invents nothing.

   tasks/A03_welldoc_cycle_check/01_column_scan/     discoveries/L03_cycle/01_prior_art/
   ├── workflow/plan.yaml    Q  code                 ├── discovery.yaml            Q  spec
   ├── results/              A  code                 ├── sources.md · verdict.md ·
   └── QA/                   A  readable             │   landscape.md              A  raw
       ├── 1-cycle-indicator.md                      └── QA/                A  readable
       └── 2-female-cgm-volume.md                        └── 1-cycle-prior-art.md
```

**NAMING IS THE INDEX.** `QA/<n>-<slug>.md`, where `n` = creation order. `ls QA/` IS the index
— numbered, ordered, greppable. It reads as a menu: *here is what this task-folder has established,
and where.* No separate INDEX file until a task-folder's QA count earns one.

**SLUG ONLY — NO PP IDS.** The filename carries a slug and nothing else. A PP id in a bank
filename is R2 broken.

**R19 — A QA FILE IS A TICKET THAT BECOMES A RECEIPT.** (JL ruling 2026-07-14.) It carries
exactly ONE MUTABLE FIELD — the **state line**. Everything below the state line is written once
and never touched again.

```markdown
# Q — <the question, restated by the EXECUTOR in its own words>
- state:   working | answered | superseded-by: QA/<m>-<slug>.md
- started: 2026-07-14T09:12          ← MANDATORY when state: working
- by:      <run id | agent | human>  ← optional provenance

## Answer     EMPTY while state: working. Filled at REPORT.
              plain words + [→ results/<file>] / [→ sources.md#S02] anchors
## Caveats    what this does NOT establish
## Not-done   what was asked but not resolved, and why
```

- `state:` — the ONLY mutable field in the file, and **MANDATORY, ALWAYS**. Values: `working` ·
  `answered` · `superseded-by: QA/<m>-<slug>.md`. (`superseded-by:` is APPENDED to the state line
  of an `answered` file; it does not replace `answered`.) A QA file with NO state line is
  MALFORMED, not "legacy": its absence exempts the file from every claim check, so a LYING
  RECEIPT ships BY OMISSION (drop one line, leave `## Answer` empty, gate green). The checker
  FAILs it — `qa-no-state`.
- `started:` — the claim's birth time, `YYYY-MM-DDTHH:MM` (produced by `date +%Y-%m-%dT%H:%M`).
  **MANDATORY on a `working` file.** A `working` file with no `started:` can never expire, so it is not a
  claim — it is a zombie by construction, and the checker FAILs it.
- `by:` — optional provenance: a run id, an agent name, or a human.

**⚠️ THE LOAD-BEARING INVARIANT IS *ONE WRITER*, NOT *WRITE-ONCE*.**

```text
   ✅ ONE WRITER — the EXECUTOR, and nobody else, EVER
   ═══════════════════════════════════════════════════════════════════════════
   the EXECUTOR writes the file TWICE, in its own folder:
     ① at the qa gate's (3) DECISION   → the CLAIM     (state: working + started:)
     ② at REPORT                       → the COMPLETION (state: answered + ## Answer)
   Two writes by the SAME OWNER is fine. Nothing is shared. Nothing is planted.

   ⛔ A CONSUMER (probe / paper / application) MUST NEVER create, claim, edit, or
      complete a QA file. Not the state line. Not the body. Not "just this once".
```

**WHY THIS IS NOT THE RETIRED `_ASK/` STUB — the distinction is WHO, not WHEN.** A half-written
QA file looks, from the outside, exactly like the mailbox stub we deleted on purpose. It is not,
and the difference is the only thing that matters:

```text
   ❌ THE `_ASK/` TRAP (dead, PART 9)   a CONSUMER plants a half-file in the bank
                                        → TWO writers on one file
                                        → an INBOX the executor must scan
                                        → the bank is probe-AWARE again

   ✅ THE CLAIM (R19)                   the EXECUTOR claims its OWN file, in its OWN
                                        folder, at the moment IT decides to work
                                        → ONE writer. Nothing planted. No inbox.
                                        → the bank stays probe-UNAWARE
```

A consumer-authored `working` file is the `_ASK/` stub wearing a `QA/` costume. It is FORBIDDEN,
and it is the same violation as the A03 leak (CC-8): a consumer session, stake in context, writing
a bank file.

**THE CLAIM LIFECYCLE — which gate path writes WHAT, and WHEN:**

```text
   qa gate path      writes                                                  produces `working`?
   ───────────────   ────────────────────────────────────────────────────    ───────────────────
   ① QA SCAN         NOTHING. The file already exists — return its path.     no
   ② DIGEST          ONCE, COMPLETE, `state: answered`. The facts are        no
                     already in results/; ZERO code runs, so the write is    (nothing to claim —
                     instant. There is nothing to claim.                      the write IS instant)
   ③ P-B-E-R         TWICE:                                                  YES, and only
                       CLAIM      at the (3) decision — `state: working`     transiently
                                  + `started:` + an EMPTY `## Answer`
                       COMPLETION at REPORT — `state: answered`
                                  + the `## Answer` body
   ───────────────────────────────────────────────────────────────────────────────────────────
   ⇒ ONLY path (3) ever produces a `working` file, and only while the run is alive.
```

**🧟 THE CLAIM MUST EXPIRE.** A crashed run would otherwise leave `state: working` forever, and
every future reader would defer to a dead run.

```text
   QA_WORKING_TTL_HOURS = 24        ← the NAMED CONSTANT. Tune it here; the checker and both
                                    qa verbs read this name. Do not hard-code 24 anywhere.

   a `working` file whose started: is older than QA_WORKING_TTL_HOURS is STALE:
     · the next qa call MAY RESTART it — rewrite the claim with a FRESH started:,
       and record the abandoned attempt in `## Not-done`.
     · the checker FAILs it (`qa-working-expired`).
   ⛔ a `working` file with NO started: is an UNEXPIRABLE claim → FAIL (`qa-working-no-started`).
```

**🏁 THE RACE GUARD — `set -C` (noclobber), and NOTHING MORE.** Two qa calls may reach the (3)
decision at the same instant and both pick `QA/3-`. Create the claim with noclobber: the loser
sees the file already exists, RE-RUNS ① QA SCAN, and DEFERS. This shrinks the race window from
THE WHOLE RUN to microseconds.

```bash
QA_WORKING_TTL_HOURS=24                          # the working-file TTL — the named constant
QA_FILE="<task-folder>/QA/<n>-<slug>.md"
mkdir -p "$(dirname "$QA_FILE")"

if ( set -C; cat > "$QA_FILE" ) 2>/dev/null <<EOF
# Q — <the question, restated by the executor in its own words>
- state:   working
- started: $(date +%Y-%m-%dT%H:%M)
- by:      <run id | agent | human>

## Answer

## Caveats

## Not-done
EOF
then
  : # CLAIM WON  → proceed with (3) P-B-E-R; complete this file at REPORT.
else
  : # CLAIM LOST → the file already exists. Re-run (1) QA SCAN and DEFER. Run nothing.
fi
```

…and the staleness test the RESTART path and the checker share:

```bash
started=$(sed -n 's/^- started:[[:space:]]*//p' "$QA_FILE" | head -1)
[ -n "$started" ] || echo "FAIL qa-working-no-started"
age_h=$(( ( $(date +%s) - $(date -d "$started" +%s) ) / 3600 ))
[ "$age_h" -ge "$QA_WORKING_TTL_HOURS" ] && echo "STALE — restartable (checker: qa-working-expired)"
```

A residual same-instant / DIFFERENT-slug collision is still possible (two claims for one
question, `QA/3-foo.md` and `QA/3-bar.md`). It is NON-FATAL — ① SCAN finds both. **DO NOT
over-engineer past this: no lock dirs, no lease servers, no ledgers.** They are all retired
machinery in a new hat (PART 9).

**R20 — SUPERSESSION.** A later run whose answer CHANGES does NOT edit the old file's body. It
writes a NEW file, and APPENDS a pointer to the OLD file's state line:

```text
   day 1    QA/1-cycle.md   - state: answered
            paper points    target: …/QA/1-cycle.md · reading: "⇒ C6 supported"
   day 40   a re-run lands NEW data. The truth CHANGED.
            the EXECUTOR writes  QA/2-cycle.md   - state: answered
            and appends to       QA/1-cycle.md   - state: answered · superseded-by: QA/2-cycle.md
                                                                     ▲ the ONLY edit ever
                                                                       permitted to a frozen file
   ⇒ the paper's target: still points at QA/1 — but that is now MACHINE-DETECTABLE.
     The checker FAILs the section (`read-target-superseded`). Before R20 nothing fired,
     because every file was internally consistent and the claim was still FALSE.
```

**RECONCILING R20 WITH R15 ("ENRICH never mutates").** R15 holds, EXACTLY as written — for the
BODY:

```text
   MUTABLE   the `state:` line — and ONLY that line, and ONLY by the file's OWN OWNER
             (the executor). Two edits are legal in a file's whole life:
               working → answered            (the completion, at REPORT)
               answered → + superseded-by:   (the pointer, when a later run changes the truth)
   FROZEN    `# Q —` · `## Answer` · `## Caveats` · `## Not-done` — forever, once written.
   ⛔ A CONSUMER writes NEITHER. Not the body, not the state line. A probe that finds a stale
      target does not "fix" the QA file — it re-points its OWN section's target: at the live one.
```

A LATER question ADDS `QA/<n+1>-<slug>.md`. A QA file's BODY is never edited — by anyone, ever.

**R10 — the three reasons a QA file may exist** (there is no fourth):

```text
   commissioned   🎯 a dispatch names it: "Deliverable: QA/<n>-<slug>.md answering <Q>"
                     reason = a consumer question exists. The EXECUTOR writes it.
   digest-only    ♻️ results/ or sources.md ALREADY answer the question, but no readable
                     digest exists → light run: read the artifacts, write the QA file,
                     run no code.   (= the qa verb's path ②)
   executor's own ✍️ an executor session judges a finding worth digesting — including
                     proactive ANSWERABILITY WORK (R17): digests and reusable code
                     written so future questions are cheap, with no question pending.

   ⛔ ABUSE GUARD  no QA file without ONE of the three reasons. A QA/ that mirrors every
                   result file is noise, not an index — the lint flags orphans.
```


PART 3b — The `qa` verb: the executor's question door
======================================================

**R11 — each executor family owns a `qa` verb.** `/haipipe-task qa` (backed by
`task/haipipe-task/fn/qa.md`) and `/haipipe-discovery qa`, symmetrically. It REPLACES the
deleted probe-aware `asks` verb — reborn probe-UNAWARE.

```text
   /haipipe-task qa "<question>" [<task-folder>]     ·     /haipipe-discovery qa "<question>" [<task-folder>]

   input: ONE question, in GENERAL language — no PP id, no paper ref, no stake.
          The verb never learns WHO asks or WHY. It answers questions. That is all.

        ┌─ ① QA SCAN     grep <task-folder>/QA/*.md  (or all task-folders, if none is given)
        │                already `answered`?        → return the QA file PATH           ~0
        │                already `working`?         → DO NOT RE-RUN. Return the path +
        │                                             "in progress since <started>"      ~0
        │                                             (unless STALE past QA_WORKING_TTL_HOURS
        │                                              — then it is RESTARTABLE, R19)
        │                                            writes NOTHING
        │
        ├─ ② DIGEST      results/ (or sources.md / verdict.md) answer it, but no
        │                readable digest exists?    → write QA/<n>-<slug>.md         cheap
        │                                             ONCE, COMPLETE, `state: answered`
        │                                             from EXISTING artifacts; no code runs
        │                                             (no claim needed — the write is instant)
        │
        └─ ③ P-B-E-R     neither → ⚑ CLAIM FIRST: write QA/<n>-<slug>.md with
              │            `state: working` + `started:` under `set -C` (R19). Lost the
              │            race? → back to ① and DEFER.
              │          then run Plan→Build→Execute→Report at the SHALLOWEST depth that
              │          answers it (the ENRICH depth ladder, R15), and COMPLETE the same
              │          file at REPORT: `state: answered` + the `## Answer` body.
              │
              └─ 🚫 REFUSE — out of scope for this executor / this task-folder.
                       The caller RE-ROUTES (wrong task-folder, or task-shaped vs discovery-shaped).
                       A REFUSE writes NO QA file — and RELEASES any claim it made.

   THREE CALLERS, one door:
     📄 the PROBE's DISPATCH    — via the executor ORCHESTRATOR agents (PART 4 ③)
     🧑 a HUMAN, directly       — the everyday "go explore this direction" verb (R18)
     🤖 the ORCHESTRATOR itself — self-directed answerability work (R17)
   the probe's MATCH may also call qa in CHECK-ONLY mode: detect ①/②, execute nothing.

   💀 old `asks` verb: read _ASK/ stubs, resolved PPNN ids  → probe-AWARE   → DEAD
   ✅ new `qa` verb:   takes a question, returns an answer  → probe-UNAWARE → R2 holds

   ⚠️ qa is the executor's SIDE door (R17). The executor session's PRIMARY mode is
      autonomous P-B-E-R — no question, no ask, just the project's own research.
```

**R21 — THE THREE READERS OF THE STATE LINE.** The whole value of the claim is on the READ side:

```text
   ① SCAN — a 2nd qa call        `state: working` → DO NOT RE-RUN. Return the path +
      (the executor, days later)  "in progress since <started>". Cost ~0. An expensive
                                  P-B-E-R run is SAVED. This is the duplicate-work fix.

   ② PROBE MATCH — a consumer     `state: working` → the question is LIVE. The consumer sets
      (PART 4 ②, a week later)     its question SECTION to `state: commissioned` and points
                                   `target:` at that QA file. **NO SECOND DISPATCH.**
                                   ⛔ It does NOT touch the QA file. It writes only its own
                                      section. The pen never crosses the wall (CC-8).

   ③ A HUMAN                       `ls QA/` + the state line now reads as BOTH:
                                   what this task-folder has ESTABLISHED, and what it is
                                   ESTABLISHING RIGHT NOW.

   ⇒ THE FAILURE THIS KILLS: two consumers ask the same question a week apart. The first
     dispatches an expensive P-B-E-R run. The second, while that run is still going, sees
     no QA file, and dispatches THE SAME RUN AGAIN. Before R19, nothing prevented it.
```

**R12 — the writer table. Every file has exactly ONE writer.**

```text
   file                                    writer            reader
   ─────────────────────────────────────   ───────────────   ─────────────────
   papers/X/1-probes/PPNN_<topic>.md       this paper        this paper
   papers/X/1-claims.md                    this paper        this paper
   tasks/<task-group>/<task-folder>/workflow/plan.yaml         the task layer    task · probe(match)
   tasks/<task-group>/<task-folder>/results/ · QA/*.md         the task layer    task · probe(match, harvest)
   discoveries/<discovery-group>/<discovery-folder>/terminal · QA/*.md   discovery layer   disc · probe(match, harvest)
   ⇒ no shared writes anywhere. Paper and executor sessions run weeks apart, lock-free.
   ⇒ a QA file is written TWICE by its ONE owner (R19: the CLAIM, then the COMPLETION),
     and a third time only to APPEND `superseded-by:` (R20). ONE WRITER survives all three.
     A consumer READS it. A consumer NEVER writes it.
```

**CC-8 — the PROBE CAUSES a QA file; the EXECUTOR AUTHORS it.** Causing a file is not authoring
a file, and that difference is the whole wall:

```text
   ❌ IF THE PROBE WRITES QA/  — this IS the A03 incident, by construction
   ══════════════════════════════════════════════════════════════════════════
   the probe session has ## Why in context (C6 dies if WellDoc has a cycle label)
        │  it opens results/, writes tasks/.../QA/1-cycle-indicator.md
        ▼
   tasks/A03_welldoc_cycle_check/result.md   ← THE FILE THAT IS ON DISK TODAY
     "to answer two claims-stage questions:  C6: … → NO   C7: … → YES"
                                             ^^^        ^^^
   💥 a consumer session, stake in context, wrote a bank file.
      → LAW 1 broken · the R12 writer table broken (the paper wrote into tasks/)
      → the evidence comes back PAPER-SHAPED; the next paper inherits C6's frame

   ✅ THE PEN NEVER CROSSES THE WALL
   ══════════════════════════════════════════════════════════════════════════
   📄 PROBE (has the stake)          🧱          ⚙️ EXECUTOR (never saw a paper)
   ─────────────────────────         WALL        ─────────────────────────────
   holds Q-paper + ## Why                        holds results/ + the code
   T1 → commission  ──────── hands ONLY this ──▶ 🤖 clean-context orchestrator
   (general language, no stake)                       │ reads results/
                                                      │ runs the qa gate ①②③
                                                      ▼
                                                  WRITES QA/<n>-<slug>.md
   reads the QA file  ◀──────── path returns ────────┘   (author: EXECUTOR)
   T2 → reading (A-paper)
   ⇒ probe CAUSED it · executor AUTHORED it · the stake never left the paper
```

So when a probe meets a bare `results/` with no digest, it does **not** write the digest itself.
It DISPATCHES a digest-only run (qa path ②): a clean-context agent reads `results/` and writes
`QA/<n>-<slug>.md`. The file the probe wanted DOES come into existence by the probe's action —
but through the executor's hand. That one hop is the entire wall.


PART 4 — The five-step loop
============================

```text
  📝 DRAFT      raises the Q-papers ({VAL:?}, GAP, open questions)
                       │
  ① ORGANIZE   PROBE phase: collect them → probe files, grouped by TOPIC
                       │
                       ▼
  ② MATCH      per Q-paper, against the READABLE corpus:
               grep {tasks,discoveries}/**/QA/*.md   (+ the qa verb, CHECK-ONLY mode)
               ⚠️ READ THE STATE LINE of every candidate (R21) — existence is no longer
                  the answer. `working` ≠ `answered` ≠ `superseded-by:`.
                       │
       ┌───────────────┼───────────────┬───────────────┬───────────────┐
       ▼               ▼               ▼               ▼               ▼
   ✅ HIT          ⏳ IN FLIGHT     🟡 PARTIAL     🟠 LEAF EXISTS   🔴 NOTHING
   a QA file       a QA file is     answers Q1,    never asked      no folder
   `state:         `state:          not Q2         this                 │
    answered`       working`            │              │                │
    answers it      → the question      └──────┬───────┘                │
       │            is ALREADY LIVE            │                        │
       │               │                       └──────────┬─────────────┘
       │               ▼                                  ▼
       │        ⛔ NO SECOND DISPATCH        ③ DISPATCH  the commission goes,
       │        · set the SECTION to                     VERBATIM, to the EXISTING
       │          `state: commissioned`                  executor orchestrators:
       │        · target: → that QA file                   Agent(haipipe-task-…-agent)
       │        · ⛔ do NOT touch the file                  Agent(haipipe-discovery-…-agent)
       │        · re-check next gate: still              THEIR CLEAN CONTEXT IS THE WALL
       │          `working` past                         (PART 5). Inside, the orchestrator
       │          QA_WORKING_TTL_HOURS ⇒ the               runs the qa gate (PART 3b):
       │          run is DEAD ⇒ re-dispatch                ① scan  ② digest  ③ P-B-E-R
       │               │                                  creating the task-folder + its OWN
       │               │                                  plan.yaml if needed.
       │               │                                  💀 the old probe GATEWAY agent is
       │               │                                     RETIRED: its SWEEP became this
       │               │                                     paper-side MATCH; its dispatch
       │               │                                     is now a direct Agent() call.
       │               │                                     (probe-review SKILL + reviewer
       │               │                                      agent SURVIVE — claim judging.)
       │               │                                            │
       └───────────────┴────────────────────┬───────────────────────┘
                                            ▼
  ④ POINT     the section's target: → the answering QA FILE (not the folder)
                                            ▼
  ⑤ INTERPRET the section's reading: (T2) · 1-claims.md flips · the lanes harvest
              ⛔ ONLY from a QA file that is `state: answered` and NOT superseded.
                 Reading a `working` file = reading an EMPTY `## Answer` (checker FAIL).
                 Reading a `superseded-by:` file = a STALE claim (checker FAIL).
```

**THE DISPATCH PAYLOAD — one spelling, and it is the EXECUTOR'S.** Both orchestrators declare a
four-way input spec that switches on `action:`. A prompt matching none of their declared forms is
undefined behaviour: with no `action:` the qa gate is never selected, and with the task-folder under the
wrong key a T3 ENRICH aimed at an existing task-folder gets opened as a NEW task-folder (a fresh P-B-E-R run
where a new config would have done). Copy this block; do not invent variants:

```text
Agent(haipipe-task-orchestrator-agent, run_in_background=<true for fresh>, prompt="
  action: qa
  project: <project_root>
  question: |
    <the section's `commission:` block, VERBATIM. Nothing else.>
  task-folder: <the section's target: — an existing task-folder path, `NEW <path>`, or omit if unknown>
")
```

…and identically for `Agent(haipipe-discovery-orchestrator-agent, ...)`. The return is a PATH to
the answering QA file.

**R13 — the cost ladder.** Cheap doors first; only T3/T4 summon an agent.

```text
  T0  JOIN     another stage's probe already asks this Q-paper  → add my serves:      ~0
  T1  LOCAL    my own registries answer it                      → answered-local      ~0
  T2  REUSE    an existing QA file answers it                   → point the section   1 grep + 1 read
  T3  ENRICH   the task-folder exists, but was never asked this        → new section → ③     agent
  T4  FRESH    no task-folder                                          → new section → ③     agent
```

**MOST PROBES SHOULD LAND ON T2.** In a healthy project the bank fills autonomously from the
executor side (R17), so most answers ALREADY EXIST before anyone asks. A commission is the
EXCEPTION, not the norm. A probe file whose every section is T3/T4 is a smell: either the MATCH
was lazy, or the bank is starving.

**R14 — MATCH ON THE ANSWER, NEVER ON THE TOPIC. ⚠️ SCOPED TO `state: answered`.** The trap is
live on disk:

```text
   CGMtoAge/PP03    "profile WellDoc cohorts"      → tasks/A04_profile_welldoc_cohorts
   CyclePhase/PP03  "scan WellDoc cycle columns"   → tasks/A03_welldoc_cycle_check

   as TOPICS, both look like "characterize WellDoc"     ⚠️ FALSE MATCH
   but A04 holds ZERO cycle evidence, and A03's answer IS claim C6's entire base.

   ⇒ a HIT counts ONLY if the QA file LITERALLY ANSWERS THIS Q-paper.
     READ the QA file. Topic similarity is not evidence. If an ANSWERED QA file does not
     answer the question, it is a T3 ENRICH — dispatch it, do not point at it.
```

⛔ **R14 DOES NOT APPLY TO A `working` FILE — AND READING IT AS IF IT DID RE-OPENS THE EXACT HOLE
R19 CLOSES.** A `working` file's `## Answer` is EMPTY BY CONSTRUCTION (that is what `working`
MEANS; the CLAIM idiom writes it empty on purpose). So a `working` file can NEVER satisfy R14's
literally-answers test — and R14's stated remedy is DISPATCH. Follow that and consumer #2
dispatches the SAME expensive run that consumer #1 is still executing, three hours in, with a
different slug so `set -C` never fires. **THE STATE LINE IS READ FIRST, BEFORE the
literally-answers test, on every reader — both consumer MATCH and both executor ① SCANs:**

```text
   state: answered   → apply R14. Does the ## Answer answer it? no ⇒ T3 ENRICH ⇒ dispatch.
   state: working    → match on the `# Q —` LINE instead: does that restated question BE my
                       question? YES ⇒ ⏳ HIT-IN-FLIGHT — commission + point at it, and DO NOT
                       DISPATCH. (Executor side: return the path + "in progress since <started>".)
   superseded-by:    → follow the chain, THEN apply R14 to the live file.
```

**R15 — ENRICH NEVER MUTATES, and the DEPTH is the executor's private business.** A new question
to an old task-folder = a NEW section + a NEW commission; the executor adds `QA/<n+1>-<slug>.md`. A QA
file's BODY is never edited (R19/R20 make its `state:` LINE the one exception, and only the
file's own owner may touch it). The executor (inside the qa gate ③) picks the SHALLOWEST depth
that answers the question — the depth IS its entry point into P-B-E-R:

```text
   a NEW question arrives at an existing task-folder
   ──────────────────────────────────────────────────────────────────────────
   depth 0  📖 READ        existing results/ already hold the answer
                           → enter at R:  write QA/<n>-<slug>.md · nothing runs
   depth 1  ⚙️ NEW RUN     an existing script answers it with a NEW config
                           → enter at E:  + configs/<new>.yaml + runs/<new>/
                             same code, new parameters/subset — never edit old runs
   depth 2  🔧 NEW SCRIPT  the task-folder's SCOPE (plan.yaml IPO) covers it, but no script
                           computes it
                           → enter at B:  + <new>.py + plan-script-<new>.yaml
                             → Execute → Report
   depth 3  🌱 NEW TASK-FOLDER    outside this task-folder's scope — a different unit of work
                           → full P-B-E-R from P: sibling task-folder, next free NN
   ──────────────────────────────────────────────────────────────────────────
   🚫 REFUSE               wrong executor / wrong shape → the caller re-routes

   scope test (depth 2 vs 3): does the question fit THIS task-folder's plan.yaml IPO —
   same inputs, same process family?    yes → new script.    no → new task-folder.

   ACCRETES (add-only):  QA files · configs · runs/ · scripts · task-folders
   FROZEN (never edit):  past results/ · a QA file's BODY · the commission
   LIVING (executor's own, ONE writer): plan.yaml — may evolve normally
                                        a QA file's `state:` LINE — and only that line,
                                        and only by the executor (R19 claim→completion,
                                        R20 supersession). The BODY stays frozen.

   🔒 THE PROBE NEVER LEARNS WHICH DEPTH WAS USED. It hands over a question and gets
      back a QA-file path. That is what "the bank is probe-unaware" buys in the OTHER
      direction: the executor is free.
```


PART 5 — The two LAWS (the wall is a DISPATCH rule, not a file rule)
=====================================================================

The live leak that proves it: `tasks/A03_welldoc_cycle_check/result.md` carries the paper's
claim ids (C6, C7, "claims-stage") — written by an executor, with NO probe file involved
anywhere. The stake traveled through a paper session's own CONTEXT, because that session did
bank work INLINE. No mailbox, no stub, no id — and the leak happened anyway. That is why the
wall cannot be a file rule.

```text
   ✅ paper ──▶ 🤖 executor ORCHESTRATOR (clean context, gets ONLY the commission)
              ──▶ qa verb ──▶ bank                                        WALL HOLDS
   ❌ paper session RUNS bank work or WRITES bank files itself,      WALL NEVER EXISTED
      stake in context

   ✅ LEGAL, and REQUIRED: a READ-ONLY grep of {tasks,discoveries}/**/QA/*.md.
      That IS ② MATCH (PART 4). Nothing is written, no code runs, nothing leaves
      the paper. The wall bans the PEN and the RUN — not the EYE.
```

**LAW 1 — A CONSUMER SESSION NEVER EXECUTES TASK/DISCOVERY WORK INLINE.**
Dispatch means: hand the `commission` block, VERBATIM, and nothing else. Never `## Why`. Never
the probe file. Never the paper. The law names the ACT, not the tool: it is broken the moment a
consumer session RUNS bank work (a script, any P-B-E-R stage) or WRITES a bank file — including a
QA digest it thinks it is being helpful by authoring. Found a bare `results/` with no digest?
DISPATCH a digest-only run (qa path ②). The probe CAUSES the QA file; the EXECUTOR authors it.

⛔ **AND THAT INCLUDES THE CLAIM.** R19 gave the QA file a mutable `state:` line; it did NOT give
a consumer a pen. A consumer may not CREATE a QA file, may not CLAIM one (`state: working`), may
not COMPLETE one, may not APPEND `superseded-by:`, and may not "fix" a stale or zombie one. It
writes its OWN section, and nothing else. **ONE WRITER — the executor — for the whole life of
the file.** A consumer-planted `working` file is the retired `_ASK/` stub in a `QA/` costume
(PART 3a), and it is the A03 leak by another name.

**LAW 2 — BACKSTOP LINT, ON TWO SURFACES.**

```text
   📄 probe files:  commission blocks carry no C\d, no H\d, no stake words
                    ("rescue", "we want", "the hoped-for", "the probe that could save …")
   ⚙️ the bank:     QA/*.md carry no consumer vocabulary
                    (C\d, H\d, "claims-stage", "the paper" meaning *our* paper)
```

LAW 2 would have caught A03. The v1 `_ASK` bridge pass never could — A03 had no `_ASK`.

Both laws are cited by the paper/application PROBE-phase workers, by the `qa` verb, and by the
checker. The checker KEEPS its filename (`check-probe-cards.sh`, 65 refs across 33 files); only
its INTERNALS are rewritten — for question sections, commission lint, target resolution, and the
bank-side QA lint.

⚠️ LAW 2 is a BACKSTOP, not the mechanism. T1 (translate-down) is SEMANTIC; a regex provably
misses real leaks. Never delete T1 on the theory that the lint will catch what it lets through.


PART 6 — Status: DERIVED per Q-paper, from the STATE LINE
==========================================================

No state is a claim about an agent (agents die; sessions end). Every state is checkable on disk.

**⚠️ STATUS IS NO LONGER DERIVED FROM MERE EXISTENCE.** Before R19, a QA file's EXISTENCE meant
"answered" — there was no way to say "someone is working on this right now", and no third state.
Now the QA file carries a `state:` line, and **the reader MUST OPEN THE FILE AND READ IT.** An
`ls` is no longer enough.

**THE BANK-SIDE READING — what a QA file's own state line means:**

```text
   on disk                                    ⇒ the question is
   ────────────────────────────────────────   ──────────────────────────────────────────
   no QA file                                 NOT ANSWERED
   QA file · state: working                   IN PROGRESS (since <started>)
                                              — unless started: is older than
                                                QA_WORKING_TTL_HOURS, in which case the
                                                claim is STALE and RESTARTABLE (R19)
   QA file · state: answered                  ANSWERED
   QA file · state: answered · superseded-by: X   ANSWERED, but STALE —
                                              the LIVE answer is X. Re-point at X.
   QA file · NO state line                    MALFORMED — `state:` is MANDATORY, always.
                                              NOT a "legacy" free pass: the absence of the
                                              line exempts the file from every claim check,
                                              which is how a LYING RECEIPT ships BY OMISSION.
                                              The checker FAILs it (`qa-no-state`). Only the
                                              file's OWNER (the executor) may add the line.
   ────────────────────────────────────────   ──────────────────────────────────────────
```

**THE SECTION-SIDE READING — the probe question section's own `state:`:**

```text
   state             disk fact
   ──────────────    ─────────────────────────────────────────────────────────
   planned           the section exists · the target task-folder is missing (or `NEW …`)
   commissioned      EITHER  the task-folder + its plan.yaml exist · no QA file yet
                     OR      the target QA file exists and is `state: working` (R21 ②)
                     — a LIVE question, either way. NO SECOND DISPATCH.
   answered          the target QA FILE exists AND is `state: answered`
                     (a `working` target is NOT `answered`. It is `commissioned`.)
   read              the section's reading: is non-empty
                     (+ 1-claims.md flipped, if the section serves a claim)
                     — LEGAL ONLY against a target that is `state: answered` and
                       carries NO `superseded-by:`.
   answered-local    target points into the paper's OWN registries; no dispatch
   failed            a reading with a dead target · the task-folder was deleted · qa REFUSEd
   ──────────────    ─────────────────────────────────────────────────────────
   the probe FILE    the aggregate of its sections — the board renders it
   💀 "verdicted"    DELETED (R7)
```

⚠️ **THE BUILD-LANE FIELDS BIND AT `commissioned`, BOTH WAYS IN.** A section is `commissioned`
whether it got there by dispatching a fresh run or by pointing at someone else's `working` file.
Either way it carries `owner:` / `eta:` / `blocks:` / `cross-project:` (PART 2). There is no new
exemption: a section that is still `commissioned` when the gate runs is BY DEFINITION build-lane,
and `check-probe-cards.sh` has no lane test.

**⚖️ THE CHECKER'S TEETH — stated HERE as LAW; `check-probe-cards.sh` implements them.** These
conditions are the entire point of the state line: they make silent-wrong-claim bugs
MACHINE-DETECTABLE. Each must **FAIL** (exit 1), with the failure code given:

```text
   ❌ read-target-working        a question section at `state: read` whose target: resolves
                                 to a QA file that is `state: working`
                                 ⇒ THE PAPER CLAIMS IT READ AN UNFINISHED ANSWER.

   ❌ read-target-superseded     a question section at `state: read` whose target: resolves
                                 to a QA file carrying `superseded-by:`
                                 ⇒ THE PAPER'S READING IS BUILT ON A STALE ANSWER.
                                 ⚠️ THIS IS THE DAY-1/DAY-40 SILENT-FALSE-CLAIM BUG: every
                                    file is internally consistent, the claim is FALSE, and
                                    before R20 NOTHING caught it.

   ❌ qa-working-no-started      a QA file at `state: working` with no `started:`
                                 ⇒ AN UNEXPIRABLE CLAIM. It can never go stale, so every
                                   future reader defers to it forever.

   ❌ qa-working-expired         a QA file at `state: working` whose `started:` is older
                                 than QA_WORKING_TTL_HOURS  (`date -d "$started"`, a machine test)
                                 ⇒ A EXPIRED `working` FILE — the run that made it is dead.

   ❌ qa-answered-empty          a QA file at `state: answered` with an EMPTY `## Answer`
                                 ⇒ A LYING RECEIPT.

   ❌ qa-no-state                a QA file under tasks/|discoveries/ with NO `- state:` line
                                 ⇒ `state:` is MANDATORY, ALWAYS. Its absence EXEMPTS the file
                                   from every check above, so a lying receipt ships BY
                                   OMISSION: drop one line, leave `## Answer` empty, gate green.
                                 (also: read-target-no-state · commissioned-target-no-state,
                                  a section pointing at such a file)

   ❌ commissioned-target-answered   a section at `state: commissioned` whose target QA file
                                 has since gone `state: answered`
                                 ⇒ THE ANSWER LANDED AND NOBODY HARVESTED IT. This CLOSES THE
                                   IN-FLIGHT LOOP: the R21-② way in (MATCH meets a `working`
                                   file ⇒ commission + point ⇒ NO DISPATCH) has NO live return,
                                   EVER, so without this tooth the section sits GREEN over an
                                   answer that is already on disk until its eta expires — weeks
                                   — with the claim it serves still unsupported.
                                 (sibling: commissioned-target-superseded ⇒ re-point target:)
```

**THE BUILD LANE** (JL rulings C4 + C6, 2026-07-14 — preserved). Most sections answer in
minutes; some legitimately take DAYS TO WEEKS (task-for-data / task-for-algo / task-for-fit, a
long acquisition). Those sit at `commissioned` for a long time, and that is HONEST — a 3-week
build must not red every downstream gate for 3 weeks. The price of passing the gate is a DATE:

```text
   at state: commissioned, a BUILD-lane section MUST carry
     owner: · eta: YYYY-MM-DD (still in the FUTURE) · blocks: · cross-project:
   ✅ eta in the future, no QA file yet   → PASSES the gate
   ❌ eta PASSED, still no QA file        → HARD FAIL at the next gate
   `date -d "$eta"` is a machine test. WITHOUT it, `commissioned` becomes the state every
   un-run section wears, and the mechanism ships as a LAUNDERING TOKEN.
   Mechanically enforced by check-probe-cards.sh (owner / eta / blocks / cross-project
   + the future-eta test).
```


PART 7 — Two session modes, two explorers
==========================================

**R17 — TWO SESSION MODES. The executor's is NOT question-driven.**

```text
   ⚙️ LEFT — executor session                📄 RIGHT — consumer session
   ═══════════════════════════              ═══════════════════════════
   just runs P-B-E-R                        asks questions
   train · sweep · profile · review         DRAFT raises Q-papers →
   — no question needed, no ask.            PROBE collects, matches,
   this IS the project's research           commissions
        │                                        │
        ▼                                        ▼
   the bank grows AUTONOMOUSLY   ◀────  probes mostly land HERE (T2 REUSE)
   plan.yaml · results/ · sources.md
        │
        └─ 🆕 ANSWERABILITY WORK — also executor-session work, probe-unaware:
           · write QA/ digests for notable findings   (R10 "executor's own")
           · build / refactor code so future questions are CHEAP to answer
           it does not know WHICH questions will come. It makes the bank
           EASIER TO ASK. That is task-native work, not probe work.
```

**R18 — QA FILES ARE EXPLORATION DIRECTIONS, AND THERE ARE TWO EXPLORERS.** A QA file is not
merely "the answer to a commissioned question" — it is a direction the task-folder has explored,
written down. Both explorers are probe-UNAWARE:

```text
   🧑 HUMAN            /haipipe-task qa "<direction>"          interactive skill
      via the skill    picks a direction, runs the qa flow, reads the QA file
                       ("what about the female subset?" → QA/3-…)

   🤖 ORCHESTRATOR     Agent(haipipe-task-orchestrator-agent)  autonomous
      via the agent    two entry reasons:
                       · COMMISSIONED  — a probe handed it a question    (RIGHT)
                       · SELF-DIRECTED — answerability work (R17): it picks a
                         worthwhile direction ITSELF and explores it       (LEFT)

   both write the SAME artifact:  <task-folder>/QA/<n>-<slug>.md
   both use the SAME gate:        ① read → ② digest → ③ P-B-E-R
   ⇒ QA/ = the task-folder's growing map of explored directions.
```

The probe is therefore ONE CALLER of a door that humans and the orchestrator already walk
through for their own reasons. It did not invent that door, and it does not own it.


PART 8 — Verbs
===============

```text
   /haipipe-probe                    → the contract, in one screen (this file)
   /haipipe-probe contract|anatomy   → the probe-file anatomy + the QA/ contract
   /haipipe-probe status             → derive the states from disk (PART 6):
                                       ls papers/*/1-probes/PP*.md + applications/*/1-probes/
                                       resolve each section's target: · ls the QA files
                                       NEVER from a stored console state
   /haipipe-probe "<question>"       → ROUTE; do not execute. A question with no paper behind
                                       it is not a probe — hand it straight to the executor's
                                       own door:
                                         task-shaped      → /haipipe-task qa "<question>"
                                         discovery-shaped → /haipipe-discovery qa "<question>"
                                       No probe file is written; the QA file IS the receipt.
                                       (If it later matters to a paper: open a section whose
                                        target: points at the already-written QA file — T2,
                                        nothing re-run.)
```


PART 9 — RETIRED MACHINERY (do not resurrect)
==============================================

```text
   💀 probes.ledger · project-unique PP ids     killed by PATH BINDING (R1). PP numbers are
                                                paper-local footnotes; nothing collides.
   💀 _ASK/ and _ANS/ mailboxes in the bank     killed by R2 (the bank is probe-unaware). The
                                                commission block in the section replaces the
                                                stub entirely.
                                                ⚠️ R19's `state: working` QA file is NOT this
                                                   coming back. The stub's sin was the WRITER
                                                   (a consumer planting a half-file), not the
                                                   half-ness. The claim is written by the file's
                                                   OWN OWNER, in its OWN folder. A CONSUMER-
                                                   authored `working` file IS the stub, and is
                                                   FORBIDDEN (LAW 1).
   💀 "write-once" as the QA invariant          it was never the real rule — **ONE WRITER** was
                                                (R19). Two writes by the same owner (CLAIM →
                                                COMPLETION) preserve everything write-once was
                                                protecting: no shared writes, no locks, no inbox.
   💀 lock dirs · lease servers · claim ledgers `set -C` (noclobber) on the working file is the
      · any coordination service              WHOLE race guard (R19). It shrinks the window from
                                                the whole run to microseconds; the residual
                                                same-instant/different-slug collision is NON-FATAL
                                                (① SCAN finds both files). DO NOT over-engineer
                                                past this. A ledger here is `probes.ledger`
                                                reborn — and that is already on this list.
   💀 the `answers:` return field               nothing to grep — the answer IS a file, and the
                                                section's target: is the pointer to it.
   💀 /haipipe-task asks (the probe-aware verb) DEAD — REBORN probe-unaware as `qa` (R11).
   💀 haipipe-probe-orchestrator-agent          the GATEWAY. RETIRED 2026-07-14. Its SWEEP
      (the evidence gateway)                    became the paper-side MATCH (PART 4 ②); its
                                                dispatch is now a direct Agent() call on the
                                                task/discovery orchestrators. Archived to
                                                ../agents/_archive/ and de-registered.
                                                ✅ SURVIVING: the haipipe-probe-review SKILL +
                                                   haipipe-probe-reviewer-agent — paper-side
                                                   claim judging, still live.
   💀 the DIRECT-ASK gateway dispatch           a direct ask no longer runs evidence work; it
                                                ROUTES to the executor's qa verb (PART 8).
   💀 "Verdict" / "verdicted"                   the word is dead (R7). Claim status lives in
                                                1-claims.md. NOTE: a DISCOVERY's own verdict.md
                                                (the Review-type terminal file) is a DIFFERENT
                                                thing, and it SURVIVES.
   💀 "row" / "table" as probe vocabulary       it is a Q-paper, in its own SECTION. And no
                                                markdown tables in probe/discovery/source docs.
   💀 "Takeaways" (the card field)              → `reading` (the section field).
   💀 1-probe-plans/                            → 1-probes/.
   💀 "card" (as the name of a probe file)      → probe. ALLOWLIST rename only: ~90 of 941 uses
                                                in this repo mean OTHER things — poster "card
                                                styles", venue-ui-card, KPI cards, _CITATION_
                                                cards, "model card". NEVER a blind sed.
   💀 the project-level probes/ store           a second telling of the executor's own artifacts.
      (Need/Findings folders, probe.yaml,       Retired 2026-07-05; legacy folders on disk are
      evidence.md, status.md)                   dead history — never read, never written, never
                                                deleted.
   💀 the INSIGHT layer (insights/, D/I/K/W)    retired 2026-07-12: zero K and zero W cards had
                                                ever been written. The evidence base is TWO
                                                warehouses — tasks/ + discoveries/.
   💀 the interactive Probe Console             .probe-console.yaml, console panels. Dashboards
                                                live in /haipipe-paper enter (open needs).
   💀 haipipe-probe-creator-agent               retired to ../_archive/_old/.
   💀 a per-paper COPY of a shared probe        one-writer-per-copy still drifts.
   💀 cross-repo pointers / content hashes      three papers are FOREIGN git repos.
   💀 a shared Deliverable/Do-not/Accepted      an acceptance space is a FUNCTION of the stake;
                                                freezing consumer-1's frame makes the evidence
                                                paper-shaped forever.
   💀 merging two papers' same-numbered probes  two lossy projections ≠ one question.
   💀 a cross-project ("continent") tier        separate repos; the buy is one avoided run.
                                                (The BUILD lane's `cross-project:` line NAMES a
                                                 candidate for the human gate — it never
                                                 CONSUMES one. That is not this tier.)
   💀 deleting T1 (translate-down)              the regex lint provably misses real leaks. T1 is
                                                semantic; LAW 2 is only a backstop.
```

Live instruments that survive, with the judgment skill: `../haipipe-probe-review/SKILL.md`
(the G1/G2/G3 gates, `supported | refuted | inconclusive`, `claim_type`), plus its
`g2_integrity_check.py` and `probe-caveats-checklist.txt`. Judgment CONTENT is that skill's
business; where the judgment LANDS (`1-claims.md` — per-claim, per-paper, private) is this
file's.
