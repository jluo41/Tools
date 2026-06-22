---
status: open
created: 2026-06-22
context: whole lifecycle flow (haipipe-paper-lifecycle router + haipipe-paper-enter console + every stage skill seed/pitch/claims/narrative/display/minimap); felt while moving through stages on Paper-Personality-Opioid-MedJournal
fixed_in: ""
---
我觉得还有一个问题，就是我感觉进入 Lifecycle 的一个 stage 后，还没怎么着，系统也不通知我什么时候出来，或者说没有让我 confirm 什么时候这个 stage 算是 over 了。我觉得这是一个很大的问题。我的 point 是：应该让我 confirm 这个 stage 是不是 ready 了，才进入下一个 stage。现在感觉系统是迫不及待地进入下个 stage 了，这个体验不好。

Distilled ask:
- The lifecycle has NO stage-transition gate. After working in a stage, the system slides into the next stage on its own. It never (a) announces "this stage is done" nor (b) asks the user to confirm before advancing. It feels impatient / eager.
- The user wants an explicit CONFIRM-BEFORE-ADVANCE gate at every stage boundary: a stage is only "over" when the user says so. The system must stop at the boundary and wait, not auto-proceed.
- This is the user-control complement to the two existing items: [console-too-dense-want-stage-progress] introduced the left-to-right stage strip with one-by-one check-off, and [pitch-skill-no-structure-gate] asked for a per-stage done-rubric. This item ties them together: the strip's "checked off" transition must be a USER-CONFIRMED gate, and the per-stage done-rubric is what the gate checks.

Proposed solution -- a Stage Gate protocol (one shared convention, applied by every stage):
1. Exit criteria per stage. Each lifecycle stage gets an explicit "definition of done" checklist (generalizes the pitch done-rubric to seed/claims/narrative/display/minimap). Lives in a shared ref doc, e.g. ref/stage-gate.md, with a per-stage criteria table.
2. Gate, don't glide. When a stage's artifact resolves, the stage skill PRESENTS its done-criteria with per-item ✓/✗ and STOPS with one question: "Stage <X> looks ready (criteria below) -- confirm to close it and move to <next>?" It does not touch the next stage until the user confirms.
3. STATUS is the latch. Only on explicit user confirm does STATUS.md advance current_layer -> next_layer. current_layer/next_layer already exist; this makes the transition gated rather than implicit.
4. Autonomy policy. In ref/delivery-need.md's AUTO-vs-PAUSE classification, "stage transition" is always a PAUSE gate. Work WITHIN a stage can be autonomous; crossing a stage boundary cannot.
5. Console shows the gate. haipipe-paper-enter renders the stage strip with a clear ACTIVE marker and an explicit "awaiting your confirm to advance" cue at the current boundary; it never reports a later stage as started unless STATUS was advanced by confirm.

Where it touches:
- new ref/stage-gate.md (protocol + per-stage exit-criteria table).
- each stage skill (seed/pitch/claims/narrative/display/minimap): add an "Exit Gate" section -> present criteria, ask, wait.
- haipipe-paper-lifecycle (router) + haipipe-paper-enter (console): enforce present-gate -> await-confirm -> advance-STATUS; forbid auto-advance.
- subsumes [pitch-skill-no-structure-gate] (pitch's content rubric becomes its exit criteria) and complements [console-too-dense-want-stage-progress] (the strip visualizes the gated transitions).

Update (2026-06-22, sharpened by the user):
- The gate was NEVER enforced. In the current paper the lifecycle advanced all the way to write-edit without the user confirming a single stage. So a current_layer reached without per-stage confirmation is ILLEGITIMATE, not just suboptimal.
- Requirement: an EXPLICIT confirm to exit each stage AND enter the next. Two-sided: "stage X done?" then "open stage Y?". The system must stop at every boundary, not only announce.
- Recovery action the user wants now: RESET the paper to the beginning (current_layer -> seed) and RE-WALK the spine one stage at a time, recording each confirmation. Resetting does NOT delete artifacts (pitch/claims/displays already exist on disk); it resets the GATE/confirmation state so each stage is re-validated and explicitly confirmed before advancing.
- Implication for STATUS.md: it needs a per-stage confirmation ledger (stage -> confirmed? -> date), separate from current_layer, so "confirmed" is tracked, not assumed. current_layer may only advance when the prior stage's ledger entry is user-confirmed.
- Ties to [stage-strip-in-every-response]: the every-turn strip must reflect the LEDGER (✅ only for user-confirmed stages), not just "artifact exists on disk".

Fix:
