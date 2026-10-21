"""A Studio topic of related papers, each read with excalidraw-read: the theme first, then one row per paper.
Asked 261013 on Paper-LLMRecPhy-Quick: "add more sNN to show the related paper by topics, just like ... s52-t06 ...
using /excalidraw-read"; "we might want to see the most relevant papers in the details".

    python topic_drawing.py draw <topic folder>      redraw one topic (what its builder calls)

The topic's face carries a `related:` yaml block; each paper's reading is `reads/<id>-<slug>/reading.yaml`
(ref/reading-spec.md), its PDF the Block's `related/paper/<file>.pdf`:

    related:
      key: <the theme's point, one sentence>
      what: <what these papers share>
      why: <why it matters to our paper>
      papers:                         # reading order
      - id: p01
        item: Gillani & Baig 2026     # the start of its related/related.md item
        says: <the paper in one line: its frames' key point>
        ref: {title: ..., authors: ..., venue: ..., year: ..., link: ...}   # its reference, from Crossref or arXiv
      open: [<a choice the person makes>, ...]

Act 1 · the theme: the key point, what the papers share and why it matters, one card per paper (its full title),
the open choices in red. Then one row per paper: its reference first (title, every author, venue, year, link, PDF,
deep read; JL 261013: "for each paper, you didn't give the paper reference, the names, the authors"), then, as
excalidraw-task draws a video's transcript, its pages with the read passages highlighted and a numbered note level
with each (Says · Comment · → Our paper), then its logic as a chain of steps and the links to our paper. A paper with no reading yet (no PDF) gets one red card from its related.md row.
Written with haipipe-studio's canvas.write, so a person's marks survive every rebuild.
"""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

import yaml

HERE = Path(__file__).resolve().parent
SKILLS = HERE.parents[2]                                              # skills/1_base
sys.path.insert(0, str(SKILLS / "excalidraw/excalidraw-task/scripts"))
import task_drawing as td  # noqa: E402   heading, rows_of, fit, transcript_frame, read_of, circled
from draw import INK, RED, Drawing  # noqa: E402

US = "Our paper"


def face_cfg(topic: Path) -> dict:
    """The face's `related:` yaml block; {} when the face has none."""
    face = topic / f"{topic.name}.md"
    m = re.search(r"```yaml\s*\n(related:.*?)```", face.read_text(encoding="utf-8"), re.S) if face.is_file() else None
    return ((yaml.safe_load(m.group(1)) or {}).get("related") or {}) if m else {}


def related_rows(block: Path) -> list[dict]:
    """The Block's related/related.md rows, each a dict keyed by its lower-cased column names."""
    table = block / "related" / "related.md"
    heads, rows = [], []
    for line in table.read_text(encoding="utf-8").splitlines() if table.is_file() else []:
        if not line.startswith("|") or set(line.replace("|", "").strip()) <= set("-: "):
            continue
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        if not heads:
            heads = [c.lower() for c in cells]
            continue
        rows.append(dict(zip(heads, cells + [""] * (len(heads) - len(cells)))))
    return rows


def who(item: str) -> str:
    return item.split(" · ")[0].strip()


def pdf_of(p: dict) -> str:
    """The paper's kept PDF, `paper/<file>.pdf` from its related.md link, or ''."""
    link = str((p.get("row") or {}).get("link", "")).strip("` ")
    return link if link.lower().endswith(".pdf") else ""


def state(p: dict) -> str:
    return ("📄 read from its PDF" if p["reading"] else
            f"⬜ PDF kept ({pdf_of(p)}), not read yet" if pdf_of(p) else "❓ no PDF yet: its abstract only")


def theme_frame(d: Drawing, title: str, cfg: dict, papers: list[dict]) -> dict:
    """⓪ the theme: its point, what the papers share and why it matters, the papers in reading order, the open
    choices in red."""
    f = d.frame(f"⓪ {title}", td.W, td.TALLEST)
    d.room(f)
    n = len(papers)
    read = sum(1 for p in papers if p["reading"])
    sub = f"{n} papers, {read} read from their PDF · one row each below: its highlighted pages, then its logic"
    y = td.heading(d, f"⓪ {title}", sub, str(cfg.get("key") or "❓ no key point in the face's related: yaml"))
    rows = [[("What these papers share", [str(cfg.get("what") or "❓")], INK),
             ("Why it matters to our paper", [str(cfg.get("why") or "❓")], INK)]]
    cards = [(f"{p['id']} · {who(p['item'])}", [f"“{ref(p)['title']}”", str(p.get("says") or ""), state(p)],
              INK if p["reading"] else RED) for p in papers]
    rows += [cards[k:k + 3] for k in range(0, len(cards), 3)]
    labels = ["why it matters", "the papers, in reading order"] + [""] * len(cards)
    if cfg.get("open"):
        rows.append([("❓ Open: yours to decide", [f"❓ {q}" for q in cfg["open"]], RED)])
        labels.append("")
    return td.fit(d, f, td.rows_of(d, y, rows, labels))


def logic_frame(d: Drawing, p: dict, spec: dict) -> dict:
    """A paper's own argument as a chain of steps, each naming the passages it rests on and, under its words, how that
    step was done (a step's optional `how`: its data, models, procedure or measures; JL 261019: "after reading it, we
    know how this paper is conducted", then "why is this not embedded within ... to make the logic more fluent"), then
    one card per claim of ours that a passage links to."""
    name = f"{p['id']} · {who(p['item'])} · its logic, and our link"
    f = d.frame(name, td.W, td.TALLEST)
    d.room(f)
    paper = spec.get("paper") or {}
    y = td.heading(d, name, str(paper.get("cite") or p["item"]), str(p.get("says") or paper.get("title") or ""))
    steps = [(f"{td.ROLE_MARK.get(st.get('role'), '▪')} {st.get('role', '')} · " +
              " ".join(td.circled(td.excerpt_number(e, 0)) for e in st.get("excerpts") or [] if re.fullmatch(r"E\d+", str(e))),
              [str(st.get("text", ""))] + [h if re.match(r"[^:]{1,24}: ", str(h)) else f"· {h}" for h in st.get("how") or []], INK)
             for st in spec.get("logic") or []]                    # `how`: how this step was done (JL 261019)
    rows = [steps[k:k + 3] for k in range(0, len(steps), 3)]
    labels = (["its argument"] + [""] * (len(steps) - 1)) if steps else []
    targets = {t["id"]: t.get("label", t["id"]) for t in (spec.get("ours") or {}).get("targets") or []}
    links = {}
    for k, ex in enumerate(spec.get("excerpts") or [], 1):
        to = (ex.get("link") or {}).get("to")
        if to:
            links.setdefault(to, []).append(f"{td.circled(td.excerpt_number(ex['id'], k))} {ex['link'].get('relation', '')}: "
                                            f"{ex['link'].get('how', '')}")
    cards = [(f"→ {US}: {to} · {targets.get(to, to)}", lines, INK) for to, lines in links.items()]
    if cards:
        rows += [cards[k:k + 2] for k in range(0, len(cards), 2)]
        labels += ["how it links to our paper"] + [""] * (len(cards) - 1)
    for q in spec.get("open") or []:
        rows.append([("❓ Open", [f"❓ {q}"], RED)])
        labels.append("")
    return td.fit(d, f, td.rows_of(d, y, rows, labels))


def ref(p: dict) -> dict:
    """The paper's reference: the face's `ref:` block, else what its related.md row says."""
    row, r = p.get("row") or {}, dict(p.get("ref") or {})
    r.setdefault("title", (row.get("item") or p["item"]).split(" · ", 1)[-1])
    r.setdefault("venue", row.get("venue", ""))
    r.setdefault("year", row.get("date", ""))
    r.setdefault("link", row.get("source", ""))
    r.setdefault("authors", "")
    return r


def reference_frame(d: Drawing, p: dict) -> dict:
    """A paper's reference, first in its row: title, every author, venue and year, link, PDF, deep read, and the
    version read. A paper with no reading yet adds one red card: what to do to read it."""
    r, row, spec = ref(p), p.get("row") or {}, (p["reading"] or (None, {}))[1]
    name = f"{p['id']} · {who(p['item'])} · the paper"
    f = d.frame(name, td.NARROW, 700)
    y = td.heading(d, name, f"{r['venue']} · {r['year']}", f"“{r['title']}”", td.NARROW)
    body = [f"Authors: {r['authors'] or '❓ not found'}", f"Published: {r['venue']}, {r['year']}", f"Link: {r['link']}",
            f"PDF: related/{pdf_of(p)}" if pdf_of(p) else "PDF: none kept",
            f"Deep read (Discovery): {row.get('read') or 'none yet'}"]
    if (spec.get("paper") or {}).get("cite"):
        body.append(f"Read from: {spec['paper']['cite']}")
    hh = td.card_height("📚 Reference", body, td.NARROW - 80)
    td.card(d, 40, y, td.NARROW - 80, hh, "📚 Reference", body, INK)
    y += hh
    if not p["reading"]:
        head = "⬜ Its PDF is kept, not read yet" if pdf_of(p) else "❓ No PDF yet"
        todo = (f"Read related/{pdf_of(p)} with excalidraw-read into reads/{p['id']}-<paper>/reading.yaml, then rebuild."
                if pdf_of(p) else "Save its PDF in related/paper/ and give it a reading here, then rebuild: its pages "
                "and logic will show.")
        red = [f"Why here (its abstract): {row.get('why here', '❓')}", todo]
        y += 40
        rh = td.card_height(head, red, td.NARROW - 80)
        td.card(d, 40, y, td.NARROW - 80, rh, head, red, RED, dashed=True)
        y += rh
    return td.fit(d, f, y)


def draw(topic: Path) -> Path:
    """Redraw one topic of related papers from its face and its readings; returns the drawing."""
    topic = topic.resolve()
    block = topic.parents[1]
    cfg = face_cfg(topic)
    if not cfg.get("papers"):
        raise SystemExit(f"{topic.name}: its face has no related: yaml with papers")
    rows = related_rows(block)
    assets = topic / "assets"
    papers = []
    for p in cfg["papers"]:
        p = {**p, "id": str(p["id"])}
        p["row"] = next((r for r in rows if r.get("item", "").startswith(str(p["item"]))), {})
        p["reading"] = td.read_of({"rid": p["id"]}, assets)
        papers.append(p)
    face = (topic / f"{topic.name}.md").read_text(encoding="utf-8")
    title = re.sub(r"^s\d+\s*·\s*", "", face.splitlines()[0]).strip() if face else topic.name
    d = Drawing()
    theme = theme_frame(d, title, cfg, papers)
    acts = [{"name": "Act 1 · The theme", "frames": [theme["id"]]}]
    for k, p in enumerate(papers, 1):
        run, w = {"rid": p["id"], "summary": p.get("says") or ""}, {"says": p.get("says") or ""}
        frames = [reference_frame(d, p)["id"]]
        if p["reading"]:
            pages = td.transcript_frame(d, run, w, assets, noun="paper", us=US,
                                        name=f"{p['id']} · {who(p['item'])} · the paper, read")
            frames += ([pages["id"]] if pages else []) + [logic_frame(d, p, p["reading"][1])["id"]]
        acts.append({"name": f"Act {k + 1} · {p['id']} · {who(p['item'])}", "frames": frames,
                     "arrow": ["its pages, read", "its logic"][:len(frames) - 1]})
    between = [(theme["id"], acts[1]["frames"][0], "one row per paper, in reading order")] if len(acts) > 1 else []
    between += [(acts[i]["frames"][0], acts[i + 1]["frames"][0], f"next: {papers[i]['id']}") for i in range(1, len(acts) - 1)]
    d.acts(acts, between=between, gap=td.GAP)
    out = topic / f"{topic.name}.excalidraw"
    d.write(out, f"excalidraw-read ref/topic_drawing.py {topic.name}")
    from render_png import render
    render(out, out.with_suffix(".png"))
    return out


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    sub = ap.add_subparsers(dest="cmd", required=True)
    sub.add_parser("draw").add_argument("topic", type=Path)
    a = ap.parse_args(argv)
    print(draw(a.topic))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
