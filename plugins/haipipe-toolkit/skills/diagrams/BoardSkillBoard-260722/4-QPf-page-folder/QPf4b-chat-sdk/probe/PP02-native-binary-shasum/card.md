# PP02-native-binary-shasum
state: planned
read: ⬜ nobody has been asked yet
serves: C1.P1.B5 · C1.P1.B7
question: Does the command-line executable packed inside the VS Code extension carry the same sha256 as the standalone claude release of the same version?
route: task
bank: new

## Where each piece lives
- `consumer/q-consumer.md` · what this page loses if the digests never come
- `executor/q-executor.md` · the stripped question, the only thing dispatched
- `executor/a-executor.md` · not written yet
- `proof/manifest.yaml` · `files: []` until EVIDENCE pulls the digests in
