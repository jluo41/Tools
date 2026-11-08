# b01 · Example data request (placeholder)

board-kind: cowork-block
state: 🟡 ACTIVE
owner: Project lead
spine: A placeholder request for a data extract from a partner office, and the review board amendment it needs; every role, date and number is made up.
close: The extract arrives under an approved amendment, and the data-use plan is filed.
status: 2026-11-06 the data owner holds the extract until the amendment is approved; our amendment draft waits to be sent.

## Topic

The cowork prototype: one coordination topic with people, as a cowork Block holds it. Every role, date, ticket and
number is a placeholder; no person or organization is named. It shows each part of a cowork page once.

- `j00_people/` who to ask, by role (📇 reference).
- `j01_data_access_request/` the request to the partner office; the next move is the data owner's.
- `j02_review_board_amendment/` the amendment the extract waits for; the next move is ours. Its Task
  `t01_data_use_plan/` is the data-use plan, written with the review board contact in rounds.
- `j03_kickoff_meeting/` the first meeting with the partner office (✅ done).

Everything sent is in `delivery/`, one folder per message with its attachments. This file and every file of the
example are written by `studio/_build/make_example.py`.

Excluded: running anything on the extract (a work Block's Task); a real request (a Project's own cowork Block).

## Questions

The questions this example Block answers, in two groups.

```yaml
questions:
- id: Q01
  title: What the partner office needs
  group: Needs
  question: What does the partner office need from us before it sends the extract?
  report: reports/q01_partner_needs/q01_partner_needs.md
  work:
  - path: j01_data_access_request
    role: The request and the data owner's reply.
- id: Q02
  title: The retention period
  group: Needs
  question: Which retention period does the data-use plan ask for?
  report: reports/q02_retention_period/q02_retention_period.md
  work:
  - path: j02_review_board_amendment/t01_data_use_plan
    role: The plan, written in rounds.
- id: Q03
  title: What could hold up the extract
  group: Blockers
  question: What could still hold up the extract once the amendment is approved?
  work:
  - path: j01_data_access_request
    role: The data owner's conditions.
```

## Related resources

```yaml
resources:
- title: Request form (placeholder)
  url: https://example.test/request-form
  questions: [Q01]
  contribution: The form the partner office asks every request to use.
```
