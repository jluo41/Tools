# Follow-up: streaming, and broken output

> "so ideal, I need to chnage my chatbot a bit, and then return the the <a2ui> json from my chat bot, right? so it will streaming out like the next token prediction ,right? what is the json is corrupted." (2026-11-27)

**A small change; it streams token by token; broken output is not sent.**

- ✏️ **A small change:** the chatbot keeps its model, tools and conversation; it adds the skill and passes the answer through the SDK.
- 🧩 **Express by default:** if you prefer JSON, the model writes it between `<a2ui-json>` and `</a2ui-json>`.
- 🌊 **It streams:** the SDK reads the answer as it arrives (`open_stream` / `openStream`), splits the chat text from the block, and sends JSON as each statement completes.
- ⚡ **The card appears early:** Express puts `root` first.
- 🛡️ **Broken output is caught:** a missing component, a wrong property or a broken ID is reported as soon as it appears, and can go back to the model to fix.
- 🩹 **Direct JSON is repaired:** the SDK strips Markdown fences and heals half-written strings while streaming.
- 💡 **Why Express:** raw JSON, with nested braces, quotes and hand-written IDs, breaks more often, especially on small models.

| 😟 Worry | 🛡️ What the SDK does |
|---|---|
| The model writes JSON token by token | Express is shorter and breaks less; the SDK writes the JSON |
| A brace or quote is missing | Express needs few; for Direct JSON the SDK repairs strings as they stream |
| A component or property is wrong | checked against the catalog, reported as soon as it appears |
| The output is invalid | not sent to the app; returned to the model to fix |
