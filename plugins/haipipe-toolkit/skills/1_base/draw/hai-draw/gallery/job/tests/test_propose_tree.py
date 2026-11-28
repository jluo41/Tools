"""propose_tree.py: Runs numbered by their type's band, `after:` set, stubs refuse to run, existing Runs untouched."""
import subprocess
import sys
from pathlib import Path

import yaml

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
import propose_tree as pt  # noqa: E402


def test_bands_order_and_stubs(tmp_path: Path):
    job = tmp_path / "j01_M-m_D-d_E-e"
    old = job / "t01_A-grpo" / "runs" / "r08_old_main"
    old.mkdir(parents=True)
    (old / "run.yaml").write_text("status: completed\n")
    plan = {"tasks": [
        {"name": "t02_A-sft", "title": "Does SFT help?", "runs": [
            {"type": "smoke", "slug": "20steps", "says": "20 steps"},
            {"type": "main", "slug": "1epoch", "says": "one epoch"},
            {"type": "sweep", "slug": "lr5e6", "says": "lr 5e-6"}]},
        {"name": "t01_A-grpo", "runs": [{"type": "repeat", "slug": "seed2", "says": "again", "after": "r08_old_main"}]}]}
    items = pt.plan_job(job, plan)
    pt.apply(items)
    runs = sorted(p.name for p in (job / "t02_A-sft" / "runs").iterdir())
    assert runs == ["r01_smoke_20steps", "r11_main_1epoch", "r21_sweep_lr5e6"]      # the order they run in
    card = yaml.safe_load((job / "t02_A-sft/runs/r11_main_1epoch/run.yaml").read_text())
    assert card["status"] == "proposed" and card["run_type"] == "main" and card["after"] == "r01_smoke_20steps"
    sweep = yaml.safe_load((job / "t02_A-sft/runs/r21_sweep_lr5e6/run.yaml").read_text())
    assert sweep["after"] == "r11_main_1epoch"
    assert "state: ◌ proposed" in (job / "t02_A-sft/t02_A-sft.md").read_text()
    rc = subprocess.run(["bash", str(job / "t02_A-sft/runs/r11_main_1epoch/r11_main_1epoch.sh")]).returncode
    assert rc == 3                                                                   # a stub never runs
    assert (old / "run.yaml").read_text() == "status: completed\n"                   # existing Runs untouched
    assert (job / "t01_A-grpo/runs/r31_repeat_seed2/run.yaml").is_file()
    assert pt.run_type("r08_old_main") == "smoke" and pt.run_type("r41_score_2048") == "score"


def test_a_task_numbered_before_the_bands_takes_the_next_number(tmp_path: Path):
    """LLMRec b01 j02 t02 holds r01-r57 from before the bands; a proposed main Run follows its last Run, r58."""
    job = tmp_path / "j02_x"
    for k in range(1, 58):
        (job / "t02_x" / "runs" / f"r{k:02d}_old").mkdir(parents=True)
    items = pt.plan_job(job, {"tasks": [{"name": "t02_x", "runs": [{"type": "main", "slug": "retry", "says": "s"}]}]})
    assert any(p.parent.name == "r58_main_retry" for k, p, _ in items if k == "run")
