---
name: haipipe-probe
description: >-
  The shared evidence-acquisition router for a consumer Page. Probe first types
  the source: existing accepted Pages go through its PageX lane, while Task or
  Discovery questions go through its QA lane with stake stripping,
  MATCH-before-DISPATCH, and exact-path answer binding. It owns the COST LADDER
  (T0 JOIN · T1 LOCAL · T2 REUSE · T3 ENRICH · T4 FRESH — only T3/T4 summon an
  agent, and most questions should land on T2) and the ENRICH DEPTH ladder the
  executor picks from without the probe ever learning which rung ran. A missing
  task folder is T4, never a refusal. Consumer plugins own the two local
  surfaces. Trigger: probe, PageX, existing Page evidence, Task evidence,
  Discovery evidence, Q-consumer, Q-executor, QA bank, QA file, match before
  dispatch, A-executor, cost ladder, cheap probe, token tax, no task folder,
  T2 reuse, enrich depth, /haipipe-probe.
allowed-tools: Bash, Read, Grep, Glob, Agent, Skill
metadata:
  version: "0.18.0"
  last_updated: "2026-08-21"
  summary: "R13 the cost ladder and R15 the enrich depth are back: five gears instead of one, and \"no task folder\" stops being a HOLD."
---

# /haipipe-probe · choose the PageX or QA evidence lane

Probe is the Page's one evidence-acquisition family. It routes by source before
doing any work; it is not a storage layout and not a Paper stage.

```text
Probe
├── source: page            ── PageX ─────▶ scoped accepted-Page binding
└── source: task|discovery  ── QA Probe ─▶ bank-owned QA file
```

PageX now sits inside the Probe family, but it remains a separate lane with a
different phase and durable surface. OUTLINE uses PageX to rank and bind exact
accepted Page files. The PROBE and EVIDENCE phases use QA Probe only for Task or
Discovery. Neither lane falls through to the other: a mistaken source type
returns to OUTLINE for correction.

## 🔀 Source router

Choose the lane from the source, not from convenience:

| Source | Lane | Phase | Durable record |
|---|---|---|---|
| accepted Board Page | PageX | OUTLINE | `pagex/<stem>.md` + exact-file links |
| Task folder | QA Probe | PROBE → EVIDENCE | `probe/PP<NN>-<slug>/` → Task `QA/` |
| Discovery folder | QA Probe | PROBE → EVIDENCE | `probe/PP<NN>-<slug>/` → Discovery `QA/` |

PageX does not create a mirror QA card for evidence already accepted by its
source Page. QA Probe does not search Pages or treat topic similarity as a bank
answer.

## 🧱 The QA wall

One exchange has four named forms:

```text
                 CONSUMER SIDE                    EXECUTOR SIDE
QUESTION         Q-consumer      ── strip stake ─▶ Q-executor
ANSWER           A-consumer      ◀─ interpret ─── A-executor
```

- `Q-consumer` states what this Page needs, why it matters, and what breaks.
- `Q-executor` is neutral and answerable without seeing the Page. It is the only
  question that may cross into a bank.
- `A-executor` is the bank's answer, preserved verbatim and bound by path.
- `A-consumer` is the Page-specific interpretation stored behind the wall at
  `consumer/a-consumer.md`. DRAFT may later turn an accepted interpretation
  into Page prose; the bank does not own it.

Stake includes Page ids, claim ids, desired conclusions, venue pressure, and
phrases such as “our paper” or “we need to show.” It may appear in Q-consumer,
but never in Q-executor, A-executor, a dispatch payload, or a bank QA file.

## 🗂 Ownership

The consumer owns its local record. The PageX lane loads
`board/page-plugins/haipipe-plugin-pagex`. The QA lane loads
`board/page-plugins/haipipe-plugin-probe`; it stores one question at:

```text
<page>/probe/PP<NN>-<slug>/
├── card.md
├── consumer/q-consumer.md
├── consumer/a-consumer.md
├── executor/q-executor.md
├── executor/a-executor.md
└── proof/
```

The bank owns the answering QA file:

```text
<task-folder>/QA/<n>-<slug>.md
<discovery-folder>/QA/<n>-<slug>.md
```

Never create `1-probes/`, an evidence Page, an S03/S04 Paper stage, or a second
consumer-side QA schema. This protocol points to the bank artifact; it does not
copy authority away from it.

## 💰 The cost ladder · cheap doors first, and only T3/T4 summon an agent

**R13, ruled 260714** (`diagram/260714-probe-qa/` v3, R1-R18, approved by JL) and
**restored here 260821**: it was dropped from this file in the 260819 phase-agent
split and survived only in the CHANGELOG, so for two days the crossing had ONE
gear — every question, however small, paid a full executor lifecycle, and a
question with no task folder had nowhere to go but HOLD.

```text
   T0 JOIN    another Q-executor already asks this   → add a Q-consumer bullet  ~0
   T1 LOCAL   my own registries answer it            → answered-local           ~0
   T2 REUSE   an existing QA file answers it         → point the entry   1 grep + 1 read
   T3 ENRICH  the task-folder exists, never asked this → new entry → ③        agent
   T4 FRESH   no task-folder                          → new entry → ③        agent
```

**T0, T1 and T2 never summon an agent.** They are a read, a grep and a bind. The
tier is chosen at ② MATCH, by READING — never guessed from the question's shape.

**CC-7 · MOST entries should land on T2.** In a healthy project the bank fills on
its own, so most answers already exist before anyone asks. A commission is the
EXCEPTION, not the norm, and a page whose every card is T3/T4 is a smell with two
possible causes: a lazy MATCH, or a starving bank. Read it as a signal about the
PROJECT, not about the question.

**The tier and the `bank:` verdict are the same judgment, named twice.** The
consumer plugin's four verdict words map onto the ladder exactly, so nothing new
is stored and no field changes:

```text
  tier        bank:     what MATCH found
  ──────────────────────────────────────────────────────────────────────
  T0 JOIN     —         another card on this page already asks it
  T1 LOCAL    —         our own registries answer it → state: answered-local
  T2 REUSE    reuse     a results folder already answers it
  T3 ENRICH   run       folder + code exist, needs a run
  T3 ENRICH   code      folder exists, code needs a change first
  T4 FRESH    new       nothing exists, create a folder
```

⚠️ **`run` / `code` / `new` are the DISPATCH DECISION, not a work plan.** They say
whether to cross at all and through which door. HOW DEEP the executor then goes is
R15's, below, and this side never learns it — the three words are a consumer-side
prediction wearing executor vocabulary, which is a naming debt, not a licence to
direct the bank's internals.

## 🔁 Five-step crossing

```text
① ORGANIZE   write Q-consumer; strip it to one neutral Q-executor
② MATCH      ask the chosen bank in --check-only mode; read candidate QA files
③ DISPATCH   only when MATCH finds no literal answer or active matching question
④ POINT      bind the exact returned QA path and preserve A-executor verbatim
⑤ INTERPRET  state what that answer means for this consumer, with its limits
```

Page lifecycle ownership is split deliberately:

```text
PROBE phase       ① ORGANIZE · ② MATCH · ③ DISPATCH
EVIDENCE phase    ④ POINT · ⑤ INTERPRET · bind proof and values
```

### ① ORGANIZE

Write the stake-bearing question locally, then make Q-executor independently
answerable. A good Q-executor names the population, variable, comparison,
method, and requested output when those are needed. It does not name the answer
the consumer hopes to receive.

Choose one QA route after the source router has ruled out an accepted Page:

- `task` for computed, measured, run-bound, or repository-local facts;
- `discovery` for literature, prior art, external facts, or novelty questions;
- `none` when neither bank can answer IN PRINCIPLE — a question about the
  future, a value judgment, a fact nobody holds. `none` is a concern, not
  permission to invent a third route.

⚠️ **`none` is not "there is no task folder yet".** That is T4 FRESH, it dispatches
normally, and the executor opens the leaf at d3 (§💰, §③). Reaching for `none`
because the bank looks empty is the commonest way a page stalls on a question that
was perfectly answerable: it turns a MISSING ANSWER into a REFUSED QUESTION, and
only the second one is terminal.

### ② MATCH before DISPATCH

Call the selected bank's QA verb with `--check-only` first:

```text
/haipipe-task qa "<Q-executor>" [<task-folder>] --check-only
/haipipe-discovery qa "<Q-executor>" [<discovery-folder>] --check-only
```

Read a candidate's state line before its answer. Reuse only when the QA file
literally answers this question. Topic similarity is not an answer.

**MATCH's output is a TIER** (§💰), and the tier decides whether ③ runs at all:

```text
  T0 · T1 · T2   ⇒ DO NOT DISPATCH. Bind, or answer locally, and stop.
  T3 · T4        ⇒ ③ DISPATCH, through the one door.
```

```text
answered              bind that path
working, live          bind/report that path; dispatch nothing
superseded-by          follow to the live QA file
near miss or no hit    proceed to DISPATCH
```

### ③ DISPATCH

**ONE DOOR, and it is an agent.** Hand the batch of still-collecting Q-executors
to `haipipe-probe-q-executor-agent`, which runs ② MATCH, ③ DISPATCH and ④ POINT
in an isolated context and returns the answered QA paths. A consumer-side worker
— paper stage, application stage, or Board Page phase producer — never calls
`haipipe-task-orchestrator-agent` or `haipipe-discovery-orchestrator-agent`
itself (JL 260820: 永远只有 haipipe-probe-q-executor-agent 才能够做这件事).

⚠️ Ruled 260820 and recorded in this file's CHANGELOG 0.14.0, but this step went
on describing a direct call to the bank verb until 260821. The verb form below
is what the COLLECTOR runs; it is not an instruction to the consumer.

The collector dispatches only Q-executor, through the bank verb without
`--check-only`. The bank chooses whether to digest existing outputs, execute a
run, enrich a discovery, or create a correctly scoped folder. Those choices
belong to the Task/Discovery contract, not to Probe.

**R15 · THE ENRICH DEPTH LADDER, and the probe never learns which rung ran.**
Restored 260821 with R13; it answers JL's "what does a new question mean to a task
folder?"

```text
  d0 READ        the results are already there; write the QA digest
  d1 NEW RUN     the script exists; a new config answers it
  d2 NEW SCRIPT  this leaf's plan.yaml IPO still covers it
  d3 NEW LEAF    it does not fit that IPO; create a correctly scoped folder
```

The EXECUTOR picks the SHALLOWEST depth that answers the question. The scope test
between d2 and d3 is one question — *does it fit THIS leaf's `plan.yaml` IPO?* —
and it is asked on the executor's side, where the IPO lives.

```text
  ✅ ACCRETES   QA files · configs · runs · scripts · leaves
  🔒 FROZEN     past results/ · existing QA files · the dispatched question
```

⚠️ **"There is no task for this" is NOT a reason to stop.** It is T4 FRESH on the
consumer side and d3 NEW LEAF on the executor's, and neither is this file's call
to make. The probe hands a question and gets back a path. A consumer that inspects
the bank deeply enough to conclude "no task exists, therefore HOLD" has done the
executor's triage with the stake in context, which is the wall failing quietly.

The return is a QA path or an explicit refusal/re-route. A refusal is complete
evidence about scope; record it rather than manufacturing an answer.

### ④ POINT

Bind the exact QA file path. Do not bind a folder, prose description, latest
glob, or copied answer without provenance. Preserve the bank answer verbatim in
the consumer record and pull only small aggregate proof files allowed by the
consumer plugin.

The bank remains authoritative. If a pulled proof and the bank disagree, mark
the consumer copy stale and re-bind.

### ⑤ INTERPRET

Write one A-consumer for each Q-consumer served in
`consumer/a-consumer.md`. State:

- the answer relevant to the consumer;
- the exact source path and any run/version;
- what the evidence does not establish;
- whether it changes the approved outline.

Interpretation may carry stake because it has returned behind the wall. It is
evidence metadata, not Page prose: EVIDENCE returns it to OUTLINE, a person
accepts it with `read:`, and later DRAFT/REVISE owns the sentence.

## 🧮 Values and proof

When one answer contains several usable values, the consumer plugin allocates
`PP<NN>.v<n>` ids in `card.md`. Each value names the exact file and field in
`proof/`; a naked number is not a value binding. Proof is aggregate-only.
Never pull row-level or PHI data into a Page.

`proof/manifest.yaml` has ONE exact shape, checked by
`page-plugins/haipipe-plugin-probe/ref/check-probe.py` — not a paraphrase of
it, the literal field names, every one required, no invented alternative
(`source_qa`/`quoted_from`/`size_bytes` are NOT this shape and fail the check):

```yaml
card: PP<NN>-<slug>
files:
  - name: <the pulled file's own name>
    kind: table | numbers | excerpt
    source: <path to the aggregate file this was pulled from>
    run: <the run/script that produced it>
    pulled: <date>
    bytes: <size>
    sha256: <hash>
    why: >-
      <why THIS file pins the answer, not a restatement of the question>
    aggregate: true
```

`aggregate: true` is not decoration: it is the PHI-safety assertion the
checker exists to enforce (only aggregated, PHI-free files may be committed
to a Page). A manifest missing it is a compliance gap, not a formatting one.

## ✅ Completion and human gate

Machine completion and consumer acceptance are distinct:

```text
answered   QA path resolves · A-executor is non-empty · proof is present or
           explicitly unnecessary
read       a person read the answer and accepted its consumer interpretation
```

Only a person marks `read`. Changing `target:` or replacing proof drops the
read gate. One Q-executor may serve many Q-consumers; ask once and cite it by id.

## 🧾 Return contract

Return a compact crossing receipt:

```text
lane:        pagex | qa-probe
route:       page | task | discovery | none
tier:        T0 JOIN | T1 LOCAL | T2 REUSE | T3 ENRICH | T4 FRESH   (§💰)
match:       reuse | working | dispatched | refused
question:    path to Q-executor
target:      exact bank QA path, when one exists
state:       planned | commissioned | answered | answered-local | read |
             deferred | failed | concern
             ⚠️ ALL EIGHT. `answered-local` (answered from the consumer's own
             registries, no bank run) was missing here until 260821 while
             haipipe-plugin-probe, ref/check-probe.py and live/plugview.py all
             carried it — and the plugin cites THIS file as the vocabulary's
             source, so the list it pointed at was short by one.
proof:       manifest path or why no proof exists
serves:      consumer outline addresses
limits:      what remains unresolved
next:        EVIDENCE | PROBE | OUTLINE | HOLD
```

For `lane: pagex`, return the exact source file, bounded scope, accepted source
version, and local PageX record instead of QA fields.

No Paper-specific runtime file is part of this contract. Paper, Application,
and any future consumer use the same source router; only their local records
differ.
