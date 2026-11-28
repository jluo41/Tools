"""Scan what workbench pages SHOW for words AGENTS.md § Page words bans (hai-ui CONSTITUTION.md A01-A03).

    python page_words.py <origin> [<origin> ...] [--max 80]      crawl each server's Home and its focus pages
    python page_words.py --running [--max 40]                    every workbench server running on this machine
    python page_words.py --html <file.html> [...]                scan saved or rendered HTML

Reads only the visible text: <script>, <style>, comments and tag attributes are dropped (a tooltip `title=` is
kept, since a reader sees it). Exit 1 and one line per hit (page, rule, the words around it) when any rule breaks.
The crawl follows `/_board/workbench?path=…&layout=focus` links from Home, breadth first, read-only (GET only).
"""
from __future__ import annotations

import argparse
import html
import re
import subprocess
import sys
import urllib.request
from collections import deque
from urllib.parse import urljoin, urlparse

RULES = [  # (article, name, pattern) over visible text
    ("A02", "provenance tag", re.compile(r"\bJL ?2\d{5}\b")),
    ("A01", "tally", re.compile(r"\b\d+ of \d+ (?:done|written|signed|verified|checked|keys|plans|tasks|runs)\b", re.I)),
    ("A01", "tally", re.compile(r"\b\d+ to fix\b", re.I)),
    ("A01", "state words", re.compile(r"\b(?:Status|State)\s*[:·]\s*\w+", re.I)),
    ("A01", "state words", re.compile(r"\bnot signed yet\b", re.I)),
    ("A03", "empty state", re.compile(r"\bnothing (?:\w+ ){0,2}yet\b|\bno subfolders\b", re.I)),
]
DROP = re.compile(r"(?is)<script\b.*?</script>|<style\b.*?</style>|<!--.*?-->|<template\b.*?</template>")
TITLE = re.compile(r'(?i)\btitle="([^"]*)"')
PAGE = re.compile(r'href="(/_board/workbench\?[^"]*layout=focus[^"]*)"')


def visible(page: str) -> str:
    page = DROP.sub(" ", page)
    titles = " ".join(TITLE.findall(page))
    text = re.sub(r"(?s)<[^>]+>", " ", page)
    return re.sub(r"\s+", " ", html.unescape(text + " " + titles))


def hits(text: str) -> list:
    out = []
    for art, name, rx in RULES:
        for m in rx.finditer(text):
            out.append((art, name, text[max(0, m.start() - 40):m.end() + 40].strip()))
    return out


def fetch(url: str) -> str:
    with urllib.request.urlopen(url, timeout=30) as r:          # noqa: S310  (the person's own server)
        return r.read().decode("utf-8", "replace")


def crawl(origin: str, limit: int):
    seen, todo = set(), deque([origin.rstrip("/") + "/"])
    while todo and len(seen) < limit:
        url = todo.popleft()
        if url in seen:
            continue
        seen.add(url)
        try:
            page = fetch(url)
        except Exception as exc:  # noqa: BLE001
            yield url, None, str(exc)
            continue
        yield url, page, ""
        for link in PAGE.findall(page):
            nxt = urljoin(url, html.unescape(link))
            if urlparse(nxt).netloc == urlparse(origin).netloc and nxt not in seen:
                todo.append(nxt)


def running() -> list:
    """http://<host>:<port> of every `_host/serve.py` process on this machine (read from ps)."""
    ps = subprocess.run(["ps", "-axww", "-o", "command="], capture_output=True, text=True).stdout
    out = []
    for line in ps.splitlines():
        if "_host/serve.py" in line:
            host = re.search(r"--host (\S+)", line)
            port = re.search(r"--port (\d+)", line)
            if port:
                out.append(f"http://{host[1] if host else '127.0.0.1'}:{port[1]}")
    return sorted(set(out))


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("origins", nargs="*")
    ap.add_argument("--html", nargs="*", default=[])
    ap.add_argument("--running", action="store_true", help="scan every workbench server running here")
    ap.add_argument("--max", type=int, default=80, help="pages per origin")
    a = ap.parse_args()
    if a.running:
        a.origins += running()
    bad = pages = 0
    sources = [(f, open(f, encoding="utf-8").read(), "") for f in a.html]
    for origin in a.origins:
        sources.extend(crawl(origin, a.max))
    for where, page, err in sources:
        if page is None:
            print(f"❗ {where}: could not read ({err})")
            bad += 1
            continue
        pages += 1
        for art, name, words in hits(visible(page)):
            print(f"❗ {art} {name}: {where}\n     …{words}…")
            bad += 1
    print(f"{pages} pages read")
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
