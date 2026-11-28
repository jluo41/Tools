"""The corpus tools (b15 s42 Ⓔ): ids and scores out, text only through get, S never reached."""
from __future__ import annotations

import importlib.util
import json
from pathlib import Path

import numpy as np
import pytest

HERE = Path(__file__).resolve().parent


def _load(name: str, file: str):
    spec = importlib.util.spec_from_file_location(name, HERE / file)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


calib_test = _load("sl_calibration_test_for_corpus_tools", "test_calibration.py")
tools = _load("sl_corpus_tools_test", "corpus_tools.py")


def _job(tmp_path):
    root, _ = calib_test.confirmed_job(tmp_path)
    rows = [json.loads(line) for line in (tmp_path / "items.jsonl").read_text().splitlines()]
    ids = [r["item_id"] for r in rows]                         # all 12, the sealed 4 included
    vec = tmp_path / "vectors"
    vec.mkdir()
    angles = np.linspace(0, np.pi / 2, len(ids))              # item i sits at angle i: neighbours are i±1
    np.save(vec / "vectors.npy", np.stack([np.cos(angles), np.sin(angles)], axis=1).astype("float32"))
    (vec / "rows.jsonl").write_text("".join(json.dumps({"row": n, "item_id": i}) + "\n" for n, i in enumerate(ids)))
    (vec / "map.json").write_text(json.dumps([{"item_id": i, "group": n % 2} for n, i in enumerate(ids)]))
    sealed = calib_test.sealed_ids(root)
    return root, vec, sealed, [i for i in ids if i not in sealed]


def test_find_neighbours_ranks_the_nearest_and_never_reaches_the_sealed(tmp_path):
    root, vec, sealed, dev = _job(tmp_path)
    out = tools.find_neighbours(root, [dev[0]], 20, vectors=vec)
    assert [o["item_id"] for o in out] == dev[1:]               # every other development item, nearest first
    assert not sealed & {o["item_id"] for o in out}
    assert [o["score"] for o in out] == sorted((o["score"] for o in out), reverse=True)
    two = tools.find_neighbours(root, [dev[0], dev[-1]], 2, vectors=vec, exclude=[dev[1]])
    assert {o["nearest_seed"] for o in two} <= {dev[0], dev[-1]} and dev[1] not in [o["item_id"] for o in two]


def test_a_sealed_seed_and_a_rank_not_ready_are_refused(tmp_path):
    root, vec, sealed, dev = _job(tmp_path)
    with pytest.raises(tools.CorpusToolRefused, match="not development items"):
        tools.find_neighbours(root, [sorted(sealed)[0]], 3, vectors=vec)
    with pytest.raises(tools.CorpusToolRefused, match="panel"):
        tools.find_neighbours(root, [dev[0]], 3, vectors=vec, rank_by="disagree")


def test_get_logs_each_read_and_holds_the_step_to_its_budget(tmp_path):
    root, vec, sealed, dev = _job(tmp_path)
    got = tools.get(root, dev[:2], step="talk-pass-1", budget=3, human_id="JL")
    assert [g["item_id"] for g in got] == dev[:2] and all(g["text"].startswith("response") for g in got)
    tools.get(root, dev[:2], step="talk-pass-1", budget=3)    # read again: not counted twice
    with pytest.raises(tools.CorpusToolRefused, match="read 2 of its 3"):
        tools.get(root, dev[2:4], step="talk-pass-1", budget=3)
    log = [json.loads(line) for line in (root / "exposure" / "group_examples.jsonl").open()]
    assert [e["where"] for e in log] == ["corpus tools · talk-pass-1"] and log[0]["item_ids"] == dev[:2]
    with pytest.raises(tools.CorpusToolRefused):
        tools.get(root, [sorted(sealed)[0]], step="x", budget=5)


def test_stats_sample_and_search_return_ids_only(tmp_path):
    root, vec, sealed, dev = _job(tmp_path)
    s = tools.stats(root, vec / "map.json")
    assert s["items"] == len(dev) and sum(s["groups"].values()) == len(dev) and s["shown"] == 0
    a = tools.sample(root, 3, seed=1, group=0, groups_map=vec / "map.json")
    assert a == tools.sample(root, 3, seed=1, group=0, groups_map=vec / "map.json") and set(a) <= set(dev)
    assert tools.search(root, "response", 50) == sorted(dev)
