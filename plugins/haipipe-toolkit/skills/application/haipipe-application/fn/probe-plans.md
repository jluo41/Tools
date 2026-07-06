Probe Plans Buffer (application)
=================================

The intervention accumulates evidence needs as **probe plans** during lifecycle work (seed, claims, display, section-edit). Instead of dispatching each probe immediately (which interrupts story work), stages buffer them and dispatch in batch when the user is ready. Mirror of `../../../paper/haipipe-paper/fn/probe-plans.md` — same card anatomy, same statuses, application paths.

Location
--------

Plans LIVE in the `_PROBE/` subfolder of the stage that spawned them (stage self-containment). `1-probe-plans/README.md` is a thin cross-stage INDEX only -- one row per plan, no plan bodies.

```
<intervention>/
├── 0-lifecycle/
│   ├── 0-seed/_PROBE/PP01_<slug>.md          plans live with their stage
│   ├── 1-claims/_PROBE/PP02_<slug>.md
│   └── 5-section-edit/{section}/_PROBE/...
└── 1-probe-plans/
    └── README.md              INDEX: | id | stage | status | refs | -- created on first plan
```

PP numbering is intervention-global (PP01, PP02, ... in creation order across stages); the index is the numbering authority.

**Legacy layout migration (on first touch):** a plan file found FLAT in `1-probe-plans/PPNN_*.md` (the pre-alignment layout) moves into the `_PROBE/` folder of its source stage (from frontmatter, or infer from content) + gets an index row. Migrate as part of whatever verb touched the file; log the move in the stage `_LOG`.

Probe Plan Card Format
-----------------------

```markdown
---
id: PP01
status: planned | dispatched | read | verdicted
mode: light | full
claim: "<the claim this probe tests, or the orientation question>"
source_stage: "<lifecycle stage that surfaced this need, e.g. 1-claims>"
source_ref: "<C<n> row or NEED label>"
created: YYYY-MM-DD
dispatched_at: ""
refs: ""
verdict: ""
---

## Need

<One sentence: what the intervention claims or needs to know.>

## Why

<Which claim / element / section this serves; what "done" looks like.>

## Route

<Expected evidence workers the gateway will likely call:>
- task: <what analysis to run, if any>
- discover: <what literature/benchmark to find, if any>

## Takeaways            ← written at TRANSLATE (light: <=5 anchored lines)

## Verdict              ← full mode only, landed at TRANSLATE
```

Statuses
--------

```
planned     filed during lifecycle work; not yet dispatched
dispatched  handed to the gateway agent (bg for fresh work)
read        light return arrived; anchored takeaways landed in this card
            (refs: = the execution artifacts — discoveries/.../sources.md, tasks/...)
verdicted   full return arrived; ## Verdict carries G1/G2/G3 + supported|refuted|inconclusive;
            the claims ledger's C-section flipped in the same TRANSLATE
```

The card is the need's WHOLE application-side lifecycle in one place: need -> dispatch record -> takeaways -> verdict. Execution artifacts stay project-side (discoveries/, tasks/), multi-consumer reusable.

Commands
--------

```
/haipipe-application probe "<claim or need>"   add a probe card to the active stage's _PROBE/
/haipipe-application probe                     show the buffer (from the index)
/haipipe-application probe run                 batch dispatch all planned cards
/haipipe-application probe run PP01            dispatch one specific card
```

Dispatch (always via haipipe-application-probe, the single dispatch point)
--------------------------------------------------------------------------

1. Resolve the project root from the intervention path.
2. For each planned card: dispatch `Agent(haipipe-probe-orchestrator-agent)` -- ALWAYS, no matter how small the need. The agent's SWEEP decides the shape in clean context (reused | enriched | fresh); the application side never sweeps the project or reads its evidence inline.
3. Update the card: status -> dispatched; index row follows.
4. Light returns at TRANSLATE: takeaways (<=5 anchored lines) land in the card (status -> read).
5. Full returns: the verdict block lands in the card's `## Verdict` (status -> verdicted) and the claims ledger flips in the same pass.

Relation to Direct task/discover Verbs
---------------------------------------

`task` and `discover` remain direct verbs for non-claim work ("just pull the click rates", "find benchmark papers"). For anything tied to an intervention claim or evidence need, the probe buffer is the right path: it preserves the claim-evidence chain and makes the evidence backlog visible and batchable.

```
claim-related evidence need  ->  /haipipe-application probe "..."  ->  buffer -> batch dispatch
non-claim utility work       ->  /haipipe-application task "..."   ->  direct dispatch
                             ->  /haipipe-application discover "..."
```
