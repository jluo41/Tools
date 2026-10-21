"""haipipe-run: each Run card says its role (JL 261020: "各司其职"). run_roles.py proposes it from the Run's name and
writes one line after `kind:`; a card that has a role keeps it."""
import io
import sys
import tempfile
import unittest
from contextlib import redirect_stdout
from pathlib import Path

SKILL = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(SKILL / "scripts"))
import run_roles  # noqa: E402


class RunRolesTest(unittest.TestCase):
    def test_the_name_proposes_the_role_first_match_wins(self):
        cases = {"r09_audit_published_site": "check", "r12_publish_site": "publish", "r58_retry_fold00": "fix",
                 "r01_smoke50": "trial", "r03_figures_by_rank": "figures", "r02_describe_table": "describe",
                 "run-page-evidence-item-e03": "evidence", "r02_fold01": "make"}
        for name, role in cases.items():
            self.assertEqual(run_roles.propose(name), role, name)

    def test_apply_writes_one_line_after_kind_and_keeps_a_role_already_set(self):
        with tempfile.TemporaryDirectory() as tmp:
            runs = Path(tmp) / "b01_topic" / "j01_job" / "t01_task" / "runs"
            for name, card in {"r01_retry_fold00": "run: r01_retry_fold00\nkind: hard\nstatus: done\n",
                               "r02_fold00": "run: r02_fold00\nkind: hard\nrole: check\n"}.items():
                (runs / name).mkdir(parents=True)
                (runs / name / "run.yaml").write_text(card)
            with redirect_stdout(io.StringIO()):
                run_roles.main([str(Path(tmp) / "b01_topic"), "--apply"])
            self.assertEqual((runs / "r01_retry_fold00" / "run.yaml").read_text(),
                             "run: r01_retry_fold00\nkind: hard\nrole: fix\nstatus: done\n")
            self.assertEqual((runs / "r02_fold00" / "run.yaml").read_text(), "run: r02_fold00\nkind: hard\nrole: check\n")


if __name__ == "__main__":
    unittest.main()
