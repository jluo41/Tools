# PROBE · What may it do alone, and what must it stop and ask for?
state: 🟡 PARTIAL
owner: JL
method: one door for evidence, a declared ceiling on what it may spend, and no exceptions for scope labels

## Question
PROBE is the only phase that may bring a fact into a paper, and it runs without a human watching. Those two sentences are only compatible because of one number: `probe_depth`, the ceiling on what PROBE may commission, which defaults to 0 and at 0 means it may harvest answers that already exist and may commission nothing. A phase that cannot spend does not need a gate in front of it. Raise that number and three unattended phases need gates again.

So the question is where the boundary of "alone" sits, and it has two edges. One is cost: what may be dispatched, who may raise the ceiling, and how a raise is recorded, which today is a command-line flag and nothing else. The other is route: PROBE is the only exit for evidence work, and the temptation is not to break that rule outright but to relabel around it, because "audit" and "re-verify" and "quick check" do not sound like evidence.

That relabelling has already happened. A live run elicited an AUDIT scope, found no named route for it, and hand-rolled a general-purpose web auditor: eighteen redundant verifications of ledger entries already marked VERIFIED, producing results with no landing path. The rule that came out of it is the right one and is stated in a reference file, which is the same location problem the announce rule has.

## Boundary
- ✅ Covered here
  What the STAGE declares and consumes: `probes:`, `probe_depth:`, the Q-consumer block, the one-route rule, and when an answer counts as interpreted.
- ↪ Covered elsewhere
  The five-step loop, the stake split and the bank's own ladder belong to `/haipipe-probe`, which this family does not own: see `QA5` and `../01-probe-qa-260726/`. What DRAFT raised is `QB8`; what REVISE does with a landed answer is `QB10`.

## Diagram
```
   🔬 PROBE                  the ONE door a fact enters by, unattended

   ── WHAT MAKES UNATTENDED SAFE: one number ────────────────────────
      probe_depth:  the ceiling on what PROBE may dispatch

        0  READ        reuse an answer that exists   free   ◄ DEFAULT
        1  NEW RUN     old script, new config        costs
        2  NEW SCRIPT  must write new code           costs more
        3  NEW FOLDER  open a new task folder        costs most

      depth ≤ ceiling  ──▶  DISPATCH
      depth >  ceiling  ──▶  DEFER, with a forward pointer recorded.
                             NEVER a silent drop.

      📍 all eight stages declare 0 today. The ladder itself is the
         bank's, not ours: task/haipipe-task/fn/qa.md.        → ⑥

   ── THE ARGUMENT IN ONE LINE ──────────────────────────────────────
      a phase that cannot SPEND does not need a human in front of it.
      That is the ONLY reason DRAFT · PROBE · REVISE run unattended
      and the human is spent once, at CHECK.               → QB11
      Raise the ceiling and you have re-opened three gates.

   ── THE ONE ROUTE, AND WHY LABELS DO NOT OPEN A SECOND ────────────
      a stage's evidence need
        │
        ▼   Skill("haipipe-paper-probe")        ⬅ THE ONLY EXIT
        │   ①organize ②match ⑦dispatch ⑧point ③interpret   → ⑥
        ▼
      Agent(haipipe-task-orchestrator-agent)
      Agent(haipipe-discovery-orchestrator-agent)

      ⛔ a stage NEVER dispatches an agent for evidence, general-purpose
         included, and NO scope label creates an exception:
         "audit" · "re-verify" · "quick check" are evidence work.
      ⛔ a stage never reads project evidence inline: not discoveries/,
         not task results, not legacy probes/. It knows what is MISSING
         from its own draft; the agent's anchored return is its only
         evidence window.
      ⛔ evidence scope is PROJECT-LOCAL. Cross-project reuse is a USER
         decision (JL 2026-07-05), never an agent's.

   ── THE FAILURE THAT WROTE THAT RULE ──────────────────────────────
      an elicited AUDIT scope had no named route, so the stage
      hand-rolled a general-purpose web auditor:
        18 redundant verifications of entries already VERIFIED
        results with NO landing path
      ⚠️ nothing was fabricated. The cost was pure waste, and the
         next one may not be.

   ── WHAT DEFERRAL COSTS, AND WHY IT IS STILL RIGHT ────────────────
      a deferred question leaves a placeholder in the prose and an
      open item on the page. That is VISIBLE DEBT, which is the point:
        visible debt   ⏸ parked, a human decides whether to spend
        the alternative   an agent quietly deciding a paper's
                          evidence budget
      live on MISQ: 11 parked values, each naming the depth that
      would release it.

   ── THE WEAKEST LINK IS THE LAST STEP ─────────────────────────────
      an answer that LANDS and is never woven back leaves the paper
      carrying a placeholder and a CLOSED probe at the same time.
      measured on MISQ 260726: 13 values and 3 citations in exactly
      that state.
```

## Content
### The ceiling is the whole safety argument
Everything else about unattended phases follows from `probe_depth`. It is the reason DRAFT, PROBE and REVISE need no gates, the reason the human's attention is spent once, and the reason a stage can be re-run without a person watching. It is also one integer in a frontmatter block, raised today by a command-line flag, with no record of who raised it or why. A raise is a spending decision and should be as visible as a gate.

### Why the route rule needs no exceptions, and gets asked for them anyway
The rule is that all evidence work leaves through the probe worker. What makes it fragile is that the tempting cases never announce themselves as evidence: an audit, a re-verification, a quick sanity check. Each sounds procedural. Each is a fact entering the paper by a route with no record, which is exactly what the one-door design exists to prevent, and the audit incident is the proof that the pressure is real rather than theoretical.

### An answer is not interpreted until the sentence changes
The loop's last step is the one done by hand and it is where the whole thing leaks. Marking a probe closed and leaving the placeholder standing produces a paper that is simultaneously answered and unanswered, and both records look correct in isolation. Thirteen values and three citations are in that state on the MISQ paper right now.

## Items to Finish
- [x] 🪜 The ceiling exists, per stage, defaulting to 0
      `probe_depth:` in all eight contracts.
- [x] 🚪 One route for evidence work
      `Skill("haipipe-paper-probe")` and nothing else; the stage never dispatches an agent itself.
- [ ] 📐 State who may raise the ceiling, and how the raise is recorded
      A raise is a spending decision. It should be as visible as a gate, and today it is a command-line flag.
- [ ] 🧠 Rule whether any stage may default above 0
      If one should, say which and why. If none should, say that, so the field cannot drift upward one paper at a time.
- [ ] 📐 Define when an answer counts as interpreted
      Woven into the prose AND its placeholder discharged. Today those are two acts and nothing checks that both happened.
- [ ] 🔎 Decide what happens to a question the bank REFUSES
      Refusal is a real outcome. The loop currently describes only answers.
- [ ] 🔧 Put the one-route rule where the workers read it
      It lives in `ref/08-stage-gate.md`. The stage that hand-rolled a web auditor was not reading that file.

## Where we are
The ceiling is implemented and honoured; the two venue questions on the MISQ paper sit deferred at depth 0 exactly as designed, which is the ladder working rather than failing. Eleven values are parked, each naming the depth that would release it.

The route rule holds now and has been broken once. The last step of the loop is done by hand and is where the leak is: sixteen items on MISQ are answered and still carry their placeholder.

## Files
- `stages/*/stage.md`
  `probe_depth:` and `probes:`; the ladder quoted in each contract.
- `2-phase/1-probe/haipipe-paper-probe/`
  The worker that owns the loop; the only exit for evidence work.
- `1-lifecycle/ref/08-stage-gate.md`
  The one-route rule, the project-local rule, and the audit incident that produced both.
- `haipipe-probe/`
  The shared layer. The loop, the stake split and the QA state contract live there, not here.

## Law
Evidence enters a paper at PROBE and nowhere else. A stage never dispatches an agent for evidence work, general-purpose included, and no scope label creates an exception: an audit, a re-verification and a quick check are all evidence work and take the same door.

A stage never reads project evidence inline. It knows what is missing from its own draft; the agent's anchored return is the paper side's only evidence window. Evidence scope is project-local, and cross-project reuse is a user decision.

`probe_depth` is the ceiling on what PROBE may dispatch and it defaults to 0. Dispatch when the bank's depth is at or below the ceiling; otherwise DEFER with a forward pointer recorded, never a silent drop. A phase that cannot spend does not need a human in front of it, and that is the only reason three of the four phases run unattended.

## Log
260726 · Rewritten from `_archive/QB4-probe-loop.md` and `_archive/QB5-cost-ladder.md`, both of which taught mechanisms that `/haipipe-probe` owns and that `../01-probe-qa-260726/` already has faces for. Under `QA1`'s Law this face keeps only the paper's half: what the stage declares, what it may spend, which route it must take, and when an answer counts as landed.
