Fence check, recorded again · t00 reason ideas of j01
=====================================================

by: reviewer agent (context R), a reviewer context that generated nothing in this Job (t00's by is the designer agent, maker context A)
why again: pass p01's check read rules.md at sha c7feb5f9fa6f. Within a minute of t00's Result, rules.md was reshaped and the fence frozen again at e19bcaf0ebfe (run-setup-inputs-j01, pass p02). This pass reads every from of t00 against the fence as it stands now.
read: t00_reason-ideas/runs/run-reason-t00/result/chains.yaml (unchanged since t00 closed) against inputs/manifest.yaml (inputs i1, frozen 261106)
checker: `python3 scripts/check_unit.py --ladder-result <Job>/t00_reason-ideas/runs/run-reason-t00` printed `PASS: ladder Result shape, fence and independence` (exit 0). The checker matches only a from's first word, so each locator below was read against the file by hand.
fence now: goal.md 11a94b37ea87 · method.md 0c49ce170f8a · rules.md e19bcaf0ebfe (its link to ../../inputs/i1/rules.md resolves). All three match the manifest's sha256. goal.md and method.md are unchanged since p01.
what moved: rules.md gained a header (rules: r1, signed), a "## Rules" heading and a "## Leave out" list that names the urgency words. Rules r1.1 to r1.4 read word for word as before.

Each topic and step
-------------------

- T1 topic (One clear ask): from `goal.md · rules for this goal`: inside. goal.md is unchanged, and the locator names its "## Rules for this goal" section.
- T1 step 1 (one clear ask, reply YES to confirm): from its topic's `goal.md · rules for this goal`: inside. goal.md's first rule says these words.
- T1 step 2 (the slot as {DAY} {TIME}): from its topic's `goal.md · rules for this goal`: inside. goal.md's second rule names the slot.
- T2 topic (Who it is from): from `rules.md · r1.2`: inside. r1.2 is under the reshaped file's "## Rules" and reads as before.
- T2 step 1 (opens with who it is from, {SENDER}): from its topic's `rules.md · r1.2`: inside. r1.2 says exactly this.
- T2 step 2 (at most 160 characters, slots not counted): from its own `rules.md · r1.1`, which overrides the topic's: inside. r1.1 says exactly this.
- T3 topic (Tone of the close): from `own knowledge`: inside. Even after the reshape, no fence file speaks to a polite close or a question form; the new leave-out list names urgency words, not tone. Own knowledge is stated openly and does not pose as a source.
- T3 step 1 (a polite close or a plain question may make a reply feel easier): from its topic's `own knowledge`: inside.

Failing steps
-------------

none

pass
