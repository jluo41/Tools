# ② The one agent, whose clean context is the wall

state: 🟡 PARTIAL
owner: JL
method: name what the agent does, list what it refuses, and be honest that the refusal is architectural rather than checked

## Question
What is in `probe/agents/`, and why is the wall enforced by an agent's ignorance rather than by a check?
One agent, 93 lines, running only the two steps that need no stake, in a context that never receives one.
It cannot leak what it was never handed, which is the layer's strongest guarantee and the only one nothing verifies.

The design decision worth seeing is how much this agent declines to do.
It does not decide reuse against the bank, it does not write the stripped question, it does not interpret the answer, and it does not judge whether anything settles anything.
Every one of those is stake-aware, so each stays with the consumer, and what is left is the mechanical middle: dispatch a batch, get paths back.

## Boundary
- ✅ Covered here
  The agent's inputs, its two steps, its explicit refusals, and what its clean context does and does not guarantee.
- ↪ Covered elsewhere
  LAW 1 itself, and whether it can be enforced, is `QA6`.
  The order of the steps is `QB1`; the two this agent runs are `QB4` and `QB5`, and whether a dispatch carried more than the q-executor is `QB4`'s check.
  The bank orchestrators it calls belong to `/haipipe-task` and `/haipipe-discovery`.

## Diagram
```
   probe/agents/haipipe-probe-q-executor-agent.md    93 lines · v1.1.0
   shared by paper AND application. The layer's ONE live agent.

   in    a SET of q-executors the bank still OWES
         (bank verdict run | code | new · state planned | commissioned)
         each with its QX id, its route, and the project root
         ── no stake · no claim id · no paper · no reason ──

   ③ DISPATCH   dedup the batch first (T0 JOIN), then hand each
                `### q-executor` VERBATIM to the orchestrator its
                route names. Omit the folder for fresh work.
   ④ POINT      write each entry's target: at the answering QA file.
                the target field only, never the stake.

   out   per entry: { QX id, target: <QA path> | in-flight | failed }

   ── what it REFUSES, and why each refusal is the same refusal ────
   ✗ ② MATCH        the bank verdict is AUTHORITATIVE, decided upstream
   ✗ ① ORGANIZE     writing the q-executor needs the stake to strip
   ✗ ⑤ INTERPRET    harvesting is reading an answer FOR a purpose
   ✗ judging        a claim's fate is the consumer's own business
   ✗ writing under tasks/ or discoveries/          LAW 1, the pen
   ✗ inventing a destination folder                the executor owns it

   the retired gateway was a 1:1 hop that forwarded one question and
   added nothing. this one takes the WHOLE batch and dedups across it.
```

## Content
### 1 · The wall is a context boundary, not a filter
#### Nothing strips the stake at this door, because nothing stake-shaped ever arrives
(the strip happened upstream, at ① ORGANIZE, in the consumer's own session)
The agent's own words are "my clean context IS the wall", and the mechanism is exactly that: it is invoked with a set of q-executors and a project root, and the stage doc holding the stake is never passed.
This is stronger than a filter, because a filter can be wrong about what counts as a stake while an absent input cannot leak.
It is also weaker than a check, because nothing observes what was actually put in the prompt, so a caller that pasted extra context would not be detected here or anywhere.

#### The one instruction for the case that should not happen
(`If stake I was not supposed to receive arrives anyway, I IGNORE it and never write it anywhere`)
The file anticipates its own violation and says what to do, which is the right instinct and the wrong kind of guarantee.
An agent asked to ignore something has already read it, and nothing records that it arrived.

### 2 · Batching is the reason this agent exists
#### It replaced a 1:1 hop with a batch that dedups
(T0 JOIN across the batch, so two identical q-executors never dispatch the same run)
The retired gateway forwarded one question to one executor and added nothing, which is why it was retired.
The value here is at the batch level: dedup before dispatch, one summary back, and the coordination churn kept out of the stage's context so the stage stays readable.
Whether the dedup has ever actually fired is unknown, because no run has been observed from the outside.

#### A batch that is all fresh work is a smell, and the agent must say so
(`either the PROBE worker's MATCH was lazy, or the bank is starving`)
This is the only judgment the agent is permitted, and it is a judgment about the process rather than about any answer.
It is also the layer's only built-in feedback on whether the cost ladder is working, which `QB3` measured from the outside and found leaning heavily on fresh work.

### 3 · What the return contract promises
The return is per entry: the QX id, and either an answering QA path, `in-flight since <started>`, or failed.
`in-flight` is the interesting one, because it is how the QA state line's `working` value reaches the consumer without the consumer ever touching a bank file.
The stage then harvests each answered target itself, at ⑤, which is where the stake legitimately re-enters.

## Items to Finish
- [x] 🤖 One agent, stake-free, question-level, shared by both families
      93 lines, v1.1.0, running ③ and ④ only.
- [x] 🚫 The refusal list is explicit, and each refusal has a stated reason
      Six refusals, each traced to either the stake or to another layer's ownership.
- [x] 📤 The return contract distinguishes answered, in-flight and failed
      Which is how a `working` QA file reaches the consumer without the consumer reading the bank.
- [ ] 🧪 The batch dedup is observed once
      T0 JOIN is claimed as this agent's reason to exist and has never been watched firing.
      This closes when a run with two identical q-executors is seen to dispatch one job, or reported not to.
- [ ] 👃 The all-fresh smell is checked against a real batch
      `QB3` measured 46 percent of the MISQ paper's entries landing on `code`, which is close to the smell this agent is told to report.
      This closes when a run either raises the smell on such a batch or is shown not to.

## Where we are
The agent is built, shipped, shared by both families, and its boundaries are the clearest writing in the layer.

Its guarantee is real but structural: it cannot leak a stake it was never handed, and nothing checks what it was handed.
Two of its own claims, the batch dedup and the all-fresh smell, have never been observed from outside, which makes them design intentions rather than measured behaviour.

## Files
- `agents/`
  The folder, its README and its CHANGELOG.
- `SKILL.md`
  The model the agent runs; it points here for anatomy, contract, ladder and laws.
