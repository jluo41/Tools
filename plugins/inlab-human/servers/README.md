# servers/ · inlab-human

Browser-served code of the inlab-human plugin. It sits beside `skills/`, `agents/`
and `mcp-servers/` and never inside a skill; the skills stay Markdown contracts.

```text
plugins/inlab-human/servers/
└── haichat-inlab/        🩺 the HAI-Chat In-Lab Console — its own FastAPI host on :8091
    ├── main.py           one app: five APIRouters + the built SPA at /
    ├── console_api.py    patients · models · predict · datasets (engine-backed)
    ├── labeling_api.py   cases + the subjective-label PI inbox
    ├── tasks_api.py      the haipipe task feed
    ├── message_api.py    compose → judge → feedback after a prediction
    ├── haichat_api.py    WS /ws/haichat — Claude Agent SDK + engine-as-MCP
    ├── web/              React + Vite SPA (Console.tsx, useConsole.ts, views.ts …)
    ├── diagram/          the design set, 00-index.txt first
    └── Dockerfile        built by HAIChat-SPACE's docker-compose.yml
```

Two rules, both inherited from the console's own design notes:

1. **One engine.** Every score comes from `../mcp-servers/endpoint-predict/server.py`,
   imported as a library by the buttons and mounted as an MCP server for the agent.
   `console_api._resolve_engine()` finds it as the plugin sibling first.
2. **Nothing study-specific is committed.** Patients, endpoints, label stores and
   projects are mounted by `INLAB_*` environment variables; see `haichat-inlab/README.md`.

This console is a standalone host, not a `workbench-*` tab of the haipipe-toolkit Board
server. HAIChat-SPACE embeds it as a per-thread iframe and builds it from
`Tools/plugins/inlab-human/servers/haichat-inlab` through its `Tools` submodule.

Run it here:

```bash
cd plugins/inlab-human/servers/haichat-inlab
uv run --python 3.11 --with fastapi --with 'uvicorn[standard]' uvicorn main:app --port 8091
# SPA: cd web && npm install && npm run build   (FastAPI then serves it at /)
```
