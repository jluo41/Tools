# PP01-keypress-double-path
state: planned
read: ⬜ nobody has been asked yet
serves: C2.P1.B4
question: On a touch device with an on-screen keyboard, how many characters reach the pseudo-terminal for one key press, and which browser event delivers each one?
route: task
bank: new

## Where each piece lives
- `consumer/q-consumer.md` · what this page loses if the count never comes
- `executor/q-executor.md` · the stripped question, the only thing dispatched
- `executor/a-executor.md` · not written yet
- `proof/manifest.yaml` · `files: []` until EVIDENCE pulls the event log in
