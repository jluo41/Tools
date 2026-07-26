# Who may commission a render
state: 🟡 PARTIAL
owner: JL
method: name the one commissioner, keep rendering off the spending ladder, and let no render touch what the manuscript shows

## Question
Who is allowed to invoke a renderer, what does it cost, and what may the result overwrite? A render has to be attemptable at any time and must never destroy a display a human has already accepted.

`QD1` settles who owns which PART of a display. It does not say who may TRIGGER one. That is a different question with a real safety property attached, and the rule answering it was written inside a stage template, which is the last place a reader would look for an authorization rule.


The approach is a commissioning asymmetry plus a candidate mode: a render can always be attempted, and it lands beside the live asset rather than on top of it. What we want is that no invocation, however casual, can destroy a display a human already accepted.
## Boundary
- ✅ Covered here
  Who commissions a render, whether it spends, and what a returned render may replace.
- ↪ Covered elsewhere
  Which layer owns which part is `QD1`; the renderer's own input and output contract is `QD2`; the spending ladder itself is `QBb2`; what makes the result auditable afterwards is `QD6`.

## Diagram
```
 QD1 SAYS WHO OWNS WHICH PART. THIS SAYS WHO MAY PULL THE TRIGGER.

 THE COMMISSIONING ASYMMETRY
   every other stage    does the work itself, or asks the bank and waits
   4-display            COMMISSIONS a named worker
                          -display-table | -figure | -diagram | -illustration
   the four stay INDEPENDENTLY REGISTERED skills, invoked by name,
   deliberately outside the stage's contract, because they must be
   usable with no paper at all.

 A RENDER IS NOT A BANK QUESTION  ── this is what decides the cost
   ┌──────────────────────────────────────────────────────────┐
   │ a BANK question  ──► task / discovery · costs ·          │
   │                      capped by probe_depth               │
   │ a RENDER         ──► the display stage's OWN step ·      │
   │                      NOT dispatched · does not spend     │
   │                      against probe_depth: 0              │
   └──────────────────────────────────────────────────────────┘
   PROBE runs a render on the USER'S VERB, and the user may strike
   any render at the gate before it runs. Authorization is explicit
   and PER-INVOCATION rather than budgeted.

 WHAT A RENDER MAY TOUCH
   candidates/   ✅ a commissioned render lands here, always
   assets/       ⛔ never
   float.tex     ⛔ never
   the status    ⛔ never
   promotion into assets/ and demotion into versions/ is a REVISE
   decision made by the CALLER, never by the renderer.

 WHY THAT ONE RULE MATTERS, live on MISQ
   S-Display-2   candidate C accepted, sitting in candidates/
                 assets/figure.pdf is still v1
                 the compiled paper still shows the OLD figure
   the gap is VISIBLE rather than silent. That is what the rule buys.
```

## Content
### The commissioning asymmetry
Display is the only stage that hands work to independently registered worker skills. Every other stage does its work itself or asks the bank a question.

```
 other stages     do the work, or ask the bank and wait
 display          COMMISSIONS a named worker: -display-table | -figure
                                              | -diagram | -illustration
```

The four renderers stay independently registered skills invoked by name. They are deliberately not part of the display stage's contract, because they must be usable without a paper at all.

### A render is not a bank question
This is the rule that decides the cost, and it is the one that had no home.

```
 a BANK question   goes to task or discovery, costs, and is capped by probe_depth
 a RENDER          is the display stage's OWN step. It is not dispatched to the bank,
                   so it does not spend against probe_depth: 0
```

PROBE runs a render on the user's verb, and the user may strike any render at the gate before it runs. So the authorization is explicit and per-invocation rather than budgeted.

### What a render may touch
A commissioned render lands in `candidates/`. It does not touch `assets/`, `float.tex`, or the unit's status.

Promotion of a winner into `assets/`, and demotion of losers into `versions/`, is a REVISE decision made by the caller, never by the renderer. That single rule is why commissioning a render can never silently change what the manuscript shows.

The MISQ paper is the live proof: `S-Display-2` has an accepted candidate C sitting in `candidates/` while `assets/figure.pdf` is still v1, so the compiled paper still shows the older figure. That gap is visible rather than silent, which is the behavior this rule buys.

## Items to Finish
- [x] 🧭 Rendering is commissioned, not performed
      The four renderers are separately registered skills invoked by name, and the stage declares them in `commissions:`.
- [x] 🛡 A render cannot replace the live asset
      Candidate mode is in the generic output contract: `assets/`, `float.tex` and status are untouched until the caller promotes.
- [ ] 🧠 Rule whether a non-display stage may commission a render
      Section-edit currently FILES a display request and never creates one, which is a ruling on this question that lives in the section-edit contract rather than here.
- [ ] 📐 State the cost rule where a worker reads it
      That a render does not spend against `probe_depth` was written in a stage template and was lost when that template was rewritten on 2026-07-26. It needs a home a fresh agent will find.

## Where we are
The mechanism is implemented and has held: renderers are separate, candidate mode protects the live asset, and the MISQ paper demonstrates the protection working.

The two rules that are NOT written down anywhere durable are the cost rule and whether any stage other than display may commission. Both were carried in prose that has since been rewritten.

## Files
- `paper/1-lifecycle/haipipe-paper-stage/stages/4-display/stage.md`
  Declares `commissions:` and the commissioning asymmetry.
- `display/ref/display-unit-output-contract.md`
  Candidate mode, and the rule that promotion belongs to the caller.
- `paper/1-lifecycle/haipipe-paper-stage/stages/5-section-edit/stage.md`
  `displays: file-only`, the existing partial answer to who else may commission.

## Log
260726 · opened. The cost rule and the candidate-mode protection were carried in the display stage template's "Render and sweep" section, which was replaced when the template became per-asset. Reconstructed here from the removed text and from `commissions:` in the stage contract.
