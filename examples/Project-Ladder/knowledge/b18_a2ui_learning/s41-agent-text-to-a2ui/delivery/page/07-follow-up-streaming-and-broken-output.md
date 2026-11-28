# Follow-up: streaming, and broken output

> "so ideal, I need to chnage my chatbot a bit, and then return the the <a2ui> json from my chat bot, right? so it will streaming out like the next token prediction ,right? what is the json is corrupted." (2026-11-27)

**A small change, yes.** The chatbot keeps its model, tools and conversation; it adds the A2UI skill to the prompt and
passes the model's answer through the Agent SDK. The model writes the `<a2ui>` block; by default it is A2UI Express,
not JSON. If you prefer JSON, the model can write it between `<a2ui-json>` and `</a2ui-json>` instead.

**It streams, token by token.** The SDK reads the answer as it arrives (`open_stream` in Python, `openStream` in
TypeScript). It separates the chat text from the `<a2ui>` block and sends JSON pieces as each statement is complete.
Express puts `root` first, so the card can appear before the model has finished writing it.

**If the output is broken, it is not sent.** The SDK checks every message against the catalog and the current surface:
a component the catalog lacks, a wrong property or a broken component ID is caught as soon as it appears. The error can
be returned to the model so it corrects itself. For Direct JSON, the SDK also strips Markdown fences and repairs
half-written strings while streaming. Express exists partly for this reason: the official docs note that raw JSON,
with its nested braces, quotes and hand-written IDs, causes more syntax errors, especially on smaller models.

| Worry | What the SDK does |
|---|---|
| The model writes JSON token by token | Express is shorter and simpler, so it breaks less; the SDK writes the JSON |
| A brace or quote is missing | Express needs few; for Direct JSON the SDK repairs strings as they stream |
| A component or property is wrong | Checked against the catalog; reported as soon as it appears |
| The output is invalid | Not sent to the app; returned to the model to fix |
