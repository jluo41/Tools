# Design-Example · Example reminder message

board-kind: design-board
channel: sms
spine: A placeholder design Block. One application (an example reminder message), one channel (sms), one signed goal made by the simplest registered method, so a reader sees every view, section and state a real design Block shows. Every word here is a placeholder.
close: every goal's kept designs released

## Topic

The prototype of a design Block on the ladder: one goal, one Job (goal × method version × inputs version → N
designs), its Tasks (t00 reason ideas, one per design, t99 review whole) and their Runs. Nothing in it names a real
application, person or organization; its inputs version is a short synthetic file.

```text
Design-Example/
├── board.md · design-goal.md        the goal list and the shared rules, each signed with a date only
├── inputs/i1/                       one synthetic inputs version, frozen
├── j01_confirm-by-reply_goal-only/  G01 × M01 m2 × i1 → N = 1
└── delivery/                        the Block's one-page summary; the release waits on a person
```

## Goals

```yaml
goals:
- id: G01
  name: confirm-by-reply
  aim: The reader replies to confirm an upcoming example appointment
  who: example recipients with an upcoming example appointment (a placeholder audience)
  venue: sms
  n: 1
  rules:
  - one clear ask, reply YES to confirm
  - names the day and time slot as {DAY} {TIME}
  leave-out: prices, offers and any reason for the appointment
  signed: ✅ 261106
- id: G02
  name: reschedule-early
  aim: The reader who cannot come reschedules before the day instead of missing it
  who: example recipients with an upcoming example appointment (a placeholder audience)
  venue: sms
  n: 1
  rules:
  - one clear ask, reply R to reschedule
  leave-out: '?'
  signed: ''
```

## Questions

```yaml
questions:
- id: Q01
  title: Which design goes to the example test?
  question: Which kept design of the Block should an example test send, and does its frozen prediction hold?
  hypothesis: The kept design of the goal-only Job is the one to send; its prediction is checked once an example test returns per-arm totals.
  acceptance: Answered when the kept design is released and an example test's per-arm totals are scored.
  work: [j01_confirm-by-reply_goal-only]
  report: reports/q01_example_test/q01_example_test.md
```
