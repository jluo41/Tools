Probe Plans Buffer
==================

The paper accumulates evidence needs as **probe plans** during lifecycle work
(seed, pitch, claims, etc.). Instead of dispatching each probe immediately
(which interrupts story work), the paper buffers them and dispatches in batch
when the user is ready.

Location
--------

```
<paper>/
└── 1-probe-plans/
    ├── README.md              index + dispatch status
    ├── PP01_<slug>.md         one file per planned probe
    ├── PP02_<slug>.md
    └── ...
```

Probe Plan File Format
-----------------------

```markdown
---
id: PP01
status: planned | dispatched | verdicted
claim: "<the claim this probe tests>"
source_stage: "<lifecycle stage that surfaced this need, e.g. 0-seed, 1-pitch>"
source_ref: "<NEED-N label or claim row from 2-claims>"
created: YYYY-MM-DD
dispatched_at: ""
probe_ref: ""
verdict: ""
---

## Claim Under Test

<One sentence: what the paper claims or needs to verify.>

## Evidence Needed

<What the probe must produce: a verdict, a robustness check, a comparison,
a literature finding. Be specific about what "done" looks like.>

## Expected Route

<Which evidence workers the probe will likely call:>
- task: <what analysis to run, if any>
- discover: <what literature/context to find, if any>

## Constraints

<Scope limits, data availability, timeline notes.>
```

Statuses
--------

```
planned     filed during lifecycle work; not yet dispatched
dispatched  sent to /haipipe-probe; probe_ref points to the active probe
verdicted   probe returned a verdict; paper can backfill into 2-claims
```

Commands
--------

```
/haipipe-paper probe "<claim or need>"     add a probe plan to the buffer
/haipipe-paper probe                       show the buffer (planned/dispatched/verdicted)
/haipipe-paper probe run                   batch dispatch all planned probes to /haipipe-probe
/haipipe-paper probe run PP01              dispatch one specific probe plan
```

Lifecycle Integration
----------------------

Any lifecycle stage can surface a probe plan:
- 0-seed: "NEED-1 (probe): expand ex ante audit" -> PP01
- 1-pitch: "Still Fragile: no CATE baseline" -> PP02
- 2-claims: GAP row -> PP03

The probe plan captures the need immediately; dispatch waits for user readiness.

When `/haipipe-paper probe run` dispatches:
1. Resolve the project root from the paper path
2. For each planned probe, call Skill("haipipe-probe", args="plan from-paper <paper_root> <probe_plan_content>")
3. Update the probe plan file: status -> dispatched, probe_ref -> the active probe path
4. When the probe deposits a verdict, the paper backfills into 2-claims and sections

Relation to Direct task/discover Verbs
---------------------------------------

The paper still accepts `task` and `discover` as direct verbs for non-claim
work (e.g., "just run this pipeline" or "find me background papers"). But for
anything tied to a paper claim or evidence need, the probe buffer is the right
path: it preserves the claim-evidence chain and makes the evidence backlog
visible and batchable.

```
claim-related evidence need  ->  /haipipe-paper probe "..."  ->  buffer -> batch dispatch
non-claim utility work       ->  /haipipe-paper task "..."   ->  direct dispatch
                             ->  /haipipe-paper discover "..."
```
