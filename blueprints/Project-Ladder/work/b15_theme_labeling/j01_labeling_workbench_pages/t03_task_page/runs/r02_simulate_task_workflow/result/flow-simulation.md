# Flow simulation · the labeling Task pages (261101)

JL 261101: "how easy they will be used, could you simulate to use it as well? To make sure the whole work flow follow
with what we desinged". Two parts: one meaning loop run for real with the actual tools, in a demo copy of the meaning
Task (`demo/`), and the whole flow walked on the drawn views (s58), by me and by a blind user simulation.

## 1 · Loop 3, run for real (demo/t03_dices350_response_safety_meaning)

```text
step          what was done                                         tool                     written
Report        report-03 written as a form: 3 cards, cases beside    collect.py new, build    runs/r01_collect_report_m03/
              each, no option pre-ticked                                                     question_collection.md, .html
Preferences   answered in Chrome as JL: Q1 A + note, Q2 A,          the form                 (the copied text)
              Q3 Defer + note; Copy feedback
(the chat)    the copied text saved, as the agent would             collect.py save          result/answer_collection.md
Update        guideline m03 as a mind map, each rule citing its     /haipipe-mindmap render  meaning/m03.mindmap.md, .html
              answer; L04 none → low; flags on the form             collect.py applied       gold/versions/l03/, applied.md
```

Works with today's tools: the report as one collect Run; a card with no pick; cases beside the question (the card's
sketch); your own rule (✍ My own decision); defer (an option); save; the guideline as a mind map; every rule of m03
traced to the answer that made it; Q1 and Q2 flagged ✅ applied, Q3 ⏳ in progress (Loop 4's report).

Gaps /haipipe-labeling-interaction must fill on top of /haipipe-interaction:

1. The form's head says "My pick is selected" though labeling cards start with none.
2. The answer file says "Answer: A, changed from my pick ." when a card had no pick.
3. The answered form still shows Copy feedback (the skill says it hides).
4. The decision record's scope and version have no field; only the note carries them.
5. Card states (Needs your judgment, Draft saved, More evidence requested) do not exist; a form is waiting or answered.

## 2 · The whole flow, walked on the drawn views

```text
#   view           you do                               the chat does                 you see next
1   D3 Evaluate    read the round report row            (round e02 already routed)    no link to meaning ❗
2   C2 Report      Copy prompt, paste                   writes report-03 (a form)     C2 row, inbox, Job 🙋
3   form / C3      answer, Copy feedback, paste         saves the answers             rows say Answered
4   C3             Copy prompt, paste                   (repeats 3) ❗                 nothing new
5   C4 Update      Copy prompt, paste ❗ (or from 4)     m03, l03, flags               C4, the form's flags
6   D1 Rewrite     Copy prompt, paste                   e03                           D1
7   D2 Run         Copy prompt, paste ❗                 labels on Train and Test      D2
8   D3 Evaluate    Copy prompt, paste ❗                 round report e03, its route   D3, or D4 when met
9   D4 Release     Sign release                         freezes h01                   E1
10  E2 Audit       review risky cases; View issue       (issue for meaning)           no link to meaning ❗
```

One meaning loop costs four pastes into the chat and three of them carry no decision; one expression round costs
three pastes for a loop that never asks.

## 3 · Findings

1. **Two sends in Preferences.** The form's Copy feedback and C3's Copy prompt both paste into the chat; the second repeats the first.
2. **Update starts twice.** C3's prompt ends "then start Update", and C4 has its own Update prompt.
3. **Expression round: three prompts, no decision.** D1, D2 and D3 each need a paste though the loop never asks you.
4. **No link across Tasks.** D3's round report and E2's audit issue point to meaning's Report, but neither has a link to it.
5. **Mock data disagreed.** D3 said "2 wrong labels, 1 rule gap" while report-03 holds one label card and two rule cards.

## 4 · A blind user simulation (a fresh agent playing JL, from the 11 screens)

```text
task                                   actions   ease   stalled on
T1 frame the label (C1)                6 + 3     3/5    which chat to paste into
T2 Loop 3, from round report e02 (C2-C4) 20-22   2/5    no link from D3; is m03 approved?
T3 a new expression round (D1-D3)      9         4/5    three pastes for steps that ask nothing
T4 release, scale, audit (D4, E1-E3)   20        2/5    Sign clickable before criteria; open T07 unseen
```

Rules: (a) only meaning asks: holds in D1 to D3, bends at E2, where you check items inside scanning; (b) every step
has a prompt: holds, but the session line named no session; (c) answers recorded and traceable: half, C4's decision
named no card and Q2's outcome (L04) was missing; (d) the round report goes back to meaning: the send holds, following
it had no link and the counts disagreed. Its top five: the session placeholder; D3 to C2 with no link and untagged
cards; no approve control in Update; E3 signing over an open issue; duplicate triggers (two Update prompts, Copy
prompt beside a greyed Start batch).

## 5 · What changed, and what waits

Fixed in the views (task_views.py, labeling_ui_cells.py), no question needed:

1. D3's round report row and E2's audit issue open meaning directly: "Open in meaning".
2. Each card says which round report sent it (· e02); the counts agree: 1 wrong label, 2 rule gaps.
3. Update names its cards: "Q1 · A safe refusal counts as none"; L04 now low (Q2); Q3 deferred to Loop 4.
4. A sign whose condition is not met is greyed: Sign release until the criteria pass; Sign the delivery while T07 is open.
5. Each prompt names its Task's chat session (dices350-safety-meaning, -expression, -scanning, …).
6. Scanning starts from its prompt only (no second Start batch button); release h01 is spelled out (m03 · e03 · l03 · x02).
7. Run's table agrees with its strip (one model still running).

Asked of JL in the waiting form, r01_collect_task_work_views (Q5 to Q7): one send in Preferences; an Approve m03 sign
in Update; a whole expression round from one prompt.

For the /haipipe-labeling-interaction build (section 1's five gaps); for later rounds: D3 comparing e02 with e01; a
link from D4's sign to its evidence; C1 before its step, with its orange bar.
