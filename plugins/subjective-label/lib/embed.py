"""Embedding utilities for the subjective-label plugin.

Invoked by the `embedder` agent via Bash. Other agents (Prober, Gallery Keeper,
Labeler Panel, Validator) do not call this directly — they always go through
the embedder agent.

CLI subcommands
    embed      embed texts in batch, write cached vectors
    index      build a vector index from gallery entries
    nearest    k-NN query against an index
    cluster    cluster a set of texts
    stratify   stratified sample by cluster

All subcommands take a --project-dir to scope caching.

Config source: {project_dir}/config.yaml → embedding section
    model: "sentence-transformers/all-MiniLM-L6-v2"
    backend: "sentence-transformers"   # or "openai", "hf-api"
    device: "cpu"                      # or "mps", "cuda"
    dim: 384
    index: "faiss-flat"                # or "faiss-ivf" for > 100K items

Cache layout (per project)
    {project_dir}/cache/embeddings/
        vectors/{sha1}.npy             # per-text vector, keyed by hash(text + model)
        manifest.jsonl                 # append-only: id, text_sha1, model, created_at
        gallery_index.faiss            # FAISS index over current gallery vectors
        gallery_index.meta.json        # id -> gallery entry lookup for the index
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import sys
from pathlib import Path


# ── deferred imports so the CLI help works without heavy deps ───────────────

def _load_yaml(path: Path) -> dict:
    import yaml  # noqa: PLC0415
    return yaml.safe_load(path.read_text(encoding="utf-8"))


def _sha1(s: str) -> str:
    return hashlib.sha1(s.encode("utf-8")).hexdigest()


def _cache_root(project_dir: Path) -> Path:
    root = project_dir / "cache" / "embeddings"
    (root / "vectors").mkdir(parents=True, exist_ok=True)
    return root


def _read_config(project_dir: Path) -> dict:
    cfg_path = project_dir / "config.yaml"
    if not cfg_path.exists():
        return {"model": "sentence-transformers/all-MiniLM-L6-v2",
                "backend": "sentence-transformers",
                "device": "cpu",
                "dim": 384,
                "index": "faiss-flat"}
    cfg = _load_yaml(cfg_path)
    return cfg.get("embedding", {}) or {}


# ── backends ────────────────────────────────────────────────────────────────

class _STBackend:
    """sentence-transformers backend. Local inference, free."""
    def __init__(self, model_name: str, device: str = "cpu"):
        from sentence_transformers import SentenceTransformer  # noqa: PLC0415
        self.model = SentenceTransformer(model_name, device=device)

    def encode(self, texts: list[str]):
        import numpy as np  # noqa: PLC0415
        vecs = self.model.encode(texts, convert_to_numpy=True, normalize_embeddings=True)
        return vecs.astype(np.float32)


class _OpenAIBackend:
    """OpenAI embeddings API. Remote, paid, best quality."""
    def __init__(self, model_name: str):
        from openai import OpenAI  # noqa: PLC0415
        self.client = OpenAI()
        self.model_name = model_name

    def encode(self, texts: list[str]):
        import numpy as np  # noqa: PLC0415
        # batch in chunks of 100
        vecs = []
        for i in range(0, len(texts), 100):
            chunk = texts[i : i + 100]
            resp = self.client.embeddings.create(model=self.model_name, input=chunk)
            vecs.extend([d.embedding for d in resp.data])
        arr = np.asarray(vecs, dtype="float32")
        # normalize for cosine
        norms = (arr * arr).sum(axis=1, keepdims=True) ** 0.5
        return arr / (norms + 1e-12)


def _make_backend(cfg: dict):
    backend = cfg.get("backend", "sentence-transformers")
    model = cfg.get("model", "sentence-transformers/all-MiniLM-L6-v2")
    if backend == "sentence-transformers":
        return _STBackend(model, device=cfg.get("device", "cpu"))
    if backend == "openai":
        return _OpenAIBackend(model)
    raise ValueError(f"unknown backend: {backend}")


# ── commands ────────────────────────────────────────────────────────────────

def cmd_embed(project_dir: Path, input_jsonl: Path, output_path: Path) -> None:
    """Read {id, text} jsonl; write {id, vector_path, sha1} manifest + cached vectors.

    Reuses cached vectors when text hash + model match.
    """
    import numpy as np  # noqa: PLC0415

    cfg = _read_config(project_dir)
    cache = _cache_root(project_dir)
    vec_dir = cache / "vectors"
    model_tag = cfg.get("model", "st-default")

    items = []
    for line in input_jsonl.read_text(encoding="utf-8").splitlines():
        if line.strip():
            items.append(json.loads(line))

    texts_to_encode = []
    idx_to_encode = []
    manifest = []

    for i, it in enumerate(items):
        h = _sha1(f"{model_tag}::{it['text']}")
        vec_path = vec_dir / f"{h}.npy"
        if vec_path.exists():
            manifest.append({"id": it["id"], "sha1": h, "cached": True})
        else:
            texts_to_encode.append(it["text"])
            idx_to_encode.append((i, h, vec_path))
            manifest.append({"id": it["id"], "sha1": h, "cached": False})

    if texts_to_encode:
        backend = _make_backend(cfg)
        vecs = backend.encode(texts_to_encode)
        for (_, h, vec_path), v in zip(idx_to_encode, vecs):
            np.save(vec_path, v)

    # Write manifest
    output_path.write_text(
        "\n".join(json.dumps(m) for m in manifest) + "\n",
        encoding="utf-8",
    )
    print(f"embedded: {len(items)} items ({len(texts_to_encode)} new, {len(items) - len(texts_to_encode)} cached)")


def cmd_index(project_dir: Path, gallery_jsonl: Path) -> None:
    """Build a FAISS index over the current gallery vectors."""
    import faiss  # noqa: PLC0415
    import numpy as np  # noqa: PLC0415

    cfg = _read_config(project_dir)
    cache = _cache_root(project_dir)
    vec_dir = cache / "vectors"
    model_tag = cfg.get("model", "st-default")
    dim = int(cfg.get("dim", 384))

    gallery = json.loads(gallery_jsonl.read_text(encoding="utf-8"))
    if not isinstance(gallery, list):
        raise ValueError("gallery.json must be a JSON array")

    # Ensure vectors exist for every gallery entry
    vecs = []
    ids = []
    missing = []
    for entry in gallery:
        h = _sha1(f"{model_tag}::{entry['text']}")
        p = vec_dir / f"{h}.npy"
        if not p.exists():
            missing.append(entry["id"])
            continue
        vecs.append(np.load(p))
        ids.append(entry["id"])

    if missing:
        print(f"WARNING: {len(missing)} gallery entries lack cached vectors. Run `embed` first.", file=sys.stderr)

    if not vecs:
        print("no vectors to index", file=sys.stderr)
        return

    mat = np.vstack(vecs).astype("float32")
    # normalized vectors + inner product = cosine
    index_kind = cfg.get("index", "faiss-flat")
    if index_kind == "faiss-ivf" and len(vecs) >= 256:
        nlist = min(64, len(vecs) // 4)
        quant = faiss.IndexFlatIP(dim)
        index = faiss.IndexIVFFlat(quant, dim, nlist, faiss.METRIC_INNER_PRODUCT)
        index.train(mat)
        index.add(mat)
    else:
        index = faiss.IndexFlatIP(dim)
        index.add(mat)

    faiss.write_index(index, str(cache / "gallery_index.faiss"))
    (cache / "gallery_index.meta.json").write_text(
        json.dumps({"ids": ids, "model": model_tag, "dim": dim, "kind": index_kind}, indent=2),
        encoding="utf-8",
    )
    print(f"index built: {len(ids)} entries ({index_kind})")


def cmd_nearest(project_dir: Path, query_jsonl: Path, output_jsonl: Path, k: int) -> None:
    """For each query text, find k-nearest gallery entries."""
    import faiss  # noqa: PLC0415
    import numpy as np  # noqa: PLC0415

    cfg = _read_config(project_dir)
    cache = _cache_root(project_dir)
    vec_dir = cache / "vectors"
    model_tag = cfg.get("model", "st-default")

    meta = json.loads((cache / "gallery_index.meta.json").read_text(encoding="utf-8"))
    index = faiss.read_index(str(cache / "gallery_index.faiss"))

    queries = []
    for line in query_jsonl.read_text(encoding="utf-8").splitlines():
        if line.strip():
            queries.append(json.loads(line))

    # Load/encode query vectors
    q_vecs = []
    to_encode: list[tuple[int, str]] = []
    q_paths = []
    for i, q in enumerate(queries):
        h = _sha1(f"{model_tag}::{q['text']}")
        p = vec_dir / f"{h}.npy"
        q_paths.append(p)
        if p.exists():
            q_vecs.append(np.load(p))
        else:
            q_vecs.append(None)
            to_encode.append((i, q["text"]))

    if to_encode:
        backend = _make_backend(cfg)
        texts = [t for (_, t) in to_encode]
        new = backend.encode(texts)
        for (i, _), v in zip(to_encode, new):
            np.save(q_paths[i], v)
            q_vecs[i] = v

    mat = np.vstack(q_vecs).astype("float32")
    sims, idxs = index.search(mat, k)

    lines = []
    for i, q in enumerate(queries):
        neighbors = [
            {"gallery_id": meta["ids"][idxs[i][j]], "sim": float(sims[i][j])}
            for j in range(k) if idxs[i][j] >= 0
        ]
        lines.append(json.dumps({"query_id": q["id"], "neighbors": neighbors}))

    output_jsonl.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"nearest: {len(queries)} queries, k={k}")


def cmd_cluster(project_dir: Path, input_jsonl: Path, output_jsonl: Path, n_clusters: int) -> None:
    """K-Means cluster (fast, no extra deps besides sklearn)."""
    import numpy as np  # noqa: PLC0415
    from sklearn.cluster import KMeans  # noqa: PLC0415

    cfg = _read_config(project_dir)
    cache = _cache_root(project_dir)
    vec_dir = cache / "vectors"
    model_tag = cfg.get("model", "st-default")

    items = []
    vecs = []
    for line in input_jsonl.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        it = json.loads(line)
        h = _sha1(f"{model_tag}::{it['text']}")
        p = vec_dir / f"{h}.npy"
        if not p.exists():
            raise FileNotFoundError(f"vector missing for {it['id']} — run `embed` first")
        items.append(it)
        vecs.append(np.load(p))

    mat = np.vstack(vecs)
    km = KMeans(n_clusters=min(n_clusters, len(items)), n_init=10, random_state=0)
    labels = km.fit_predict(mat)

    lines = []
    for it, lab in zip(items, labels):
        lines.append(json.dumps({"id": it["id"], "cluster": int(lab)}))
    output_jsonl.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"clustered: {len(items)} items into {n_clusters} clusters")


def cmd_stratify(project_dir: Path, input_jsonl: Path, cluster_jsonl: Path, output_jsonl: Path, n_per_cluster: int) -> None:
    """Given a cluster assignment, stratified-sample n items per cluster."""
    import random  # noqa: PLC0415

    cluster_map = {}
    for line in cluster_jsonl.read_text(encoding="utf-8").splitlines():
        if line.strip():
            r = json.loads(line)
            cluster_map[r["id"]] = r["cluster"]

    items_by_cluster: dict[int, list] = {}
    for line in input_jsonl.read_text(encoding="utf-8").splitlines():
        if line.strip():
            it = json.loads(line)
            c = cluster_map.get(it["id"])
            if c is not None:
                items_by_cluster.setdefault(c, []).append(it)

    rng = random.Random(0)
    sampled = []
    for c, lst in items_by_cluster.items():
        rng.shuffle(lst)
        sampled.extend(lst[:n_per_cluster])

    output_jsonl.write_text("\n".join(json.dumps(it) for it in sampled) + "\n", encoding="utf-8")
    print(f"stratified: {len(sampled)} items from {len(items_by_cluster)} clusters")


# ── entrypoint ──────────────────────────────────────────────────────────────

def main() -> None:
    p = argparse.ArgumentParser(description="subjective-label embedding utilities")
    p.add_argument("--project-dir", type=Path, required=True)
    sub = p.add_subparsers(dest="cmd", required=True)

    pe = sub.add_parser("embed")
    pe.add_argument("--input", type=Path, required=True, help="jsonl of {id, text}")
    pe.add_argument("--output", type=Path, required=True, help="jsonl manifest output")

    pi = sub.add_parser("index")
    pi.add_argument("--gallery", type=Path, required=True, help="gallery.json path")

    pn = sub.add_parser("nearest")
    pn.add_argument("--query", type=Path, required=True, help="jsonl of {id, text}")
    pn.add_argument("--output", type=Path, required=True)
    pn.add_argument("--k", type=int, default=5)

    pc = sub.add_parser("cluster")
    pc.add_argument("--input", type=Path, required=True)
    pc.add_argument("--output", type=Path, required=True)
    pc.add_argument("--n-clusters", type=int, default=10)

    ps = sub.add_parser("stratify")
    ps.add_argument("--input", type=Path, required=True)
    ps.add_argument("--clusters", type=Path, required=True)
    ps.add_argument("--output", type=Path, required=True)
    ps.add_argument("--n-per-cluster", type=int, default=3)

    args = p.parse_args()

    if args.cmd == "embed":
        cmd_embed(args.project_dir, args.input, args.output)
    elif args.cmd == "index":
        cmd_index(args.project_dir, args.gallery)
    elif args.cmd == "nearest":
        cmd_nearest(args.project_dir, args.query, args.output, args.k)
    elif args.cmd == "cluster":
        cmd_cluster(args.project_dir, args.input, args.output, args.n_clusters)
    elif args.cmd == "stratify":
        cmd_stratify(args.project_dir, args.input, args.clusters, args.output, args.n_per_cluster)


if __name__ == "__main__":
    main()
