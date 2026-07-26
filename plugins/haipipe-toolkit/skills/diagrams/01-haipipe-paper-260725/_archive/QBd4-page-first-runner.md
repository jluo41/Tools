# A page-first stage runner
state: ✅ SETTLED
owner: JL
method: resolve one S page, claim one item, dispatch one bounded worker, and write back

## Question
What should `haipipe-paper-stage` do when the Board asks it to work an item or a queue?

The current interface is stage-first and often phase-first, which makes the user remember internal verbs. A Board-first system should supply an S-page path and optional item id, while the runner derives the stage, phase, dependencies, worker, and stop condition from the page and its contract.

## Boundary
- ✅ Covered here
  The runner loop, minimum invocation, routing responsibility, and stop conditions.
- ↪ Covered elsewhere
  The stage contract form is `QE1`; fresh-agent acceptance is `QE2`; the queue schema is `QBd2`.

  ↪ On the boardform board: the board-side entry points that would invoke this runner are `QD1`-`QD3` on the boardform board. This page is the only one of the four that is genuinely paper-side: what `haipipe-paper-stage` does when it is invoked.
## Diagram
```
 THE USER NAMES A PAGE. THE RUNNER DERIVES EVERYTHING ELSE.

  ✗ STAGE-FIRST, often PHASE-FIRST      ✅ PAGE-FIRST
   the user must remember                work --page <S-face> [--item I4]
   internal verbs: which stage,          and nothing else
   which phase, which worker

 THE LOOP
   resolve the page, and its explicit stage key
   load stages/index.yml + ONLY that stage's contract
   read  requires · style-from · Content · queue · comments · state
   select and CLAIM one allowed item
   dispatch the worker declared for its kind
   verify what came back
   write  Content · item handoff · Where we are · state · Board
   continue only if the user asked to work the QUEUE

 WHERE IT STOPS  — five, and all five are deliberate
   🧠 a human decision            ⚠️ an unresolved dependency
   💸 spend authorization         ⚠️ failed verification
   🚪 the CHECK gate

 WHAT CHANGED, AND WHAT DID NOT
   DPRC is still the safety model. It stops being the user's
   remote control: phases become QUEUE SEMANTICS, not vocabulary
   a person has to hold in their head.
```

## Content
### Entry
```text
work --page <S-face-path> [--item <local-id>]
```

### Loop
```
resolve page and explicit stage key
load stages/index.yml and only that stage contract
read requires, style-from, Content, queue, comments, and state
select and claim one allowed item
dispatch the worker declared for its kind
verify the returned result
update Content, item handoff, Where we are, state, and Board
continue only when the user asked to work the queue
```

### Stop
Stop at a human decision, spend authorization, unresolved dependency, CHECK gate, or failed verification.
DPRC remains a safety model, but phases become queue semantics rather than the user's remote-control language.

## Items to Finish
- [x] 🧭 Choose page-first invocation
      The Board provides a page and optional item, not a sequence of internal phase commands.
- [ ] 📐 Give every page an explicit stage key
      The runner must not infer execution logic from filenames, Pages order, or Board family.
- [ ] 🧰 Declare worker routes in each stage contract
      The root runner knows the loop, not the craft of every stage.
- [ ] 🧪 Forward-test three item kinds
      Test one Section edit, one existing Display revision, and one evidence-bearing request.

## Where we are
The loop is designed and recorded.
The live stage skill remains stage-first and has not been compacted around this entry.

## Files
- `haipipe-paper-stage/SKILL.md`
  The runner to narrow.
- `stages/index.yml`
  The stage registry.
- `stages/*/stage.md`
  The permitted worker routes and stop conditions.
