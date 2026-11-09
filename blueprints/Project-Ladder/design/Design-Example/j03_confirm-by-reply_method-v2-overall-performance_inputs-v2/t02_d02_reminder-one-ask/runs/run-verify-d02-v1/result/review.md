Verify · j03 d02 reminder-one-ask · draft 1
===========================================

by: reviewer agent (context R), who generated and revised nothing in this Job (the draft is the designer agent's, maker context A)
read: runs/run-generate-d02/result/design.md and elements.yaml (draft 1; no revise pass exists), against inputs/goal.md, inputs/rules.md, inputs/past-designs.md and inputs/manifest.yaml (all four match their sha256)
tests: M02 m1's ④ lists T0 and T1; T2 is not run
verdict: failed (T0 ✗ r1.2, T1 ✓)

The text
--------

Reminder: your appointment is on {DAY} at {TIME}. Reply YES to confirm. Reply STOP to opt out.

T0 rules · fail (r1.2)
----------------------

- r1.2 opens with who it is from, {SENDER}: **fail**. The text opens with "Reminder:", and {SENDER} appears nowhere in it, so the reader is never told who the message is from. P1, whose opening this design keeps, itself opens "{SENDER}: Reminder of …"; the draft kept the word "Reminder" and dropped the sender before it.
- goal · one clear ask, reply YES to confirm: pass. "Reply YES to confirm." is the only ask, and YES appears once. P1's second ask ("or call us to change it") is gone, as the idea intends. The STOP line is r1.3's opt-out, not a second ask.
- goal · names the slot as {DAY} {TIME}: pass. {DAY} and {TIME} both appear as slots, in that order ("on {DAY} at {TIME}"). Read as: the day and time come through these two slots. The rule does not say the two must touch.
- goal · leave out prices, offers and any reason for the appointment: pass. None appears.
- r1.1 at most 160 characters, slots not counted: pass. 83 characters without the {DAY} and {TIME} slots; the draft's own count (83) agrees. There is no {SENDER} to count.
- r1.3 says how to stop, Reply STOP to opt out: pass. It ends "Reply STOP to opt out." word for word.
- r1.4 plain words, no abbreviation the reader must decode: pass. There is no abbreviation; "Reminder", YES and STOP are plain.
- leave out · health, account or personal detail beyond the slots; urgency words: pass. "your appointment" names only what the goal confirms. No urgency word appears (now, last chance, final notice).

T1 sources · pass
-----------------

- opening "Reminder:" from `past-designs.md · P1`: inside. P1's text carries "Reminder" ("{SENDER}: Reminder of your appointment …").
- slot "your appointment is on {DAY} at {TIME}." from `goal.md · rules for this goal`: inside; it is goal.md's second rule.
- ask "Reply YES to confirm." from `goal.md · rules for this goal`: inside; it is goal.md's first rule.
- stop line "Reply STOP to opt out." from `rules.md · r1.3`: inside; r1.3 says these words.

Every element's words are found in the text.

What to change
--------------

- **r1.2:** open the message with {SENDER}, keeping the reminder opening right after it, as P1 does. For example: "{SENDER}: Reminder of your appointment on {DAY} at {TIME}. Reply YES to confirm. Reply STOP to opt out." That is 84 characters without the slots, well inside r1.1. Add the sender as its own opening element, from `rules.md · r1.2`; the reminder words keep `past-designs.md · P1`.
- Change nothing else: the one ask, the slot, the stop line and the sources all pass.

This fix needs no input the fence lacks (r1.2 and P1 are both in it), so it is a revise of this design, not a hold.
