# The four phases, and why evidence enters only at PROBE
state: 🟡 PARTIAL
owner: JL
method: keep DPRC; pin down what each phase may and may not do

## Question
Why does every stage run DRAFT, PROBE, REVISE, CHECK, and why may evidence enter at only one of them? The order is not workflow convenience. It is what makes an unattended run safe, and what lets every fact in the finished paper be traced back through a single door.

The phases are not a workflow convenience. They exist so that a claim's evidence has exactly one entry point, which is what makes a finished paper auditable: every number and every citation can be traced back to the probe entry that produced it. If DRAFT could fetch evidence, or REVISE could quietly add a citation, that trace breaks and nobody can tell what was verified from what was plausible.


The approach is to fix the order and give exactly one phase the right to bring evidence in. What we want is that every fact in the finished paper can be traced back through a single door, so a reader asking where a number came from always has one place to look rather than four.
## Boundary
- ✅ Covered here
  What each phase may do, and the rule that evidence enters only at PROBE.
- ↪ Covered elsewhere
  The mechanics of a probe entry are `QBb1`; what PROBE may spend is `QBb2`; what DRAFT writes where it does not yet know is `QBb3`.

## Diagram
```
 ONE DOOR FOR EVIDENCE, AND THIS IS WHY THE TRACE HOLDS

  ┌ DRAFT ──────────┐   writes the artifact
  │ raise questions │   RAISES questions · never answers one
  └────────┬────────┘   {VAL:? …} [Q-Section-4]   \cite{TOADD} [Q-…]
           │
  ┌ PROBE ─▼─────────────────────────────────────────┐  ⬅ THE ONLY DOOR
  │ ① organize  strip the stake, make it executable  │
  │ ② match     is the answer already in the bank?   │
  │ ③ dispatch  what match cannot close  ──► task /  │
  │                                          discovery│
  │ ④ point     the probe entry names its target     │
  │ ⑤ interpret bring it back WITH its caveats       │
  └────────┬─────────────────────────────────────────┘
           │
  ┌ REVISE ▼────────┐   rewrite to venue quality
  │ unattended      │   substitute answers that LANDED
  └────────┬────────┘   leaves %% {CC-*}: why-comments
           │            NEVER introduces a fact
  ┌ CHECK ─▼────────┐   🧠 the human, once per stage
  │ the only gate   │   reads the changes and the reasons TOGETHER
  └─────────────────┘

 WHAT THE RULE BUYS
   every number and every citation in the finished paper
   traces back to the probe entry that produced it.
   If DRAFT could fetch, or REVISE could add a citation,
   nobody could tell VERIFIED from PLAUSIBLE.

 IT BECAME LITERALLY TRUE ON 2026-07-20
   before   DRAFT: write + organize + match      "mostly one door"
   after    DRAFT: write.  PROBE: ① … ⑤          one door
```

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
