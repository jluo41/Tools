# Follow-up: does the agent now return JSON?

> "for this, previous, agent only return text, now you wwant agent to return json, right? this will be the changes, right? and we need to add the skill of A2UI to our chatbot?" (2026-11-27)

**The model still returns text.** Its answer has two parts: the chat text, as before, and a block between `<a2ui>` and
`</a2ui>` written in A2UI Express (`root = Card(Column([FlightCard(...), Button(...)]))`). The model may write the JSON
directly instead, but it does not have to.

**Your server turns the block into JSON.** The SDK's compiler checks the block against `catalog.json` and emits the
JSON messages (`createSurface`, `updateComponents`, `updateDataModel`). The chat text goes to the app as before. The
app shows the text and, under it, the flight cards.

**Yes, the chatbot gets the A2UI skill.** You do not write it: the SDK generates it from `catalog.json`. It tells the
model the Express grammar and each allowed component, for example `FlightCard(flightNumber, origin, destination,
price, passengers)`. It sits beside your own instructions and tools, which stay as they are.

| | Before | After |
|---|---|---|
| Prompt | your instructions, your tools | the same, **plus the A2UI skill** |
| The model writes | text | text **plus an `<a2ui>` block** |
| Your server | passes the text on | passes the text on **and compiles the block into JSON** |
| The app | a chat bubble | a chat bubble **and a surface drawn by the renderer** |
