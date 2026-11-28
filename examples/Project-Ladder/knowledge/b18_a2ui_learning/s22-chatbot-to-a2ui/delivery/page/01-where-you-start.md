# Where you start

A chatbot today: your instructions and tools go into the prompt, the model answers in text, your server passes the
text to the app, and the app shows a chat bubble. None of that is thrown away. Six steps add an interface beside the
text. Steps 1 to 4 are on your server, 5 and 6 in your app.

![Resource 5 · Quickstart: where each part lives in Travel A2UI](../../../s01-official-sources/assets/resource-5.png)

The tools come in three kinds (Resource 6, README; and the official SDK page):

| Kind | What it does | Packages |
|---|---|---|
| Agent SDK | turns the catalog into a skill, compiles the model's output | Python `a2ui-agent-sdk`; TypeScript `@a2ui/agent`; Dart `a2ui_agent` |
| Renderer SDK | draws the surface with native widgets | `@a2ui/react`, `@a2ui/lit`, `@a2ui/angular`, `a2ui_flutter`, SwiftUI, Jetpack Compose |
| Core SDK | the protocol, used inside both | `a2ui-core`, `@a2ui/web_core`, `a2ui_core` |
