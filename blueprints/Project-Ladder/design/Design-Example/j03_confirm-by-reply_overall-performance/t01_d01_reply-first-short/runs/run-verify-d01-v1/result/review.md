Verify · j03 d01 reply-first-short · draft 1
============================================

by: reviewer agent (context R), who generated and revised nothing in this Job (the draft is the designer agent's, maker context A)
read: runs/run-generate-d01/result/design.md and elements.yaml (draft 1; no revise pass exists), against inputs/goal.md, inputs/rules.md, inputs/past-designs.md and inputs/manifest.yaml (all four match their sha256)
tests: M02 m1's ④ lists T0 and T1; T2 is not run
verdict: passed (T0 ✓, T1 ✓)

The text
--------

{SENDER}: Reply YES to confirm your appointment, {DAY} {TIME}. Reply STOP to opt out.

T0 rules · pass
---------------

- goal · one clear ask, reply YES to confirm: pass. "Reply YES to confirm your appointment" is the only ask, and YES appears once. The STOP line is r1.3's opt-out, not a second ask.
- goal · names the slot as {DAY} {TIME}: pass. The text has "{DAY} {TIME}", exactly the rule's form.
- goal · leave out prices, offers and any reason for the appointment: pass. None appears.
- r1.1 at most 160 characters, slots not counted: pass. 66 characters without the {SENDER}, {DAY} and {TIME} slots; the draft's own count (66) agrees. r1.1's list of uncounted slots does not name {SENDER}; if the sender's name counts, any name up to 94 characters still fits.
- r1.2 opens with who it is from, {SENDER}: pass. The text starts "{SENDER}:".
- r1.3 says how to stop, Reply STOP to opt out: pass. It ends "Reply STOP to opt out." word for word.
- r1.4 plain words, no abbreviation the reader must decode: pass. There is no abbreviation; YES and STOP are the reply words.
- leave out · health, account or personal detail beyond the slots; urgency words: pass. "your appointment" names only what the goal confirms. No urgency word appears (now, last chance, final notice).

T1 sources · pass
-----------------

- opening "{SENDER}:" from `rules.md · r1.2`: inside; r1.2 is in the fence's rules.md.
- ask "Reply YES to confirm your appointment" from `past-designs.md · P2`: inside. P2's text carries these words verbatim, and its result line (+1.1 pp against the control) is the `because`.
- slot "{DAY} {TIME}." from `goal.md · rules for this goal`: inside; it is goal.md's second rule.
- stop line "Reply STOP to opt out." from `rules.md · r1.3`: inside; r1.3 says these words.

Every element's words are found in the text.

What to change
--------------

Nothing for this verify.
