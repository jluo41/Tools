# returned

## Ask

second review of the revised script of K01

## Summary

Now reads I01's gap.csv per group through ctx.result (COLUMNS none), recovers each SE from the symmetric Wald interval, and writes exactly pooling.csv and verdict.json; gate passes on cross. One fix: if I01 refuses a group, ctx.result raises and the run fails ('run it first') instead of refusing; a thinner second group (MDE here sits just under 20) shows it. Refuse with ctx.refuse naming the cut.

## Changed

<nothing>
