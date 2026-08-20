# PP01-phase-contract-count
state: answered-local
read: ⬜ answered 260819 by a local read; a person still has to read a-executor.md and tick this
serves: C1.P2.B3 · C4.P2.B4 · C4.P3.B6
question: How many phases does the page workflow declare, how many of them ship a contract file, and how many person-reserved ticks does the set of contracts define?
route: task
bank: code · answered locally, no dispatch needed: the count is a read of page-workflows/

## Where the parts are
- consumer/q-consumer.md  the stake, and what this page loses without it
- executor/q-executor.md  the stripped question, and the only thing dispatched
- proof/                  empty until an answer lands

## Values
- v1 · phases the loop declares · 7 · proof/phase-census.json .phases_declared
- v2 · contracts that ship · 6 · proof/phase-census.json .contracts_shipping
- v3 · person-reserved ticks · 5 · proof/phase-census.json .person_reserved_ticks
- v4 · runs executed · NOT HERE · owned by PP02-run-receipt-coverage
