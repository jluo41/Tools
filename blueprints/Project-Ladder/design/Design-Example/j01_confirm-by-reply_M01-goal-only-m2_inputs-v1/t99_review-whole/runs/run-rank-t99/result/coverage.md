Coverage · j01 · the kept 1 of 6
================================

by: reviewer agent (context R), who generated and revised nothing in this Job
read: the six design Tasks (each face's ## Design, its elements.yaml, and its run-verify-d0N-v1/result/review.md), the face's n (1), inputs/goal.md, inputs/method.md and inputs/manifest.yaml
rule: M01 m2 ⑤, rank the N + 5 and keep the top N. N = 1, so six are ranked and one is kept.
T3 pretest: the method's ⑤ does not ask for it, so none ran.

The forecasts are placeholders
------------------------------

This Job is a public placeholder example. Every `predicted` value in ranking.csv is a placeholder forecast, in percentage points against the control. It rests on own knowledge alone: the fence (M01 m2 sees the goal only) holds no data, examples or reading to forecast from. None is an observed effect.

The fence names no control. The forecasts assume the control is the channel's current confirm-by-reply message. They should be re-read once the Exp names its control.

The ranking
-----------

All six designs passed their verify of draft 1 (T0 ✓, T1 ✓), so none is left out. The order rests on the goal's one clear ask, read the way t00's first topic reads it: the reply word should be the easiest thing to find, with the slot beside it. How well a reader finds a word is own knowledge, stated here.

1. d01 yes-first · +1.5 pp [+0.4; +2.6] · kept
2. d02 slot-first · +1.2 pp [+0.2; +2.2]
3. d05 thanks-close · +1.0 pp [-0.1; +2.1]
4. d06 question-ask · +0.8 pp [-0.8; +2.4]
5. d03 one-sentence · +0.4 pp [-0.7; +1.5]
6. d04 fewest-words · -0.5 pp [-2.0; +1.0]

Does the kept cover the goal
----------------------------

- **Aim (the reader replies to confirm):** d01 asks for one reply, YES, in its first words after the sender.
- **Who:** it speaks to the reader about "your appointment" and nothing else.
- **Slot:** {DAY} and {TIME} follow the ask directly, so the reader checks the slot where they reply.
- **Leave out:** there is no price, offer or reason for the appointment, no health, account or personal detail, and no urgency word.
- **Shared rules r1.1 to r1.4:** all met on the text, per its verify. It has 71 characters without the slots, opens with "{SENDER}:", ends with "Reply STOP to opt out." and has no abbreviation.

Yes: the one kept design covers the whole goal.

No two alike
------------

With N = 1, only one design is kept, so no two kept designs can be alike. Among the six, d02 and d05 are near-twins: d05 is d02 with "Thank you." added and "it" dropped. d01 and d02 differ only in word order. If N were larger, d05 would not be kept next to d02.

Inputs used
-----------

- **goal.md:** the ask and the slot (d01's ask and slot elements), plus its leave-out list, which the verify checked.
- **rules.md:** r1.2 (the opening) and r1.3 (the stop line) as elements; the verify checked r1.1, r1.4 and the leave-out list on the text.
- **method.md:** the ⑤ rule above.
- **The manifest's other parts:** whose information, its form, examples, tools, reading and the last unit hold nothing for M01 m2, so no design could use them.
- **Own knowledge:** d01 has no own-knowledge element. Only the order of the six and the forecasts rest on own knowledge.

Every fence file is used where it should be.

Why the others drop
-------------------

- **d02 slot-first:** as clear as d01, but YES comes second, after the slot. It is close behind, and the two ranges overlap. It is the natural second arm if N grows.
- **d05 thanks-close:** d02's text with "Thank you." added. The courtesy carries no expected gain and makes the message longer, and as d02's near-twin it adds no new direction.
- **d06 question-ask:** the question invites a reply, but also free-text answers that are not YES ("yes I will", "no"). That widens its range downward.
- **d03 one-sentence:** the ask closes one long sentence, in lowercase after a semicolon, so the reply word is the hardest of the full forms to find.
- **d04 fewest-words:** the shortest, but nothing says what YES confirms; the word for the appointment is absent, as its verify noted. The reader must infer it, and the range reaches below zero.

Dropped designs keep their Tasks; nothing is deleted.

Gaps
----

- **No control in the fence:** see the placeholder note above. Next owner: the goal owner or the Exp setup.
- **The fence's rules.md changed after t00:** each verify review notes this. r1.1 to r1.4 read the same in both versions, so no rank depends on it. Next owner: the Job's inputs setup.
- **d03's element record is malformed:** its "slot and ask" `because` (noted in its verify review). This does not change d03's rank. Next owner: the designer side, through the workflow's projection.
