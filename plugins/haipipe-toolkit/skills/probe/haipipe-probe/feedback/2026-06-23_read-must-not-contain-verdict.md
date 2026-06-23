---
date: 2026-06-23
status: fixed
fixed_in: "4.3.0"
source: process audit of P.0623c
scope: fn/read.md + probe.yaml schema
---

# Read must not contain verdict-like content

P.0623c's evidence.md contained "The concordance hypothesis is NOT supported"
and probe.yaml had a result: block with direction: refute. Both are verdict
statements that belong in Judge, not Read.

Read = present the gathered results legibly for the user to internalize.
Judge = decide what claim the evidence supports.

The boundary was stated in SKILL.md but not enforced. The orchestrator agent
(or the monolithic session) wrote the verdict into Read because it was obvious
from the data — but "obvious" is still a judgment call that should be explicit.

Fix ideas:
- Add to fn/read.md: "evidence.md MUST NOT contain phrases like 'supported',
  'not supported', 'refuted', 'confirmed'. Use neutral language: 'the data
  shows X', 'the difference is Y pp'."
- Probe-reviewer should flag verdict-in-Read as a revise item
- The result: block in probe.yaml is only for lean atoms (parent: declared);
  full probes must not embed it at Read stage
