# Candidates and promotion
state: ✅ SETTLED
owner: JL
method: make visual alternatives reversible until the consumer makes an explicit selection

## Question
When does a render become the visual a reader sees?

A render is a candidate until the consumer approves promotion.
Only the selected output belongs in `assets/`.

## Diagram
```text
recipe/ ──► candidates/A-figure.pdf ──► review ──► assets/figure.pdf
                  │                                   │
                  └──── rejected / superseded ─────► versions/
```

## Content
### Candidate mode protects the live manuscript
Candidate rendering does not change Intake, `assets/`, `float.tex`, or the unit's accepted status.
It is safe to explore different visual forms and emphasis before a decision.

### Promotion belongs to the consumer
Paper Display decides whether a candidate supports the reader's argument.
The renderer may produce alternatives but cannot select one for the paper.

## Items to Finish
- [x] 🅰️ Define candidate-mode write boundaries
      Candidates and candidate recipes are isolated from the selected bundle.
- [x] 🏁 Assign promotion to the caller
      Promotion and demotion are REVISE decisions, not renderer behavior.

## Where we are
The generic output contract prohibits silent replacement of a reader-facing asset.

## Files
- `display/ref/display-unit-output-contract.md`
  Candidate-mode invariants.
- `paper/1-lifecycle/4-display/ref/paper-adapter.md`
  Paper's promotion owner.

## Law
Law: A renderer may propose; the consumer alone promotes.

## Log
260727 · Candidate mode was retained as the reversible boundary before human review.
