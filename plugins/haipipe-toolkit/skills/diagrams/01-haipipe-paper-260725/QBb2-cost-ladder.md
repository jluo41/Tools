# What may a stage spend without asking?
state: 🟡 PARTIAL
owner: JL
method: keep the ceiling per stage; keep the default at zero

## Question
How much work may a stage commission on its own, and what forces it to stop and ask? Every stage declares a spending ceiling and the default is zero. That single number is what makes an unattended run safe rather than merely convenient.

Every stage declares `probe_depth`, a ceiling on what its PROBE phase may dispatch. The default is 0, which means PROBE may only harvest answers that already exist. That single number is what makes the unattended phases safe: a phase that cannot spend does not need a human in front of it.


The approach is a declared ceiling per stage, defaulting to zero, so an unattended phase can harvest what already exists and can never commission work. What we want is a lifecycle that is safe to run without a human watching, which is only true if the expensive actions are structurally out of reach.
## Boundary
- ✅ Covered here
  The ladder, the per-stage ceiling, and what raising it means.
- ↪ Covered elsewhere
  The gate that the ceiling makes safe is `QB3`; the loop the ceiling governs is `QBb1`.

## Diagram
```
 ONE NUMBER IS WHAT MAKES THREE UNATTENDED PHASES SAFE

   probe_depth:  the ceiling on what PROBE may dispatch

   0  READ        reuse an answer that exists      free, nothing runs   ◄ DEFAULT
   1  NEW RUN     old script, new config           costs
   2  NEW SCRIPT  must write new code              costs more
   3  NEW FOLDER  open a new task folder           costs most

   depth ≤ ceiling  ──►  DISPATCH
   depth >  ceiling  ──►  DEFER, with a forward pointer recorded
                          never a silent drop

 THE ARGUMENT IN ONE LINE
   a phase that cannot SPEND does not need a human in front of it.
   That is the only reason DRAFT · PROBE · REVISE run unattended and
   the human is spent once, at CHECK  (QB3).
   Raise the ceiling and you have re-opened three gates.

 WHAT DEFERRAL COSTS, AND WHY IT IS STILL RIGHT
   a deferred question leaves a placeholder in the prose and an open
   item on the page.  That is VISIBLE DEBT, which is the point:
     visible debt   ⏸ parked  ── a human decides whether to spend
     the alternative           ── an agent quietly deciding a paper's
                                  evidence budget
   Live on MISQ: 11 parked values, each naming the depth that would
   release it.
```

## Content
### The ladder
```
 0  READ        reuse an answer that already exists   free, nothing runs
 1  NEW RUN     old script, new config                costs
 2  NEW SCRIPT  must write new code                   costs more
 3  NEW FOLDER  open a new task folder                costs most
```
A question is dispatched when its depth is at or below the stage's ceiling, and DEFERRED otherwise, with a forward pointer recorded rather than a silent drop.

### Why the default is zero
It makes the design's central promise true: DRAFT, PROBE and REVISE run unattended, and the human is spent once, at CHECK. That only holds if none of those phases can commit compute, money or PHI access on their own.

### What deferral costs, and why it is still right
A deferred question leaves a placeholder in the prose and an open item on the page. That is visible debt, which is the point: the alternative is an agent quietly deciding a paper's evidence budget.

## Items to Finish
- [x] 🪜 The ladder exists and is per stage
      `probe_depth:` in every contract, defaulting to 0.
- [ ] 📐 State who may raise it, and how the raise is recorded
      A raise is a spending decision. It should be as visible as a gate, and today it is a command-line flag.
- [ ] 🧠 Rule whether a stage may ever default above 0
      If any stage should, say which and why; if none should, say that, so the field cannot drift upward one paper at a time.

## Where we are
Implemented and honoured. On the MISQ paper the two venue questions sit deferred at depth 0 exactly as designed, which is the ladder working rather than failing.

## Files
- `stages/*/stage.md`
  The `probe_depth:` field and the ladder, quoted in each contract.
