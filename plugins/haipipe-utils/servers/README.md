# servers/ · the API face of haipipe-utils

Everything reachable over HTTP lives here, and nothing here is a skill. The
folder is a sibling of `skills/`: plugin-level infrastructure that serves the
skills' normalizers as an API. A request carries the input, the response
carries the result, and nothing is rendered.

```
servers/
├── _host/                the one process: serve.py mounts every lane under one port
│   ├── serve.py          --port 8070 --store <ExternalStore> --only food,insulin --list
│   ├── run.sh            picks an interpreter with fastapi (venv, uv, python3) and runs serve.py
│   └── tests/            test_host.py (no bank needed) · run_suites.py (every lane's suite)
├── api-food/             /food        server.py · tests/test_server.py · examples/
├── api-exercise/         /exercise    server.py · tests/test_server.py · examples/
├── api-medication/       /medication  server.py · tests/test_server.py · examples/ (both halves of the insulin chain)
└── api-insulin/          /insulin     server.py · tests/test_server.py
skills/describe-<noun>/   the resolver: <noun>norm/ (client.py, dialect, retrieve, aggregate), pipeline.py, benchmark/
```

## Two words, two things

A **skill** (`skills/describe-<noun>/`) is the resolver and its contract: the
`<noun>norm` package, its `client.py` door (`normalize()` with the `local` |
`http` transport switch), its regression suite and its benchmark. An **api
lane** (`servers/api-<noun>/`) is that skill's face on the wire: the FastAPI app
that exposes `normalize()` over HTTP, the black-box service suite that drives it,
and the recorded request/response examples. `describe-food` ↔ `api-food`.

## The API

Every lane answers the same three routes under its prefix:

| route | body | answer |
|---|---|---|
| `GET /<noun>/healthz` | none | the bank it is actually serving, so a caller knows which corpus answered |
| `POST /<noun>/normalize` | one item, e.g. `{"item": "Novolin R"}` | one record with its provenance columns |
| `POST /<noun>/normalize/batch` | a list, in input order | `{"results": [...], ...}` one record per input, order held, misses as `null` |

The host adds `GET /` (the lanes, their routes, their `<NOUN>NORM_URL` names)
and `GET /healthz` (every lane's health in one answer, `status: ok | degraded`).
Each lane's interactive docs sit at `/<noun>/docs`. Food also has
`POST /food/normalize/image` (multipart frames) and `/food/normalize/image/batch`.

```
python servers/_host/serve.py --store /path/to/_WorkSpace/ExternalStore
curl -s localhost:8070/healthz
curl -s localhost:8070/food/normalize -H 'content-type: application/json' -d '{"food":"fried rice; egg"}'
curl -s localhost:8070/exercise/normalize -H 'content-type: application/json' -d '{"activity":"Walking","minutes":30,"weight_kg":82}'
curl -s localhost:8070/medication/normalize -H 'content-type: application/json' -d '{"item":"612997","dose":39}'
curl -s localhost:8070/insulin/normalize -H 'content-type: application/json' -d '{"item":"Insulin lispro-aabc"}'
```

A consumer that used a lane's old standalone port keeps working after one
change: `FOODNORM_URL=http://127.0.0.1:8070/food` where it said `:8077`
(exercise `:8078` → `/exercise`, medication `:8079` → `/medication`, insulin
`:8080` → `/insulin`). The client appends `/normalize/batch` as before.

## Banks

A lane finds its reference bank from an explicit variable (`FOODNORM_DB`,
`EXNORM_DB`, `MEDNORM_DB`, `INSNORM_LEXICON`) or from `$LOCAL_EXTERNAL_STORE`,
which `--store` sets before any lane imports. Insulin carries its PK table in
the package and needs no store. A lane whose bank is missing still mounts and
reports `degraded` on its `/healthz`; a lane that fails to import is listed
under `failed` on the host `/healthz` and the rest keep serving (`--strict`
turns that into a non-zero exit).

## Testing

| Want | Run |
|---|---|
| Host wiring, no bank needed | `python servers/_host/tests/test_host.py` |
| Every lane's service suite against a live host | `python servers/_host/tests/run_suites.py --store <ExternalStore>` |
| One lane's suite against any URL | `INSNORM_URL=http://127.0.0.1:8070/insulin python servers/api-insulin/tests/test_server.py` |
| Regenerate a lane's examples | `python servers/api-<noun>/examples/run_examples.py` (against `<NOUN>NORM_URL`) |

The suites are black-box: they only POST to a URL, so they prove the wire, and
they run unchanged against a lane served standalone
(`uvicorn server:app --app-dir servers/api-insulin`, with
`skills/describe-insulin` on `PYTHONPATH`).

No system Python here has fastapi; `run.sh` falls back to `uv run --with fastapi …`.

## Rules

1. **Arrow one way.** Lanes import the skills' `<noun>norm` packages. Skills
   import nothing from here; their `client.py` only knows a URL.
2. **Routes are the contract.** `/healthz`, `/normalize`, `/normalize/batch`
   did not change in the move; only the prefix was added. Response envelopes
   stay as each lane had them (`results` plus `n` for food, `results` plus
   `count` for the others); every client reads `results`.
3. **A lane owns its files.** Server, suite and examples for one noun sit in
   one folder. Adding a noun is adding `servers/api-<noun>/server.py`; the host
   discovers it.
