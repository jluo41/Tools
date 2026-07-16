Probe files (application)
==========================

The intervention accumulates its open QUESTIONS as **probe files** during lifecycle work (seed, the 1a–1d evidence ladder, pitch, narrative, display, section-edit).
The DRAFT phase RAISES the questions; the PROBE phase COLLECTS them into probe files and binds each one to an answer.

The MODEL itself is owned by `../../../probe/haipipe-probe/SKILL.md` (the constitution).
Read that; this file only carries the application-side paths and verbs.
This is the paper twin's `fn/probes.md`, the same document with application paths.

Location — one FLAT pool, one file per TOPIC
----------------------------------------------

```
<intervention>/
└── 1-probes/
    ├── PP01_refill-timing.md     one file per TOPIC, question sections inside
    ├── PP02_channel-capacity.md
    └── README.md                 a GENERATED board (see below); the files win
```

- `1-probes/` — NOT `1-probe-plans/`, NOT a per-stage `_PROBE/` folder. Both are RETIRED.
- Stage affinity is a SECTION's `serves:` field, never the file's path. One flat cross-stage pool.
- PP numbers are **intervention-local footnote numbers**. `ls 1-probes/` is the numbering authority.
  There is no ledger, and no PP id ever crosses to the task/discovery bank — so two interventions may both carry a PP03 with nothing to reconcile, the way two books both carry a footnote 4.
- **Legacy migration (on first touch):** a file found in `1-probe-plans/` or `0-lifecycle/<stage>/_PROBE/` is rewritten into `1-probes/` in the new shape by whatever verb touched it.
  Log the move in the stage `_LOG`. Do not migrate what you did not touch.
  Stage-owned working docs (`_CITATION_`, `_VALUES_`, `_DISPLAY_`, `_DESCRIPTIONS/`) do NOT move — they stay with their stage.

Probe file anatomy
-------------------

Full spec: the constitution's "The probe file" section. In brief — one `## Why` per FILE, one SECTION per question:

```markdown
# PP01 — refill-reminder timing feasibility
- mode: light | full

## Why
The stake, in intervention vocabulary (which claim dies, and how).
NEVER dispatched. NEVER copied anywhere. It does not leave this file.

## Q1 — response window
- serves: 1c-claims (C2)
- target: tasks/X03_refill_timing/01_window_scan/QA/1-response-window.md
- state:  read
- q-executor: |
    The question in GENERAL language — no claim ids, no stake, no hint of which
    answer is wanted. This is the DISPATCH PAYLOAD, and nothing else is. FROZEN.
- a-consumer: |
    What the answer MEANS for this intervention. Written at harvest.

- values: … · sources: … · displays: …     the harvest lanes
```

⛔ No markdown tables in a probe file. It holds SECTIONS. The words "card", "row" and "table" are not part of this vocabulary.

**BUILD-lane fields** — present ONLY at `state: commissioned`, on work that takes days to weeks (a task run over new data, or a long acquisition such as a DUA/IRB): `owner:` · `eta: YYYY-MM-DD` · `blocks:` · `cross-project: <sibling path | none-found>`.
A future `eta` PASSES the gate — a 3-week build has not failed, it is WORKING, and it must not red every downstream gate for 3 weeks.
An `eta` that has PASSED with no answer is a HARD FAIL: without the date test, `commissioned` becomes the state every un-run section wears and the mechanism ships as a laundering token.
`cross-project:` is MANDATORY on every BUILD-lane section (JL rulings C4 + C6, 2026-07-14). Enforced by `check-probe-cards.sh`.

States (DERIVED from disk — never asserted)
--------------------------------------------

```
planned          the section exists · the target leaf is missing (or `NEW …`)
commissioned     the task-folder + its plan.yaml exist · the QA file is absent
answered          the target QA FILE exists
read             the section's a-consumer: is non-empty (+ 1c-claims.md flipped, if it serves a claim)
answered-local   target points into the intervention's OWN registries; no dispatch happened
failed           a reading with a dead target · the task-folder was deleted · the qa verb REFUSEd
```

💀 `verdicted` is DELETED. 💀 `dispatched` is DELETED (say `commissioned`).
A claim's STATUS (`supported | refuted | inconclusive` + confidence) lives in `0-lifecycle/1c-claims/1c-claims.md`, flipping its C-line and Evidence Campaign row.
It is not a probe field. There is no `## Verdict`, and there is no G1/G2/G3 review gate.

Binding is by PATH, never by id
--------------------------------

A section's `target:` is a PATH to the answering file — a **QA file** in the bank:

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
/haipipe-application probe "<question>"   raise a question -> a SECTION in the right topic's probe
                                          file (creating the file if the topic is new)
/haipipe-application probe                show the board (derived from 1-probes/ on disk, never stored)
/haipipe-application probe run            run the five-step loop over every open section
/haipipe-application probe run PP01       run it for one probe file
```

All four go through `haipipe-application-probe` (the PROBE phase worker) — the single door.

The loop (owned by haipipe-application-probe)
-----------------------------------------------

```
DRAFT raises the questions
  ① ORGANIZE   collect them into 1-probes/, grouped by topic; write each q-executor (T1)
  ② MATCH      T0 JOIN · T1 LOCAL · T2 REUSE (grep the bank's QA corpus, and READ the hits)
               → most sections should stop HERE. A q-executor is the EXCEPTION, not the norm.
  ③ DISPATCH   T3/T4 only, via Agent(haipipe-probe-q-executor-agent), which hands the q-executor
               VERBATIM to Agent(haipipe-task-orchestrator-agent) / Agent(haipipe-discovery-orchestrator-agent)
               in stake-free clean context — that context IS the wall.
  ④ POINT      target: → the answering QA FILE (verify with ls + the state line)
  ⑤ INTERPRET  a-consumer: → 1c-claims.md flips → the harvest lanes pay out
```

⛔ **MATCH BEFORE DISPATCH.** The pre-redesign rule was "dispatch every planned probe, ALWAYS, no matter how small the need".
That is now exactly backwards: the bank fills AUTONOMOUSLY from the executor side, so in a healthy project most answers already exist before anyone asks.
A probe file whose every section is T3/T4 is a SMELL — either the MATCH was lazy, or the bank is starving. Say which, in the reply.

Lifecycle Integration
----------------------

Any lifecycle stage can raise a question:
- 0-seed: "landscape / prior interventions" -> a section in the matching topic's probe file
- 1a-descriptions: a data-profile question -> a section (its `values:` lane lands in `_DESCRIPTIONS/DS<n>`)
- 1c-claims: every GAP / weak claim -> a section

The section captures the question immediately; the MATCH may close it for free, and only a T3/T4 section is ever dispatched.

Relation to the direct task / discover verbs
---------------------------------------------

The umbrella keeps `task` and `discover` as direct verbs for NON-claim utility work ("just pull the click rates", "find benchmark papers").
Anything tied to an intervention claim or evidence need goes through a stage's PROBE phase — the probe file preserves the claim-evidence chain and makes the backlog visible.
A question with no intervention behind it does not need a probe file at all — hand it straight to the executor's own door (`/haipipe-task qa` / `/haipipe-discovery qa`); if the answer later matters, open a section whose `target:` points at the already-written QA file (a T2 REUSE — nothing re-runs).
