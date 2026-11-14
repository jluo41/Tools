"""A paper's Evidence Items: each page's typed item contract, the hero items the paper hangs on, and the
Supporting Runs tree those items cite.
Moved from paper.py, which re-exports the names its callers import from there (`from live.paper import ...`)."""
import re
from pathlib import Path

from src.outline_version import plan_dir

from live.paper_text import VERSION_DIR, part_of, read
from live.paper_work_homes import _addresses


_LOCAL_RUN_RE = re.compile(r"`?(run-[\w.-]+)`?")
_MODES = ("reuse", "rerun", "new-run", "new run", "new-task", "new round", "registered", "complete")


def _parse_supporting(value):
    """`Execution · reuse · b03j02t01r04; Discovery · reuse · b01j01t02r02` →
    [{owner, mode, addr, raw}]. `[]` and blanks name nothing."""
    out = []
    v = (value or "").strip()
    if not v or v in ("[]", "—", "-", "none"):
        return out
    for part in v.split(";"):
        part = part.strip()
        if not part:
            continue
        toks = [t.strip().strip("`") for t in part.split("·")]
        addrs = _addresses(part)
        out.append({"owner": toks[0] if toks else "", "mode": " · ".join(toks[1:-1]) if len(toks) > 2 else "",
                    "addr": addrs[0] if addrs else "", "raw": part})
    return out


def _parse_local(value):
    """`Page · Evidence Item · reuse · run-value-0901-score → results/…/result.yaml` → {mode, run, result}."""
    v = (value or "").strip()
    left, _, right = v.partition("→")
    m = _LOCAL_RUN_RE.search(left)
    mode = next((t for t in _MODES if re.search(r"(^|·)\s*%s\s*(·|$)" % re.escape(t), left)), "")
    return {"mode": mode, "run": m.group(1) if m else "", "result": right.strip().strip("`"), "raw": v}


def _page_items(folder, stem):
    """The typed Evidence Item contract of one page: id · type · target · desc
    · Label · Expected · Supporting Runs · Local Run · Verified/Status.
    `### E…` is a live item; `#### E…` is a retired one (kept, marked). An item
    ends at the next heading of ANY level, so a retired block never leaks into
    the live item above it."""
    items = read(plan_dir(folder) / (stem + "-evidence-items.md"))
    out = []
    for m in re.finditer(r"^(#{3,4})\s+(E\d{2})-([A-Z]+)-([\w-]+)\s*·\s*(.*)$", items, re.M):
        retired = len(m.group(1)) == 4
        rest = [x.strip() for x in m.group(5).split("·")]
        target = rest[0] if (not retired and len(rest) > 1) else ""
        desc = " · ".join(rest[1:] if target else rest)
        tail = items[m.end():]
        nx = re.search(r"\n#{1,6}\s", tail)
        body = tail[:nx.start()] if nx else tail
        f = {k.strip().lower(): v.strip() for k, v in re.findall(r"^- \*\*([\w ]+)\*\*:\s*(.*)$", body, re.M)}
        out.append({"id": "%s-%s-%s" % m.group(2, 3, 4), "type": m.group(3), "target": target,
                    "desc": desc, "label": f.get("label", ""), "retired": retired,
                    "expected": f.get("expected", ""),
                    "supporting": _parse_supporting(f.get("supporting runs", "")),
                    "local": _parse_local(f.get("local run", "")),
                    "status": _item_status(f, _parse_local(f.get("local run", "")), folder)})
    return out


def _item_status(fields, local, folder):
    """An Evidence Item's state from its own lines. An explicit Status wins; else the
    Local Run's Result on disk says it is ready (items keep no Status line, so every
    card used to read "contract only", JL 260928); else a named Local Run is planned."""
    explicit = fields.get("status") or fields.get("accepted") or fields.get("verified")
    if explicit:
        return explicit
    result = (local.get("result") or "").split()
    if result and (folder / result[0]).is_file():
        return "Result ready"
    if local.get("mode") == "complete":
        return "Result not found"
    return "run planned" if local.get("run") or local.get("mode") else "contract only"


def item_name(item_id):
    """`E03-VALUE-lbp-main-effect` → `Evalue03`: type first, never a bare E03 (JL 260928)."""
    m = re.match(r"E(\d+)-([A-Z]+)", item_id or "")
    return "E%s%s" % (m.group(2).lower(), m.group(1)) if m else item_id


def hero_evidence(d):
    """The few Results the paper hangs on: every DISPLAY item on a Main or
    Appendix page (what the paper prints) and every VALUE item on the Abstract
    page (what the paper states first). Section pages keep their full Evidence Space."""
    b = d["board"]
    out = []
    for p in d["sections"]:
        folder_name = p["group"]["folder"] or (Path(p["rel"]).parts[0] if p["rel"] else "")
        if not p["rel"] or not (folder_name.endswith(("-Main", "-Appendix")) or VERSION_DIR.match(folder_name)):
            continue
        folder = (b / p["rel"]).parent
        abstract = p["stem"].lower().endswith("abstract")
        for it in _page_items(folder, p["stem"]):
            if it["retired"]:
                continue
            if it["type"] in ("DISPLAY", "TABLE") or (abstract and it["type"] == "VALUE"):
                it.update({"page": p["stem"], "rel": p["rel"],     # a version holds both: the part is in the stem
                           "part": "appendix" if folder_name.endswith("-Appendix") else part_of(p["stem"]),
                           "why": "printed display" if it["type"] != "VALUE" else "stated in the Abstract"})
                out.append(it)
    return out


def supporting_tree(d):
    """The owner-native Runs this paper's Evidence Items cite, as a
    Block › Job › Task › Run tree per owner (Execution = the Task home,
    Discovery = the Discovery home). Each Run lists who uses it."""
    b = d["board"]
    cited, loose = {}, []
    for p in d["pages"]:
        if not p["rel"]:
            continue
        for it in _page_items((b / p["rel"]).parent, p["stem"]):
            if it["retired"]:
                continue
            for sp in it["supporting"]:
                owner = "Discovery" if sp["owner"].lower().startswith("discover") else "Execution"
                user = {"page": p["stem"], "rel": p["rel"], "item": it["id"], "label": it["label"], "mode": sp["mode"]}
                if not sp["addr"]:
                    loose.append(dict(user, owner=owner, raw=sp["raw"]))
                    continue
                cited.setdefault((owner, sp["addr"]), []).append(user)
    trees = {"Execution": d["blocks"]["tree"], "Discovery": d["disc"]["tree"]}
    out = {"Execution": {}, "Discovery": {}, "loose": loose, "n": len(cited)}
    for (owner, addr), users in sorted(cited.items()):
        m = re.match(r"^(b\d{2})(j\d{2})?(t\d{2})?(r\d{2})?$", addr)
        if not m:
            continue
        bb, jj, tt, rr = m.groups()
        blk = next((x for x in trees[owner] if x["addr"] == bb), None)
        job = next((x for x in (blk["jobs"] if blk else []) if x["addr"] == bb + (jj or "")), None) if jj else None
        task = next((x for x in (job["tasks"] if job else []) if x["addr"] == bb + (jj or "") + (tt or "")), None) if tt else None
        found = []
        if task is not None and rr:
            found = [(stem, path) for stem, path in task["ticket_list"] if stem == rr or stem.startswith(rr + "_")]
        status = ""
        for stem, _ in found:
            status = task["receipt_map"].get(stem, status)
        node = out[owner].setdefault(bb, {"blk": blk, "jobs": {}})
        jnode = node["jobs"].setdefault(jj or "", {"job": job, "tasks": {}})
        tnode = jnode["tasks"].setdefault(tt or "", {"task": task, "runs": []})
        tnode["runs"].append({"addr": addr, "r": rr or "", "tickets": found, "status": status, "users": users,
                              "on_disk": bool(found) if rr else (task is not None if tt else job is not None)})
    return out
