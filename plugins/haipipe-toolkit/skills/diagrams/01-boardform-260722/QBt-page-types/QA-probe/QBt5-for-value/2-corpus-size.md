# Fabricated Corpus size and exclusions

- state:    read
- route:    task
- bank:     ../../../../../../../examples/Fabricated-Project/tasks/T01_corpus-census/QA/1-corpus-size.md
- output: 2-corpus-size.data/size.csv

🚫 FABRICATED, and this one is fabricated on purpose in a way the other is not:
its `- bank:` names a task tree that does not exist. That is not an oversight. It
is what a paper looks like when its executor tree has not been cloned, and it is
the state `unit.py check` must be able to report without pretending.

This record demonstrates the `task` route: the answer was produced somewhere else,
the bank stays there, and this file holds the binding, a digest, and the extract
this paper needs. Nothing from the bank is copied into the paper except the
Caveats.

## Question

How large is the Fabricated Corpus, and how was its page count arrived at?

## Answer

400 pages across 9 boards, after 62 exclusions that are policy rather than error.

The bank left its per-board rows with the census run rather than typing 462 lines
into an answer. This paper needs those rows, so it holds an EXTRACT at
`2-corpus-size.data/size.csv`, 9 rows grouped from the run's 462, with its origin
recorded in `2-corpus-size.data/extracted-from.md`.

The extract is a copy, and it is the only copy this chain makes. Everything
upstream of it may be large, remote, or restricted; everything downstream is small
and lives here. That boundary is deliberate, and on a real paper it is exactly
where an aggregate crosses out of a secure tree while the micro-data never does.

## Caveats

- The 62 exclusions are policy, not error. A different policy gives a different
  denominator, and every rate built on this inherits that choice.
- The extract is a copy. Re-running the census makes it stale, and this record
  returns to `working` until someone re-extracts deliberately. Nothing refreshes
  silently, because a silent refresh moves numbers under a figure a person has
  already accepted.

Copied WHOLE from the bank rather than digested, which is the rule for limits on
any route.
