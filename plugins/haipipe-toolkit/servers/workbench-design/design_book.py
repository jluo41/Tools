"""A Design Method Book on the focus page: the designer of one kind of thing (a message, a checklist), beside the Design Board that runs it,
as the Insight Question Book sits beside its Board. It holds method types (M01 goal only, M02 overall performance …),
side by side, and each type's signed versions. Its views, in plain words, each answering one question:

    Method     what each method type does, step by step (① See input … ⑤ Review whole), in its newest version
    Versions   each type's signed versions: what changed from the one before, who signed, which Jobs ran it
    Ideas      the proposals the Board's Jobs and experiments sent back; a type's next version is cut from here
    Scorecard  how each method did on the Boards it serves: pass rate, first try, and predicted vs observed

then the shared MindMap and 🧭 Around the Work (the page adds both). Read-only; a version is signed by a person
through haipipe-design-method, never here.
"""
from __future__ import annotations

from pathlib import Path

from live import design_reader as R
from live import design_views as V
from live.design_focus import _big, _link, _tabs, _section, _kv, _copy, _step
from live.frame import esc, pop, reader, table

BOOK_VIEWS = (("method", "Method"), ("versions", "Versions"), ("ideas", "Ideas"), ("scorecard", "Scorecard"))
STEP_ORDER = ("① See input", "② Reason ideas", "③ Conduct process", "④ Review item", "⑤ Review whole")

VIEW_SKILLS = {
    "method": (("haipipe-design-method", "keeps each method type's five steps, frozen once signed"),),
    "versions": (("haipipe-design-method", "cuts a type's next version from a signed proposal"),),
    "ideas": (("haipipe-design-method", "writes a proposal from a Job or an experiment"),),
    "scorecard": (("haipipe-design-method", "scores each method from what the experiments returned"),),
}


def _steps_table(rel: dict) -> str:
    steps = rel["steps"]
    rows = [(esc(k), esc(str(steps.get(k, "—")))) for k in STEP_ORDER if k in steps]
    return table(("step", "what it does"), rows) if rows else ""


def _changed(a: dict, b: dict) -> list:
    return [k for k in STEP_ORDER if str(a["steps"].get(k, "")) != str(b["steps"].get(k, ""))]


def _job_links(rel: dict, root: Path) -> str:
    return " · ".join(_link(j["path"], root, j["name"]) for j in rel["jobs"]) or "no Job yet"


def _signed(rel: dict) -> bool:
    return rel["signed"].startswith("✅")


def _method(book: dict, folder: Path, root: Path) -> tuple:
    kinds = [k for k in book["types"] if k["releases"]]
    if not kinds:
        return "", _big("No method yet", "next: add the first method type")
    names = " · ".join(f'{k["method"]} {k["title"]}'.strip() for k in kinds)
    big = _big((f'The {book["channel"]} designer: ' if book["channel"] else "") + names,
               "all signed" if all(_signed(r) for k in kinds for r in k["releases"]) else "waits for your sign")
    tabs = []
    for k in kinds:
        new = k["releases"][-1]
        sees = "".join(f"<li>{esc(str(s))}</li>" for s in new["sees"])
        body = (_kv([("version", esc(new["version"])), ("signed", esc(new["signed"] or "not yet")),
                     ("Jobs", _job_links(new, root)), ("face", _link(k["path"], root, k["name"]))])
                + _steps_table(new) + (f"<p>Step ① sees</p><ul>{sees}</ul>" if sees else "")
                + (pop(reader(new["card_path"], root), new["card_path"].name, "Open") if new["card_path"].is_file() else ""))
        tabs.append((f'{k["method"]} {k["title"]}'.strip(), new["signed"] or new["state"], body))
    res = big + _section("🪜 The five steps", _tabs("method", tabs), "")
    rows = [(esc(f'{k["method"]} {k["title"]}'.strip()), esc(str(k["releases"][-1]["steps"].get(STEP_ORDER[0], "—"))))
            for k in kinds]
    res += _section("👀 What step ① sees", table(("method", "① See input"), rows), "")
    from live import design as _design                       # the channel's own rules: the Guide's venue pack
    rules = _design.venue_defaults(book["channel"]) if book["channel"] else {}
    if rules:
        res += _section("📏 The channel's rules", table(("rule", "the channel keeps"),
                                                        [(esc(k), esc(v)) for k, v in rules.items()]), book["channel"])
    return "", res


def _versions(book: dict, folder: Path, root: Path) -> tuple:
    rels = book["releases"]
    waits = [r for r in rels if not _signed(r)]
    big = _big("Every version is signed" if rels and not waits else
               f'{len(waits)} version{"" if len(waits) == 1 else "s"} wait{"s" if len(waits) == 1 else ""} for your sign'
               if rels else "No version yet", "all signed" if rels and not waits else "waits for your sign" if rels else "")
    tabs, rows = [], []
    for k in book["types"]:
        mine = k["releases"]
        for n, rel in reversed(list(enumerate(mine))):
            before = mine[n - 1] if n else None
            change = (", ".join(_changed(before, rel)) or "nothing in the steps") if before else "the first signed version"
            body = _kv([("changed from " + (before["version"] if before else "—"), esc(change)),
                        ("signed", esc(rel["signed"] or "not yet")), ("Jobs", _job_links(rel, root)),
                        ("face", _link(rel["path"], root, rel["name"]))]) + _steps_table(rel)
            tabs.append((rel["id"], rel["signed"] or rel["state"], body))
        rows += [(esc(f'{a["id"]} → {b["version"]}'), esc(", ".join(_changed(a, b)) or "nothing")) for a, b in zip(mine, mine[1:])]
    res = big + _section("🔖 The versions", _tabs("release", tabs), "")
    res += _section("🧭 What changed between versions", table(("from → to", "steps that changed"), rows) if rows else "", "")
    return "", res


def _ideas(book: dict, folder: Path, root: Path) -> tuple:
    props = book["proposals"]
    waiting = [p for p in props if p["state"] in ("waiting", "open", "")]
    big = _big(f'{len(waiting)} idea{"" if len(waiting) == 1 else "s"} wait{"s" if len(waiting) == 1 else ""} for you' if waiting else
               "No idea waits" if props else "No idea yet", "waiting for you" if waiting else "")
    tabs = []
    for p in props:
        src = Path(p["from"]) if p["from"] else None
        src_path = (folder.parent.parent / src) if src else None
        body = _kv([("changes", esc(p["step"] or p["kind"])),
                    ("from", _link(src_path, root, src_path.name) if src_path and src_path.exists() else esc(p["from"] or "—")),
                    ("state", esc(p["state"] + (f' · taken in {p["taken_in"]}' if p["taken_in"] else ""))),
                    ("file", pop(reader(p["path"], root), p["path"].name, "Open"))]) + f'<p>{esc(p["body"])}</p>'
        tabs.append((p["title"], "waiting for you" if p in waiting else p["state"], body))
    res = big + _section("💡 Proposals", _tabs("idea", tabs), f'{len(waiting)} wait{"s" if len(waiting) == 1 else ""} for you' if waiting else "")
    rows = [(f'Sign or return the idea {esc(p["title"])}', "the next version is cut only when a person signs",
             "waiting for you", pop(reader(p["path"], root), p["path"].name, "Open")) for p in waiting]
    rows.append(("Write a new idea", "from a Job's ranking or an experiment's scores", "open",
                 _copy("run-propose-method-<slug>", "Block", folder, root)))
    return _step("✍️ Ideas to settle", rows), res


def _scorecard(book: dict, folder: Path, root: Path) -> tuple:
    rows, tested_any = [], 0
    for board in book["boards"]:
        b = R.board(board)
        for rel in book["releases"]:
            js = [j for j in b["jobs"] if j["release"] == rel["id"]]
            if not js:
                continue
            live = sum((V._live(j["designs"]) for j in js), [])
            sc = [s for (jid, _), s in b["scores"].items() if jid in {j["id"] for j in js}]
            tested_any += len(sc)
            rows.append((esc(rel["id"]), _link(board, root, board.name),
                         " · ".join(_link(j["path"], root, j["id"]) for j in js),
                         esc(f'{100 * len(V._passed(live)) // max(len(live), 1)}%' if live else "—"),
                         esc(f'{sum(d["first_try"] for d in live)} of {len(live)}' if live else "—"),
                         esc(f'{len(sc)} designs' if sc else "not yet"),
                         esc(f'{sum(s.get("in_range") == "✓" for s in sc)} of {len(sc)}' if sc else "—")))
    big = _big(f"Tested on {tested_any} design{'' if tested_any == 1 else 's'}: a hint, not a verdict" if tested_any
               else "No method tested yet", "few arms tested" if tested_any else "waits on an experiment")
    res = big + _section("🏅 Each method, on the Boards it serves",
                         table(("method", "Board", "Jobs", "pass rate", "first try", "tested", "in range"), rows) if rows else "",
                         "from the Boards' own scores")
    return "", res


PARTS = {"method": _method, "versions": _versions, "ideas": _ideas, "scorecard": _scorecard}


def book_view(folder: Path, root: Path, key: str) -> tuple:
    """(process, results) of one Book view."""
    return PARTS[key](R.method_book(folder, root), folder, root)
