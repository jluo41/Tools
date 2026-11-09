"""A Design Method Book on the focus page (JL 261109: "we should have both designer block and design block, just like
Workbench Insight"): the method's own Block, beside the Design Board that runs it, as the Insight Question Book sits
beside its Board. Its views, in plain words, each answering one question:

    Method     what the newest release does, step by step (① See input … ⑤ Review whole)
    Versions   each release: what it was cut from, what changed from the one before, who signed, which Jobs ran it
    Ideas      the proposals the Board's Jobs and experiments sent back; the next release is cut from here
    Scorecard  how each release did on the Boards it serves: pass rate, first try, and predicted vs observed

then the shared MindMap and 🧭 Around the Work (the page adds both). Read-only; a release is signed by a person
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
    "method": (("haipipe-design-method", "keeps each release's five steps, frozen once signed"),),
    "versions": (("haipipe-design-method", "cuts the next release from a signed proposal"),),
    "ideas": (("haipipe-design-method", "writes a proposal from a Job or an experiment"),),
    "scorecard": (("haipipe-design-method", "scores each release from what the experiments returned"),),
}


def _steps_table(rel: dict) -> str:
    steps = rel["steps"]
    rows = [(esc(k), esc(str(steps.get(k, "—")))) for k in STEP_ORDER if k in steps]
    return table(("step", "what it does"), rows) if rows else ""


def _changed(a: dict, b: dict) -> list:
    return [k for k in STEP_ORDER if str(a["steps"].get(k, "")) != str(b["steps"].get(k, ""))]


def _job_links(rel: dict, root: Path) -> str:
    return " · ".join(_link(j["path"], root, j["name"]) for j in rel["jobs"]) or "no Job yet"


def _method(book: dict, folder: Path, root: Path) -> tuple:
    rels = book["releases"]
    if not rels:
        return "", _big("No release yet", "next: cut the first release")
    new = rels[-1]
    big = _big(f'{new["id"]} is the newest release: {new["title"] or new["from"]}',
               "signed" if new["signed"].startswith("✅") else "waits for your sign")
    res = big + _section("🪜 The five steps", _steps_table(new), new["id"])
    sees = "".join(f"<li>{esc(str(s))}</li>" for s in new["sees"])
    res += _section("👀 What step ① sees", f"<ul>{sees}</ul>" if sees else "", f'{len(new["sees"])} parts')
    res += _section("📄 The frozen recipe", pop(reader(new["path"] / "method.md", root), "method.md", "Open")
                    + f' <span class=mut>cut from {esc(new["from"])}</span>' if (new["path"] / "method.md").is_file() else "",
                    "frozen")
    return "", res


def _versions(book: dict, folder: Path, root: Path) -> tuple:
    rels = book["releases"]
    signed = sum(r["signed"].startswith("✅") for r in rels)
    big = _big(f'{len(rels)} release{"" if len(rels) == 1 else "s"}, {signed} signed' if rels else "No release yet",
               "all signed" if rels and signed == len(rels) else "waits for your sign" if rels else "next: cut the first release")
    tabs = []
    for k, rel in reversed(list(enumerate(rels))):
        before = rels[k - 1] if k else None
        change = (", ".join(_changed(before, rel)) or "nothing in the steps") if before else "the first release"
        body = _kv([("cut from", esc(rel["from"])), ("changed from " + (before["id"] if before else "—"), esc(change)),
                    ("signed", esc(rel["signed"] or "not yet")), ("Jobs", _job_links(rel, root)),
                    ("face", _link(rel["path"], root, rel["name"]))]) + _steps_table(rel)
        tabs.append((rel["id"], rel["signed"] or rel["state"], body))
    res = big + _section("🔖 The releases", _tabs("release", tabs), rels[-1]["id"] if rels else "")
    rows = [(esc(f'{a["id"]} → {b["id"]}'), esc(", ".join(_changed(a, b)) or "nothing"),
             "one step" if len(_changed(a, b)) == 1 else f'{len(_changed(a, b))} steps')
            for a, b in zip(rels, rels[1:])]
    res += _section("🧭 What changed between releases", table(("from → to", "steps that changed", "how much"), rows) if rows else "",
                    "one step a release" if rows and all(len(_changed(a, b)) <= 1 for a, b in zip(rels, rels[1:])) else "")
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
    rows = [(f'Sign or return the idea {esc(p["title"])}', "the next release is cut only when a person signs",
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
               else "No release tested yet", "few arms tested" if tested_any else "waits on an experiment")
    res = big + _section("🏅 Each release, on the Boards it serves",
                         table(("release", "Board", "Jobs", "pass rate", "first try", "tested", "in range"), rows) if rows else "",
                         "from the Boards' own scores")
    return "", res


PARTS = {"method": _method, "versions": _versions, "ideas": _ideas, "scorecard": _scorecard}


def book_view(folder: Path, root: Path, key: str) -> tuple:
    """(process, results) of one Book view."""
    return PARTS[key](R.method_book(folder, root), folder, root)
