# PP02-run-receipt-coverage
state: answered-local
read: ⬜ answered 260819 by a local read; a person still has to read a-executor.md and tick this
serves: C12.P2.B3
question: Which runs are stored under the board's _runs/page/ tree, how many receipts does each hold, and which phases appear across all of them?
route: task
bank: code

## Where the parts are
- consumer/q-consumer.md  the stake, and what this page loses without it
- executor/q-executor.md  the stripped question, and the only thing dispatched
- proof/                  empty until an answer lands

## Values
- v1 · runs stored · 4 · proof/run-index.json .runs_total
- v2 · receipts across all runs · 24 · proof/run-index.json .receipts_total
- v3 · phases covered by any run · 6 of 7 · proof/run-index.json .coverage
- v4 · phases never executed · 1 (COMPILE) · proof/run-index.json .phases_never_run
