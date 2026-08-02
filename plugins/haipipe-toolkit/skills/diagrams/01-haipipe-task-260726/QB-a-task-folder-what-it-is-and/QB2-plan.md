# PLAN: what must be fixed before any code exists
state: 🔴 OPEN
owner: JL
method: write the IPO contract, and let the reviewer judge the contract rather than the intention

## Opening
What does PLAN have to settle so that BUILD has nothing left to invent? It writes one thing, `workflow/plan.yaml`, in the IPO shape: what goes in, what happens, what comes out. Everything after it is judged against that file, so a vague plan does not fail here, it fails at Report, where the cost of being wrong is a run that already burned.

The difficulty is that a plan is judged before anything can be tested. A reviewer at this phase has no code and no numbers, only a description of both, so the only thing it can catch is a contract that is incomplete or internally inconsistent. That is a narrower job than it sounds and it needs saying, because a reviewer that tries to judge whether the plan is a good idea is doing the researcher's job with less information.

What is unresolved is what "complete" means for an IPO block. The schema exists. Whether an output declared as `metrics.json` with no keys named is complete, or whether a plan must name the actual fields it will produce, decides whether Report can be checked mechanically at all.

**Covered elsewhere**: The IPO schema itself is `haipipe-workflow`'s; the reviewer pairing is `QB6`; what Report checks the plan against is `QB5`; the run naming that a plan's outputs must respect is `QC1`.

## Diagram
```
   PLAN                                    writes workflow/plan.yaml
                                            and plan-script-<name>.yaml

    creator drafts ────▶ reviewer checks IPO compliance ────▶ ↺
                              │
                              ▼
                    pass / warn / revise / fail

   ── what a reviewer HERE can actually judge ────────────────
      ✅ is every Input named, and does it exist or have an owner?
      ✅ does every Output have a name and a home?
      ✅ do the Steps consume the Inputs and produce the Outputs?
      ✅ is the run name legal, and does it match what QC1 requires?
      ────────────────────────────────────────────────────────
      ✗ is this a good experiment?        the researcher's call
      ✗ will it work?                     nothing here can know
      ✗ are these the right metrics?      a claim about the world

      a reviewer that reaches past the line is guessing with less
      context than the person who wrote the plan.

   ── the unresolved question ────────────────────────────
      output: results/<run>/metrics.json          complete?
      output: results/<run>/metrics.json
              keys: [mae, rmse, n]                complete.

      only the second can be MECHANICALLY checked at Report.
      Requiring it costs the author real effort at the phase
      where they know the least.                    → Items
```

## Content
### PLAN's product is a contract, and its reader is Report
`workflow/plan.yaml` is not documentation. It is the thing Report is measured against, which is
what makes the IPO shape at both ends worth the ceremony: the same structure holds intent and
evidence, so the comparison is mechanical rather than a reading.

That is also why the reviewer's job here is narrow. It is not asked whether the plan is wise, it
is asked whether the plan is a contract at all.

### File ownership at this phase is one line and it is absolute
PLAN touches only `workflow/plan*.yaml`. Not the code, not the configs, not a run script.

The reason is not tidiness. If PLAN could write a config, the contract and its implementation
would have one author and Gate 1 would have nothing independent to compare.

### Where the phase currently is
21 of 107 task-folders have a `workflow/` at all, so four fifths of the bank was built without a
plan file. That is not necessarily wrong, since most of those predate the phase, but it does mean
the contract-versus-evidence comparison has never been exercised at scale.

## Aims
- [ ] 📐 Rule what makes an IPO block complete
      Whether an output must name its keys, or whether a filename is enough. This decides if `QB5` can check Report mechanically or only by reading.
- [ ] ✂️ State the reviewer's boundary at this phase
      It judges the contract, not the idea. Written nowhere; a reviewer that drifts past it produces confident objections about research it cannot see.
- [ ] 📈 Decide whether the 86 planless folders matter
      21 of 107 have `workflow/`. Either the rest are legacy and exempt, or the phase is not actually mandatory, and the docs currently imply the second while reading like the first.

## States
The phase runs, the schema exists, and the completeness question is untouched. Nothing here has
been ruled.

- 260726 CC · 📏 Counted the adoption
      21 of 107 task-folders carry a `workflow/`. Written from `SKILL.md` and `fn/stage-plan.md`.

## Files
- `fn/stage-plan.md`
  The phase contract: what it reads, what it writes.
- `task-lifecycle.workflow.js`
  The creator/reviewer loop this phase runs inside.

## Log
260726 · Created with the board.
