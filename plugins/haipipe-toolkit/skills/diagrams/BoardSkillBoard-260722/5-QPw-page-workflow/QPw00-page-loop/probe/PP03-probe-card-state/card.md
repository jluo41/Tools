# PP03-probe-card-state
state: answered-local
read: ⬜ answered 260819 by a local read; a person still has to read a-executor.md and tick this
serves: C4.P6.B5
question: Across this board, how many probe cards exist, how many bibex entries, how many display units, and how many of each have reached the state that means a person has read or accepted them?
route: task
bank: code

## Where the parts are
- consumer/q-consumer.md  the stake, and what this page loses without it
- executor/q-executor.md  the stripped question, and the only thing dispatched
- proof/                  empty until an answer lands

## Values
- v1 · probe cards on the board · 23 · proof/lane-census.json .probe_cards_total
- v2 · cards still at planned · 13 · proof/lane-census.json .probe_by_state.planned
- v3 · cards a person has read · 0 · proof/lane-census.json .probe_read_ticked
- v4 · display units rendered · 10 of 10 · proof/lane-census.json .display_rendered
- v5 · display units accepted · 0 · proof/lane-census.json .display_accepted
