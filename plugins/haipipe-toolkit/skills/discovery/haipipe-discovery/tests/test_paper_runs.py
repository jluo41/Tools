from __future__ import annotations

import importlib.util
import os
import sys
import tempfile
import unittest
from pathlib import Path


SCRIPT = Path(__file__).parents[1] / "scripts" / "paper_runs.py"
SPEC = importlib.util.spec_from_file_location("paper_runs", SCRIPT)
assert SPEC and SPEC.loader
paper_runs = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = paper_runs
SPEC.loader.exec_module(paper_runs)


def make_pair(
    topic: Path,
    stem: str,
    *,
    status: str = "complete",
    key: str = "Demo2026",
    doi: str = "10.1000/demo",
) -> None:
    runs = topic / "runs"
    result = topic / "results" / stem
    runs.mkdir(parents=True, exist_ok=True)
    result.mkdir(parents=True, exist_ok=True)
    ticket = runs / f"{stem}.sh"
    ticket.write_text("#!/usr/bin/env bash\nset -euo pipefail\n", encoding="utf-8")
    ticket.chmod(0o755)
    (result / "runtime.yaml").write_text(
        f"""run: {stem}
status: {status}
trigger:
  kind: citation
  input: Demo paper
subject:
  kind: paper
  title: Demo paper
bib:
  source: person-supplied-complete-fixture-entry
  mode: verbatim_copy
executed_at: "2026-09-01T12:00:00-04:00"
""",
        encoding="utf-8",
    )
    if status != "complete":
        return
    (result / f"{stem}.md").write_text(
        f"# Demo paper\n\n- run: {stem}\n- cite: @{key}\n",
        encoding="utf-8",
    )
    (result / "facts.md").write_text("# Facts\n\n- A fact.\n", encoding="utf-8")
    (result / f"{stem}.bib").write_text(
        f"""@article{{{key},
  title = {{Demo paper}},
  author = {{Example, Ada}},
  year = {{2026}},
  doi = {{{doi}}}
}}
""",
        encoding="utf-8",
    )


class PaperRunContractTest(unittest.TestCase):
    def test_valid_pair_and_aggregate(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            topic = Path(temp) / "01_demo_topic"
            make_pair(topic, "r01_example2026_demo")
            (topic / "discovery.yaml").write_text(
                "page: demo-topic.md\n", encoding="utf-8"
            )
            errors, counts, entries = paper_runs.check_topic(topic)
            self.assertEqual([], errors)
            self.assertEqual(1, counts["complete"])
            self.assertEqual(["Demo2026"], [entry.key for entry in entries])
            self.assertIn("@article{Demo2026", paper_runs.aggregate_bib(entries))
            self.assertEqual(
                topic / "evidence" / "bibex" / "demo-topic.bib",
                paper_runs.default_bib_path(topic),
            )
            self.assertEqual(0, paper_runs.command_build_bib(topic, None, True))
            self.assertTrue(paper_runs.default_bib_path(topic).is_file())

    def test_missing_bib_fails_complete_result(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            topic = Path(temp) / "01_demo_topic"
            stem = "r01_example2026_demo"
            make_pair(topic, stem)
            (topic / "results" / stem / f"{stem}.bib").unlink()
            errors, _, _ = paper_runs.check_topic(topic)
            self.assertTrue(
                any(error.startswith("complete-artifact-missing:") for error in errors)
            )

    def test_orphan_result_fails(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            topic = Path(temp) / "01_demo_topic"
            stem = "r01_example2026_demo"
            make_pair(topic, stem, status="planned")
            os.unlink(topic / "runs" / f"{stem}.sh")
            errors, _, _ = paper_runs.check_topic(topic)
            self.assertTrue(any(error.startswith("orphan-result:") for error in errors))

    def test_cite_key_mismatch_fails(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            topic = Path(temp) / "01_demo_topic"
            stem = "r01_example2026_demo"
            make_pair(topic, stem, key="Right2026")
            card = topic / "results" / stem / f"{stem}.md"
            card.write_text(card.read_text().replace("@Right2026", "@Wrong2026"))
            errors, _, _ = paper_runs.check_topic(topic)
            self.assertTrue(
                any(error.startswith("card-cite-mismatch:") for error in errors)
            )

    def test_conflicting_doi_fails(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            topic = Path(temp) / "01_demo_topic"
            make_pair(
                topic,
                "r01_example2026_demo",
                key="DemoA2026",
                doi="10.1000/same",
            )
            make_pair(
                topic,
                "r02_example2026_other",
                key="DemoB2026",
                doi="10.1000/same",
            )
            errors, _, _ = paper_runs.check_topic(topic)
            self.assertTrue(any(error.startswith("bib-doi-conflict:") for error in errors))

    def test_formatted_metadata_bib_mode_fails(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            topic = Path(temp) / "01_demo_topic"
            stem = "r01_example2026_demo"
            make_pair(topic, stem)
            runtime = topic / "results" / stem / "runtime.yaml"
            runtime.write_text(
                runtime.read_text().replace(
                    "mode: verbatim_copy", "mode: formatted_from_metadata"
                ),
                encoding="utf-8",
            )
            errors, _, _ = paper_runs.check_topic(topic)
            self.assertTrue(
                any(error.startswith("runtime-bib-mode-invalid:") for error in errors)
            )


if __name__ == "__main__":
    unittest.main()
