"""The Overall Report's figures (ref/overall_figures.py, JL 261013: "figures to show it to quickly get the outcome"):
each kind drawn from a cited Run's result table only, its file named <X>-<name>.png, and its source cited the way
the pages cite. Placeholder tables, no data."""
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "ref"))
import overall_figures as OF  # noqa: E402

R = "runs/r01_full/result/"


def _csv(job: Path, rel: str, text: str) -> str:
    (job / rel).parent.mkdir(parents=True, exist_ok=True)
    (job / rel).write_text(text, encoding="utf-8")
    return rel


@pytest.fixture
def job(tmp_path):
    j = tmp_path / "j01_prototype-p1-demo_data-Demov1"
    _csv(j, "t06_I01_funnel/" + R + "overall_rates.csv",
         "outcome,n,k,rate_pct\nclicked,100,60,60.0\nredeemed,100,2,2.0\nopted_out,100,1,1.0\n")
    _csv(j, "t07_I02_arms/" + R + "rates_by_arm.csv",
         "level,outcome,n,k,rate_pct,ci_lo_pct,ci_hi_pct,suppressed\n"
         "armA,clicked,50,33,66.0,60.0,72.0,False\nmyDefault,clicked,50,30,60.0,54.0,66.0,False\n"
         "armC,clicked,50,25,50.0,44.0,56.0,False\narmD,clicked,5,1,20.0,1.0,60.0,True\n")
    _csv(j, "t19_I14_cuts/runs/r07_cross/result/arm_cells.csv",
         "partition,arm,rate_pct\ncutA,armA,55\ncutA,armC,45\ncutB,armA,65\ncutB,armC,58\n")
    _csv(j, "t25_I20_age/" + R + "rates_by_age.csv",
         "level,outcome,rate_pct\n20.0,clicked,45\n60.0,clicked,66\n")
    return j


def test_every_kind_draws_from_its_table(job, tmp_path):
    specs = [
        {"name": "funnel", "title": "t", "kind": "bars", "table": "t06_I01_funnel/" + R + "overall_rates.csv",
         "label": "outcome", "value": "rate_pct", "count": "k", "of": "n", "rows": {"clicked": "Clicked", "redeemed": "Redeemed"}},
        {"name": "arms", "title": "t", "kind": "dots", "table": "t07_I02_arms/" + R + "rates_by_arm.csv",
         "where": {"outcome": "clicked"}, "label": "level", "value": "rate_pct", "low": "ci_lo_pct", "high": "ci_hi_pct",
         "mark": {"armA": "best", "myDefault": "reference", "*": "drop"}},
        {"name": "cuts", "title": "t", "kind": "lines", "table": "t19_I14_cuts/runs/r07_cross/result/arm_cells.csv",
         "x": "partition", "group": "arm", "value": "rate_pct", "columns": {"cutA": "A", "cutB": "B"}, "mark": {"armA": "best"}},
        {"name": "drivers", "title": "t", "kind": "ranges", "rows": [
            {"label": "The message", "table": "t07_I02_arms/" + R + "rates_by_arm.csv", "where": {"outcome": "clicked"},
             "value": "rate_pct"},
            {"label": "Age", "table": "t25_I20_age/" + R + "rates_by_age.csv", "where": {"outcome": "clicked"},
             "value": "rate_pct", "names": {"20.0": "ages 20-24"}}]}]
    made = OF.draw(job, "X01", specs, tmp_path / "figures")
    assert [p.name for _, p in made] == ["X01-funnel.png", "X01-arms.png", "X01-cuts.png", "X01-drivers.png"]
    assert all(p.stat().st_size > 2000 for _, p in made)
    assert OF.cite(specs[3]) == "(I02 · t07), (I20 · t25)"
    assert OF.cite(specs[0]) == "(I01 · t06)"


def test_a_suppressed_row_and_unknown_kind(job, tmp_path):
    df = OF._table(job, "t07_I02_arms/" + R + "rates_by_arm.csv", {"outcome": "clicked"}, "rate_pct")
    assert "armD" not in set(df["level"])                       # a cell the Run hid stays hidden
    with pytest.raises(SystemExit):
        OF.draw(job, "X01", [{"name": "x", "kind": "pie", "table": "t06_I01_funnel/" + R + "overall_rates.csv"}],
                tmp_path / "figures")


def test_words():
    assert OF._words("progressFeedback", {}) == "progress feedback"
    assert OF._words("20.0", {}) == "20"
    assert OF._words("default", {"default": "default message"}) == "default message"
