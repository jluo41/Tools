"""What leaves the paper: the delivery/ folder (outputs, build manifest, compile order, display register,
Rounds) and the G0-G5 gates read from files.
Moved from paper.py, which re-exports the names its callers import from there (`from live.paper import ...`)."""
import json
import re
from datetime import datetime
from pathlib import Path

from src.common import delivery_dir as source_delivery_dir, delivery_read_lane_dir

from live.paper_text import VERSION_DIR, read, scalar


def gates(d):
    """G0–G5 as haipipe-paper-workflow names them, each read from a file, never
    inferred from a percentage. A gate no file can answer says so."""
    b = d["board"]
    g = []
    s00 = d["story00"]
    folder = (b / s00["rel"]).parent if s00 and s00["rel"] else None
    receipt = folder is not None and any((folder / r).is_file() for r in
                                         ("workflow/selection.yaml", "handoff/paper-ideation.yaml"))
    g.append(("G0", "Ideation → Story",
              "✅ I3 receipt · %d Story page(s)" % len(d["stories"]) if receipt
              else "⬜ open · no I3 receipt · %d Story page(s)" % len(d["stories"])))
    g.append(("G1", "Story → work", "— read on the Story's workflow records"))
    g.append(("G2", "work → Story", "— read on the Story's §5 evidence rows"))
    rows = sum(len(s["sections"]) for s in d["story"])
    minted = sum(1 for s in d["story"] for r in s["sections"] if r["rel"])
    g.append(("G3", "Story → Section",
              ("✅ every Section Narrative row has a Section page" if minted == rows
               else "⬜ a Section Narrative row has no Section page") if rows else "⬜ no Section Narrative rows"))
    man = delivery_dir(b) / "build-manifest.json"
    if man.is_file():
        try:
            j = json.loads(man.read_text(encoding="utf-8"))
            rd = j.get("readiness") or {}
            g.append(("G4", "Section → Compile", "%s · %s/%s pages ready" % (
                j.get("status", "?"), rd.get("ready", "?"), rd.get("total", "?"))))
        except (OSError, ValueError):
            g.append(("G4", "Section → Compile", "manifest unreadable"))
    else:
        g.append(("G4", "Section → Compile", "⬜ no build · delivery/build-manifest.json absent"))
    g.append(("G5", "Round → next route", "%d Round page(s)" % len(d["rounds"])
              if d["rounds"] else "⬜ no Round yet"))
    return g


def _stamp(path):
    try:
        return datetime.fromtimestamp(Path(path).stat().st_mtime).strftime("%Y-%m-%d %H:%M")
    except OSError:
        return ""


def _mtime(path):
    try:
        return Path(path).stat().st_mtime
    except OSError:
        return 0.0


def _size(path):
    try:
        n = float(Path(path).stat().st_size)
    except OSError:
        return ""
    for u in ("B", "KB", "MB", "GB"):
        if n < 1024 or u == "GB":
            return ("%d B" % n) if u == "B" else "%.1f %s" % (n, u)
        n /= 1024.0
    return ""


def _toml_scalars(text):
    """`[section]` + `key = "value"` → {"section.key": value}; enough for paper-build.toml."""
    out, sect = {}, ""
    for line in (text or "").splitlines():
        t = line.strip()
        m = re.match(r"^\[([\w.-]+)\]", t)
        if m:
            sect = m.group(1)
            continue
        m = re.match(r'^([\w-]+)\s*=\s*"([^"]*)"', t) or re.match(r"^([\w-]+)\s*=\s*([^#\s]+)", t)
        if m:
            out[(sect + "." if sect else "") + m.group(1)] = m.group(2)
    return out


def _links(text):
    """The board's `## Links` rows: name  path."""
    out, on = {}, False
    for line in (text or "").splitlines():
        if line.startswith("## "):
            on = line.strip() == "## Links"
            continue
        m = re.match(r"^([\w-]+)\s{2,}(\S.*?)\s*$", line) if on else None
        if m:
            out[m.group(1)] = m.group(2)
    return out


def delivery_dir(b):
    """Paper output at Block storage; choose the latest built version if needed."""
    root = source_delivery_dir(b)
    if (root / "paper-build.toml").is_file() or (root / "build-manifest.json").is_file():
        return root
    versions = sorted((v for v in b.iterdir() if v.is_dir() and VERSION_DIR.match(v.name)),
                      key=lambda v: VERSION_DIR.match(v.name).group(1)) if b.is_dir() else []
    found = [source_delivery_dir(v) for v in versions if source_delivery_dir(v).is_dir()]
    built = [d for d in found if (d / "build-manifest.json").is_file()]
    return (built or found)[-1] if found else root


def delivery_info(d, ddir=None):
    """What leaves the paper: delivery/ (generated whole by haipipe-paper-assemble),
    its manifest, the compile order with every Section page's fragment and lanes,
    the display register, the checks, the Round pages and returned manuscripts.
    `ddir` reads one version's delivery/ in place of the Board's newest."""
    b = Path(d["board"]).resolve()
    text = read(b / "board.md")
    ddir = ddir or delivery_dir(b)
    at = ddir.relative_to(b).as_posix() + "/"               # delivery/ · j01_v1_<desk>/delivery/
    info = {"dir": ddir if ddir.is_dir() else None, "manifest": None, "toml": {}, "outputs": [],
            "returned": [], "order": [], "order_src": "", "pages": [], "displays": [], "display_note": "",
            "assets": [], "links": _links(text), "built": "", "stale": [], "rounds": []}
    for p in d["rounds"]:
        t = p["text"]
        folder = (b / p["rel"]).parent if p["rel"] else None
        subs = [x.name for x in sorted(folder.iterdir()) if x.is_dir() and not x.name.startswith(".")] if folder else []
        info["rounds"].append({"stem": p["stem"], "rel": p["rel"], "state": scalar(t, "state"),
                               "kind": scalar(t, "round-kind"), "from": scalar(t, "received-from"),
                               "at": scalar(t, "received-at"), "due": scalar(t, "response-due"),
                               "base": scalar(t, "base-build"), "venue": scalar(t, "venue-page"), "subs": subs})
    if info["dir"] is None:
        return info
    toml = _toml_scalars(read(ddir / "paper-build.toml"))
    info["toml"] = toml
    man = None
    if (ddir / "build-manifest.json").is_file():
        try:
            man = json.loads(read(ddir / "build-manifest.json"))
        except ValueError:
            man = {"error": "build-manifest.json is not valid JSON"}
    info["manifest"] = man
    info["built"] = (man or {}).get("built", "") or ""
    built_t = 0.0
    if info["built"]:
        try:
            built_t = datetime.fromisoformat(info["built"]).timestamp()
        except ValueError:
            built_t = 0.0
    # outputs: what paper-build.toml [outputs] names, else what sits in latex/ and word/
    named = [(k.split(".", 1)[1], v) for k, v in toml.items() if k.startswith("outputs.") and
             k.split(".", 1)[1] in ("main_pdf", "main_docx", "supplement_pdf", "supplement_docx")]
    # the cover letter shows on its own Delivery tab (_cover_panes), never beside the manuscript
    if not named:
        named = [("pdf", str(x.relative_to(ddir))) for x in sorted((ddir / "latex").glob("*.pdf")) if (ddir / "latex").is_dir()] + \
                [("docx", str(x.relative_to(ddir))) for x in sorted((ddir / "word").glob("*.docx")) if (ddir / "word").is_dir()]
    for what, rel in named:
        f = ddir / rel
        info["outputs"].append({"what": what.replace("_", " "), "rel": at + rel, "path": f, "exists": f.is_file(),
                                "size": _size(f), "stamp": _stamp(f),
                                "stale": bool(f.is_file() and built_t and _mtime(f) + 5 < built_t)})
    if (ddir / "word-feedback").is_dir():
        for f in sorted(ddir / "word-feedback").iterdir() if False else sorted((ddir / "word-feedback").iterdir()):
            if f.is_file() and not f.name.startswith("."):
                info["returned"].append({"name": f.name, "rel": at + "word-feedback/" + f.name, "path": f,
                                         "size": _size(f), "stamp": _stamp(f)})
    # compile order: the manifest's, else the Story's §8 block
    order = []
    if man and isinstance(man.get("order"), dict):
        order = [(x, "main") for x in man["order"].get("main", [])] + [(x, "appendix") for x in man["order"].get("appendix", [])]
        info["order_src"] = "build-manifest.json (%s)" % (man.get("order_source") or "").split(" · ")[0]
    elif d["story"] and d["story"][0]["order"]:
        order = [(x, "main" if "-Main-" in x else "appendix") for x in d["story"][0]["order"]]
        info["order_src"] = "Story §8 compile order (no build yet)"
    info["order"] = order
    mpages = {p.get("id"): p for p in (man or {}).get("pages", []) if isinstance(p, dict)}
    by_stem = {p["stem"]: p for p in d["pages"]}
    for pid, part in order:
        pg = by_stem.get(pid)
        rel = pg["rel"] if pg else ""
        folder = (b / rel).parent if rel else None
        md_t = _mtime(b / rel) if rel else 0.0
        frag = delivery_read_lane_dir(folder, "latex") / (pid + ".tex") if folder else None
        lanes = []
        if folder:
            lat = delivery_read_lane_dir(folder, "latex")
            pdfs = [x for x in (lat.glob(pid + "*.pdf") if lat.is_dir() else [])]
            lanes.append(("📜", "latex", bool(pdfs), max((_mtime(x) for x in pdfs), default=0.0)))
            wd = delivery_read_lane_dir(folder, "word") / (pid + ".docx")
            lanes.append(("📝", "word", wd.is_file(), _mtime(wd)))
            web = delivery_read_lane_dir(folder, "web") / "index.html"
            lanes.append(("🌐", "web", web.is_file(), _mtime(web)))
        mp = mpages.get(pid, {})
        stale = bool(rel and built_t and md_t > built_t + 5)
        if stale:
            info["stale"].append(pid)
        info["pages"].append({"id": pid, "part": part, "rel": rel, "state": scalar(pg["text"], "state") if pg else "",
                              "minted": bool(rel), "frag": bool(frag and frag.is_file()),
                              "frag_stale": bool(frag and frag.is_file() and md_t > _mtime(frag) + 5),
                              "lanes": lanes, "ready": mp.get("ready"), "reasons": mp.get("reasons") or [],
                              "warnings": mp.get("warnings") or [],
                              "outline": ((mp.get("outline") or {}).get("version") or ""),
                              "approval": ((mp.get("outline") or {}).get("approval") or "").split(" · ")[0],
                              "stale": stale})
    reg = read(ddir / "display-register.md")
    m = re.search(r"^Built .*$", reg, re.M)
    info["display_note"] = m.group(0) if m else ""
    fence = re.search(r"```text\n(.*?)```", reg, re.S)
    if fence:
        for line in fence.group(1).splitlines():
            if not line.strip() or line.startswith("PRINTED"):
                continue
            cells = re.split(r"\s{2,}", line.strip())
            if len(cells) >= 4:
                info["displays"].append(cells + [""] * (5 - len(cells)))
    sa = ddir / "latex" / "submission-assets"
    if sa.is_dir():
        info["assets"] = [{"name": x.name, "rel": at + "latex/submission-assets/" + x.name, "path": x, "size": _size(x)}
                          for x in sorted(sa.iterdir()) if x.is_file() and not x.name.startswith(".")]
    return info


def _not_ready_ids(rd):
    """`readiness.not_ready` from build-manifest.json: the engine writes one
    {"id", "reasons"} dict per page (build_delivery.py), older manifests a bare
    id string. Either way the Delivery card names the page, never the dict."""
    out = []
    for x in rd.get("not_ready") or []:
        out.append(str(x.get("id", "?")) if isinstance(x, dict) else str(x))
    return out
