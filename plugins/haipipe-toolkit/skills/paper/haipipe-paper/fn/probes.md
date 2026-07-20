Probe files (paper)
====================

The paper accumulates its open QUESTIONS as **probe files** during lifecycle work (seed,
resource, claims, pitch, narrative, display, section-edit). The DRAFT phase RAISES the questions
AND authors their probe plan (① ORGANIZE + ② MATCH: q-executor / route / bank / target); the
PROBE phase runs the plan forward (③ DISPATCH → ④ POINT → ⑤ INTERPRET) and binds each to an answer.

The MODEL itself is owned by `../../../probe/haipipe-probe/SKILL.md` (v9.5.0).
Read that; this file only carries the paper-side paths and verbs. The application twin is the
same document with application paths.

Location — one FLAT pool, one file per TOPIC
----------------------------------------------

```
<paper>/
└── 1-probes/
    ├── PP01_welldoc-feasibility.md   one file per TOPIC, question entries inside
    ├── PP02_cgm-horizon.md
    └── README.md                     a GENERATED board (see below); the files win
```

- `1-probes/` — NOT `1-probe-plans/`, NOT a per-stage `_PROBE/` folder. Both are RETIRED.
- Stage affinity is an ENTRY's `### q-consumer` bullet, never the file's path. One flat cross-stage pool.
- PP numbers are **paper-local footnote numbers**. `ls 1-probes/` is the numbering authority.
  There is no ledger, and no PP id ever crosses to the task/discovery bank — so two papers may
  both carry a PP03 with nothing to reconcile, the way two books both carry a footnote 4.
- **Legacy migration (on first touch):** a file found in `1-probe-plans/` or
  `0-lifecycle/<stage>/_PROBE/` is rewritten into `1-probes/` in the new shape by whatever verb
  touched it. Log the move in the stage `_LOG`. Do not migrate what you did not touch.
  `1-probes/` is the only consumer-side source of truth; `_LOG_<stage>.md` is the only sidecar.

Probe file anatomy
-------------------

Full spec: `probe/haipipe-probe/SKILL.md` → "The probe file". In brief — there is NO `## Why` (the stake
lives in each Q-consumer, in the stage doc, not here); one file per TOPIC; one `## QX<n>` ENTRY per
Q-EXECUTOR, each with four `###` subsections. The file is Q-executor-oriented — the consumers hang
off it.

```markdown
# PP01 — WellDoc data feasibility

## QX1 — cycle indicator

### q-executor
Scan all 40 WellDoc CSV tables for menstrual/cycle/hormone columns. Report which exist, or none.
Deliverable: QA digest + machine artifact. Accepted: present | absent.

### q-consumer
* Q-Claim-6 — does WellDoc have a cycle column? (C6 dies if it does)

### bank binding
**route**: task
**bank**: reuse
**target**: tasks/A03_welldoc_cycle_check/01_column_scan/QA/1-cycle-indicator.md
**state**: read

### a-executor
No cycle column in 40 tables.
```

- `### q-executor` — the question in GENERAL language: no claim ids, no stake, no hint of which
  answer is wanted. This is the DISPATCH PAYLOAD, and nothing else is. FROZEN once written. Carries
  its own `Deliverable:` line and an `Accepted: a | b` line.
- `### q-consumer` — one bullet per Q-consumer this q-executor serves: the stage-doc `Q-<Stage>-<n>`
  id + that consumer's ORIGINAL question, copied in (review-only, never dispatched). One q-executor
  serving several Q-consumers IS reuse, structurally. A stage gate greps these ids for its stage
  token (Q-Seed-1 → seed).
- `### bank binding` — four `**field**:` lines: `route` (task | discovery, the dispatch door,
  AUTHORITATIVE), `bank` (reuse | run | code | new — the DRAFT verdict, judged by a read-only grep
  ON THE ANSWER), `target` (a PATH to the answering QA FILE, `NEW <path>` while unwritten, `NEW ?`
  while even the folder is undecided), `state` (DERIVED from disk, never asserted).
- `### a-executor` — a COPY of the answering QA file's answer, written at HARVEST (PROBE ⑤); empty
  until answered. The consumer-side single source of truth. Each Q-consumer then writes its OWN
  a-consumer in its stage doc (station ②), anchored `[source: PP<NN>]` back to this copy.

The STAKE never appears in a probe file — it lives in each Q-consumer, in the stage doc.

⛔ No markdown tables in a probe file. It holds ENTRIES. The words "card", "row" and "table"
are not part of this vocabulary.

**BUILD-lane fields** — present ONLY at `state: commissioned`, on work that takes days to weeks
(`task-for-data` / `task-for-algo` / `task-for-fit`, or a long acquisition such as a DUA/IRB),
added under `### bank binding`:
`**owner**:` · `**eta**: YYYY-MM-DD` · `**blocks**:` · `**cross-project**: <sibling path | none-found>`.
A future `eta` PASSES the gate — a 3-week build has not failed, it is WORKING, and it must not
red every downstream gate for 3 weeks. An `eta` that has PASSED with no answer is a HARD FAIL:
without the date test, `commissioned` becomes the state every un-run section wears and the
mechanism ships as a laundering token. `cross-project:` is MANDATORY on every BUILD-lane section.
Enforced by `check-probe-cards.sh`.

States (DERIVED from disk — never asserted)
--------------------------------------------

```
planned          the entry exists · the target leaf is missing (or `NEW …`)
commissioned     the task-folder + its plan.yaml exist · the QA file is absent
answered         the target QA FILE exists
read             the entry's `### a-executor` is non-empty (+ 1b-claims.md flipped, if it serves a claim)
answered-local   target points into the paper's OWN registries; no dispatch happened
failed           a reading with a dead target · the task-folder was deleted · the qa verb REFUSEd
```

An entry in flight is `commissioned`.
A claim's STATUS (`supported | refuted | inconclusive` + confidence + claim_type)
lives in `0-lifecycle/1b-claims/1b-claims.md`. It is not a probe field.

Binding is by PATH, never by id
--------------------------------

An entry's `target` is a PATH to the answering file — a **QA file** in the bank:

```
tasks/<task-group>/<task-folder>/QA/<n>-<slug>.md          discoveries/<discovery-group>/<discovery-folder>/QA/<n>-<slug>.md
```

The QA file is the EXECUTOR's readable digest of a direction it explored: `# Q` / `## Answer` /
`## Caveats` / `## Not-done`, in general language, with anchors into `results/` or `sources.md`.
`ls QA/` IS the index. Point at the FILE, never the folder — a leaf that answered three things
cannot tell you which one is yours.

**The probe CAUSES a QA file; the EXECUTOR AUTHORS it.** When a probe meets a bare `results/`
with no digest, it does not write the digest: it DISPATCHES a digest-only run. A paper session
that writes in the bank has broken LAW 1, whatever it ends up writing — that is exactly how
`tasks/A03_welldoc_cycle_check/result.md` ended up carrying "C6"/"C7".

Commands
---------

```
/haipipe-paper probe "<question>"   raise a question -> a QX<n> ENTRY in the right topic's probe
                                    file (creating the file if the topic is new)
/haipipe-paper probe                show the board (derived from 1-probes/ on disk, never stored)
/haipipe-paper probe run            run the five-step loop over every open entry
/haipipe-paper probe run PP01       run it for one probe file
```

All four go through `haipipe-paper-probe` (the PROBE phase worker) — the single door.

The loop — DRAFT authors ①②; haipipe-paper-probe runs ③④⑤
----------------------------------------------------------

```
DRAFT authors the plan (probe v9.5.0):
  ① ORGANIZE   collect the questions into 1-probes/, grouped by topic; find-or-open each
               `## QX<n>`, write its `### q-executor` (stake stripped), copy the Q-consumer
               under `### q-consumer`, and choose its `route`:
  ② MATCH      T0 JOIN · T1 LOCAL · T2 REUSE — grep the bank's QA corpus, READ the hits, and
               ROOT each question to a SPECIFIC folder: set `bank` (reuse | run | code | new)
               and `target` (an existing QA path, or `NEW <path>`).
               → most entries should stop HERE. A NEW dispatch is the EXCEPTION, not the norm.
  ── ONE human gate reviews draft + probe plan together ──
PROBE runs the plan forward (route/bank are AUTHORITATIVE — executed, not re-decided):
  ③ DISPATCH   target: NEW only: the `### q-executor` block, VERBATIM, to
                 Agent(haipipe-task-orchestrator-agent)
                 Agent(haipipe-discovery-orchestrator-agent)
               their clean context IS the wall; dispatch goes direct.
  ④ POINT      target: → the answering QA FILE (open it, read the state: line)
  ⑤ INTERPRET  `### a-executor` (copy the QA answer, HARVEST inline: source anchors,
                 values, display-unit paths) → each consumer's a-consumer in its stage
                 doc → 1b-claims.md flips
```

⛔ **MATCH (at DRAFT) BEFORE DISPATCH (at PROBE).** The bank fills AUTONOMOUSLY from the executor
side, so in a healthy project most answers already exist before anyone asks. A probe file whose
every entry is NEW-to-dispatch is a SMELL — either the MATCH was lazy, or the bank is starving.
Say which, in the reply.

Lifecycle Integration
----------------------

Any lifecycle stage can raise a question:
- 0-seed: "NEED-1 (probe): expand ex ante audit" -> an entry in the matching topic's probe file
- 1-resource: each GATE-1-approved `Q<n>` -> an entry, plus a `-> PP<NN>` backlink written back
  into 1a-resource.md (that backlink is the mechanical proof the question was ASKED, and the
  CHECK gate tests it)
- 2-claims: every GAP / weak claim -> an entry

The entry captures the question immediately; the MATCH may close it for free, and only a T3/T4
entry is ever dispatched.

A standalone question — one with no paper behind it
----------------------------------------------------

There is no `task` or `discover` verb on the paper front door; the paper reaches the bank only
through a stage's PROBE phase. A question with no paper behind it does not need a probe file at
all — a HUMAN hands it straight to the executor's own door:

```
/haipipe-task qa "<question>"        the everyday "go explore this" verb; the QA file is the receipt
/haipipe-discovery qa "<question>"   same, for external evidence
```

If that answer later matters to the paper, open an entry whose `target` points at the
already-written QA file. That is a T2 REUSE — nothing re-runs.
