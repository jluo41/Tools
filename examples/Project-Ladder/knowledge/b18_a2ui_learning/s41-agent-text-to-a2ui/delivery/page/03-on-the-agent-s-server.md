# On the agent's server

1. **A component catalog.** `catalog.json` lists the components and functions the app allows. It is the guardrail:
   the agent cannot use a component the app lacks.
2. **A skill for the model.** The Agent SDK turns the catalog into prompt instructions and grammar rules; your agent
   adds them to the model's prompt.
3. **A compiler.** The model's interface output goes to the SDK's compiler, which checks it against the catalog.
4. **A transport.** The checked messages (`updateComponents`, `updateDataModel`) travel over AG-UI, A2A, MCP or a
   WebSocket.

Your agent code and model calls stay; the official diagram marks them "Outside the SDK".
