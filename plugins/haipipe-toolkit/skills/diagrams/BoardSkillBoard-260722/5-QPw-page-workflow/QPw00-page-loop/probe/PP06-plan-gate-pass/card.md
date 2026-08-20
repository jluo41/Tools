# PP06-plan-gate-pass
state: answered-local
read: ⬜ answered 260819 by running the four checkers locally; a person still has to read a-executor.md and tick this
serves: C2.P3.B5
question: How many outline plans on this board pass all four self-consistency checks, and which check fails most often?
route: task
bank: code · answered locally, no dispatch needed: the four checkers already exist and run on this repo

## Where the parts are
- consumer/q-consumer.md  the stake, and what this page loses without it
- executor/q-executor.md  the stripped question, and the only thing dispatched
- proof/                  the census behind the answer

## Values
- v1 · outline plans on the board · 17 · proof/plan-gate-census.json .plans_total
- v2 · plans passing all four checks · 6 · proof/plan-gate-census.json .plans_passing_all_four
- v3 · plans failing coverage · 10 · proof/plan-gate-census.json .fails_by_check_counts.coverage
- v4 · plans failing address · 0 · proof/plan-gate-census.json .fails_by_check_counts.address
- v5 · plans failing shape · 0 · proof/plan-gate-census.json .fails_by_check_counts.shape
- v6 · plans failing value · 1 · proof/plan-gate-census.json .fails_by_check_counts.value
