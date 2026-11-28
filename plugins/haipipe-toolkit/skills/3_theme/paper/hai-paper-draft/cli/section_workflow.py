#!/usr/bin/env python3
"""Where a paper Section stands in its workflow, read from disk, and the step to run next (ref/workflow.md).

    python3 section_workflow.py <Section Task folder>

Six steps (JL 261116: "when I open a new secton draft, then I can run the tasks one by one and get a close to review
draft"): W0 Examples, W1 Plan (the person signs), W2 Write, W3 Rate, W4 Fix loop (the AI accepts what the blind
reader keeps, comments on the rest, stops after two rounds that keep nothing), W5 Ready (the person joins). Each step
is judged from a file, never from memory, so the line printed here is the one a page may show. Read only.
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

ROW = re.compile(r"(?m)^- B\d+[a-z]* · [Ss]\d+[a-z]* · ")
PASS = re.compile(r"(?m)^## Pass (\d+)[^\n]*?on draft v([\d.]+)")
SCORES = re.compile(r"(?m)^- (?:C\d+\.P\d+\.)?[Ss]\d+[a-z]* · (?:\([^)]*\) · )?logic (\d+(?:\.\d+)?)/10 · read "
                    r"(\d+(?:\.\d+)?)/10(?: · ai (\d+(?:\.\d+)?)/10)?")
REPORT = re.compile(r"(?mi)^### (?:Revise|Current draft) review report")   # the card the page reads ★ from
STEPS = (("W0", "examples"), ("W1", "plan"), ("W2", "write"), ("W3", "rate"), ("W4", "fix loop"), ("W5", "ready"))


def vkey(p: Path) -> list:
    return [int(x) for x in re.findall(r"\d+", p.stem.rsplit("-v", 1)[-1])]


def newest_draft(task: Path) -> Path | None:
    drafts = sorted(task.glob("draft/*-draft-v*.md"), key=vkey)
    return drafts[-1] if drafts else None


def face(task: Path) -> str:
    f = task / f"{task.name}.md"
    return f.read_text(encoding="utf-8", errors="replace") if f.is_file() else ""


def line(text: str, key: str) -> str:
    m = re.search(rf"(?m)^{key}:\s*(.*?)\s*$", text)
    return m.group(1) if m else ""


def examples(task: Path) -> tuple:
    said = line(face(task), "examples")
    if said.startswith("none"):
        return True, f"none, {said}"
    if not said:
        return False, "no examples: line on the face"
    for up in (task, *list(task.parents)[:3]):
        topic = up / said
        if topic.is_dir():
            shots = list(topic.glob("reads/*/shots/*.jpg"))
            return bool(shots), f"{said}, {len(shots)} section screenshots" if shots else f"{said} has no screenshots"
    return False, f"{said} not found"


def split(draft: Path) -> tuple:
    text = draft.read_text(encoding="utf-8", errors="replace")
    i = text.find("## 3 ·")
    return text[:i] if i >= 0 else text, text[i:] if i >= 0 else ""


def newest_pass(task: Path) -> tuple:
    """(pass number, draft version it rated, its text) of the revise record's highest-numbered Pass with sentence lines."""
    rec = next(iter(task.glob("draft/records/*-revise.md")), None)
    if not rec:
        return None
    text = rec.read_text(encoding="utf-8", errors="replace")
    heads = list(PASS.finditer(text))
    # by Pass number, as the page's _revise_passes reads them: a record may list the newest first (t00_abstract 261118)
    for k in sorted(range(len(heads)), key=lambda i: int(heads[i].group(1)), reverse=True):
        body = text[heads[k].end():heads[k + 1].start() if k + 1 < len(heads) else len(text)]
        if SCORES.search(body):          # without the report heading the page shows no ★ (t02_results 261118)
            return int(heads[k].group(1)), heads[k].group(2), body, bool(REPORT.search(body))
    return None


def open_ai_comments(task: Path) -> int:
    rec = next(iter(task.glob("draft/records/*-comments.md")), None)
    if not rec:
        return 0
    blocks = re.split(r"(?m)^### Comment ", rec.read_text(encoding="utf-8", errors="replace"))[1:]
    return sum(1 for b in blocks if re.search(r"(?m)^State:\s*open", b) and re.search(r"\bAI:", b))


def ai_comments_without_card(task: Path, pass_text: str) -> list:
    """Open AI comment numbers that no `### Edit` card of the newest Pass answers (`Answers: Comment N`): an AI comment
    always comes with its proposed edit (CONSTITUTION A03, JL 261118: "please also leave the proposed solution")."""
    rec = next(iter(task.glob("draft/records/*-comments.md")), None)
    if not rec:
        return []
    answered = set(re.findall(r"Comment (\d+)", " ".join(re.findall(r"(?m)^Answers:[^\n]*", pass_text))))
    out = []
    for b in re.split(r"(?m)^### Comment ", rec.read_text(encoding="utf-8", errors="replace"))[1:]:
        n = b.split(" ", 1)[0]
        if re.search(r"(?m)^State:\s*open", b) and re.search(r"\bAI:", b) and n not in answered:
            out.append(n)
    return out


PARA = re.compile(r"(?m)^- (C\d+\.P\d+) · (?:paragraph )?(\d+(?:\.\d+)?)/10\b.*$")


def paragraph_counts(pass_text: str) -> tuple:
    """(rated paragraph ids, open under 8, settled under 8) from a Pass's `Paragraphs:` lines (CONSTITUTION A02)."""
    rated, open_, settled = set(), 0, 0
    for m in PARA.finditer(pass_text):
        rated.add(m.group(1))
        if float(m.group(2)) < 8:
            if re.search(r"AI decided:|asked in Comment \d+", m.group(0)):
                settled += 1
            else:
                open_ += 1
    return rated, open_, settled


TITLE = re.compile(r"(?m)^- (C\d+(?:\.P\d+)?) · title (\d+(?:\.\d+)?)/10\b.*$")


def titles_in(draft_text: str) -> set:
    """Every part title C<n> and paragraph title C<n>.P<m> the Draft holds (CONSTITUTION A02)."""
    parts = set(re.findall(r"(?m)^- (C\d+) · ", draft_text[draft_text.find("### Structure Overview"):][:4000]))
    return parts | set(re.findall(r"(?m)^### (C\d+\.P\d+) · ", draft_text))


def title_counts(pass_text: str) -> tuple:
    """(rated title ids, open under 8, settled under 8) from a Pass's `Titles:` lines."""
    rated, open_, settled = set(), 0, 0
    for m in TITLE.finditer(pass_text):
        rated.add(m.group(1))
        if float(m.group(2)) < 8:
            if re.search(r"AI decided:|asked in Comment \d+", m.group(0)):
                settled += 1
            else:
                open_ += 1
    return rated, open_, settled


def w4_counts(pass_text: str) -> tuple:
    """(open under 8, under 8 settled by `AI decided:` or `asked in Comment N`, cards `State: proposed`) in one Pass (CONSTITUTION A01)."""
    lines = re.findall(r"(?m)^- (?:C\d+\.P\d+\.)?[Ss]\d+[a-z]* · .*$", pass_text)
    low = [(min(float(a), float(b), float(c or 10)), bool(re.search(r"AI decided:|asked in Comment \d+", ln))) for ln in lines for a, b, c in SCORES.findall(ln)]
    return (sum(v < 8 and not d for v, d in low), sum(v < 8 and d for v, d in low),
            sum(1 for b in re.split(r"(?m)^### ", pass_text)                 # a proposed card that answers no comment
                if re.search(r"(?m)^State:\s*proposed\b", b) and not re.search(r"(?m)^Answers:\s*Comment", b)))


def grammar_findings(draft: Path) -> list:
    """[(sentence, kind, text)] from hai-draft-review cli/grammar.py (CONSTITUTION A04)."""
    sys.path.insert(0, str(Path(__file__).resolve().parents[4] / "1_base/draft/hai-draft-review/cli"))
    from grammar import check
    return check(draft)


def status(task: Path) -> list:
    """[(step, name, done, what was read)] in order."""
    out = []
    ok, said = examples(task)
    out.append(ok and said)
    draft = newest_draft(task)
    plan, prose = split(draft) if draft else ("", "")
    head = draft.read_text(encoding="utf-8", errors="replace")[:4000] if draft else ""
    signed = "✅" in line(head, "approved")
    out.append(signed and f"{draft.name} approved")
    n_plan, n_text = len(ROW.findall(plan)), len(ROW.findall(prose))
    out.append(n_text and n_text >= n_plan and f"{n_text} sentences in the Draft text for {n_plan} Bullets")
    p = newest_pass(task)                   # a Pass on an older version is stale: the text changed after it
    version = draft.stem.rsplit("-v", 1)[-1] if draft else ""
    rated = p and p[1] == version and p[3]
    # titles are rated like sentences (CONSTITUTION A02, JL 261118): every C<n> and C<n>.P<m> needs a Titles: line
    t_rated, t_open, t_settled = title_counts(p[2] if p else "")
    t_missing = sorted(titles_in(draft.read_text(encoding="utf-8", errors="replace")) - t_rated) if draft else []
    p_rated, p_open, p_settled = paragraph_counts(p[2] if p else "")
    # a P0 title paragraph is one title sentence: its Titles: line rates it, no Paragraphs: line (t00_abstract 261118)
    p_missing = sorted(set(re.findall(r"(?m)^### (C\d+\.P[1-9]\d*) · ", split(draft)[1])) - p_rated) if draft else []
    t_missing += p_missing
    out.append((rated and not t_missing, p and (f"Pass {p[0]} rated v{p[1]}" + ("" if p[3] else ", but has no ### Revise review report "
               "heading, so the page shows no ★") + ("" if "Standard:" in p[2] else " (no Standard: line)")
               + (f", {len(t_missing)} titles or paragraphs unrated ({', '.join(t_missing[:4])}{' …' if len(t_missing) > 4 else ''})"
                  if t_missing else f", {len(t_rated)} titles, {len(p_rated)} paragraphs"))))
    # the AI proposes, accepts and reviews (CONSTITUTION A01, JL 261118): a sentence under 8 is settled by the AI
    # ("AI decided: …" on its Pass line, when it is sure) or by an open AI comment (when it is not); no card waits
    under, decided, waiting = w4_counts(p[2] if p else "")
    under, decided = under + t_open + p_open, decided + t_settled + p_settled
    no_card = ai_comments_without_card(task, p[2] if p else "")
    asks = open_ai_comments(task)
    # grammar a machine can see (CONSTITUTION A04, JL 261118): the fix loop stays open while any is left
    gram = grammar_findings(draft) if draft else []
    out.append((rated and waiting == 0 and not no_card and not gram and (under == 0 or under <= asks),
                (f"{under} under 8 open, {decided} settled (AI decided or asked), {asks} open AI comments"
                 + (f", {waiting} cards wait for a person with no comment" if waiting else "")
                 + (f", AI comments {', '.join(no_card)} have no proposed card" if no_card else "")
                 + (f", {len(gram)} grammar findings ({', '.join(f'{a} {k}' for a, k, _ in gram[:4])}"
                    f"{' …' if len(gram) > 4 else ''}; grammar.py)" if gram else "")) if rated else ""))
    home = task.parents[1] / "delivery" / task.parent.name / task.name     # the exporter writes into latex/ (or word/)
    built = sorted(home.glob("**/*.pdf"), key=lambda f: f.stat().st_mtime) if home.is_dir() else []
    fresh = bool(built) and draft and built[-1].stat().st_mtime >= draft.stat().st_mtime
    seen = (f"{built[-1].relative_to(home)} {'built after' if fresh else 'older than'} {draft.name}" if built and draft
            else f"no PDF under delivery/{task.parent.name}/{task.name}/")
    out.append((bool(out[4][0]) and bool(fresh), seen))
    out = [d if isinstance(d, tuple) else (d, d) for d in out]
    return [(s, n, bool(d), str(w or "")) for (s, n), (d, w) in zip(STEPS, out)]


NEXT = {
    "W0": "read 3 to 4 published papers of the same article type and venue: SKILL.md § Examples first",
    "W1": "propose the Structure against the examples and the Narrative row, then the person signs (page.py sign)",
    "W2": "write the Draft text from the signed plan, then page.py adopt and page.py export",
    "W3": "rate with fresh agents: hai-draft-eval-paragraph-agent and hai-draft-eval-sentence-agent",
    "W4": "fix every grammar.py finding; rewrite each item under 8, blind A/B, adopt what is kept; then the AI settles each one left: sure, write AI decided: on its Pass line; not sure, an AI comment",
    "W5": "page.py export, then page.py health --final; the person reads the 🤖 comments and checks each sentence",
}


def main(argv: list) -> int:
    if len(argv) != 1:
        print(__doc__)
        return 2
    task = Path(argv[0]).resolve()
    rows = status(task)
    print(task.name)
    for s, n, done, what in rows:
        print(f"  {'✅' if done else '⬜'} {s} {n:<9} {what}")
    nxt = next(((s, n) for s, n, done, _ in rows if not done), None)
    # the person's comments come first, every turn (hai-draft CONSTITUTION A01, JL 261118)
    rec = next(iter(task.glob("draft/records/*-comments.md")), None)
    if rec:
        sys.path.insert(0, str(Path(__file__).resolve().parents[4] / "1_base/draft/hai-draft/src"))
        from comment_health import unanswered
        left = unanswered(rec)
        if left:
            print("next: 🙋 reply first, then fix: " + "; ".join(f"Comment {n} · {a} \"{w}\"" for n, a, w in left))
            return 0
    print(f"next: {nxt[0]} {nxt[1]}: {NEXT[nxt[0]]}" if nxt else "next: 🙋 the person: read the open comments, ✓ each sentence")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
