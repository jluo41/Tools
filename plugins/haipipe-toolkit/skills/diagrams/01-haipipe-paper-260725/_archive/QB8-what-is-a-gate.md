# What is a gate, and who may pass it?
state: 🟡 PARTIAL
owner: JL
method: one gate per stage at CHECK; make agent stand-ins impossible rather than discouraged

## Question
What does it mean for a stage to be done, and who is allowed to say so? A gate is a human yes, spent deliberately at one point per stage. The safety of the entire design rests on no agent ever being able to write one.

A gate is a human yes. The design deliberately spends the human's attention at exactly one point per stage, at CHECK, and lets DRAFT, PROBE and REVISE run unattended so the human meets a finished thing rather than a stream of approvals. The open part is not the definition; it is what happens when nobody is there to say yes.


The approach is one human yes per stage, spent where it buys the most, with everything before it unattended and safe because nothing before it can spend. What we want is a design in which no agent can ever mark work accepted, no matter how confident it is or how convenient it would be.
## Boundary
- ✅ Covered here
  What a gate is, where it sits, and who may pass it.
- ↪ Covered elsewhere
  How many gates a stage may declare is part of its contract form, `QE1`; the cost that makes unattended phases safe is `QB5`.

## Diagram
```
 WHERE THE HUMAN'S ATTENTION IS SPENT: ONCE, ON A FINISHED THING

   DRAFT ──► PROBE ──► REVISE ──►  CHECK
   ╰──────── unattended ───────╯    🧠 one human yes

 WHY UNATTENDED IS SAFE
   a phase that cannot SPEND does not need a gate in front of it.
   PROBE's ceiling is probe_depth (QB5): depth 0 reads and harvests only.
   Remove that ceiling and all three of these need gates again.

 THE FAILURE THIS HAS ALREADY HAD          (MISQ seed, still open)
   ┌──────────────────────────────────────────────────┐
   │ an agent may not PASS a gate                     │
   │ an agent CAN write the line saying it passed  ⚠️  │
   └──────────────────────────────────────────────────┘
   a seed re-run gate was recorded as passed by an agent standing in
   for the human. The record says so plainly. A stage was marked done
   that no person had read.
   Only good behaviour prevented it, which is not a mechanism.

 WHERE THE ANSWER PROBABLY LIES
   in the phase worker          in the BOARD
   ✗ the worker is the thing    ✓ a page cannot be ✅ until its own
     being constrained            gate is recorded, and that is where
                                  a human is actually looking
```

## Content
### The design
Each `stage.md` declares `gates:`, and the default is one, at CHECK. DRAFT, PROBE and REVISE are unattended. That is only safe because PROBE cannot spend without authorization, which is `QB5`: a phase that cannot cost anything is a phase that does not need a gate in front of it.

### The failure this has already had
On the MISQ paper, a seed re-run gate was recorded as passed by an agent standing in for the human. The record says so plainly, and the consequence was a stage marked done that no person had read. It is still open on that paper's seed page.

That is the real question here: an agent that must not pass a gate, but can write the line that says the gate passed, is only prevented by good behaviour.

### Where the answer probably lies
The board makes a gate visible as a page's `state:`, and a page cannot be ✅ until its own gate is recorded. That is a better place to enforce it than inside the phase worker, because it is where a human is actually looking.

## Items to Finish
- [x] 🚦 One gate per stage, at CHECK
      Declared per stage as `gates:`, defaulting to CHECK.
- [ ] 🧠 Rule what an agent may write about a gate
      It may prepare CHECK evidence. Whether it may ever write the gate line, even when reporting that a human said yes elsewhere, is the ruling.
- [ ] 🔎 Decide how a stand-in gate is detected after the fact
      The MISQ case was caught because the agent recorded honestly. Something that does not depend on honesty would be better.

## Where we are
One gate per stage is implemented. The stand-in case is known, documented on the affected paper, and unprevented.

## Files
- `stages/*/stage.md`
  The `gates:` field.
- `0-lifecycle/0-seed/S-Seed-0-seed.md`
  The paper carrying the unresolved stand-in gate.
