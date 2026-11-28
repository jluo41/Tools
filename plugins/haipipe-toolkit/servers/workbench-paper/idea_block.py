"""An Idea Block in paper/ (`paper/Idea-<Slug>/`, `board-kind: ideation-block`; hai-ideation references/idea-block.md):
one row per Idea Job, its question, its mark and the Paper it went to, in place of a Paper Board's views
(Paper-Idea 261124: an Idea Block drew as a Paper Board with Support blocks and Writing).

A Job's face gives `state:` (selection_contract.STATES: selected, deferred, eliminated, open) and `went to:`
(a path to a Paper Board, then its venue and version in brackets); its question is the face's `## Question`,
else its ideation.yaml `question:`.
"""
from __future__ import annotations

import re
from pathlib import Path

MARKS = {"selected": "✅", "open": "⬜", "deferred": "⏸", "eliminated": "❌"}
CSS = ("<style>.idea-jobs td{vertical-align:top}.idea-jobs tr.idea-out td{opacity:.55}"
       ".idea-jobs tr.idea-out td.idea-q{text-decoration:line-through}</style>")


def is_idea_block(folder) -> bool:
    folder = Path(folder)
    if folder.name.startswith("Idea-"):
        return True
    face = folder / "board.md"
    head = face.read_text(encoding="utf-8", errors="ignore")[:2000] if face.is_file() else ""
    return bool(re.search(r"(?m)^board-kind:\s*ideation-block\s*$", head))


def idea_block_of(folder) -> Path | None:
    """The Idea Block a folder sits in (itself, or the Block above a Job or Task), or None."""
    for p in (Path(folder), *Path(folder).parents):
        if (p / "board.md").is_file():
            return p if is_idea_block(p) else None
    return None


def _field(text: str, key: str) -> str:
    m = re.search(rf"(?mi)^{re.escape(key)}:\s*(.+?)\s*$", text)
    return m[1] if m else ""


def _question(job: Path, text: str) -> str:
    m = re.search(r"(?ms)^## Question\s*\n+(.+?)(?:\n\s*\n|\n## |\Z)", text)
    if m:
        return " ".join(m[1].split())
    y = job / "ideation.yaml"
    return _field(y.read_text(encoding="utf-8", errors="ignore"), "question") if y.is_file() else ""


def idea_jobs(block) -> list[dict]:
    """[{job, question, state, went, where}] for each jNN Job with a face, in number order."""
    out = []
    for job in sorted(p for p in Path(block).glob("j[0-9]*_*") if p.is_dir()):
        face = job / f"{job.name}.md"
        text = face.read_text(encoding="utf-8", errors="ignore") if face.is_file() else ""
        went = _field(text, "went to")
        m = re.match(r"(\S+)\s*(.*)$", went)
        target = (job / m[1]).resolve() if m else None
        out.append({"job": job, "question": _question(job, text), "state": _field(text, "state").casefold(),
                    "went": target if target and target.is_dir() else None,
                    "where": re.sub(r"^\(+|\)+$", "", m[2]).strip() if m else ""})
    return out


def ideas_html(block, root) -> str:
    from live.focus_base import page_url
    from live.frame import esc
    rows = []
    for r in idea_jobs(block):
        went = ""
        if r["went"] is not None:
            went = (f'<a href="{esc(page_url(r["went"], root))}">{esc(r["went"].name)}</a>'
                    + (f' <small class=mut>{esc(r["where"])}</small>' if r["where"] else ""))
        cls = ' class=idea-out' if r["state"] == "eliminated" else ""
        rows.append(f'<tr{cls}><td>{MARKS.get(r["state"], "")}</td>'
                    f'<td><a href="{esc(page_url(r["job"], root))}">{esc(r["job"].name)}</a></td>'
                    f'<td class=idea-q>{esc(r["question"])}</td><td>{went}</td></tr>')
    if not rows:
        return ""
    return (CSS + '<table class="wf-table idea-jobs"><thead><tr><th></th><th>Idea Job</th><th>Question</th>'
            '<th>Went to</th></tr></thead><tbody>' + "".join(rows) + "</tbody></table>")


def report_views(block, root) -> dict:
    """{key: (name, build)}: the Idea Block's one view."""
    return {"ideas": ("Ideas", lambda: '<h2>📋 Review Content</h2>' + ideas_html(block, root))}


def job_views(job, root) -> dict:
    """{key: (name, build)}: an Idea Job's face as its one view (its question, claim and where it came from), its
    header lines left to the identity line and the Block's row."""
    from live.focus_base import markdown
    job = Path(job)
    face = job / f"{job.name}.md"
    if not face.is_file():
        return {}
    text = face.read_text(encoding="utf-8", errors="ignore")
    body = text[text.find("\n## "):] if "\n## " in text else ""
    return {"idea": ("Idea", lambda: '<h2>📋 Review Content</h2>' + markdown(body, job, Path(root)))}


RECEIPT = re.compile(r"\]\(([^)\s]+\.ya?ml)\)")


def receipt_rows(task) -> list[tuple[Path, list[dict]]]:
    """[(receipt, [{claim_id, verdict, confidence}])] for each novelty receipt the Task's face links
    (`kind: idea-novelty-check`, hai-ideation novelty-check)."""
    import yaml
    task = Path(task)
    face = task / f"{task.name}.md"
    text = face.read_text(encoding="utf-8", errors="ignore") if face.is_file() else ""
    out = []
    for href in dict.fromkeys(RECEIPT.findall(text)):
        p = (task / href).resolve()
        try:
            doc = yaml.safe_load(p.read_text(encoding="utf-8")) if p.is_file() else None
        except Exception:
            doc = None
        if isinstance(doc, dict) and doc.get("kind") == "idea-novelty-check":
            out.append((p, [c for c in doc.get("claims") or [] if isinstance(c, dict)]))
    return out


def task_views(task, root) -> dict:
    """{key: (name, build)}: an assessment Task under an Idea Job (task-type: ideation; Paper-Idea 261124: its verdicts
    were hidden behind the work-Task frame): its face body, then one row per claim of each novelty receipt it links."""
    from live.focus_base import markdown, page_url
    from live.frame import _file_url, esc
    task, root = Path(task), Path(root)
    face = task / f"{task.name}.md"
    if not face.is_file():
        return {}

    def build():
        text = face.read_text(encoding="utf-8", errors="ignore")
        body = text[text.find("\n## "):] if "\n## " in text else ""
        html = '<h2>📋 Review Content</h2>' + markdown(body, task, root)
        for receipt, claims in receipt_rows(task):
            rows = "".join(f'<tr><td>{esc(str(c.get("claim_id", "")))}</td><td>{esc(str(c.get("verdict", "")))}</td>'
                           f'<td>{esc(str(c.get("confidence", "")))}</td></tr>' for c in claims)
            try:
                href = _file_url(receipt, root)
            except Exception:
                href = page_url(receipt.parent, root)
            html += (f'<h3>Novelty: <a href="{esc(href)}">{esc(receipt.name)}</a></h3>'
                     '<table class="wf-table"><thead><tr><th>Claim</th><th>Verdict</th><th>Confidence</th></tr></thead>'
                     f'<tbody>{rows}</tbody></table>')
        return html
    return {"assessment": ("Assessment", build)}
