"""Measure how fast the side pane and its Block page load, and where the time goes (JL 261126: "a new task to
measure the speed of Files Tree loading, the speed test and code efficiency").

    <host venv python> bench_pane.py [--base http://127.0.0.1:5623] [--blocks b17_theme_work b11_theme_insight ...]
                                     [--repeat 3] [--no-profile]

For each Block it asks a running workbench for the Files panel and the Block page, each --repeat times with a pause
longer than the panel's git cache, and prints the median time and the first request's (the server may keep a built
page, so the first is the one a new visit waits for), the size,
the style and script blocks and how many bytes of them repeat. Then it renders one Block's Files panel in this
process under cProfile and prints the five slowest workbench functions. A row over a limit is marked ❗ and the
script exits 1, so a check round can run it as is.
"""
from __future__ import annotations

import argparse
import re
import statistics
import sys
import time
import urllib.request
from pathlib import Path
from urllib.parse import quote

SPACE = next(p for p in Path(__file__).resolve().parents if (p / "plugins" / "haipipe-toolkit").is_dir())
WORK = "examples/Project-Ladder/work"
LIMITS = {"panel_s": 1.0, "page_s": 1.5, "page_kb": 1200, "repeat_kb": 100}
BLOCK_RE = re.compile(r"<(style|script)\b[^>]*>(.*?)</\1>", re.S | re.I)


def fetch(base: str, path: str, extra: str = "") -> tuple[float, bytes]:
    url = f"{base}/_board/workbench?layout=focus&path={quote(path)}{extra}"
    t0 = time.perf_counter()
    body = urllib.request.urlopen(url, timeout=60).read()
    return time.perf_counter() - t0, body


def blocks(html: str) -> tuple[int, int]:
    """(style and script blocks, bytes of the copies after the first of each)."""
    seen, extra, n = set(), 0, 0
    for m in BLOCK_RE.finditer(html):
        n += 1
        if m[0] in seen:
            extra += len(m[0].encode())
        seen.add(m[0])
    return n, extra


def measure(base: str, block: str, repeat: int) -> dict:
    path = f"{WORK}/{block}"
    panel, page, body = [], [], b""
    for i in range(repeat):
        if i:
            time.sleep(10.5)                                  # past the panel's 10 s git cache
        panel.append(fetch(base, path, "&panel=files")[0])
        t, body = fetch(base, path)
        page.append(t)
    n, extra = blocks(body.decode("utf-8", "replace"))
    return {"block": block, "panel_s": statistics.median(panel), "page_s": statistics.median(page),
            "panel_first": panel[0], "page_first": page[0],
            "page_kb": len(body) / 1024, "blocks": n, "repeat_kb": extra / 1024}


def profile(block: str, top: int = 5) -> list[tuple[float, str]]:
    """The slowest workbench functions (cumulative seconds) while one Block's Files panel renders in this process."""
    import cProfile
    import pstats
    sys.path.insert(0, str(SPACE / "plugins/haipipe-toolkit/servers/_host"))
    from host_paths import bootstrap
    bootstrap()
    from live import focus_page, frame
    folder = (SPACE / WORK / block).resolve()
    theme = frame.themes().get(frame.theme_of(folder, SPACE), frame.VANILLA)
    time.sleep(10.5)
    prof = cProfile.Profile()
    prof.runcall(focus_page.render, theme, SPACE, folder, panel="files")
    rows = []
    for (file, line, name), (_, _, _, cum, _) in pstats.Stats(prof).stats.items():
        if "/servers/" in file and "/page/block_index_page/focus_page.py" not in file:
            rows.append((cum, f"{file.split('/servers/')[1]}:{line} {name}"))
    return sorted(rows, reverse=True)[:top]


def main(argv: list[str]) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--base", default="http://127.0.0.1:5623")
    ap.add_argument("--blocks", nargs="+", default=["b17_theme_work", "b11_theme_insight", "b16_theme_paper"])
    ap.add_argument("--repeat", type=int, default=3)
    ap.add_argument("--no-profile", action="store_true")
    a = ap.parse_args(argv)
    over = False
    print("| Block | Files panel (first) | Block page (first) | page size | style+script blocks | repeated |")
    print("| --- | --- | --- | --- | --- | --- |")
    for block in a.blocks:
        r = measure(a.base, block, a.repeat)
        worst = dict(r, panel_s=max(r["panel_s"], r["panel_first"]), page_s=max(r["page_s"], r["page_first"]))
        mark = {k: " ❗" if worst[k] > LIMITS[k] else "" for k in LIMITS}
        over |= any(mark.values())
        print(f"| {block} | {r['panel_s']:.2f} s ({r['panel_first']:.2f}){mark['panel_s']} | "
              f"{r['page_s']:.2f} s ({r['page_first']:.2f}){mark['page_s']} | "
              f"{r['page_kb']:.0f} KB{mark['page_kb']} | {r['blocks']} | {r['repeat_kb']:.0f} KB{mark['repeat_kb']} |")
    print(f"\nlimits: panel {LIMITS['panel_s']} s, page {LIMITS['page_s']} s, page {LIMITS['page_kb']} KB, "
          f"repeated {LIMITS['repeat_kb']} KB")
    if not a.no_profile:
        print(f"\nslowest functions while {a.blocks[0]}'s Files panel renders (cumulative):")
        for cum, where in profile(a.blocks[0]):
            print(f"- {cum:.3f} s  {where}")
    return 1 if over else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
