# 3. Compile the model's output

**Change:** the model's answer passes through the SDK before it goes out.
**Tool:** the Agent SDK's generator and parser (`A2uiGenerator`, Express by default). Streaming: `open_stream`
(Python) or `openStream` (TypeScript); one-shot: `parse_response` / `parseResponse`. It splits the chat text from the
`<a2ui>` block, parses each statement as it completes, checks it against the catalog and the surface, and emits JSON
messages. Invalid output is not sent; it can be returned to the model to fix (see s41, s42).
**In Travel A2UI:** `apps/server/src/travel_a2ui/brain/catalog.py`.
