"""delivery_publish.py: [publish] copies only into a round's clean/ (ScalingGlucose, Pp-AgreeableRx 261122)."""
import os
import re
import shutil
import sys
from datetime import datetime
from pathlib import Path

SCRIPTS = Path(__file__).resolve().parents[1] / "scripts"


def run(tmp_path, dest, files):
    (tmp_path / "env.sh").write_text("")
    here = tmp_path / "delivery"; here.mkdir(exist_ok=True)
    (here / "m.pdf").write_bytes(b"%PDF")
    ns = {"CFG": {"publish": {"dir": str(dest), "files": files}}, "OUT": {"pdf": "m.pdf"}, "HERE": here,
          "ENGINE_DIR": SCRIPTS, "BUILD_WARNINGS": [], "rel": lambda p: here / p, "_doc_parts": lambda p: p.read_bytes(),
          "re": re, "os": os, "sys": sys, "shutil": shutil, "datetime": datetime, "Path": Path}
    exec((SCRIPTS / "delivery_publish.py").read_text(encoding="utf-8"), ns)
    return ns["publish"]({}), ns["BUILD_WARNINGS"]


def test_a_flat_folder_gets_nothing(tmp_path):
    flat = tmp_path / "GlucoseScalingLaw" / "v1118"; flat.mkdir(parents=True)
    done, warn = run(tmp_path, flat, {"pdf": "Paper-X-draft.pdf"})
    assert done == {} and not list(flat.iterdir()) and "adopt-round" in warn[0]


def test_a_rounds_clean_folder_gets_numbered_files_and_its_marker(tmp_path):
    clean = tmp_path / "Round1-v1118" / "clean"; clean.mkdir(parents=True)
    done, warn = run(tmp_path, clean, {"pdf": "1-Paper-X-v1118-manuscript-clean.pdf"})
    assert list(done) == ["1-Paper-X-v1118-manuscript-clean.pdf"] and not warn
    assert len(list(clean.glob("last-update-*.txt"))) == 1
    _, warn = run(tmp_path, clean, {"pdf": "Paper-X.pdf"})
    assert "N-<Name>-vMMDD-<kind>" in warn[0]
