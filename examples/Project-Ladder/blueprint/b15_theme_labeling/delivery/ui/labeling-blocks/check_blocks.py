"""Guard independent Block ownership, generated artifacts and embedded-only navigation."""
from pathlib import Path
import json
import re
from build_blocks import BLOCKS, EXAMPLES, HERE, fragment


def check():
    ids = set()
    for name, _ in BLOCKS:
        block = EXAMPLES / name
        face = (block / "board.md").read_text()
        assert "board-kind: labeling-board" in face
        assert "preview-only: true" in face
        model = json.loads((block / "delivery/ui/model.json").read_text())
        assert model["blockId"] == name and name not in ids
        ids.add(name)
        html = (block / "delivery/ui/block.html").read_text()
        assert html == fragment(model), name + " stale generation"
        assert re.search(r'<h1>' + re.escape(model["name"]) + r'</h1>', html)
        assert not re.search(r'<(?:a|iframe)\b|\bhref\s*=|\bsrc\s*=', html)
        assert not re.search(r'<(?:html|head|body)\b|<!doctype', html, re.I)
        assert not re.search(r'__BLOCK_[A-Z]+__', html)
        assert len(html.encode()) < 1_000_000
        assert not any(x in model for x in ["baseline", "baselineLabel", "baselineGroup", "topic"])
        assert model["example"] == "synthetic"
        for job in model["jobs"]:
            assert job["name"] and job["tasks"]
            assert all(not re.match(r'^[tjs]\d', t["name"], re.I) for t in job["tasks"])
            if model["kind"] == "scale":
                assert dict(job["inputs"])["Guideline"] == "guideline-v2"
                assert not job["complete"] or job["signed"] and job["qualified"]
    js = (HERE / "block-preview.js").read_text()
    assert not re.search(r'window\.open\s*\(|location\.|history\.|document\.title|\bfetch\s*\(|XMLHttpRequest|WebSocket', js)
    assert "row.hidden=!t" in js
    assert not any(EXAMPLES.parent.joinpath("blueprint/b15_theme_labeling", p).exists() for p in (
        "s11-itemization-job-preview", "s12-guideline-job-preview", "s14-scale-job-preview"))
    print("PASS: 3 independent Block owners; matching embedded previews; no child page routes or navigation")


if __name__ == "__main__":
    check()
