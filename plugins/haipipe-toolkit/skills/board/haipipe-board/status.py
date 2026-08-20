#!/usr/bin/env python3
"""Render the three-line closing block for one Board-attached session.

The Board files own durable facts. CLI flags describe only the live turn:
focus, mode, status, and next action. This script never writes.

Examples:
    python3 status.py BOARD --focus QD9 --mode implementation --next "run tests"
    python3 status.py BOARD --focus group:QD --mode discussion
    python3 status.py BOARD --focus QD9 --mode sourcing
"""
import argparse
import os
import re
import sys
import urllib.parse
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

from src.parse import parse_dir  # noqa: E402
from live.home import board_slug  # noqa: E402  (QE2 owns the slug; one copy)


MODES = ("discussion", "sourcing", "implementation", "review", "status")
STATUSES = ("ready", "working", "blocked", "done")
MARKERS = {"ready": "🟢", "working": "🔥", "blocked": "⛔", "done": "✅"}
LOOPBACK_URL = "http://127.0.0.1:5599"


try:                                            # the phase row, JL 260820
    from src.page_phase import phase_state, compact as phase_compact
except ImportError:                             # pragma: no cover
    sys.path.insert(0, str(Path(__file__).resolve().parent))
    from src.page_phase import phase_state, compact as phase_compact


def short_board_name(name, board=None):
    """A compact, human label for the clickable line.

    The BOARD'S OWN TITLE wins (JL 260802: of `boardform · QB/QB4`, "I think it
    should be haipipe-board · QB4"). `board.md`'s first heading is what the
    board calls itself, and the folder name is an accident of the day it was
    created: `01-boardform-260722` says nothing a reader wants, while its title
    line says `/haipipe-board`. This is the same rule the pages follow, that a
    name states what the thing IS.

    Falls back to the folder name with its `NN-` ordinal and `-YYMMDD` date
    stripped, for a board whose title is a sentence rather than a name.
    """
    if board is not None:
        try:
            head = (board / "board.md").read_text(encoding="utf-8").split("\n", 1)[0]
        except OSError:
            head = ""
        m = re.match(r"#\s+/?([A-Za-z][\w-]*)\s*[:·]", head)
        if m:
            return m.group(1)
    trimmed = re.sub(r"^\d+[-_]", "", name)
    trimmed = re.sub(r"[-_]\d{6}$", "", trimmed)
    return trimmed or name


def configured_base_url(root, explicit=None):
    """Resolve the reader-facing URL without executing the repo's env.sh.

    A CLI value wins, then the live environment, then the one machine-local
    HAIPIPE_BOARD_URL assignment in <served-root>/env.sh. Shared clones retain
    the loopback fallback without inheriting another machine's tailnet address.
    """
    if explicit:
        return explicit.rstrip("/")
    value = os.environ.get("HAIPIPE_BOARD_URL", "").strip()
    if value:
        return value.rstrip("/")

    # WALK UP for env.sh (JL 260803). `--root` defaults to cwd, and a person
    # running this from inside a board folder got the loopback URL even with a
    # tailnet address configured one or six directories above. The SPACE root
    # is where env.sh lives; every board is somewhere beneath it.
    start = Path(root).resolve()
    for candidate in [start, *start.parents]:
        try:
            lines = (candidate / "env.sh").read_text(encoding="utf-8").splitlines()
        except (OSError, UnicodeError):
            continue
        for line in lines:
            match = re.match(
                r"^\s*(?:export\s+)?HAIPIPE_BOARD_URL\s*=\s*"
                r"([\"']?)(https?://[^\"'\s#]+)\1\s*(?:#.*)?$",
                line,
            )
            if match:
                return match.group(2).rstrip("/")
    return LOOPBACK_URL


def group_code(group):
    match = re.match(r"^(Q[0-9A-Za-z]+)\b", group or "")
    return match.group(1) if match else ""


def group_label(group):
    return group or "unassigned · not in Pages"


def resolve_group(value, groups):
    value = (value or "").strip()
    if value.lower().startswith("group:"):
        value = value.split(":", 1)[1].strip()
    folded = value.casefold()
    matches = [
        group for group in groups
        if group.casefold() == folded or group_code(group).casefold() == folded
    ]
    return matches[0] if len(matches) == 1 else None


def resolve_focus(value, pages, groups):
    value = (value or "board").strip()
    if value.casefold() in {"board", "top", "board.md"}:
        return {"kind": "board", "label": "board · top", "anchor": "top",
                "file": "board.md", "group": "", "id": "board"}

    raw = value.split(":", 1)[1].strip() if value.lower().startswith("page:") else value
    folded = raw.casefold()
    page_matches = [
        page for page in pages
        if folded in {
            page["id"].casefold(),
            page["file"].casefold(),
            Path(page["file"]).stem.casefold(),
        }
    ]
    if len(page_matches) == 1:
        page = page_matches[0]
        return {
            "kind": "page",
            "label": f'page · {page["id"]} · {page["title"]}',
            "anchor": page["id"],
            "file": page["file"],
            "group": page.get("group", ""),
            "id": page["id"],
        }

    group = resolve_group(value, groups)
    if group:
        code = group_code(group)
        return {"kind": "group", "label": f"group · {group}",
                "anchor": "qlist", "file": "board.md", "group": group,
                "code": code, "id": code or group}
    return None


def board_url(board, root, base_url, anchor):
    """The link a human clicks. Prefers QC9's split site when the board has one,
    because that is what JL reads now; the one-file board.html stays as the
    fallback for boards that have not been split yet (JL 260731: board.html is
    on its way out, so nothing new should send anyone to it)."""
    try:
        relative = board.resolve().relative_to(root.resolve())
    except ValueError:
        return None
    path = urllib.parse.quote(relative.as_posix(), safe="/")
    base = f"{base_url.rstrip('/')}/{path}"
    site = board / "board"
    if not (site.is_dir() and (site / "index.html").exists()):
        return f"{base}/{'board.html'}#{anchor}"

    # anchor is a page id (QD2), a group code (QD), or an index anchor
    tail = anchor if anchor and anchor not in ("top", "qlist", "all") else ""

    long_url = f"{base}/board/index.html"
    resolved = not tail
    if tail:
        for html in sorted(site.glob("*/*.html")):
            if html.stem.split("-")[0] == tail:
                long_url = f"{base}/board/{html.parent.name}/{html.name}"
                resolved = True
                break
        else:
            if (site / f"{tail}.html").exists():
                long_url = f"{base}/board/{tail}.html"
                resolved = True

    # QE2 · the short route, and it is the DEFAULT once the generated site is
    # there. 78 of the 131 characters JL measured on 260802 were the path from
    # the SPACE root down to the board folder, and a chat surface expands
    # `[label](url)` back into `label (url)`, so a person reads that length no
    # matter what the strip does. `/b/<slug>[/<page>]` is a 302 from
    # `live/home.py`, which owns the slug so the route and the printed label
    # can never disagree about what a board is called.
    #
    # An anchor that resolves to no generated file keeps the long URL, because
    # the route answers 404 there: a long working link beats a short dead one.
    if resolved:
        slug = urllib.parse.quote(board_slug(board.name, board.parent.name), safe="")
        short = f"{base_url.rstrip('/')}/b/{slug}"
        return f"{short}/{urllib.parse.quote(tail, safe='')}" if tail else short
    return long_url


def render(board, focus="board", mode="status", status="ready", next_action="",
           queue="", root=None, base_url=None, no_url=False):
    board = Path(board).resolve()
    root = Path(root or Path.cwd()).resolve()
    base_url = configured_base_url(root, base_url)
    meta, pages, _warnings = parse_dir(board)
    groups = list(dict.fromkeys(
        [page.get("group", "") for page in pages if page.get("group")]
        + list(meta.get("groups", {}).keys())
    ))

    problem = ""
    target = resolve_focus(focus, pages, groups)
    if target is None:
        problem = f"focus {focus!r} does not identify one page or group"
        target = {"kind": "board", "label": f"unresolved · {focus}",
                  "anchor": "top", "file": "board.md", "group": "",
                  "id": str(focus)}

    derived_queue = target.get("group", "")
    explicit_queue = resolve_group(queue, groups) if queue else None
    if queue and explicit_queue is None:
        problem = f"queue {queue!r} does not identify one page group"
    elif explicit_queue and derived_queue and explicit_queue != derived_queue:
        problem = (
            f"queue {explicit_queue!r} contradicts the focus queue "
            f"{derived_queue!r}"
        )
    active_queue = explicit_queue or derived_queue

    if target["kind"] == "board" and not active_queue:
        queue_text = "board-level · cross-group"
    else:
        queue_text = group_label(active_queue)

    if mode == "sourcing" and target["kind"] == "board" and not explicit_queue:
        problem = "sourcing must serve one page or page group"

    url = board_url(board, root, base_url, target["anchor"])
    if url is None:
        problem = f"Board is outside the served root {root}"
    # JL 260801: a chat reply should not carry a raw address, and the terminal
    # expands every markdown link back into `label (url)`, so a link is the raw
    # address. The label already names the board and the page, and the reader
    # has the board open; `--url` opts back in for a reader who does not.
    # The label is a LINK by default again (JL 260802: "I cannot click the url
    # here, right?"). The 260801 default hid it because the TUI expanded a
    # markdown link back into `label (url)` and the raw address was glaring;
    # in a surface that renders markdown the label stays short AND clickable,
    # which is what was wanted both times. `--no-url` still opts out.
    if no_url:
        url = None

    queue_id = group_code(active_queue)
    if active_queue and not queue_id:
        queue_id = active_queue.split(" · ", 1)[0].strip()
    if target["kind"] == "board":
        location = f"{queue_id}/board" if queue_id else "board"
    elif target["kind"] == "group":
        location = queue_id or target["id"]
    else:
        location = f"{queue_id or 'unassigned'}/{target['id']}"

    if problem:
        status = "blocked"
        next_action = problem
    elif not next_action:
        next_action = f"continue {mode} on {location}"

    marker = MARKERS[status]
    # `QB/QB4` repeats itself: the page id already carries its group letter
    # (JL 260802 wrote it as `haipipe-board · QB4`). Keep the group only when
    # the id does not already start with it.
    if "/" in location:
        grp, _, pg = location.partition("/")
        if pg.upper().startswith(grp.upper()):
            location = pg
    attachment = f"{short_board_name(board.name, board)} · {location}"
    # Three rows, and the address rides INSIDE the board-page name (JL 260802).
    # The one-row version merged place and status and lost the shape: these are
    # three different things a reader looks for in three different moments, and
    # the link belongs on the name because the name is what it points at.
    # The address rides INSIDE the name, on whichever surface this lands on
    # (JL 260802: "embed this to the haipipe-paper · QA").
    #
    # A terminal has a real hyperlink escape, OSC 8, so the label is clickable
    # with the URL never drawn. A chat reply renders markdown, where `[a](b)`
    # does the same job. The wrong one on either surface shows the raw address,
    # which is the thing being removed, so pick by whether stdout is a TTY.
    # JL 260802 ruled the chat form: the address is SHOWN, in parentheses, not
    # hidden behind a label. A markdown link is only clickable where markdown
    # renders, and the strip is read in places that do not render it (a paste,
    # a log, a phone), where `[a](b)` is noise around an address you then cannot
    # copy. The short `/b/<board>/<page>` route is what makes showing it
    # bearable: it is one line, it is typeable, and it redirects to the long
    # path. The terminal keeps OSC 8, because there the label IS clickable.
    if url:
        if sys.stdout.isatty():
            where = f"🧭 \033]8;;{url}\033\\{attachment}\033]8;;\033\\"
        else:
            where = f"🧭 {attachment} ({url})"
    else:
        where = f"🧭 {attachment}"
    # A FOURTH row when the focus is one PAGE, because "working" does not say
    # WHERE in the page workflow you are (JL 260820: "how to update this so I
    # know which phase of the page I am in?"). Read from disk by
    # src/page_phase.py, the same module `cli/pagephase.py` prints in full, so
    # the two can never drift. Board- and group-level strips stay three rows:
    # a phase belongs to one page and averaging it over a group means nothing.
    rows = [where + "  ", f"{marker} {status} · {mode}  "]
    if target["kind"] == "page" and not problem:
        st = phase_state(board / target["file"], board)
        if st:
            rows.append(phase_compact(st) + "  ")
    rows.append(f"→ {next_action}")
    return "\n".join(rows)


def main(argv=None):
    parser = argparse.ArgumentParser(
        description="render one three-line Board closing block; never writes files"
    )
    parser.add_argument("board", help="Board folder containing board.md")
    parser.add_argument(
        "--focus", default="board",
        help="board, page id/path, or group:<id/title>",
    )
    parser.add_argument("--mode", choices=MODES, default="status")
    parser.add_argument("--status", choices=STATUSES, default="ready")
    parser.add_argument("--next", dest="next_action", default="")
    parser.add_argument(
        "--queue", default="",
        help="optional page-group id/title; normally derived from a page focus",
    )
    parser.add_argument(
        "--root", default=str(Path.cwd()),
        help="root served by serve.py; defaults to cwd",
    )
    parser.add_argument(
        "--base-url",
        default=None,
        help=(
            "reader-facing origin; defaults to HAIPIPE_BOARD_URL from the "
            "environment or <root>/env.sh, then loopback"
        ),
    )
    parser.add_argument(
        "--no-url",
        action="store_true",
        help="print a plain label with no link (the link is the default)",
    )
    parser.add_argument(
        "--url",
        action="store_true",
        help="accepted and ignored: a linked label is the default (JL 260802)",
    )
    args = parser.parse_args(argv)
    board = Path(args.board)
    if not (board / "board.md").is_file():
        parser.error(f"{board} has no board.md")
    print(render(
        board=board,
        focus=args.focus,
        mode=args.mode,
        status=args.status,
        next_action=args.next_action,
        queue=args.queue,
        root=args.root,
        base_url=args.base_url,
        no_url=args.no_url,
    ))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
