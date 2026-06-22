---
status: fixed (structure-claims two-stage gate + delivery-need.md drain loop)
created: 2026-06-22
context: haipipe-paper-claims (claim lifecycle stage); how it should orchestrate haipipe-probe -> haipipe-task + haipipe-insight for solid evidence. Extends 2026-06-22_claims-ledger-thin-no-status-no-evidence.
fixed_in: ""
---
feedback for the claim in the lifecycle, the content is so thin, you need the solid evidences to support it!! plesae think about how to use haipipe-probe to call haipipe-insight and haipipe-task to make this better, you can also learn to borrow the ideas from Tools/references/academic-research-skills or Tools/references/aris

Distilled ask:
- The claim stage produces thin content; a claim is not done until SOLID evidence backs it.
- The claims skill should not just list status/source; it should drive an evidence-gathering ORCHESTRATION: haipipe-probe as the conductor that calls haipipe-task (compute the result) and haipipe-insight (preserve judged meaning/caveat), then backfills a confirmed verdict into the claim row.
- Borrow concrete ideas from Tools/references/academic-research-skills and Tools/references/aris for how rigorous claim/evidence/citation work is structured.

Why this matters (links): extends [claims-ledger-thin-no-status-no-evidence]. The earlier item said the ledger lacks status + quantified evidence; this item says the FIX is an orchestration: probe(plan->gather->read->judge->return) where gather calls task/discovery and return files insight, so every claim row traces to a confirmed probe verdict + an insight card, not a "planned Table".

Suggested fix direction (skill, later pass):
- Make haipipe-paper-claims emit, per weak/GAP claim, a concrete probe contract (claim + evidence needed) and route it: /haipipe-probe plan from-need. Probe Gather calls /haipipe-task (run-X regression) and /haipipe-discover (lit anchor); probe Return files /haipipe-insight (K card) and backfills the verdict path + quantified result into the claim row.
- Adopt the reference libraries' rigor patterns (see the design proposal produced this session): explicit evidence grading, claim-evidence-citation linkage, falsification/limitation per claim.
- A claim row done-rubric: status + confirmed probe verdict ref + quantified result + insight card ref + caveat. No "planned" anchors.

Concrete borrows from aris (Tools/references/aris) -- mapped to the haipipe stack:
- TWO-STAGE EVIDENCE GATE (aris shared-references/evidence-precheck.md + tools/evidence_check.py):
  stage 1 = deterministic, no-model, fail-closed: does the cited table path exist AND does the cited number actually appear in it? Catches "planned Table 1" / hallucinated anchors for free. stage 2 = cross-model jury: does the real number SUPPORT the claim. "verified != correct": existence is execution-completeness, support is the quality verdict.
  -> haipipe gap: probe Judge already has stage 2 (probe-integrity-auditor-agent + claim-verifier-agent, builder!=judge). The MISSING piece is stage 1. Adopt evidence_check.py as a deterministic pre-gate in probe READ. Run it on the current 5 claims today -> all fail (planned anchors absent) -> honest GAP, zero model cost.
- result-to-claim (aris): after a task run, a verdict gate judges what the results support / don't / what's missing, then routes pivot|supplement|confirm. ~ our claim-verifier-agent. Run ONCE per result change, never on a timer.
- kill-argument (aris): adversarial single-most-damaging-rejection pass (200-word reject memo -> point-by-point defense) before a headline claim is accepted. haipipe has reviewers but no explicit kill pass -> add it to probe Judge for headline claims.
- citation-audit (aris): every external lit anchor (discovery) mechanically checked -> use for the C5 / literature-anchor side.
- falsification per claim (already in our probes/0622 probe.yaml) -> require a falsification line on every claim row.
- zero-context fresh reviewer (aris paper-claim-audit): judge with NO prior context to kill confirmation bias -> the haipipe builder!=judge rule already enforces this; keep it.

Orchestration (probe as conductor): 2-claims emits need -> /haipipe-probe plan (claim+falsification+run-X table:value) -> GATHER /haipipe-task (run regression) -> READ stage-1 evidence_check (existence) -> JUDGE stage-2 integrity+claim-verifier+kill-argument (support) -> RETURN /haipipe-insight K card + backfill the claim row (status, verdict path, table:value pre-checked, insight ref, caveat).

Fix:
