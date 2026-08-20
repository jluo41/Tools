# PP04-auditor-verdict
state: answered-local
read: ⬜ answered 260819 by running the auditor; a person still has to read a-executor.md and tick this
serves: C13.P1.B5
question: What does the deterministic lifecycle auditor return for each stored run, and which fault codes does it emit?
route: task
bank: code

## Where the parts are
- consumer/q-consumer.md  the stake, and what this page loses without it
- executor/q-executor.md  the stripped question, and the only thing dispatched
- proof/                  empty until an answer lands

## Values
- v1 · runs audited · 4 · proof/auditor-verdicts.json, one key per run
- v2 · runs that PASS · 0 · proof/auditor-verdicts.json, no key with an empty list
- v3 · findings in total · 8 · proof/auditor-verdicts.json, summed
- v4 · distinct fault codes · 5 · artifact-version-mismatch, checked-version-mismatch, max-steps-exceeded, page-path-stale, version-continuity
- v5 · real contract violations · 1 · checked-version-mismatch at 260818-1543 receipt[2]
