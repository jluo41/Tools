Probe files (application)
==========================

The intervention accumulates its open QUESTIONS as **probe files** during lifecycle work (seed, the 1a–1d evidence ladder, pitch, narrative, display, section-edit).
The DRAFT phase RAISES the questions AND authors their probe plan (① ORGANIZE + ② MATCH: q-executor / route / bank / target); the PROBE phase runs the plan forward (③ DISPATCH → ④ POINT → ⑤ INTERPRET) and binds each one to an answer.

The MODEL itself is owned by `../../../probe/haipipe-probe/SKILL.md`.
Read that; this file only carries the application-side paths and verbs.
This is the paper twin's `fn/probes.md`, the same document with application paths.

Location — one FLAT pool, one file per TOPIC
----------------------------------------------

```
<intervention>/
└── 1-probes/
    ├── PP01_refill-timing.md     one file per TOPIC, question entries inside
    ├── PP02_channel-capacity.md
    └── README.md                 a GENERATED board (see below); the files win
```

- `1-probes/` — NOT `1-probe-plans/`, NOT a per-stage `_PROBE/` folder. Both are RETIRED.
- Stage affinity is a `### q-consumer` bullet's stage-doc id, never the file's path. One flat cross-stage pool.
- PP numbers are **intervention-local footnote numbers**. `ls 1-probes/` is the numbering authority.
  There is no ledger, and no PP id ever crosses to the task/discovery bank — so two interventions may both carry a PP03 with nothing to reconcile, the way two books both carry a footnote 4.
- **Legacy migration (on first touch):** a file found in `1-probe-plans/` or `0-lifecycle/<stage>/_PROBE/` is rewritten into `1-probes/` in the new shape by whatever verb touched it.
  Log the move in the stage `_LOG`. Do not migrate what you did not touch.
  There are NO stage-owned sidecar docs — the answer + its numbers live in the entry's `### a-executor`, anchored to `target:`. `_LOG` is the only kept sidecar.

Probe file anatomy
-------------------

Full spec: the "The probe file" section of `../../../probe/haipipe-probe/SKILL.md`. In brief — one `## QX<n>` ENTRY per q-executor, four `###` subsections each; no `## Why` (the stake lives in each Q-consumer, in the stage doc):

```markdown
# PP01 — refill-reminder timing feasibility

## QX1 — response window

### q-executor
The question in GENERAL language — no claim ids, no stake, no hint of which
answer is wanted. This is the DISPATCH PAYLOAD, and nothing else is. FROZEN.
Deliverable: <what comes back>
Accepted: <a> | <b>

### q-consumer
* Q-Claims-2 — that consumer's ORIGINAL question, copied in (id + wording)

### bank binding
**route**: task | discovery
**bank**: reuse | run | code | new
**target**: tasks/X03_refill_timing/01_window_scan/QA/1-response-window.md
**state**: planned | commissioned | answered | read | answered-local | failed

### a-executor
A COPY of the answering QA file's answer, written at harvest — with any
numbers/citations inline, each anchored [→ target QA]. Empty until answered.
```

⛔ No markdown tables in a probe file. It holds `## QX<n>` ENTRIES with `###` subsections. The words "card", "row" and "table" are not part of this vocabulary.

**BUILD-lane fields** — present ONLY at `state: commissioned`, on work that takes days to weeks (a task run over new data, or a long acquisition such as a DUA/IRB), added under `### bank binding`: `**owner**:` · `**eta**: YYYY-MM-DD` · `**blocks**:` · `**cross-project**: <sibling path | none-found>`.
A future `eta` PASSES the gate — a 3-week build has not failed, it is WORKING, and it must not red every downstream gate for 3 weeks.
An `eta` that has PASSED with no answer is a HARD FAIL: without the date test, `commissioned` becomes the state every un-run entry wears and the mechanism ships as a laundering token.
`cross-project:` is MANDATORY on every BUILD-lane entry. Enforced by `check-probe-cards.sh`.

States (DERIVED from disk — never asserted)
--------------------------------------------

```
planned          the entry exists · the target leaf is missing (or `NEW …`)
commissioned     the task-folder + its plan.yaml exist · the QA file is absent
answered         the target QA FILE exists
read             the entry's `### a-executor` is non-empty (+ 1c-claims.md flipped, if it serves a claim)
answered-local   target points into the intervention's OWN registries; no dispatch happened
failed           a reading with a dead target · the task-folder was deleted · the qa verb REFUSEd
```

An entry in flight is `commissioned`.
A claim's STATUS (`supported | refuted | inconclusive` + confidence) lives in `0-lifecycle/1c-claims/1c-claims.md`, flipping its C-line and Evidence Campaign row.
It is not a probe field: the probe carries the evidence, the author writes the judgment.

Binding is by PATH, never by id
--------------------------------

An entry's `target:` is a PATH to the answering file — a **QA file** in the bank:

```
tasks/<task-group>/<task-folder>/QA/<n>-<slug>.md          discoveries/<discovery-group>/<discovery-folder>/QA/<n>-<slug>.md
```

The QA file is the EXECUTOR's readable digest of a direction it explored: `# Q` / `## Answer` / `## Caveats` / `## Not-done`, in general language, with anchors into `results/` or `sources.md`.
`ls QA/` IS the index. Point at the FILE, never the folder — a leaf that answered three things cannot tell you which one is yours.

**The probe CAUSES a QA file; the EXECUTOR AUTHORS it.** When a probe meets a bare `results/` with no digest, it does not write the digest: it DISPATCHES a digest-only run.
An intervention session that writes in the bank has broken LAW 1, whatever it ends up writing.

Commands
---------

```
/haipipe-application probe "<question>"   raise a question -> an ENTRY in the right topic's probe
                                          file (creating the file if the topic is new)
/haipipe-application probe                show the board (derived from 1-probes/ on disk, never stored)
/haipipe-application probe run            run the loop forward over every open entry
/haipipe-application probe run PP01       run it for one probe file
```

All four go through `haipipe-application-probe` (the PROBE phase worker) — the single door.

The loop — DRAFT authors ①②; haipipe-application-probe runs ③④⑤
-----------------------------------------------------------------

```
DRAFT authors the plan (① ORGANIZE + ② MATCH):
  ① ORGANIZE   collect the questions into 1-probes/, grouped by topic; write each entry's
               `### q-executor` (stake stripped, + Deliverable/Accepted) + `### q-consumer`
               bullet + `route`
  ② MATCH      T0 JOIN · T1 LOCAL · T2 REUSE — grep the bank's QA corpus, READ the hits, and
               root each question to a SPECIFIC bank folder in `bank` (reuse | run | code | new),
               setting `target` (an existing path, or `NEW <path>`).
               → most entries should stop HERE. A NEW dispatch is the EXCEPTION, not the norm.
  ── ONE human gate reviews draft + probe plan together ──
PROBE runs the plan forward (route/bank are AUTHORITATIVE — executed, not re-decided):
  ③ DISPATCH   target: NEW only, via Agent(haipipe-probe-q-executor-agent), which hands the
               `### q-executor` VERBATIM to Agent(haipipe-task-orchestrator-agent) /
               Agent(haipipe-discovery-orchestrator-agent) in stake-free clean context —
               that context IS the wall.
  ④ POINT      target: → the answering QA FILE (verify with ls + the state line)
  ⑤ INTERPRET  `### a-executor` (the copy, numbers inline) → stage-doc a-consumer → 1c-claims.md flips
```

⛔ **MATCH BEFORE DISPATCH — both at PROBE, in that order.** The bank fills AUTONOMOUSLY from the executor side, so in a healthy project most answers already exist before anyone asks.
A probe file whose every entry is NEW-to-dispatch is a SMELL — either the MATCH was lazy, or the bank is starving. Say which, in the reply.

Lifecycle Integration
----------------------

Any lifecycle stage can raise a question:
- 0-seed: "landscape / prior interventions" -> an entry in the matching topic's probe file
- 1a-descriptions: a data-profile question -> an entry (the answer's numbers land in the entry's `### a-executor`, anchored to target:)
- 1c-claims: every GAP / weak claim -> an entry

The entry captures the question immediately; the MATCH may close it for free, and only a T3/T4 entry is ever dispatched.

Relation to the direct task / discover verbs
---------------------------------------------

The umbrella keeps `task` and `discover` as direct verbs for NON-claim utility work ("just pull the click rates", "find benchmark papers").
Anything tied to an intervention claim or evidence need goes through a stage's PROBE phase — the probe file preserves the claim-evidence chain and makes the backlog visible.
A question with no intervention behind it does not need a probe file at all — hand it straight to the executor's own door (`/haipipe-task qa` / `/haipipe-discovery qa`); if the answer later matters, open an entry whose `target:` points at the already-written QA file (a T2 REUSE — nothing re-runs).
