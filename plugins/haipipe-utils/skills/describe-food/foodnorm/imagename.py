"""
Stage 0: image -> food name.

The cohorts that photograph a meal instead of typing it leave a `FoodName` that
names no food -- CGMacros writes the literal string 'Unknown' on all 1,644 of
its diet rows, and the photo carries the meal. Every stage after this one takes
a STRING, so this stage's whole job is to produce one:

    photo(s)  ->  "scrambled eggs; toast"  ->  dialect -> retrieve -> aggregate

That seam is the point. A derived name enters the pipeline as an `item_list` or
`single_item`, shapes the benchmark already scores, so an image engine is graded
by the machinery that already exists rather than by a second benchmark.

**The engine is swappable, exactly as the corpus is.**

    FOODNORM_IMAGE_ENGINE=null     the default -- today's behaviour, made explicit
    FOODNORM_IMAGE_ENGINE=claude   Claude vision through the OAuth `claude` CLI
    FOODNORM_IMAGE_ENGINE=replay   names a previous run already bought, free

`null` is a real engine and not an absence: it gives the benchmark a baseline row
to compare against instead of a blank.

**Auth is OAuth, never an API key.** The engine shells out to the `claude` CLI,
which holds the user's own OAuth session. The three API-key variables are
stripped from the subprocess environment so a proxy or key in `env.sh` cannot
silently take over the call.

⚠️ **A derived name is not a typed name.** The library's existing contract says a
confidently wrong food is worse than a missing one; stage 0 is the easiest place
in the system to violate it, because a model's guess is the same TYPE as a
human's entry. So an engine returns a record carrying its own confidence, and
the caller writes `NameSource` / `NameConf` beside the name. A row whose food was
invented must stay distinguishable from a row whose food was reported.
"""
import json
import os
import pathlib
import subprocess
import tempfile
from collections import namedtuple
from typing import Callable, Dict, List, Optional, Sequence

# food_name  the derived string, in the dialect layer's own grammar ('a; b; c')
# portion_g  grams, when the engine estimated one; None is the normal case
# conf       0-1, the engine's confidence in the NAMING (not in the nutrition)
# engine     which backend produced it, for the NameSource column
# raw        the engine's unparsed reply, kept for audit
ImageRead = namedtuple("ImageRead", "food_name portion_g conf engine raw")

# Model default. Haiku is cheaper and was wrong on the first CGMacros photo we
# checked (beaten eggs in a bowl, read as 'sausage; oil'), which is the corpus's
# characteristic difficulty rather than an unlucky draw: many frames are
# mid-preparation, not a plated meal. Override with FOODNORM_IMAGE_MODEL.
DEFAULT_MODEL = os.environ.get("FOODNORM_IMAGE_MODEL", "claude-sonnet-5")

# Meals per CLI call. The Claude Code system prompt is billed per CALL, not per
# image, so batching is the only real cost lever: one meal per call measured
# $0.039, and the prompt is ~50k cached tokens of that.
DEFAULT_BATCH = int(os.environ.get("FOODNORM_IMAGE_BATCH", "10"))

# Seconds for one CLI call, scaled by batch size.
TIMEOUT_PER_MEAL = 60

_PROMPT_HEAD = """You are reading meal photographs from a nutrition study.

For each MEAL below, read every image listed for it and name the food.

Rules:
- Name GENERIC foods, the way a food composition table would: "scrambled eggs",
  not "Mom's Sunday eggs"; "white rice", not "Uncle Ben's".
- Separate multiple foods with '; '. Lowercase. No portions, no brands, no
  adjectives about appearance.
- Two images for one meal are the SAME meal photographed BEFORE and AFTER
  eating. Name the food from whichever image shows more food.
- A photo may show ingredients or cooking in progress rather than a served
  plate. Name the DISH BEING MADE, or the ingredients if no dish is evident.
- If no food is visible at all, use "" and conf 0.
- conf is 0-1: your confidence that the naming is correct.

Return ONLY a JSON array, one object per meal, in the same order, no prose:
[{"meal": 1, "foods": "scrambled eggs; toast", "conf": 0.8}]
"""


def null_engine(meals: Sequence[Sequence[str]], **kw) -> List[Optional[ImageRead]]:
    """The default. Returns nothing for every meal, which is today's behaviour.

    It exists so 'we did not read the images' is a configuration the benchmark
    can name and score, rather than an empty cell.
    """
    return [None] * len(meals)


def _claude_env() -> Dict[str, str]:
    """The subprocess environment: this repo's env.sh exports a proxy base URL
    and an auth token, and either would route the call away from the user's
    OAuth session. Strip all three key variables so the CLI uses OAuth only.
    """
    env = dict(os.environ)
    for k in ("ANTHROPIC_BASE_URL", "ANTHROPIC_AUTH_TOKEN", "ANTHROPIC_API_KEY"):
        env.pop(k, None)
    return env


def _parse_reply(text: str, n: int) -> List[Optional[dict]]:
    """The CLI returns free text; recover the JSON array or give up cleanly.

    Never raises. A malformed reply costs the batch its names, not the run.
    """
    if not text:
        return [None] * n
    s = text.strip()
    if s.startswith("```"):
        s = s.split("\n", 1)[-1].rsplit("```", 1)[0]
    start, end = s.find("["), s.rfind("]")
    if start == -1 or end == -1:
        return [None] * n
    try:
        parsed = json.loads(s[start:end + 1])
    except (ValueError, TypeError):
        return [None] * n
    if not isinstance(parsed, list):
        return [None] * n

    out: List[Optional[dict]] = [None] * n
    for i, item in enumerate(parsed):
        if not isinstance(item, dict):
            continue
        # Trust the model's own 'meal' index when it is sane, position otherwise.
        idx = item.get("meal")
        pos = (idx - 1) if isinstance(idx, int) and 1 <= idx <= n else i
        if 0 <= pos < n:
            out[pos] = item
    return out


def claude_engine(
    meals: Sequence[Sequence[str]],
    model: str = None,
    batch: int = None,
    verbose: bool = False,
) -> List[Optional[ImageRead]]:
    """Claude vision through the OAuth `claude` CLI, batched.

    Args:
        meals: one entry per meal, each a sequence of ABSOLUTE image paths.
               Path joining is the caller's, because where a cohort keeps its
               photos is a property of that cohort and not of this stage.
        model: model id; defaults to FOODNORM_IMAGE_MODEL or sonnet.
        batch: meals per CLI call; defaults to FOODNORM_IMAGE_BATCH.

    Returns one entry per input meal, None where the read failed. Never raises:
    a dead subprocess must cost the batch its names, not the enrichment run.
    """
    model = model or DEFAULT_MODEL
    batch = batch or DEFAULT_BATCH
    out: List[Optional[ImageRead]] = []

    # Run from an empty directory. The CLI loads CLAUDE.md, skills and settings
    # from its cwd into the system prompt, and every one of those tokens is
    # billed on every call for a job that needs none of them.
    with tempfile.TemporaryDirectory(prefix="foodnorm-img-") as bare:
        for start in range(0, len(meals), batch):
            chunk = list(meals[start:start + batch])
            lines = [_PROMPT_HEAD]
            for i, paths in enumerate(chunk, 1):
                lines.append(f"MEAL {i}: " + ", ".join(paths))
            prompt = "\n".join(lines)

            try:
                proc = subprocess.run(
                    ["claude", "-p", prompt,
                     "--allowedTools", "Read",
                     "--model", model,
                     "--output-format", "json"],
                    cwd=bare, env=_claude_env(), capture_output=True, text=True,
                    timeout=TIMEOUT_PER_MEAL * max(len(chunk), 1),
                )
                payload = json.loads(proc.stdout)
                text = payload.get("result", "")
                if verbose:
                    print(f"  meals {start + 1}-{start + len(chunk)}: "
                          f"${payload.get('total_cost_usd', 0):.4f} "
                          f"{payload.get('duration_ms', 0)}ms")
            except (subprocess.TimeoutExpired, subprocess.SubprocessError,
                    ValueError, OSError, KeyError) as e:
                if verbose:
                    print(f"  meals {start + 1}-{start + len(chunk)}: FAILED {e}")
                out.extend([None] * len(chunk))
                continue

            for item in _parse_reply(text, len(chunk)):
                if not item or not str(item.get("foods", "")).strip():
                    out.append(None)
                    continue
                try:
                    conf = float(item.get("conf", 0.0))
                except (TypeError, ValueError):
                    conf = 0.0
                out.append(ImageRead(
                    food_name=str(item["foods"]).strip(),
                    portion_g=None,
                    conf=conf,
                    engine=f"claude-vision:{model}",
                    raw=json.dumps(item, ensure_ascii=False),
                ))

    return out


def replay_engine(meals: Sequence[Sequence[str]], path: str = None,
                  verbose: bool = False, **kw) -> List[Optional[ImageRead]]:
    """Re-serve names a previous run already bought, keyed by image path.

    A model call is the expensive part of this lane and the LEAST likely thing
    to need repeating: every methodology fix -- a corrected gold filter, a
    different bank, a calibration -- changes what happens AFTER the name. Without
    replay each of those costs a fresh run of the same photos, which is how a
    benchmark quietly becomes too expensive to correct.

    Reads FOODNORM_IMAGE_REPLAY, a JSON object mapping '\n'-joined image paths
    to {"foods": str, "conf": float, "engine": str}. A meal absent from the file
    returns None, exactly as a failed read would.
    """
    path = path or os.environ.get("FOODNORM_IMAGE_REPLAY")
    if not path:
        raise ValueError("replay engine needs FOODNORM_IMAGE_REPLAY or path=")
    book = json.loads(pathlib.Path(path).read_text())

    out: List[Optional[ImageRead]] = []
    hit = 0
    for paths in meals:
        item = book.get("\n".join(paths))
        if not item or not str(item.get("foods", "")).strip():
            out.append(None)
            continue
        hit += 1
        out.append(ImageRead(
            food_name=str(item["foods"]).strip(),
            portion_g=item.get("portion_g"),
            conf=float(item.get("conf", 0.0)),
            engine=str(item.get("engine", "replay")),
            raw=json.dumps(item, ensure_ascii=False),
        ))
    if verbose:
        print(f"  replay: {hit}/{len(meals)} meals served from {path}")
    return out


ENGINES: Dict[str, Callable] = {
    "null": null_engine,
    "claude": claude_engine,
    "replay": replay_engine,
}


def get_engine(name: str = None) -> Callable:
    """Resolve an engine by name, or by FOODNORM_IMAGE_ENGINE, defaulting to null.

    An unknown name raises rather than falling back: silently reading no images
    when the caller asked for vision is the failure this whole module's
    provenance discipline exists to prevent.
    """
    name = name or os.environ.get("FOODNORM_IMAGE_ENGINE", "null")
    if name not in ENGINES:
        raise ValueError(f"unknown image engine {name!r}; have {sorted(ENGINES)}")
    return ENGINES[name]


def read_images(meals: Sequence[Sequence[str]], engine=None, **kw) -> List[Optional[ImageRead]]:
    """The door: meals of absolute image paths -> one ImageRead or None each."""
    fn = engine if callable(engine) else get_engine(engine)
    return fn(meals, **kw)
