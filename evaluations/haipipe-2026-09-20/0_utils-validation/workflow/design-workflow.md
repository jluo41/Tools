# Current Design workflow

This is a definition view from the current Design owners (v0.4.0). No live Design Folder was supplied, so actual runtime inventory and a human queue cannot be determined. The stable Space ids are goal, design, insight, runtime, delivery; reader-facing names are the five Space names below.

## Workflow list

| Run Spec / type | Actor and target | Action and close rule | Routes | Planned demand |
|---|---|---|---|---|
| commission / Design.commission | Named person; one item exact config version | Release or Hold; preserve exact decision and fingerprint in decision.yaml plus runtime.yaml | release -> generate; hold -> HOLD | C Commission records, at most one release per item |
| generate / Design.generate | Designer agent; one released item | Generate/revise; Result integrity and self-check records must pass; preserve truthful failure | pass -> verify; records-check failure -> generate after person queues revise | N Generate records |
| verify / Design.verify | Fresh independent agent; exact immutable generation Results | Complete coverage of every artifact x criterion; valid pass/fail settles the review | pass -> CLOSE/Delivery ready; valid fail -> generate; records-check failure/unresolved -> verify, person queues review again | J Verify records |

A valid independent fail review is complete with route generate. An invalid or unresolved review is failed with route verify. Neither creates a Commission hold. Commission alone is the bounded human decision Run; comments, clicks, and queue actions are internal interactions and do not add another decision Run.

## Space matrix

| Run Spec | Goal Space | Design Space | Insight Space | Run Space | Delivery Space |
|---|---|---|---|---|---|
| commission | Read-only Brief line and Insight board | Human Release/Hold; exact goal and rules it pins | Read-only pinned insight sources and hashes | Read-only person, time, words, route, same Run receipt | Empty |
| generate | Empty | Read-only latest draft with a clean records check and self-check marks | Empty | Read-only agent, time, verdict n/m, checks, draft, feedback, same Run id | Read-only exact draft after its independent Verify passes |
| verify | Empty | Read-only rule marks of the reviewed draft | Empty | Read-only independent reviewer, time, verdict n/m, checks, same Run id | Empty |

All 15 Cells, including six empty ones, are explicit in design-workflow.json. Cell bindings present or collect the row's declared gate; they never add a gate or Run. The Design owner declares the Spaces and haipipe-workbench-design presents them. Skill bindings are derived from the owner workflow and the utility's worked schema.

Expected count per item is C + N + J, counting allocated records including held, failed, blocked and superseded Runs. On the ordinary path with one release and no earlier hold, C=1 and the expression is 1 + N + J. A first-pass success has C=1,N=1,J=1 (3 Runs); a hold then release then first-pass success has C=2,N=1,J=1 (4 Runs). These are examples, not observed runtime counts. Steps, internal revisions within the frozen target, checks, calls, Results, renderings, and Spaces add no Run identities.

After a candidate passes its independent review and records check, the exact Generate Result becomes ready for Delivery. Delivery projects that draft and its Verify pointer without another approval or Run; Design stops at the handoff. A review that fails the records check (including unresolved coverage) produces a failed Verify receipt, route verify, state verify invalid; the person queues a fresh Verify over the unchanged draft. A valid completed review is not repeated. Candidate changes require a new Generate revise with frozen base and feedback.

## Runs Overview

Not assessed: no actual Design Folder or receipts were supplied. Do not turn the three definition rows into three observed Runs. Runtime rows, when supplied, must include native id, Spec/type, target, actor, status, gate outcome, route, Result, receipt, and projected-in Cells.

## Human Queue

Not assessed: no actual waiting Commission or gate was supplied. A waiting row must point to an existing Run id; no named person or pending decision has been invented.

## Skill Coverage

| Literal skill | Cells | Version | Lines | Evidence |
|---|---|---|---:|---|
| haipipe-design-workflow | commission@goal, commission@design, generate@design, generate@delivery, verify@design | 0.4.0 | 198 | source resolved; quality and field-test ? |
| haipipe-design-unit | generate@design, verify@design | 0.4.0 | 146 | source resolved; quality and field-test ? |
| haipipe-insight | commission@insight | 1.6.0 | 359 | source resolved; quality and field-test ? |
| haipipe-run | commission@runtime, generate@runtime, verify@runtime | 0.26.1 | 693 | source resolved; quality and field-test ? |

Sources: haipipe-design/SKILL.md (roster/count/closure), haipipe-design-workflow/SKILL.md (Specs/routes/Space bindings), its references/run-profile.md (native identity and receipts), haipipe-run/SKILL.md (Run versus Step), haipipe-workbench-design/ref/space-mapping.md (state meanings). Exact source paths and Cell bindings are preserved in design-workflow.json.
