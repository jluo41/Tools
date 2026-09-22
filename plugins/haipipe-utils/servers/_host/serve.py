#!/usr/bin/env python3
"""
haipipe-utils API host. One process, one port, every normalizer behind its own
prefix. The input goes in the request body, the result comes back in the
response, and nothing is rendered.

    python servers/_host/serve.py                            # 127.0.0.1:8070, every lane
    python servers/_host/serve.py --only insulin,medication  # a subset
    python servers/_host/serve.py --store /path/to/_WorkSpace/ExternalStore
    python servers/_host/serve.py --list                     # what would mount, no import

    curl -s localhost:8070/                                  # the lanes and their routes
    curl -s localhost:8070/healthz                           # which bank each lane serves
    curl -s localhost:8070/insulin/normalize -H 'content-type: application/json' \\
         -d '{"item":"Novolin R"}'

LANES. `servers/api-<noun>/server.py` is a complete FastAPI app with the same
three routes, GET /healthz, POST /normalize, POST /normalize/batch, and the host
mounts it at `/<noun>`. The routes inside a lane did not change when the lane
moved here out of `skills/describe-<noun>/`; a consumer's `<NOUN>NORM_URL` only
gained the prefix (`http://127.0.0.1:8070/food` where it was `:8077`), and the
skill's `client.py` still appends `/normalize/batch` to it.

ARROW. Servers import skills, never the reverse. The host puts
`skills/describe-<noun>/` on sys.path so `<noun>norm` imports as a bare name,
then loads the lane's `server.py` by file under the module name `api_<noun>`,
which is why four files may share the name `server.py`.

BANKS. A lane opens its reference bank from `<NOUN>NORM_DB` or from
`$LOCAL_EXTERNAL_STORE`; `--store` sets that variable before any lane imports.
A lane whose bank is missing still mounts and says so on its own /healthz. A
lane that fails to import is listed under `failed` on the host /healthz and on
stderr, and the other lanes keep serving; `--strict` makes that a non-zero exit.

NOT AUTHENTICATED, bound to 127.0.0.1 by default. Food, exercise, medication
and insulin logs are PHI. Put a gate in front before this listens on a network.
"""
from __future__ import annotations

import argparse
import importlib.util
import inspect
import os
import sys
from contextlib import asynccontextmanager
from pathlib import Path
from typing import Dict, Iterable, List, Optional

HOST = Path(__file__).resolve().parent          # plugins/haipipe-utils/servers/_host
SERVERS = HOST.parent                           # plugins/haipipe-utils/servers
PLUGIN = SERVERS.parent                         # plugins/haipipe-utils
SKILLS = PLUGIN / "skills"

VERSION = "0.2.0"
DEFAULT_HOST = os.environ.get("HAIPIPE_UTILS_HOST", "127.0.0.1")
DEFAULT_PORT = int(os.environ.get("HAIPIPE_UTILS_PORT", "8070"))

# The env var each lane's client.py reads its URL from. Named here so the banner
# and the suite runner print the right one; a lane not listed gets <NOUN>NORM_URL.
URL_VAR = {"food": "FOODNORM_URL", "exercise": "EXNORM_URL",
           "medication": "MEDNORM_URL", "insulin": "INSNORM_URL"}


def url_var(noun: str) -> str:
    return URL_VAR.get(noun, f"{noun.upper()}NORM_URL")


def lane_dir(noun: str) -> Path:
    return SERVERS / f"api-{noun}"


def skill_dir(noun: str) -> Path:
    return SKILLS / f"describe-{noun}"


def package_of(noun: str) -> str:
    """The resolver package the lane imports: the one `*norm/` with an __init__."""
    d = skill_dir(noun)
    if d.is_dir():
        for p in sorted(d.iterdir()):
            if p.is_dir() and p.name.endswith("norm") and (p / "__init__.py").exists():
                return p.name
    return "?"


def lanes() -> List[str]:
    """Every servers/api-<noun>/server.py, by noun, sorted. Discovery, not a list."""
    return sorted(p.name[len("api-"):] for p in SERVERS.glob("api-*")
                  if (p / "server.py").is_file())


def load(noun: str):
    """Import one lane's server.py under the module name api_<noun>, with its
    skill dir on sys.path so `<noun>norm` resolves. Returns the module: its
    `app` is the FastAPI app, its `healthz` the function the host aggregates."""
    skill = skill_dir(noun)
    if not skill.is_dir():
        raise FileNotFoundError(f"lane api-{noun} has no skill at {skill}")
    if str(skill) not in sys.path:
        sys.path.insert(0, str(skill))
    path = lane_dir(noun) / "server.py"
    spec = importlib.util.spec_from_file_location(f"api_{noun}", path)
    mod = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = mod
    spec.loader.exec_module(mod)
    if not hasattr(mod, "app"):
        raise AttributeError(f"{path} defines no `app`")
    return mod


def _lane_health(mod) -> Dict:
    fn = getattr(mod, "healthz", None)
    if fn is None:
        return {"ok": None, "detail": "lane defines no healthz()"}
    try:
        info = dict(fn())
    except Exception as e:                      # HTTPException(503), or a cold bank
        detail = getattr(e, "detail", None) or f"{type(e).__name__}: {e}"
        return {"ok": False, "status": "degraded", "detail": str(detail)}
    info.setdefault("ok", info.get("status", "ok") == "ok")
    return info


def _routes(app) -> List[str]:
    out = []
    for r in app.routes:
        methods = getattr(r, "methods", None)
        path = getattr(r, "path", "")
        if not methods or path in ("/openapi.json", "/docs", "/docs/oauth2-redirect", "/redoc"):
            continue
        for m in sorted(set(methods) - {"HEAD", "OPTIONS"}):
            out.append(f"{m} {path}")
    return sorted(out)


def create_app(only: Optional[Iterable[str]] = None, store: Optional[str] = None,
               strict: bool = False):
    """Build the host app. `only` = nouns to mount (default: every lane found);
    `store` = the _WorkSpace/ExternalStore the banks resolve under.
    Also the uvicorn factory: `uvicorn --app-dir servers/_host --factory serve:create_app`."""
    from fastapi import FastAPI

    if store:
        os.environ["LOCAL_EXTERNAL_STORE"] = str(Path(store).expanduser().resolve())
    have = lanes()
    wanted = list(only) if only else have
    unknown = [n for n in wanted if n not in have]
    if unknown:
        raise SystemExit(f"no lane servers/api-{unknown[0]}/server.py; have {have}")

    mounted, failed = {}, {}
    for noun in wanted:
        try:
            mounted[noun] = load(noun)
        except Exception as e:                  # loud, and the rest keep serving
            failed[noun] = f"{type(e).__name__}: {e}"
            print(f"[haipipe-utils] lane {noun} failed to import: {failed[noun]}",
                  file=sys.stderr)
    if failed and strict:
        raise SystemExit(f"--strict: {len(failed)} lane(s) failed: {', '.join(failed)}")
    if not mounted:
        raise SystemExit("no lane imported; nothing to serve")

    @asynccontextmanager
    async def lifespan(app):
        # Starlette does not run a mounted app's startup handlers, and food's
        # warm-up (open the bank, build its FTS cursor) lives in one. Run them.
        for mod in mounted.values():
            for handler in list(getattr(mod.app.router, "on_startup", [])):
                r = handler()
                if inspect.isawaitable(r):
                    await r
        yield
        for mod in mounted.values():
            for handler in list(getattr(mod.app.router, "on_shutdown", [])):
                r = handler()
                if inspect.isawaitable(r):
                    await r

    app = FastAPI(title="haipipe-utils", version=VERSION, lifespan=lifespan,
                  description="Normalizer APIs: free text in a cohort's dialect -> "
                              "a reference bank -> numbers with provenance. "
                              "One prefix per noun.")
    for noun, mod in mounted.items():
        app.mount(f"/{noun}", mod.app, name=noun)

    @app.get("/")
    def index():
        return {"service": "haipipe-utils", "version": VERSION,
                "lanes": {noun: {"prefix": f"/{noun}", "title": mod.app.title,
                                 "version": mod.app.version, "url_var": url_var(noun),
                                 "routes": _routes(mod.app), "docs": f"/{noun}/docs"}
                          for noun, mod in mounted.items()},
                "failed": failed}

    @app.get("/healthz")
    def healthz():
        per = {noun: _lane_health(mod) for noun, mod in mounted.items()}
        ok = not failed and all(v.get("ok") for v in per.values())
        return {"status": "ok" if ok else "degraded", "version": VERSION,
                "store": os.environ.get("LOCAL_EXTERNAL_STORE"),
                "lanes": per, "failed": failed}

    app.state.mounted = mounted
    app.state.failed = failed
    return app


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description="haipipe-utils API host: every normalizer "
                                             "behind one port, one prefix per noun.")
    ap.add_argument("--host", default=DEFAULT_HOST)
    ap.add_argument("--port", type=int, default=DEFAULT_PORT)
    ap.add_argument("--store", default=None,
                    help="the _WorkSpace/ExternalStore the banks live under (sets LOCAL_EXTERNAL_STORE)")
    ap.add_argument("--only", default=None,
                    help="comma-separated nouns to mount, e.g. food,insulin (default: every servers/api-*)")
    ap.add_argument("--strict", action="store_true",
                    help="exit non-zero if any lane fails to import")
    ap.add_argument("--list", action="store_true",
                    help="print the lanes that would mount and exit, importing nothing")
    a = ap.parse_args(argv)

    if a.list:
        for noun in lanes():
            print(f"{noun:11s} /{noun:<11s} servers/api-{noun}/server.py  <- "
                  f"skills/describe-{noun}/{package_of(noun)}/")
        return 0

    only = [s.strip() for s in a.only.split(",") if s.strip()] if a.only else None
    app = create_app(only=only, store=a.store, strict=a.strict)

    import uvicorn
    base = f"http://{a.host}:{a.port}"
    print(f"haipipe-utils {VERSION} · {base}   (index: /   health: /healthz)")
    print(f"  store       {os.environ.get('LOCAL_EXTERNAL_STORE') or '<lane defaults>'}")
    for noun in app.state.mounted:
        print(f"  {noun:11s} {base}/{noun:<11s} {url_var(noun)}={base}/{noun}")
    for noun, err in app.state.failed.items():
        print(f"  {noun:11s} FAILED  {err}")
    uvicorn.run(app, host=a.host, port=a.port, log_level="info")
    return 0


if __name__ == "__main__":
    sys.exit(main())
