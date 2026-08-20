# a-executor

Run on 260819 against every plan on this board: 17 plans found at `<page>/outline/<stem>-outline-v<N>.md`, highest version per page.

**Plans passing all four checks: 6 of 17** — QPf1-folder, QPf10-skill, QPf2-draw-attach, QPf3-slide, QPf4a-chat-per-question, QPf7-word.

**Per check** (`src/plan_shape.py check()/check_serves()/check_coverage()` per plan, `checks/values.py sweep()` for the value check):

```
coverage   10 plans fail · 30 unserved owing marks   ← fails most often
address     0 plans fail · every serves: names a real bullet
shape       0 plans fail · no plan contradicts its Page Type
value       1 plan fails · QPw00-page-loop, 6 stale quoted values
```

**The coverage failures are concentrated**: QPf4d (9 gaps), QPf4b (8), QPf9 (4), QPf5 (3) carry 24 of the 30; six more pages carry one each. `checks/outline.py` reports the same gaps under "still inside the PREPARE loop" and its overall verdict stays pass, so a coverage gap is an open loop, not a broken page.

**The one value failure is not arithmetic**: QPw00's cards quote run/card/display counts that were true when written and moved when later passes added runs, cards and units. Re-pulling those proofs is EVIDENCE's work.

**Caveat**: only QPw00-page-loop has cards with `## Values` blocks, so the value check is vacuous on the other 16 plans. A plan with no recomputable values passes it by absence, not by verification.
