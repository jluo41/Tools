---
status: fixed
created: 2026-07-09
updated: 2026-07-09
occurrences: 1
context: enter console / 01_sms_young_male (descriptions frontier)
fixed_in: "haipipe-application-enter 2.2.0"
regressed: ""
---
"you should let me know what probes to release"

The console dashboard reads the probe state (index + per-stage `_EVIDENCE/` cards)
but only surfaced it as a single buried "run PP02" line in Recommended Next. The
user wants an explicit RELEASABLE-PROBES menu on the dashboard: which planned/held
cards are unblocked and awaiting the user's go, which are blocked (and on what),
and which are already read/done. Releasable = status planned AND dependencies met
AND held for review (review-before-release). Suggest a dedicated dashboard block
(or an Open-Needs sub-list) that enumerates each releasable PPNN with its stage,
mode, route, deps, and the exact `/haipipe-application probe run PPNN` command.

Fix: enter SKILL.md 2.2.0 -- new `## Releasable Probes` dashboard section
(between Open Needs and Loopback Diagnosis): one row per planned+deps-met
PPNN (stage, mode, need, deps, exact `probe run PPNN` command) + a one-line
dispatched/read/verdicted roster summary. Never buried in Recommended Next.
