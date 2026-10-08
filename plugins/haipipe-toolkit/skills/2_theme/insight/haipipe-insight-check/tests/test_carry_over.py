"""carry_over.py on a toy register board: every field carried word for word, ids renamed by one
rule, logic refusals not asked, data refusals asked, the same bytes on a second run."""
import sys
import textwrap
from pathlib import Path

import pytest
import yaml

HERE = Path(__file__).resolve()
sys.path.insert(0, str(HERE.parents[1] / "ref"))
sys.path.insert(0, str(HERE.parents[2] / "haipipe-insight" / "ref"))
import carry_over as co  # noqa: E402
import check_block as ci  # noqa: E402

META = textwrap.dedent("""\
    # What the toy extract holds

    state: 🟡 PARTIAL
    page-type: meta
    owner: someone

    ## Opening

    What data does this board read?

    ## Content

    #### 2 · Partition Register

    **Partitions**: the only place a partition is defined.

    ```text
    name     population block          config      group
    ─────────────────────────────────────────────────────
    full     where: []  unfiltered     full.yaml   1-full/
    alpha    g eq a                    alpha.yaml  2-alpha/
             AND h lte 3.0
    beta     h gte 1.0 AND lte 2.0     beta.yaml   3-beta/
    cross    no rows of its own        (none)      9-cross/
    ```

    **In plain words.** alpha is group a at low h.

    #### 3 · Shared Thresholds

    ```text
    file      src/_thresholds.yaml    LIVE
    ```

    ## Aims

    - not carried
    """)

DATA = textwrap.dedent("""\
    # What the replication asks of the data

    page-type: question
    question-level: data
    owner: someone

    ## Opening

    What must be observed?

    ## Content

    ### 1 · Queue

    **Queue**: this level's questions.

    ```text
    id   question                Gen-1   full         alpha          beta           cross
    ──────────────────────────────────────────────────────────────────────────────────────
    QD1  what does it hold?      Data/1  🟡 D01-full  🚫 full-only   🚫 full-only   ·
    QD2  how many rows reach     (none)  ✅ D02-full  🟡 D02-alpha   🚫 thin        ·
         each step?

    🚫 full-only  a property of the extract.
    ```

    #### 2 · QD1 · Extract Shape

    **The ask**: what is in this extract, at what shape?

    **Why now**: every later rate divides by it.

    **What would answer it**: the row count, read from the file.
    - E1 · compute · the row count · pass: one count · retired: two units in one need
        cut: full
        unit: the extract
        measure: rows
        by: none
        uncertainty: none: exact counts
        rivals: none
        output: shape.csv [n_rows] ; metrics.json [shape.n_rows, shape.n_cols]
    - E2 · compute · the row count · pass: one count
        cut: the whole extract
        unit: the extract
        measure: rows
        by: none
        uncertainty: none: exact counts
        rivals: none
        output: metrics.json [shape.n_rows]
    **Needs agreed**: ✅ 261002

    **Where it stands**: answered.

    #### 3 · QD2 · Funnel Counts

    **The ask**: how many rows reach each step?

    **Why now**: a partition needs its own denominator.

    A second paragraph of why.

    **What would answer it**: the count per step.
    - E1 · compute · rows per step · pass: a count per step
        cut: the cell's partition
        unit: one row
        measure: rows
        by: step
        uncertainty: none: exact counts
        rivals: none
        output: steps.csv [step, n]
    **Needs agreed**: ✅ 261002

    **Where it stands**: answered.

    ## Law

    Nothing here concludes.
    """)


def register(level, letter, below, extra=""):
    return textwrap.dedent(f"""\
        # What the replication asks at {level}

        page-type: question
        question-level: {level}
        owner: someone

        ## Opening

        A {level} register.

        ## Content

        ### 1 · Queue

        ```text
        id   question          Gen-1   full         alpha        beta         cross
        ──────────────────────────────────────────────────────────────────────────────
        Q{letter}1  is it so?         (none)  🟡 {letter}01-full  🚫 defer     🚫 defer     ·
        ```

        #### 2 · Q{letter}1 · Toy {level}

        **The ask**: is it so, and does it hold?

        **Why now**: a toy reason.

        **What would answer it**: a toy answer.
        - E1 · cite · the count · from: Q{below}.E1
        - E2 · judge · whether it is so · from: E1
        **Needs agreed**: ✅ 261002

        **Where it stands**: answered.{extra}
        """)


WISDOM = textwrap.dedent("""\
    # What the replication asks of wisdom

    page-type: question
    question-level: wisdom
    owner: someone

    ## Content

    ### 1 · Queue

    ```text
    id   question           Gen-1     partition  QW1                QW2
    ──────────────────────────────────────────────────────────────────────────
    QW1  which should we    Wisdom/1  full       🟡 W01-full        🟡 W02-full
         send?                        alpha      🟡 W01-alpha       🚫 full-only
    QW2  which to explore?  Wisdom/2  beta       🟡 W01-beta        🚫 full-only
    ```

    #### 2 · QW1 · Send Slate

    **The ask**: which messages should we send?

    **Why now**: a toy reason.

    **What would answer it**: a slate.
    - E1 · cite · the claim · from: QK1.E2
    **Needs agreed**: ✅ 261002

    **Where it stands**: answered.

    **What we expect to lose here**: the predicted tiers.

    #### 3 · QW2 · Explore Slate

    **The ask**: which approaches should we explore?

    **Why now**: a toy reason.

    **What would answer it**: a slate.
    - E1 · judge · what to explore · from: QK1.E2
    **Needs agreed**: ✅ 261002

    **Where it stands**: answered.
    """)


@pytest.fixture
def old(tmp_path):
    project = tmp_path / "Project-Toy"
    board = project / "insights" / "Toy-InsightBoard"
    meta = board / "0-MT-meta"
    pages = {"MT00-meta": META, "MT01-question-data": DATA,
             "MT02-question-information": register("information", "I", "D2"),
             "MT03-question-knowledge": register("knowledge", "K", "I1"), "MT04-question-wisdom": WISDOM}
    for name, text in pages.items():
        (meta / name).mkdir(parents=True)
        (meta / name / f"{name}.md").write_text(text)
    (board / "board.md").write_text("# Toy board\n\n## Topic\n\nOne toy question.\n\n## Board Structure\n\nold\n")
    (project / "src").mkdir()
    (project / "src" / "_thresholds.yaml").write_text("# header\n# more\n\ncommon:\n  ci_level: 0.95   # kept\n")
    return board


def carry(old, tmp_path, name="b52_toy_dikw"):
    proto = old.parent / name
    assert co.main([str(old), str(proto), "--dataset", "toy=data/x.parquet",
                    "--report", str(tmp_path / "report.md")]) == 0
    return proto


def q(proto, rel):
    return yaml.safe_load((proto / rel).read_text().split("---")[1])


def test_every_field_is_carried_word_for_word(old, tmp_path):
    proto = carry(old, tmp_path)
    d1 = q(proto, "j01_data/t01_extract_shape/question.md")
    assert d1["question"] == "what does it hold?" and d1["name"] == "Extract Shape"
    assert d1["ask"] == "what is in this extract, at what shape?" and d1["agreed"] == "✅ 261002"
    assert d1["needs"]["E1"]["retired"] == "two units in one need"
    assert d1["needs"]["E2"]["output"] == {"metrics.json": ["shape.n_rows"]}
    d2 = q(proto, "j01_data/t02_funnel_counts/question.md")
    assert d2["question"] == "how many rows reach each step?"
    text = (proto / "j01_data/t02_funnel_counts/question.md").read_text()
    assert "**Why now**: a partition needs its own denominator.\n\nA second paragraph of why." in text
    w1 = proto / "j04_wisdom/t01_send_slate/question.md"
    assert "**What we expect to lose here**: the predicted tiers." in w1.read_text()
    assert q(proto, "j04_wisdom/t01_send_slate/question.md")["question"] == "which should we send?"
    assert q(proto, "j04_wisdom/t02_explore_slate/question.md")["source"]["gen1"] == "Wisdom/2"
    diffs, rows = co.compare(old, proto)
    assert diffs == [] and any(r[2] == "division text, rebuilt" for r in rows)


def test_ids_are_renamed_by_one_rule(old, tmp_path):
    proto = carry(old, tmp_path)
    i1 = q(proto, "j02_information/t01_toy_information/question.md")
    assert i1["needs"]["E1"]["from"] == "D02.E1" and i1["needs"]["E2"]["from"] == ["E1"]
    assert i1["source"]["id"] == "QI1"


def test_logic_refusals_are_not_asked_and_data_refusals_are(old, tmp_path):
    proto = carry(old, tmp_path)
    assert q(proto, "j01_data/t01_extract_shape/question.md")["partitions"]["asked"] == ["full"]
    assert q(proto, "j01_data/t02_funnel_counts/question.md")["partitions"] == {"asked": "all"}
    k1 = q(proto, "j03_knowledge/t01_toy_knowledge/question.md")["partitions"]
    assert k1["asked"] == ["full"] and "🚫 defer on alpha, beta" in k1["not_elsewhere"]
    assert q(proto, "j04_wisdom/t01_send_slate/question.md")["partitions"] == {"asked": "all"}
    assert q(proto, "j04_wisdom/t02_explore_slate/question.md")["partitions"]["asked"] == ["full"]


def test_meta_partitions_and_thresholds(old, tmp_path):
    proto = carry(old, tmp_path)
    parts = yaml.safe_load((proto / "meta/partitions.md").read_text().split("---")[1])["partitions"]
    assert parts == [{"name": "full", "where": []},
                     {"name": "alpha", "where": [{"column": "g", "eq": "a"}, {"column": "h", "lte": 3.0}]},
                     {"name": "beta", "where": [{"column": "h", "gte": 1.0}, {"column": "h", "lte": 2.0}]},
                     {"name": "cross", "of": ["alpha", "beta"]}]
    assert "**In plain words.** alpha is group a at low h." in (proto / "meta/partitions.md").read_text()
    meta = (proto / "meta/meta.md").read_text()
    assert "What data does this board read?" in meta and "owner:" not in meta and "not carried" not in meta
    th = (proto / "meta/thresholds.yaml").read_text()
    assert "ci_level: 0.95   # kept" in th and "# header" not in th
    assert yaml.safe_load(th)["power"] == {"smallest_effect_pp": None}
    assert "Nothing here concludes." in (proto / "j01_data/level.md").read_text()
    board = (proto / "board.md").read_text()
    assert "board-kind: task-block" in board and "workbench: insight" in board and "toy: data/x.parquet" in board and "One toy question." in board and "old" not in board


def test_the_same_bytes_twice_and_never_over_a_prototype(old, tmp_path):
    a, b = carry(old, tmp_path, "P-A"), carry(old, tmp_path, "P-B")
    files = sorted(p.relative_to(a) for p in a.rglob("*") if p.is_file())
    assert files == sorted(p.relative_to(b) for p in b.rglob("*") if p.is_file())
    assert all((a / f).read_bytes() == (b / f).read_bytes() for f in files)
    with pytest.raises(SystemExit):
        co.main([str(old), str(a)])


def test_a_changed_field_is_a_difference(old, tmp_path):
    proto = carry(old, tmp_path)
    f = proto / "j01_data/t01_extract_shape/question.md"
    f.write_text(f.read_text().replace("every later rate divides by it.", "every later rate needs it."))
    diffs, _ = co.compare(old, proto)
    assert {d[0] for d in diffs} == {"QD1 · why now", "QD1 · division text, rebuilt"}
    assert co.main([str(old), str(proto), "--check"]) == 1


def test_a_carried_prototype_reads_in_the_checker(old, tmp_path):
    proto = carry(old, tmp_path)
    qs, dup = ci.load_questions(proto)
    assert dup == [] and sorted(qs) == ["D01", "D02", "I01", "K01", "W01", "W02"]
    parts = yaml.safe_load((proto / "meta/partitions.md").read_text().split("---")[1])["partitions"]
    problems, notes = ci.check_question("K01", *qs["K01"], qs, {}, parts, qs["K01"][1]["_prose"])
    assert problems == [] and any("Q1 one thing" in n for n in notes)
    problems, _ = ci.check_question("D02", *qs["D02"], qs, {}, parts, qs["D02"][1]["_prose"])
    assert problems == ["D02: j01_data/t02_funnel_counts/scripts: expected one script with SPEC = \"D02\", found 0"
                        .replace("j01_data/t02_funnel_counts/scripts", str(qs["D02"][0] / "scripts"))]
