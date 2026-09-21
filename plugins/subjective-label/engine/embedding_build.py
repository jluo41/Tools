#!/usr/bin/env python3
"""P0 ``embedding-build``: one corpus × one embedder, written as one Run.

This is the optional P0 step 5 of ``label-building-workflow``.  It embeds every
development item (``population_status: eligible``) once, never a sealed item,
and writes a versioned namespace:

    cache/embeddings/<version>/
        manifest.json    model, encoder steps, preprocessing, example, population, map, groups, checksums
        vectors.npy      float32, one L2-normalised row per development item
        rows.jsonl       row, item_id, text_hash, input_sha256, tokens, cut
        map.jsonl        item_id, x, y, group   (2D map for the Data Space)
        groups.json      k-means groups: size and keywords, no item text

Embeddings are representation only (``ref/ref-embeddings.md``): a group, a
neighbour, or a map position never sets a label, a region, or gold.  So this
step is not gated on G0; it refuses only a HOLD job or a job whose P0 files do
not verify.  The embedder choice lives on the Run Ticket, so ``config.yaml``
(a P0 authority file) is never edited.

The person choosing the embedder picks from ``CATALOG`` (open-weight models that
run locally through sentence-transformers); the Board's write door accepts only
catalog ids and starts the build in the background.  Each model gets its own
folder, so building one never changes another.

CLI
    build    --job-root <labeling> --started-by <person> [--model ID] [--groups K] [--seed 0] ...
    status   --job-root <labeling>      built, building, failed, or not built, per catalog model
    catalog                             the models a person may choose
    show     --job-root <labeling>      newest manifest
    examples --job-root <labeling> --version V --group N --human-id H
                                        a group's most typical items with text; logged in exposure/group_examples.jsonl
"""

from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
import os
import re
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Callable

HERE = Path(__file__).resolve().parent
_SPEC = importlib.util.spec_from_file_location("subjective_label_calibration_for_embedding", HERE / "calibration.py")
cal = importlib.util.module_from_spec(_SPEC)
assert _SPEC.loader is not None
_SPEC.loader.exec_module(cal)
job = cal.job

SCHEMA = "subjective-label-embedding/v1"
DEFAULT_MODEL = "sentence-transformers/all-MiniLM-L6-v2"
PREPROCESSING = "text_then_context/v1"
EXAMPLE_INPUT = "I'm sorry, but I can't help with that."  # made up; never a corpus item
BUILD_MARKER = ".building.json"
BUILD_LOG = "build.log"
EXPOSURE_LOG = "exposure/group_examples.jsonl"  # who saw which item text outside the Label screen

# Open-weight embedders a person may choose.  Sizes and licenses are the model
# cards' (checked 2026-09-16); `max_tokens` is what sentence-transformers loads; `dim` and `max_tokens` are recorded again from the
# loaded model at build time, so the manifest never trusts this table.
CATALOG = (
    {"id": "Qwen/Qwen3-Embedding-0.6B", "maker": "Alibaba Qwen", "params": "0.6B", "dim": 1024,
     "max_tokens": 32768, "license": "Apache-2.0", "download": "1.2 GB", "recommended": True,
     "instruct": "Instruct: {task}\nQuery:",
     "note": "Best for its size; reads a whole conversation."},
    {"id": "BAAI/bge-m3", "maker": "BAAI", "params": "568M", "dim": 1024, "max_tokens": 8192,
     "license": "MIT", "download": "2.3 GB",
     "note": "Widely used and solid; reads many languages."},
    {"id": "intfloat/multilingual-e5-large-instruct", "maker": "Microsoft (intfloat)", "params": "560M",
     "dim": 1024, "max_tokens": 512, "license": "MIT", "download": "1.1 GB",
     "instruct": "Instruct: {task}\nQuery: ",
     "note": "Good mid-size model; reads about 400 words at most."},
    {"id": "Qwen/Qwen3-Embedding-4B", "maker": "Alibaba Qwen", "params": "4B", "dim": 2560,
     "max_tokens": 40960, "license": "Apache-2.0", "download": "8.1 GB", "dtype": "bfloat16",
     "instruct": "Instruct: {task}\nQuery:",
     "note": "Better, several times slower."},
    {"id": "Qwen/Qwen3-Embedding-8B", "maker": "Alibaba Qwen", "params": "8B", "dim": 4096,
     "max_tokens": 40960, "license": "Apache-2.0", "download": "15.2 GB", "dtype": "bfloat16",
     "instruct": "Instruct: {task}\nQuery:",
     "note": "Best on public tests; the slowest here."},
    {"id": "sentence-transformers/all-mpnet-base-v2", "maker": "sentence-transformers", "params": "110M",
     "dim": 768, "max_tokens": 384, "license": "Apache-2.0", "download": "0.4 GB",
     "note": "Small and fast."},
    {"id": "sentence-transformers/all-MiniLM-L6-v2", "maker": "sentence-transformers", "params": "22M",
     "dim": 384, "max_tokens": 256, "license": "Apache-2.0", "download": "0.1 GB",
     "note": "Tiny and fastest; cuts long conversations short."},
)


def catalog_entry(model: str) -> dict | None:
    return next((dict(entry) for entry in CATALOG if entry["id"] == model), None)


def resolve_device(device: str) -> str:
    if device != "auto":
        return device
    try:
        import torch  # noqa: PLC0415
    except ImportError:
        return "cpu"
    if torch.cuda.is_available():
        return "cuda"
    if getattr(torch.backends, "mps", None) and torch.backends.mps.is_available():
        return "mps"
    return "cpu"


GROUP_METHOD = "kmeans-cosine"

# What a person may set for one build.  Each distinct combination is its own
# folder and its own Run; the defaults keep the plain model name.
INPUT_MODES = {
    "reply_context": "the reply, a blank line, then the context",
    "reply": "the reply only",
    "context": "the context only",
}
MAP_METHODS = {"tsne": "t-SNE", "pca": "PCA"}
DEFAULT_SETTINGS = {"input": "reply_context", "instruction": None, "groups": None, "map": "tsne", "seed": 0}

Encoder = Callable[[list[str]], "object"]


class EmbeddingRefused(RuntimeError):
    """The build cannot run on this job; the message names why."""


def normalize_settings(model: str, *, input_mode: str = "reply_context", instruction: str | None = None,
                       groups: int | None = None, map_method: str = "tsne", seed: int = 0) -> dict:
    """Check one build's settings; refuse anything the engine cannot do honestly."""
    if input_mode not in INPUT_MODES:
        raise EmbeddingRefused(f"unknown text choice {input_mode!r}; pick one of {sorted(INPUT_MODES)}")
    if map_method not in MAP_METHODS:
        raise EmbeddingRefused(f"unknown map method {map_method!r}; pick one of {sorted(MAP_METHODS)}")
    if groups is not None:
        try:
            groups = int(groups)
        except (TypeError, ValueError):
            raise EmbeddingRefused(f"group count must be a whole number, not {groups!r}") from None
        if not 2 <= groups <= 20:
            raise EmbeddingRefused("group count must be between 2 and 20, or auto")
    try:
        seed = int(seed)
    except (TypeError, ValueError):
        raise EmbeddingRefused(f"seed must be a whole number, not {seed!r}") from None
    if not 0 <= seed <= 99999:
        raise EmbeddingRefused("seed must be between 0 and 99999")
    instruction = " ".join(str(instruction or "").split()) or None
    if instruction:
        if len(instruction) > 300:
            raise EmbeddingRefused("instruction must be 300 characters or fewer")
        entry = catalog_entry(model)
        if entry is not None and not entry.get("instruct"):
            raise EmbeddingRefused(f"{model} does not take an instruction; pick a Qwen3 or e5-instruct model")
    return {"input": input_mode, "instruction": instruction, "groups": groups, "map": map_method, "seed": seed}


def version_name(model: str, settings: dict | None = None) -> str:
    """Cache namespace: the model name, plus one short tag per non-default setting."""
    slug = re.sub(r"[^a-z0-9]+", "-", model.rsplit("/", 1)[-1].lower()).strip("-")
    if not slug:
        raise EmbeddingRefused(f"cannot name a cache namespace for model {model!r}")
    settings = settings or DEFAULT_SETTINGS
    tags = []
    if settings.get("input", "reply_context") != "reply_context":
        tags.append({"reply": "reply-only", "context": "context-only"}[settings["input"]])
    if settings.get("instruction"):
        tags.append("instr-" + hashlib.sha1(settings["instruction"].encode("utf-8")).hexdigest()[:6])
    if settings.get("groups"):
        tags.append(f"k{int(settings['groups'])}")
    if settings.get("map", "tsne") != "tsne":
        tags.append(settings["map"])
    if int(settings.get("seed") or 0):
        tags.append(f"seed{int(settings['seed'])}")
    return "-".join([slug, *tags])


def settings_summary(settings: dict | None) -> str:
    """Plain words for a person: what this build did differently."""
    settings = settings or DEFAULT_SETTINGS
    bits = [INPUT_MODES[settings.get("input") or "reply_context"]]
    if settings.get("instruction"):
        bits.append(f'instruction "{settings["instruction"]}"')
    bits.append(f'{settings["groups"]} groups' if settings.get("groups") else "groups chosen automatically")
    bits.append(f'{MAP_METHODS[settings.get("map") or "tsne"]} map')
    bits.append(f'seed {int(settings.get("seed") or 0)}')
    return ", ".join(bits)


def _now() -> str:
    return datetime.now(timezone.utc).astimezone().isoformat(timespec="seconds")


def _input_text(row: dict, text_field: str, context_field: str, mode: str = "reply_context") -> str:
    """The reply first, so a long context can never truncate it away."""
    text = str(row.get(text_field) or "")
    context = str(row.get(context_field) or "")
    if mode == "reply":
        return text.strip()
    if mode == "context":
        return context.strip()
    return f"{text}\n\n{context}".strip()


def _sentence_transformer(model: str, device: str, dtype: str | None = None) -> Encoder:
    try:
        from sentence_transformers import SentenceTransformer  # noqa: PLC0415
    except ImportError as error:
        raise EmbeddingRefused(
            "sentence-transformers is not installed in this Python "
            f"({sys.executable}); install it, then rerun") from error
    model_kwargs = {}
    if dtype:
        import torch  # noqa: PLC0415
        model_kwargs["dtype"] = getattr(torch, dtype)
    encoder = SentenceTransformer(model, device=device, model_kwargs=model_kwargs or None)

    def encode(texts: list[str]):
        return encoder.encode(texts, convert_to_numpy=True, normalize_embeddings=True,
                              batch_size=32, show_progress_bar=False)

    def steps() -> list[dict]:
        described = []
        for module in encoder:
            name = type(module).__name__
            entry = {"module": name}
            if name == "Transformer":
                entry["max_tokens"] = int(encoder.max_seq_length)
            elif name == "Pooling":
                entry["mode"] = str(getattr(module, "pooling_mode", "") or
                                    (module.get_pooling_mode_str() if hasattr(module, "get_pooling_mode_str") else ""))
            described.append(entry)
        return described

    encode.max_tokens = int(encoder.max_seq_length)
    encode.steps = steps
    encode.count_tokens = lambda texts: [len(ids) for ids in encoder.tokenizer(texts)["input_ids"]]
    encode.word_pieces = lambda text: [encoder.tokenizer.decode([i]) for i in encoder.tokenizer(text)["input_ids"]]
    return encode


def _library_versions() -> dict:
    versions = {}
    for name in ("sentence_transformers", "torch", "sklearn", "numpy"):
        try:
            versions[name] = __import__(name).__version__
        except Exception:  # noqa: BLE001 - provenance is best-effort per library
            continue
    return versions


def _choose_groups(vectors, seed: int, groups: int | None) -> tuple[list[int], int, dict]:
    import numpy as np  # noqa: PLC0415
    from sklearn.cluster import KMeans  # noqa: PLC0415
    from sklearn.metrics import silhouette_score  # noqa: PLC0415

    n = len(vectors)
    if groups is not None:
        candidates = [max(1, min(groups, n))]
    else:
        candidates = list(range(4, max(4, min(12, n // 10)) + 1)) if n >= 40 else [max(1, min(3, n))]
    scores: dict[str, float] = {}
    best = None
    for k in candidates:
        fit = KMeans(n_clusters=k, n_init=10, random_state=seed).fit(vectors)
        score = (float(silhouette_score(vectors, fit.labels_, metric="cosine"))
                 if 1 < k < n else 0.0)
        scores[str(k)] = round(score, 4)
        if best is None or score > best[0]:
            best = (score, k, fit.labels_)
    assert best is not None
    labels = np.asarray(best[2])
    # Number groups by size, largest first, so G1 is always the biggest.
    order = sorted(set(labels.tolist()), key=lambda g: (-int((labels == g).sum()), g))
    renumber = {old: new for new, old in enumerate(order)}
    return [renumber[int(g)] for g in labels], best[1], scores


SPEAKER_TAG = re.compile(r"(?m)^\s*[A-Z][A-Z_ ]{1,20}:")
# "don't" splits into "don"; a keyword like that reads as a typo
CONTRACTION_FRAGMENTS = frozenset({"don", "doesn", "didn", "isn", "wasn", "aren", "weren", "couldn", "wouldn",
                                   "shouldn", "haven", "hasn", "hadn", "won", "ain", "ll", "ve", "re"})


def _keywords(texts: list[str], groups: list[int], k: int, per_group: int = 6) -> dict[int, list[str]]:
    """Words that are more common inside a group than overall; speaker tags such as USER: dropped."""
    import numpy as np  # noqa: PLC0415
    from sklearn.feature_extraction.text import TfidfVectorizer  # noqa: PLC0415

    texts = [SPEAKER_TAG.sub(" ", t) for t in texts]
    try:
        from sklearn.feature_extraction.text import ENGLISH_STOP_WORDS  # noqa: PLC0415
        stop = sorted(ENGLISH_STOP_WORDS | CONTRACTION_FRAGMENTS)
        tfidf = TfidfVectorizer(stop_words=stop, min_df=2, max_df=0.5,
                                token_pattern=r"(?u)\b[a-zA-Z][a-zA-Z]{2,}\b")
        matrix = tfidf.fit_transform(texts)
    except ValueError:  # vocabulary empty after filtering
        return {g: [] for g in range(k)}
    terms = np.asarray(tfidf.get_feature_names_out())
    overall = np.asarray(matrix.mean(axis=0)).ravel()
    labels = np.asarray(groups)
    words: dict[int, list[str]] = {}
    for g in range(k):
        mask = labels == g
        if not mask.any():
            words[g] = []
            continue
        lift = np.asarray(matrix[mask].mean(axis=0)).ravel() - overall
        top = [int(i) for i in np.argsort(-lift)[:per_group] if lift[int(i)] > 0]
        words[g] = [str(terms[i]) for i in top]
    return words


def _map_2d(vectors, seed: int, method: str = "tsne") -> list[tuple[float, float]]:
    n = len(vectors)
    if n < 5:
        return [(float(i), 0.0) for i in range(n)]
    if method == "pca":
        from sklearn.decomposition import PCA  # noqa: PLC0415
        coords = PCA(n_components=2, random_state=seed).fit_transform(vectors)
    else:
        from sklearn.manifold import TSNE  # noqa: PLC0415
        perplexity = float(max(2, min(30, (n - 1) // 3)))
        coords = TSNE(n_components=2, perplexity=perplexity, init="pca", metric="cosine",
                      random_state=seed).fit_transform(vectors)
    lo, hi = coords.min(axis=0), coords.max(axis=0)
    span = (hi - lo)
    span[span == 0] = 1.0
    scaled = (coords - lo) / span
    return [(round(float(x), 5), round(float(y), 5)) for x, y in scaled]


MAP3D_FILE = "map3d.jsonl"


def _map_3d(vectors, seed: int, method: str = "tsne") -> list[tuple[float, float, float]]:
    """3D positions for the rotating view, centred on 0 and scaled into -1..1."""
    import numpy as np  # noqa: PLC0415

    n = len(vectors)
    if n < 5:
        return [(float(i), 0.0, 0.0) for i in range(n)]
    if method == "pca":
        from sklearn.decomposition import PCA  # noqa: PLC0415
        coords = PCA(n_components=3, random_state=seed).fit_transform(vectors)
    else:
        from sklearn.manifold import TSNE  # noqa: PLC0415
        perplexity = float(max(2, min(30, (n - 1) // 3)))
        coords = TSNE(n_components=3, perplexity=perplexity, init="pca", metric="cosine",
                      random_state=seed).fit_transform(vectors)
    coords = coords - coords.mean(axis=0)
    scale = float(np.abs(coords).max()) or 1.0
    coords = coords / scale
    return [(round(float(x), 5), round(float(y), 5), round(float(z), 5)) for x, y, z in coords]


def ensure_map3d(job_root: Path, version: str) -> Path:
    """Write the 3D view for a build made before 3D existed; the vectors are not touched."""
    import numpy as np  # noqa: PLC0415

    folder = Path(job_root) / "cache" / "embeddings" / str(version)
    manifest_path = folder / "manifest.json"
    if not manifest_path.is_file():
        raise EmbeddingRefused(f"no embedding named {version!r} on this job")
    target = folder / MAP3D_FILE
    if target.is_file():
        return target
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    method = (manifest.get("map") or {}).get("method") or "tsne"
    seed = int((manifest.get("map") or {}).get("seed") or 0)
    rows = cal._read_jsonl(folder / "rows.jsonl")
    vectors = np.load(folder / "vectors.npy").astype("float32")
    coords = _map_3d(vectors, seed, method)
    target.write_bytes(cal._jsonl_bytes(
        [{"item_id": str(row["item_id"]), "x": x, "y": y, "z": z} for row, (x, y, z) in zip(rows, coords)]))
    return target


def _pid_alive(pid) -> bool:
    try:
        os.kill(int(pid), 0)
    except (ProcessLookupError, TypeError, ValueError):
        return False
    except PermissionError:
        return True
    return True


def _marker(folder: Path) -> dict | None:
    path = folder / BUILD_MARKER
    if not path.is_file():
        return None
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return {}


def running_build(job_root: Path) -> dict | None:
    """The build in progress on this job, if its process is still alive."""
    base = Path(job_root) / "cache" / "embeddings"
    for folder in sorted(base.glob("*/")) if base.is_dir() else []:
        mark = _marker(folder)
        if mark and _pid_alive(mark.get("pid")):
            return {"version": folder.name, **mark}
    return None


def preflight(job_root: Path, model: str, settings: dict | None = None) -> tuple[str, Path]:
    """Refuse before any model loads: HOLD, broken P0 files, or another build running."""
    job_root = Path(job_root).resolve()
    state = job.status(job_root)
    if state.get("hold"):
        raise EmbeddingRefused(f"HOLD · {state.get('hold_reason')}; this job is read-only")
    if state.get("missing") or state.get("integrity_errors"):
        raise EmbeddingRefused("P0 files do not verify: "
                               + "; ".join(state.get("integrity_errors") or ["P0 files missing"]))
    version = version_name(model, settings)
    busy = running_build(job_root)
    if busy and busy.get("pid") != os.getpid():
        raise EmbeddingRefused(f"{busy['version']} is still building; one build at a time")
    return version, job_root / "cache" / "embeddings" / version


def build(job_root: Path, *, model: str = DEFAULT_MODEL, device: str = "auto",
          groups: int | None = None, seed: int = 0, input_mode: str = "reply_context",
          instruction: str | None = None, map_method: str = "tsne", encoder: Encoder | None = None,
          channel: str = "cli", started_by: str | None = None) -> dict:
    """Embed the development pool once, with these settings, as one complete Run.

    A build starts only when a person asks for it; ``started_by`` names that person and is
    written on the Run Ticket and the manifest, so the page can say who started every build.
    """
    job_root = Path(job_root).resolve()
    settings = normalize_settings(model, input_mode=input_mode, instruction=instruction, groups=groups,
                                  map_method=map_method, seed=seed)
    version, out = preflight(job_root, model, settings)
    if (out / "manifest.json").is_file():
        existing = json.loads((out / "manifest.json").read_text(encoding="utf-8"))
        corpus_now = job.sha256_file(job_root / "corpus" / "items.jsonl")
        if existing.get("population", {}).get("corpus_items_sha256") != corpus_now:
            raise EmbeddingRefused(f"{version} was built from a different corpus; a changed corpus is a new job")
        return {"version": version, "run": existing.get("run"), "built": False, "manifest": existing}
    out.mkdir(parents=True, exist_ok=True)
    marker = out / BUILD_MARKER
    marker.write_text(json.dumps({"pid": os.getpid(), "model": model, "started_at": _now(),
                                  "channel": channel, "settings": settings}), encoding="utf-8")
    try:
        return _build(job_root, version, out, model=model, device=resolve_device(device),
                      settings=settings, encoder=encoder, channel=channel, started_by=started_by)
    finally:
        marker.unlink(missing_ok=True)


def _build(job_root: Path, version: str, out: Path, *, model: str, device: str, settings: dict,
           encoder: Encoder | None, channel: str, started_by: str | None = None) -> dict:
    import numpy as np  # noqa: PLC0415

    entry = catalog_entry(model) or {}
    groups, seed = settings["groups"], settings["seed"]
    prompt = entry["instruct"].format(task=settings["instruction"]) if settings["instruction"] and entry.get("instruct") \
        else (f'Instruct: {settings["instruction"]}\nQuery: ' if settings["instruction"] else "")
    config = job.load_mapping(job_root / "config.yaml")
    corpus_cfg = config.get("corpus") if isinstance(config.get("corpus"), dict) else {}
    text_field = str(corpus_cfg.get("text_field") or "text")
    context_field = str(corpus_cfg.get("context_field") or "context_prev")
    rows = cal._corpus_rows(job_root)
    eligible = [r for r in rows if r.get("population_status") == "eligible" and r.get("item_id") is not None]
    # A fenced v2 corpus contains development rows only. Its public manifest
    # carries the sealed count, while protected item ids and text stay outside
    # this reader. Older corpora can still report their inline sealed rows.
    n_sealed = sum(1 for r in rows if r.get("population_status") == "sealed")
    corpus_manifest_path = job_root / "corpus" / "manifest.json"
    if corpus_manifest_path.is_file():
        corpus_manifest = job.load_mapping(corpus_manifest_path)
        if "n_sealed" in corpus_manifest:
            try:
                n_sealed = int(corpus_manifest["n_sealed"])
            except (TypeError, ValueError):
                raise EmbeddingRefused("corpus manifest has an invalid n_sealed count") from None
            if n_sealed < 0:
                raise EmbeddingRefused("corpus manifest has a negative n_sealed count")
    if not eligible:
        raise EmbeddingRefused("no development item is marked population_status: eligible")
    eligible.sort(key=lambda r: str(r["item_id"]))
    texts = [_input_text(r, text_field, context_field, settings["input"]) for r in eligible]
    empty = sum(1 for t in texts if not t)
    if empty:
        raise EmbeddingRefused(f"{empty} development items have no text for {INPUT_MODES[settings['input']]}")
    model_inputs = [prompt + t for t in texts]

    target = version
    run = cal._run_name(job_root, "embedding-build", target)
    started = _now()
    ticket_common = dict(
        operation="embedding-build", phase="P0", episode="contract", target=target,
        commission={"requested_by": channel, "started_by": started_by, "embedder": {"model": model, "device": device,
                                                          "dtype": entry.get("dtype") or "float32",
                                                          "in_catalog": bool(entry)},
                    "preprocessing": PREPROCESSING, "groups": GROUP_METHOD, "settings": settings},
        inputs=[{"path": "corpus/items.jsonl", "sha256": job.sha256_file(job_root / "corpus" / "items.jsonl")}],
        worker={"kind": "cli", "name": "subjective-label.engine.embedding_build:build"},
        acceptance="every eligible item embedded once; no sealed item read; no label written",
    )
    cal._write_run(job_root, run, status="running", started_at=started, finished_at=None,
                   outcome="embedding", artifacts=[], **ticket_common)

    try:
        encode = encoder or _sentence_transformer(model, device, entry.get("dtype"))
        vectors = np.asarray(encode(model_inputs), dtype="float32")
        if vectors.ndim != 2 or vectors.shape[0] != len(texts):
            raise EmbeddingRefused(f"encoder returned shape {vectors.shape} for {len(texts)} texts")
        norms = np.linalg.norm(vectors, axis=1, keepdims=True)
        vectors = vectors / np.where(norms == 0, 1.0, norms)
        group_of, k, scores = _choose_groups(vectors, seed, groups)
        words = _keywords(texts, group_of, k)
        coords = _map_2d(vectors, seed, settings["map"])
        coords3 = _map_3d(vectors, seed, settings["map"])
        max_tokens = getattr(encode, "max_tokens", None)
        counts = encode.count_tokens(model_inputs) if hasattr(encode, "count_tokens") else [None] * len(texts)
        example_vector = np.asarray(encode([prompt + EXAMPLE_INPUT]), dtype="float32")[0]
        example_vector = example_vector / (np.linalg.norm(example_vector) or 1.0)
        example = {
            "input": EXAMPLE_INPUT, "prompt": prompt or None, "note": "made up; not a corpus item",
            "word_pieces": encode.word_pieces(prompt + EXAMPLE_INPUT) if hasattr(encode, "word_pieces") else None,
            "vector_first": [round(float(v), 4) for v in example_vector[:8]],
            "dim": int(example_vector.shape[0]),
            "length": round(float(np.linalg.norm(example_vector)), 4),
        }
    except Exception as error:
        runtime_path = job_root / "results" / run / "runtime.yaml"
        runtime = job.load_mapping(runtime_path)
        runtime.update({"status": "failed", "finished_at": _now(),
                        "failure": f"{type(error).__name__}: {error}"[:500]})
        runtime_path.write_bytes(job.yaml_bytes(runtime))
        raise

    np.save(out / "vectors.npy", vectors)
    rows_out = [{"row": i, "item_id": str(r["item_id"]), "text_hash": r.get("text_hash"),
                 "input_sha256": job.sha256_bytes(t.encode("utf-8")), "tokens": n,
                 "cut": bool(max_tokens and n and n > max_tokens)}
                for i, (r, t, n) in enumerate(zip(eligible, model_inputs, counts))]
    (out / "rows.jsonl").write_bytes(cal._jsonl_bytes(rows_out))
    map_rows = [{"item_id": str(r["item_id"]), "x": x, "y": y, "group": g}
                for r, (x, y), g in zip(eligible, coords, group_of)]
    (out / "map.jsonl").write_bytes(cal._jsonl_bytes(map_rows))
    (out / MAP3D_FILE).write_bytes(cal._jsonl_bytes(
        [{"item_id": str(r["item_id"]), "x": x, "y": y, "z": z} for r, (x, y, z) in zip(eligible, coords3)]))
    group_rows = [{"group": g, "size": group_of.count(g), "keywords": words.get(g, [])} for g in range(k)]
    (out / "groups.json").write_bytes(job.json_bytes({
        "method": GROUP_METHOD, "k": k, "seed": seed, "silhouette_by_k": scores, "groups": group_rows,
        "authority": "representation only; a group is never a label",
    }))
    files = ["vectors.npy", "rows.jsonl", "map.jsonl", MAP3D_FILE, "groups.json"]
    manifest = {
        "schema": SCHEMA, "run": run, "version": version, "created_at": _now(),
        "settings": settings, "settings_summary": settings_summary(settings),
        "started_by": {"person": started_by, "via": channel},
        "model": {"id": model, "backend": "sentence-transformers" if encoder is None else "injected",
                  "device": device, "dtype": entry.get("dtype") or "float32", "dim": int(vectors.shape[1]),
                  "params": entry.get("params"), "license": entry.get("license"), "maker": entry.get("maker"),
                  "libraries": _library_versions()},
        "preprocessing": {"id": PREPROCESSING, "text_field": text_field, "context_field": context_field,
                          "input": settings["input"], "join": INPUT_MODES[settings["input"]],
                          "prompt": prompt or None, "normalize": "l2"},
        "encoder": {"steps": encode.steps() if hasattr(encode, "steps") else [],
                    "max_tokens": max_tokens,
                    "items_cut": sum(1 for row in rows_out if row["cut"]),
                    "longest_tokens": max((n for n in counts if n), default=None)},
        "example": example,
        "population": {"eligible_embedded": len(eligible), "sealed_excluded": n_sealed,
                       "corpus_items_sha256": job.sha256_file(job_root / "corpus" / "items.jsonl")},
        "index": {"kind": "numpy-flat", "metric": "cosine", "file": "vectors.npy", "rows": "rows.jsonl"},
        "map": {"method": settings["map"], "seed": seed, "file": "map.jsonl", "file_3d": MAP3D_FILE},
        "groups": {"method": GROUP_METHOD, "k": k, "seed": seed, "file": "groups.json"},
        "files": [{"path": f, "sha256": job.sha256_file(out / f)} for f in files],
        "authority": "representation only; no label, region, or gold is written or implied",
    }
    job.write_once(out / "manifest.json", job.json_bytes(manifest))
    rel = f"cache/embeddings/{version}"
    cal._write_run(job_root, run, status="complete", started_at=started, finished_at=_now(),
                   outcome=f"{len(eligible)} items embedded ({n_sealed} held-back test items left out); {k} groups",
                   artifacts=[{"path": f"{rel}/{f}", "sha256": job.sha256_file(out / f)}
                              for f in ["manifest.json", *files]],
                   **ticket_common)
    return {"version": version, "run": run, "built": True, "manifest": manifest}


def builds(job_root: Path) -> list[dict]:
    """Every complete embedding namespace, oldest first; read-only."""
    base = Path(job_root) / "cache" / "embeddings"
    if not base.is_dir():
        return []
    found = []
    for manifest in base.glob("*/manifest.json"):
        try:
            data = json.loads(manifest.read_text(encoding="utf-8"))
            if data.get("schema") != SCHEMA:
                continue
            found.append({"folder": manifest.parent, "manifest": data,
                          "map": cal._read_jsonl(manifest.parent / "map.jsonl"),
                          "map3d": cal._read_jsonl(manifest.parent / MAP3D_FILE),
                          "groups": json.loads((manifest.parent / "groups.json").read_text(encoding="utf-8"))})
        except (OSError, ValueError):
            continue
    return sorted(found, key=lambda hit: str(hit["manifest"].get("created_at") or ""))


def latest(job_root: Path) -> dict | None:
    """The newest complete embedding namespace, read-only; None when none exists."""
    found = builds(job_root)
    return found[-1] if found else None


def neighbors(job_root: Path, version: str, item_id: str, k: int = 6) -> dict:
    """The k development items nearest one item, by cosine on that build's vectors.

    Nearness is representation only: a neighbour never lends its label (ref-embeddings.md).
    Sealed items are not in the vectors, so they can never be returned.
    """
    import numpy as np  # noqa: PLC0415

    folder = Path(job_root) / "cache" / "embeddings" / str(version)
    if not (folder / "manifest.json").is_file():
        raise EmbeddingRefused(f"no embedding named {version!r} on this job")
    rows = cal._read_jsonl(folder / "rows.jsonl")
    ids = [str(row["item_id"]) for row in rows]
    if str(item_id) not in ids:
        raise EmbeddingRefused(f"item {item_id!r} is not in this embedding")
    vectors = np.load(folder / "vectors.npy").astype("float32")
    index = ids.index(str(item_id))
    scores = vectors @ vectors[index]
    scores[index] = -9.0
    order = np.argsort(-scores)[:max(1, min(int(k), len(ids) - 1))]
    groups = {str(row.get("item_id")): row.get("group")
              for row in cal._read_jsonl(folder / "map.jsonl")}
    return {
        "version": str(version), "item_id": str(item_id), "group": groups.get(str(item_id)),
        "tokens": rows[index].get("tokens"), "cut": rows[index].get("cut"),
        "neighbors": [{"item_id": ids[int(i)], "similarity": round(float(scores[int(i)]), 4),
                       "group": groups.get(ids[int(i)])} for i in order],
    }


def waiting_items(job_root: Path) -> dict[str, str]:
    """Items drawn into a round batch that have no final label yet, with the round that drew them."""
    waiting: dict[str, str] = {}
    for round_path in cal._round_dirs(Path(job_root)):
        states = cal._item_states(round_path)
        for row in cal._read_jsonl(round_path / "human_batch.jsonl"):
            item_id = str(row.get("item_id"))
            if not (states.get(item_id) or {}).get("final"):
                waiting[item_id] = round_path.name
    return waiting


def seen_items(job_root: Path) -> dict[str, str]:
    """Every item whose text was shown as a group example, with the first time it was shown."""
    seen: dict[str, str] = {}
    for line in cal._read_jsonl(Path(job_root) / EXPOSURE_LOG):
        for item_id in line.get("item_ids") or []:
            seen.setdefault(str(item_id), str(line.get("at")))
    return seen


def _record_exposure(job_root: Path, *, human_id: str | None, channel: str, where: str, version: str,
                     item_ids: list[str], group: int | None = None) -> None:
    """Append who saw which item text, and where; this log is only ever appended to."""
    log = Path(job_root) / EXPOSURE_LOG
    log.parent.mkdir(parents=True, exist_ok=True)
    line = {"at": _now(), "human_id": human_id, "channel": channel, "where": where,
            "version": str(version), "item_ids": list(item_ids)}
    if group is not None:
        line["group"] = group
    with log.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(line, sort_keys=True) + "\n")


def _build_folder(job_root: Path, version: str) -> tuple[Path, dict]:
    folder = Path(job_root) / "cache" / "embeddings" / str(version)
    if not (folder / "manifest.json").is_file():
        raise EmbeddingRefused(f"no embedding named {version!r} on this job")
    if job.status(Path(job_root)).get("hold"):
        raise EmbeddingRefused("this job is read-only (HOLD), so showing item text cannot be recorded")
    return folder, json.loads((folder / "manifest.json").read_text(encoding="utf-8"))


def _texts(job_root: Path, manifest: dict) -> tuple[dict, str, str]:
    pre = manifest.get("preprocessing") or {}
    text_field, context_field = str(pre.get("text_field") or "text"), str(pre.get("context_field") or "context_prev")
    corpus = {str(row.get("item_id")): row for row in cal._corpus_rows(Path(job_root))
              if row.get("population_status") == "eligible"}
    return corpus, text_field, context_field


def item_text(job_root: Path, version: str, item_id: str, *, human_id: str | None = None,
              channel: str = "cli") -> dict:
    """One map item's text, unless it waits in a round batch; recorded in the exposure log like examples."""
    job_root = Path(job_root).resolve()
    folder, manifest = _build_folder(job_root, version)
    item_id = str(item_id)
    if item_id not in {str(row["item_id"]) for row in cal._read_jsonl(folder / "rows.jsonl")}:
        raise EmbeddingRefused(f"item {item_id!r} is not in this embedding")
    waiting = waiting_items(job_root)
    if item_id in waiting:
        raise EmbeddingRefused(f"item {item_id} waits in {waiting[item_id]}; its text opens on the Label screen")
    corpus, text_field, context_field = _texts(job_root, manifest)
    row = corpus.get(item_id) or {}
    _record_exposure(job_root, human_id=human_id, channel=channel, where="embedding map item",
                     version=version, item_ids=[item_id])
    return {"version": str(version), "item_id": item_id, "text": str(row.get(text_field) or ""),
            "context": str(row.get(context_field) or "")}


def group_examples(job_root: Path, version: str, group: int, *, k: int = 3, offset: int = 0,
                   human_id: str | None = None, channel: str = "cli") -> dict:
    """The development items most typical of one group, nearest its centre first, with their text.

    Items waiting in a round batch without a final label are left out, so the first look at
    them stays on the Label screen.  Showing text is an exposure: each call that returns items
    appends one line to ``exposure/group_examples.jsonl`` naming who saw which items, so a later
    round can tell a fresh item from one already seen.  A HOLD job cannot record it, so it refuses.
    """
    import numpy as np  # noqa: PLC0415

    job_root = Path(job_root).resolve()
    folder, manifest = _build_folder(job_root, version)
    k, offset = int(k), int(offset)
    if not 1 <= k <= 10 or offset < 0:
        raise EmbeddingRefused("examples come 1 to 10 at a time, from offset 0 or more")
    ids = [str(row["item_id"]) for row in cal._read_jsonl(folder / "rows.jsonl")]
    group_of = {str(row["item_id"]): row.get("group") for row in cal._read_jsonl(folder / "map.jsonl")}
    n_groups = int((manifest.get("groups") or {}).get("k") or 0)
    if not 0 <= int(group) < n_groups:
        raise EmbeddingRefused(f"this embedding has groups 1 to {n_groups}")
    group = int(group)
    members = [i for i, item_id in enumerate(ids) if group_of.get(item_id) == group]
    vectors = np.load(folder / "vectors.npy").astype("float32")[members]
    centre = vectors.mean(axis=0)
    centre = centre / (np.linalg.norm(centre) or 1.0)
    closeness = vectors @ centre
    ranked = [(ids[members[int(i)]], float(closeness[int(i)])) for i in np.argsort(-closeness)]

    waiting = waiting_items(job_root)
    hidden = sorted({waiting[item_id] for item_id, _ in ranked if item_id in waiting})
    visible = [(item_id, score) for item_id, score in ranked if item_id not in waiting]
    page = visible[offset:offset + k]

    corpus, text_field, context_field = _texts(job_root, manifest)
    examples = [{"item_id": item_id, "closeness": round(score, 3),
                 "text": str(corpus.get(item_id, {}).get(text_field) or ""),
                 "context": str(corpus.get(item_id, {}).get(context_field) or "")}
                for item_id, score in page if item_id in corpus]
    if examples:
        _record_exposure(job_root, human_id=human_id, channel=channel, where="embedding group examples",
                         version=version, item_ids=[e["item_id"] for e in examples], group=group)
    return {
        "version": str(version), "group": group, "size": len(members), "offset": offset,
        "examples": examples, "more": offset + k < len(visible),
        "hidden_waiting": len(ranked) - len(visible), "hidden_rounds": hidden,
    }


def _log_tail(path: Path, lines: int = 4) -> list[str]:
    if not path.is_file():
        return []
    text = path.read_text(encoding="utf-8", errors="replace").replace("\r", "\n")
    kept = [line.strip() for line in text.splitlines()
            if line.strip() and "it/s]" not in line and "Loading weights" not in line]
    return [line[:300] for line in kept[-lines:]]


BUTTON_CHANNEL = "board labeling screen"


def who_started(commission: dict | None) -> dict:
    """Who asked for a build and how it was started, from its Run Ticket; older tickets kept it as free text."""
    commission = commission or {}
    channel = str(commission.get("requested_by") or "")
    person = commission.get("started_by")
    note = None
    if not person:
        asked = re.search(r"requested by (\S+)(?: in (\w+))?", channel)
        if asked:
            person, note = asked.group(1), (f"asked in {asked.group(2)}" if asked.group(2) else None)
    return {"person": person or None, "via": "run button" if channel.startswith(BUTTON_CHANNEL) else "terminal",
            "note": note}


def build_status(job_root: Path) -> list[dict]:
    """One row per catalog model plus any other built model: built, building, failed, stopped, none."""
    job_root = Path(job_root)
    built = {hit["manifest"]["version"]: hit["manifest"] for hit in builds(job_root)}
    models = [{**entry, "version": version_name(entry["id"]), "settings": dict(DEFAULT_SETTINGS)} for entry in CATALOG]
    known = {entry["version"] for entry in models}
    base = job_root / "cache" / "embeddings"
    for folder in sorted(base.glob("*/")) if base.is_dir() else []:
        if folder.name in known:
            continue
        manifest = built.get(folder.name) or {}
        mark = _marker(folder) or {}
        model_id = (manifest.get("model") or {}).get("id") or mark.get("model")
        if not model_id:
            continue
        settings = manifest.get("settings") or mark.get("settings") or dict(DEFAULT_SETTINGS)
        entry = catalog_entry(model_id) or {"id": model_id, "note": "built outside the catalog"}
        models.append({**entry, "version": folder.name, "settings": settings, "variant": True})
    rows = []
    for entry in models:
        version = entry["version"]
        folder = base / version
        runs = sorted((job_root / "results").glob(f"rl*_embedding-build_{version}/runtime.yaml")) \
            if (job_root / "results").is_dir() else []
        runtime = job.load_mapping(runs[-1]) if runs else {}
        mark = _marker(folder)
        if version in built:
            state = "built"
        elif mark is not None and _pid_alive(mark.get("pid")):
            state = "building"
        elif mark is not None or runtime.get("status") == "running":
            state = "stopped"
        elif runtime.get("status") == "failed":
            state = "failed"
        else:
            state = "none"
        run = (built.get(version) or {}).get("run") or runtime.get("run")
        ticket = job.load_mapping(job_root / "runs" / f"{run}.yaml") if run and (job_root / "runs" / f"{run}.yaml").is_file() else {}
        rows.append({**entry, "state": state, "settings_summary": settings_summary(entry.get("settings")),
                     "run": run, "started": who_started(ticket.get("commission")) if run else None,
                     "failure": runtime.get("failure") if state in {"failed", "stopped"} else None,
                     "log_tail": _log_tail(folder / BUILD_LOG) if state in {"failed", "stopped", "building"} else []})
    return rows


def start_background_build(job_root: Path, model: str, *, channel: str, started_by: str,
                           input_mode: str = "reply_context",
                           instruction: str | None = None, groups: int | None = None,
                           map_method: str = "tsne", seed: int = 0,
                           python: str | None = None) -> tuple[subprocess.Popen, str]:
    """Check, then start `build` in its own process; the caller must keep and poll the Popen."""
    if not str(started_by or "").strip():
        raise EmbeddingRefused("a build starts only when a person asks; name who asked")
    if catalog_entry(model) is None:
        raise EmbeddingRefused(f"{model!r} is not in the embedding catalog")
    settings = normalize_settings(model, input_mode=input_mode, instruction=instruction, groups=groups,
                                  map_method=map_method, seed=seed)
    job_root = Path(job_root).resolve()
    version, out = preflight(job_root, model, settings)
    if (out / "manifest.json").is_file():
        raise EmbeddingRefused(f"{version} is already built with these settings")
    out.mkdir(parents=True, exist_ok=True)
    log = (out / BUILD_LOG).open("w", encoding="utf-8")
    env = {**os.environ, "PYTHONUNBUFFERED": "1", "TOKENIZERS_PARALLELISM": "false"}
    proc = subprocess.Popen(
        [python or sys.executable, str(Path(__file__).resolve()), "build", "--job-root", str(job_root),
         "--model", model, "--device", "auto", "--channel", channel, "--started-by", str(started_by),
         "--input", settings["input"], "--map", settings["map"], "--seed", str(settings["seed"]),
         *(["--groups", str(settings["groups"])] if settings["groups"] else []),
         *(["--instruction", settings["instruction"]] if settings["instruction"] else [])],
        stdout=log, stderr=subprocess.STDOUT, stdin=subprocess.DEVNULL, env=env, start_new_session=True)
    log.close()
    (out / BUILD_MARKER).write_text(json.dumps({"pid": proc.pid, "model": model, "started_at": _now(),
                                                "channel": channel, "settings": settings}), encoding="utf-8")
    return proc, version


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    sub = parser.add_subparsers(dest="cmd", required=True)
    b = sub.add_parser("build", help="embed the development pool as one embedding-build Run")
    b.add_argument("--job-root", type=Path, required=True)
    b.add_argument("--model", default=DEFAULT_MODEL)
    b.add_argument("--device", default="auto", help="auto picks cuda, then mps, then cpu")
    b.add_argument("--channel", default="cli")
    b.add_argument("--started-by", required=True,
                   help="the person who asked for this run; a build never starts on its own")
    b.add_argument("--groups", type=int, default=None, help="fixed k (2-20); default picks 4..12 by silhouette")
    b.add_argument("--seed", type=int, default=0)
    b.add_argument("--input", default="reply_context", choices=sorted(INPUT_MODES), help="which text to embed")
    b.add_argument("--instruction", default=None, help="task instruction, Qwen3 and e5-instruct models only")
    b.add_argument("--map", default="tsne", choices=sorted(MAP_METHODS), help="how to draw the 2D and 3D map")
    s = sub.add_parser("show", help="print the newest embedding manifest")
    s.add_argument("--job-root", type=Path, required=True)
    st = sub.add_parser("status", help="built, building, failed, or not built, per model")
    st.add_argument("--job-root", type=Path, required=True)
    nb = sub.add_parser("neighbors", help="the development items nearest one item")
    nb.add_argument("--job-root", type=Path, required=True)
    nb.add_argument("--version", required=True)
    nb.add_argument("--item-id", required=True)
    nb.add_argument("--k", type=int, default=6)
    sub.add_parser("catalog", help="the models a person may choose")
    ex = sub.add_parser("examples", help="the most typical items of one group, with text (recorded as seen)")
    ex.add_argument("--job-root", type=Path, required=True)
    ex.add_argument("--version", required=True)
    ex.add_argument("--group", type=int, required=True, help="group number as shown, G1 = 1")
    ex.add_argument("--k", type=int, default=3)
    ex.add_argument("--offset", type=int, default=0)
    ex.add_argument("--human-id", required=True, help="who will read the text; written to the exposure log")
    ex.add_argument("--channel", default="cli")
    m3 = sub.add_parser("map3d", help="add the 3D view to a build made before 3D existed")
    m3.add_argument("--job-root", type=Path, required=True)
    m3.add_argument("--version", required=True)
    args = parser.parse_args(argv)
    try:
        if args.cmd == "build":
            result = build(args.job_root, model=args.model, device=args.device, groups=args.groups,
                           seed=args.seed, input_mode=args.input, instruction=args.instruction,
                           map_method=args.map, channel=args.channel, started_by=args.started_by)
            m = result["manifest"]
            print(json.dumps({"run": result["run"], "version": result["version"], "built": result["built"],
                              "embedded": m["population"]["eligible_embedded"],
                              "sealed_excluded": m["population"]["sealed_excluded"],
                              "groups": m["groups"]["k"]}, indent=2))
        elif args.cmd == "status":
            rows = build_status(args.job_root)
            print(json.dumps([{k: r.get(k) for k in ("id", "state", "run", "failure")} for r in rows], indent=2))
        elif args.cmd == "neighbors":
            print(json.dumps(neighbors(args.job_root, args.version, args.item_id, args.k), indent=2))
        elif args.cmd == "examples":
            print(json.dumps(group_examples(args.job_root, args.version, args.group - 1, k=args.k, offset=args.offset,
                                            human_id=args.human_id, channel=args.channel), indent=2, ensure_ascii=False))
        elif args.cmd == "map3d":
            print(ensure_map3d(args.job_root, args.version))
        elif args.cmd == "catalog":
            print(json.dumps(list(CATALOG), indent=2))
        else:
            hit = latest(args.job_root)
            print(json.dumps(hit["manifest"] if hit else None, indent=2))
    except (EmbeddingRefused, cal.LabelingRefused, RuntimeError) as error:
        print(f"refused: {error}", file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
