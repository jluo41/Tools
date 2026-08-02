# PROBE · What may it do alone, and what must it stop and ask for?
state: 🟡 PARTIAL
owner: JL
method: one door for evidence, a declared ceiling on what it may spend, and no exceptions for scope labels

## Opening
PROBE is the only phase that may bring a fact into a paper, and it runs without a human watching. Those two sentences are only compatible because of one number: `probe_depth`, the ceiling on what PROBE may commission, which defaults to 0 and at 0 means it may harvest answers that already exist and may commission nothing. A phase that cannot spend does not need a gate in front of it. Raise that number and three unattended phases need gates again.

So the question is where the boundary of "alone" sits, and it has two edges. One is cost: what may be dispatched, who may raise the ceiling, and how a raise is recorded, which today is a command-line flag and nothing else. The other is route: PROBE is the only exit for evidence work, and the temptation is not to break that rule outright but to relabel around it, because "audit" and "re-verify" and "quick check" do not sound like evidence.

That relabelling has already happened. A live run elicited an AUDIT scope, found no named route for it, and hand-rolled a general-purpose web auditor: eighteen redundant verifications of ledger entries already marked VERIFIED, producing results with no landing path. The rule that came out of it is the right one and is stated in a reference file, which is the same location problem the announce rule has.

Scope: This page covers What the STAGE declares and consumes: `probes:`, `probe_depth:`, the Q-consumer block, the one-route rule, and when an answer counts as interpreted. Neighbouring pages cover The five-step loop, the stake split and the bank's own ladder belong to `/haipipe-probe`, which this family does not own: see `QA5` and `../01-probe-qa-260726/`. What DRAFT raised is `QC4a`; what REVISE does with a landed answer is `QC4c`.

## Diagram
```
   🔬 PROBE                  the ONE door a fact enters by, unattended

   ── WHAT MAKES UNATTENDED SAFE: one number ────────────────────────
      probe_depth:  the ceiling on what PROBE may dispatch
                    one integer, 0..3, and 0 is the default

      depth(bank) ≤ ceiling  ──▶  DISPATCH
      depth(bank) >  ceiling  ──▶  DEFER, and the entry must DECLARE
                                   `deferred: depth-<n> · <reason>`.
                                   NEVER a silent drop.

      ↪ THE RUNGS ARE NOT OURS. What depth 1, 2 and 3 mean is the
        bank's ladder, and the bank documents FIVE cost rungs against
        these FOUR depths with no map between them: `QB3@probe`. This
        face restates neither, because restating a ladder somebody
        else has not finished reconciling is how two copies drift.
      📍 verified 260727: all eight contracts declare `probe_depth: 0`,
         each quoting the same dispatch rule beside it.

   ── THE ARGUMENT IN ONE LINE ──────────────────────────────────────
      a phase that cannot SPEND does not need a human in front of it.
      That is the ONLY reason DRAFT · PROBE · REVISE run unattended
      and the human is spent once, at CHECK.               → QC4d
      Raise the ceiling and you have re-opened three gates.
      ⚠️ and a FOURTH, inside PROBE itself. The shared loop puts a
         human APPROVE gate between ② MATCH and ③ DISPATCH
         (`QB1@probe`). At depth 0 step ③ is never reached, so that
         gate never fires: it is UNREACHABLE, not absent. The first
         paper to raise the ceiling meets a gate mid-phase that no
         paper face has ever mentioned.

   ── THE ONE ROUTE, AND WHY LABELS DO NOT OPEN A SECOND ────────────
      a stage's evidence need
        │
        ▼   Skill("haipipe-paper-probe")        ⬅ THE ONLY EXIT
        │   five steps in one fixed order, owned by `QB1@probe`
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

   ── WHO READS THESE FIELDS, AND HOW THEY FAIL ────────────────────
      probes:       reader ③, but `check-probe-cards.sh` reads the
                    directory it names, so the SHAPE is enforced
                    🔊 LOUD-ish, and it is a `done_criteria` line on
                    seven of the eight contracts.
      probe_depth:  reader ③ THE EXECUTOR             fails 🔇 SILENT
                    a ceiling nothing enforces is a suggestion, and
                    this one is the single number the unattended
                    design rests on.                            → QC2
      to bind  a raise is a SPENDING decision and should leave the same
               kind of trace a gate does. Today it is a command-line
               flag that vanishes. Make `--depth N` write a line into
               the owning S page's `## Log`, where the gate row already
               is, and a raise becomes as auditable as a gate without
               becoming one.
               ⚠️ not a `_LOG_<stage>.md`. The `log:` field was retired
                  2026-07-26 and no live paper ever carried the sidecar
                  it declared (`stages/CONTRACT.md:114`). The S page's
                  `## Log` is the only history there is.
```

## Content
### The ceiling is the whole safety argument
Everything else about unattended phases follows from `probe_depth`. It is the reason DRAFT, PROBE and REVISE need no gates, the reason the human's attention is spent once, and the reason a stage can be re-run without a person watching. It is also one integer in a frontmatter block, raised today by a command-line flag, with no record of who raised it or why. A raise is a spending decision and should be as visible as a gate.

### Why the route rule needs no exceptions, and gets asked for them anyway
The rule is that all evidence work leaves through the probe worker. What makes it fragile is that the tempting cases never announce themselves as evidence: an audit, a re-verification, a quick sanity check. Each sounds procedural. Each is a fact entering the paper by a route with no record, which is exactly what the one-door design exists to prevent, and the audit incident is the proof that the pressure is real rather than theoretical.

### An answer is not interpreted until the sentence changes
The loop's last step is the one done by hand and it is where the whole thing leaks. Marking a probe closed and leaving the placeholder standing produces a paper that is simultaneously answered and unanswered, and both records look correct in isolation. Thirteen values and three citations are in that state on the MISQ paper right now.

## Aims
- [x] 📐 The ceiling exists per stage and defaults to 0
      Verified 260727: `probe_depth: 0` in all eight `stages/*/stage.md`, each quoting the dispatch rule beside it.
- [x] 📐 One route for evidence work, with no label exception
      `1-lifecycle/ref/08-stage-gate.md:95`: the worker plus collector chain is the only exit, and "audit", "re-verify" and "quick check" take the same door.
- [x] 📐 Who may raise the ceiling is already written down
      `2-phase/1-probe/haipipe-paper-probe/SKILL.md:120`: "NEVER raise the ceiling on your own initiative. `--depth` is the human act that authorizes spend." `haipipe-paper-stage/SKILL.md:146` says the same and calls it the act the removed DRAFT gate used to be.
- [x] 🔍 A deferral is declared, never dropped
      Five of five `state: deferred` entries in the MISQ `1-probes/` carry their `deferred: depth-<n> · <reason>` line, which is the rule `check-probe-cards.sh` enforces.
- [~] ↪ MOVED to `QB3@probe` · the 0-3 rung labels, and the five-rung cost ladder they do not map onto
- [~] ↪ MOVED to `QB1@probe` · the five-step loop, which this face had listed with its step numbers scrambled
- [~] ↪ MOVED to `QC1@probe` · what a bank REFUSAL is. Already ruled in the shared layer: `probe/haipipe-probe/SKILL.md:342` declares `failed` for "the executor REFUSED", and `concern` for a doubt no bank route can close.
- [ ] 🔧 Put the one-route rule where unattended workers read it
      `ref/08-stage-gate.md:95` holds it, and the three phases that run unattended cite that file NOWHERE: `haipipe-paper-draft`, `haipipe-paper-probe` and `haipipe-paper-revise` contain no reference to it. CHECK cites it twice (`haipipe-paper-check/SKILL.md:87`, `:292`) and the stage router once as a filename in a reference list (`haipipe-paper-stage/SKILL.md:69`). So the file is cited by the phase that has a human in front of it and by none of the three that do not.
- [ ] 📐 Make a raise leave the trace a gate leaves
      Who may raise is settled; the RECORD is not. `probe --depth N` is a flag that vanishes with the session, so no paper can be read back to find out what it was allowed to spend. One line into the owning S page's `## Log`, beside the gate row, makes a raise as auditable as a gate without making it a gate. Not a `_LOG_<stage>.md`: `log:` was retired 2026-07-26 and the sidecar it declared never existed on any live paper (`stages/CONTRACT.md:114`).
- [ ] 🧠 Rule whether a stage may default above 0
      Two live options. Either no stage ever may, so the field is a constant and upward drift is closed by rule; or name the stage that may and the test it must pass. All eight declare 0, which is why the question has never had to be answered.
- [ ] 📐 Say what DISCHARGES a placeholder, not just answers it
      The PROBE half is already mechanical: `check-probe-cards.sh` FAILs `qa-answered-empty` and an `answered` target whose `### a-executor` is still empty. The prose half is not. Nothing connects a closed entry to the `[Q-…]` bracket still standing in the sentence it was raised for.
- [ ] 🔍 Re-derive this face's counts, naming the counting rule
      It cites 11 parked values and 13 values plus 3 citations answered-with-placeholder. On disk `1-probes/` holds 15 entries (5 answered, 5 deferred, 3 read, 2 commissioned) and `sections/` carries 56 `{VAL:?}` and 89 `\cite{TOADD}`. No rule reproduces 11, 13 or 3.
- [ ] 🔧 Source the audit incident's numbers, or drop them
      `2-phase/1-probe/haipipe-paper-probe/CHANGELOG.md:367` records the incident and its fix verbatim, and nothing else does. The "18 redundant verifications" and "no landing path" appear nowhere on disk, and an unsourced count is the wrong kind of example on the face that argues for one door.

## States
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

- Evidence enters a paper at PROBE and nowhere else. A stage never dispatches an agent for evidence work, general-purpose included, and no scope label creates an exception: an audit, a re-verification and a quick check are all evidence work and take the same door.
- A stage never reads project evidence inline. It knows what is missing from its own draft; the agent's anchored return is the paper side's only evidence window. Evidence scope is project-local, and cross-project reuse is a user decision.
- `probe_depth` is the ceiling on what PROBE may dispatch and it defaults to 0. Dispatch when the bank's depth is at or below the ceiling; otherwise DEFER with a forward pointer recorded, never a silent drop. A phase that cannot spend does not need a human in front of it, and that is the only reason three of the four phases run unattended.

## Discussion
> CC 260727: `probe_depth` may not deserve to be a contract field, and `QC2`'s own Law is what raises the doubt. All eight contracts declare the identical constant 0, nothing reads the field to refuse anything, and the thing that actually binds a run is the invocation's `--depth`, which the worker takes as the HIGHER of the two (`haipipe-paper-probe/SKILL.md:93`). By `QC2`'s test, a field that no program checks, that no human consults at a named moment, and that has never differed between stages is decoration. Two options. Keep it, on the argument that a per-stage ceiling is where a future stage would say it needs a different default, and that the number is the whole safety argument so it should be visible in the contract that carries it. Or delete it and let 0 be the invocation default, so the only ceiling is the one a human passes. My recommendation is KEEP, and the cost of keeping is exactly the item above: until a raise writes a line into the owning S page's `## Log`, the field advertises a spending discipline that leaves no evidence it was ever honoured, which is the same shape as the advisory `upstream:` block `QC2` complains about. The cost of deleting is that the eight contracts stop documenting the ceiling at all, and a reader would have to learn it from a worker's SKILL.md.

## Log
260726 · Rewritten from `_archive/QB4-probe-loop.md` and `_archive/QB5-cost-ladder.md`, both of which taught mechanisms that `/haipipe-probe` owns and that `../01-probe-qa-260726/` already has faces for. Under `QA1`'s Law this face keeps only the paper's half: what the stage declares, what it may spend, which route it must take, and when an answer counts as landed.

260727 · Verified against `skills/paper/` and finished the cut the 260726 rewrite had started. `probe_depth: 0` confirmed in all eight contracts. Two mechanisms still owned by the shared layer left the Diagram: the 0-3 rung LABELS, now a pointer to `QB3@probe`, which is where the finding that the bank documents five cost rungs against four depths with no map between them already lives; and the five-step loop, which this face had printed as `①organize ②match ⑦dispatch ⑧point ③interpret`, three of the five numbers wrong against `QB1@probe`'s `③ DISPATCH ④ POINT ⑤ INTERPRET`. Reading `QB1@probe` for that correction surfaced something no paper face had said: the shared loop puts a human APPROVE gate between ② MATCH and ③ DISPATCH, and at depth 0 step ③ is never reached, so the gate is unreachable rather than absent. That is a stronger version of this face's own argument and it is now in the Diagram. Two items closed as already true rather than open: who may raise the ceiling is stated outright at `haipipe-paper-probe/SKILL.md:120`, so the open half narrowed to the raise's TRACE; and bank refusal is already a declared state, `failed` at `probe/haipipe-probe/SKILL.md:342`, so that item became a pointer. One item became `[x]` with a number: all five deferred entries on the live paper carry their depth reason. Two counts could not be reproduced and are now items rather than silent prose, the "18 redundant verifications" (nowhere on disk; the CHANGELOG records the incident and the fix, not a count) and the 11/13/3 placeholder tallies (`1-probes/` holds 15 entries and `sections/` 56 `{VAL:?}` plus 89 `\cite{TOADD}`). Two later corrections from the main session, both verified here before applying. The `--depth` trace was retargeted off `_LOG` onto the owning S page's `## Log`: `log:` was retired 2026-07-26 and `stages/CONTRACT.md:114` records that the `_LOG_<stage>.md` it declared on all eight stages never existed on any live paper, so the suggestion had been pointing at a file that cannot be written. Putting the spend line beside the gate row is also the better answer, since a reader looking for what a stage was allowed to do now finds the authorisation and the approval in one place. And the one-route item stopped overclaiming: the file IS cited, twice by CHECK (`haipipe-paper-check/SKILL.md:87`, `:292`) and once by the router, and the sharp fact is that `draft`, `probe` and `revise` cite it nowhere. The three phases that run without a human are the three that do not reference the rule they are bound by, which is a better statement of the gap than "the workers do not read it".
