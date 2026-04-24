"""Small-classifier utilities for the subjective-label plugin.

Invoked by the `classifier` agent via Bash. Manages a small supervised model
trained on gallery + confirmed panel labels; exposes predict and uncertainty
operations for Tier 1 of the 3-tier cascade and active-learning hard mining.

CLI subcommands
    train        train a model on gallery + extra labels
    predict      score every input item
    uncertainty  return items sorted by uncertainty (hardest first)
    hard_mining  top-k hard items, excluding those already in gallery

All subcommands take --project-dir for per-project caching.

Config source: {project_dir}/config.yaml → classifier section
    backend: "logreg"   # or "setfit", "lora-bert"
    thresholds:
      accept_margin: 0.3
      accept_prob: 0.7
    train:
      cv_folds: 5
      val_split: 0.2
      include_panel_labels: true   # use confirmed panel items in addition to gallery
"""

from __future__ import annotations

import argparse
import hashlib
import json
import pickle
import sys
from pathlib import Path


# ── shared helpers ──────────────────────────────────────────────────────────

def _sha1(s: str) -> str:
    return hashlib.sha1(s.encode("utf-8")).hexdigest()


def _load_yaml(path: Path) -> dict:
    import yaml  # noqa: PLC0415
    return yaml.safe_load(path.read_text(encoding="utf-8")) or {}


def _read_config(project_dir: Path) -> dict:
    cfg_path = project_dir / "config.yaml"
    if not cfg_path.exists():
        return {"backend": "logreg", "thresholds": {"accept_margin": 0.3, "accept_prob": 0.7}}
    cfg = _load_yaml(cfg_path)
    return cfg.get("classifier", {}) or {}


def _embedding_config(project_dir: Path) -> dict:
    cfg_path = project_dir / "config.yaml"
    if not cfg_path.exists():
        return {"model": "sentence-transformers/all-MiniLM-L6-v2"}
    cfg = _load_yaml(cfg_path)
    return cfg.get("embedding", {}) or {}


def _vec_path_for(project_dir: Path, text: str) -> Path:
    emb_cfg = _embedding_config(project_dir)
    model_tag = emb_cfg.get("model", "st-default")
    h = _sha1(f"{model_tag}::{text}")
    return project_dir / "cache" / "embeddings" / "vectors" / f"{h}.npy"


def _load_vectors(project_dir: Path, items: list[dict]):
    """Load embedding vectors for items. Requires lib/embed.py to have been
    run first (so vectors are cached)."""
    import numpy as np  # noqa: PLC0415
    vecs = []
    ids = []
    missing = []
    for it in items:
        p = _vec_path_for(project_dir, it["text"])
        if not p.exists():
            missing.append(it["id"])
            continue
        vecs.append(np.load(p))
        ids.append(it["id"])
    if missing:
        raise FileNotFoundError(
            f"{len(missing)} items missing embedding vectors (e.g. {missing[:3]}). "
            "Run `python lib/embed.py ... embed` first."
        )
    return np.vstack(vecs), ids


# ── backends ────────────────────────────────────────────────────────────────

class _LogRegBackend:
    """Logistic regression on frozen embeddings. Trains in < 1 second."""

    def __init__(self):
        from sklearn.linear_model import LogisticRegression  # noqa: PLC0415
        self.clf = LogisticRegression(max_iter=1000, class_weight="balanced", C=1.0)
        self.classes_ = None

    def fit(self, X, y):
        self.clf.fit(X, y)
        self.classes_ = list(self.clf.classes_)

    def predict_proba(self, X):
        return self.clf.predict_proba(X)

    def to_pickle(self, path: Path):
        path.write_bytes(pickle.dumps({"clf": self.clf, "classes_": self.classes_}))

    @classmethod
    def from_pickle(cls, path: Path):
        data = pickle.loads(path.read_bytes())
        inst = cls()
        inst.clf = data["clf"]
        inst.classes_ = data["classes_"]
        return inst


class _SetFitBackend:
    """SetFit: fine-tunes a sentence-transformer + classification head on
    few examples per label. Heavier but higher quality."""

    def __init__(self, base_model: str = "sentence-transformers/all-MiniLM-L6-v2"):
        from setfit import SetFitModel  # noqa: PLC0415
        self.base_model = base_model
        self.model = None
        self.classes_ = None

    def fit(self, texts: list[str], y: list[str]):
        from setfit import SetFitModel, Trainer, TrainingArguments  # noqa: PLC0415
        from datasets import Dataset  # noqa: PLC0415

        classes = sorted(set(y))
        self.classes_ = classes
        label_to_id = {c: i for i, c in enumerate(classes)}
        ds = Dataset.from_dict({"text": texts, "label": [label_to_id[l] for l in y]})
        self.model = SetFitModel.from_pretrained(self.base_model)
        args = TrainingArguments(batch_size=8, num_iterations=20, num_epochs=1)
        trainer = Trainer(model=self.model, train_dataset=ds, args=args)
        trainer.train()

    def predict_proba_texts(self, texts: list[str]):
        import numpy as np  # noqa: PLC0415
        probs = self.model.predict_proba(texts)
        return np.asarray(probs)

    def save(self, dir_: Path):
        self.model.save_pretrained(str(dir_))
        (dir_ / "classes_.json").write_text(json.dumps(self.classes_))

    @classmethod
    def load(cls, dir_: Path):
        from setfit import SetFitModel  # noqa: PLC0415
        inst = cls()
        inst.model = SetFitModel.from_pretrained(str(dir_))
        inst.classes_ = json.loads((dir_ / "classes_.json").read_text())
        return inst


# ── commands ────────────────────────────────────────────────────────────────

def _gather_training_data(project_dir: Path, gallery_path: Path, extras: list[Path], include_panel_labels: bool) -> list[dict]:
    """Return [{id, text, label}] from gallery + optional confirmed panel labels."""
    items = []
    gallery = json.loads(gallery_path.read_text(encoding="utf-8"))
    for e in gallery:
        items.append({"id": e["id"], "text": e["text"], "label": e["label"]})

    if include_panel_labels:
        for extra_path in extras:
            if not extra_path.exists():
                continue
            for line in extra_path.read_text(encoding="utf-8").splitlines():
                if not line.strip():
                    continue
                r = json.loads(line)
                # Only include panel-unanimous / category-D items (safe labels)
                if r.get("provenance") in ("panel-unanimous",) and r.get("category") in (None, "D"):
                    items.append({"id": r["id"], "text": r["text"], "label": r["label"]})

    # Dedupe on id (gallery wins)
    seen = set()
    unique = []
    for it in items:
        if it["id"] in seen:
            continue
        seen.add(it["id"])
        unique.append(it)
    return unique


def cmd_train(project_dir: Path, gallery: Path, extras: list[Path], output_dir: Path, backend: str) -> None:
    import numpy as np  # noqa: PLC0415
    from sklearn.model_selection import cross_val_score  # noqa: PLC0415

    cfg = _read_config(project_dir)
    include_panel = (cfg.get("train", {}) or {}).get("include_panel_labels", True)

    train = _gather_training_data(project_dir, gallery, extras, include_panel)
    if len(train) < 4:
        raise ValueError(f"need ≥ 4 training items, have {len(train)}")

    output_dir.mkdir(parents=True, exist_ok=True)
    (output_dir / "label_encoder.json").write_text(
        json.dumps(sorted({it["label"] for it in train})), encoding="utf-8"
    )

    if backend == "logreg":
        X, ids = _load_vectors(project_dir, train)
        y = np.asarray([it["label"] for it in train])
        m = _LogRegBackend()
        m.fit(X, y)
        m.to_pickle(output_dir / "model.pkl")
        # CV
        try:
            scores = cross_val_score(m.clf, X, y, cv=min(5, len(set(y))), scoring="f1_macro")
            cv_f1 = float(scores.mean())
        except Exception:
            cv_f1 = None
        metrics = {"backend": backend, "n_train": len(train), "classes": m.classes_, "cv_f1_macro": cv_f1}

    elif backend == "setfit":
        texts = [it["text"] for it in train]
        y = [it["label"] for it in train]
        m = _SetFitBackend()
        m.fit(texts, y)
        model_dir = output_dir / "model"
        m.save(model_dir)
        metrics = {"backend": backend, "n_train": len(train), "classes": m.classes_, "cv_f1_macro": None}

    else:
        raise ValueError(f"unknown backend: {backend}")

    (output_dir / "train_metrics.json").write_text(json.dumps(metrics, indent=2), encoding="utf-8")

    # Update 'latest' symlink
    latest = output_dir.parent / "latest"
    try:
        if latest.is_symlink() or latest.exists():
            latest.unlink()
        latest.symlink_to(output_dir.name)
    except OSError:
        pass  # Windows / restricted filesystems

    print(f"trained: backend={backend}, n_train={len(train)}, cv_f1={metrics.get('cv_f1_macro')}")


def _load_model(model_dir: Path):
    pkl = model_dir / "model.pkl"
    if pkl.exists():
        return "logreg", _LogRegBackend.from_pickle(pkl)
    setfit_dir = model_dir / "model"
    if setfit_dir.exists():
        return "setfit", _SetFitBackend.load(setfit_dir)
    raise FileNotFoundError(f"no model found in {model_dir}")


def cmd_predict(project_dir: Path, model_dir: Path, input_jsonl: Path, output_jsonl: Path) -> None:
    import numpy as np  # noqa: PLC0415

    backend, m = _load_model(model_dir)
    items = [json.loads(l) for l in input_jsonl.read_text(encoding="utf-8").splitlines() if l.strip()]

    if backend == "logreg":
        X, ids = _load_vectors(project_dir, items)
        probs = m.predict_proba(X)
        classes = m.classes_
    else:
        texts = [it["text"] for it in items]
        probs = m.predict_proba_texts(texts)
        classes = m.classes_
        ids = [it["id"] for it in items]

    lines = []
    for i, it in enumerate(items):
        p = probs[i]
        all_probs = {classes[j]: float(p[j]) for j in range(len(classes))}
        top = sorted(all_probs.items(), key=lambda kv: kv[1], reverse=True)
        top1, top2 = top[0], top[1] if len(top) > 1 else (None, 0.0)
        margin = float(top1[1] - (top2[1] if top2 else 0.0))
        entropy = float(-(p * np.log(p + 1e-12)).sum())
        lines.append(json.dumps({
            "id": it["id"],
            "label": top1[0],
            "prob": float(top1[1]),
            "margin": margin,
            "entropy": entropy,
            "all_probs": all_probs,
        }))

    output_jsonl.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"predict: {len(items)} items, backend={backend}")


def cmd_uncertainty(project_dir: Path, model_dir: Path, input_jsonl: Path, output_jsonl: Path, top_k: int, metric: str) -> None:
    # Run predict in-place then rank
    import tempfile
    with tempfile.NamedTemporaryFile("w", suffix=".jsonl", delete=False) as tf:
        tmp = Path(tf.name)
    try:
        cmd_predict(project_dir, model_dir, input_jsonl, tmp)
        rows = [json.loads(l) for l in tmp.read_text(encoding="utf-8").splitlines() if l.strip()]
        key = "entropy" if metric == "entropy" else None
        if key == "entropy":
            rows.sort(key=lambda r: r["entropy"], reverse=True)
        else:
            # margin ascending = hardest first
            rows.sort(key=lambda r: r["margin"])
        out = rows[:top_k]
        output_jsonl.write_text("\n".join(json.dumps(r) for r in out) + "\n", encoding="utf-8")
        print(f"uncertainty: top {len(out)} by {metric}")
    finally:
        try:
            tmp.unlink()
        except FileNotFoundError:
            pass


def cmd_hard_mining(project_dir: Path, model_dir: Path, input_jsonl: Path, exclude_json: Path, output_jsonl: Path, top_k: int) -> None:
    # Exclude items already in gallery
    exclude_ids = set()
    if exclude_json.exists():
        gal = json.loads(exclude_json.read_text(encoding="utf-8"))
        exclude_ids = {e["id"] for e in gal}

    items = [json.loads(l) for l in input_jsonl.read_text(encoding="utf-8").splitlines() if l.strip()]
    filtered = [it for it in items if it["id"] not in exclude_ids]

    import tempfile
    with tempfile.NamedTemporaryFile("w", suffix=".jsonl", delete=False) as tf:
        tmp = Path(tf.name)
    try:
        tmp.write_text("\n".join(json.dumps(it) for it in filtered) + "\n", encoding="utf-8")
        cmd_uncertainty(project_dir, model_dir, tmp, output_jsonl, top_k, "margin")
    finally:
        try:
            tmp.unlink()
        except FileNotFoundError:
            pass


# ── entrypoint ──────────────────────────────────────────────────────────────

def main() -> None:
    p = argparse.ArgumentParser(description="subjective-label classifier utilities")
    p.add_argument("--project-dir", type=Path, required=True)
    sub = p.add_subparsers(dest="cmd", required=True)

    pt = sub.add_parser("train")
    pt.add_argument("--backend", default="logreg", choices=["logreg", "setfit"])
    pt.add_argument("--gallery", type=Path, required=True)
    pt.add_argument("--extra", type=Path, nargs="*", default=[], help="optional panel_labels.jsonl files")
    pt.add_argument("--output", type=Path, required=True, help="output dir (e.g. cache/classifier/iter_N/)")

    pp = sub.add_parser("predict")
    pp.add_argument("--model", type=Path, required=True, help="model dir written by train")
    pp.add_argument("--input", type=Path, required=True)
    pp.add_argument("--output", type=Path, required=True)

    pu = sub.add_parser("uncertainty")
    pu.add_argument("--model", type=Path, required=True)
    pu.add_argument("--input", type=Path, required=True)
    pu.add_argument("--output", type=Path, required=True)
    pu.add_argument("--top-k", type=int, default=100)
    pu.add_argument("--metric", default="margin", choices=["margin", "entropy"])

    ph = sub.add_parser("hard_mining")
    ph.add_argument("--model", type=Path, required=True)
    ph.add_argument("--input", type=Path, required=True)
    ph.add_argument("--exclude", type=Path, required=True, help="gallery.json (ids to exclude)")
    ph.add_argument("--output", type=Path, required=True)
    ph.add_argument("--top-k", type=int, default=50)

    args = p.parse_args()
    if args.cmd == "train":
        cmd_train(args.project_dir, args.gallery, args.extra, args.output, args.backend)
    elif args.cmd == "predict":
        cmd_predict(args.project_dir, args.model, args.input, args.output)
    elif args.cmd == "uncertainty":
        cmd_uncertainty(args.project_dir, args.model, args.input, args.output, args.top_k, args.metric)
    elif args.cmd == "hard_mining":
        cmd_hard_mining(args.project_dir, args.model, args.input, args.exclude, args.output, args.top_k)


if __name__ == "__main__":
    main()
