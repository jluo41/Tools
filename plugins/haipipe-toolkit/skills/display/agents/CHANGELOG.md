haipipe-display-unit-agent · Changelog
======================================

Skill-scoped changelog (never loaded at invocation; read on demand). Versions
match the agent's frontmatter `version:`. Newest first.

## 0.1.0 — 2026-08-17

First contract, on JL's 260817 question "我们怎么让它能够自动去产生这些图片呢?
我觉得是不是应该靠一些 sub-agent 之类的?"

**One agent per 🖼 bullet**, because a unit is exactly one bullet's worth of
work, and fanning out per bullet is what makes the render step parallel. The
agent is a PRODUCER only: it resolves the intake, routes the kind through
`haipipe-display`, renders, compiles, looks at the PDF, and writes the README.

Three boundaries, and each is a 260817 failure rather than a precaution:

- **It refuses a bullet whose intake does not exist.** A unit folder that
  exists reads as declared work, and `1 display declared · 0 unit folders` is
  how a page shipped with a sentence in place of the deliverable.
- **It never types a value.** The recipe reads the frozen intake at run time,
  so a printed cell can always be checked against the card's `proof/`.
- **It never judges its own claim.** Both defects found that day rendered
  perfectly: Stata's `="771,449"` split inside the number and delivered 11
  cells where 5 were expected, and a sentence claiming a unique `run_data_`
  prefix was disproved by the very listing the unit froze. A producer asked
  "is my figure right" says yes to both, so the judge is
  `haipipe-board-reviewer-agent`, in its own context.

`looked_at: no` in the receipt is a HOLD, not a pass: a clipped label is
invisible in the source and obvious in the picture, which is how the first
QC4 diagram's diamond was caught eating its own sublabel.
