# ③ DISPATCH · what crosses the wall?

state: 🟡 PARTIAL
owner: JL
method: one fixed payload block, copied rather than composed, and a ceiling gate that runs before any of it

## Question
This is the single point where the wall is crossed; what is allowed through, and what decides whether the crossing happens at all?
The `### q-executor` text verbatim and nothing else, after a ceiling gate compares the entry's depth against what the run is authorized to spend.
The payload is a block to copy rather than a message to write, because a composed message is where helpfulness leaks a stake.

The failure mode here is not malice, it is consideration.
Sending "a bit of context" reads as helpful and is exactly what makes the answer unreusable, so the defence is that there is nothing to compose.
One block, copied, so a reviewer can compare what was sent against one known string instead of judging whether a paraphrase leaked.

## Boundary
- ✅ Covered here
  The payload, the ceiling gate that precedes it, what deferring means, and the division of labour with the executor.
- ↪ Covered elsewhere
  The agent that receives the payload is `QA3`; the verdict this step consumes is `QB3`'s; where the returned path lands is `QB5`.
  What a paper may authorize, and who raises it, is `QB9@paper`.

## Diagram
```
   ── the CEILING GATE, before any dispatch ────────────────────────
       depth(bank) <= probe_depth   →  ③ DISPATCH it
       depth(bank) >  probe_depth   →  DEFER, and STOP for that entry

   DEFERRING IS A CORRECT OUTCOME, and it must be DECLARED:
       **state**: deferred
       **deferred**: depth-2 · needs a new script to join review text
                     to the claims panel; nobody has authorized it.
   a `deferred` with no such line is a `planned` in a costume, and
   FAILs as deferred-undeclared — 5 of the 12 real failures on MISQ,
   and a code the APPLICATION fork does not emit at all.

   ── the PAYLOAD, copied not composed ─────────────────────────────
   Agent(haipipe-task-orchestrator-agent, prompt="
     action: qa
     project: <project_root>
     question: |
       <the ENTRY's q-executor block, VERBATIM. Nothing else.>
     task-folder: <existing path | NEW <path> | omit if unknown>
   ")
   …and identically for the discovery orchestrator.

   ⛔ NOT sent: the ### q-consumer copies · the probe file · the paper

   ── route on the TARGET, not on the verdict ──────────────────────
   target: <an existing QA path>  → skip ③, go to ④⑤
   target: NEW <path>             → ③ dispatch, WHATEVER the verdict

   ⚠️ `bank: reuse` + `target: NEW` is the COMMON case, not a
      contradiction: the results already answer it and nobody has
      written the readable digest. It still requires ③, because
      LAW 1 forbids a consumer authoring a bank file.
```

## Content
### 1 · The executor decides how, never what
The consumer's `route` and `bank` verdict are authoritative, because at plan time the consumer already knows which partition holds the answer.
Everything after that, the shape of the work and its depth, belongs to the executor in its own clean context, and it returns a PATH to the answering QA file rather than a narrative.
The destination folder for fresh work is deliberately omitted, because the orchestrator owns its own namespace and decides enrich-versus-new itself.

### 2 · Two rules that bind here live in only one fork
#### `route on the TARGET, not on the verdict` is stated in the paper adapter alone
(the shared model says `bank` is the plan and `state` is where it is now, and stops there)
The rule that decides whether ③ runs at all, and the `bank: reuse` + `target: NEW` case it exists to disambiguate, appear in `haipipe-paper-probe/SKILL.md` and not in the constitution.
An application worker following only the shared model has to derive it, and the case it disambiguates is described there as the common one.

#### `deferred-undeclared` is enforced by one fork and stated by the model for both
The constitution states the deferral rule for the layer, the paper checker enforces it, and the application checker does not emit the code at all.
So an application entry can sit `deferred` with no depth-and-cost line and pass a gate that would red the identical entry in a paper.

## Items to Finish
- [x] 📦 One copyable dispatch block; variants are not to be invented
- [x] 🎯 The executor returns a PATH to the answering QA file
- [x] 🚧 The ceiling gate runs before any dispatch, and deferring is a declared outcome
- [x] 🙈 The destination folder is omitted for fresh work, so the executor owns its namespace
- [ ] 🧪 A dispatch carrying more than the q-executor is detected
      Nothing inspects what a session actually sent, so this rule relies entirely on review.
      It is also the one rule whose violation leaves no artifact, which is `QA6`'s LAW 1 problem in its sharpest form.
- [ ] 📖 `route on the target, not the verdict` moves into the shared model
      A rule that decides whether the wall is crossed lives in one of two adapters, and the case it disambiguates is described as the common one.
      This closes when the constitution states it, since both families need it.
- [ ] 🍴 `deferred-undeclared` is ported to the application fork
      Held with `QA4`'s fork ruling; noted here because this is the step the rule guards.

## Where we are
Built and running, with the payload rule doing the work it was designed to do: there is nothing to compose, so there is nothing to leak.

Splitting this step onto its own page found two rules that bind at the crossing and live in only one of the two adapters.
One is `route on the TARGET, not on the verdict`, which decides whether the crossing happens.
The other is the enforcement of declared deferral, which is stated generally and checked in one family.

## Files
- `SKILL.md`
  The payload block and the dispatch rules.
- `agents/`
  The collector that receives it.
- `haipipe-paper-probe/`
  The ceiling gate, and the target-versus-verdict rule that has no home in the model.
