# The four phases, and why evidence enters only at PROBE
state: 🟡 PARTIAL
owner: JL
method: keep DPRC; pin down what each phase may and may not do

## Question
Why does every stage run DRAFT, PROBE, REVISE, CHECK, and why may evidence enter at only one of them?

The phases are not a workflow convenience. They exist so that a claim's evidence has exactly one entry point, which is what makes a finished paper auditable: every number and every citation can be traced back to the probe entry that produced it. If DRAFT could fetch evidence, or REVISE could quietly add a citation, that trace breaks and nobody can tell what was verified from what was plausible.

## Boundary
- ✅ Covered here
  What each phase may do, and the rule that evidence enters only at PROBE.
- ↪ Covered elsewhere
  The mechanics of a probe entry are `QD1`; what PROBE may spend is `QD2`; what DRAFT writes where it does not yet know is `QD3`.

## Content
### What each phase is for
```
 DRAFT    write the artifact; RAISE questions; never answer them
 PROBE    the only door: organize each question, match it against the bank,
          dispatch what match cannot close, point at the answer, interpret it back
 REVISE   rewrite to venue quality; substitute answers that landed; leave
          why-comments; never introduce a fact
 CHECK    the human reads quality, flags and why-comments at once, and rules
```

### The rule that makes it work
DRAFT raises questions and nothing else. That was not always true: organizing and matching used to live in DRAFT, and were moved into PROBE on 2026-07-20 when the gate they had been merged into was removed. The move is what made "evidence enters only at PROBE" literally true rather than approximately true.

### Why REVISE is unattended
REVISE changes prose directly and leaves `%% {CC-*}:` why-comments explaining each change. It is fully automatic because the human reads the changes and the reasons together at CHECK, which is cheaper for the human than approving edits one at a time.

## Items to Finish
- [x] 🚪 Evidence has exactly one door
      DRAFT raises, PROBE answers; the 2026-07-20 move made it true in the contracts.
- [ ] 📐 State what REVISE may never do
      It may substitute an answer that landed and it may rewrite prose. Whether it may add a citation it happens to know is the case that decides whether the trace holds.
- [ ] 🧠 Rule whether a stage may skip a phase
      Some stages have nothing to probe. Today they run PROBE and it closes empty. Decide whether that is right, or whether a stage may declare a phase inapplicable.

## Where we are
The four phases are implemented and each has its own worker skill. The one-door rule is stated in `PHILOSOPHY.md` and enforced by the phase workers' contracts, not by a checker.

## Files
- `PHILOSOPHY.md`
  Evidence routing.
- `../../2-phase/`
  The four phase workers, one folder each.
