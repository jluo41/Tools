---
name: haipipe-probe
description: "The probe layer's constitution: a probe is a paper-level Q/A map (papers/<P>/1-probes/PPNN_<topic>.md) binding each question by PATH to a QA file in the probe-unaware task/discovery bank. Owns probe-file anatomy, the QA state-line contract, the five-step loop, the cost ladder, the two LAWS, status derivation, the writer table, the checker's FAIL conditions. Trigger: probe, probe file, PPNN, commission, reading, QA file, qa verb, state, working, claim, superseded, evidence, Q-paper, /haipipe-probe."
argument-hint: "[contract | anatomy | status | \"<question>\"]"
allowed-tools: Bash, Read, Grep, Glob, Agent, Skill
metadata:
  version: "8.3.0"
  last_updated: "2026-07-14"
  summary: "v8.3 — the probe layer's constitution. Full version history: ./CHANGELOG.md"
---

Skill: haipipe-probe — the probe layer's constitution
=====================================================

Spec of record: `Tools/plugins/haipipe-toolkit/diagram/260714-probe-qa/` (v3, approved JL 2026-07-14, R1-R21).
This SKILL is that spec's operative form.
Everything else in the toolkit cites THIS file for its vocabulary; where they disagree, this file wins.

⚠️ ONE SOURCE FOR THE VOCABULARY.
The task/discovery twins, the `qa` verbs, the probe workers and `check-probe-cards.sh` all COPY the canonical strings from here — the `state:` values, the field names (`state:` / `started:` / `by:`), the TTL constant `QA_WORKING_TTL_HOURS`, the timestamp format `YYYY-MM-DDTHH:MM`, the `set -C` idiom.
They drifted before. Change it HERE, then propagate.


PART 0 — Definition
===================

A probe is a PAPER-LEVEL document, nothing else.
It collects this paper's DRAFT-stage questions (Q-papers), groups them by topic, and links each to a QA file in the task/discovery bank.
The bank never learns probes exist.
Applications are identical in shape: `applications/<A>/1-probes/PPNN_<topic>.md`.

```text
   📝 DRAFT stage    Q-papers are BORN here ({VAL:?}, GAP markers, open questions)
        │  the PROBE phase COLLECTS them
        ▼
   📄 PAPER LEVEL   papers/Paper-X/1-probes/PP03_welldoc-feasibility.md   ← one file per TOPIC
       ## Why       🔒 the stake — NEVER leaves this file
       ## Q1 ## Q2  one SECTION per Q-paper: serves · target · state · commission · reading
        │  binds by PATH ▼  (no PP id ever crosses)
   ⚙️ EXECUTOR LEVEL (task = discovery, same shape) — probe-UNAWARE
       tasks/A03_welldoc_cycle_check/01_column_scan/
       ├── workflow/plan.yaml   results/       (executor's own, code-oriented)
       └── QA/1-cycle-indicator.md              (executor's own, READABLE, indexed)
```

R1 — BINDING IS BY PATH, NOT BY ID.
A section holds `target: tasks/.../QA/1-cycle-indicator.md`.
PP numbers are PAPER-LOCAL footnote numbers: two papers may both carry a PP04, and nothing collides because no PP id ever crosses to the bank.
There is no ledger, no shared namespace, nothing to renumber.

R2 — THE BANK IS PROBE-UNAWARE, BUT NOT QUESTION-DEAF.
Under `tasks/` and `discoveries/` there is no `_ASK/`, no `_ANS/`, no `answers:` field, no PP id.
What the executor understands is a plain QUESTION, through its own `qa` verb (PART 3b), which takes general language in and gives a QA file back.
Probe-unaware is not unreachable: the executor answers questions without ever learning who asks, or why.


PART 1 — Four quadrants, two translations
=========================================

```text
        PAPER-SPECIFIC                          PAPER-AGNOSTIC
   Q-paper  "H2 dies unless α < 0.5"  ──T1──▶   Q-general  "what is α?"  ──▶ executor reads
      ▲  closes the loop              ABSTRACT  = the commission             (never sees a paper)
      │                                              │  executor works
   A-paper  "α=0.34<0.5 ⇒ H2 held"   ◀──T2──   A-general  "α=0.34±0.02"  ◀── executor writes
   = the reading → 1-claims.md flips  INTERPRET = QA/<n>-<slug>.md
```

R3 — the PAPER owns BOTH translations.
T1 is a semantic REWRITE that strips the stake out; T2 adds the stake back.
The executor translates NOTHING — which is what makes A-general reusable: Paper-A reads "α=0.34" as "H2 supported", Paper-B reads the SAME file as "C4 inconclusive".
Same fact, two readings. Correct.

R4 — consumer ⟷ probe ⟷ executor never talk directly.
The probe IS the map: T1 and T2 live inside each question section, as `commission` and `reading`.


PART 2 — The probe file: one topic, question SECTIONS
=====================================================

R5 — one file per TOPIC; each Q-paper is ONE SECTION, generated in the PROBE phase from the DRAFT-stage questions.
⛔ The words "row" and "table" are BANNED in this layer — it is a Q-paper, in its own SECTION. No markdown tables inside a probe file, ever.

```text
   # PP03 — WellDoc data feasibility
   - mode: light | full

   ## Why   🔒 the STAKE, in paper vocabulary. NEVER handed to any executor, NEVER copied anywhere.

   ## Q1 — cycle indicator
   - serves: 1-claims (C6)
   - target: tasks/A03_welldoc_cycle_check/01_column_scan/QA/1-cycle-indicator.md
   - state:  read                            ← DERIVED (PART 6), never asserted
   - commission: |                           ← Q-general, T1-translated, FROZEN — the dispatch payload
       Scan all 40 WellDoc CSV tables for menstrual/cycle/hormone columns. Report which exist, or none.
       Deliverable: QA digest + machine artifact. Do-not: no new data pulls. Accepted: present | absent.
   - reading: |                              ← A-paper (T2), written at harvest
       No cycle column in 40 tables ⇒ C6 supported. → 1-claims.md C6 flips.
```

The five section fields:
- serves: — which stage/claim of MY paper this Q-paper is for; the affinity field a stage gate greps.
- target: — a PATH to the answering FILE (R1); `NEW <task-folder-path>` while the task-folder does not exist. Point at the FILE, never the folder.
- state: — `planned | commissioned | answered | read | answered-local | failed`. DERIVED from disk (PART 6), never asserted.
- commission: — the Q-general, T1-translated, paper-agnostic, FROZEN once written; this is the dispatch payload and nothing else.
- reading: — the A-paper, the T2 interpretation, written at harvest; empty until answered.

HARVEST LANES.
`values:` / `sources:` / `displays:` carry pointers that feed MY `_VALUES_` slot map, MY `.bib`/`_CITATION_` cards, MY `0-displays/` units.
They are paid by the citation/values/display harvesters (transcription only), and omitted entirely when a return carries nothing for them.

BUILD-LANE FIELDS (JL rulings C4 + C6, 2026-07-14).
A section whose answer legitimately takes DAYS-TO-WEEKS additionally carries, and ONLY at `state: commissioned`:
```text
   - owner: <who> · eta: YYYY-MM-DD · blocks: <the claim/demand ids it gates>
   - cross-project: <sibling-project path NAMED as a reuse candidate, or `none-found`>
```
⚠️ THERE IS NO "FAST COMMISSION" EXEMPTION.
A section still at `state: commissioned` when the gate runs is BY DEFINITION build-lane, so the four fields are UNCONDITIONAL there.
`check-probe-cards.sh` enforces them with no lane test: `commissioned-no-owner` / `-no-eta` / `-no-blocks` / `-no-cross-project`.
`cross-project:` is how a named sibling-source candidate reaches the one human gate whose job is authorizing SPEND (the MATCH may NAME it but never CONSUME it).

R6 — the commission lives IN the section.
It survives a dead paper session with ZERO files on the bank side: the paper is the memory.
A section still `planned` two weeks later ⇒ any later session re-dispatches from the commission text, verbatim.

R7 — there is NO "Verdict".
The word is DEAD; `verdicted` as a state is DELETED.
The section's `reading` carries A-paper; the CLAIM's status (`supported | refuted | inconclusive`, plus confidence, claim_type, the G1/G2/G3 gates) lives in `1-claims.md`, judged per-claim, per-paper, PRIVATE.
Judgment CONTENT is still governed by `../haipipe-probe-review/SKILL.md`; only its landing site changed.
⚠️ A DISCOVERY's own `verdict.md` (Review-type terminal file) is a DIFFERENT, executor-native thing, and it SURVIVES.

R8 — the probe file is the ONLY bilingual document.
`## Why` and `reading` speak paper; `commission` speaks general. That is what makes commission blocks a lint surface (LAW 2).


PART 3a — The executor side: QA/, on BOTH banks
===============================================

R9 — every executor task-folder MAY carry a `QA/` folder — task AND discovery, same shape, same rules (optional; not every task-folder has one).
WHY: plan.yaml / results/ / sources.md are code- and evidence-oriented; QA/ is the executor's READABLE digest of what it has established.

NAMING IS THE INDEX.
`QA/<n>-<slug>.md`, where `n` = creation order. `ls QA/` IS the index — numbered, ordered, greppable.
SLUG ONLY — NO PP IDS. A PP id in a bank filename is R2 broken.

R19 — A QA FILE IS A TICKET THAT BECOMES A RECEIPT (JL ruling 2026-07-14).
It carries exactly ONE MUTABLE FIELD — the state line. Everything below it is written once and never touched again.

```markdown
# Q — <the question, restated by the EXECUTOR in its own words>
- state:   working | answered | superseded-by: QA/<m>-<slug>.md
- started: 2026-07-14T09:12          ← MANDATORY when state: working
- by:      <run id | agent | human>  ← optional provenance

## Answer     EMPTY while state: working. Filled at REPORT. plain words + [→ results/<file>] anchors
## Caveats    what this does NOT establish
## Not-done   what was asked but not resolved, and why
```

- state: — the ONLY mutable field, and MANDATORY, ALWAYS. `superseded-by:` is APPENDED to an `answered` line, it does not replace `answered`. A file with NO state line is MALFORMED (not "legacy"): its absence exempts the file from every claim check, so a lying receipt ships by omission. Checker FAILs it — `qa-no-state`.
- started: — the claim's birth time, `YYYY-MM-DDTHH:MM` (from `date +%Y-%m-%dT%H:%M`). MANDATORY on a `working` file: without it the claim can never expire, so it is a zombie. Checker FAILs it — `qa-working-no-started`.
- by: — optional provenance.

⚠️ THE LOAD-BEARING INVARIANT IS *ONE WRITER*, NOT *WRITE-ONCE*.
The EXECUTOR writes the file TWICE, in its own folder: ① at the qa gate's (3) DECISION → the CLAIM (`state: working` + `started:`); ② at REPORT → the COMPLETION (`state: answered` + `## Answer`).
Two writes by the same owner is fine. Nothing is shared, nothing is planted.
⛔ A CONSUMER (probe / paper / application) MUST NEVER create, claim, edit, or complete a QA file — not the state line, not the body, not "just this once".
A consumer-authored `working` file is the retired `_ASK/` stub in a `QA/` costume; the sin is the WRITER, not the half-ness.

THE CLAIM LIFECYCLE — which qa gate path writes what:
```text
   ① QA SCAN    NOTHING — the file already exists, return its path.        no `working`
   ② DIGEST     ONCE, COMPLETE, `state: answered` from existing results/.  no `working` (write is instant)
   ③ P-B-E-R    TWICE: CLAIM at (3) decision (`state: working` + empty     YES, transiently
                Answer); COMPLETION at REPORT (`state: answered` + body).
```

🧟 THE CLAIM MUST EXPIRE.
```text
   QA_WORKING_TTL_HOURS = 24   ← the NAMED CONSTANT. The checker and both qa verbs read this name; never hard-code 24.
   a `working` file whose started: is older than QA_WORKING_TTL_HOURS is STALE:
     · the next qa call MAY RESTART it — rewrite the claim with a FRESH started:, record the abandoned try in ## Not-done.
     · the checker FAILs it (`qa-working-expired`).
```

🏁 THE RACE GUARD — `set -C` (noclobber), and NOTHING MORE.
Two qa calls may reach the (3) decision at once and both pick `QA/3-`; create the claim under noclobber, and the loser re-runs ① QA SCAN and DEFERS.

```bash
QA_WORKING_TTL_HOURS=24
QA_FILE="<task-folder>/QA/<n>-<slug>.md"
mkdir -p "$(dirname "$QA_FILE")"
if ( set -C; cat > "$QA_FILE" ) 2>/dev/null <<EOF
# Q — <the question, restated by the executor>
- state:   working
- started: $(date +%Y-%m-%dT%H:%M)
- by:      <run id | agent | human>

## Answer

## Caveats

## Not-done
EOF
then : # CLAIM WON  → proceed with (3) P-B-E-R; complete at REPORT.
else : # CLAIM LOST → the file exists. Re-run ① QA SCAN and DEFER. Run nothing.
fi
```

A residual same-instant / DIFFERENT-slug collision is NON-FATAL — ① SCAN finds both files.
⛔ DO NOT over-engineer past `set -C`: no lock dirs, no lease servers, no ledgers (all retired machinery in a new hat, PART 9).

R20 — SUPERSESSION.
A later run whose answer CHANGES does NOT edit the old file's body; it writes a NEW file and APPENDS a pointer to the OLD file's state line.
```text
   day 1    QA/1-cycle.md  - state: answered            paper target: → QA/1 · reading "⇒ C6 supported"
   day 40   a re-run lands NEW data. The truth CHANGED.
            the EXECUTOR writes QA/2-cycle.md - state: answered
            and appends       QA/1-cycle.md - state: answered · superseded-by: QA/2-cycle.md
   ⇒ the paper's target: still points at QA/1 — now MACHINE-DETECTABLE. Checker FAILs it (`read-target-superseded`).
```

RECONCILING R20 WITH R15 ("ENRICH never mutates"). R15 holds EXACTLY — for the BODY:
```text
   MUTABLE   the `state:` line, ONLY, and ONLY by the file's own owner. Two edits in a file's whole life:
               working → answered           (completion, at REPORT)
               answered → + superseded-by:  (the pointer, when a later run changes the truth)
   FROZEN    `# Q —` · `## Answer` · `## Caveats` · `## Not-done` — forever, once written.
   ⛔ A CONSUMER writes NEITHER. A probe that finds a stale target re-points its OWN section's target: at the live one.
```

R10 — the three reasons a QA file may exist (there is no fourth):
- commissioned — a dispatch names it ("Deliverable: QA/<n>-<slug>.md answering <Q>"). The EXECUTOR writes it.
- digest-only — results/ or sources.md already answer it but no readable digest exists → light run (qa verb path ②).
- executor's own — an executor session judges a finding worth digesting, including proactive ANSWERABILITY WORK (R17).
⛔ ABUSE GUARD: no QA file without one of the three; a QA/ mirroring every result file is noise, and the lint flags orphans.

R12 — the writer table. Every file has exactly ONE writer.
```text
   papers/X/1-probes/PPNN_<topic>.md · papers/X/1-claims.md          this paper       this paper
   tasks/<g>/<f>/workflow/plan.yaml · results/ · QA/*.md             the task layer   task · probe(match, harvest)
   discoveries/<g>/<f>/terminal · QA/*.md                            discovery layer  disc · probe(match, harvest)
   ⇒ no shared writes anywhere; paper and executor sessions run weeks apart, lock-free.
   ⇒ a QA file is written TWICE by its ONE owner (R19), + a third time only to append superseded-by: (R20).
     A consumer READS it. A consumer NEVER writes it.
```

CC-8 — the PROBE CAUSES a QA file; the EXECUTOR AUTHORS it.
When a probe meets a bare `results/` with no digest it does NOT write the digest — it DISPATCHES a digest-only run (qa path ②): a clean-context agent reads `results/` and writes `QA/<n>-<slug>.md`.
The file comes into existence by the probe's action, but through the executor's hand. That one hop is the entire wall.
The live counter-example on disk: `tasks/A03_welldoc_cycle_check/result.md` carries C6/C7 ("claims-stage") — a consumer session wrote a bank file, and the evidence came back paper-shaped. That is the A03 leak.


PART 3b — The `qa` verb: the executor's question door
=====================================================

R11 — each executor family owns a `qa` verb: `/haipipe-task qa` and `/haipipe-discovery qa`, symmetrically.
It REPLACES the deleted probe-aware `asks` verb — reborn probe-UNAWARE (takes a question, returns an answer).
Input: ONE question in GENERAL language — no PP id, no paper ref, no stake. The verb never learns WHO asks or WHY.

```text
   ① QA SCAN   grep <task-folder>/QA/*.md (or all task-folders, if none given)
               already `answered`? → return the QA file PATH.                            writes NOTHING
               already `working`?  → DO NOT RE-RUN. Return path + "in progress since <started>"
                                     (unless STALE past QA_WORKING_TTL_HOURS — then RESTARTABLE, R19).
   ② DIGEST    results/ (or sources.md / verdict.md) answer it, no digest exists?
               → write QA/<n>-<slug>.md ONCE, COMPLETE, `state: answered`, no code runs.
   ③ P-B-E-R   neither → ⚑ CLAIM FIRST (write `state: working` + `started:` under `set -C`, R19;
               lost the race? → back to ①, DEFER). Then run Plan→Build→Execute→Report at the SHALLOWEST
               depth that answers it (R15), and COMPLETE the same file at REPORT.
   🚫 REFUSE   out of scope for this executor / task-folder. The caller RE-ROUTES. Writes NO QA file; RELEASES any claim.
```

THREE CALLERS, one door:
- 📄 the PROBE's DISPATCH — via the executor ORCHESTRATOR agents (PART 4 ③).
- 🧑 a HUMAN, directly — the everyday "go explore this direction" verb (R18).
- 🤖 the ORCHESTRATOR itself — self-directed answerability work (R17).
The probe's MATCH may also call qa in CHECK-ONLY mode: detect ①/②, execute nothing.
⚠️ qa is the executor's SIDE door; its PRIMARY mode is autonomous P-B-E-R — no question, just the project's own research.

R21 — THE THREE READERS OF THE STATE LINE. The whole value of the claim is on the READ side.
```text
   ① SCAN (a 2nd qa call, days later)   `working` → DO NOT RE-RUN, return path + "in progress since <started>".
                                        An expensive run is SAVED. This is the duplicate-work fix.
   ② PROBE MATCH (a consumer, a week later)  `working` → the question is LIVE. Set the section to
                                        `state: commissioned`, point target: at that QA file, NO SECOND DISPATCH.
                                        ⛔ Do NOT touch the QA file — write only the section. The pen never crosses the wall.
   ③ A HUMAN                            `ls QA/` + the state line reads as BOTH what the folder has ESTABLISHED
                                        and what it is ESTABLISHING right now.
   ⇒ THE FAILURE THIS KILLS: two consumers ask the same question a week apart; the second, mid-run, sees no QA
     file and dispatches THE SAME RUN AGAIN. Before R19, nothing prevented it.
```


PART 4 — The five-step loop
===========================

```text
  📝 DRAFT      raises the Q-papers ({VAL:?}, GAP, open questions)
  ① ORGANIZE   PROBE phase: collect them → probe files, grouped by TOPIC
  ② MATCH      per Q-paper, grep {tasks,discoveries}/**/QA/*.md (+ qa verb, CHECK-ONLY)
               ⚠️ READ THE STATE LINE of every candidate (R21) — existence is no longer the answer.
       ┌──────────┬──────────────┬───────────┬──────────────┬──────────┐
    ✅ HIT      ⏳ IN FLIGHT    🟡 PARTIAL  🟠 LEAF EXISTS  🔴 NOTHING
    answered    working         →           →              →
    → point    → commission +   ─────────── ③ DISPATCH ──────────────
               target:, NO      the commission goes VERBATIM to the EXISTING orchestrators:
               2nd dispatch       Agent(haipipe-task-orchestrator-agent) / Agent(haipipe-discovery-orchestrator-agent)
                                  THEIR CLEAN CONTEXT IS THE WALL (PART 5). Inside, they run the qa gate ①②③.
                                  💀 the old probe GATEWAY agent is RETIRED: its SWEEP became this paper-side MATCH,
                                     its dispatch is now a direct Agent() call. (probe-review SKILL + reviewer agent SURVIVE.)
  ④ POINT      the section's target: → the answering QA FILE (not the folder)
  ⑤ INTERPRET  the section's reading: (T2) · 1-claims.md flips · the lanes harvest
               ⛔ ONLY from a QA file that is `state: answered` and NOT superseded.
```

THE DISPATCH PAYLOAD — one spelling, and it is the EXECUTOR'S. Copy this block; do not invent variants:
```text
Agent(haipipe-task-orchestrator-agent, run_in_background=<true for fresh>, prompt="
  action: qa
  project: <project_root>
  question: |
    <the section's `commission:` block, VERBATIM. Nothing else.>
  task-folder: <the section's target: — an existing path, `NEW <path>`, or omit if unknown>
")
```
…and identically for `Agent(haipipe-discovery-orchestrator-agent, ...)`. The return is a PATH to the answering QA file.

R13 — the cost ladder. Cheap doors first; only T3/T4 summon an agent.
```text
  T0 JOIN    another stage's probe already asks this Q-paper  → add my serves:      ~0
  T1 LOCAL   my own registries answer it                      → answered-local      ~0
  T2 REUSE   an existing QA file answers it                   → point the section   1 grep + 1 read
  T3 ENRICH  the task-folder exists, never asked this         → new section → ③     agent
  T4 FRESH   no task-folder                                   → new section → ③     agent
```
MOST PROBES SHOULD LAND ON T2 — in a healthy project the bank fills autonomously from the executor side (R17), so most answers already exist before anyone asks.
A probe file whose every section is T3/T4 is a smell: either the MATCH was lazy, or the bank is starving.

R14 — MATCH ON THE ANSWER, NEVER ON THE TOPIC. ⚠️ SCOPED TO `state: answered`.
A HIT counts ONLY if the QA file LITERALLY ANSWERS THIS Q-paper — READ it; topic similarity is not evidence.
An answered QA file that does not answer the question is a T3 ENRICH: dispatch it, do not point at it.
⛔ R14 DOES NOT APPLY TO A `working` FILE. Its `## Answer` is EMPTY BY CONSTRUCTION, so it can never pass the literally-answers test, and R14's remedy (DISPATCH) would re-open the exact hole R19 closes.
THE STATE LINE IS READ FIRST, on every reader:
```text
   state: answered   → apply R14. Does ## Answer answer it? no ⇒ T3 ENRICH ⇒ dispatch.
   state: working    → match on the `# Q —` LINE: is that restated question MY question? YES ⇒ ⏳ HIT-IN-FLIGHT
                       — commission + point, DO NOT DISPATCH. (Executor side: return path + "in progress since <started>".)
   superseded-by:    → follow the chain, THEN apply R14 to the live file.
```

R15 — ENRICH NEVER MUTATES, and the DEPTH is the executor's private business.
A new question to an old task-folder = a NEW section + a NEW commission; the executor adds `QA/<n+1>-<slug>.md`.
The executor (inside qa gate ③) picks the SHALLOWEST depth that answers it — the depth IS its entry point into P-B-E-R:
```text
   depth 0 📖 READ        existing results/ hold the answer      → enter at R: write QA, nothing runs
   depth 1 ⚙️ NEW RUN     an existing script + a NEW config      → enter at E: + configs/<new>.yaml + runs/<new>/
   depth 2 🔧 NEW SCRIPT  in-scope (plan.yaml IPO) but no script → enter at B: + <new>.py → Execute → Report
   depth 3 🌱 NEW TASK-FOLDER  outside scope                     → full P-B-E-R from P: sibling folder, next NN
   🚫 REFUSE              wrong executor / wrong shape           → the caller re-routes
   scope test (2 vs 3): does the question fit THIS task-folder's plan.yaml IPO?  yes → new script.  no → new task-folder.
   🔒 THE PROBE NEVER LEARNS WHICH DEPTH WAS USED — it hands over a question, gets back a QA-file path.
```


PART 5 — The two LAWS (the wall is a DISPATCH rule, not a file rule)
===================================================================

The leak that proves it: `tasks/A03_welldoc_cycle_check/result.md` carries the paper's claim ids (C6, C7), written by an executor, with NO probe file involved.
The stake traveled through a paper session's own CONTEXT, because that session did bank work INLINE. No mailbox, no stub, no id — and the leak happened anyway.
That is why the wall cannot be a file rule.

```text
   ✅ paper ──▶ 🤖 executor ORCHESTRATOR (clean context, gets ONLY the commission) ──▶ qa verb ──▶ bank   WALL HOLDS
   ❌ paper session RUNS bank work or WRITES bank files itself, stake in context                    WALL NEVER EXISTED
   ✅ LEGAL & REQUIRED: a READ-ONLY grep of {tasks,discoveries}/**/QA/*.md — that IS ② MATCH. The wall bans the PEN and the RUN, not the EYE.
```

LAW 1 — A CONSUMER SESSION NEVER EXECUTES TASK/DISCOVERY WORK INLINE.
Dispatch means: hand the `commission` block VERBATIM, and nothing else — never `## Why`, never the probe file, never the paper.
The law names the ACT, not the tool: it is broken the moment a consumer session RUNS bank work or WRITES a bank file (including a QA digest it thinks it is being helpful by authoring).
⛔ AND THAT INCLUDES THE CLAIM. R19 gave the QA file a mutable state line; it did NOT give a consumer a pen.
A consumer may not CREATE, CLAIM, COMPLETE, or APPEND `superseded-by:` to a QA file, nor "fix" a stale or zombie one. ONE WRITER — the executor — for the whole life of the file.

LAW 2 — BACKSTOP LINT, ON TWO SURFACES.
```text
   📄 probe files:  commission blocks carry no C\d, no H\d, no stake words ("rescue", "we want", "the hoped-for")
   ⚙️ the bank:     QA/*.md carry no consumer vocabulary (C\d, H\d, "claims-stage", "the paper" meaning *our* paper)
```
LAW 2 would have caught A03; the v1 `_ASK` bridge pass never could (A03 had no `_ASK`).
Both laws are cited by the paper/application PROBE-phase workers, the `qa` verb, and the checker.
`check-probe-cards.sh` KEEPS its filename (65 refs across 33 files); only its internals are rewritten.
⚠️ LAW 2 is a BACKSTOP, not the mechanism. T1 (translate-down) is SEMANTIC; a regex provably misses real leaks — never delete T1 on the theory the lint catches what it lets through.


PART 6 — Status: DERIVED per Q-paper, from the STATE LINE
=========================================================

No state is a claim about an agent (agents die; sessions end). Every state is checkable on disk.
⚠️ STATUS IS NO LONGER DERIVED FROM MERE EXISTENCE — the reader MUST OPEN THE FILE AND READ THE STATE LINE. An `ls` is not enough.

THE BANK-SIDE READING — what a QA file's own state line means:
```text
   no QA file                                 NOT ANSWERED
   state: working                             IN PROGRESS (since <started>) — unless older than
                                              QA_WORKING_TTL_HOURS, then STALE + RESTARTABLE (R19)
   state: answered                            ANSWERED
   state: answered · superseded-by: X         ANSWERED but STALE — the live answer is X. Re-point at X.
   NO state line                              MALFORMED — `state:` is MANDATORY, always. Checker FAILs it (`qa-no-state`).
```

THE SECTION-SIDE READING — the probe question section's own `state:`:
```text
   planned          the section exists · the target task-folder is missing (or `NEW …`)
   commissioned     the task-folder + plan.yaml exist, no QA file yet  OR  the target QA file is `state: working` (R21 ②)
                    — a LIVE question either way. NO SECOND DISPATCH.
   answered         the target QA FILE exists AND is `state: answered` (a `working` target is `commissioned`, not `answered`)
   read             the section's reading: is non-empty (+ 1-claims.md flipped) — LEGAL ONLY against a target that
                    is `state: answered` and carries NO `superseded-by:`
   answered-local   target points into the paper's OWN registries; no dispatch
   failed           a reading with a dead target · the task-folder was deleted · qa REFUSEd
   💀 "verdicted"   DELETED (R7)
```
⚠️ THE BUILD-LANE FIELDS BIND AT `commissioned`, BOTH WAYS IN (fresh run or pointing at someone's `working` file): owner/eta/blocks/cross-project, unconditional, no lane test.

⚖️ THE CHECKER'S TEETH — stated HERE as LAW; `check-probe-cards.sh` implements them. Each must FAIL (exit 1):
- read-target-working — section `read` whose target: is a `working` QA file ⇒ the paper claims it read an unfinished answer.
- read-target-superseded — section `read` whose target: carries `superseded-by:` ⇒ reading built on a stale answer (THE DAY-1/DAY-40 SILENT-FALSE-CLAIM BUG: every file consistent, the claim false, nothing caught it before R20).
- qa-working-no-started — a `working` QA file with no `started:` ⇒ an unexpirable claim.
- qa-working-expired — a `working` QA file whose `started:` is older than QA_WORKING_TTL_HOURS (`date -d`) ⇒ the run is dead.
- qa-answered-empty — a `state: answered` QA file with an EMPTY `## Answer` ⇒ a lying receipt.
- qa-no-state — a QA file under tasks/|discoveries/ with NO `- state:` line ⇒ a lying receipt by omission (also: read-target-no-state · commissioned-target-no-state).
- commissioned-target-answered — a `commissioned` section whose target went `answered` ⇒ the answer landed and nobody harvested it (closes the in-flight loop; sibling: commissioned-target-superseded ⇒ re-point target:).

THE BUILD LANE (JL rulings C4 + C6, 2026-07-14).
Most sections answer in minutes; some legitimately take DAYS-TO-WEEKS and sit at `commissioned` — that is HONEST, and a 3-week build must not red every downstream gate for 3 weeks. The price of passing the gate is a DATE:
```text
   at state: commissioned, a BUILD-lane section MUST carry owner: · eta: YYYY-MM-DD (FUTURE) · blocks: · cross-project:
   ✅ eta in the future, no QA file yet  → PASSES        ❌ eta PASSED, still no QA file  → HARD FAIL at the next gate
   `date -d "$eta"` is a machine test. WITHOUT it, `commissioned` becomes a LAUNDERING TOKEN every un-run section wears.
```


PART 7 — Two session modes, two explorers
=========================================

R17 — TWO SESSION MODES. The executor's is NOT question-driven.
```text
   ⚙️ EXECUTOR session         just runs P-B-E-R (train · sweep · profile · review) — no question, no ask.
                               the bank grows AUTONOMOUSLY; probes mostly land here (T2 REUSE).
                               🆕 ANSWERABILITY WORK: write QA digests for notable findings (R10), build/refactor
                                  code so future questions are CHEAP — probe-unaware, task-native work.
   📄 CONSUMER session         asks questions: DRAFT raises Q-papers → PROBE collects, matches, commissions.
```

R18 — QA FILES ARE EXPLORATION DIRECTIONS, AND THERE ARE TWO EXPLORERS (both probe-UNAWARE).
```text
   🧑 HUMAN         /haipipe-task qa "<direction>"          picks a direction, runs the qa flow, reads the QA file
   🤖 ORCHESTRATOR  Agent(haipipe-task-orchestrator-agent)  COMMISSIONED (a probe handed it a question) OR
                                                            SELF-DIRECTED (answerability work, R17)
   both write the SAME artifact QA/<n>-<slug>.md · both use the SAME gate ①→②→③ · QA/ = the folder's growing map.
```
The probe is therefore ONE CALLER of a door humans and the orchestrator already walk through for their own reasons. It did not invent that door, and does not own it.


PART 8 — Verbs
==============

```text
   /haipipe-probe                    → the contract, in one screen (this file)
   /haipipe-probe contract|anatomy   → the probe-file anatomy + the QA/ contract
   /haipipe-probe status             → derive states from disk (PART 6): ls papers/*/1-probes/PP*.md +
                                       applications/*/1-probes/, resolve each target:, ls the QA files. Never a stored state.
   /haipipe-probe "<question>"       → ROUTE, do not execute. A question with no paper behind it is not a probe —
                                       hand it to the executor's own door: task-shaped → /haipipe-task qa,
                                       discovery-shaped → /haipipe-discovery qa. The QA file IS the receipt.
                                       (If it later matters to a paper: open a section whose target: points at it — T2.)
```


PART 9 — RETIRED MACHINERY (do not resurrect)
=============================================

```text
   💀 probes.ledger · project-unique PP ids   killed by PATH BINDING (R1) — PP numbers are paper-local footnotes.
   💀 _ASK/ and _ANS/ mailboxes               killed by R2 — the commission block replaces the stub entirely.
                                              ⚠️ R19's `state: working` file is NOT this coming back: the stub's sin
                                                 was the WRITER (a consumer planting a half-file), not the half-ness.
   💀 "write-once" as the QA invariant        it was never the rule — ONE WRITER was (R19). Two writes by the same owner.
   💀 lock dirs · lease servers · claim ledgers  `set -C` on the working file is the WHOLE race guard (R19). A ledger
                                              here is probes.ledger reborn — already on this list.
   💀 the `answers:` return field             nothing to grep — the answer IS a file, target: is the pointer.
   💀 /haipipe-task asks (probe-aware)         DEAD — reborn probe-unaware as `qa` (R11).
   💀 haipipe-probe-orchestrator-agent         the GATEWAY. RETIRED 2026-07-14: its SWEEP became the paper-side MATCH,
      (the evidence gateway)                   its dispatch a direct Agent() call. Archived, de-registered.
                                              ✅ SURVIVING: haipipe-probe-review SKILL + haipipe-probe-reviewer-agent.
   💀 the DIRECT-ASK gateway dispatch          a direct ask ROUTES to the executor's qa verb (PART 8), runs no evidence work.
   💀 "Verdict" / "verdicted"                  dead (R7); claim status lives in 1-claims.md. A DISCOVERY's own verdict.md SURVIVES.
   💀 "row" / "table" as probe vocabulary      it is a Q-paper, in its own SECTION. No markdown tables in probe/discovery/source docs.
   💀 "Takeaways" (the card field)             → `reading` (the section field).
   💀 1-probe-plans/                           → 1-probes/.
   💀 "card" (as the name of a probe file)     → probe. ALLOWLIST rename only (~90 of 941 uses mean OTHER things). NEVER a blind sed.
   💀 the project-level probes/ store          a second telling of the executor's own artifacts. Retired 2026-07-05; dead history.
   💀 the INSIGHT layer (insights/, D/I/K/W)   retired 2026-07-12: zero K and zero W ever written. The base is tasks/ + discoveries/.
   💀 the interactive Probe Console            .probe-console.yaml, console panels. Dashboards live in /haipipe-paper enter.
   💀 haipipe-probe-creator-agent              retired to ../_archive/_old/.
   💀 a per-paper COPY of a shared probe        one-writer-per-copy still drifts.
   💀 cross-repo pointers / content hashes      three papers are FOREIGN git repos.
   💀 a shared Deliverable/Do-not/Accepted      an acceptance space is a FUNCTION of the stake; freezing consumer-1's frame makes evidence paper-shaped forever.
   💀 merging two papers' same-numbered probes  two lossy projections ≠ one question.
   💀 a cross-project ("continent") tier        separate repos; the buy is one avoided run. (BUILD-lane cross-project: NAMES a candidate, never CONSUMES one.)
   💀 deleting T1 (translate-down)              the regex lint provably misses real leaks; T1 is semantic, LAW 2 only a backstop.
```

Live instruments that survive: `../haipipe-probe-review/SKILL.md` (the G1/G2/G3 gates, `supported | refuted | inconclusive`, `claim_type`), plus its `g2_integrity_check.py` and `probe-caveats-checklist.txt`.
Judgment CONTENT is that skill's business; where the judgment LANDS (`1-claims.md`, per-claim, per-paper, private) is this file's.
