---
mindmap: 1
title: If My Agent Only Returns Text, What Changes?
written: yes
---

# If My Agent Only Returns Text, What Changes?

- On the agent's server <!-- branch-0 -->
  - Component catalog: catalog.json <!-- node-0-0 -->
  - Skill for the model, from the SDK <!-- node-0-1 -->
  - Compiler checks the output <!-- node-0-2 -->
  - Transport: AG-UI, A2A, MCP, WebSocket <!-- node-0-3 -->
- In your app <!-- branch-1 -->
  - A renderer for your platform <!-- node-1-0 -->
  - One surface on the screen <!-- node-1-1 -->
  - Actions go back to the agent <!-- node-1-2 -->
- What stays <!-- branch-2 -->
  - The text answer <!-- node-2-0 -->
  - Your agent code and model calls <!-- node-2-1 -->
- First step <!-- branch-3 -->
  - Fixed messages, no model (j01) <!-- node-3-0 -->
