"""Move a Page's older Evidence Items into cards: `draft/<stem>-evidence-items.md` → `evidence/cards.yaml`.

A Page made before 2026-10-16 keeps its evidence as typed Evidence Items (`### E01-CITE-<slug> · C1.P1.B3 · …`
blocks with `Supporting Runs`, `Local Run` and `Decide` lines). The draft Task's 3 · Evidence step reads cards
(../SKILL.md, JL 261016), so this writes them from the items, one card per Discovery or work Task:

    python from_items.py <task> [<task> …]            dry run: what each Task's cards would hold
    python from_items.py <task> [<task> …] --write    write evidence/cards.yaml and evidence/proposals.md

1. **Kind by world**: a Discovery Supporting Run gives a CITE item, an Execution one a VALUE item (JL 261016: "if the
   value is from the citation, then it should be the Ecite"); each item keeps its Evidence Item id (`item:`) and
   its label.
2. **for**: the sentence numbers of the Bullets the item serves, read from §1 of the newest draft
   (`- B<k> · S<n> · …` under `### C<x>.P<y>`); a suffixed id (`S3a`) counts as its number; none found → 0.
3. **need** when there is nothing to read: a Run still to make (`new-run`, `new-task`, `new-job`, proposed at that
   level), an address that no longer resolves in the Project's `discovery/` or `work/` (say a Block that moved), or
   no Supporting Run at all. `cards.py propose` turns each need into a line a person ticks.
4. **Left out**: DISPLAY items (a figure or table is haipipe-display's), and items decided `defer` or `drop`, or
   retired: no printed sentence needs them. The header counts them.

The Evidence Items file stays: the Page's export still reads it for its gates until haipipe-draft's exporter reads
cards. Nothing else is touched.
"""
import argparse
import datetime as dt
import re
import sys
from pathlib import Path

import yaml

sys.path.insert(0, str(Path(__file__).resolve().parent))
import cards  # noqa: E402

ITEM = re.compile(r"^### (E\d+[a-z]?)-(CITE|VALUE|DISPLAY)-([\w-]+)\s*·\s*([^·\n]*)(?:·\s*(.*))?$")
FIELD = re.compile(r"^- \*\*([\w ]+)\*\*:\s*(.*)$")
SUPPORT = re.compile(r"(Discovery|Execution)\s*·\s*([\w -]+?)\s*·\s*(b\d+(?:j\d+)?(?:t\d+)?(?:r\d+)?)\b")
BULLET = re.compile(r"^- B(\d+) · S(\d+)[a-z]* · ")
HEAD = re.compile(r"^### (C\d+\.P\d+)\b")
DRAFT = re.compile(r"-(?:draft|outline)-v(\d+(?:\.\d+)*)\.md$")


def newest_draft(task: Path):
    files = [p for p in (task / "draft").glob("*.md") if DRAFT.search(p.name)]
    return max(files, key=lambda p: tuple(int(x) for x in DRAFT.search(p.name).group(1).split(".")), default=None)


def sentence_map(draft: Path) -> dict:
    """`C1.P1.B3` → 2, from §1 Structure of the draft (the first `## ` part whose title starts `1 ·`)."""
    out, para, inside = {}, None, False
    for line in draft.read_text(encoding="utf-8", errors="replace").splitlines() if draft else []:
        if line.startswith("## "):
            if inside:
                break
            inside = bool(re.match(r"## 1\s*·", line))
            continue
        h = HEAD.match(line)
        if inside and h:
            para = h.group(1)
        b = BULLET.match(line)
        if inside and para and b:
            out[f"{para}.B{b.group(1)}"] = int(b.group(2))
    return out


def read_items(path: Path) -> list:
    items, cur = [], None
    for line in path.read_text(encoding="utf-8", errors="replace").splitlines():
        m = ITEM.match(line)
        if m:
            cur = {"id": f"{m.group(1)}-{m.group(2)}-{m.group(3)}", "type": m.group(2), "where": m.group(4).strip(),
                   "title": (m.group(5) or "").strip(), "fields": {}}
            items.append(cur)
            continue
        f = FIELD.match(line)
        if cur and f:
            cur["fields"][f.group(1).strip()] = f.group(2).strip()
        elif line.startswith("## "):
            cur = None
    return items


def addresses(where: str) -> list:
    return re.findall(r"C\d+\.P\d+\.B\d+", where)


def dotted(compact: str) -> str:
    return ".".join(re.findall(r"[bjtr]\d+", compact))


def left_out(it: dict) -> str:
    decide = it["fields"].get("Decide", "")
    local = it["fields"].get("Local Run", "")
    if it["type"] == "DISPLAY":
        return "display"
    if re.search(r"☑\s*(defer|drop)", decide):
        return re.search(r"☑\s*(defer|drop)", decide).group(1)
    if "(retired)" in local or "retired" in it["fields"].get("Status", ""):
        return "retired"
    return ""


def build(task: Path) -> tuple:
    stem = task.name
    items_md = task / "draft" / f"{stem}-evidence-items.md"
    if not items_md.is_file():
        return None, {"no items": 1}
    project = cards.project_root(task)
    smap = sentence_map(newest_draft(task))
    by_card, needs, counts = {}, {"cite": [], "value": []}, {}
    for it in read_items(items_md):
        why = left_out(it)
        if why:
            counts[why] = counts.get(why, 0) + 1
            continue
        fors = sorted({smap[a] for a in addresses(it["where"]) if a in smap}) or [0]
        base = {"for": fors, "item": it["id"]}
        label = it["fields"].get("Label")
        if label:
            base["label"] = label
        support = it["fields"].get("Supporting Runs", "")
        found = SUPPORT.findall(support)
        if not found:
            kind = "cite" if it["type"] == "CITE" else "value"
            needs[kind].append({"need": f"{it['title'] or it['id']}: no Supporting Run names a source"
                                + (f" ({support[:140]})" if support and support != "[]" else ""), **base})
            counts["need"] = counts.get("need", 0) + 1
            continue
        gone = {"cite": [], "value": []}                      # addresses that no longer resolve, one need per item
        for world, mode, addr in found:
            kind = "cite" if world == "Discovery" else "value"
            address = dotted(addr)
            parts = address.split(".")
            if mode.startswith("new"):
                level = {4: "run", 3: "run", 2: "task", 1: "job"}[len(parts)]
                needs[kind].append({"need": f"{it['title'] or it['id']}: the {mode} {world} Run is not made yet",
                                    "propose": {"level": level, "in": address}, **base})
                counts["need"] = counts.get("need", 0) + 1
                continue
            try:
                cards.resolve(project, kind, address)
            except ValueError:
                gone[kind].append(address)
                continue
            source, run = ".".join(parts[:3]), parts[3] if len(parts) == 4 else None
            entry = {**({"run": run} if run else {}), **base}
            if not run:
                entry["need"] = f"{it['title'] or it['id']}: name the Run of {source} it reads"
                counts["need"] = counts.get("need", 0) + 1
            by_card.setdefault((kind, source), []).append(entry)
            counts[kind] = counts.get(kind, 0) + 1
        for kind, addrs in gone.items():
            if addrs:
                needs[kind].append({"need": f"{it['title'] or it['id']}: {', '.join(addrs)} no longer {'resolves' if len(addrs) == 1 else 'resolve'} in "
                                            f"{cards.THEME[kind]}/; point it at the Runs that replaced them", **base})
                counts["need"] = counts.get("need", 0) + 1
    out = [{"kind": k, "source": s, "items": v} for (k, s), v in by_card.items()]
    titles = {"cite": "Sources still needed", "value": "Results still needed"}
    out += [{"kind": k, "title": titles[k], "items": v} for k, v in needs.items() if v]
    return out, counts


def write(task: Path, card_list: list, counts: dict) -> Path:
    ev = task / "evidence"
    ev.mkdir(exist_ok=True)
    left = ", ".join(f"{n} {k}" for k, n in sorted(counts.items()) if k in ("display", "defer", "drop", "retired"))
    head = (f"# {task.name}'s evidence (haipipe-evidence cards), moved from draft/{task.name}-evidence-items.md on "
            f"{dt.date.today():%y%m%d} by from_items.py.\n"
            f"# `for` is the sentence number (S<n>) of the newest draft's §1; `item` the Evidence Item it came from.\n"
            f"# Left out: {left or 'nothing'}. The Page's export still reads the Evidence Items for its gates.\n"
            f"# Check: haipipe-evidence scripts/cards.py check.\n")
    path = ev / "cards.yaml"
    path.write_text(head + yaml.safe_dump({"evidence": card_list}, sort_keys=False, allow_unicode=True, width=120),
                    encoding="utf-8")
    cards.write_proposals(ev / "proposals.md", cards.proposals(card_list, task.name))
    return path


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("tasks", nargs="+", type=Path)
    ap.add_argument("--write", action="store_true")
    a = ap.parse_args()
    for task in a.tasks:
        card_list, counts = build(task)
        if card_list is None:
            print(f"{task.name}: no draft/{task.name}-evidence-items.md, nothing to move")
            continue
        n_items = sum(len(c["items"]) for c in card_list)
        summary = " · ".join(f"{k} {v}" for k, v in sorted(counts.items()))
        print(f"{task.name}: {len(card_list)} cards, {n_items} items ({summary})")
        if a.write and card_list:
            print("  wrote", write(task, card_list, counts))
    return 0


if __name__ == "__main__":
    sys.exit(main())
