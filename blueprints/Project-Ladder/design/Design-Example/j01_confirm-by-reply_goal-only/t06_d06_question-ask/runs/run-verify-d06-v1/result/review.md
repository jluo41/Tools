Verify · d06 question-ask · draft 1
===================================

by: reviewer agent (context R), who generated and revised nothing in this Job (the draft is the designer agent's, maker context A)
read: runs/run-generate-d06/result/design.md and elements.yaml (draft 1; no revise pass exists), against inputs/goal.md, inputs/rules.md and inputs/manifest.yaml
tests: M01 m2's ④ lists T0 and T1; T2 is not run
verdict: passed (T0 ✓, T1 ✓)

The text
--------

{SENDER}: Will you make your appointment on {DAY} at {TIME}? Reply YES to confirm. Reply STOP to opt out.

T0 rules · pass
---------------

- goal · one clear ask, reply YES to confirm: pass. The question and "Reply YES to confirm." call for one reply, YES, which appears once. The STOP line is r1.3's opt-out, not a second ask.
- goal · names the slot as {DAY} {TIME}: pass. {DAY} and {TIME} both appear as slots, in that order ("on {DAY} at {TIME}"). Read as: the day and time come through these two slots. The rule does not say the two must touch.
- goal · leave out prices, offers and any reason for the appointment: pass. None appears.
- r1.1 at most 160 characters, slots not counted: pass. 86 characters without the {SENDER}, {DAY} and {TIME} slots; the draft's own count (86) agrees. r1.1's list of uncounted slots does not name {SENDER}; if the sender's name counts, any name up to 74 characters still fits.
- r1.2 opens with who it is from, {SENDER}: pass. The text starts "{SENDER}:".
- r1.3 says how to stop, Reply STOP to opt out: pass. It ends "Reply STOP to opt out." word for word.
- r1.4 plain words, no abbreviation the reader must decode: pass. There is no abbreviation; YES and STOP are the reply words.
- leave out · health, account or personal detail beyond the slots; urgency words: pass. "your appointment" names only what the goal confirms. No urgency word appears (now, last chance, final notice).

T1 sources · pass
-----------------

- opening "{SENDER}:" from `rules.md · r1.2`: inside; r1.2 is in the fence's rules.md.
- question "Will you make your appointment on {DAY} at {TIME}?" from `own knowledge`: inside. It is allowed and stated openly, matching t00's tone topic. The {DAY} {TIME} slot inside it also rests on goal.md, so this entry claims less than it could; it never claims a source it lacks.
- ask "Reply YES to confirm." from `goal.md · rules for this goal`: inside; it is goal.md's first rule.
- stop line "Reply STOP to opt out." from `rules.md · r1.3`: inside; r1.3 says these words.

Every element's words are found in the text.

What to change
--------------

Nothing for this verify.

Note on the fence
-----------------

inputs/rules.md now hashes to e19bcaf0ebfe, and the manifest moved with it. The fence check recorded c7feb5f9fa6f. r1.1 to r1.4 read the same in both versions, so no verdict here depends on the change. The ladder freezes the fence after t00, so the inputs owner should confirm it.
