# 3. Compile the model's output

**The model's answer goes through the SDK before it leaves your server.**

- ✏️ **Change:** pass the answer to the SDK instead of straight to the app.
- 🧰 **Tool:** `A2uiGenerator` (Express by default); streaming `open_stream` / `openStream`, one-shot `parse_response` / `parseResponse`.
- 🔀 It splits the chat text from the `<a2ui>` block.
- ✅ It checks each statement against the catalog, then emits JSON messages.
- ⚠️ Invalid output is not sent; it can go back to the model to fix (s41, s42).
- 📂 **In Travel A2UI:** `apps/server/src/travel_a2ui/brain/catalog.py`

✅ **You know it when:** you can say what reaches the app when the model makes a mistake.
