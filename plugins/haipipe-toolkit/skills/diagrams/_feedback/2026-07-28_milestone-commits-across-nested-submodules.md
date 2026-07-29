---
status: open
created: 2026-07-28
updated: 2026-07-28
occurrences: 1
kind: preference
context: version control
lands_in: "the board skill's operating notes"
session: "the 2026-07-27 MISQ §3 Theory + display session (board: examples/Project-Personality-OpioidRx/papers/Paper-Personality2Opioid-MISQ2026/0-lifecycle)"
fixed_in: ""
regressed: ""
---
JL, verbatim: "can we mark this as a mile stone first."

The paper is nested two submodules deep, so a milestone is three commits: the paper repo, then the
submodule ref bump in the project repo, then in Physician-SPACE. Committing only the paper repo
leaves the milestone invisible from the top level.

What the milestone found, which is the reason to do them at all: 144 uncommitted files and 32M of
untracked work, most of it from EARLIER sessions and entirely unprotected. The restore point mattered
more than the tidy diff.

Two judgment calls worth keeping. Commit on main, because this repo's whole history is direct commits
to main and a branch across three nested submodules complicates the ref bumps for no benefit. And do
not chase a live parallel session: one was mid-write on a probe file, so I committed its FINISHED QA
artifact and left the in-flight file out, saying so in the commit message.
