---
status: open
created: 2026-06-22
context: P.0605 discretion-gradient / Gather->Read (osteo arm session)
fixed_in: ""
---

JL (reporter's words): "为什么 gather 和 read 就在一起了?很快一下就过去了,是不是 read 没有必要独自存在?" — i.e. the moment Gather was wired, Read flipped ✅ in the same strip render, so Read looked like it had no independent existence and the lifecycle jumped Gather→Read→Judge in one motion.

Why it happened this session (mechanism, for whoever fixes it):
- `evidence.md` (the Read artifact) was written EARLY, during the osteo comparison turn, before Gather's arm refs resolved on disk. So Read was already satisfied.
- The strip is a strict left-to-right frontier: it pins the first not-done step as ▶️ and forces every step to its right to ⬜ regardless of whether that step's artifact exists. So Read stayed ⬜ (hidden) until Gather cleared, then snapped to ✅ instantly — looking like Gather and Read "happened together."
- Net: Read was actually done before Gather completed (out of lifecycle order), and the frontier rule masked that until the end.

The real design question this raises: does Read deserve to be its own lifecycle step, or should it fold into Gather?
- Conceptually they differ: Gather = link evidence + every ref resolves; Read = summarize what the gathered numbers say (evidence.md). The map even gives them different done-predicates.
- But in copilot mode you almost always read as you link, so the gap collapses (as it did here). Standalone Read is most meaningful when you Gather many refs without yet synthesizing them.

Fix: skill-owner decision among — (a) MERGE Gather+Read into one "collect + summarize" step (Read becomes an internal sub-action), simplifying the lifecycle to Plan→Gather→Judge→Return; OR (b) KEEP Read separate but enforce ordering so the Read artifact is not written/credited before Gather resolves, and/or have the strip surface "Read artifact present but Gather incomplete" instead of silently hiding it; OR (c) keep as-is and just document that Read routinely collapses into Gather in copilot sessions. Recommend (b): the Read/Judge split is load-bearing, and the confusion is an ordering+visibility bug, not a redundant step.

## Deeper (JL, same day): Read has no "participation"

JL: "read 在用户的感觉上是没有参与感的 … 这个地方是不是停下来,给用户看看结果是什么样的,然后让用户 internalize 呢 … read/judge/return 这三个彼此有重叠,应该好好想想."

Participation lens — who actually ACTS at each step:
- Plan   user frames the claim + picks framing (HIGH; we used AskUserQuestion)
- Gather agent links/calls; user gates costly work (MEDIUM)
- Read   agent writes evidence.md FOR the user (NEAR-ZERO) <- the complaint
- Judge  agent runs gates + proposes verdict; user approves (LOW)
- Return agent files to paper/insight (LOW)
From Gather on it is agent-acts / user-approves. Read is where the agent digests on the user's behalf — but the USER is the one who should internalize the numbers.

The overlap, named (and WHY the splits exist — do not discard the rationale):
- Read   = what did the evidence say?            (descriptive)
- Judge  = what claim can we honestly make?      (normative)  <- split from Read ON PURPOSE as an anti-overclaim guardrail
- Return = where does the verdict go?            (propagation) <- split to force deliberate filing, not auto-push into the paper
The conceptual splits are sound; the problem is the FELT experience, not the concepts.

Observed this session: the participatory part was the live chat (show OLS -> "show C2/C3/C4" -> "what about IV" -> "report robust"). That ad-hoc back-and-forth WAS Read+Judge, and it felt participatory; the formal evidence.md / verdict.md lagged and felt like bookkeeping. Lesson: design the participation INTO the lifecycle, don't leave it to chat.

Fix (revised): keep the conceptual model, redesign INTERACTION OWNERSHIP —
  - Make Read an explicit STOP-and-INTERNALIZE gate: agent's job = make the evidence legible and PRESENT a results panel (numbers + a visual); user's job = absorb + react; the reaction is the input to Judge. Read becomes the MOST participatory step, not the least.
  - Re-tag each step by who drives it (user / joint / agent) so the felt flow matches the lifecycle.

## Decision (JL, same day): Read elevate AGREED; Judge/Return STAY SEPARATE; rename Return

- Read-as-stop: AGREED, proceed.
- Judge vs Return: do NOT fuse (reversed the earlier "consider fusing"). JL: "judge 像 claim,return 像沉淀" — Judge = make the claim; the last step = let that judged knowledge 沉淀 (settle and accrue) into the durable record (insight KB + backfill the source). Two distinct acts.
- RENAME "Return" to a word carrying 沉淀 / settling-deposit meaning. Candidates + trade-offs:
    Deposit     literal 沉淀/沉积; short; PLACES knowledge into the store; no clash with Judge   <- RECOMMEND
    Consolidate memory-consolidation = experience made durable/accrued; precise; 4 syllables, breaks the short-verb rhythm
    Distill     沉淀下来的精华 = keep the essence; evocative; leans "compress" more than "place"
    Settle      nicest sediment imagery BUT collides with Judge ("settle a question" = decide) -> AVOID, it reblurs the very split JL wants
  NOT "Archive" — too cold/cold-storage, loses the accrual/foundation sense of 沉淀.
- Refactor only after the word is locked: SKILL.md verb list + Commands, ref/lifecycle-map.md, fn/return.md (-> fn/<word>.md), ref/stage-strip.sh labels + return.md predicate, console router alias table. Keep `return.md` filename or rename consistently.

## Refinement (JL, same day): crisp Gather-done + participant manifest before Read

JL: "什么时候 gather 结束 ... 就是 task 和 discovery 跑完了,gather 就算结束了,然后说一下哪些 task 或者 discovery 参与了,然后才是读."

- Gather is DONE iff every PARTICIPATING task AND discovery has FINISHED RUNNING (and every linked existing artifact resolves) -- not merely when refs are declared. "Called but still running / pending" = Gather NOT done. (Strengthens the strip's current predicate, which only checks ref resolution.)
- At the Gather->Read boundary, STATE THE ROSTER: one line naming which tasks / discoveries actually participated (the evidence that ran). This manifest IS the boundary marker.
- That roster is exactly what Read then presents for the user to internalize -- which is what gives Read its participation. Handoff: "these N tasks/discoveries ran -> here is what they say (Read = stop + internalize)."
- Felt sequence becomes: Gather (collect; ends with "X, Y, Z ran") -> Read (present those results; user absorbs) -> Judge (claim) -> Deposit/沉淀 (settle into durable KB + backfill source).

Implication: strip Gather-done predicate should require task/discovery COMPLETION; console should emit the participant manifest as the Gather->Read transition line.
