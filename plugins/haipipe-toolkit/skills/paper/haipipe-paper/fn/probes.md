Probe files (paper)
====================

The paper accumulates its open QUESTIONS as **probe files** during lifecycle work (seed,
resource, claims, pitch, narrative, display, section-edit). The DRAFT phase RAISES the questions;
the PROBE phase COLLECTS them into probe files and binds each one to an answer.

The MODEL itself is owned by `../../../probe/haipipe-probe/SKILL.md` (v8.0.0, the constitution).
Read that; this file only carries the paper-side paths and verbs. The application twin is the
same document with application paths.

Location — one FLAT pool, one file per TOPIC
----------------------------------------------

```
<paper>/
└── 1-probes/
    ├── PP01_welldoc-feasibility.md   one file per TOPIC, question sections inside
    ├── PP02_cgm-horizon.md
    └── README.md                     a GENERATED board (see below); the files win
```

- `1-probes/` — NOT `1-probe-plans/`, NOT a per-stage `_PROBE/` folder. Both are RETIRED.
- Stage affinity is a SECTION's `serves:` field, never the file's path. One flat cross-stage pool.
- PP numbers are **paper-local footnote numbers**. `ls 1-probes/` is the numbering authority.
  There is no ledger, and no PP id ever crosses to the task/discovery bank — so two papers may
  both carry a PP03 with nothing to reconcile, the way two books both carry a footnote 4.
- **Legacy migration (on first touch):** a file found in `1-probe-plans/` or
  `0-lifecycle/<stage>/_PROBE/` is rewritten into `1-probes/` in the new shape by whatever verb
  touched it. Log the move in the stage `_LOG`. Do not migrate what you did not touch.
  Stage-owned working docs (`_CITATION_`, `_VALUES_`, `_EVIDENCE_`, `_DISPLAY_`) do NOT move —
  they stay with their stage.

Probe file anatomy
-------------------

Full spec: the constitution's "The probe file" section. In brief — one `## Why` per FILE, one SECTION per question:

```markdown
# PP01 — WellDoc data feasibility
- mode: light | full

## Why
The stake, in paper vocabulary (which claims die, and how).
NEVER dispatched. NEVER copied anywhere. It does not leave this file.

## Q1 — cycle indicator
- serves: 1-claims (C6)
- target: tasks/A03_welldoc_cycle_check/01_column_scan/QA/1-cycle-indicator.md
- state:  read
- q-executor: |
    The question in GENERAL language — no claim ids, no stake, no hint of which
    answer is wanted. This is the DISPATCH PAYLOAD, and nothing else is. FROZEN.
- a-consumer: |
    What the answer MEANS for this paper. Written at harvest.

- values: … · sources: … · displays: …     the harvest lanes
```

⛔ No markdown tables in a probe file. It holds SECTIONS. The words "card", "row" and "table"
are not part of this vocabulary.

**BUILD-lane fields** — present ONLY at `state: commissioned`, on work that takes days to weeks
(`task-for-data` / `task-for-algo` / `task-for-fit`, or a long acquisition such as a DUA/IRB):
`owner:` · `eta: YYYY-MM-DD` · `blocks:` · `cross-project: <sibling path | none-found>`.
A future `eta` PASSES the gate — a 3-week build has not failed, it is WORKING, and it must not
red every downstream gate for 3 weeks. An `eta` that has PASSED with no answer is a HARD FAIL:
without the date test, `commissioned` becomes the state every un-run section wears and the
mechanism ships as a laundering token. `cross-project:` is MANDATORY on every BUILD-lane section
(JL rulings C4 + C6, 2026-07-14). Enforced by `check-probe-cards.sh`.

States (DERIVED from disk — never asserted)
--------------------------------------------

```
planned          the section exists · the target leaf is missing (or `NEW …`)
commissioned     the task-folder + its plan.yaml exist · the QA file is absent
answered         the target QA FILE exists
read             the section's a-consumer: is non-empty (+ 1b-claims.md flipped, if it serves a claim)
answered-local   target points into the paper's OWN registries; no dispatch happened
failed           a reading with a dead target · the task-folder was deleted · the qa verb REFUSEd
```

💀 `verdicted` is DELETED. 💀 `dispatched` is DELETED (say `commissioned`).
A claim's STATUS (`supported | refuted | inconclusive` + confidence + claim_type)
lives in `0-lifecycle/1b-claims/1b-claims.md`. It is not a probe field. There is no `## Verdict`.

Binding is by PATH, never by id
--------------------------------

A section's `target:` is a PATH to the answering file — a **QA file** in the bank:

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
/haipipe-paper probe "<question>"   raise a question -> a SECTION in the right topic's probe
                                    file (creating the file if the topic is new)
/haipipe-paper probe                show the board (derived from 1-probes/ on disk, never stored)
/haipipe-paper probe run            run the five-step loop over every open section
/haipipe-paper probe run PP01       run it for one probe file
```

All four go through `haipipe-paper-probe` (the PROBE phase worker) — the single door.

The loop (owned by haipipe-paper-probe)
-----------------------------------------

```
DRAFT raises the questions
  ① ORGANIZE   collect them into 1-probes/, grouped by topic; write each q-executor (T1)
  ② MATCH      T0 JOIN · T1 LOCAL · T2 REUSE (grep the bank's QA corpus, and READ the hits)
               → most sections should stop HERE. A q-executor is the EXCEPTION, not the norm.
  ③ DISPATCH   T3/T4 only: the q-executor block, VERBATIM, to
                 Agent(haipipe-task-orchestrator-agent)
                 Agent(haipipe-discovery-orchestrator-agent)
               their clean context IS the wall; dispatch goes direct.
  ④ POINT      target: → the answering QA FILE (verify with ls)
  ⑤ INTERPRET  a-consumer: → 1b-claims.md flips → the harvest lanes pay out
```

⛔ **MATCH BEFORE DISPATCH.** The pre-v8 rule was "dispatch every planned probe, ALWAYS, no
matter how small the need". That is now exactly backwards: the bank fills AUTONOMOUSLY from the
executor side, so in a healthy project most answers already exist before anyone asks. A probe
file whose every section is T3/T4 is a SMELL — either the MATCH was lazy, or the bank is
starving. Say which, in the reply.

Lifecycle Integration
----------------------

Any lifecycle stage can raise a question:
- 0-seed: "NEED-1 (probe): expand ex ante audit" -> a section in the matching topic's probe file
- 1-resource: each GATE-1-approved `Q<n>` -> a section, plus a `-> PP<NN>` backlink written back
  into 1a-resource.md (that backlink is the mechanical proof the question was ASKED, and the
  CHECK gate tests it)
- 2-claims: every GAP / weak claim -> a section

The section captures the question immediately; the MATCH may close it for free, and only a T3/T4
section is ever dispatched.

A standalone question — one with no paper behind it
----------------------------------------------------

There is no `task` or `discover` verb on the paper front door; the paper reaches the bank only
through a stage's PROBE phase. A question with no paper behind it does not need a probe file at
all — a HUMAN hands it straight to the executor's own door:

```
/haipipe-task qa "<question>"        the everyday "go explore this" verb; the QA file is the receipt
/haipipe-discovery qa "<question>"   same, for external evidence
```

If that answer later matters to the paper, open a section whose `target:` points at the
already-written QA file. That is a T2 REUSE — nothing re-runs.
