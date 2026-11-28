# From a Text Chatbot to A2UI, Step by Step

## Where you start

A chatbot today: your instructions and tools go into the prompt, the model answers in text, your server passes the
text to the app, and the app shows a chat bubble. None of that is thrown away. Six steps add an interface beside the
text. Steps 1 to 4 are on your server, 5 and 6 in your app.

![Resource 5 · Quickstart: where each part lives in Travel A2UI](../../s01-official-sources/assets/resource-5.png)

The tools come in three kinds (Resource 6, README; and the official SDK page):

| Kind | What it does | Packages |
|---|---|---|
| Agent SDK | turns the catalog into a skill, compiles the model's output | Python `a2ui-agent-sdk`; TypeScript `@a2ui/agent`; Dart `a2ui_agent` |
| Renderer SDK | draws the surface with native widgets | `@a2ui/react`, `@a2ui/lit`, `@a2ui/angular`, `a2ui_flutter`, SwiftUI, Jetpack Compose |
| Core SDK | the protocol, used inside both | `a2ui-core`, `@a2ui/web_core`, `a2ui_core` |

## 1. Choose the catalog

**Change:** decide which components the agent may draw.
**Tool:** the Basic Catalog, built into every official renderer: `Text`, `Row`, `Column`, `List`, `Button`,
`TextField` and more. Start with it; write your own `catalog.json` only when you need a component it lacks.
**In Travel A2UI:** `catalogs/a2ui-travel/catalog.json` adds `FlightOption`, `HotelCard`, `DateRangePicker` and
`PriceSummary` to the basic ones. The catalog is the guardrail: the agent can only ask for what the app can draw.

## 2. Generate the skill and add it to the prompt

**Change:** your prompt gets one more part.
**Tool:** the Agent SDK's skill generator (`SkillGenerator`; inside the SDK, `PromptGenerator`). It reads the catalog
and writes a Markdown skill: the Express grammar and one signature per component, such as
`FlightOption(airline, departTime, arriveTime, origin, destination, price, action, ...)`.
**In Travel A2UI:** `scripts/build_skills.py` writes `skills/` (`a2ui-core` teaches the notation, `a2ui-travel` this
catalog). Rerun it when the catalog changes.
Your own instructions and tools, for example a flight search, stay as they are.

## 3. Compile the model's output

**Change:** the model's answer passes through the SDK before it goes out.
**Tool:** the Agent SDK's generator and parser (`A2uiGenerator`, Express by default). Streaming: `open_stream`
(Python) or `openStream` (TypeScript); one-shot: `parse_response` / `parseResponse`. It splits the chat text from the
`<a2ui>` block, parses each statement as it completes, checks it against the catalog and the surface, and emits JSON
messages. Invalid output is not sent; it can be returned to the model to fix (see s41, s42).
**In Travel A2UI:** `apps/server/src/travel_a2ui/brain/catalog.py`.

## 4. Send the messages

**Change:** the JSON messages travel to the app beside the text.
**Tool:** your existing channel, or an official integration: `a2ui-a2a` (A2A protocol), `a2ui-adk` (Google ADK), AG-UI,
MCP or a WebSocket.
**In Travel A2UI:** server-sent events.

## 5. Render in the app

**Change:** the app hosts a renderer in one region of the screen, the surface. Navigation and chat stay your code.
**Tool:** a Renderer SDK: `@a2ui/react`, `@a2ui/lit`, `@a2ui/angular`, `a2ui_flutter`, SwiftUI or Jetpack Compose.
It applies `createSurface`, `updateComponents` and `updateDataModel` and keeps bound values live.
**In Travel A2UI:** `renderers/react/` and `renderers/flutter/`, used by `apps/web/` and `apps/flutter/`.

## 6. Handle actions

**Change:** a tap on a button reaches your agent.
**Tool:** the renderer sends an `action` message (for example `confirm_booking` with the passenger counts); your server
hands it to the agent, which answers with new text and, if needed, new messages. Local edits, such as changing the
passenger count, need nothing from the agent.
**In Travel A2UI:** the agent in `apps/server/src/travel_a2ui/brain/` receives the event.

## Try explaining

Name the steps your chatbot already has (the prompt, the model call, a channel to the app). Then name the three A2UI
packages you would add, one for the server and two for a React app, and say which step each one serves.
