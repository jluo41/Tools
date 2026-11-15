# b41 · AgreeableRx Replay

board-kind: task-block
spine: Replay the week the AgreeableRx paper (Paper-AgreeablePrescriptionDiscretion, MISQ) and its paper workbench were reshaped, from the sessions' own transcripts.
close: The Block's own sections show the week, the sessions, every decision by topic with JL's words, and what is still open.

## Topic

Eleven Claude Code sessions worked the paper from 2026-11-08 to 2026-11-14 (US Eastern): the main paper session,
one session per Section (t00 to t07 and the Appendix), and WorkBench-Paper-UI, which built the paper workbench.
`src/extract.py` pulls a timestamped timeline from each transcript; two reading agents wrote the decision logs
`src/decisions-A.md` and `src/decisions-B.md`; `src/build.py` turns them into the topics and the page.

## Topics

```text
s01-sessions     who worked on what
s02-nov08 … s08-nov14   one topic per day: what happened, then each decision
s09-still-open   asked or proposed and not settled
```

## How to rebuild

Edit `src/decisions-A.md` or `src/decisions-B.md`, then run `python3 src/build.py`. It rewrites `src/data.json`,
`delivery/website/replay.html` and every `sNN-<topic>/sNN-<topic>.md` face; edit the logs, never the generated files.

## Review Content

### 🗺️ The map

embed: src/review/map.svg

### 🗓️ The week

embed: src/review/week.md

### 👥 Sessions

embed: src/review/sessions.md

## Plan + Results

each: src/review/day-*.md

## Findings

each: src/review/area-*.md

### ❓ Still open

embed: src/review/still-open.md

## Jobs

1. `j01_decision_logs`: read the eleven transcripts into two decision logs
2. `j02_replay_build`: turn the logs into the Studio topics and these sections

## Deliverables

The same content as one standalone file, `delivery/website/replay.html`, for reading outside the workbench.

```yaml
deliverables: []
```

## Usage

`delivery/website/replay.html` is the same week as one page you open in a browser, with no server: Days, Sessions and Still open.
