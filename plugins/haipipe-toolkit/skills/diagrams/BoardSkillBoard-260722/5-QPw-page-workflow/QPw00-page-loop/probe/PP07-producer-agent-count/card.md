# PP07-producer-agent-count
state: answered-local
read: ⬜ answered 260819 by a local read; a person still has to read a-executor.md and tick this
serves: C12.P3.B3
question: How many producer agents exist on disk for the page workflow's phases, and which phases lack one of their own?
route: task
bank: code · answered locally, no dispatch needed: the count is a read of page-workflows/agents/ and the controller's PRODUCER_AGENTS table

## Where the parts are
- consumer/q-consumer.md  the stake, and what this page loses without it
- executor/q-executor.md  the stripped question, and the only thing dispatched
- proof/                  the census behind the answer

## Values
- v1 · agent files in page-workflows/agents/ · 6 · proof/agent-census.json .agent_files_total
- v2 · phases with a producer agent of their own · 5 · proof/agent-census.json .phases_with_own_producer
- v3 · phases lacking one · 2 (COMPILE, CHECK) · proof/agent-census.json .phases_lacking
- v4 · support agents in skills/board/agents/ · 4 · proof/agent-census.json .support_agent_files
