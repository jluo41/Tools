# If My Agent Only Returns Text, What Changes?

## The question

> "suppose I have the agent, only return the text, to use A2UI, do I need to chagne anything?" (2026-11-27)

## Short answer

Yes, on both sides. The agent learns to describe an interface and sends it as A2UI messages; the app hosts a renderer
that draws it. The text answer can stay: in the official flight example the agent still writes "Here are direct
flights", and the two flight cards appear under it.

![Resource 1 · Architecture](../../s01-official-sources/assets/resource-1.png)

## On the agent's server

1. **A component catalog.** `catalog.json` lists the components and functions the app allows. It is the guardrail:
   the agent cannot use a component the app lacks.
2. **A skill for the model.** The Agent SDK turns the catalog into prompt instructions and grammar rules; your agent
   adds them to the model's prompt.
3. **A compiler.** The model's interface output goes to the SDK's compiler, which checks it against the catalog.
4. **A transport.** The checked messages (`updateComponents`, `updateDataModel`) travel over AG-UI, A2A, MCP or a
   WebSocket.

Your agent code and model calls stay; the official diagram marks them "Outside the SDK".

## In your app

1. **A renderer** for your platform: Flutter, Web (React, Lit, Angular), SwiftUI or Compose.
2. **A surface**: one region of the screen the renderer draws. Navigation and chat stay your own code.
3. **Actions back**: a tap on a button sends an `action` message to the agent. Editing a bound value, such as the
   passenger count, changes only the local data model and sends nothing.

## The smallest first step

Send fixed A2UI messages from the server, a static payload, before teaching the model anything. That is what the
practice Job j01 does with one card. Then add the catalog and the SDK, then handle actions. Resource 5 (Travel A2UI)
shows all three steps in one small app.

## Follow-up: does the agent now return JSON?

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

## Follow-up: streaming, and broken output

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

## Try explaining

Point to the two boxes in the Resource 1 diagram that your agent did not have before, and say what each one does
with the model's output.
