# What is a gate, and who may pass it?
state: 🟡 PARTIAL
owner: JL
method: one gate per stage at CHECK; make agent stand-ins impossible rather than discouraged

## Question
What does it mean for a stage to be done, and who is allowed to say so?

A gate is a human yes. The design deliberately spends the human's attention at exactly one point per stage, at CHECK, and lets DRAFT, PROBE and REVISE run unattended so the human meets a finished thing rather than a stream of approvals. The open part is not the definition; it is what happens when nobody is there to say yes.

## Boundary
- ✅ Covered here
  What a gate is, where it sits, and who may pass it.
- ↪ Covered elsewhere
  How many gates a stage may declare is part of its contract form, `QE1`; the cost that makes unattended phases safe is `QD2`.

## Content
### The design
Each `stage.md` declares `gates:`, and the default is one, at CHECK. DRAFT, PROBE and REVISE are unattended. That is only safe because PROBE cannot spend without authorization, which is `QD2`: a phase that cannot cost anything is a phase that does not need a gate in front of it.

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
