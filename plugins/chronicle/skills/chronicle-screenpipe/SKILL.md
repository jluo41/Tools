---
name: chronicle-screenpipe
description: Record a meeting from the computer with screenpipe and turn it into a raw markdown transcript routed into the vault. Verb-routed — `start` launches a scoped recording (AUDIO-ONLY by default, add vision for slides), `end` stops it and extracts the transcript, `extract` pulls a past time window from the existing DB without recording. Hands the raw .md to /obsidian-note to file a clean meeting note. Use when the user says /screenpipe, "record this meeting", "start recording", "stop recording", "transcribe the meeting", "记录会议".
created: 2026-06-28T00:22
updated: 2026-06-28T00:22
---

# /chronicle-screenpipe — record a meeting → raw transcript → vault note

Thin wrapper over a locally-installed [screenpipe](https://screenpi.pe). screenpipe
is the capture engine (mic + system audio, optionally screen+OCR); this skill scopes
ONE meeting, extracts it from `~/.screenpipe/db.sqlite`, and routes the result.

## Routing — pick the verb from the user's words

| User says | Verb | Action |
|---|---|---|
| "start recording", "record this meeting", "/screenpipe start" | **start** | `bin/sp-start.sh <slug>` |
| "stop", "end the meeting", "/screenpipe end" | **end** | `bin/sp-end.sh` → then route |
| "transcribe yesterday's call", "pull the 2-3pm meeting" | **extract** | `bin/sp-extract.py --date/--start/--end` → then route |

Derive `<slug>` from the meeting topic: 2–4 lowercase hyphenated words
(e.g. `a1c-team-sync`, `golden-phd-chat`).

## start — launch a scoped recording

```bash
bin/sp-start.sh <slug>               # AUDIO-ONLY (default): mic + system audio
bin/sp-start.sh <slug> --with-vision # also record screen → slides as "iframes"
```

- **Audio-only is the default** (`screenpipe --disable-vision`): no screen capture,
  no OCR, smaller DB, fewer privacy concerns. This is what you want for most meetings.
- Records a timezone-free **row-id watermark** so `end` knows exactly what is new.
- Refuses if a meeting is already active. One meeting at a time.
- ⚠️ **Consent:** this captures other people's audio. Confirm everyone is okay
  being recorded before starting — same obligation as any recorder.

## end — stop and extract

```bash
bin/sp-end.sh                 # kill screenpipe, extract everything since `start`
bin/sp-end.sh --keep-running  # extract but leave screenpipe running
```

Writes the raw transcript to
`_WorkSpace/screenpipe-raw/<YYMMDD-HHMM>-<slug>.md` and prints its path.

## extract — a past window, no recording

For meetings already in the DB (e.g. screenpipe was running 24/7):

```bash
bin/sp-extract.py --db ~/.screenpipe/db.sqlite --out <path.md> --slug <slug> \
    --date 2026-06-05                         # whole local day, OR
    --start "2026-06-05T20:00:00" --end "...21:00:00"   # explicit window
# add  --mode audio+vision  to also select screens shown.
```

## route — file it into the vault (always the last step)

After `end`/`extract` produce the raw `.md`, hand it to **/obsidian-note**:
it logs to the diary, keeps the raw file in `_WorkSpace`, and writes a clean
structured **meeting note** into `1-EVENT-SPACE` linking the raw transcript.
Do NOT hand-author the meeting note here — that is obsidian-note's job.

## What the raw markdown contains

1. **Header** — slug, mode, time span, turn/frame counts.
2. **Speakers** — ranked by airtime, capped at 8 (+ collapsed tail).
3. **Transcript** — consecutive same-speaker lines merged; mic/system
   double-captures deduped.
4. **Screens shown** — only in `audio+vision` mode: distinct screens deduped
   by OCR similarity, with thumbnails when screenpipe saved a snapshot.

## Known limits (set expectations — don't oversell)

- **Diarization is noisy.** screenpipe over-fragments speakers (one person → many
  `speaker_id`s). The legend ranks by airtime and collapses the tail, but speaker
  labels still need human verification/renaming in the meeting note.
- **Transcription is Whisper-grade** and degrades on heavy code-switching
  (e.g. Mandarin+English) and crosstalk. Treat the transcript as a searchable
  rough record, not a verbatim minute.
- **System audio** must be captured for the *other* participants to appear
  (`is_input_device=0`). If only your mic shows up, screenpipe's audio loopback
  isn't configured.

## Files

```
bin/sp-start.sh    launch scoped recording, write watermark marker
bin/sp-end.sh      stop + extract since watermark
bin/sp-extract.py  the extractor (transcript merge, dedup, frame selection)
```
