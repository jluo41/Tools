---
name: chronicle-daily
description: Roll up a day's session .txt files in ~/Daily/<date>/ into one Excalidraw canvas, then mark the day closed and sync to git. Triggered by a 22:00 cron OR on demand. Idempotent — re-running on a closed day is a no-op. After close, new sessions automatically route to tomorrow's folder. Use when the user says "做一下今天的总结" / "rollup today" / scheduled job fires.
---

# /chronicle-daily — End-of-day rollup

## What this skill does

At ~22:00 every day, take all `YYMMDD-HHMM-*.txt` files in
`~/Daily/<date>/` and turn them into one Excalidraw canvas, then **close
the day**. Closing is the signal that no more sessions belong to this
date — `chronicle-session` will route post-close work to tomorrow.

## When to invoke

- ⏰ scheduled job (launchd / cron / claudeclaw) fires at 22:00 local
- 🧑 user says "rollup today" / "做一下今天的总结" / `/chronicle-daily`
- 🛠️ manual catch-up: `/chronicle-daily 2026-04-25` to close a missed day

## Inputs

```
~/Daily/YYYY-MM-DD/
├── 260426-session-A.txt    (multiple sessions accumulated through the day)
├── 260426-session-B.txt
└── 260426-session-C.txt
```

## Outputs

```
~/Daily/YYYY-MM-DD/
├── 260426-session-*.txt          (untouched)
├── canvas-260426.excalidraw      ← built by txt-to-canvas.py (rebuild)
└── .closed                       ← sentinel: day is finalized
```

## Idempotence rule

```
if exists(.closed):
    log "already closed, skipping"
    exit 0
```

Re-running on a closed day does **nothing**. To force a rebuild, the user
must delete `.closed` first (rare; only for fixing a bad rollup).

## Why rebuild (not append) is correct here

By the time `chronicle-daily` runs, the day is final. Rebuild from `.txt`
is:
- ✅ Simpler — one source of truth
- ✅ Idempotent — same input → same canvas
- ✅ Safe — no manual annotations exist yet (canvas is being created)

`txt-append-to-canvas.py` is for ad-hoc accretion **before** rollup, or
on already-closed canvases the user has annotated. Not used here.

## Sync workflow (use the bin script — don't reimplement)

```
chronicle-daily/bin/rollup.sh [YYYY-MM-DD]    (default: today)
```

Internals (see `bin/rollup.sh`):

```
1. cd ~/Daily
2. git pull --rebase --autostash
3. resolve target date (arg, or today)
4. if .closed exists → exit 0
5. count YYMMDD-HHMM-*.txt → if 0, exit with warning
6. run txt-to-canvas.py <date>/      (rebuild)
7. touch <date>/.closed
8. git add canvas + .closed
9. git commit -m "rollup(<date>): N sessions"
10. git push (retry once)
```

## Installing the cron

```
chronicle-daily/bin/install-cron.sh
```

This sets up a 22:00-daily trigger via one of:

```
🅰️ macOS launchd (preferred on jluo41's Mac Studio / mini)
   ~/Library/LaunchAgents/dev.jluo41.chronicle-daily.plist

🅱️ claudeclaw:jobs   (if the heartbeat daemon is running)
🅲 vanilla crontab    (fallback)
```

The script picks 🅰️ on Darwin, 🅲 elsewhere. Use `--dry-run` to print the
plist without installing.

## Manual catch-up examples

```bash
# Today (the usual scheduled call)
chronicle-daily/bin/rollup.sh

# Yesterday — only works if not yet closed
chronicle-daily/bin/rollup.sh 2026-04-25

# Force rebuild a closed day (rare; for fixing a bad rollup)
rm ~/Daily/2026-04-25/.closed
chronicle-daily/bin/rollup.sh 2026-04-25
```

## Sister skill

- `chronicle-session` — writes per-session `.txt` files (the input here)
- Underlying renderer: `diagram-ascii-canvas/bin/txt-to-canvas.py`
