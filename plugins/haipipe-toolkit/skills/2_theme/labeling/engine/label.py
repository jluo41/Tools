"""Generic LLM labeler for the subjective-label engine (canonical; S0).

Turns a guideline version into predictions: load `guideline/versions/<v>.md`
as the system prompt, label every item with one or more engines. The label set
is READ FROM CONFIG (`labels.values`) or `--labels` — nothing here is frozen to
HIGH/LOW/NONE or to any construct. Ported from the per-task
`prompt_llm_labeler.py` (B01–B03) and de-specialized.

Two engines act as two independent annotators → their pairwise agreement is a
reliability signal (NOT ground truth; see note-update.md).

Replies are accepted as valid JSON only (optionally inside one ``` fence). Anything
else is `pred: PARSE_ERROR`, `status: failed`, with a short `reason` error code; the
parser never guesses a label from free text and never stores raw model output.
On a v2 job root nothing is sent to a model until G0 passes (engine/gates.py),
and model inputs are restricted to exact text for canonical eligible items in
the Page's fenced development corpus. Sealed test text is never read here.

As a tool (b15 s42-D54): ``lm_labeler(job_root, item_ids, guideline, engine, model=...)`` returns each item's
label, region (when the config has regions), confidence and reason. The model reads the turns before the
item, then the reply it judges. Engines: claude_sdk, codex, openai_api, and two OpenAI-compatible ones for
the panel of open models: ``openrouter`` (OPENROUTER_API_KEY; e.g. qwen/qwen3-30b-a3b, google/gemma-3-27b-it)
and ``ollama`` (a local server; e.g. gpt-oss:20b). A missing key holds before any item is sent.

Usage:
    python engine/label.py --project-dir <task> --version v01 --engine both
    python engine/label.py --project-dir <task> --version G_01 --engine openrouter --model google/gemma-3-27b-it
    python engine/label.py --project-dir <task> --version v01 --labels HIGH,LOW,NONE
    python engine/label.py --project-dir <task> --version v01 --input eval/anchor_set.jsonl --tag anchor

Output: <project>/eval/per_version/<tag>_<engine>_results.jsonl
Config source: <project>/config.yaml
    labels: {values: [...], type: categorical|ordinal}
    labeler: {engines: {claude_sdk: {model: haiku}, codex: {model: gpt-5.5},
                        openai_api: {model: gpt-4o-mini}}}  # optional overrides
"""

from __future__ import annotations

import argparse
import asyncio
import json
import os
import re
import sys
import time
from pathlib import Path

_ENGINE_DIR = str(Path(__file__).resolve().parent)
if _ENGINE_DIR not in sys.path:
    sys.path.insert(0, _ENGINE_DIR)
from gates import GateHold, guard_job_root  # noqa: E402

_FENCE = re.compile(r"\A```(?:json)?[ \t]*\n?(.*?)\n?```\Z", re.DOTALL | re.IGNORECASE)


def _read_config(project_dir: Path) -> dict:
    import yaml  # noqa: PLC0415
    p = project_dir / "config.yaml"
    return (yaml.safe_load(p.read_text(encoding="utf-8")) or {}) if p.exists() else {}


def _resolve_labels(cfg: dict, override: str | None) -> list[str]:
    if override:
        return [x.strip() for x in override.split(",") if x.strip()]
    labels = (cfg.get("labels") or {}).get("values")
    if not labels:
        raise SystemExit(
            "no label set: add `labels.values` to config.yaml or pass --labels A,B,C")
    return [str(x) for x in labels]


def _regions(cfg: dict) -> list[str] | None:
    values = (cfg.get("regions") or {}).get("values")
    return [str(v) for v in values] if values else None


def _canonical_v2_items(project_dir: Path, cfg: dict, input_rows: list[dict]) -> list[dict]:
    """Resolve v2 inputs only through the Page's canonical eligible corpus."""
    if cfg.get("schema_version") != "subjective-label/v2":
        return input_rows

    corpus_cfg = cfg.get("corpus") if isinstance(cfg.get("corpus"), dict) else {}
    text_field = str(corpus_cfg.get("text_field") or "text")
    context_field = str(corpus_cfg.get("context_field") or "context_prev")
    corpus_path = project_dir / "corpus" / "items.jsonl"
    eligible: dict[str, str] = {}
    context: dict[str, str] = {}
    try:
        corpus_rows = [
            json.loads(line)
            for line in corpus_path.read_text(encoding="utf-8").splitlines()
            if line.strip()
        ]
    except (OSError, json.JSONDecodeError) as error:
        raise ValueError(f"canonical v2 corpus is unavailable or invalid: {type(error).__name__}") from None

    for row in corpus_rows:
        if not isinstance(row, dict):
            raise ValueError("canonical v2 corpus rows must be objects")
        if row.get("population_status") != "eligible":
            continue
        raw_id = row.get("item_id")
        item_id = str(raw_id).strip() if raw_id is not None else ""
        text = row.get(text_field)
        if not item_id or not isinstance(text, str) or not text.strip():
            raise ValueError("canonical eligible corpus rows need item_id and non-empty configured text")
        if item_id in eligible:
            raise ValueError(f"canonical eligible corpus has duplicate item_id {item_id!r}")
        eligible[item_id] = text
        context[item_id] = str(row.get(context_field) or "")

    canonical: list[dict] = []
    for source in input_rows:
        if not isinstance(source, dict):
            raise ValueError("v2 model input rows must be objects")
        raw_id = source.get("item_id", source.get("id"))
        item_id = str(raw_id).strip() if raw_id is not None else ""
        if not item_id or item_id not in eligible:
            raise ValueError("v2 model input is not a canonical eligible corpus item")
        text = eligible[item_id]
        for field in {"text", text_field}:
            supplied = source.get(field)
            if supplied is not None and supplied != text:
                raise ValueError(f"v2 model input text does not match canonical eligible item {item_id!r}")
        row = dict(source)
        row.update({"item_id": item_id, "id": item_id, "text": text, "context": context[item_id],
                    "population_status": "eligible"})
        canonical.append(row)
    return canonical


def _output_contract(labels: list[str], regions: list[str] | None = None) -> str:
    opts = "|".join(labels)
    region = f'"region": "{"|".join(regions)}", ' if regions else ""
    return (
        "\n\n---\n"
        "You are labeling ONE item for the dimension above.\n"
        "Respond with a single line of JSON and nothing else:\n"
        f'{{"label": "{opts}", {region}"confidence": 0.0-1.0, "reason": "<=12 words"}}\n'
        f"The label MUST be exactly one of {', '.join(labels)}."
        + (f" The region says where the item sits: one label clearly ({', '.join(regions[:len(labels)])}),"
           f" or between labels ({', '.join(regions[len(labels):])})." if regions else "")
    )


def _parse_failure(code: str) -> dict:
    return {"label": "PARSE_ERROR", "region": None, "confidence": None, "reason": f"parse_error:{code}",
            "parse": "fail", "status": "failed"}


def _make_parser(labels: list[str], regions: list[str] | None = None):
    upper = {l.upper(): l for l in labels}
    region_upper = {r.upper(): r for r in regions or []}

    def parse_label(raw: str) -> dict:
        text = (raw or "").strip()
        if not text:
            return _parse_failure("empty_output")
        fenced = _FENCE.match(text)
        if fenced:
            text = fenced.group(1).strip()
        try:
            obj = json.loads(text)
        except json.JSONDecodeError:
            return _parse_failure("not_json")
        if not isinstance(obj, dict):
            return _parse_failure("not_json_object")
        lab = obj.get("label")
        if not isinstance(lab, str):
            return _parse_failure("label_missing")
        if lab.strip().upper() not in upper:
            return _parse_failure("label_not_in_set")
        region = obj.get("region")
        if regions:
            if not isinstance(region, str) or region.strip().upper() not in region_upper:
                return _parse_failure("region_not_in_set")
            region = region_upper[region.strip().upper()]
        return {"label": upper[lab.strip().upper()], "region": region if regions else None,
                "confidence": obj.get("confidence"), "reason": obj.get("reason", ""), "parse": "json",
                "status": "ok"}

    return parse_label


# ── Transports (OAuth engines; mirror B01_llm_open_rec/00_llm_engine_test) ──

async def label_claude_sdk(system_prompt: str, text: str, model: str = "haiku") -> str:
    from claude_agent_sdk import ClaudeSDKClient, ClaudeAgentOptions
    from claude_agent_sdk.types import AssistantMessage, TextBlock
    opts = ClaudeAgentOptions(allowed_tools=[], permission_mode="acceptEdits",
                              max_turns=1, model=model, system_prompt=system_prompt)
    out = ""
    async with ClaudeSDKClient(options=opts) as c:
        await c.query(text)
        async for m in c.receive_response():
            if isinstance(m, AssistantMessage):
                for b in m.content:
                    if isinstance(b, TextBlock):
                        out = b.text
    return out


async def label_codex(system_prompt: str, text: str, model: str = "gpt-5.5") -> str:
    from codex_oauth import CodexOAuthClient
    async with CodexOAuthClient(model=model) as c:
        r = await c.complete(messages=[{"role": "system", "content": system_prompt},
                                       {"role": "user", "content": text}])
    return r.content


async def label_openai_api(
    system_prompt: str, text: str, model: str = "gpt-4o-mini"
) -> str:
    """OpenAI API-key transport; never falls back to Codex OAuth."""
    from openai import AsyncOpenAI

    client = AsyncOpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
    response = await client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": text},
        ],
        temperature=0,
    )
    return response.choices[0].message.content or ""


# Open models through an OpenAI-compatible endpoint (b15 s42-D52, D54: the panel E). OpenRouter serves many open
# models by name (qwen/…, google/gemma-…); Ollama serves the ones pulled on this machine.
OPEN_ENDPOINTS = {
    "openrouter": ("https://openrouter.ai/api/v1", "OPENROUTER_API_KEY"),
    "ollama": ("http://localhost:11434/v1", None),
}


def _open_engine(name: str):
    base_url, key_env = OPEN_ENDPOINTS[name]

    async def label_open(system_prompt: str, text: str, model: str) -> str:
        from openai import AsyncOpenAI

        client = AsyncOpenAI(base_url=os.environ.get(f"{name.upper()}_BASE_URL", base_url),
                             api_key=os.environ.get(key_env) if key_env else name)
        response = await client.chat.completions.create(
            model=model,
            messages=[{"role": "system", "content": system_prompt}, {"role": "user", "content": text}],
            temperature=0,
        )
        return response.choices[0].message.content or ""

    return label_open


ENGINES = {
    "claude_sdk": label_claude_sdk,
    "codex": label_codex,
    "openai_api": label_openai_api,
    "openrouter": _open_engine("openrouter"),
    "ollama": _open_engine("ollama"),
}
DEFAULT_MODEL = {
    "claude_sdk": "haiku",
    "codex": "gpt-5.5",
    "openai_api": "gpt-4o-mini",
    "openrouter": "qwen/qwen3-30b-a3b",
    "ollama": "gpt-oss:20b",
}
KEY_ENV = {"openai_api": "OPENAI_API_KEY", "openrouter": "OPENROUTER_API_KEY"}


def _message(item: dict) -> str:
    """What the model reads: the turns before, then the reply it judges."""
    context = str(item.get("context") or "").strip()
    return f"Before:\n{context}\n\nJudge this reply:\n{item['text']}" if context else item["text"]


async def run_engine(project_dir: Path, engine: str, version: str, tag: str,
                     system_prompt: str, items: list, parse_label, model: str,
                     concurrency: int = 4, output_path: Path | None = None):
    guard_job_root(project_dir, "G0")
    fn = ENGINES[engine]
    sem = asyncio.Semaphore(concurrency)
    results = [None] * len(items)

    async def one(i, item):
        async with sem:
            t0 = time.time()
            try:
                raw = await fn(system_prompt, _message(item), model)
                parsed = parse_label(raw)
                err = None
            except Exception as e:
                raw, parsed, err = "", {"label": "ERROR", "parse": "exception",
                                        "status": "failed"}, f"{type(e).__name__}: {e}"
            results[i] = {
                "anchor_idx": item["anchor_idx"], "id": item["id"], "engine": engine, "model": model,
                "version": version, "pred": parsed["label"], "region": parsed.get("region"),
                "status": parsed.get("status", "failed"), "parse": parsed.get("parse"),
                "confidence": parsed.get("confidence"), "reason": parsed.get("reason", ""),
                "elapsed_s": round(time.time() - t0, 2), "error": err,
            }
            print(f"  [{engine}] {item['anchor_idx']:>2}/{len(items)}  {results[i]['pred']:<12} "
                  f"({results[i]['elapsed_s']}s)" + (f"  ERR {err}" if err else ""), flush=True)

    await asyncio.gather(*(one(i, it) for i, it in enumerate(items)))

    out = output_path or (
        project_dir / "eval" / "per_version" / f"{tag}_{engine}_results.jsonl"
    )
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text("".join(json.dumps(r, ensure_ascii=False) + "\n" for r in results))
    n_ok = sum(1 for r in results if r["pred"] not in ("PARSE_ERROR", "ERROR"))
    print(f"  -> {engine}: {n_ok}/{len(items)} valid labels  written {out.name}")
    return results


def _guideline(pd: Path, version: str) -> Path:
    for g in (pd / "policy" / "versions" / version / "guideline.md", pd / "guideline" / "versions" / f"{version}.md",
              pd / "guideline" / "guideline.md"):
        if g.exists():
            return g
    raise SystemExit(f"guideline not found for {version}")


def lm_labeler(job_root: Path, item_ids: list[str], guideline: str, engine: str, *, model: str | None = None,
               output: Path | None = None, concurrency: int = 4) -> list[dict]:
    """b15 s42 lm_labeler(items, guideline, engine): each item's label, region, confidence and reason under one
    guideline version, from one engine (claude_sdk, codex, openai_api, openrouter, ollama). Development items
    only, after G0; nothing is sent when the engine's key is missing."""
    pd = Path(job_root).resolve()
    guard_job_root(pd, "G0")
    if engine not in ENGINES:
        raise SystemExit(f"engine is one of {', '.join(ENGINES)}")
    if KEY_ENV.get(engine) and not os.environ.get(KEY_ENV[engine]):
        raise SystemExit(f"HOLD · {KEY_ENV[engine]} is not configured; no item was transmitted")
    cfg = _read_config(pd)
    labels, regions = _resolve_labels(cfg, None), _regions(cfg)
    items = _canonical_v2_items(pd, cfg, [{"item_id": str(i)} for i in item_ids])
    for n, it in enumerate(items):
        it.setdefault("anchor_idx", n + 1)
    prompt = _guideline(pd, guideline).read_text().strip() + _output_contract(labels, regions)
    model = model or ((cfg.get("labeler") or {}).get("engines") or {}).get(engine, {}).get("model") \
        or DEFAULT_MODEL[engine]
    out = output or pd / "eval" / "per_version" / f"{guideline}_{engine}_{model.replace('/', '_')}_results.jsonl"
    return asyncio.run(run_engine(pd, engine, guideline, guideline, prompt, items, _make_parser(labels, regions),
                                  model, concurrency, out))


async def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--project-dir", type=Path, required=True)
    ap.add_argument("--version", default="v01", help="guideline version = system prompt")
    ap.add_argument(
        "--engine",
        default="both",
        choices=["claude_sdk", "codex", "openai_api", "openrouter", "ollama", "both"],
    )
    ap.add_argument("--labels", default=None, help="override config labels, e.g. HIGH,LOW,NONE")
    ap.add_argument(
        "--input",
        default=None,
        help="jsonl of items (default: corpus/items.jsonl, then legacy eval/anchor_set.jsonl)",
    )
    ap.add_argument("--tag", default=None, help="output-name prefix (default: version)")
    ap.add_argument("--concurrency", type=int, default=4)
    ap.add_argument("--limit", type=int, default=None, help="send only the first N items")
    ap.add_argument("--model", default=None, help="override the selected engine's model")
    ap.add_argument("--output", type=Path, default=None, help="explicit JSONL output path")
    args = ap.parse_args()

    pd = args.project_dir.resolve()
    try:
        guard_job_root(pd, "G0")
    except GateHold as hold:
        raise SystemExit(str(hold)) from None
    cfg = _read_config(pd)
    labels = _resolve_labels(cfg, args.labels)
    regions = _regions(cfg)
    parse_label = _make_parser(labels, regions)
    eng_cfg = (cfg.get("labeler") or {}).get("engines") or {}
    engines = ["claude_sdk", "codex"] if args.engine == "both" else [args.engine]
    for eng in engines:
        if KEY_ENV.get(eng) and not os.environ.get(KEY_ENV[eng]):
            raise SystemExit(f"HOLD · {KEY_ENV[eng]} is not configured; no item was transmitted")

    if args.input:
        src = Path(args.input)
    elif (pd / "corpus" / "items.jsonl").is_file():
        src = pd / "corpus" / "items.jsonl"
    else:
        src = pd / "eval" / "anchor_set.jsonl"
    if not src.is_absolute():
        src = pd / src
    try:
        items = [json.loads(l) for l in src.read_text(encoding="utf-8").splitlines() if l.strip()]
        items = _canonical_v2_items(pd, cfg, items)
    except (OSError, json.JSONDecodeError, ValueError) as error:
        raise SystemExit(f"HOLD · {error}") from None
    if args.limit is not None:
        if args.limit < 1:
            raise SystemExit("--limit must be positive")
        items = items[: args.limit]
    for i, it in enumerate(items):
        it.setdefault("anchor_idx", i + 1)
        it.setdefault("id", it.get("item_id", f"item-{i + 1}"))

    gpath = pd / "policy" / "versions" / args.version / "guideline.md"
    if not gpath.exists():
        gpath = pd / "guideline" / "versions" / f"{args.version}.md"
    if not gpath.exists():
        gpath = pd / "guideline" / "guideline.md"
    if not gpath.exists():
        raise SystemExit(f"guideline not found for {args.version}: {gpath}")
    system_prompt = gpath.read_text().strip() + _output_contract(labels, regions)

    tag = args.tag or args.version

    print("=" * 60)
    print(f"LLM Labeler — guideline {args.version} — labels {labels}")
    print(f"  items: {len(items)}   engines: {engines}")
    print("=" * 60)
    for eng in engines:
        model = args.model or (eng_cfg.get(eng) or {}).get("model") \
            or (os.environ.get("OPENAI_MODEL") if eng == "openai_api" else None) \
            or DEFAULT_MODEL[eng]
        print(f"\n[{eng} · {model}]")
        out = args.output
        if out is not None and not out.is_absolute():
            out = pd / out
        if out is not None and len(engines) > 1:
            raise SystemExit("--output requires exactly one engine")
        await run_engine(pd, eng, args.version, tag, system_prompt, items, parse_label,
                         model, args.concurrency, out)


if __name__ == "__main__":
    asyncio.run(main())
