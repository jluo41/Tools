"""A source video's screenshots: download it once, keep its distinct frames, and lay them out on one contact sheet.
Asked 261012: "could we get the screenshot of the video as well if possible?"

    python video_frames.py <video url> [--every 3] [--cache <folder>]    the cache folder, with frames/ and sheet.jpg
    python video_frames.py --sheet <cache folder>                        rebuild the contact sheet

A Bilibili video comes through the same player API the transcripts used, at the best quality served without a login
(480p). Everything lands in the SPACE's ignored `_WorkSpace/video_frames/<id>/`: the video, one frame every few
seconds with the near-repeats dropped (`frames/t0123.jpg`, named by second), and `sheet.jpg`, every kept frame with
its time, for a person or an agent to pick from. A topic copies only the frames it picks into its own `assets/`.
"""
from __future__ import annotations

import argparse
import json
import re
import shutil
import subprocess
import sys
import urllib.error
import urllib.request
from pathlib import Path

UA = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 Chrome/140 Safari/537.36"}
MOST = 48                                                     # frames on one sheet


def space_of(start: Path) -> Path:
    return next((p for p in (start, *start.parents) if (p / "Tools").exists()), start)


def video_id(url: str) -> str:
    m = re.search(r"(BV[0-9A-Za-z]{10})", url) or re.search(r"(?:v=|youtu\.be/)([\w-]{11})", url)
    if not m:
        raise SystemExit(f"{url}: not a Bilibili or YouTube video address")
    return m.group(1)


def patient(fn, tries: int = 5):
    """Bilibili caps how often one machine may ask (HTTP 412, 514, 532): wait longer each time, then try again."""
    import time
    for k in range(tries):
        try:
            return fn()
        except urllib.error.HTTPError as err:
            if err.code not in (412, 429, 514, 532) or k == tries - 1:
                raise
            time.sleep(20 * (k + 1))


def get_json(url: str, referer: str) -> dict:
    req = urllib.request.Request(url, headers={**UA, "Referer": referer, "Accept": "application/json"})
    return patient(lambda: json.load(urllib.request.urlopen(req, timeout=30)))


def download_bilibili(bv: str, out: Path) -> Path:
    """One video; a multi-part one (a course in parts) part by part, then joined in order into one file, so its
    seconds run on the same timeline as a transcript of all its parts."""
    page = f"https://www.bilibili.com/video/{bv}/"
    parts = get_json(f"https://api.bilibili.com/x/player/pagelist?bvid={bv}", page)["data"]   # view? is 412
    if len(parts) == 1:
        return download_part(bv, parts[0]["cid"], out)
    files = []
    for p in parts:
        f = out.with_name(f"video.p{p['page']:02d}.mp4")
        if not (f.is_file() and f.stat().st_size > 10_000):
            download_part(bv, p["cid"], f)
        files.append(f)
    listing = out.with_name("parts.txt")
    listing.write_text("".join(f"file '{f.name}'\n" for f in files))
    joined = out.with_name("video.joined.mp4")
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "concat", "-safe", "0", "-i", str(listing), "-c", "copy",
                    str(joined)], check=True)
    joined.replace(out)
    for f in files + [listing]:
        f.unlink()
    return out


def download_part(bv: str, cid: int, out: Path) -> Path:
    page = f"https://www.bilibili.com/video/{bv}/"
    play = get_json(f"https://api.bilibili.com/x/player/playurl?fnval=16&fnver=0&fourk=1&bvid={bv}&cid={cid}", page)
    streams = sorted(play["data"]["dash"]["video"], key=lambda v: (v["id"], "avc" in v.get("codecs", "")))
    best = streams[-1]                                         # the best served without a login
    req = urllib.request.Request(best.get("baseUrl") or best["base_url"],
                                 headers={**UA, "Referer": "https://www.bilibili.com/", "Origin": "https://www.bilibili.com"})
    part = out.with_suffix(".part")                            # renamed only when whole: a stopped fetch is redone

    def get():
        with urllib.request.urlopen(req, timeout=300) as r, part.open("wb") as f:
            want = int(r.headers.get("Content-Length") or 0)
            shutil.copyfileobj(r, f)
        if want and part.stat().st_size < want:                # Bilibili may close early with no error: try again
            raise urllib.error.HTTPError(req.full_url, 532, f"short read {part.stat().st_size} of {want}", None, None)
    patient(get)
    part.replace(out)
    return out


def download(url: str, cache: Path) -> Path:
    cache.mkdir(parents=True, exist_ok=True)
    out = cache / "video.mp4"
    if out.is_file() and out.stat().st_size > 10_000:
        return out
    vid = video_id(url)
    if vid.startswith("BV"):
        return download_bilibili(vid, out)
    ytdlp = shutil.which("yt-dlp")
    if not ytdlp:
        raise SystemExit(f"{url}: a YouTube video needs yt-dlp")
    subprocess.run([ytdlp, "-f", "bv*[height<=720]/b[height<=720]", "-o", str(out), url], check=True)
    return out


def frames(video: Path, cache: Path, every: float = 2.0) -> list[Path]:
    """One frame every `every` seconds, then the ones worth reading (`pick`): each slide once it is whole."""
    import numpy as np
    from PIL import Image
    raw = cache / "raw"
    shutil.rmtree(raw, ignore_errors=True)
    raw.mkdir()
    subprocess.run(["ffmpeg", "-v", "error", "-i", str(video), "-vf", f"fps=1/{every},scale='min(720,iw)':-2",
                    "-q:v", "3", str(raw / "%05d.jpg")], check=True)
    keep = cache / "frames"
    shutil.rmtree(keep, ignore_errors=True)
    keep.mkdir()
    paths = sorted(raw.glob("*.jpg"))
    out = []
    for k in pick(paths):
        dst = keep / f"t{int(k * every):04d}.jpg"
        shutil.copy(paths[k], dst)
        out.append(dst)
    shutil.rmtree(raw, ignore_errors=True)
    return out


def pick(paths: list) -> list[int]:
    """Which samples to keep. A dark slide video builds each slide up, holds it, then clears it: keep the sample just
    before its bright marks drop (the slide whole) or before a cut, never a cross-fade between two slides (a
    sample halfway between its neighbours). A bright, filmed video: keep the first sample of each
    run of change. Near-repeats are dropped either way; the last sample (a recap) is kept."""
    import numpy as np
    from PIL import Image
    small, ink = [], []                                           # small copies only: a long course has thousands
    for p in paths:
        g = Image.open(p).convert("L")
        small.append(np.asarray(g.resize((48, 48)), dtype=float))
        a = np.asarray(g.resize((96, 170)), dtype=float)
        ink.append(float((a[17:] > 110).mean()))              # below the top tenth, where a channel's mark sits
    diff = lambda i, j: float(np.abs(small[i] - small[j]).mean())   # noqa: E731
    n = len(paths)
    if not n:
        return []
    if float(np.median(ink)) > 0.25:                              # bright: filmed, a person talking
        keep, last = [], None
        for k in range(n):
            if last is None or diff(k, last) > 7:
                keep.append(k)
                last = k
        return keep
    ends = [k for k in range(n - 1) if ink[k + 1] < 0.75 * ink[k] or diff(k, k + 1) > 5] + [n - 1]
    blend = lambda k: (0 < k < n - 1 and diff(k - 1, k) > 1.5 and diff(k, k + 1) > 1.5          # noqa: E731
                       and diff(k - 1, k) + diff(k, k + 1) <= 1.15 * diff(k - 1, k + 1))
    ends = [k - 1 if blend(k) else k for k in ends]                # a cross-fade: the sample before shows the slide whole
    keep = []
    for k in ends:
        if ink[k] < 0.002:                                         # a blank between slides
            continue
        if keep and diff(k, keep[-1]) < 4:                         # the same slide again
            if ink[k] > ink[keep[-1]]:
                keep[-1] = k
            continue
        keep.append(k)
    return keep


def reframe(cache: Path, every: float = 2.0) -> Path:
    """Frames and sheet again from a cached video, no download (after the frame rule changed)."""
    frames(cache / "video.mp4", cache, every)
    return sheet(cache)


def sheet(cache: Path) -> Path:
    """Every kept frame (at most MOST, spread over the video) with its time, in one picture."""
    from PIL import Image, ImageDraw, ImageFont
    fs = sorted((cache / "frames").glob("t*.jpg"))
    if len(fs) > MOST:
        fs = [fs[round(i * (len(fs) - 1) / (MOST - 1))] for i in range(MOST)]
    if not fs:
        raise SystemExit(f"{cache}: no frames")
    im0 = Image.open(fs[0])
    tw = 240
    th = round(im0.height * tw / im0.width)
    cols = 8 if th >= tw else 6
    rows = -(-len(fs) // cols)
    out = Image.new("RGB", (cols * (tw + 8) + 8, rows * (th + 36) + 8), "white")
    draw = ImageDraw.Draw(out)
    try:
        font = ImageFont.truetype("/System/Library/Fonts/Supplemental/Arial.ttf", 22)
    except OSError:
        font = ImageFont.load_default()
    for i, p in enumerate(fs):
        x, y = 8 + (i % cols) * (tw + 8), 8 + (i // cols) * (th + 36)
        out.paste(Image.open(p).convert("RGB").resize((tw, th)), (x, y + 30))
        sec = int(p.stem[1:])
        draw.text((x, y + 2), f"{sec // 60}:{sec % 60:02d}  ({sec} s)", fill="black", font=font)
    dst = cache / "sheet.jpg"
    out.save(dst, quality=80)
    return dst


def nearest(cache: Path, sec: float) -> Path | None:
    """The kept frame nearest a second of the video."""
    fs = sorted((cache / "frames").glob("t*.jpg"))
    return min(fs, key=lambda p: abs(int(p.stem[1:]) - sec)) if fs else None


def cache_of(url: str, start: Path) -> Path:
    return space_of(start) / "_WorkSpace" / "video_frames" / video_id(url)


def fetch(url: str, start: Path, every: float = 2.0) -> Path:
    cache = cache_of(url, start)
    if not (cache / "sheet.jpg").is_file():
        frames(download(url, cache), cache, every)
        sheet(cache)
    return cache


def main(argv=None) -> int:
    p = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    p.add_argument("url", nargs="?")
    p.add_argument("--every", type=float, default=2.0)
    p.add_argument("--reframe", type=Path, help="a cache folder: rebuild its frames and sheet from video.mp4")
    p.add_argument("--cache", type=Path)
    p.add_argument("--sheet", type=Path)
    a = p.parse_args(argv)
    if a.sheet:
        print(sheet(a.sheet))
        return 0
    if a.reframe:
        print(reframe(a.reframe, a.every), len(list((a.reframe / "frames").glob("t*.jpg"))), "frames")
        return 0
    cache = a.cache or cache_of(a.url, Path.cwd())
    if not (cache / "sheet.jpg").is_file():
        frames(download(a.url, cache), cache, a.every)
        sheet(cache)
    print(cache, len(list((cache / "frames").glob("t*.jpg"))), "frames")
    return 0


if __name__ == "__main__":
    sys.exit(main())
