# Two declarations of the same dependency
state: ✅ SETTLED
owner: JL
method: keep one; the one that cannot go stale

## Question
If a stage gives a reading order and its page declares requirements, are those two dependency declarations?

Both exist today and they say roughly the same thing in different words. One is hand-maintained and has been wrong for weeks; the other is generated and carries live gate states. That is not a tie.

## Boundary
- ✅ Covered here
  `inputs:` in the contract versus `requires:` on the page.
- ↪ Covered elsewhere
  What the page does with its dependencies is the Stage Contract block, `QF1`; the ordering it implies is not Pages order, which the board already states.

## Content
### The two forms
```
 stage.md  read_order:        optional craft: which material DRAFT opens first
                              not a dependency graph

 the page  requires:          optional dependency declaration
                              rendered by sync into a Stage Contract that names
                              each source, its GATE STATE, and what it provides
```

### The evidence
The section-edit contract's old `inputs:` included `z-structure`, a dangling architecture path. That stale entry has now been removed rather than copied into the dependency graph.

Meanwhile `requires:` carries something `inputs:` cannot: the upstream page's gate state at the moment of rendering. A stage can therefore see that its input exists AND has not passed its gate, which is a different and more useful fact than a path.

### The honest case for keeping inputs
A reading list is an ORDER, and `requires:` is a set. "Open the venue blueprint before the claims ledger" is craft guidance that a dependency graph does not express. If `inputs:` dies, that ordering has to survive somewhere.

## Law
Dependencies are optional. When a page declares `requires:`, that field is the authoritative dependency graph. A stage may declare optional `read_order:` to preserve writing craft; it states sequence only and cannot create a dependency.

## Items to Finish
- [x] 🧠 Rule which declaration is authoritative
      `requires:` on the page, with `inputs:` deleted; or `inputs:` kept and repointed, with a stated reason for the duplication.
- [x] 📐 If deleted: rehome the reading ORDER
      The sequence DRAFT opens things in is real craft. Say where it lives.
- [x] 🧪 Verify no stage reads a path that does not exist
      Whichever survives, this check should pass and today does not.

## Where we are
Settled and implemented. The two contracts that carried `inputs:` now use `read_order:`; the known dangling `z-structure` entry is gone. A page may leave `requires:` blank without inventing a dependency.

## Files
- `stages/5-section-edit/stage.md`
  Four of five inputs archived.
- `0-lifecycle/5-section-edit/6-results/S-Main-7-results.md`
  The same dependencies, generated, with gate states.
