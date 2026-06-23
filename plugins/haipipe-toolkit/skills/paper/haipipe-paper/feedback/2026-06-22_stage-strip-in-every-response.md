---
status: fixed
created: 2026-06-22
context: whole haipipe-paper skill family (orchestrator + enter console + every stage skill); how the assistant closes/opens turns in a paper session
fixed_in: "paper ref/stage-strip.sh + ref/stage-gate.md v2.0.0"
---
how could I make every response with haipipe-paper to have `seed ✅  pitch ✅  claims ✅  narrative ✅  display ✅  minimap ✅  →  write/edit 🔥   →  review ⬜`? add this to the feedback and think about how to do it.

Distilled ask:
- Every assistant response in a haipipe-paper session should carry the lifecycle stage strip, so the user always sees which stage we are in without asking.
- The strip is the canonical spine seed -> pitch -> claims -> narrative -> display -> minimap -> write/edit -> review, with one marker per stage: ✅ done (before current), 🔥 current, ⬜ not started (after current). The current stage = STATUS.md `current_layer`.
- This is the always-on, every-turn version of [console-too-dense-want-stage-progress] (which asked for the strip on first console enter) and the visible half of [stage-advance-needs-user-confirm] (gate rule 5: the console shows the gate). At a stage boundary the 🔥 carries "awaiting your confirm to advance".

Proposed mechanism (layered; pick depth):
1. Single source of truth = STATUS.md `current_layer`. The strip is DERIVED, never hand-typed, so it cannot drift. Precondition: STATUS.md must be kept current (a stale current_layer = a lying strip).
2. Deterministic renderer. A tiny helper (e.g. ref/stage-strip.sh or .py) reads a paper's STATUS.md `current_layer` + the fixed spine order and prints the strip with ✅/🔥/⬜. Skills/console call it instead of typing the strip, so every render is identical and correct.
3. Return-contract rule. Amend the haipipe-paper orchestrator "Specialist Return Contract" and haipipe-paper-enter so the FIRST line of every reply in a paper session is the stage strip (run the helper). Each stage skill inherits this. This is the haipipe-native, no-extra-infra path; it relies on the persistent skill instruction staying in context during the session.
4. (Bulletproof option) A UserPromptSubmit hook. When cwd is inside a paper folder (STATUS.md with current_layer present), the hook injects the freshly-rendered strip as a system-reminder every turn. This guarantees the data is fresh each turn and nudges the model to print it, independent of whether the skill text is still in context. More infra; only if rule 3 proves unreliable.

Recommendation: start with 1+2+3 (source of truth + helper + return-contract rule); add 4 only if it still gets skipped. Note: no Claude Code mechanism can edit the assistant's visible output directly, so "every response" is ultimately a behavioral convention; the helper + return-contract rule + (optional) per-turn hook reminder is the strongest enforcement available.

Update (2026-06-22, placement changed by user): the strip moves from the FIRST line to the LAST line of every reply. It now CLOSES the reply, placed AFTER the machine-readable return-contract tail (status/paper_root/current_layer/next), not opens it. Rule 3 above should read "LAST line", not "FIRST line". Applied: haipipe-paper/SKILL.md section retitled "Stage Strip (end every reply)" with "END every reply ... as the VERY LAST line, AFTER the return-contract tail"; haipipe-paper-enter Output Format now leads with the emoji sections and ends with the strip after the tail. The derive-from-STATUS helper and no-drift rule are unchanged.

Fix:
