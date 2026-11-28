"""The corpus tools: how the agent reads a job's corpus without holding it (b15 s42 Ⓔ).

The agent never loads the corpus into its context. It calls these over the job's frozen corpus and a set of
item vectors, and reads an item's text only through ``get``:

    stats             counts: the development items, the groups, how many have been shown
    sample            random items, from one group or all, by seed: ids only
    search            items whose text holds every word of a query: ids only
    find_neighbours   k new items near a seed set (a pool, your corrections), ranked by ``rank_by``: ids and scores
    get               one or more items' text; each call is logged and held to its step's reading budget

Three guards live here, not in the agent:

1. Only development items are ever returned. Every tool reads the job's ``corpus/items.jsonl`` and keeps
   ``population_status: eligible`` rows; the sealed final exam is not in that file, and an item id that is
   not eligible is refused as a seed, so S can never be reached, even when the vectors hold it.
2. ``get`` appends every text it returns to ``exposure/group_examples.jsonl`` (the log the Embedding view
   and the item table share), so a later round knows what a person or the agent has already read.
3. ``get`` takes a step name and its budget (c_ask, c_pick, c_learn): once the log holds that many items for
   the step, it refuses and the agent works on ids, counts and scores alone.

``find_neighbours`` ranks by ``nearest`` today: the best cosine between a candidate and any seed item. The
other ways to rank (``confidence``, ``disagree``, ``classifier``, ``value``) need a round's panel labels or
your gold; until those exist they refuse with what is missing.

Vectors come from a folder holding ``rows.jsonl`` (``item_id`` per row, in row order) and ``vectors.npy``:
the job's own ``cache/embeddings/<version>/`` or an items Task's embedding Run (its heavy folder); the groups
come from that Run's ``map.json``, read where it lies.

    python corpus_tools.py stats --job-root <labeling/> [--map <map.json>]
    python corpus_tools.py sample --job-root <labeling/> --n 5 --seed 1 [--group 3 --map <map.json>]
    python corpus_tools.py search --job-root <labeling/> --query "invest money" --k 10
    python corpus_tools.py find-neighbours --job-root <labeling/> --vectors <folder> --seed-ids a,b --k 20
    python corpus_tools.py get --job-root <labeling/> --ids a,b --step talk-pass-2 --budget 4 --human-id <id>
"""
from __future__ import annotations

import argparse
import importlib.util
import json
import random
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent


_SPEC = importlib.util.spec_from_file_location("subjective_label_embedding_for_corpus_tools",
                                               HERE / "embedding_build.py")
emb = importlib.util.module_from_spec(_SPEC)
assert _SPEC.loader is not None
_SPEC.loader.exec_module(emb)
cal, job = emb.cal, emb.job

RANK_BY = ("nearest", "confidence", "disagree", "classifier", "value")
NEEDS = {"confidence": "the panel's sealed labels (run a round's LABEL first)",
         "disagree": "the panel's sealed labels (run a round's LABEL first)",
         "classifier": "your gold (close a round first)",
         "value": "the panel's labels and your gold (close a round first)"}


class CorpusToolRefused(RuntimeError):
    """A call the guards refuse: a sealed or unknown item, a spent budget, a way to rank not ready yet."""


def _eligible(job_root: Path) -> dict[str, dict]:
    return {str(r["item_id"]): r for r in cal._corpus_rows(Path(job_root))
            if r.get("population_status") == "eligible" and r.get("item_id") is not None}


def _fields(job_root: Path) -> tuple[str, str]:
    corpus = job.load_mapping(Path(job_root) / "config.yaml").get("corpus") or {}
    return str(corpus.get("text_field") or "text"), str(corpus.get("context_field") or "context_prev")


def _vectors(folder: Path, keep: set[str]):
    """(ids, unit vectors) for the eligible items the folder holds; every other row is dropped."""
    import numpy as np
    folder = Path(folder)
    rows = cal._read_jsonl(folder / "rows.jsonl")
    vectors = np.load(folder / "vectors.npy").astype("float32")
    if len(rows) != len(vectors):
        raise CorpusToolRefused(f"{folder}: rows.jsonl has {len(rows)} rows, vectors.npy {len(vectors)}")
    index = [i for i, r in enumerate(rows) if str(r.get("item_id")) in keep]
    ids = [str(rows[i]["item_id"]) for i in index]
    v = vectors[index]
    norms = np.linalg.norm(v, axis=1, keepdims=True)
    return ids, v / np.where(norms == 0, 1, norms)


def _groups(where: Path | None) -> dict[str, int]:
    """item -> group, from a map file (map.json or map.jsonl) or a folder holding one, when there is one."""
    if where is None:
        return {}
    where = Path(where)
    for f in ([where] if where.is_file() else [where / "map.json", where / "map.jsonl"]):
        name = f.name
        if f.is_file():
            rows = json.loads(f.read_text(encoding="utf-8")) if name.endswith(".json") else cal._read_jsonl(f)
            return {str(r["item_id"]): int(r["group"]) for r in rows if "group" in r}
    return {}


def stats(job_root: Path, groups_map: Path | None = None) -> dict:
    items = _eligible(job_root)
    groups: dict[int, int] = {}
    for item_id, g in _groups(groups_map).items():
        if item_id in items:
            groups[g] = groups.get(g, 0) + 1
    seen = emb.seen_items(Path(job_root))
    return {"items": len(items), "groups": dict(sorted(groups.items())),
            "shown": len([i for i in seen if i in items])}


def sample(job_root: Path, n: int, seed: int, group: int | None = None, groups_map: Path | None = None) -> list[str]:
    items = sorted(_eligible(job_root))
    if group is not None:
        g = _groups(groups_map)
        if not g:
            raise CorpusToolRefused("a group needs --map, the embedding's map.json")
        items = [i for i in items if g.get(i) == group]
    return sorted(random.Random(seed).sample(items, min(int(n), len(items))))


def search(job_root: Path, query: str, k: int = 20) -> list[str]:
    """Items whose context or text holds every word of the query, by keyword; ids only, no text."""
    text_field, context_field = _fields(job_root)
    words = [w for w in re.findall(r"\w+", query.lower()) if w]
    hits = [i for i, r in _eligible(job_root).items()
            if words and all(w in f"{r.get(context_field) or ''} {r.get(text_field) or ''}".lower() for w in words)]
    return sorted(hits)[:int(k)]


def find_neighbours(job_root: Path, seed: list[str], k: int, *, vectors: Path, rank_by: str = "nearest",
                    exclude: list[str] = ()) -> list[dict]:
    """k development items near the seed set, best first: each with its score and its nearest seed item."""
    if rank_by not in RANK_BY:
        raise CorpusToolRefused(f"rank_by is one of {', '.join(RANK_BY)}")
    if rank_by != "nearest":
        raise CorpusToolRefused(f"rank_by={rank_by} needs {NEEDS[rank_by]}")
    items = _eligible(job_root)
    seed = [str(s) for s in seed]
    outside = [s for s in seed if s not in items]
    if outside:
        raise CorpusToolRefused(f"not development items, so not a seed: {', '.join(outside)}")
    ids, v = _vectors(vectors, set(items))
    at = {i: n for n, i in enumerate(ids)}
    missing = [s for s in seed if s not in at]
    if missing:
        raise CorpusToolRefused(f"no vector for: {', '.join(missing)}")
    sims = v @ v[[at[s] for s in seed]].T                      # cosine to each seed item
    best, which = sims.max(axis=1), sims.argmax(axis=1)
    skip = set(seed) | {str(x) for x in exclude}
    ranked = sorted((i for i in range(len(ids)) if ids[i] not in skip), key=lambda i: (-float(best[i]), ids[i]))
    return [{"item_id": ids[i], "score": round(float(best[i]), 4), "nearest_seed": seed[int(which[i])]}
            for i in ranked[:int(k)]]


def _spent(job_root: Path, step: str) -> set[str]:
    where = f"corpus tools · {step}"
    return {str(i) for line in cal._read_jsonl(Path(job_root) / emb.EXPOSURE_LOG)
            if line.get("where") == where for i in line.get("item_ids") or []}


def get(job_root: Path, item_ids: list[str], *, step: str, budget: int, human_id: str | None = None,
        channel: str = "cli") -> list[dict]:
    """The items' text, logged; refused when it would take the step past its reading budget."""
    job_root = Path(job_root).resolve()
    if job.status(job_root).get("hold"):
        raise CorpusToolRefused("this job is read-only (HOLD), so showing item text cannot be recorded")
    items = _eligible(job_root)
    item_ids = [str(i) for i in item_ids]
    outside = [i for i in item_ids if i not in items]
    if outside:
        raise CorpusToolRefused(f"not development items: {', '.join(outside)}")
    waiting = emb.waiting_items(job_root)
    held = [i for i in item_ids if i in waiting]
    if held:
        raise CorpusToolRefused(f"waiting in a round, so read on the Label screen: {', '.join(held)}")
    spent = _spent(job_root, step)
    new = [i for i in item_ids if i not in spent]
    if len(spent) + len(new) > int(budget):
        raise CorpusToolRefused(f"step {step} has read {len(spent)} of its {budget}; {len(new)} more would pass it")
    text_field, context_field = _fields(job_root)
    if new:
        emb._record_exposure(job_root, human_id=human_id, channel=channel, where=f"corpus tools · {step}",
                             version="items", item_ids=new)
    return [{"item_id": i, "context": str(items[i].get(context_field) or ""),
             "text": str(items[i].get(text_field) or "")} for i in item_ids]


def _ids(s: str) -> list[str]:
    return [x.strip() for x in s.split(",") if x.strip()]


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="the corpus tools: read a labeling job's corpus by ids and budgets")
    sub = ap.add_subparsers(dest="cmd", required=True)
    for name in ("stats", "sample", "search", "find-neighbours", "get"):
        p = sub.add_parser(name)
        p.add_argument("--job-root", type=Path, required=True)
        if name == "find-neighbours":
            p.add_argument("--vectors", type=Path, required=True)
        if name in ("stats", "sample"):
            p.add_argument("--map", type=Path, help="the embedding's map.json: each item's group")
        if name == "sample":
            p.add_argument("--n", type=int, required=True)
            p.add_argument("--seed", type=int, required=True)
            p.add_argument("--group", type=int)
        if name == "search":
            p.add_argument("--query", required=True)
            p.add_argument("--k", type=int, default=20)
        if name == "find-neighbours":
            p.add_argument("--seed-ids", required=True)
            p.add_argument("--k", type=int, default=20)
            p.add_argument("--rank-by", default="nearest", choices=RANK_BY)
            p.add_argument("--exclude", default="")
        if name == "get":
            p.add_argument("--ids", required=True)
            p.add_argument("--step", required=True)
            p.add_argument("--budget", type=int, required=True)
            p.add_argument("--human-id")
    a = ap.parse_args(argv)
    try:
        if a.cmd == "stats":
            out = stats(a.job_root, a.map)
        elif a.cmd == "sample":
            out = sample(a.job_root, a.n, a.seed, a.group, a.map)
        elif a.cmd == "search":
            out = search(a.job_root, a.query, a.k)
        elif a.cmd == "find-neighbours":
            out = find_neighbours(a.job_root, _ids(a.seed_ids), a.k, vectors=a.vectors, rank_by=a.rank_by,
                                  exclude=_ids(a.exclude))
        else:
            out = get(a.job_root, _ids(a.ids), step=a.step, budget=a.budget, human_id=a.human_id)
    except CorpusToolRefused as error:
        print(json.dumps({"refused": str(error)}, ensure_ascii=False))
        return 2
    print(json.dumps(out, ensure_ascii=False, indent=1))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
