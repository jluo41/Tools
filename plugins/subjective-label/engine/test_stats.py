"""Focused regression tests for the engine statistics and helper modules.

Run from inside engine/ (the repo-root `code/` package shadows stdlib `code`):
    python -m pytest -q test_stats.py
All data is small and in memory or under tmp_path; no real job is built.
"""
from __future__ import annotations

import asyncio
import importlib.util
import json
import subprocess
import sys
import types
from pathlib import Path

import pytest
import yaml


HERE = Path(__file__).resolve().parent
if str(HERE) not in sys.path:
    sys.path.insert(0, str(HERE))

LABELS = ["HIGH", "LOW", "NONE"]


def _load(name: str):
    spec = importlib.util.spec_from_file_location(f"sl_stats_{name}", HERE / f"{name}.py")
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


kappa = _load("kappa")
converge = _load("converge")
label = _load("label")
sample = _load("sample")
classify = _load("classify")
embed = _load("embed")
license_ = _load("license")
page_plugin = _load("page_plugin")


def _gates():
    import gates  # noqa: PLC0415

    return gates


def write_jsonl(path: Path, rows: list[dict]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("".join(json.dumps(r) + "\n" for r in rows), encoding="utf-8")


def v2_job(root: Path) -> Path:
    root.mkdir(parents=True, exist_ok=True)
    (root / "config.yaml").write_text(
        yaml.safe_dump({"schema_version": "subjective-label/v2",
                        "labels": {"values": LABELS}}),
        encoding="utf-8",
    )
    return root


@pytest.fixture
def fake_status(monkeypatch):
    """Replace job.status with a controllable fake; no real job is built."""
    state = {"phase": "P0", "g0_receipt_valid": False, "calls": 0}

    def status(job_root):
        state["calls"] += 1
        return {k: v for k, v in state.items() if k != "calls"}

    fake = types.ModuleType("job")
    fake.status = status
    monkeypatch.setitem(sys.modules, "job", fake)
    return state


# ── fix 1 · classifier trains on human-confirmed gold only ──────────────────

def test_classifier_training_excludes_panel_consensus(tmp_path):
    gallery = tmp_path / "gallery.json"
    gallery.write_text(json.dumps([{"id": "g1", "text": "t1", "label": "HIGH"}]))
    extra = tmp_path / "panel_labels.jsonl"
    write_jsonl(extra, [
        {"id": "p1", "text": "t2", "label": "LOW",
         "provenance": "panel-unanimous", "category": "D"},
        {"id": "h1", "text": "t3", "label": "NONE", "provenance_tier": "human_confirmed"},
    ])
    rows = classify._gather_training_data(tmp_path, gallery, [extra], True)
    assert {r["id"] for r in rows} == {"g1", "h1"}


# ── fix 2 · failures are counted, never silently dropped ────────────────────

def _kappa_project(tmp_path: Path, preds: dict, gold: dict, version: str = "v01") -> Path:
    pd = tmp_path / "proj"
    pd.mkdir(parents=True, exist_ok=True)
    (pd / "config.yaml").write_text(yaml.safe_dump({"labels": {"values": LABELS}}))
    write_jsonl(pd / "eval" / "anchor_set.jsonl",
                [{"anchor_idx": i, "gold": g} for i, g in gold.items()])
    write_jsonl(pd / "eval" / "per_version" / f"{version}_solo_results.jsonl",
                [{"anchor_idx": i, "pred": p} for i, p in preds.items()])
    return pd


def _run_kappa(pd: Path, version: str) -> list[dict]:
    out = subprocess.run(
        [sys.executable, str(HERE / "kappa.py"), "--project-dir", str(pd),
         "--version", version, "--engines", "solo"],
        capture_output=True, text=True, cwd=HERE,
    )
    assert out.returncode == 0, out.stderr
    traj = pd / "eval" / "trajectory.jsonl"
    return [json.loads(l) for l in traj.read_text().splitlines() if l.strip()]


GOLD10 = {i: ("HIGH" if i % 2 else "LOW") for i in range(1, 11)}
PREDS_HALF_FAILED = {1: "HIGH", 2: "LOW", 3: "HIGH", 4: "LOW", 5: "HIGH",
                     6: "PARSE_ERROR", 7: "PARSE_ERROR", 8: "ERROR", 9: None}  # 10 missing


def test_kappa_report_counts_failures_and_adds_all_item_metrics(tmp_path):
    pd = _kappa_project(tmp_path, PREDS_HALF_FAILED, GOLD10)
    report = _run_kappa(pd, "v01")[-1]
    # existing keys kept
    assert report["kappa_solo_vs_gold"] == 1.0
    assert report["acc_solo_vs_gold"] == 1.0
    # failures reported and scored as wrong
    assert report["n_scored_solo_vs_gold"] == 5
    assert report["n_failed_solo_vs_gold"] == 5
    assert report["acc_all_solo_vs_gold"] == 0.5
    assert report["kappa_all_solo_vs_gold"] == pytest.approx(0.3333, abs=1e-3)
    assert report["n_failed_majority_vs_gold"] == 5
    assert report["kappa_all_majority_vs_gold"] < 1.0


def test_score_vs_gold_ordinal_counts_failure_as_maximal_error():
    gold = {1: "LOW", 2: "HIGH", 3: "NONE", 4: "HIGH"}
    pred = {1: "LOW", 2: "HIGH", 3: "NONE", 4: "PARSE_ERROR"}
    s = kappa.score_vs_gold(pred, gold, ["NONE", "LOW", "HIGH"], "ordinal")
    assert s["kappa"] == 1.0 and s["n_scored"] == 3 and s["n_failed"] == 1
    assert s["kappa_all"] < 1.0 and s["acc_all"] == 0.75


# ── fix 3 · no valid vote is UNRESOLVED, never NONE ─────────────────────────

def test_majority_without_valid_vote_is_unresolved(tmp_path):
    out = kappa.majority([{1: "PARSE_ERROR", 2: "HIGH"}, {1: "ERROR", 2: None}],
                         LABELS, "NONE", "none_loses")
    assert out[1] == "UNRESOLVED"
    assert out[2] == "HIGH"
    # and it is excluded from class metrics (no phantom NONE predictions)
    pd = _kappa_project(tmp_path, PREDS_HALF_FAILED, GOLD10)
    report = _run_kappa(pd, "v01")[-1]
    assert report["per_label_majority"]["NONE"]["precision"] is None
    assert report["per_label_majority_n_failed"] == 5


# ── fix 4 · F1 is 0.0, not None, when the class was never hit ───────────────

def test_f1_zero_when_no_true_positive():
    stats = kappa.per_label_prf({1: "LOW"}, {1: "HIGH"}, LABELS)
    assert stats["HIGH"]["f1"] == 0.0     # gold present, never predicted
    assert stats["LOW"]["f1"] == 0.0      # predicted, never gold
    assert stats["NONE"]["f1"] is None    # neither gold nor predicted


# ── fix 5 · natural version sort ────────────────────────────────────────────

def test_kappa_trajectory_uses_natural_version_order(tmp_path):
    gold = {1: "HIGH", 2: "LOW"}
    pd = _kappa_project(tmp_path, {1: "HIGH", 2: "LOW"}, gold, version="v9")
    for v in ("v10", "v2"):
        write_jsonl(pd / "eval" / "per_version" / f"{v}_solo_results.jsonl",
                    [{"anchor_idx": 1, "pred": "HIGH"}, {"anchor_idx": 2, "pred": "LOW"}])
    for v in ("v9", "v10", "v2"):
        rows = _run_kappa(pd, v)
    assert [r["version"] for r in rows] == ["v2", "v9", "v10"]


def test_converge_cli_uses_natural_version_order(tmp_path):
    pd = tmp_path / "proj"
    write_jsonl(pd / "eval" / "trajectory.jsonl", [
        {"version": "v10", "anchor_kappa": 0.80, "heldout_kappa": 0.79},
        {"version": "v9", "anchor_kappa": 0.40, "heldout_kappa": 0.39},
    ])
    out = subprocess.run([sys.executable, str(HERE / "converge.py"), "--project-dir", str(pd)],
                         capture_output=True, text=True, cwd=HERE)
    assert out.returncode == 0, out.stderr
    verdict = json.loads(out.stdout)
    assert verdict["anchor_kappa"] == 0.80
    assert verdict["verdict"] == "IMPROVING"


# ── fix 6 · plateau is a diagnostic; below the floor never reads converged ──

def test_converge_plateau_below_quality_floor_is_not_converged():
    low = [{"version": "v1", "anchor_kappa": 0.10, "heldout_kappa": 0.10},
           {"version": "v2", "anchor_kappa": 0.11, "heldout_kappa": 0.10}]
    r = converge.assess(low, quality_floor=0.6)
    assert "CONVERGED" not in r["verdict"] and "PLATEAU" not in r["verdict"]
    assert r["verdict"] == "BELOW_QUALITY_FLOOR"
    ok = [{"version": "v3", "anchor_kappa": 0.78, "heldout_kappa": 0.76},
          {"version": "v4", "anchor_kappa": 0.79, "heldout_kappa": 0.77}]
    r = converge.assess(ok, quality_floor=0.6)
    assert r["verdict"] == "PLATEAU_DIAGNOSTIC"
    assert "CONVERGED" not in converge.assess(low)["verdict"]


def test_converge_cli_reads_stopping_quality_floor(tmp_path):
    pd = tmp_path / "proj"
    write_jsonl(pd / "eval" / "trajectory.jsonl", [
        {"version": "v1", "anchor_kappa": 0.10, "heldout_kappa": 0.10},
        {"version": "v2", "anchor_kappa": 0.11, "heldout_kappa": 0.10},
    ])
    (pd / "config.yaml").write_text(yaml.safe_dump({"stopping": {"quality_floor": 0.6}}))
    out = subprocess.run([sys.executable, str(HERE / "converge.py"), "--project-dir", str(pd)],
                         capture_output=True, text=True, cwd=HERE)
    assert out.returncode == 0, out.stderr
    verdict = json.loads(out.stdout)
    assert verdict["verdict"] == "BELOW_QUALITY_FLOOR"
    assert verdict["quality_floor"] == 0.6


@pytest.mark.parametrize("script", ["kappa.py", "converge.py"])
def test_cli_without_args_prints_usage(script):
    out = subprocess.run([sys.executable, str(HERE / script)],
                         capture_output=True, text=True, cwd=HERE)
    assert out.returncode != 0
    assert "usage" in out.stderr.lower()
    assert "Traceback" not in out.stderr


# ── fix 7 · parser accepts valid JSON only, never guesses ───────────────────

def test_label_parser_does_not_guess():
    parse = label._make_parser(LABELS)
    echoed = '{"label": "HIGH|LOW|NONE", "confidence": 0.0-1.0, "reason": "<=12 words"}'
    for raw in (echoed, "Not HIGH. Final answer: LOW", "HIGH", ""):
        got = parse(raw)
        assert got["label"] == "PARSE_ERROR", (raw, got)
        assert got["parse"] == "fail"
        assert "Final answer" not in got["reason"] and len(got["reason"]) <= 40
    ok = parse('{"label": "low", "confidence": 0.8, "reason": "short"}')
    assert ok["label"] == "LOW" and ok["parse"] == "json"


def test_run_engine_marks_parse_failure_without_raw_text(tmp_path, monkeypatch):
    async def fake(system_prompt, text, model):
        return "Considering everything, the answer is HIGH because of the wording"

    monkeypatch.setitem(label.ENGINES, "fake", fake)
    items = [{"anchor_idx": 1, "id": "a1", "text": "item"}]
    rows = asyncio.run(label.run_engine(tmp_path, "fake", "v01", "t", "sys", items,
                                        label._make_parser(LABELS), "m", 1,
                                        tmp_path / "out.jsonl"))
    assert rows[0]["pred"] == "PARSE_ERROR"
    assert rows[0]["status"] == "failed"
    assert "Considering" not in rows[0]["reason"]


# ── fix 8 · sampling: dedup, quota math, provenance, order invariance ───────

def _corpus(n_signal_a=4, n_both=2, n_none=40):
    rows = [{"id": f"b{i}", "text": "alpha beta"} for i in range(n_both)]
    rows += [{"id": f"a{i}", "text": "beta only"} for i in range(n_signal_a)]
    rows += [{"id": f"n{i}", "text": "silent"} for i in range(n_none)]
    return rows


def test_sample_dedups_before_slicing_so_later_strata_fill():
    rows = _corpus()
    lex = {"alpha": r"alpha", "beta": r"beta"}   # b* fire both; alpha has only b*
    for seed in range(10):
        s = sample.sample(rows, lex, {}, per_stratum=2, none_quota=0.0, seed=seed)
        by = {k: sum(1 for p in s if p["stratum"] == k) for k in ("alpha", "beta")}
        assert by == {"alpha": 2, "beta": 2}, (seed, by)
        assert len({p["id"] for p in s}) == len(s)


def test_sample_none_quota_math():
    rows = _corpus()
    lex = {"beta": r"beta"}
    zero = sample.sample(rows, lex, {}, per_stratum=4, none_quota=0.0, seed=1)
    assert sum(p["stratum"] == "none_quota" for p in zero) == 0
    half = sample.sample(rows, lex, {}, per_stratum=4, none_quota=0.5, seed=1)
    assert sum(p["stratum"] == "none_quota" for p in half) == 4
    full = sample.sample(rows, lex, {}, per_stratum=4, none_quota=1.0, seed=1)
    assert sum(p["stratum"] == "none_quota" for p in full) == 40


def test_sample_emits_seed_and_inclusion_probability():
    rows = _corpus()
    s = sample.sample(rows, {"beta": r"beta"}, {}, per_stratum=3, none_quota=0.5, seed=7)
    for p in s:
        assert p["seed"] == 7
    beta = [p for p in s if p["stratum"] == "beta"]
    none = [p for p in s if p["stratum"] == "none_quota"]
    assert all(p["inclusion_probability"] == pytest.approx(3 / 6) for p in beta)
    assert all(p["inclusion_probability"] == pytest.approx(3 / 40) for p in none)


def test_sample_same_seed_is_invariant_to_corpus_order():
    rows = _corpus(n_signal_a=20, n_both=0, n_none=60)
    lex = {"beta": r"beta"}
    a = sample.sample(rows, lex, {}, per_stratum=5, none_quota=0.5, seed=3)
    b = sample.sample(list(reversed(rows)), lex, {}, per_stratum=5, none_quota=0.5, seed=3)
    assert [(p["id"], p["stratum"]) for p in a] == [(p["id"], p["stratum"]) for p in b]


def test_probe_reports_ids_and_counts_only():
    rows = [{"id": "x1", "text": "a distinctive private sentence about beta"}]
    report = sample.base_rate(rows, {"beta": r"beta"})
    assert "distinctive private sentence" not in json.dumps(report)
    assert report["per_stratum"]["beta"]["n"] == 1


# ── fix 9 · page plugin field parsing and outcome rendering ─────────────────

def test_page_plugin_field_does_not_cross_newline_and_outcome_is_bounded(tmp_path, monkeypatch):
    page = tmp_path / "S-Label-9-demo.md"
    page.write_text("# demo\n")
    root = tmp_path / "labeling"
    (root / "runs").mkdir(parents=True)
    (root / "runs" / "rl-01.yaml").write_text("phase: P1\ntarget:\n  name: nested\n")
    (root / "results" / "rl-01").mkdir(parents=True)
    (root / "results" / "rl-01" / "runtime.yaml").write_text("status: complete\n")
    long_outcome = "<script>alert(1)</script> " + "x" * 400
    (root / "results" / "rl-01" / "result.yaml").write_text(f"outcome: {long_outcome}\n")

    rows = page_plugin._runs(root)
    assert rows[0]["target"] == "—"
    assert len(rows[0]["outcome"]) <= 160

    fake_job = types.SimpleNamespace(status=lambda r: {"phase": "P1"})
    monkeypatch.setattr(page_plugin, "_job_module", lambda: fake_job)
    rendered = page_plugin.render(page)
    assert "<script>alert" not in rendered
    assert "&lt;script&gt;alert" in rendered


# ── fix 10 · G0 gate before model, embedding, or sampling work ──────────────

def test_require_gate_holds_until_g0_passes(tmp_path, fake_status):
    gates = _gates()
    job = v2_job(tmp_path / "job")
    with pytest.raises(gates.GateHold):
        gates.require_gate(job, "G0")
    fake_status.update(phase="P1", g0_receipt_valid=False)
    with pytest.raises(gates.GateHold):
        gates.require_gate(job, "G0")
    fake_status.update(phase="P1", g0_receipt_valid=True)
    gates.require_gate(job, "G0")
    with pytest.raises(gates.GateHold):
        gates.require_gate(job, "G9")


def test_v2_entry_points_hold_before_g0(tmp_path, fake_status, monkeypatch):
    gates = _gates()
    job = v2_job(tmp_path / "job")
    items = tmp_path / "items.jsonl"
    write_jsonl(items, [{"id": "a1", "text": "item"}])

    sent = []

    async def spy(system_prompt, text, model):
        sent.append(text)
        return '{"label": "HIGH"}'

    monkeypatch.setitem(label.ENGINES, "spy", spy)
    with pytest.raises(gates.GateHold):
        asyncio.run(label.run_engine(job, "spy", "v01", "t", "sys",
                                     [{"anchor_idx": 1, "id": "a1", "text": "item"}],
                                     label._make_parser(LABELS), "m", 1, tmp_path / "o.jsonl"))
    assert sent == []

    def no_backend(cfg):
        raise AssertionError("embedding backend must not be built before G0")

    monkeypatch.setattr(embed, "_make_backend", no_backend)
    with pytest.raises(gates.GateHold):
        embed.cmd_embed(job, items, tmp_path / "manifest.jsonl")
    with pytest.raises(gates.GateHold):
        embed.cmd_stratify(job, items, items, tmp_path / "strat.jsonl", 1)

    with pytest.raises(gates.GateHold):
        sample.sample([{"id": "a1", "text": "beta"}], {"beta": "beta"}, {}, job_root=job)

    with pytest.raises(gates.GateHold):
        classify.cmd_train(job, tmp_path / "missing-gallery.json", [], tmp_path / "m", "logreg")
    assert fake_status["calls"] >= 5


def test_legacy_project_dir_keeps_working_with_warning(tmp_path, fake_status, capsys):
    legacy = tmp_path / "legacy"
    legacy.mkdir()
    (legacy / "config.yaml").write_text(yaml.safe_dump({"labels": {"values": LABELS}}))
    picked = sample.sample([{"id": "a1", "text": "beta"}], {"beta": "beta"}, {},
                           per_stratum=1, none_quota=0.0, job_root=legacy)
    assert [p["id"] for p in picked] == ["a1"]
    assert "legacy" in capsys.readouterr().err.lower()
    assert fake_status["calls"] == 0


def test_sample_cli_finds_job_root_above_corpus(tmp_path):
    job = v2_job(tmp_path / "job")
    corpus = job / "corpus" / "items.jsonl"
    write_jsonl(corpus, [{"id": "a1", "text": "beta"}])
    assert sample._find_job_root(corpus) == job.resolve()


# ── fix 11 · external-validity wording ──────────────────────────────────────

def test_license_verdict_never_claims_autonomy():
    raters = {f"i{k}": ["POS", "POS", "POS"] if k % 2 else ["NEG", "NEG", "NEG"] for k in range(10)}
    agent = {i: v[0] for i, v in raters.items()}
    out = json.dumps(license_.assess(agent, raters, ["POS", "NEG", "NEU"])).lower()
    assert "autonomy" not in out and "licens" not in out
    assert "external-validity diagnostic" in out
