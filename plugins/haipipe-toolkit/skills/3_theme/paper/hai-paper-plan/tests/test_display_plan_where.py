"""display_plan.rows: a row's `where` places it Main, Supplement (Extended Data, eAppendix) or SI (a Nature journal's
Supplementary Information, a document apart; ScalingGlucose-Board-v2 261122)."""
import importlib.util
from pathlib import Path

spec = importlib.util.spec_from_file_location("display_plan", Path(__file__).resolve().parents[1] / "scripts" / "display_plan.py")
dp = importlib.util.module_from_spec(spec); spec.loader.exec_module(dp)


def test_where_reads_main_supplement_and_si(tmp_path):
    face = tmp_path / "s06-paper-displays" / "s06-paper-displays.md"
    face.parent.mkdir()
    face.write_text("# s06\n\n| Display | type | where |\n|---|---|---|\n| Figure 1 | figure | main |\n"
                    "| Extended Data Fig. 1 | figure | supplement |\n| Display S1 | table | SI |\n"
                    "| Display S2 | table | Supplementary Information |\n")
    assert [r["where"] for r in dp.rows(tmp_path)] == ["main", "supplement", "si", "si"]
