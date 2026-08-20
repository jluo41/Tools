# PP05-phase-run-time
state: concern
read: ⬜ BLOCKED 260819; two named inputs are missing, see executor/a-executor.md
serves: C14.P2.B4
question: How long does each phase take, measured from the timestamps of stored receipts rather than estimated?
route: task
bank: run · blocked: the receipt shape carries no start/end pair (re-verified 260819 after the PROBE receipt landed with one timestamp), and EVIDENCE and COMPILE have no receipt at all

## Where the parts are
- consumer/q-consumer.md  the stake, and what this page loses without it
- executor/q-executor.md  the stripped question, and the only thing dispatched
- proof/                  empty until an answer lands

## Values
- v1 · phases with a measured duration · 0 · proof/manifest.yaml why_empty
- v2 · blocking inputs named · 2 · no start/end pair in any receipt, PROBE's 260819 one included; no receipt at all for EVIDENCE/COMPILE
