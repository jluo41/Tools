---
mindmap: 1
title: From a Text Chatbot to A2UI, Step by Step
written: yes
---

# From a Text Chatbot to A2UI, Step by Step

- On your server <!-- branch-0 -->
  - 1 Catalog: Basic Catalog, or catalog.json <!-- node-0-0 -->
  - 2 Skill: SkillGenerator, added to the prompt <!-- node-0-1 -->
  - 3 Compile: A2uiGenerator, open_stream <!-- node-0-2 -->
  - 4 Send: a2ui-a2a, a2ui-adk, AG-UI, MCP <!-- node-0-3 -->
- In your app <!-- branch-1 -->
  - 5 Render: @a2ui/react, a2ui_flutter, SwiftUI, Compose <!-- node-1-0 -->
  - 6 Actions: action back to the agent <!-- node-1-1 -->
- Stays the same <!-- branch-2 -->
  - Your instructions and tools <!-- node-2-0 -->
  - The model and the chat text <!-- node-2-1 -->
- Packages <!-- branch-3 -->
  - Agent SDK: a2ui-agent-sdk, @a2ui/agent, a2ui_agent <!-- node-3-0 -->
  - Renderer SDK: @a2ui/react and others <!-- node-3-1 -->
  - Core SDK: a2ui-core, @a2ui/web_core <!-- node-3-2 -->
