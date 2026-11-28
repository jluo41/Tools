"""page.py structure (M-D14), the version Job's main-text budget (M-D11) and the Story row a Section restates (M-D09)."""
from pathlib import Path

from src.folder_health import OK, WARN, folder_health
from src.page_structure import structure, words


def sentences(start: int, n: int, text: str = "One two three four.") -> str:
    return "".join(f"- B{k + 1} · s{start + k} · {text}\n" for k in range(n))


def draft(stem: str, version: str, paras: list, approved: str = "✅ JL 261113 · in chat: \"ok\"") -> str:
    """paras: [(pid, heading, first sentence, count)]."""
    overview = "".join(f"- C{c} · Claim number {c}\n" for c in sorted({int(p[0][1:].split('.')[0]) for p in paras}))
    body = "".join(f"### {pid} · {head} · s{a} to s{a + n - 1}\n{sentences(a, n)}\n" for pid, head, a, n in paras)
    return (f"# {stem} · draft v{version}\ndraft-version: v{version}\napproved: {approved}\n\n"
            f"## 1 · Structure · Bullet Point Table\n\n### Structure Overview\n\n{overview}\n"
            f"## 2 · Scratch\n\n## 3 · Draft · Reading and Revise\n\n{body}")


def section(job: Path, name: str, kind: str, paras: list, version: str = "1.0", previous: list | None = None) -> Path:
    folder = job / name
    (folder / "draft" / "previous").mkdir(parents=True)
    (folder / f"{name}.md").write_text(f"# {name}\ntask-type: draft\nsection_kind: {kind}\n", encoding="utf-8")
    (folder / "draft" / f"{name}-draft-v{version}.md").write_text(draft(name, version, paras), encoding="utf-8")
    if previous:
        (folder / "draft" / "previous" / f"{name}-draft-v0.9.md").write_text(draft(name, "0.9", previous), encoding="utf-8")
    return folder


LONG = "With a linear head on the frozen model, short forecasts gain most"


def test_a_section_prints_claims_paragraphs_ranges_and_marks(tmp_path):
    folder = section(tmp_path, "t02_results", "results",
                     [("C1.P1", "Study design and data", 1, 5), ("C1.P2", LONG, 6, 3)])
    got = structure(folder).splitlines()
    assert got == [
        "t02_results · Draft v1.0 · plan ✅ JL 261113 · 32 words",
        "C1  Claim number 1",
        "  P1   Study design and data                     s1-s5  5 sent  20 w",
        "  P2   With a linear head on the frozen model,   s6-s8  3 sent  12 w  ⚠",
        "       short forecasts gain most",
    ]
    assert words("a \\ref{fig:x} b $x$ <!-- n -->") == 4


def test_a_review_run_adds_the_logic_score(tmp_path):
    (tmp_path / "board.md").write_text("# Paper\n", encoding="utf-8")
    job = tmp_path / "j11_writing_v1"
    folder = section(job, "t02_results", "results", [("C1.P1", "Data", 1, 5)])
    res = tmp_path / "j31_review_v1" / "t03_paragraph_logic" / "runs" / "r01_review" / "result"
    res.mkdir(parents=True)
    (res / "logic-t02_results.md").write_text("# x\n\n### C1.P1 · Data · 7/10\nClaim: x\n", encoding="utf-8")
    assert structure(folder).splitlines()[2].endswith("5 sent  20 w   7/10")


def board_with_job(tmp_path: Path, cap: str = "3,500") -> Path:
    (tmp_path / "board.md").write_text("# Paper\nvenue: Nature Machine Intelligence\n", encoding="utf-8")
    call = tmp_path / "venues" / "nature-machine-intelligence"
    call.mkdir(parents=True)
    (call / "call.md").write_text("| what | limit | counts |\n|---|---|---|\n"
                                  f"| words | up to {cap} | the main text (Introduction, Results, Discussion); not the "
                                  "abstract, Methods |\n", encoding="utf-8")
    job = tmp_path / "j11_writing_v1"
    job.mkdir()
    (job / "j11_writing_v1.md").write_text("# j11\n\n## Narrative\n\n<!-- haipipe:compile-order:start -->\nmain:\n"
                                           "- t01_introduction\n- t02_results\n- t04_methods\n"
                                           "<!-- haipipe:compile-order:end -->\n", encoding="utf-8")
    section(job, "t04_methods", "methods", [("C1.P1", "Data", 1, 5)])
    section(job, "t02_results", "results", [("C1.P1", "Data", 1, 6)], previous=[("C1.P1", "Data", 1, 5)])
    section(job, "t01_introduction", "introduction", [("C1.P1", "Why", 1, 4)])
    return job


def test_a_version_job_prints_each_section_in_order_and_the_budget(tmp_path):
    job = board_with_job(tmp_path)
    out = structure(job).splitlines()
    heads = [line.split(" · ")[0] for line in out if " · Draft v" in line]
    assert heads == ["t01_introduction", "t02_results", "t04_methods"]
    assert out[-1] == ("Main text: 40 of 3,500 words (t01_introduction 16 + t02_results 24) · "
                       "venues/nature-machine-intelligence/call.md")
    report = folder_health(job)
    assert report["verdict"] == OK and report["findings"][0]["check"] == "budget"


def test_the_budget_warns_when_over_and_names_who_grew(tmp_path):
    job = board_with_job(tmp_path, cap="30")
    assert structure(job).splitlines()[-1].startswith("Main text: 40 of 30 words, 10 over ⚠")
    found = folder_health(job)["findings"]
    assert [f["level"] for f in found] == [WARN]
    assert "over the 30 cap" in found[0]["message"] and "grew since the previous Draft: t02_results +4" in found[0]["message"]


STORY = ("# s02\n\n## Content\n\n### 8 · Section Narrative\n\n```text\nTITLE            Scaling is not universal\n```\n\n"
         "#### 8.1 · Claims\n\n| id | claim |\n|---|---|\n| C1 | The short forecast gains. |\n"
         "| C6 | Scale does not close the gap. |\n\n### 9 · Venue\n\nx\n")


def test_a_changed_story_row_is_named_only_to_the_sections_that_restate_it(tmp_path):
    from src.page_sign import sign, sign_narrative
    (tmp_path / "board.md").write_text("# Paper\nstory-current: s02-story\n", encoding="utf-8")
    (tmp_path / "s02-story").mkdir()
    story = tmp_path / "s02-story" / "s02-story.md"
    story.write_text(STORY, encoding="utf-8")
    job = tmp_path / "j11_writing_v1"
    job.mkdir()
    (job / "j11_writing_v1.md").write_text(
        "# j11\n\n## Narrative\n\n| Section | question | claims |\n|---|---|---|\n"
        "| t02_results | What did scale buy? | C1, C6 |\n| t00_abstract | Where? | C1 |\n", encoding="utf-8")
    results = section(job, "t02_results", "results", [("C1.P1", "Data", 1, 5)])
    abstract = section(job, "t00_abstract", "abstract", [("C1.P1", "Abstract", 1, 5)])
    assert sign_narrative(job, "sign")["ok"] and sign(results, "go")["ok"] and sign(abstract, "go")["ok"]
    assert "## Story rows it was signed against" in (results / "draft" / "records" / "t02_results-sign.md").read_text()
    assert [f for f in folder_health(results)["findings"] if f["check"] == "narrative"] == []
    story.write_text(STORY.replace("does not close the gap.", "does not close the gap in general."), encoding="utf-8")
    sign_narrative(job, "re-sign")
    # M-D09 (JL 261115): while the version drafts, neither Section is told
    assert [f for f in folder_health(results)["findings"] if f["check"] == "narrative"] == []
    assert [f for f in folder_health(abstract)["findings"] if f["check"] == "narrative"] == []
    face = job / "j11_writing_v1.md"
    face.write_text(face.read_text().replace("# j11\n", "# j11\nstate: sent\n"), encoding="utf-8")
    told = [f for f in folder_health(results)["findings"] if f["check"] == "narrative"]
    assert [f["level"] for f in told] == [WARN]     # after the send, the Section that restates C6 learns of it
    assert told[0]["message"].startswith("Story row C6 in s02-story.md § 8 changed since this Section's plan was signed; "
                                         "t02_results restates it")
    quiet = [f for f in folder_health(abstract)["findings"] if f["check"] == "narrative"]
    assert [f["level"] for f in quiet] == ["INFO"] and "does not name them" in quiet[0]["message"]
    assert levels_row(folder_health(results)) == []    # the row check still reads only its own row


def levels_row(report):
    return [f["level"] for f in report["findings"] if f["check"] == "row"]
