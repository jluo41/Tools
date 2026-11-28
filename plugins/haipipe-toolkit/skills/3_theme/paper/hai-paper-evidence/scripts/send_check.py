"""send_check.py · the one check before a send or a co-author round: citations and values, sorted into what the
paper PRINTS WRONG and what is only NOT RECORDED yet (AgreeableJama-Board 261123, JL: one door for citations and
values; paper_check.py said "65 to fix" and chain_check.py "947 failures", with no way to tell a wrong number from
missing bookkeeping).

    python send_check.py <paper Board> [--writing jNN_writing_v<MMDD>_<desk>] [--out send-check.md]

It reads only (a temporary folder for the value ledger) and runs, in this order:

    citations · details   cite_tasks.py's ledger: a key with no bib entry or TOADD prints "?" or a gap; one key in
                          back-to-back sentences; a key with no signed CITE Result is a record not kept yet
    citations · web       master.bbl: an entry with no DOI that prints no URL; an access date written as data
                          ("Accessed: 2026-08-21") rather than in words
    citations · order     word_compare.py --citations on the version's Word file (numbers in order of first citation)
    citations · support   cite_support.py: each citing sentence read against its source (sheet and sources there)
    values · printed      values_ledger.py check: a printed number that differs from its value is wrong; a number
                          with no binding, or a binding proposed and not ticked, is a record not kept yet
    values · chain        chain_check.py: work, value, display and Section Runs agree with each other (records)

Three groups in the output: ❗ the paper prints something wrong, ⬜ a record is missing, 🙋 waits on a person.
The exit code is the number of ❗ lines, so a send waits until it is 0. paper_check.py stays the progress list.
"""
from __future__ import annotations

import argparse
import contextlib
import importlib.util
import io
import re
import sys
import tempfile
from collections import Counter
from pathlib import Path

import yaml

HERE = Path(__file__).resolve()
sys.path.insert(0, str(HERE.parent))
import cite_support as cs  # noqa: E402
import cite_tasks as ct  # noqa: E402

ASSEMBLE = HERE.parents[2] / "hai-paper-assemble" / "scripts"
ISO_ACCESS = re.compile(r"Accessed:?\s*\d{4}-\d{2}-\d{2}")


def _module(path: Path, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def bbl_items(text: str) -> dict:
    """{key: the entry as printed} from a master.bbl."""
    out = {}
    for part in re.split(r"\\bibitem(?:\[[^\]]*\])?", text)[1:]:
        m = re.match(r"\s*\{([^}]*)\}", part)
        if m:
            out[m[1]] = part[m.end():].split("\\end{thebibliography}")[0].strip()
    return out


def web_lines(bbl: Path, dois: dict | None = None) -> list[str]:
    """The printed entries that print neither a DOI nor a URL (saying when the bib holds a DOI the style dropped),
    and the access dates written as data."""
    if not bbl.is_file():
        return []
    out, dois = [], dois or {}
    for k, e in bbl_items(bbl.read_text(encoding="utf-8", errors="ignore")).items():
        if not re.search(r"doi|\\url|\\href|https?://", e, re.I):
            out.append(f"{k}: the bib holds doi {dois[k]}, the reference prints none (the bibstyle drops it)"
                       if dois.get(k) else f"{k}: no DOI and no URL printed")
        if ISO_ACCESS.search(e):
            out.append(f"{k}: the access date prints as {ISO_ACCESS.search(e)[0]!r}; write it in words "
                       f"(AMA: \"Accessed August 21, 2026.\")")
    return out


def citations(paper, wrong, missing, person):
    L = ct.ledger(paper)
    for r in L["rows"]:
        if r["status"] in ("TOADD", "missing-bib"):
            wrong.append(("citations · details", f"{r['key']}: {ct.WORDS[r['status']]} (cited at {r['cited_in']})"))
    for p in L["pairs"]:
        wrong.append(("citations · details", f"{p['section']} {p['sentences']}: {p['key']} in back-to-back sentences"))
    unsigned = Counter(ct.WORDS[r["status"]] for r in L["rows"] if r["status"] in ("card-only", "bib-only"))
    for words, n in unsigned.items():
        missing.append(("citations · details", f"{n} keys {words}; no signed CITE Result"))
    latex = paper.board / "delivery" / paper.job.name / "latex"
    wrong += [("citations · web", x) for x in web_lines(latex / "master.bbl", cs.dois(paper))]
    word = paper.board / "delivery" / paper.job.name / "word" / f"{paper.board.name}.docx"
    if word.is_file():
        wc = _module(ASSEMBLE / "word_compare.py", "word_compare")
        lines = wc.citation_order(word)
        wrong += [("citations · order", x.lstrip("- ")) for x in lines if x.startswith("- ")]
        person += [("citations · order", x) for x in lines if x.startswith("not found")]
    else:
        missing.append(("citations · order", f"no Word file at {word.relative_to(paper.board)}"))
    rows = cs.load(cs.task_dir(paper.j03) / "support.yaml")
    if not rows:
        missing.append(("citations · support", "no reading sheet: run cite_support.py sources, then sheet"))
        return
    now = {(r["section"], r["sentence"], r["key"]): r["hash"] for r in cs.citing(paper)}
    rows = [r for r in rows if (r.get("section"), str(r.get("sentence")), r.get("key")) in now]
    for r in rows:
        if now[(r["section"], str(r["sentence"]), r["key"])] != r.get("hash"):
            r["reading"], r["was"] = "", {"text": r.get("text")}
    J = cs.judge(rows, cs.task_dir(paper.j03))
    wrong += [("citations · support", f"{cs.where(r)}: {why}") for r, why in J["wrong"]]
    person += [("citations · support", f"{cs.where(r)}: not checkable: {why}") for r, why in J["person"]]
    unread = len(now) - len(rows) + len(J["missing"])
    if unread:
        missing.append(("citations · support", f"{unread} of {len(now)} citing sentence-key pairs not read against "
                                               "their source"))


def values(paper, wrong, missing):
    j02 = next((d for d in sorted(paper.board.glob("j0*_evidence_value")) if d.is_dir()), None)
    if j02 is None:
        missing.append(("values · printed", "no value Job (jNN_evidence_value)"))
        return
    vl = _module(HERE.parent / "values_ledger.py", "values_ledger")
    with tempfile.TemporaryDirectory() as tmp, contextlib.redirect_stdout(io.StringIO()):
        vl.check(j02, Path(tmp))
        doc = yaml.safe_load((Path(tmp) / "values.yaml").read_text(encoding="utf-8")) or {}
    for r in doc.get("rows") or []:
        if r.get("status") == "differs":
            wrong.append(("values · printed", f"{r['where']}: prints {r.get('printed')}, the value {r.get('id')} "
                                              f"is {r.get('value')}"))
    seen = Counter(r.get("status") for r in doc.get("rows") or [] if r.get("status") not in ("match", "differs"))
    for status, n in sorted(seen.items()):
        missing.append(("values · printed", f"{n} printed numbers {vl.WORDS.get(status, status)}"))
    head = doc.get("headline") or ""
    m = re.search(r"(\d+) printed numbers with no binding", head)
    if m:
        missing.append(("values · printed", f"{m[1]} printed numbers with no binding"))
    cc = _module(HERE.parent / "chain_check.py", "chain_check")
    rep = cc.chain(paper.board, None)
    for rule, n in sorted(Counter(str(f["rule"]) for f in rep.fails).items()):
        missing.append(("values · chain", f"rule {rule}: {n} records disagree (chain_check.py names each)"))


def run(board: Path, writing=None) -> tuple[list, list, list, str]:
    board = Path(board).resolve()
    paper = ct.Paper(board / "j03_evidence_cite", writing)
    wrong, missing, person = [], [], []
    citations(paper, wrong, missing, person)
    values(paper, wrong, missing)
    return wrong, missing, person, paper.job.name


def render(board: Path, job: str, wrong, missing, person) -> str:
    lines = [f"# send_check {Path(board).name} · {job}", ""]
    for mark, title, items in (("❗", "The paper prints something wrong", wrong), ("⬜", "A record is missing", missing),
                               ("🙋", "Waits on a person", person)):
        if items:
            lines += [f"## {mark} {title}", ""] + [f"- {where}: {what}" for where, what in items] + [""]
    if not wrong:
        lines += ["✅ nothing printed wrong was found", ""]
    return "\n".join(lines)


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("board", type=Path, help="the paper Board")
    ap.add_argument("--writing", help="the writing Job (default: the claim groups' or the newest)")
    ap.add_argument("--out", type=Path, help="write the report there too")
    a = ap.parse_args(argv)
    wrong, missing, person, job = run(a.board, a.writing)
    text = render(a.board, job, wrong, missing, person)
    print(text)
    if a.out:
        a.out.write_text(text, encoding="utf-8")
    return len(wrong)


if __name__ == "__main__":
    sys.exit(main())
