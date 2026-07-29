---
status: open
created: 2026-07-28
updated: 2026-07-28
occurrences: 2
kind: defect
context: build.py marker report
lands_in: "build.py"
session: "the 2026-07-27 MISQ §3 Theory + display session (board: examples/Project-Personality-OpioidRx/papers/Paper-Personality2Opioid-MISQ2026/0-lifecycle)"
fixed_in: ""
regressed: ""
---
build.py's marker report scans `sections/*.tex` for `\ref` and never scans the S page's own
Content prose.

Consequence, observed twice in one day: I wrote `Figure~\ref{fig:research-model}` into
S-Main-3's Content at P2.S3, and the checker kept reporting the label as "referenced by no section",
which was true of the tex and useless as a signal. Then JL renamed the label to `fig:theory-model`
and the pointer broke with ZERO warning. The unit README's note that "no sections/*.tex referenced
it, so nothing in the compiled tree moved" was true of the tex and false of the markdown, which did
reference it.

Smallest high-value fix on the board: compare `\ref{}` keys written in markdown Content against
`\label{}` on disk, and report a markdown-side dangling reference separately from a tex-side one.
Testable immediately against `fig:theory-model`.
