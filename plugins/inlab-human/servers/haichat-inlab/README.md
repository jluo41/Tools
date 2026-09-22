# haichat-inlab — In-Lab Clinical Model Console

Lives at `plugins/inlab-human/servers/haichat-inlab/`, beside the plugin's
`mcp-servers/endpoint-predict/` engine that it imports. HAIChat-SPACE builds and
runs it through its `Tools` submodule (`docker compose up haichat-inlab`).

A clinician-facing console over a **prediction endpoint**: pick a patient, read their
record, pick a model, get the score. Served as a single page so HAI-Chat can render it
as a **per-thread iframe embed** — the console sits beside the conversation, and the
conversation is Mattermost.

```
┌──────────────┬───────────────────────────────┬───────────────┐
│ 👥 Patients  │  🗂️ Raw record                 │  🧠 Models    │
│ 📋 Chart     │  every table / column / row    │  ▶ Run        │
│  (as of the  │  ⚠️ rows the model never saw   │  score card   │
│   index date)│     (they postdate the score)  │  + data gaps  │
└──────────────┴───────────────────────────────┴───────────────┘
```

**The score always comes from the endpoint, verbatim.** Nothing in this service
computes, estimates, or adjusts a risk score. The ▶ Run button is a plain HTTP
POST to the model's endpoint — no LLM, no credentials.

**HaiChat** (standalone mode only) is the agent path beside it: a Genie-style
right drawer over `/ws/haichat`, backed by the Claude Agent SDK (local Claude
Code login — subscription, never a pay-per-token API key) with the SAME
endpoint-predict engine mounted as MCP. Every tool call blocks on the
clinician's Allow/Deny in the drawer. Embedded in a HAI-Chat thread the drawer
is hidden — there, Mattermost is the chat and haichat-me-agent is the agent.

## Boundaries

| Concern | Where it lives |
|---|---|
| Prediction logic (payload build, trigger pick, gap report) | the **inlab-human engine** — `../../mcp-servers/endpoint-predict/server.py` (this plugin's own), imported, never reimplemented |
| The console UI + REST | **here** |
| The chat, and the agent that narrates a score | **Mattermost + `haichat-ai/haichat-me-agent`** (openclaw reads the same `inlab-human` skills) |
| Patients, endpoints, cohorts | **the study repo** — injected by env, never baked in |

The engine is shared with the agent on purpose: the buttons and the assistant must
reach the endpoint through the *same code*, or the demo is a lie.

## Configure

Nothing study-specific is committed here. The service is inert until you point it
at a cohort:

| Env | Meaning |
|---|---|
| `INLAB_PATIENT_STORE` | directory of `<patient_id>.json` records |
| `INLAB_ENDPOINT_STORE` | directory of packaged endpoints (a `6-EndpointStore`) |
| `INLAB_REGISTRY` | JSON map `{"<package>": "http://host:port"}` |
| `INLAB_ENGINE` | *(optional)* path to the `endpoint-predict` dir. Unset ⇒ the plugin sibling `../../mcp-servers/endpoint-predict`, else walk up looking for `Tools/plugins/inlab-human/…` |
| `INLAB_LABEL_STORE` | *(optional)* dir of subjective-label dimension folders (a project's `tasks/`). Lights up the 📌 Case and ✏️ Annotate views |

`GET /api/health` reports the resolved config and which endpoints are live.

## Run

```bash
# dev — API on :8091, SPA on :5174 (proxies /api)
cd web && npm install && npm run dev &
INLAB_PATIENT_STORE=… INLAB_ENDPOINT_STORE=… INLAB_REGISTRY=… \
    uvicorn main:app --port 8091

# or one process: build the SPA, FastAPI serves it at /
cd web && npm install && npm run build && cd ..
INLAB_… uvicorn main:app --port 8091      # → http://127.0.0.1:8091
```

Docker (`docker compose up haichat-inlab`) mounts the engine and the stores rather
than copying them into the image — patient data must never enter a container image.

## API

| Route | Returns |
|---|---|
| `GET /api/patients` | roster |
| `GET /api/patients/{id}` | curated chart **as of the prediction date** (later rows withheld) |
| `GET /api/patients/{id}/raw` | every table/column/row; later rows **flagged**, not hidden |
| `GET /api/models` | packaged models + whether their endpoint answers |
| `POST /api/predict` | `{patient_id, model}` → endpoint response + data-gap report |
| `GET /api/health` | config + live endpoints |
| `GET /api/cases` | the case universe (one case = one annotation point), label history joined; `?human_id=` `?q=` |
| `GET /api/labeling/dimensions` | mounted subjective-label projects (status, κ, labels) |
| `GET /api/labeling/{dim}` | one dimension: state, guideline+versions, gallery, trajectory, the PI's inbox |
| `POST /api/labeling/{dim}/decision` | the ONE labeling write: the researcher's adjudication → `human_decisions.jsonl` |
| `WS /ws/haichat` | HaiChat agent session (Agent SDK + engine-as-MCP). Client sends `user`/`approval_response`/`interrupt`; server sends `ready`/`delta`/`assistant`/`tool_call`/`tool_result`/`approval_request`/`done`/`error` |

HaiChat extras via env: `INLAB_AGENT_MODEL` (optional model override for the
agent; default = the local Claude Code default).
