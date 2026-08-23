# 3-deliver : compose the artifact, then audit & ship it

Everything downstream of the argument. `1-lifecycle` decides what the intervention says and `2-phase` writes each stage; this group turns that settled lifecycle into a **composed artifact** and gets it **channel-ready**. Named to match `paper/3-deliver/`, but kept FLAT — application delivers markdown/channel artifacts (SMS, email, dashboard), not a LaTeX manuscript, so it has no `scaffold / compile / typeset` machinery to sub-phase.

## Shape of this group

```text
3-deliver/
├── README.md                          ← you are here
│
├── haipipe-application-artifact       COMPOSE: build 0-artifacts/<slug>-v{N}.md from the pinned
│                                       venue profile + the required lifecycle stages, through a DPRC pass
├── haipipe-application-claim-audit    AUDIT: every artifact claim traces to an adopted A entry
│                                       (artifact -> adopted A -> C -> anchor); no claim outruns its evidence
├── haipipe-application-review         AUDIT: audience fit, tone/length compliance, claim traceability
└── haipipe-application-deploy         SHIP: package + deliver through the channel (SMS/dashboard/email) — STUB
```

## The intent gradient

The four skills group by verb-intent — the same gradient as `paper/3-deliver` (build → audit → polish → ship), collapsed to what a markdown/channel deliverable needs:

```text
COMPOSE   artifact         makes the deliverable (venue profile IS the instruction set; one skill, all venues)
   ↓
AUDIT     claim-audit      read-only, produce findings — never mutate the artifact
          review
   ↓
SHIP      deploy           produce & move the artifact to its channel
```

`claim-audit` and `review` only REPORT (they never rewrite the artifact — wording fixes route back to the owning lifecycle stage). `deploy` produces and moves; it does not judge.

## Why flat (not sub-phased like paper)

`paper/3-deliver` splits into `1-build / 2-audit / 3-polish / 4-ship` because a LaTeX manuscript needs a folder scaffolded, tex compiled, typesetting polished, and a PDF shipped. An intervention artifact is markdown composed straight from the lifecycle — there is no build or polish sub-stage to fill. So application adopts paper's `3-deliver` name and its verb-intent, not its LaTeX sub-phasing. If a future venue ever needs a real build/polish pipeline, revisit and split then.

## Relationship to neighbors

| Need | Go to |
|------|-------|
| Decide story, claims, venue | `1-lifecycle` (then come back here) |
| Compose the deliverable | `haipipe-application-artifact` (the `draft` verb) |
| Do the artifact's claims trace to evidence? | `haipipe-application-claim-audit` |
| Audience fit / tone / length / compliance | `haipipe-application-review` |
| Ship to the channel | `haipipe-application-deploy` |
| Post-deploy A/B refinement | `4-iterate/` |
