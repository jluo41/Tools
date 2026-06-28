#!/usr/bin/env python3
"""sp-extract.py — pull one meeting out of the screenpipe DB into raw markdown.

Selection mode (pick ONE window definition):
  --after-audio-id N --after-frame-id N   rows created after a watermark (live meetings)
  --start ISO --end ISO                    explicit timestamp window
  --date YYYY-MM-DD                         whole local day (handy for testing)

Output: a raw markdown file with
  1. a header (slug / mode / time span / speaker legend)
  2. the merged dialogue transcript (consecutive same-speaker lines joined)
  3. (only if vision frames exist) selected "useful iframes" — distinct screens
     shown during the meeting, deduped by OCR similarity, with thumbnails when
     screenpipe captured a snapshot image.

Stdlib only. The markdown is the archival truth; /obsidian-note turns it into a
clean meeting note.
"""

import argparse
import os
import re
import sqlite3
import sys
from difflib import SequenceMatcher

# ----- speaker labelling -----------------------------------------------------


def speaker_names(conn):
    """Map speaker_id -> display name (real name if labelled, else 'Speaker N')."""
    names = {}
    try:
        for sid, name in conn.execute("SELECT id, name FROM speakers"):
            if name and str(name).strip():
                names[sid] = str(name).strip()
    except sqlite3.OperationalError:
        pass
    return names


def label_for(sid, is_input, names, ordinal):
    if sid in names:
        return names[sid]
    if sid is None:
        return "Me (mic)" if is_input else "Others"
    # stable ordinal so the same speaker_id reads the same throughout
    tag = "🎤" if is_input else "🔊"
    return f"Speaker {ordinal[sid]} {tag}"


# ----- transcript ------------------------------------------------------------


def fetch_transcript(conn, where, params):
    rows = conn.execute(
        f"""
        SELECT timestamp, transcription, speaker_id, is_input_device
        FROM audio_transcriptions
        WHERE transcription IS NOT NULL AND length(trim(transcription)) > 0
          AND {where}
        ORDER BY timestamp, id
        """,
        params,
    ).fetchall()
    return rows


def merge_transcript(rows, names):
    """Join consecutive lines from the same speaker into one paragraph, after
    dropping mic/system double-captures (same utterance heard on both devices)."""
    ordinal = {}
    for _, _, sid, _ in rows:
        if sid is not None and sid not in ordinal:
            ordinal[sid] = len(ordinal) + 1

    airtime = {}  # label -> total chars (drives the legend ranking + cap)
    blocks = []   # [label, start_ts, [text...]]
    recent = []   # last few normalised texts, to kill device double-captures
    for ts, text, sid, is_input in rows:
        text = re.sub(r"\s+", " ", text).strip()
        if not text:
            continue
        if any(SequenceMatcher(None, text, r).ratio() >= 0.90 for r in recent):
            continue  # near-duplicate of a just-seen line (mic vs system) → skip
        recent = (recent + [text])[-4:]
        label = label_for(sid, is_input, names, ordinal)
        airtime[label] = airtime.get(label, 0) + len(text)
        if blocks and blocks[-1][0] == label:
            blocks[-1][2].append(text)
        else:
            blocks.append([label, ts, [text]])
    return blocks, ordinal, airtime


# ----- frame ("iframe") selection -------------------------------------------


def fetch_frames(conn, where, params):
    try:
        rows = conn.execute(
            f"""
            SELECT f.timestamp, f.app_name, f.window_name, f.browser_url,
                   f.snapshot_path, COALESCE(o.text, f.full_text, '') AS txt
            FROM frames f
            LEFT JOIN ocr_text o ON o.frame_id = f.id
            WHERE {where}
            ORDER BY f.timestamp, f.id
            """,
            params,
        ).fetchall()
    except sqlite3.OperationalError:
        return []
    return rows


def select_iframes(rows, max_frames=12, sim_threshold=0.80, min_chars=40):
    """Keep only distinct screens: drop frames whose OCR is ~the same as the
    last kept one, or that have too little text to be a useful slide/doc."""
    kept = []
    last_txt = ""
    for ts, app, win, url, snap, txt in rows:
        norm = re.sub(r"\s+", " ", (txt or "")).strip()
        if len(norm) < min_chars:
            continue
        if last_txt and SequenceMatcher(None, last_txt, norm).ratio() >= sim_threshold:
            continue
        kept.append({"ts": ts, "app": app, "win": win, "url": url,
                     "snap": snap, "txt": norm})
        last_txt = norm
    dropped = max(0, len(kept) - max_frames)
    return kept[:max_frames], dropped, len(rows)


# ----- rendering -------------------------------------------------------------


def render(slug, mode, blocks, ordinal, names, airtime, iframes, frame_drop, frame_total):
    out = []
    out.append(f"# Raw meeting capture — {slug}\n")
    span = ""
    if blocks:
        span = f"{blocks[0][1]} → {blocks[-1][1]}"
    out.append(f"- **mode:** {mode}")
    out.append(f"- **span:** {span or 'n/a'}")
    out.append(f"- **source:** screenpipe `db.sqlite` (raw, unedited)")
    out.append(f"- **turns:** {len(blocks)}  ·  **frames kept:** {len(iframes)}\n")

    # speaker legend — ranked by airtime, capped (diarization over-fragments,
    # so a long tail of tiny speaker_ids is noise, not real participants).
    if airtime:
        ranked = sorted(airtime.items(), key=lambda x: x[1], reverse=True)
        top = ranked[:8]
        out.append("## Speakers")
        out.append("_Diarization is approximate — verify & rename. "
                   "Labels ranked by airtime; long tail collapsed._\n")
        for label, chars in top:
            out.append(f"- **{label}** — ~{chars} chars _(rename in note)_")
        if len(ranked) > len(top):
            tail = sum(c for _, c in ranked[len(top):])
            out.append(f"- _+{len(ranked) - len(top)} minor/fragmented "
                       f"speakers (~{tail} chars total)_")
        out.append("")

    out.append("## Transcript\n")
    if not blocks:
        out.append("_No audio transcriptions found in this window._\n")
    for label, ts, parts in blocks:
        t = ts[11:19] if len(ts) >= 19 else ts
        out.append(f"**{label}** · `{t}`")
        out.append(" ".join(parts) + "\n")

    if iframes:
        out.append("## Screens shown (selected frames)\n")
        out.append(f"_Selected {len(iframes)} distinct screens"
                   + (f" (+{frame_drop} more deduped)" if frame_drop else "")
                   + f" from {frame_total} raw frames._\n")
        for i, fr in enumerate(iframes, 1):
            t = fr["ts"][11:19] if len(fr["ts"]) >= 19 else fr["ts"]
            where = fr["app"] or "?"
            if fr["win"]:
                where += f" — {fr['win']}"
            out.append(f"### {i}. `{t}` · {where}")
            if fr["url"]:
                out.append(f"<{fr['url']}>")
            if fr["snap"] and os.path.exists(fr["snap"]):
                out.append(f"![frame {i}]({fr['snap']})")
            snippet = fr["txt"][:600]
            out.append(f"> {snippet}{'…' if len(fr['txt']) > 600 else ''}\n")
    return "\n".join(out) + "\n"


# ----- main ------------------------------------------------------------------


def build_where(args):
    if args.date:
        return "date(timestamp)=?", [args.date], "date(f.timestamp)=?", [args.date]
    if args.start and args.end:
        return ("timestamp BETWEEN ? AND ?", [args.start, args.end],
                "f.timestamp BETWEEN ? AND ?", [args.start, args.end])
    # watermark mode (default)
    return ("id > ?", [args.after_audio_id], "f.id > ?", [args.after_frame_id])


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--db", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--slug", default="meeting")
    ap.add_argument("--mode", default="audio-only")
    ap.add_argument("--start-ts", default="")
    ap.add_argument("--after-audio-id", type=int, default=0)
    ap.add_argument("--after-frame-id", type=int, default=0)
    ap.add_argument("--start", default="")
    ap.add_argument("--end", default="")
    ap.add_argument("--date", default="")
    ap.add_argument("--max-frames", type=int, default=12)
    args = ap.parse_args()

    if not os.path.exists(args.db):
        sys.exit(f"✗ db not found: {args.db}")

    conn = sqlite3.connect(f"file:{args.db}?mode=ro", uri=True)
    a_where, a_params, f_where, f_params = build_where(args)

    names = speaker_names(conn)
    rows = fetch_transcript(conn, a_where, a_params)
    blocks, ordinal, airtime = merge_transcript(rows, names)

    iframes, frame_drop, frame_total = [], 0, 0
    if args.mode != "audio-only":
        frows = fetch_frames(conn, f_where, f_params)
        iframes, frame_drop, frame_total = select_iframes(frows, args.max_frames)

    md = render(args.slug, args.mode, blocks, ordinal, names, airtime,
                iframes, frame_drop, frame_total)
    os.makedirs(os.path.dirname(os.path.abspath(args.out)), exist_ok=True)
    with open(args.out, "w") as fh:
        fh.write(md)

    print(f"  transcript turns: {len(blocks)}  frames: {len(iframes)}", file=sys.stderr)
    print(args.out)


if __name__ == "__main__":
    main()
