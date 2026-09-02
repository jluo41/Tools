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


def make_topic_path(root: Path, task_name: str = "t01_demo_topic") -> Path:
    return (
        root
        / "discoveries"
        / "b01_fixture_domain"
        / "j01_fixture_inquiry"
        / task_name
    )


def make_topic_contract(
    topic: Path,
    *,
    discovery_type: str = "topic-summary",
    legacy: bool = False,
) -> None:
    topic.mkdir(parents=True, exist_ok=True)
    page = f"{topic.name}.md"
    (topic / page).write_text(
        """# Demo topic
state: 🔴 OPEN
owner: CC
folder-kind: discovery
method: Analyze admitted evidence.

## Opening
What does the evidence say?
This Page owns one bounded evidence question and the records used to answer it.
Each admitted source enters through a canonical Subject and one numbered Run.
A reader can see the current boundary, evidence route, and next action here.

## Writing Style
**Language and voice**: Use plain English and active voice.
**Sentence shape**: Put one claim on each source line.
**Evidence rule**: Keep claims tied to their owning Results and cite keys.
**Required sections**: Keep all four Discovery roles and matching Aims.
**Optional sections**: Add a top-level Diagram only when it helps.
**Question and boundary**: State the inquiry and admission rule.
**Type payload**: Synthesize the selected article promise.
**Evidence map**: Bind support to Results and cite keys.
**Limits and next move**: State limits and the next lawful route.
**Section rules**: Keep subject-specific Content and Aim names aligned.

## Content
### 1 · Question and boundary · demo evidence question
**Evidence boundary**: how the open question admits a source.
```text
❓ Question  open
🧾 Evidence  pending
```

No evidence has been admitted yet.

### 2 · Type payload · demo topic summary
**Summary payload**: where the topic synthesis will be written.
```text
📄 Page     open
🗂 Record   pending
```

The summary is not written yet.

### 3 · Evidence map · demo sources
**Source lineage**: how admitted evidence becomes traceable.
```text
🗃 Candidate  unresolved
🧾 Result     pending
```

No source has been admitted yet.

### 4 · Limits and next move · demo decision
**Open decision**: what remains and where the inquiry goes next.
```text
⚠️ Limit  no evidence
➡️ Next   admit or hold
```

The evidence boundary remains open.

## Aims
### A1 · 🔎 Question and boundary · demo evidence question
- 🔨 A1.1 · The evidence question is answered.
  **Done when:** The answer is supported by admitted Results.
  **Now:** The inquiry is open.

### A2 · 📚 Type payload · demo topic summary
- 🔨 A2.1 · The topic summary answers the question.
  **Done when:** The Page carries a supported synthesis.
  **Now:** The summary is open.

### A3 · 🔗 Evidence map · demo sources
- 🔨 A3.1 · Evidence is traceable to Results.
  **Done when:** Every claim names a Result and cite key.
  **Now:** No source is admitted.

### A4 · 🧭 Limits and next move · demo decision
- ✅ A4.1 · The current limitation and next route are explicit.
  **Done when:** A reader can choose admit or hold.
  **Now:** Both routes are visible.
""",
        encoding="utf-8",
    )
    type_fields = (
        "type: Review\nrole: topic_summary\n"
        if legacy
        else f"discovery_type: {discovery_type}\n"
    )
    block_id = topic.parent.parent.name[:3]
    job_id = topic.parent.name[:3]
    task_id = topic.name[:3]
    readable = f"{block_id}.{job_id}.{task_id}"
    compact = f"{block_id}{job_id}{task_id}"
    (topic / "discovery.yaml").write_text(
        "version: 6\n"
        "kind: discovery\n"
        f"address: {readable}\n"
        f"address_compact: {compact}\n"
        f"block:\n  id: {block_id}\n  slug: fixture_domain\n  title: Fixture domain\n"
        f"job:\n  id: {job_id}\n  slug: fixture_inquiry\n  title: Fixture inquiry\n"
        f"task:\n  id: {task_id}\n  slug: {topic.name[4:]}\n  title: Demo topic\n"
        f"page: {page}\n"
        "status: planned\n"
        f"{type_fields}",
        encoding="utf-8",
    )


def make_pair(
    topic: Path,
    stem: str,
    *,
    status: str = "complete",
    key: str = "Demo2026",
    doi: str = "10.1000/demo",
) -> None:
    if not (topic / "discovery.yaml").is_file():
        make_topic_contract(topic)
    runs = topic / "runs"
    result = topic / "results" / stem
    runs.mkdir(parents=True, exist_ok=True)
    result.mkdir(parents=True, exist_ok=True)
    ticket = runs / f"{stem}.sh"
    ticket.write_text("#!/usr/bin/env bash\nset -euo pipefail\n", encoding="utf-8")
    ticket.chmod(0o755)
    readable = topic.joinpath("discovery.yaml").read_text(encoding="utf-8")
    topic_address = paper_runs._field(readable, paper_runs.ADDRESS_FIELD_RE)
    topic_compact = paper_runs._field(readable, paper_runs.ADDRESS_COMPACT_FIELD_RE)
    run_id = stem[:3]
    (result / "runtime.yaml").write_text(
        f"""run: {stem}
address: {topic_address}.{run_id}
address_compact: {topic_compact}{run_id}
family: discovery
operation: paper-analysis
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
    def test_page_requires_writing_style(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            topic = make_topic_path(Path(temp))
            make_topic_contract(topic)
            page = topic / f"{topic.name}.md"
            page.write_text(
                page.read_text(encoding="utf-8").replace(
                    "## Writing Style", "## Local prose notes"
                ),
                encoding="utf-8",
            )
            errors, _, _ = paper_runs.check_topic(topic)
            self.assertTrue(
                any(error.startswith("page-writing-style-missing:") for error in errors)
            )

    def test_content_division_requires_captioned_face_diagram(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            topic = make_topic_path(Path(temp))
            make_topic_contract(topic)
            page = topic / f"{topic.name}.md"
            page.write_text(
                page.read_text(encoding="utf-8").replace(
                    "**Evidence boundary**: how the open question admits a source.",
                    "Evidence boundary without a caption.",
                ),
                encoding="utf-8",
            )
            errors, _, _ = paper_runs.check_topic(topic)
            self.assertTrue(
                any(
                    error.startswith("page-content-division-diagram-missing:")
                    for error in errors
                )
            )

    def test_terminal_status_requires_report(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            topic = make_topic_path(Path(temp))
            make_topic_contract(topic)
            manifest = topic / "discovery.yaml"
            manifest.write_text(
                manifest.read_text(encoding="utf-8").replace(
                    "status: planned", "status: ok"
                ),
                encoding="utf-8",
            )
            errors, _, _ = paper_runs.check_topic(topic)
            self.assertTrue(
                any(error.startswith("manifest-report-missing:") for error in errors)
            )

    def test_content_and_aim_group_names_must_match(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            topic = make_topic_path(Path(temp))
            make_topic_contract(topic)
            page = topic / f"{topic.name}.md"
            page.write_text(
                page.read_text(encoding="utf-8").replace(
                    "### A1 · 🔎 Question and boundary · demo evidence question",
                    "### A1 · 🔎 Question and boundary · changed name",
                ),
                encoding="utf-8",
            )
            errors, _, _ = paper_runs.check_topic(topic)
            self.assertTrue(
                any(error.startswith("page-aim-name-drift:") for error in errors)
            )

    def test_done_page_cannot_keep_an_active_aim(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            topic = make_topic_path(Path(temp))
            make_topic_contract(topic)
            page = topic / f"{topic.name}.md"
            page.write_text(
                page.read_text(encoding="utf-8").replace(
                    "state: 🔴 OPEN", "state: ✅ REPORTED"
                ),
                encoding="utf-8",
            )
            errors, _, _ = paper_runs.check_topic(topic)
            self.assertTrue(
                any(error.startswith("page-done-with-open-aim:") for error in errors)
            )

    def test_every_bjt_level_requires_its_letter(self) -> None:
        for level, expected_error in (
            ("block", "address-block-name-invalid:"),
            ("job", "address-job-name-invalid:"),
            ("task", "address-task-name-invalid:"),
        ):
            with self.subTest(level=level), tempfile.TemporaryDirectory() as temp:
                topic = make_topic_path(Path(temp))
                make_topic_contract(topic)
                target = {
                    "block": topic.parent.parent,
                    "job": topic.parent,
                    "task": topic,
                }[level]
                target.rename(target.with_name(target.name[1:]))
                moved_topic = next(Path(temp).rglob("t01_demo_topic"), None)
                if level == "task":
                    moved_topic = next(Path(temp).rglob("01_demo_topic"))
                assert moved_topic is not None
                errors, _, _ = paper_runs.check_topic(moved_topic)
                self.assertTrue(
                    any(error.startswith(expected_error) for error in errors), errors
                )

    def test_run_name_requires_r_letter(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            topic = make_topic_path(Path(temp))
            make_pair(topic, "r01_example2026_demo")
            run = topic / "runs" / "r01_example2026_demo.sh"
            run.rename(run.with_name("01_example2026_demo.sh"))
            errors, _, _ = paper_runs.check_topic(topic)
            self.assertTrue(any(error.startswith("orphan-result:") for error in errors))
            self.assertTrue(any(error.startswith("runname-invalid:") for error in errors))

    def test_all_canonical_page_types_are_valid_without_fake_runs(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            for index, discovery_type in enumerate(
                sorted(paper_runs.DISCOVERY_TYPES), start=1
            ):
                with self.subTest(discovery_type=discovery_type):
                    task_name = (
                        f"t{index:02d}_{discovery_type.replace('-', '_')}_page"
                    )
                    topic = make_topic_path(Path(temp), task_name)
                    make_topic_contract(topic, discovery_type=discovery_type)
                    errors, counts, entries = paper_runs.check_topic(topic)
                    self.assertEqual([], errors)
                    self.assertEqual(0, sum(counts.values()))
                    self.assertEqual([], entries)

    def test_valid_pair_and_aggregate(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            topic = make_topic_path(Path(temp))
            make_pair(topic, "r01_example2026_demo")
            errors, counts, entries = paper_runs.check_topic(topic)
            self.assertEqual([], errors)
            self.assertEqual(1, counts["complete"])
            self.assertEqual(["Demo2026"], [entry.key for entry in entries])
            self.assertIn("@article{Demo2026", paper_runs.aggregate_bib(entries))
            self.assertEqual(
                topic / "evidence" / "bibex" / "t01_demo_topic.bib",
                paper_runs.default_bib_path(topic),
            )
            self.assertEqual(0, paper_runs.command_build_bib(topic, None, True))
            self.assertTrue(paper_runs.default_bib_path(topic).is_file())

    def test_missing_bib_fails_complete_result(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            topic = make_topic_path(Path(temp))
            stem = "r01_example2026_demo"
            make_pair(topic, stem)
            (topic / "results" / stem / f"{stem}.bib").unlink()
            errors, _, _ = paper_runs.check_topic(topic)
            self.assertTrue(
                any(error.startswith("complete-artifact-missing:") for error in errors)
            )

    def test_orphan_result_fails(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            topic = make_topic_path(Path(temp))
            stem = "r01_example2026_demo"
            make_pair(topic, stem, status="planned")
            os.unlink(topic / "runs" / f"{stem}.sh")
            errors, _, _ = paper_runs.check_topic(topic)
            self.assertTrue(any(error.startswith("orphan-result:") for error in errors))

    def test_cite_key_mismatch_fails(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            topic = make_topic_path(Path(temp))
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
            topic = make_topic_path(Path(temp))
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
            topic = make_topic_path(Path(temp))
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

    def test_legacy_type_and_role_are_readable(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            topic = make_topic_path(Path(temp))
            make_topic_contract(topic, legacy=True)
            make_pair(topic, "r01_example2026_demo")
            errors, _, _ = paper_runs.check_topic(topic)
            self.assertEqual([], errors)

    def test_invalid_discovery_type_fails(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            topic = make_topic_path(Path(temp))
            make_topic_contract(topic, discovery_type="paper-type-that-does-not-exist")
            errors, _, _ = paper_runs.check_topic(topic)
            self.assertTrue(
                any(
                    error.startswith("manifest-discovery-type-invalid:")
                    for error in errors
                )
            )

    def test_canonical_and_legacy_type_must_agree(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            topic = make_topic_path(Path(temp))
            make_topic_contract(topic, discovery_type="topic-summary")
            manifest = topic / "discovery.yaml"
            manifest.write_text(
                manifest.read_text(encoding="utf-8")
                + "type: Idea\nrole: novelty_check\n",
                encoding="utf-8",
            )
            errors, _, _ = paper_runs.check_topic(topic)
            self.assertTrue(
                any(
                    error.startswith("manifest-discovery-type-conflict:")
                    for error in errors
                )
            )

    def test_paper_subject_requires_paper_analysis_operation(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            topic = make_topic_path(Path(temp))
            stem = "r01_example2026_demo"
            make_pair(topic, stem)
            runtime = topic / "results" / stem / "runtime.yaml"
            runtime.write_text(
                runtime.read_text(encoding="utf-8").replace(
                    "operation: paper-analysis", "operation: source-analysis"
                ),
                encoding="utf-8",
            )
            errors, _, _ = paper_runs.check_topic(topic)
            self.assertTrue(
                any(
                    error.startswith("runtime-operation-subject-mismatch:")
                    for error in errors
                )
            )

    def test_runtime_global_address_must_match_path(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            topic = make_topic_path(Path(temp))
            stem = "r01_example2026_demo"
            make_pair(topic, stem)
            runtime = topic / "results" / stem / "runtime.yaml"
            runtime.write_text(
                runtime.read_text(encoding="utf-8").replace(
                    "address: b01.j01.t01.r01", "address: b01.j01.t99.r01"
                ),
                encoding="utf-8",
            )
            errors, _, _ = paper_runs.check_topic(topic)
            self.assertTrue(
                any(error.startswith("runtime-address-mismatch:") for error in errors)
            )

    def test_unresolved_run_still_requires_resolved_subject(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            topic = make_topic_path(Path(temp))
            stem = "r01_example2026_demo"
            make_pair(topic, stem, status="unresolved")
            runtime = topic / "results" / stem / "runtime.yaml"
            text = runtime.read_text(encoding="utf-8")
            text = text.replace(
                "subject:\n  kind: paper\n  title: Demo paper\n", ""
            )
            runtime.write_text(text, encoding="utf-8")
            errors, _, _ = paper_runs.check_topic(topic)
            self.assertTrue(
                any(error.startswith("runtime-subject-missing:") for error in errors)
            )

    def test_non_paper_subject_accepts_source_analysis_operation(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            topic = make_topic_path(Path(temp))
            stem = "r01_example2026_demo"
            make_pair(topic, stem)
            runtime = topic / "results" / stem / "runtime.yaml"
            text = runtime.read_text(encoding="utf-8")
            text = text.replace("operation: paper-analysis", "operation: source-analysis")
            text = text.replace("kind: paper", "kind: report")
            runtime.write_text(text, encoding="utf-8")
            errors, _, _ = paper_runs.check_topic(topic)
            self.assertEqual([], errors)


if __name__ == "__main__":
    unittest.main()
