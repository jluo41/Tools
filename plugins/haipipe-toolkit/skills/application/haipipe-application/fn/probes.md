Probe files (application)
===========================

The intervention accumulates its open QUESTIONS as **probe files** during lifecycle work
(seed, claims, venue, display, section-edit). The DRAFT phase RAISES the questions; the PROBE
phase COLLECTS them into probe files and binds each one to an answer.

Mirror of `../../../paper/haipipe-paper/fn/probes.md` — same probe model, same anatomy,
application paths. The MODEL itself is owned by `../../../probe/haipipe-probe/SKILL.md`
(the constitution). Read that; this file only carries the application-side paths and verbs.

Location — one FLAT pool, one file per TOPIC
----------------------------------------------

```
<intervention>/
└── 1-probes/
    ├── PP01_refill-timing.md      one file per TOPIC, sections inside
    ├── PP02_channel-capability.md
    └── README.md                  a GENERATED board (see below); the files win
```

- `1-probes/` — NOT `1-probe-plans/`, NOT a per-stage `_PROBE/` folder. Both are RETIRED.
- Stage affinity is a SECTION's `serves:` field, never the file's path. One flat cross-stage pool.
- PP numbers are **application-local footnote numbers**. `ls 1-probes/` is the numbering
  authority. There is no ledger, and no PP id ever crosses to the task/discovery bank — so an
  application and a paper may both carry a PP03 with nothing to reconcile.
- **Legacy migration (on first touch):** a file found in `1-probe-plans/` or
  `0-lifecycle/<stage>/_PROBE/` is rewritten into `1-probes/` in the new shape by whatever verb
  touched it. Log the move in the stage `_LOG`. Do not migrate what you did not touch.

Probe file anatomy
-------------------

Full spec: the constitution's "The probe file" section. In brief — one `## Why` per FILE, one SECTION per question:

```markdown
# PP01 — refill timing feasibility
- mode: light | full

## Why
The stake, in intervention vocabulary (which claims die, and how).
NEVER dispatched. NEVER copied anywhere. It does not leave this file.

## Q1 — refill window observability
- serves: 1-claims (C2)
- target: tasks/A03_refill_window_scan/01_column_scan/QA/1-refill-window.md
- state:  read
- commission: |
    The question in GENERAL language — no claim ids, no stake, no hint of which
    answer is wanted. This is the DISPATCH PAYLOAD, and nothing else is. FROZEN.
- reading: |
    What the answer MEANS for this intervention. Written at harvest.

- values: … · sources: … · displays: …     the harvest lanes
```

⛔ No markdown tables in a probe file. It holds SECTIONS. The words "card", "row" and "table"
are not part of this vocabulary.

**BUILD-lane fields** — present ONLY at `state: commissioned`, on work that takes days to weeks:
`owner:` · `eta: YYYY-MM-DD` · `blocks:` · `cross-project: <sibling path | none-found>`.
A future `eta` PASSES the gate; an `eta` that has passed with no answer is a HARD FAIL.

States (DERIVED from disk — never asserted)
--------------------------------------------

```
planned          the section exists · the target leaf is missing (or `NEW …`)
commissioned     the task-folder + its plan.yaml exist · the QA file is absent
answered         the target QA FILE exists
read             the section's reading: is non-empty (+ 1-claims.md flipped, if it serves a claim)
answered-local   target points into the intervention's OWN registries; no dispatch happened
failed           a reading with a dead target · the task-folder was deleted · the qa verb REFUSEd
```

💀 `verdicted` is DELETED. 💀 `dispatched` is DELETED (say `commissioned`).
A claim's STATUS (`supported | refuted | inconclusive` + confidence + claim_type)
lives in `0-lifecycle/1-claims/1-claims.md`. It is not a probe field. There is no `## Verdict`.

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
with no digest, it does not write the digest: it DISPATCHES a digest-only run. An
intervention session that writes in the bank has broken LAW 1, whatever it ends up writing.

Commands
---------

```
/haipipe-application probe "<question>"   raise a question -> a SECTION in the right topic's
                                          probe file (creating the file if the topic is new)
/haipipe-application probe                show the board (derived from 1-probes/, never stored)
/haipipe-application probe run            run the five-step loop over every open section
/haipipe-application probe run PP01       run it for one probe file
```

All four go through `haipipe-application-probe` (the PROBE phase worker) — the single door.

The loop (owned by haipipe-application-probe)
-----------------------------------------------

```
DRAFT raises the questions
  ① ORGANIZE   collect them into 1-probes/, grouped by topic; write each commission (T1)
  ② MATCH      T0 JOIN · T1 LOCAL · T2 REUSE (grep the bank's QA corpus, and READ the hits)
               → most sections should stop HERE. A commission is the EXCEPTION.
  ③ DISPATCH   T3/T4 only: the commission block, VERBATIM, to
                 Agent(haipipe-task-orchestrator-agent)
                 Agent(haipipe-discovery-orchestrator-agent)
               their clean context IS the wall. 💀 the probe gateway agent is RETIRED.
  ④ POINT      target: → the answering QA FILE (verify with ls)
  ⑤ INTERPRET  reading: → the claims ledger flips → the harvest lanes pay out
```

Relation to the direct task/discover verbs
--------------------------------------------

`task` and `discover` remain direct verbs for non-claim utility work. And a question with no
intervention behind it does not need a probe file at all — hand it straight to the executor's
own door:

```
/haipipe-task qa "<question>"        the everyday "go explore this" verb; the QA file is the receipt
/haipipe-discovery qa "<question>"   same, for external evidence
```

If that answer later matters to the intervention, open a section whose `target:` points at the
already-written QA file. That is a T2 REUSE — nothing re-runs.
