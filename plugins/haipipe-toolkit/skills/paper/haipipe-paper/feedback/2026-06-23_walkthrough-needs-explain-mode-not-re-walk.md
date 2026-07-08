---
status: open
created: 2026-06-23
context: Paper-SuitableMessageForRx-JAMANO — user said "go through the whole paper from the beginning, from seed"
fixed_in: ""
---
When the user asked to "go through the whole paper from the beginning, from seed," I (the skill flow) interpreted it as a re-walk-and-EDIT pass: each stage skill ran its illuminate->elicit->gate protocol, surfaced taste decisions, and asked the user to choose changes (venue, pitch refresh scope, hook lead). The user's actual intent was the opposite: "help me understand what we have done before, NOT restart the whole processing."

There is no read-only EXPLAIN / TOUR mode in the lifecycle. Every stage skill is built to MODIFY (illuminate + elicit + gate + write tex). A user who just wants to understand the existing artifacts has no path that doesn't drag them into editing decisions.

Fix: Add an explicit "explain" / "tour" / "walk-through-to-understand" mode to the orchestrator and to each stage skill. In that mode: summarize what THIS paper already has at the stage, in plain language, with no taste questions and no edits. Distinguish it at the orchestrator from the editing re-walk. Likely trigger words: "understand", "explain", "what did we do", "walk me through", "go through ... to understand". The default for "go through the paper" should probably be EXPLAIN, not EDIT.
