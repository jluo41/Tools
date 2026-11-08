Verify · j03 d02 reminder-one-ask · draft 2
===========================================

by: reviewer agent (context R2), who generated, revised, reasoned or reviewed nothing else in this Job (draft 1 and its revise are the designer agent's, maker context A; verify v1 is context R)
read: runs/run-revise-d02/passes/p01-1108/design.md, elements.yaml and feedback.md (draft 2 = 1 + one revise pass), against inputs/goal.md, inputs/rules.md, inputs/past-designs.md, inputs/method.md and inputs/manifest.yaml. All four fence files match their sha256: goal.md 11a94b37ea87 · method.md 827409845f5e · past-designs.md 63ecf227d9fa · rules.md e19bcaf0ebfe
tests: M02 m1's ④ lists T0 and T1; T2 is not run
verdict: passed (T0 ✓, T1 ✓)

The text
--------

{SENDER}: Reminder of your appointment on {DAY} at {TIME}. Reply YES to confirm. Reply STOP to opt out.

103 characters as written; 84 without the {SENDER}, {DAY} and {TIME} slots. No {NAME} or {LINK} slot appears.

T0 rules · pass
---------------

Goal rules (goal.md):

- one clear ask, reply YES to confirm: pass. "Reply YES to confirm." is the one ask, and YES appears once. The control's second ask ("or call us to change it") is not there. "Reply STOP to opt out." is r1.3's opt-out, not a second ask.
- names the day and time slot as {DAY} {TIME}: pass, on this reading: the day and time are named by the {DAY} and {TIME} slots, which both appear, in that order ("on {DAY} at {TIME}"). A reading that wants the two slots side by side would fail this text, and would also fail both past designs in the fence (P1 and P2 both write "on {DAY} at {TIME}"), so it is not taken here. See the notes.
- leave out prices, offers and any reason for the appointment: pass. None appears; "Reminder of your appointment" names the appointment and gives no reason for it.

Shared rules r1 (rules.md):

- r1.1 at most 160 characters, slots not counted: pass. 84 characters without the {SENDER}, {DAY} and {TIME} slots; the draft's own count (84) agrees. r1.1's list of uncounted slots names {NAME}, {DAY}, {TIME} and {LINK} but not {SENDER}. Counted as written, the text is 92 characters, and a sender's name of up to 76 characters still fits.
- r1.2 opens with who it is from, {SENDER}: pass. The text's first characters are "{SENDER}:". This was v1's failure, and it is fixed.
- r1.3 says how to stop, Reply STOP to opt out: pass. "Reply STOP to opt out." is the last sentence, word for word.
- r1.4 plain words, no abbreviation the reader must decode: pass. There is no abbreviation; YES and STOP are the reply words, written out.
- leave out any health, account or personal detail beyond the slots: pass. Beyond the slots the text names only "your appointment", which is what the goal asks the reader to confirm.
- leave out urgency words (now, last chance, final notice): pass. None appears; "Reminder" is not one of them.

T1 sources · pass
-----------------

The fence files (manifest.yaml) are goal.md, method.md, past-designs.md and rules.md. Each element's from and its locator, read against the file:

- opening "{SENDER}:" from `rules.md · r1.2`: inside. rules.md has r1.2, "opens with who it is from: {SENDER}".
- reminder "Reminder of your appointment" from `past-designs.md · P1`: inside. P1 is the file's section "P1 · the control (arm A)", and its text has these four words verbatim.
- slot "on {DAY} at {TIME}." from `goal.md · rules for this goal`: inside. goal.md has the heading "Rules for this goal", and its second rule names the slot.
- ask "Reply YES to confirm." from `goal.md · rules for this goal`: inside; it is goal.md's first rule.
- stop line "Reply STOP to opt out." from `rules.md · r1.3`: inside; r1.3 says these words.

No element rests on own knowledge. The five elements' words, joined in order, make up the whole text, so every word of the message has a source.

What to change
--------------

Nothing for this verify.

Notes outside the tests (none changes the verdict)
--------------------------------------------------

- The revise changed only what v1 named. Compared with draft 1, {SENDER} now opens the message and the reminder words take P1's form ("Reminder of your appointment on" in place of "Reminder: your appointment is on"). The ask and the stop line are unchanged.
- The element record marks opening and reminder `changed: draft 2` but leaves the slot element's `changed` empty, although its words went from "your appointment is on {DAY} at {TIME}." to "on {DAY} at {TIME}.": the first words moved into the reminder element, and "is" was dropped. The record misses this one change; the text is not affected. Next owner: the designer side, when the element record is projected.
- Two rules were read with a choice, stated above so a later reader can disagree: the {DAY} {TIME} rule as "uses both slots" rather than "the two slots side by side", and r1.1's count with {SENDER} left out (84) or counted (92). Both readings of r1.1 pass. If the stricter readings were meant, the next owners are the goal's owner (new goal wording) and the shared rules' owner (an r2 that names {SENDER}), each through a new inputs version.
- Draft 2 is now the control P1 without its second ask. That matters for the rank (⑤), not for this verify.
