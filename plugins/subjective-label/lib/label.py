"""Generic LLM labeler for the subjective-label engine (canonical; S0).

Turns a guideline version into predictions: load `guideline/versions/<v>.md`
as the system prompt, label every item with one or more engines. The label set
is READ FROM CONFIG (`labels.values`) or `--labels` — nothing here is frozen to
HIGH/LOW/NONE or to any construct. Ported from the per-task
`prompt_llm_labeler.py` (B01–B03) and de-specialized.

Two engines act as two independent annotators → their pairwise agreement is a
reliability signal (NOT ground truth; see note-update.md).

Usage:
    python lib/label.py --project-dir <task> --version v01 --engine both
    python lib/label.py --project-dir <task> --version v01 --labels HIGH,LOW,NONE
    python lib/label.py --project-dir <task> --version v01 --input eval/anchor_set.jsonl --tag anchor

Output: <project>/eval/per_version/<tag>_<engine>_results.jsonl
Config source: <project>/config.yaml
    labels: {values: [...], type: categorical|ordinal}
    labeler: {engines: {claude_sdk: {model: haiku}, codex: {model: gpt-5.5}}}  # optional overrides
"""

import argparse
import asyncio
import json
import re
import time
from pathlib import Path


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


def _output_contract(labels: list[str]) -> str:
    opts = "|".join(labels)
    return (
        "\n\n---\n"
        "You are labeling ONE item for the dimension above.\n"
        "Respond with a single line of JSON and nothing else:\n"
        f'{{"label": "{opts}", "confidence": 0.0-1.0, "reason": "<=12 words"}}\n'
        f"The label MUST be exactly one of {', '.join(labels)}."
    )


def _make_parser(labels: list[str]):
    upper = {l.upper(): l for l in labels}
    # match longest label first so substrings don't shadow (e.g. LOW vs SLOW)
    ordered = sorted(labels, key=len, reverse=True)

    def parse_label(raw: str) -> dict:
        text = (raw or "").strip()
        m = re.search(r"\{.*\}", text, re.DOTALL)
        if m:
            try:
                obj = json.loads(m.group(0))
                lab = str(obj.get("label", "")).upper().strip()
                if lab in upper:
                    return {"label": upper[lab], "confidence": obj.get("confidence"),
                            "reason": obj.get("reason", ""), "parse": "json"}
            except json.JSONDecodeError:
                pass
        up = text.upper()
        for lab in ordered:
            if re.search(rf"\b{re.escape(lab.upper())}\b", up):
                return {"label": lab, "confidence": None, "reason": "", "parse": "regex"}
        return {"label": "PARSE_ERROR", "confidence": None, "reason": text[:120], "parse": "fail"}

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


ENGINES = {"claude_sdk": label_claude_sdk, "codex": label_codex}
DEFAULT_MODEL = {"claude_sdk": "haiku", "codex": "gpt-5.5"}


async def run_engine(project_dir: Path, engine: str, version: str, tag: str,
                     system_prompt: str, items: list, parse_label, model: str,
                     concurrency: int = 4):
    fn = ENGINES[engine]
    sem = asyncio.Semaphore(concurrency)
    results = [None] * len(items)

    async def one(i, item):
        async with sem:
            t0 = time.time()
            try:
                raw = await fn(system_prompt, item["text"], model)
                parsed = parse_label(raw)
                err = None
            except Exception as e:
                raw, parsed, err = "", {"label": "ERROR", "parse": "exception"}, f"{type(e).__name__}: {e}"
            results[i] = {
                "anchor_idx": item["anchor_idx"], "id": item["id"], "engine": engine,
                "version": version, "pred": parsed["label"],
                "confidence": parsed.get("confidence"), "reason": parsed.get("reason", ""),
                "elapsed_s": round(time.time() - t0, 2), "error": err,
            }
            print(f"  [{engine}] {item['anchor_idx']:>2}/{len(items)}  {results[i]['pred']:<12} "
                  f"({results[i]['elapsed_s']}s)" + (f"  ERR {err}" if err else ""), flush=True)

    await asyncio.gather(*(one(i, it) for i, it in enumerate(items)))

    out = project_dir / "eval" / "per_version" / f"{tag}_{engine}_results.jsonl"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text("".join(json.dumps(r, ensure_ascii=False) + "\n" for r in results))
    n_ok = sum(1 for r in results if r["pred"] not in ("PARSE_ERROR", "ERROR"))
    print(f"  -> {engine}: {n_ok}/{len(items)} valid labels  written {out.name}")
    return results


async def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--project-dir", type=Path, required=True)
    ap.add_argument("--version", default="v01", help="guideline version = system prompt")
    ap.add_argument("--engine", default="both", choices=["claude_sdk", "codex", "both"])
    ap.add_argument("--labels", default=None, help="override config labels, e.g. HIGH,LOW,NONE")
    ap.add_argument("--input", default=None, help="jsonl of items (default: eval/anchor_set.jsonl)")
    ap.add_argument("--tag", default=None, help="output-name prefix (default: version)")
    ap.add_argument("--concurrency", type=int, default=4)
    args = ap.parse_args()

    pd = args.project_dir.resolve()
    cfg = _read_config(pd)
    labels = _resolve_labels(cfg, args.labels)
    parse_label = _make_parser(labels)

    src = Path(args.input) if args.input else pd / "eval" / "anchor_set.jsonl"
    if not src.is_absolute():
        src = pd / src
    items = [json.loads(l) for l in src.read_text().splitlines() if l.strip()]
    for i, it in enumerate(items):
        it.setdefault("anchor_idx", i + 1)

    gpath = pd / "guideline" / "versions" / f"{args.version}.md"
    if not gpath.exists():
        gpath = pd / "guideline" / "guideline.md"
    system_prompt = gpath.read_text().strip() + _output_contract(labels)

    tag = args.tag or args.version
    eng_cfg = (cfg.get("labeler") or {}).get("engines") or {}
    engines = ["claude_sdk", "codex"] if args.engine == "both" else [args.engine]

    print("=" * 60)
    print(f"LLM Labeler — guideline {args.version} — labels {labels}")
    print(f"  items: {len(items)}   engines: {engines}")
    print("=" * 60)
    for eng in engines:
        model = (eng_cfg.get(eng) or {}).get("model", DEFAULT_MODEL[eng])
        print(f"\n[{eng} · {model}]")
        await run_engine(pd, eng, args.version, tag, system_prompt, items, parse_label,
                         model, args.concurrency)


if __name__ == "__main__":
    asyncio.run(main())
