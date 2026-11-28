"""Item cards: the Markdown cards beside a page, keyed by an item's address (ref/cards.md).

Three files sit in the owning page's records folder, in the format Draft Lab already writes:
  <stem>-comments.md   ### Comment <n> · <address>, Quote:, State:, - Note · <time>[ · who]: …, - Reply · …
  <stem>-revise.md     ## Pass k sections; ### Edit · <address> · <why> cards with By:, Why:, Original:, Expected:, State:
  <stem>-checked.md    - <address> · <time> · <the words it saw>
A draft Task keeps them in draft/records/, any other page in records/; a Project's stem is `project`.

This module is pure: it parses, and it writes through `edit()` (an advisory lock beside the file, then a temporary file
renamed over it). Draft Lab's own actions (draft_step_revise_notes) parse with `parse_comments` and write with
`write_text`; this module's actions serve every other page. The page is never written here; only its card files.
"""
from __future__ import annotations

import datetime
import fcntl
import os
import re
import tempfile
from contextlib import contextmanager
from pathlib import Path

from live.sentence_id import sid

ADDRESS = re.compile(r"^[A-Za-z0-9_-]+(\.[A-Za-z0-9_-]+)*$")
EDIT_STATES = ("proposed", "accepted", "rejected")
_CACHE: dict = {}                     # records folder -> (mtimes, cards)
# lock files, outside every repository, at one place every process agrees on (TMPDIR differs between a server and
# an agent's shell, so tempfile.gettempdir() alone would give them different locks)
LOCKS = (Path("/tmp") if Path("/tmp").is_dir() else Path(tempfile.gettempdir())) / "hai-locks"


# ── where the files are ───────────────────────────────────────────────────────────────────────────────────────────
def page_face(page: Path) -> Path | None:
    """The page's own Markdown: `<folder>.md`, a Block's `board.md`, a Project's `project.md`."""
    for name in (page.name + ".md", "board.md", "project.md"):
        if (page / name).is_file():
            return page / name
    return None


def records_dir(page: Path) -> Path:
    """`draft/records/` for a draft Task (it has a draft/ folder), else `records/`."""
    return page / "draft" / "records" if (page / "draft").is_dir() else page / "records"


def stem(page: Path) -> str:
    face = page_face(page)
    return face.stem if face else page.name


def files(page: Path) -> dict:
    """{'comments' | 'revise' | 'checked': the path}, whether or not it exists yet."""
    base, s = records_dir(page), stem(page)
    return {k: base / f"{s}-{k}.md" for k in ("comments", "revise", "checked")}


# ── reading ────────────────────────────────────────────────────────────────────────────────────────────────────────
def parse_comments(path: Path) -> list:
    """One dict per `### Comment <n> · <address>` block: n, target, quote, state (open, answered, done), thread
    [(Note|Reply, time[ · who], words)]."""
    if not path.is_file():
        return []
    out = []
    for m in re.finditer(r"(?ms)^### Comment (\d+) · ([^\n]+?)[^\S\n]*\n(.*?)(?=^### |^## |\Z)",
                         path.read_text(encoding="utf-8", errors="replace")):
        body = m.group(3)
        field = lambda k: (re.search(r"(?m)^" + k + r":[^\S\n]*(.*)$", body) or [None, ""])[1].strip()
        out.append({"n": m.group(1), "target": m.group(2).strip(), "quote": field("Quote"),
                    "state": (field("State").split() or ["open"])[0].lower(),
                    # a message may go on in indented lines ("  1. Problem: …", "  - …"): kept with it, one per line
                    "thread": [(w, t, x + "".join("\n" + y.strip() for y in more.splitlines() if y.strip()))
                               for w, t, x, more in re.findall(r"(?m)^- (Note|Reply) · (.+?): (.*)$((?:\n[ \t]+\S.*)*)", body)]})
    return out


def parse_edits(path: Path) -> list:
    """One dict per `### Edit · <address> · <why>` card: head, address, why, original, expected, state, pass."""
    if not path.is_file():
        return []
    text, out, title = path.read_text(encoding="utf-8", errors="replace"), [], ""
    for m in re.finditer(r"(?ms)^(## [^\n]*|### (Edit · [^\n]+?))[^\S\n]*\n(.*?)(?=^### |^## |\Z)", text):
        if m.group(1).startswith("## "):
            title = m.group(1)[3:].strip()
            continue
        head = m.group(2).strip()
        body = re.sub(r"(?m)^[-*][^\S\n]+(Why|Original|Expected|State|By):", r"\1:", m.group(3))
        field = lambda k: (re.search(r"(?m)^" + k + r":[^\S\n]*(.*)$", body) or [None, ""])[1].strip()
        parts = [x.strip() for x in head.split(" · ")]
        state = (field("State").split() or ["proposed"])[0].lower()
        out.append({"head": head, "address": parts[1] if len(parts) > 1 else "", "why": " · ".join(parts[2:]),
                    "original": field("Original"), "expected": field("Expected"), "by": field("By"),
                    "state": "proposed" if state in ("jl's", "jl") else state, "pass": title})
    return out


def parse_checked(path: Path) -> dict:
    """{address: the words it saw} from `- <address> · <time> · <words>` lines."""
    if not path.is_file():
        return {}
    return {m.group(1): m.group(2).strip() for m in re.finditer(r"(?m)^- ([A-Za-z0-9_.-]+) · [^·]+ · (.*)$",
                                                                path.read_text(encoding="utf-8", errors="replace"))}


def card_key(page: Path, address: str) -> str:
    """The address as cards are keyed: on a draft Task a sentence id in either case (S8, s8) is one key, s8."""
    return sid(address) if (page / "draft").is_dir() else address


def cards(page: Path) -> dict:
    """{address: {'comments': [...], 'edits': [...], 'checked': words or None}} for one page, read once and kept
    until one of its three files changes. On a draft Task the addresses compare through card_key() (S8 is s8)."""
    paths = files(page)
    key = str(records_dir(page))
    mt = tuple(p.stat().st_mtime_ns if p.is_file() else 0 for p in paths.values())
    hit = _CACHE.get(key)
    if hit and hit[0] == mt:
        return hit[1]
    out: dict = {}
    slot = lambda a: out.setdefault(card_key(page, a), {"comments": [], "edits": [], "checked": None})
    for c in parse_comments(paths["comments"]):
        slot(c["target"])["comments"].append(c)
    for e in parse_edits(paths["revise"]):
        if e["address"]:
            slot(e["address"])["edits"].append(e)
    for a, words in parse_checked(paths["checked"]).items():
        slot(a)["checked"] = words
    _CACHE[key] = (mt, out)
    return out


# ── writing ────────────────────────────────────────────────────────────────────────────────────────────────────────
@contextmanager
def locked(path: Path):
    """An advisory lock on the file, held while one writer reads and rewrites it. The lock file sits outside the
    repository (<temp>/hai-locks/, named by the file's real path), so a click never leaves an untracked file."""
    path.parent.mkdir(parents=True, exist_ok=True)
    LOCKS.mkdir(parents=True, exist_ok=True)
    name = os.path.realpath(path).strip(os.sep).replace(os.sep, "!") + ".lock"
    with open(LOCKS / name[-240:], "w") as fh:
        fcntl.flock(fh, fcntl.LOCK_EX)
        try:
            yield
        finally:
            fcntl.flock(fh, fcntl.LOCK_UN)


def write_text(path: Path, text: str) -> None:
    """Write through a temporary file in the same folder, renamed over the old one: never a half-written file. A
    symlink is written through to its target, and the file keeps its mode (a new one gets the usual 0666 - umask)."""
    path = Path(os.path.realpath(path))
    path.parent.mkdir(parents=True, exist_ok=True)
    if path.exists():
        mode = path.stat().st_mode & 0o7777
    else:
        mask = os.umask(0)
        os.umask(mask)
        mode = 0o666 & ~mask
    fd, tmp = tempfile.mkstemp(prefix="." + path.name + ".", dir=path.parent)
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as fh:
            fh.write(text)
        os.chmod(tmp, mode)
        os.replace(tmp, path)
    except BaseException:
        if os.path.exists(tmp):
            os.unlink(tmp)
        raise


def edit(path: Path, change, new_file: str = ""):
    """Under the lock, read the file (or `new_file` when it is missing), call change(text) -> (new text or None,
    result), write the new text if there is one, and return the result."""
    with locked(path):
        text = path.read_text(encoding="utf-8") if path.is_file() else new_file
        new, result = change(text)
        if new is not None and new != text:
            write_text(path, new)
        return result


def _now() -> str:
    return f"{datetime.datetime.now():%Y-%m-%d %H:%M}"


def _block(text: str, head_re: str):
    return list(re.finditer(r"(?ms)^### " + head_re + r"[^\S\n]*\n(.*?)(?=^### |^## |\Z)", text))


def comment_act(page: Path, p: dict) -> tuple:
    """add | reply | done | reopen | delete one comment on an item; refused (409) when its state changed on disk
    since the page showed it (`was`). Returns (status, {ok, n, state} | {ok: False, err})."""
    path = files(page)["comments"]
    act, n, address = str(p.get("act") or ""), str(p.get("n") or ""), card_key(page, str(p.get("address") or ""))
    words = " ".join(str(p.get("text") or "").split())
    who = " ".join(str(p.get("who") or "").split())[:60]
    note = f"- Note · {_now()}" + (f" · {who}" if who else "") + f": {words}\n"
    first = f"# {stem(page)} · comments\n\nComments on the items of this page; each is answered by a Reply and closed by its person.\n"

    def change(text):
        if act == "add":
            if not ADDRESS.match(address):
                return None, (400, {"ok": False, "err": "no such item address"})
            if not words:
                return None, (400, {"ok": False, "err": "the comment is empty"})
            k = str(max([int(m) for m in re.findall(r"(?m)^### Comment (\d+) · ", text)] or [0]) + 1)
            quote = " ".join(str(p.get("quote") or "").split())[:400]
            new = (text.rstrip("\n") + f"\n\n### Comment {k} · {address}\n" + (f"Quote: {quote}\n" if quote else "")
                   + "State: open\n" + note)
            return new, (200, {"ok": True, "n": k, "state": "open"})
        found = _block(text, "Comment " + re.escape(n) + r" · [^\n]*")
        if not n or len(found) != 1:
            return None, (409, {"ok": False, "err": "the comment changed on disk; reload"})
        body = found[0].group(1)
        cur = (re.search(r"(?m)^State:[^\S\n]*(\S*)", body) or [None, "open"])[1].lower() or "open"
        if p.get("was") and str(p["was"]) != cur:
            return None, (409, {"ok": False, "err": f"it is {cur} on disk now; reload", "state": cur})
        if act == "delete":
            if re.search(r"(?m)^- Reply · ", body):
                return None, (409, {"ok": False, "err": "it has a reply; mark it done instead"})
            rest = text[found[0].end():].lstrip("\n")
            return (text[:found[0].start()].rstrip("\n") + ("\n\n" + rest if rest.strip() else "\n"),
                    (200, {"ok": True, "n": n, "state": "deleted"}))
        if act == "reply":
            if not words:
                return None, (400, {"ok": False, "err": "the reply is empty"})
            body, state = body.rstrip("\n") + "\n" + note, "open"
        elif act in ("done", "reopen"):
            state = "done" if act == "done" else "open"
        else:
            return None, (400, {"ok": False, "err": "add, reply, done, reopen or delete"})
        line = f"State: {state}" + (f" · {_now()}" if state == "done" else "")
        body = re.sub(r"(?m)^State:.*$", line, body, count=1) if re.search(r"(?m)^State:", body) else line + "\n" + body
        if not body.endswith("\n\n") and text[found[0].end():].strip():
            body = body.rstrip("\n") + "\n\n"
        return text[:found[0].start(1)] + body + text[found[0].end(1):], (200, {"ok": True, "n": n, "state": state})

    return edit(path, change, first)


def check_act(page: Path, p: dict) -> tuple:
    """check | uncheck an item: one line with the words the person saw; a check lapses when the words change.
    A person's mark only; an agent never writes it."""
    path, address = files(page)["checked"], card_key(page, str(p.get("address") or ""))
    if not ADDRESS.match(address):
        return 400, {"ok": False, "err": "no such item address"}
    words = " ".join(str(p.get("words") or "").split())[:400]
    head = (f"# {stem(page)} · checked items\n\nItems the person passed. A pass leaves a checked item as it is while "
            "its words are the ones below.\n\n")

    def change(text):
        lines = [l for l in text.splitlines() if l.startswith("- ") and card_key(page, l[2:].split(" · ")[0]) != address]
        if p.get("act") == "check":
            lines.append(f"- {address} · {_now()} · {words}")
        return head + "\n".join(sorted(lines)) + "\n", (200, {"ok": True, "checked": p.get("act") == "check"})

    return edit(path, change, head)


def edit_card_act(page: Path, p: dict) -> tuple:
    """accept | reject | undo one `### Edit · <address> · …` card: only its State: line changes (the words are written
    by the item's own adapter or by the next Run). `was` guards against a card changed on disk."""
    path = files(page)["revise"]
    head, want = str(p.get("card") or ""), {"accept": "accepted", "reject": "rejected", "undo": "proposed"}.get(
        str(p.get("act") or ""))
    if not want:
        return 400, {"ok": False, "err": "accept, reject or undo"}
    if not path.is_file():
        return 404, {"ok": False, "err": f"no {path.name}"}

    def change(text):
        found = _block(text, re.escape(head))
        if not found and (page / "draft").is_dir():      # s8 finds an older S8 card on a draft Task
            found = _block(text, re.sub(r"(?<!\w)[Ss](\d+[a-z]*)\b", r"[Ss]\1", re.escape(head)))
        if len(found) != 1:
            return None, (409, {"ok": False, "err": "the card changed on disk; reload"})
        body = re.sub(r"(?m)^[-*][^\S\n]+(State):", r"\1:", found[0].group(1))
        cur = re.search(r"(?m)^State:[^\S\n]*(\S*)", body)
        now = (cur.group(1).lower() if cur and cur.group(1) else "proposed")
        now = "proposed" if now in ("jl's", "jl") else now
        if p.get("was") and str(p["was"]) != now:
            return None, (409, {"ok": False, "err": f"it is {now} on disk now; reload", "state": now})
        line = "State: proposed" if want == "proposed" else f"State: {want} · {_now()}"
        body = re.sub(r"(?m)^State:.*$", line, body, count=1) if cur else body.rstrip("\n") + f"\n{line}\n\n"
        return text[:found[0].start(1)] + body + text[found[0].end(1):], (200, {"ok": True, "state": want})

    return edit(path, change)
