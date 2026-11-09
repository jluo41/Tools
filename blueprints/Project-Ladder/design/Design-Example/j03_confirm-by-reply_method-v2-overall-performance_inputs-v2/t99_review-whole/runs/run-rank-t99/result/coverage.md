Coverage · j03 confirm by reply, by Overall performance · rank t99
==================================================================

by: reviewer agent (context R2), who generated, revised or reasoned no design of this Job (every draft and the revise are the designer agent's, maker context A; verify d01 v1 and d02 v1 are context R; verify d02 v2 is this context)
read: inputs/goal.md, inputs/rules.md, inputs/past-designs.md, inputs/method.md and inputs/manifest.yaml (all four files match their sha256); the Job face's n (1, the same as goal.md); d01's draft 1 (run-generate-d01), its elements.yaml and its review (run-verify-d01-v1, passed); d02's draft 2 (run-revise-d02 pass p01-1108), its elements.yaml and its review (run-verify-d02-v2, passed)
rule: M02 m1's ⑤, "rank, keep the top N", with N = 1. ⑤ asks for no pretest, so T3 is not run.
kept: d01 reply-first-short. Dropped: d02 reminder-one-ask.
ranked: every design of the Job. Both passed their last verify; none was left out.

The forecasts are placeholders
------------------------------

This is a public example. The e01 results in past-designs.md are synthetic, and every number in ranking.csv is a reviewer's forecast reasoned from them, not a measurement. Each forecast is in percentage points against the control P1 (18.0% replied YES in e01, n 500).

Also, e01's interval for P2 (+1.1 pp [+0.1; +2.1] at n 500 per arm) is much narrower than 500 per arm would give at an 18% rate (about ±4.8 pp at 95%). The ranges here follow the fence's placeholder scale and claim no statistical power.

The ranking
-----------

    rank 1 · d01 · +0.9 pp [-0.2; +2.0] · kept
    rank 2 · d02 · +0.4 pp [-0.6; +1.4] · dropped

The designs are ranked by the centre of each forecast; the lower ends give the same order.

- d01 · {SENDER}: Reply YES to confirm your appointment, {DAY} {TIME}. Reply STOP to opt out.
  It is P2 with the slot written shorter. P2 differed from the control in two ways at once: the ask moved to the front in place of the reminder words, and the second ask ("or call us to change it") was left out. Together those came back +1.1 pp [+0.1; +2.1]. d01 keeps both. The forecast is pulled toward the control because P2 was the better of only two arms, so its result is likely to shrink on a retest (own knowledge). It is widened because e01 did not test the shorter slot (own knowledge).
- d02 · {SENDER}: Reminder of your appointment on {DAY} at {TIME}. Reply YES to confirm. Reply STOP to opt out.
  It is the control P1 without its second ask. It carries one of P2's two changes (one ask) but not the other (the ask in front). e01 cannot split P2's +1.1 pp between the two, so the forecast sits between the control and P2, and its range crosses zero (own knowledge on how the effect splits).

Does the kept design cover the goal
-----------------------------------

Yes, on every line of goal.md:

- aim, the reader replies to confirm: the ask is the first sentence after the sender, "Reply YES to confirm your appointment".
- who, the placeholder audience: nothing in the text narrows the audience or speaks to anyone else.
- venue sms: one message of 66 characters without the slots, or 74 with {SENDER} counted as written.
- n 1: one design is kept.
- leave out prices, offers and any reason for the appointment: none appears.
- one clear ask, reply YES to confirm: one ask, and YES appears once.
- names the day and time slot as {DAY} {TIME}: in exactly that form.
- the shared rules r1.1 to r1.4 and both leave-out lists: passed in d01's verify v1 (T0 ✓, T1 ✓). A recount here also gives 66.

No two alike
------------

Only one design is kept, so no two kept designs can be alike. The two ranked designs are not alike either. d01 puts the ask first and drops the reminder words; d02 keeps the control's reminder opening and puts the ask after the slot. They share only the opening and the stop line, which r1.2 and r1.3 require of every message.

Which inputs were used
----------------------

- goal.md: the coverage check above, and the source of both designs' slot and ask.
- rules.md: r1.2 (the opening) and r1.3 (the stop line) in both designs; r1.1, r1.4 and the leave-out lists as checks.
- past-designs.md: P2's words and its e01 result for d01 and its forecast; P1's words for d02; the control's 18.0% (n 500) as the base both forecasts are measured against.
- method.md: ④'s tests (T0 and T1) for which verifies count, and ⑤'s rule (rank, keep the top N, no pretest).
- manifest.yaml: the four files and their sha256. The parts it marks "nothing" (Information, Tools, Reading, From the last unit) have no file, and this rank needed none.
- own knowledge: the shrinkage of P2's result, the risk of d01's shorter slot, and how P2's effect splits between its two changes for d02. All three are marked as own knowledge above and are not cited as fence sources.

Why d02 drops
-------------

N is 1, and d01 ranks above it. d02's forecast is lower and its range crosses zero. It keeps the control's order, with the ask after the reminder and the slot, and e01 gives no evidence that this order beats the ask in front. d02 keeps its Task and its passed verify and is folded as dropped. Nothing is deleted.

Gaps
----

- M02 m1's ⑤ says "rank, keep the top N" and names no ranking key. This rank uses the forecast against the control (its centre, then its lower end). Next owner: the method's next version, if ⑤ should name its key.
- The Job's own collection Run r02_collect_ranking_rule records a placeholder rule: "rank j03's drafts by how much of the stronger past design each keeps". It is outside the fence (not in manifest.yaml, and its applied_by is empty), so this rank does not use it as a source. It would give the same order: d01 keeps P2's ask word for word, and d02 keeps the control's form. Next owner: the Job's setup, through a new inputs version, if the rule should bind a rank.
- The e01 interval in past-designs.md is narrower than its sample size allows (see the note on placeholders above). Next owner: the fence's author, if a later example is meant to be read as having real statistical power.
