## 0.2.0 · 2026-09-29 · Readable name; records at the two ends (JL 260928)

- Identity `run-scratch-<MMDD>-<target>` (older `rp-scratch-NN_<target>` still reads).
- The first note writes only the ticket; autosaves change only the notes in `## 2 · Scratch`;
  Finish is the close and writes `results/` and one log line.

## 0.1.0 · 2026-09-22

- New skill: the Scratch Run (`rp-scratch-NN_<target>`) gets its own contract,
  carved out of the Structure skill and the workflow controller, so the Run
  list has one skill per Run. Behaviour unchanged: open from Draft Space, Save
  keeps it open, a manual Finish with an AI Summary closes it.
