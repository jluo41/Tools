# j01 · The reader study

job-of: b03_inlab-human (261009)
spine: STUDY mode: `/inlab-human` (0.2.0) with `-bundle`, `-review`, `-report` (0.1.0), the bundle and feedback contracts in `skills/ref/`, and the narrator agent.
close: Each recorded question has a report Page with an answer status, and every answered question names the change that settled it.

## Topic

A clinician reads de-identified cases blind, then assisted: a frozen review_bundle.json (the score from the
endpoint, a narrative from the narrator agent, gold kept apart), one structured row per case in responses.jsonl,
and a report that scores the model and its influence on the clinician. Two rules: the score is deterministic,
and the bundle is frozen. The plugin has no tests.

## Questions

```yaml
questions:
- id: Q01
  title: Is the reader protocol enforced and checked?
  question: Blinding (no score before the blind answer), the bundle's separation of presentation, model output and
    gold, and the response contract are stated in the skills and refs; nothing checks them automatically. What should
    be checked, and where?
  hypothesis: 'A schema check in build_bundle.py and a small test suite: bundle invariants, gold never in the presentation,
    and a review that refuses to reveal before a blind answer is recorded.'
  acceptance: Answered when a broken bundle and a premature reveal each fail a test.
  work: []
  report: reports/q01_protocol_checks/q01_protocol_checks.md
```
