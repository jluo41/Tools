# On the agent's server

**Four things are added; your agent code stays.**

- 📋 **A catalog:** `catalog.json` lists the components the app allows; the agent cannot use one the app lacks.
- 🧠 **A skill:** the Agent SDK turns the catalog into prompt instructions and grammar rules, added to the model's prompt.
- ✅ **A compiler:** the model's interface output goes to the SDK, which checks it against the catalog.
- 📤 **A transport:** the checked messages (`updateComponents`, `updateDataModel`) go over AG-UI, A2A, MCP or a WebSocket.
- ♻️ **Unchanged:** your agent code and model calls; the official diagram marks them "Outside the SDK".
