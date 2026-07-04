Probe Plans Buffer
==================

The paper accumulates evidence needs as **probe plans** during lifecycle work
(seed, pitch, claims, etc.). Instead of dispatching each probe immediately
(which interrupts story work), the paper buffers them and dispatches in batch
when the user is ready.

Location
--------

Plans LIVE in the `_PROBE/` subfolder of the stage that spawned them (stage self-containment, JL 2026-06-29 ruling). `1-probe-plans/README.md` is a thin cross-stage INDEX only -- one row per plan, no plan bodies.

```
<paper>/
├── 0-lifecycle/
│   ├── 0-seed/_PROBE/PP01_<slug>.md          plans live with their stage
│   ├── 1-claims/_PROBE/PP02_<slug>.md
│   └── 5-section-edit/{section}/_PROBE/...
└── 1-probe-plans/
    └── README.md              INDEX: | id | stage | status | probe_ref | -- created on first plan
```

PP numbering is paper-global (PP01, PP02, ... in creation order across stages); the index is the numbering authority.

**Legacy layout migration (on first touch):** a plan file found FLAT in `1-probe-plans/PPNN_*.md` moves into the `_PROBE/` folder of its `source_stage` (from frontmatter, or infer from content) + gets an index row. A legacy `_DISCOVERY_{stage}.md` next to a stage artifact folds into the owning plan file (takeaways -> plan `## Takeaways`; candidate papers -> `_CITATION_{stage}.md` via citation harvest) and is then deleted. Migrate as part of whatever verb touched the file; log the move in the stage `_LOG`.

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
dispatched  sent through haipipe-paper-probe; probe_ref points to the active probe
read        light probe finished Read; takeaways backfilled into this plan file
verdicted   full probe returned a verdict; paper can backfill into 1-claims
```

The plan file is the need's WHOLE paper-side lifecycle in one place: need -> dispatch record (probe_ref) -> takeaways (<=5 lines, written back after Read). There is no separate `_DISCOVERY_` takeaways file (retired 2026-07-04).

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

When `/haipipe-paper probe run` dispatches (always via haipipe-paper-probe, the single dispatch point):
1. Resolve the project root from the paper path
2. For each planned probe: sweep reuse-before-create, then dispatch via Agent(haipipe-probe-orchestrator-agent) by default (clean context); a tiny single lookup may inline Skill("haipipe-probe")
3. Update the probe plan file: status -> dispatched, probe_ref -> the active probe path; update the index row
4. Light probes return at Read: takeaways (<=5 lines) backfill into the plan file (status -> read); when the Read output carries literature sources, haipipe-paper-probe-citation HARVESTs them into _CITATION_{stage}.md
5. Full probes deposit a verdict: the paper backfills into 1-claims and sections (status -> verdicted)

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
