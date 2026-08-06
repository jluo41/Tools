# Drift counts by type-key tenure

- state:    answered
- route:    local
- provides: 1-drift-counts.data/counts.csv

🚫 FABRICATED. No corpus was counted. The FORMAT is what this file teaches.

`route: local` means the answer was produced here and there is no bank elsewhere,
so this file IS the original. On a real paper most records carry `route: task` or
`route: discovery` and a `- bank:` path instead; then the answer lives in that
task or discovery tree, this file holds only the binding and a digest, and
`source/build.py` extracts from the bank rather than from this file. The bank is
never copied into the paper.

## Question

Across the Fabricated Corpus, how many pages drifted from their contract in the
last release window, split by how long the page has declared a type key?

## Answer

Five tenure bands, counted once over the whole corpus. A drift event is one
release in which a page's rendered sections stopped matching the sections its
contract declares.

```text
  band                        pages   drift   ci_low   ci_high
  ─────────────────────────────────────────────────────────────
  inferred from filename        214      37     14.2     20.4
  key declared 0-3 months        61       9     10.1     19.4
  key declared 4-6 months        48       4      4.6     12.8
  key declared 7-12 months       44       2      1.9      8.7
  key declared 13+ months        33       1      1.1      7.2
```

This table is the ONE place these numbers are typed. `counts.csv` is parsed out of
it, never retyped, and the parse requires every line inside the fence to match or
it fails. Proven by changing `48` to `4B` and watching the build exit 1.

## Caveats

- Tenure is not assigned. A page declared its key whenever its author got to it,
  so early declarers may differ from late ones in ways this count cannot see.
- No control for page size, and longer pages have more sections to drift.

Anything built on this answer says ASSOCIATION, never REDUCES.

On a `task` or `discovery` route these limits are the one thing copied WHOLE from
the bank rather than digested. A digest of an ANSWER is a convenience; a digest of
a LIMIT is how a paper ends up claiming more than its design supports.
